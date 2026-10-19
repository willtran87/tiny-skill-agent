# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T07:50:48.298783+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **24/32** (planned: 32).
- Correct case statuses: **30/32**.
- Required gold evidence cited: **35/35**.
- Reference/provenance checks: **147/147**.
- False-positive findings in the 20 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| cyber_remote_access_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_pump_service_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_driver_screening_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| gl_subcontract_limit_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_incident_rate_calculation | matched | matched | 1 / 1 | 2 / 2 | PASS |
| property_reserves_exact_threshold | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_roof_exact_boundary | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| cyber_patch_coverage_boundary | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_alarm_equal_reports | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| cyber_backup_immutability_conflict | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| auto_mileage_corrected_denominator | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| property_later_repair_does_not_rewrite_history | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_electrical_exception | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| cyber_service_account_exception | no_match | insufficient_evidence | 0 / 0 | 2 / 2 | FAIL |
| gl_hot_work_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
| auto_passenger_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
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
| wc_activity_explicitly_not_performed | no_match | no_match | 0 / 0 | 1 / 1 | FAIL |
| property_inspection_date_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_cross_source_alarm_and_value | matched | matched | 1 / 1 | 2 / 2 | PASS |
| gl_loss_aggregation_without_duplicate | matched | matched | 1 / 1 | 1 / 1 | FAIL |
| cyber_restore_duration_cross_midnight | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| property_expired_exception_certificate | matched | matched | 1 / 1 | 2 / 2 | PASS |

## Reasons and diagnostics

### cyber_remote_access_unknown

**Expected:** Administrator MFA does not establish workforce MFA; blank or unavailable records do not prove absence of the control.

**Model:** The subject is 'remote workforce login' to Harbor Analytics. The period in scope is 'as of 2025-09-01'. The evidence indicates that MFA is enabled for all four cloud administrators (E1), but there is no information about ordinary workforce remote access or VPN authentication. The questionnaire does not specify whether the workforce uses VPN or remote desktop, and the broker's email states that a VPN configuration report was not available (E2). Since there is insufficient evidence to confirm that MFA protects ALL remote workforce logins, the condition cannot be confirmed as true. However, it also cannot be definitively proven false due to missing data about ordinary workforce access. Therefore, the truth of the trigger is unknown. There are no explicit exception prerequisites mentioned in the rule that would apply here. There is no actual incompatible observation. The lack of information about workforce remote access does not create a contradiction with the presence of MFA for administrators.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 5; elapsed: 29.7s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence indicates that MFA is enabled for all four cloud administrators (E1), but there is no information about ordinary workforce remote access or VPN authentication. The questionnaire does not specify whether the workforce uses VPN or remote desktop, and the broker's email states that a VPN configuration report was not available (E2). Since there is insufficient evidence to confirm that MFA protects ALL remote workforce logins, the condition cannot be confirmed as true. However, it also cannot be definitively proven false due to missing data about ordinary workforce access. Therefore, the truth of the trigger is unknown. There are no explicit exception prerequisites mentioned in the rule that would apply here.

### property_pump_service_unknown

**Expected:** Unlocated records and a visual inspection cannot establish a missed service visit.

**Model:** Subject is the fire pump at Cedar Components; period in scope is calendar 2025 The evidence does not contain any record of fire pump servicing occurring in 2025. E1 states that the maintenance binder was held off site and unavailable, which implies no accessible service records. E2 indicates that the pump contractor's 2025 service invoice cannot be located, and there is no confirmation of whether the visit took place. There are no positive assertions confirming that servicing occurred in 2025. Therefore, it cannot be established that the fire pump was serviced during calendar 2025. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no contradictory observations regarding the fire pump's servicing status in 2025. The lack of service records does not constitute a contradiction but rather an absence of evidence supporting the servicing occurred.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 13.8s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence does not contain any record of fire pump servicing occurring in 2025. E1 states that the maintenance binder was held off site and unavailable, which implies no accessible service records. E2 indicates that the pump contractor's 2025 service invoice cannot be located, and there is no confirmation of whether the visit took place. There are no positive assertions confirming that servicing occurred in 2025. Therefore, it cannot be established that the fire pump was serviced during calendar 2025. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### auto_driver_screening_unknown

**Expected:** Neither the interview process nor missing files establishes whether all MVR reviews occurred.

**Model:** The criterion requires that motor vehicle records be reviewed for every employed driver before hire, and a record of this review must exist. Evidence E1 indicates that the MVR review field is unanswered, which means there is no documented evidence of whether reviews occurred. Evidence E2 states that driver files (which would include MVR records) have not been provided, and there is no confirmation or denial of pre-hire MVR reviews. Since the absence of documentation does not prove that the activity did not occur, and the lack of explicit information about MVR reviews cannot establish a negative decision, this situation involves missing evidence rather than definitive proof of non-compliance.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 6; elapsed: 14.5s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that motor vehicle records be reviewed for every employed driver before hire, and a record of this review must exist. Evidence E1 indicates that the MVR review field is unanswered, which means there is no documented evidence of whether reviews occurred. Evidence E2 states that driver files (which would include MVR records) have not been provided, and there is no confirmation or denial of pre-hire MVR reviews. Since the absence of documentation does not prove that the activity did not occur, and the lack of explicit information about MVR reviews cannot establish a negative decision, this situation involves missing evidence rather than definitive proof of non-compliance.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_subcontract_limit_unknown

**Expected:** Unspecified insurance limits cannot satisfy or disprove the $2 million requirement.

