# Fresh synthetic underwriting evaluation, version 1

## Protocol fixed before inference

This set adds 32 newly authored scenarios beyond the 12 earlier development cases. It covers property, cyber, commercial auto, general liability, and workers' compensation. All businesses, rules, thresholds, and facts are invented. The cases were authored by the same assistant that implemented the assessment API; they are not a blinded external or underwriter-validated benchmark. They were not previously run through the model or used to tune production prompts/code.

The authoring source is [build_unseen_cases.py](build_unseen_cases.py). Its output [unseen_cases_v1.json](unseen_cases_v1.json) was generated once, validated, and frozen before the first evaluation. Regeneration refuses to overwrite it. Labels and permitted citation alternatives are not adjusted after seeing model outputs. Production assessment and adapter files also remain unchanged across all three runs. The runner records and checks file hashes before and after every run to prevent mixing versions.

## Scenarios

- Missing information: workforce MFA, fire-pump servicing, driver screening, subcontractor insurance limits.
- Quantitative boundaries: collision frequency, reserve months, exact roof-age and patch-coverage thresholds.
- Conflicts and timing: incompatible reports, corrected mileage, historical impairment followed by repair.
- Exceptions and applicability: documented rewiring, service-account controls, operational scope exclusions.
- Multiple findings and corroboration: independent buildings/drivers/applications versus two reports of one event.
- Entity/period alignment: sister companies, prior-year controls, building-specific rules, partial-year payroll.
- Documents versus activities: missing required submission documents versus missing evidence that an activity occurred.
- Cross-source synthesis: conjunctive requirements, claim deduplication, elapsed time across midnight, expired exceptions.

Evidence consists of short report/email/log-style passages with explicit subject, period, and contextual detail. Each case evaluates one criterion against already-extracted evidence. The set does not simulate entire submission packages, extraction failures, unbounded context, or simultaneous multi-criterion assessment.

## Repetition settings

Three fresh evaluations use the existing local `qwen3-coder:30b` with temperature 0, seed 42, context 8,192, output cap 4,096, unchanged case order, and default assessment configuration. No previous case/run results are fed into subsequent calls. Ollama remains warm between runs. Identical seed/temperature evaluates reproducibility under these settings; it does not estimate sensitivity to sampling seeds, shuffled source order, alternate models, or stochastic temperatures.

```powershell
.venv\Scripts\python -m evals.repeat --runs 3 --output evals/results/unseen-v1-three-runs
```

Use a new output directory for subsequent repetitions. The runner refuses to overwrite prior artifacts. Each case is checkpointed by the existing evaluator; each completed run produces full JSON, Markdown, and an execution log. The summary updates after each completed run and clearly states how many planned runs finished.

## Frozen scoring

Gold labels specify the final status, expected decision readiness, required citations, and independent findings. Strict pass requires all existing checks plus the expected readiness value. Finding records are matched one-to-one to gold citation sets. Some corroboration/history scenarios explicitly permit alternative citation sets; these are declared in the frozen dataset, not inferred after the run. Existing fixtures without alternatives retain their exact-set scoring. No model receives gold labels or rationale.

Accuracy and consistency are separate:

- **Status accuracy:** how often the final status matches the gold label.
- **Strict accuracy:** status, citations, atomic findings, reference integrity, coverage, and readiness all pass.
- **Readiness accuracy:** `decision_ready` matches the case's expected readiness.
- **False-positive findings:** findings emitted for a case whose gold status is nonmatched.
- **Status agreement:** a case receives the same final status in every run, whether right or wrong.
- **Decision agreement:** final status, finding citation groups, and readiness agree across runs. Wording, ordering, and generated IDs are excluded.
- **Consistently wrong:** a stable final status disagrees with gold in every run.
- **Ready despite expected abstention:** a case labeled insufficient evidence nonetheless becomes decision ready.

Automated matching is not a semantic grade of explanations. Strict citation failures may reflect a different citation choice rather than an incorrect underwriting conclusion; per-case diagnostics and explanations are retained for review. Repeated results on the same 32 cases do not increase the number of independent cases to 96. No population accuracy confidence interval is warranted from this nonrepresentative synthetic set.

## Results

See [the repeated-run summary](results/unseen-v1-three-runs/summary.md), [machine-readable metrics](results/unseen-v1-three-runs/summary.json), and [frozen manifest](results/unseen-v1-three-runs/manifest.json). Each run's complete trace and report are in that folder. The original baseline and all development-set runs remain preserved separately.

Completed results: **17/32, 16/32, 16/32 strict passes** and **20/32, 19/32, 19/32 correct statuses**. Decisions agreed across all runs for 31/32 cases, but only 16/32 passed every run. Each run included six incorrect statuses marked decision ready. See [the manual failure analysis](results/unseen-v1-three-runs/interpretation.md) for arithmetic, criterion-polarity, exception, source-combination, and validation failures. No production fixes were made during this evaluation.
