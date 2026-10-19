# First-use long-document holdout

State: **interrupted**

Synthetic, author-labeled cases frozen before inference. Production code is unchanged. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 3/3 | 3/3 | 2/3 | 0/3 | False | False | False |
| cyber | 618 / 1424 | 3/3 | 3/3 | 3/3 | 0/3 | False | False | False |

## property

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[concern] A cold-storage building whose roof is more than 25 years old is a concern unless a complete roof replacement has been documented within the last 2 years.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: Identify North and South separately: 28 and 31 exceed 25, with no replacement exception. East is excluded by its documented replacement/current age.

Candidate:

Assessment: The rule applies to cold-storage buildings, and the evidence identifies three refrigerated buildings (North, South, and East) that are the subject of the evaluation. The scope is in_scope as the rule's applicability is not explicitly restricted to exclude these buildings. For North building: roof age is 28 years, which exceeds 25 years; no complete replacement has occurred within the last 2 years (assessment date is 30 September 2026, and the latest replacement was on 1 March 2026, which is more than 2 years ago). For South building: roof age is 31 years, which exceeds 25 years; no complete replacement has occurred within the last 2 years. For East building: roof age is 0 years, which does not exceed 25 years, so this building does not meet the condition for concern based on roof age alone. The exception applies only if a complete roof replacement has been documented within the last 2 years. For North and South buildings, no such documentation exists. For East building, a complete replacement was documented on 1 March 2026, which is within the last 2 years (as of 30 September 2026). Therefore, the exception applies to East building but not to North or South. There are no conflicting pieces of evidence regarding the roof ages or replacement dates for the buildings. All relevant information is consistent and supports the determination of condition and exception status.
Finding: The North building's roof is 28 years old, which exceeds the 25-year threshold, and no complete replacement has been documented within the last 2 years. Therefore, it meets the condition for concern.
Finding: The South building's roof is 31 years old, which exceeds the 25-year threshold, and no complete replacement has been documented within the last 2 years. Therefore, it meets the condition for concern.

### G2 (explicit)

Current sprinkler inspection certificates with no outstanding deficiencies for every cold-storage building are a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: All three buildings have current certificates and no deficiencies; the all-buildings requirement is established.

Candidate:

Assessment: The rule applies to all cold-storage buildings. The subject is the three buildings (North, South, and East) operated by Alder. The period in scope is the current assessment date of 30 September 2026. Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations refuting this claim in the provided evidence. The rule does not contain an explicit exception. There is no indication that any of the buildings fall under an exception to the requirement for current sprinkler inspection certificates with no outstanding deficiencies. There are no conflicting observations regarding the sprinkler inspection certificates for any of the buildings. All observations support that each building has a current certificate with no outstanding deficiencies.
Finding: The sprinkler inspection certificate for the North building records no outstanding deficiencies, meeting the condition for this strength.
Finding: The sprinkler inspection certificate for the South building records no outstanding deficiencies, meeting the condition for this strength.
Finding: The sprinkler inspection certificate for the East building records no outstanding deficiencies, meeting the condition for this strength.
scope_reason: The rule applies to all cold-storage buildings. The subject is the three buildings (North, South, and East) operated by Alder. The period in scope is the current assessment date of 30 September 2026.
condition_reason: Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations refuting this claim in the provided evidence.
exception_reason: The rule does not contain an explicit exception. There is no indication that any of the buildings fall under an exception to the requirement for current sprinkler inspection certificates with no outstanding deficiencies.
conflict_reason: There are no conflicting observations regarding the sprinkler inspection certificates for any of the buildings. All observations support that each building has a current certificate with no outstanding deficiencies.

### G3 (explicit)

[concern] A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: The panels meet the trigger, but current independent approval for all three makes the stated exception apply; do not claim the panels are noncombustible.

Candidate:

Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, all of which are within the scope of the evaluation. Observation E32 states that 'All three buildings have combustible insulated wall panels; current independent fire-engineering certification approves those panels in North, South, and East.' This directly supports the trigger condition for each building. The rule's trigger is true for all three buildings. The rule includes an exception: 'unless a current independent fire-engineering certification approves those panels.' Observation E32 confirms that current independent fire-engineering certification does approve the combustible insulated wall panels in all three buildings (North, South, and East). Therefore, the exception applies to each building. There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of current independent fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible insulated wall panels and that current independent fire-engineering certifications approve those panels.
scope_reason: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, all of which are within the scope of the evaluation.
condition_reason: Observation E32 states that 'All three buildings have combustible insulated wall panels; current independent fire-engineering certification approves those panels in North, South, and East.' This directly supports the trigger condition for each building. The rule's trigger is true for all three buildings.
exception_reason: The rule includes an exception: 'unless a current independent fire-engineering certification approves those panels.' Observation E32 confirms that current independent fire-engineering certification does approve the combustible insulated wall panels in all three buildings (North, South, and East). Therefore, the exception applies to each building.
conflict_reason: There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of current independent fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible insulated wall panels and that current independent fire-engineering certifications approve those panels.