**Model:** The criterion requires that every active roofing subcontractor maintain at least $2 million of general liability limits, and this requirement is tested by the existence of records documenting those limits. Although the subcontractors are marked as insured in the vendor register (E1), no records confirming the specific limits have been provided. The certificates requesting the limits have not been received (E2). Since the absence of documentation regarding the limits cannot be used to affirmatively prove that the limits are below $2 million, and because the requirement is about documented limits rather than mere insured status, a negative decision cannot be legitimately made based on the available evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 6; elapsed: 15.4s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that every active roofing subcontractor maintain at least $2 million of general liability limits, and this requirement is tested by the existence of records documenting those limits. Although the subcontractors are marked as insured in the vendor register (E1), no records confirming the specific limits have been provided. The certificates requesting the limits have not been received (E2). Since the absence of documentation regarding the limits cannot be used to affirmatively prove that the limits are below $2 million, and because the requirement is about documented limits rather than mere insured status, a negative decision cannot be legitimately made based on the available evidence.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_incident_rate_calculation

**Expected:** Three divided by 24 times 100 is 12.5, above 10. This is one aggregate finding, not three separate collision findings.

**Model:** The rule applies to the fleet level for the year 2025. The subject is Summit Couriers, which is within the scope of the guideline. The preventable collision count for 2025 is 3 (from E1). The active fleet count is 24 (from E2). The frequency is calculated as (3 collisions / 24 vehicles) * 100 = 12.5 collisions per 100 vehicles. Since 12.5 > 10, the condition is true. There are no explicit exception prerequisites mentioned in the rule that would apply to Summit Couriers. There are no conflicting observations regarding the preventable collision count or active fleet count for Summit Couriers.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 0; model calls: 5; elapsed: 16.5s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The preventable collision count for 2025 is 3 (from E1). The active fleet count is 24 (from E2). The frequency is calculated as (3 collisions / 24 vehicles) * 100 = 12.5 collisions per 100 vehicles. Since 12.5 > 10, the condition is true. There are no explicit exception prerequisites mentioned in the rule that would apply to Summit Couriers.

### property_reserves_exact_threshold

**Expected:** 480,000 / 120,000 equals exactly four months; at least includes equality.

**Model:** Subject is Bay Storage; period is as of 2025-08-31 The evidence shows that Bay Storage's unrestricted cash as of 2025-08-31 is $480,000 and its monthly operating expense is $120,000. The calculation is: $480,000 / $120,000 = 4 months. This meets the requirement of at least four months of operating expense. Therefore, the condition is true. The rule does not specify any exceptions that would apply to this case. There are no conflicting observations in the provided evidence.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 12.8s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The evidence shows that Bay Storage's unrestricted cash as of 2025-08-31 is $480,000 and its monthly operating expense is $120,000. The calculation is: $480,000 / $120,000 = 4 months. This meets the requirement of at least four months of operating expense. Therefore, the condition is true. The rule does not specify any exceptions that would apply to this case.

### property_roof_exact_boundary

**Expected:** Exactly 20 does not exceed a strictly greater-than-20 threshold.

**Model:** The subject is 'the roof at Unit 7' and the period in scope is 'on the assessment date of 2025-07-01'. The evidence states that the roof was installed on 2005-07-01 and the survey dated 2025-07-01 records an age of exactly 20 years. The time elapsed from installation to assessment date is exactly 20 years, not strictly older than 20 years. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule. There are no conflicting observations regarding the roof's installation date or age.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 12.5s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining if the roof at Unit 7 is strictly older than 20 years on the assessment date of 2025-07-01. Evidence E1 states that the roof was installed on 2005-07-01 and that the survey dated 2025-07-01 records an age of exactly 20 years. Since the roof's age is exactly 20 years, it does not meet the condition of being 'strictly older than 20 years.' Therefore, the criterion's condition is false.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that the roof was installed on 2005-07-01 and the survey dated 2025-07-01 records an age of exactly 20 years. The time elapsed from installation to assessment date is exactly 20 years, not strictly older than 20 years. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule.

### cyber_patch_coverage_boundary

**Expected:** 95/100 equals 95%, meeting an inclusive threshold despite five exceptions.

**Model:** The subject is '100 in-scope servers' and the period in scope is 'all critical patches installed within 14 days of release'. The payload scope includes these 100 servers as specified in E1. From E1, 95 out of 100 servers (95%) met the 14-day critical-patch deadline. This meets the threshold of at least 95%. The remaining 5 servers are not specified as having exceeded the 14-day window, but since only 3 were patched on day 20 and 2 remain outstanding, it is implied that they did not meet the deadline. Therefore, the condition is true. There are no explicit exception prerequisites mentioned in the rule text for C1. No conflicting observations were found. All data points support that 95 out of 100 servers met the deadline, which satisfies the condition.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 13.4s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. From E1, 95 out of 100 servers (95%) met the 14-day critical-patch deadline. This meets the threshold of at least 95%. The remaining 5 servers are not specified as having exceeded the 14-day window, but since only 3 were patched on day 20 and 2 remain outstanding, it is implied that they did not meet the deadline. Therefore, the condition is true. There are no explicit exception prerequisites mentioned in the rule text for C1.

### property_alarm_equal_reports

**Expected:** Equal-authority incompatible observations of the same state require abstention and both citations.

