# Guideline extraction and consistency: regression comparison

**Completed and verified.** The core assessment improves on the repeated case set, and longer-document criterion recall improves. Short-guideline extraction regresses, and the long-document readiness gate holds every case. These changes should not be treated as an overall production-readiness improvement. All changes remain uncommitted.

## Changes

- Unlabelled guideline extraction reviews every remaining nonempty source line, including lines without classification words. Already parsed labelled rules retain deterministic coverage. Line reviews precede outcome extraction in the structured schema. Each review links its substantive rules to exact source quotations.
- An implicit criterion can carry a separate `classification_quote` from the same source, preserving the rule quotation and the guideline's own mapping to `strength` or `concern`. An outcome word alone is not assigned a hardcoded underwriting classification.
- Extraction has one bounded structural/quotation repair attempt by default. Explicitly declared ambiguity fails closed. Line coverage and exact quotation checks are deterministic; deciding which lines contain rules and whether a classification mapping is meaningful remains a model task.
- The final consistency review checks the delivered assessment and active explanation against original criteria and evidence. Issues reference explanation section IDs. Exact scope/exception quotations from the rule or its same-source context and applicability/status compatibility are checked in Python. Missing, uncertain, invalid or adverse reviews block `decision_ready`.
- A focused negative review that changes the decision archives the superseded predicate explanation, avoiding two opposing rationales in the active explanation. The history remains available for audit.
- Prompts distinguish scope exclusions, failed conditions, missing records, unresolved contradictions, exceptions, strict thresholds, and collective versus individual findings. These instructions improve behavior but do not guarantee it.

## Integration and cost

No dependency, external service, retrieval layer, middleware lifecycle, or agent loop was added. The standard LangChain adapter handles the new review stage. The core still accepts a model callable and portable Pydantic inputs; the existing optional completion middleware uses the same API.

This is not zero-cost verification: the consistency check adds one model call per assessed criterion, subject to the existing bounded retry policy. Extraction may use one additional repair call. Disabling consistency review produces provisional results, not a shortcut to `decision_ready`.

Custom model callables must support `stage="consistency_review"`; custom extractors must provide the new `reviewed_lines` and classification mapping fields. See [integration guidance](../../docs/INTEGRATION.md). Existing standard adapters handle these changes. `coverage.complete` retains its source/assessment coverage meaning; readiness additionally requires successful consistency review.

## Protocol and interpretation

All suites use the local `qwen3-coder:30b`, temperature 0 and seed 42, preserving each suite's baseline context/output settings, fixtures and scoring. The long-document suite uses 32,768/8,192 tokens; the core and 32-case suites use 8,192/4,096. The final code is frozen across all three repeated 32-case runs.

The six long-document cases contain 18 criteria (11 explicit, seven implicit) and about 2,042–2,084 words of guideline/application text per case. These fixtures have now informed development: this is a regression comparison, not a fresh held-out estimate. All cases are synthetic and author-labelled, without independent underwriter validation. Three repeats of 32 cases are 96 case-runs, not 96 independent examples.

The automatic explanation judge is unchanged and uses the same local model. Its exact-excerpt format failures leave explanations ungraded, and it can miss semantic contradictions. A separate assistant audit uses the same five-dimension rubric as the baseline, explicitly identifies its reviewer, and preserves automatic scores. It is not blinded expert grading.

## Longer-document results

The final run is `2026-10-19-guideline-consistency-release-documents`. Earlier runs are retained diagnostics.

| Metric | Before | After |
| --- | --- | --- |
| Complete usable criterion inventories | 2/6 | 6/6 |
| Criteria extracted | 8/18 | 18/18 |
| Implicit criteria extracted | 0/7 | 7/7 |
| Correct final statuses | 7/18 | 17/18 |
| Correct finding sets, including empty sets | 8/18 | 17/18 |
| Complete pipeline coverage | 2/6 | 3/6 |
| All ready cases | 2/6 | 0/6 |
| Ready cases with wrong status or finding set | 1 | 0 |
| Automatic strict case passes | 1/6 | 1/6 |
| Produced explanations passing assistant audit | 3/8 | 15/18 |
| Expected explanations passing assistant audit | 3/18 | 15/18 |
| Automatic judge: graded / ungraded / missing | 3 / 5 / 10 | 12 / 6 / 0 |
| Assessment model attempts | 33 | 87 |
| Extraction model attempts | 6 | 6 |
| Production seconds | 280.2 | 641.3 |
| Separate explanation-judge seconds | 46.0 | 99.0 |

