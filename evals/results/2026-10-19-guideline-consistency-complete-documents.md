# First-use long-document holdout

State: **completed**

Synthetic, author-labeled cases frozen before inference. Production code is unchanged. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 3/3 | 3/3 | 2/3 | 3/3 | False | False | False |
| cyber | 618 / 1424 | 3/3 | 3/3 | 3/3 | 0/3 | True | False | False |
| fleet | 632 / 1452 | 3/3 | 3/3 | 3/3 | 3/3 | False | False | True |
| manufacturing | 636 / 1419 | 3/3 | 3/3 | 3/3 | 0/3 | True | False | False |
| hospitality | 635 / 1427 | 3/3 | 3/3 | 3/3 | 0/3 | True | False | False |
| contractor | 640 / 1425 | 3/3 | 2/3 | 3/3 | 0/3 | True | True | False |

## property

Error: `None`; judge error: `None`.

### G1 (explicit)

[concern] A cold-storage building whose roof is more than 25 years old is a concern unless a complete roof replacement has been documented within the last 2 years.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: Identify North and South separately: 28 and 31 exceed 25, with no replacement exception. East is excluded by its documented replacement/current age.

Candidate:

Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, as identified in E2. The assessment date is 30 September 2026, and the relevant period is the time up to that date. For North building (E8): roof age is 28 years, which is greater than 25 years. No complete replacement has occurred, so this building meets the trigger condition for concern. For South building (E9): roof age is 31 years, which is greater than 25 years. No complete replacement has occurred, so this building also meets the trigger condition for concern. For East building (E10): roof age is 0 years because a complete replacement occurred on 1 March 2026. Since this replacement was within the last 2 years (as of 30 September 2026), this building does not meet the trigger condition for concern. The rule states an exception: 'unless a complete roof replacement has been documented within the last 2 years.' For North and South buildings, no such documentation exists. For East building, a complete replacement was documented on 1 March 2026, which is within the last 2 years (as of 30 September 2026). Therefore, the exception applies to East building but not to North or South. There are no conflicting observations regarding roof age or replacement documentation for any of the buildings. The information is clear and consistent across the evidence provided.
Finding: The North building has a roof that is 28 years old, which exceeds the 25-year threshold. No complete roof replacement has been documented within the last 2 years, so it meets the trigger condition for concern.
Finding: The South building has a roof that is 31 years old, which exceeds the 25-year threshold. No complete roof replacement has been documented within the last 2 years, so it meets the trigger condition for concern.
scope_reason: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, as identified in E2. The assessment date is 30 September 2026, and the relevant period is the time up to that date.
condition_reason: For North building (E8): roof age is 28 years, which is greater than 25 years. No complete replacement has occurred, so this building meets the trigger condition for concern. For South building (E9): roof age is 31 years, which is greater than 25 years. No complete replacement has occurred, so this building also meets the trigger condition for concern. For East building (E10): roof age is 0 years because a complete replacement occurred on 1 March 2026. Since this replacement was within the last 2 years (as of 30 September 2026), this building does not meet the trigger condition for concern.
exception_reason: The rule states an exception: 'unless a complete roof replacement has been documented within the last 2 years.' For North and South buildings, no such documentation exists. For East building, a complete replacement was documented on 1 March 2026, which is within the last 2 years (as of 30 September 2026). Therefore, the exception applies to East building but not to North or South.
conflict_reason: There are no conflicting observations regarding roof age or replacement documentation for any of the buildings. The information is clear and consistent across the evidence provided.

- rule_application: 2/2. Correctly identifies that the rule applies to individual buildings and correctly lists the relevant buildings (North, South, East) as specified in the evidence. Excerpt: "Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, as identified in E2."
- factual_grounding: 2/2. Accurately cites roof ages and replacement dates from evidence E8, E9, and E10, correctly applying the rule's threshold of 25 years and the exception for replacements within the last two years. Excerpt: "For North building (E8): roof age is 28 years, which is greater than 25 years. No complete replacement has occurred, so this building meets the trigger condition for concern. For South building (E9): roof age is 31 years, which is greater than 25 years. No complete replacement has occurred, so this building also meets the trigger condition for concern. For East building (E10): roof age is 0 years because a complete replacement occurred on 1 March 2026."
- scope_and_exceptions: 2/2. Correctly identifies and applies the exception for the East building while clearly explaining why North and South do not qualify under the exception. Excerpt: "The rule states an exception: 'unless a complete roof replacement has been documented within the last 2 years.' For North and South buildings, no such documentation exists. For East building, a complete replacement was documented on 1 March 2026, which is within the last 2 years (as of 30 September 2026). Therefore, the exception applies to East building but not to North or South."
- logical_support: 2/2. Provides clear logical reasoning that connects roof age and replacement dates directly to the rule's trigger and exception conditions. Excerpt: "For North and South buildings, no such documentation exists. For East building, a complete replacement was documented on 1 March 2026, which is within the last 2 years (as of 30 September 2026). Therefore, the exception applies to East building but not to North or South."
- no_unsupported_claims: 2/2. Asserts consistency in the evidence without introducing unsupported claims or contradictions. Excerpt: "There are no conflicting observations regarding roof age or replacement documentation for any of the buildings. The information is clear and consistent across the evidence provided."
### G2 (explicit)

