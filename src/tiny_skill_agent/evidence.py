"""Reusable tool provenance collection and exact-text validation."""

import json
import re
from dataclasses import dataclass, replace
from typing import Any, Iterable, Mapping

from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.types import Command


EVIDENCE_KINDS = {"directive", "data"}
SOURCE_KINDS = frozenset({"tool", "skill", "system_prompt"})


def tag_tool(
    tool: BaseTool,
    kind: str,
    *,
    source_kind: str = "tool",
    source_arg: str | None = None,
    source_prefix: str = "",
    **attributes: Any,
) -> BaseTool:
    """Declare how a tool's successful output may be used as evidence."""
    if not kind:
        raise ValueError("Tool kind must be nonempty")
    if source_kind not in {"tool", "skill"}:
        raise ValueError("Tool source_kind must be 'tool' or 'skill'")
    if source_kind == "skill" and (not source_arg or source_prefix != "skill:"):
        raise ValueError("Skill sources require source_arg and source_prefix='skill:'")
    if source_kind == "skill" and kind != "directive":
        raise ValueError("Skill sources must be directives")
    if source_kind == "tool" and source_prefix.startswith("skill:"):
        raise ValueError("Tool sources cannot use the skill: prefix")
    meta: dict[str, Any] = {**attributes, "kind": kind, "source_kind": source_kind}
    if source_arg:
        meta.update(source_arg=source_arg, source_prefix=source_prefix)
    existing = tool.metadata or {}
    tool.metadata = {
        **existing,
        "_meta": {**existing.get("_meta", {}), **meta},
    }
    return tool


def tagged_result(content: str, kind: str, *, source: str | None = None) -> tuple[str, dict]:
    """Return content and runtime metadata from a content_and_artifact tool."""
    meta = {"kind": kind}
    if source is not None:
        meta["source"] = source
    return content, {"_meta": meta}


class EvidenceMetadataMiddleware(AgentMiddleware):
    """Attach registered `_meta` to ordinary tool results automatically."""

    def __init__(self, tools: Iterable[BaseTool]):
        self.registry = {tool.name: tool for tool in tools}

    def _attach(self, request: Any, response: Any) -> Any:
        if isinstance(response, Command):
            tool = self.registry.get(request.tool_call["name"])
            if tool is None or (tool.metadata or {}).get("_meta", {}).get("kind") not in EVIDENCE_KINDS:
                return response
            update = response.update
            if not isinstance(update, Mapping):
                raise ValueError("Evidence Command requires a mapping update with tool messages")
            messages = update.get("messages", [])
            if not isinstance(messages, (list, tuple)) or not any(
                isinstance(message, ToolMessage) and message.tool_call_id == request.tool_call["id"]
                for message in messages
            ):
                raise ValueError("Evidence Command requires a matching ToolMessage in update['messages']")
            return replace(response, update={**update, "messages": [
                self._attach(request, message)
                if isinstance(message, ToolMessage) and message.tool_call_id == request.tool_call["id"]
                else message for message in messages
            ]})
        if not isinstance(response, ToolMessage) or response.status != "success":
            return response
        call = request.tool_call
        tool = self.registry.get(call["name"])
        if tool is None:
            return response
        declared = (tool.metadata or {}).get("_meta", {})
        if declared.get("kind") not in EVIDENCE_KINDS:
            return response

        expected: dict[str, Any] = {
            key: value
            for key, value in declared.items()
            if key not in {"source_arg", "source_prefix"}
        }
        source_arg = declared.get("source_arg")
        if source_arg:
            value = call.get("args", {}).get(source_arg)
            if not isinstance(value, str) or not value:
                raise ValueError(f"Tool {tool.name} call has no {source_arg!r} source")
            expected["source"] = f"{declared.get('source_prefix', '')}{value}"

        artifact = response.artifact
        artifact_dict = artifact.copy() if isinstance(artifact, dict) else {}
        if artifact is not None and not isinstance(artifact, dict):
            artifact_dict["payload"] = artifact
        existing = artifact_dict.get("_meta")
        if existing is not None:
            if not isinstance(existing, dict) or existing.get("kind") not in {
                expected["kind"], "error"
            }:
                raise ValueError(f"Tool {tool.name} result kind disagrees with registered kind")
            if existing.get("kind") == "error":
                return response
            for key, value in expected.items():
                if key in existing and existing[key] != value:
                    raise ValueError(f"Tool {tool.name} {key} does not match its call")
        artifact_dict["_meta"] = {**(existing or {}), **expected}
        return response.model_copy(update={"name": tool.name, "artifact": artifact_dict})

    def wrap_tool_call(self, request: Any, handler: Any) -> Any:
        return self._attach(request, handler(request))

    async def awrap_tool_call(self, request: Any, handler: Any) -> Any:
        return self._attach(request, await handler(request))


