# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T06:07:50.137711+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **22/32** (planned: 32).
- Correct case statuses: **30/32**.
- Required gold evidence cited: **35/35**.
- Reference/provenance checks: **145/145**.
- False-positive findings in the 20 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| cyber_remote_access_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_pump_service_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_driver_screening_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| gl_subcontract_limit_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_incident_rate_calculation | matched | matched | 1 / 1 | 2 / 2 | FAIL |
| property_reserves_exact_threshold | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_roof_exact_boundary | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| cyber_patch_coverage_boundary | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_alarm_equal_reports | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| cyber_backup_immutability_conflict | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| auto_mileage_corrected_denominator | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| property_later_repair_does_not_rewrite_history | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_electrical_exception | no_match | no_match | 0 / 0 | 2 / 2 | PASS |
| cyber_service_account_exception | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
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
| gl_document_submission_condition | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| wc_document_absence_is_concern | matched | no_match | 0 / 1 | 1 / 1 | FAIL |
| wc_activity_explicitly_not_performed | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| property_inspection_date_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_cross_source_alarm_and_value | matched | matched | 1 / 1 | 2 / 2 | FAIL |
| gl_loss_aggregation_without_duplicate | matched | matched | 1 / 1 | 1 / 1 | FAIL |
| cyber_restore_duration_cross_midnight | no_match | no_match | 0 / 0 | 2 / 2 | FAIL |
| property_expired_exception_certificate | matched | matched | 1 / 1 | 2 / 2 | PASS |

## Reasons and diagnostics

### cyber_remote_access_unknown

**Expected:** Administrator MFA does not establish workforce MFA; blank or unavailable records do not prove absence of the control.

**Model:** The criterion requires that MFA protects every remote workforce login to Harbor Analytics as of 2025-09-01. Evidence E1 indicates that MFA is enabled for all four cloud administrators but does not confirm whether all remote workforce logins are protected. Evidence E2 states that the VPN configuration report was not available and the broker did not verify the remote-login configuration, leaving uncertainty about whether all remote workforce logins are protected by MFA. Since there is insufficient evidence to confirm that every remote workforce login is protected by MFA, the condition cannot be definitively evaluated.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 18.8s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that MFA protects every remote workforce login to Harbor Analytics as of 2025-09-01. Evidence E1 indicates that MFA is enabled for all four cloud administrators but does not confirm whether all remote workforce logins are protected. Evidence E2 states that the VPN configuration report was not available and the broker did not verify the remote-login configuration, leaving uncertainty about whether all remote workforce logins are protected by MFA. Since there is insufficient evidence to confirm that every remote workforce login is protected by MFA, the condition cannot be definitively evaluated.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_pump_service_unknown

**Expected:** Unlocated records and a visual inspection cannot establish a missed service visit.

**Model:** The criterion requires determining whether the fire pump at Cedar Components was not serviced during calendar 2025. Evidence E1 shows the pump appears clean with no visible leaks and its gauge is in normal band, but this visual inspection does not establish whether servicing occurred in 2025. Evidence E2 indicates that the pump contractor's 2025 service invoice cannot be located, and the contractor's archive is still being checked, without confirming whether the visit took place. There is no direct evidence that the pump was not serviced in 2025, nor is there explicit confirmation of servicing. The lack of documentation and inability to confirm the service event leaves the condition unknown.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 17.8s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires determining whether the fire pump at Cedar Components was not serviced during calendar 2025. Evidence E1 shows the pump appears clean with no visible leaks and its gauge is in normal band, but this visual inspection does not establish whether servicing occurred in 2025. Evidence E2 indicates that the pump contractor's 2025 service invoice cannot be located, and the contractor's archive is still being checked, without confirming whether the visit took place. There is no direct evidence that the pump was not serviced in 2025, nor is there explicit confirmation of servicing. The lack of documentation and inability to confirm the service event leaves the condition unknown.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_driver_screening_unknown

**Expected:** Neither the interview process nor missing files establishes whether all MVR reviews occurred.

**Model:** The criterion requires that motor vehicle records be reviewed for every employed driver before hire. While E1 indicates that hiring includes an interview and a route test, it does not confirm whether MVR reviews were conducted. E2 states that driver files have not been provided and there is no confirmation of pre-hire MVR reviews. Since the specific information about whether MVR reviews occurred for all drivers is missing, we cannot definitively conclude that the condition was met.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 6; elapsed: 17.6s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that motor vehicle records be reviewed for every employed driver before hire. While E1 indicates that hiring includes an interview and a route test, it does not confirm whether MVR reviews were conducted. E2 states that driver files have not been provided and there is no confirmation of pre-hire MVR reviews. Since the specific information about whether MVR reviews occurred for all drivers is missing, we cannot definitively conclude that the condition was met.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_subcontract_limit_unknown

**Expected:** Unspecified insurance limits cannot satisfy or disprove the $2 million requirement.

**Model:** The rule applies to every active roofing subcontractor. The subject is the two active roofing subcontractors identified: North Roof and Ridge Team. The evidence shows that both subcontractors are marked as insured in the vendor register (E1), but no general liability limits or policy numbers are recorded. Certificates have been requested but not received (E2). There is no confirmation of the limits. Therefore, it cannot be determined whether the limits meet or exceed $2 million. The lack of documented limits means the supporting facts are absent. There are no explicit exception prerequisites listed in the rule that would apply to this case. There is no actual incompatible observation. The evidence does not confirm or deny the limits, but there are no contradictory facts regarding the subcontractors' status or limits.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 15.4s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence shows that both subcontractors are marked as insured in the vendor register (E1), but no general liability limits or policy numbers are recorded. Certificates have been requested but not received (E2). There is no confirmation of the limits. Therefore, it cannot be determined whether the limits meet or exceed $2 million. The lack of documented limits means the supporting facts are absent. There are no explicit exception prerequisites listed in the rule that would apply to this case.

### auto_incident_rate_calculation

**Expected:** Three divided by 24 times 100 is 12.5, above 10. This is one aggregate finding, not three separate collision findings.

