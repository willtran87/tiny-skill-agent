# End-to-end document and case-isolation evaluation

State: **completed**. Model: `qwen3-coder:30b`.

Live ReAct agent, raw text/Markdown/JSON documents, registered tool provenance, production extraction and completion assessment. Two profiles use separate checkpointed conversations with the same turn order. Gold is excluded from model inputs. Synthetic, short, non-expert-labeled cases; no OCR, PDF layout, or semantic explanation judging.

| Profile | Turns | Strict passes | Collected | Criteria extracted | Gold spans extracted | Isolated inputs | Correct statuses | Correct findings | Ready | Unsafe ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retained_history | 7 | 1 | 7 | 6 | 11/11 | 3 | 3 | 2 | 1 | 0 |
| case_scoped | 7 | 4 | 7 | 6 | 11/11 | 7 | 6 | 6 | 2 | 0 |

`retained_history` is the unmodified default extractor. `case_scoped` is an evaluation integration example selecting tool results by application-owned document IDs. It does not change production extraction or assessment, and the agent still sees prior conversation history.

| Profile | Turn | Expected → actual | Findings actual/expected | Isolated | Ready | Strict |
| --- | --- | --- | --- | --- | --- | --- |
| retained_history | property_a | matched → matched | 2/2 | True | False | FAIL |
| retained_history | property_b_missing | insufficient_evidence → matched | 2/0 | False | False | FAIL |
| retained_history | property_b_followup | no_match → matched | 2/0 | False | False | FAIL |
| retained_history | cyber_c | matched → matched | 1/1 | True | True | PASS |
| retained_history | cyber_d_missing | insufficient_evidence → matched | 1/0 | False | False | FAIL |
| retained_history | cyber_d_followup | matched → matched | 2/1 | False | False | FAIL |
| retained_history | unlabelled_criterion | matched → missing | 0/1 | True | False | FAIL |
| case_scoped | property_a | matched → matched | 2/2 | True | False | FAIL |
| case_scoped | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| case_scoped | property_b_followup | no_match → no_match | 0/0 | True | True | PASS |
| case_scoped | cyber_c | matched → matched | 1/1 | True | True | PASS |
| case_scoped | cyber_d_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| case_scoped | cyber_d_followup | matched → matched | 1/1 | True | False | FAIL |
| case_scoped | unlabelled_criterion | matched → missing | 0/1 | True | False | FAIL |

## Diagnostics

### retained_history / property_a

The rule applies separately to each insured building. The evidence contains information about two buildings (Warehouse 1 and Warehouse 2) within application A. Facts proving: Warehouse 1 roof age is 24 years (E1); Warehouse 2 roof age is 29 years (E3). Facts refuting: None. Given unknown information, it's possible that other buildings may have roof ages <= 20 years. Condition is true because both buildings exceed the 20-year threshold. No explicit exceptions mentioned in the rule text. The rule does not specify any conditions under which this concern would not apply. There are no conflicting observations regarding the roof ages of the buildings. All evidence consistently reports roof ages for Warehouse 1 (24 years) and Warehouse 2 (29 years), both exceeding 20 years.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 5; assessment call attempts: 3; seconds: 15.7. Error: `None`.

### retained_history / property_b_missing

The rule applies to each insured building. The subject is the roof age of individual buildings. The period in scope is the current application as per the guideline. Facts proving: E1 and E2 show that Warehouse 1 has a roof age of 24 years, and E3 shows that Warehouse 2 has a roof age of 29 years. Both exceed 20 years. Facts refuting: None directly refute the trigger; all buildings mentioned have roof ages exceeding 20 years. Given unknown information: Since no other buildings are mentioned in the evidence for application A, we cannot determine if there are additional buildings with roof ages ≤ 20 years. However, the existing evidence supports that at least two buildings (Warehouse 1 and Warehouse 2) meet the condition. Therefore, condition = true. There are no explicit exception prerequisites mentioned in the rule text for C1. The guideline does not list any exceptions to this concern. Exception = does_not_apply. There are no actual incompatible observations in the evidence provided. All evidence points to roof ages exceeding 20 years for the buildings mentioned, which aligns with the trigger condition. Conflict = none.

Foreign input sources: `['doc:property-a.md']`. Foreign cited sources: `['doc:property-a.md']`.

LLM responses (agent + assessment): 7; assessment call attempts: 5; seconds: 21.5. Error: `None`.

### retained_history / property_b_followup

