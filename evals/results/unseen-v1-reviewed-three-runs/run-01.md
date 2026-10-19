# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T00:02:21.034554+00:00. State: **interrupted**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **8/14** (planned: 32).
- Correct case statuses: **9/14**.
- Required gold evidence cited: **15/16**.
- Reference/provenance checks: **50/50**.
- False-positive findings in the 10 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| cyber_remote_access_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_pump_service_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_driver_screening_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| gl_subcontract_limit_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_incident_rate_calculation | matched | insufficient_evidence | 0 / 1 | 2 / 2 | FAIL |
| property_reserves_exact_threshold | matched | insufficient_evidence | 0 / 1 | 1 / 1 | FAIL |
| property_roof_exact_boundary | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| cyber_patch_coverage_boundary | matched | insufficient_evidence | 0 / 1 | 1 / 1 | FAIL |
| property_alarm_equal_reports | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| cyber_backup_immutability_conflict | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| auto_mileage_corrected_denominator | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| property_later_repair_does_not_rewrite_history | matched | missing | 0 / 1 | 0 / 1 | FAIL |
| property_electrical_exception | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| cyber_service_account_exception | no_match | insufficient_evidence | 0 / 0 | 2 / 2 | FAIL |

## Reasons and diagnostics

### cyber_remote_access_unknown

**Expected:** Administrator MFA does not establish workforce MFA; blank or unavailable records do not prove absence of the control.

**Model:** The subject is remote workforce login to Harbor Analytics. The period in scope is as of 2025-09-01. Facts that PROVE the quoted trigger: E1 states that MFA is enabled for all four cloud administrators, but does not confirm MFA for the entire remote workforce. E2 indicates that a VPN configuration report was requested but not available, and the broker has not verified remote-login configuration. Facts that REFUTE the quoted trigger: E1 shows no confirmation of MFA for ordinary workforce remote access; E2 confirms lack of verification of remote-login configuration. Given unknown information, it is possible that MFA protects all remote workforce logins, but this cannot be confirmed from the evidence provided. Therefore, condition=true. The rule does not specify any explicit exceptions. Therefore, exception=does_not_apply.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 1; model calls: 5; elapsed: 14.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts that PROVE the quoted trigger: E1 states that MFA is enabled for all four cloud administrators, but does not confirm MFA for the entire remote workforce. E2 indicates that a VPN configuration report was requested but not available, and the broker has not verified remote-login configuration. Facts that REFUTE the quoted trigger: E1 shows no confirmation of MFA for ordinary workforce remote access; E2 confirms lack of verification of remote-login configuration. Given unknown information, it is possible that MFA protects all remote workforce logins, but this cannot be confirmed from the evidence provided. Therefore, condition=true. The rule does not specify any explicit exceptions. Therefore, exception=does_not_apply.

### property_pump_service_unknown

**Expected:** Unlocated records and a visual inspection cannot establish a missed service visit.

**Model:** The subject is the fire pump at Cedar Components, and the period in scope is calendar 2025. The quoted trigger requires determining whether the fire pump at Cedar Components was not serviced during 2025. Evidence E1 states that the maintenance binder was held off site and unavailable to the surveyor, which does not confirm or refute service activity in 2025. Evidence E2 indicates that the pump contractor's 2025 service invoice cannot be located, and the contractor's archive is still being checked, with no assertion that the work did not occur. These facts do not prove the fire pump was serviced during 2025, but they also do not definitively prove it was not serviced. Therefore, the condition is unknown. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this situation.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 10.0s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The quoted trigger requires determining whether the fire pump at Cedar Components was not serviced during 2025. Evidence E1 states that the maintenance binder was held off site and unavailable to the surveyor, which does not confirm or refute service activity in 2025. Evidence E2 indicates that the pump contractor's 2025 service invoice cannot be located, and the contractor's archive is still being checked, with no assertion that the work did not occur. These facts do not prove the fire pump was serviced during 2025, but they also do not definitively prove it was not serviced. Therefore, the condition is unknown. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this situation.

### auto_driver_screening_unknown

**Expected:** Neither the interview process nor missing files establishes whether all MVR reviews occurred.

