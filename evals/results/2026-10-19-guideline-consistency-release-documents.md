# Long-document regression rerun

This is a rerun after these fixtures informed development, not a fresh holdout. See [the comparison and separate explanation audit](2026-10-19-guideline-consistency-comparison.md). The table below retains the frozen automatic scorer and its judge failures.

State: **completed**

Synthetic, author-labeled cases with unchanged fixtures and scoring. Production code was frozen during this rerun. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 3/3 | 3/3 | 2/3 | 3/3 | False | False | False |
| cyber | 618 / 1424 | 3/3 | 2/3 | 3/3 | 0/3 | False | False | False |
| fleet | 632 / 1452 | 3/3 | 3/3 | 3/3 | 3/3 | False | False | False |
| manufacturing | 636 / 1419 | 3/3 | 3/3 | 3/3 | 0/3 | False | False | False |
| hospitality | 635 / 1427 | 3/3 | 3/3 | 3/3 | 3/3 | False | False | False |
| contractor | 640 / 1425 | 3/3 | 3/3 | 3/3 | 3/3 | False | False | True |

## property

Error: `None`; judge error: `None`.

### G1 (explicit)

[concern] A cold-storage building whose roof is more than 25 years old is a concern unless a complete roof replacement has been documented within the last 2 years.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: Identify North and South separately: 28 and 31 exceed 25, with no replacement exception. East is excluded by its documented replacement/current age.

Candidate:

Assessment: The rule applies to cold-storage buildings, and the evidence identifies three such buildings: North, South, and East. The scope is in_scope because the rule's population includes these individual buildings. For each building, the roof age is determined from the evidence: North building roof age is 28 years; South building roof age is 31 years; East building roof age is 0 years. The condition requires that a building's roof be more than 25 years old to be a concern. Both North and South buildings meet this threshold (28 > 25 and 31 > 25). The exception applies if a complete roof replacement has been documented within the last 2 years. For East building, this is met as the replacement occurred on 1 March 2026, which is within the last 2 years from the assessment date (30 September 2026). For North and South buildings, no such documentation exists, so they do not meet the exception. There are no conflicting pieces of evidence regarding roof ages or replacement dates for any building. The information is clear and consistent across the provided evidence.
Finding: The North building has a roof age of 28 years, which exceeds the 25-year threshold. No complete roof replacement has been documented within the last 2 years, so it meets the condition for concern.
Finding: The South building has a roof age of 31 years, which exceeds the 25-year threshold. No complete roof replacement has been documented within the last 2 years, so it meets the condition for concern.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to individual cold-storage buildings and properly includes all relevant buildings (North, South, East) in the scope. Excerpt: "Assessment: The rule applies to cold-storage buildings, and the evidence identifies three such buildings: North, South, and East. The scope is in_scope because the rule's population includes these individual buildings."
- factual_grounding: 2/2. The candidate accurately cites and applies the roof ages from the evidence (28, 31, 0 years) to evaluate each building against the rule's threshold. Excerpt: "For each building, the roof age is determined from the evidence: North building roof age is 28 years; South building roof age is 31 years; East building roof age is 0 years."
- scope_and_exceptions: 2/2. The candidate correctly identifies that North and South exceed the 25-year threshold, properly applies the exception for East due to recent replacement, and excludes East from concern while including North and South. Excerpt: "The condition requires that a building's roof be more than 25 years old to be a concern. Both North and South buildings meet this threshold (28 > 25 and 31 > 25). The exception applies if a complete roof replacement has been documented within the last 2 years. For East building, this is met as the replacement occurred on 1 March 2026, which is within the last 2 years from the assessment date (30 September 2026). For North and South buildings, no such documentation exists, so they do not meet the exception."
- logical_support: 2/2. The logical flow clearly explains why North and South are concerns (age > 25, no replacement) and why East is not (age 0, replacement within 2 years), with correct arithmetic and reasoning. Excerpt: "Both North and South buildings meet this threshold (28 > 25 and 31 > 25). The exception applies if a complete roof replacement has been documented within the last 2 years. For East building, this is met as the replacement occurred on 1 March 2026, which is within the last 2 years from the assessment date (30 September 2026). For North and South buildings, no such documentation exists, so they do not meet the exception."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims, clearly states that there are no contradictions in the evidence, and bases all conclusions on cited facts. Excerpt: "There are no conflicting pieces of evidence regarding roof ages or replacement dates for any building. The information is clear and consistent across the provided evidence."
### G2 (explicit)

Current sprinkler inspection certificates with no outstanding deficiencies for every cold-storage building are a strength.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: All three buildings have current certificates and no deficiencies; the all-buildings requirement is established.

Candidate:

Assessment: The rule applies to all cold-storage buildings, which are North, South, and East. The assessment date is 30 September 2026. Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations indicating outstanding deficiencies for any of the buildings. The rule does not contain an explicit exception that would apply to this case. The rule simply requires current certificates with no outstanding deficiencies for every cold-storage building, without additional prerequisites or conditions. There are no conflicting observations regarding the sprinkler inspection certificates for any of the buildings. All three buildings have current certificates with no outstanding deficiencies as stated in E22.
Finding: The sprinkler inspection certificate for the North building records no outstanding deficiencies, satisfying the condition.
Finding: The sprinkler inspection certificate for the South building records no outstanding deficiencies, satisfying the condition.
Finding: The sprinkler inspection certificate for the East building records no outstanding deficiencies, satisfying the condition.
scope_reason: The rule applies to all cold-storage buildings, which are North, South, and East. The assessment date is 30 September 2026.
condition_reason: Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations indicating outstanding deficiencies for any of the buildings.
exception_reason: The rule does not contain an explicit exception that would apply to this case. The rule simply requires current certificates with no outstanding deficiencies for every cold-storage building, without additional prerequisites or conditions.
conflict_reason: There are no conflicting observations regarding the sprinkler inspection certificates for any of the buildings. All three buildings have current certificates with no outstanding deficiencies as stated in E22.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to all cold-storage buildings and includes the relevant buildings in scope. Excerpt: "Assessment: The rule applies to all cold-storage buildings, which are North, South, and East."
- factual_grounding: 2/2. The candidate accurately cites the evidence (E22) and correctly applies it to support that all buildings meet the rule's conditions. Excerpt: "Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings."
- scope_and_exceptions: 2/2. The candidate correctly identifies the scope as all three buildings and notes the relevant assessment date. Excerpt: "The rule applies to all cold-storage buildings, which are North, South, and East. The assessment date is 30 September 2026."
- logical_support: 2/2. The candidate clearly explains how the evidence satisfies the rule's requirements for all buildings with no logical gaps or unsupported assumptions. Excerpt: "Evidence E22 states that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly supports the trigger condition for all three buildings. There are no observations indicating outstanding deficiencies for any of the buildings."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and correctly notes that there are no exceptions or contradictions in the evidence. Excerpt: "There are no observations indicating outstanding deficiencies for any of the buildings. The rule does not contain an explicit exception that would apply to this case."
### G3 (explicit)

