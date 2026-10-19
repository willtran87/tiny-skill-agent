# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T07:30:26.823376+00:00. State: **completed**.

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

**Model:** The rule applies to employees, and the evidence mentions 42 employees. The subject is in scope. The evidence does not contain any information about fire-safety training completion rates or numbers of employees who have completed the training. Therefore, it is impossible to determine whether the completion rate is below 90%. The condition is unknown. There are no explicit exception prerequisites mentioned in the rule. There are no conflicting observations in the provided evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 24.8s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence does not contain any information about fire-safety training completion rates or numbers of employees who have completed the training. Therefore, it is impossible to determine whether the completion rate is below 90%. The condition is unknown. There are no explicit exception prerequisites mentioned in the rule.

### unrelated_lexical_overlap

**Expected:** The training population and subject differ. Accountants completing cybersecurity training says nothing about forklift training.

**Model:** The rule applies to forklift operators. The evidence mentions office accountants completing cybersecurity training but does not mention any forklift operators or their training status. The evidence states 'No forklift-operator training records were provided.' This indicates that there is no documentation confirming whether forklift operators completed the required training. Since the rule requires all forklift operators to have completed certified forklift safety training during 2025, and no records are available to confirm this, the condition cannot be verified as true or false based on the provided evidence. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There is no conflicting evidence regarding forklift operator training in the provided information. The absence of records does not constitute a contradiction but rather an unknown status.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 11.1s.

**Independent review (C1):** scope `unknown`, condition `unknown`, exception `does_not_apply`. The evidence states 'No forklift-operator training records were provided.' This indicates that there is no documentation confirming whether forklift operators completed the required training. Since the rule requires all forklift operators to have completed certified forklift safety training during 2025, and no records are available to confirm this, the condition cannot be verified as true or false based on the provided evidence. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### contradiction_unresolved

**Expected:** Equally authoritative contemporaneous reports conflict. Both must be cited and the conflict cannot be resolved from these inputs.

**Model:** The subject is 'warehouse sprinkler system' and the period in scope is '2025-06-30'. The evidence batch includes observations about Warehouse A's sprinkler system on that date. Observation E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. Observation E2 states that the same system was fully operational on 2025-06-30. These observations directly contradict each other regarding the state of the sprinkler system on the specified date. There are no supporting facts for the trigger condition as both observations are equally valid and contradictory. There are no explicit exception prerequisites mentioned in the rule text. There is an actual incompatible observation: E1 reports the system was inoperable while E2 reports it was fully operational on 2025-06-30. These observations concern the same subject (warehouse A sprinkler system) and time (2025-06-30), and neither has supported precedence. This constitutes an unresolved conflict.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 1; model calls: 6; elapsed: 17.8s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Observation E1 states that the warehouse A sprinkler system was inoperable on 2025-06-30. Observation E2 states that the same system was fully operational on 2025-06-30. These observations directly contradict each other regarding the state of the sprinkler system on the specified date. There are no supporting facts for the trigger condition as both observations are equally valid and contradictory. There are no explicit exception prerequisites mentioned in the rule text.

### contradiction_explicit_correction

**Expected:** The explicit correction resolves the conflict for the same date. This is not missing evidence or an exclusion from scope.

**Model:** The subject is the warehouse sprinkler system, and the period in scope is 2025-06-30. Evidence E1 initially states that the warehouse sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since E2 supersedes E1, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. Evidence E1 and E2 present contradictory observations regarding the status of the warehouse sprinkler system on 2025-06-30. However, E2 is a correction that supersedes E1, resolving the contradiction in favor of the system being operational.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 1; model calls: 7; elapsed: 21.8s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "the warehouse sprinkler system was inoperable on 2025-06-30", "scope_reason": "The subject is the warehouse sprinkler system, and the period in scope is 2025-06-30.", "scope": "in_scope", "condition_reason": "Evidence E1 states that the warehouse sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since E2 supersedes E1, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational.", "condition": "false", "exception_reason": "There are no explicit exception prerequisites mentioned in the rule that would apply to this case.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "Evidence E1 and E2 present contradictory observations regarding the status of the warehouse sprinkler system on 2025-06-30. However, E2 is a correction that supersedes E1, resolving the contradiction in favor of the system being operational.", "conflict": "none", "findings": [{"subject": "warehouse sprinkler system", "evidence_ids": ["E1", "E2"], "reason": "Although E1 initially reported the system as inoperable on 2025-06-30, a correction from E2 issued on 2025-07-01 explicitly states that the sprinkler system was fully operational on that date. Since E2 supersedes E1, the system's status is confirmed as operational."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...rmed as operational.")]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Negative-evidence review (C1):** `supported`. The criterion requires determining if the warehouse sprinkler system was inoperable on 2025-06-30. Although E1 initially states the system was inoperable, E2 provides a signed correction that explicitly states the inoperable entry was a transcription error and that the system was fully operational on that date. This correction supersedes the initial report.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Evidence E1 initially states that the warehouse sprinkler system was inoperable on 2025-06-30. However, evidence E2 provides a signed correction issued on 2025-07-01, stating that the inoperable entry in R1 was a transcription error and that the sprinkler system was fully operational on 2025-06-30. Since E2 supersedes E1, the actual status of the sprinkler system on 2025-06-30 is confirmed as operational. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### exception_qualifies

