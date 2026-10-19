# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-18T23:25:19.017177+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **7/8** (planned: 8).
- Correct case statuses: **7/8**.
- Required gold evidence cited: **10/10**.
- Reference/provenance checks: **38/38**.
- False-positive findings in the 6 nonmatched gold cases: **2**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| unrelated_financials | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| unrelated_lexical_overlap | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| contradiction_unresolved | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| contradiction_explicit_correction | no_match | matched | 2 / 0 | 1 / 1 | FAIL |
| exception_qualifies | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| exception_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
| multiple_concerns_one_source | matched | matched | 2 / 2 | 2 / 2 | PASS |
| multiple_strengths_across_sources | matched | matched | 2 / 2 | 2 / 2 | PASS |

## Reasons and diagnostics

### unrelated_financials

**Expected:** Revenue and headcount do not establish training completion. Absence of relevant evidence does not establish no_match.

**Model:** The provided evidence (E1) only reports the applicant's annual revenue and number of employees, but does not include any information about fire-safety training completion rates. To assess whether the annual fire-safety training completion is below 90% of employees, specific data regarding training completion percentages would be required, which is absent from the supplied evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 13.8s.

### unrelated_lexical_overlap

**Expected:** The training population and subject differ. Accountants completing cybersecurity training says nothing about forklift training.

**Model:** The criterion requires evidence that all forklift operators completed certified forklift safety training during 2025. However, the provided evidence (E1) only mentions that office accountants completed cybersecurity training and explicitly states that no forklift-operator training records were provided. This absence of evidence regarding forklift operators' training prevents a determination of whether the criterion is met.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 2.7s.

### contradiction_unresolved

**Expected:** Equally authoritative contemporaneous reports conflict. Both must be cited and the conflict cannot be resolved from these inputs.

**Model:** There is an unresolved conflict between two independent qualified inspections of the same warehouse sprinkler system on 2025-06-30. Inspection A (E1) states the system was inoperable, while Inspection B (E2) states it was fully operational. Neither inspection indicates precedence or correction over the other, and no additional evidence is provided to resolve this contradiction. As such, the condition for flagging a concern cannot be definitively established.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 3; elapsed: 5.2s.

### contradiction_explicit_correction

**Expected:** The explicit correction resolves the conflict for the same date. This is not missing evidence or an exclusion from scope.

**Model:** The evidence indicates that the warehouse sprinkler system was inoperable on 2025-06-30, which directly satisfies the condition specified in criterion C1. However, a correction issued on 2025-07-01 explicitly states that the inoperable entry in the original report was a transcription error and that the system was fully operational on 2025-06-30. Despite this correction, the initial report (E1) meets the criterion's condition, and the correction (E2) contradicts it. Since the correction supersedes the original report, the final determination is based on the corrected information.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 7.8s.

### exception_qualifies

**Expected:** The rule applies to this occupied building but its explicit exception defeats the concern. Certification is four months old and exceeds the 10-year threshold.

**Model:** The building is occupied and its roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold for concern. However, a licensed engineer certified Building A's roof had 12 years of remaining useful life on 2025-03-01. This certification satisfies the exception condition of the criterion, which allows flagging a concern for a roof older than 20 years only if there is no licensed engineer certification of at least 10 years of remaining useful life within the past 12 months. Since the certification was provided within the past 12 months and indicates more than 10 years of remaining useful life, the exception applies and the roof does not require flagging as a concern.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 2; captured call errors: 0; model calls: 4; elapsed: 9.1s.

### exception_scope_exclusion

**Expected:** The explicit fryer scope excludes this premises. No service history is needed to establish the exclusion.

**Model:** The criterion explicitly applies only to commercial kitchens with deep-fat fryers. The evidence states that the premises operates exclusively as a cold-food sandwich shop, has no deep-fat fryers, and no hot-cooking equipment. This subject is outside the explicit scope of the rule.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 2.2s.

### multiple_concerns_one_source

**Expected:** A and B each warrant a separate concern; C does not. A single combined finding fails the requested output granularity even if it cites both roofs.

**Model:** The criterion requires flagging a separate concern for each occupied building whose roof is more than 20 years old. Evidence E1 shows Building A is occupied and has a 24-year-old roof, and evidence E2 shows Building B is occupied and has a 31-year-old roof. Both buildings meet the condition of being occupied with roofs older than 20 years, thus qualifying for separate concerns.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 4.7s.

### multiple_strengths_across_sources

**Expected:** Each warehouse qualifies independently, requiring two strength records under C1. Cross-source consolidation must preserve the separate findings.

**Model:** The criterion requires recording a separate strength for each warehouse with monitored automatic sprinklers covering 100% of its floor area. Both the North and South warehouses meet this condition, as evidenced by the inspection reports.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 5.6s.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, and complete coverage. Atomic records are checked against exact gold citation sets in these small fixtures. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on eight short cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. No production prompt or API behavior is changed by this evaluation.