## cyber

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[strength] MFA on every active privileged account is a strength.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: 23/24 is not every account. The active emergency account is in scope and there is no exception; this is affirmative failure, not missing evidence.

Candidate:

Assessment: The rule applies to active privileged accounts within the scope of the assessment. The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. The remaining account is an active emergency administrator without MFA. The evidence states that 'MFA is enabled for 23 of the 24 active privileged accounts; the remaining account is an active emergency administrator without MFA.' This means that not every active privileged account has MFA enabled, which contradicts the trigger condition. Therefore, the rule's trigger does not hold. The rule does not contain any explicit exception prerequisites or validity dates. It simply states that MFA on every active privileged account is a strength without any conditions that would exempt certain accounts. There are no conflicting observations regarding the MFA status of the privileged accounts. The evidence clearly states that 23 out of 24 accounts have MFA enabled, and one account (emergency administrator) does not. These observations do not contradict each other in terms of the subject or time period.
scope_reason: The rule applies to active privileged accounts within the scope of the assessment. The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. The remaining account is an active emergency administrator without MFA.
condition_reason: The evidence states that 'MFA is enabled for 23 of the 24 active privileged accounts; the remaining account is an active emergency administrator without MFA.' This means that not every active privileged account has MFA enabled, which contradicts the trigger condition. Therefore, the rule's trigger does not hold.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates. It simply states that MFA on every active privileged account is a strength without any conditions that would exempt certain accounts.
conflict_reason: There are no conflicting observations regarding the MFA status of the privileged accounts. The evidence clearly states that 23 out of 24 accounts have MFA enabled, and one account (emergency administrator) does not. These observations do not contradict each other in terms of the subject or time period.

### G2 (explicit)

A successful isolated recovery test within the last 90 days is a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: 15 August is 46 days before 30 September, within 90; a successful isolated test is recorded.

Candidate:

Assessment: The rule applies to the subject of cyber security controls for the payroll service provider. The period in scope is the current assessment period ending 30 September 2026, as indicated by the submission date and the assessment context. An isolated payroll recovery test succeeded on 15 August 2026 (E21). The test was conducted within the last 90 days from the assessment date of 30 September 2026. The test log records restored data and a successful application start, confirming the success of the recovery test. Therefore, the condition is supported by evidence. The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no stated conditions under which this strength would not apply. There are no conflicting observations regarding the isolated recovery test within the last 90 days. The evidence clearly supports a successful test on 15 August 2026, which falls within the required timeframe.
Finding: An isolated payroll recovery test succeeded on 15 August 2026, which is within the last 90 days from the assessment date of 30 September 2026. The test log confirms restored data and a successful application start, satisfying the condition for this strength.
scope_reason: The rule applies to the subject of cyber security controls for the payroll service provider. The period in scope is the current assessment period ending 30 September 2026, as indicated by the submission date and the assessment context.
condition_reason: An isolated payroll recovery test succeeded on 15 August 2026 (E21). The test was conducted within the last 90 days from the assessment date of 30 September 2026. The test log records restored data and a successful application start, confirming the success of the recovery test. Therefore, the condition is supported by evidence.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no stated conditions under which this strength would not apply.
conflict_reason: There are no conflicting observations regarding the isolated recovery test within the last 90 days. The evidence clearly supports a successful test on 15 August 2026, which falls within the required timeframe.

### G3 (implicit)

Refer any account that stores unencrypted portable copies of payroll data for adverse treatment.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: Unencrypted portable payroll copies meet the referral rule; the guideline's vocabulary maps adverse treatment to concern.

Candidate:

Assessment: The rule applies to accounts storing unencrypted portable copies of payroll data. The subject is the Birch hosted payroll services account, and the period is current as of 30 September 2026. Evidence E31 states: 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that unencrypted portable copies of payroll data are stored. The evidence confirms the presence of unencrypted payroll data on portable drives, which meets the rule's requirement. The rule does not contain any explicit exception language. There is no stated exception that would apply to this situation. There are no conflicting observations regarding the storage of unencrypted portable copies of payroll data. The evidence clearly indicates that two USB drives hold unencrypted payroll exports.
Finding: Two portable USB drives currently hold unencrypted payroll exports used by the support team. This constitutes unencrypted portable copies of payroll data as required by the rule.
scope_reason: The rule applies to accounts storing unencrypted portable copies of payroll data. The subject is the Birch hosted payroll services account, and the period is current as of 30 September 2026.
condition_reason: Evidence E31 states: 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that unencrypted portable copies of payroll data are stored. The evidence confirms the presence of unencrypted payroll data on portable drives, which meets the rule's requirement.
exception_reason: The rule does not contain any explicit exception language. There is no stated exception that would apply to this situation.
conflict_reason: There are no conflicting observations regarding the storage of unencrypted portable copies of payroll data. The evidence clearly indicates that two USB drives hold unencrypted payroll exports.