**Model:** The subject is 'monitored fire alarm at Orchard Packaging' and the period in scope is '10:00 on 2025-06-12'. Observation E1 states that the central monitoring status was OFFLINE at 10:00 on 2025-06-12 for Orchard Packaging (account OP-11). Observation E2 states the opposite, that it was ONLINE at the same time. There are no other observations supporting or refuting the trigger condition directly. The presence of conflicting reports does not allow a determination of truth based on available evidence alone. There is no explicit exception mentioned in the rule text. There is an actual incompatible observation: E1 reports the alarm as OFFLINE while E2 reports it as ONLINE at the same time and location. These observations are contradictory regarding the status of the monitored fire alarm.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 24.7s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if the monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12.", "scope_reason": "The criterion explicitly applies to the monitored fire alarm at Orchard Packaging, which matches the subject of the evidence. There is no explicit exclusion of the subject by the rule; thus, scope is in_scope.", "scope": "in_scope", "condition_reason": "The condition requires that the monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12. Evidence E1 states that the central monitoring status was OFFLINE at that time, which directly supports the condition. Although E2 reports ONLINE status for the same time and site, this is a conflicting report, but the condition is evaluated based on the actual state as reported by one source.", "condition": "true", "exception_reason": "There are no explicit exceptions in the rule text that would apply to this case. The rule does not specify conditions under which the concern would not be flagged, such as a required maintenance log or a specific override mechanism.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There is a conflict between E1 and E2 regarding the status of the fire alarm at Orchard Packaging at 10:00 on 2025-06-12. E1 reports OFFLINE, while E2 reports ONLINE. However, since the condition is based on the actual state as reported by one source (E1), and no correction or precedence is documented, the conflict does not negate the established condition.", "conflict": "unresolved", "findings": [{"subject": "Orchard Packaging", "evidence_ids": ["E1"], "reason": "The monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12, as reported by E1. This meets the condition for flagging a concern."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r... flagging a concern.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Observation E1 states that the central monitoring status was OFFLINE at 10:00 on 2025-06-12 for Orchard Packaging (account OP-11). Observation E2 states the opposite, that it was ONLINE at the same time. There are no other observations supporting or refuting the trigger condition directly. The presence of conflicting reports does not allow a determination of truth based on available evidence alone. There is no explicit exception mentioned in the rule text.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_backup_immutability_conflict

**Expected:** Contradictory same-period attestations cannot be resolved by source votes or department titles.

**Model:** The subject is the production backup vault PV-3, and the period in scope is 2025-08-31. E1 states that the security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31. E2 states that the infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31. These statements directly contradict each other regarding the state of immutable retention on the same vault and date. There is no supporting evidence that confirms the retention was enabled; rather, there are two conflicting attestations. There are no explicit exception prerequisites mentioned in the rule or evidence for this criterion. There is a direct contradiction between E1 and E2 regarding whether immutable retention was enabled or disabled on vault PV-3 on 2025-08-31. Both attestations concern the same subject and time period, and neither provides sufficient evidence to resolve the discrepancy.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 5; elapsed: 15.2s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. E1 states that the security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31. E2 states that the infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31. These statements directly contradict each other regarding the state of immutable retention on the same vault and date. There is no supporting evidence that confirms the retention was enabled; rather, there are two conflicting attestations. There are no explicit exception prerequisites mentioned in the rule or evidence for this criterion.

### auto_mileage_corrected_denominator

**Expected:** Three per two million equals 1.5 per million, below two; the explicit correction controls the denominator.

**Model:** The rule applies to Northline's 2025 preventable collision rate. The subject is Northline, and the period in scope is calendar year 2025. Northline had three preventable collisions in 2025. The final corrected mileage is 2,000,000 miles (from E3). The rate is calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This does not exceed the threshold of 2 per million miles. Therefore, the condition is false. The rule does not specify any exceptions that would apply to this case. There are no conflicting observations regarding the mileage or collision count for Northline in 2025. The corrected mileage from E3 supersedes the original estimate from E2, but this does not create a contradiction with the collision data from E1.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 7; elapsed: 19.7s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining whether Northline's 2025 preventable collision rate exceeds two per million miles. The evidence shows three preventable collisions occurred in 2025, and the final corrected mileage is 2,000,000 miles. This results in a rate of 1.5 preventable collisions per million miles, which does not exceed the threshold of two per million miles. Therefore, the condition is false, and the criterion should be flagged as not met.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Northline had three preventable collisions in 2025. The final corrected mileage is 2,000,000 miles (from E3). The rate is calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This does not exceed the threshold of 2 per million miles. Therefore, the condition is false. The rule does not specify any exceptions that would apply to this case.

### property_later_repair_does_not_rewrite_history

**Expected:** The historical impairment remains a concern; a later repair is a state change, not a correction.

**Model:** The subject is Cedar Depot, and the period in scope is the historical assessment date 2025-03-01. On 2025-03-01, E1 states that 'the inspector found the sprinkler control valve seized closed and the sprinkler system impaired.' This directly supports the trigger condition that the sprinkler system was impaired on the historical assessment date. The later repair on 2025-03-05 does not alter the historical condition as specified in the rule. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There is no conflicting evidence regarding the impairment of the sprinkler system on 2025-03-01. E2 describes a repair that occurred after the assessment date, which does not contradict the finding of impairment on the historical date.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 17.7s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. On 2025-03-01, E1 states that 'the inspector found the sprinkler control valve seized closed and the sprinkler system impaired.' This directly supports the trigger condition that the sprinkler system was impaired on the historical assessment date. The later repair on 2025-03-05 does not alter the historical condition as specified in the rule. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### property_electrical_exception

**Expected:** The age trigger applies but the documented complete replacement establishes the explicit exception.