**Model:** The rule applies to the fleet level for the year 2025. The subject is Summit Couriers, which is a single fleet entity. The time period in scope is 2025. The preventable collision count for 2025 is 3 (from E1). The active fleet count is 24 (from E2). The frequency is calculated as (3 collisions / 24 vehicles) * 100 = 12.5 collisions per 100 vehicles. This exceeds the threshold of 10 collisions per 100 active vehicles. Therefore, the condition is true. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not contain any 'unless' or 'except' clauses that would apply to this case. There are no conflicting observations in the evidence that would create an unresolved contradiction regarding the preventable collision count or the active fleet count. All data points support the calculation of the frequency.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 5; elapsed: 16.5s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The preventable collision count for 2025 is 3 (from E1). The active fleet count is 24 (from E2). The frequency is calculated as (3 collisions / 24 vehicles) * 100 = 12.5 collisions per 100 vehicles. This exceeds the threshold of 10 collisions per 100 active vehicles. Therefore, the condition is true. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not contain any 'unless' or 'except' clauses that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_reserves_exact_threshold

**Expected:** 480,000 / 120,000 equals exactly four months; at least includes equality.

**Model:** The rule applies to Bay Storage as the subject, with scope covering the period as of 2025-08-31. The evidence shows that as of 2025-08-31, Bay Storage has unrestricted cash of $480,000 and monthly operating expense of $120,000. The ratio of cash to monthly expenses is $480,000 / $120,000 = 4 months. This meets the requirement of at least four months of operating expense coverage. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case. There are no conflicting observations in the provided evidence that would create an unresolved contradiction regarding the cash reserves or operating expenses of Bay Storage.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 15.1s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The evidence shows that as of 2025-08-31, Bay Storage has unrestricted cash of $480,000 and monthly operating expense of $120,000. The ratio of cash to monthly expenses is $480,000 / $120,000 = 4 months. This meets the requirement of at least four months of operating expense coverage. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case.

### property_roof_exact_boundary

**Expected:** Exactly 20 does not exceed a strictly greater-than-20 threshold.

**Model:** The rule concerns the roof at Unit 7, and the assessment date is 2025-07-01. The evidence is about Unit 7's roof. The roof was installed on 2005-07-01. The assessment date is 2025-07-01. The age of the roof is exactly 20 years (2025-07-01 - 2005-07-01 = 20 years). The rule requires the roof to be strictly older than 20 years, which means it must be more than 20 years. Since the age is exactly 20 years, it does not meet the condition of being strictly older than 20 years. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule. There are no conflicting observations in the evidence provided. The roof installation date and assessment date are clearly stated, and there is no contradiction in the information given.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 15.3s.

**Negative-evidence review (C1):** `supported`. The evidence indicates that Unit 7's roof was installed on 2005-07-01, and the assessment date is 2025-07-01, resulting in an exact age of 20 years. The criterion requires the roof to be 'strictly older than 20 years,' which means the condition is not met because the age is exactly 20 years, not older. This is a direct contradiction to the criterion's requirement.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The roof was installed on 2005-07-01. The assessment date is 2025-07-01. The age of the roof is exactly 20 years (2025-07-01 - 2005-07-01 = 20 years). The rule requires the roof to be strictly older than 20 years, which means it must be more than 20 years. Since the age is exactly 20 years, it does not meet the condition of being strictly older than 20 years. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule.

### cyber_patch_coverage_boundary

**Expected:** 95/100 equals 95%, meeting an inclusive threshold despite five exceptions.

**Model:** The rule applies to 100 in-scope servers, and the evidence covers exactly these 100 servers. Of the 100 in-scope servers, 95 met the 14-day critical-patch deadline. This is 95/100 = 95%. Since 95% equals the threshold of 95%, the condition is satisfied. There are no explicit exceptions mentioned in the rule text. No conflicting observations are present. All data points support that 95 out of 100 servers met the deadline, with no contradictory records.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 17.1s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Of the 100 in-scope servers, 95 met the 14-day critical-patch deadline. This is 95/100 = 95%. Since 95% equals the threshold of 95%, the condition is satisfied. There are no explicit exceptions mentioned in the rule text.

### property_alarm_equal_reports

**Expected:** Equal-authority incompatible observations of the same state require abstention and both citations.

**Model:** The subject is 'monitored fire alarm at Orchard Packaging' and the period in scope is '10:00 on 2025-06-12'. The payload scope covers this time and location, so the scope is in_scope. Observation E1 states that the central monitoring status was OFFLINE at 10:00 on 2025-06-12 for Orchard Packaging (OP-11). Observation E2 states the opposite, that it was ONLINE at the same time. There are no other observations supporting or refuting the trigger directly. The condition is true based on E1's report but contradicted by E2. Since both providers have equal authority and no correction is documented, the actual status cannot be confirmed from available evidence. There are no explicit exception prerequisites mentioned in the rule text for C1. There is an actual incompatible observation: E1 reports the alarm was OFFLINE at 10:00 on 2025-06-12, while E2 reports it was ONLINE at the same time and location. These observations contradict each other regarding the status of the monitored fire alarm at Orchard Packaging.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 29.8s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if the monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12.", "scope_reason": "The scope is in_scope because the evidence directly references 'Orchard Packaging, account OP-11' which matches the subject specified in the criterion.", "scope": "in_scope", "condition_reason": "The condition is TRUE because the evidence states that 'central monitoring status was OFFLINE at 10:00 on 2025-06-12' for Orchard Packaging, which directly satisfies the trigger clause of the criterion. The evidence E1 from Provider A confirms this condition.", "condition": "true", "exception_reason": "There are no explicit exceptions mentioned in the criterion text that would apply to this case; therefore, the exception status is does_not_apply.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There is a conflict between the evidence provided by Provider A (which indicates the alarm was offline) and Provider B (which states it was online). However, since Provider B's evidence directly contradicts the condition and no further clarification is given, this conflict is unresolved. Despite the conflict, the condition remains true based on the evidence that supports it.", "conflict": "unresolved", "findings": [{"subject": "Orchard Packaging", "evidence_ids": ["E1"], "reason": "The monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12, as confirmed by the evidence E1 which states 'central monitoring status was OFFLINE at 10:00 on 2025-06-12.' This directly meets the condition specified in criterion C1."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...ied in criterion C1.")]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. Observation E1 states that the central monitoring status was OFFLINE at 10:00 on 2025-06-12 for Orchard Packaging (OP-11). Observation E2 states the opposite, that it was ONLINE at the same time. There are no other observations supporting or refuting the trigger directly. The condition is true based on E1's report but contradicted by E2. Since both providers have equal authority and no correction is documented, the actual status cannot be confirmed from available evidence. There are no explicit exception prerequisites mentioned in the rule text for C1.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_backup_immutability_conflict

