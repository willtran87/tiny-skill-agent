# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T05:52:30.977250+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **7/8** (planned: 8).
- Correct case statuses: **8/8**.
- Required gold evidence cited: **10/10**.
- Reference/provenance checks: **33/33**.
- False-positive findings in the 6 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| unrelated_financials | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| unrelated_lexical_overlap | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| contradiction_unresolved | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| contradiction_explicit_correction | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| exception_qualifies | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| exception_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
| multiple_concerns_one_source | matched | matched | 2 / 2 | 2 / 2 | PASS |
| multiple_strengths_across_sources | matched | matched | 2 / 2 | 2 / 2 | PASS |

## Reasons and diagnostics

### unrelated_financials

**Expected:** Revenue and headcount do not establish training completion. Absence of relevant evidence does not establish no_match.

**Model:** The rule applies to employees and their fire-safety training completion status. The evidence batch includes information about the number of employees but does not contain any information about fire-safety training completion rates. The evidence provided only states that there are 42 employees but does not include any data on fire-safety training completion. Without information on how many employees have completed the training, it is impossible to determine if the completion rate is below 90%. Therefore, the condition cannot be evaluated as true or false based on the available evidence. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no conflicting observations regarding fire-safety training completion rates in the provided evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 31.0s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence provided only states that there are 42 employees but does not include any data on fire-safety training completion. Without information on how many employees have completed the training, it is impossible to determine if the completion rate is below 90%. Therefore, the condition cannot be evaluated as true or false based on the available evidence. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### unrelated_lexical_overlap

**Expected:** The training population and subject differ. Accountants completing cybersecurity training says nothing about forklift training.

**Model:** The criterion requires recording a strength when all forklift operators completed certified forklift safety training during 2025. Evidence E1 states that no forklift-operator training records were provided during 2025, but it does not explicitly state that the training was not completed. Since there is missing evidence regarding whether forklift operators actually completed the required training, the condition cannot be definitively evaluated.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 5; elapsed: 13.5s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires recording a strength when all forklift operators completed certified forklift safety training during 2025. Evidence E1 states that no forklift-operator training records were provided during 2025, but it does not explicitly state that the training was not completed. Since there is missing evidence regarding whether forklift operators actually completed the required training, the condition cannot be definitively evaluated.

### contradiction_unresolved

**Expected:** Equally authoritative contemporaneous reports conflict. Both must be cited and the conflict cannot be resolved from these inputs.

**Model:** The subject is 'warehouse sprinkler system' and the period in scope is '2025-06-30'. The evidence batch covers this date and subject. Observation E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. Observation E2 states that the same system was fully operational on 2025-06-30. These observations directly contradict each other regarding the state of the sprinkler system on the specified date. There are no additional supporting facts for either claim, and the contradiction is unresolved. The rule does not contain any explicit exception prerequisites or validity dates. There is an actual incompatible observation: E1 claims the system was inoperable while E2 claims it was fully operational on 2025-06-30. These observations concern the same subject and time, and neither has supported precedence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 3; model calls: 7; elapsed: 27.9s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if the warehouse sprinkler system was inoperable on 2025-06-30.", "scope_reason": "scope=in_scope because the evidence E1 directly addresses the warehouse sprinkler system's operability as of the specified date (2025-06-30) and is within the inspection scope (inspection:a). The rule applies to the warehouse sprinkler system, which is the subject of both inspection reports.", "scope": "in_scope", "condition_reason": "condition=true because evidence E1 explicitly states that the Warehouse A sprinkler system was inoperable on 2025-06-30, which matches the trigger condition exactly. The conflicting evidence E2 from inspection B stating the system was fully operational does not override this as it is not resolved and both inspections are independent with no documented precedence or correction.", "condition": "true", "exception_reason": "exception=does_not_apply because there are no exceptions specified in the criterion text that would negate or modify the stated condition for this case. The rule does not contain any conditional language that would exempt this situation.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "conflict=unresolved because there are two conflicting observations: E1 states the system was inoperable on 2025-06-30, while E2 states it was fully operational. No correction or precedence is documented between these inspections, leaving the truth of the condition unresolved.", "conflict": "unresolved", "findings": [{"subject": "Warehouse A sprinkler system", "evidence_ids": ["E1"], "reason": "The inspection report confirms that the warehouse sprinkler system was inoperable on 2025-06-30, triggering the concern as specified in criterion C1. However, due to unresolved conflict with E2, this finding is based on the available evidence only."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...lable evidence only.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Observation E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. Observation E2 states that the same system was fully operational on 2025-06-30. These observations directly contradict each other regarding the state of the sprinkler system on the specified date. There are no additional supporting facts for either claim, and the contradiction is unresolved. The rule does not contain any explicit exception prerequisites or validity dates.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### contradiction_explicit_correction

