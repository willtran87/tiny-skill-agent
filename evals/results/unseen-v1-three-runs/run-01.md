# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-18T23:41:41.893601+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **17/32** (planned: 32).
- Correct case statuses: **20/32**.
- Required gold evidence cited: **31/35**.
- Reference/provenance checks: **132/132**.
- False-positive findings in the 20 nonmatched gold cases: **2**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| cyber_remote_access_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_pump_service_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_driver_screening_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| gl_subcontract_limit_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_incident_rate_calculation | matched | insufficient_evidence | 0 / 1 | 2 / 2 | FAIL |
| property_reserves_exact_threshold | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_roof_exact_boundary | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| cyber_patch_coverage_boundary | matched | matched | 1 / 1 | 1 / 1 | PASS |
| property_alarm_equal_reports | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | FAIL |
| cyber_backup_immutability_conflict | insufficient_evidence | insufficient_evidence | 0 / 0 | 2 / 2 | PASS |
| auto_mileage_corrected_denominator | no_match | matched | 1 / 0 | 2 / 2 | FAIL |
| property_later_repair_does_not_rewrite_history | matched | matched | 2 / 1 | 1 / 1 | FAIL |
| property_electrical_exception | no_match | matched | 1 / 0 | 2 / 2 | FAIL |
| cyber_service_account_exception | no_match | missing | 0 / 0 | 0 / 2 | FAIL |
| gl_hot_work_scope_exclusion | not_applicable | insufficient_evidence | 0 / 0 | 1 / 1 | FAIL |
| auto_passenger_scope_exclusion | not_applicable | not_applicable | 0 / 0 | 1 / 1 | PASS |
| property_multiple_warehouse_concerns | matched | matched | 2 / 2 | 2 / 2 | PASS |
| auto_multiple_expired_licences | matched | missing | 0 / 2 | 0 / 2 | FAIL |
| cyber_multiple_restore_strengths | matched | matched | 2 / 2 | 2 / 2 | PASS |
| property_corroboration_not_two_events | matched | matched | 1 / 1 | 0 / 0 | PASS |
| gl_sister_company_evidence | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| cyber_prior_year_does_not_prove_current | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_building_specific_scope | not_applicable | no_match | 0 / 0 | 1 / 1 | FAIL |
| wc_partial_payroll_period | insufficient_evidence | not_applicable | 0 / 0 | 0 / 0 | FAIL |
| gl_document_submission_condition | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| wc_document_absence_is_concern | matched | no_match | 0 / 1 | 1 / 1 | FAIL |
| wc_activity_explicitly_not_performed | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| property_inspection_date_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_cross_source_alarm_and_value | matched | no_match | 0 / 1 | 2 / 2 | FAIL |
| gl_loss_aggregation_without_duplicate | matched | matched | 1 / 1 | 1 / 1 | FAIL |
| cyber_restore_duration_cross_midnight | no_match | insufficient_evidence | 0 / 0 | 2 / 2 | FAIL |
| property_expired_exception_certificate | matched | no_match | 0 / 1 | 2 / 2 | FAIL |

## Reasons and diagnostics

### cyber_remote_access_unknown

**Expected:** Administrator MFA does not establish workforce MFA; blank or unavailable records do not prove absence of the control.

**Model:** The criterion requires that MFA protects every remote workforce login to Harbor Analytics as of 2025-09-01. Evidence E1 indicates that MFA is enabled for all four cloud administrators but does not confirm whether all remote workforce logins are protected, and the response about workforce VPN and remote desktop authentication was left blank. Evidence E2 states that the VPN configuration report was not available and the broker has not verified the remote-login configuration. These gaps in information prevent a determination of whether all remote workforce logins are protected by MFA.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 18.2s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that MFA protects every remote workforce login to Harbor Analytics as of 2025-09-01. Evidence E1 indicates that MFA is enabled for all four cloud administrators but does not confirm whether all remote workforce logins are protected, and the response about workforce VPN and remote desktop authentication was left blank. Evidence E2 states that the VPN configuration report was not available and the broker has not verified the remote-login configuration. These gaps in information prevent a determination of whether all remote workforce logins are protected by MFA.

### property_pump_service_unknown

**Expected:** Unlocated records and a visual inspection cannot establish a missed service visit.

