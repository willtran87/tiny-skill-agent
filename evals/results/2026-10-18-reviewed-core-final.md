# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T00:31:50.673096+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **8/8** (planned: 8).
- Correct case statuses: **8/8**.
- Required gold evidence cited: **10/10**.
- Reference/provenance checks: **34/34**.
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

**Model:** The subject is employees and the period in scope is annual, as indicated by 'annual fire-safety training completion'. The payload scope covers the whole case, which includes all relevant evidence for this criterion. The quoted trigger requires that annual fire-safety training completion be below 90% of employees. However, no evidence is provided regarding actual fire-safety training completion rates among employees. Since there is no data on how many employees have completed the training, we cannot prove or refute whether the completion rate is below 90%. Therefore, the condition is unknown. There are no explicit exception prerequisites mentioned in the rule that would apply here. The rule does not specify any conditions under which this concern would not be flagged. There are no conflicting observations regarding fire-safety training completion rates in the provided evidence. The only piece of evidence (E1) relates to financials and employee count but does not mention training completion.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 7.0s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The quoted trigger requires that annual fire-safety training completion be below 90% of employees. However, no evidence is provided regarding actual fire-safety training completion rates among employees. Since there is no data on how many employees have completed the training, we cannot prove or refute whether the completion rate is below 90%. Therefore, the condition is unknown. There are no explicit exception prerequisites mentioned in the rule that would apply here. The rule does not specify any conditions under which this concern would not be flagged.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### unrelated_lexical_overlap

**Expected:** The training population and subject differ. Accountants completing cybersecurity training says nothing about forklift training.

**Model:** The criterion requires that all forklift operators completed certified forklift safety training during 2025. Evidence E1 states that no forklift-operator training records were provided, but it does not explicitly state that forklift operators did not complete the training. The absence of records does not establish that the condition is false, as missing evidence does not prove non-compliance.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 8.3s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that all forklift operators completed certified forklift safety training during 2025. Evidence E1 states that no forklift-operator training records were provided, but it does not explicitly state that forklift operators did not complete the training. The absence of records does not establish that the condition is false, as missing evidence does not prove non-compliance.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states 'No forklift-operator training records were provided.' This directly refutes the condition that all forklift operators completed certified forklift safety training during 2025. There is no mention of any forklift operator completing training, and the absence of records indicates a lack of completion. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule.

### contradiction_unresolved

**Expected:** Equally authoritative contemporaneous reports conflict. Both must be cited and the conflict cannot be resolved from these inputs.

**Model:** The subject is the warehouse sprinkler system, and the period in scope is 2025-06-30. Facts proving the quoted trigger: E1 states 'Warehouse A sprinkler system: inoperable on 2025-06-30.' This directly supports that the system was inoperable. Facts refuting the trigger: E2 states 'Warehouse A sprinkler system: fully operational on 2025-06-30.' This directly contradicts the inoperability claim. Given that both inspections are independent and qualified, and no precedence or correction is documented for either, the contradiction remains unresolved. Therefore, condition=unknown. There are no explicit exception prerequisites mentioned in the criterion text for C1. The rule does not specify any conditions under which this concern would not apply. Hence, exception=does_not_apply. There is an actual incompatible observation between E1 and E2 regarding the status of the warehouse sprinkler system on 2025-06-30. E1 claims it was inoperable, while E2 claims it was fully operational. These observations concern the same subject (warehouse sprinkler system) and time (2025-06-30), and neither has documented precedence or correction. Therefore, conflict=unresolved.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 4; model calls: 7; elapsed: 21.4s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if the warehouse sprinkler system was inoperable on 2025-06-30.", "scope_reason": "The payload's scope field 'inspection:a' identifies the evidence batch, not the rule's applicability. The criterion's applicability is determined by the inspection date and subject matter, which aligns with the evidence provided in inspection:a. However, since there are two conflicting inspections (a and b), the overall case scope must be considered for determining the final assessment.", "scope": "in_scope", "condition_reason": "The evidence E1 directly states 'Warehouse A sprinkler system: inoperable on 2025-06-30.' This confirms that the warehouse sprinkler system was indeed inoperable on the specified date, meeting the condition's requirement. Although there is conflicting evidence from inspection:b (E2), the assessment for inspection:a specifically evaluates E1 as supporting the condition.", "condition": "true", "exception_reason": "There are no explicit exceptions mentioned in the criterion text that would prevent the condition from being met. The rule does not specify any conditions under which the inoperability of the sprinkler system would not constitute a concern.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There is a direct contradiction between E1 and E2. E1 states that the system was inoperable on 2025-06-30, while E2 states it was fully operational on the same date. These two pieces of evidence contradict each other, creating an unresolved conflict.", "conflict": "unresolved", "findings": [{"subject": "Warehouse A sprinkler system", "evidence_ids": ["E1"], "reason": "The inspection report indicates that the warehouse sprinkler system was inoperable on 2025-06-30, which directly meets the condition specified in criterion C1."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...ied in criterion C1.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; condition_quote must be an exact excerpt from the requested criterion.text

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts proving the quoted trigger: E1 states 'Warehouse A sprinkler system: inoperable on 2025-06-30.' This directly supports that the system was inoperable. Facts refuting the trigger: E2 states 'Warehouse A sprinkler system: fully operational on 2025-06-30.' This directly contradicts the inoperability claim. Given that both inspections are independent and qualified, and no precedence or correction is documented for either, the contradiction remains unresolved. Therefore, condition=unknown. There are no explicit exception prerequisites mentioned in the criterion text for C1. The rule does not specify any conditions under which this concern would not apply. Hence, exception=does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### contradiction_explicit_correction

