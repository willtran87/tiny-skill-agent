# End-to-end document and case-isolation evaluation

State: **completed**. Model: `qwen3-coder:30b`.

Live ReAct agent, raw text/Markdown/JSON documents, registered tool provenance, production extraction and completion assessment. Two profiles use separate checkpointed conversations with the same turn order. Gold is excluded from model inputs. Synthetic, short, non-expert-labeled cases; no OCR, PDF layout, or semantic explanation judging.

| Profile | Turns | Strict passes | Collected | Criteria extracted | Gold spans extracted | Isolated inputs | Correct statuses | Correct findings | Ready | Unsafe ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retained_history | 7 | 5 | 7 | 7 | 11/11 | 7 | 7 | 6 | 3 | 0 |
| case_scoped | 7 | 5 | 7 | 7 | 11/11 | 7 | 7 | 6 | 3 | 0 |

Hardened integration: `retained_history` uses the production middleware's scope_from_context and optional prose extractor. `case_scoped` retains the previous custom mapper, with the same extraction and production scope guard. Both use application-owned source IDs supplied afresh in invocation context; agent conversation history is retained.

| Profile | Turn | Expected → actual | Findings actual/expected | Isolated | Ready | Strict |
| --- | --- | --- | --- | --- | --- | --- |
| retained_history | property_a | matched → matched | 2/2 | True | False | FAIL |
| retained_history | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| retained_history | property_b_followup | no_match → no_match | 0/0 | True | True | PASS |
| retained_history | cyber_c | matched → matched | 1/1 | True | True | PASS |
| retained_history | cyber_d_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| retained_history | cyber_d_followup | matched → matched | 1/1 | True | True | PASS |
| retained_history | unlabelled_criterion | matched → matched | 1/1 | True | False | FAIL |
| case_scoped | property_a | matched → matched | 2/2 | True | False | FAIL |
| case_scoped | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| case_scoped | property_b_followup | no_match → no_match | 0/0 | True | True | PASS |
| case_scoped | cyber_c | matched → matched | 1/1 | True | True | PASS |
| case_scoped | cyber_d_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| case_scoped | cyber_d_followup | matched → matched | 1/1 | True | True | PASS |
| case_scoped | unlabelled_criterion | matched → matched | 1/1 | True | False | FAIL |

## Diagnostics

### retained_history / property_a

The rule applies separately to each insured building. The subject is Warehouse 1 (roof age 24 years) and Warehouse 2 (roof age 29 years). Both are within the scope of the application A. Warehouse 1 has a roof age of 24 years, which is greater than 20 years. Warehouse 2 has a roof age of 29 years, which is also greater than 20 years. Both buildings meet the condition. There are no explicit exceptions mentioned in the rule. No conflicting observations found. Both warehouses have documented roof ages that satisfy the condition.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 34.6. Error: `None`.

### retained_history / property_b_missing

The criterion states that a building with a roof older than 20 years is a concern. However, the roof age for Warehouse 1 is explicitly stated as 'null' and noted as 'Roof age has not been supplied.' Since there is no evidence indicating the roof is older than 20 years, and the information is missing, it cannot be concluded that this condition is met.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 15.0. Error: `None`.

### retained_history / property_b_followup

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The evidence batch includes information about this specific building. The roof age for Warehouse 1 was initially reported as null ('Roof age has not been supplied'). However, a follow-up document (E6-E10) provides a verified roof age of 5 years. Since 5 years is not greater than 20 years, the condition that the roof is older than 20 years is false. There are no explicit exceptions mentioned in the rule text for this criterion. There is no actual incompatible observation. The initial report stated 'Roof age has not been supplied' but the subsequent verified information shows a roof age of 5 years, which does not meet the condition of being older than 20 years.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 19.8. Error: `None`.

### retained_history / cyber_c