**Model:** There is an unresolved conflict between the two source assessments regarding whether the fire pump at Cedar Components was serviced during calendar 2025. The surveyor's report (E1) indicates that the maintenance binder was unavailable, which implies a lack of service records, but does not definitively prove no servicing occurred in 2025. In contrast, the facilities email (E2) explicitly states that the pump contractor's 2025 service invoice cannot be located and it is unclear whether the visit took place, directly supporting the criterion. Since these sources present contradictory evidence without a clear resolution, the conflict remains unresolved.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 1; model calls: 4; elapsed: 7.0s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

### auto_driver_screening_unknown

**Expected:** Neither the interview process nor missing files establishes whether all MVR reviews occurred.

**Model:** The criterion requires that motor vehicle records be reviewed for every employed driver before hire. Evidence E1 indicates that hiring includes an interview and a route test, but the MVR review field is unanswered, meaning it's unknown whether MVR reviews occurred. Evidence E2 states that driver files have not been provided and there is no confirmation of pre-hire MVR reviews. Since the condition cannot be confirmed as true due to missing evidence about whether MVR reviews were actually conducted, this constitutes missing evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 4; elapsed: 5.7s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that motor vehicle records be reviewed for every employed driver before hire. Evidence E1 indicates that hiring includes an interview and a route test, but the MVR review field is unanswered, meaning it's unknown whether MVR reviews occurred. Evidence E2 states that driver files have not been provided and there is no confirmation of pre-hire MVR reviews. Since the condition cannot be confirmed as true due to missing evidence about whether MVR reviews were actually conducted, this constitutes missing evidence.

### gl_subcontract_limit_unknown

**Expected:** Unspecified insurance limits cannot satisfy or disprove the $2 million requirement.

**Model:** The criterion requires that every active roofing subcontractor maintain at least $2 million of general liability limits. Evidence E1 indicates that two active roofing subcontractors (North Roof and Ridge Team) are marked as insured in the vendor register, but the register does not record limits or policy numbers. Evidence E2 states that certificates for both subcontractors have been requested but not received, and their general liability limits have not been confirmed. Since there is no evidence confirming that the limits meet or exceed $2 million, and the information necessary to verify this is missing, the condition cannot be determined to be true or false based on the available evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 6.6s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that every active roofing subcontractor maintain at least $2 million of general liability limits. Evidence E1 indicates that two active roofing subcontractors (North Roof and Ridge Team) are marked as insured in the vendor register, but the register does not record limits or policy numbers. Evidence E2 states that certificates for both subcontractors have been requested but not received, and their general liability limits have not been confirmed. Since there is no evidence confirming that the limits meet or exceed $2 million, and the information necessary to verify this is missing, the condition cannot be determined to be true or false based on the available evidence.

### auto_incident_rate_calculation

**Expected:** Three divided by 24 times 100 is 12.5, above 10. This is one aggregate finding, not three separate collision findings.

**Model:** The guideline requires assessing whether preventable collision frequency exceeds 10 collisions per 100 active vehicles for the year 2025. The evidence indicates that Summit operated 24 active vehicles during 2025, and no information is provided regarding the number of preventable collisions. Since there is no data on collisions to calculate the frequency, the condition cannot be evaluated.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 5; elapsed: 6.2s.