**Model:** The building was constructed in 1952, which is before 1960. The subject is an individual building, and the rule applies to buildings constructed before 1960. The building was constructed in 1952, which satisfies the 'before 1960' condition. A licensed contractor documented complete replacement of the original electrical wiring in 2018, which is after 2010. Therefore, the exception condition is met, and the trigger does not hold. The rule includes an exception: 'unless a licensed contractor documents complete replacement of its original electrical wiring after 2010.' The evidence shows that a licensed contractor documented complete replacement in 2018, which satisfies this exception. Therefore, the exception applies. There are no conflicting observations regarding the building's construction year or the wiring replacement documentation. The evidence supports that the building was constructed before 1960 and that complete replacement occurred after 2010.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 16.8s.

**Negative-evidence review (C1):** `supported`. The criterion requires documentation of complete replacement of electrical wiring after 2010. Evidence E2 shows a licensed contractor certified that all original electrical wiring was removed and replaced in 2018, which satisfies the documentation requirement for the activity. The building was constructed in 1952, so the condition for flagging a concern is not met because the wiring was completely replaced after 2010.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `applies`. The building was constructed in 1952, which satisfies the 'before 1960' condition. A licensed contractor documented complete replacement of the original electrical wiring in 2018, which is after 2010. Therefore, the exception condition is met, and the trigger does not hold. The rule includes an exception: 'unless a licensed contractor documents complete replacement of its original electrical wiring after 2010.' The evidence shows that a licensed contractor documented complete replacement in 2018, which satisfies this exception. Therefore, the exception applies.

### cyber_service_account_exception

**Expected:** Both exception requirements are established, so lack of MFA does not trigger the concern for this account.

**Model:** The criterion requires flagging concerns for accounts without MFA, except for specific exceptions. The evidence shows that the account 'invoice-sync' lacks MFA but is a noninteractive service account with interactive login disabled. Additionally, there is documentation of credential rotation occurring every 14 days, which meets the requirement of no more than 30 days. Since all conditions are met to qualify for the exception, the criterion's condition could still be true given the known information.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 16.2s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires flagging concerns for accounts without MFA, except for specific exceptions. The evidence shows that the account 'invoice-sync' lacks MFA but is a noninteractive service account with interactive login disabled. Additionally, there is documentation of credential rotation occurring every 14 days, which meets the requirement of no more than 30 days. Since all conditions are met to qualify for the exception, the criterion's condition could still be true given the known information.

### gl_hot_work_scope_exclusion

**Expected:** The explicit operational scope excludes this applicant; a missing permit manual is irrelevant.

**Model:** The subject is a contractor performing on-site welding or flame cutting at customers' premises. The evidence shows that Pine Design provides remote CAD drafting only and does not perform fabrication, installation, welding, flame cutting, or physical work at customer sites. The rule's trigger requires contractors performing on-site welding or flame cutting at customers' premises. However, the evidence shows that Pine Design performs remote CAD drafting only and does not perform any physical work at customer sites, including welding or flame cutting. Therefore, the subject does not meet the condition for applicability. The rule does not contain explicit exception prerequisites. The scope restriction 'only to contractors performing on-site welding or flame cutting' is sufficient to exclude Pine Design from the application of this criterion. There are no conflicting observations regarding whether Pine Design performs on-site welding or flame cutting. The evidence clearly states that Pine Design provides remote CAD drafting only and does not perform any physical work at customer sites.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 10.4s.

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The rule's trigger requires contractors performing on-site welding or flame cutting at customers' premises. However, the evidence shows that Pine Design performs remote CAD drafting only and does not perform any physical work at customer sites, including welding or flame cutting. Therefore, the subject does not meet the condition for applicability. The rule does not contain explicit exception prerequisites. The scope restriction 'only to contractors performing on-site welding or flame cutting' is sufficient to exclude Pine Design from the application of this criterion.

### auto_passenger_scope_exclusion

**Expected:** Freight-only operations are outside the explicit passengers-for-hire scope.

**Model:** The rule applies to vehicles carrying passengers for hire. E1 states that Granite Freight operates five box trucks carrying packaged commercial goods and does not transport passengers for hire. The subject (vehicles) are not in the scope of the rule. The trigger is 'emergency evacuation training is not completed annually.' However, since the vehicles do not carry passengers for hire, the condition is not applicable to the subject matter. There is no supporting or refuting evidence regarding emergency evacuation training because the rule does not apply. There are no explicit exception prerequisites mentioned in the rule that would apply here. No conflicting observations exist. The evidence clearly indicates that the vehicles do not carry passengers for hire, which is the exclusion criterion for this rule.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 9.1s.

**Independent review (C1):** scope `out_of_scope`, condition `unknown`, exception `does_not_apply`. The trigger is 'emergency evacuation training is not completed annually.' However, since the vehicles do not carry passengers for hire, the condition is not applicable to the subject matter. There is no supporting or refuting evidence regarding emergency evacuation training because the rule does not apply. There are no explicit exception prerequisites mentioned in the rule that would apply here.

### property_multiple_warehouse_concerns

**Expected:** East and West qualify independently; extinguishers and future plans do not satisfy the condition, and the office is excluded.