@dataclass
class EvidenceLedger:
    directive_sources: dict[str, list[str]]
    fact_sources: dict[str, str]
    tool_evidence: list[dict[str, Any]]
    source_kinds: dict[str, str]

    def as_prompt_data(self) -> dict[str, Any]:
        return {
            "tool_evidence": self.tool_evidence,
            "directive_sources": self.directive_sources,
            "fact_sources": self.fact_sources,
            "source_kinds": self.source_kinds,
        }


@dataclass
class SourceCatalog:
    """Run-local short IDs and the observed sources they represent."""

    entries: dict[str, dict[str, Any]]

    def as_prompt_data(self) -> dict[str, dict[str, Any]]:
        """Give the model readable sources without long internal source IDs."""
        return {
            short_id: {key: value for key, value in entry.items() if key != "source_id"}
            for short_id, entry in self.entries.items()
        }


def build_source_catalog(ledger: EvidenceLedger) -> SourceCatalog:
    """Assign S1, S2, ... to each observed directive or fact source."""
    source_ids = dict.fromkeys([*ledger.directive_sources, *ledger.fact_sources])
    tool_names = {
        item["source_id"]: item["tool_name"] for item in ledger.tool_evidence
    }
    entries: dict[str, dict[str, Any]] = {}
    seen_tool_results: set[tuple[str, tuple[str, ...] | str]] = set()
    for source_id in source_ids:
        kind = ledger.source_kinds[source_id]
        if kind == "tool":
            content: tuple[str, ...] | str = (
                tuple(ledger.directive_sources[source_id])
                if source_id in ledger.directive_sources
                else ledger.fact_sources[source_id]
            )
            repeated_result = (tool_names.get(source_id, source_id), content)
            if repeated_result in seen_tool_results:
                continue
            seen_tool_results.add(repeated_result)
        short_id = f"S{len(entries) + 1}"
        if kind == "system_prompt":
            label = "System prompt"
        elif kind == "skill":
            label = f"Skill: {source_id.removeprefix('skill:')}"
        else:
            label = f"Tool: {tool_names.get(source_id, source_id)} ({short_id})"
        entry: dict[str, Any] = {
            "source_id": source_id,
            "source_kind": kind,
            "label": label,
        }
        if source_id in ledger.directive_sources:
            entry["directive_lines"] = ledger.directive_sources[source_id]
        if source_id in ledger.fact_sources:
            entry["fact_content"] = ledger.fact_sources[source_id]
        entries[short_id] = entry
    return SourceCatalog(entries)


def build_criterion_inventory(
    catalog: SourceCatalog,
    *,
    labels: tuple[str, ...] = ("strength", "concern"),
    allowed_source_kinds: Iterable[str] = SOURCE_KINDS,
    allowed_source_ids: Iterable[str] | None = None,
) -> dict[str, dict[str, str]]:
    """Give each observed, permitted classified criterion a run-local C-number."""
    allowed_kinds = set(allowed_source_kinds)
    allowed_ids = None if allowed_source_ids is None else set(allowed_source_ids)
    if not allowed_kinds <= SOURCE_KINDS:
        raise ValueError("Unknown criterion source kind")
    pattern = re.compile(r"^\[(" + "|".join(re.escape(label) for label in labels) + r")\]\s+")
    inventory: dict[str, dict[str, str]] = {}
    seen: set[tuple[str, str]] = set()
    for source_id, entry in catalog.entries.items():
        if entry["source_kind"] not in allowed_kinds:
            continue
        if allowed_ids is not None and entry["source_id"] not in allowed_ids:
            continue
        for line in entry.get("directive_lines", []):
            identity = (entry["source_id"], line)
            if pattern.match(line) and identity not in seen:
                seen.add(identity)
                inventory[f"C{len(inventory) + 1}"] = {
                    "criterion": line,
                    "criterion_source_id": source_id,
                }
    return inventory


ASSESSMENT_STATUSES = frozenset({
    "matched", "no_match", "insufficient_evidence", "not_applicable"
})


