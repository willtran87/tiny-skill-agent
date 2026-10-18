"""Small LangChain and LangGraph adapters for the assessment API."""

import json
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from langchain_core.messages import ToolMessage

from .assessment import (
    ASSESSMENT_PROMPT, AssessmentConfig, AssessmentInputs, AssessmentModel,
    CoverageDraft, Criterion, Evidence, assess,
)
from .evidence import (
    SOURCE_KINDS, build_criterion_inventory, build_fact_spans,
    build_source_catalog, collect_evidence,
)


def inputs_from_messages(
    messages: Iterable[Any], tools: Iterable[Any], *,
    system_prompt: str | None = None,
    labels: tuple[str, ...] = ("strength", "concern"),
    allowed_source_kinds: Iterable[str] = SOURCE_KINDS,
    allowed_source_ids: Iterable[str] | None = None,
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
    catalog = build_source_catalog(ledger)
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
    evidence = []
    for key, span in build_fact_spans(catalog).items():
        source = catalog.entries[span["source_id"]]
        evidence.append(Evidence(
            id=key, source_id=source["source_id"], source_label=source["label"],
            locator=span["locator"], quote=span["quote"], context=span["context"],
        ))
    return AssessmentInputs(criteria=criteria, evidence=evidence)


def make_langchain_assessor(model: Any, *, method: str | None = None) -> AssessmentModel:
    """Wrap a chat model supporting with_structured_output as an assess callable.

    Pass method='json_schema' for the notebook's Ollama configuration. Other
    providers can use their default or an explicitly supported method. Provider
    exceptions, parsing failures, and truncation are retried/reported by assess.
    """
    options = {"method": method} if method is not None else {}
    structured = model.with_structured_output(CoverageDraft, include_raw=True, **options)

    def invoke(payload: dict[str, Any]) -> CoverageDraft:
        response = structured.invoke([
            ("system", ASSESSMENT_PROMPT),
            ("human", json.dumps(payload, ensure_ascii=False)),
        ])
        raw = response.get("raw")
        metadata = getattr(raw, "response_metadata", {}) or {}
        if any(metadata.get(key) in {"length", "max_tokens", "max_output_tokens", "output_limit"}
               for key in ("finish_reason", "done_reason", "stop_reason")):
            raise ValueError("Model output was truncated")
        if response.get("parsing_error") or response.get("parsed") is None:
            raise ValueError(f"Model output could not be parsed: {response.get('parsing_error')}")
        return CoverageDraft.model_validate(response["parsed"])

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