**Extraction and status recall improve, but readiness is overconservative.** Zero incorrect-ready results is achieved with zero ready cases; it does not demonstrate reliable selective accuracy. Four cases are decidable under the fixture gold, yet all are held. The contractor rescue-drill error observed during development is corrected: requested-but-unsupplied records yield `insufficient_evidence`, not a confirmed negative.

The previous hotel pool error is corrected to `not_applicable`. Roof replacement, missing driver-review records, the strict 30-day threshold, and the contractor documentation requirement are explained more consistently. Three explanations still fail the assistant audit: cyber confuses refutation of a rule with conflicting evidence; fleet treats a disputed brake defect as established; manufacturing reverses the open-container trigger. The production critic catches the first two but misses the third.

| Case | Final outcome and reason for hold |
| --- | --- |
| Property | All statuses correct; collective sprinkler strength split into three findings. Roof predicate/consistency reviews fail validation, blocking readiness. The accepted critic does not catch sprinkler granularity. |
| Cyber | MFA should be `no_match`, but the model returns `insufficient_evidence` by treating 23/24 versus an every-account rule as conflicting evidence. Critic flags it. |
| Fleet | All statuses correct; unresolved inspections and missing records legitimately require abstention. One source assessment also fails validation; brake explanation remains inconsistent. |
| Manufacturing | All statuses and finding sets correct, but one source assessment fails validation. Critic misses the reversed trigger wording. |
| Hospitality | All statuses and finding sets correct. Critic falsely claims exactly 30 satisfies more-than-30 and holds a sound threshold explanation. |
| Contractor | All statuses and findings correct. Missing drill records correctly require abstention. Critic also questions this sound missing-evidence explanation. |

Relative to the assistant audit, the production critic has 17 valid reviews: it flags two flawed explanations and three adequate ones, accepts one flawed explanation and 11 adequate ones, and leaves one additional review unverified. These are small, author-reviewed counts, not independently validated critic precision/recall. The gate reduces readiness but does not certify reasoning.

The automatic strict score remains 1/6. In the baseline it passed property while missing a contradictory explanation; in the final run it passes contractor. Requiring the assistant-audited explanations alongside objective correctness, coverage and expected readiness yields **0/6 before and 1/6 after**. The assistant audit is a separate measurement; stored automatic scores remain unchanged. All 12 automatically graded final explanations receive passing grades, including fleet's flawed brake explanation, so the judge remains unreliable.

Production time increases 2.29 times while assessed criteria increase from eight to 18. The ratio combines greater coverage, more reviews and retries; it is not a controlled estimate of consistency-review overhead. Local wall-clock latency is observational.

Reports: [before](2026-10-19-heldout-long-documents.md), [after](2026-10-19-guideline-consistency-release-documents.md), [baseline explanation audit](2026-10-19-heldout-explanation-audit.json), [updated explanation audit](2026-10-19-guideline-consistency-release-explanation-audit.json).

## Repeated 32-case assessment API evaluation

Counts are run 1 / run 2 / run 3, with the same 32 cases each time.

| Metric | Before | After |
| --- | --- | --- |
| Strict passes / 32 | 19 / 21 / 20 | 22 / 22 / 22 |
| Correct statuses / 32 | 28 / 28 / 28 | 30 / 30 / 30 |
| Correct readiness / 32 | 20 / 21 / 20 | 22 / 22 / 22 |
| Ready cases | 10 / 11 / 10 | 12 / 12 / 12 |
| Wrong status or findings marked ready | 1 / 0 / 0 | 0 / 0 / 0 |
| Ready despite expected abstention | 0 / 0 / 0 | 0 / 0 / 0 |
| False-positive findings | 1 / 1 / 1 | 0 / 0 / 0 |
| Incomplete cases | 0 / 1 / 1 | 1 / 1 / 1 |
| Model calls | 154 / 155 / 154 | 197 / 197 / 197 |
| Seconds | 509.3 / 503.9 / 499.0 | 683.9 / 736.4 / 691.3 |

