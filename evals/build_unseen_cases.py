"""Authoring source for the frozen synthetic holdout-style set; no model calls.

All thresholds/policies and businesses are invented. Do not regenerate or edit
the JSON after evaluation begins; new versions should use new artifact names.
"""
import json
from pathlib import Path

cases = []


def add(cid, category, line, criterion, classification, observations, status, required, findings, rationale, alternatives=None):
    evidence = [{"id": f"E{i}", "source_id": source, "source_label": source,
                 "locator": f"paragraph:{i}", "quote": quote, "context": context}
                for i, (source, quote, context) in enumerate(observations, 1)]
    gold = [{"id": f"finding_{i}", "evidence_ids": ids} for i, ids in enumerate(findings, 1)]
    if alternatives:
        for finding, options in zip(gold, alternatives):
            finding["acceptable_evidence_sets"] = options
    cases.append({"id": cid, "category": category, "line_of_business": line,
                  "criteria": [{"id": "C1", "source_id": f"synthetic-guideline:{line}:v1",
                                "source_label": "Invented evaluation guideline", "text": criterion,
                                "classification": classification}],
                  "evidence": evidence,
                  "expected": {"status": status, "required_evidence_ids": required, "findings": gold,
                               "decision_ready": status != "insufficient_evidence", "rationale": rationale}})


add("cyber_remote_access_unknown", "missing_information", "cyber",
    "Record a strength if MFA protects every remote workforce login to Harbor Analytics as of 2025-09-01.", "strength", [
        ("questionnaire:it", "Harbor Analytics employs 85 staff across three offices. MFA is enabled for all four cloud administrators. The response to the separate question about workforce VPN and remote desktop authentication was left blank.", "Renewal submission dated 2025-09-01; administrator controls do not describe ordinary workforce remote access."),
        ("broker:email", "The client has requested its VPN configuration report but it was not available at submission. The broker has not verified the remote-login configuration. No losses were reported on the application.", "No additional attestation of workforce MFA was supplied.")],
    "insufficient_evidence", [], [], "Administrator MFA does not establish workforce MFA; blank or unavailable records do not prove absence of the control.")

add("property_pump_service_unknown", "missing_information", "property",
    "Flag a concern if the fire pump at Cedar Components was not serviced during calendar 2025.", "concern", [
        ("survey:equipment", "Cedar Components operates a 42,000-square-foot machining plant. The fire pump appears clean, has no visible leaks, and its local gauge is in the normal band. The maintenance binder was held off site and unavailable to the surveyor.", "Survey completed 2026-01-15. Visual condition does not establish whether servicing occurred in 2025."),
        ("facilities:email", "We cannot yet locate the pump contractor's 2025 service invoice. We are still checking the contractor's archive and cannot confirm whether the visit took place.", "Open document request; no assertion that the work did not occur.")],
    "insufficient_evidence", [], [], "Unlocated records and a visual inspection cannot establish a missed service visit.")

add("auto_driver_screening_unknown", "missing_information", "commercial_auto",
    "Record a strength if current motor vehicle records were reviewed for every employed driver before hire.", "strength", [
        ("fleet:application", "Maple Dispatch lists 18 employed delivery drivers and six vans. Hiring includes an interview and a route test. The MVR review field is unanswered; payroll records show no employee turnover this quarter.", "Application describes employed drivers only."),
        ("broker:followup", "The driver files have not been provided. There is no statement from the applicant confirming or denying pre-hire MVR reviews.", "The request remains outstanding.")],
    "insufficient_evidence", [], [], "Neither the interview process nor missing files establishes whether all MVR reviews occurred.")

add("gl_subcontract_limit_unknown", "missing_information", "general_liability",
    "Record a strength if every active roofing subcontractor maintains at least $2 million of general liability limits.", "strength", [
        ("contractor:schedule", "Elm Renovation uses two active roofing subcontractors, North Roof and Ridge Team. Both are marked insured in the vendor register. The register does not record limits or policy numbers.", "Active subcontractor population is complete for this assessment."),
        ("broker:certificate_request", "Certificates for both roofing subcontractors have been requested but not received. Their general liability limits have not been confirmed.", "Insured status alone is not an attestation of a particular limit.")],
    "insufficient_evidence", [], [], "Unspecified insurance limits cannot satisfy or disprove the $2 million requirement.")

