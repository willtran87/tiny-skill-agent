# First-use long-document holdout

State: **completed**

Synthetic, author-labeled cases frozen before inference. Production code is unchanged. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 3/3 | 3/3 | 3/3 | 3/3 | True | False | True |
| cyber | 618 / 1424 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |
| fleet | 632 / 1452 | 2/3 | 2/3 | 2/3 | 0/3 | False | False | False |
| manufacturing | 636 / 1419 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |
| hospitality | 635 / 1427 | 3/3 | 2/3 | 3/3 | 0/3 | True | True | False |
| contractor | 640 / 1425 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |

## property

Error: `None`; judge error: `None`.

### G1 (explicit)

[concern] A cold-storage building whose roof is more than 25 years old is a concern unless a complete roof replacement has been documented within the last 2 years.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: Identify North and South separately: 28 and 31 exceed 25, with no replacement exception. East is excluded by its documented replacement/current age.

Candidate:

Assessment: The rule applies to individual cold-storage buildings (North, South, and East) with roof ages exceeding 25 years. The assessment date is 30 September 2026, and the relevant period for roof age and replacement documentation is current as of that date. Facts proving the trigger: North building roof age is 28 years (E8); South building roof age is 31 years (E9). Facts refuting the trigger: East building had a complete roof replacement on 1 March 2026 (E10), making its roof age 0 years. Given that North and South buildings exceed 25 years old and have no documented complete replacement within the last 2 years, the condition is true for these two buildings. The East building does not meet the trigger criteria due to recent replacement documentation. Therefore, the rule's trigger holds for North and South buildings but not for East. The rule does not specify any explicit exceptions that would apply to the described circumstances. No exception prerequisites or validity dates are mentioned in the rule text. There are no actual incompatible observations regarding roof ages or replacement documentation for the same buildings at the same time. The North and South buildings have roof ages exceeding 25 years without recent complete replacements, while the East building has a documented complete replacement within the last 2 years. These are distinct conditions for different buildings.
Finding: The North building's roof is 28 years old, exceeding the 25-year threshold. No complete roof replacement has been documented within the last 2 years, meeting the rule's trigger condition.
Finding: The South building's roof is 31 years old, exceeding the 25-year threshold. No complete roof replacement has been documented within the last 2 years, meeting the rule's trigger condition.
scope_reason: The rule applies to individual cold-storage buildings (North, South, and East) with roof ages exceeding 25 years. The assessment date is 30 September 2026, and the relevant period for roof age and replacement documentation is current as of that date.
condition_reason: Facts proving the trigger: North building roof age is 28 years (E8); South building roof age is 31 years (E9). Facts refuting the trigger: East building had a complete roof replacement on 1 March 2026 (E10), making its roof age 0 years. Given that North and South buildings exceed 25 years old and have no documented complete replacement within the last 2 years, the condition is true for these two buildings. The East building does not meet the trigger criteria due to recent replacement documentation. Therefore, the rule's trigger holds for North and South buildings but not for East.
exception_reason: The rule does not specify any explicit exceptions that would apply to the described circumstances. No exception prerequisites or validity dates are mentioned in the rule text.
conflict_reason: There are no actual incompatible observations regarding roof ages or replacement documentation for the same buildings at the same time. The North and South buildings have roof ages exceeding 25 years without recent complete replacements, while the East building has a documented complete replacement within the last 2 years. These are distinct conditions for different buildings.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to individual buildings and accurately states the threshold of 25 years, matching the reference's trigger condition. Excerpt: "Assessment: The rule applies to individual cold-storage buildings (North, South, and East) with roof ages exceeding 25 years."
- factual_grounding: 2/2. The excerpt correctly cites the relevant evidence and accurately reflects the facts that support the application of the rule to North and South buildings, and the exclusion of East. Excerpt: "Facts proving the trigger: North building roof age is 28 years (E8); South building roof age is 31 years (E9). Facts refuting the trigger: East building had a complete roof replacement on 1 March 2026 (E10), making its roof age 0 years."
- scope_and_exceptions: 2/2. The excerpt clearly defines the scope of the rule application to individual buildings and correctly identifies the assessment date and period, including the exclusion of East due to documented replacement. Excerpt: "The rule applies to individual cold-storage buildings (North, South, and East) with roof ages exceeding 25 years. The assessment date is 30 September 2026, and the relevant period for roof age and replacement documentation is current as of that date."
- logical_support: 2/2. The excerpt logically explains why the rule's trigger applies to North and South but not to East, based on the age and replacement history of each building. Excerpt: "Given that North and South buildings exceed 25 years old and have no documented complete replacement within the last 2 years, the condition is true for these two buildings. The East building does not meet the trigger criteria due to recent replacement documentation."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims and correctly notes that there are no exceptions specified in the rule, and that the conditions for each building are distinct. Excerpt: "The rule does not specify any explicit exceptions that would apply to the described circumstances. No exception prerequisites or validity dates are mentioned in the rule text. There are no actual incompatible observations regarding roof ages or replacement documentation for the same buildings at the same time."
### G2 (explicit)

