# First-use long-document holdout

State: **running**

Synthetic, author-labeled cases frozen before inference. Production code is unchanged. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 3/3 | 3/3 | 2/3 | 0/3 | False | False | False |
| cyber | 618 / 1424 | 3/3 | 3/3 | 3/3 | 3/3 | True | False | True |
| fleet | 632 / 1452 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |

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

Error: `{'type': 'ValueError', 'message': 'Source review must cover every document line exactly once'}`; judge error: `None`.

### G1 (explicit)

[concern] A heavy goods vehicle with an unresolved brake defect is a concern.

Expected `insufficient_evidence`; actual `missing`. Explanation: 0/10 (missing).

Reference: The equally authoritative H7 records conflict for the same date with no correction; abstain rather than select one report or emit a settled concern.

Candidate:

No explanation produced.

### G2 (explicit)

[strength] Completed annual driving-record reviews for all active drivers are a strength.

Expected `insufficient_evidence`; actual `missing`. Explanation: 0/10 (missing).

Reference: The register is missing. This does not prove that reviews were not performed; evidence is insufficient to establish all-driver coverage.

Candidate:

No explanation produced.

### G3 (implicit)

Give favorable treatment when verified telematics show a harsh-braking rate below 2 events per 1000 miles across the active fleet.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: 54 / 36000 * 1000 = 1.5, strictly below 2. Favorable treatment maps to strength.

Candidate:

No explanation produced.
