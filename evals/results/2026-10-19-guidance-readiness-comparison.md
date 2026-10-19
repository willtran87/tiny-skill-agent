# Operational guidance and readiness: regression comparison

**Completed and verified.** Operational-guidance extraction is recovered. Gold-decidable holds fall from 10 to 8 per repeated run, while observed incorrect-ready results remain zero in the final evaluations. Some conservative holds and two status errors remain.

## Revision

- The standard LangChain extractor reviews the whole source, including known labelled outcomes. Each line is classified as context, outcome rule, or unresolved before rules are emitted. Required object keys bind every source line and a dynamic enum binds allowed labels. Code translates this to the existing extraction contract and deduplicates known criteria. Operational advice remains in full source context. Ambiguous actual rules still fail extraction.
- The standard LangChain case inference reads original evidence and review-candidate IDs. Custom assessment-callable payloads remain compatible. Provisional source opinions remain in the result audit trail but no longer anchor the case inference.
- Combining complementary evidence can change a partial-source decision without fabricating a conflict. Required review citations remain enforced. Mixed conclusive source judgments and unresolved source conflicts still require a non-`none` resolution.
- The LangChain adapter describes evidence-batch coverage separately from the rule applicability predicate. The consistency schema places its rationale before its verdict and distinguishes an unrestricted subject from unknown applicability.

No new dependency, model stage, external service, middleware lifecycle change, or agent-loop change. The core callable and custom extraction response contracts remain compatible; custom callable payloads retain provisional source assessments; the standard adapter omits them from model inference.

## Safety gates retained

Exact criterion/mapping quotations, source-line coverage, case isolation, evidence allowlists, source coverage, predicate/status validation, negative-evidence review, independent status and finding-citation agreement, and final explanation consistency remain required. Missing or adverse reviews still hold readiness. The code does not promote results by dropping unknown or adverse reviews.

## Protocol

Compare against the immediately preceding `guideline-consistency-release` reports. Same local `qwen3-coder:30b`, temperature 0, seed 42, suite-specific context/output settings, fixtures and scorers. Source/evaluation hashes are frozen in `2026-10-19-guidance-readiness-validated-manifest.json` for the final runs. Earlier `probe`, initial, and `release` reports are diagnostics and excluded from final metrics; final reports use `validated`. The first document rerun was interrupted after a malformed fleet extraction; required line keys and an allowed-label enum address that format failure.

These synthetic cases have informed development; they are regression tests, not fresh held-out evidence or independent underwriter validation. Three repeated runs reuse the same 32 cases. Exact citation checks do not establish semantic truth. The automatic explanation judge uses the same local model and can miss errors or fail formatting.


A subsequent diagnostic recovered all long-document criteria but incorrectly marked
the contractor case ready: correlated reviewers treated unsupplied records as
proof that a documented drill did not exist. The final revision adds two structured
evidence distinctions within the existing negative review and a deterministic
nonreceipt guard. A focused replay returns insufficient evidence. The final full
evaluations below include this correction; the diagnostic unsafe result is retained.


## Completed suite comparison

The baseline is the immediately preceding release, not the original first-use results.

| Metric | Before | After |
| --- | --- | --- |
| Core strict passes / 8 | 7 | 8 |
| Contrast strict passes / 4 | 3 | 4 |
| End-to-end extracted criteria / 14 | 8 | 14 |
| End-to-end correct statuses / 14 | 8 | 14 |
| End-to-end correct finding sets / 14 | 6 | 12 |
| End-to-end strict passes / 14 | 6 | 10 |
| Long-document criteria / 18 | 18 | 18 |
| Long-document implicit criteria / 7 | 7 | 7 |
| Long-document correct statuses / 18 | 17 | 18 |
| Long-document correct finding sets / 18 | 17 | 17 |
| Long-document automatic strict cases / 6 | 1 | 1 |
| Long-document complete pipelines / 6 | 3 | 3 |

### Readiness, including availability

| Suite | Ready before / after | Incorrect-ready before / after |
| --- | --- | --- |
| core | 4 / 4 | 0 / 0 |
| contrasts | 1 / 2 | 0 / 0 |
| e2e | 4 / 6 | 0 / 0 |
| documents | 0 / 1 | 0 / 0 |

All six failed short cyber extractions are recovered across both conversation profiles.
Missing counts remain insufficient; supported follow-ups can become ready. All 14
final end-to-end assessments are isolated, with no foreign input or cited sources.
The baseline produced eight isolated assessments; six failed extraction before
assessment, rather than leaking case evidence.

The two property turns still fail gold finding-citation checks. Both unlabelled-rule
turns extract correctly but are held for differing finding citation groups between
case assessment and independent review. The agreement gate is retained.

The long-document cyber case is now correct and ready. Contractor correctly abstains
on requested-but-unsupplied rescue-drill records. Property still fragments a
collective sprinkler finding and has invalid exception reviews. Manufacturing has
incomplete source coverage. Hospitality's final result and consistency review are
correct, but initial-versus-independent disagreement still holds it. Fleet has
legitimate insufficient-evidence outcomes and an additional coverage failure.

### Explanation measurement limitation

The unchanged automatic judge graded 6/18 explanations, down from 12/18; the other
12 have judge-format errors, principally noncontiguous quoted excerpts. Ungraded
is not a semantic failure or a semantic pass. No new blinded or expert explanation
audit was performed, and no claim of improved overall explanation quality is made.
The six graded explanations pass the automatic rubric, which is still a fallible
same-model evaluator. Stored scores and gold were not altered.

### Model attempts and observed time

