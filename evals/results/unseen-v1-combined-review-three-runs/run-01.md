# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T00:34:58.311470+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **19/32** (planned: 32).
- Correct case statuses: **28/32**.
- Required gold evidence cited: **35/35**.
- Reference/provenance checks: **150/150**.
- False-positive findings in the 20 nonmatched gold cases: **1**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| cyber_remote_access_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_pump_service_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_driver_screening_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| gl_subcontract_limit_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_incident_rate_calculation | matched | matched | 1 / 1 | 2 / 2 | FAIL |
| property_reserves_exact_threshold | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_roof_exact_boundary | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| cyber_patch_coverage_boundary | matched | no_match | 0 / 1 | 1 / 1 | FAIL |
| property_alarm_equal_reports | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| cyber_backup_immutability_conflict | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| auto_mileage_corrected_denominator | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| property_later_repair_does_not_rewrite_history | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_electrical_exception | no_match | matched | 1 / 0 | 2 / 2 | FAIL |
| cyber_service_account_exception | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| gl_hot_work_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
| auto_passenger_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | FAIL |
| property_multiple_warehouse_concerns | matched | matched | 2 / 2 | 2 / 2 | FAIL |
| auto_multiple_expired_licences | matched | matched | 2 / 2 | 2 / 2 | FAIL |
| cyber_multiple_restore_strengths | matched | matched | 2 / 2 | 2 / 2 | PASS |
| property_corroboration_not_two_events | matched | matched | 1 / 1 | 0 / 0 | PASS |
| gl_sister_company_evidence | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| cyber_prior_year_does_not_prove_current | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_building_specific_scope | not_applicable | no_match | 0 / 0 | 1 / 1 | FAIL |
| wc_partial_payroll_period | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| gl_document_submission_condition | no_match | no_match | 0 / 0 | 1 / 1 | FAIL |
| wc_document_absence_is_concern | matched | matched | 1 / 1 | 1 / 1 | PASS |
| wc_activity_explicitly_not_performed | no_match | insufficient_evidence | 0 / 0 | 1 / 1 | FAIL |
| property_inspection_date_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_cross_source_alarm_and_value | matched | matched | 1 / 1 | 2 / 2 | FAIL |
| gl_loss_aggregation_without_duplicate | matched | matched | 1 / 1 | 1 / 1 | FAIL |
| cyber_restore_duration_cross_midnight | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| property_expired_exception_certificate | matched | matched | 1 / 1 | 2 / 2 | PASS |

## Reasons and diagnostics

### cyber_remote_access_unknown

**Expected:** Administrator MFA does not establish workforce MFA; blank or unavailable records do not prove absence of the control.

**Model:** The subject is remote workforce login to Harbor Analytics. The period in scope is as of 2025-09-01. Facts that PROVE this quoted trigger: E1 states that MFA is enabled for all four cloud administrators, but does not confirm MFA for the entire remote workforce. E2 indicates that a VPN configuration report was requested but not available, and no attestation of workforce MFA was supplied. Facts that REFUTE it: There is no evidence confirming that MFA protects ALL remote workforce logins; the questionnaire does not address ordinary workforce remote access, and the broker's email confirms lack of verification and availability of required documentation. Could it still be true given unknown information? Unknown - while there may be unreported MFA implementation for the workforce, there is insufficient evidence to confirm this. Condition: unknown There are no explicit exception prerequisites mentioned in the rule text. Exception: does_not_apply No actual incompatible observations were found in the evidence provided. The lack of confirmation regarding workforce MFA does not constitute a contradiction with any stated facts. Conflict: none

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 1; model calls: 5; elapsed: 15.4s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts that PROVE this quoted trigger: E1 states that MFA is enabled for all four cloud administrators, but does not confirm MFA for the entire remote workforce. E2 indicates that a VPN configuration report was requested but not available, and no attestation of workforce MFA was supplied. Facts that REFUTE it: There is no evidence confirming that MFA protects ALL remote workforce logins; the questionnaire does not address ordinary workforce remote access, and the broker's email confirms lack of verification and availability of required documentation. Could it still be true given unknown information? Unknown - while there may be unreported MFA implementation for the workforce, there is insufficient evidence to confirm this. Condition: unknown There are no explicit exception prerequisites mentioned in the rule text. Exception: does_not_apply

### property_pump_service_unknown

**Expected:** Unlocated records and a visual inspection cannot establish a missed service visit.

**Model:** Subject is the fire pump at Cedar Components; period in scope is calendar 2025 Facts that PROVE this quoted trigger: None. The evidence does not contain any confirmation that the fire pump was serviced during 2025. Facts that REFUTE it: The surveyor notes that the maintenance binder was held off site and unavailable, which implies no direct evidence of service records being present. However, the visual condition of the pump (clean, no leaks, normal gauge) does not definitively prove or disprove servicing. Could it still be true given unknown information? Yes, because the absence of evidence of service does not confirm non-service; there may be records elsewhere or the service may have occurred but not been documented in the available sources. Condition is: unknown No explicit exception prerequisites are mentioned in the rule text. Exception is: does_not_apply There are no actual incompatible observations identified. The visual condition of the pump does not contradict the lack of service documentation, and the unavailability of records does not directly conflict with any stated facts about the pump's condition. Conflict is: none

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 11.1s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts that PROVE this quoted trigger: None. The evidence does not contain any confirmation that the fire pump was serviced during 2025. Facts that REFUTE it: The surveyor notes that the maintenance binder was held off site and unavailable, which implies no direct evidence of service records being present. However, the visual condition of the pump (clean, no leaks, normal gauge) does not definitively prove or disprove servicing. Could it still be true given unknown information? Yes, because the absence of evidence of service does not confirm non-service; there may be records elsewhere or the service may have occurred but not been documented in the available sources. Condition is: unknown No explicit exception prerequisites are mentioned in the rule text. Exception is: does_not_apply

### auto_driver_screening_unknown

**Expected:** Neither the interview process nor missing files establishes whether all MVR reviews occurred.

**Model:** The criterion requires that motor vehicle records be reviewed for every employed driver before hire. Evidence E1 indicates that hiring includes an interview and a route test, but the MVR review field is unanswered, meaning it's unknown whether MVR reviews occurred. Evidence E2 states that driver files have not been provided and there is no confirmation of whether pre-hire MVR reviews were conducted. Since the condition cannot be confirmed due to missing evidence about whether MVR reviews actually took place, this constitutes missing evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 14.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that motor vehicle records be reviewed for every employed driver before hire. Evidence E1 indicates that hiring includes an interview and a route test, but the MVR review field is unanswered, meaning it's unknown whether MVR reviews occurred. Evidence E2 states that driver files have not been provided and there is no confirmation of whether pre-hire MVR reviews were conducted. Since the condition cannot be confirmed due to missing evidence about whether MVR reviews actually took place, this constitutes missing evidence.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the trigger: None explicitly stated. Facts that REFUTE the trigger: E1 states 'The MVR review field is unanswered' and E2 states 'The driver files have not been provided' and 'no statement from the applicant confirming or denying pre-hire MVR reviews.' Given unknown information: Since there is no confirmation of MVR review completion, it cannot be determined if all drivers had their records reviewed before hire. Condition is FALSE because there is no evidence that MVRs were reviewed for every employed driver before hire. Rule does not specify any exceptions; does_not_apply

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_subcontract_limit_unknown