Current sprinkler inspection certificates with no outstanding deficiencies for every cold-storage building are a strength.

Expected `matched`; actual `matched`. Explanation: 10/10 (graded).

Reference: All three buildings have current certificates and no deficiencies; the all-buildings requirement is established.

Candidate:

Assessment: The rule applies to all cold-storage buildings, which are North, South, and East. The assessment date is 30 September 2026, and the proposed insurance period begins on 1 November 2026. The evidence batch covers the submission as of the assessment date. The evidence shows that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly proves that all three cold-storage buildings have current sprinkler inspection certificates with no outstanding deficiencies. There are no facts that refute this statement. Given the information provided, it is true that current sprinkler inspection certificates with no outstanding deficiencies exist for every cold-storage building. There is no explicit exception mentioned in the rule text for C3. The rule does not specify any conditions under which this strength would not apply. There are no conflicting observations regarding the sprinkler inspection certificates for any of the cold-storage buildings. All three buildings (North, South, and East) have certificates with no outstanding deficiencies as stated in E22.
Finding: All three cold-storage buildings (North, South, and East) have current sprinkler inspection certificates with no outstanding deficiencies, which satisfies the strength criterion C3.
scope_reason: The rule applies to all cold-storage buildings, which are North, South, and East. The assessment date is 30 September 2026, and the proposed insurance period begins on 1 November 2026. The evidence batch covers the submission as of the assessment date.
condition_reason: The evidence shows that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly proves that all three cold-storage buildings have current sprinkler inspection certificates with no outstanding deficiencies. There are no facts that refute this statement. Given the information provided, it is true that current sprinkler inspection certificates with no outstanding deficiencies exist for every cold-storage building.
exception_reason: There is no explicit exception mentioned in the rule text for C3. The rule does not specify any conditions under which this strength would not apply.
conflict_reason: There are no conflicting observations regarding the sprinkler inspection certificates for any of the cold-storage buildings. All three buildings (North, South, and East) have certificates with no outstanding deficiencies as stated in E22.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to all buildings and accurately reflects the scope of the strength criterion. Excerpt: "Assessment: The rule applies to all cold-storage buildings, which are North, South, and East."
- factual_grounding: 2/2. The excerpt correctly cites the supporting evidence and accurately reflects that all buildings meet the strength criteria. Excerpt: "The evidence shows that 'Current sprinkler certificates cover North, South, and East; each records no outstanding deficiencies.' This directly proves that all three cold-storage buildings have current sprinkler inspection certificates with no outstanding deficiencies."
- scope_and_exceptions: 2/2. The excerpt correctly identifies the scope of application as all buildings and includes relevant dates for context. Excerpt: "The rule applies to all cold-storage buildings, which are North, South, and East. The assessment date is 30 September 2026, and the proposed insurance period begins on 1 November 2026."
- logical_support: 2/2. The excerpt logically supports the conclusion by directly linking the evidence to the stated strength. Excerpt: "Given the information provided, it is true that current sprinkler inspection certificates with no outstanding deficiencies exist for every cold-storage building."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims and correctly notes that there are no exceptions specified in the rule. Excerpt: "There is no explicit exception mentioned in the rule text for C3. The rule does not specify any conditions under which this strength would not apply."
### G3 (explicit)

[concern] A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.

Expected `no_match`; actual `no_match`. Explanation: 10/10 (graded).

Reference: The panels meet the trigger, but current independent approval for all three makes the stated exception apply; do not claim the panels are noncombustible.

Candidate:

Assessment: The rule applies to individual cold-storage buildings. The subject is each building (North, South, and East). The period in scope is the present assessment date of 30 September 2026. Facts that PROVE the quoted trigger: E32 states that all three buildings have combustible insulated wall panels. Facts that REFUTE it: E32 also states that current independent fire-engineering certification approves those panels in North, South, and East. Given that the certification is current and approves the panels, the condition is false - the rule's trigger does not hold because the exception applies. The certification covers all buildings, so there is no concern for any of them. The exception prerequisite is 'a current independent fire-engineering certification approves those panels'. E32 explicitly states that current independent fire-engineering certification approves those panels in North, South, and East. The validity date is not specified but the term 'current' implies it is valid at the assessment date of 30 September 2026. Therefore, the exception applies to all three buildings. There are no actual incompatible observations with the same subject and time. The evidence shows that certification covers all buildings and is current, which satisfies the exception condition. No unresolved conflicts exist.
scope_reason: The rule applies to individual cold-storage buildings. The subject is each building (North, South, and East). The period in scope is the present assessment date of 30 September 2026.
condition_reason: Facts that PROVE the quoted trigger: E32 states that all three buildings have combustible insulated wall panels. Facts that REFUTE it: E32 also states that current independent fire-engineering certification approves those panels in North, South, and East. Given that the certification is current and approves the panels, the condition is false - the rule's trigger does not hold because the exception applies. The certification covers all buildings, so there is no concern for any of them.
exception_reason: The exception prerequisite is 'a current independent fire-engineering certification approves those panels'. E32 explicitly states that current independent fire-engineering certification approves those panels in North, South, and East. The validity date is not specified but the term 'current' implies it is valid at the assessment date of 30 September 2026. Therefore, the exception applies to all three buildings.
conflict_reason: There are no actual incompatible observations with the same subject and time. The evidence shows that certification covers all buildings and is current, which satisfies the exception condition. No unresolved conflicts exist.

- rule_application: 2/2. The excerpt correctly identifies that the rule applies to individual buildings and accurately reflects the trigger condition. Excerpt: "Assessment: The rule applies to individual cold-storage buildings. The subject is each building (North, South, and East)."
- factual_grounding: 2/2. The excerpt correctly cites the evidence and accurately reflects that while the trigger condition is met, the exception applies due to the certification. Excerpt: "Facts that PROVE the quoted trigger: E32 states that all three buildings have combustible insulated wall panels. Facts that REFUTE it: E32 also states that current independent fire-engineering certification approves those panels in North, South, and East."
- scope_and_exceptions: 2/2. The excerpt correctly identifies the scope of application and the relevant time frame for the exception. Excerpt: "The rule applies to individual cold-storage buildings. The subject is each building (North, South, and East). The period in scope is the present assessment date of 30 September 2026."
- logical_support: 2/2. The excerpt logically explains why the rule's trigger does not apply due to the exception, correctly linking the certification to the exclusion of concern. Excerpt: "Given that the certification is current and approves the panels, the condition is false - the rule's trigger does not hold because the exception applies. The certification covers all buildings, so there is no concern for any of them."
- no_unsupported_claims: 2/2. The excerpt avoids unsupported claims and correctly identifies the exception prerequisite and its applicability based on the evidence. Excerpt: "The exception prerequisite is 'a current independent fire-engineering certification approves those panels'. E32 explicitly states that current independent fire-engineering certification approves those panels in North, South, and East. The validity date is not specified but the term 'current' implies it is valid at the assessment date of 30 September 2026."

