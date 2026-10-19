# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T05:27:23.697241+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **7/8** (planned: 8).
- Correct case statuses: **8/8**.
- Required gold evidence cited: **10/10**.
- Reference/provenance checks: **33/33**.
- False-positive findings in the 6 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| unrelated_financials | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| unrelated_lexical_overlap | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | FAIL |
| contradiction_unresolved | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| contradiction_explicit_correction | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| exception_qualifies | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| exception_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
| multiple_concerns_one_source | matched | matched | 2 / 2 | 2 / 2 | PASS |
| multiple_strengths_across_sources | matched | matched | 2 / 2 | 2 / 2 | PASS |

## Reasons and diagnostics

### unrelated_financials

**Expected:** Revenue and headcount do not establish training completion. Absence of relevant evidence does not establish no_match.

**Model:** The rule applies to employees, and the evidence mentions 42 employees. The subject is in scope. The evidence does not provide information about fire-safety training completion rates or numbers of employees who have completed training. Without data on how many employees have completed the training, it's impossible to determine if the completion rate is below 90%. Therefore, the condition cannot be evaluated as true or false based on the provided evidence. There are no explicit exception prerequisites mentioned in the rule text that would apply to this case. There are no conflicting observations in the provided evidence that would create an unresolved contradiction regarding fire-safety training completion rates.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 28.2s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence does not provide information about fire-safety training completion rates or numbers of employees who have completed training. Without data on how many employees have completed the training, it's impossible to determine if the completion rate is below 90%. Therefore, the condition cannot be evaluated as true or false based on the provided evidence. There are no explicit exception prerequisites mentioned in the rule text that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### unrelated_lexical_overlap

**Expected:** The training population and subject differ. Accountants completing cybersecurity training says nothing about forklift training.

