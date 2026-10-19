# All-outcome review: regression comparison

**Completed and verified.** Counts below are runs 1 / 2 / 3 on the same 32 synthetic cases.

## Larger evaluation comparison

| Metric | Before | After |
| --- | --- | --- |
| Strict passes (out of 32) | 17 / 16 / 16 | 19 / 21 / 20 |
| Correct statuses (out of 32) | 20 / 19 / 19 | 28 / 28 / 28 |
| Wrong status marked decision ready | 6 / 6 / 6 | 1 / 0 / 0 |
| Ready despite gold requiring abstention | 1 / 1 / 1 | 0 / 0 / 0 |
| False-positive findings, including provisional ones | 2 / 2 / 2 | 1 / 1 / 1 |
| All decision-ready cases | 16 / 16 / 16 | 10 / 11 / 10 |
| Ready cases with correct status | 10 / 10 / 10 | 9 / 11 / 10 |
| Readiness matching gold (out of 32) | 24 / 24 / 24 | 20 / 21 / 20 |
| Incomplete cases | 6 / 7 / 7 | 0 / 1 / 1 |
| Model calls | 120 / 121 / 121 | 154 / 155 / 154 |
| Measured seconds | 230.4 / 215.7 / 224.6 | 509.3 / 503.9 / 499.0 |

Across the 96 case-runs, correct statuses increased from **58/96 to 84/96**. Wrong statuses marked ready fell from **18 to 1**. These are repeated executions of 32 cases, not 96 independent examples.

Inference took approximately **2.25 times** the baseline time, with 463 calls versus 362. More explicit reasoning and the additional review increase cost; no dependencies were added. Latency is observational and affected by local machine/model conditions.

Readiness matching gold declined because the revised system holds more decidable cases for manual review. Gold readiness describes whether the supplied facts are sufficient for a correct decision; it does not validate the model's particular proposal. A conservative hold can lose readiness credit while preventing an incorrect ready result. Strict passes include that readiness check.

## Consistency

- Same final status across all runs: **31/32 → 32/32**.
- Same status, finding citation groups, and readiness: **31/32 → 29/32**.
- Passed all three runs: **16/32 → 19/32**.
- Status judgments became more consistent; readiness still varied. Repeated agreement is not proof of correctness.

## Original evaluation suites

| Suite | Before strict passes | After strict passes |
| --- | --- | --- |
| [Original eight cases](2026-10-18-reviewed-core-final.md) | 8/8 | 8/8 |
| [Four sufficiency contrasts](2026-10-18-reviewed-contrasts-final.md) | 4/4 | 3/4 |

The contrast regression is `explicit_activity_did_not_occur`: a direct statement that an elevator was not inspected should yield `no_match`, but the model returns `insufficient_evidence` by confusing refutation of the rule with a factual contradiction. It remains non-ready. The smaller suites do not label readiness, so their strict scores exclude that check.

## Remaining larger-suite errors

| Case | Expected | Observed in all three runs | Readiness |
| --- | --- | --- | --- |
| `cyber_patch_coverage_boundary` | `matched` | `no_match` | False / False / False |
| `property_electrical_exception` | `no_match` | `matched` | False / False / False |
| `property_building_specific_scope` | `not_applicable` | `no_match` | True / False / False |
| `wc_activity_explicitly_not_performed` | `no_match` | `insufficient_evidence` | False / False / False |

The single remaining incorrect-ready result is the building-specific scope case in run 1: an explicitly excluded steel-frame building is labeled `no_match` instead of `not_applicable`. The electrical-exception case emits one false-positive concern per run; each is held as non-ready. The percentage-threshold case substitutes an all-servers requirement for the stated 95% threshold. The activity case confuses evidence refuting a criterion with evidence contradicting other evidence.

**The readiness flag still needs human oversight.** The changes substantially reduce observed false-ready decisions, but same-model review and valid citations do not establish semantic correctness.

## Verification

- 72 unit/integration/scoring tests passed for this implementation.
- All 96 final larger-suite results revalidated against `AssessmentResult`; saved scores were recomputed and matched.
- All accepted citation-integrity checks passed. This checks references and source text, not whether the interpretation follows.
- Frozen runtime/evaluation/data hashes matched after all runs; model digest, inference settings, gold labels, and ordered cases matched the baseline.
- Notebook JSON and Python code-cell syntax checked.


## Implementation changes

- The model quotes the criterion trigger and evaluates scope, condition truth, exceptions, and factual conflicts separately. Python derives status and basis, removing the redundant model-selected status/basis pair.
- Every criterion receives an independent assessment of the original evidence under a separate prompt. Prior judgments are withheld. The same local model performs both passes; this is not independent expert validation.
- A valid review supplies the final displayed result. The initial case proposal and review are both retained. Readiness requires agreement on status and the multiset of finding citation groups; missing/invalid reviews, missing initial cases, insufficient evidence, and incomplete source coverage block readiness.
- Review corrections do not automatically become ready. Findings returned while readiness is false remain provisional. Disabling the all-outcome review cannot bypass the readiness gate.
- Final negative decisions retain the original focused evidence-sufficiency challenge. Its specialized question can catch missing-information errors repeated by the two general passes. Disabling or failing it leaves a negative unverified and blocks readiness.
- Criterion quotations, evidence references, source boundaries, status derivation, and finding shape are checked deterministically. Arithmetic, exception interpretation, and semantic support still depend on the model.

The change adds no dependencies, external services, retrieval system, or orchestration framework. It adds one general review call per criterion and retains the focused check for final negatives, with the existing bounded retry policy. Extra calls and more explicit explanations increase inference time.

## Protocol

The original 32-case dataset, gold labels, scoring criteria, case order, model digest, temperature 0, seed 42, 8,192-token context, and 4,096-token output limit are preserved. The final implementation is frozen across three repeated runs. These cases now inform development, so this is a regression comparison, not new held-out accuracy. The cases are synthetic and have not been independently labeled by underwriters.

Baseline: [three original runs](unseen-v1-three-runs/summary.md). Updated: [three combined-review runs](unseen-v1-combined-review-three-runs/summary.md). Each directory contains manifests, JSON call traces, Markdown reports, logs, and summary metrics.

## Known limitations to inspect

The intermediate general-review-only runs contain cases where both passes mistake unconfirmed subcontractor insurance limits or missing driver-screening records for refuted conditions. That motivated retaining the narrower negative-evidence check. Other observed errors include scope exclusions confused with false conditions, an inclusive percentage threshold replaced by an all-items requirement, and evidence refuting a condition treated as an unresolved conflict. Multiple reviews still use the same model and cannot certify correctness.

Exact finding citation-group comparison can also hold valid results for manual review when both passes use different legitimate corroboration. Strict fixture scoring includes expected readiness, so a correct status with a conservative hold can still fail the strict benchmark. Consult status accuracy, false-ready counts, ready-case counts, and strict passes together.

## Preserved development iterations

- [Initial eight-case review check](2026-10-18-reviewed-core.md): 6/8 strict passes. It exposed missing-evidence and correction-polarity regressions in the first review prompt.
- [Interrupted diagnostic run](unseen-v1-reviewed-three-runs/run-01.md): 14 completed cases; stopped after unsupported unresolved-conflict selections were identified. Its manifest is marked interrupted. It is excluded from the final three-run comparison.
- [Completed intermediate general-review-only runs](unseen-v1-reviewed-final-three-runs/summary.md): preserved separately. They motivated keeping the focused negative check after general review.
- The combined revision requires an explicit conflict explanation, distinguishes actual incompatible observations from refutation of a criterion, and retains the focused negative check. No gold labels were changed to fit the outputs.