**Correct statuses improve from 84/96 to 90/96 case-runs; strict passes improve from 60/96 to 66/96.** Incorrect-ready results fall from one to zero while ready case-runs rise from 31 to 36. Those 36 ready case-runs are the same 12 unique cases repeated three times. This is evidence on a small synthetic regression set, not an estimated production error rate.

Status agreement across runs remains 32/32 → 32/32. Agreement on status, finding citation groups and readiness improves 29/32 → 32/32. Explanation wording and subject-label wording are excluded from that signature. Repetition can stabilize incorrect judgments.

The patch-percentage boundary, electrical exception and explicit non-occurrence cases are corrected in all three final runs. Two status errors remain in every run:

- `property_building_specific_scope`: an explicit scope exclusion is still called `no_match` rather than `not_applicable`. Independent-review disagreement blocks readiness; the new critic accepts the incorrect scope interpretation.
- `wc_document_absence_is_concern`: an explicit concern about missing required documentation is missed and called `no_match`. This is a new false negative compared with the baseline. It is held from readiness.

Eight other conclusive cases per run have correct statuses/findings but remain held. One has incomplete source coverage; other holds arise from review disagreement or consistency checks. Strict scoring includes expected readiness, so those conservative holds are failures. False-positive findings are eliminated on this set, but the missed documentation concern remains important.

The three runs use 591 calls versus 463 before (+28%) and take 2,111.6 seconds versus 1,512.2 seconds (about 1.40 times). All cases have pre-extracted criteria and evidence, so this comparison isolates the assessment layer better than the document suite. It still uses observational local timings.

Reports: [baseline three runs](unseen-v1-combined-review-three-runs/summary.md), [updated three runs](guideline-consistency-release-three-runs/summary.md).

## Original small suites

| Suite | Statuses before → after | Strict passes before → after | Ready cases before → after | Calls before → after | Seconds before → after |
| --- | --- | --- | --- | --- | --- |
| Original eight | 8/8 → 8/8 | 8/8 → 7/8 | 4 → 4 | 36 → 44 | 104.9 → 175.3 |
| Four sufficiency contrasts | 3/4 → 3/4 | 3/4 → 3/4 | 1 → 1 | 15 → 19 | 33.7 → 49.5 |

Both suites have zero wrong statuses marked ready before and after. Their strict scores do not include gold readiness. The original-suite regression is `exception_qualifies`: the correct `no_match` result is held because one source assessment fails validation. The contrast failure remains `explicit_activity_did_not_occur`: the model mistakes an explicit negative fact for an unresolved evidence conflict. An intermediate 4/4 contrast result is preserved but is not the final implementation's score.

Reports: [original eight before](2026-10-18-reviewed-core-final.md), [after](2026-10-19-guideline-consistency-release-core.md); [contrasts before](2026-10-18-reviewed-contrasts-final.md), [after](2026-10-19-guideline-consistency-release-contrasts.md).

## End-to-end documents and case isolation

| Metric, across two profiles | Before | After |
| --- | --- | --- |
| Criteria extracted | 14/14 | 8/14 |
| Correct final statuses | 14/14 | 8/14 |
| Correct finding sets | 14/14 | 6/14 |
| Strict passes | 10/14 | 6/14 |
| Complete pipeline coverage | 13/14 | 8/14 |
| Ready turns | 6/14 | 4/14 |
| Incorrect-ready turns | 0 | 0 |
| Extraction errors | 0 | 6 |
| Assessment / extraction attempts | 52 / 2 | 39 / 20 |
| Seconds | 210.1 | 164.8 |