The rule applies to each insured building. The subject is the roof age of individual buildings. The period in scope is the current application as stated in the guideline. Facts proving: Warehouse 1 in application A has a roof age of 24 years (E1, E2). Warehouse 2 in application A has a roof age of 29 years (E3). Facts refuting: No building in application B has a roof age over 20 years as the roof age was updated to 5 years (E13). Could it still be true given unknown information? Yes, if there are other buildings not yet accounted for. Condition is true because at least one building (Warehouse 1 in A) meets the condition of having a roof older than 20 years. There are no explicit exception prerequisites mentioned in the rule text. The guideline does not list any exceptions to this concern. Exception does not apply. There are no actual incompatible observations with the same subject and time. The roof age of Warehouse 1 in application A is 24 years, which satisfies the condition. The roof age of Warehouse 1 in application B was updated to 5 years (E13), but this is a different building and application. Conflict = none.

Foreign input sources: `['doc:property-a.md']`. Foreign cited sources: `['doc:property-a.md']`.

LLM responses (agent + assessment): 9; assessment call attempts: 7; seconds: 27.4. Error: `None`.

### retained_history / cyber_c

The subject is 'Northbank Services, application C' and the period is not specified, but the evidence covers the current state of the applicant's accounts. The scope is in_scope. Facts that PROVE the quoted trigger: E1 shows 8 active privileged accounts, and E2 shows 8 MFA-protected privileged accounts. This indicates all active privileged accounts are protected by MFA. Facts that REFUTE the quoted trigger: None identified. Given unknown information, it is possible that some accounts may not be accounted for or that protection status might change, but based on provided evidence, the condition is true. There are no explicit exception prerequisites mentioned in the rule text. The rule does not specify any conditions under which this strength would not apply. Therefore, exception=does_not_apply. There are no actual incompatible observations identified in the evidence. All documents consistently report that all 8 active privileged accounts are protected by MFA. Conflict=none.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 5; assessment call attempts: 3; seconds: 11.5. Error: `None`.

### retained_history / cyber_d_missing

scope is in_scope because the evidence is from doc:cyber-a.txt which is the specified scope for this criterion The condition states that MFA protection on every active privileged account is a strength. Evidence E1 shows there are 8 active privileged accounts, and E2 shows that 8 of those accounts are MFA-protected. Since the protected count (8) equals the active inventory count (8), all active privileged accounts have MFA protection, satisfying the condition. exception does_not_apply because there are no explicit exceptions mentioned in the criterion text that would prevent the strength from applying conflict none because all evidence supports that all active privileged accounts have MFA protection; there are no contradictory pieces of evidence

Foreign input sources: `['doc:cyber-a.txt']`. Foreign cited sources: `['doc:cyber-a.txt']`.

LLM responses (agent + assessment): 8; assessment call attempts: 6; seconds: 22.1. Error: `None`.

### retained_history / cyber_d_followup

The rule applies to active privileged accounts for each applicant. Evidence E1-E3 covers Northbank Services, application C. Evidence E4-E6 covers Southbank Services, application D. Evidence E7-E9 covers the same applicant and application as E4-E6 but with updated information. For Northbank Services (application C): Active privileged accounts = 8 (E1), MFA-protected privileged accounts = 8 (E3). Since the protected count equals the active inventory count, this proves the trigger is true. For Southbank Services (application D): Active privileged accounts = 12 (E4), but MFA-protected account count has not yet been provided (E6). However, a supplement (E7-E9) later provides MFA-protected privileged accounts = 12, matching the active inventory count. This also proves the trigger is true. Therefore, the condition is true for both applicants. There are no explicit exception prerequisites mentioned in the rule text that would apply to either applicant. There are no actual incompatible observations between the evidence records. All data points support that MFA protection is present on every active privileged account for both applicants.

Foreign input sources: `['doc:cyber-a.txt']`. Foreign cited sources: `['doc:cyber-a.txt']`.

LLM responses (agent + assessment): 8; assessment call attempts: 6; seconds: 27.9. Error: `None`.

### retained_history / unlabelled_criterion

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 2; assessment call attempts: 0; seconds: 1.6. Error: `None`.

### case_scoped / property_a

The rule applies separately to each insured building. The evidence contains information about two buildings (Warehouse 1 and Warehouse 2) within application A. Facts proving: Warehouse 1 roof age is 24 years (E1); Warehouse 2 roof age is 29 years (E3). Facts refuting: None. Given unknown information, it's possible that other buildings may have roof ages <= 20 years. Condition is true because both buildings exceed the 20-year threshold. No explicit exceptions mentioned in the rule text. The rule does not specify any conditions under which this concern would not apply. There are no conflicting observations regarding the roof ages of the buildings. All evidence consistently reports roof ages for Warehouse 1 (24 years) and Warehouse 2 (29 years), both exceeding 20 years.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 5; assessment call attempts: 3; seconds: 13.0. Error: `None`.