**Model:** The subject is an occupied storage warehouse. The period in scope is current condition, as indicated by the context of each observation. E1 describes East Warehouse as a storage warehouse that is occupied daily and has no automatic sprinklers. This meets the trigger condition of an occupied storage warehouse lacking automatic sprinklers. E2 describes West Warehouse as a storage warehouse that is occupied on both shifts and has no automatic sprinklers, meeting the same condition. E3 describes an office-only building which is outside the scope of this criterion. There are no explicit exceptions mentioned in the rule text for C1. There are no conflicting observations regarding the occupancy or presence of automatic sprinklers for E1 and E2. The observations do not contradict each other in terms of the criteria being evaluated.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 24.9s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. E1 describes East Warehouse as a storage warehouse that is occupied daily and has no automatic sprinklers. This meets the trigger condition of an occupied storage warehouse lacking automatic sprinklers. E2 describes West Warehouse as a storage warehouse that is occupied on both shifts and has no automatic sprinklers, meeting the same condition. E3 describes an office-only building which is outside the scope of this criterion. There are no explicit exceptions mentioned in the rule text for C1.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_multiple_expired_licences

**Expected:** Two independently identified employees meet the concern; Driver C does not.

**Model:** The rule applies to currently employed drivers with licences that expired before 2025-09-01 and were not renewed by that date. Driver A is currently employed, and their licence expired on 2025-07-31, which is before 2025-09-01. Driver B is also currently employed, and their licence expired on 2025-08-15, which is also before 2025-09-01. Driver C is currently employed but holds a valid licence through 2027-02-01, so they do not meet the trigger condition. For Driver A: The licence expired on 2025-07-31 (before 2025-09-01), and it was unrenewed as of 2025-09-01. This supports the trigger condition. For Driver B: The licence expired on 2025-08-15 (before 2025-09-01), and it was unrenewed as of 2025-09-01. This also supports the trigger condition. For Driver C: Their licence is valid through 2027-02-01, so they do not meet the expired licence requirement. There are no explicit exceptions mentioned in the rule text for this criterion. There are no conflicting observations regarding the licence status or employment status of Drivers A and B. The evidence clearly indicates that both drivers were employed and had expired licences not renewed by 2025-09-01.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 35.5s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. For Driver A: The licence expired on 2025-07-31 (before 2025-09-01), and it was unrenewed as of 2025-09-01. This supports the trigger condition. For Driver B: The licence expired on 2025-08-15 (before 2025-09-01), and it was unrenewed as of 2025-09-01. This also supports the trigger condition. For Driver C: Their licence is valid through 2027-02-01, so they do not meet the expired licence requirement. There are no explicit exceptions mentioned in the rule text for this criterion.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_multiple_restore_strengths

**Expected:** Each application independently meets both timing conditions and warrants its own strength.

**Model:** The rule applies to business-critical applications. Both Billing and Inventory are designated as business-critical. The assessment date is 2025-09-01. For Billing: The restore test completed on 2025-08-10, which is within the last 90 days from 2025-09-01 (83 days). The recovery time was 3 hours, which is less than or equal to 4 hours. For Inventory: The restore test completed on 2025-07-20, which is within the last 90 days from 2025-09-01 (45 days). The recovery time was exactly 4 hours, which is less than or equal to 4 hours. Both applications meet the condition. There are no explicit exceptions mentioned in the rule that would apply to either application. There are no conflicting observations regarding the restore tests or recovery times for either application.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 18.2s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. For Billing: The restore test completed on 2025-08-10, which is within the last 90 days from 2025-09-01 (83 days). The recovery time was 3 hours, which is less than or equal to 4 hours. For Inventory: The restore test completed on 2025-07-20, which is within the last 90 days from 2025-09-01 (45 days). The recovery time was exactly 4 hours, which is less than or equal to 4 hours. Both applications meet the condition. There are no explicit exceptions mentioned in the rule that would apply to either application.

### property_corroboration_not_two_events

**Expected:** One generator/test warrants one finding; either source independently supports it and both may be cited together.

**Model:** The subject is standby generator G-1 at Birch Cold Storage. The period in scope is August 2025. The evidence shows that generator G-1 successfully supplied full building load during its completed test on 2025-08-12, which falls within August 2025. Both E1 (contractor record) and E2 (engineer verification) confirm this event. There are no observations refuting the successful testing under full building load. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no actual incompatible observations. Both E1 and E2 corroborate the same test event without contradiction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 16.9s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The evidence shows that generator G-1 successfully supplied full building load during its completed test on 2025-08-12, which falls within August 2025. Both E1 (contractor record) and E2 (engineer verification) confirm this event. There are no observations refuting the successful testing under full building load. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### gl_sister_company_evidence

**Expected:** A sister company's recall is not evidence of the applicant's recall history; absence of applicant records is not proof of no recall.

**Model:** The criterion requires determining if Aspen Foods LLC had a product recall during 2025. Evidence E2 indicates that Aspen Beverage LLC (a separate sister company) recalled a beverage product in May 2025, but provides no recall history for Aspen Foods LLC. The applicant's own recall response remains unanswered. Since the recall is attributed to a different legal entity and there is no explicit record of a recall for Aspen Foods LLC, the condition cannot be confirmed as true based on available evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 16.7s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires determining if Aspen Foods LLC had a product recall during 2025. Evidence E2 indicates that Aspen Beverage LLC (a separate sister company) recalled a beverage product in May 2025, but provides no recall history for Aspen Foods LLC. The applicant's own recall response remains unanswered. Since the recall is attributed to a different legal entity and there is no explicit record of a recall for Aspen Foods LLC, the condition cannot be confirmed as true based on available evidence.

### cyber_prior_year_does_not_prove_current

**Expected:** A previous-year control assessment and unknown post-migration controls cannot establish the current-year requirement.

