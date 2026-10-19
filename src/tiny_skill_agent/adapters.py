"""Small LangChain and LangGraph adapters for the assessment API."""

import json
import re
from collections.abc import Callable, Iterable, Mapping
from typing import Any, Literal
from pydantic import Field, create_model

from langchain_core.messages import ToolMessage

from .assessment import (
    ASSESSMENT_PROMPT, AssessmentConfig, AssessmentInputs, AssessmentModel,
    CoverageDraft, Criterion, Evidence, NoMatchReviewDraft, NO_MATCH_REVIEW_PROMPT, assess,
    PredicateDraft, PREDICATE_PROMPT, DECISION_REVIEW_PROMPT,
    ConsistencyDraft, CONSISTENCY_REVIEW_PROMPT,
    GroundedNoMatchReviewDraft,
)
from .evidence import (
    SOURCE_KINDS, build_criterion_inventory, build_fact_spans,
    build_source_catalog, collect_evidence,
)
from .criteria import (CriterionExtraction, CriterionExtractor, SourceReview,
                       SourceLineDecision, CriterionQuote, SOURCE_REVIEW_PROMPT)


def inputs_from_messages(
    messages: Iterable[Any], tools: Iterable[Any], *,
    system_prompt: str | None = None,
    labels: tuple[str, ...] = ("strength", "concern"),
    allowed_source_kinds: Iterable[str] = SOURCE_KINDS,
    allowed_source_ids: Iterable[str] | None = None,
    source_scope_ids: Iterable[str] | None = None,
    criterion_extractor: CriterionExtractor | None = None,
    extraction_max_retries: int = 1,
) -> AssessmentInputs:
    """Convert observed tagged tool messages to portable criteria/evidence records.

    Use EvidenceMetadataMiddleware when executing the tools. Pass the actual
    system prompt used for this run; dynamic prompts are not reconstructed.
    Multimodal/block content requires caller extraction before this adapter.
    """
    if not isinstance(extraction_max_retries, int) or extraction_max_retries < 0:
        raise ValueError("extraction_max_retries must be a nonnegative integer")
    messages, tools = list(messages), list(tools)
    evidence_tools = {tool.name for tool in tools if (tool.metadata or {}).get("_meta", {}).get("kind") in {"directive", "data"}}
    if any(isinstance(message, ToolMessage) and message.status == "success"
           and message.name in evidence_tools and not isinstance(message.content, str) for message in messages):
        raise ValueError("Extract block/multimodal tool content to text or explicit Evidence records first")
    ledger = collect_evidence(messages, tools, system_prompt=system_prompt)
    # Scope the ledger before catalog deduplication: identical content belonging
    # to different cases must not hide the active case's source.
    if source_scope_ids is not None:
        selected = set(source_scope_ids)
        observed = set(ledger.directive_sources) | set(ledger.fact_sources)
        if missing := selected - observed:
            raise ValueError(f"Case scope sources have not been observed: {sorted(missing)}")
        ledger.directive_sources = {k: v for k, v in ledger.directive_sources.items() if k in selected}
        ledger.fact_sources = {k: v for k, v in ledger.fact_sources.items() if k in selected}
        ledger.source_kinds = {k: v for k, v in ledger.source_kinds.items() if k in selected}
        ledger.tool_evidence = [e for e in ledger.tool_evidence if e["source_id"] in selected]
    catalog = build_source_catalog(ledger)
    allowed_source_kinds = set(allowed_source_kinds)
    allowed_source_ids = None if allowed_source_ids is None else set(allowed_source_ids)
    inventory = build_criterion_inventory(
        catalog, labels=labels, allowed_source_kinds=allowed_source_kinds,
        allowed_source_ids=allowed_source_ids,
    )
    criteria = []
    for key, entry in inventory.items():
        source = catalog.entries[entry["criterion_source_id"]]
        criteria.append(Criterion(
            id=key, text=entry["criterion"], source_id=source["source_id"],
            source_label=source["label"],
            classification=entry["criterion"].split("]", 1)[0][1:],
            context="\n".join(source["directive_lines"]),
        ))
    if criterion_extractor is not None:
        for source in catalog.entries.values():
            if "directive_lines" not in source or source["source_kind"] not in allowed_source_kinds:
                continue
            if allowed_source_ids is not None and source["source_id"] not in allowed_source_ids:
                continue
            text = "\n".join(source["directive_lines"])
            known = {c.text: c.classification for c in criteria if c.source_id == source["source_id"]}
            # Known labelled lines already have deterministic coverage.
            lines = {f"L{i}": line for i, line in enumerate(source["directive_lines"], 1) if line.strip() and line not in known}
            if not lines:
                continue
            payload = {"stage": "criterion_extraction", "source_id": source["source_id"],
                       "text": text, "labels": list(labels), "known_criteria": known, "source_lines": lines}
            for attempt in range(extraction_max_retries + 1):
                try:
                    extracted = CriterionExtraction.model_validate(criterion_extractor(payload))
                    if not extracted.complete or extracted.issues:
                        # Declared semantic ambiguity is not a schema-repair request.
                        raise RuntimeError(f"Incomplete criterion extraction for {source['source_id']}: {extracted.issues}")
                    additions = _validated_extraction(extracted, lines=lines, known=known, text=text,
                        labels=labels, source=source, start_id=len(criteria) + 1)
                    criteria.extend(additions)
                    break
                except RuntimeError as exc:
                    raise ValueError(str(exc)) from exc
                except ValueError as exc:
                    if attempt == extraction_max_retries:
                        raise
                    payload = {**payload, "validation_feedback": str(exc)}
    evidence = []
    for key, span in build_fact_spans(catalog).items():
        source = catalog.entries[span["source_id"]]
        evidence.append(Evidence(
            id=key, source_id=source["source_id"], source_label=source["label"],
            locator=span["locator"], quote=span["quote"], context=span["context"],
        ))
    return AssessmentInputs(criteria=criteria, evidence=evidence)


