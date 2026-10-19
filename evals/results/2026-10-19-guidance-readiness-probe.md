# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T06:44:10.655142+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **0/4** (planned: 4).
- Correct case statuses: **4/4**.
- Required gold evidence cited: **7/7**.
- Reference/provenance checks: **23/23**.
- False-positive findings in the 1 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| auto_incident_rate_calculation | matched | matched | 1 / 1 | 2 / 2 | FAIL |
| property_cross_source_alarm_and_value | matched | matched | 1 / 1 | 2 / 2 | FAIL |
| gl_loss_aggregation_without_duplicate | matched | matched | 1 / 1 | 1 / 1 | FAIL |
| cyber_restore_duration_cross_midnight | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |

## Reasons and diagnostics

### auto_incident_rate_calculation

**Expected:** Three divided by 24 times 100 is 12.5, above 10. This is one aggregate finding, not three separate collision findings.

**Model:** The rule applies to the fleet level for the year 2025. The subject is Summit Couriers, which is a single fleet entity. The time period in scope is 2025. The preventable collision count for 2025 is 3 (from E1). The active fleet count is 24 (from E2). The frequency is calculated as (3 collisions / 24 vehicles) * 100 = 12.5 collisions per 100 vehicles. Since 12.5 > 10, the condition is true. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations in the evidence provided that would create an unresolved contradiction regarding the preventable collision count or the active fleet count.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 39.1s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The preventable collision count for 2025 is 3 (from E1). The active fleet count is 24 (from E2). The frequency is calculated as (3 collisions / 24 vehicles) * 100 = 12.5 collisions per 100 vehicles. Since 12.5 > 10, the condition is true. There are no explicit exception prerequisites mentioned in the rule text for C1.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_cross_source_alarm_and_value

**Expected:** The value and whole-stock alarm condition require combining both sources into one strength.

**Model:** The subject is Haven Parts, and the period in scope is as of 2025-09-01, based on the evidence dates. The evidence covers all insured stock for this date. The entire insured stock is in a continuously monitored intruder-alarm area: E2 confirms that the entire interior of Haven Parts' sole warehouse is covered by an intruder alarm with continuous remote monitoring as of 2025-09-01. The total declared stock value is $425,000 (E1), which is no greater than $500,000. Both conditions of the trigger are met. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case. There are no actual incompatible observations. Both E1 and E2 support the trigger condition without contradiction.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 17.8s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The entire insured stock is in a continuously monitored intruder-alarm area: E2 confirms that the entire interior of Haven Parts' sole warehouse is covered by an intruder alarm with continuous remote monitoring as of 2025-09-01. The total declared stock value is $425,000 (E1), which is no greater than $500,000. Both conditions of the trigger are met. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case.

### gl_loss_aggregation_without_duplicate

**Expected:** Distinct claims sum to $325,000, above $300,000. Do not add the repeated GL-101 again or create a finding per claim.