add("auto_incident_rate_calculation", "quantitative_boundaries", "commercial_auto",
    "Flag one fleet-level concern if 2025 preventable collision frequency exceeds 10 collisions per 100 active vehicles. Use the stated active fleet count as denominator.", "concern", [
        ("lossrun:2025", "Summit Couriers recorded three preventable collisions during 2025. Two additional glass-only claims were not collisions. These counts are final for the full calendar year.", "Preventable collision count is three; do not include the glass claims."),
        ("fleet:2025", "Summit operated 24 active vehicles throughout 2025. Four spare vehicles held in storage were not active and are outside the stated active fleet count.", "Denominator requested by the guideline is 24.")],
    "matched", ["E1", "E2"], [["E1", "E2"]], "Three divided by 24 times 100 is 12.5, above 10. This is one aggregate finding, not three separate collision findings.")

add("property_reserves_exact_threshold", "quantitative_boundaries", "property",
    "Record a strength if Bay Storage holds unrestricted cash reserves covering at least four months of its stated operating expense.", "strength", [
        ("finance:certified", "Bay Storage's certified schedule reports unrestricted cash of $480,000 and monthly operating expense of $120,000 as of 2025-08-31. Restricted tenant deposits are reported separately and are excluded from cash above.", "Both values use USD; the supplied expense is the denominator for this guideline.")],
    "matched", ["E1"], [["E1"]], "480,000 / 120,000 equals exactly four months; at least includes equality.")

add("property_roof_exact_boundary", "quantitative_boundaries", "property",
    "Flag a concern if the roof at Unit 7 is strictly older than 20 years on the assessment date of 2025-07-01.", "concern", [
        ("survey:unit7", "Unit 7's roof was installed on 2005-07-01. The survey dated 2025-07-01 records an age of exactly 20 years. It is a single roof with no later overlay or separate roof section.", "Assessment date and documented age are aligned.")],
    "no_match", ["E1"], [], "Exactly 20 does not exceed a strictly greater-than-20 threshold.")

add("cyber_patch_coverage_boundary", "quantitative_boundaries", "cyber",
    "Record a strength if at least 95% of the 100 in-scope servers have all critical patches installed within 14 days of release.", "strength", [
        ("security:patch_export", "The signed August patch summary covers all 100 in-scope servers. Ninety-five met the 14-day critical-patch deadline, three were patched on day 20, and two remain outstanding. Desktop endpoints are listed in a separate report.", "Use only the 100 servers in this complete summary; assessment date 2025-09-01.")],
    "matched", ["E1"], [["E1"]], "95/100 equals 95%, meeting an inclusive threshold despite five exceptions.")

add("property_alarm_equal_reports", "unresolved_conflict", "property",
    "Flag a concern if the monitored fire alarm at Orchard Packaging was offline at 10:00 on 2025-06-12.", "concern", [
        ("alarm:provider_a", "Orchard Packaging, account OP-11: central monitoring status was OFFLINE at 10:00 on 2025-06-12. This is the final signed export for the site and timestamp.", "Provider A and B reports have equal stated authority. No correction, clock offset, or precedence is documented."),
        ("alarm:provider_b", "Orchard Packaging, account OP-11: central monitoring status was ONLINE at 10:00 on 2025-06-12. This is the final signed export for the site and timestamp.", "Same site and time as Provider A; the conflict is unexplained.")],
    "insufficient_evidence", ["E1", "E2"], [], "Equal-authority incompatible observations of the same state require abstention and both citations.")

add("cyber_backup_immutability_conflict", "unresolved_conflict", "cyber",
    "Record a strength if the production backup vault had immutable retention enabled on 2025-08-31.", "strength", [
        ("security:signed_attestation", "The security lead attests that production vault PV-3 had immutable retention enabled throughout 2025-08-31. The vault holds the applicant's accounting backups.", "Signed on 2025-09-01. No precedence over the infrastructure attestation is specified."),
        ("infrastructure:signed_attestation", "The infrastructure lead attests that immutable retention on production vault PV-3 was disabled throughout 2025-08-31. No other production backup vault was in use.", "Signed on 2025-09-01. Both attestations concern the same configuration and period.")],
    "insufficient_evidence", ["E1", "E2"], [], "Contradictory same-period attestations cannot be resolved by source votes or department titles.")