**Expected:** Unspecified insurance limits cannot satisfy or disprove the $2 million requirement.

**Model:** The criterion requires that every active roofing subcontractor maintain at least $2 million of general liability limits. While the evidence shows that both subcontractors are marked as insured in the vendor register (E1), it does not provide information about their actual liability limits. Additionally, certificates requesting the limits have not been received (E2). Since there is no confirmation of whether the limits meet the required $2 million threshold, and the absence of documentation cannot be taken as proof that the condition is false, the condition could still be true given what is unknown.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 12.2s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that every active roofing subcontractor maintain at least $2 million of general liability limits. While the evidence shows that both subcontractors are marked as insured in the vendor register (E1), it does not provide information about their actual liability limits. Additionally, certificates requesting the limits have not been received (E2). Since there is no confirmation of whether the limits meet the required $2 million threshold, and the absence of documentation cannot be taken as proof that the condition is false, the condition could still be true given what is unknown.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the quoted trigger: None. Facts that REFUTE it: The evidence shows that certificates for both roofing subcontractors (North Roof and Ridge Team) have been requested but not received, and their general liability limits have not been confirmed. Given unknown information, it cannot be determined if the limits meet the $2 million threshold. Therefore, condition = false. There are no explicit exception prerequisites mentioned in the rule that would apply to this situation. The rule does not specify any conditions under which the strength requirement might be waived or modified. Exception = does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_incident_rate_calculation

**Expected:** Three divided by 24 times 100 is 12.5, above 10. This is one aggregate finding, not three separate collision findings.

**Model:** The rule applies to the fleet level for the year 2025, with the subject being Summit Couriers' fleet operations during that period. Facts that PROVE: Summit Couriers recorded three preventable collisions in 2025 (E1). Facts that REFUTE: None directly refute the collision count. Given unknown information, it is possible the count could be higher or lower, but based on available evidence, the count is confirmed as three. The calculation is: (3 collisions / 24 active vehicles) * 100 = 12.5 collisions per 100 active vehicles. Since 12.5 > 10, the condition is TRUE. The rule does not specify any exceptions that would apply to Summit Couriers' situation. No explicit exception prerequisites or validity dates are mentioned in the guideline. There are no actual incompatible observations identified between E1 and E2. Both pieces of evidence support the same subject (Summit Couriers) and time period (2025), with E1 providing the collision count and E2 providing the active vehicle count.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 1; model calls: 5; elapsed: 18.6s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE: Summit Couriers recorded three preventable collisions in 2025 (E1). Facts that REFUTE: None directly refute the collision count. Given unknown information, it is possible the count could be higher or lower, but based on available evidence, the count is confirmed as three. The calculation is: (3 collisions / 24 active vehicles) * 100 = 12.5 collisions per 100 active vehicles. Since 12.5 > 10, the condition is TRUE. The rule does not specify any exceptions that would apply to Summit Couriers' situation. No explicit exception prerequisites or validity dates are mentioned in the guideline.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_reserves_exact_threshold

**Expected:** 480,000 / 120,000 equals exactly four months; at least includes equality.

**Model:** The subject is Bay Storage, and the period in scope is as of 2025-08-31, based on the evidence provided. Facts proving: The evidence states that Bay Storage's unrestricted cash is $480,000 and its monthly operating expense is $120,000 as of 2025-08-31. Calculation: $480,000 / $120,000 = 4 months. This meets the 'at least four months' requirement. Facts refuting: None provided. Given unknown information: No additional data affects this calculation. Therefore, condition is true. The rule does not specify any exceptions that apply to this situation. There are no explicit exception prerequisites or validity dates mentioned in the guideline. There are no conflicting observations in the provided evidence. All data points support the conclusion that Bay Storage meets the strength requirement.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 11.0s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts proving: The evidence states that Bay Storage's unrestricted cash is $480,000 and its monthly operating expense is $120,000 as of 2025-08-31. Calculation: $480,000 / $120,000 = 4 months. This meets the 'at least four months' requirement. Facts refuting: None provided. Given unknown information: No additional data affects this calculation. Therefore, condition is true. The rule does not specify any exceptions that apply to this situation. There are no explicit exception prerequisites or validity dates mentioned in the guideline.

### property_roof_exact_boundary

**Expected:** Exactly 20 does not exceed a strictly greater-than-20 threshold.

**Model:** The subject is the roof at Unit 7, and the period in scope is the assessment date of 2025-07-01. The evidence states that the roof was installed on 2005-07-01 and the survey dated 2025-07-01 records an age of exactly 20 years. Since the roof was installed on 2005-07-01, it would be exactly 20 years old on 2025-07-01. The trigger requires the roof to be strictly older than 20 years, which is not met. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the guideline for this criterion. There are no conflicting observations regarding the roof's installation date or age. The evidence clearly states that the roof was installed on 2005-07-01 and is exactly 20 years old on the assessment date of 2025-07-01.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 13.3s.

**Negative-evidence review (C1):** `supported`. The evidence establishes that Unit 7's roof was installed on 2005-07-01, and the assessment date is 2025-07-01, making the roof exactly 20 years old. The criterion requires the roof to be 'strictly older than 20 years,' which means it must be more than 20 years. Since the roof is exactly 20 years old and not strictly older, the condition is not met.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that the roof was installed on 2005-07-01 and the survey dated 2025-07-01 records an age of exactly 20 years. Since the roof was installed on 2005-07-01, it would be exactly 20 years old on 2025-07-01. The trigger requires the roof to be strictly older than 20 years, which is not met. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the guideline for this criterion.

### cyber_patch_coverage_boundary

**Expected:** 95/100 equals 95%, meeting an inclusive threshold despite five exceptions.

**Model:** The subject is '100 in-scope servers' and the period in scope is 'within 14 days of release'. The payload scope covers the whole case, which includes the assessment date 2025-09-01. Facts that PROVE: 95 out of 100 servers met the 14-day critical-patch deadline. Facts that REFUTE: 3 servers were patched on day 20, and 2 remain outstanding. Could it still be true given unknown information? Yes, if the remaining 2 servers are patched within 14 days or if the assessment date is after 14 days from patch release. Condition status: false, because less than 95% (95/100 = 95%) of servers have all critical patches installed within 14 days. No explicit exception prerequisites or validity dates are mentioned in the rule text. There are no actual incompatible observations. The evidence shows that 95 servers met the deadline, while 5 did not (3 on day 20 and 2 outstanding). This does not create a contradiction in facts but rather a failure to meet the threshold.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 11.9s.

