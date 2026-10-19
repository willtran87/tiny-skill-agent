# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T00:22:58.819381+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **17/32** (planned: 32).
- Correct case statuses: **25/32**.
- Required gold evidence cited: **35/35**.
- Reference/provenance checks: **145/145**.
- False-positive findings in the 20 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| cyber_remote_access_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_pump_service_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_driver_screening_unknown | insufficient_evidence | no_match | 0 / 0 | 0 / 0 | FAIL |
| gl_subcontract_limit_unknown | insufficient_evidence | no_match | 0 / 0 | 0 / 0 | FAIL |
| auto_incident_rate_calculation | matched | matched | 1 / 1 | 2 / 2 | FAIL |
| property_reserves_exact_threshold | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_roof_exact_boundary | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| cyber_patch_coverage_boundary | matched | no_match | 0 / 1 | 1 / 1 | FAIL |
| property_alarm_equal_reports | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| cyber_backup_immutability_conflict | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| auto_mileage_corrected_denominator | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| property_later_repair_does_not_rewrite_history | matched | matched | 1 / 1 | 1 / 1 | FAIL |
| property_electrical_exception | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| cyber_service_account_exception | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| gl_hot_work_scope_exclusion | not_applicable | no_match | 0 / 0 | 1 / 1 | FAIL |
| auto_passenger_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | FAIL |
| property_multiple_warehouse_concerns | matched | matched | 2 / 2 | 2 / 2 | FAIL |
| auto_multiple_expired_licences | matched | matched | 2 / 2 | 2 / 2 | FAIL |
| cyber_multiple_restore_strengths | matched | matched | 2 / 2 | 2 / 2 | PASS |
| property_corroboration_not_two_events | matched | matched | 1 / 1 | 0 / 0 | PASS |
| gl_sister_company_evidence | insufficient_evidence | no_match | 0 / 0 | 0 / 0 | FAIL |
| cyber_prior_year_does_not_prove_current | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_building_specific_scope | not_applicable | no_match | 0 / 0 | 1 / 1 | FAIL |
| wc_partial_payroll_period | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| gl_document_submission_condition | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| wc_document_absence_is_concern | matched | matched | 1 / 1 | 1 / 1 | PASS |
| wc_activity_explicitly_not_performed | no_match | insufficient_evidence | 0 / 0 | 1 / 1 | FAIL |
| property_inspection_date_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_cross_source_alarm_and_value | matched | matched | 1 / 1 | 2 / 2 | PASS |
| gl_loss_aggregation_without_duplicate | matched | matched | 1 / 1 | 1 / 1 | PASS |
| cyber_restore_duration_cross_midnight | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| property_expired_exception_certificate | matched | matched | 1 / 1 | 2 / 2 | PASS |

## Reasons and diagnostics

### cyber_remote_access_unknown

**Expected:** Administrator MFA does not establish workforce MFA; blank or unavailable records do not prove absence of the control.

**Model:** The rule concerns remote workforce login protection as of 2025-09-01. The evidence spans cover the workforce size and MFA status of administrators, but do not confirm workforce MFA for remote logins. Facts that PROVE the trigger: E1 states MFA is enabled for all four cloud administrators, but does not confirm workforce MFA for remote access. Facts that REFUTE the trigger: E2 indicates no VPN configuration report was available and the broker did not verify remote-login configuration. Given unknown information about workforce remote login MFA status, the condition remains UNKNOWN. The rule does not specify any explicit exceptions. No exception prerequisites or validity dates are mentioned. No actual incompatible observations are present in the evidence. E1 and E2 do not contradict each other regarding workforce MFA status for remote logins.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 10.8s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts that PROVE the trigger: E1 states MFA is enabled for all four cloud administrators, but does not confirm workforce MFA for remote access. Facts that REFUTE the trigger: E2 indicates no VPN configuration report was available and the broker did not verify remote-login configuration. Given unknown information about workforce remote login MFA status, the condition remains UNKNOWN. The rule does not specify any explicit exceptions. No exception prerequisites or validity dates are mentioned.

### property_pump_service_unknown

**Expected:** Unlocated records and a visual inspection cannot establish a missed service visit.

**Model:** Subject is the fire pump at Cedar Components; period in scope is calendar 2025. The quoted trigger requires that the fire pump at Cedar Components was NOT serviced during calendar 2025. Evidence E1 states that the maintenance binder was held off site and unavailable to the surveyor, which does not confirm or refute service activity in 2025. Evidence E2 indicates that the pump contractor's 2025 service invoice cannot be located, and they are still checking the contractor's archive, without asserting that the visit did not occur. These facts do not definitively prove or disprove the servicing occurred in 2025. Therefore, the condition is unknown. The rule does not specify any explicit exceptions that would apply to this situation. There are no actual incompatible observations identified in the evidence. Both E1 and E2 relate to the maintenance status of the fire pump but do not contradict each other directly. The lack of documentation does not inherently conflict with the possibility that service occurred.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 11.0s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The quoted trigger requires that the fire pump at Cedar Components was NOT serviced during calendar 2025. Evidence E1 states that the maintenance binder was held off site and unavailable to the surveyor, which does not confirm or refute service activity in 2025. Evidence E2 indicates that the pump contractor's 2025 service invoice cannot be located, and they are still checking the contractor's archive, without asserting that the visit did not occur. These facts do not definitively prove or disprove the servicing occurred in 2025. Therefore, the condition is unknown. The rule does not specify any explicit exceptions that would apply to this situation.

### auto_driver_screening_unknown

**Expected:** Neither the interview process nor missing files establishes whether all MVR reviews occurred.

**Model:** Subject is employed drivers; period is before hire Facts that PROVE the trigger: None explicitly stated. Facts that REFUTE the trigger: E1 states 'The MVR review field is unanswered' indicating no confirmation of review; E2 states 'The driver files have not been provided' and 'no statement from the applicant confirming or denying pre-hire MVR reviews,' which means lack of evidence for review. Given unknown information: Since there's no explicit confirmation of MVR review for any driver, it cannot be confirmed that reviews occurred for every employed driver before hire. Therefore, condition is FALSE. Rule does not specify any exceptions applicable to this scenario. No actual incompatible observations identified. Both E1 and E2 indicate absence of MVR review confirmation or documentation, but they do not contradict each other directly.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 10.1s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the trigger: None explicitly stated. Facts that REFUTE the trigger: E1 states 'The MVR review field is unanswered' indicating no confirmation of review; E2 states 'The driver files have not been provided' and 'no statement from the applicant confirming or denying pre-hire MVR reviews,' which means lack of evidence for review. Given unknown information: Since there's no explicit confirmation of MVR review for any driver, it cannot be confirmed that reviews occurred for every employed driver before hire. Therefore, condition is FALSE. Rule does not specify any exceptions applicable to this scenario.

### gl_subcontract_limit_unknown

**Expected:** Unspecified insurance limits cannot satisfy or disprove the $2 million requirement.

