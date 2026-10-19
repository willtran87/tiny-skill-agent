# Interpretation of the fresh-case evaluation

Use [summary.md](summary.md) for final run counts and consistency metrics. This document records a manual reading of representative failures, primarily from [run 1](run-01.md), with the full inputs and rejected attempts in [its JSON trace](run-01.json). No runtime changes were made in response to these results.

## The earlier perfect score did not generalize

All three runs completed with the frozen dataset, implementation, model digest, and settings verified. Results were **17/32, 16/32, and 16/32 strict passes** and **20/32, 19/32, and 19/32 correct final statuses**. Final status/finding-citation/readiness signatures agreed for **31/32** cases; **16/32** passed every run. Twelve cases consistently failed the status check, including two with no accepted case assessment. The MFA case passed in run 1 but had no accepted case assessment in runs 2 and 3.

Every run had **six cases marked ready with an incorrect status**, including **one case that should have abstained for missing annual data**, and **two false-positive findings**. Readiness matched gold in 24/32 cases per run. Incomplete source/case coverage affected six cases in run 1 and seven in each later run. Across the three runs there were 362 model calls and approximately 11.2 minutes of measured assessment time. All **58 unit/integration/scoring tests pass**; these tests check implementation behavior and do not substitute for the model evaluation.

The larger set exposes substantive judgment errors in addition to malformed responses. High agreement across repeated runs must not be read as high accuracy. The new cases and expected answers were frozen before the first inference call; labels were not changed to accommodate model outputs.

## Observed failure types

| Type | Example | Observation |
| --- | --- | --- |
| Arithmetic and combining sources | `auto_mileage_corrected_denominator` | The model recognized the corrected two-million-mile denominator, but still claimed three collisions exceeded two per million. The correct rate is 1.5 per million. |
| Missing a supplied fact | `auto_incident_rate_calculation` | The case explanation claimed the collision count was unavailable, although the case payload included both the count and active-fleet denominator. |
| Explanation/status disagreement | `property_electrical_exception` | The explanation said documented complete rewiring removed the concern, while the structured result returned `matched` and a concern. Enum consistency alone cannot catch this semantic inconsistency. |
| Criterion polarity | `wc_document_absence_is_concern` | Confirmed absence of the required submission document should satisfy the concern criterion. The case and negative reviewer instead treated absence as support for `no_match`. |
| Exception validity | `property_expired_exception_certificate` | The model correctly explained that expired approval could not satisfy the exception, but selected `no_match`; the reviewer also approved that negative decision. |
| Applicability versus incomplete evidence | `wc_partial_payroll_period` | Partial-year payroll was labeled `not_applicable`, rather than insufficient evidence for an applicable annual rule. This incorrect status was decision ready. |
| Duplicate findings | `property_later_repair_does_not_rewrite_history` | The case returned two findings for one historical impairment and its later repair, despite correctly describing the historical state. |
| Overly broad conflict candidates and failed repair | `auto_multiple_expired_licences` | Two expired drivers and one valid driver legitimately differ. The detector required a different-scope review, but the model repeatedly omitted it; validation rejected the entire case output. |
| Incomplete source coverage despite a correct final conclusion | `property_alarm_equal_reports`, `gl_loss_aggregation_without_duplicate` | Final status/reason or findings were correct, but a source response repeatedly violated the schema. Coverage remained incomplete, so strict scoring failed and readiness was blocked. |

The cited shortcomings were observed in these traces. They do not establish how often each failure occurs in real underwriting submissions.

## What the safeguards do and do not establish

Source IDs, citation expansion, status/basis consistency, nested-finding structure, and review requirements enforce useful mechanical constraints. Rejected responses are retained, and missing/invalid assessments block readiness. Those behaviors are functioning in cases with incomplete source or case outputs.

However, two model-selected fields can agree with each other while both disagree with the explanation and facts. A focused reviewer using the same model can also repeat the criterion-polarity error. A `matched` or `not_applicable` decision does not go through the negative-evidence review. Consequently `decision_ready` is an operational signal, not demonstrated underwriting correctness, even after the missing-evidence fix.

## Limits of this exercise

- These are 32 unique synthetic, single-criterion scenarios; three runs yield 96 executions, not 96 independent cases.
- The same assistant authored the new cases and the implementation. Gold labels are explicit but not independently reviewed by an underwriter.
- Fixed seed/temperature tests deployment-setting repeatability, not robustness across models, stochastic settings, source ordering, or prompt variants.
- Strict scoring includes exact/predeclared citation alternatives and coverage/readiness. A strict failure can have a correct final judgment; consult status accuracy and failure diagnostics separately.
- Already-extracted short observations bypass tool gathering, OCR, tables, long submission packages, and multi-criterion interactions.

The results justify revisiting confidence based on the earlier small suite. A next improvement should target the demonstrated arithmetic, criterion-polarity, explanation/status, and entity-scope failures and then be tested on another independently labeled fresh set. The current run is retained as an unchanged benchmark rather than tuned until it passes.