## cyber

Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`; judge error: `None`.

### G1 (explicit)

[strength] MFA on every active privileged account is a strength.

Expected `no_match`; actual `missing`. Explanation: 0/10 (missing).

Reference: 23/24 is not every account. The active emergency account is in scope and there is no exception; this is affirmative failure, not missing evidence.

Candidate:

No explanation produced.

### G2 (explicit)

A successful isolated recovery test within the last 90 days is a strength.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: 15 August is 46 days before 30 September, within 90; a successful isolated test is recorded.

Candidate:

No explanation produced.

### G3 (implicit)

Refer any account that stores unencrypted portable copies of payroll data for adverse treatment.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: Unencrypted portable payroll copies meet the referral rule; the guideline's vocabulary maps adverse treatment to concern.

Candidate:

No explanation produced.


## fleet

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[concern] A heavy goods vehicle with an unresolved brake defect is a concern.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 0/10 (judge_error).

Reference: The equally authoritative H7 records conflict for the same date with no correction; abstain rather than select one report or emit a settled concern.

Candidate:

Assessment: The rule concerns heavy goods vehicles and applies to the period around the assessment date (30 September 2026). Vehicle H7 is specifically mentioned as having an unresolved brake defect, which falls within the scope of the rule. Facts that PROVE: Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect (E8). Facts that REFUTE: Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other (E9). Given that there are two conflicting reports for the same vehicle on the same date, and neither corrects the other, the status of whether the brake defect is unresolved remains unknown. However, since the rule states 'an unresolved brake defect' as a concern, and we have evidence of a reported defect without resolution, the condition is true. There are no explicit exception prerequisites or validity dates mentioned in the rule text for C1 that would apply here. The rule does not specify any conditions under which this concern would not apply. There are two conflicting inspection reports for vehicle H7 on the same date (29 September 2026), but neither report corrects the other. This creates an unresolved conflict regarding whether there was a brake defect, but since one report explicitly states there is an unresolved brake defect, and the rule applies to such situations, this does not negate the finding.
scope_reason: The rule concerns heavy goods vehicles and applies to the period around the assessment date (30 September 2026). Vehicle H7 is specifically mentioned as having an unresolved brake defect, which falls within the scope of the rule.
condition_reason: Facts that PROVE: Inspector A's signed 29 September 2026 inspection of vehicle H7 records an unresolved brake defect (E8). Facts that REFUTE: Inspector B's equally authoritative signed 29 September 2026 inspection of vehicle H7 records no brake defect; neither report corrects the other (E9). Given that there are two conflicting reports for the same vehicle on the same date, and neither corrects the other, the status of whether the brake defect is unresolved remains unknown. However, since the rule states 'an unresolved brake defect' as a concern, and we have evidence of a reported defect without resolution, the condition is true.
exception_reason: There are no explicit exception prerequisites or validity dates mentioned in the rule text for C1 that would apply here. The rule does not specify any conditions under which this concern would not apply.
conflict_reason: There are two conflicting inspection reports for vehicle H7 on the same date (29 September 2026), but neither report corrects the other. This creates an unresolved conflict regarding whether there was a brake defect, but since one report explicitly states there is an unresolved brake defect, and the rule applies to such situations, this does not negate the finding.

### G2 (explicit)

[strength] Completed annual driving-record reviews for all active drivers are a strength.

Expected `insufficient_evidence`; actual `insufficient_evidence`. Explanation: 0/10 (judge_error).

Reference: The register is missing. This does not prove that reviews were not performed; evidence is insufficient to establish all-driver coverage.

Candidate:

Assessment: The criterion requires that annual driving-record reviews be completed for all active drivers to constitute a strength. Evidence E22 explicitly states that the broker has requested but not received the annual driving-record review register. This absence of the required documentation means that it cannot be confirmed whether reviews were completed for all 18 active drivers. Since the necessary evidence is missing, a negative decision cannot be legitimately made based on the available information.
scope_reason: The rule concerns annual driving-record reviews for active drivers. The assessment date is 30 September 2026, and the proposed insurance period begins on 1 November 2026. The subject is active drivers within the fleet.
condition_reason: The evidence shows that there are 18 active drivers (E22). However, the broker has requested but not received the annual driving-record review register (E22). This absence of the required documentation means that it cannot be confirmed whether all active drivers have completed their annual driving-record reviews. The lack of the register is a direct contradiction to the requirement for proof of completion. Therefore, the facts refute the trigger condition. Condition = false.
exception_reason: There are no explicit exceptions mentioned in the rule text that would apply to this situation.
conflict_reason: There is no actual incompatible observation with the same subject and time. The only issue is the missing document which does not constitute a conflict but rather a lack of evidence to support the condition.

### G3 (implicit)

Give favorable treatment when verified telematics show a harsh-braking rate below 2 events per 1000 miles across the active fleet.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: 54 / 36000 * 1000 = 1.5, strictly below 2. Favorable treatment maps to strength.

Candidate:

No explanation produced.


## manufacturing

Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`; judge error: `None`.

### G1 (implicit)

Decline operations using a production press without an interlocked guard.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: P4 is in use and unguarded; a proposed retrofit is not completion. Decline maps to concern.

Candidate:

No explanation produced.

### G2 (implicit)