**Model:** The subject is active roofing subcontractors. The period in scope is the assessment period for the case. Facts that PROVE the quoted trigger: None provided. Facts that REFUTE it: E1 states that both subcontractors (North Roof and Ridge Team) are marked insured in the vendor register, but the register does not record limits or policy numbers; E2 states that certificates for both subcontractors have been requested but not received, and their general liability limits have not been confirmed. Could it still be true given unknown information? Yes, if the limits were confirmed to be at least $2 million, the trigger would hold. However, the lack of confirmation and receipt of certificates means we cannot establish that the limits are met. Condition is: false There are no explicit exception prerequisites mentioned in the rule text for C1. There are no actual incompatible observations identified. E1 and E2 both relate to the same subject (roofting subcontractors) but do not contradict each other directly; rather, they both indicate a lack of confirmed limits.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 11.4s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the quoted trigger: None provided. Facts that REFUTE it: E1 states that both subcontractors (North Roof and Ridge Team) are marked insured in the vendor register, but the register does not record limits or policy numbers; E2 states that certificates for both subcontractors have been requested but not received, and their general liability limits have not been confirmed. Could it still be true given unknown information? Yes, if the limits were confirmed to be at least $2 million, the trigger would hold. However, the lack of confirmation and receipt of certificates means we cannot establish that the limits are met. Condition is: false There are no explicit exception prerequisites mentioned in the rule text for C1.

### auto_incident_rate_calculation

**Expected:** Three divided by 24 times 100 is 12.5, above 10. This is one aggregate finding, not three separate collision findings.

**Model:** The rule applies to the fleet level for the year 2025, with the subject being Summit Couriers' fleet operations during that period. The facts proving this trigger are: (1) Summit Couriers recorded three preventable collisions during 2025 (E1), and (2) Summit operated 24 active vehicles throughout 2025 (E2). The calculation is: (3 collisions / 24 active vehicles) * 100 = 12.5 collisions per 100 active vehicles. This exceeds the threshold of 10 collisions per 100 active vehicles. There are no facts that refute this trigger. Given the known information, the condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule text for C1. There are no actual incompatible observations identified between E1 and E2. Both pieces of evidence support the calculation required by the rule without contradiction.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 6; elapsed: 21.0s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one fleet-level concern if 2025 preventable collision frequency exceeds 10 collisions per 100 active vehicles. Use the stated active fleet count as denominator.", "scope_reason": "scope is in_scope because the evidence relates to the 2025 calendar year and the rule applies to that period. The payload's scope field 'lossrun:2025' identifies the evidence batch but does not exclude the subject from rule applicability.", "scope": "in_scope", "condition_reason": "The calculated collision frequency is 3 collisions per 100 active vehicles (3/24 = 0.125 collisions per vehicle, or 12.5 collisions per 100 vehicles). This exceeds the threshold of 10 collisions per 100 active vehicles specified in the criterion. The calculation uses the stated active fleet count of 24 vehicles from E2 as the denominator.", "condition": "true", "exception_reason": "Exception does_not_apply because there are no explicit prerequisites or validity dates for an exception to the rule's condition, and no exception is stated in the criterion text.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "conflict is unresolved because there are no conflicting evidence items provided in conflict_candidates; only one piece of evidence (E1) exists and it does not contradict the stated condition.", "conflict": "unresolved", "findings": [{"subject": "Summit Couriers", "evidence_ids": ["E1", "E2"], "reason": "The preventable collision frequency for Summit Couriers in 2025 was 12.5 collisions per 100 active vehicles, which exceeds the threshold of 10 collisions per 100 active vehicles specified in criterion C1. This meets the condition for flagging a fleet-level concern."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...fleet-level concern.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The facts proving this trigger are: (1) Summit Couriers recorded three preventable collisions during 2025 (E1), and (2) Summit operated 24 active vehicles throughout 2025 (E2). The calculation is: (3 collisions / 24 active vehicles) * 100 = 12.5 collisions per 100 active vehicles. This exceeds the threshold of 10 collisions per 100 active vehicles. There are no facts that refute this trigger. Given the known information, the condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule text for C1.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_reserves_exact_threshold

**Expected:** 480,000 / 120,000 equals exactly four months; at least includes equality.

**Model:** The rule concerns Bay Storage's financial position as of a specific date, with the evidence span E1 providing data as of 2025-08-31. The subject is Bay Storage, and the period in scope is 2025-08-31. Facts that prove: E1 states that Bay Storage's unrestricted cash is $480,000 and monthly operating expense is $120,000 as of 2025-08-31. Calculation: $480,000 / $120,000 = 4 months. This meets the 'at least four months' requirement. Facts that refute: None provided. Given unknown information: No additional data affects this calculation directly. Condition status: true. The rule does not specify any explicit exceptions or prerequisites for applying this strength. Therefore, no exception applies. There are no conflicting observations in the evidence provided that would contradict the stated facts about Bay Storage's cash reserves and operating expenses.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 11.1s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that prove: E1 states that Bay Storage's unrestricted cash is $480,000 and monthly operating expense is $120,000 as of 2025-08-31. Calculation: $480,000 / $120,000 = 4 months. This meets the 'at least four months' requirement. Facts that refute: None provided. Given unknown information: No additional data affects this calculation directly. Condition status: true. The rule does not specify any explicit exceptions or prerequisites for applying this strength. Therefore, no exception applies.

### property_roof_exact_boundary

**Expected:** Exactly 20 does not exceed a strictly greater-than-20 threshold.

**Model:** The subject is the roof at Unit 7, and the period in scope is the assessment date of 2025-07-01. The evidence states that 'Unit 7's roof was installed on 2005-07-01' and 'the survey dated 2025-07-01 records an age of exactly 20 years.' This proves the roof is exactly 20 years old on the assessment date. Since the rule requires the roof to be 'strictly older than 20 years,' this condition is not met. Therefore, the trigger does not hold true. There are no explicit exception prerequisites mentioned in the guideline for C1. There are no conflicting observations regarding the roof's installation date or age. The evidence is consistent and clearly indicates that the roof was installed on 2005-07-01, making it exactly 20 years old on 2025-07-01.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 8.1s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that 'Unit 7's roof was installed on 2005-07-01' and 'the survey dated 2025-07-01 records an age of exactly 20 years.' This proves the roof is exactly 20 years old on the assessment date. Since the rule requires the roof to be 'strictly older than 20 years,' this condition is not met. Therefore, the trigger does not hold true. There are no explicit exception prerequisites mentioned in the guideline for C1.

### cyber_patch_coverage_boundary

**Expected:** 95/100 equals 95%, meeting an inclusive threshold despite five exceptions.