**Negative-evidence review (C1):** `supported`. The criterion requires that at least 95% of the 100 in-scope servers have all critical patches installed within 14 days of release. Evidence E1 shows that 95 out of 100 servers met this deadline, but 5 servers (3 patched on day 20 and 2 outstanding) did not meet the 14-day deadline. Since the criterion demands that ALL critical patches be installed within 14 days for at least 95% of servers, and more than 5% failed to meet this requirement, the condition is not satisfied.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE: 95 out of 100 servers met the 14-day critical-patch deadline. Facts that REFUTE: 3 servers were patched on day 20, and 2 remain outstanding. Could it still be true given unknown information? Yes, if the remaining 2 servers are patched within 14 days or if the assessment date is after 14 days from patch release. Condition status: false, because less than 95% (95/100 = 95%) of servers have all critical patches installed within 14 days. No explicit exception prerequisites or validity dates are mentioned in the rule text.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_alarm_equal_reports

**Expected:** Equal-authority incompatible observations of the same state require abstention and both citations.

**Model:** The subject is the monitored fire alarm at Orchard Packaging, and the period in scope is 10:00 on 2025-06-12. Facts proving the trigger: E1 states that the central monitoring status was OFFLINE at 10:00 on 2025-06-12 for Orchard Packaging, account OP-11. Facts refuting the trigger: E2 states that the central monitoring status was ONLINE at 10:00 on 2025-06-12 for the same site and account. Given that there is a direct contradiction between the two sources regarding the status of the fire alarm at the exact time in question, and no correction or precedence is documented, the truth of whether the alarm was offline cannot be confirmed. Therefore, condition=unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this concern would not apply. Hence, exception=does_not_apply. There is an actual incompatible observation between E1 and E2 regarding the status of the fire alarm at Orchard Packaging at 10:00 on 2025-06-12. E1 reports OFFLINE while E2 reports ONLINE. These observations concern the same subject (Orchard Packaging fire alarm) and time (10:00 on 2025-06-12). Since there is no documented correction or precedence, this constitutes an unresolved conflict. Conflict=unresolved.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 6; elapsed: 24.9s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if the monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12.", "scope_reason": "The scope is determined by the rule's applicability, which is 'synthetic-guideline:property:v1'. The payload's scope field 'alarm:provider_b' is only an evidence-batch identifier and does not define the rule's scope. Evidence E1 relates directly to the monitored fire alarm at Orchard Packaging as specified in criterion C1.", "scope": "in_scope", "condition_reason": "The condition is TRUE because evidence E1 explicitly states that 'Orchard Packaging, account OP-11: central monitoring status was OFFLINE at 10:00 on 2025-06-12', which directly matches the trigger clause in criterion C1. The evidence confirms the fire alarm was offline at the specified time.", "condition": "true", "exception_reason": "There are no explicit exceptions stated in criterion C1 that would prevent the flagging of a concern based on the fire alarm being offline at the specified time. The rule does not specify any conditions under which the monitoring status being offline would not constitute a concern.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There is an unresolved conflict between Provider A (E1) and Provider B (E2). Provider A states the system was OFFLINE while Provider B states it was ONLINE at the same time. However, since the rule's scope is defined by 'synthetic-guideline:property:v1' and not by the payload's scope, and E1 is the only evidence directly supporting the condition in this context, the conflict remains unresolved.", "conflict": "unresolved", "findings": [{"subject": "Orchard Packaging", "evidence_ids": ["E1"], "reason": "The monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12, as stated in evidence E1."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...ated in evidence E1.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts proving the trigger: E1 states that the central monitoring status was OFFLINE at 10:00 on 2025-06-12 for Orchard Packaging, account OP-11. Facts refuting the trigger: E2 states that the central monitoring status was ONLINE at 10:00 on 2025-06-12 for the same site and account. Given that there is a direct contradiction between the two sources regarding the status of the fire alarm at the exact time in question, and no correction or precedence is documented, the truth of whether the alarm was offline cannot be confirmed. Therefore, condition=unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this concern would not apply. Hence, exception=does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_backup_immutability_conflict

**Expected:** Contradictory same-period attestations cannot be resolved by source votes or department titles.

**Model:** The subject is the production backup vault PV-3, and the period in scope is 2025-08-31. Facts proving the trigger: E1 states that 'the security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31.' This directly supports the condition. Facts refuting the trigger: E2 states that 'the infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31.' This contradicts the condition. Given that both attestations are signed on 2025-09-01 and concern the same configuration and period, but provide contradictory information about the state of immutable retention, the truth cannot be determined with certainty from the provided evidence alone. Therefore, condition = unknown. There are no explicit exception prerequisites mentioned in the rule or evidence that would apply to this situation. The rule does not specify any conditions under which the strength would not be recorded. Exception = does_not_apply. There is an actual incompatible observation between E1 and E2 regarding the state of immutable retention on vault PV-3 during 2025-08-31. E1 claims it was enabled, while E2 claims it was disabled. These observations concern the same subject (vault PV-3) and time period (2025-08-31). Since there is no indication of precedence or correction, this constitutes an unresolved conflict. Conflict = unresolved.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 3; model calls: 6; elapsed: 23.2s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts proving the trigger: E1 states that 'the security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31.' This directly supports the condition. Facts refuting the trigger: E2 states that 'the infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31.' This contradicts the condition. Given that both attestations are signed on 2025-09-01 and concern the same configuration and period, but provide contradictory information about the state of immutable retention, the truth cannot be determined with certainty from the provided evidence alone. Therefore, condition = unknown. There are no explicit exception prerequisites mentioned in the rule or evidence that would apply to this situation. The rule does not specify any conditions under which the strength would not be recorded. Exception = does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_mileage_corrected_denominator

**Expected:** Three per two million equals 1.5 per million, below two; the explicit correction controls the denominator.

**Model:** The subject is Northline and the period in scope is 2025. The evidence shows that Northline had three preventable collisions in 2025 (E1). The final corrected mileage is 2,000,000 miles (E3), which supersedes the original 1,000,000 miles reported (E2). The rate is calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This does not exceed the threshold of two per million miles. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule. There are no conflicting observations regarding the mileage or collision count for Northline in 2025.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 24.7s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion requires determining whether Northline's 2025 preventable collision rate exceeds two per million miles. Using the final corrected mileage of 2,000,000 miles (from E3) and three preventable collisions (from E1), the rate is 1.5 per million miles. This does not exceed the threshold of two per million miles, so the condition is false.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence shows that Northline had three preventable collisions in 2025 (E1). The final corrected mileage is 2,000,000 miles (E3), which supersedes the original 1,000,000 miles reported (E2). The rate is calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This does not exceed the threshold of two per million miles. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_later_repair_does_not_rewrite_history

**Expected:** The historical impairment remains a concern; a later repair is a state change, not a correction.