The rule applies to active privileged accounts for the applicant 'Northbank Services, application C'. The subject is the applicant and the period is current as per the evidence. The evidence shows that there are 8 active privileged accounts and all 8 are MFA-protected. This directly supports the trigger condition that MFA protection is on every active privileged account. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no conflicting observations in the provided evidence. All documents consistently report that all 8 active privileged accounts are MFA-protected.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 16.9. Error: `None`.

### retained_history / cyber_d_missing

The rule applies to active privileged accounts for the applicant 'Southbank Services, application D'. The subject is in scope. The evidence shows that there are 12 active privileged accounts (E1). However, the MFA-protected account count has not yet been provided (E2, E3). Since the rule requires that ALL active privileged accounts have MFA protection to be a strength, and no information is available regarding whether these 12 accounts are protected, the condition cannot be confirmed as true. The lack of data on MFA protection means we cannot affirm that every account is protected. There are no explicit exceptions mentioned in the rule text for this criterion. There are no conflicting observations regarding the MFA protection status of the accounts. The only information is that the count has not yet been provided, which does not create a contradiction.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 17.4. Error: `None`.

### retained_history / cyber_d_followup

The rule applies to active privileged accounts for the applicant 'Southbank Services, application D'. The subject is in scope because the evidence provides counts for both active privileged accounts and MFA-protected accounts for this specific applicant. The evidence shows that there are 12 active privileged accounts (E1) and 12 MFA-protected privileged accounts (E5). Since the protected count equals the active inventory count, the condition 'MFA protection on every active privileged account' is met. The fact that the MFA-protected account count was not provided initially (E3) does not change this conclusion as the final documentation confirms 12 MFA-protected accounts. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not contain any 'unless' or 'except' conditions that would apply to this case. There are no conflicting observations regarding the MFA protection status of privileged accounts for Southbank Services, application D. The evidence consistently shows that all 12 active privileged accounts are protected by MFA.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 25.4. Error: `None`.

### retained_history / unlabelled_criterion

The rule applies to each insured building individually, as stated in the context: 'Apply this rule separately to each insured building.' The subject of the evidence is the main building of Applicant Orchard Storage. The evidence shows that the main building's roof age is 25 years (E2). Since 25 years is greater than 20 years, the condition 'roof older than 20 years' is met. Therefore, the trigger is true. There are no explicit exceptions mentioned in the rule text for C1. The rule does not contain any conditional language such as 'unless' or 'except' that would apply to this case. There are no conflicting observations in the provided evidence that would create an unresolved contradiction regarding the roof age of the main building. The evidence consistently states that the roof is 25 years old.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 15.0. Error: `None`.

### case_scoped / property_a

The rule applies separately to each insured building. The evidence includes two buildings (Warehouse 1 and Warehouse 2) from the same application A, so both are in scope. Warehouse 1 has a roof age of 24 years, which is greater than 20 years; Warehouse 2 has a roof age of 29 years, which is also greater than 20 years. Both buildings meet the condition. There are no explicit exceptions mentioned in the rule. No conflicting observations were found. Both buildings have clearly stated roof ages that satisfy the condition.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 20.3. Error: `None`.

### case_scoped / property_b_missing

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The evidence batch includes information about this specific building. The roof age for Warehouse 1 is stated as null in the application, indicating that the roof age has not been supplied. There are no observations supporting or refuting a roof age greater than 20 years. Therefore, it cannot be determined if the condition is met. There are no explicit exception prerequisites mentioned in the rule text. There are no conflicting observations regarding the roof age of Warehouse 1. The only information provided is that the roof age has not been supplied.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 15.0. Error: `None`.

### case_scoped / property_b_followup

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The evidence batch includes information about this specific building. The roof age for Warehouse 1 was initially reported as null ('Roof age has not been supplied'). However, a follow-up document (E6-E10) provides a verified roof age of 5 years. Since 5 years is not greater than 20 years, the condition that the roof is older than 20 years is false. There are no explicit exceptions mentioned in the rule text for this criterion. There is no actual incompatible observation. The initial report stated that roof age was not supplied, but a subsequent verified document provided the roof age as 5 years. This resolved the uncertainty without creating a contradiction.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 19.8. Error: `None`.