**Model:** The rule applies to forklift operators, and the evidence mentions office accountants completing cybersecurity training but does not mention any forklift operator training records. The evidence states 'No forklift-operator training records were provided.' This directly refutes the trigger condition that all forklift operators completed certified forklift safety training during 2025. There is no supporting evidence that any forklift operator completed the required training. There are no explicit exception prerequisites mentioned in the rule text. The evidence states that no forklift-operator training records were provided, which directly contradicts the requirement that all forklift operators completed certified forklift safety training during 2025.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 6; elapsed: 17.4s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "all forklift operators completed certified forklift safety training during 2025", "scope_reason": "The rule's scope is limited to the 'hr:2025' payload, which contains evidence about office accountants completing cybersecurity training but no information about forklift operators or their training records.", "scope": "out_of_scope", "condition_reason": "The condition requires that all forklift operators completed certified forklift safety training during 2025. However, the provided evidence (E1) states that 'No forklift-operator training records were provided,' which means there is no confirmation that any forklift operator completed the required training. Since the evidence does not establish whether the training was completed, and no records are available to confirm compliance, the condition cannot be evaluated as true or false.", "condition": "unknown", "exception_reason": "There are no explicit exceptions mentioned in the rule text that would apply to this situation.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There is no conflicting evidence provided; however, the lack of training records makes it impossible to determine if the condition is met.", "conflict": "unresolved", "findings": []}]. Got: 1 validation error for PredicateDraft
0
  Value error, unresolved conflict requires basis unresolved_conflict and insufficient_evidence [type=value_error, input_value={'criterion_id': 'C1', 'r...icable', 'findings': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states 'No forklift-operator training records were provided.' This directly refutes the trigger condition that all forklift operators completed certified forklift safety training during 2025. There is no supporting evidence that any forklift operator completed the required training. There are no explicit exception prerequisites mentioned in the rule text.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### contradiction_unresolved

**Expected:** Equally authoritative contemporaneous reports conflict. Both must be cited and the conflict cannot be resolved from these inputs.

**Model:** The subject is 'warehouse sprinkler system' and the period in scope is '2025-06-30'. The evidence batch covers this date and subject. Evidence E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. Evidence E2 states that the same system was fully operational on the same date. These observations directly contradict each other regarding the state of the sprinkler system on the specified date. Since there is no correction or precedence documented, and both inspections are from independent qualified sources at the same time, the actual condition cannot be determined with certainty based on the provided evidence. There are no explicit exception prerequisites mentioned in the criterion that would apply to this case. There is a direct contradiction between E1 (sprinkler system inoperable) and E2 (sprinkler system fully operational) for the same subject and date. No correction or precedence is documented, making this an unresolved conflict.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 2; model calls: 7; elapsed: 22.2s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.; condition_quote must be an exact excerpt from the requested criterion.text

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Evidence E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. Evidence E2 states that the same system was fully operational on the same date. These observations directly contradict each other regarding the state of the sprinkler system on the specified date. Since there is no correction or precedence documented, and both inspections are from independent qualified sources at the same time, the actual condition cannot be determined with certainty based on the provided evidence. There are no explicit exception prerequisites mentioned in the criterion that would apply to this case.

### contradiction_explicit_correction

**Expected:** The explicit correction resolves the conflict for the same date. This is not missing evidence or an exclusion from scope.

**Model:** The subject is the warehouse sprinkler system, and the period in scope is 2025-06-30. Evidence E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since the correction supersedes the original report, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational. Therefore, the trigger condition is false. The rule does not specify any exceptions that would apply to this case. There is a direct contradiction between E1, which claims the system was inoperable on 2025-06-30, and E2, which corrects this to state it was fully operational. However, since E2 supersedes E1, there is no unresolved conflict; the corrected fact is that the system was operational.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 18.0s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining if the warehouse sprinkler system was inoperable on 2025-06-30. Evidence E1 initially states the system was inoperable, but E2 provides a signed correction from the original inspector stating that the inoperable entry was a transcription error and that the system was fully operational on that date. This correction supersedes the initial report and explicitly contradicts the condition in the criterion.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Evidence E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since the correction supersedes the original report, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational. Therefore, the trigger condition is false. The rule does not specify any exceptions that would apply to this case.

### exception_qualifies

**Expected:** The rule applies to this occupied building but its explicit exception defeats the concern. Certification is four months old and exceeds the 10-year threshold.

**Model:** The subject is Building A, which is occupied. The period in scope is as of 2025-07-01. Building A's roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. However, a licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life. Since this certification was within the past 12 months (2025-03-01 to 2025-07-01), and the remaining useful life exceeds 10 years, the exception applies. The rule includes an exception for when a licensed engineer certifies at least 10 years of remaining useful life within the past 12 months. The certification on 2025-03-01 meets this condition (12 years > 10 years, and date is within past 12 months). Therefore, the exception applies. There is no actual incompatible observation. The engineer's certification supports the exception condition and contradicts the trigger condition, but since the exception applies, there is no conflict.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 6; elapsed: 26.7s.

**Negative-evidence review (C1):** `supported`. The building is occupied and its roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. However, a licensed engineer certified on 2025-03-01 that the roof had 12 years of remaining useful life, which satisfies the exception condition of at least 10 years of remaining useful life within the past 12 months. Therefore, the concern does not apply.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `applies`. Building A's roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. However, a licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life. Since this certification was within the past 12 months (2025-03-01 to 2025-07-01), and the remaining useful life exceeds 10 years, the exception applies. The rule includes an exception for when a licensed engineer certifies at least 10 years of remaining useful life within the past 12 months. The certification on 2025-03-01 meets this condition (12 years > 10 years, and date is within past 12 months). Therefore, the exception applies.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### exception_scope_exclusion

**Expected:** The explicit fryer scope excludes this premises. No service history is needed to establish the exclusion.

**Model:** The subject is a commercial kitchen. The period in scope is the time of inspection. The evidence indicates the premises operates as a cold-food sandwich shop with no deep-fat fryers or hot-cooking equipment. The rule's trigger requires the presence of deep-fat fryers in a commercial kitchen. Evidence E1 explicitly states that the premises operates exclusively as a cold-food sandwich shop and has no deep-fat fryers or hot-cooking equipment. Therefore, the subject does not meet the applicability condition for this rule. The rule does not contain explicit exception prerequisites. The scope restriction 'This rule applies only to commercial kitchens with deep-fat fryers' is sufficient to exclude this case. There are no conflicting observations regarding the presence or absence of deep-fat fryers. The evidence clearly states there are none.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 1; model calls: 5; elapsed: 13.0s.

**Rejected responses:** condition_quote must be an exact excerpt from the requested criterion.text

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The rule's trigger requires the presence of deep-fat fryers in a commercial kitchen. Evidence E1 explicitly states that the premises operates exclusively as a cold-food sandwich shop and has no deep-fat fryers or hot-cooking equipment. Therefore, the subject does not meet the applicability condition for this rule. The rule does not contain explicit exception prerequisites. The scope restriction 'This rule applies only to commercial kitchens with deep-fat fryers' is sufficient to exclude this case.

### multiple_concerns_one_source

**Expected:** A and B each warrant a separate concern; C does not. A single combined finding fails the requested output granularity even if it cites both roofs.

**Model:** The rule applies to occupied buildings with roofs older than 20 years. The evidence batch contains information about three buildings (A, B, and C) and their respective roof ages and occupancy status. Building A is occupied and has a 24-year-old roof, which exceeds the 20-year threshold. Building B is occupied and has a 31-year-old roof, also exceeding the 20-year threshold. Building C is occupied but has a 5-year-old roof, which does not exceed the 20-year threshold. Therefore, Buildings A and B meet the condition, while Building C does not. The rule does not specify any exceptions that would apply to these buildings. There are no explicit prerequisites or validity dates mentioned for an exception. There are no conflicting observations regarding the occupancy status or roof age of Buildings A and B. All evidence supports that these buildings meet the criteria for the concern.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 13.0s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Building A is occupied and has a 24-year-old roof, which exceeds the 20-year threshold. Building B is occupied and has a 31-year-old roof, also exceeding the 20-year threshold. Building C is occupied but has a 5-year-old roof, which does not exceed the 20-year threshold. Therefore, Buildings A and B meet the condition, while Building C does not. The rule does not specify any exceptions that would apply to these buildings. There are no explicit prerequisites or validity dates mentioned for an exception.

### multiple_strengths_across_sources

**Expected:** Each warehouse qualifies independently, requiring two strength records under C1. Cross-source consolidation must preserve the separate findings.

**Model:** The rule applies to individual warehouses, and both the North and South warehouses are mentioned as having monitored automatic sprinklers covering 100% of their floor areas. The evidence batch includes inspections for both warehouses. Both E1 and E2 confirm that the North and South warehouses each have monitored automatic sprinklers covering 100% of their respective floor areas. This directly supports the trigger condition that each warehouse must have monitored automatic sprinklers covering 100% of its floor area. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply. There are no conflicting observations between E1 and E2 regarding the sprinkler coverage. Both reports confirm 100% coverage for their respective warehouses, and there is no indication of contradictory data.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 18.2s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Both E1 and E2 confirm that the North and South warehouses each have monitored automatic sprinklers covering 100% of their respective floor areas. This directly supports the trigger condition that each warehouse must have monitored automatic sprinklers covering 100% of its floor area. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
