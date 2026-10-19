# Longer-document holdout: results and interpretation

## Main result

The first frozen run exposed substantive failures. **Only 8/18 expected criteria
reached usable assessment results, and one of two decision-ready cases had an
incorrect status.** The automatic explanation judge was not reliable enough to
establish explanation quality on its own.

Six new synthetic accounts contain 18 criteria: 11 explicit and seven implicit.
Each packet contains 2,042–2,084 words, comprising a 618–642-word guideline and a
1,419–1,452-word application. Facts occur early, in the middle, and late among
administrative material. These are modestly longer text documents, not a test of
very large windows, OCR, PDF layouts, or independently labeled production files.

Production code and prompts were unchanged from merged commit `9d74649`.
Documents, gold, scorer, and implementation hashes were frozen before inference
and remained unchanged. There was one run, with no fixes or selective reruns to
improve the result. The same local `qwen3-coder:30b` ran the pipeline and separate
evaluation judge. Context/output limits were 32,768/8,192 tokens; temperature 0,
seed 42. The largest recorded production prompt was 7,424 tokens, so this run
does not establish behavior near the context limit.

## Case results

Status and finding columns use the full three-criterion gold inventory per case,
including missing criteria. Finding-set correctness includes correct empty sets;
it is not a finding-level recall percentage.

| Case | Usable criteria | Correct statuses | Correct finding sets | Ready | Automatic strict pass |
| --- | --- | --- | --- | --- | --- |
| Property | 3/3 | 3/3 | 3/3 | Yes | Yes, but explanation audit found a failure |
| Cyber | 0/3 | 0/3 | 0/3 | No | No |
| Fleet | 2/3 | 2/3 | 2/3 | No | No |
| Manufacturing | 0/3 | 0/3 | 0/3 | No | No |
| Hospitality | 3/3 | 2/3 | 3/3 | **Yes, with an incorrect status** | No |
| Contractor | 0/3 | 0/3 | 0/3 | No | No |
| **Total** | **8/18** | **7/18** | **8/18** | **2/6** | **1/6** |

- Document collection: **6/6** packets retrieved.
- Complete usable criterion inventories: **2/6** cases.
- Explicit criteria reaching assessment: **8/11**.
- Implicit criteria reaching assessment: **0/7**.
- Among eight assessed criteria, statuses were correct for **7/8**; the full
  end-to-end denominator remains **7/18**.
- The three returned assessment results passed raw source/locator checks. Three
  extraction failures had no result to validate; they are unavailable, not
  fabricated-source failures.
- Objective unsafe-ready cases: **1/6 total, or 1/2 ready cases**. This tiny sample
  does not estimate a production rate.
- Automatic strict passes: **1/6**. Requiring the separate qualitative explanation
  audit to pass would leave **0/6**; automatic scores were not overwritten.

## Failure analysis

### 1. Implicit guidelines are not supported by the current extraction contract

The manuals explicitly define referral/decline as concern and favorable
treatment/positive credit as strength. The actual implicit rule lines do not
repeat those labels. In cyber, manufacturing, and contractor, the extractor
proposed implicit quotations with inferred classifications. The production
validator rejected them because the quoted rule itself lacked its classification
word. Assessment therefore became unavailable, including otherwise supported
explicit rules in those mixed documents.

This is a known contract boundary exposed by the test, not proof the model could
not locate the implicit rule. The raw extraction traces distinguish proposals
from accepted assessment inputs. Enabling implicit rules would require a
principled representation of the source-backed classification mapping rather
than simply treating an inferred label as an exact quote.

In fleet, the extractor instead returned the existing explicit rules and claimed
completeness while omitting the implicit telematics rule. The full-inventory
scorer caught the omission. The case was held for other reasons, so it did not
produce an unsafe-ready result in this run. This demonstrates why a model's
`complete=true` is not proof of criterion completeness.

### 2. Scope exclusion can still be marked ready as a negative match

The hotel guideline explicitly restricts its pool rule to properties operating a
guest swimming pool. The application states there is no such pool. Gold is
`not_applicable`; final output was `no_match`, with `decision_ready=True`.

The explanation itself says the rule does not apply, but the structured scope
judgment failed to represent that exclusion. Agreement/review gates did not
prevent the incorrect ready result. Exact citations and reviewer agreement are
insufficient semantic checks.

### 3. Correct final statuses can coexist with contradictory explanations

The property roof explanation says no exception prerequisites or validity dates
are specified despite a quoted two-year replacement exception. Its findings are
correct, but the explanation contains a false statement about the rule.