add("auto_mileage_corrected_denominator", "temporal_and_corrections", "commercial_auto",
    "Flag one concern if Northline's 2025 preventable collision rate exceeds two per million miles. Use the final corrected mileage when an explicit correction exists.", "concern", [
        ("lossrun:northline", "Northline's final calendar-2025 loss run contains three preventable collisions and no disputed collision classification.", "All events are within the requested year."),
        ("fleet:original_mileage", "The initial 2025 mileage statement reported 1,000,000 miles. It was issued before the fleet accountant completed reconciliation of the odometer uploads.", "This is the original version, not an independently verified final total."),
        ("fleet:signed_correction", "The fleet accountant's signed correction explicitly supersedes the original 2025 statement: actual calendar-2025 mileage was 2,000,000. The original upload omitted half of the vehicles; the collision count is unchanged.", "Correction issued 2026-01-20 for the same 2025 exposure period.")],
    "no_match", ["E1", "E3"], [], "Three per two million equals 1.5 per million, below two; the explicit correction controls the denominator.")

add("property_later_repair_does_not_rewrite_history", "temporal_and_corrections", "property",
    "Flag a concern if Cedar Depot's sprinkler system was impaired on the historical assessment date 2025-03-01. Later repair does not alter that historical condition.", "concern", [
        ("inspection:historical", "At Cedar Depot on 2025-03-01, the inspector found the sprinkler control valve seized closed and the sprinkler system impaired. The impairment notice was issued the same day.", "Historical condition at the exact assessment date."),
        ("contractor:repair", "On 2025-03-05 the contractor replaced the seized valve and restored the sprinkler system. This certificate describes a repair completed on March 5, not a correction to the March 1 impairment report.", "Restoration occurred four days after the requested date.")],
    "matched", ["E1"], [["E1"],], "The historical impairment remains a concern; a later repair is a state change, not a correction.", alternatives=[[["E1"], ["E1", "E2"]]])

add("property_electrical_exception", "exceptions_and_scope", "property",
    "Flag a concern for a building constructed before 1960 unless a licensed contractor documents complete replacement of its original electrical wiring after 2010.", "concern", [
        ("schedule:building", "The sole insured building at Willow Print was constructed in 1952 and remains in active use. Its floor area is 18,000 square feet; the application lists routine cosmetic renovation in 2022.", "Cosmetic renovation alone does not establish wiring replacement."),
        ("electrical:completion", "A licensed electrical contractor certifies that all original electrical wiring throughout Willow Print's insured building was removed and replaced in 2018. The completion certificate covers the entire building, including concealed branch circuits.", "This is full replacement, not inspection or partial rewiring.")],
    "no_match", ["E1", "E2"], [], "The age trigger applies but the documented complete replacement establishes the explicit exception.")

add("cyber_service_account_exception", "exceptions_and_scope", "cyber",
    "Flag a concern for an account without MFA, except a noninteractive service account with interactive login disabled and a documented credential rotation interval no longer than 30 days.", "concern", [
        ("identity:account", "Account invoice-sync lacks MFA. It is a noninteractive integration account; interactive login is disabled by policy and configuration. The applicant's human accounts are outside this account-specific review.", "Assess only invoice-sync."),
        ("security:rotation", "The credential management log for invoice-sync shows a documented automatic rotation interval of 14 days. The administrator confirms the policy is active rather than merely planned.", "Same account as the identity export.")],
    "no_match", ["E1", "E2"], [], "Both exception requirements are established, so lack of MFA does not trigger the concern for this account.")

add("gl_hot_work_scope_exclusion", "exceptions_and_scope", "general_liability",
    "This criterion applies only to contractors performing on-site welding or flame cutting at customers' premises. Flag a concern if they lack a documented hot-work permit procedure.", "concern", [
        ("operations:attestation", "Pine Design provides remote CAD drafting only. It does not perform fabrication, installation, welding, flame cutting, or physical work at customer sites. All deliverables are electronic files.", "Signed complete description of applicant operations for the policy period.")],
    "not_applicable", ["E1"], [], "The explicit operational scope excludes this applicant; a missing permit manual is irrelevant.")

add("auto_passenger_scope_exclusion", "exceptions_and_scope", "commercial_auto",
    "For vehicles carrying passengers for hire, flag a concern if emergency evacuation training is not completed annually.", "concern", [
        ("fleet:operations", "Granite Freight operates five box trucks carrying packaged commercial goods. It does not transport passengers for hire. Drivers and incidental employee helpers are the only occupants.", "This attestation covers the entire insured fleet and current operations.")],
    "not_applicable", ["E1"], [], "Freight-only operations are outside the explicit passengers-for-hire scope.")