**Expected:** The explicit correction resolves the conflict for the same date. This is not missing evidence or an exclusion from scope.

**Model:** The subject is the warehouse sprinkler system, and the period in scope is 2025-06-30. Evidence E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since E2 supersedes E1, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational. Therefore, the trigger condition is false. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. Evidence E1 and E2 present contradictory observations regarding the status of the warehouse sprinkler system on 2025-06-30. However, E2 is a correction that supersedes E1, resolving the contradiction in favor of the system being operational. Therefore, there is no unresolved conflict.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 20.8s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining if the warehouse sprinkler system was inoperable on 2025-06-30. Although E1 initially states the system was inoperable, E2 provides a signed correction from the original inspector stating that the inoperable entry was a transcription error and that the system was fully operational on that date. This correction supersedes the initial report, directly contradicting the condition in the criterion.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Evidence E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since E2 supersedes E1, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational. Therefore, the trigger condition is false. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### exception_qualifies

**Expected:** The rule applies to this occupied building but its explicit exception defeats the concern. Certification is four months old and exceeds the 10-year threshold.

**Model:** The subject is Building A, which is occupied. The period in scope is as of 2025-07-01. Building A's roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. A licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life. Since 12 years is greater than or equal to 10 years, this certification satisfies the exception condition. Therefore, the trigger for flagging a concern does not apply. The exception applies because a licensed engineer certified at least 10 years of remaining useful life (12 years) within the past 12 months (the certification was on 2025-03-01, which is within 12 months of 2025-07-01). There are no conflicting observations regarding the roof age or the engineer's certification. The evidence supports that the roof is 25 years old and was certified with 12 years of remaining useful life, which satisfies the exception.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 8; elapsed: 32.0s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "For an occupied building, flag a concern for a roof older than 20 years", "scope_reason": "scope is in_scope because the subject 'Building A' is an occupied building and falls within the application:building scope as specified in the user request.", "scope": "in_scope", "condition_reason": "The condition is true because Building A is occupied and its roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold for flagging a concern.", "condition": "true", "exception_reason": "The exception does not apply because there is no evidence that a licensed engineer certified at least 10 years of remaining useful life within the past 12 months for Building A's roof. The absence of such certification means the exception cannot be established.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "conflict is unresolved because there is no contradictory evidence provided regarding the age of the roof or any certification; the only evidence confirms the roof is 25 years old and no certification is mentioned.", "conflict": "unresolved", "findings": [{"subject": "Building A", "evidence_ids": ["E1"], "reason": "Building A is occupied and its roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold for flagging a concern. No certification was provided to invoke the exception."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...nvoke the exception.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Negative-evidence review (C1):** `supported`. The criterion requires flagging a concern for a roof older than 20 years, except when a licensed engineer certified at least 10 years of remaining useful life within the past 12 months. Evidence E1 establishes that Building A's roof is 25 years old as of 2025-07-01, meeting the age condition. Evidence E2 states that on 2025-03-01, a licensed engineer certified that Building A's roof had 12 years of remaining useful life. Since 2025-03-01 is within the past 12 months from 2025-07-01, and 12 years exceeds the required 10 years of remaining useful life, the exception condition is met. Therefore, no concern should be flagged.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `applies`. Building A's roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. A licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life. Since 12 years is greater than or equal to 10 years, this certification satisfies the exception condition. Therefore, the trigger for flagging a concern does not apply. The exception applies because a licensed engineer certified at least 10 years of remaining useful life (12 years) within the past 12 months (the certification was on 2025-03-01, which is within 12 months of 2025-07-01).