Current sprinkler inspection certificates with no outstanding deficiencies for every cold-storage building are a strength.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: All three buildings have current certificates and no deficiencies; the all-buildings requirement is established.

Candidate:

Assessment: The rule applies to all cold-storage buildings, which are North, South, and East. The assessment date is 30 September 2026. Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations indicating outstanding deficiencies for any of the buildings. The rule does not contain an explicit exception. The absence of an exception means that the standard condition applies without qualification. There are no conflicting observations regarding the sprinkler inspection certificates or deficiencies for any of the buildings. All three buildings have current certificates with no outstanding deficiencies recorded.
Finding: The sprinkler inspection certificate for the North building records no outstanding deficiencies, satisfying the condition.
Finding: The sprinkler inspection certificate for the South building records no outstanding deficiencies, satisfying the condition.
Finding: The sprinkler inspection certificate for the East building records no outstanding deficiencies, satisfying the condition.
scope_reason: The rule applies to all cold-storage buildings, which are North, South, and East. The assessment date is 30 September 2026.
condition_reason: Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations indicating outstanding deficiencies for any of the buildings.
exception_reason: The rule does not contain an explicit exception. The absence of an exception means that the standard condition applies without qualification.
conflict_reason: There are no conflicting observations regarding the sprinkler inspection certificates or deficiencies for any of the buildings. All three buildings have current certificates with no outstanding deficiencies recorded.

- rule_application: 2/2. Correctly identifies that the rule applies to all buildings and lists the relevant ones. Excerpt: "Assessment: The rule applies to all cold-storage buildings, which are North, South, and East."
- factual_grounding: 2/2. Accurately cites evidence E22 and correctly applies it to support the rule's conditions. Excerpt: "Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings."
- scope_and_exceptions: 2/2. Correctly identifies that no exception exists and appropriately applies the standard condition to all buildings. Excerpt: "The rule does not contain an explicit exception. The absence of an exception means that the standard condition applies without qualification."
- logical_support: 2/2. Logically connects the evidence to the rule's conditions without ambiguity. Excerpt: "Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings."
- no_unsupported_claims: 2/2. Asserts consistency in evidence without introducing unsupported claims. Excerpt: "There are no conflicting observations regarding the sprinkler inspection certificates or deficiencies for any of the buildings. All three buildings have current certificates with no outstanding deficiencies recorded."
### G3 (explicit)

[concern] A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.

Expected `no_match`; actual `no_match`. Explanation: 10/10 (graded).

Reference: The panels meet the trigger, but current independent approval for all three makes the stated exception apply; do not claim the panels are noncombustible.

Candidate:

Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, all of which are within the scope of the evaluation. All three buildings (North, South, and East) have combustible insulated wall panels. Each building has a current independent fire-engineering certification that approves those panels. The condition is supported by E32 which states: 'All three buildings have combustible insulated wall panels; current independent fire-engineering certification approves those panels in North, South, and East.' The rule has an exception that applies when a current independent fire-engineering certification approves the combustible insulated wall panels. Since all three buildings have such certifications, the exception applies to each building. There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of current independent fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible insulated wall panels and that each has a current independent fire-engineering certification approving those panels.
scope_reason: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, all of which are within the scope of the evaluation.
condition_reason: All three buildings (North, South, and East) have combustible insulated wall panels. Each building has a current independent fire-engineering certification that approves those panels. The condition is supported by E32 which states: 'All three buildings have combustible insulated wall panels; current independent fire-engineering certification approves those panels in North, South, and East.'
exception_reason: The rule has an exception that applies when a current independent fire-engineering certification approves the combustible insulated wall panels. Since all three buildings have such certifications, the exception applies to each building.
conflict_reason: There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of current independent fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible insulated wall panels and that each has a current independent fire-engineering certification approving those panels.

- rule_application: 2/2. Correctly identifies that the rule applies to individual buildings and lists all relevant ones. Excerpt: "Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, all of which are within the scope of the evaluation."
- factual_grounding: 2/2. Accurately cites evidence E32 and correctly applies it to the rule's conditions. Excerpt: "All three buildings (North, South, and East) have combustible insulated wall panels. Each building has a current independent fire-engineering certification that approves those panels. The condition is supported by E32 which states: 'All three buildings have combustible insulated wall panels; current independent fire-engineering certification approves those panels in North, South, and East.'"
- scope_and_exceptions: 2/2. Correctly identifies and applies the exception for all three buildings. Excerpt: "The rule has an exception that applies when a current independent fire-engineering certification approves the combustible insulated wall panels. Since all three buildings have such certifications, the exception applies to each building."
- logical_support: 2/2. Logically connects the presence of certifications to the rule's exception, correctly concluding that no concern is raised. Excerpt: "Since all three buildings have such certifications, the exception applies to each building."
- no_unsupported_claims: 2/2. Asserts consistency in evidence without introducing unsupported claims. Excerpt: "There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of current independent fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible insulated wall panels and that each has a current independent fire-engineering certification approving those panels."