Both profiles have identical final totals: 4/7 statuses, 3/7 finding sets, and 3/7 strict passes. This is a **regression in availability and end-to-end accuracy**. In each profile, all three cyber turns fail extraction because the model promotes counting definitions and evidence-handling advice into separate outcome criteria, then invents or omits their classification mapping. Exact-source validation rejects them. It does not silently accept invented criteria, but it loses an otherwise usable assessment. All documents were retrieved in all 14 turns.

All eight produced assessments contain only permitted case sources, with no foreign citations. Four of eight cross-case transitions have verified isolated assessments; the other four lack an assessment because extraction failed. This is not evidence of leakage, nor a full isolation pass. Property's two-building findings use citation groups that differ from the exact fixture targets, producing two additional finding-set failures; both turns are held.

The lower runtime is caused by six early extraction failures, not an efficiency improvement. The ordinary-prose roof guideline and property follow-up both pass in both profiles. The valid same-source context quotation rejection seen during development is fixed.

Reports: [before](2026-10-19-e2e-explicit-scope-prose.md), [after](2026-10-19-guideline-consistency-release-e2e.md).

## Preserved development diagnostics

All earlier `guideline-consistency-documents*`, `guideline-consistency-final-documents*`, `guideline-consistency-complete-documents*`, non-release core/contrast/E2E reports, and `consistency-calibration.json` are development diagnostics. Their JSON states identify completed or interrupted runs; interrupted reports include only completed cases. Some names contain `final`, `complete`, or `verified`; only the **release-prefixed reports and release-three-runs directory** belong to this final comparison. No diagnostic is substituted for a final result.

They record extraction schema compliance problems, missing mapping quotations, overly skeptical critique prompts, rejection of valid same-source context quotations, and collective finding fragmentation. The final revision requires full line reviews, removes a redundant line-kind field, uses explanation section IDs, permits exact same-source context clauses, and distinguishes documentary existence from submission. A small generic example distinguishes operational guidance from outcome rules. The six short-cyber extraction failures remain despite those changes. Gold labels, documents and scoring were not changed to fit outputs.

## Verification

- **120 unit/integration/scoring tests pass** with `.venv\Scripts\python -m unittest discover -s tests`.
- All 122 produced `AssessmentResult` objects revalidate; all 128 saved case/turn scores recompute exactly. Six E2E extraction failures have no assessment object and remain scored failures.
- The three-run aggregate summary recomputes exactly from the 96 saved cases.
- Frozen runtime, corpus and scorer hashes match final manifests. Baseline fixture/scorer content, case order, model digest and settings are preserved. Older raw hash differences were verified as line-ending conversion; the 32-case dataset is byte-identical.
- Exact rule/classification quotations and all 18 assistant-audit excerpts were checked against their saved source/explanation text.
- No scoring-only keys occur in 806 recorded production assessment/extraction payloads. Separate evaluation-only judge calls intentionally receive reference answers.
- `git diff --check` passes. No production dependencies or middleware lifecycle changes were introduced.

See [the verification record](2026-10-19-guideline-consistency-verification.json). Valid quotations and IDs establish provenance, not semantic entailment. These tests do not cover OCR/PDF layout recovery or production-scale context lengths.

## Reproduce

From the repository root with the project environment and local Ollama running, choose fresh paths so previous results are preserved:

```powershell
.venv\Scripts\python -m unittest discover -s tests
.venv\Scripts\python -m evals.run --output evals/results/new-core.json
.venv\Scripts\python -m evals.run --cases evals/sufficiency_cases.json --output evals/results/new-contrasts.json
.venv\Scripts\python -m evals.e2e --hardened --output evals/results/new-e2e.json
.venv\Scripts\python -m evals.holdout --output evals/results/new-documents.json
.venv\Scripts\python -m evals.repeat --runs 3 --output evals/results/new-three-runs
```

The final implementation is a small, source-aware assessment extension, with improved recall and core decisions on these fixtures. The next unresolved issues are separating operational guidance from outcome criteria reliably, reducing false holds without weakening safety, and validating explanations with stronger independent evaluation. The present `decision_ready` flag is not a correctness certificate.
