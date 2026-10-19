# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-18T23:32:28.116253+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **8/8** (planned: 8).
- Correct case statuses: **8/8**.
- Required gold evidence cited: **10/10**.
- Reference/provenance checks: **36/36**.
- False-positive findings in the 6 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| unrelated_financials | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| unrelated_lexical_overlap | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| contradiction_unresolved | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| contradiction_explicit_correction | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| exception_qualifies | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| exception_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
| multiple_concerns_one_source | matched | matched | 2 / 2 | 2 / 2 | PASS |
| multiple_strengths_across_sources | matched | matched | 2 / 2 | 2 / 2 | PASS |

## Reasons and diagnostics

### unrelated_financials

**Expected:** Revenue and headcount do not establish training completion. Absence of relevant evidence does not establish no_match.

**Model:** The evidence provided does not contain any information regarding fire-safety training completion rates or employee attendance at such training. Since the criterion requires data on annual fire-safety training completion being below 90% of employees, and no such data is present in the supplied evidence, the condition cannot be evaluated.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 2.4s.

### unrelated_lexical_overlap

**Expected:** The training population and subject differ. Accountants completing cybersecurity training says nothing about forklift training.

**Model:** The criterion requires that all forklift operators completed certified forklift safety training during 2025. Evidence E1 states that no forklift-operator training records were provided, but it does not explicitly state that forklift operators did not complete the training. The absence of records does not establish that the condition is false, as missing evidence does not prove non-compliance.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 3.6s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that all forklift operators completed certified forklift safety training during 2025. Evidence E1 states that no forklift-operator training records were provided, but it does not explicitly state that forklift operators did not complete the training. The absence of records does not establish that the condition is false, as missing evidence does not prove non-compliance.

### contradiction_unresolved

**Expected:** Equally authoritative contemporaneous reports conflict. Both must be cited and the conflict cannot be resolved from these inputs.

**Model:** There is an unresolved conflict between two independent qualified inspections of the same warehouse sprinkler system on the same date (2025-06-30). One inspection (E1) states the system was inoperable, while another (E2) states it was fully operational. Since there is no documented precedence or correction and the conflicting observations cannot be reconciled, the status is insufficient_evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 3; elapsed: 4.4s.

### contradiction_explicit_correction

**Expected:** The explicit correction resolves the conflict for the same date. This is not missing evidence or an exclusion from scope.

**Model:** The final assessment resolves the conflict between the initial report and the correction. The original report (E1) stated that the warehouse sprinkler system was inoperable on 2025-06-30, which would have satisfied the criterion for flagging a concern. However, a signed correction issued on 2025-07-01 (E2) explicitly states that the inoperable entry was a transcription error and that the system was fully operational on 2025-06-30. This correction supersedes the original report, negating the condition for flagging a concern. Therefore, the criterion is not satisfied.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 1; model calls: 5; elapsed: 7.8s.

**Rejected responses:** Model output could not be parsed: Failed to parse CoverageDraft from completion [{"criterion_id": "C1", "reason": "The warehouse sprinkler system was determined to be fully operational on 2025-06-30, as stated in the signed correction issued on 2025-07-01. This correction supersedes the previous finding that the system was inoperable, thereby negating the condition for flagging a concern.", "evidence_ids": ["E2"], "conflict": "none", "basis": "condition_met", "status": "no_match", "findings": []}]. Got: 1 validation error for CoverageDraft
0
  Value error, status disagrees with basis [type=value_error, input_value={'criterion_id': 'C1', 'r..._match', 'findings': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Negative-evidence review (C1):** `supported`. The criterion requires determining if the warehouse sprinkler system was inoperable on 2025-06-30. Although E1 initially states the system was inoperable, E2 provides a signed correction from the original inspector stating that the inoperable entry was a transcription error and that the system was fully operational on that date. This correction supersedes the initial report.

### exception_qualifies

**Expected:** The rule applies to this occupied building but its explicit exception defeats the concern. Certification is four months old and exceeds the 10-year threshold.

**Model:** The building is occupied and its roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold for concern. However, a licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life, which satisfies the exception condition of having at least 10 years of remaining useful life within the past 12 months. Therefore, the concern is not flagged.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 7.4s.

**Negative-evidence review (C1):** `supported`. The criterion requires that for an occupied building, a concern be flagged for a roof older than 20 years, except when a licensed engineer has certified at least 10 years of remaining useful life within the past 12 months. Evidence E1 establishes that Building A is occupied and its roof is 25 years old as of 2025-07-01, satisfying the age condition. Evidence E2 states that on 2025-03-01, a licensed engineer certified that Building A's roof had 12 years of remaining useful life. Since this certification was made within the past 12 months (as of 2025-07-01), it satisfies the exception condition. Therefore, no concern should be flagged under C1.

### exception_scope_exclusion

**Expected:** The explicit fryer scope excludes this premises. No service history is needed to establish the exclusion.

**Model:** The subject of the inspection does not meet the explicit scope requirement of the criterion, which applies only to commercial kitchens with deep-fat fryers. The evidence clearly states that the premises operates exclusively as a cold-food sandwich shop with no deep-fat fryers or hot-cooking equipment, thereby excluding it from the rule's application.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 2.6s.

### multiple_concerns_one_source

**Expected:** A and B each warrant a separate concern; C does not. A single combined finding fails the requested output granularity even if it cites both roofs.

**Model:** The criterion requires flagging a separate concern for each occupied building whose roof is more than 20 years old. Evidence E1 shows Building A is occupied and has a 24-year-old roof, which satisfies the condition. Evidence E2 shows Building B is occupied and has a 31-year-old roof, which also satisfies the condition. Evidence E3 shows Building C is occupied but has a 5-year-old roof, which does not satisfy the age requirement.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 5.2s.

### multiple_strengths_across_sources

**Expected:** Each warehouse qualifies independently, requiring two strength records under C1. Cross-source consolidation must preserve the separate findings.

**Model:** The evidence shows that both the North and South warehouses have monitored automatic sprinklers covering 100% of their respective floor areas, which satisfies the condition for recording a separate strength for each warehouse. The subject is each warehouse, and the time scope is current as per the inspection reports. There are no explicit exceptions mentioned in the criterion that would apply to these cases.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 5.9s.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, and complete coverage. Atomic records are checked against exact gold citation sets in these small fixtures. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
