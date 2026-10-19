# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T06:49:43.446963+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **8/8** (planned: 8).
- Correct case statuses: **8/8**.
- Required gold evidence cited: **10/10**.
- Reference/provenance checks: **35/35**.
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

**Model:** The rule applies to employees in the organization. The evidence E1 states there are 42 employees, which is the subject of the rule. The evidence does not contain any information about fire-safety training completion rates or numbers of employees who have completed the training. Therefore, it is impossible to determine whether the completion rate is below 90%. The condition is unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations in the provided evidence that would create an unresolved contradiction regarding the fire-safety training completion rate.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 9.7s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence does not contain any information about fire-safety training completion rates or numbers of employees who have completed the training. Therefore, it is impossible to determine whether the completion rate is below 90%. The condition is unknown. There are no explicit exception prerequisites mentioned in the rule text for C1.

### unrelated_lexical_overlap

**Expected:** The training population and subject differ. Accountants completing cybersecurity training says nothing about forklift training.

**Model:** The criterion requires that all forklift operators completed certified forklift safety training during 2025. Evidence E1 states that no forklift-operator training records were provided, but it does not explicitly state whether the training was or was not completed. Since there is a lack of evidence regarding the completion of forklift operator training, and the absence of records does not prove that the training did not occur, the condition cannot be confirmed as false based on the available information.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 12.5s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that all forklift operators completed certified forklift safety training during 2025. Evidence E1 states that no forklift-operator training records were provided, but it does not explicitly state whether the training was or was not completed. Since there is a lack of evidence regarding the completion of forklift operator training, and the absence of records does not prove that the training did not occur, the condition cannot be confirmed as false based on the available information.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### contradiction_unresolved

**Expected:** Equally authoritative contemporaneous reports conflict. Both must be cited and the conflict cannot be resolved from these inputs.

**Model:** The subject is 'warehouse sprinkler system' and the period in scope is '2025-06-30'. The evidence batch includes observations about Warehouse A. Observation E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. Observation E2 states that the warehouse A sprinkler system was fully operational on 2025-06-30. These observations directly contradict each other regarding the state of the sprinkler system on the same date. There are no supporting facts for the trigger condition as both observations are equally valid and there is no resolution provided. There are no explicit exception prerequisites mentioned in the rule. There is an actual incompatible observation. E1 reports the system was inoperable on 2025-06-30, while E2 reports it was fully operational on the same date. These observations are about the same subject (warehouse A sprinkler system) and time (2025-06-30), making them contradictory.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 1; model calls: 6; elapsed: 18.1s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Observation E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. Observation E2 states that the warehouse A sprinkler system was fully operational on 2025-06-30. These observations directly contradict each other regarding the state of the sprinkler system on the same date. There are no supporting facts for the trigger condition as both observations are equally valid and there is no resolution provided. There are no explicit exception prerequisites mentioned in the rule.

### contradiction_explicit_correction

**Expected:** The explicit correction resolves the conflict for the same date. This is not missing evidence or an exclusion from scope.

**Model:** The subject is the warehouse sprinkler system, and the period in scope is 2025-06-30. Evidence E1 initially states that the warehouse sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since E2 supersedes E1, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. Evidence E1 and E2 present contradictory observations regarding the status of the warehouse sprinkler system on 2025-06-30. However, E2 is a correction that supersedes E1, resolving the contradiction in favor of the system being operational.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 1; model calls: 7; elapsed: 20.7s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "the warehouse sprinkler system was inoperable on 2025-06-30", "scope_reason": "The subject is the warehouse sprinkler system, and the period in scope is 2025-06-30.", "scope": "in_scope", "condition_reason": "Evidence E1 states that the warehouse sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since E2 supersedes E1, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational.", "condition": "false", "exception_reason": "There are no explicit exception prerequisites mentioned in the rule that would apply to this case.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "Evidence E1 and E2 present contradictory observations regarding the status of the warehouse sprinkler system on 2025-06-30. However, E2 is a correction that supersedes E1, resolving the contradiction in favor of the system being operational.", "conflict": "none", "findings": [{"subject": "warehouse sprinkler system", "evidence_ids": ["E1", "E2"], "reason": "Although E1 initially reported the system as inoperable on 2025-06-30, a correction from E2 issued on 2025-07-01 explicitly states that the sprinkler system was fully operational on that date. Since E2 supersedes E1, the system's status is confirmed as operational."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...rmed as operational.")]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Negative-evidence review (C1):** `supported`. The criterion requires determining if the warehouse sprinkler system was inoperable on 2025-06-30. Although E1 initially states the system was inoperable, E2 provides a signed correction from the original inspector stating that the inoperable entry was a transcription error and that the system was fully operational on that date. This correction supersedes the initial report and directly contradicts the condition in C1.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Evidence E1 initially states that the warehouse sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since E2 supersedes E1, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### exception_qualifies

