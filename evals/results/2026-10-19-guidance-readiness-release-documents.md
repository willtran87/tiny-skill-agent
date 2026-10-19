# First-use long-document holdout

State: **completed**

Synthetic, author-labeled cases frozen before inference. Production code is unchanged. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 3/3 | 3/3 | 2/3 | 0/3 | False | False | False |
| cyber | 618 / 1424 | 3/3 | 3/3 | 3/3 | 3/3 | True | False | True |
| fleet | 632 / 1452 | 3/3 | 3/3 | 3/3 | 3/3 | False | False | False |
| manufacturing | 636 / 1419 | 3/3 | 3/3 | 3/3 | 0/3 | False | False | False |
| hospitality | 635 / 1427 | 3/3 | 3/3 | 3/3 | 0/3 | False | False | False |
| contractor | 640 / 1425 | 3/3 | 2/3 | 3/3 | 0/3 | True | True | False |

## property

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[concern] A cold-storage building whose roof is more than 25 years old is a concern unless a complete roof replacement has been documented within the last 2 years.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: Identify North and South separately: 28 and 31 exceed 25, with no replacement exception. East is excluded by its documented replacement/current age.

Candidate:

Assessment: The rule applies to cold-storage buildings, and the evidence describes three refrigerated buildings: North, South, and East. Each building's roof age is specified, making them all in scope for this rule. For the North building, the roof age is 28 years, which exceeds the 25-year threshold. No complete replacement has been documented. For the South building, the roof age is 31 years, exceeding the threshold, with no complete replacement documented. For the East building, a complete roof replacement occurred on 1 March 2026, making its roof age 0 years, which is within the last 2 years. Therefore, the condition is true for North and South buildings but false for East. The exception requires that a complete roof replacement has been documented within the last 2 years. For North and South buildings, no such documentation exists. For East building, the replacement was documented on 1 March 2026, which is within the last 2 years (as of 30 September 2026). Therefore, the exception applies only to the East building. There are no conflicting pieces of evidence regarding roof ages or replacement documentation for any of the buildings. All relevant information is consistent and supports the stated roof ages and replacement dates.
Finding: The North building has a roof age of 28 years, which exceeds the 25-year threshold, and no complete replacement has been documented within the last 2 years. Therefore, it meets the condition for concern.
Finding: The South building has a roof age of 31 years, which exceeds the 25-year threshold, and no complete replacement has been documented within the last 2 years. Therefore, it meets the condition for concern.

### G2 (explicit)

Current sprinkler inspection certificates with no outstanding deficiencies for every cold-storage building are a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: All three buildings have current certificates and no deficiencies; the all-buildings requirement is established.

Candidate:

Assessment: The rule applies to all cold-storage buildings. The subject is the three buildings (North, South, and East) operated by Alder. The period in scope is the current assessment date of 30 September 2026. Evidence E22 states: 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports that all three buildings have current sprinkler inspection certificates with no outstanding deficiencies. Therefore, the condition is true. The rule does not contain an explicit exception. There are no prerequisites or validity dates for exceptions mentioned in the rule text. There are no conflicting observations regarding the sprinkler inspection certificates for any of the buildings. All three buildings are covered by current certificates with no outstanding deficiencies as stated in E22.
Finding: The sprinkler inspection certificate for the North building records no outstanding deficiencies, satisfying the condition of the rule.
Finding: The sprinkler inspection certificate for the South building records no outstanding deficiencies, satisfying the condition of the rule.
Finding: The sprinkler inspection certificate for the East building records no outstanding deficiencies, satisfying the condition of the rule.
scope_reason: The rule applies to all cold-storage buildings. The subject is the three buildings (North, South, and East) operated by Alder. The period in scope is the current assessment date of 30 September 2026.
condition_reason: Evidence E22 states: 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports that all three buildings have current sprinkler inspection certificates with no outstanding deficiencies. Therefore, the condition is true.
exception_reason: The rule does not contain an explicit exception. There are no prerequisites or validity dates for exceptions mentioned in the rule text.
conflict_reason: There are no conflicting observations regarding the sprinkler inspection certificates for any of the buildings. All three buildings are covered by current certificates with no outstanding deficiencies as stated in E22.

### G3 (explicit)

[concern] A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: The panels meet the trigger, but current independent approval for all three makes the stated exception apply; do not claim the panels are noncombustible.