**Model:** Subject is employed drivers; period in scope is before hire. Facts that PROVE the trigger: None explicitly stated. Facts that REFUTE the trigger: E1 states 'The MVR review field is unanswered' indicating no confirmation of MVR review; E2 states 'The driver files have not been provided' and 'no statement from the applicant confirming or denying pre-hire MVR reviews,' which means there's no evidence of MVR review. Given unknown information, it cannot be confirmed that MVR reviews were conducted for every employed driver before hire. Condition is FALSE because there is no evidence supporting the trigger. Rule does not specify any exceptions.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 4; elapsed: 8.5s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the trigger: None explicitly stated. Facts that REFUTE the trigger: E1 states 'The MVR review field is unanswered' indicating no confirmation of MVR review; E2 states 'The driver files have not been provided' and 'no statement from the applicant confirming or denying pre-hire MVR reviews,' which means there's no evidence of MVR review. Given unknown information, it cannot be confirmed that MVR reviews were conducted for every employed driver before hire. Condition is FALSE because there is no evidence supporting the trigger. Rule does not specify any exceptions.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_subcontract_limit_unknown

**Expected:** Unspecified insurance limits cannot satisfy or disprove the $2 million requirement.

**Model:** The subject is active roofing subcontractors. The period in scope is the assessment period, as indicated by the evidence context. Facts that PROVE the quoted trigger: None. Facts that REFUTE the quoted trigger: E1 states that both subcontractors (North Roof and Ridge Team) are marked insured in the vendor register, but the register does not record limits or policy numbers; E2 states that certificates for both subcontractors have been requested but not received, and their general liability limits have not been confirmed. Could it still be true given unknown information? Yes, but only if the limits are confirmed to be at least $2 million, which is not established. Condition is FALSE because there is no evidence of the required limits being met. There are no explicit exception prerequisites mentioned in the rule.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 10.1s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the quoted trigger: None. Facts that REFUTE the quoted trigger: E1 states that both subcontractors (North Roof and Ridge Team) are marked insured in the vendor register, but the register does not record limits or policy numbers; E2 states that certificates for both subcontractors have been requested but not received, and their general liability limits have not been confirmed. Could it still be true given unknown information? Yes, but only if the limits are confirmed to be at least $2 million, which is not established. Condition is FALSE because there is no evidence of the required limits being met. There are no explicit exception prerequisites mentioned in the rule.

### auto_incident_rate_calculation

**Expected:** Three divided by 24 times 100 is 12.5, above 10. This is one aggregate finding, not three separate collision findings.

**Model:** The subject is Summit Couriers, and the period in scope is 2025. Facts that PROVE this quoted trigger: E1 shows Summit Couriers recorded three preventable collisions during 2025. E2 shows Summit operated 24 active vehicles throughout 2025. Facts that REFUTE it: None. Could it still be true given unknown information? Yes, if the actual number of active vehicles was higher than 24 or if more preventable collisions occurred. Calculation: (3 collisions / 24 active vehicles) * 100 = 12.5 collisions per 100 active vehicles. Since 12.5 > 10, the condition is true. A rule without exceptions uses does_not_apply. There are no explicit exception prerequisites mentioned in the guideline.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 1; model calls: 5; elapsed: 14.4s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one fleet-level concern if 2025 preventable collision frequency exceeds 10 collisions per 100 active vehicles. Use the stated active fleet count as denominator.", "scope_reason": "The subject is Summit Couriers, and the period in scope is 2025.", "scope": "in_scope", "condition_reason": "Facts that PROVE this quoted trigger: E1 shows Summit Couriers recorded three preventable collisions during 2025. E2 shows Summit operated 24 active vehicles throughout 2025. Facts that REFUTE it: None. Could it still be true given unknown information? Yes, if the actual number of active vehicles was higher than 24 or if more preventable collisions occurred. Calculation: (3 collisions / 24 active vehicles) * 100 = 12.5 collisions per 100 active vehicles. Since 12.5 > 10, the condition is true.", "condition": "true", "exception_reason": "A rule without exceptions uses does_not_apply. There are no explicit exception prerequisites mentioned in the guideline.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict": "unresolved", "findings": [{"subject": "Summit Couriers", "evidence_ids": ["E1", "E2"], "reason": "Summit Couriers recorded three preventable collisions during 2025, operating 24 active vehicles. The collision frequency of 12.5 per 100 active vehicles exceeds the threshold of 10 per 100 active vehicles, triggering a fleet-level concern."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...fleet-level concern.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE this quoted trigger: E1 shows Summit Couriers recorded three preventable collisions during 2025. E2 shows Summit operated 24 active vehicles throughout 2025. Facts that REFUTE it: None. Could it still be true given unknown information? Yes, if the actual number of active vehicles was higher than 24 or if more preventable collisions occurred. Calculation: (3 collisions / 24 active vehicles) * 100 = 12.5 collisions per 100 active vehicles. Since 12.5 > 10, the condition is true. A rule without exceptions uses does_not_apply. There are no explicit exception prerequisites mentioned in the guideline.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_reserves_exact_threshold

