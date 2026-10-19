"""Run from the repository root: python -m evals.run --model qwen3-coder:30b."""

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import time
from urllib.request import urlopen

from tiny_skill_agent.assessment import ASSESSMENT_PROMPT, NO_MATCH_REVIEW_PROMPT, PREDICATE_PROMPT, DECISION_REVIEW_PROMPT, AssessmentConfig, AssessmentInputs, assess


def score_case(case, result):
    """Gold status/span checks, not a semantic judge of the generated reason.

    Atomic finding checks require a separate record with the expected citation
    set for each entity in these fixtures. A combined record cannot pass for two.
    """
    expected = case["expected"]
    cid = case["criteria"][0]["id"]
    row = result["criterion_assessments"].get(cid)
    observed = set(row["evidence_ids"]) if row else set()
    required = set(expected["required_evidence_ids"])
    evidence = {item["id"]: item for item in case["evidence"]}
    references = []
    for assessment in result["criterion_assessments"].values():
        references.extend(eid in evidence for eid in assessment["evidence_ids"])
    for sid, rows in result["source_assessments"].items():
        for assessment in rows.values():
            references.extend(eid in evidence and evidence[eid]["source_id"] == sid
                              for eid in assessment["evidence_ids"])
    findings = result["findings"]
    for finding in findings:
        rule = case["criteria"][0]
        references.append(finding["criterion_id"] == cid
                          and finding["criterion_source"] == rule["source_id"]
                          and finding["criterion"] == rule["text"]
                          and finding["classification"] == rule["classification"])
        for fact in finding["facts"]:
            original = evidence.get(fact["evidence_id"])
            references.append(original is not None and all(
                fact[key] == original.get(source_key, "")
                for key, source_key in (("source", "source_id"), ("source_label", "source_label"),
                                        ("locator", "locator"), ("quote", "quote"), ("context", "context"))))
    predicted_sets = [(finding["criterion_id"], frozenset(f["evidence_id"] for f in finding["facts"])) for finding in findings]
    # One-to-one matching permits predeclared equivalent citations without
    # allowing a combined finding to count as two independent findings.
    options = [{frozenset(ids) for ids in f.get("acceptable_evidence_sets", [f["evidence_ids"]])}
               for f in expected["findings"]]
    assigned = {}
    def match(gold_index, visited):
        for index, (criterion_id, citations) in enumerate(predicted_sets):
            if index in visited or criterion_id != cid or citations not in options[gold_index]:
                continue
            visited.add(index)
            if index not in assigned or match(assigned[index], visited):
                assigned[index] = gold_index
                return True
        return False
    atomic_correct = len(predicted_sets) == len(options) and all(match(i, set()) for i in range(len(options)))
    checks = {
        "status_correct": row is not None and row["status"] == expected["status"],
        "required_evidence_covered": row is not None and required <= observed,
        "atomic_findings_correct": atomic_correct,
        "reference_integrity": all(references),
        "coverage_complete": result["coverage"]["complete"],
    }
    if "decision_ready" in expected:
        checks["readiness_correct"] = result["coverage"]["decision_ready"] == expected["decision_ready"]
    return {
        **checks, "passed": all(checks.values()),
        "expected_status": expected["status"], "actual_status": row["status"] if row else "missing",
        "expected_findings": len(expected["findings"]), "actual_findings": len(findings),
        "required_evidence_count": len(required), "required_evidence_found": len(required & observed),
        "missing_required_evidence": sorted(required - observed),
        "reference_checks": len(references), "reference_checks_passed": sum(references),
        "false_positive_findings": len(findings) if expected["status"] != "matched" else 0,
        "reason": row["reason"] if row else "No accepted case assessment.",
    }


