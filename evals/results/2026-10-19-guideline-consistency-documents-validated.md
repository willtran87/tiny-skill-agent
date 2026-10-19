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

Assessment: The rule applies to cold-storage buildings, and the evidence identifies three refrigerated buildings (North, South, and East) that are the subject of the assessment. The scope is in_scope because the rule's applicability is not explicitly restricted to any particular building or subset of buildings. The condition requires evaluating each building's roof age against the 25-year threshold and checking for documented complete replacement within the last 2 years. For North (28 years old, no replacement), South (31 years old, no replacement), and East (0 years old, replaced on 1 March 2026), only North and South meet the age criterion (>25 years) and lack recent replacement documentation. East does not meet the age threshold, so it is not a concern under this rule. The exception applies when 'a complete roof replacement has been documented within the last 2 years.' For North and South buildings, there is no documentation of replacement within the last 2 years. East building had a replacement on 1 March 2026, which is within the last 2 years (as of 30 September 2026), so it satisfies the exception. There are no conflicting pieces of evidence regarding roof ages or replacement documentation for the buildings. All relevant information is clearly stated in the submission documents.
Finding: The North building's roof is 28 years old, exceeding the 25-year threshold, and no complete replacement has been documented within the last 2 years, making it a concern under criterion C1.
Finding: The South building's roof is 31 years old, exceeding the 25-year threshold, and no complete replacement has been documented within the last 2 years, making it a concern under criterion C1.

### G2 (explicit)

Current sprinkler inspection certificates with no outstanding deficiencies for every cold-storage building are a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: All three buildings have current certificates and no deficiencies; the all-buildings requirement is established.

Candidate:

Assessment: The rule applies to all cold-storage buildings. The subject is the three refrigerated buildings (North, South, and East) operated by Alder. The period in scope is current as of the assessment date 30 September 2026. The evidence shows that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations indicating outstanding deficiencies on any of the certificates. There is no explicit exception stated in the rule text that would apply to this case. The rule does not contain any 'unless' or 'except' clauses that would modify its application. There are no conflicting observations regarding the sprinkler inspection certificates for any of the buildings. All three buildings have current certificates with no outstanding deficiencies recorded.
Finding: The sprinkler inspection certificate for the North building records no outstanding deficiencies, meeting the condition of the rule.
Finding: The sprinkler inspection certificate for the South building records no outstanding deficiencies, meeting the condition of the rule.
Finding: The sprinkler inspection certificate for the East building records no outstanding deficiencies, meeting the condition of the rule.
scope_reason: The rule applies to all cold-storage buildings. The subject is the three refrigerated buildings (North, South, and East) operated by Alder. The period in scope is current as of the assessment date 30 September 2026.
condition_reason: The evidence shows that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations indicating outstanding deficiencies on any of the certificates.
exception_reason: There is no explicit exception stated in the rule text that would apply to this case. The rule does not contain any 'unless' or 'except' clauses that would modify its application.
conflict_reason: There are no conflicting observations regarding the sprinkler inspection certificates for any of the buildings. All three buildings have current certificates with no outstanding deficiencies recorded.

### G3 (explicit)

[concern] A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: The panels meet the trigger, but current independent approval for all three makes the stated exception apply; do not claim the panels are noncombustible.

Candidate:

Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, as identified in the application. The period in scope is the present assessment date of 30 September 2026. Observation E32 states that 'All three buildings have combustible insulated wall panels' and 'current independent fire-engineering certification approves those panels in North, South, and East.' This directly supports the trigger condition for each building. The rule's exception is met for all three buildings because current certifications approve the panels. The rule explicitly states an exception: 'A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.' Since E32 confirms that current independent fire-engineering certification approves the panels in all three buildings (North, South, and East), the exception applies to each of them. There are no incompatible observations regarding the combustible wall panels or fire-engineering certifications for any of the buildings. The evidence consistently shows that all three buildings have combustible insulated wall panels and that current independent fire-engineering certification approves those panels.
scope_reason: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, as identified in the application. The period in scope is the present assessment date of 30 September 2026.
condition_reason: Observation E32 states that 'All three buildings have combustible insulated wall panels' and 'current independent fire-engineering certification approves those panels in North, South, and East.' This directly supports the trigger condition for each building. The rule's exception is met for all three buildings because current certifications approve the panels.
exception_reason: The rule explicitly states an exception: 'A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.' Since E32 confirms that current independent fire-engineering certification approves the panels in all three buildings (North, South, and East), the exception applies to each of them.
conflict_reason: There are no incompatible observations regarding the combustible wall panels or fire-engineering certifications for any of the buildings. The evidence consistently shows that all three buildings have combustible insulated wall panels and that current independent fire-engineering certification approves those panels.


## cyber

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[strength] MFA on every active privileged account is a strength.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: 23/24 is not every account. The active emergency account is in scope and there is no exception; this is affirmative failure, not missing evidence.

Candidate:

Assessment: The rule applies to active privileged accounts within the scope of the assessment period. The subject is the privileged access inventory, which contains 24 active accounts as of the submission date (30 September 2026). Evidence E8 states that there are 24 active privileged accounts. Evidence E9 indicates that MFA is enabled for 23 of these 24 accounts, with one account (an active emergency administrator) lacking MFA. Since the rule requires MFA on 'every' active privileged account to be a strength, and one account does not have MFA, the trigger condition is false. The rule does not contain any explicit exception prerequisites or validity dates that would apply in this case. There is no indication of an exception that would override the requirement for MFA on all active privileged accounts. There are no conflicting observations regarding the presence or absence of MFA on privileged accounts. The evidence clearly indicates that 23 out of 24 accounts have MFA enabled, with one exception. No unresolved contradictions exist between different pieces of evidence concerning the same subject and time period.
scope_reason: The rule applies to active privileged accounts within the scope of the assessment period. The subject is the privileged access inventory, which contains 24 active accounts as of the submission date (30 September 2026).
condition_reason: Evidence E8 states that there are 24 active privileged accounts. Evidence E9 indicates that MFA is enabled for 23 of these 24 accounts, with one account (an active emergency administrator) lacking MFA. Since the rule requires MFA on 'every' active privileged account to be a strength, and one account does not have MFA, the trigger condition is false.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates that would apply in this case. There is no indication of an exception that would override the requirement for MFA on all active privileged accounts.
conflict_reason: There are no conflicting observations regarding the presence or absence of MFA on privileged accounts. The evidence clearly indicates that 23 out of 24 accounts have MFA enabled, with one exception. No unresolved contradictions exist between different pieces of evidence concerning the same subject and time period.

### G2 (explicit)

A successful isolated recovery test within the last 90 days is a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: 15 August is 46 days before 30 September, within 90; a successful isolated test is recorded.

Candidate:

Assessment: The rule applies to the subject of cyber security controls for the payroll service provider. The period in scope is the time around the assessment date 30 September 2026, as the rule refers to tests 'within the last 90 days'. Evidence E21 states: 'An isolated payroll recovery test succeeded on 15 August 2026; the test log records restored data and a successful application start.' The test occurred on 15 August 2026, which is within 90 days of the assessment date 30 September 2026. Therefore, the condition is supported by evidence. The rule does not contain an explicit exception. There are no stated validity dates or prerequisites for exceptions that would apply here. There are no conflicting observations regarding the isolated recovery test in the provided evidence. The single observation confirms a successful test within the required timeframe.
Finding: An isolated payroll recovery test was successfully completed on 15 August 2026, which falls within the last 90 days prior to the assessment date of 30 September 2026. This satisfies the condition for a strength as defined by the rule.
scope_reason: The rule applies to the subject of cyber security controls for the payroll service provider. The period in scope is the time around the assessment date 30 September 2026, as the rule refers to tests 'within the last 90 days'.
condition_reason: Evidence E21 states: 'An isolated payroll recovery test succeeded on 15 August 2026; the test log records restored data and a successful application start.' The test occurred on 15 August 2026, which is within 90 days of the assessment date 30 September 2026. Therefore, the condition is supported by evidence.
exception_reason: The rule does not contain an explicit exception. There are no stated validity dates or prerequisites for exceptions that would apply here.
conflict_reason: There are no conflicting observations regarding the isolated recovery test in the provided evidence. The single observation confirms a successful test within the required timeframe.

### G3 (implicit)

Refer any account that stores unencrypted portable copies of payroll data for adverse treatment.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: Unencrypted portable payroll copies meet the referral rule; the guideline's vocabulary maps adverse treatment to concern.

Candidate:

Assessment: The rule applies to accounts storing unencrypted portable copies of payroll data. The subject is the applicant's storage of payroll data on portable devices. The period in scope is the present assessment date, 30 September 2026. Evidence E31 states that 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence confirms the presence of unencrypted payroll data on portable devices, which meets the rule's requirement. The rule does not contain an explicit exception. There are no stated prerequisites or validity dates for exceptions to this rule. There are no conflicting observations regarding the storage of unencrypted portable copies of payroll data. The evidence clearly indicates that two USB drives hold unencrypted payroll exports, which satisfies the rule's condition.
Finding: Two portable USB drives currently hold unencrypted payroll exports used by the support team. This constitutes unencrypted portable copies of payroll data stored on accounts, triggering the rule's condition for adverse treatment.
scope_reason: The rule applies to accounts storing unencrypted portable copies of payroll data. The subject is the applicant's storage of payroll data on portable devices. The period in scope is the present assessment date, 30 September 2026.
condition_reason: Evidence E31 states that 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence confirms the presence of unencrypted payroll data on portable devices, which meets the rule's requirement.
exception_reason: The rule does not contain an explicit exception. There are no stated prerequisites or validity dates for exceptions to this rule.
conflict_reason: There are no conflicting observations regarding the storage of unencrypted portable copies of payroll data. The evidence clearly indicates that two USB drives hold unencrypted payroll exports, which satisfies the rule's condition.