def _validated_extraction(extracted, *, lines, known, text, labels, source, start_id):
    known = dict(known)
    new_criteria = []
    reviewed = {r.line_id: r for r in extracted.reviewed_lines}
    if len(reviewed) != len(extracted.reviewed_lines) or set(reviewed) != set(lines):
        raise ValueError("Criterion extraction must review every source line exactly once")
    all_quotes = set(known) | {r.quote for r in extracted.criteria}
    covered = set(known)
    for lid, review in reviewed.items():
        for quote in review.rule_quotes:
            if quote not in all_quotes or not (quote in lines[lid] or lines[lid] in quote):
                raise ValueError("Line review must link to an extracted rule covering that source line")
            covered.add(quote)
    if not all_quotes <= covered:
        raise ValueError("Every extracted rule must be covered by a source line review")
    for row in extracted.criteria:
        if not row.quote.strip() or row.quote not in text:
            raise ValueError("Extracted criterion must be an exact nonempty source quotation")
        if row.classification not in labels:
            raise ValueError("Extracted criterion uses an unapproved classification")
        names_label = lambda quote: re.search(r"(?<!\w)" + re.escape(row.classification) + r"(?!\w)", quote, re.IGNORECASE) is not None
        mapping = "" if names_label(row.quote) else row.classification_quote
        if mapping and (mapping not in text or not names_label(mapping)):
            raise ValueError("Classification mapping must be an exact source quote naming the classification. First check whether this is actually a new outcome criterion: definitions, counting instructions and advice about interpreting evidence remain context, with rule_quotes=[], rather than new classified criteria. Do not invent a mapping for operational guidance.")
        if not names_label(row.quote) and not mapping:
            raise ValueError(f"Candidate {row.quote!r} does not contain the label {row.classification!r}. If this is a definition, counting instruction or advice about interpreting evidence, remove it from criteria and set its line's rule_quotes=[]; it remains source context. Only a substantive outcome criterion needs classification_quote as the exact source sentence defining that outcome's label. Never invent a mapping. If a substantive criterion has no mapping, declare incomplete.")
        if row.quote in known:
            if known[row.quote] != row.classification:
                raise ValueError("Extraction reclassifies an existing criterion")
            continue
        if any(row.quote in existing or existing in row.quote for existing in known):
            raise ValueError("Extracted criterion overlaps an already extracted rule; preserve atomic rules and their classifications")
        known[row.quote] = row.classification
        new_criteria.append(Criterion(
            id=f"C{start_id + len(new_criteria)}", text=row.quote,
            source_id=source["source_id"], source_label=source["label"],
            classification=row.classification, context=text, classification_quote=mapping,
        ))
    return new_criteria


def make_langchain_criterion_extractor(model: Any, *, method: str | None = None) -> CriterionExtractor:
    """One optional structured call per permitted directive source; no hidden retries."""
    options = {"method": method} if method is not None else {}
    def invoke(payload):
        # Review the entire document, including already-known outcomes. Asking
        # for only leftovers biases extraction toward inventing extra criteria.
        lines = {f"L{i}": line for i, line in enumerate(payload.get("text", "").splitlines(), 1)
                 if line.strip()}
        provider_payload = {**payload, "source_lines": lines}
        labels = tuple(payload.get("labels", ()))
        quote_schema = create_model("ClassifiedSourceQuote", __base__=CriterionQuote,
            classification=(Literal[labels], Field(description="One supplied outcome label."))) if labels else CriterionQuote
        line_schema = create_model("SourceLineDisposition", __base__=SourceLineDecision,
            criteria=(list[quote_schema], SourceLineDecision.model_fields["criteria"]))
        # Required object keys prevent skipped/duplicate lines; a runtime enum
        # prevents invented labels. These remain checked after generation too.
        line_map = create_model("SourceLineMap", __config__={"extra": "forbid"},
            **{key: (line_schema, ...) for key in lines})
        schema = create_model("SourceCriterionReview", __base__=SourceReview,
            lines=(line_map, Field(description="Review every supplied line key, including context.")))
        structured = model.with_structured_output(schema, include_raw=True, **options)
        response = structured.invoke([
            ("system", SOURCE_REVIEW_PROMPT),
            ("human", json.dumps(provider_payload, ensure_ascii=False)),
        ])
        metadata = getattr(response.get("raw"), "response_metadata", {}) or {}
        if any(metadata.get(key) in {"length", "max_tokens", "max_output_tokens", "output_limit"}
               for key in ("finish_reason", "done_reason", "stop_reason")):
            raise ValueError("Criterion extraction was truncated")
        if response.get("parsing_error") or response.get("parsed") is None:
            raise ValueError(f"Criterion extraction could not be parsed: {response.get('parsing_error')}")
        reviewed = schema.model_validate(response["parsed"])
        decisions = [(key, getattr(reviewed.lines, key)) for key in lines]
        issues = [f"{key}: {line.reason}" for key, line in decisions if line.role == "unresolved"]
        return CriterionExtraction(
            complete=not issues, issues=issues,
            reviewed_lines=[{"line_id": key, "rule_quotes": [c.quote for c in line.criteria]}
                            for key, line in decisions if key in payload.get("source_lines", {})],
            criteria=[c for _, line in decisions for c in line.criteria],
        )

    return invoke