### case_scoped / property_b_missing

The rule applies to each insured building. The subject is 'Warehouse 1' which is an insured building. The quoted trigger states that a building with a roof older than 20 years is a concern. Evidence E4 shows that the roof_age_years for Warehouse 1 is null, indicating that the roof age has not been supplied. There are no facts proving that the roof age exceeds 20 years, and there are no facts refuting it either. Given that the roof age is not provided, we cannot confirm that the roof is older than 20 years. Therefore, the condition is unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no actual incompatible observations. The evidence shows that the roof age has not been supplied, but this does not contradict the rule's trigger directly.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 5; assessment call attempts: 3; seconds: 13.2. Error: `None`.

### case_scoped / property_b_followup

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics' application B. The initial evidence (E4) shows that the roof age for Warehouse 1 was null, indicating no information was provided. However, a subsequent update (E9) provides a verified roof age of 5 years. Since 5 years is not greater than 20 years, the condition that the roof is older than 20 years is false. There are no explicit exception prerequisites mentioned in the rule text for C1. There is no actual incompatible observation. The roof age was initially not provided but later updated to 5 years, which does not meet the condition of being older than 20 years.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 8; assessment call attempts: 6; seconds: 19.5. Error: `None`.

### case_scoped / cyber_c

The subject is 'Northbank Services, application C' and the period is not specified, but the evidence covers a single application at a point in time. The scope is in_scope as the evidence directly relates to the applicant's privileged accounts. Facts that PROVE this trigger: E1 shows 'Active privileged accounts: 8', and E2 shows 'MFA-protected privileged accounts: 8'. These indicate all active privileged accounts are protected by MFA. Facts that REFUTE it: None provided. Given unknown information, the condition could still be true if there are no additional unreported privileged accounts or protection gaps. Condition is TRUE because the evidence confirms that all 8 active privileged accounts are MFA-protected. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply. Exception status is does_not_apply. There are no actual incompatible observations in the evidence provided. All documents consistently report that all active privileged accounts (8) are MFA-protected. Conflict status is none.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 5; assessment call attempts: 3; seconds: 12.2. Error: `None`.

### case_scoped / cyber_d_missing

The subject is 'Southbank Services, application D' and the period is unspecified but covers the current assessment period. The evidence shows 12 active privileged accounts. Facts proving: There are 12 active privileged accounts as stated in E1. Facts refuting: The MFA-protected account count has not yet been provided, as stated in E2 and E3. Given unknown information: Since the MFA-protected account count is not provided, we cannot confirm whether all 12 accounts have MFA protection. Therefore, condition = unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. No actual incompatible observations were found. The evidence shows 12 active privileged accounts but does not provide the MFA-protected account count, which leaves the condition unknown rather than contradictory.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 5; assessment call attempts: 3; seconds: 10.0. Error: `None`.

### case_scoped / cyber_d_followup

The subject is Southbank Services, application D. The period in scope is the time of the application review. Facts proving: E1 shows 12 active privileged accounts; E4-E5 show 12 MFA-protected privileged accounts. Facts refuting: None. Given that both counts match, the condition is true. The rule tests whether all active privileged accounts are protected by MFA, which is satisfied here. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations regarding the MFA protection status of privileged accounts for Southbank Services, application D.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 6; assessment call attempts: 4; seconds: 14.5. Error: `None`.

### case_scoped / unlabelled_criterion

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 2; assessment call attempts: 0; seconds: 1.5. Error: `None`.

## Scoring and limitations

Strict passes require collection, exact criterion/classification extraction, all gold supporting spans, source/locator integrity, no foreign inputs, correct status and atomic findings, expected readiness, and complete assessment coverage. Findings are matched one-to-one on required raw supporting spans; additional same-case citations are allowed. Empty/missing criteria cannot pass as a correct abstention. Unsafe ready means the pipeline marked a result ready despite a collection, extraction, isolation, status, or finding failure.

The unlabelled guideline is intentionally ordinary prose without the current extractor's bracketed classification convention. Failure counts against end-to-end performance; it is not silently normalized. Same-case follow-up support includes an earlier document. This tests the existing deterministic text/JSON extractor, not a new LLM parser. Isolation is checked at the assessment input boundary; an agent's free-text answer can still reflect retained history and is not semantically scored. Replayed tools and all model outputs are retained in JSON. These seven turn fixtures are not independent production samples.