def build_fact_spans(catalog: SourceCatalog) -> dict[str, dict[str, str]]:
    """Index every observed text line or JSON leaf with its source context."""
    spans: dict[str, dict[str, str]] = {}

    def add(source_id: str, locator: str, quote: str, context: str) -> None:
        spans[f"E{len(spans) + 1}"] = {
            "source_id": source_id,
            "locator": locator,
            "quote": quote,
            "context": context,
        }

    for source_id, entry in catalog.entries.items():
        if "fact_content" not in entry:
            continue
        raw = entry["fact_content"]
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            lines = raw.splitlines()
            for index, line in enumerate(lines):
                if not line.strip():
                    continue
                neighbors = [
                    lines[other].strip()
                    for other in range(max(0, index - 1), min(len(lines), index + 2))
                    if lines[other].strip()
                ]
                add(source_id, f"line:{index + 1}", line.strip(), "\n".join(neighbors))
            continue

        def escape_pointer(token: str) -> str:
            return token.replace("~", "~0").replace("/", "~1")

        def visit(value: Any, path: str, labels: tuple[str, ...], parent: Any) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    visit(child, f"{path}/{escape_pointer(str(key))}", (*labels, str(key)), value)
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    visit(child, f"{path}/{index}", (*labels, str(index)), value)
            else:
                quote = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
                label = ".".join(part for part in labels if not part.isdecimal())
                context = f"{label}: {quote}" if label else str(quote)
                if isinstance(parent, dict) and len(parent) > 1:
                    context += " | parent: " + json.dumps(parent, ensure_ascii=False)
                add(source_id, f"json:{path or '/'}", str(quote), context)

        visit(parsed, "", (), None)
    return spans