def make_langchain_assessor(model: Any, *, method: str | None = None) -> AssessmentModel:
    """Wrap a chat model supporting with_structured_output as an assess callable.

    Pass method='json_schema' for the notebook's Ollama configuration. Other
    providers can use their default or an explicitly supported method. Provider
    exceptions, parsing failures, and truncation are retried/reported by assess.
    """
    options = {"method": method} if method is not None else {}
    structured = model.with_structured_output(PredicateDraft, include_raw=True, **options)

    def invoke(payload: dict[str, Any]) -> CoverageDraft | NoMatchReviewDraft | PredicateDraft:
        reviewing = payload.get("stage") == "no_match_review"
        independent = payload.get("stage") == "decision_review"
        consistency = payload.get("stage") == "consistency_review"
        schema = ConsistencyDraft if consistency else GroundedNoMatchReviewDraft if reviewing else PredicateDraft
        runnable = model.with_structured_output(schema, include_raw=True, **options) if reviewing or consistency else structured
        # Do not overload the model's applicability predicate "scope" with an
        # orchestration label such as whole_case or a source identifier.
        provider_payload = {key: value for key, value in payload.items() if key not in {"scope", "source_assessments"}}
        provider_payload["evidence_batch"] = (
            "Partial observations from one source; other sources may supply missing facts."
            if payload.get("stage") == "source" else
            "All supplied observations for this case; combine complementary sources.")
        response = runnable.invoke([
            ("system", CONSISTENCY_REVIEW_PROMPT if consistency else NO_MATCH_REVIEW_PROMPT if reviewing else DECISION_REVIEW_PROMPT if independent else PREDICATE_PROMPT),
            ("human", json.dumps(provider_payload, ensure_ascii=False)),
        ])
        raw = response.get("raw")
        metadata = getattr(raw, "response_metadata", {}) or {}
        if any(metadata.get(key) in {"length", "max_tokens", "max_output_tokens", "output_limit"}
               for key in ("finish_reason", "done_reason", "stop_reason")):
            raise ValueError("Model output was truncated")
        if response.get("parsing_error") or response.get("parsed") is None:
            raise ValueError(f"Model output could not be parsed: {response.get('parsing_error')}")
        draft = schema.model_validate(response["parsed"])
        if not reviewing and not consistency:
            for row in draft.root:
                rule = payload["criteria"].get(row.criterion_id)
                if rule is None or row.condition_quote not in rule["text"]:
                    raise ValueError("condition_quote must be an exact excerpt from the requested criterion.text")
        return draft if reviewing or independent or consistency else CoverageDraft([row.assessment() for row in draft.root])

    return invoke


def make_assessment_node(
    model: AssessmentModel, *,
    config: AssessmentConfig | Mapping[str, Any] | None = None,
    input_mapper: Callable[[Mapping[str, Any]], AssessmentInputs | Mapping[str, Any]] | None = None,
    input_key: str = "assessment_input",
    output_key: str = "assessment",
    request_key: str = "input_prompt",
) -> Callable[[Mapping[str, Any]], dict[str, Any]]:
    """Return a synchronous LangGraph node with an explicit, serializable update.

    By default state[input_key] contains AssessmentInputs or its model_dump().
    input_mapper can adapt arbitrary state, including a message history via
    inputs_from_messages. The node never mutates incoming state. LangGraph may
    run it within an async graph, but model calls inside it remain synchronous.
    Checkpointing is at the node boundary, not between individual assessments.
    """
    settings = AssessmentConfig.model_validate(config or {})
    if len({input_key, output_key, request_key}) != 3:
        raise ValueError("Input, output, and request state keys must be distinct")

    def node(state: Mapping[str, Any]) -> dict[str, Any]:
        inputs = AssessmentInputs.model_validate(
            input_mapper(state) if input_mapper is not None else state[input_key]
        )
        result = assess(
            criteria=inputs.criteria, evidence=inputs.evidence, model=model,
            config=settings, request=state.get(request_key, ""),
        )
        return {output_key: result.model_dump(mode="json")}

    return node