## cyber

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[strength] MFA on every active privileged account is a strength.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: 23/24 is not every account. The active emergency account is in scope and there is no exception; this is affirmative failure, not missing evidence.

Candidate:

Assessment: The rule applies to active privileged accounts within the scope of the assessment. The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. The remaining account is an active emergency administrator without MFA. The evidence states that 'MFA is enabled for 23 of the 24 active privileged accounts; the remaining account is an active emergency administrator without MFA.' This means that not every active privileged account has MFA enabled, which contradicts the trigger condition. Therefore, the rule's trigger does not hold true. The rule does not contain any explicit exception prerequisites or validity dates mentioned in the text. There is no indication of an exception applying to this case. There are no conflicting observations regarding MFA status on privileged accounts. The evidence clearly states that 23 out of 24 accounts have MFA enabled, and one does not. This is a straightforward factual discrepancy rather than an unresolved conflict.
scope_reason: The rule applies to active privileged accounts within the scope of the assessment. The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. The remaining account is an active emergency administrator without MFA.
condition_reason: The evidence states that 'MFA is enabled for 23 of the 24 active privileged accounts; the remaining account is an active emergency administrator without MFA.' This means that not every active privileged account has MFA enabled, which contradicts the trigger condition. Therefore, the rule's trigger does not hold true.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates mentioned in the text. There is no indication of an exception applying to this case.
conflict_reason: There are no conflicting observations regarding MFA status on privileged accounts. The evidence clearly states that 23 out of 24 accounts have MFA enabled, and one does not. This is a straightforward factual discrepancy rather than an unresolved conflict.

### G2 (explicit)

A successful isolated recovery test within the last 90 days is a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: 15 August is 46 days before 30 September, within 90; a successful isolated test is recorded.

Candidate:

Assessment: The rule applies to the subject of cyber security controls for the payroll service provider. The period in scope is the time around the assessment date 30 September 2026, as the rule refers to tests 'within the last 90 days'. The evidence E21 states: 'An isolated payroll recovery test succeeded on 15 August 2026; the test log records restored data and a successful application start.' The test occurred on 15 August 2026, which is within 90 days of the assessment date 30 September 2026. Therefore, the condition is supported by evidence. There is no explicit exception stated in the rule text for C2. The rule does not contain any 'unless' or 'except' clauses that would apply to this case. There are no conflicting observations regarding the isolated recovery test in the provided evidence. The single observation confirms a successful test within the required timeframe.
Finding: An isolated payroll recovery test was successfully completed on 15 August 2026, which falls within the last 90 days prior to the assessment date of 30 September 2026. This satisfies the condition for a strength as defined by rule C2.
scope_reason: The rule applies to the subject of cyber security controls for the payroll service provider. The period in scope is the time around the assessment date 30 September 2026, as the rule refers to tests 'within the last 90 days'.
condition_reason: The evidence E21 states: 'An isolated payroll recovery test succeeded on 15 August 2026; the test log records restored data and a successful application start.' The test occurred on 15 August 2026, which is within 90 days of the assessment date 30 September 2026. Therefore, the condition is supported by evidence.
exception_reason: There is no explicit exception stated in the rule text for C2. The rule does not contain any 'unless' or 'except' clauses that would apply to this case.
conflict_reason: There are no conflicting observations regarding the isolated recovery test in the provided evidence. The single observation confirms a successful test within the required timeframe.

### G3 (implicit)

Refer any account that stores unencrypted portable copies of payroll data for adverse treatment.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: Unencrypted portable payroll copies meet the referral rule; the guideline's vocabulary maps adverse treatment to concern.

Candidate:

Assessment: The rule applies to accounts storing unencrypted portable copies of payroll data. The subject is the applicant's storage of payroll data on portable USB drives. The period in scope is the current assessment date 30 September 2026. Evidence E31 states that 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence confirms the presence of unencrypted payroll data on portable drives, which meets the rule's requirement. The rule does not contain an explicit exception. There is no stated exception that would apply to this situation. There are no conflicting observations regarding the storage of unencrypted payroll data on portable USB drives. The evidence clearly establishes that two USB drives hold unencrypted payroll exports.
Finding: Two portable USB drives store unencrypted payroll exports used by the support team, which meets the rule's trigger condition for referring accounts that store unencrypted portable copies of payroll data.
scope_reason: The rule applies to accounts storing unencrypted portable copies of payroll data. The subject is the applicant's storage of payroll data on portable USB drives. The period in scope is the current assessment date 30 September 2026.
condition_reason: Evidence E31 states that 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence confirms the presence of unencrypted payroll data on portable drives, which meets the rule's requirement.
exception_reason: The rule does not contain an explicit exception. There is no stated exception that would apply to this situation.
conflict_reason: There are no conflicting observations regarding the storage of unencrypted payroll data on portable USB drives. The evidence clearly establishes that two USB drives hold unencrypted payroll exports.


