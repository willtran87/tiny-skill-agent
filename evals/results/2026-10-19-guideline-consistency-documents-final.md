# First-use long-document holdout

State: **completed**

Synthetic, author-labeled cases frozen before inference. Production code is unchanged. Gold is scoring-only; the separate explanation judge sees gold after assessment and uses the same local model. This is not expert validation or a repeatability study.

| Case | Words (guide / application) | Criteria | Statuses | Findings | Explanation passes | Ready | Objective unsafe ready | Strict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| property | 642 / 1429 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |
| cyber | 618 / 1424 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |
| fleet | 632 / 1452 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |
| manufacturing | 636 / 1419 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |
| hospitality | 635 / 1427 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |
| contractor | 640 / 1425 | 0/3 | 0/3 | 0/3 | 0/3 | False | False | False |

## property

Error: `{'type': 'ValueError', 'message': 'Line review cannot omit a known rule'}`; judge error: `None`.

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

Error: `{'type': 'ValueError', 'message': 'Criterion extraction must review every source line exactly once'}`; judge error: `None`.

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

Error: `{'type': 'ValueError', 'message': 'Line review cannot omit a known rule'}`; judge error: `None`.

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


## manufacturing

Error: `{'type': 'ValueError', 'message': 'Criterion extraction must review every source line exactly once'}`; judge error: `None`.

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

Error: `{'type': 'ValueError', 'message': 'Line review cannot omit a known rule'}`; judge error: `None`.

### G1 (explicit)

[concern] A hotel kitchen suppression system with service overdue by more than 30 days is a concern.

Expected `no_match`; actual `missing`. Explanation: 0/10 (missing).

Reference: Exactly 30 days does not exceed 30; preserve the strict greater-than threshold despite the service being overdue.

Candidate:

No explanation produced.

### G2 (explicit)

[concern] An unfenced guest swimming pool is a concern; this rule applies only to properties operating a guest swimming pool.

Expected `not_applicable`; actual `missing`. Explanation: 0/10 (missing).

Reference: No guest pool means the rule is out of scope; do not label this an in-scope negative or treat the fountain as a pool.

Candidate:

No explanation produced.

### G3 (explicit)

Unrestricted cash covering at least 6 months of fixed operating costs is a strength.

Expected `matched`; actual `missing`. Explanation: 0/10 (missing).

Reference: 780000/120000 = 6.5 months, at least 6; restricted deposits were excluded and should not be added.

Candidate:

No explanation produced.


## contractor

Error: `{'type': 'ValueError', 'message': 'Line review cannot omit a known rule'}`; judge error: `None`.

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