| Suite | Assessment attempts before / after | Extraction attempts before / after | Production seconds before / after |
| --- | --- | --- | --- |
| core | 44 / 42 | 0 / 0 | 175.3 / 143.6 |
| contrasts | 19 / 19 | 0 / 0 | 49.5 / 44.7 |
| e2e | 39 / 67 | 20 / 14 | 164.8 / 292.3 |
| documents | 87 / 91 | 6 / 7 | 641.3 / 639.1 |

End-to-end assessment work increases because six additional turns now reach
assessment. The extraction attempts fall from 20 to 14. These wall-clock times
are observations on one local machine, not controlled speed benchmarks.

## Repeated 32-case assessment comparison

All three final runs completed on the same frozen implementation and model settings.
Counts are run 1 / run 2 / run 3; these are 32 reused cases, not 96 independent examples.

| Metric | Before | After |
| --- | --- | --- |
| Strict passes / 32 | 22 / 22 / 22 | 24 / 24 / 24 |
| Correct statuses / 32 | 30 / 30 / 30 | 30 / 30 / 30 |
| Correct readiness / 32 | 22 / 22 / 22 | 24 / 24 / 24 |
| Ready cases | 12 / 12 / 12 | 14 / 14 / 14 |
| Ready with wrong status or findings | 0 / 0 / 0 | 0 / 0 / 0 |
| Ready despite required abstention | 0 / 0 / 0 | 0 / 0 / 0 |
| False-positive findings | 0 / 0 / 0 | 0 / 0 / 0 |
| Incomplete cases | 1 / 1 / 1 | 1 / 1 / 1 |
| Validation/provider errors captured | 37 / 37 / 37 | 20 / 20 / 20 |
| Model attempts | 197 / 197 / 197 | 181 / 181 / 181 |
| Gold-decidable cases held | 10 / 10 / 10 | 8 / 8 / 8 |

Status agreement: **32/32**; decision agreement: **32/32** across three runs (both 32/32 before). Decision signatures compare final statuses, finding citation groups, and readiness; they do not certify identical wording or explanation quality.

Total model attempts: **591 → 543**. Observed total assessment time: **2111.6 → 1713.5 seconds**.

Gold-decidable held means the fixture expects a conclusive, ready assessment but
readiness is false. It includes incorrect/provisional results and failed reviews;
it does not mean the final gate should simply be bypassed. The net reduction is
10 to 8 per run (20%). All ready results also pass the full scored checks, including
required citations, rather than only the status/finding checks in the summary table.

### Recoveries and regressions

Four cases become correctly ready in every run:

- `auto_incident_rate_calculation`
- `auto_mileage_corrected_denominator`
- `wc_document_absence_is_concern`
- `property_cross_source_alarm_and_value`

Two previously ready cases acquire conservative holds:

- `gl_document_submission_condition`: correct negative decision, consistency hold.
- `wc_activity_explicitly_not_performed`: correct negative decision, invalid independent review.

The missing-document concern changes from incorrect `no_match` to correct `matched`.
The service-account exception changes from correct-but-held `no_match` to incorrect
`insufficient_evidence`: its reviewer recognizes exception facts but still abstains.
The building-scope case remains incorrectly `no_match` rather than `not_applicable`.
Both wrong statuses are held. Overall status accuracy therefore remains 30/32.

Other holds remain on multiple warehouse concerns, expired licences, duplicate-claim
aggregation, and a restore spanning midnight. Missing initial assessments, invalid
reviews, citation disagreements, or consistency objections remain visible and block
readiness. This is a modest net readiness improvement, not elimination of false holds.

## Verification and scope

- 127 unit/integration tests pass; whitespace validation passes.
- All 128 final saved assessment results validate against the output models.
- All 128 scores and the three-run summary recompute exactly.
- All 55 ready case-runs pass their scored checks; repeated cases are counted repeatedly.
- All 18 long-document rules and their nonempty mapping quotes resolve to the source.
- 783 assessment/extraction payloads contain no benchmark-only gold keys.
- Final source hashes match the frozen manifest; fixtures/scorers and model digest/settings match the baseline checks.
- Middleware lifecycle, agent loop, dependency manifests, and custom callable signatures are unchanged. Custom review metadata fields are optional; the standard provider schema requires them.

The nonreceipt safeguard depends on model-selected evidence categories. It improves
this measured failure but is not a proof of semantic support. Findings and reasons
still require human scrutiny where the report identifies disagreements or uncertainty.
Changes remain uncommitted.

## Reproduction

Choose fresh output paths; the runners refuse to overwrite prior results.

```powershell
.venv\Scripts\python -m unittest discover -s tests
.venv\Scripts\python -m evals.run --output evals/results/new-core.json
.venv\Scripts\python -m evals.run --cases evals/sufficiency_cases.json --output evals/results/new-contrasts.json
.venv\Scripts\python -m evals.e2e --hardened --output evals/results/new-e2e.json
.venv\Scripts\python -m evals.holdout --output evals/results/new-documents.json
.venv\Scripts\python -m evals.repeat --runs 3 --output evals/results/new-three-runs
```

## Final report files

- [Core](2026-10-19-guidance-readiness-validated-core.md)
- [Contrasts](2026-10-19-guidance-readiness-validated-contrasts.md)
- [End-to-end](2026-10-19-guidance-readiness-validated-e2e.md)
- [Long documents](2026-10-19-guidance-readiness-validated-documents.md)
- [Repeated runs](guidance-readiness-validated-three-runs/summary.md)
- [Metrics](2026-10-19-guidance-readiness-metrics.json)
- [Verification](2026-10-19-guidance-readiness-verification.json)