## fleet

Error: `None`; judge error: `None`.

### G1 (explicit)

[concern] A heavy goods vehicle with an unresolved brake defect is a concern.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 10/10 (graded).

Reference: The equally authoritative H7 records conflict for the same date with no correction; abstain rather than select one report or emit a settled concern.

Candidate:

Assessment: The rule applies to heavy goods vehicles. The evidence mentions eight heavy goods vehicles, with vehicle H7 being the only one with a disputed brake defect. The assessment date is 30 September 2026. Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect (E8). Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other (E9). The two inspections are contemporaneous and contradictory, with no correction provided. This creates an unresolved factual disagreement about the brake defect status of vehicle H7. Since the rule requires an 'unresolved' brake defect to constitute a concern, and there is such an unresolved defect for vehicle H7, the condition is met. The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no stated conditions under which this rule would not apply. There is a factual contradiction between E8 (inspector A's report of unresolved brake defect) and E9 (inspector B's report of no brake defect) concerning vehicle H7. These observations are about the same subject (vehicle H7) and time period (29 September 2026), but they directly contradict each other without one correcting the other. This constitutes an unresolved conflict regarding the brake defect status of vehicle H7.
scope_reason: The rule applies to heavy goods vehicles. The evidence mentions eight heavy goods vehicles, with vehicle H7 being the only one with a disputed brake defect. The assessment date is 30 September 2026.
condition_reason: Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect (E8). Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other (E9). The two inspections are contemporaneous and contradictory, with no correction provided. This creates an unresolved factual disagreement about the brake defect status of vehicle H7. Since the rule requires an 'unresolved' brake defect to constitute a concern, and there is such an unresolved defect for vehicle H7, the condition is met.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no stated conditions under which this rule would not apply.
conflict_reason: There is a factual contradiction between E8 (inspector A's report of unresolved brake defect) and E9 (inspector B's report of no brake defect) concerning vehicle H7. These observations are about the same subject (vehicle H7) and time period (29 September 2026), but they directly contradict each other without one correcting the other. This constitutes an unresolved conflict regarding the brake defect status of vehicle H7.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to heavy goods vehicles, which is the relevant trigger for applying the rule in question. Excerpt: "Assessment: The rule applies to heavy goods vehicles."
- factual_grounding: 2/2. The excerpt accurately cites the specific evidence from the documents that supports the factual claims about the conflicting inspections. Excerpt: "Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect (E8). Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other (E9)."
- scope_and_exceptions: 2/2. This excerpt correctly identifies the absence of exceptions in the rule and confirms that no stated conditions prevent application. Excerpt: "The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no stated conditions under which this rule would not apply."
- logical_support: 2/2. The excerpt clearly explains that because the rule requires an unresolved defect and one exists, the condition is satisfied, providing logical support for the conclusion. Excerpt: "Since the rule requires an 'unresolved' brake defect to constitute a concern, and there is such an unresolved defect for vehicle H7, the condition is met."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by clearly stating that the contradiction exists and is unresolved, without introducing new assumptions or fabrications. Excerpt: "There is a factual contradiction between E8 (inspector A's report of unresolved brake defect) and E9 (inspector B's report of no brake defect) concerning vehicle H7. These observations are about the same subject (vehicle H7) and time period (29 September 2026), but they directly contradict each other without one correcting the other."
### G2 (explicit)

[strength] Completed annual driving-record reviews for all active drivers are a strength.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 10/10 (graded).

Reference: The register is missing. This does not prove that reviews were not performed; evidence is insufficient to establish all-driver coverage.

Candidate:

Assessment: The criterion requires that annual driving-record reviews be completed for all active drivers to constitute a strength. Evidence E22 explicitly states that the broker has requested but not received the annual driving-record review register. This absence of the required documentation means that it cannot be confirmed whether reviews were completed for all 18 active drivers. Since the necessary evidence is missing, a negative decision cannot be legitimately made based on the available information.

- rule_application: 2/2. The excerpt correctly identifies the rule's requirement and applies it appropriately to the context of driver reviews. Excerpt: "Assessment: The criterion requires that annual driving-record reviews be completed for all active drivers to constitute a strength."
- factual_grounding: 2/2. The excerpt accurately cites the evidence that supports the lack of documentation, grounding the explanation in factual data. Excerpt: "Evidence E22 explicitly states that the broker has requested but not received the annual driving-record review register."
- scope_and_exceptions: 2/2. The excerpt correctly acknowledges that the lack of evidence prevents a definitive conclusion, which aligns with the 'insufficient_evidence' status. Excerpt: "Since the necessary evidence is missing, a negative decision cannot be legitimately made based on the available information."
- logical_support: 2/2. The excerpt logically connects the missing evidence to the inability to confirm compliance, supporting the conclusion that evidence is insufficient. Excerpt: "This absence of the required documentation means that it cannot be confirmed whether reviews were completed for all 18 active drivers."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by clearly stating that a conclusion cannot be drawn due to lack of evidence. Excerpt: "Since the necessary evidence is missing, a negative decision cannot be legitimately made based on the available information."
### G3 (implicit)