**Expected:** Contradictory same-period attestations cannot be resolved by source votes or department titles.

**Model:** The subject is 'production backup vault' and the period is '2025-08-31'. The evidence batch covers this time and subject. E1 states that 'production vault PV-3 had immutable retention enabled throughout 2025-08-31', which supports the trigger. E2 states that 'immutable retention on production vault PV-3 was disabled throughout 2025-08-31', which refutes the trigger. There is a direct contradiction between these two attestations regarding the same vault and date. There are no explicit exception prerequisites mentioned in the rule. E1 and E2 present contradictory observations about the state of immutable retention on production vault PV-3 on 2025-08-31. E1 says it was enabled, while E2 says it was disabled. These are incompatible facts concerning the same subject and time.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 1; model calls: 6; elapsed: 22.6s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. E1 states that 'production vault PV-3 had immutable retention enabled throughout 2025-08-31', which supports the trigger. E2 states that 'immutable retention on production vault PV-3 was disabled throughout 2025-08-31', which refutes the trigger. There is a direct contradiction between these two attestations regarding the same vault and date. There are no explicit exception prerequisites mentioned in the rule.

### auto_mileage_corrected_denominator

**Expected:** Three per two million equals 1.5 per million, below two; the explicit correction controls the denominator.

**Model:** The rule applies to Northline's 2025 preventable collision rate, and the evidence covers the 2025 calendar year. The evidence shows three preventable collisions occurred in 2025. The final corrected mileage is 2,000,000 miles (from E3). The rate is calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This is less than the threshold of 2 per million miles. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no conflicting observations regarding the mileage or collision count for Northline in 2025. The corrected mileage supersedes the original, but does not change the number of collisions.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 1; model calls: 8; elapsed: 31.6s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E3']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion requires determining whether Northline's 2025 preventable collision rate exceeds two per million miles. Using the final corrected mileage of 2,000,000 miles (from E3) and three preventable collisions (from E1), the rate is 1.5 per million miles, which does not exceed the threshold of two per million miles. This conclusion is supported by the explicit evidence of the corrected mileage and collision count.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence shows three preventable collisions occurred in 2025. The final corrected mileage is 2,000,000 miles (from E3). The rate is calculated as 3 collisions / 2,000,000 miles = 0.0000015 collisions per mile, or 1.5 per million miles. This is less than the threshold of 2 per million miles. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_later_repair_does_not_rewrite_history

**Expected:** The historical impairment remains a concern; a later repair is a state change, not a correction.

**Model:** The subject is Cedar Depot, and the period in scope is the historical assessment date 2025-03-01. The inspection evidence (E1) states that on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired. This directly supports the trigger condition that the sprinkler system was impaired on the historical assessment date. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There is no conflicting evidence regarding the impairment of the sprinkler system on 2025-03-01. The repair documented in E2 occurred after the assessment date and does not alter the historical condition.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 22.2s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The inspection evidence (E1) states that on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired. This directly supports the trigger condition that the sprinkler system was impaired on the historical assessment date. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### property_electrical_exception

**Expected:** The age trigger applies but the documented complete replacement establishes the explicit exception.

**Model:** The building was constructed in 1952, which is before 1960. The subject is the insured building at Willow Print. The building was constructed in 1952, which satisfies the 'before 1960' condition. A licensed electrical contractor documented complete replacement of all original electrical wiring in 2018, which is after 2010. Therefore, the exception condition is met and the trigger does not hold. The rule requires that a licensed contractor documents complete replacement of original electrical wiring after 2010. Evidence E2 shows that a licensed electrical contractor certified that all original electrical wiring was removed and replaced in 2018, which satisfies this exception prerequisite. The exception applies. There are no conflicting observations regarding the building's construction date or the wiring replacement documentation. The evidence supports that the building was constructed before 1960 and that complete replacement occurred after 2010.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 1; model calls: 7; elapsed: 27.5s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion requires a licensed contractor to document complete replacement of original electrical wiring after 2010. Evidence E2 shows that a licensed electrical contractor certified that all original electrical wiring was removed and replaced in 2018, which satisfies the documentation requirement for complete replacement after 2010.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `applies`. The building was constructed in 1952, which satisfies the 'before 1960' condition. A licensed electrical contractor documented complete replacement of all original electrical wiring in 2018, which is after 2010. Therefore, the exception condition is met and the trigger does not hold. The rule requires that a licensed contractor documents complete replacement of original electrical wiring after 2010. Evidence E2 shows that a licensed electrical contractor certified that all original electrical wiring was removed and replaced in 2018, which satisfies this exception prerequisite. The exception applies.

### cyber_service_account_exception

**Expected:** Both exception requirements are established, so lack of MFA does not trigger the concern for this account.