**Model:** The subject is '100 in-scope servers' and the period in scope is 'within 14 days of release'. The payload scope covers the complete summary of 100 servers as stated in E1. Facts that PROVE: 95 out of 100 servers met the 14-day critical-patch deadline. Facts that REFUTE: 3 servers were patched on day 20, and 2 remain outstanding. Given that 95/100 = 0.95 or 95%, this meets the threshold. However, since 2 servers remain outstanding, they do not meet the requirement of 'all critical patches installed within 14 days'. Therefore, the condition is FALSE because not all servers have met the deadline. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this strength would not apply. No actual incompatible observations exist in the evidence provided. All data points relate to the same subject (100 servers) and time frame (patch deadline). The data shows that while 95 servers met the deadline, 2 did not, which creates a contradiction with the 'all critical patches installed' requirement but does not constitute an unresolved conflict.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 12.0s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE: 95 out of 100 servers met the 14-day critical-patch deadline. Facts that REFUTE: 3 servers were patched on day 20, and 2 remain outstanding. Given that 95/100 = 0.95 or 95%, this meets the threshold. However, since 2 servers remain outstanding, they do not meet the requirement of 'all critical patches installed within 14 days'. Therefore, the condition is FALSE because not all servers have met the deadline. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this strength would not apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_alarm_equal_reports

**Expected:** Equal-authority incompatible observations of the same state require abstention and both citations.

