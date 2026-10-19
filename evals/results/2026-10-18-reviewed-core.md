# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-18T23:59:24.891157+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **6/8** (planned: 8).
- Correct case statuses: **6/8**.
- Required gold evidence cited: **10/10**.
- Reference/provenance checks: **37/37**.
- False-positive findings in the 6 nonmatched gold cases: **1**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| unrelated_financials | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| unrelated_lexical_overlap | insufficient_evidence | no_match | 0 / 0 | 0 / 0 | FAIL |
| contradiction_unresolved | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| contradiction_explicit_correction | no_match | matched | 1 / 0 | 1 / 1 | FAIL |
| exception_qualifies | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| exception_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
| multiple_concerns_one_source | matched | matched | 2 / 2 | 2 / 2 | PASS |
| multiple_strengths_across_sources | matched | matched | 2 / 2 | 2 / 2 | PASS |

## Reasons and diagnostics

### unrelated_financials

**Expected:** Revenue and headcount do not establish training completion. Absence of relevant evidence does not establish no_match.

**Model:** The criterion concerns annual fire-safety training completion rates among employees, which falls within the scope of the whole case review. There are no explicit exclusions in the rule that would limit its application to a specific subset of the case. The condition requires determining whether annual fire-safety training completion is below 90% of employees. However, there is no evidence provided regarding actual training completion rates or numbers of employees who have completed the training. The only data available relates to total employees (42) and revenue ($8 million), which do not support calculation of training completion percentages. There are no explicit exceptions stated in the rule that would apply to this situation. The rule does not specify any conditions under which the requirement for fire-safety training completion might be waived or otherwise not applicable.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 18.2s.

### unrelated_lexical_overlap

**Expected:** The training population and subject differ. Accountants completing cybersecurity training says nothing about forklift training.

**Model:** The criterion concerns forklift operator training completion during 2025, which falls within the scope of the whole case review. The evidence shows that no forklift-operator training records were provided during 2025. Since there is no confirmation that all forklift operators completed certified forklift safety training, the condition is not met. There are no explicit exceptions stated in the rule that would apply to this situation.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 5.5s.

### contradiction_unresolved

**Expected:** Equally authoritative contemporaneous reports conflict. Both must be cited and the conflict cannot be resolved from these inputs.

**Model:** The criterion concerns the operability status of the warehouse sprinkler system on a specific date (2025-06-30), which falls within the scope of the whole case review. The condition is evaluated based on whether the warehouse sprinkler system was inoperable on 2025-06-30. Evidence E1 states that the system was inoperable on this date, while E2 states it was fully operational. These conflicting statements create an unresolved conflict regarding the actual status of the system on the specified date. There are no explicit exceptions provided in the rule that would apply to this situation. The rule does not specify any conditions under which the determination of inoperability might be waived or altered.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 3; model calls: 6; elapsed: 16.1s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "scope_reason": "The rule's scope is defined as 'whole_case', but the source assessments explicitly define scope for each inspection. The evidence E1 and E2 are from distinct inspections (inspection:a and inspection:b), which are separate entities. Therefore, the scope of each individual inspection applies to its own assessment.", "scope": "in_scope", "condition_reason": "For inspection:a, the evidence E1 states that 'Warehouse A sprinkler system: inoperable on 2025-06-30.' This directly satisfies the condition that the warehouse sprinkler system was inoperable on the specified date. For inspection:b, the evidence E2 states that 'Warehouse A sprinkler system: fully operational on 2025-06-30,' which contradicts the condition and makes it false.", "condition": "true", "exception_reason": "There are no explicit exceptions stated in rule C1 that would apply to either inspection. The rule does not specify any conditions under which inoperability would be excused or ignored.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict": "unresolved", "findings": [{"subject": "inspection:a", "evidence_ids": ["E1"], "reason": "The warehouse sprinkler system was inoperable on 2025-06-30, as stated in the inspection report E1."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...nspection report E1.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

### contradiction_explicit_correction

**Expected:** The explicit correction resolves the conflict for the same date. This is not missing evidence or an exclusion from scope.

**Model:** The criterion concerns the status of the warehouse sprinkler system on a specific date (2025-06-30), which falls within the scope of the whole case review. The original inspection report (E1) states that the warehouse sprinkler system was inoperable on 2025-06-30. However, a subsequent correction (E2) issued on 2025-07-01 explicitly states that this inoperable entry was a transcription error and that the system was fully operational on 2025-06-30. The correction supersedes the original report. There are no explicit exceptions stated in the rule that would apply to this situation. The rule does not specify any conditions under which the inoperability of the system might be excused or deemed acceptable.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 11.1s.

### exception_qualifies

**Expected:** The rule applies to this occupied building but its explicit exception defeats the concern. Certification is four months old and exceeds the 10-year threshold.

**Model:** The criterion applies to occupied buildings and assesses roof age as of 2025-07-01. Building A is occupied and the roof age is assessed as of the specified date, so the scope is met. Building A's roof is 25 years old as of 2025-07-01. Since 25 > 20, the condition for flagging a concern based on roof age is met. A licensed engineer certified Building A's roof had 12 years of remaining useful life on 2025-03-01. This certification was within the past 12 months (as of 2025-07-01) and indicates at least 10 years of remaining useful life, satisfying the exception criteria.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 1; model calls: 5; elapsed: 13.6s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

### exception_scope_exclusion

**Expected:** The explicit fryer scope excludes this premises. No service history is needed to establish the exclusion.

**Model:** The rule explicitly applies only to commercial kitchens with deep-fat fryers. The evidence shows the premises operates exclusively as a cold-food sandwich shop with no deep-fat fryers or hot-cooking equipment, which falls outside the scope of this rule. The condition cannot be evaluated because the premises does not operate as a commercial kitchen with deep-fat fryers. The evidence explicitly states there are no deep-fat fryers or hot-cooking equipment. There are no explicit exceptions in the rule that would apply to this situation, as the scope itself excludes this case.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 5.4s.

### multiple_concerns_one_source

**Expected:** A and B each warrant a separate concern; C does not. A single combined finding fails the requested output granularity even if it cites both roofs.

**Model:** The criterion applies to occupied buildings with roofs older than 20 years. The scope includes all buildings in the case, as no explicit exclusion is provided. For each building, the roof age is compared against the 20-year threshold. Building A has a 24-year-old roof (24 > 20), Building B has a 31-year-old roof (31 > 20), and Building C has a 5-year-old roof (5 < 20). Both Building A and Building B meet the condition. There are no explicit exceptions in the rule that would apply to any of the buildings. All buildings are occupied, and there is no indication that any special conditions exempt them from the rule.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 10.2s.

### multiple_strengths_across_sources

**Expected:** Each warehouse qualifies independently, requiring two strength records under C1. Cross-source consolidation must preserve the separate findings.

**Model:** The criterion applies to the whole case as it requires recording separate strengths for each warehouse with monitored automatic sprinklers covering 100% of floor area, which is a general requirement across all warehouses in the case. Both the North and South warehouses have monitored automatic sprinklers covering 100% of their respective floor areas, as stated in E1 and E2. Each warehouse meets the condition independently. There are no explicit exceptions mentioned in the rule that would apply to either warehouse, such as exclusions for specific types of warehouses or time periods.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 12.2s.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