def validate_evidence_assessment_batch(
    assessments: Iterable[Any], expected_ids: Iterable[str],
    spans: Mapping[str, Mapping[str, str]],
    *, allowed_source_ids: Iterable[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Validate one source or case assessment batch and its evidence IDs."""
    expected = set(expected_ids)
    allowed = None if allowed_source_ids is None else set(allowed_source_ids)
    accepted: dict[str, dict[str, Any]] = {}

    def check_ids(ids: Iterable[str], criterion_id: str) -> None:
        for evidence_id in ids:
            span = spans.get(evidence_id)
            if span is None:
                raise ValueError(f"{criterion_id}: unknown evidence ID: {evidence_id}")
            if allowed is not None and span["source_id"] not in allowed:
                raise ValueError(f"{criterion_id}: evidence ID is outside the requested source")

    for item in assessments:
        row = dict(item if isinstance(item, Mapping) else item.model_dump())
        criterion_id = row["criterion_id"]
        if criterion_id not in expected:
            raise ValueError(f"Unrequested criterion ID: {criterion_id}")
        if criterion_id in accepted:
            raise ValueError(f"Duplicate criterion ID: {criterion_id}")
        status = row["status"]
        status_ids = row["evidence_ids"]
        if status not in ASSESSMENT_STATUSES:
            raise ValueError(f"{criterion_id}: unknown assessment status: {status}")
        if not isinstance(row["reason"], str) or not row["reason"].strip():
            raise ValueError(f"{criterion_id}: reason is required")
        if status in {"matched", "no_match", "not_applicable"} and not status_ids:
            raise ValueError(f"{criterion_id}: {status} requires cited evidence")
        check_ids(status_ids, criterion_id)
        accepted[criterion_id] = row
    return accepted


def source_assessment_coverage(
    assessments: Mapping[str, Mapping[str, Any]],
    source_ids: Iterable[str], criterion_ids: Iterable[str],
) -> dict[str, Any]:
    """Report missing criterion assessments for every observed data source."""
    source_ids = list(source_ids)
    criterion_ids = list(criterion_ids)
    missing = [
        {"source_id": source_id, "criterion_id": criterion_id}
        for source_id in source_ids for criterion_id in criterion_ids
        if criterion_id not in assessments.get(source_id, {})
    ]
    return {
        "sources": len(source_ids),
        "criteria": len(criterion_ids),
        "expected_pairs": len(source_ids) * len(criterion_ids),
        "missing": missing,
        "complete": not missing,
    }


def evidence_assessment_coverage(
    assessments: Mapping[str, Mapping[str, Any]], inventory: Mapping[str, Any],
    *, confirmed_no_match: Iterable[str] = (),
) -> dict[str, Any]:
    """Separate assessment coverage from whether evidence suffices for a decision."""
    report: dict[str, Any] = {"total": len(inventory)}
    for status in ("matched", "no_match", "insufficient_evidence", "not_applicable"):
        report[status] = [
            criterion_id for criterion_id in inventory
            if assessments.get(criterion_id, {}).get("status") == status
        ]
    report["missing"] = [criterion_id for criterion_id in inventory if criterion_id not in assessments]
    confirmed = set(confirmed_no_match)
    report["unconfirmed_no_match"] = [
        criterion_id for criterion_id in report["no_match"] if criterion_id not in confirmed
    ]
    report["complete"] = not report["missing"] and not report["unconfirmed_no_match"]
    report["decision_ready"] = report["complete"] and not report["insufficient_evidence"]
    return report


def expand_evidence_findings(
    assessments: Mapping[str, Mapping[str, Any]],
    inventory: Mapping[str, Mapping[str, str]],
    spans: Mapping[str, Mapping[str, str]],
    catalog: SourceCatalog,
) -> list[dict[str, Any]]:
    """Resolve all evidence IDs; derive classification from exact criterion text."""
    records: list[dict[str, Any]] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    for criterion_id, assessment in assessments.items():
        if assessment["status"] != "matched":
            continue
        criterion = inventory[criterion_id]
        criterion_entry = catalog.entries[criterion["criterion_source_id"]]
        match = re.match(r"^\[(strength|concern)\]\s+", criterion["criterion"])
        if match is None:
            raise ValueError(f"{criterion_id}: criterion has no classification")
        candidate_findings = assessment.get("findings") or [{
            "evidence_ids": assessment["evidence_ids"], "reason": assessment["reason"]
        }]
        for finding in candidate_findings:
            candidate = finding if isinstance(finding, Mapping) else finding.model_dump()
            evidence_ids = list(dict.fromkeys(candidate["evidence_ids"]))
            identity = (criterion_id, tuple(sorted(evidence_ids)))
            if identity in seen:
                continue
            seen.add(identity)
            facts = []
            for evidence_id in evidence_ids:
                span = spans[evidence_id]
                source = catalog.entries[span["source_id"]]
                facts.append({
                    "evidence_id": evidence_id,
                    "source": source["source_id"],
                    "source_label": source["label"],
                    "locator": span["locator"],
                    "quote": span["quote"],
                    "context": span["context"],
                })
            records.append({
                "criterion": criterion["criterion"],
                "criterion_source": criterion_entry["source_id"],
                "criterion_source_label": criterion_entry["label"],
                "classification": match.group(1),
                "facts": facts,
                "reason": candidate["reason"],
            })
    return records


def validate_assessment_batch(
    assessments: Iterable[Any], expected_ids: Iterable[str]
) -> dict[str, dict[str, Any]]:
    """Reject duplicate/unrequested IDs and inconsistent assessment statuses."""
    expected = set(expected_ids)
    accepted: dict[str, dict[str, Any]] = {}
    for item in assessments:
        row = dict(item if isinstance(item, Mapping) else item.model_dump())
        criterion_id = row["criterion_id"]
        if criterion_id not in expected:
            raise ValueError(f"Unrequested criterion ID: {criterion_id}")
        if criterion_id in accepted:
            raise ValueError(f"Duplicate criterion ID: {criterion_id}")
        status = row["status"]
        findings = row["findings"]
        if status not in {"matched", "no_match", "uncertain"}:
            raise ValueError(f"Unknown assessment status: {status}")
        if status == "matched" and not findings:
            raise ValueError(f"{criterion_id}: matched requires a finding")
        if status != "matched" and findings:
            raise ValueError(f"{criterion_id}: {status} requires empty findings")
        accepted[criterion_id] = row
    return accepted


def expand_assessments_to_records(
    assessments: Mapping[str, Mapping[str, Any]], inventory: Mapping[str, Mapping[str, str]]
) -> list[dict[str, Any]]:
    """Attach deterministic criterion text and source IDs to matched facts."""
    records: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for criterion_id, assessment in assessments.items():
        if assessment["status"] != "matched":
            continue
        criterion = inventory[criterion_id]
        for candidate in assessment["findings"]:
            finding = dict(candidate if isinstance(candidate, Mapping) else candidate.model_dump())
            key = (criterion_id, finding["fact_source_id"], finding["fact"])
            if key in seen:
                continue
            seen.add(key)
            records.append({**criterion, **finding})
    return records


def criterion_coverage(
    assessments: Mapping[str, Mapping[str, Any]], inventory: Mapping[str, Any],
    *, confirmed_no_match: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Report exactly which observed criteria have a final assessment."""
    report: dict[str, Any] = {"total": len(inventory)}
    for status in ("matched", "no_match", "uncertain"):
        report[status] = [
            criterion_id for criterion_id in inventory
            if assessments.get(criterion_id, {}).get("status") == status
        ]
    report["missing"] = [criterion_id for criterion_id in inventory if criterion_id not in assessments]
    confirmed = set(report["no_match"] if confirmed_no_match is None else confirmed_no_match)
    report["unconfirmed_no_match"] = [
        criterion_id for criterion_id in report["no_match"] if criterion_id not in confirmed
    ]
    report["complete"] = not (
        report["uncertain"] or report["missing"] or report["unconfirmed_no_match"]
    )
    return report


def enrich_record_sources(records: Iterable[Any], catalog: SourceCatalog) -> list[dict[str, Any]]:
    """Resolve model-selected short IDs into full IDs and readable labels."""
    enriched: list[dict[str, Any]] = []
    for number, record in enumerate(records, start=1):
        row = dict(record if isinstance(record, Mapping) else record.model_dump())
        for role, required_content in (("criterion", "directive_lines"), ("fact", "fact_content")):
            short_id = row.pop(f"{role}_source_id")
            entry = catalog.entries.get(short_id)
            if entry is None or required_content not in entry:
                raise ValueError(f"Row {number}: unknown {role} source ID: {short_id}")
            row[f"{role}_source"] = entry["source_id"]
            row[f"{role}_source_label"] = entry["label"]
        enriched.append(row)
    return enriched


def collect_evidence(
    messages: Iterable[Any],
    tools: Iterable[BaseTool],
    *,
    system_prompt: str | None = None,
) -> EvidenceLedger:
    """Route successful tool results by registered and runtime `_meta.kind`."""
    messages = list(messages)
    registry = {tool.name: tool for tool in tools}
    calls = {
        call["id"]: call
        for message in messages
        if isinstance(message, AIMessage)
        for call in message.tool_calls
    }
    directives = {"system_prompt": system_prompt.splitlines()} if system_prompt else {}
    source_kinds = {"system_prompt": "system_prompt"} if system_prompt else {}
    ledger = EvidenceLedger(directives, {}, [], source_kinds)

    for message in messages:
        if not isinstance(message, ToolMessage) or message.status != "success":
            continue
        call = calls.get(message.tool_call_id)
        if call is None or call["name"] != message.name:
            raise ValueError("Tool result does not match an observed tool call")
        tool = registry.get(message.name)
        if tool is None:
            raise ValueError(f"Unregistered tool result: {message.name}")
        declared = (tool.metadata or {}).get("_meta", {})
        if not isinstance(declared, dict) or not declared.get("kind"):
            raise ValueError(f"Tool {message.name} has no registered _meta.kind")
        artifact = message.artifact if isinstance(message.artifact, dict) else {}
        runtime = artifact.get("_meta") or message.additional_kwargs.get("_meta")
        if declared["kind"] in EVIDENCE_KINDS and not isinstance(runtime, dict):
            raise ValueError(f"Tool {message.name} result is missing _meta.kind")
        runtime = runtime or declared
        if not isinstance(runtime, dict) or runtime.get("kind") not in {
            declared["kind"], "error"
        }:
            raise ValueError(f"Tool {message.name} result kind disagrees with registered kind")
        kind = runtime["kind"]
        if kind not in EVIDENCE_KINDS:
            continue
        source_kind = declared.get("source_kind", "tool")
        if source_kind not in {"tool", "skill"} or runtime.get("source_kind") != source_kind:
            raise ValueError(f"Tool {message.name} source kind disagrees with registered kind")

        source_arg = declared.get("source_arg")
        if source_arg:
            arg_value = call.get("args", {}).get(source_arg)
            if not isinstance(arg_value, str) or not arg_value:
                raise ValueError(f"Tool {message.name} call has no {source_arg!r} source")
            source_id = f"{declared.get('source_prefix', '')}{arg_value}"
            if runtime.get("source") != source_id:
                raise ValueError(f"Tool {message.name} source does not match its call")
        else:
            source_id = f"tool:{message.name}#{message.tool_call_id}"
            if runtime.get("source") not in (None, source_id):
                raise ValueError(f"Tool {message.name} supplied an unexpected source")
        if source_id == "system_prompt" or (
            source_kind == "skill" and not source_id.startswith("skill:")
        ) or (source_kind == "tool" and source_id.startswith("skill:")):
            raise ValueError(f"Tool {message.name} has an invalid source ID")
        previous_kind = ledger.source_kinds.setdefault(source_id, source_kind)
        if previous_kind != source_kind:
            raise ValueError(f"Source {source_id} has conflicting source kinds")

        content = str(message.content)
        ledger.tool_evidence.append(
            {"source_id": source_id, "tool_name": message.name, "_meta": runtime, "content": content}
        )
        if kind == "directive":
            ledger.directive_sources.setdefault(source_id, []).extend(content.splitlines())
        else:
            ledger.fact_sources[source_id] = content
    return ledger


def exact_fact_values(raw_output: str) -> set[str]:
    """Extract complete lines or JSON leaf values, never substrings."""
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        return {line.strip() for line in raw_output.splitlines() if line.strip()}

    values: set[str] = set()

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif value is not None:
            values.add(str(value))

    visit(parsed)
    return values


def validate_record_sources(
    records: Iterable[Any],
    ledger: EvidenceLedger,
    *,
    allowed_criterion_source_kinds: Iterable[str] = SOURCE_KINDS,
    allowed_criterion_source_ids: Iterable[str] | None = None,
) -> None:
    """Check exact citations against their named sources and permitted source kinds."""
    allowed_kinds = set(allowed_criterion_source_kinds)
    allowed_ids = None if allowed_criterion_source_ids is None else set(allowed_criterion_source_ids)
    if not allowed_kinds <= SOURCE_KINDS:
        raise ValueError("Unknown criterion source kind")
    for number, record in enumerate(records, start=1):
        row: Mapping[str, Any] = (
            record if isinstance(record, Mapping) else record.model_dump()
        )
        criterion_source = row["criterion_source"]
        fact_source = row["fact_source"]
        if criterion_source not in ledger.directive_sources:
            raise ValueError(f"Row {number}: criterion source was not observed")
        if allowed_ids is not None and criterion_source not in allowed_ids:
            raise ValueError(f"Row {number}: criterion source ID is not allowed")
        if ledger.source_kinds.get(criterion_source) not in allowed_kinds:
            raise ValueError(f"Row {number}: criterion source kind is not allowed")
        if row["criterion"] not in ledger.directive_sources[criterion_source]:
            raise ValueError(f"Row {number}: criterion is not an exact source line")
        if fact_source not in ledger.fact_sources:
            raise ValueError(f"Row {number}: fact source was not observed")
        if row["fact"] not in exact_fact_values(ledger.fact_sources[fact_source]):
            raise ValueError(f"Row {number}: fact is not an exact tool-returned value")


def validate_criterion_labels(
    records: Iterable[Any], *, labels: tuple[str, ...] = ("strength", "concern")
) -> None:
    """Require classification to match the cited criterion's bracketed label."""
    pattern = re.compile(r"^\[(" + "|".join(re.escape(label) for label in labels) + r")\]\s+")
    for number, record in enumerate(records, start=1):
        row: Mapping[str, Any] = (
            record if isinstance(record, Mapping) else record.model_dump()
        )
        match = pattern.match(row["criterion"])
        if match is None:
            raise ValueError(f"Row {number}: cited criterion has no classification")
        if row["classification"] != match.group(1):
            raise ValueError(f"Row {number}: classification does not match the criterion")


def derive_criterion_classifications(
    records: Iterable[Any], *, labels: tuple[str, ...] = ("strength", "concern")
) -> list[dict[str, Any]]:
    """Add classification from each cited criterion's bracketed label."""
    pattern = re.compile(r"^\[(" + "|".join(re.escape(label) for label in labels) + r")\]\s+")
    classified: list[dict[str, Any]] = []
    for number, record in enumerate(records, start=1):
        row = dict(record if isinstance(record, Mapping) else record.model_dump())
        match = pattern.match(row["criterion"])
        if match is None:
            raise ValueError(f"Row {number}: cited criterion has no classification")
        if "classification" in row and row["classification"] != match.group(1):
            raise ValueError(f"Row {number}: classification does not match the criterion")
        row["classification"] = match.group(1)
        classified.append(row)
    return classified