add("property_multiple_warehouse_concerns", "multiple_and_corroborated_findings", "property",
    "Record a separate concern for each occupied storage warehouse lacking automatic sprinklers. Office-only buildings are outside this criterion.", "concern", [
        ("survey:east", "East Warehouse stores finished plastic goods, is occupied daily, and has no automatic sprinklers. Portable extinguishers are present at the exits.", "This is an insured storage warehouse, not an office."),
        ("survey:west", "West Warehouse stores cardboard cartons and is occupied on both shifts. It has no automatic sprinklers; a sprinkler installation is proposed for next year but is not complete.", "Current condition, not planned improvements."),
        ("schedule:office", "The administration building is occupied but used solely as an office, with no warehouse storage operations. It has no automatic sprinklers.", "Separate office-only building.")],
    "matched", ["E1", "E2"], [["E1"], ["E2"]], "East and West qualify independently; extinguishers and future plans do not satisfy the condition, and the office is excluded.")

add("auto_multiple_expired_licences", "multiple_and_corroborated_findings", "commercial_auto",
    "Record a separate concern for each currently employed driver whose licence expired before 2025-09-01 and has not been renewed by that date.", "concern", [
        ("hr:driver_a", "Driver A is a currently employed delivery driver. The verified licence expired on 2025-07-31, and the licensing check confirms it remained unrenewed on 2025-09-01.", "Fictional driver label; same assessment date as the criterion."),
        ("hr:driver_b", "Driver B is a currently employed delivery driver. The verified licence expired on 2025-08-15, and the licensing check confirms no renewal as of 2025-09-01.", "Separate employed driver."),
        ("hr:driver_c", "Driver C remains employed and holds a licence valid through 2027-02-01. The next routine licence check is scheduled for the following quarter.", "A valid licence does not qualify as a concern.")],
    "matched", ["E1", "E2"], [["E1"], ["E2"]], "Two independently identified employees meet the concern; Driver C does not.")

add("cyber_multiple_restore_strengths", "multiple_and_corroborated_findings", "cyber",
    "Record a separate strength for each business-critical application with a completed restore test within the last 90 days and a demonstrated recovery time no longer than four hours. Assess as of 2025-09-01.", "strength", [
        ("test:billing", "Billing is designated business-critical. Its full restore test completed on 2025-08-10 with measured recovery time of 3 hours. Production data integrity checks passed, and this was a completed test rather than a tabletop exercise.", "All details refer to the billing application."),
        ("test:inventory", "Inventory is designated business-critical. Its full restore test completed on 2025-07-20 with measured recovery time of exactly 4 hours. The test restored the complete application and passed integrity checks.", "Separate application; four hours is inclusive.")],
    "matched", ["E1", "E2"], [["E1"], ["E2"]], "Each application independently meets both timing conditions and warrants its own strength.")

add("property_corroboration_not_two_events", "multiple_and_corroborated_findings", "property",
    "Record a strength for each standby generator successfully tested under full building load during August 2025. Multiple reports of the same test are one finding.", "strength", [
        ("contractor:test", "Generator G-1 at Birch Cold Storage successfully supplied full building load during its completed test on 2025-08-12. This is the site's only standby generator and its only August full-load test.", "Signed contractor record of test T-118."),
        ("engineer:verification", "The site engineer independently confirms that generator G-1 successfully supplied full building load during test T-118 on 2025-08-12. This note corroborates the contractor report of that same test.", "Same generator and event, not an additional test.")],
    "matched", [], [["E1"]], "One generator/test warrants one finding; either source independently supports it and both may be cited together.", alternatives=[[["E1"], ["E2"], ["E1", "E2"]]])

add("gl_sister_company_evidence", "entity_and_period_alignment", "general_liability",
    "Flag a concern if the named applicant, Aspen Foods LLC, had a product recall during 2025.", "concern", [
        ("broker:corporate_chart", "The named applicant is Aspen Foods LLC. Aspen Beverage LLC is a separate sister company, not included as an insured in this submission. Both companies share a holding company and street address.", "Do not transfer operating events between legal entities."),
        ("news:recall_summary", "Aspen Beverage LLC recalled a beverage product in May 2025. The summary gives no recall history for Aspen Foods LLC, and the applicant's own recall response remains unanswered.", "The event belongs to the separate sister company.")],
    "insufficient_evidence", [], [], "A sister company's recall is not evidence of the applicant's recall history; absence of applicant records is not proof of no recall.")