**Expected:** 480,000 / 120,000 equals exactly four months; at least includes equality.

**Model:** The subject is Bay Storage, and the period in scope is as of 2025-08-31, based on the evidence provided. Facts that PROVE the quoted trigger: The evidence states that Bay Storage's unrestricted cash is $480,000 and its monthly operating expense is $120,000 as of 2025-08-31. Calculation: $480,000 / $120,000 = 4 months. This meets the 'at least four months' requirement.

Facts that REFUTE the quoted trigger: None.

Could it still be true given unknown information? No additional information is needed to confirm the trigger since all required data is provided and sufficient for evaluation.

Condition status: true The rule does not specify any explicit exceptions or prerequisites that would prevent applying this strength. Therefore, no exception applies.

Exception status: does_not_apply

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 1; model calls: 4; elapsed: 19.2s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Record a strength if Bay Storage holds unrestricted cash reserves covering at least four months of its stated operating expense.", "scope_reason": "The subject is Bay Storage, and the period in scope is as of 2025-08-31, based on the evidence provided.", "scope": "in_scope", "condition_reason": "Facts that PROVE the quoted trigger: The evidence states that Bay Storage's unrestricted cash is $480,000 and its monthly operating expense is $120,000 as of 2025-08-31. Calculation: $480,000 / $120,000 = 4 months. This meets the 'at least four months' requirement.\n\nFacts that REFUTE the quoted trigger: None.\n\nCould it still be true given unknown information? No additional information is needed to confirm the trigger since all required data is provided and sufficient for evaluation.\n\nCondition status: true", "condition": "true", "exception_reason": "The rule does not specify any explicit exceptions or prerequisites that would prevent applying this strength. Therefore, no exception applies.\n\nException status: does_not_apply", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict": "unresolved", "findings": [{"subject": "Bay Storage", "evidence_ids": ["E1"], "reason": "Bay Storage holds unrestricted cash reserves of $480,000, which covers exactly four months of its stated monthly operating expense of $120,000. This meets the guideline's requirement for recording a strength."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...ecording a strength.")]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE the quoted trigger: The evidence states that Bay Storage's unrestricted cash is $480,000 and its monthly operating expense is $120,000 as of 2025-08-31. Calculation: $480,000 / $120,000 = 4 months. This meets the 'at least four months' requirement.

Facts that REFUTE the quoted trigger: None.

Could it still be true given unknown information? No additional information is needed to confirm the trigger since all required data is provided and sufficient for evaluation.

Condition status: true The rule does not specify any explicit exceptions or prerequisites that would prevent applying this strength. Therefore, no exception applies.

Exception status: does_not_apply

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_roof_exact_boundary

**Expected:** Exactly 20 does not exceed a strictly greater-than-20 threshold.

**Model:** The subject is the roof at Unit 7, and the period in scope is the assessment date of 2025-07-01. The evidence states that 'Unit 7's roof was installed on 2005-07-01' and 'the survey dated 2025-07-01 records an age of exactly 20 years.' This means the roof is exactly 20 years old on the assessment date. The trigger requires the roof to be strictly older than 20 years, which is not met since it is exactly 20 years old. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 8.3s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that 'Unit 7's roof was installed on 2005-07-01' and 'the survey dated 2025-07-01 records an age of exactly 20 years.' This means the roof is exactly 20 years old on the assessment date. The trigger requires the roof to be strictly older than 20 years, which is not met since it is exactly 20 years old. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule.

### cyber_patch_coverage_boundary

**Expected:** 95/100 equals 95%, meeting an inclusive threshold despite five exceptions.

**Model:** The subject is '100 in-scope servers' and the period in scope is 'within 14 days of release'. The payload scope covers the whole case, which includes the relevant evidence batch. Facts that PROVE the quoted trigger: 95 out of 100 servers (95%) met the 14-day critical-patch deadline. Facts that REFUTE it: 3 servers were patched on day 20, and 2 remain outstanding, meaning they did not meet the 14-day deadline. Given these facts, the condition is FALSE because less than 95% of servers (specifically, only 95/100 = 95%) met the requirement, but the requirement is that at least 95% must be met, and the remaining 5% did not meet the deadline. The unknown information does not change this conclusion. There are no explicit exception prerequisites mentioned in the rule text.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 10.2s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the quoted trigger: 95 out of 100 servers (95%) met the 14-day critical-patch deadline. Facts that REFUTE it: 3 servers were patched on day 20, and 2 remain outstanding, meaning they did not meet the 14-day deadline. Given these facts, the condition is FALSE because less than 95% of servers (specifically, only 95/100 = 95%) met the requirement, but the requirement is that at least 95% must be met, and the remaining 5% did not meet the deadline. The unknown information does not change this conclusion. There are no explicit exception prerequisites mentioned in the rule text.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_alarm_equal_reports

