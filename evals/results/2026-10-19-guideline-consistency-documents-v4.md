# First-use long-document holdout

State: **interrupted**

Synthetic, author-labeled cases frozen before inference. Production code is unchanged. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 3/3 | 3/3 | 2/3 | 0/3 | False | False | False |
| cyber | 618 / 1424 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |

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

Error: `{'type': 'ValueError', 'message': 'Implicit criterion requires a source-backed classification_quote'}`; judge error: `None`.

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