[concern] A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.

Expected `no_match`; actual `no_match`. Explanation: 10/10 (graded).

Reference: The panels meet the trigger, but current independent approval for all three makes the stated exception apply; do not claim the panels are noncombustible.

Candidate:

Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, as identified in the application. The period in scope is the present assessment date of 30 September 2026. Observation E32 states that 'All three buildings have combustible insulated wall panels' and 'current independent fire-engineering certification approves those panels in North, South, and East.' This directly supports the trigger condition for each building. The rule's exception is met for all three buildings because each has current independent fire-engineering certification approving the combustible panels. The rule explicitly states an exception: 'unless a current independent fire-engineering certification approves those panels.' Evidence E32 confirms that current independent fire-engineering certification does approve the panels in all three buildings (North, South, and East). Therefore, the exception applies to all three buildings. There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of current independent fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible panels and that certification approves them.
scope_reason: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, as identified in the application. The period in scope is the present assessment date of 30 September 2026.
condition_reason: Observation E32 states that 'All three buildings have combustible insulated wall panels' and 'current independent fire-engineering certification approves those panels in North, South, and East.' This directly supports the trigger condition for each building. The rule's exception is met for all three buildings because each has current independent fire-engineering certification approving the combustible panels.
exception_reason: The rule explicitly states an exception: 'unless a current independent fire-engineering certification approves those panels.' Evidence E32 confirms that current independent fire-engineering certification does approve the panels in all three buildings (North, South, and East). Therefore, the exception applies to all three buildings.
conflict_reason: There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of current independent fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible panels and that certification approves them.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to individual buildings and includes all relevant ones (North, South, East) in scope. Excerpt: "Assessment: The rule applies to individual cold-storage buildings. The subject buildings are North, South, and East, as identified in the application."
- factual_grounding: 2/2. The candidate accurately cites the evidence (E32) and correctly applies it to show that all buildings meet the rule's trigger condition. Excerpt: "Observation E32 states that 'All three buildings have combustible insulated wall panels' and 'current independent fire-engineering certification approves those panels in North, South, and East.' This directly supports the trigger condition for each building."
- scope_and_exceptions: 2/2. The candidate correctly identifies that the exception applies to all buildings due to the certification, and properly explains how this negates the concern. Excerpt: "The rule's exception is met for all three buildings because each has current independent fire-engineering certification approving the combustible panels. The rule explicitly states an exception: 'unless a current independent fire-engineering certification approves those panels.' Evidence E32 confirms that current independent fire-engineering certification does approve the panels in all three buildings (North, South, and East). Therefore, the exception applies to all three buildings."
- logical_support: 2/2. The candidate clearly explains how the evidence satisfies the rule's exception condition for all buildings, correctly applying the logic of the rule. Excerpt: "The rule explicitly states an exception: 'unless a current independent fire-engineering certification approves those panels.' Evidence E32 confirms that current independent fire-engineering certification does approve the panels in all three buildings (North, South, and East). Therefore, the exception applies to all three buildings."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims, clearly states there are no contradictions, and bases conclusions solely on cited facts. Excerpt: "There are no conflicting observations regarding the presence of combustible insulated wall panels or the existence of current independent fire-engineering certifications for any of the buildings. The evidence consistently supports that all three buildings have combustible panels and that certification approves them."

## cyber

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[strength] MFA on every active privileged account is a strength.

Expected `no_match`; actual `insufficient_evidence`. Explanation: 0/10 (judge_error).

Reference: 23/24 is not every account. The active emergency account is in scope and there is no exception; this is affirmative failure, not missing evidence.

Candidate:

Assessment: The rule applies to active privileged accounts. The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. One account (emergency administrator) is active but does not have MFA. The evidence states that 'MFA is enabled for 23 of the 24 active privileged accounts; the remaining account is an active emergency administrator without MFA.' This directly contradicts the rule's requirement that MFA be on 'every' active privileged account. The trigger condition is false because one active privileged account lacks MFA. The rule does not contain any explicit exception language. There are no prerequisites or validity dates mentioned for an exception to apply. There is a direct contradiction between the rule's requirement that MFA be on every active privileged account and the evidence showing one active account (emergency administrator) without MFA. This constitutes an actual incompatible observation.
scope_reason: The rule applies to active privileged accounts. The evidence shows there are 24 active privileged accounts, and MFA is enabled for 23 of them. One account (emergency administrator) is active but does not have MFA.
condition_reason: The evidence states that 'MFA is enabled for 23 of the 24 active privileged accounts; the remaining account is an active emergency administrator without MFA.' This directly contradicts the rule's requirement that MFA be on 'every' active privileged account. The trigger condition is false because one active privileged account lacks MFA.
exception_reason: The rule does not contain any explicit exception language. There are no prerequisites or validity dates mentioned for an exception to apply.
conflict_reason: There is a direct contradiction between the rule's requirement that MFA be on every active privileged account and the evidence showing one active account (emergency administrator) without MFA. This constitutes an actual incompatible observation.

### G2 (explicit)

A successful isolated recovery test within the last 90 days is a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: 15 August is 46 days before 30 September, within 90; a successful isolated test is recorded.

Candidate:

Assessment: The rule applies to the subject of isolated recovery testing, which is relevant to cybersecurity controls. The period in scope is the last 90 days from the assessment date (30 September 2026). An isolated payroll recovery test succeeded on 15 August 2026 (E21). The test log records restored data and a successful application start. The assessment date is 30 September 2026, so the test occurred within the last 90 days (15 August to 30 September = 46 days). This supports the trigger condition. The rule does not contain an explicit exception. There are no stated validity dates or prerequisites for exceptions that would apply here. There are no conflicting observations regarding the isolated recovery test. The single observation confirms a successful test within the required timeframe.
Finding: An isolated payroll recovery test succeeded on 15 August 2026, which falls within the last 90 days from the assessment date of 30 September 2026. This meets the condition for a strength as defined by the rule.
scope_reason: The rule applies to the subject of isolated recovery testing, which is relevant to cybersecurity controls. The period in scope is the last 90 days from the assessment date (30 September 2026).
condition_reason: An isolated payroll recovery test succeeded on 15 August 2026 (E21). The test log records restored data and a successful application start. The assessment date is 30 September 2026, so the test occurred within the last 90 days (15 August to 30 September = 46 days). This supports the trigger condition.
exception_reason: The rule does not contain an explicit exception. There are no stated validity dates or prerequisites for exceptions that would apply here.
conflict_reason: There are no conflicting observations regarding the isolated recovery test. The single observation confirms a successful test within the required timeframe.

### G3 (implicit)

Refer any account that stores unencrypted portable copies of payroll data for adverse treatment.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: Unencrypted portable payroll copies meet the referral rule; the guideline's vocabulary maps adverse treatment to concern.

Candidate:

Assessment: The rule applies to accounts that store unencrypted portable copies of payroll data. The subject is the account storing such data, and the period in scope is the current assessment date (30 September 2026). Evidence E31 states: 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence identifies specific storage devices (USB drives) containing unencrypted payroll data, which meets the rule's requirement. The rule does not contain any explicit exception prerequisites or validity dates. There is no exception stated that would apply to this situation. There are no conflicting observations regarding the storage of unencrypted portable copies of payroll data. The evidence clearly identifies two USB drives holding unencrypted payroll exports, with no contradictory information provided.
Finding: The evidence shows that two portable USB drives currently hold unencrypted payroll exports used by the support team. This directly satisfies the rule's trigger condition that accounts store unencrypted portable copies of payroll data, warranting referral for adverse treatment.
scope_reason: The rule applies to accounts that store unencrypted portable copies of payroll data. The subject is the account storing such data, and the period in scope is the current assessment date (30 September 2026).
condition_reason: Evidence E31 states: 'Two portable USB drives currently hold unencrypted payroll exports used by the support team.' This directly supports the trigger condition that accounts store unencrypted portable copies of payroll data. The evidence identifies specific storage devices (USB drives) containing unencrypted payroll data, which meets the rule's requirement.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates. There is no exception stated that would apply to this situation.
conflict_reason: There are no conflicting observations regarding the storage of unencrypted portable copies of payroll data. The evidence clearly identifies two USB drives holding unencrypted payroll exports, with no contradictory information provided.


## fleet

Error: `None`; judge error: `None`.

### G1 (explicit)

[concern] A heavy goods vehicle with an unresolved brake defect is a concern.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 10/10 (graded).

Reference: The equally authoritative H7 records conflict for the same date with no correction; abstain rather than select one report or emit a settled concern.

Candidate:

Assessment: The rule applies to heavy goods vehicles. The evidence mentions that Cedar operates a fleet with eight heavy goods vehicles, and specifically identifies vehicle H7 as having an unresolved brake defect. Evidence E8 states 'Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect.' Evidence E9 states 'Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other.' These two observations directly contradict each other regarding vehicle H7. Since there is no correction or resolution provided for this contradiction, and both inspectors are noted as equally authoritative, the actual state of the brake defect on vehicle H7 remains unresolved. Therefore, the condition 'A heavy goods vehicle with an unresolved brake defect is a concern' is true. The rule does not contain any explicit exception language. There are no stated validity dates or prerequisites for exceptions that would apply to this case. There is a direct contradiction between E8 and E9 regarding the brake defect status of vehicle H7. Inspector A recorded an unresolved brake defect, while Inspector B recorded no brake defect. Since neither report corrects the other and both are equally authoritative, this creates an unresolved conflict about the specific state of vehicle H7's brakes at the time of inspection.
scope_reason: The rule applies to heavy goods vehicles. The evidence mentions that Cedar operates a fleet with eight heavy goods vehicles, and specifically identifies vehicle H7 as having an unresolved brake defect.
condition_reason: Evidence E8 states 'Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect.' Evidence E9 states 'Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other.' These two observations directly contradict each other regarding vehicle H7. Since there is no correction or resolution provided for this contradiction, and both inspectors are noted as equally authoritative, the actual state of the brake defect on vehicle H7 remains unresolved. Therefore, the condition 'A heavy goods vehicle with an unresolved brake defect is a concern' is true.
exception_reason: The rule does not contain any explicit exception language. There are no stated validity dates or prerequisites for exceptions that would apply to this case.
conflict_reason: There is a direct contradiction between E8 and E9 regarding the brake defect status of vehicle H7. Inspector A recorded an unresolved brake defect, while Inspector B recorded no brake defect. Since neither report corrects the other and both are equally authoritative, this creates an unresolved conflict about the specific state of vehicle H7's brakes at the time of inspection.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to heavy goods vehicles, which is the trigger for the assessment. This aligns with the reference's classification of the concern as applying to heavy goods vehicles. Excerpt: "Assessment: The rule applies to heavy goods vehicles."
- factual_grounding: 2/2. The excerpt accurately cites the specific evidence from the documents, correctly identifying the conflicting reports regarding vehicle H7's brake defect status. This directly supports the factual basis for the conclusion. Excerpt: "Evidence E8 states 'Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect.' Evidence E9 states 'Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other.'"
- scope_and_exceptions: 2/2. This excerpt correctly identifies the absence of exception language in the rule, which is relevant to the scope and supports the conclusion that no exceptions apply. Excerpt: "The rule does not contain any explicit exception language. There are no stated validity dates or prerequisites for exceptions that would apply to this case."
- logical_support: 2/2. The excerpt provides logical reasoning that connects the conflicting evidence to the conclusion that the condition is met, explaining why the unresolved defect constitutes a concern. Excerpt: "Since there is no correction or resolution provided for this contradiction, and both inspectors are noted as equally authoritative, the actual state of the brake defect on vehicle H7 remains unresolved. Therefore, the condition 'A heavy goods vehicle with an unresolved brake defect is a concern' is true."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by directly referencing the evidence and clearly stating that the contradiction is unresolved, without introducing assumptions or fabricated facts. Excerpt: "There is a direct contradiction between E8 and E9 regarding the brake defect status of vehicle H7. Inspector A recorded an unresolved brake defect, while Inspector B recorded no brake defect. Since neither report corrects the other and both are equally authoritative, this creates an unresolved conflict about the specific state of vehicle H7's brakes at the time of inspection."
### G2 (explicit)