### case_scoped / cyber_c

The rule applies to active privileged accounts for the applicant 'Northbank Services, application C'. The subject is the applicant and the period is current as per the evidence. The evidence shows that there are 8 active privileged accounts and all 8 are MFA-protected. This directly supports the trigger condition that MFA protection is on every active privileged account. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no conflicting observations in the provided evidence. All documents consistently report that all 8 active privileged accounts are MFA-protected.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 16.0. Error: `None`.

### case_scoped / cyber_d_missing

The rule applies to active privileged accounts for the applicant 'Southbank Services, application D'. The subject is in scope. The evidence shows that there are 12 active privileged accounts (E1). However, the MFA-protected account count has not yet been provided (E2, E3). Since the rule requires that ALL active privileged accounts have MFA protection to be a strength, and no information is available regarding whether these 12 accounts are protected, the condition cannot be confirmed as true. The lack of data on MFA protection means we cannot affirm that every account is protected. There are no explicit exceptions mentioned in the rule text for this criterion. There are no conflicting observations regarding the MFA protection status of the accounts. The only information is that the count has not yet been provided, which does not create a contradiction.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 18.4. Error: `None`.

### case_scoped / cyber_d_followup

The rule applies to active privileged accounts for the applicant 'Southbank Services, application D'. The subject is in scope because the evidence provides counts for both active privileged accounts and MFA-protected accounts for this specific applicant. The evidence shows that there are 12 active privileged accounts (E1) and 12 MFA-protected privileged accounts (E5). Since the protected count equals the active inventory count, the condition 'MFA protection on every active privileged account' is met. The fact that the MFA-protected account count was not provided initially (E3) does not change this conclusion as the final documentation confirms 12 MFA-protected accounts. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not contain any 'unless' or 'except' conditions that would apply to this case. There are no conflicting observations regarding the MFA protection status of privileged accounts for Southbank Services, application D. The evidence consistently shows that all 12 active privileged accounts are protected by MFA.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 29.5. Error: `None`.

### case_scoped / unlabelled_criterion

The rule applies to each insured building individually, as stated in the context: 'Apply this rule separately to each insured building.' The subject of the evidence is the main building of Applicant Orchard Storage. The evidence shows that the main building's roof age is 25 years (E2). Since 25 years is greater than 20 years, the condition 'roof older than 20 years' is met. Therefore, the trigger is true. There are no explicit exceptions mentioned in the rule text for C1. The rule does not contain any conditional language such as 'unless' or 'except' that would apply to this case. There are no conflicting observations in the provided evidence that would create an unresolved contradiction regarding the roof age of the main building. The evidence consistently states that the roof is 25 years old.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 15.6. Error: `None`.

## Scoring and limitations

Strict passes require collection, exact criterion/classification extraction, all gold supporting spans, source/locator integrity, no foreign inputs, correct status and atomic findings, expected readiness, and complete assessment coverage. Findings are matched one-to-one on required raw supporting spans; additional same-case citations are allowed. Empty/missing criteria cannot pass as a correct abstention. Unsafe ready means the pipeline marked a result ready despite a collection, extraction, isolation, status, or finding failure.

The unlabelled guideline is intentionally ordinary prose without bracketed classification. Failure counts against end-to-end performance; the fixture is not normalized. Hardened runs opt into structured exact-quote criterion extraction, while evidence extraction stays deterministic. Same-case follow-up support includes an earlier document. Isolation is checked at the assessment input boundary; an agent's free-text answer can still reflect retained history and is not semantically scored. Replayed tools and model outputs are retained in JSON. These seven turn fixtures are not independent production samples.