**Expected:** The explicit correction resolves the conflict for the same date. This is not missing evidence or an exclusion from scope.

**Model:** The subject is the warehouse sprinkler system, and the period in scope is 2025-06-30. The evidence shows that Report R1 (E1) states the warehouse sprinkler system was inoperable on 2025-06-30. However, a correction (E2) issued on 2025-07-01 explicitly states that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. The correction supersedes R1. Therefore, the facts that prove the trigger are refuted by the correction, which establishes that the system was operational. Condition is false. There are no explicit exception prerequisites mentioned in the rule text for C1. There is an actual incompatible observation: E1 claims the system was inoperable on 2025-06-30, while E2 (a correction) states it was fully operational on that date. These contradict each other regarding the same subject and time period. However, since E2 supersedes E1, this contradiction is resolved in favor of E2's assertion.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 0; model calls: 5; elapsed: 13.3s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining if the warehouse sprinkler system was inoperable on 2025-06-30. Although E1 initially states the system was inoperable, E2 provides a signed correction from the original inspector stating that the inoperable entry was a transcription error and that the system was fully operational on that date. This correction supersedes the initial report.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence shows that Report R1 (E1) states the warehouse sprinkler system was inoperable on 2025-06-30. However, a correction (E2) issued on 2025-07-01 explicitly states that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. The correction supersedes R1. Therefore, the facts that prove the trigger are refuted by the correction, which establishes that the system was operational. Condition is false. There are no explicit exception prerequisites mentioned in the rule text for C1.

### exception_qualifies

**Expected:** The rule applies to this occupied building but its explicit exception defeats the concern. Certification is four months old and exceeds the 10-year threshold.

**Model:** The subject is Building A, which is occupied. The period in scope is as of 2025-07-01. Facts that PROVE the quoted trigger: Building A is occupied and its roof is 25 years old as of 2025-07-01 (E1). Facts that REFUTE it: A licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life, which exceeds the 10-year threshold. Given that the certification was within the past 12 months (2025-03-01 to 2025-07-01), it satisfies the exception condition. Therefore, the trigger is FALSE because the exception applies. The exception prerequisite is that a licensed engineer certified at least 10 years of remaining useful life within the past 12 months. The certification on 2025-03-01 meets this requirement as it was within the past 12 months (2025-03-01 to 2025-07-01) and stated 12 years of remaining useful life, which is greater than 10 years. The exception applies. There are no actual incompatible observations. E1 states the roof is 25 years old, and E2 states it has 12 years of remaining useful life, which is consistent with a 25-year-old roof having 12 years left. No unresolved conflicts exist.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 22.5s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion requires that for an occupied building, a concern be flagged for a roof older than 20 years, except when a licensed engineer has certified at least 10 years of remaining useful life within the past 12 months. Evidence E1 establishes that Building A is occupied and its roof is 25 years old as of 2025-07-01, satisfying the age condition. Evidence E2 states that on 2025-03-01, a licensed engineer certified that Building A's roof had 12 years of remaining useful life. Since this certification was made within the past 12 months (as of 2025-07-01), it satisfies the exception condition. Therefore, no concern should be flagged under C1.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `applies`. Facts that PROVE the quoted trigger: Building A is occupied and its roof is 25 years old as of 2025-07-01 (E1). Facts that REFUTE it: A licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life, which exceeds the 10-year threshold. Given that the certification was within the past 12 months (2025-03-01 to 2025-07-01), it satisfies the exception condition. Therefore, the trigger is FALSE because the exception applies. The exception prerequisite is that a licensed engineer certified at least 10 years of remaining useful life within the past 12 months. The certification on 2025-03-01 meets this requirement as it was within the past 12 months (2025-03-01 to 2025-07-01) and stated 12 years of remaining useful life, which is greater than 10 years. The exception applies.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### exception_scope_exclusion