[strength] Completed annual driving-record reviews for all active drivers are a strength.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 10/10 (graded).

Reference: The register is missing. This does not prove that reviews were not performed; evidence is insufficient to establish all-driver coverage.

Candidate:

Assessment: The criterion requires that annual driving-record reviews have been completed for all active drivers. Evidence E22 states that there are 18 active drivers and that the broker has requested but not received the annual driving-record review register. Since the register has not been provided, it cannot be determined whether reviews were completed for all drivers. The absence of the register does not prove that reviews were not done, but rather indicates a gap in documentation that prevents verification of the criterion's condition.

- rule_application: 2/2. The excerpt correctly identifies the rule's application to annual driving-record reviews for all active drivers, which is the core of the assessment. Excerpt: "Assessment: The criterion requires that annual driving-record reviews have been completed for all active drivers."
- factual_grounding: 2/2. The excerpt accurately cites the evidence regarding the number of active drivers and the missing register, grounding the explanation in factual data. Excerpt: "Evidence E22 states that there are 18 active drivers and that the broker has requested but not received the annual driving-record review register."
- scope_and_exceptions: 2/2. This excerpt correctly addresses the scope by acknowledging that the lack of documentation does not confirm non-compliance but highlights a gap in evidence. Excerpt: "The absence of the register does not prove that reviews were not done, but rather indicates a gap in documentation that prevents verification of the criterion's condition."
- logical_support: 2/2. The excerpt logically explains why insufficient evidence leads to an 'insufficient_evidence' status, connecting the missing register to the inability to verify compliance. Excerpt: "Since the register has not been provided, it cannot be determined whether reviews were completed for all drivers. The absence of the register does not prove that reviews were not done, but rather indicates a gap in documentation that prevents verification of the criterion's condition."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by clearly stating that the lack of evidence does not confirm non-compliance, which is consistent with the reference rationale. Excerpt: "The absence of the register does not prove that reviews were not done, but rather indicates a gap in documentation that prevents verification of the criterion's condition."
### G3 (implicit)

Give favorable treatment when verified telematics show a harsh-braking rate below 2 events per 1000 miles across the active fleet.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: 54 / 36000 * 1000 = 1.5, strictly below 2. Favorable treatment maps to strength.

Candidate:

Assessment: The rule applies to the active fleet as a whole, and the evidence includes a verified active-fleet telematics report covering all heavy goods vehicles in the fleet. The subject is the entire active fleet during the reporting period. The verified active-fleet telematics report (E32) records 54 harsh-braking events over 36000 miles. Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile = 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met. The calculation shows that the harsh-braking rate is below the threshold of 2 events per 1000 miles. The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no stated conditions under which this rule would not apply. There are no conflicting observations regarding the harsh-braking rate or the telematics data in the evidence. The single telematics report provides a clear and consistent measure of fleet performance.
Finding: The verified active-fleet telematics report shows 54 harsh-braking events over 36000 miles, which calculates to 1.5 events per 1000 miles. This rate is below the threshold of 2 events per 1000 miles required for favorable treatment.
scope_reason: The rule applies to the active fleet as a whole, and the evidence includes a verified active-fleet telematics report covering all heavy goods vehicles in the fleet. The subject is the entire active fleet during the reporting period.
condition_reason: The verified active-fleet telematics report (E32) records 54 harsh-braking events over 36000 miles. Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile = 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met. The calculation shows that the harsh-braking rate is below the threshold of 2 events per 1000 miles.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no stated conditions under which this rule would not apply.
conflict_reason: There are no conflicting observations regarding the harsh-braking rate or the telematics data in the evidence. The single telematics report provides a clear and consistent measure of fleet performance.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to the entire active fleet, which is essential for applying the correct scope. Excerpt: "Assessment: The rule applies to the active fleet as a whole, and the evidence includes a verified active-fleet telematics report covering all heavy goods vehicles in the fleet."
- factual_grounding: 2/2. This excerpt accurately cites the specific evidence and provides the factual data needed to support the calculation and conclusion. Excerpt: "The verified active-fleet telematics report (E32) records 54 harsh-braking events over 36000 miles."
- scope_and_exceptions: 2/2. The excerpt correctly identifies the absence of exceptions, which is relevant for determining the scope and confirming that the rule applies without limitation. Excerpt: "The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There are no stated conditions under which this rule would not apply."
- logical_support: 2/2. The excerpt provides clear arithmetic and logical reasoning that directly supports the conclusion that the harsh-braking rate meets the threshold. Excerpt: "Calculating the rate: 54 events / 36000 miles = 0.0015 events per mile = 1.5 events per 1000 miles. Since 1.5 is less than 2, the condition is met."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by affirming that there is no conflict in the data, which supports the validity of the calculation and conclusion. Excerpt: "There are no conflicting observations regarding the harsh-braking rate or the telematics data in the evidence. The single telematics report provides a clear and consistent measure of fleet performance."

## manufacturing

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (implicit)

Decline operations using a production press without an interlocked guard.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: P4 is in use and unguarded; a proposed retrofit is not completion. Decline maps to concern.

Candidate:

Assessment: The rule applies to operations using a production press. The subject is the production press P4, which is mentioned in the technical exhibit (E8). The period in scope is the current assessment date of 30 September 2026. Evidence E8 states that 'Production press P4 remains in daily use without an interlocked guard; the proposed retrofit has not been ordered.' This directly supports the trigger condition that operations are being conducted using a production press without an interlocked guard. There is no evidence of an interlocked guard being installed or ordered. The rule does not contain any explicit exception language. There is no indication that any exception prerequisites are met. There are no conflicting observations regarding the presence or absence of an interlocked guard on production press P4. The evidence clearly states that the press remains in daily use without an interlocked guard.
Finding: The production press P4 is in daily use without an interlocked guard, which directly triggers the rule's condition. No evidence exists of an interlocked guard being installed or ordered.
scope_reason: The rule applies to operations using a production press. The subject is the production press P4, which is mentioned in the technical exhibit (E8). The period in scope is the current assessment date of 30 September 2026.
condition_reason: Evidence E8 states that 'Production press P4 remains in daily use without an interlocked guard; the proposed retrofit has not been ordered.' This directly supports the trigger condition that operations are being conducted using a production press without an interlocked guard. There is no evidence of an interlocked guard being installed or ordered.
exception_reason: The rule does not contain any explicit exception language. There is no indication that any exception prerequisites are met.
conflict_reason: There are no conflicting observations regarding the presence or absence of an interlocked guard on production press P4. The evidence clearly states that the press remains in daily use without an interlocked guard.

### G2 (implicit)

Allow positive credit when completed hot-work permits and fire-watch records cover every hot-work job in the last 12 months.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: All 9 jobs have both required records over the required period; positive credit maps to strength.

Candidate:

Assessment: The rule applies to hot-work jobs in the last 12 months, with the assessment date being 30 September 2026. The subject is the applicant's hot-work practices during this period. Evidence E20 states that 'The complete 12-month hot-work register lists 9 jobs; signed permits and completed fire-watch records are attached for all 9.' This directly supports that all 9 hot-work jobs in the last 12 months have corresponding completed permits and fire-watch records. Therefore, the condition is true. The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There is no indication of an exception that would prevent the application of the rule. There are no conflicting observations regarding hot-work permits or fire-watch records in the last 12 months. All documented jobs have supporting records, and there is no indication of any contradiction in the evidence.
Finding: All 9 hot-work jobs in the last 12 months have corresponding completed hot-work permits and fire-watch records as documented in E20.
scope_reason: The rule applies to hot-work jobs in the last 12 months, with the assessment date being 30 September 2026. The subject is the applicant's hot-work practices during this period.
condition_reason: Evidence E20 states that 'The complete 12-month hot-work register lists 9 jobs; signed permits and completed fire-watch records are attached for all 9.' This directly supports that all 9 hot-work jobs in the last 12 months have corresponding completed permits and fire-watch records. Therefore, the condition is true.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates that would apply to this case. There is no indication of an exception that would prevent the application of the rule.
conflict_reason: There are no conflicting observations regarding hot-work permits or fire-watch records in the last 12 months. All documented jobs have supporting records, and there is no indication of any contradiction in the evidence.

### G3 (implicit)

Refer a finishing area with flammable liquids in open containers, except while the liquids are inside an approved enclosed dispensing system.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: The recorded enclosed system meets the exception and there is no open-container exposure outside it; no concern should be emitted.

Candidate:

Assessment: The rule applies to the finishing area where flammable liquids are handled. The subject is the finishing area's handling of flammable liquids, and the period in scope is the current assessment period (30 September 2026). Evidence E30 states that 'The finishing-area liquids are entirely inside an approved enclosed dispensing system; no containers are open outside it.' This directly supports the trigger condition that flammable liquids are not in open containers outside an approved enclosed dispensing system. Therefore, the condition is true. The rule includes an exception: 'except while the liquids are inside an approved enclosed dispensing system.' Evidence E30 confirms that the liquids are indeed inside an approved enclosed dispensing system, which satisfies the exception prerequisite. Therefore, the exception applies. There are no conflicting observations regarding whether the finishing area has flammable liquids in open containers or whether they are inside an approved enclosed dispensing system. The single observation E30 directly supports the exception and does not create any unresolved contradictions.
scope_reason: The rule applies to the finishing area where flammable liquids are handled. The subject is the finishing area's handling of flammable liquids, and the period in scope is the current assessment period (30 September 2026).
condition_reason: Evidence E30 states that 'The finishing-area liquids are entirely inside an approved enclosed dispensing system; no containers are open outside it.' This directly supports the trigger condition that flammable liquids are not in open containers outside an approved enclosed dispensing system. Therefore, the condition is true.
exception_reason: The rule includes an exception: 'except while the liquids are inside an approved enclosed dispensing system.' Evidence E30 confirms that the liquids are indeed inside an approved enclosed dispensing system, which satisfies the exception prerequisite. Therefore, the exception applies.
conflict_reason: There are no conflicting observations regarding whether the finishing area has flammable liquids in open containers or whether they are inside an approved enclosed dispensing system. The single observation E30 directly supports the exception and does not create any unresolved contradictions.


## hospitality

Error: `None`; judge error: `None`.

### G1 (explicit)

[concern] A hotel kitchen suppression system with service overdue by more than 30 days is a concern.

Expected `no_match`; actual `no_match`. Explanation: 10/10 (graded).

Reference: Exactly 30 days does not exceed 30; preserve the strict greater-than threshold despite the service being overdue.

Candidate:

Assessment: The rule applies to a hotel kitchen suppression system. The subject is the kitchen suppression system at Elm urban hotel. The period in scope is the current assessment period ending 30 September 2026. The technical exhibit (E8) states: 'The kitchen suppression system's scheduled service date was 31 August 2026. It remains unserviced as of 30 September 2026, exactly 30 days overdue.' This indicates the system was due on 31 August 2026 and remained unserviced as of 30 September 2026, which is exactly 30 days overdue. The rule requires service to be overdue by more than 30 days to constitute a concern. Since the delay is exactly 30 days and not more than 30 days, the condition is false. The rule does not contain an explicit exception. There are no stated prerequisites or validity dates for an exception to apply. There are no conflicting observations regarding the kitchen suppression system's service date or its overdue status as of 30 September 2026. The single observation E8 provides a clear statement about the system's scheduled service date and current status.
scope_reason: The rule applies to a hotel kitchen suppression system. The subject is the kitchen suppression system at Elm urban hotel. The period in scope is the current assessment period ending 30 September 2026.
condition_reason: The technical exhibit (E8) states: 'The kitchen suppression system's scheduled service date was 31 August 2026. It remains unserviced as of 30 September 2026, exactly 30 days overdue.' This indicates the system was due on 31 August 2026 and remained unserviced as of 30 September 2026, which is exactly 30 days overdue. The rule requires service to be overdue by more than 30 days to constitute a concern. Since the delay is exactly 30 days and not more than 30 days, the condition is false.
exception_reason: The rule does not contain an explicit exception. There are no stated prerequisites or validity dates for an exception to apply.
conflict_reason: There are no conflicting observations regarding the kitchen suppression system's service date or its overdue status as of 30 September 2026. The single observation E8 provides a clear statement about the system's scheduled service date and current status.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to a hotel kitchen suppression system and specifies the relevant subject and time period, aligning with the reference's trigger and scope. Excerpt: "Assessment: The rule applies to a hotel kitchen suppression system. The subject is the kitchen suppression system at Elm urban hotel. The period in scope is the current assessment period ending 30 September 2026."
- factual_grounding: 2/2. The excerpt accurately cites the technical exhibit E8 and correctly states that the system was exactly 30 days overdue, matching the factual content provided in the reference. Excerpt: "The technical exhibit (E8) states: 'The kitchen suppression system's scheduled service date was 31 August 2026. It remains unserviced as of 30 September 2026, exactly 30 days overdue.' This indicates the system was due on 31 August 2026 and remained unserviced as of 30 September 2026, which is exactly 30 days overdue."
- scope_and_exceptions: 2/2. The excerpt correctly identifies that there is no explicit exception in the rule and confirms the absence of conflicting observations, which aligns with the reference's rationale. Excerpt: "The rule does not contain an explicit exception. There are no stated prerequisites or validity dates for an exception to apply. There are no conflicting observations regarding the kitchen suppression system's service date or its overdue status as of 30 September 2026."
- logical_support: 2/2. This excerpt correctly applies the rule's threshold (more than 30 days) and logically concludes that since the delay is exactly 30 days, it does not meet the concern criteria, which matches the reference's rationale. Excerpt: "The rule requires service to be overdue by more than 30 days to constitute a concern. Since the delay is exactly 30 days and not more than 30 days, the condition is false."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by relying solely on the cited evidence (E8) and does not introduce any assumptions or contradictions. Excerpt: "The single observation E8 provides a clear statement about the system's scheduled service date and current status."
### G2 (explicit)

[concern] An unfenced guest swimming pool is a concern; this rule applies only to properties operating a guest swimming pool.

Expected `not_applicable`; actual `not_applicable`. Explanation: 10/10 (graded).

Reference: No guest pool means the rule is out of scope; do not label this an in-scope negative or treat the fountain as a pool.

Candidate:

Assessment: The rule applies to properties operating a guest swimming pool. The evidence shows the property does not operate a guest swimming pool (E20). The rule's trigger is that a property operates a guest swimming pool. Evidence E20 states: 'The property does not operate a guest swimming pool.' This directly contradicts the condition required for the rule to apply. No supporting evidence of a guest swimming pool exists. The rule has no explicit exception prerequisites mentioned. The only restriction is that it applies only to properties operating a guest swimming pool, which this property does not do. There are no conflicting observations regarding whether the property operates a guest swimming pool. The evidence is clear that it does not operate one.
scope_reason: The rule applies to properties operating a guest swimming pool. The evidence shows the property does not operate a guest swimming pool (E20).
condition_reason: The rule's trigger is that a property operates a guest swimming pool. Evidence E20 states: 'The property does not operate a guest swimming pool.' This directly contradicts the condition required for the rule to apply. No supporting evidence of a guest swimming pool exists.
exception_reason: The rule has no explicit exception prerequisites mentioned. The only restriction is that it applies only to properties operating a guest swimming pool, which this property does not do.
conflict_reason: There are no conflicting observations regarding whether the property operates a guest swimming pool. The evidence is clear that it does not operate one.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies only to properties with guest swimming pools and accurately states that this property does not operate one, aligning with the reference's scope. Excerpt: "Assessment: The rule applies to properties operating a guest swimming pool. The evidence shows the property does not operate a guest swimming pool (E20)."
- factual_grounding: 2/2. The excerpt accurately cites and interprets the evidence (E20) to support that no guest swimming pool exists, which is consistent with the reference's factual grounding. Excerpt: "Evidence E20 states: 'The property does not operate a guest swimming pool.' This directly contradicts the condition required for the rule to apply. No supporting evidence of a guest swimming pool exists."
- scope_and_exceptions: 2/2. The excerpt correctly identifies the scope of the rule and notes the absence of any exceptions, which aligns with the reference's rationale. Excerpt: "The rule has no explicit exception prerequisites mentioned. The only restriction is that it applies only to properties operating a guest swimming pool, which this property does not do."
- logical_support: 2/2. This excerpt correctly applies the rule's trigger and logically concludes that since the condition is not met, the rule does not apply, matching the reference's logic. Excerpt: "The rule's trigger is that a property operates a guest swimming pool. Evidence E20 states: 'The property does not operate a guest swimming pool.' This directly contradicts the condition required for the rule to apply."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by relying on the cited evidence and does not introduce any assumptions or contradictions. Excerpt: "The evidence is clear that it does not operate one."
### G3 (explicit)

Unrestricted cash covering at least 6 months of fixed operating costs is a strength.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: 780000/120000 = 6.5 months, at least 6; restricted deposits were excluded and should not be added.

Candidate:

Assessment: The rule applies to the applicant (Elm urban hotel) as a whole, with no explicit exclusion. The subject is the organization's financial position regarding unrestricted cash and fixed operating costs. The period in scope is the assessment date 30 September 2026. The evidence shows that unrestricted cash is $780,000 and fixed operating costs are $120,000 per month. Calculating the months covered: $780,000 / $120,000 = 6.5 months. Since 6.5 months is greater than or equal to 6 months, the condition is met. The rule tests whether the unrestricted cash covers at least 6 months of fixed operating costs, which it does. There are no explicit exception prerequisites mentioned in the rule text for C3. The rule does not contain any 'unless' or 'except' clauses that would apply to this case. There are no conflicting observations regarding the unrestricted cash amount or fixed operating costs in the evidence provided. All relevant data points support the calculation of 6.5 months coverage, which meets the threshold of at least 6 months.
Finding: Unrestricted cash of $780,000 covers 6.5 months of fixed operating costs at $120,000 per month, meeting the requirement of at least 6 months.
scope_reason: The rule applies to the applicant (Elm urban hotel) as a whole, with no explicit exclusion. The subject is the organization's financial position regarding unrestricted cash and fixed operating costs. The period in scope is the assessment date 30 September 2026.
condition_reason: The evidence shows that unrestricted cash is $780,000 and fixed operating costs are $120,000 per month. Calculating the months covered: $780,000 / $120,000 = 6.5 months. Since 6.5 months is greater than or equal to 6 months, the condition is met. The rule tests whether the unrestricted cash covers at least 6 months of fixed operating costs, which it does.
exception_reason: There are no explicit exception prerequisites mentioned in the rule text for C3. The rule does not contain any 'unless' or 'except' clauses that would apply to this case.
conflict_reason: There are no conflicting observations regarding the unrestricted cash amount or fixed operating costs in the evidence provided. All relevant data points support the calculation of 6.5 months coverage, which meets the threshold of at least 6 months.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to the applicant as a whole and specifies the relevant subject and time period, aligning with the reference's trigger and scope. Excerpt: "Assessment: The rule applies to the applicant (Elm urban hotel) as a whole, with no explicit exclusion. The subject is the organization's financial position regarding unrestricted cash and fixed operating costs. The period in scope is the assessment date 30 September 2026."
- factual_grounding: 2/2. The excerpt accurately cites the relevant financial figures from the evidence (E30), which aligns with the reference's factual grounding. Excerpt: "The evidence shows that unrestricted cash is $780,000 and fixed operating costs are $120,000 per month."
- scope_and_exceptions: 2/2. The excerpt correctly identifies the absence of exceptions and notes that no 'unless' or 'except' clauses apply, which aligns with the reference's rationale. Excerpt: "There are no explicit exception prerequisites mentioned in the rule text for C3. The rule does not contain any 'unless' or 'except' clauses that would apply to this case."
- logical_support: 2/2. The excerpt correctly performs the arithmetic and logically concludes that the condition is met, matching the reference's rationale for the calculation. Excerpt: "Calculating the months covered: $780,000 / $120,000 = 6.5 months. Since 6.5 months is greater than or equal to 6 months, the condition is met. The rule tests whether the unrestricted cash covers at least 6 months of fixed operating costs, which it does."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims by relying on the cited evidence and correctly supports the conclusion with the arithmetic provided. Excerpt: "All relevant data points support the calculation of 6.5 months coverage, which meets the threshold of at least 6 months."

## contractor

Error: `None`; judge error: `None`.

### G1 (explicit)

[strength] Current insurance certificates for every active subcontractor are a strength.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: All four active subcontractors are covered by current certificates; the population and validity period are established.

Candidate:

Assessment: The rule applies to the current period, and the evidence batch covers the proposed policy period beginning 1 November 2026. The subject is 'every active subcontractor' within the scope of the applicant's operations. Evidence E8 states: 'The active subcontractor register contains 4 firms; all 4 have current insurance certificates covering the proposed policy period.' This directly supports that all active subcontractors have current insurance certificates, which satisfies the trigger condition. There are no observations refuting this claim. The rule does not contain an explicit exception. No exception prerequisites are mentioned or satisfied in the evidence. There are no incompatible observations regarding the insurance certificates of active subcontractors. All observations support that all 4 active subcontractors have current insurance certificates covering the proposed policy period.
Finding: All 4 firms listed in the active subcontractor register have current insurance certificates covering the proposed policy period (1 November 2026 onwards), satisfying the condition that current insurance certificates for every active subcontractor are a strength.
scope_reason: The rule applies to the current period, and the evidence batch covers the proposed policy period beginning 1 November 2026. The subject is 'every active subcontractor' within the scope of the applicant's operations.
condition_reason: Evidence E8 states: 'The active subcontractor register contains 4 firms; all 4 have current insurance certificates covering the proposed policy period.' This directly supports that all active subcontractors have current insurance certificates, which satisfies the trigger condition. There are no observations refuting this claim.
exception_reason: The rule does not contain an explicit exception. No exception prerequisites are mentioned or satisfied in the evidence.
conflict_reason: There are no incompatible observations regarding the insurance certificates of active subcontractors. All observations support that all 4 active subcontractors have current insurance certificates covering the proposed policy period.

- rule_application: 2/2. The candidate correctly identifies that the rule applies to the current period and aligns it with the proposed policy period, correctly identifying the subject as 'every active subcontractor' within the applicant's operations. Excerpt: "Assessment: The rule applies to the current period, and the evidence batch covers the proposed policy period beginning 1 November 2026. The subject is 'every active subcontractor' within the scope of the applicant's operations."
- factual_grounding: 2/2. The candidate accurately cites E8 and correctly interprets its content to support that all four active subcontractors have valid insurance certificates for the proposed period. Excerpt: "Evidence E8 states: 'The active subcontractor register contains 4 firms; all 4 have current insurance certificates covering the proposed policy period.' This directly supports that all active subcontractors have current insurance certificates, which satisfies the trigger condition."
- scope_and_exceptions: 2/2. The candidate correctly identifies the temporal and operational scope of the rule and confirms that there are no exceptions or prerequisites mentioned in the rule or evidence. Excerpt: "The rule applies to the current period, and the evidence batch covers the proposed policy period beginning 1 November 2026. The subject is 'every active subcontractor' within the scope of the applicant's operations."
- logical_support: 2/2. The candidate clearly explains how the cited evidence logically leads to the conclusion that the rule's condition is satisfied, with no contradictory information. Excerpt: "Evidence E8 states: 'The active subcontractor register contains 4 firms; all 4 have current insurance certificates covering the proposed policy period.' This directly supports that all active subcontractors have current insurance certificates, which satisfies the trigger condition. There are no observations refuting this claim."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and ensures that all assertions are grounded in the cited evidence, with no contradictions or invented facts. Excerpt: "There are no observations refuting this claim. The rule does not contain an explicit exception. No exception prerequisites are mentioned or satisfied in the evidence. There are no incompatible observations regarding the insurance certificates of active subcontractors. All observations support that all 4 active subcontractors have current insurance certificates covering the proposed policy period."
### G2 (implicit)