def validate_cases(dataset):
    seen = set()
    for case in dataset["cases"]:
        if case["id"] in seen:
            raise ValueError(f"Duplicate case: {case['id']}")
        seen.add(case["id"])
        inputs = AssessmentInputs.model_validate({k: case[k] for k in ("criteria", "evidence")})
        if len(inputs.criteria) != 1:
            raise ValueError("These fixtures require exactly one criterion per case")
        ids = {e.id for e in inputs.evidence}
        if len(ids) != len(inputs.evidence):
            raise ValueError("Duplicate evidence IDs")
        expected = case["expected"]
        gold_ids = set(expected["required_evidence_ids"])
        for finding in expected["findings"]:
            if not finding["evidence_ids"]:
                raise ValueError("Gold findings require evidence")
            gold_ids.update(finding["evidence_ids"])
            for option in finding.get("acceptable_evidence_sets", []):
                if not option:
                    raise ValueError("Alternative citation sets cannot be empty")
                gold_ids.update(option)
            if "acceptable_evidence_sets" in finding and not finding["acceptable_evidence_sets"]:
                raise ValueError("At least one citation alternative is required")
        if "decision_ready" in expected and not isinstance(expected["decision_ready"], bool):
            raise ValueError("Expected decision_ready must be a boolean")
        if not gold_ids <= ids:
            raise ValueError(f"Unknown gold evidence IDs in {case['id']}")
        if expected["status"] not in {"matched", "no_match", "not_applicable", "insufficient_evidence"}:
            raise ValueError("Unknown gold status")
        if bool(expected["findings"]) != (expected["status"] == "matched"):
            raise ValueError("Gold findings and status disagree")


