# First-use long-document holdout

State: **interrupted**

Synthetic, author-labeled cases frozen before inference. Production code is unchanged. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |
| cyber | 618 / 1424 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |

## property

Error: `{'type': 'ValueError', 'message': 'Rule line reviews require quotations; context/mapping reviews cannot create rules'}`; judge error: `None`.

### G1 (explicit)

[concern] A cold-storage building whose roof is more than 25 years old is a concern unless a complete roof replacement has been documented within the last 2 years.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: Identify North and South separately: 28 and 31 exceed 25, with no replacement exception. East is excluded by its documented replacement/current age.

Candidate:

No explanation produced.

### G2 (explicit)

Current sprinkler inspection certificates with no outstanding deficiencies for every cold-storage building are a strength.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: All three buildings have current certificates and no deficiencies; the all-buildings requirement is established.

Candidate:

No explanation produced.

### G3 (explicit)

[concern] A cold-storage building with combustible insulated wall panels is a concern unless a current independent fire-engineering certification approves those panels.

Expected `no_match`; actual `missing`. Explanation: 0/10 (missing).

Reference: The panels meet the trigger, but current independent approval for all three makes the stated exception apply; do not claim the panels are noncombustible.

Candidate:

No explanation produced.


## cyber

Error: `{'type': 'ValueError', 'message': 'Rule line reviews require quotations; context/mapping reviews cannot create rules'}`; judge error: `None`.

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