**Expected:** The rule applies to this occupied building but its explicit exception defeats the concern. Certification is four months old and exceeds the 10-year threshold.

**Model:** The subject is Building A, which is occupied. The period in scope is as of 2025-07-01. Building A's roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. The certified remaining useful life is 12 years as of 2025-03-01. Since this certification was within the past 12 months (2025-03-01 to 2025-07-01), it satisfies the exception condition for a licensed engineer's certification of at least 10 years of remaining useful life. The exception applies because a licensed engineer certified that Building A's roof had at least 10 years of remaining useful life (12 years) within the past 12 months (as of 2025-03-01). No conflicting observations exist. The evidence supports that the roof is older than 20 years but also confirms a valid certification of remaining useful life within the exception period.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 27.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion requires a licensed engineer to have certified at least 10 years of remaining useful life within the past 12 months. The evidence shows that on 2025-03-01, a licensed engineer certified Building A's roof had 12 years of remaining useful life, which satisfies the condition. Therefore, the concern should not be flagged.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `applies`. Building A's roof is 25 years old as of 2025-07-01, which exceeds the 20-year threshold. The certified remaining useful life is 12 years as of 2025-03-01. Since this certification was within the past 12 months (2025-03-01 to 2025-07-01), it satisfies the exception condition for a licensed engineer's certification of at least 10 years of remaining useful life. The exception applies because a licensed engineer certified that Building A's roof had at least 10 years of remaining useful life (12 years) within the past 12 months (as of 2025-03-01).

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### exception_scope_exclusion

**Expected:** The explicit fryer scope excludes this premises. No service history is needed to establish the exclusion.

**Model:** The rule explicitly restricts application to 'commercial kitchens with deep-fat fryers'. The evidence states that the premises operates exclusively as a cold-food sandwich shop and has no deep-fat fryers. The trigger condition requires that the hood suppression system has not been serviced in the past six months. However, since the premises has no deep-fat fryers, it does not meet the scope requirement for this rule. The lack of deep-fat fryers means the rule's applicability is excluded regardless of service history. There are no explicit exception prerequisites mentioned in the rule text that would apply to this case. No conflicting observations exist. The evidence clearly states the premises has no deep-fat fryers, which directly excludes it from the rule's scope.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 10.3s.

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The trigger condition requires that the hood suppression system has not been serviced in the past six months. However, since the premises has no deep-fat fryers, it does not meet the scope requirement for this rule. The lack of deep-fat fryers means the rule's applicability is excluded regardless of service history. There are no explicit exception prerequisites mentioned in the rule text that would apply to this case.

### multiple_concerns_one_source

**Expected:** A and B each warrant a separate concern; C does not. A single combined finding fails the requested output granularity even if it cites both roofs.

**Model:** The rule applies to occupied buildings with roofs older than 20 years. The subject is the occupancy status and roof age of each building. Building A is occupied and has a 24-year-old roof (24 > 20), which supports the trigger. Building B is occupied and has a 31-year-old roof (31 > 20), which also supports the trigger. Building C is occupied but has a 5-year-old roof (5 ≤ 20), which does not support the trigger. There are no explicit exceptions mentioned in the rule. No conflicting observations found. All buildings' statuses and roof ages are clearly stated without contradiction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 13.8s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Building A is occupied and has a 24-year-old roof (24 > 20), which supports the trigger. Building B is occupied and has a 31-year-old roof (31 > 20), which also supports the trigger. Building C is occupied but has a 5-year-old roof (5 ≤ 20), which does not support the trigger. There are no explicit exceptions mentioned in the rule.

### multiple_strengths_across_sources

**Expected:** Each warehouse qualifies independently, requiring two strength records under C1. Cross-source consolidation must preserve the separate findings.

**Model:** The rule applies to individual warehouses, and both the North and South warehouses are mentioned as having monitored automatic sprinklers covering 100% of their floor areas. Both E1 and E2 confirm that the North and South warehouses have monitored automatic sprinklers covering 100% of their respective floor areas. These observations directly support the trigger condition of the rule, which requires a separate strength to be recorded for each warehouse meeting this criterion. There are no explicit exception prerequisites mentioned in the rule that would apply to either warehouse. There are no conflicting observations regarding the sprinkler coverage of the North or South warehouses. Both E1 and E2 support the same condition without contradiction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 17.0s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Both E1 and E2 confirm that the North and South warehouses have monitored automatic sprinklers covering 100% of their respective floor areas. These observations directly support the trigger condition of the rule, which requires a separate strength to be recorded for each warehouse meeting this criterion. There are no explicit exception prerequisites mentioned in the rule that would apply to either warehouse.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