Candidate:

Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, all of which are in scope as part of the Alder cold-storage facilities. All three buildings (North, South, and East) have combustible insulated wall panels. A current independent fire-engineering certification approves those panels in all three buildings. The condition 'a cold-storage building with combustible insulated wall panels' is met, but the exception 'a current independent fire-engineering certification approves those panels' also applies for each building. Therefore, the trigger does not establish a concern because the exception applies to all three buildings. The rule states that the concern does not apply 'unless a current independent fire-engineering certification approves those panels.' Evidence E32 confirms that 'current independent fire-engineering certification approves those panels in North, South, and East.' All three buildings meet the exception criteria, so the exception applies to all subjects. There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible insulated wall panels and that current independent fire-engineering certifications approve those panels.
scope_reason: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, all of which are in scope as part of the Alder cold-storage facilities.
condition_reason: All three buildings (North, South, and East) have combustible insulated wall panels. A current independent fire-engineering certification approves those panels in all three buildings. The condition 'a cold-storage building with combustible insulated wall panels' is met, but the exception 'a current independent fire-engineering certification approves those panels' also applies for each building. Therefore, the trigger does not establish a concern because the exception applies to all three buildings.
exception_reason: The rule states that the concern does not apply 'unless a current independent fire-engineering certification approves those panels.' Evidence E32 confirms that 'current independent fire-engineering certification approves those panels in North, South, and East.' All three buildings meet the exception criteria, so the exception applies to all subjects.
conflict_reason: There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible insulated wall panels and that current independent fire-engineering certifications approve those panels.


## cyber

Error: `None`; judge error: `None`.

### G1 (explicit)

[strength] MFA on every active privileged account is a strength.

Expected `no_match`; actual `no_match`. Explanation: 10/10 (graded).

Reference: 23/24 is not every account. The active emergency account is in scope and there is no exception; this is affirmative failure, not missing evidence.

Candidate:

Assessment: The rule applies to active privileged accounts. The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. The remaining account is an active emergency administrator without MFA. The evidence states that 'MFA is enabled for 23 of the 24 active privileged accounts; the remaining account is an active emergency administrator without MFA.' This means that not every active privileged account has MFA enabled. Therefore, the condition is false because the rule requires MFA on EVERY active privileged account. The rule does not contain any explicit exception prerequisites or validity dates. There is no exception stated that would apply to this situation. There are no conflicting observations regarding the MFA status of privileged accounts. The evidence clearly states that 23 out of 24 accounts have MFA enabled, with one exception being an active emergency administrator without MFA. This does not create an unresolved conflict as it directly addresses the subject matter of the rule.
scope_reason: The rule applies to active privileged accounts. The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. The remaining account is an active emergency administrator without MFA.
condition_reason: The evidence states that 'MFA is enabled for 23 of the 24 active privileged accounts; the remaining account is an active emergency administrator without MFA.' This means that not every active privileged account has MFA enabled. Therefore, the condition is false because the rule requires MFA on EVERY active privileged account.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates. There is no exception stated that would apply to this situation.
conflict_reason: There are no conflicting observations regarding the MFA status of privileged accounts. The evidence clearly states that 23 out of 24 accounts have MFA enabled, with one exception being an active emergency administrator without MFA. This does not create an unresolved conflict as it directly addresses the subject matter of the rule.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to active privileged accounts, which matches the reference's trigger condition. Excerpt: "Assessment: The rule applies to active privileged accounts."
- factual_grounding: 2/2. The candidate accurately cites the number of accounts and their MFA status from the provided evidence. Excerpt: "The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. The remaining account is an active emergency administrator without MFA."
- scope_and_exceptions: 2/2. The candidate correctly notes that there are no exceptions in the rule and that the active emergency account is in scope. Excerpt: "The rule does not contain any explicit exception prerequisites or validity dates. There is no exception stated that would apply to this situation."
- logical_support: 2/2. The candidate logically concludes that since one account lacks MFA, the condition fails as required by the rule. Excerpt: "Therefore, the condition is false because the rule requires MFA on EVERY active privileged account."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and directly ties the evidence to the rule's requirements. Excerpt: "This does not create an unresolved conflict as it directly addresses the subject matter of the rule."
### G2 (explicit)

A successful isolated recovery test within the last 90 days is a strength.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: 15 August is 46 days before 30 September, within 90; a successful isolated test is recorded.

Candidate:

Assessment: The rule applies to the subject of isolated recovery testing for the payroll service. The period in scope is the last 90 days from the assessment date (30 September 2026). An isolated payroll recovery test succeeded on 15 August 2026 (E21). The test log records restored data and a successful application start. The assessment date is 30 September 2026, so the test occurred within the last 90 days (15 August 2026 to 30 September 2026 = 46 days). This supports the trigger condition. The rule does not contain an explicit exception. There are no stated validity dates or prerequisites for exceptions that would apply here. There are no conflicting observations regarding the isolated recovery test. The single observation E21 confirms a successful test on 15 August 2026, which falls within the required timeframe.
Finding: A successful isolated recovery test was conducted on 15 August 2026, which falls within the last 90 days from the assessment date of 30 September 2026. The test log confirms restored data and a successful application start.
scope_reason: The rule applies to the subject of isolated recovery testing for the payroll service. The period in scope is the last 90 days from the assessment date (30 September 2026).
condition_reason: An isolated payroll recovery test succeeded on 15 August 2026 (E21). The test log records restored data and a successful application start. The assessment date is 30 September 2026, so the test occurred within the last 90 days (15 August 2026 to 30 September 2026 = 46 days). This supports the trigger condition.
exception_reason: The rule does not contain an explicit exception. There are no stated validity dates or prerequisites for exceptions that would apply here.
conflict_reason: There are no conflicting observations regarding the isolated recovery test. The single observation E21 confirms a successful test on 15 August 2026, which falls within the required timeframe.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to isolated recovery testing for the payroll service. Excerpt: "Assessment: The rule applies to the subject of isolated recovery testing for the payroll service."
- factual_grounding: 2/2. The candidate accurately cites the date of the test and its outcome from the evidence. Excerpt: "An isolated payroll recovery test succeeded on 15 August 2026 (E21). The test log records restored data and a successful application start."
- scope_and_exceptions: 2/2. The candidate correctly identifies that there are no exceptions in the rule and that the test falls within the required timeframe. Excerpt: "The rule does not contain an explicit exception. There are no stated validity dates or prerequisites for exceptions that would apply here."
- logical_support: 2/2. The candidate correctly calculates the time frame and shows that the test meets the rule's requirement. Excerpt: "The assessment date is 30 September 2026, so the test occurred within the last 90 days (15 August 2026 to 30 September 2026 = 46 days). This supports the trigger condition."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and directly ties the evidence to the rule's requirements. Excerpt: "The single observation E21 confirms a successful test on 15 August 2026, which falls within the required timeframe."
### G3 (implicit)

Refer any account that stores unencrypted portable copies of payroll data for adverse treatment.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: Unencrypted portable payroll copies meet the referral rule; the guideline's vocabulary maps adverse treatment to concern.

Candidate:

Assessment: The rule applies to accounts that store unencrypted portable copies of payroll data. The subject is the account storing such data, and the period in scope is the current assessment date (30 September 2026). Evidence E31 states: 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence confirms the presence of unencrypted payroll data on portable drives, which meets the rule's requirement. The rule does not contain an explicit exception. There is no stated condition under which this rule would not apply. There are no conflicting observations regarding the storage of unencrypted portable copies of payroll data on USB drives. The evidence E31 clearly states that two portable USB drives hold unencrypted payroll exports used by the support team.
Finding: The evidence shows that two portable USB drives currently hold unencrypted payroll exports used by the support team, which satisfies the condition of storing unencrypted portable copies of payroll data as required by the rule.
scope_reason: The rule applies to accounts that store unencrypted portable copies of payroll data. The subject is the account storing such data, and the period in scope is the current assessment date (30 September 2026).
condition_reason: Evidence E31 states: 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence confirms the presence of unencrypted payroll data on portable drives, which meets the rule's requirement.
exception_reason: The rule does not contain an explicit exception. There is no stated condition under which this rule would not apply.
conflict_reason: There are no conflicting observations regarding the storage of unencrypted portable copies of payroll data on USB drives. The evidence E31 clearly states that two portable USB drives hold unencrypted payroll exports used by the support team.

- rule_application: 2/2. The candidate correctly identifies the subject of the rule as accounts storing unencrypted portable copies of payroll data. Excerpt: "Assessment: The rule applies to accounts that store unencrypted portable copies of payroll data."
- factual_grounding: 2/2. The candidate accurately cites the evidence that supports the presence of unencrypted payroll data on portable drives. Excerpt: "Evidence E31 states: 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.'"
- scope_and_exceptions: 2/2. The candidate correctly notes that there are no exceptions in the rule and that the situation meets the rule's requirements. Excerpt: "The rule does not contain an explicit exception. There is no stated condition under which this rule would not apply."
- logical_support: 2/2. The candidate logically connects the evidence to the rule's requirements and correctly concludes that the condition is met. Excerpt: "This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence confirms the presence of unencrypted payroll data on portable drives, which meets the rule's requirement."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and directly ties the evidence to the rule's requirements. Excerpt: "The evidence E31 clearly states that two portable USB drives hold unencrypted payroll exports used by the support team."

## fleet

Error: `None`; judge error: `None`.

### G1 (explicit)

[concern] A heavy goods vehicle with an unresolved brake defect is a concern.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 10/10 (graded).

Reference: The equally authoritative H7 records conflict for the same date with no correction; abstain rather than select one report or emit a settled concern.

Candidate:

Assessment: The rule applies to heavy goods vehicles. The evidence mentions that Cedar operates eight heavy goods vehicles, and specifically discusses vehicle H7 as having an unresolved brake defect. The assessment date is 30 September 2026, and the inspection was conducted on 29 September 2026. Evidence E8 states that 'Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect.' Evidence E9 states that 'Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other.' These two observations directly contradict each other regarding vehicle H7. Since there is no correction or resolution provided for this contradiction, and both inspectors are stated to be equally authoritative, the actual state of the brake defect on vehicle H7 remains unresolved. Therefore, the condition 'A heavy goods vehicle with an unresolved brake defect is a concern' is true based on the contradictory evidence. The rule does not contain any explicit exception prerequisites or validity dates mentioned in the text provided. There is no indication that an exception applies to this situation. There is a direct conflict between E8 and E9 regarding vehicle H7's brake defect status. E8 states there is an unresolved brake defect, while E9 states there is no brake defect. These observations are about the same subject (vehicle H7) at the same time (29 September 2026), and they contradict each other. However, since neither report corrects the other and both inspectors are equally authoritative, this constitutes an unresolved conflict.
scope_reason: The rule applies to heavy goods vehicles. The evidence mentions that Cedar operates eight heavy goods vehicles, and specifically discusses vehicle H7 as having an unresolved brake defect. The assessment date is 30 September 2026, and the inspection was conducted on 29 September 2026.
condition_reason: Evidence E8 states that 'Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect.' Evidence E9 states that 'Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other.' These two observations directly contradict each other regarding vehicle H7. Since there is no correction or resolution provided for this contradiction, and both inspectors are stated to be equally authoritative, the actual state of the brake defect on vehicle H7 remains unresolved. Therefore, the condition 'A heavy goods vehicle with an unresolved brake defect is a concern' is true based on the contradictory evidence.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates mentioned in the text provided. There is no indication that an exception applies to this situation.
conflict_reason: There is a direct conflict between E8 and E9 regarding vehicle H7's brake defect status. E8 states there is an unresolved brake defect, while E9 states there is no brake defect. These observations are about the same subject (vehicle H7) at the same time (29 September 2026), and they contradict each other. However, since neither report corrects the other and both inspectors are equally authoritative, this constitutes an unresolved conflict.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to heavy goods vehicles, which matches the reference's trigger condition. Excerpt: "Assessment: The rule applies to heavy goods vehicles."
- factual_grounding: 2/2. The candidate accurately cites and grounds the explanation on the specific evidence provided, correctly identifying the contradiction between two authoritative reports. Excerpt: "Evidence E8 states that 'Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect.' Evidence E9 states that 'Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other.'"
- scope_and_exceptions: 2/2. The candidate correctly notes that there are no exceptions in the rule and appropriately addresses the scope of the rule application. Excerpt: "The rule does not contain any explicit exception prerequisites or validity dates mentioned in the text provided. There is no indication that an exception applies to this situation."
- logical_support: 2/2. The candidate logically connects the contradictory evidence to the conclusion that the vehicle is a concern, correctly applying the rule's logic. Excerpt: "Since there is no correction or resolution provided for this contradiction, and both inspectors are stated to be equally authoritative, the actual state of the brake defect on vehicle H7 remains unresolved. Therefore, the condition 'A heavy goods vehicle with an unresolved brake defect is a concern' is true based on the contradictory evidence."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and directly references the evidence without introducing assumptions or contradictions. Excerpt: "There is a direct conflict between E8 and E9 regarding vehicle H7's brake defect status. E8 states there is an unresolved brake defect, while E9 states there is no brake defect. These observations are about the same subject (vehicle H7) at the same time (29 September 2026), and they contradict each other."
### G2 (explicit)

[strength] Completed annual driving-record reviews for all active drivers are a strength.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 10/10 (graded).

Reference: The register is missing. This does not prove that reviews were not performed; evidence is insufficient to establish all-driver coverage.

Candidate:

Assessment: The rule applies to active drivers. Evidence E22 states there are 18 active drivers, and the broker has requested but not received the annual driving-record review register. The rule requires that annual driving-record reviews be completed for all active drivers. Evidence E22 indicates that the broker has requested the annual driving-record review register but has not received it. This means there is no record confirming that the reviews have been completed for all 18 drivers. Therefore, the supporting facts are absent, and we cannot confirm that the condition is true. The lack of documentation does not prove that the reviews were not done, but it also does not confirm they were done. Thus, the condition is unknown. There is no explicit exception stated in the rule for this criterion. There are no conflicting observations regarding the completion of annual driving-record reviews for active drivers. The only relevant evidence is that the register has not been provided, which does not establish either the presence or absence of the reviews.
scope_reason: The rule applies to active drivers. Evidence E22 states there are 18 active drivers, and the broker has requested but not received the annual driving-record review register.
condition_reason: The rule requires that annual driving-record reviews be completed for all active drivers. Evidence E22 indicates that the broker has requested the annual driving-record review register but has not received it. This means there is no record confirming that the reviews have been completed for all 18 drivers. Therefore, the supporting facts are absent, and we cannot confirm that the condition is true. The lack of documentation does not prove that the reviews were not done, but it also does not confirm they were done. Thus, the condition is unknown.
exception_reason: There is no explicit exception stated in the rule for this criterion.
conflict_reason: There are no conflicting observations regarding the completion of annual driving-record reviews for active drivers. The only relevant evidence is that the register has not been provided, which does not establish either the presence or absence of the reviews.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to active drivers, aligning with the reference's trigger condition. Excerpt: "Assessment: The rule applies to active drivers."
- factual_grounding: 2/2. The candidate accurately cites the evidence and correctly grounds the explanation on the lack of documentation. Excerpt: "Evidence E22 states there are 18 active drivers, and the broker has requested but not received the annual driving-record review register."
- scope_and_exceptions: 2/2. The candidate correctly identifies that there are no exceptions mentioned in the rule, which aligns with the reference's rationale. Excerpt: "There is no explicit exception stated in the rule for this criterion."
- logical_support: 2/2. The candidate logically explains why insufficient evidence leads to an unknown status, correctly applying the rule's logic. Excerpt: "Therefore, the supporting facts are absent, and we cannot confirm that the condition is true. The lack of documentation does not prove that the reviews were not done, but it also does not confirm they were done. Thus, the condition is unknown."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and correctly notes the absence of contradictory evidence. Excerpt: "There are no conflicting observations regarding the completion of annual driving-record reviews for active drivers. The only relevant evidence is that the register has not been provided, which does not establish either the presence or absence of the reviews."
### G3 (implicit)

