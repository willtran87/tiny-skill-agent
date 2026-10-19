"""Small LangChain and LangGraph adapters for the assessment API."""

import json
import re
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from langchain_core.messages import ToolMessage

from .assessment import (
    ASSESSMENT_PROMPT, AssessmentConfig, AssessmentInputs, AssessmentModel,
    CoverageDraft, Criterion, Evidence, NoMatchReviewDraft, NO_MATCH_REVIEW_PROMPT, assess,
    PredicateDraft, PREDICATE_PROMPT, DECISION_REVIEW_PROMPT,
)
from .evidence import (
    SOURCE_KINDS, build_criterion_inventory, build_fact_spans,
    build_source_catalog, collect_evidence,
)
from .criteria import CRITERION_EXTRACTION_PROMPT, CriterionExtraction, CriterionExtractor


def inputs_from_messages(
    messages: Iterable[Any], tools: Iterable[Any], *,
    system_prompt: str | None = None,
    labels: tuple[str, ...] = ("strength", "concern"),
    allowed_source_kinds: Iterable[str] = SOURCE_KINDS,
    allowed_source_ids: Iterable[str] | None = None,
    source_scope_ids: Iterable[str] | None = None,
    criterion_extractor: CriterionExtractor | None = None,
) -> AssessmentInputs:
    """Convert observed tagged tool messages to portable criteria/evidence records.

    Use EvidenceMetadataMiddleware when executing the tools. Pass the actual
    system prompt used for this run; dynamic prompts are not reconstructed.
    Multimodal/block content requires caller extraction before this adapter.
    """
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
            # Only explicit outcome labels are supported by this conservative
            # contract. Do not ask a model to reinterpret definitions around
            # already classified rules when no additional candidates exist.
            candidates = list(dict.fromkeys(line for line in source["directive_lines"]
                if line not in known and any(re.search(r"(?<!\w)" + re.escape(label) + r"(?!\w)", line, re.IGNORECASE)
                                             for label in labels)))
            if not candidates:
                continue
            extracted = CriterionExtraction.model_validate(criterion_extractor({
                "stage": "criterion_extraction", "source_id": source["source_id"],
                "text": text, "labels": list(labels), "known_criteria": known, "candidate_lines": candidates,
            }))
            if not extracted.complete or extracted.issues:
                raise ValueError(f"Incomplete criterion extraction for {source['source_id']}: {extracted.issues}")
            for row in extracted.criteria:
                if not row.quote.strip() or row.quote not in text:
                    raise ValueError("Extracted criterion must be an exact nonempty source quotation")
                if row.classification not in labels:
                    raise ValueError("Extracted criterion uses an unapproved classification")
                if re.search(r"(?<!\w)" + re.escape(row.classification) + r"(?!\w)", row.quote, re.IGNORECASE) is None:
                    raise ValueError("Extracted prose criterion must explicitly name its classification in the quote")
                if row.quote in known:
                    if known[row.quote] != row.classification:
                        raise ValueError("Extraction reclassifies an existing criterion")
                    continue
                if any(row.quote in existing or existing in row.quote for existing in known):
                    raise ValueError("Extracted criterion overlaps an already extracted rule; preserve atomic rules and their classifications")
                known[row.quote] = row.classification
                criteria.append(Criterion(
                    id=f"C{len(criteria) + 1}", text=row.quote,
                    source_id=source["source_id"], source_label=source["label"],
                    classification=row.classification, context=text,
                ))
    evidence = []
    for key, span in build_fact_spans(catalog).items():
        source = catalog.entries[span["source_id"]]
        evidence.append(Evidence(
            id=key, source_id=source["source_id"], source_label=source["label"],
            locator=span["locator"], quote=span["quote"], context=span["context"],
        ))
    return AssessmentInputs(criteria=criteria, evidence=evidence)


def make_langchain_criterion_extractor(model: Any, *, method: str | None = None) -> CriterionExtractor:
    """One optional structured call per permitted directive source; no hidden retries."""
    options = {"method": method} if method is not None else {}
    structured = model.with_structured_output(CriterionExtraction, include_raw=True, **options)

    def invoke(payload):
        response = structured.invoke([
            ("system", CRITERION_EXTRACTION_PROMPT),
            ("human", json.dumps(payload, ensure_ascii=False)),
        ])
        metadata = getattr(response.get("raw"), "response_metadata", {}) or {}
        if any(metadata.get(key) in {"length", "max_tokens", "max_output_tokens", "output_limit"}
               for key in ("finish_reason", "done_reason", "stop_reason")):
            raise ValueError("Criterion extraction was truncated")
        if response.get("parsing_error") or response.get("parsed") is None:
            raise ValueError(f"Criterion extraction could not be parsed: {response.get('parsing_error')}")
        return CriterionExtraction.model_validate(response["parsed"])

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
        schema = NoMatchReviewDraft if reviewing else PredicateDraft
        runnable = model.with_structured_output(schema, include_raw=True, **options) if reviewing else structured
        response = runnable.invoke([
            ("system", NO_MATCH_REVIEW_PROMPT if reviewing else DECISION_REVIEW_PROMPT if independent else PREDICATE_PROMPT),
            ("human", json.dumps(payload, ensure_ascii=False)),
        ])
        raw = response.get("raw")
        metadata = getattr(raw, "response_metadata", {}) or {}
        if any(metadata.get(key) in {"length", "max_tokens", "max_output_tokens", "output_limit"}
               for key in ("finish_reason", "done_reason", "stop_reason")):
            raise ValueError("Model output was truncated")
        if response.get("parsing_error") or response.get("parsed") is None:
            raise ValueError(f"Model output could not be parsed: {response.get('parsing_error')}")
        draft = schema.model_validate(response["parsed"])
        if not reviewing:
            for row in draft.root:
                rule = payload["criteria"].get(row.criterion_id)
                if rule is None or row.condition_quote not in rule["text"]:
                    raise ValueError("condition_quote must be an exact excerpt from the requested criterion.text")
        return draft if reviewing or independent else CoverageDraft([row.assessment() for row in draft.root])

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