**Expected:** The rule applies to this occupied building but its explicit exception defeats the concern. Certification is four months old and exceeds the 10-year threshold.

**Model:** The subject is Building A, which is occupied. The period in scope is as of 2025-07-01. Building A's roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. A licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life. Since 2025-03-01 is within the past 12 months (as of 2025-07-01), and 12 years > 10 years, this certification satisfies the exception condition. The exception applies because a licensed engineer certified at least 10 years of remaining useful life (12 years) within the past 12 months (on 2025-03-01). No actual incompatible observations exist. The engineer's certification supports the exception and contradicts the trigger condition, but does not create an unresolved conflict since it is a valid exception.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 24.6s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The roof of Building A is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. However, a licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life, which satisfies the exception condition of at least 10 years of remaining useful life within the past 12 months. Therefore, the criterion's condition is false because the exception applies.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `applies`. Building A's roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. A licensed engineer certified on 2025-03-01 that Building A's roof had 12 years of remaining useful life. Since 2025-03-01 is within the past 12 months (as of 2025-07-01), and 12 years > 10 years, this certification satisfies the exception condition. The exception applies because a licensed engineer certified at least 10 years of remaining useful life (12 years) within the past 12 months (on 2025-03-01).

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### exception_scope_exclusion

**Expected:** The explicit fryer scope excludes this premises. No service history is needed to establish the exclusion.

**Model:** The subject is a commercial kitchen, and the rule's applicability is limited to those with deep-fat fryers. The evidence indicates the premises operates as a cold-food sandwich shop with no deep-fat fryers or hot-cooking equipment. The evidence states that the premises operates exclusively as a cold-food sandwich shop and has no deep-fat fryers. Since the rule applies only to commercial kitchens with deep-fat fryers, this subject does not meet the applicability criteria for the rule's trigger condition. The rule does not contain explicit exception prerequisites. The scope restriction is based on the type of equipment present rather than any exception logic. There are no conflicting observations regarding the presence or absence of deep-fat fryers. The evidence clearly states there are none, which is consistent with the rule's scope restriction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 1; model calls: 5; elapsed: 13.0s.

**Rejected responses:** condition_quote must be an exact excerpt from the requested criterion.text

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The evidence states that the premises operates exclusively as a cold-food sandwich shop and has no deep-fat fryers. Since the rule applies only to commercial kitchens with deep-fat fryers, this subject does not meet the applicability criteria for the rule's trigger condition. The rule does not contain explicit exception prerequisites. The scope restriction is based on the type of equipment present rather than any exception logic.

### multiple_concerns_one_source

**Expected:** A and B each warrant a separate concern; C does not. A single combined finding fails the requested output granularity even if it cites both roofs.

**Model:** The rule applies to occupied buildings with roofs older than 20 years. The subject is the building's occupancy status and roof age. Building A is occupied and has a 24-year-old roof (24 > 20). Building B is occupied and has a 31-year-old roof (31 > 20). Building C is occupied but has a 5-year-old roof (5 <= 20). Therefore, Buildings A and B meet the condition, while Building C does not. There are no explicit exceptions mentioned in the rule. No conflicting observations found. All buildings' statuses and roof ages are clearly stated without contradiction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 13.8s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Building A is occupied and has a 24-year-old roof (24 > 20). Building B is occupied and has a 31-year-old roof (31 > 20). Building C is occupied but has a 5-year-old roof (5 <= 20). Therefore, Buildings A and B meet the condition, while Building C does not. There are no explicit exceptions mentioned in the rule.

### multiple_strengths_across_sources

**Expected:** Each warehouse qualifies independently, requiring two strength records under C1. Cross-source consolidation must preserve the separate findings.

**Model:** The rule applies to warehouses with monitored automatic sprinklers covering 100% of their floor area. The evidence includes observations about the North and South warehouses. Both E1 and E2 confirm that the North and South warehouses have monitored automatic sprinklers covering 100% of their respective floor areas. These observations directly support the trigger condition. There are no explicit exception prerequisites mentioned in the rule. The rule does not specify any conditions under which this strength would not apply. There are no conflicting observations regarding the sprinkler coverage in either warehouse. Both E1 and E2 support the same condition without contradiction.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 15.1s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Both E1 and E2 confirm that the North and South warehouses have monitored automatic sprinklers covering 100% of their respective floor areas. These observations directly support the trigger condition. There are no explicit exception prerequisites mentioned in the rule. The rule does not specify any conditions under which this strength would not apply.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