Give favorable treatment when verified telematics show a harsh-braking rate below 2 events per 1000 miles across the active fleet.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: 54 / 36000 * 1000 = 1.5, strictly below 2. Favorable treatment maps to strength.

Candidate:

Assessment: The rule applies to the active fleet as a whole, and the evidence includes a verified active-fleet telematics report covering all heavy goods vehicles in operation. The subject is the entire fleet's harsh-braking rate during the reporting period. The verified active-fleet telematics report (E32) records 54 harsh-braking events over 36000 miles. Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile, or 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met. The rule does not contain an explicit exception clause that would apply to this case. There are no stated validity dates or prerequisites for exceptions in the rule text. There are no conflicting observations regarding the harsh-braking rate or fleet coverage in the provided evidence. The telematics data is presented as a single, verified report for the entire active fleet.
Finding: The verified active-fleet telematics report shows 54 harsh-braking events over 36000 miles, equating to 1.5 events per 1000 miles, which is below the threshold of 2 events per 1000 miles.
scope_reason: The rule applies to the active fleet as a whole, and the evidence includes a verified active-fleet telematics report covering all heavy goods vehicles in operation. The subject is the entire fleet's harsh-braking rate during the reporting period.
condition_reason: The verified active-fleet telematics report (E32) records 54 harsh-braking events over 36000 miles. Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile, or 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met.
exception_reason: The rule does not contain an explicit exception clause that would apply to this case. There are no stated validity dates or prerequisites for exceptions in the rule text.
conflict_reason: There are no conflicting observations regarding the harsh-braking rate or fleet coverage in the provided evidence. The telematics data is presented as a single, verified report for the entire active fleet.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to the entire fleet and that the evidence supports this application. Excerpt: "Assessment: The rule applies to the active fleet as a whole, and the evidence includes a verified active-fleet telematics report covering all heavy goods vehicles in operation."
- factual_grounding: 2/2. The excerpt accurately cites the specific data from the evidence that supports the factual claims. Excerpt: "The verified active-fleet telematics report (E32) records 54 harsh-braking events over 36000 miles."
- scope_and_exceptions: 2/2. The excerpt correctly identifies the absence of any exceptions in the rule, which is relevant to the scope. Excerpt: "The rule does not contain an explicit exception clause that would apply to this case. There are no stated validity dates or prerequisites for exceptions in the rule text."
- logical_support: 2/2. The excerpt provides clear arithmetic and logical reasoning to support that the condition is satisfied. Excerpt: "Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile, or 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by clearly stating that the data is verified and covers the entire fleet, without introducing assumptions. Excerpt: "The telematics data is presented as a single, verified report for the entire active fleet."

## manufacturing

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (implicit)

Decline operations using a production press without an interlocked guard.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: P4 is in use and unguarded; a proposed retrofit is not completion. Decline maps to concern.

Candidate:

Assessment: The rule applies to operations using a production press. The subject is the production press P4, which is mentioned in the technical exhibit (E8). The period in scope is the current assessment date of 30 September 2026. Evidence E8 states that 'Production press P4 remains in daily use without an interlocked guard; the proposed retrofit has not been ordered.' This directly supports the trigger condition that operations are being conducted using a production press without an interlocked guard. There is no evidence of an interlocked guard being installed or ordered. The rule does not contain any explicit exception prerequisites. Therefore, exception=does_not_apply. There are no conflicting observations regarding the presence or absence of an interlocked guard on production press P4. The evidence is clear that no interlocked guard is installed.
Finding: The production press P4 is in daily use without an interlocked guard, which directly triggers the rule's condition. No evidence exists of an interlocked guard being installed or ordered.
scope_reason: The rule applies to operations using a production press. The subject is the production press P4, which is mentioned in the technical exhibit (E8). The period in scope is the current assessment date of 30 September 2026.
condition_reason: Evidence E8 states that 'Production press P4 remains in daily use without an interlocked guard; the proposed retrofit has not been ordered.' This directly supports the trigger condition that operations are being conducted using a production press without an interlocked guard. There is no evidence of an interlocked guard being installed or ordered.
exception_reason: The rule does not contain any explicit exception prerequisites. Therefore, exception=does_not_apply.
conflict_reason: There are no conflicting observations regarding the presence or absence of an interlocked guard on production press P4. The evidence is clear that no interlocked guard is installed.

### G2 (implicit)

Allow positive credit when completed hot-work permits and fire-watch records cover every hot-work job in the last 12 months.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: All 9 jobs have both required records over the required period; positive credit maps to strength.

Candidate:

Assessment: The rule applies to hot-work jobs in the last 12 months, with no explicit exclusion for the subject. The evidence batch covers the period up to 30 September 2026, which includes the last 12 months ending on that date. The evidence E20 states: 'The complete 12-month hot-work register lists 9 jobs; signed permits and completed fire-watch records are attached for all 9.' This directly supports that all 9 hot-work jobs in the last 12 months have corresponding completed permits and fire-watch records. Therefore, the condition is met. The rule does not contain any explicit exception prerequisites or validity dates. There is no exception that would apply to this case. There are no conflicting observations regarding the hot-work jobs or their permits and fire-watch records in the last 12 months. All relevant evidence supports that every job is covered.
Finding: All 9 hot-work jobs in the last 12 months (as of 30 September 2026) have corresponding signed permits and completed fire-watch records attached, satisfying the condition for positive credit.
scope_reason: The rule applies to hot-work jobs in the last 12 months, with no explicit exclusion for the subject. The evidence batch covers the period up to 30 September 2026, which includes the last 12 months ending on that date.
condition_reason: The evidence E20 states: 'The complete 12-month hot-work register lists 9 jobs; signed permits and completed fire-watch records are attached for all 9.' This directly supports that all 9 hot-work jobs in the last 12 months have corresponding completed permits and fire-watch records. Therefore, the condition is met.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates. There is no exception that would apply to this case.
conflict_reason: There are no conflicting observations regarding the hot-work jobs or their permits and fire-watch records in the last 12 months. All relevant evidence supports that every job is covered.

### G3 (implicit)

Refer a finishing area with flammable liquids in open containers, except while the liquids are inside an approved enclosed dispensing system.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: The recorded enclosed system meets the exception and there is no open-container exposure outside it; no concern should be emitted.

Candidate:

Assessment: The rule applies to the finishing area, which is explicitly mentioned in the evidence as containing flammable liquids. The period of assessment is 30 September 2026, which aligns with the submission date and the rule's applicability during that time frame. Evidence E30 states that 'The finishing-area liquids are entirely inside an approved enclosed dispensing system; no containers are open outside it.' This directly supports the trigger condition by confirming that flammable liquids are not in open containers in the finishing area, but rather are contained within an approved enclosed dispensing system. Therefore, the condition is true. The rule includes an exception: 'except while the liquids are inside an approved enclosed dispensing system.' Evidence E30 confirms that the liquids are indeed inside such a system, which means the exception applies. However, since the trigger condition (flammable liquids in open containers) is false due to the presence of the enclosed system, the exception does not negate the finding but rather supports that no referral is needed. There are no conflicting observations regarding whether the finishing area contains flammable liquids in open containers. The evidence clearly states that all liquids are inside an approved enclosed dispensing system, which satisfies the exception to the rule.
scope_reason: The rule applies to the finishing area, which is explicitly mentioned in the evidence as containing flammable liquids. The period of assessment is 30 September 2026, which aligns with the submission date and the rule's applicability during that time frame.
condition_reason: Evidence E30 states that 'The finishing-area liquids are entirely inside an approved enclosed dispensing system; no containers are open outside it.' This directly supports the trigger condition by confirming that flammable liquids are not in open containers in the finishing area, but rather are contained within an approved enclosed dispensing system. Therefore, the condition is true.
exception_reason: The rule includes an exception: 'except while the liquids are inside an approved enclosed dispensing system.' Evidence E30 confirms that the liquids are indeed inside such a system, which means the exception applies. However, since the trigger condition (flammable liquids in open containers) is false due to the presence of the enclosed system, the exception does not negate the finding but rather supports that no referral is needed.
conflict_reason: There are no conflicting observations regarding whether the finishing area contains flammable liquids in open containers. The evidence clearly states that all liquids are inside an approved enclosed dispensing system, which satisfies the exception to the rule.


## hospitality

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[concern] A hotel kitchen suppression system with service overdue by more than 30 days is a concern.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: Exactly 30 days does not exceed 30; preserve the strict greater-than threshold despite the service being overdue.

Candidate:

Assessment: The rule applies to a hotel kitchen suppression system. The subject is the kitchen suppression system at Elm urban hotel. The period in scope is the current assessment period ending 30 September 2026. Evidence E8 states: 'The kitchen suppression system's scheduled service date was 31 August 2026. It remains unserviced as of 30 September 2026, exactly 30 days overdue.' This indicates the system was due on 31 August 2026 and remained unserviced as of the assessment date (30 September 2026). The delay is exactly 30 days, not more than 30 days. Therefore, the condition is false because the delay does not exceed 30 days. The rule does not contain an explicit exception. There are no prerequisites or validity dates for exceptions mentioned in the rule text. There are no conflicting observations regarding the kitchen suppression system's service date or its overdue status as of 30 September 2026. The evidence is clear and unambiguous.
scope_reason: The rule applies to a hotel kitchen suppression system. The subject is the kitchen suppression system at Elm urban hotel. The period in scope is the current assessment period ending 30 September 2026.
condition_reason: Evidence E8 states: 'The kitchen suppression system's scheduled service date was 31 August 2026. It remains unserviced as of 30 September 2026, exactly 30 days overdue.' This indicates the system was due on 31 August 2026 and remained unserviced as of the assessment date (30 September 2026). The delay is exactly 30 days, not more than 30 days. Therefore, the condition is false because the delay does not exceed 30 days.
exception_reason: The rule does not contain an explicit exception. There are no prerequisites or validity dates for exceptions mentioned in the rule text.
conflict_reason: There are no conflicting observations regarding the kitchen suppression system's service date or its overdue status as of 30 September 2026. The evidence is clear and unambiguous.