def render_report(report):
    rows = report["cases"]
    scores = [r["score"] for r in rows]
    meta = report["metadata"]
    lines = ["# Synthetic assessment evaluation", "",
             f"Model: `{meta['model']}`. Started: {meta['started_at']}. State: **{report['state']}**.", "",
             "Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.", "",
             f"- Strict fixture passes: **{sum(s['passed'] for s in scores)}/{len(scores)}** (planned: {meta['planned_cases']}).",
             f"- Correct case statuses: **{sum(s['status_correct'] for s in scores)}/{len(scores)}**.",
             f"- Required gold evidence cited: **{sum(s['required_evidence_found'] for s in scores)}/{sum(s['required_evidence_count'] for s in scores)}**.",
             f"- Reference/provenance checks: **{sum(s['reference_checks_passed'] for s in scores)}/{sum(s['reference_checks'] for s in scores)}**.",
             f"- False-positive findings in the {sum(r['expected']['status'] != 'matched' for r in rows)} nonmatched gold cases: **{sum(s['false_positive_findings'] for s in scores)}**.", "",
             "| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |",
             "| --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        s = row["score"]
        lines.append(f"| {row['id']} | {s['expected_status']} | {s['actual_status']} | {s['actual_findings']} / {s['expected_findings']} | {s['required_evidence_found']} / {s['required_evidence_count']} | {'PASS' if s['passed'] else 'FAIL'} |")
    lines.extend(["", "## Reasons and diagnostics", ""])
    for row in rows:
        s = row["score"]
        lines.extend([f"### {row['id']}", "", f"**Expected:** {row['expected']['rationale']}", "",
                      f"**Model:** {s['reason']}", "",
                      f"Coverage complete: `{row['result']['coverage']['complete']}`; decision ready: `{row['result']['coverage']['decision_ready']}`; source/case disagreements: {len(row['result']['disagreements'])}; captured call errors: {len(row['result']['coverage']['errors'])}; model calls: {len(row['calls'])}; elapsed: {row['elapsed_seconds']:.1f}s.", ""])
        errors = list(dict.fromkeys(e["error"] for e in row["result"]["coverage"]["errors"]))
        if errors:
            lines.extend(["**Rejected responses:** " + "; ".join(errors), ""])
        for key, review in row["result"].get("no_match_reviews", {}).items():
            lines.extend([f"**Negative-evidence review ({key}):** `{review['verdict']}`. {review['reason']}", ""])
        for key, review in row["result"].get("decision_reviews", {}).items():
            lines.extend([f"**Independent review ({key}):** scope `{review['scope']}`, condition `{review['condition']}`, exception `{review['exception']}`. {review['condition_reason']} {review['exception_reason']}", ""])
        if row["result"]["coverage"].get("review_disagreements"):
            lines.extend(["**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.", ""])
    lines.extend(["## Interpretation limits", "",
                  "Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.", "",
                  "Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.", "",
                  "This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="qwen3-coder:30b")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--output", type=Path, help="JSON output path; companion Markdown is also written")
    args = parser.parse_args()
    raw = args.cases.read_bytes()
    dataset = json.loads(raw)
    validate_cases(dataset)
    from langchain_ollama import ChatOllama
    from tiny_skill_agent.adapters import make_langchain_assessor

    config = AssessmentConfig()
    settings = {"temperature": 0, "seed": 42, "num_ctx": 8192, "num_predict": 4096}
    model = ChatOllama(model=args.model, base_url=args.base_url, **settings,
                       client_kwargs={"timeout": 180})
    invoke = make_langchain_assessor(model, method="json_schema")
    started = datetime.now(timezone.utc)
    output = args.output or Path("evals/results") / (started.strftime("%Y%m%dT%H%M%SZ") + ".json")
    if output.suffix != ".json":
        parser.error("--output must end in .json")
    if output.exists() or output.with_suffix(".md").exists():
        parser.error("Output already exists; choose a new path to preserve prior runs")
    repo = Path(__file__).resolve().parents[1]
    def git(*command):
        return subprocess.check_output(["git", *command], cwd=repo, text=True).strip()
    with urlopen(args.base_url.rstrip("/") + "/api/tags", timeout=10) as response:
        tags = json.load(response)
    with urlopen(args.base_url.rstrip("/") + "/api/version", timeout=10) as response:
        ollama_version = json.load(response)
    report = {"state": "running", "metadata": {
        "started_at": started.isoformat(), "model": args.model, "model_settings": settings,
        "ollama_version": ollama_version, "model_metadata": next((m for m in tags["models"] if m["name"] == args.model), None),
        "git_commit": git("rev-parse", "HEAD"), "git_status": git("status", "--short"),
        "dataset_sha256": hashlib.sha256(raw).hexdigest(),
        "assessment_prompt_sha256": hashlib.sha256(ASSESSMENT_PROMPT.encode()).hexdigest(),
        "no_match_review_prompt_sha256": hashlib.sha256(NO_MATCH_REVIEW_PROMPT.encode()).hexdigest(),
        "predicate_prompt_sha256": hashlib.sha256(PREDICATE_PROMPT.encode()).hexdigest(),
        "decision_review_prompt_sha256": hashlib.sha256(DECISION_REVIEW_PROMPT.encode()).hexdigest(),
        "implementation_sha256": {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (repo / "src/tiny_skill_agent/assessment.py", repo / "src/tiny_skill_agent/adapters.py", Path(__file__).resolve())},
        "packages": {p: version(p) for p in ("langchain", "langchain-ollama", "langgraph", "pydantic")},
        "assessment_config": config.model_dump(), "planned_cases": len(dataset["cases"]),
    }, "cases": []}
    output.parent.mkdir(parents=True, exist_ok=True)
    def save():
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        output.with_suffix(".md").write_text(render_report(report), encoding="utf-8")
    save()
    for case in dataset["cases"]:
        print(f"START {case['id']}", flush=True)
        calls = []
        def traced(payload):
            call = {"payload": payload}
            calls.append(call)
            call_start = time.monotonic()
            try:
                draft = invoke(payload)
                call["output"] = draft.model_dump(mode="json")
                return draft
            except Exception as exc:
                call["error"] = str(exc)
                raise
            finally:
                call["elapsed_seconds"] = round(time.monotonic() - call_start, 3)
                print(f"  {payload['stage']} {payload['scope']}: {call['elapsed_seconds']:.1f}s", flush=True)
        case_start = time.monotonic()
        result = assess(criteria=case["criteria"], evidence=case["evidence"], model=traced, config=config,
                        request="Assess the supplied underwriting criteria. Preserve each independent qualifying finding and its supporting evidence.")
        entry = {"id": case["id"], "category": case["category"], "expected": case["expected"],
                 "result": result.model_dump(mode="json"), "calls": calls,
                 "elapsed_seconds": round(time.monotonic() - case_start, 3)}
        entry["score"] = score_case(case, entry["result"])
        report["cases"].append(entry)
        save()
        print(f"RESULT {case['id']}: {'PASS' if entry['score']['passed'] else 'FAIL'}; status={entry['score']['actual_status']}; findings={entry['score']['actual_findings']}/{entry['score']['expected_findings']}", flush=True)
    report["state"] = "completed"
    report["metadata"]["finished_at"] = datetime.now(timezone.utc).isoformat()
    save()
    print(f"Saved {output} and {output.with_suffix('.md')}", flush=True)


if __name__ == "__main__":
    main()