add("cyber_prior_year_does_not_prove_current", "entity_and_period_alignment", "cyber",
    "Record a strength if all business-critical systems had tested offline backups during calendar 2025.", "strength", [
        ("audit:2024", "The 2024 audit confirmed tested offline backups for all business-critical systems in calendar 2024. The audit does not cover subsequent periods.", "Report date 2025-01-15 does not change its 2024 coverage period."),
        ("broker:2025_update", "The client migrated storage platforms in March 2025. The 2025 backup test records and offline-storage configuration have not yet been supplied, and current effectiveness is unverified.", "No attestation that the prior configuration remained in place.")],
    "insufficient_evidence", [], [], "A previous-year control assessment and unknown post-migration controls cannot establish the current-year requirement.")

add("property_building_specific_scope", "entity_and_period_alignment", "property",
    "For Building A only, this criterion applies if its structural frame is combustible wood. Flag a concern if that building lacks automatic sprinklers.", "concern", [
        ("survey:a", "Building A has a steel structural frame and concrete external walls. It has no automatic sprinklers. The engineer confirms there is no combustible wood structural frame in Building A.", "The criterion is explicitly restricted to Building A."),
        ("survey:b", "Building B on the same campus has a combustible wood structural frame and no sprinklers. It is a separate insured building with its own survey.", "Building B is not the subject of this criterion.")],
    "not_applicable", ["E1"], [], "Building A fails the wood-frame applicability condition; Building B cannot make an A-specific rule applicable.")

add("wc_partial_payroll_period", "entity_and_period_alignment", "workers_compensation",
    "Flag a concern if the insured's total overtime hours exceed 15% of all hours worked during the full 2025 calendar year.", "concern", [
        ("payroll:q1", "The insured's January-March 2025 payroll summary shows 2,000 overtime hours and 10,000 total hours worked. It covers only the first quarter, when a temporary order increased production.", "Numerator and denominator are both Q1, not annual figures."),
        ("payroll:request", "The April-December 2025 hours have not been supplied. The applicant has not provided an annual total or stated that the first-quarter rate continued.", "Full-year exposure cannot be inferred by annualizing a temporary quarter.")],
    "insufficient_evidence", [], [], "A 20% quarter does not establish the full-year rate when the remaining nine months are unknown.")

add("gl_document_submission_condition", "documentation_vs_activity", "general_liability",
    "Record a strength if signed hold-harmless agreements for every active subcontractor were supplied with this submission. This rule evaluates document submission itself.", "strength", [
        ("intake:complete_receipt", "The completed submission inventory confirms that no signed hold-harmless agreements were supplied for any of the three active subcontractors. The inventory covers all received attachments, not a partial folder search.", "The agreements may or may not exist elsewhere; this statement establishes what was submitted.")],
    "no_match", ["E1"], [], "Confirmed nonsubmission disproves a submission-specific strength without assuming no agreements exist.")

add("wc_document_absence_is_concern", "documentation_vs_activity", "workers_compensation",
    "Flag a concern if the submission lacks the required current written machine lockout procedure. Evaluate the presence of that document in the completed submission, not whether workers follow a procedure.", "concern", [
        ("intake:document_inventory", "The intake reviewer checked the complete final submission for Delta Fabrication. It includes payroll, a loss run, and an equipment list, but the required current written lockout procedure was not supplied.", "Complete submission inventory; the document request is a stated criterion requirement.")],
    "matched", ["E1"], [["E1"]], "This criterion explicitly targets a missing submission document, so its confirmed absence supports a concern.")

add("wc_activity_explicitly_not_performed", "documentation_vs_activity", "workers_compensation",
    "Record a strength if every newly hired production employee received machine-safety induction before first operating production equipment in 2025.", "strength", [
        ("manager:signed_declaration", "The plant manager confirms that two newly hired production employees first operated production equipment on 2025-05-02 without receiving machine-safety induction. Induction was subsequently completed on 2025-05-08.", "Explicit observation of timing; this is not merely missing training paperwork.")],
    "no_match", ["E1"], [], "The explicit delayed induction disproves the all-employees pre-operation requirement despite later completion.")