**Model:** The criterion requires that all business-critical systems had tested offline backups during calendar 2025. Evidence E1 confirms tested offline backups for all business-critical systems in calendar 2024, but does not cover 2025. Evidence E2 indicates that backup test records and offline-storage configuration for 2025 have not yet been supplied, and current effectiveness is unverified. Since there is no evidence of testing occurring in 2025, and the records required to prove such testing are not provided, it cannot be determined whether the condition was met.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 17.1s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that all business-critical systems had tested offline backups during calendar 2025. Evidence E1 confirms tested offline backups for all business-critical systems in calendar 2024, but does not cover 2025. Evidence E2 indicates that backup test records and offline-storage configuration for 2025 have not yet been supplied, and current effectiveness is unverified. Since there is no evidence of testing occurring in 2025, and the records required to prove such testing are not provided, it cannot be determined whether the condition was met.

### property_building_specific_scope

**Expected:** Building A fails the wood-frame applicability condition; Building B cannot make an A-specific rule applicable.

**Model:** The criterion explicitly restricts application to Building A. The subject of the evidence is Building A. The evidence states that 'Building A has a steel structural frame and concrete external walls' and 'the engineer confirms there is no combustible wood structural frame in Building A.' Since the criterion applies only if the building has a combustible wood structural frame, and Building A does not have such a frame, the condition for applying the criterion is not met. Therefore, the trigger is false. There are no explicit exception prerequisites mentioned in the rule text that would apply to this case. There is no actual incompatible observation. The evidence confirms that Building A does not have a combustible wood structural frame, which directly contradicts the condition required for the criterion to apply.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 2; model calls: 8; elapsed: 21.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion applies only to Building A, and the evidence confirms that Building A has a steel structural frame and concrete external walls, with no combustible wood structural frame. Since the condition for applying the criterion (combustible wood structural frame) is not met, the criterion does not apply to Building A.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that 'Building A has a steel structural frame and concrete external walls' and 'the engineer confirms there is no combustible wood structural frame in Building A.' Since the criterion applies only if the building has a combustible wood structural frame, and Building A does not have such a frame, the condition for applying the criterion is not met. Therefore, the trigger is false. There are no explicit exception prerequisites mentioned in the rule text that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### wc_partial_payroll_period

**Expected:** A 20% quarter does not establish the full-year rate when the remaining nine months are unknown.

**Model:** The rule applies to the insured's total overtime hours during the full 2025 calendar year. The subject is the insured, and the period in scope is the entire year 2025. The evidence shows 2,000 overtime hours in Q1 (January-March) out of 10,000 total hours worked. However, the full-year data is not provided. The April-December hours have not been supplied, and there is no indication that the first-quarter rate continued. Since the rule requires a full year's data to compute the percentage, and the denominator (total annual hours) cannot be determined from the available evidence, the condition cannot be evaluated. Therefore, it is unknown whether the overtime hours exceed 15% of all hours worked during 2025. There are no explicit exception prerequisites mentioned in the rule text for C1. There is no actual incompatible observation. The evidence does not contradict itself; it simply lacks complete data to evaluate the condition.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 5; elapsed: 17.2s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence shows 2,000 overtime hours in Q1 (January-March) out of 10,000 total hours worked. However, the full-year data is not provided. The April-December hours have not been supplied, and there is no indication that the first-quarter rate continued. Since the rule requires a full year's data to compute the percentage, and the denominator (total annual hours) cannot be determined from the available evidence, the condition cannot be evaluated. Therefore, it is unknown whether the overtime hours exceed 15% of all hours worked during 2025. There are no explicit exception prerequisites mentioned in the rule text for C1.

### gl_document_submission_condition

**Expected:** Confirmed nonsubmission disproves a submission-specific strength without assuming no agreements exist.

**Model:** The rule applies to the submission as a whole, evaluating whether signed hold-harmless agreements were supplied for all active subcontractors. The subject is the submission and its contents. The evidence (E1) states that 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly supports the trigger condition being false, as the requirement for supplying these documents was not met. The statement confirms that the required documents were absent from the submission. There are no explicit exception prerequisites mentioned in the rule text. The rule does not contain any conditional language such as 'unless' or 'except' that would create an applicable exception for this case. There are no conflicting observations in the provided evidence that would create an unresolved contradiction regarding whether signed hold-harmless agreements were supplied. The single statement from E1 clearly indicates absence of these documents.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 11.7s.

**Negative-evidence review (C1):** `supported`. The criterion requires that signed hold-harmless agreements be supplied with the submission for every active subcontractor. Evidence E1 explicitly states that 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly establishes that the documentation requirement was not met, as the agreements were not submitted.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence (E1) states that 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly supports the trigger condition being false, as the requirement for supplying these documents was not met. The statement confirms that the required documents were absent from the submission. There are no explicit exception prerequisites mentioned in the rule text. The rule does not contain any conditional language such as 'unless' or 'except' that would create an applicable exception for this case.

### wc_document_absence_is_concern

**Expected:** This criterion explicitly targets a missing submission document, so its confirmed absence supports a concern.