**Model:** The subject is Cedar Depot and the period in scope is 2025-03-01, which matches the historical assessment date mentioned in the guideline. Facts that PROVE this quoted trigger: E1 states 'At Cedar Depot on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired.' This directly establishes that the sprinkler system was impaired on the assessment date. Facts that REFUTE it: None provided. Could it still be true given unknown information? Yes, since the evidence clearly shows impairment on 2025-03-01, and later repair does not alter historical condition. Condition is TRUE. The rule does not specify any exceptions that would apply to this situation. There are no explicit exception prerequisites mentioned in the guideline text. Exception status is DOES_NOT_APPLY. There are no actual incompatible observations with the same subject and time. E2 describes a repair that occurred after the assessment date, which does not contradict the finding of impairment on 2025-03-01. Conflict status is NONE.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 14.7s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE this quoted trigger: E1 states 'At Cedar Depot on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired.' This directly establishes that the sprinkler system was impaired on the assessment date. Facts that REFUTE it: None provided. Could it still be true given unknown information? Yes, since the evidence clearly shows impairment on 2025-03-01, and later repair does not alter historical condition. Condition is TRUE. The rule does not specify any exceptions that would apply to this situation. There are no explicit exception prerequisites mentioned in the guideline text. Exception status is DOES_NOT_APPLY.

### property_electrical_exception

**Expected:** The age trigger applies but the documented complete replacement establishes the explicit exception.

**Model:** The building was constructed in 1952, which is before 1960. The subject is the building at Willow Print. Facts that PROVE the quoted trigger: The building was constructed in 1952 (before 1960). Facts that REFUTE the quoted trigger: A licensed electrical contractor documented complete replacement of original electrical wiring in 2018, which is after 2010. Given this documentation, the trigger condition is met and the concern should be flagged. The presence of a licensed contractor's certification of full replacement after 2010 negates the need for a concern. Therefore, condition=true. There are no explicit exception prerequisites mentioned in the rule text that would apply here. The rule does not specify any conditions under which this concern would not apply beyond the documented replacement of wiring after 2010 by a licensed contractor. Exception=does_not_apply. There are no actual incompatible observations. E1 establishes the building was constructed in 1952, and E2 shows that complete replacement occurred in 2018 by a licensed contractor. These facts support rather than contradict each other regarding the trigger condition. Conflict=none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 14.1s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE the quoted trigger: The building was constructed in 1952 (before 1960). Facts that REFUTE the quoted trigger: A licensed electrical contractor documented complete replacement of original electrical wiring in 2018, which is after 2010. Given this documentation, the trigger condition is met and the concern should be flagged. The presence of a licensed contractor's certification of full replacement after 2010 negates the need for a concern. Therefore, condition=true. There are no explicit exception prerequisites mentioned in the rule text that would apply here. The rule does not specify any conditions under which this concern would not apply beyond the documented replacement of wiring after 2010 by a licensed contractor. Exception=does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_service_account_exception

**Expected:** Both exception requirements are established, so lack of MFA does not trigger the concern for this account.

**Model:** The subject is 'invoice-sync' and the period is current as per evidence batch scope. Facts that PROVE the quoted trigger: The account 'invoice-sync' lacks MFA. Facts that REFUTE it: The account is a noninteractive service account with interactive login disabled, and has a documented credential rotation interval of 14 days (which is less than or equal to 30 days). Given this information, the condition is TRUE because the exception criteria are met. The exception prerequisites are: 1) noninteractive service account, 2) interactive login disabled, 3) documented credential rotation interval no longer than 30 days. All these are satisfied for 'invoice-sync'. The validity dates are not specified, but the evidence confirms the policy is active rather than merely planned. There are no actual incompatible observations. All facts support the exception criteria being met for 'invoice-sync'.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 5; elapsed: 14.3s.

**Negative-evidence review (C1):** `supported`. The criterion allows for accounts without MFA to be flagged as a concern, except for noninteractive service accounts with interactive login disabled and documented credential rotation no longer than 30 days. The evidence shows that invoice-sync is a noninteractive integration account with interactive login disabled, and has a documented automatic rotation interval of 14 days, which meets the exception criteria.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `applies`. Facts that PROVE the quoted trigger: The account 'invoice-sync' lacks MFA. Facts that REFUTE it: The account is a noninteractive service account with interactive login disabled, and has a documented credential rotation interval of 14 days (which is less than or equal to 30 days). Given this information, the condition is TRUE because the exception criteria are met. The exception prerequisites are: 1) noninteractive service account, 2) interactive login disabled, 3) documented credential rotation interval no longer than 30 days. All these are satisfied for 'invoice-sync'. The validity dates are not specified, but the evidence confirms the policy is active rather than merely planned.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_hot_work_scope_exclusion

**Expected:** The explicit operational scope excludes this applicant; a missing permit manual is irrelevant.

**Model:** The subject is a contractor performing on-site welding or flame cutting at customers' premises. The period in scope is the policy period. The evidence E1 states that Pine Design provides remote CAD drafting only and does not perform fabrication, installation, welding, flame cutting, or physical work at customer sites. This directly contradicts the trigger condition that requires contractors to be performing on-site welding or flame cutting. Therefore, the subject is not within the scope of the criterion. There are no explicit exception prerequisites mentioned in the criterion text. There is no actual incompatible observation. The evidence clearly indicates that Pine Design does not perform on-site welding or flame cutting, which means they do not meet the subject requirement of the criterion.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 7.1s.

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The evidence E1 states that Pine Design provides remote CAD drafting only and does not perform fabrication, installation, welding, flame cutting, or physical work at customer sites. This directly contradicts the trigger condition that requires contractors to be performing on-site welding or flame cutting. Therefore, the subject is not within the scope of the criterion. There are no explicit exception prerequisites mentioned in the criterion text.

### auto_passenger_scope_exclusion

**Expected:** Freight-only operations are outside the explicit passengers-for-hire scope.

**Model:** The subject is vehicles carrying passengers for hire. The period in scope is not specified, but the rule applies to annual completion requirements. The evidence states that Granite Freight operates five box trucks carrying packaged commercial goods and does not transport passengers for hire. Since the subject (vehicles carrying passengers for hire) is not applicable to this case, the condition cannot be evaluated as true or false based on the provided evidence. There are no explicit exception prerequisites mentioned in the rule that would apply to this situation. No conflicting observations are present. The evidence clearly indicates that the fleet does not carry passengers for hire, which is the subject of the rule.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 6.2s.

**Independent review (C1):** scope `out_of_scope`, condition `unknown`, exception `does_not_apply`. The evidence states that Granite Freight operates five box trucks carrying packaged commercial goods and does not transport passengers for hire. Since the subject (vehicles carrying passengers for hire) is not applicable to this case, the condition cannot be evaluated as true or false based on the provided evidence. There are no explicit exception prerequisites mentioned in the rule that would apply to this situation.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_multiple_warehouse_concerns

**Expected:** East and West qualify independently; extinguishers and future plans do not satisfy the condition, and the office is excluded.