**Model:** The subject is 'invoice-sync' which is identified as a noninteractive integration account. The review scope is 'Assess only invoice-sync.' The account 'invoice-sync' lacks MFA, as stated in E1. It is a noninteractive service account with interactive login disabled (E1). The credential rotation interval is documented as 14 days (E2), which is less than or equal to 30 days. These observations support the trigger condition for flagging a concern. The exception applies because 'invoice-sync' is a noninteractive service account with interactive login disabled and has a documented credential rotation interval of 14 days, which is no longer than 30 days. All prerequisites for the exception are met. There are no actual incompatible observations. The evidence supports that the account is noninteractive, login is disabled, and rotation interval is within the limit. No contradictions exist.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 1; captured call errors: 4; model calls: 9; elapsed: 28.4s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern for an account without MFA", "scope_reason": "scope is in_scope because the evidence concerns the 'invoice-sync' account, which is within the specified identity:account scope.", "scope": "in_scope", "condition_reason": "The condition is true because the 'invoice-sync' account lacks MFA. The evidence explicitly states that this account does not have MFA enabled.", "condition": "true", "exception_reason": "The exception does not apply because although the account is noninteractive and has interactive login disabled, there is no documented credential rotation interval provided in the evidence to confirm it meets the 'no longer than 30 days' requirement.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "conflict is unresolved because while the evidence confirms the account lacks MFA and is noninteractive with disabled interactive login, it does not provide information about credential rotation interval to verify if the exception criteria are met.", "conflict": "unresolved", "findings": [{"subject": "invoice-sync", "evidence_ids": ["E1"], "reason": "The account lacks MFA and does not meet the documented credential rotation interval exception, thus triggering the concern."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...ggering the concern.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; Scope/exception quotations must occur in criterion.text or its same-source context

**Negative-evidence review (C1):** `supported`. The account invoice-sync lacks MFA, but it qualifies as an exception under the criterion. It is a noninteractive service account with interactive login disabled, and it has documented credential rotation at intervals no longer than 30 days (14 days in this case). The criterion explicitly allows for such accounts to not trigger a concern when they meet these specific conditions.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `applies`. The account 'invoice-sync' lacks MFA, as stated in E1. It is a noninteractive service account with interactive login disabled (E1). The credential rotation interval is documented as 14 days (E2), which is less than or equal to 30 days. These observations support the trigger condition for flagging a concern. The exception applies because 'invoice-sync' is a noninteractive service account with interactive login disabled and has a documented credential rotation interval of 14 days, which is no longer than 30 days. All prerequisites for the exception are met.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_hot_work_scope_exclusion

**Expected:** The explicit operational scope excludes this applicant; a missing permit manual is irrelevant.

**Model:** The criterion applies to contractors performing on-site welding or flame cutting at customers' premises. The subject, Pine Design, is described as providing remote CAD drafting only and does not perform fabrication, installation, welding, flame cutting, or physical work at customer sites. The evidence shows that Pine Design performs remote CAD drafting only and does not engage in on-site welding or flame cutting activities. There is no indication that Pine Design performs any physical work at customer sites. Therefore, the subject does not meet the trigger condition of performing on-site welding or flame cutting. The rule does not contain explicit exception prerequisites. The scope restriction excludes Pine Design based on its operational description, but this is a matter of applicability rather than an exception that would apply to this specific case. There are no conflicting observations regarding Pine Design's activities. The evidence clearly states that Pine Design does not perform on-site work, which is consistent with the criterion's scope restriction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 10.4s.

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The evidence shows that Pine Design performs remote CAD drafting only and does not engage in on-site welding or flame cutting activities. There is no indication that Pine Design performs any physical work at customer sites. Therefore, the subject does not meet the trigger condition of performing on-site welding or flame cutting. The rule does not contain explicit exception prerequisites. The scope restriction excludes Pine Design based on its operational description, but this is a matter of applicability rather than an exception that would apply to this specific case.

### auto_passenger_scope_exclusion

**Expected:** Freight-only operations are outside the explicit passengers-for-hire scope.

**Model:** The rule applies to vehicles carrying passengers for hire. The evidence shows Granite Freight operates five box trucks carrying packaged commercial goods and does not transport passengers for hire. The rule's trigger requires that emergency evacuation training is not completed annually. However, since Granite Freight does not operate vehicles carrying passengers for hire, the condition is not applicable to this subject. There is no evidence of emergency evacuation training for any vehicles in this fleet. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no conflicting observations regarding emergency evacuation training for vehicles carrying passengers for hire. The evidence clearly states that Granite Freight does not transport passengers for hire, which means the rule's scope does not apply to this subject.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 9.7s.

**Independent review (C1):** scope `out_of_scope`, condition `false`, exception `does_not_apply`. The rule's trigger requires that emergency evacuation training is not completed annually. However, since Granite Freight does not operate vehicles carrying passengers for hire, the condition is not applicable to this subject. There is no evidence of emergency evacuation training for any vehicles in this fleet. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### property_multiple_warehouse_concerns

**Expected:** East and West qualify independently; extinguishers and future plans do not satisfy the condition, and the office is excluded.

**Model:** The subject is an occupied storage warehouse. The period in scope is the current condition as described in the evidence. The evidence describes two warehouses (East and West) that are storage warehouses, occupied daily and lacking automatic sprinklers, respectively. The office-only building (E3) is outside this criterion. The East Warehouse (E1) is an occupied storage warehouse lacking automatic sprinklers. The West Warehouse (E2) is also an occupied storage warehouse lacking automatic sprinklers. Both meet the trigger condition of being occupied storage warehouses without automatic sprinklers. Office-only buildings are excluded per the criterion. There are no explicit exceptions mentioned in the rule that would apply to these cases. No conflicting observations were found. Both warehouses are clearly identified as occupied storage facilities without automatic sprinklers, and the office-only building (E3) is explicitly excluded from this criterion.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 34.1s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The East Warehouse (E1) is an occupied storage warehouse lacking automatic sprinklers. The West Warehouse (E2) is also an occupied storage warehouse lacking automatic sprinklers. Both meet the trigger condition of being occupied storage warehouses without automatic sprinklers. Office-only buildings are excluded per the criterion. There are no explicit exceptions mentioned in the rule that would apply to these cases.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### auto_multiple_expired_licences

**Expected:** Two independently identified employees meet the concern; Driver C does not.

**Model:** The rule applies to currently employed drivers with licences expiring before 2025-09-01 and not renewed by that date. Driver A and Driver B are currently employed and had licences expire before 2025-09-01; Driver C is employed but has a valid licence. Driver A is currently employed, and their licence expired on 2025-07-31, which is before 2025-09-01. The licensing check confirms the licence remained unrenewed as of 2025-09-01. Driver B is currently employed, and their licence expired on 2025-08-15, also before 2025-09-01. The licensing check confirms no renewal as of 2025-09-01. These observations support the trigger condition. There are no explicit exceptions mentioned in the rule that would apply to either Driver A or Driver B. There are no conflicting observations regarding the employment status or licence expiration dates of Driver A or Driver B. The evidence supports that both drivers meet the criteria for a concern.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 43.4s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. Driver A is currently employed, and their licence expired on 2025-07-31, which is before 2025-09-01. The licensing check confirms the licence remained unrenewed as of 2025-09-01. Driver B is currently employed, and their licence expired on 2025-08-15, also before 2025-09-01. The licensing check confirms no renewal as of 2025-09-01. These observations support the trigger condition. There are no explicit exceptions mentioned in the rule that would apply to either Driver A or Driver B.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_multiple_restore_strengths

**Expected:** Each application independently meets both timing conditions and warrants its own strength.

**Model:** The rule applies to business-critical applications. Both Billing and Inventory are designated as business-critical. The assessment date is 2025-09-01. For Billing: The restore test completed on 2025-08-10, which is within the last 90 days from 2025-09-01 (83 days). The recovery time was 3 hours, which is no longer than four hours. For Inventory: The restore test completed on 2025-07-20, which is within the last 90 days from 2025-09-01 (45 days). The recovery time was exactly 4 hours, which meets the 'no longer than four hours' requirement. Both applications satisfy the condition. There are no explicit exceptions mentioned in the rule that would apply to either application. There are no conflicting observations regarding the restore tests or recovery times for either application.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 1; model calls: 6; elapsed: 32.7s.

**Rejected responses:** Unrequested or duplicate criterion ID: C1

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. For Billing: The restore test completed on 2025-08-10, which is within the last 90 days from 2025-09-01 (83 days). The recovery time was 3 hours, which is no longer than four hours. For Inventory: The restore test completed on 2025-07-20, which is within the last 90 days from 2025-09-01 (45 days). The recovery time was exactly 4 hours, which meets the 'no longer than four hours' requirement. Both applications satisfy the condition. There are no explicit exceptions mentioned in the rule that would apply to either application.

### property_corroboration_not_two_events

**Expected:** One generator/test warrants one finding; either source independently supports it and both may be cited together.

**Model:** The rule applies to standby generators tested under full building load during August 2025. The subject is generator G-1 at Birch Cold Storage, which was tested during August 2025. The evidence shows that generator G-1 was successfully tested under full building load on 2025-08-12, which falls within August 2025. Both E1 (contractor record) and E2 (engineer verification) confirm this test occurred during the specified period and met the required conditions. There are no contradictory observations regarding the test date or load condition. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. The rule does not contain any 'unless' or 'except' clauses, so no exceptions are specified. There are no conflicting observations regarding the test date, load condition, or generator involved. Both E1 and E2 corroborate the same event with consistent details.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 22.0s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The evidence shows that generator G-1 was successfully tested under full building load on 2025-08-12, which falls within August 2025. Both E1 (contractor record) and E2 (engineer verification) confirm this test occurred during the specified period and met the required conditions. There are no contradictory observations regarding the test date or load condition. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. The rule does not contain any 'unless' or 'except' clauses, so no exceptions are specified.

### gl_sister_company_evidence

**Expected:** A sister company's recall is not evidence of the applicant's recall history; absence of applicant records is not proof of no recall.

**Model:** The criterion requires determining if Aspen Foods LLC had a product recall during 2025. Evidence E2 indicates that Aspen Beverage LLC (a separate sister company) recalled a beverage product in May 2025, but provides no recall history for Aspen Foods LLC. The applicant's own recall response remains unanswered. While the recall involved a sister company, the evidence does not establish whether Aspen Foods LLC had any recall during 2025. Since there is no direct evidence of a recall by Aspen Foods LLC and the applicant did not provide a response, it cannot be confirmed that the condition is false.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 1; model calls: 7; elapsed: 27.1s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires determining if Aspen Foods LLC had a product recall during 2025. Evidence E2 indicates that Aspen Beverage LLC (a separate sister company) recalled a beverage product in May 2025, but provides no recall history for Aspen Foods LLC. The applicant's own recall response remains unanswered. While the recall involved a sister company, the evidence does not establish whether Aspen Foods LLC had any recall during 2025. Since there is no direct evidence of a recall by Aspen Foods LLC and the applicant did not provide a response, it cannot be confirmed that the condition is false.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_prior_year_does_not_prove_current

**Expected:** A previous-year control assessment and unknown post-migration controls cannot establish the current-year requirement.

**Model:** The criterion requires testing of offline backups for all business-critical systems during calendar 2025. Evidence E1 only covers testing in 2024, and E2 indicates that backup test records and offline-storage configuration for 2025 have not yet been supplied. Since there is no evidence confirming that all business-critical systems had tested offline backups during 2025, the condition cannot be verified as true.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 28.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires testing of offline backups for all business-critical systems during calendar 2025. Evidence E1 only covers testing in 2024, and E2 indicates that backup test records and offline-storage configuration for 2025 have not yet been supplied. Since there is no evidence confirming that all business-critical systems had tested offline backups during 2025, the condition cannot be verified as true.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_building_specific_scope

**Expected:** Building A fails the wood-frame applicability condition; Building B cannot make an A-specific rule applicable.

**Model:** The criterion explicitly restricts application to Building A only, as stated in the context of evidence E1. Evidence E1 states that 'Building A has a steel structural frame and concrete external walls' and 'the engineer confirms there is no combustible wood structural frame in Building A.' Since the criterion requires a combustible wood structural frame to apply, and Building A's frame is steel, the condition is not met. The fact that Building A lacks automatic sprinklers does not trigger the concern because the primary condition (combustible wood frame) is not satisfied. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations regarding Building A's structural frame or sprinkler status in the provided evidence. The evidence clearly states that Building A has a steel frame and no sprinklers, which does not meet the condition for triggering the concern.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 8; elapsed: 28.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

**Negative-evidence review (C1):** `supported`. The criterion applies specifically to Building A and requires that if its structural frame is combustible wood, then automatic sprinklers must be present. Evidence E1 explicitly states that Building A has a steel structural frame and concrete external walls, and that the engineer confirms there is no combustible wood structural frame in Building A. Since Building A does not have a combustible wood structural frame, the condition for applying the criterion is not met, and therefore no concern should be flagged.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Evidence E1 states that 'Building A has a steel structural frame and concrete external walls' and 'the engineer confirms there is no combustible wood structural frame in Building A.' Since the criterion requires a combustible wood structural frame to apply, and Building A's frame is steel, the condition is not met. The fact that Building A lacks automatic sprinklers does not trigger the concern because the primary condition (combustible wood frame) is not satisfied. There are no explicit exception prerequisites mentioned in the rule text for C1.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### wc_partial_payroll_period

**Expected:** A 20% quarter does not establish the full-year rate when the remaining nine months are unknown.

**Model:** The rule applies to the full 2025 calendar year. The subject is the insured's total overtime hours versus total hours worked in 2025. The evidence shows 2,000 overtime hours and 10,000 total hours for Q1 2025. However, the full-year data is missing. The April-December 2025 hours have not been supplied (E2). The rule requires annual figures, but only quarterly data is provided. The numerator and denominator cannot be computed for the full year. Therefore, the condition cannot be evaluated as true or false based on available evidence. There are no explicit exception prerequisites mentioned in the rule text. No conflicting observations are present. The evidence does not contain contradictory data about overtime or total hours worked. There is no unresolved conflict between the two pieces of evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 7; elapsed: 28.1s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence shows 2,000 overtime hours and 10,000 total hours for Q1 2025. However, the full-year data is missing. The April-December 2025 hours have not been supplied (E2). The rule requires annual figures, but only quarterly data is provided. The numerator and denominator cannot be computed for the full year. Therefore, the condition cannot be evaluated as true or false based on available evidence. There are no explicit exception prerequisites mentioned in the rule text.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_document_submission_condition

**Expected:** Confirmed nonsubmission disproves a submission-specific strength without assuming no agreements exist.

**Model:** The rule applies to the submission as a whole, evaluating whether all required documents were provided. The evidence batch covers the entire submission inventory. The evidence (E1) states that 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly supports the trigger condition being false, as the required documents were not submitted. The statement confirms the absence of the required documentation. The rule does not contain explicit exception prerequisites or validity dates that would apply to this case. There are no conflicting observations regarding the submission of signed hold-harmless agreements. The single evidence item E1 clearly states that no such agreements were supplied for any subcontractor.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 12.6s.

**Negative-evidence review (C1):** `supported`. The evidence directly states that no signed hold-harmless agreements were supplied for any of the three active subcontractors. This explicit statement establishes that the documentation requirement was not met, which supports a negative decision for the criterion.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence (E1) states that 'no signed hold-harmless agreements were supplied for any of the three active subcontractors.' This directly supports the trigger condition being false, as the required documents were not submitted. The statement confirms the absence of the required documentation. The rule does not contain explicit exception prerequisites or validity dates that would apply to this case.

### wc_document_absence_is_concern

**Expected:** This criterion explicitly targets a missing submission document, so its confirmed absence supports a concern.

**Model:** The subject is Delta Fabrication, and the period is the complete final submission as referenced in the evidence. The evidence states that 'the required current written lockout procedure was not supplied' in the complete final submission. This directly supports the trigger condition that the submission lacks the required document. The rule evaluates presence of the document in the submission, not worker compliance. There is no explicit exception mentioned in the rule text for C1, and no evidence of an applicable exception being met. No conflicting observations are present. The evidence clearly indicates that the required document was not supplied in the submission.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 2; model calls: 7; elapsed: 20.7s.

**Rejected responses:** condition_quote must be an exact excerpt from the requested criterion.text; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag a concern if the submission lacks the required current written machine lockout procedure. Evaluate the presence of that document in the completed submission, not whether workers follow a procedure.", "scope_reason": "The subject is Delta Fabrication, and the period is the complete final submission as referenced in the evidence.", "scope": "in_scope", "condition_reason": "The evidence states that 'the required current written lockout procedure was not supplied' in the complete final submission. This directly supports the trigger condition that the submission lacks the required document. The rule evaluates presence of the document in the submission, not worker compliance.", "condition": "false", "exception_reason": "There is no explicit exception mentioned in the rule text for C1, and no evidence of an applicable exception being met.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "No conflicting observations are present. The evidence clearly indicates that the required document was not supplied in the submission.", "conflict": "none", "findings": [{"subject": "Delta Fabrication", "evidence_ids": ["E1"], "reason": "The complete final submission for Delta Fabrication did not include the required current written machine lockout procedure, as stated in E1. This meets the condition for flagging a concern under criterion C1."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r... under criterion C1.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Negative-evidence review (C1):** `supported`. The criterion requires evaluation of whether the required current written machine lockout procedure is present in the completed submission. Evidence E1 explicitly states that the required procedure was not supplied in the submission. This directly supports a negative decision as the procedure is missing from the submission.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that 'the required current written lockout procedure was not supplied' in the complete final submission. This directly supports the trigger condition that the submission lacks the required document. The rule evaluates presence of the document in the submission, not worker compliance. There is no explicit exception mentioned in the rule text for C1, and no evidence of an applicable exception being met.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### wc_activity_explicitly_not_performed

**Expected:** The explicit delayed induction disproves the all-employees pre-operation requirement despite later completion.

**Model:** The rule applies to newly hired production employees who operated production equipment in 2025. The evidence E1 describes two such employees who first operated equipment on 2025-05-02 and received induction on 2025-05-08, which is after they began operating equipment. The evidence shows that two newly hired production employees operated production equipment on 2025-05-02 without receiving machine-safety induction. Induction was subsequently completed on 2025-05-08. Since the employees operated equipment before receiving induction, this condition is false. The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There is no conflicting evidence in the provided information. The observation clearly states that the employees operated equipment before receiving induction, which directly contradicts the requirement of the rule.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 1; model calls: 6; elapsed: 20.5s.

**Rejected responses:** Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "every newly hired production employee received machine-safety induction before first operating production equipment in 2025", "scope_reason": "The rule applies to newly hired production employees who operated production equipment in 2025. The evidence E1 describes two such employees who first operated equipment on 2025-05-02 and received induction on 2025-05-08, which is after they began operating equipment.", "scope": "in_scope", "condition_reason": "The evidence shows that two newly hired production employees operated production equipment on 2025-05-02 without receiving machine-safety induction. Induction was subsequently completed on 2025-05-08. Since the employees operated equipment before receiving induction, this condition is false.", "condition": "false", "exception_reason": "The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case.", "exception": "does_not_apply", "evidence_ids": ["E1"], "conflict_reason": "There is no conflicting evidence in the provided information. The observation clearly states that the employees operated equipment before receiving induction, which directly contradicts the requirement of the rule.", "conflict": "none", "findings": [{"subject": "newly hired production employees", "evidence_ids": ["E1"], "reason": "Two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction, which was completed on 2025-05-08. This violates the requirement that all such employees receive induction before operating equipment."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...operating equipment.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Negative-evidence review (C1):** `supported`. The criterion requires that every newly hired production employee received machine-safety induction before first operating production equipment in 2025. Evidence E1 explicitly states that two newly hired production employees operated production equipment on 2025-05-02 without receiving machine-safety induction, and that induction was completed later on 2025-05-08. This directly contradicts the condition of the criterion, as the employees did not receive the required induction prior to operating equipment.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence shows that two newly hired production employees operated production equipment on 2025-05-02 without receiving machine-safety induction. Induction was subsequently completed on 2025-05-08. Since the employees operated equipment before receiving induction, this condition is false. The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case.

### property_inspection_date_unknown

**Expected:** Without the last-completed date, the twelve-month condition is unknown.

**Model:** The rule applies to the last completed electrical thermographic inspection at Fern Mill, with a reference point of 2025-09-01. There is no recorded date for the last completed electrical thermographic inspection at Fern Mill. E1 states that Fern Mill cannot locate the date and contractor records were lost. This lack of information means it is impossible to determine whether the inspection was completed more than 12 months before 2025-09-01. Therefore, the condition cannot be evaluated as true or false based on available evidence. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no conflicting observations regarding the date of the last electrical thermographic inspection at Fern Mill. The only evidence (E1) indicates a lack of documentation, not a contradiction.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 19.0s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. There is no recorded date for the last completed electrical thermographic inspection at Fern Mill. E1 states that Fern Mill cannot locate the date and contractor records were lost. This lack of information means it is impossible to determine whether the inspection was completed more than 12 months before 2025-09-01. Therefore, the condition cannot be evaluated as true or false based on available evidence. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### property_cross_source_alarm_and_value

**Expected:** The value and whole-stock alarm condition require combining both sources into one strength.

**Model:** The subject is 'Haven Parts' and the period is as of 2025-09-01. The evidence batch covers this date and subject. The total declared stock value is $425,000 (from E1), which is less than $500,000. The entire insured stock is in a continuously monitored intruder-alarm area (from E2). Both conditions of the trigger are met. There are no explicit exception prerequisites mentioned in the rule. No conflicting observations were found. Both E1 and E2 support the trigger condition without contradiction.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 1; model calls: 6; elapsed: 25.4s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2', 'E1']. Explain resolution, different scope, or unresolved conflict.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The total declared stock value is $425,000 (from E1), which is less than $500,000. The entire insured stock is in a continuously monitored intruder-alarm area (from E2). Both conditions of the trigger are met. There are no explicit exception prerequisites mentioned in the rule.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_loss_aggregation_without_duplicate

**Expected:** Distinct claims sum to $325,000, above $300,000. Do not add the repeated GL-101 again or create a finding per claim.

**Model:** The rule applies to 2025 general liability claims. The evidence includes two distinct 2025 claims (GL-101 and GL-102) as noted in E1. The subject is the total paid amounts for these claims. The evidence shows two distinct 2025 general liability claims: GL-101 with a paid amount of $150,000 and GL-102 with a paid amount of $175,000. The broker's note (E2) confirms that GL-101 is duplicated but does not alter the paid amounts or indicate additional claims. Therefore, the total paid amount for distinct 2025 claims is $150,000 + $175,000 = $325,000. This exceeds the threshold of $300,000. The condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case. There is no actual incompatible observation. The broker's note (E2) confirms GL-101 is a duplicate reference but does not contradict the paid amounts or claim existence. Both claims are distinct and valid for the purpose of calculating total paid amounts.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 6; model calls: 9; elapsed: 37.6s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000.", "scope_reason": "The scope is in_scope because the evidence pertains to 2025 general liability claims as required by the criterion. The rule's applicability is not restricted to a specific population or subject beyond the claim note itself, so the scope is in_scope.", "scope": "in_scope", "condition_reason": "The total paid amounts for distinct 2025 general liability claims are calculated as $150,000 (GL-101) + $175,000 (GL-102) = $325,000. This exceeds the threshold of $30300,000 specified in the criterion. The evidence E1 lists two separate claims, GL-101 and GL-102, with paid amounts of $150,000 and $175,000 respectively. The evidence E2 indicates that GL-101 is referenced twice but is explicitly identified as a duplicate. Therefore, only one distinct claim (GL-101) is counted with its latest paid amount of $150,000. However, the assessment from 'lossrun:primary' includes both claims in the calculation, which results in a total exceeding $300,000.", "condition": "true", "exception_reason": "There are no explicit exceptions mentioned in the criterion that would apply to this case.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "There is a conflict between the two source assessments. The 'lossrun:primary' assessment includes both claims (GL-101 and GL-102) in the calculation, resulting in a total of $325,000, which exceeds the threshold. In contrast, the 'broker:claim_note' assessment identifies GL-101 as a duplicate and only counts it once, leading to a total of $150,000, which does not exceed the threshold. The conflict arises from the interpretation of whether GL-101 should be counted twice or once in the total calculation.", "conflict": "unresolved", "findings": [{"subject": "2025 general liability claims", "evidence_ids": ["E1"], "reason": "The total paid amounts for distinct 2025 general liability claims (GL-101 and GL-102) amount to $325,000, which exceeds the $300,000 threshold. Therefore, one concern is flagged as per the criterion."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...s per the criterion.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; Model output could not be parsed: Failed to parse PredicateDraft from completion [{"criterion_id": "C1", "condition_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000.", "scope_reason": "The scope is in_scope because the evidence pertains to 2025 general liability claims as required by the criterion. The rule's applicability is not restricted to a specific population or subject beyond the claim note itself, so the scope is in_scope.", "scope": "in_scope", "condition_reason": "The total paid amounts for distinct 2025 general liability claims are calculated as $150,000 (GL-101) + $175,000 (GL-102) = $325,000. This exceeds the threshold of $300,000 specified in the criterion. The evidence E1 lists two separate claims, GL-101 and GL-102, with paid amounts of $150,000 and $175,000 respectively. The evidence E2 indicates that GL-101 is referenced twice but is explicitly identified as a duplicate. Therefore, only one distinct claim (GL-101) is counted with its latest paid amount of $150,000. However, the assessment from 'lossrun:primary' includes both claims in the calculation, which results in a total exceeding $300,000.", "condition": "true", "exception_reason": "There are no explicit exceptions mentioned in the criterion that would apply to this case.", "exception": "does_not_apply", "evidence_ids": ["E1", "E2"], "conflict_reason": "There is a conflict between the two source assessments. The 'lossrun:primary' assessment includes both claims (GL-101 and GL-102) in the calculation, resulting in a total of $325,000, which exceeds the threshold. In contrast, the 'broker:claim_note' assessment identifies GL-101 as a duplicate and only counts it once, leading to a total of $1150,000, which does not exceed the threshold. The conflict arises from the interpretation of whether GL-101 should be counted twice or once in the total calculation.", "conflict": "unresolved", "findings": [{"subject": "2025 general liability claims", "evidence_ids": ["E1"], "reason": "The total paid amounts for distinct 2025 general liability claims (GL-101 and GL-102) amount to $325,000, which exceeds the $300,000 threshold. Therefore, one concern is flagged as per the criterion."}]}]. Got: 1 validation error for PredicateDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...s per the criterion.')]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE ; Model output could not be parsed: Failed to parse ConsistencyDraft from completion [{"criterion_id": "C1", "scope_quote": "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000.", "scope_applies": true, "exception_quote": "", "verdict": "supported", "issues": [{"explanation_id": "assessment.reason", "reason": "The explanation contains no contradictory statements. It correctly identifies two distinct 2025 claims (GL-101 and GL-102), accurately calculates their total paid amounts as $325,000, and correctly concludes that this exceeds the $300,000 threshold. The note about duplication in E2 does not introduce any inconsistency because it only refers to a duplicate claim reference, not an additional claim or altered paid amount."}], "reason": "The final assessment aligns with the rule's requirement. The total paid amount for distinct 2025 general liability claims is $325,000, which exceeds the $300,000 threshold. There are no exceptions or contradictions in the evidence that would prevent this conclusion. The duplicate reference in E2 does not affect the validity of either claim or its paid amount."}]. Got: 1 validation error for ConsistencyDraft
0
  Value error, Explanation issues cannot receive a supported verdict [type=value_error, input_value={'criterion_id': 'C1', 's...im or its paid amount."}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. The evidence shows two distinct 2025 general liability claims: GL-101 with a paid amount of $150,000 and GL-102 with a paid amount of $175,000. The broker's note (E2) confirms that GL-101 is duplicated but does not alter the paid amounts or indicate additional claims. Therefore, the total paid amount for distinct 2025 claims is $150,000 + $175,000 = $325,000. This exceeds the threshold of $300,000. The condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### cyber_restore_duration_cross_midnight

**Expected:** Elapsed time is 25.5 hours, exceeding the 24-hour maximum despite a successful eventual restore.

**Model:** The subject is the full restore of the payroll application, and the period in scope is from 2025-08-01 08:00 UTC to 2025-08-02 09:30 UTC. The restore started at 2025-08-01 08:00 UTC and completed at 2025-08-02 09:30 UTC. Elapsed time = 25 hours and 30 minutes. Since the elapsed time exceeds 24 hours, the condition is false. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case. There are no conflicting observations in the evidence provided.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 6; elapsed: 17.1s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining whether the completed full restore of the payroll application took no longer than 24 hours, using the supplied UTC start and completion timestamps. The start timestamp is 2025-08-01 08:00 UTC (E1) and the completion timestamp is 2025-08-02 09:30 UTC (E2). Calculating the elapsed time: from 2025-08-01 08:00 to 2025-08-02 09:30 is exactly 25 hours and 30 minutes. This exceeds the 24-hour threshold, so the condition of the criterion is not met.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The restore started at 2025-08-01 08:00 UTC and completed at 2025-08-02 09:30 UTC. Elapsed time = 25 hours and 30 minutes. Since the elapsed time exceeds 24 hours, the condition is false. There are no explicit exception prerequisites or validity dates mentioned in the rule that would apply to this case.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### property_expired_exception_certificate

**Expected:** The height trigger is met and the explicit approval exception is unavailable on the assessment date.

**Model:** The subject is Linden Distribution's storage area on 2025-09-01. The period in scope is 2025-09-01. On 2025-09-01, combustible packaged stock was stacked to 5.2 metres at Linden Distribution (E1). This exceeds the 4-metre threshold. The engineer's high-stack approval allowed stacks up to 5.5 metres but expired on 2025-06-30 (E2). No renewal or extension was issued before 2025-09-01. Therefore, the approval is not valid on 2025-09-01. The condition is true: combustible stock was stacked above four metres and the exception does not apply. The exception requires that an engineer's specific high-stack approval remains valid on 2025-09-01. However, the approval expired on 2025-06-30 and no renewal or extension was issued before 2025-09-01 (E2). Therefore, the exception does not apply. There are no actual incompatible observations. E1 confirms the stack height was 5.2 metres; E2 confirms the approval expired on 2025-06-30 with no renewal before 2025-09-01. These facts do not contradict each other.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 24.1s.

**Independent review (C1):** scope `in_scope`, condition `true`, exception `does_not_apply`. On 2025-09-01, combustible packaged stock was stacked to 5.2 metres at Linden Distribution (E1). This exceeds the 4-metre threshold. The engineer's high-stack approval allowed stacks up to 5.5 metres but expired on 2025-06-30 (E2). No renewal or extension was issued before 2025-09-01. Therefore, the approval is not valid on 2025-09-01. The condition is true: combustible stock was stacked above four metres and the exception does not apply. The exception requires that an engineer's specific high-stack approval remains valid on 2025-09-01. However, the approval expired on 2025-06-30 and no renewal or extension was issued before 2025-09-01 (E2). Therefore, the exception does not apply.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
