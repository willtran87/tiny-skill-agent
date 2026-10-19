"""Freeze inputs/code, run identical evaluations, and report consistency separately from accuracy."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from evals.run import validate_cases


def signature(case):
    """Ignore wording/order; preserve final status, finding citation groups, and readiness."""
    result = case["result"]
    statuses = sorted((cid, row["status"]) for cid, row in result["criterion_assessments"].items())
    findings = sorted((f["criterion_id"], sorted(set(c["evidence_id"] for c in f["facts"]))) for f in result["findings"])
    return json.dumps([statuses, findings, result["coverage"]["decision_ready"]], sort_keys=True)


def summarize(reports):
    if not reports:
        raise ValueError("At least one completed report is required")
    ids = [c["id"] for c in reports[0]["cases"]]
    if any(r["state"] != "completed" or [c["id"] for c in r["cases"]] != ids for r in reports):
        raise ValueError("Reports must be completed and contain the same ordered cases")
    indexes = [{c["id"]: c for c in r["cases"]} for r in reports]
    rows = []
    for cid in ids:
        cases = [index[cid] for index in indexes]
        scores = [c["score"] for c in cases]
        statuses = [s["actual_status"] for s in scores]
        signatures = [signature(c) for c in cases]
        rows.append({"id": cid, "category": cases[0]["category"],
                     "expected_status": cases[0]["expected"]["status"],
                     "statuses": statuses, "strict_passes": sum(s["passed"] for s in scores),
                     "status_correct_runs": sum(s["status_correct"] for s in scores),
                     "status_agreement": len(set(statuses)) == 1,
                     "decision_agreement": len(set(signatures)) == 1,
                     "readiness": [c["result"]["coverage"]["decision_ready"] for c in cases],
                     "expected_readiness": cases[0]["expected"]["decision_ready"],
                     "pass_pattern": [s["passed"] for s in scores],
                     "failure_checks": [[k for k in ("status_correct", "required_evidence_covered", "atomic_findings_correct", "reference_integrity", "coverage_complete", "readiness_correct") if not s.get(k, True)] for s in scores],
                     "consistently_wrong_status": len(set(statuses)) == 1 and not any(s["status_correct"] for s in scores)})
    runs = []
    for number, report in enumerate(reports, 1):
        cases = report["cases"]
        runs.append({"run": number, "cases": len(cases),
                     "strict_passes": sum(c["score"]["passed"] for c in cases),
                     "correct_statuses": sum(c["score"]["status_correct"] for c in cases),
                     "correct_readiness": sum(c["score"]["readiness_correct"] for c in cases),
                     "false_positive_findings": sum(c["score"]["false_positive_findings"] for c in cases),
                     "ready_despite_expected_abstention": sum(c["result"]["coverage"]["decision_ready"] and not c["expected"]["decision_ready"] for c in cases),
                     "ready_with_wrong_status": sum(c["result"]["coverage"]["decision_ready"] and not c["score"]["status_correct"] for c in cases),
                     "ready_cases": sum(c["result"]["coverage"]["decision_ready"] for c in cases),
                     "ready_with_wrong_status_or_findings": sum(c["result"]["coverage"]["decision_ready"] and not (c["score"]["status_correct"] and c["score"]["atomic_findings_correct"]) for c in cases),
                     "incomplete_cases": sum(not c["result"]["coverage"]["complete"] for c in cases),
                     "captured_errors": sum(len(c["result"]["coverage"]["errors"]) for c in cases),
                     "model_calls": sum(len(c["calls"]) for c in cases),
                     "elapsed_seconds": round(sum(c["elapsed_seconds"] for c in cases), 3)})
    return {"runs_completed": len(reports), "unique_cases": len(ids), "runs": runs,
            "status_agreement_cases": sum(r["status_agreement"] for r in rows),
            "decision_agreement_cases": sum(r["decision_agreement"] for r in rows),
            "all_runs_passed_cases": sum(r["strict_passes"] == len(reports) for r in rows),
            "consistently_wrong_status_cases": [r["id"] for r in rows if r["consistently_wrong_status"]],
            "cases": rows}


def render(summary, manifest):
    n, repeats = summary["unique_cases"], summary["runs_completed"]
    lines = ["# Repeated evaluation of synthetic underwriting cases", "",
             f"Model: `{manifest['model']}`. **{repeats}/{manifest['planned_runs']} completed runs**, {n} unique synthetic cases per run.", "",
             "Same temperature (0), seed (42), case order, model, and implementation each run. No production changes were made between runs. This measures repeatability at the configured settings, not robustness across temperatures, seeds, or models. Cases are synthetic and not underwriter-validated. They were frozen before the first model run.", "",
             "| Run | Strict pass | Correct status | Correct readiness | False-positive findings | Ready despite expected abstention | Wrong status marked ready | Calls | Seconds |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in summary["runs"]:
        lines.append(f"| {r['run']} | {r['strict_passes']}/{n} | {r['correct_statuses']}/{n} | {r['correct_readiness']}/{n} | {r['false_positive_findings']} | {r['ready_despite_expected_abstention']} | {r['ready_with_wrong_status']} | {r['model_calls']} | {r['elapsed_seconds']:.1f} |")
    lines.extend(["", "## Consistency", "",
                  f"- Same final status in all completed runs: **{summary['status_agreement_cases']}/{n}**.",
                  f"- Same status, finding citation groups, and readiness in all runs: **{summary['decision_agreement_cases']}/{n}**.",
                  f"- Passed every completed run: **{summary['all_runs_passed_cases']}/{n}**.",
                  f"- Consistently wrong final status: **{len(summary['consistently_wrong_status_cases'])}/{n}**.", "",
                  "Agreement excludes explanation wording, subject-label wording, citation order, and generated finding IDs. Consistency is not correctness. Repeated judgments on the same cases are not independent samples of real-world accuracy.", "",
                  "## Category results", "", "| Category | Strict passes / case-runs | Correct status / case-runs |", "| --- | --- | --- |"])
    categories = sorted({r["category"] for r in summary["cases"]})
    for category in categories:
        group = [r for r in summary["cases"] if r["category"] == category]
        lines.append(f"| {category} | {sum(r['strict_passes'] for r in group)}/{len(group)*repeats} | {sum(r['status_correct_runs'] for r in group)}/{len(group)*repeats} |")
    lines.extend(["", "## Per-case outcomes", "",
                  "| Case | Expected | Actual status by run | Strict passes | Readiness by run | Decision agreement |",
                  "| --- | --- | --- | --- | --- | --- |"])
    for r in summary["cases"]:
        lines.append(f"| {r['id']} | {r['expected_status']} | {', '.join(r['statuses'])} | {r['strict_passes']}/{repeats} | {', '.join(str(v) for v in r['readiness'])} | {r['decision_agreement']} |")
    lines.extend(["", "## Failure diagnostics", ""])
    for r in summary["cases"]:
        if r["strict_passes"] < repeats:
            failures = "; ".join(f"run {i}: {', '.join(checks)}" for i, checks in enumerate(r["failure_checks"], 1) if checks)
            lines.append(f"- **{r['id']}**: {failures}.")
    lines.extend(["", "## Method and limits", "",
                  "Gold statuses, readiness, required evidence, findings, and any acceptable citation alternatives were authored before inference. Strict scoring checks status, one-to-one finding citation groups, required references, reference integrity, complete coverage, and labeled readiness. It does not automatically prove the explanation's semantic correctness. Alternative citation sets are predeclared; the scorer does not invent them after seeing outputs.", "",
                  "Each case has one criterion and a small set of already-extracted prose observations. The scenarios include realistic operational detail but do not represent complete submissions, independent expert labels, document extraction, multi-criterion batches, or large-context performance. The set was authored by the same assistant that developed the system. It is fresh regression evidence, not a blinded external benchmark. Identical temperature/seed runs may repeat exactly due to deterministic inference. Warm model/cache conditions affect latency.", "",
                  "See `manifest.json` for frozen hashes and run settings, `summary.json` for metrics, and each `run-NN.json` / `.md` for complete inputs, model calls, proposals, reviews, and reasons. Logs preserve execution progress. No model call receives gold expectations.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path("evals/unseen_cases_v1.json"))
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--model", default="qwen3-coder:30b")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.runs < 2:
        parser.error("At least two runs are required")
    if args.output.exists():
        parser.error("Output directory already exists; preserve previous runs by choosing a new directory")
    repo = Path(__file__).resolve().parents[1]
    dataset = json.loads(args.cases.read_text(encoding="utf-8"))
    validate_cases(dataset)
    if any("decision_ready" not in c["expected"] for c in dataset["cases"]):
        parser.error("Repeated suite requires gold readiness labels")
    files = [args.cases.resolve(), Path(__file__).resolve(), repo / "evals/run.py",
             repo / "src/tiny_skill_agent/assessment.py", repo / "src/tiny_skill_agent/adapters.py"]
    def hashes():
        return {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    frozen = hashes()
    manifest = {"state": "running", "started_at": datetime.now(timezone.utc).isoformat(),
                "planned_runs": args.runs, "case_count": len(dataset["cases"]), "model": args.model,
                "model_settings": {"temperature": 0, "seed": 42, "num_ctx": 8192, "num_predict": 4096},
                "case_order": [c["id"] for c in dataset["cases"]], "frozen_sha256": frozen,
                "status_distribution": dict(Counter(c["expected"]["status"] for c in dataset["cases"])),
                "gold_not_expert_validated": True}
    args.output.mkdir(parents=True)
    def save_manifest():
        (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    save_manifest()
    reports = []
    for number in range(1, args.runs + 1):
        if hashes() != frozen:
            raise RuntimeError("Frozen files changed; refusing to mix implementations or datasets")
        path = args.output / f"run-{number:02d}.json"
        print(f"RUN {number}/{args.runs}", flush=True)
        with path.with_suffix(".log").open("w", encoding="utf-8") as log:
            process = subprocess.Popen([sys.executable, "-m", "evals.run", "--cases", str(args.cases.resolve()),
                                        "--model", args.model, "--output", str(path.resolve())], cwd=repo,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
            for line in process.stdout:
                log.write(line)
                log.flush()
                if line.startswith(("RESULT", "Saved")):
                    print(f"[{number}] {line.strip()}", flush=True)
            code = process.wait()
        if code != 0 or hashes() != frozen:
            manifest["state"] = "failed"
            save_manifest()
            raise RuntimeError(f"Run {number} failed or frozen files changed; see saved log")
        reports.append(json.loads(path.read_text(encoding="utf-8")))
        summary = summarize(reports)
        (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        (args.output / "summary.md").write_text(render(summary, manifest), encoding="utf-8")
    manifest["state"] = "completed"
    manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
    save_manifest()
    print(f"COMPLETED: {args.output / 'summary.md'}", flush=True)


if __name__ == "__main__":
    main()