**Model:** The rule applies to 2025 general liability claims. Evidence E1 lists two distinct 2025 claims (GL-101 and GL-102), which are the only 2025 GL claims in the evidence batch. The rule requires counting each claim ID once using its latest paid amount. Claim GL-101 has a paid amount of $150,000 (from E1). Claim GL-102 has a paid amount of $175,000 (from E1). The broker's note (E2) confirms that GL-101 is duplicated and not an additional claim. Therefore, only two distinct claims are counted: GL-101 ($150,000) and GL-102 ($175,000). Total paid amount = $150,000 + $175,000 = $325,000. Comparison: $325,000 > $300,000. The condition is true. The rule does not specify any exceptions. There are no explicit exception prerequisites or validity dates mentioned in the guideline. There are no conflicting observations regarding the paid amounts or claim IDs for 2025 general liability claims. The broker's note (E2) clarifies that GL-101 is a duplicate reference, not an additional claim, which supports rather than contradicts the claim count. No unresolved contradictions exist.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 4; model calls: 8; elapsed: 33.4s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000. Count each claim ID once, using its latest stated paid amount.", "scope_reason": "The scope is whole_case, which indicates the assessment applies to the entire case file; there are no explicit exclusions for the subject matter in the rule text.", "scope": "in_scope", "condition_reason": "There are two distinct 2025 general liability claims: GL-101 with a paid amount of $150,000 and GL-202 with a paid amount of $175,000. The total paid amount is $325,000, which exceeds the threshold of $300,000. Each claim ID is counted once using its latest stated paid amount.", "condition": "true", "exception_reason": "There are no exceptions explicitly stated in the rule that would apply to this case.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "The evidence shows a potential conflict: E1 lists two separate claims (GL-101 and GL-102) with paid amounts of $150,000 and $175,000 respectively. E2 indicates that the broker's note repeats claim GL-101 at its same latest paid amount of $150,000, suggesting a duplicate reference rather than an additional claim. However, since the rule requires counting each claim ID once using its latest stated paid amount and does not specify how to handle duplicates, the conflict is unresolved.", "conflict": "unresolved", "findings": [{"subject": "whole_case", "evidence_ids": ["E1"], "reason": "The total paid amounts for distinct 2025 general liability claims (GL-101 at $150,000 and GL-202 at $175,000) sum to $325,000, which exceeds the $300,000 threshold. The duplicate reference in E2 does not alter this calculation as it refers to the same claim ID."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...o the same claim ID.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000. Count each claim ID once, using its latest stated paid amount.", "scope_reason": "The scope is whole_case, which indicates the assessment applies to the entire case file; there are no explicit exclusions for the subject matter in the rule text.", "scope": "in_scope", "condition_reason": "There are two distinct 2025 general liability claims: GL-101 with a paid amount of $150,000 and GL-202 with a paid amount of $175,000. The total paid amount is $325,000, which exceeds the threshold of $30300,000. Each claim ID is counted once using its latest stated paid amount.", "condition": "true", "exception_reason": "There are no exceptions explicitly stated in the rule that would apply to this case.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "The evidence shows a potential conflict: E1 lists two separate claims (GL-101 and GL-202) with paid amounts of $150,000 and $175,000 respectively. E2 indicates that the broker's note repeats claim GL-101 at its same latest paid amount of $150,000, suggesting a duplicate reference rather than an additional claim. However, since the rule requires counting each claim ID once using its latest stated paid amount and does not specify how to handle duplicates, the conflict is unresolved.", "conflict": "unresolved", "findings": [{"subject": "whole_case", "evidence_ids": ["E1"], "reason": "The total paid amounts for distinct 2025 general liability claims (GL-101 at $150,000 and GL-202 at $175,000) sum to $325,000, which exceeds the $300,000 threshold. The duplicate reference in E2 does not alter this calculation as it refers to the same claim ID."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...o the same claim ID.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000. Count each claim ID once, using its latest stated paid amount.", "scope_reason": "The scope is whole_case, which indicates the assessment applies to the entire case file; there are no explicit exclusions for the subject matter in the rule text.", "scope": "in_scope", "condition_reason": "There are two distinct 2025 general liability claims: GL-101 with a paid amount of $150,000 and GL-102 with a paid amount of $175,000. The total paid amount is $325,000, which exceeds the threshold of $300,000. Each claim ID is counted once using its latest stated paid amount.", "condition": "true", "exception_reason": "There are no exceptions explicitly stated in the rule that would apply to this case.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "The evidence shows a potential conflict: E1 lists two separate claims (GL-101 and GL-102) with paid amounts of $150,000 and $175,000 respectively. E2 indicates that the broker's note repeats claim GL-101 at its same latest paid amount of $150,000, suggesting a duplicate reference rather than an additional claim. However, since the rule requires counting each claim ID once using its latest stated paid amount and does not specify how to handle duplicates, the conflict is unresolved.", "conflict": "unresolved", "findings": [{"subject": "whole_case", "evidence_ids": ["E1"], "reason": "The total paid amounts for distinct 2025 general liability claims (GL-101 at $150,000 and GL-102 at $175,000) sum to $325,000, which exceeds the $300,000 threshold. The duplicate reference in E2 does not alter this calculation as it refers to the same claim ID."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...o the same claim ID.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; Scope/exception quotations must occur in criterion.text or its same-source context

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The rule requires counting each claim ID once using its latest paid amount. Claim GL-101 has a paid amount of $150,000 (from E1). Claim GL-102 has a paid amount of $175,000 (from E1). The broker's note (E2) confirms that GL-101 is duplicated and not an additional claim. Therefore, only two distinct claims are counted: GL-101 ($150,000) and GL-102 ($175,000). Total paid amount = $150,000 + $175,000 = $325,000. Comparison: $325,000 > $300,000. The condition is true. The rule does not specify any exceptions. There are no explicit exception prerequisites or validity dates mentioned in the guideline.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_restore_duration_cross_midnight

**Expected:** Elapsed time is 25.5 hours, exceeding the 24-hour maximum despite a successful eventual restore.

**Model:** The subject is the full restore of the payroll application, and the period in scope is from 2025-08-01 08:00 UTC to 2025-08-02 09:30 UTC. The restore started at 2025-08-01 08:00 UTC and completed at 2025-08-02 09:30 UTC. Elapsed time = 25 hours and 30 minutes. Since the elapsed time exceeds 24 hours, the condition is false. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case. There are no conflicting observations in the provided evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 21.2s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion requires determining whether the completed full restore of the payroll application took no longer than 24 hours, using the supplied UTC start and completion timestamps. The start timestamp is 2025-08-01 08:00 UTC (E1) and the completion timestamp is 2025-08-02 09:30 UTC (E2). Calculating the elapsed time: from 08:00 on August 1 to 09:30 on August 2 is exactly 25 hours and 30 minutes. This exceeds the 24-hour threshold specified in the criterion, making the condition false.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The restore started at 2025-08-01 08:00 UTC and completed at 2025-08-02 09:30 UTC. Elapsed time = 25 hours and 30 minutes. Since the elapsed time exceeds 24 hours, the condition is false. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