**Model:** The subject is the monitored fire alarm at Orchard Packaging, and the period in scope is 10:00 on 2025-06-12. Facts proving the trigger: E1 states that the central monitoring status was OFFLINE at 10:00 on 2025-06-12 for Orchard Packaging, account OP-11. Facts refuting the trigger: E2 states that the central monitoring status was ONLINE at 10:00 on 2025-06-12 for the same site and account. Given that there is a direct contradiction between the two sources regarding the status of the fire alarm at the exact time in question, and no correction or precedence is documented, the condition remains unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this concern would not apply. There is an actual incompatible observation between E1 and E2. E1 reports the fire alarm as OFFLINE at 10:00 on 2025-06-12, while E2 reports it as ONLINE at the same time and location. These observations are about the same subject (fire alarm at Orchard Packaging) and time (10:00 on 2025-06-12), making the conflict unresolved.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 6; elapsed: 20.7s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if the monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12.", "scope_reason": "scope is in_scope because the evidence E1 directly addresses the monitored fire alarm at Orchard Packaging at the specified time (10:00 on 2025-06-12) and the scope 'alarm:provider_a' is relevant to the evidence source.", "scope": "in_scope", "condition_reason": "condition is TRUE because E1 explicitly states that 'Orchard Packaging, account OP-11: central monitoring status was OFFLINE at 10:00 on 2025-06-12', which directly matches the trigger condition in C1.", "condition": "true", "exception_reason": "exception is does_not_apply because there are no explicit exceptions stated in the criterion C1 that would negate the condition when the fire alarm was offline at the specified time.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "conflict is unresolved because E1 and E2 present contradictory statements about the status of the fire alarm at Orchard Packaging at 10:00 on 2025-06-12, with no resolution or explanation provided.", "conflict": "unresolved", "findings": [{"subject": "Orchard Packaging", "evidence_ids": ["E1"], "reason": "The monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12, as stated in E1, which directly triggers the concern outlined in C1."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...cern outlined in C1.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts proving the trigger: E1 states that the central monitoring status was OFFLINE at 10:00 on 2025-06-12 for Orchard Packaging, account OP-11. Facts refuting the trigger: E2 states that the central monitoring status was ONLINE at 10:00 on 2025-06-12 for the same site and account. Given that there is a direct contradiction between the two sources regarding the status of the fire alarm at the exact time in question, and no correction or precedence is documented, the condition remains unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this concern would not apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_backup_immutability_conflict

**Expected:** Contradictory same-period attestations cannot be resolved by source votes or department titles.

**Model:** The subject is the production backup vault PV-3, and the period in scope is 2025-08-31. Facts proving the trigger: E1 states that 'the security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31.' This directly supports the condition. Facts refuting the trigger: E2 states that 'the infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31.' This contradicts the condition. Given that both attestations are signed on 2025-09-01 and concern the same configuration and period, there is a direct contradiction between them. Since the rule's trigger requires immutable retention to be enabled, and one attestation says it was enabled while another says it was disabled, the condition cannot be definitively determined as true or false without resolving this contradiction. Therefore, condition=unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which the strength would not apply. Hence, exception=does_not_apply. There is an actual incompatible observation between E1 and E2 regarding the status of immutable retention on vault PV-3 for 2025-08-31. E1 claims it was enabled, while E2 claims it was disabled. These contradicting statements concern the same subject (vault PV-3) and time period (2025-08-31). Therefore, conflict=unresolved.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 3; model calls: 6; elapsed: 20.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Record a strength if the production backup vault had immutable retention enabled on 2025-08-31.", "scope_reason": "The rule's applicability includes both security:signed_attestation and infrastructure:signed_attestation as evidence sources for assessing the criterion. The scope is whole_case, which encompasses all relevant evidence for evaluating this criterion.", "scope": "in_scope", "condition_reason": "The condition is TRUE because the security lead's attestation (E1) directly confirms that 'production vault PV-3 had immutable retention enabled throughout 2025-08-31.' This satisfies the requirement of the criterion for a strength.", "condition": "true", "exception_reason": "There are no explicit exceptions stated in the criterion text that would apply to this case. The criterion does not list any conditions under which immutable retention being enabled would not qualify as a strength.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There is a conflict between E1 and E2, where E1 supports the condition being true (immutable retention enabled) and E2 contradicts it (immutable retention disabled). However, the resolution of this conflict requires evaluating which attestation is more authoritative or accurate. Since both attestations are signed on 2025-09-01 and concern the same configuration and period, and there is no indication that one supersedes the other, the conflict remains unresolved.", "conflict": "unresolved", "findings": [{"subject": "production backup vault PV-3", "evidence_ids": ["E1"], "reason": "The security lead's attestation confirms that immutable retention was enabled on 2025-08-31, meeting the criterion's requirement for a strength."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...ment for a strength.")]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts proving the trigger: E1 states that 'the security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31.' This directly supports the condition. Facts refuting the trigger: E2 states that 'the infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31.' This contradicts the condition. Given that both attestations are signed on 2025-09-01 and concern the same configuration and period, there is a direct contradiction between them. Since the rule's trigger requires immutable retention to be enabled, and one attestation says it was enabled while another says it was disabled, the condition cannot be definitively determined as true or false without resolving this contradiction. Therefore, condition=unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which the strength would not apply. Hence, exception=does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_mileage_corrected_denominator

**Expected:** Three per two million equals 1.5 per million, below two; the explicit correction controls the denominator.

**Model:** The subject is Northline and the period in scope is 2025. The facts that prove this trigger are: E1 states there were three preventable collisions in 2025, and E3 provides the corrected mileage of 2,000,000 miles for 2025. The facts that refute it are none. Given the known information, the rate can be calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This is less than the threshold of 2 per million miles. Therefore, condition is false. There are no explicit exception prerequisites mentioned in the rule text. There are no actual incompatible observations. E1 and E3 both refer to the same 2025 period, but E3 corrects the mileage from 1,000,000 miles to 2,000,000 miles, which does not create a contradiction with E1's collision count. The correction supersedes the original statement without altering the number of collisions.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 20.7s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The facts that prove this trigger are: E1 states there were three preventable collisions in 2025, and E3 provides the corrected mileage of 2,000,000 miles for 2025. The facts that refute it are none. Given the known information, the rate can be calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This is less than the threshold of 2 per million miles. Therefore, condition is false. There are no explicit exception prerequisites mentioned in the rule text.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_later_repair_does_not_rewrite_history

**Expected:** The historical impairment remains a concern; a later repair is a state change, not a correction.

**Model:** The subject is Cedar Depot and the period in scope is the historical assessment date 2025-03-01. Facts that PROVE this quoted trigger: E1 states that 'At Cedar Depot on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired.' This directly establishes that the sprinkler system was impaired on the assessment date. Facts that REFUTE it: None provided; the evidence confirms impairment on the date in question. Could it still be true given unknown information? No additional information is needed to confirm the impairment occurred on 2025-03-01 as stated in E1. Therefore, condition=true. The rule does not specify any explicit exception prerequisites or validity dates that would apply here. There are no exceptions mentioned that would prevent the concern from being flagged. Exception=does_not_apply. There are no actual incompatible observations with their IDs. The evidence shows impairment on 2025-03-01 (E1) and repair on 2025-03-05 (E2), but these events occurred at different times and do not contradict each other regarding the historical condition. Conflict=none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 6; elapsed: 20.3s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if Cedar Depot's sprinkler system was impaired on the historical assessment date 2025-03-01.", "scope_reason": "scope is in_scope because the evidence directly addresses the historical assessment date of 2025-03-01 for Cedar Depot and the rule explicitly applies to this date and location.", "scope": "in_scope", "condition_reason": "condition is TRUE because the evidence states that 'At Cedar Depot on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired', which directly confirms that the sprinkler system was impaired on the historical assessment date of 2025-03-01.", "condition": "true", "exception_reason": "exception is does_not_apply because there are no explicit exceptions mentioned in the rule text that would prevent the condition from being met, and no prerequisites for an exception are established in the evidence.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "conflict is unresolved because the evidence does not provide information about the actual condition of the sprinkler system on 2025-03-01, only that it was repaired after that date. The inspection report from E1 directly contradicts the repair report from E2 regarding the system's state at the assessment date.", "conflict": "unresolved", "findings": [{"subject": "Cedar Depot", "evidence_ids": ["E1"], "reason": "The inspection report from 2025-03-01 explicitly states that the sprinkler system was impaired, meeting the condition for flagging a concern."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r... flagging a concern.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE this quoted trigger: E1 states that 'At Cedar Depot on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired.' This directly establishes that the sprinkler system was impaired on the assessment date. Facts that REFUTE it: None provided; the evidence confirms impairment on the date in question. Could it still be true given unknown information? No additional information is needed to confirm the impairment occurred on 2025-03-01 as stated in E1. Therefore, condition=true. The rule does not specify any explicit exception prerequisites or validity dates that would apply here. There are no exceptions mentioned that would prevent the concern from being flagged. Exception=does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_electrical_exception

**Expected:** The age trigger applies but the documented complete replacement establishes the explicit exception.

**Model:** The payload's scope field identifies the evidence batch as 'schedule:building', which matches the criterion's applicability to building-level assessments. The rule applies to building-level assessments, and the evidence batch 'schedule:building' is relevant to this assessment. The building was constructed in 1952, which is before 1960, triggering the concern condition. However, there is no documentation from a licensed contractor that complete replacement of the original electrical wiring occurred after 2010. The evidence E1 states that the building was constructed in 1952 and remains in active use, with routine cosmetic renovation listed in 2022, but this does not establish wiring replacement. Evidence E2 shows a licensed contractor documented complete replacement of original electrical wiring in 2018, which satisfies the requirement for replacement after 2010. However, the initial assessment based on E1 alone would flag the concern because it lacks documentation of replacement after 2010. There are no explicit exceptions provided in the criterion text that would apply to this situation. The rule requires documentation of complete replacement by a licensed contractor after 2010, which is not present in the initial evidence E1. There are no conflicting pieces of evidence that would prevent the determination of the condition. The evidence E1 clearly states the construction year and renovation details, but does not provide documentation of wiring replacement. Evidence E2 provides documentation of complete replacement by a licensed contractor in 2018, which satisfies the requirement.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 6; elapsed: 19.7s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern for a building constructed before 1960 unless a licensed contractor documents complete replacement of its original electrical wiring after 2010.", "scope_reason": "The building was constructed in 1952, which is before 1960. The period in scope is the time frame from 2010 onwards for electrical wiring replacement verification.", "scope": "in_scope", "condition_reason": "The building at Willow Print was constructed in 1952, which satisfies the 'before 1960' condition. The evidence shows that a licensed electrical contractor certified complete replacement of all original electrical wiring in 2018, which is after 2010. Therefore, the condition is true because the building meets the construction date requirement and the required documentation of complete replacement after 2010 exists.", "condition": "true", "exception_reason": "There are no explicit exception prerequisites mentioned in the rule that would apply to this situation. The rule does not specify any conditions under which the concern would not be flagged, such as specific types of renovations or alternative documentation methods.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "There are no conflicting observations. E1 states the building was constructed in 1952 and had routine cosmetic renovation in 2022, while E2 confirms complete replacement of electrical wiring by a licensed contractor in 2018. These do not contradict each other as the renovation and wiring replacement occurred at different times and address different aspects of the building.", "conflict": "none", "findings": []}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...atched', 'findings': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

### cyber_service_account_exception

**Expected:** Both exception requirements are established, so lack of MFA does not trigger the concern for this account.

**Model:** The subject is 'invoice-sync' account, and the period in scope is the current assessment period as specified in the context. Facts that PROVE the quoted trigger: The account 'invoice-sync' lacks MFA. Facts that REFUTE it: The account is a noninteractive service account with interactive login disabled, and has a documented credential rotation interval of 14 days (which is less than or equal to 30 days). Given that the account meets the exception criteria (noninteractive, login disabled, and rotation interval <= 30 days), the trigger is REFUTED by these facts. Therefore, condition=true. The rule includes an exception for 'a noninteractive service account with interactive login disabled and a documented credential rotation interval no longer than 30 days.' The evidence shows that 'invoice-sync' is a noninteractive integration account with interactive login disabled, and the credential rotation interval is 14 days (which satisfies the <= 30 days requirement). Therefore, the exception applies. There are no actual incompatible observations. The evidence supports that the account is noninteractive, login is disabled, and rotation interval is within the allowed limit of 30 days. All conditions align with the exception criteria.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 14.3s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `applies`. Facts that PROVE the quoted trigger: The account 'invoice-sync' lacks MFA. Facts that REFUTE it: The account is a noninteractive service account with interactive login disabled, and has a documented credential rotation interval of 14 days (which is less than or equal to 30 days). Given that the account meets the exception criteria (noninteractive, login disabled, and rotation interval <= 30 days), the trigger is REFUTED by these facts. Therefore, condition=true. The rule includes an exception for 'a noninteractive service account with interactive login disabled and a documented credential rotation interval no longer than 30 days.' The evidence shows that 'invoice-sync' is a noninteractive integration account with interactive login disabled, and the credential rotation interval is 14 days (which satisfies the <= 30 days requirement). Therefore, the exception applies.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_hot_work_scope_exclusion

**Expected:** The explicit operational scope excludes this applicant; a missing permit manual is irrelevant.

**Model:** The subject is a contractor performing on-site welding or flame cutting at customers' premises. The period in scope is the policy period. Facts that PROVE this quoted trigger: Pine Design does not perform fabrication, installation, welding, flame cutting, or physical work at customer sites. This directly contradicts the requirement for on-site welding or flame cutting. Facts that REFUTE it: The evidence explicitly states that Pine Design provides remote CAD drafting only and does not perform any physical work at customer sites. Could it still be true given unknown information? No, because the evidence clearly excludes any on-site work involving welding or flame cutting. Condition is FALSE. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this criterion would not apply. Exception status is does_not_apply. There are no actual incompatible observations. The evidence clearly states that Pine Design does not perform on-site welding or flame cutting, which directly contradicts the trigger condition. However, since the trigger is false (no on-site work), there's no conflict to resolve.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 8.2s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE this quoted trigger: Pine Design does not perform fabrication, installation, welding, flame cutting, or physical work at customer sites. This directly contradicts the requirement for on-site welding or flame cutting. Facts that REFUTE it: The evidence explicitly states that Pine Design provides remote CAD drafting only and does not perform any physical work at customer sites. Could it still be true given unknown information? No, because the evidence clearly excludes any on-site work involving welding or flame cutting. Condition is FALSE. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this criterion would not apply. Exception status is does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_passenger_scope_exclusion

**Expected:** Freight-only operations are outside the explicit passengers-for-hire scope.

**Model:** The subject is vehicles operating in a commercial fleet context. The period in scope is the current operational status as described in the evidence. The quoted trigger requires vehicles carrying passengers for hire. Evidence E1 states that Granite Freight operates box trucks carrying packaged commercial goods and does not transport passengers for hire. Drivers and incidental employee helpers are the only occupants, indicating no passenger transport. Therefore, the condition is refuted by the evidence. There are no explicit exception prerequisites mentioned in the rule text that would apply to this situation. No actual incompatible observations exist. The evidence clearly indicates that the fleet does not carry passengers for hire, which directly contradicts the trigger condition of the rule.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 6.4s.

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The quoted trigger requires vehicles carrying passengers for hire. Evidence E1 states that Granite Freight operates box trucks carrying packaged commercial goods and does not transport passengers for hire. Drivers and incidental employee helpers are the only occupants, indicating no passenger transport. Therefore, the condition is refuted by the evidence. There are no explicit exception prerequisites mentioned in the rule text that would apply to this situation.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_multiple_warehouse_concerns

**Expected:** East and West qualify independently; extinguishers and future plans do not satisfy the condition, and the office is excluded.

**Model:** The subject is 'occupied storage warehouse' and the period is 'current'. The scope is in_scope because the evidence covers current conditions of warehouses. Facts that PROVE the quoted trigger: E1 shows East Warehouse is occupied daily and has no automatic sprinklers; E2 shows West Warehouse is occupied on both shifts and has no automatic sprinklers. Facts that REFUTE it: None directly refute the trigger as both warehouses are occupied and lack sprinklers. Given unknown information, it could still be true that these are occupied storage warehouses lacking automatic sprinklers. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this concern would not apply. Therefore, exception=does_not_apply. There are no actual incompatible observations between the evidence items. E1 and E2 both describe occupied warehouses lacking automatic sprinklers, which aligns with the rule's trigger. The context of E3 (office-only building) is different from the storage warehouses described in E1 and E2, so it does not create a conflict. Conflict=none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 24.8s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE the quoted trigger: E1 shows East Warehouse is occupied daily and has no automatic sprinklers; E2 shows West Warehouse is occupied on both shifts and has no automatic sprinklers. Facts that REFUTE it: None directly refute the trigger as both warehouses are occupied and lack sprinklers. Given unknown information, it could still be true that these are occupied storage warehouses lacking automatic sprinklers. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this concern would not apply. Therefore, exception=does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_multiple_expired_licences

**Expected:** Two independently identified employees meet the concern; Driver C does not.

**Model:** The criterion applies to currently employed drivers with licences expired before 2025-09-01 and unrenewed by that date. The evidence batch includes three drivers: Driver A, Driver B, and Driver C. All are currently employed, but only Drivers A and B meet the licence expiry and renewal criteria. Facts proving the trigger: Driver A's licence expired on 2025-07-31 (before 2025-09-01) and was unrenewed by 2025-09-01. Driver B's licence expired on 2025-08-15 (before 2025-09-01) and was unrenewed by 2025-09-01. Facts refuting the trigger: Driver C's licence is valid through 2027-02-01, so it does not meet the expired condition. Given unknown information, the trigger could still be true for Drivers A and B if no further evidence emerges about their renewal status after 2025-09-01. Condition: true. No explicit exceptions are mentioned in the rule text. The criterion does not list any conditions under which this concern would not apply. Exception: does_not_apply. There are no actual incompatible observations between the drivers' records. All three drivers are currently employed, and their licence statuses are clearly defined without contradiction. Conflict: none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 33.9s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts proving the trigger: Driver A's licence expired on 2025-07-31 (before 2025-09-01) and was unrenewed by 2025-09-01. Driver B's licence expired on 2025-08-15 (before 2025-09-01) and was unrenewed by 2025-09-01. Facts refuting the trigger: Driver C's licence is valid through 2027-02-01, so it does not meet the expired condition. Given unknown information, the trigger could still be true for Drivers A and B if no further evidence emerges about their renewal status after 2025-09-01. Condition: true. No explicit exceptions are mentioned in the rule text. The criterion does not list any conditions under which this concern would not apply. Exception: does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_multiple_restore_strengths

**Expected:** Each application independently meets both timing conditions and warrants its own strength.

**Model:** The rule applies to business-critical applications. Evidence E1 concerns the billing application, and E2 concerns the inventory application. Both are designated business-critical. The assessment date is 2025-09-01. For billing (E1): The restore test completed on 2025-08-10, which is within the last 90 days from 2025-09-01 (83 days). The recovery time was 3 hours, which is less than or equal to 4 hours. These facts prove the trigger for billing. For inventory (E2): The restore test completed on 2025-07-20, which is within the last 90 days from 2025-09-01 (45 days). The recovery time was exactly 4 hours, which is less than or equal to 4 hours. These facts prove the trigger for inventory. No facts refute either case. Given no unknown information that would change these conclusions, the condition is true. The rule does not specify any exceptions. Therefore, exception=does_not_apply. There are no conflicting observations between E1 and E2 as they refer to different applications (billing vs inventory). Both meet the criteria independently. Conflict=none.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 16.7s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. For billing (E1): The restore test completed on 2025-08-10, which is within the last 90 days from 2025-09-01 (83 days). The recovery time was 3 hours, which is less than or equal to 4 hours. These facts prove the trigger for billing. For inventory (E2): The restore test completed on 2025-07-20, which is within the last 90 days from 2025-09-01 (45 days). The recovery time was exactly 4 hours, which is less than or equal to 4 hours. These facts prove the trigger for inventory. No facts refute either case. Given no unknown information that would change these conclusions, the condition is true. The rule does not specify any exceptions. Therefore, exception=does_not_apply.

### property_corroboration_not_two_events

**Expected:** One generator/test warrants one finding; either source independently supports it and both may be cited together.

**Model:** The rule applies to standby generators tested under full building load during August 2025. The subject is generator G-1 at Birch Cold Storage, and the period in scope is August 2025. Facts that PROVE: E1 states that Generator G-1 successfully supplied full building load during its completed test on 2025-08-12. E2 corroborates this by confirming the site engineer independently verified the same test (T-118) occurred on 2025-08-12. Facts that REFUTE: None explicitly refute the successful full-load test during August 2025. Given unknown information, it is possible the test was not conducted under full building load or outside August 2025, but no such evidence exists. Condition is TRUE because both E1 and E2 confirm a single test of generator G-1 under full building load occurred in August 2025. The rule does not specify any exceptions that would prevent recording the strength. No exception prerequisites are mentioned, so the finding applies without exception. There are no actual incompatible observations between E1 and E2. Both documents refer to the same test (T-118) of generator G-1 on 2025-08-12, confirming the same event. Conflict is NONE.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 15.1s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE: E1 states that Generator G-1 successfully supplied full building load during its completed test on 2025-08-12. E2 corroborates this by confirming the site engineer independently verified the same test (T-118) occurred on 2025-08-12. Facts that REFUTE: None explicitly refute the successful full-load test during August 2025. Given unknown information, it is possible the test was not conducted under full building load or outside August 2025, but no such evidence exists. Condition is TRUE because both E1 and E2 confirm a single test of generator G-1 under full building load occurred in August 2025. The rule does not specify any exceptions that would prevent recording the strength. No exception prerequisites are mentioned, so the finding applies without exception.

### gl_sister_company_evidence

**Expected:** A sister company's recall is not evidence of the applicant's recall history; absence of applicant records is not proof of no recall.

**Model:** The rule concerns Aspen Foods LLC specifically, and the evidence indicates that the recall event occurred with Aspen Beverage LLC in May 2025. The companies are separate entities. Facts proving: The evidence shows that Aspen Beverage LLC recalled a beverage product in May 2025 (E2). Facts refuting: The recall summary explicitly states there is no recall history for Aspen Foods LLC (E2), and the applicant's own recall response remains unanswered (E2). Given unknown information, it cannot be confirmed whether Aspen Foods LLC had a recall during 2025. Condition status: false. The trigger does not apply to Aspen Foods LLC because the recall was for Aspen Beverage LLC. There are no explicit exception prerequisites mentioned in the rule text. The rule does not provide any exceptions that would apply to this situation. Exception status: does_not_apply. There is no actual incompatible observation between the two pieces of evidence. E1 identifies Aspen Foods LLC as the applicant and notes that Aspen Beverage LLC is a separate company, while E2 states that the recall was for Aspen Beverage LLC. These facts do not contradict each other but rather clarify that the recall event pertains to a different entity.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 12.7s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts proving: The evidence shows that Aspen Beverage LLC recalled a beverage product in May 2025 (E2). Facts refuting: The recall summary explicitly states there is no recall history for Aspen Foods LLC (E2), and the applicant's own recall response remains unanswered (E2). Given unknown information, it cannot be confirmed whether Aspen Foods LLC had a recall during 2025. Condition status: false. The trigger does not apply to Aspen Foods LLC because the recall was for Aspen Beverage LLC. There are no explicit exception prerequisites mentioned in the rule text. The rule does not provide any exceptions that would apply to this situation. Exception status: does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_prior_year_does_not_prove_current

**Expected:** A previous-year control assessment and unknown post-migration controls cannot establish the current-year requirement.

**Model:** The rule requires testing of offline backups during calendar 2025. The subject is business-critical systems. The period in scope is calendar 2025. Facts that PROVE the quoted trigger: E1 states that 'The 2024 audit confirmed tested offline backups for all business-critical systems in calendar 2024.' However, this does not confirm testing occurred during 2025. Facts that REFUTE it: E2 states that 'The 2025 backup test records and offline-storage configuration have not yet been supplied, and current effectiveness is unverified.' This indicates no confirmation of testing in 2025. Given unknown information: Since there are no records confirming backup testing in 2025, the condition cannot be confirmed as true or false. The rule's trigger holds if all business-critical systems had tested offline backups during calendar 2025, but evidence is missing for that period. Therefore, condition=unknown. The rule does not specify any explicit exceptions. No exception prerequisites or validity dates are mentioned in the guideline text. There is no actual incompatible observation between E1 and E2. E1 covers 2024, while E2 addresses 2025. They refer to different time periods and subjects (2024 audit vs. 2025 storage migration). No conflict exists.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 12.8s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts that PROVE the quoted trigger: E1 states that 'The 2024 audit confirmed tested offline backups for all business-critical systems in calendar 2024.' However, this does not confirm testing occurred during 2025. Facts that REFUTE it: E2 states that 'The 2025 backup test records and offline-storage configuration have not yet been supplied, and current effectiveness is unverified.' This indicates no confirmation of testing in 2025. Given unknown information: Since there are no records confirming backup testing in 2025, the condition cannot be confirmed as true or false. The rule's trigger holds if all business-critical systems had tested offline backups during calendar 2025, but evidence is missing for that period. Therefore, condition=unknown. The rule does not specify any explicit exceptions. No exception prerequisites or validity dates are mentioned in the guideline text.

### property_building_specific_scope

**Expected:** Building A fails the wood-frame applicability condition; Building B cannot make an A-specific rule applicable.

**Model:** The subject is Building A and the period is current as of the survey date. The evidence batch covers the relevant time period for Building A's structural characteristics. Facts that PROVE the trigger: E1 states 'Building A has a steel structural frame and concrete external walls' and 'The engineer confirms there is no combustible wood structural frame in Building A.' This directly contradicts the condition that Building A must have a combustible wood structural frame. Facts that REFUTE the trigger: The evidence clearly shows Building A has a steel structural frame, not combustible wood. Given this information, the trigger cannot be true. Condition = false The rule does not contain any explicit exception prerequisites or validity dates that would apply to Building A's situation. There are no actual incompatible observations with the same subject and time period. The evidence clearly establishes that Building A has a steel structural frame, which contradicts the requirement for combustible wood. There is no unresolved contradiction.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 6; elapsed: 15.9s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the trigger: E1 states 'Building A has a steel structural frame and concrete external walls' and 'The engineer confirms there is no combustible wood structural frame in Building A.' This directly contradicts the condition that Building A must have a combustible wood structural frame. Facts that REFUTE the trigger: The evidence clearly shows Building A has a steel structural frame, not combustible wood. Given this information, the trigger cannot be true. Condition = false The rule does not contain any explicit exception prerequisites or validity dates that would apply to Building A's situation.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### wc_partial_payroll_period

**Expected:** A 20% quarter does not establish the full-year rate when the remaining nine months are unknown.

**Model:** The rule applies to the full 2025 calendar year. The subject is the insured's total overtime hours versus total hours worked in 2025. Facts that PROVE the quoted trigger: E1 shows 2,000 overtime hours and 10,000 total hours for Q1 2025. This gives an overtime rate of 20% (2,000/10,000). Facts that REFUTE it: E2 states that April-December 2025 hours have not been supplied, and the applicant did not provide an annual total or confirm that Q1 rates continued. Given unknown information (missing Q2-Q4 data), the overtime percentage could still be below 15% if the remaining quarters had significantly fewer overtime hours than Q1. However, with only Q1 data available, we cannot definitively determine whether the condition is met for the full year. Therefore, condition=true is not established due to insufficient evidence. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this concern would not apply. No actual incompatible observations are present. E1 and E2 do not contradict each other; rather, they provide complementary information about the data availability for different parts of the year.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 1; model calls: 5; elapsed: 15.8s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts that PROVE the quoted trigger: E1 shows 2,000 overtime hours and 10,000 total hours for Q1 2025. This gives an overtime rate of 20% (2,000/10,000). Facts that REFUTE it: E2 states that April-December 2025 hours have not been supplied, and the applicant did not provide an annual total or confirm that Q1 rates continued. Given unknown information (missing Q2-Q4 data), the overtime percentage could still be below 15% if the remaining quarters had significantly fewer overtime hours than Q1. However, with only Q1 data available, we cannot definitively determine whether the condition is met for the full year. Therefore, condition=true is not established due to insufficient evidence. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this concern would not apply.

### gl_document_submission_condition

**Expected:** Confirmed nonsubmission disproves a submission-specific strength without assuming no agreements exist.

**Model:** The subject is the submission and its attachments. The period in scope is the time of this submission. Facts that PROVE this quoted trigger: The evidence E1 states 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly contradicts the condition that agreements were supplied. Facts that REFUTE it: The statement in E1 explicitly indicates the absence of signed agreements for the subcontractors. Could it still be true given unknown information? No, because the evidence clearly states what was submitted, and there is no indication of any signed agreements being provided. Therefore, condition = false. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply. Exception = does_not_apply. There are no actual incompatible observations in the evidence provided. The statement in E1 is clear and unambiguous about what was submitted, and there are no conflicting facts presented. Conflict = none.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 7.4s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE this quoted trigger: The evidence E1 states 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly contradicts the condition that agreements were supplied. Facts that REFUTE it: The statement in E1 explicitly indicates the absence of signed agreements for the subcontractors. Could it still be true given unknown information? No, because the evidence clearly states what was submitted, and there is no indication of any signed agreements being provided. Therefore, condition = false. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply. Exception = does_not_apply.

### wc_document_absence_is_concern

**Expected:** This criterion explicitly targets a missing submission document, so its confirmed absence supports a concern.

**Model:** The subject is Delta Fabrication, and the period in scope is the complete final submission as referenced in the evidence. The evidence states: 'The intake reviewer checked the complete final submission for Delta Fabrication. It includes payroll, a loss run, and an equipment list, but the required current written lockout procedure was not supplied.' This directly proves that the required document was not provided in the submission. There are no facts refuting this claim. Given this information, the condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule text for C1. There are no conflicting observations in the evidence that would create an unresolved contradiction regarding the presence or absence of the required document.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 8.4s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The evidence states: 'The intake reviewer checked the complete final submission for Delta Fabrication. It includes payroll, a loss run, and an equipment list, but the required current written lockout procedure was not supplied.' This directly proves that the required document was not provided in the submission. There are no facts refuting this claim. Given this information, the condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule text for C1.

### wc_activity_explicitly_not_performed

**Expected:** The explicit delayed induction disproves the all-employees pre-operation requirement despite later completion.

**Model:** The rule concerns newly hired production employees and their machine-safety induction timing relative to first operating production equipment in 2025. The evidence E1 describes two newly hired production employees who first operated production equipment on 2025-05-02 without receiving machine-safety induction, with induction completed on 2025-05-08. Facts that PROVE the quoted trigger: None directly prove the trigger because the employees did not receive induction before operating equipment. Facts that REFUTE it: E1 explicitly states that two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction, and induction was completed on 2025-05-08. This shows that at least one employee did not receive induction before operating equipment, which contradicts the requirement of 'every newly hired production employee received machine-safety induction before first operating production equipment'. Given this explicit contradiction, the trigger is false regardless of unknown information. The rule does not specify any exceptions for this criterion. There are no exception prerequisites or validity dates mentioned that would apply here. There is an actual incompatible observation: E1 states that two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction, which directly contradicts the requirement in the rule that 'every newly hired production employee received machine-safety induction before first operating production equipment'. This is a clear conflict between the evidence and the rule's trigger condition.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 9.7s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the quoted trigger: None directly prove the trigger because the employees did not receive induction before operating equipment. Facts that REFUTE it: E1 explicitly states that two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction, and induction was completed on 2025-05-08. This shows that at least one employee did not receive induction before operating equipment, which contradicts the requirement of 'every newly hired production employee received machine-safety induction before first operating production equipment'. Given this explicit contradiction, the trigger is false regardless of unknown information. The rule does not specify any exceptions for this criterion. There are no exception prerequisites or validity dates mentioned that would apply here.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_inspection_date_unknown

**Expected:** Without the last-completed date, the twelve-month condition is unknown.

**Model:** The subject is the last completed electrical thermographic inspection at Fern Mill. The period in scope is up to 2025-09-01. The quoted trigger requires determining whether the last completed electrical thermographic inspection at Fern Mill occurred more than 12 months before 2025-09-01. Evidence E1 states that 'Fern Mill cannot locate the date of its last completed electrical thermographic inspection' and that 'some contractor records were lost during a server migration.' This directly proves that the date is unknown, which refutes the ability to confirm whether the inspection was more than 12 months prior to 2025-09-01. Evidence E2 indicates that the August site survey did not include thermographic testing or verify any earlier test dates, so it does not provide information about the last completed inspection date. Given the missing records and lack of verification in the evidence, the condition cannot be confirmed as true or false, but remains unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no actual incompatible observations identified. E1 and E2 both relate to the lack of information regarding the date of the last inspection, but they do not contradict each other.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 14.2s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The quoted trigger requires determining whether the last completed electrical thermographic inspection at Fern Mill occurred more than 12 months before 2025-09-01. Evidence E1 states that 'Fern Mill cannot locate the date of its last completed electrical thermographic inspection' and that 'some contractor records were lost during a server migration.' This directly proves that the date is unknown, which refutes the ability to confirm whether the inspection was more than 12 months prior to 2025-09-01. Evidence E2 indicates that the August site survey did not include thermographic testing or verify any earlier test dates, so it does not provide information about the last completed inspection date. Given the missing records and lack of verification in the evidence, the condition cannot be confirmed as true or false, but remains unknown. There are no explicit exception prerequisites mentioned in the rule text for C1.

### property_cross_source_alarm_and_value

**Expected:** The value and whole-stock alarm condition require combining both sources into one strength.

**Model:** The subject is Haven Parts' insured stock. The period in scope is as of 2025-09-01, based on the declaration and certificate evidence dates. Facts that PROVE the trigger: E1 states that the total insured stock is $425,000 as of 2025-09-01; E2 certifies that the entire interior of Haven Parts' sole warehouse is covered by an intruder alarm with continuous remote monitoring as of 2025-09-01. Facts that REFUTE the trigger: None. Given unknown information, the trigger could still be true. Condition status: true. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this strength would not apply. Exception status: does_not_apply. There are no actual incompatible observations between E1 and E2. Both pieces of evidence support the conditions required by the rule for the same subject (Haven Parts) and time period (as of 2025-09-01). Conflict status: none.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 13.9s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE the trigger: E1 states that the total insured stock is $425,000 as of 2025-09-01; E2 certifies that the entire interior of Haven Parts' sole warehouse is covered by an intruder alarm with continuous remote monitoring as of 2025-09-01. Facts that REFUTE the trigger: None. Given unknown information, the trigger could still be true. Condition status: true. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this strength would not apply. Exception status: does_not_apply.

### gl_loss_aggregation_without_duplicate

**Expected:** Distinct claims sum to $325,000, above $300,000. Do not add the repeated GL-101 again or create a finding per claim.

**Model:** The subject is 2025 general liability claims; the period in scope is 2025. Facts proving: E1 states that claim GL-101 has a paid amount of $150,000 and claim GL-102 has a paid amount of $175,000. These are separate claims incurred during 2025. Facts refuting: E2 identifies GL-101 as a duplicate reference, not an additional claim. However, the rule requires using the latest stated paid amount per claim ID, and E1's quote gives the final amounts for each claim. Calculation: Total paid = $150,000 (GL-101) + $175,000 (GL-102) = $325,000. Comparison: $325,000 > $300,000. Therefore, the trigger condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule text for C1. No actual incompatible observations exist. E2 identifies a duplicate reference but does not contradict the paid amounts stated in E1. The rule's requirement is to count each claim ID once using its latest paid amount, which is satisfied by E1.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 2; model calls: 6; elapsed: 23.9s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts proving: E1 states that claim GL-101 has a paid amount of $150,000 and claim GL-102 has a paid amount of $175,000. These are separate claims incurred during 2025. Facts refuting: E2 identifies GL-101 as a duplicate reference, not an additional claim. However, the rule requires using the latest stated paid amount per claim ID, and E1's quote gives the final amounts for each claim. Calculation: Total paid = $150,000 (GL-101) + $175,000 (GL-102) = $325,000. Comparison: $325,000 > $300,000. Therefore, the trigger condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule text for C1.

### cyber_restore_duration_cross_midnight

**Expected:** Elapsed time is 25.5 hours, exceeding the 24-hour maximum despite a successful eventual restore.

**Model:** The subject is the full restore of the payroll application, and the period in scope is from 2025-08-01 08:00 UTC to 2025-08-02 09:30 UTC. The start timestamp is 2025-08-01 08:00 UTC (E1) and the completion timestamp is 2025-08-02 09:30 UTC (E2). The elapsed time is calculated as follows:

From 2025-08-01 08:00 UTC to 2025-08-02 08:00 UTC = 24 hours
From 2025-08-02 08:00 UTC to 2025-08-02 09:30 UTC = 1 hour 30 minutes
Total elapsed time = 25 hours 30 minutes.

Since the elapsed time (25 hours 30 minutes) exceeds the maximum allowed duration of 24 hours, this condition is false. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this situation. There are no conflicting observations regarding the start or completion timestamps of the payroll application restore.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 11.6s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The start timestamp is 2025-08-01 08:00 UTC (E1) and the completion timestamp is 2025-08-02 09:30 UTC (E2). The elapsed time is calculated as follows:

From 2025-08-01 08:00 UTC to 2025-08-02 08:00 UTC = 24 hours
From 2025-08-02 08:00 UTC to 2025-08-02 09:30 UTC = 1 hour 30 minutes
Total elapsed time = 25 hours 30 minutes.

Since the elapsed time (25 hours 30 minutes) exceeds the maximum allowed duration of 24 hours, this condition is false. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this situation.

### property_expired_exception_certificate

**Expected:** The height trigger is met and the explicit approval exception is unavailable on the assessment date.

**Model:** The subject is combustible stock stacking at Linden Distribution. The period in scope is 2025-09-01, which matches the survey date. The facts that prove this trigger are: E1 states that combustible packaged stock was stacked to 5.2 metres at Linden Distribution on 2025-09-01. This exceeds the 4-metre threshold. The facts that refute it are: E2 shows that the engineer's high-stack approval for the same storage area expired on 2025-06-30 and no renewal or extension was issued before 2025-09-01. Therefore, the approval is not valid on 2025-09-01. Given that the stack height exceeds 4 metres and the approval is expired, the trigger condition is true. The exception requires an engineer's specific high-stack approval to remain valid on 2025-09-01. E2 confirms that the approval expired on 2025-06-30 and no renewal or extension was issued before 2025-09-01. Therefore, the exception does not apply. There are no actual incompatible observations. E1 documents the stack height exceeding 4 metres, and E2 documents that the approval expired before the survey date. These facts do not contradict each other; they simply establish that the stack height exceeds the limit and that there is no valid approval.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 16.7s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The facts that prove this trigger are: E1 states that combustible packaged stock was stacked to 5.2 metres at Linden Distribution on 2025-09-01. This exceeds the 4-metre threshold. The facts that refute it are: E2 shows that the engineer's high-stack approval for the same storage area expired on 2025-06-30 and no renewal or extension was issued before 2025-09-01. Therefore, the approval is not valid on 2025-09-01. Given that the stack height exceeds 4 metres and the approval is expired, the trigger condition is true. The exception requires an engineer's specific high-stack approval to remain valid on 2025-09-01. E2 confirms that the approval expired on 2025-06-30 and no renewal or extension was issued before 2025-09-01. Therefore, the exception does not apply.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
