# Evidence sufficiency and decision readiness

## Change

The previous negative confirmation repeated the original judgment and could repeat the same mistake. The API now uses a focused `no_match_review` stage with a separate schema and prompt. It receives the original criterion and all evidence, without the earlier model's status, explanation, or source proposals. It asks which observed fact disproves the condition, and whether the condition could still be true given missing information.

The same configured model performs the review. It is a separate task, not an independent model or human assessment. The review can confirm affirmative negative evidence, identify missing evidence, identify unresolved conflict, or require reassessment. Original negative proposals and accepted reviews remain in the result.

Missing evidence or unresolved conflict deterministically changes the case to `insufficient_evidence` and blocks readiness. A failed/inconclusive review leaves the original negative unverified and blocks readiness. Skipping review with `confirm_no_match=False` also leaves negatives unverified: complete coverage alone cannot make them ready. Unknown references or uncited confirmations are rejected through bounded retries.

## Original eight cases

The model (`qwen3-coder:30b`), model settings, original cases, gold labels, and scoring rules were unchanged. The reviewer replaces the previous repeated case confirmation.

| Metric | Previous implementation | With sufficiency review |
| --- | ---: | ---: |
| Strict cases passed | 7/8 | **8/8** |
| Correct final statuses | 7/8 | **8/8** |
| Required gold citations | 10/10 | **10/10** |
| Accepted reference/provenance checks | 36/36 | **36/36** |
| False-positive findings | 0 | **0** |
| Independent findings in matched cases | 4/4 | **4/4** |
| Model calls | 25 | **24** |
| Elapsed assessment time | 40.3s | **39.4s** |

One source response had inconsistent basis/status and recovered after validation feedback. The focused review of the missing-training-records case returned `missing_evidence`: it explicitly distinguished unprovided records from a statement that training did not occur. The API retained the original `no_match` proposal, changed the final case status to `insufficient_evidence`, and set `decision_ready=False`.

Both unrelated-evidence cases and the unresolved-contradiction case are not ready. The explicit correction and applicable exception receive supported negative reviews and remain ready. The scope-exclusion and multiple-finding cases retain their correct results. These readiness values were checked separately against the intended outcomes; they are not part of the unchanged original strict scorer.

## Additional contrast cases

Four synthetic cases were authored before this focused run to check that the review does not indiscriminately abstain on all negatives. No changes were made based on their results.

| Case | Final status | Decision ready | Result |
| --- | --- | --- | --- |
| Elevator inspection records not supplied; activity unknown | `insufficient_evidence` | False | PASS |
| Manager explicitly confirms an elevator was not inspected | `no_match` | True | PASS |
| Rule requires certificate submission; administrator confirms none submitted | `no_match` | True | PASS |
| Roof age of five years against concern threshold above twenty | `no_match` | True | PASS |

**4/4 passed**, with 11 model calls in 12.5 seconds and no rejected responses. The three negatives all received supported reviews. Latencies are observations from single local runs, not controlled performance benchmarks.

## Validation and limits

All **52 unit/integration tests pass**. Six new tests cover review downgrades with preserved proposals, disabled reviews, invalid references/retry feedback, inconclusive reviews, unresolved conflicts, and supported confirmation. All twelve live cases had the expected readiness state. The model can still make a semantic error in the reviewer; the deterministic gate enforces its verdict and validated citations, not factual truth. These small synthetic development cases are not expert-validated production accuracy estimates, and the original eight cases have informed implementation changes.

Custom model callables must handle the new `no_match_review` stage with `NoMatchReviewDraft`; the supplied LangChain adapter selects it automatically. The LangGraph state contract is unchanged. See [integration guidance](../../docs/INTEGRATION.md#structured-output-migration).

## Artifacts

- [Eight-case report](2026-10-18-qwen3-coder-30b-sufficiency.md) and [full trace](2026-10-18-qwen3-coder-30b-sufficiency.json)
- [Contrast report](2026-10-18-qwen3-coder-30b-sufficiency-contrasts.md) and [full trace](2026-10-18-qwen3-coder-30b-sufficiency-contrasts.json)
- [Earlier implementation comparison](2026-10-18-comparison.md)