Fleet's final statuses correctly abstain. Its retained explanations nevertheless
say a disputed defect establishes a finding and that missing review records
refute completion. The focused negative review corrected the latter final
assessment, but the earlier decision-review explanation remains visible and
contradictory. Source-stage errors and review disagreements also kept fleet
non-ready.

The hotel's service-boundary explanation first says exactly 30 days meets a
strictly greater-than-30 trigger, then correctly says it does not. The final
status is correct; the written justification is internally inconsistent.

## Explanation-quality checks

The frozen rubric scores rule application, factual grounding, scope/exceptions,
logical support, and absence of unsupported claims, each 0–2. A pass requires
8/10 or more with no zero dimension. The candidate text includes final assessment
and finding reasons plus the retained review explanations. Missing outputs are
kept distinct from poor explanations and judge errors.

| Explanation outcome | Count |
| --- | --- |
| Expected explanations | 18 |
| Produced explanations | 8 |
| Missing because no assessment/criterion was available | 10 |
| Explanations with a valid automatic grade | 3 |
| Explanations left ungraded because their case's judge response failed validation | 5 |
| Automatic rubric passes | 3/3 valid grades; **not 3/8 proven-good explanations** |
| Separate qualitative audit passes | **3/8 produced; 3/18 end-to-end** |

The model judge awarded every property explanation 10/10, including the false
no-exception statement. Its justification repeated that error. Fleet and hotel
judge responses contained noncontiguous excerpts presented as contiguous quotes,
so the validator rejected each whole response. Those five explanations are
**ungraded**, not automatic zero-quality judgments. No judge retry was used.

I reviewed all eight produced explanations using the same rubric. This is an
assistant audit by the fixture author, **not independent human/expert validation**.
Scores and exact excerpts are saved in the
[audit JSON](2026-10-19-heldout-explanation-audit.json); original automatic scores
remain untouched.

| Case / criterion | Audit score | Outcome | Main observation |
| --- | --- | --- | --- |
| Property / roof | 7/10 | Fail | False no-exception claim |
| Property / sprinkler certificates | 10/10 | Pass | Evidence establishes all-building coverage |
| Property / wall panels | 9/10 | Pass | Correct exception application; minor trigger/exception wording imprecision |
| Fleet / brakes | 4/10 | Fail | Claims a settled finding despite unresolved conflict |
| Fleet / driver reviews | 5/10 | Fail | Retained reason mistakes missing records for falsehood |
| Hotel / overdue service | 7/10 | Fail | Contradictory strict-threshold reasoning |
| Hotel / swimming pool | 4/10 | Fail | Recognizes exclusion but emits an in-scope negative |
| Hotel / cash reserves | 10/10 | Pass | Correct 6.5-month calculation and inclusive threshold |

Both ready cases contain at least one explanation that fails this audit. The
property case has correct final outcomes; the hotel additionally has an incorrect
status. These are distinct defects and should not be collapsed into one metric.

## Verification and cost

- **105 unit tests pass**, including eight new scoring-integrity tests.
- All three returned results revalidated against `AssessmentResult`.
- Every stored score recomputed identically; all frozen file hashes matched.
- Production assessment/extraction payloads exclude scoring gold and rationales.
- 33 assessment call attempts, six extraction calls, and three evaluation-only
  judge calls. No new dependency or production middleware layer.
- Observed production execution time: about **280 seconds**; judging added about
  **46 seconds**. These local measurements are not controlled latency estimates.

## Interpretation

The earlier short-document regression results overstated how broadly the solution
could be expected to generalize. This test identifies concrete gaps in implicit
rule handling, inventory completeness, scope classification, and explanation
consistency. It also shows that the chosen same-model judge needs validation
before its ratings can be treated as quality evidence.

The next improvements should target those observed failures. Preserve this first
run as the baseline; future tuning makes these cases regression fixtures and
requires another unseen set for a fresh accuracy estimate. Source data and labels
here are synthetic and self-authored, with shared boilerplate across documents.
No production accuracy or safety claim follows from this sample.

## Artifacts

- [Frozen protocol](../HOLDOUT_EVALUATION.md)
- [Automatic report](2026-10-19-heldout-long-documents.md)
- [Raw calls, outputs, hashes, and scores](2026-10-19-heldout-long-documents.json)
- [Separate explanation audit](2026-10-19-heldout-explanation-audit.json)
- [Corpus and gold](../holdout/cases.json)