**Expected:** Equal-authority incompatible observations of the same state require abstention and both citations.

**Model:** The subject is the monitored fire alarm at Orchard Packaging, and the period in scope is 10:00 on 2025-06-12. The evidence shows conflicting statuses for the fire alarm at Orchard Packaging at 10:00 on 2025-06-12. E1 states that the central monitoring status was OFFLINE, while E2 states it was ONLINE. There is no additional information to resolve this contradiction, so we cannot definitively prove or refute the trigger condition based on the provided evidence alone. Therefore, the condition is unknown. There are no explicit exception prerequisites mentioned in the rule text for C1.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 6; elapsed: 18.9s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if the monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12.", "scope_reason": "scope=alarm:provider_a is in scope because the evidence E1 specifically references this scope and the rule's applicability is not explicitly restricted to other scopes.", "scope": "in_scope", "condition_reason": "condition=TRUE because the evidence E1 directly states that 'Orchard Packaging, account OP-11: central monitoring status was OFFLINE at 10:00 on 2025-06-12.' This confirms the fire alarm was offline at the specified time and location, matching exactly the trigger condition in C1.", "condition": "true", "exception_reason": "exception=does_not_apply because there are no explicit exceptions listed in the rule text that would negate or modify the condition for C1. The rule does not specify any circumstances under which the offline status should be ignored.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict": "unresolved", "findings": [{"subject": "Orchard Packaging", "evidence_ids": ["E1"], "reason": "The fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12, as stated in E1. This directly satisfies the condition of C1 which flags a concern for such an event."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...n for such an event.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence shows conflicting statuses for the fire alarm at Orchard Packaging at 10:00 on 2025-06-12. E1 states that the central monitoring status was OFFLINE, while E2 states it was ONLINE. There is no additional information to resolve this contradiction, so we cannot definitively prove or refute the trigger condition based on the provided evidence alone. Therefore, the condition is unknown. There are no explicit exception prerequisites mentioned in the rule text for C1.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_backup_immutability_conflict

**Expected:** Contradictory same-period attestations cannot be resolved by source votes or department titles.

**Model:** The subject is the production backup vault PV-3, and the period in scope is 2025-08-31. Facts proving the trigger: E1 states that 'the security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31.' This directly supports the condition. Facts refuting the trigger: E2 states that 'the infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31.' This directly contradicts the condition. Given the contradictory attestations, and no further evidence to resolve the contradiction, the truth of the condition remains unknown. The rule does not specify any exceptions that would apply in this case. There are no explicit exception prerequisites mentioned.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 1; model calls: 5; elapsed: 16.7s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts proving the trigger: E1 states that 'the security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31.' This directly supports the condition. Facts refuting the trigger: E2 states that 'the infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31.' This directly contradicts the condition. Given the contradictory attestations, and no further evidence to resolve the contradiction, the truth of the condition remains unknown. The rule does not specify any exceptions that would apply in this case. There are no explicit exception prerequisites mentioned.

### auto_mileage_corrected_denominator

**Expected:** Three per two million equals 1.5 per million, below two; the explicit correction controls the denominator.

**Model:** The subject is Northline's 2025 preventable collision rate, and the period in scope is calendar year 2025. The evidence shows three preventable collisions occurred in 2025 (E1). The final corrected mileage is 2,000,000 miles (E3), which supersedes the original 1,000,000 miles reported (E2). The rate is calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This is less than the threshold of 2 per million miles. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule text for C1.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 15.9s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence shows three preventable collisions occurred in 2025 (E1). The final corrected mileage is 2,000,000 miles (E3), which supersedes the original 1,000,000 miles reported (E2). The rate is calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This is less than the threshold of 2 per million miles. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule text for C1.

### property_later_repair_does_not_rewrite_history

**Expected:** The historical impairment remains a concern; a later repair is a state change, not a correction.