**Model:** The subject is Delta Fabrication, and the period in scope is the complete final submission as referenced in the evidence. The evidence states that 'the required current written lockout procedure was not supplied' in the complete final submission. This directly supports the trigger condition that the submission lacks the required document. The absence of the document is confirmed by the intake reviewer's check of the complete final submission. There are no explicit exception prerequisites mentioned in the rule text for C1, and no validity dates or conditions are provided that would apply to this case. There are no conflicting observations regarding the presence or absence of the required written lockout procedure in the submission. The evidence clearly states that it was not supplied, and there is no contradictory information provided.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 11.2s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The evidence states that 'the required current written lockout procedure was not supplied' in the complete final submission. This directly supports the trigger condition that the submission lacks the required document. The absence of the document is confirmed by the intake reviewer's check of the complete final submission. There are no explicit exception prerequisites mentioned in the rule text for C1, and no validity dates or conditions are provided that would apply to this case.

### wc_activity_explicitly_not_performed

**Expected:** The explicit delayed induction disproves the all-employees pre-operation requirement despite later completion.

**Model:** The criterion applies to newly hired production employees who operated production equipment in 2025. The evidence describes two such employees who operated equipment in 2025, so the scope is in_scope. The condition requires that every newly hired production employee received machine-safety induction before first operating production equipment in 2025. Evidence E1 states that two employees operated equipment on 2025-05-02 without receiving induction, which was completed later on 2025-05-08. This means the condition is not met for these employees. There are no explicit exceptions in the criterion text that would apply to this situation. There is no conflicting evidence provided; E1 directly contradicts the condition by stating that employees operated equipment without prior induction.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 7; elapsed: 20.5s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "every newly hired production employee received machine-safety induction before first operating production equipment in 2025", "scope_reason": "The rule applies to newly hired production employees who operated production equipment in 2025. The evidence E1 describes two such employees who first operated equipment on 2025-05-02 without receiving induction, which is within the scope of 2025.", "scope": "in_scope", "condition_reason": "The evidence shows that two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction. Although induction was completed on 2025-05-08, the employees operated equipment before receiving the required training. This directly contradicts the condition that all such employees received induction before first operating equipment.", "condition": "false", "exception_reason": "There are no explicit exception prerequisites mentioned in the rule text for C1.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "The evidence E1 directly contradicts the condition by stating that employees operated equipment before receiving induction. There is no conflicting evidence regarding the timing of the induction or operation.", "conflict": "none", "findings": [{"subject": "newly hired production employees who first operated production equipment on 2025-05-02", "evidence_ids": ["E1"], "reason": "Two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction, which violates the requirement that all such employees receive induction before operating equipment."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...operating equipment.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Negative-evidence review (C1):** `supported`. The criterion requires that a record exist showing every newly hired production employee received machine-safety induction before first operating production equipment in 2025. The evidence shows that two employees operated production equipment on 2025-05-02 without receiving the induction, and that the induction was subsequently completed on 2025-05-08. This demonstrates that the condition of receiving induction before operating equipment was not met for these employees, which is a decisive observation that contradicts the criterion's requirement.

### property_inspection_date_unknown

**Expected:** Without the last-completed date, the twelve-month condition is unknown.

**Model:** Subject is Fern Mill; period in scope is before 2025-09-01 The last completed electrical thermographic inspection date is unknown. E1 states that Fern Mill cannot locate the date of its last completed electrical thermographic inspection due to lost contractor records. E2 indicates that the survey did not include thermographic testing or verify the date of any earlier test. No supporting facts establish that the inspection was completed more than 12 months before 2025-09-01. Therefore, it cannot be confirmed that the condition is true. No explicit exception prerequisites are mentioned in the rule. There are no actual incompatible observations. Both E1 and E2 indicate a lack of information regarding the date of the last inspection, but they do not contradict each other.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 16.4s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The last completed electrical thermographic inspection date is unknown. E1 states that Fern Mill cannot locate the date of its last completed electrical thermographic inspection due to lost contractor records. E2 indicates that the survey did not include thermographic testing or verify the date of any earlier test. No supporting facts establish that the inspection was completed more than 12 months before 2025-09-01. Therefore, it cannot be confirmed that the condition is true. No explicit exception prerequisites are mentioned in the rule.

### property_cross_source_alarm_and_value

**Expected:** The value and whole-stock alarm condition require combining both sources into one strength.

**Model:** The subject is 'Haven Parts' and the period is as of 2025-09-01. The evidence batch covers the relevant time and subject. The total declared stock value is $425,000 (from E1), which is less than $500,000. The entire insured stock is in a continuously monitored intruder-alarm area (from E2). Both conditions of the trigger are met. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no conflicting observations regarding the declared stock value or the alarm system status.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 15.0s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The total declared stock value is $425,000 (from E1), which is less than $500,000. The entire insured stock is in a continuously monitored intruder-alarm area (from E2). Both conditions of the trigger are met. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### gl_loss_aggregation_without_duplicate

**Expected:** Distinct claims sum to $325,000, above $300,000. Do not add the repeated GL-101 again or create a finding per claim.