**Rejected responses:** Model output could not be parsed: Failed to parse CoverageDraft from completion [{"criterion_id": "C1", "reason": "The fleet's preventable collision frequency of 3 collisions per 100 active vehicles does not exceed the threshold of 10 collisions per 100 active vehicles, therefore no fleet-level concern is flagged.", "evidence_ids": ["E1"], "conflict": "none", "basis": "condition_met", "status": "no_match", "findings": []}]. Got: 1 validation error for CoverageDraft
0
  Value error, status disagrees with basis [type=value_error, input_value={'criterion_id': 'C1', 'r..._match', 'findings': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

### property_reserves_exact_threshold

**Expected:** 480,000 / 120,000 equals exactly four months; at least includes equality.

**Model:** Bay Storage holds unrestricted cash reserves of $480,000, which covers at least four months of its stated operating expense of $120,000 per month. The calculation shows that $480,000 divided by $120,000 equals exactly four months, meeting the minimum requirement for a strength.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 4.1s.

### property_roof_exact_boundary

**Expected:** Exactly 20 does not exceed a strictly greater-than-20 threshold.

**Model:** The roof at Unit 7 was installed on 2005-07-01, making it exactly 20 years old as of the assessment date 2025-07-01. Since the criterion requires flagging if the roof is 'strictly older than 20 years,' and the roof's age is exactly 20 years (not older), the condition is not met.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 4.0s.

**Negative-evidence review (C1):** `supported`. The evidence establishes that Unit 7's roof was installed on 2005-07-01, and the assessment date is 2025-07-01, making the roof exactly 20 years old. The criterion requires the roof to be 'strictly older than 20 years,' which means it must be more than 20 years. Since the roof is exactly 20 years old and not strictly older, the condition is not met.

### cyber_patch_coverage_boundary

**Expected:** 95/100 equals 95%, meeting an inclusive threshold despite five exceptions.

**Model:** The criterion requires that at least 95% of the 100 in-scope servers have all critical patches installed within 14 days of release. Evidence E1 shows that 95 out of 100 servers met the 14-day deadline, three were patched on day 20, and two remain outstanding. Since the two outstanding servers do not meet the requirement, the total number of servers meeting the condition is 98 out of 100, which is 98%. This exceeds the 95% threshold, thus satisfying the criterion.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 4.9s.

### property_alarm_equal_reports

**Expected:** Equal-authority incompatible observations of the same state require abstention and both citations.

**Model:** There is an unresolved conflict between Provider A and Provider B regarding the status of the monitored fire alarm at Orchard Packaging at 10:00 on 2025-06-12. Provider A reports the alarm as OFFLINE, while Provider B reports it as ONLINE. Since the conflict cannot be resolved based on the provided evidence, the assessment cannot determine whether the condition for flagging a concern is met.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 1; captured call errors: 3; model calls: 5; elapsed: 6.5s.

**Rejected responses:** Model output could not be parsed: Failed to parse CoverageDraft from completion [{"criterion_id": "C1", "reason": "The monitored fire alarm at Orchard Packaging was reported as ONLINE at 10:00 on 2025-06-12, which directly contradicts the condition that it be offline. Therefore, the concern is not flagged.", "evidence_ids": ["E2"], "conflict": "unresolved", "basis": "condition_not_met", "status": "no_match", "findings": []}]. Got: 1 validation error for CoverageDraft
0
  Value error, unresolved conflict requires basis unresolved_conflict and insufficient_evidence [type=value_error, input_value={'criterion_id': 'C1', 'r..._match', 'findings': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

### cyber_backup_immutability_conflict

**Expected:** Contradictory same-period attestations cannot be resolved by source votes or department titles.

**Model:** There is an unresolved conflict between the two attestations regarding whether production vault PV-3 had immutable retention enabled on 2025-08-31. The security lead attests that it was enabled, while the infrastructure lead states it was disabled. Since the criterion requires a definitive yes or no for the condition and the evidence presents contradictory claims about the same subject and time period without resolution, the assessment cannot be finalized.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 3; elapsed: 4.4s.

### auto_mileage_corrected_denominator

**Expected:** Three per two million equals 1.5 per million, below two; the explicit correction controls the denominator.

**Model:** Northline's 2025 preventable collision rate exceeds two per million miles. The fleet accountant's signed correction explicitly supersedes the original 2025 statement, establishing that actual calendar-2025 mileage was 2,000,000 miles. The original upload omitted half of the vehicles; the collision count is unchanged. This corrected mileage of 2,000,000 miles is used to calculate the preventable collision rate, which exceeds two per million miles as required by the criterion.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 9.6s.

### property_later_repair_does_not_rewrite_history

**Expected:** The historical impairment remains a concern; a later repair is a state change, not a correction.

**Model:** The historical inspection on 2025-03-01 found that Cedar Depot's sprinkler system was impaired, with a seized closed control valve. This condition existed at the time of assessment and is flagged as a concern per the criterion. The later repair on 2025-03-05 does not alter the historical condition as specified in the criterion.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 6.9s.

### property_electrical_exception

**Expected:** The age trigger applies but the documented complete replacement establishes the explicit exception.

**Model:** The building was constructed in 1952, which is before 1960, triggering the initial concern. However, a licensed contractor's documentation of complete replacement of original electrical wiring after 2010 is present in E2, which satisfies the criterion. Therefore, no concern is flagged.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 1; model calls: 4; elapsed: 7.3s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2']. Explain resolution, different scope, or unresolved conflict.

### cyber_service_account_exception

**Expected:** Both exception requirements are established, so lack of MFA does not trigger the concern for this account.

**Model:** No accepted case assessment.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 5; elapsed: 7.8s.

**Rejected responses:** Model output could not be parsed: Failed to parse CoverageDraft from completion [{"criterion_id": "C1", "reason": "The account 'invoice-sync' lacks MFA, but it qualifies as a noninteractive service account with interactive login disabled, which is an exception specified in the criterion. Additionally, the credential rotation interval is documented as 14 days, which satisfies the requirement of no longer than 30 days. Therefore, the condition for flagging a concern is not met.", "evidence_ids": ["E1", "E2"], "conflict": "none", "basis": "exception_applies", "status": "no_match", "findings": [{"subject": "invoice-sync", "evidence_ids": ["E1", "E2"], "reason": "The account 'invoice-sync' is a noninteractive service account with interactive login disabled, and it has a documented credential rotation interval of 14 days, which meets the exception criteria for MFA exemption."}]}]. Got: 1 validation error for CoverageDraft
0
  Value error, matched requires findings; other statuses require an empty findings list [type=value_error, input_value={'criterion_id': 'C1', 'r...a for MFA exemption."}]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

### gl_hot_work_scope_exclusion

**Expected:** The explicit operational scope excludes this applicant; a missing permit manual is irrelevant.

**Model:** The criterion applies only to contractors performing on-site welding or flame cutting at customers' premises. The evidence shows that Pine Design provides remote CAD drafting only and does not perform any physical work at customer sites, including welding or flame cutting. Since the contractor does not engage in the specified activities, the condition of the criterion cannot be met, but this does not constitute a negative decision because the criterion's applicability is limited to specific activities that are not performed by Pine Design.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 4.1s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion applies only to contractors performing on-site welding or flame cutting at customers' premises. The evidence shows that Pine Design provides remote CAD drafting only and does not perform any physical work at customer sites, including welding or flame cutting. Since the contractor does not engage in the specified activities, the condition of the criterion cannot be met, but this does not constitute a negative decision because the criterion's applicability is limited to specific activities that are not performed by Pine Design.

### auto_passenger_scope_exclusion

**Expected:** Freight-only operations are outside the explicit passengers-for-hire scope.

**Model:** The criterion applies to vehicles carrying passengers for hire, requiring annual emergency evacuation training. Granite Freight's fleet operates five box trucks that transport commercial goods, not passengers for hire. The subject does not meet the explicit scope condition of 'vehicles carrying passengers for hire,' and therefore the criterion does not apply.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 2.4s.

### property_multiple_warehouse_concerns

**Expected:** East and West qualify independently; extinguishers and future plans do not satisfy the condition, and the office is excluded.

**Model:** The assessment correctly identifies two separate storage warehouses that meet the criterion's conditions: East Warehouse and West Warehouse. Each is occupied and lacks automatic sprinklers, qualifying as separate concerns under C1. The office-only building (E3) is properly excluded from the scope of the criterion, as explicitly stated in the guideline. There is no conflict between these findings because they concern distinct subjects within different scopes. Therefore, both findings are valid and independently qualifying.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 1; captured call errors: 1; model calls: 5; elapsed: 10.8s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

### auto_multiple_expired_licences

**Expected:** Two independently identified employees meet the concern; Driver C does not.

**Model:** No accepted case assessment.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 6; elapsed: 17.4s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E1', 'E2', 'E3']. Explain resolution, different scope, or unresolved conflict.

### cyber_multiple_restore_strengths

**Expected:** Each application independently meets both timing conditions and warrants its own strength.

**Model:** The criterion requires a separate strength to be recorded for each business-critical application with a completed restore test within the last 90 days and a demonstrated recovery time no longer than four hours, as of 2025-09-01. Evidence E1 shows that the billing application, designated as business-critical, underwent a completed restore test on 2025-08-10 with a recovery time of 3 hours, which is within the last 90 days and under the 4-hour limit. Evidence E2 shows that the inventory application, also designated as business-critical, had a completed restore test on 2025-07-20 with a recovery time of exactly 4 hours, which also meets the criteria. Both applications satisfy the conditions, and each has an independent qualifying finding.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 8.6s.

### property_corroboration_not_two_events

**Expected:** One generator/test warrants one finding; either source independently supports it and both may be cited together.

**Model:** The evidence shows that Generator G-1 at Birch Cold Storage was successfully tested under full building load during August 2025, specifically on 2025-08-12. This test qualifies as a standalone finding because it represents the only August full-load test conducted at this site, and the generator is noted as the site's only standby generator. Multiple reports of the same test (from contractor and engineer) are considered one finding as per the criterion's instruction.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 7.6s.

### gl_sister_company_evidence

**Expected:** A sister company's recall is not evidence of the applicant's recall history; absence of applicant records is not proof of no recall.

**Model:** The criterion requires determining if Aspen Foods LLC had a product recall during 2025. Evidence E2 states that Aspen Beverage LLC recalled a beverage product in May 2025, but the summary gives no recall history for Aspen Foods LLC. Although the companies are separate entities sharing a holding company and street address, the recall event is explicitly attributed to Aspen Beverage LLC, not Aspen Foods LLC. However, the applicant's own recall response remains unanswered, leaving uncertainty about whether Aspen Foods LLC had any recall activity during 2025.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 4; elapsed: 6.3s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires determining if Aspen Foods LLC had a product recall during 2025. Evidence E2 states that Aspen Beverage LLC recalled a beverage product in May 2025, but the summary gives no recall history for Aspen Foods LLC. Although the companies are separate entities sharing a holding company and street address, the recall event is explicitly attributed to Aspen Beverage LLC, not Aspen Foods LLC. However, the applicant's own recall response remains unanswered, leaving uncertainty about whether Aspen Foods LLC had any recall activity during 2025.

### cyber_prior_year_does_not_prove_current

**Expected:** A previous-year control assessment and unknown post-migration controls cannot establish the current-year requirement.

**Model:** The criterion requires testing of offline backups for all business-critical systems during calendar 2025. Evidence E1 confirms tested offline backups for all business-critical systems in calendar 2024, but does not cover 2025. Evidence E2 indicates that backup test records and offline-storage configuration for 2025 have not yet been supplied, and current effectiveness is unverified. Since there is no evidence confirming that all business-critical systems had tested offline backups during calendar 2025, the condition cannot be confirmed as true.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 4; elapsed: 6.6s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires testing of offline backups for all business-critical systems during calendar 2025. Evidence E1 confirms tested offline backups for all business-critical systems in calendar 2024, but does not cover 2025. Evidence E2 indicates that backup test records and offline-storage configuration for 2025 have not yet been supplied, and current effectiveness is unverified. Since there is no evidence confirming that all business-critical systems had tested offline backups during calendar 2025, the condition cannot be confirmed as true.

### property_building_specific_scope

**Expected:** Building A fails the wood-frame applicability condition; Building B cannot make an A-specific rule applicable.

**Model:** The criterion applies only to Building A, and the evidence confirms that Building A has a steel structural frame and concrete external walls with no combustible wood structural frame. Since the building does not meet the condition of having a combustible wood structural frame, the criterion does not apply. Although Building A lacks automatic sprinklers, this does not trigger the concern because the primary condition for applying the criterion is not met.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 5.6s.

**Negative-evidence review (C1):** `supported`. The criterion applies specifically to Building A and requires that if its structural frame is combustible wood, then automatic sprinklers should be present as a concern. Evidence E1 explicitly states that Building A has a steel structural frame and concrete external walls, and that the engineer confirms there is no combustible wood structural frame in Building A. Since Building A does not have a combustible wood structural frame, the condition for applying the criterion is not met, and therefore no concern should be flagged.

### wc_partial_payroll_period

**Expected:** A 20% quarter does not establish the full-year rate when the remaining nine months are unknown.

**Model:** The criterion requires assessing whether the insured's total overtime hours exceed 15% of all hours worked during the full 2025 calendar year. However, the evidence provided only covers the first quarter (January-March 2025) and does not reflect the full annual figures. The evidence indicates 2,000 overtime hours out of 10,000 total hours worked for Q1, which is 20% of that quarter's hours. Since the evidence is limited to a partial year and does not provide annual data, it cannot be used to determine if the threshold of 15% for the full year has been exceeded.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 5.6s.

### gl_document_submission_condition

**Expected:** Confirmed nonsubmission disproves a submission-specific strength without assuming no agreements exist.

**Model:** The evidence directly contradicts the condition required for a strength. The submission inventory confirms that no signed hold-harmless agreements were supplied for any of the three active subcontractors, which means the documented requirement for submission of such agreements was not met.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 3.4s.

**Negative-evidence review (C1):** `supported`. The evidence explicitly states that no signed hold-harmless agreements were supplied for any of the three active subcontractors. This directly contradicts the criterion's requirement that such agreements be provided with the submission.

### wc_document_absence_is_concern

**Expected:** This criterion explicitly targets a missing submission document, so its confirmed absence supports a concern.

**Model:** The submission lacks the required current written machine lockout procedure. The intake reviewer explicitly checked the complete final submission for Delta Fabrication and confirmed that the required document was not supplied, even though other documents such as payroll, a loss run, and an equipment list were included.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 3.7s.

**Negative-evidence review (C1):** `supported`. The criterion requires evaluation of whether the submission lacks the required current written machine lockout procedure. Evidence E1 explicitly states that the required current written lockout procedure was not supplied in the submission. This directly supports a negative decision as the procedure is missing from the completed submission.

### wc_activity_explicitly_not_performed

**Expected:** The explicit delayed induction disproves the all-employees pre-operation requirement despite later completion.

**Model:** The criterion requires that every newly hired production employee received machine-safety induction before first operating production equipment in 2025. However, the evidence shows that two newly hired production employees operated production equipment on 2025-05-02 without receiving the required induction, which was subsequently completed on 2025-05-08. This condition is not met for these employees, thus failing to satisfy the criterion.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 4.7s.

**Negative-evidence review (C1):** `supported`. The criterion requires that every newly hired production employee received machine-safety induction before first operating production equipment in 2025. Evidence E1 explicitly states that two newly hired production employees operated production equipment on 2025-05-02 without receiving machine-safety induction, and that induction was completed later on 2025-05-08. This directly contradicts the condition of the criterion, as it establishes that at least one employee did not receive the required induction before operating equipment.

### property_inspection_date_unknown

**Expected:** Without the last-completed date, the twelve-month condition is unknown.

**Model:** The evidence indicates that Fern Mill cannot locate the date of its last completed electrical thermographic inspection, and contractor records were lost during a server migration. Since there is no confirmed date for the last inspection, it is not possible to determine whether the inspection was more than 12 months before 2025-09-01. Therefore, the condition for flagging a concern cannot be evaluated.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 4.8s.

### property_cross_source_alarm_and_value

**Expected:** The value and whole-stock alarm condition require combining both sources into one strength.

**Model:** The insured stock value of $425,000 does not exceed the $500,000 threshold, and all stock is held inside a single insured warehouse. However, the evidence does not establish that the warehouse is in a continuously monitored intruder-alarm area, which is a required condition for this criterion.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 6; elapsed: 8.4s.

**Rejected responses:** Model output could not be parsed: Failed to parse CoverageDraft from completion [{"criterion_id": "C1", "reason": "The evidence shows that the entire interior of the warehouse is covered by an intruder alarm with continuous remote monitoring, meeting the requirement for a continuously monitored intruder-alarm area. However, the total declared stock value is not provided in the evidence, so it cannot be determined whether it is no greater than $500,000.", "evidence_ids": ["E2"], "conflict": "none", "basis": "condition_met", "status": "insufficient_evidence", "findings": []}]. Got: 1 validation error for CoverageDraft
0
  Value error, status disagrees with basis [type=value_error, input_value={'criterion_id': 'C1', 'r...idence', 'findings': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

**Negative-evidence review (C1):** `supported`. The criterion requires that the entire insured stock be in a continuously monitored intruder-alarm area and that the total declared stock value be no greater than $500,000. Evidence E1 confirms that the total insured stock is $425,000, which is below the $500,000 threshold. Evidence E2 confirms that the entire interior of Haven Parts' sole warehouse is covered by an intruder alarm with continuous remote monitoring. Since both conditions are met, the criterion is satisfied.

### gl_loss_aggregation_without_duplicate

**Expected:** Distinct claims sum to $325,000, above $300,000. Do not add the repeated GL-101 again or create a finding per claim.

**Model:** The total paid amounts for distinct 2025 general liability claims exceed $300,000. However, the evidence shows that GL-101 is referenced twice—once in the loss run and once in the broker's note—but the broker explicitly identifies this as a duplicate reference to the same claim, not an additional claim. Therefore, only one instance of GL-101 should be counted. The correct total paid amount for distinct claims is $150,000 (GL-101) + $175,000 (GL-102) = $325,000, which exceeds the threshold of $300,000. However, since GL-101 appears twice and is identified as a duplicate, only one instance should count toward the total. Thus, the actual distinct claims are GL-101 ($150,000) and GL-102 ($175,000), totaling $325,000, which exceeds the threshold. But because of the duplicate identification in E2, the claim GL-101 is not counted twice, so the total remains $325,000, which satisfies the condition.

Coverage complete: `False`; decision ready: `False`; source/case disagreements: 0; captured call errors: 3; model calls: 5; elapsed: 10.2s.

**Rejected responses:** Model output could not be parsed: Failed to parse CoverageDraft from completion [{"criterion_id": "C1", "reason": "The evidence shows that only one distinct 2025 general liability claim (GL-101) is referenced, with a latest paid amount of $150,000. Since the total paid amounts for distinct claims do not exceed $300,000, no concern is flagged.", "evidence_ids": ["E2"], "conflict": "none", "basis": "condition_met", "status": "no_match", "findings": []}]. Got: 1 validation error for CoverageDraft
0
  Value error, status disagrees with basis [type=value_error, input_value={'criterion_id': 'C1', 'r..._match', 'findings': []}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error
For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE 

### cyber_restore_duration_cross_midnight

**Expected:** Elapsed time is 25.5 hours, exceeding the 24-hour maximum despite a successful eventual restore.

**Model:** There is a conflict between the two source assessments for criterion C1. The 'restore:start_log' source assesses the criterion as insufficient evidence due to missing completion timestamp, while the 'restore:completion_log' source assesses it as matched based on the completion timestamp being within the 24-hour threshold. However, the final resolution must consider that only one of the timestamps is sufficient for evaluation, and the completion timestamp in E2 supports a strength assessment. The conflict is unresolved because the start time from E1 does not contradict the completion time from E2, but the initial assessment from 'restore:start_log' was based on incomplete information.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 1; model calls: 4; elapsed: 8.2s.

**Rejected responses:** C1: review opposing source judgments; conflict must not be none and assessment evidence_ids must include ['E2']. Explain resolution, different scope, or unresolved conflict.

### property_expired_exception_certificate

**Expected:** The height trigger is met and the explicit approval exception is unavailable on the assessment date.

**Model:** The evidence presents a direct conflict between the surveyor's report and the engineer's approval. The surveyor states that combustible stock was stacked to 5.2 metres at Linden Distribution on 2025-09-01, referencing an engineer's high-stack approval for this storage area. However, the engineer confirms that the approval for this same storage area explicitly allowed stacks up to 5.5 metres but expired on 2025-06-30, with no renewal or extension issued before 2025-09-01. Since the approval is not valid on the assessment date (2025-09-01), the exception does not apply, and the concern for combustible stock stacked above four metres should be flagged.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 12.8s.

**Negative-evidence review (C1):** `supported`. The criterion requires that combustible stock stacked above four metres be flagged as a concern, except where an engineer's specific high-stack approval remains valid on 2025-09-01. Evidence E1 shows that at Linden Distribution on 2025-09-01, combustible packaged stock was stacked to 5.2 metres, and the applicant refers to an engineer's high-stack approval for this storage area. However, evidence E2 states that the approval for this same storage area explicitly allowed stacks up to 5.5 metres but expired on 2025-06-30, with no renewal or extension issued before 2025-09-01. Since the approval expired prior to the survey date and no valid approval exists on 2025-09-01, the condition for an exception does not hold.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