**Model:** No accepted case assessment.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 6; model calls: 8; elapsed: 25.3s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if Cedar Depot's sprinkler system was impaired on the historical assessment date 2025-03-01", "scope_reason": "The subject is Cedar Depot and the period in scope is 2025-03-01, which matches the historical assessment date mentioned in the guideline.", "scope": "in_scope", "condition_reason": "The facts that PROVE this quoted trigger are found in E1, which states 'At Cedar Depot on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired.' This directly establishes that the sprinkler system was impaired on the assessment date. There are no facts that REFUTE this trigger. Given the evidence, it is true that the sprinkler system was impaired on 2025-03-01.", "condition": "true", "exception_reason": "There are no explicit exception prerequisites mentioned in the guideline for C1. Therefore, the exception status is 'does_not_apply'.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict": "unresolved", "findings": [{"subject": "Cedar Depot", "evidence_ids": ["E1"], "reason": "The historical inspection on 2025-03-01 found that the sprinkler control valve was seized closed and the sprinkler system was impaired, which meets the condition for flagging a concern as specified in criterion C1."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...ied in criterion C1.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

### property_electrical_exception

**Expected:** The age trigger applies but the documented complete replacement establishes the explicit exception.

**Model:** The scope is 'whole_case', but the rule's applicability is determined by the evidence sources. The subject of assessment is the building at Willow Print, which is identified in both evidence sources E1 and E2. The payload's scope field is only an evidence-batch identifier, not the rule's applicability. The building is the relevant subject for applying this criterion. The condition requires that a concern be flagged if a building was constructed before 1960 AND there is no documentation of complete replacement of original electrical wiring after 2010 by a licensed contractor. The building at Willow Print was constructed in 1952, which satisfies the first part of the condition (before 1960). However, evidence E2 shows that a licensed contractor documented complete replacement of all original electrical wiring in 2018, which satisfies the exception requirement (replacement after 2010). Therefore, the condition is FALSE because the exception applies. The exception explicitly states that if a licensed contractor documents complete replacement of original electrical wiring after 2010, then the concern should not be flagged. Evidence E2 confirms that such documentation exists (the replacement occurred in 2018). Therefore, the exception applies.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 1; captured call errors: 4; model calls: 7; elapsed: 23.2s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern for a building constructed before 1960 unless a licensed contractor documents complete replacement of its original electrical wiring after 2010.", "scope_reason": "The subject is the building at Willow Print, constructed in 1952. The period in scope is from 2010 onwards, as the rule requires documentation of complete replacement after that date.", "scope": "in_scope", "condition_reason": "Facts that PROVE the quoted trigger: The building was constructed in 1952 (before 1960), and a licensed contractor documented complete replacement of all original electrical wiring in 2018. Facts that REFUTE it: None directly refute the trigger since the building is pre-1960 and the wiring was replaced after 2010. Given unknown information, the trigger could still be true if no other conditions are met. Condition is TRUE because the building was constructed before 1960 and the electrical wiring was completely replaced after 2010 by a licensed contractor.", "condition": "true", "exception_reason": "There are no explicit exception prerequisites mentioned in the rule text that would apply here. The rule does not specify any conditions under which this concern would not be flagged. Exception status is: does_not_apply", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict": "resolved", "findings": []}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...atched', 'findings': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

### cyber_service_account_exception

**Expected:** Both exception requirements are established, so lack of MFA does not trigger the concern for this account.

**Model:** The subject is 'invoice-sync' account, and the period in scope is the current assessment period as specified in the task instructions. Facts that PROVE the quoted trigger: The account 'invoice-sync' lacks MFA (E1). Facts that REFUTE it: The account is a noninteractive service account with interactive login disabled, and has a documented credential rotation interval of 14 days which is less than or equal to 30 days (E2). Given that the account meets the exception criteria (noninteractive, login disabled, rotation interval <= 30 days), it could still be true that the rule's trigger holds, but the exception applies. However, since the exception explicitly allows for this scenario, the condition is FALSE because the exception applies. The account 'invoice-sync' qualifies as a noninteractive service account with interactive login disabled and has a documented credential rotation interval of 14 days (less than or equal to 30 days). The exception prerequisites are met, and the validity dates are not specified as expired. Therefore, the exception applies.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 15.3s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `applies`. Facts that PROVE the quoted trigger: The account 'invoice-sync' lacks MFA (E1). Facts that REFUTE it: The account is a noninteractive service account with interactive login disabled, and has a documented credential rotation interval of 14 days which is less than or equal to 30 days (E2). Given that the account meets the exception criteria (noninteractive, login disabled, rotation interval <= 30 days), it could still be true that the rule's trigger holds, but the exception applies. However, since the exception explicitly allows for this scenario, the condition is FALSE because the exception applies. The account 'invoice-sync' qualifies as a noninteractive service account with interactive login disabled and has a documented credential rotation interval of 14 days (less than or equal to 30 days). The exception prerequisites are met, and the validity dates are not specified as expired. Therefore, the exception applies.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