**Model:** Subject is occupied storage warehouse; period is current (as of survey dates). Facts proving: E1 shows East Warehouse is occupied daily and has no automatic sprinklers; E2 shows West Warehouse is occupied on both shifts and has no automatic sprinklers. Facts refuting: None directly refute the trigger. Given unknown information, it's possible that some warehouses might have been equipped with sprinklers since the surveys were conducted, but current evidence supports the trigger. Condition: true. No explicit exceptions mentioned in the guideline for C1. The rule applies to all occupied storage warehouses lacking automatic sprinklers without specifying exclusions based on occupancy type or other factors. Exception: does_not_apply. No actual incompatible observations found between E1 and E2 regarding their respective warehouses' status as occupied storage facilities without automatic sprinklers. Both are consistent with the criterion's trigger. Conflict: none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 25.2s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts proving: E1 shows East Warehouse is occupied daily and has no automatic sprinklers; E2 shows West Warehouse is occupied on both shifts and has no automatic sprinklers. Facts refuting: None directly refute the trigger. Given unknown information, it's possible that some warehouses might have been equipped with sprinklers since the surveys were conducted, but current evidence supports the trigger. Condition: true. No explicit exceptions mentioned in the guideline for C1. The rule applies to all occupied storage warehouses lacking automatic sprinklers without specifying exclusions based on occupancy type or other factors. Exception: does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_multiple_expired_licences

**Expected:** Two independently identified employees meet the concern; Driver C does not.

**Model:** The subject is currently employed drivers. The period in scope is before 2025-09-01, with the renewal check as of 2025-09-01. Facts proving: Driver A's licence expired on 2025-07-31 (before 2025-09-01) and was unrenewed as of 2025-09-01. Driver B's licence expired on 2025-08-15 (before 2025-09-01) and was unrenewed as of 2025-09-01. Facts refuting: Driver C's licence is valid through 2027-02-01, so it does not meet the expired condition. Given unknown information, it is possible that other drivers may have expired licences but were not checked. Condition is true for Drivers A and B because both are currently employed, their licences expired before 2025-09-01, and they were unrenewed by that date. No explicit exceptions mentioned in the rule. The rule does not specify any conditions under which this concern would not apply. There are no actual incompatible observations between the evidence for Drivers A and B. Both drivers meet the criteria independently, and their licence statuses do not contradict each other.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 35.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts proving: Driver A's licence expired on 2025-07-31 (before 2025-09-01) and was unrenewed as of 2025-09-01. Driver B's licence expired on 2025-08-15 (before 2025-09-01) and was unrenewed as of 2025-09-01. Facts refuting: Driver C's licence is valid through 2027-02-01, so it does not meet the expired condition. Given unknown information, it is possible that other drivers may have expired licences but were not checked. Condition is true for Drivers A and B because both are currently employed, their licences expired before 2025-09-01, and they were unrenewed by that date. No explicit exceptions mentioned in the rule. The rule does not specify any conditions under which this concern would not apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_multiple_restore_strengths

**Expected:** Each application independently meets both timing conditions and warrants its own strength.

**Model:** The rule applies to business-critical applications with completed restore tests within the last 90 days and recovery times ≤ 4 hours, as of 2025-09-01. For Billing (E1): The test completed on 2025-08-10, which is within the last 90 days from 2025-09-01 (83 days). Recovery time was 3 hours, which is ≤ 4 hours. This satisfies both conditions. For Inventory (E2): The test completed on 2025-07-20, which is within the last 90 days from 2025-09-01 (45 days). Recovery time was exactly 4 hours, which is ≤ 4 hours. This also satisfies both conditions. Both applications meet the criteria. No explicit exceptions are mentioned in the rule text or evidence for either application. There are no conflicting observations between the two applications. Both meet the criteria independently.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 19.6s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. For Billing (E1): The test completed on 2025-08-10, which is within the last 90 days from 2025-09-01 (83 days). Recovery time was 3 hours, which is ≤ 4 hours. This satisfies both conditions. For Inventory (E2): The test completed on 2025-07-20, which is within the last 90 days from 2025-09-01 (45 days). Recovery time was exactly 4 hours, which is ≤ 4 hours. This also satisfies both conditions. Both applications meet the criteria. No explicit exceptions are mentioned in the rule text or evidence for either application.

### property_corroboration_not_two_events

**Expected:** One generator/test warrants one finding; either source independently supports it and both may be cited together.

**Model:** The subject is standby generator G-1 at Birch Cold Storage, and the period in scope is August 2025. Facts that PROVE: E1 states that Generator G-1 successfully supplied full building load during its completed test on 2025-08-12. E2 corroborates this by confirming the same test (T-118) occurred on 2025-08-12. Facts that REFUTE: None identified. Given unknown information, it is possible that additional tests occurred but are not documented. However, the evidence confirms one test under full load during August 2025. Therefore, condition = true. The rule does not specify any exceptions. No exception prerequisites or validity dates are mentioned. exception = does_not_apply There are no actual incompatible observations. Both E1 and E2 refer to the same test (T-118) on 2025-08-12 for the same generator (G-1). No contradictions exist between these records. conflict = none

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 15.3s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE: E1 states that Generator G-1 successfully supplied full building load during its completed test on 2025-08-12. E2 corroborates this by confirming the same test (T-118) occurred on 2025-08-12. Facts that REFUTE: None identified. Given unknown information, it is possible that additional tests occurred but are not documented. However, the evidence confirms one test under full load during August 2025. Therefore, condition = true. The rule does not specify any exceptions. No exception prerequisites or validity dates are mentioned. exception = does_not_apply

### gl_sister_company_evidence

**Expected:** A sister company's recall is not evidence of the applicant's recall history; absence of applicant records is not proof of no recall.

**Model:** The criterion requires determining if Aspen Foods LLC had a product recall during 2025. Evidence E2 indicates that Aspen Beverage LLC (a separate sister company) recalled a beverage product in May 2025, but provides no recall history for Aspen Foods LLC. The applicant's own recall response remains unanswered. While the recall involved a sister company, the evidence does not establish whether Aspen Foods LLC had a recall during 2025. The condition could still be true given what is unknown.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 5; elapsed: 12.8s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires determining if Aspen Foods LLC had a product recall during 2025. Evidence E2 indicates that Aspen Beverage LLC (a separate sister company) recalled a beverage product in May 2025, but provides no recall history for Aspen Foods LLC. The applicant's own recall response remains unanswered. While the recall involved a sister company, the evidence does not establish whether Aspen Foods LLC had a recall during 2025. The condition could still be true given what is unknown.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the quoted trigger: None. The evidence shows that Aspen Beverage LLC, a separate sister company, recalled a beverage product in May 2025. This recall does not involve Aspen Foods LLC. Facts that REFUTE the quoted trigger: The recall summary explicitly states that there is no recall history for Aspen Foods LLC and the applicant's own recall response remains unanswered, indicating no recall occurred for Aspen Foods LLC during 2025. Could it still be true given unknown information? No, because the evidence clearly indicates that the recall was for a different company (Aspen Beverage LLC) and there is no indication of any recall for Aspen Foods LLC. There are no explicit exception prerequisites mentioned in the rule.

### cyber_prior_year_does_not_prove_current