**Expected:** The explicit fryer scope excludes this premises. No service history is needed to establish the exclusion.

**Model:** The subject is a commercial kitchen. The period in scope is the past six months for hood suppression system service. The evidence E1 states that 'This premises operates exclusively as a cold-food sandwich shop. It has no deep-fat fryers and no hot-cooking equipment.' This directly contradicts the requirement for commercial kitchens with deep-fat fryers. Therefore, the trigger condition is not met because the subject does not fall within the scope of kitchens with deep-fat fryers. There are no explicit exception prerequisites mentioned in the rule text. No conflicting observations exist. The evidence clearly indicates that the premises does not operate as a commercial kitchen with deep-fat fryers, which is a prerequisite for this rule to apply.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 7.8s.

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The evidence E1 states that 'This premises operates exclusively as a cold-food sandwich shop. It has no deep-fat fryers and no hot-cooking equipment.' This directly contradicts the requirement for commercial kitchens with deep-fat fryers. Therefore, the trigger condition is not met because the subject does not fall within the scope of kitchens with deep-fat fryers. There are no explicit exception prerequisites mentioned in the rule text.

### multiple_concerns_one_source

**Expected:** A and B each warrant a separate concern; C does not. A single combined finding fails the requested output granularity even if it cites both roofs.

**Model:** The rule applies to occupied buildings with roofs older than 20 years. The evidence spans cover buildings A, B, and C, all of which are occupied. Facts proving the trigger: E1 states Building A is occupied and has a 24-year-old roof (24 > 20); E2 states Building B is occupied and has a 31-year-old roof (31 > 20). Facts refuting the trigger: E3 states Building C is occupied but has a 5-year-old roof (5 <= 20). Given unknown information, it's possible that additional buildings exist with roofs older than 20 years but not mentioned in the evidence. Condition is true for Buildings A and B, false for Building C. The rule does not specify any exceptions. No explicit exception prerequisites or validity dates are provided. There are no actual incompatible observations in the evidence. Each building's status (occupied) and roof age are clearly stated without contradiction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 10.6s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts proving the trigger: E1 states Building A is occupied and has a 24-year-old roof (24 > 20); E2 states Building B is occupied and has a 31-year-old roof (31 > 20). Facts refuting the trigger: E3 states Building C is occupied but has a 5-year-old roof (5 <= 20). Given unknown information, it's possible that additional buildings exist with roofs older than 20 years but not mentioned in the evidence. Condition is true for Buildings A and B, false for Building C. The rule does not specify any exceptions. No explicit exception prerequisites or validity dates are provided.

### multiple_strengths_across_sources

**Expected:** Each warehouse qualifies independently, requiring two strength records under C1. Cross-source consolidation must preserve the separate findings.

**Model:** The rule applies to warehouses with monitored automatic sprinklers covering 100% of their floor area. The evidence spans E1 and E2 both refer to specific warehouses (North and South) with this characteristic. Facts proving the quoted trigger: E1 states 'North warehouse has monitored automatic sprinklers covering 100% of its floor area.' E2 states 'South warehouse has monitored automatic sprinklers covering 100% of its floor area.' These directly support that each warehouse has monitored automatic sprinklers covering 100% of its floor area. No facts refute this trigger. Given the known information, the trigger is true. The rule does not specify any exceptions. Therefore, no exception prerequisites need to be checked. There are no conflicting observations between E1 and E2. Both pieces of evidence refer to different warehouses (North and South) with the same characteristic, which does not create an inconsistency.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 14.0s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts proving the quoted trigger: E1 states 'North warehouse has monitored automatic sprinklers covering 100% of its floor area.' E2 states 'South warehouse has monitored automatic sprinklers covering 100% of its floor area.' These directly support that each warehouse has monitored automatic sprinklers covering 100% of its floor area. No facts refute this trigger. Given the known information, the trigger is true. The rule does not specify any exceptions. Therefore, no exception prerequisites need to be checked.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