add("property_inspection_date_unknown", "documentation_vs_activity", "property",
    "Flag a concern if the last completed electrical thermographic inspection at Fern Mill was more than 12 months before 2025-09-01.", "concern", [
        ("maintenance:records", "Fern Mill cannot locate the date of its last completed electrical thermographic inspection. Some contractor records were lost during a server migration. The facilities manager cannot confirm when the work was last completed.", "Missing dates and lost records do not establish an overdue inspection."),
        ("survey:visual", "The electrical rooms were tidy at the August site survey. No visible scorching was observed. The survey did not include thermographic testing or verify the date of any earlier test.", "Visual observations do not establish the requested elapsed time.")],
    "insufficient_evidence", [], [], "Without the last-completed date, the twelve-month condition is unknown.")

add("property_cross_source_alarm_and_value", "cross_source_synthesis", "property",
    "Record one strength if the entire insured stock is in a continuously monitored intruder-alarm area and the total declared stock value is no greater than $500,000.", "strength", [
        ("stock:declaration", "Haven Parts declares total insured stock of $425,000 as of 2025-09-01. All stock, including seasonal overflow, is held inside its sole insured warehouse. There is no outdoor or off-site stock.", "USD; the declaration is complete for all insured stock."),
        ("security:certificate", "The alarm contractor certifies that the entire interior of Haven Parts' sole warehouse is covered by an intruder alarm with continuous remote monitoring. The system was active on 2025-09-01.", "Scope includes all warehouse storage areas.")],
    "matched", ["E1", "E2"], [["E1", "E2"]], "The value and whole-stock alarm condition require combining both sources into one strength.")

add("gl_loss_aggregation_without_duplicate", "cross_source_synthesis", "general_liability",
    "Flag one concern if total paid amounts for distinct 2025 general liability claims exceed $300,000. Count each claim ID once, using its latest stated paid amount.", "concern", [
        ("lossrun:primary", "The final 2025 general liability loss run lists claim GL-101 with paid amount $150,000 and claim GL-102 with paid amount $175,000. These are separate claims, both incurred during 2025. There are no other 2025 GL claims.", "All values USD, paid amounts rather than incurred reserves."),
        ("broker:claim_note", "The broker's separate note repeats claim GL-101 at its same latest paid amount of $150,000. This is a duplicate reference to GL-101, not an additional claim or additional payment.", "Duplicate identification is explicit.")],
    "matched", ["E1"], [["E1"]], "Distinct claims sum to $325,000, above $300,000. Do not add the repeated GL-101 again or create a finding per claim.", alternatives=[[["E1"], ["E1", "E2"]]])

add("cyber_restore_duration_cross_midnight", "cross_source_synthesis", "cyber",
    "Record a strength if the completed full restore of the payroll application took no longer than 24 hours. Compute elapsed time using the supplied UTC start and completion timestamps.", "strength", [
        ("restore:start_log", "The payroll application's full restore began at 2025-08-01 08:00 UTC. This timestamp is the start of actual restoration, not the time the incident was reported.", "Use UTC; there were no clock corrections."),
        ("restore:completion_log", "The full payroll application restore completed at 2025-08-02 09:30 UTC and passed verification. The team had previously restored a small test folder, but that was not the full application restore.", "Use the full application's completion time.")],
    "no_match", ["E1", "E2"], [], "Elapsed time is 25.5 hours, exceeding the 24-hour maximum despite a successful eventual restore.")

add("property_expired_exception_certificate", "cross_source_synthesis", "property",
    "Flag a concern for combustible stock stacked above four metres, except where an engineer's specific high-stack approval remains valid on 2025-09-01.", "concern", [
        ("survey:stack_height", "At Linden Distribution on 2025-09-01, combustible packaged stock was stacked to 5.2 metres. The applicant refers the surveyor to its engineer's high-stack approval for this storage area.", "Height and storage-area identity were measured and verified."),
        ("engineer:approval", "The approval for Linden's same storage area explicitly allowed stacks up to 5.5 metres but expired on 2025-06-30. The engineer confirms no renewal or extension was issued before 2025-09-01.", "The approval's stated validity is material; its height limit alone is insufficient.")],
    "matched", ["E1", "E2"], [["E1", "E2"]], "The height trigger is met and the explicit approval exception is unavailable on the assessment date.")


if __name__ == "__main__":
    target = Path(__file__).with_name("unseen_cases_v1.json")
    if target.exists():
        raise SystemExit("Refusing to overwrite the frozen dataset")
    target.write_text(json.dumps({"version": 1, "description": "32 newly authored synthetic underwriting scenarios. Invented rules, thresholds, companies, and observations; not expert-validated. One criterion per case; assessed evidence is already extracted. Freeze before any model run.", "cases": cases}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(cases)} cases to {target}")