**Expected:** A previous-year control assessment and unknown post-migration controls cannot establish the current-year requirement.

**Model:** The rule concerns calendar 2025. The evidence batch covers the whole case, including 2025. Facts that PROVE: E1 states that offline backups were tested for all business-critical systems in calendar 2024, but does not confirm testing in 2025. Facts that REFUTE: E2 states that backup test records and offline-storage configuration for 2025 have not yet been supplied, and current effectiveness is unverified. Given unknown information about 2025 backups, the condition cannot be confirmed as true or false. Condition = unknown. The rule does not specify any explicit exceptions. No exception prerequisites to check. Exception = does_not_apply. There are no actual incompatible observations between E1 and E2 regarding the same subject and time period. E1 covers 2024, E2 covers 2025. Different subjects/times can coexist (different_scope). Conflict = none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 6; elapsed: 16.9s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts that PROVE: E1 states that offline backups were tested for all business-critical systems in calendar 2024, but does not confirm testing in 2025. Facts that REFUTE: E2 states that backup test records and offline-storage configuration for 2025 have not yet been supplied, and current effectiveness is unverified. Given unknown information about 2025 backups, the condition cannot be confirmed as true or false. Condition = unknown. The rule does not specify any explicit exceptions. No exception prerequisites to check. Exception = does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_building_specific_scope

**Expected:** Building A fails the wood-frame applicability condition; Building B cannot make an A-specific rule applicable.

**Model:** The subject is Building A and the period is current as of the survey date. The facts that prove the trigger are: 1) The engineer confirms there is no combustible wood structural frame in Building A (E1). 2) Building A has a steel structural frame and concrete external walls (E1). These facts refute the condition that Building A has a combustible wood structural frame. Since the criterion applies only if the building has a combustible wood structural frame, and it does not, the trigger is false. The fact that Building A lacks automatic sprinklers is irrelevant to whether the trigger is met because the trigger requires the presence of combustible wood structural frame. There are no explicit exception prerequisites mentioned in the criterion for Building A. There are no actual incompatible observations with the same subject and time. The evidence E1 confirms that Building A has a steel structural frame, which contradicts the requirement of having a combustible wood structural frame for the criterion to apply. However, this contradiction does not create an unresolved conflict because it simply means the trigger condition is not met.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 12.5s.

**Negative-evidence review (C1):** `supported`. The criterion applies specifically to Building A and requires that if its structural frame is combustible wood, then automatic sprinklers should be present as a concern. Evidence E1 explicitly states that Building A has a steel structural frame and concrete external walls, and that the engineer confirms there is no combustible wood structural frame in Building A. Since Building A does not have a combustible wood structural frame, the condition for applying the criterion is not met, and therefore no concern should be flagged.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The facts that prove the trigger are: 1) The engineer confirms there is no combustible wood structural frame in Building A (E1). 2) Building A has a steel structural frame and concrete external walls (E1). These facts refute the condition that Building A has a combustible wood structural frame. Since the criterion applies only if the building has a combustible wood structural frame, and it does not, the trigger is false. The fact that Building A lacks automatic sprinklers is irrelevant to whether the trigger is met because the trigger requires the presence of combustible wood structural frame. There are no explicit exception prerequisites mentioned in the criterion for Building A.

### wc_partial_payroll_period

**Expected:** A 20% quarter does not establish the full-year rate when the remaining nine months are unknown.

**Model:** The rule applies to the full 2025 calendar year. The subject is the insured's total overtime hours versus total hours worked in 2025. Facts that PROVE: E1 shows 2,000 overtime hours and 10,000 total hours for Q1 2025. Facts that REFUTE: E2 states that April-December 2025 hours have not been supplied, and the first-quarter rate cannot be assumed to continue. Given unknown information (missing Q2-Q4 data), it is impossible to determine if total overtime hours exceed 15% of all hours worked in 2025. Condition = unknown. Rule does not specify any exceptions. No actual incompatible observations identified. E1 and E2 present different time periods and data availability, but do not contradict each other directly. Conflict = none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 4; elapsed: 12.4s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Facts that PROVE: E1 shows 2,000 overtime hours and 10,000 total hours for Q1 2025. Facts that REFUTE: E2 states that April-December 2025 hours have not been supplied, and the first-quarter rate cannot be assumed to continue. Given unknown information (missing Q2-Q4 data), it is impossible to determine if total overtime hours exceed 15% of all hours worked in 2025. Condition = unknown. Rule does not specify any exceptions.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_document_submission_condition

**Expected:** Confirmed nonsubmission disproves a submission-specific strength without assuming no agreements exist.

**Model:** The subject is the submission and its attachments. The period in scope is the time of submission as defined by the intake process. Facts that PROVE the quoted trigger: None. The evidence E1 explicitly states that 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly contradicts the requirement for submission of such documents. Facts that REFUTE the quoted trigger: E1 confirms that no signed hold-harmless agreements were submitted for any active subcontractor, which means the condition is not met. Could it still be true given unknown information? No, because the evidence clearly indicates the absence of these documents in the submission. Therefore, condition = false. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which the submission of signed hold-harmless agreements would be excused or waived. Hence, exception = does_not_apply. There are no actual incompatible observations in the evidence provided that would create a conflict with the trigger condition. The single piece of evidence E1 clearly states the absence of signed hold-harmless agreements, which directly contradicts but does not conflict with the rule's requirement. Therefore, conflict = none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 9.4s.

**Negative-evidence review (C1):** `supported`. The evidence explicitly states that no signed hold-harmless agreements were supplied for any of the three active subcontractors. This directly contradicts the criterion's requirement that such agreements be provided with the submission.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the quoted trigger: None. The evidence E1 explicitly states that 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly contradicts the requirement for submission of such documents. Facts that REFUTE the quoted trigger: E1 confirms that no signed hold-harmless agreements were submitted for any active subcontractor, which means the condition is not met. Could it still be true given unknown information? No, because the evidence clearly indicates the absence of these documents in the submission. Therefore, condition = false. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which the submission of signed hold-harmless agreements would be excused or waived. Hence, exception = does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### wc_document_absence_is_concern

**Expected:** This criterion explicitly targets a missing submission document, so its confirmed absence supports a concern.