### G2 (explicit)

[concern] An unfenced guest swimming pool is a concern; this rule applies only to properties operating a guest swimming pool.

Expected `not_applicable`; actual `not_applicable`. Explanation: 0/10 (judge_error).

Reference: No guest pool means the rule is out of scope; do not label this an in-scope negative or treat the fountain as a pool.

Candidate:

Assessment: The rule applies to properties operating a guest swimming pool. The evidence shows the property does not operate a guest swimming pool. The evidence states 'The property does not operate a guest swimming pool' (E20). This directly supports that there is no guest swimming pool, which means the condition for the concern is not met. The rule specifically applies only to properties operating a guest swimming pool, and since this property does not operate one, the trigger does not apply. The rule does not contain any explicit exception prerequisites or validity dates. It simply states that an unfenced guest swimming pool is a concern for properties operating such pools. There are no conditions under which this rule would not apply. There are no conflicting observations regarding whether the property operates a guest swimming pool. The evidence clearly states that the property does not operate a guest swimming pool, and there is no contradictory information in the provided evidence.
scope_reason: The rule applies to properties operating a guest swimming pool. The evidence shows the property does not operate a guest swimming pool.
condition_reason: The evidence states 'The property does not operate a guest swimming pool' (E20). This directly supports that there is no guest swimming pool, which means the condition for the concern is not met. The rule specifically applies only to properties operating a guest swimming pool, and since this property does not operate one, the trigger does not apply.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates. It simply states that an unfenced guest swimming pool is a concern for properties operating such pools. There are no conditions under which this rule would not apply.
conflict_reason: There are no conflicting observations regarding whether the property operates a guest swimming pool. The evidence clearly states that the property does not operate a guest swimming pool, and there is no contradictory information in the provided evidence.

### G3 (explicit)

Unrestricted cash covering at least 6 months of fixed operating costs is a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: 780000/120000 = 6.5 months, at least 6; restricted deposits were excluded and should not be added.

Candidate:

Assessment: The rule applies to the applicant (Elm urban hotel) as a whole, with no explicit exclusion. The subject is the organization's financial position regarding unrestricted cash and fixed operating costs. The period in scope is the current assessment date, 30 September 2026. The evidence shows that unrestricted cash is $780,000 and fixed operating costs are $120,000 per month. Calculating the months covered: $780,000 / $120,000 = 6.5 months. Since 6.5 months is greater than or equal to 6 months, the condition is met. The rule tests whether unrestricted cash covers at least 6 months of fixed operating costs, which it does. The rule does not contain an explicit exception. There are no prerequisites for an exception that are satisfied in this case. There are no conflicting observations regarding the unrestricted cash amount or fixed operating costs that would create an unresolved contradiction. The figures provided are consistent and support the condition.
Finding: Unrestricted cash of $780,000 covers 6.5 months of fixed operating costs ($120,000/month), meeting the requirement of at least 6 months.
scope_reason: The rule applies to the applicant (Elm urban hotel) as a whole, with no explicit exclusion. The subject is the organization's financial position regarding unrestricted cash and fixed operating costs. The period in scope is the current assessment date, 30 September 2026.
condition_reason: The evidence shows that unrestricted cash is $780,000 and fixed operating costs are $120,000 per month. Calculating the months covered: $780,000 / $120,000 = 6.5 months. Since 6.5 months is greater than or equal to 6 months, the condition is met. The rule tests whether unrestricted cash covers at least 6 months of fixed operating costs, which it does.
exception_reason: The rule does not contain an explicit exception. There are no prerequisites for an exception that are satisfied in this case.
conflict_reason: There are no conflicting observations regarding the unrestricted cash amount or fixed operating costs that would create an unresolved contradiction. The figures provided are consistent and support the condition.


## contractor

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[strength] Current insurance certificates for every active subcontractor are a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: All four active subcontractors are covered by current certificates; the population and validity period are established.

Candidate:

Assessment: The rule applies to the current state as of the assessment date (30 September 2026), covering the proposed policy period beginning 1 November 2026. The subject is 'every active subcontractor' within the scope of Fir's operations and subcontracts during this period. Evidence E8 states: 'The active subcontractor register contains 4 firms; all 4 have current insurance certificates covering the proposed policy period.' This directly supports that all active subcontractors have current insurance certificates, which is the trigger condition for this strength. There are no explicit exceptions stated in the rule text. The rule does not contain any conditional language such as 'unless' or 'except' that would create an exception for this strength. There are no conflicting observations regarding the presence of insurance certificates for active subcontractors. All evidence points to the existence of current certificates for all 4 active subcontractors.
Finding: All 4 active subcontractors have current insurance certificates covering the proposed policy period, meeting the condition for this strength.
scope_reason: The rule applies to the current state as of the assessment date (30 September 2026), covering the proposed policy period beginning 1 November 2026. The subject is 'every active subcontractor' within the scope of Fir's operations and subcontracts during this period.
condition_reason: Evidence E8 states: 'The active subcontractor register contains 4 firms; all 4 have current insurance certificates covering the proposed policy period.' This directly supports that all active subcontractors have current insurance certificates, which is the trigger condition for this strength.
exception_reason: There are no explicit exceptions stated in the rule text. The rule does not contain any conditional language such as 'unless' or 'except' that would create an exception for this strength.
conflict_reason: There are no conflicting observations regarding the presence of insurance certificates for active subcontractors. All evidence points to the existence of current certificates for all 4 active subcontractors.

### G2 (implicit)

Refer contracts that transfer structural design responsibility to the applicant unless an executed agreement delegates that responsibility to an insured licensed engineer.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: Design responsibility is contractually assumed and no executed delegation supports the exception; referral maps to concern.

Candidate:

Assessment: The rule applies to contracts involving the applicant (Fir mechanical installations) and concerns structural design responsibility transfers. The period in scope is the proposed policy period beginning 1 November 2026, as indicated by the submission date of 30 September 2026 and the proposed insurance period. Evidence E20 states: 'The current Riverside contract transfers structural design responsibility to Fir. No executed agreement delegates that responsibility to an engineer.' This directly supports the trigger condition that a contract transfers structural design responsibility to the applicant (Fir), and there is no executed agreement delegating that responsibility to an insured licensed engineer, as required by the exception. Therefore, the condition is true. The rule includes an exception: 'unless an executed agreement delegates that responsibility to an insured licensed engineer.' Evidence E20 indicates that no such executed agreement exists. The exception prerequisites are not met, so the exception does not apply. There are no conflicting observations regarding whether the Riverside contract transfers structural design responsibility to Fir or whether an executed agreement delegates that responsibility to an insured licensed engineer. The evidence is clear and consistent.
Finding: The Riverside contract transfers structural design responsibility to Fir, and no executed agreement delegates that responsibility to an insured licensed engineer. This triggers the referral requirement under criterion C2.
scope_reason: The rule applies to contracts involving the applicant (Fir mechanical installations) and concerns structural design responsibility transfers. The period in scope is the proposed policy period beginning 1 November 2026, as indicated by the submission date of 30 September 2026 and the proposed insurance period.
condition_reason: Evidence E20 states: 'The current Riverside contract transfers structural design responsibility to Fir. No executed agreement delegates that responsibility to an engineer.' This directly supports the trigger condition that a contract transfers structural design responsibility to the applicant (Fir), and there is no executed agreement delegating that responsibility to an insured licensed engineer, as required by the exception. Therefore, the condition is true.
exception_reason: The rule includes an exception: 'unless an executed agreement delegates that responsibility to an insured licensed engineer.' Evidence E20 indicates that no such executed agreement exists. The exception prerequisites are not met, so the exception does not apply.
conflict_reason: There are no conflicting observations regarding whether the Riverside contract transfers structural design responsibility to Fir or whether an executed agreement delegates that responsibility to an insured licensed engineer. The evidence is clear and consistent.

### G3 (implicit)

Allow positive credit for a documented rescue drill for every crew scheduled for confined-space entry during the policy period.

Expected `insufficient_evidence`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: Two crews are in scope but drill records are missing; absence of records does not prove drills did not happen or establish positive credit.

Candidate:

Assessment: The rule applies to crews scheduled for confined-space entry during the policy period. The policy period begins on 1 November 2026, and the evidence indicates two crews are scheduled for confined-space entry during this period. The evidence states that 'Two crews are scheduled for confined-space entry during the policy period; rescue-drill records have been requested but are not yet supplied.' This means that while there are two crews scheduled, no documented rescue drill records have been provided. The rule requires documented rescue drills for each crew, and since these documents are missing, the condition is not met. The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no conflicting observations regarding the requirement for documented rescue drills. The only relevant observation is that rescue drill records have not been supplied, which directly contradicts the condition.
scope_reason: The rule applies to crews scheduled for confined-space entry during the policy period. The policy period begins on 1 November 2026, and the evidence indicates two crews are scheduled for confined-space entry during this period.
condition_reason: The evidence states that 'Two crews are scheduled for confined-space entry during the policy period; rescue-drill records have been requested but are not yet supplied.' This means that while there are two crews scheduled, no documented rescue drill records have been provided. The rule requires documented rescue drills for each crew, and since these documents are missing, the condition is not met.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case.
conflict_reason: There are no conflicting observations regarding the requirement for documented rescue drills. The only relevant observation is that rescue drill records have not been supplied, which directly contradicts the condition.