### exception_scope_exclusion

**Expected:** The explicit fryer scope excludes this premises. No service history is needed to establish the exclusion.

**Model:** The subject is a commercial kitchen, and the period in scope is the past six months for hood suppression system service. The evidence indicates the premises operates as a cold-food sandwich shop with no deep-fat fryers or hot-cooking equipment. The rule's trigger requires a commercial kitchen with deep-fat fryers. Evidence E1 states that the premises operates exclusively as a cold-food sandwich shop and has no deep-fat fryers or hot-cooking equipment. This directly contradicts the subject requirement for the rule, making the condition false. The rule does not contain explicit exception prerequisites. Since the scope is out_of_scope due to lack of deep-fat fryers, no exception applies. There are no conflicting observations regarding the presence or absence of deep-fat fryers. The evidence clearly states there are none, which is sufficient to determine that the subject does not meet the rule's applicability criteria.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 1; model calls: 5; elapsed: 15.0s.

**Rejected responses:** condition_quote must be an exact excerpt from the requested criterion.text

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The rule's trigger requires a commercial kitchen with deep-fat fryers. Evidence E1 states that the premises operates exclusively as a cold-food sandwich shop and has no deep-fat fryers or hot-cooking equipment. This directly contradicts the subject requirement for the rule, making the condition false. The rule does not contain explicit exception prerequisites. Since the scope is out_of_scope due to lack of deep-fat fryers, no exception applies.

### multiple_concerns_one_source

**Expected:** A and B each warrant a separate concern; C does not. A single combined finding fails the requested output granularity even if it cites both roofs.

**Model:** The rule applies to occupied buildings with roofs older than 20 years. The evidence includes three buildings: Building A (24-year-old roof), Building B (31-year-old roof), and Building C (5-year-old roof). All three are occupied. Building A is occupied and has a 24-year-old roof, which is greater than 20 years. Building B is occupied and has a 31-year-old roof, which is also greater than 20 years. Building C is occupied but has a 5-year-old roof, which is not greater than 20 years. Therefore, the trigger condition is true for Buildings A and B, and false for Building C. There are no explicit exceptions mentioned in the rule text. No conflicting observations were found. All evidence supports the condition for Buildings A and B, and contradicts it for Building C.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 15.1s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Building A is occupied and has a 24-year-old roof, which is greater than 20 years. Building B is occupied and has a 31-year-old roof, which is also greater than 20 years. Building C is occupied but has a 5-year-old roof, which is not greater than 20 years. Therefore, the trigger condition is true for Buildings A and B, and false for Building C. There are no explicit exceptions mentioned in the rule text.

### multiple_strengths_across_sources

**Expected:** Each warehouse qualifies independently, requiring two strength records under C1. Cross-source consolidation must preserve the separate findings.

**Model:** The rule applies to individual warehouses, and both the North and South warehouses are mentioned as having monitored automatic sprinklers covering 100% of their floor areas. The scope is in_scope. Both E1 and E2 confirm that the North and South warehouses have monitored automatic sprinklers covering 100% of their respective floor areas. These observations directly support the trigger condition. There are no explicit exception prerequisites mentioned in the rule text for C1. Therefore, the exception status is does_not_apply. There are no conflicting observations regarding the sprinkler coverage in either warehouse. Both E1 and E2 support the same condition without contradiction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 20.0s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Both E1 and E2 confirm that the North and South warehouses have monitored automatic sprinklers covering 100% of their respective floor areas. These observations directly support the trigger condition. There are no explicit exception prerequisites mentioned in the rule text for C1. Therefore, the exception status is does_not_apply.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