**Model:** The rule applies to 2025 general liability claims. Evidence E1 lists two distinct 2025 claims (GL-101 and GL-102), which are the only relevant claims in the batch. There are two distinct 2025 general liability claims: GL-101 with paid amount $150,000 and GL-102 with paid amount $175,000. Total paid amount = $150,000 + $175,000 = $325,000. Since $325,000 > $300,000, the condition is true. The rule does not specify any exceptions that would apply to this case. No exception prerequisites are mentioned or satisfied. There is no actual incompatible observation. E2 identifies a duplicate reference to GL-101 but does not contradict the paid amount or existence of the claim. The paid amounts in E1 are used as stated, and E2 confirms that GL-101 is not an additional claim.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 28.9s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000.", "scope_reason": "The rule applies to 2025 general liability claims. The evidence includes two 2025 claims (GL-101 and GL-102), which are within the scope of the rule.", "scope": "in_scope", "condition_reason": "There are two distinct 2025 general liability claims: GL-101 with a paid amount of $150,000 and GL-102 with a paid amount of $175,000. The total paid amount is $325,000 ($150,000 + $175,000). This exceeds the threshold of $300,000.", "condition": "true", "exception_reason": "There are no explicit exceptions in the rule text that apply to this case. The rule does not specify any conditions under which the threshold would not apply.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "There is a conflict between E1 and E2 regarding claim GL-101. E1 lists GL-101 with a paid amount of $150,000, while E2 states that the broker's note repeats GL-101 at the same latest paid amount of $150,000, indicating it is a duplicate reference and not an additional claim. However, since the rule requires counting each claim ID once using its latest stated paid amount, and both sources agree on the amount for GL-101, this does not change the total calculation.", "conflict": "unresolved", "findings": [{"subject": "2025 general liability claims", "evidence_ids": ["E1"], "reason": "The total paid amounts for distinct 2025 general liability claims (GL-101 at $150,000 and GL-102 at $175,000) exceed the threshold of $300,000. Therefore, one concern is flagged."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r... concern is flagged.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000.", "scope_reason": "The rule applies to 2025 general liability claims. The evidence includes two 2025 claims (GL-101 and GL-102), which are within the scope of the rule.", "scope": "in_scope", "condition_reason": "There are two distinct 2025 general liability claims: GL-101 with a paid amount of $150,000 and GL-102 with a paid amount of $175,000. The total paid amount is $325,000 ($1150,000 + $175,000). This exceeds the threshold of $300,000.", "condition": "true", "exception_reason": "There are no explicit exceptions in the rule text that apply to this case. The rule does not specify any conditions under which the threshold would not apply.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "There is a conflict between E1 and E2 regarding claim GL-101. E1 lists GL-101 with a paid amount of $150,000, while E2 states that the broker's note repeats GL-101 at the same latest paid amount of $150,000, indicating it is a duplicate reference and not an additional claim. However, since the rule requires counting each claim ID once using its latest stated paid amount, and both sources agree on the amount for GL-101, this does not change the total calculation.", "conflict": "unresolved", "findings": [{"subject": "2025 general liability claims", "evidence_ids": ["E1"], "reason": "The total paid amounts for distinct 2025 general liability claims (GL-101 at $150,000 and GL-102 at $175,000) exceed the threshold of $300,000. Therefore, one concern is flagged."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r... concern is flagged.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. There are two distinct 2025 general liability claims: GL-101 with paid amount $150,000 and GL-102 with paid amount $175,000. Total paid amount = $150,000 + $175,000 = $325,000. Since $325,000 > $300,000, the condition is true. The rule does not specify any exceptions that would apply to this case. No exception prerequisites are mentioned or satisfied.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_restore_duration_cross_midnight

**Expected:** Elapsed time is 25.5 hours, exceeding the 24-hour maximum despite a successful eventual restore.

**Model:** The subject is the full restore of the payroll application, and the period in scope is from 2025-08-01 08:00 UTC to 2025-08-02 09:30 UTC. The restore started at 2025-08-01 08:00 UTC and completed at 2025-08-02 09:30 UTC. Elapsed time = 25 hours and 30 minutes. Since 25 hours 30 minutes > 24 hours, the condition is false. The rule does not specify any exceptions that would apply to this case. There are no conflicting observations in the evidence provided.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 20.3s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion requires recording a strength if the completed full restore took no longer than 24 hours. The evidence provides start and completion timestamps that allow calculation of elapsed time. The condition can be evaluated as true or false based on these timestamps, so a negative decision is possible only if the elapsed time exceeds 24 hours.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The restore started at 2025-08-01 08:00 UTC and completed at 2025-08-02 09:30 UTC. Elapsed time = 25 hours and 30 minutes. Since 25 hours 30 minutes > 24 hours, the condition is false. The rule does not specify any exceptions that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_expired_exception_certificate

**Expected:** The height trigger is met and the explicit approval exception is unavailable on the assessment date.

**Model:** The subject is the storage area at Linden Distribution, and the period in scope is 2025-09-01, which matches the date of the survey. On 2025-09-01, combustible packaged stock was stacked to 5.2 metres at Linden Distribution. This exceeds the 4-metre threshold. The engineer's high-stack approval allowed stacks up to 5.5 metres but expired on 2025-06-30. No renewal or extension was issued before 2025-09-01. Therefore, the approval is not valid on 2025-09-01. The condition is true because the stack height exceeds 4 metres and the exception does not apply. The engineer's high-stack approval for Linden's storage area expired on 2025-06-30, and no renewal or extension was issued before 2025-09-01. The exception prerequisite (valid approval) is not met. There are no actual incompatible observations. E1 reports the stack height as 5.2 metres, and E2 confirms that the approval expired on 2025-06-30 with no renewal before 2025-09-01. These facts support the trigger condition rather than contradicting it.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 20.0s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. On 2025-09-01, combustible packaged stock was stacked to 5.2 metres at Linden Distribution. This exceeds the 4-metre threshold. The engineer's high-stack approval allowed stacks up to 5.5 metres but expired on 2025-06-30. No renewal or extension was issued before 2025-09-01. Therefore, the approval is not valid on 2025-09-01. The condition is true because the stack height exceeds 4 metres and the exception does not apply. The engineer's high-stack approval for Linden's storage area expired on 2025-06-30, and no renewal or extension was issued before 2025-09-01. The exception prerequisite (valid approval) is not met.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