**Model:** The subject is Delta Fabrication and the period is the complete final submission as referenced in the evidence. Facts that PROVE this quoted trigger: The intake reviewer checked the complete final submission for Delta Fabrication and found that it includes payroll, a loss run, and an equipment list, but the required current written lockout procedure was not supplied. Facts that REFUTE it: None directly refute the lack of the required document; however, the absence of the lockout procedure in the submission directly supports the trigger condition. Could it still be true given unknown information? Yes, if there were other means of verifying the presence of the lockout procedure that are not mentioned in the evidence, but based on the provided information, the lack of the document is sufficient to establish the concern. Condition: true There are no explicit exception prerequisites or validity dates mentioned in the criterion text for C1. Exception: does_not_apply There are no actual incompatible observations identified in the evidence provided. The evidence clearly states that the required current written lockout procedure was not supplied in the submission, which aligns with the trigger condition. Conflict: none

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 2; model calls: 5; elapsed: 15.9s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "The intake reviewer checked the complete final submission for Delta Fabrication. It includes payroll, a loss run, and an equipment list, but the required current written lockout procedure was not supplied.", "scope_reason": "The subject is Delta Fabrication and the period is the complete final submission.", "scope": "in_scope", "condition_reason": "Facts that PROVE this quoted trigger: The intake reviewer explicitly checked the complete final submission and confirmed that the required current written lockout procedure was not supplied. Facts that REFUTE it: None; the evidence directly states the document was missing. Could it still be true given unknown information? No, because the evidence clearly indicates the absence of the required document in the submission.", "condition": "false", "exception_reason": "The rule does not specify any exceptions that would apply to this situation.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There are no conflicting observations regarding the presence or absence of the required lockout procedure in the submission. The evidence clearly indicates the document was not supplied.", "conflict": "none", "findings": [{"subject": "Delta Fabrication", "evidence_ids": ["E1"], "reason": "The intake reviewer checked the complete final submission for Delta Fabrication and confirmed that the required current written lockout procedure was not supplied, which constitutes a lack of the required document in the submission."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...t in the submission.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; condition_quote must be an exact excerpt from the requested criterion.text

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE this quoted trigger: The intake reviewer checked the complete final submission for Delta Fabrication and found that it includes payroll, a loss run, and an equipment list, but the required current written lockout procedure was not supplied. Facts that REFUTE it: None directly refute the lack of the required document; however, the absence of the lockout procedure in the submission directly supports the trigger condition. Could it still be true given unknown information? Yes, if there were other means of verifying the presence of the lockout procedure that are not mentioned in the evidence, but based on the provided information, the lack of the document is sufficient to establish the concern. Condition: true There are no explicit exception prerequisites or validity dates mentioned in the criterion text for C1. Exception: does_not_apply

### wc_activity_explicitly_not_performed

**Expected:** The explicit delayed induction disproves the all-employees pre-operation requirement despite later completion.

**Model:** Subject is newly hired production employees; period in scope is 2025. Facts proving the trigger: The evidence (E1) states that two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction. This directly contradicts the requirement that all such employees received induction before operating equipment in 2025. Facts refuting the trigger: The same evidence shows that induction was subsequently completed on 2025-05-08, but this does not satisfy the condition because the employees operated equipment before receiving induction. Could it still be true given unknown information? No, because the specific timing of when the employees first operated equipment and whether they received induction prior to that is explicitly stated in the evidence. Condition: false. The rule does not specify any exceptions for this criterion. There are no explicit exception prerequisites or validity dates mentioned. Exception: does_not_apply. There is an actual incompatible observation: E1 states that employees operated production equipment on 2025-05-02 without receiving machine-safety induction, which directly contradicts the requirement in the rule. Conflict: unresolved.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 9.8s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts proving the trigger: The evidence (E1) states that two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction. This directly contradicts the requirement that all such employees received induction before operating equipment in 2025. Facts refuting the trigger: The same evidence shows that induction was subsequently completed on 2025-05-08, but this does not satisfy the condition because the employees operated equipment before receiving induction. Could it still be true given unknown information? No, because the specific timing of when the employees first operated equipment and whether they received induction prior to that is explicitly stated in the evidence. Condition: false. The rule does not specify any exceptions for this criterion. There are no explicit exception prerequisites or validity dates mentioned. Exception: does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_inspection_date_unknown

**Expected:** Without the last-completed date, the twelve-month condition is unknown.

**Model:** The subject is the last completed electrical thermographic inspection at Fern Mill. The period in scope is up to 2025-09-01. The quoted trigger requires determining whether the last completed electrical thermographic inspection at Fern Mill occurred more than 12 months before 2025-09-01. Evidence E1 states that 'Fern Mill cannot locate the date of its last completed electrical thermographic inspection' and that 'Some contractor records were lost during a server migration.' This directly refutes the ability to confirm when the inspection was last completed, which is necessary to evaluate the trigger. Evidence E2 indicates that the survey did not include thermographic testing or verify the date of any earlier test, further supporting that no confirmation of inspection dates exists. Given these facts, it cannot be determined whether the condition is true or false; however, since the rule's trigger hinges on a specific date comparison and no such date can be established, the condition is unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. Therefore, the exception status is 'does_not_apply'. There are no actual incompatible observations identified between the evidence items E1 and E2 regarding the inspection date. Both pieces of evidence indicate a lack of information about the last inspection date, but they do not contradict each other. Therefore, there is no unresolved conflict.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 11.5s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The quoted trigger requires determining whether the last completed electrical thermographic inspection at Fern Mill occurred more than 12 months before 2025-09-01. Evidence E1 states that 'Fern Mill cannot locate the date of its last completed electrical thermographic inspection' and that 'Some contractor records were lost during a server migration.' This directly refutes the ability to confirm when the inspection was last completed, which is necessary to evaluate the trigger. Evidence E2 indicates that the survey did not include thermographic testing or verify the date of any earlier test, further supporting that no confirmation of inspection dates exists. Given these facts, it cannot be determined whether the condition is true or false; however, since the rule's trigger hinges on a specific date comparison and no such date can be established, the condition is unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. Therefore, the exception status is 'does_not_apply'.

### property_cross_source_alarm_and_value

**Expected:** The value and whole-stock alarm condition require combining both sources into one strength.

**Model:** The subject is Haven Parts, and the period in scope is as of 2025-09-01, based on the evidence dates. Facts that PROVE the trigger: E1 states that the total insured stock is $425,000 as of 2025-09-01, which is less than $500,000; E2 certifies that the entire interior of Haven Parts' sole warehouse is covered by an intruder alarm with continuous remote monitoring as of 2025-09-01. Facts that REFUTE the trigger: None identified. Given unknown information, it's possible that some stock may not be in a continuously monitored area or that the declared value exceeds $500,000, but no such evidence exists. Therefore, condition=true. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply. Hence, exception=does_not_apply. There are no actual incompatible observations identified between E1 and E2. Both pieces of evidence support the conditions required by the rule. Conflict=none.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 13.3s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts that PROVE the trigger: E1 states that the total insured stock is $425,000 as of 2025-09-01, which is less than $500,000; E2 certifies that the entire interior of Haven Parts' sole warehouse is covered by an intruder alarm with continuous remote monitoring as of 2025-09-01. Facts that REFUTE the trigger: None identified. Given unknown information, it's possible that some stock may not be in a continuously monitored area or that the declared value exceeds $500,000, but no such evidence exists. Therefore, condition=true. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply. Hence, exception=does_not_apply.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_loss_aggregation_without_duplicate

**Expected:** Distinct claims sum to $325,000, above $300,000. Do not add the repeated GL-101 again or create a finding per claim.

**Model:** Subject is general liability claims in 2025; period in scope is 2025. Facts proving: E1 states two distinct 2025 GL claims, GL-101 with $150,000 and GL-102 with $175,000. Facts refuting: E2 identifies E1's GL-101 as a duplicate reference, not an additional claim. Given unknown information: The latest paid amount for GL-101 is confirmed at $150,000 in both sources; GL-102's amount is $175,000. Total = $325,000. Since E2 indicates GL-101 is a duplicate, only one instance of GL-101 should be counted. Therefore, the total paid amounts for distinct claims = $150,000 + $175,000 = $325,000. This exceeds $300,000. Condition is true. No explicit exception prerequisites or validity dates mentioned in the rule. There is no actual incompatible observation. E2 clarifies that GL-101 is a duplicate reference, but does not contradict the paid amounts or claim existence. Both claims are distinct in nature and time, and E2 only addresses duplication of reference, not the validity of the claim itself.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 6; elapsed: 27.6s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000. Count each claim ID once, using its latest stated paid amount.", "scope_reason": "The scope is whole_case, which encompasses all evidence relevant to the assessment of 2025 general liability claims. The rule's applicability is not limited to any specific source batch; however, the evidence provided is from lossrun:primary and broker:claim_note sources. The subject of the assessment is the 2025 general liability claims listed in these sources.", "scope": "in_scope", "condition_reason": "The condition requires assessing whether total paid amounts for distinct 2025 general liability claims exceed $300,000. From E1, there are two distinct 2025 general liability claims: GL-101 with a paid amount of $150,000 and GL-102 with a paid amount of $175,000. The total paid amount is $325,000 ($1150,000 + $175,000). Since $325,000 exceeds the threshold of $300,000, the condition is met.", "condition": "true", "exception_reason": "There are no explicit exceptions listed in the criterion text that would apply to this situation. The rule does not specify any conditions under which the flagging would be waived or skipped.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There is a conflict between E1 and E2 regarding the number of distinct claims. E1 lists two distinct claims (GL-101 and GL-102), while E2 indicates that GL-101 is a duplicate reference, implying only one distinct claim exists. However, E2 does not provide an alternative paid amount for a second claim, and E1's evidence of two separate claims with different paid amounts is not contradicted by E2's statement about duplication.", "conflict": "unresolved", "findings": [{"subject": "2025 general liability claims", "evidence_ids": ["E1"], "reason": "The total paid amount for distinct 2025 general liability claims (GL-101: $150,000 and GL-102: $175,000) equals $325,000, which exceeds the threshold of $300,000. This meets the condition for flagging a concern."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r... flagging a concern.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Facts proving: E1 states two distinct 2025 GL claims, GL-101 with $150,000 and GL-102 with $175,000. Facts refuting: E2 identifies E1's GL-101 as a duplicate reference, not an additional claim. Given unknown information: The latest paid amount for GL-101 is confirmed at $150,000 in both sources; GL-102's amount is $175,000. Total = $325,000. Since E2 indicates GL-101 is a duplicate, only one instance of GL-101 should be counted. Therefore, the total paid amounts for distinct claims = $150,000 + $175,000 = $325,000. This exceeds $300,000. Condition is true. No explicit exception prerequisites or validity dates mentioned in the rule.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_restore_duration_cross_midnight

**Expected:** Elapsed time is 25.5 hours, exceeding the 24-hour maximum despite a successful eventual restore.

**Model:** The subject is the full restore of the payroll application, and the period in scope is from 2025-08-01 08:00 UTC to 2025-08-02 09:30 UTC. The facts that prove this trigger are: E1 states the restore began at 2025-08-01 08:00 UTC, and E2 states it completed at 2025-08-02 09:30 UTC. The elapsed time is calculated as follows: From 2025-08-01 08:00 to 2025-08-02 09:30 is exactly 25 hours and 30 minutes. Since 25 hours and 30 minutes is greater than 24 hours, the condition is false. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply here. There are no actual incompatible observations with the same subject and time period. The timestamps provided in E1 and E2 are consistent with each other and support the calculation of elapsed time.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 1; model calls: 6; elapsed: 17.9s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion requires determining whether the completed full restore of the payroll application took no longer than 24 hours. The start timestamp is 2025-08-01 08:00 UTC and the completion timestamp is 2025-08-02 09:30 UTC. Calculating the elapsed time: from 08:00 on August 1 to 09:30 on August 2 is exactly 25 hours and 30 minutes. This exceeds the 24-hour threshold, making the condition false. The evidence directly supports this calculation.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The facts that prove this trigger are: E1 states the restore began at 2025-08-01 08:00 UTC, and E2 states it completed at 2025-08-02 09:30 UTC. The elapsed time is calculated as follows: From 2025-08-01 08:00 to 2025-08-02 09:30 is exactly 25 hours and 30 minutes. Since 25 hours and 30 minutes is greater than 24 hours, the condition is false. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply here.

### property_expired_exception_certificate

**Expected:** The height trigger is met and the explicit approval exception is unavailable on the assessment date.

**Model:** The subject is combustible stock at Linden Distribution storage area. The period in scope is 2025-09-01, which matches the survey date. The facts that prove this trigger are: (1) At Linden Distribution on 2025-09-01, combustible packaged stock was stacked to 5.2 metres, and (2) The applicant refers the surveyor to its engineer's high-stack approval for this storage area. The facts that refute it are: (1) The engineer's approval for Linden's same storage area explicitly allowed stacks up to 5.5 metres but expired on 2025-06-30, and (2) The engineer confirms no renewal or extension was issued before 2025-09-01. Given that the approval expired before the survey date and no renewal was issued, it is not valid on 2025-09-01. Therefore, the condition is true because the stack height exceeds four metres and there is no valid high-stack approval. The exception applies if an engineer's specific high-stack approval remains valid on 2025-09-01. However, the engineer's approval expired on 2025-06-30 and no renewal or extension was issued before 2025-09-01. Therefore, the exception does not apply. There are no actual incompatible observations. E1 indicates that the stack height was 5.2 metres and refers to an engineer's approval, while E2 states that the approval expired on 2025-06-30 with no renewal before 2025-09-01. These do not contradict each other directly; rather, they support the conclusion that the stack height exceeded the limit and there was no valid approval.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 17.3s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The facts that prove this trigger are: (1) At Linden Distribution on 2025-09-01, combustible packaged stock was stacked to 5.2 metres, and (2) The applicant refers the surveyor to its engineer's high-stack approval for this storage area. The facts that refute it are: (1) The engineer's approval for Linden's same storage area explicitly allowed stacks up to 5.5 metres but expired on 2025-06-30, and (2) The engineer confirms no renewal or extension was issued before 2025-09-01. Given that the approval expired before the survey date and no renewal was issued, it is not valid on 2025-09-01. Therefore, the condition is true because the stack height exceeds four metres and there is no valid high-stack approval. The exception applies if an engineer's specific high-stack approval remains valid on 2025-09-01. However, the engineer's approval expired on 2025-06-30 and no renewal or extension was issued before 2025-09-01. Therefore, the exception does not apply.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