Refer contracts that transfer structural design responsibility to the applicant unless an executed agreement delegates that responsibility to an insured licensed engineer.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: Design responsibility is contractually assumed and no executed delegation supports the exception; referral maps to concern.

Candidate:

Assessment: The rule applies to contracts transferring structural design responsibility to the applicant. The subject is the applicant (Fir mechanical installations), and the period in scope is the proposed policy period beginning 1 November 2026. Evidence E20 states: 'The current Riverside contract transfers structural design responsibility to Fir. No executed agreement delegates that responsibility to an engineer.' This directly supports the trigger condition that a contract transfers structural design responsibility to the applicant (Fir) and that no executed agreement delegates that responsibility to an insured licensed engineer. Therefore, the condition is true. The rule states 'unless an executed agreement delegates that responsibility to an insured licensed engineer.' There is no evidence of any executed agreement delegating structural design responsibility to an insured licensed engineer. The exception prerequisites are not met, so the exception does not apply. There are no conflicting observations regarding whether the Riverside contract transfers structural design responsibility to Fir or whether any executed agreement delegates that responsibility to an insured licensed engineer. The evidence is clear and consistent.
Finding: The Riverside contract transfers structural design responsibility to Fir, and no executed agreement delegates that responsibility to an insured licensed engineer. This triggers the referral requirement under criterion C2.
scope_reason: The rule applies to contracts transferring structural design responsibility to the applicant. The subject is the applicant (Fir mechanical installations), and the period in scope is the proposed policy period beginning 1 November 2026.
condition_reason: Evidence E20 states: 'The current Riverside contract transfers structural design responsibility to Fir. No executed agreement delegates that responsibility to an engineer.' This directly supports the trigger condition that a contract transfers structural design responsibility to the applicant (Fir) and that no executed agreement delegates that responsibility to an insured licensed engineer. Therefore, the condition is true.
exception_reason: The rule states 'unless an executed agreement delegates that responsibility to an insured licensed engineer.' There is no evidence of any executed agreement delegating structural design responsibility to an insured licensed engineer. The exception prerequisites are not met, so the exception does not apply.
conflict_reason: There are no conflicting observations regarding whether the Riverside contract transfers structural design responsibility to Fir or whether any executed agreement delegates that responsibility to an insured licensed engineer. The evidence is clear and consistent.

- rule_application: 2/2. The candidate correctly identifies the rule's application to contracts transferring structural design responsibility, specifying the applicant and the relevant time period. Excerpt: "Assessment: The rule applies to contracts transferring structural design responsibility to the applicant. The subject is the applicant (Fir mechanical installations), and the period in scope is the proposed policy period beginning 1 November 2026."
- factual_grounding: 2/2. The candidate accurately cites E20 and correctly interprets it as supporting both parts of the rule's trigger condition. Excerpt: "Evidence E20 states: 'The current Riverside contract transfers structural design responsibility to Fir. No executed agreement delegates that responsibility to an engineer.' This directly supports the trigger condition that a contract transfers structural design responsibility to the applicant (Fir) and that no executed agreement delegates that responsibility to an insured licensed engineer."
- scope_and_exceptions: 2/2. The candidate correctly identifies and evaluates the exception condition in the rule, concluding that it does not apply due to lack of supporting evidence. Excerpt: "The rule states 'unless an executed agreement delegates that responsibility to an insured licensed engineer.' There is no evidence of any executed agreement delegating structural design responsibility to an insured licensed engineer. The exception prerequisites are not met, so the exception does not apply."
- logical_support: 2/2. The candidate provides clear logical reasoning from the evidence to conclude that the rule's condition is met and that the exception does not apply. Excerpt: "Therefore, the condition is true. The rule states 'unless an executed agreement delegates that responsibility to an insured licensed engineer.' There is no evidence of any executed agreement delegating structural design responsibility to an insured licensed engineer. The exception prerequisites are not met, so the exception does not apply."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and ensures consistency in the interpretation of the evidence. Excerpt: "There are no conflicting observations regarding whether the Riverside contract transfers structural design responsibility to Fir or whether any executed agreement delegates that responsibility to an insured licensed engineer. The evidence is clear and consistent."
### G3 (implicit)

Allow positive credit for a documented rescue drill for every crew scheduled for confined-space entry during the policy period.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 10/10 (graded).

Reference: Two crews are in scope but drill records are missing; absence of records does not prove drills did not happen or establish positive credit.

Candidate:

Assessment: The criterion requires documentation of a rescue drill for every crew scheduled for confined-space entry during the policy period. While it is noted that two crews are scheduled for confined-space entry and that rescue-drill records have been requested but are not yet supplied, there is no evidence that the rescue drills were actually conducted or documented. The absence of the required documentation means the condition cannot be verified as met.

- rule_application: 2/2. The candidate correctly identifies and applies the rule's requirement to document rescue drills for each crew scheduled for confined-space entry. Excerpt: "Assessment: The criterion requires documentation of a rescue drill for every crew scheduled for confined-space entry during the policy period."
- factual_grounding: 2/2. The candidate accurately cites E30 and correctly interprets its content to show that while crews are scheduled, the required documentation is missing. Excerpt: "While it is noted that two crews are scheduled for confined-space entry and that rescue-drill records have been requested but are not yet supplied, there is no evidence that the rescue drills were actually conducted or documented."
- scope_and_exceptions: 2/2. The candidate correctly identifies the scope of the rule as applying to all crews scheduled for confined-space entry during the policy period. Excerpt: "The criterion requires documentation of a rescue drill for every crew scheduled for confined-space entry during the policy period."
- logical_support: 2/2. The candidate logically concludes that without the required documentation, the condition cannot be satisfied, which aligns with the reference's rationale. Excerpt: "The absence of the required documentation means the condition cannot be verified as met."
- no_unsupported_claims: 2/2. The candidate avoids unsupported claims and clearly states that the lack of documentation prevents verification of the condition. Excerpt: "Assessment: The criterion requires documentation of a rescue drill for every crew scheduled for confined-space entry during the policy period. While it is noted that two crews are scheduled for confined-space entry and that rescue-drill records have been requested but are not yet supplied, there is no evidence that the rescue drills were actually conducted or documented."