Allow positive credit when completed hot-work permits and fire-watch records cover every hot-work job in the last 12 months.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: All 9 jobs have both required records over the required period; positive credit maps to strength.

Candidate:

No explanation produced.

### G3 (implicit)

Refer a finishing area with flammable liquids in open containers, except while the liquids are inside an approved enclosed dispensing system.

Expected `no_match`; actual `missing`. Explanation: 0/10 (missing).

Reference: The recorded enclosed system meets the exception and there is no open-container exposure outside it; no concern should be emitted.

Candidate:

No explanation produced.


## hospitality

Error: `None`; judge error: `{'type': 'ValueError', 'message': 'Judge excerpt is not in candidate explanation'}`.

### G1 (explicit)

[concern] A hotel kitchen suppression system with service overdue by more than 30 days is a concern.

Expected `no_match`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: Exactly 30 days does not exceed 30; preserve the strict greater-than threshold despite the service being overdue.

Candidate:

Assessment: The rule applies to a hotel kitchen suppression system. The subject is the kitchen suppression system at Elm urban hotel. The period in scope is the current assessment period ending 30 September 2026. The quoted trigger states that a concern arises if a hotel kitchen suppression system has service overdue by more than 30 days. Evidence E8 directly states: 'The kitchen suppression system's scheduled service date was 31 August 2026. It remains unserviced as of 30 September 2026, exactly 30 days overdue.' This proves the trigger condition is met because the system was due on 31 August and remained unserviced until 30 September, which is exactly 30 days overdue. There are no facts that refute this. Given that the system was unserviced for exactly 30 days, it is not more than 30 days overdue, but the rule uses 'more than 30 days' which excludes equality. Therefore, the condition is false because the service is overdue by exactly 30 days, not more than 30 days. The rule does not contain any explicit exception prerequisites or validity dates mentioned in the text. There is no exception that would apply to this situation. There are no actual incompatible observations with the same subject and time period. The evidence E8 clearly establishes the overdue status of the suppression system, but it does not establish that it is overdue by more than 30 days as required by the rule's trigger.
scope_reason: The rule applies to a hotel kitchen suppression system. The subject is the kitchen suppression system at Elm urban hotel. The period in scope is the current assessment period ending 30 September 2026.
condition_reason: The quoted trigger states that a concern arises if a hotel kitchen suppression system has service overdue by more than 30 days. Evidence E8 directly states: 'The kitchen suppression system's scheduled service date was 31 August 2026. It remains unserviced as of 30 September 2026, exactly 30 days overdue.' This proves the trigger condition is met because the system was due on 31 August and remained unserviced until 30 September, which is exactly 30 days overdue. There are no facts that refute this. Given that the system was unserviced for exactly 30 days, it is not more than 30 days overdue, but the rule uses 'more than 30 days' which excludes equality. Therefore, the condition is false because the service is overdue by exactly 30 days, not more than 30 days.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates mentioned in the text. There is no exception that would apply to this situation.
conflict_reason: There are no actual incompatible observations with the same subject and time period. The evidence E8 clearly establishes the overdue status of the suppression system, but it does not establish that it is overdue by more than 30 days as required by the rule's trigger.

### G2 (explicit)

[concern] An unfenced guest swimming pool is a concern; this rule applies only to properties operating a guest swimming pool.

Expected `not_applicable`; actual `no_match`. Explanation: 0/10 (judge_error).

Reference: No guest pool means the rule is out of scope; do not label this an in-scope negative or treat the fountain as a pool.

Candidate:

Assessment: The subject is 'Elm urban hotel' and the period is '30 September 2026' as per the assessment date. The rule applies to properties operating a guest swimming pool. Facts that PROVE the quoted trigger: E20 states 'The property does not operate a guest swimming pool.' This directly contradicts the trigger condition of having an unfenced guest swimming pool. Facts that REFUTE it: E20 explicitly states that there is no guest swimming pool operated by the property. Could it still be true given unknown information? No, because the explicit statement in E20 negates the presence of a guest swimming pool, which is a prerequisite for the trigger to apply. Therefore, condition = false. The rule does not contain any explicit exception prerequisites or validity dates mentioned. The rule applies to properties operating a guest swimming pool, but there's no stated exception that would prevent this rule from applying if a guest swimming pool were present. Since the property does not operate a guest swimming pool, the rule does not apply at all, making the exception status 'does_not_apply'. There are no actual incompatible observations with ID E20. The statement in E20 clearly indicates that there is no guest swimming pool, which directly contradicts the trigger condition. There is no unresolved conflict between evidence and the criterion.
scope_reason: The subject is 'Elm urban hotel' and the period is '30 September 2026' as per the assessment date. The rule applies to properties operating a guest swimming pool.
condition_reason: Facts that PROVE the quoted trigger: E20 states 'The property does not operate a guest swimming pool.' This directly contradicts the trigger condition of having an unfenced guest swimming pool. Facts that REFUTE it: E20 explicitly states that there is no guest swimming pool operated by the property. Could it still be true given unknown information? No, because the explicit statement in E20 negates the presence of a guest swimming pool, which is a prerequisite for the trigger to apply. Therefore, condition = false.
exception_reason: The rule does not contain any explicit exception prerequisites or validity dates mentioned. The rule applies to properties operating a guest swimming pool, but there's no stated exception that would prevent this rule from applying if a guest swimming pool were present. Since the property does not operate a guest swimming pool, the rule does not apply at all, making the exception status 'does_not_apply'.
conflict_reason: There are no actual incompatible observations with ID E20. The statement in E20 clearly indicates that there is no guest swimming pool, which directly contradicts the trigger condition. There is no unresolved conflict between evidence and the criterion.

### G3 (explicit)

Unrestricted cash covering at least 6 months of fixed operating costs is a strength.

Expected `matched`; actual `matched`. Explanation: 0/10 (judge_error).

Reference: 780000/120000 = 6.5 months, at least 6; restricted deposits were excluded and should not be added.

Candidate:

Assessment: The rule applies to the applicant (Elm urban hotel) and concerns the period up to the assessment date of 30 September 2026. The subject is the financial position of the hotel, specifically its unrestricted cash reserves in relation to fixed operating costs. The facts that prove this quoted trigger are: E30 states 'Unrestricted cash is 780000 dollars; fixed operating costs are 120000 dollars per month.' The calculation shows that 780000 / 120000 = 6.5 months of coverage, which meets the 'at least 6 months' requirement. There are no facts that refute this trigger. Given the known values, it is certain that the condition is true. There is no explicit exception stated for this rule in the provided text. The rule does not have any prerequisites or validity dates mentioned that would prevent its application. There are no actual incompatible observations with the quoted trigger. All evidence supports the condition being met. No unresolved conflicts exist between different pieces of evidence concerning the same subject and time period.
Finding: The unrestricted cash of $780,000 covers 6.5 months of fixed operating costs ($120,000/month), meeting the requirement of at least 6 months of coverage.
scope_reason: The rule applies to the applicant (Elm urban hotel) and concerns the period up to the assessment date of 30 September 2026. The subject is the financial position of the hotel, specifically its unrestricted cash reserves in relation to fixed operating costs.
condition_reason: The facts that prove this quoted trigger are: E30 states 'Unrestricted cash is 780000 dollars; fixed operating costs are 120000 dollars per month.' The calculation shows that 780000 / 120000 = 6.5 months of coverage, which meets the 'at least 6 months' requirement. There are no facts that refute this trigger. Given the known values, it is certain that the condition is true.
exception_reason: There is no explicit exception stated for this rule in the provided text. The rule does not have any prerequisites or validity dates mentioned that would prevent its application.
conflict_reason: There are no actual incompatible observations with the quoted trigger. All evidence supports the condition being met. No unresolved conflicts exist between different pieces of evidence concerning the same subject and time period.


## contractor

Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`; judge error: `None`.

### G1 (explicit)

[strength] Current insurance certificates for every active subcontractor are a strength.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: All four active subcontractors are covered by current certificates; the population and validity period are established.

Candidate:

No explanation produced.

### G2 (implicit)

Refer contracts that transfer structural design responsibility to the applicant unless an executed agreement delegates that responsibility to an insured licensed engineer.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: Design responsibility is contractually assumed and no executed delegation supports the exception; referral maps to concern.

Candidate:

No explanation produced.

### G3 (implicit)

Allow positive credit for a documented rescue drill for every crew scheduled for confined-space entry during the policy period.

Expected `insufficient_evidence`; actual `missing`. Explanation: 0/10 (missing).

Reference: Two crews are in scope but drill records are missing; absence of records does not prove drills did not happen or establish positive credit.

Candidate:

No explanation produced.