Give favorable treatment when verified telematics show a harsh-braking rate below 2 events per 1000 miles across the active fleet.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: 54 / 36000 * 1000 = 1.5, strictly below 2. Favorable treatment maps to strength.

Candidate:

Assessment: The rule applies to the active fleet. The evidence shows data for the active fleet, including 8 heavy goods vehicles and 18 active drivers. The telematics report covers the active fleet during the reporting period. The verified active-fleet telematics report records 54 harsh-braking events over 36000 miles during the reporting period. Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile. Converting to events per 1000 miles: 0.0015 * 1000 = 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met. The rule does not contain an explicit exception that would apply to this case. There are no stated validity dates or prerequisites for exceptions. There are no conflicting observations regarding the harsh-braking rate in the telematics report. The data is consistent and directly supports the condition.
Finding: The verified active-fleet telematics report shows 54 harsh-braking events over 36000 miles, which calculates to 1.5 events per 1000 miles. This is below the threshold of 2 events per 1000 miles, meeting the condition for favorable treatment.
scope_reason: The rule applies to the active fleet. The evidence shows data for the active fleet, including 8 heavy goods vehicles and 18 active drivers. The telematics report covers the active fleet during the reporting period.
condition_reason: The verified active-fleet telematics report records 54 harsh-braking events over 36000 miles during the reporting period. Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile. Converting to events per 1000 miles: 0.0015 * 1000 = 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met.
exception_reason: The rule does not contain an explicit exception that would apply to this case. There are no stated validity dates or prerequisites for exceptions.
conflict_reason: There are no conflicting observations regarding the harsh-braking rate in the telematics report. The data is consistent and directly supports the condition.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to the active fleet, matching the reference's trigger condition. Excerpt: "Assessment: The rule applies to the active fleet."
- factual_grounding: 2/2. The candidate accurately cites and uses the factual data from the evidence to support the calculation. Excerpt: "The verified active-fleet telematics report records 54 harsh-braking events over 36000 miles during the reporting period."
- scope_and_exceptions: 2/2. The candidate correctly identifies the absence of exceptions and appropriately addresses the scope. Excerpt: "The rule does not contain an explicit exception that would apply to this case. There are no stated validity dates or prerequisites for exceptions."
- logical_support: 2/2. The candidate provides clear arithmetic and correctly applies it to meet the rule's threshold. Excerpt: "Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile. Converting to events per 1000 miles: 0.0015 * 1000 = 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and correctly notes that the data is consistent and sufficient. Excerpt: "There are no conflicting observations regarding the harsh-braking rate in the telematics report. The data is consistent and directly supports the condition."

## manufacturing

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (implicit)

Decline operations using a production press without an interlocked guard.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: P4 is in use and unguarded; a proposed retrofit is not completion. Decline maps to concern.

Candidate:

Assessment: The rule applies to operations using a production press. The subject is the production press P4, which is mentioned in the technical exhibit (E8). The period in scope is the current assessment date of 30 September 2026. The technical exhibit (E8) states that 'Production press P4 remains in daily use without an interlocked guard; the proposed retrofit has not been ordered.' This directly supports the trigger condition that operations are being conducted using a production press without an interlocked guard. The rule does not contain any explicit exception language. There is no indication that any exception prerequisites are met or that there is an applicable exception. There are no conflicting observations regarding the presence or absence of an interlocked guard on production press P4. The single observation (E8) clearly indicates that the press operates without an interlocked guard.
Finding: The technical exhibit (E8) confirms that production press P4 remains in daily use without an interlocked guard, which directly triggers the rule's condition for declining operations using such equipment.
scope_reason: The rule applies to operations using a production press. The subject is the production press P4, which is mentioned in the technical exhibit (E8). The period in scope is the current assessment date of 30 September 2026.
condition_reason: The technical exhibit (E8) states that 'Production press P4 remains in daily use without an interlocked guard; the proposed retrofit has not been ordered.' This directly supports the trigger condition that operations are being conducted using a production press without an interlocked guard.
exception_reason: The rule does not contain any explicit exception language. There is no indication that any exception prerequisites are met or that there is an applicable exception.
conflict_reason: There are no conflicting observations regarding the presence or absence of an interlocked guard on production press P4. The single observation (E8) clearly indicates that the press operates without an interlocked guard.

### G2 (implicit)

Allow positive credit when completed hot-work permits and fire-watch records cover every hot-work job in the last 12 months.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: All 9 jobs have both required records over the required period; positive credit maps to strength.

Candidate:

Assessment: The rule applies to hot-work jobs in the last 12 months, with no explicit exclusion for the subject. The evidence batch includes a complete 12-month hot-work register listing 9 jobs with signed permits and completed fire-watch records attached for all 9. The evidence E20 states that 'The complete 12-month hot-work register lists 9 jobs; signed permits and completed fire-watch records are attached for all 9.' This directly supports the trigger condition. There are no observations refuting this claim within the provided evidence. The rule does not contain an explicit exception clause. No exception prerequisites are mentioned or satisfied in the evidence. There are no incompatible observations identified in the evidence that would create a conflict with the trigger condition.
Finding: The complete 12-month hot-work register lists 9 jobs with signed permits and completed fire-watch records attached for all 9, satisfying the condition that completed hot-work permits and fire-watch records cover every hot-work job in the last 12 months.
scope_reason: The rule applies to hot-work jobs in the last 12 months, with no explicit exclusion for the subject. The evidence batch includes a complete 12-month hot-work register listing 9 jobs with signed permits and completed fire-watch records attached for all 9.
condition_reason: The evidence E20 states that 'The complete 12-month hot-work register lists 9 jobs; signed permits and completed fire-watch records are attached for all 9.' This directly supports the trigger condition. There are no observations refuting this claim within the provided evidence.
exception_reason: The rule does not contain an explicit exception clause. No exception prerequisites are mentioned or satisfied in the evidence.
conflict_reason: There are no incompatible observations identified in the evidence that would create a conflict with the trigger condition.

### G3 (implicit)

Refer a finishing area with flammable liquids in open containers, except while the liquids are inside an approved enclosed dispensing system.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: The recorded enclosed system meets the exception and there is no open-container exposure outside it; no concern should be emitted.

Candidate:

Assessment: The rule applies to the finishing area, which is explicitly mentioned in the evidence as containing flammable liquids. The period of assessment is 30 September 2026, which aligns with the submission date and the rule's applicability. Evidence E30 states that 'The finishing-area liquids are entirely inside an approved enclosed dispensing system; no containers are open outside it.' This directly supports the trigger condition by confirming that flammable liquids are not in open containers in the finishing area, except when they are inside an approved enclosed dispensing system. Therefore, the condition is true. The rule includes an exception: 'except while the liquids are inside an approved enclosed dispensing system.' Evidence E30 confirms that the liquids are indeed inside such a system, which satisfies the exception prerequisite. Therefore, the exception applies. There are no conflicting observations regarding whether the finishing area contains flammable liquids in open containers or whether they are inside an approved enclosed dispensing system. The single observation E30 clearly supports the exception and does not create any unresolved conflicts.
scope_reason: The rule applies to the finishing area, which is explicitly mentioned in the evidence as containing flammable liquids. The period of assessment is 30 September 2026, which aligns with the submission date and the rule's applicability.
condition_reason: Evidence E30 states that 'The finishing-area liquids are entirely inside an approved enclosed dispensing system; no containers are open outside it.' This directly supports the trigger condition by confirming that flammable liquids are not in open containers in the finishing area, except when they are inside an approved enclosed dispensing system. Therefore, the condition is true.
exception_reason: The rule includes an exception: 'except while the liquids are inside an approved enclosed dispensing system.' Evidence E30 confirms that the liquids are indeed inside such a system, which satisfies the exception prerequisite. Therefore, the exception applies.
conflict_reason: There are no conflicting observations regarding whether the finishing area contains flammable liquids in open containers or whether they are inside an approved enclosed dispensing system. The single observation E30 clearly supports the exception and does not create any unresolved conflicts.


## hospitality

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[concern] A hotel kitchen suppression system with service overdue by more than 30 days is a concern.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: Exactly 30 days does not exceed 30; preserve the strict greater-than threshold despite the service being overdue.

Candidate:

Assessment: The subject is a hotel kitchen suppression system. The period in scope is from the scheduled service date of 31 August 2026 to the assessment date of 30 September 2026. The kitchen suppression system's scheduled service date was 31 August 2026 (E8). As of 30 September 2026, exactly 30 days have passed since the scheduled service date. The rule requires the service to be overdue by more than 30 days. Since the service is exactly 30 days overdue and not more than 30 days overdue, the condition is false. There is no explicit exception stated in the rule for C1. No conflicting observations are present regarding the service date or its overdue status.
scope_reason: The subject is a hotel kitchen suppression system. The period in scope is from the scheduled service date of 31 August 2026 to the assessment date of 30 September 2026.
condition_reason: The kitchen suppression system's scheduled service date was 31 August 2026 (E8). As of 30 September 2026, exactly 30 days have passed since the scheduled service date. The rule requires the service to be overdue by more than 30 days. Since the service is exactly 30 days overdue and not more than 30 days overdue, the condition is false.
exception_reason: There is no explicit exception stated in the rule for C1.
conflict_reason: No conflicting observations are present regarding the service date or its overdue status.

### G2 (explicit)

[concern] An unfenced guest swimming pool is a concern; this rule applies only to properties operating a guest swimming pool.

Expected `not_applicable`; actual `not_applicable`. Explanation: 0/10 (judge_error).

Reference: No guest pool means the rule is out of scope; do not label this an in-scope negative or treat the fountain as a pool.

Candidate:

Assessment: The rule applies to properties operating a guest swimming pool. The evidence shows the property does not operate a guest swimming pool (E20). The rule's trigger is that there is an unfenced guest swimming pool. However, evidence E20 explicitly states 'The property does not operate a guest swimming pool.' This directly contradicts the condition required for the rule to apply. Therefore, the trigger is false. The rule does not contain any explicit exception prerequisites or validity dates. It simply applies to properties operating a guest swimming pool without additional conditions. There are no conflicting observations regarding whether the property operates a guest swimming pool. The single observation E20 clearly states that there is no guest swimming pool, which directly contradicts the trigger condition.
scope_reason: The rule applies to properties operating a guest swimming pool. The evidence shows the property does not operate a guest swimming pool (E20).
condition_reason: The rule's trigger is that there is an unfenced guest swimming pool. However, evidence E20 explicitly states 'The property does not operate a guest swimming pool.' This directly contradicts the condition required for the rule to apply. Therefore, the trigger is false.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates. It simply applies to properties operating a guest swimming pool without additional conditions.
conflict_reason: There are no conflicting observations regarding whether the property operates a guest swimming pool. The single observation E20 clearly states that there is no guest swimming pool, which directly contradicts the trigger condition.

### G3 (explicit)

Unrestricted cash covering at least 6 months of fixed operating costs is a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: 780000/120000 = 6.5 months, at least 6; restricted deposits were excluded and should not be added.

Candidate:

Assessment: The rule applies to the applicant (Elm urban hotel), and the subject is the financial position of the business as of the assessment date (30 September 2026). Unrestricted cash is 780,000 dollars; fixed operating costs are 120,000 dollars per month. The calculation is: 780,000 / 120,000 = 6.5 months. Since 6.5 months is greater than or equal to 6 months, the condition is met. There is no explicit exception stated in the rule for C3. No conflicting observations were found regarding the unrestricted cash or fixed operating costs.
Finding: Unrestricted cash of 780,000 dollars covers 6.5 months of fixed operating costs (120,000 dollars per month), meeting the requirement of at least 6 months.
scope_reason: The rule applies to the applicant (Elm urban hotel), and the subject is the financial position of the business as of the assessment date (30 September 2026).
condition_reason: Unrestricted cash is 780,000 dollars; fixed operating costs are 120,000 dollars per month. The calculation is: 780,000 / 120,000 = 6.5 months. Since 6.5 months is greater than or equal to 6 months, the condition is met.
exception_reason: There is no explicit exception stated in the rule for C3.
conflict_reason: No conflicting observations were found regarding the unrestricted cash or fixed operating costs.


## contractor

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[strength] Current insurance certificates for every active subcontractor are a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: All four active subcontractors are covered by current certificates; the population and validity period are established.

Candidate:

Assessment: The rule applies to active subcontractors during the proposed policy period. The evidence shows that the applicant has an active subcontractor register containing 4 firms, all of which have current insurance certificates covering the proposed policy period (E8). The evidence directly supports that all 4 active subcontractors have current insurance certificates covering the proposed policy period. There are no observations indicating any subcontractor lacks a current certificate. The statement 'The active subcontractor register contains 4 firms; all 4 have current insurance certificates covering the proposed policy period' (E8) confirms that each of the 4 subcontractors has a valid certificate. There is no exception stated in the rule text. The rule does not contain any conditional language such as 'unless' or 'except' that would create an exception for this strength. There are no conflicting observations regarding the insurance certificates of the active subcontractors. All evidence points to the presence of current certificates for all 4 subcontractors.
Finding: All 4 active subcontractors have current insurance certificates covering the proposed policy period, meeting the requirement for this strength.
scope_reason: The rule applies to active subcontractors during the proposed policy period. The evidence shows that the applicant has an active subcontractor register containing 4 firms, all of which have current insurance certificates covering the proposed policy period (E8).
condition_reason: The evidence directly supports that all 4 active subcontractors have current insurance certificates covering the proposed policy period. There are no observations indicating any subcontractor lacks a current certificate. The statement 'The active subcontractor register contains 4 firms; all 4 have current insurance certificates covering the proposed policy period' (E8) confirms that each of the 4 subcontractors has a valid certificate.
exception_reason: There is no exception stated in the rule text. The rule does not contain any conditional language such as 'unless' or 'except' that would create an exception for this strength.
conflict_reason: There are no conflicting observations regarding the insurance certificates of the active subcontractors. All evidence points to the presence of current certificates for all 4 subcontractors.

### G2 (implicit)

Refer contracts that transfer structural design responsibility to the applicant unless an executed agreement delegates that responsibility to an insured licensed engineer.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: Design responsibility is contractually assumed and no executed delegation supports the exception; referral maps to concern.

Candidate:

Assessment: The rule applies to contracts transferring structural design responsibility to the applicant. The subject is the applicant (Fir mechanical installations), and the period in scope is the proposed policy period beginning 1 November 2026. Evidence E20 states: 'The current Riverside contract transfers structural design responsibility to Fir. No executed agreement delegates that responsibility to an engineer.' This directly supports the trigger condition that contracts transfer structural design responsibility to the applicant, and there is no executed agreement delegating that responsibility to an insured licensed engineer. The rule contains an exception: 'unless an executed agreement delegates that responsibility to an insured licensed engineer.' Evidence does not show any executed agreement delegating structural design responsibility to an insured licensed engineer. Therefore, the exception does not apply. There are no conflicting observations regarding whether contracts transfer structural design responsibility to the applicant or whether any executed agreement delegates that responsibility to an insured licensed engineer. The evidence is clear and consistent.
Finding: The Riverside contract transfers structural design responsibility to Fir, and no executed agreement delegates that responsibility to an insured licensed engineer. This triggers the referral requirement under criterion C2.
scope_reason: The rule applies to contracts transferring structural design responsibility to the applicant. The subject is the applicant (Fir mechanical installations), and the period in scope is the proposed policy period beginning 1 November 2026.
condition_reason: Evidence E20 states: 'The current Riverside contract transfers structural design responsibility to Fir. No executed agreement delegates that responsibility to an engineer.' This directly supports the trigger condition that contracts transfer structural design responsibility to the applicant, and there is no executed agreement delegating that responsibility to an insured licensed engineer.
exception_reason: The rule contains an exception: 'unless an executed agreement delegates that responsibility to an insured licensed engineer.' Evidence does not show any executed agreement delegating structural design responsibility to an insured licensed engineer. Therefore, the exception does not apply.
conflict_reason: There are no conflicting observations regarding whether contracts transfer structural design responsibility to the applicant or whether any executed agreement delegates that responsibility to an insured licensed engineer. The evidence is clear and consistent.

### G3 (implicit)

Allow positive credit for a documented rescue drill for every crew scheduled for confined-space entry during the policy period.

Expected `insufficient_evidence`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: Two crews are in scope but drill records are missing; absence of records does not prove drills did not happen or establish positive credit.

Candidate:

Assessment: The rule applies to crews scheduled for confined-space entry during the policy period. The evidence shows that two crews are scheduled for confined-space entry during the policy period (E30). The rule requires a documented rescue drill for every crew scheduled for confined-space entry. Evidence E30 states that 'Two crews are scheduled for confined-space entry during the policy period; rescue-drill records have been requested but are not yet supplied.' This indicates that while crews are scheduled, the required documentation (rescue drill records) has not been provided. Therefore, the condition is not met. The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no conflicting observations regarding the requirement for documented rescue drills. The only relevant observation is that rescue drill records have not been supplied, which does not create a contradiction with any other evidence.
scope_reason: The rule applies to crews scheduled for confined-space entry during the policy period. The evidence shows that two crews are scheduled for confined-space entry during the policy period (E30).
condition_reason: The rule requires a documented rescue drill for every crew scheduled for confined-space entry. Evidence E30 states that 'Two crews are scheduled for confined-space entry during the policy period; rescue-drill records have been requested but are not yet supplied.' This indicates that while crews are scheduled, the required documentation (rescue drill records) has not been provided. Therefore, the condition is not met.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case.
conflict_reason: There are no conflicting observations regarding the requirement for documented rescue drills. The only relevant observation is that rescue drill records have not been supplied, which does not create a contradiction with any other evidence.
