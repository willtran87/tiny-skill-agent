# End-to-end document and case-isolation evaluation

State: **completed**. Model: `qwen3-coder:30b`.

Live ReAct agent, raw text/Markdown/JSON documents, registered tool provenance, production extraction and completion assessment. Two profiles use separate checkpointed conversations with the same turn order. Gold is excluded from model inputs. Synthetic, short, non-expert-labeled cases; no OCR, PDF layout, or semantic explanation judging.

| Profile | Turns | Strict passes | Collected | Criteria extracted | Gold spans extracted | Isolated inputs | Correct statuses | Correct findings | Ready | Unsafe ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retained_history | 7 | 5 | 7 | 7 | 11/11 | 7 | 7 | 7 | 3 | 0 |
| case_scoped | 7 | 5 | 7 | 7 | 11/11 | 7 | 7 | 7 | 3 | 0 |

Hardened integration: `retained_history` uses the production middleware's scope_from_context and optional prose extractor. `case_scoped` retains the previous custom mapper, with the same extraction and production scope guard. Both use application-owned source IDs supplied afresh in invocation context; agent conversation history is retained.

| Profile | Turn | Expected → actual | Findings actual/expected | Isolated | Ready | Strict |
| --- | --- | --- | --- | --- | --- | --- |
| retained_history | property_a | matched → matched | 2/2 | True | False | FAIL |
| retained_history | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| retained_history | property_b_followup | no_match → no_match | 0/0 | True | True | PASS |
| retained_history | cyber_c | matched → matched | 1/1 | True | True | PASS |
| retained_history | cyber_d_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| retained_history | cyber_d_followup | matched → matched | 1/1 | True | False | FAIL |
| retained_history | unlabelled_criterion | matched → matched | 1/1 | True | True | PASS |
| case_scoped | property_a | matched → matched | 2/2 | True | False | FAIL |
| case_scoped | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| case_scoped | property_b_followup | no_match → no_match | 0/0 | True | True | PASS |
| case_scoped | cyber_c | matched → matched | 1/1 | True | True | PASS |
| case_scoped | cyber_d_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| case_scoped | cyber_d_followup | matched → matched | 1/1 | True | False | FAIL |
| case_scoped | unlabelled_criterion | matched → matched | 1/1 | True | True | PASS |

## Diagnostics

### retained_history / property_a

The rule applies separately to each insured building. The evidence contains information about two buildings (Warehouse 1 and Warehouse 2) under the same application A, so both are in scope. Facts proving: Warehouse 1 roof age is 24 years (E1, E2); Warehouse 2 roof age is 29 years (E2, E3). Facts refuting: None. Given the known ages, both buildings exceed the 20-year threshold. The condition is true because both buildings have roofs older than 20 years. No explicit exception prerequisites are mentioned in the rule text. The rule does not specify any conditions under which this concern would not apply. There are no conflicting observations regarding the roof ages of Warehouse 1 or Warehouse 2. All evidence consistently reports the ages as 24 and 29 years respectively, with no contradiction in the data.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 5; extraction calls: 0; assessment call attempts: 3; seconds: 13.7. Error: `None`.

### retained_history / property_b_missing

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The period in scope is the current application. The quoted trigger states that a building with a roof older than 20 years is a concern. Facts proving this would be a roof age value greater than 20 years. Facts refuting it would be a roof age value less than or equal to 20 years, or a missing roof age value. In this case, the roof_age_years field is null, and the note indicates 'Roof age has not been supplied.' This leaves the condition unknown because there is insufficient information to determine if the roof age exceeds 20 years. There are no explicit exception prerequisites mentioned in the rule text for C1. Therefore, the exception status is 'does_not_apply'. There are no actual incompatible observations. The roof age is not provided, which does not create a contradiction with any other evidence.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 5; extraction calls: 0; assessment call attempts: 3; seconds: 10.6. Error: `None`.

### retained_history / property_b_followup

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The period in scope is the current application period as indicated by the guideline. The initial evidence (E1-E5) shows that the roof age for Warehouse 1 was not supplied, indicated by 'null' in E4 and note 'Roof age has not been supplied.' in E5. However, subsequent evidence (E6-E10) provides a verified roof age of 5 years for Warehouse 1. Since 5 years is less than 20 years, the condition is false. There are no explicit exception prerequisites mentioned in the rule text that would apply here. There is no actual incompatible observation. The initial lack of roof age information was resolved with a verified age of 5 years, which does not meet the condition for concern.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 0; assessment call attempts: 5; seconds: 16.4. Error: `None`.

### retained_history / cyber_c

The subject is 'Northbank Services, application C' and the period is not specified, but the evidence covers the current state of the applicant's accounts. The scope is in_scope as the evidence directly relates to the applicant's privileged account status. Facts that PROVE this quoted trigger: E1 shows 'Active privileged accounts: 8', and E2 shows 'MFA-protected privileged accounts: 8'. These indicate that all active privileged accounts are protected by MFA. Facts that REFUTE it: None provided. Given the information, it is possible that all active privileged accounts are protected by MFA, so the condition is true. There are no explicit exception prerequisites mentioned in the rule for C1. The rule does not specify any conditions under which this strength would not apply. Therefore, exception=does_not_apply. There are no actual incompatible observations in the evidence provided. All documents support that all active privileged accounts are protected by MFA. Conflict=none.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 5; extraction calls: 0; assessment call attempts: 3; seconds: 12.5. Error: `None`.

### retained_history / cyber_d_missing

The subject is 'Southbank Services' with application D. The period in scope is the current assessment period as no specific time frame is mentioned. Facts proving: E1 states there are 12 active privileged accounts for Southbank Services, application D. Facts refuting: E2 and E3 state that the MFA-protected account count has not yet been provided. Given that the protected-account count is absent, we cannot confirm that all 12 active privileged accounts have MFA protection. Therefore, condition=unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no actual incompatible observations identified. E1 provides the number of active privileged accounts, while E2 and E3 indicate that the MFA-protected account count is not yet provided. These do not contradict each other directly.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 5; extraction calls: 0; assessment call attempts: 3; seconds: 10.4. Error: `None`.

### retained_history / cyber_d_followup

The subject is Southbank Services, application D. The period in scope is the time of assessment for application D. Facts proving: E1 shows 12 active privileged accounts; E4-E5 show 12 MFA-protected privileged accounts. Facts refuting: None. Given that both counts match exactly, and no information suggests otherwise, the condition is true. No explicit exception prerequisites are mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply. There are no actual incompatible observations. All evidence supports that 12 out of 12 active privileged accounts have MFA protection, which aligns with the strength criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 0; assessment call attempts: 4; seconds: 14.3. Error: `None`.

### retained_history / unlabelled_criterion

The rule applies to each insured building. The evidence mentions 'Main building' with roof age of 25 years, which is the subject in scope. Facts proving: E2 states 'Main building: roof age is 25 years.' This directly supports that the roof is older than 20 years. Facts refuting: None. Given unknown information: No other facts contradict this, and no additional evidence is needed to confirm the roof age. Condition status: true. The rule does not specify any exceptions. There are no explicit exception prerequisites or validity dates mentioned. Exception status: does_not_apply. There are no actual incompatible observations. Both evidence items refer to the same building's roof age and do not contradict each other. Conflict status: none.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 13.7. Error: `None`.

### case_scoped / property_a

The rule applies separately to each insured building. The evidence shows two buildings (Warehouse 1 and Warehouse 2) with roof ages of 24 and 29 years respectively, both exceeding 20 years. Facts proving: Warehouse 1 has a 24-year-old roof (E1, E2); Warehouse 2 has a 29-year-old roof (E2, E3). Facts refuting: None. Given unknown information: The rule's trigger is met for both buildings as both have roofs older than 20 years. Condition: true No explicit exception prerequisites or validity dates mentioned in the rule. Exception: does_not_apply No actual incompatible observations identified. Warehouse 1 and Warehouse 2 are different buildings with different roof ages, but both meet the concern criteria independently. Conflict: none

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 0; assessment call attempts: 5; seconds: 25.1. Error: `None`.

### case_scoped / property_b_missing

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The period in scope is the current application. The quoted trigger states that a building with a roof older than 20 years is a concern. Facts proving this would be a roof age value greater than 20 years. Facts refuting it would be a roof age value less than or equal to 20 years, or a missing roof age value. In this case, the roof_age_years field is null, and the note indicates 'Roof age has not been supplied.' This leaves the condition unknown because there is insufficient information to determine if the roof age exceeds 20 years. There are no explicit exception prerequisites mentioned in the rule text for C1. Therefore, the exception status is 'does_not_apply'. There are no actual incompatible observations. The roof age is not provided, which does not create a contradiction with any other evidence.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 5; extraction calls: 0; assessment call attempts: 3; seconds: 11.5. Error: `None`.

### case_scoped / property_b_followup

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The period in scope is the current application period as indicated by the guideline. The initial evidence (E1-E5) shows that the roof age for Warehouse 1 was not supplied, indicated by 'null' in E4 and note 'Roof age has not been supplied.' in E5. However, subsequent evidence (E6-E10) provides a verified roof age of 5 years for Warehouse 1. Since 5 years is less than 20 years, the condition is false. There are no explicit exception prerequisites mentioned in the rule text that would apply here. There is no actual incompatible observation. The initial lack of roof age information was resolved with a verified age of 5 years, which does not meet the condition for concern.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 0; assessment call attempts: 5; seconds: 18.0. Error: `None`.

### case_scoped / cyber_c

The subject is 'Northbank Services, application C' and the period is not specified, but the evidence covers the current state of the applicant's accounts. The scope is in_scope. Facts that PROVE the quoted trigger: E1 shows 8 active privileged accounts, and E2 shows 8 MFA-protected privileged accounts. These facts confirm that every active privileged account has MFA protection. Facts that REFUTE the trigger: None. Given the known information, it is true that MFA protection exists on every active privileged account. Therefore, condition=true. There are no explicit exception prerequisites mentioned in the rule. The rule does not specify any conditions under which this strength would not apply. Exception=does_not_apply. There are no actual incompatible observations in the evidence provided. All documents consistently report that all 8 active privileged accounts are protected by MFA. Conflict=none.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 5; extraction calls: 0; assessment call attempts: 3; seconds: 13.7. Error: `None`.

### case_scoped / cyber_d_missing

The subject is 'Southbank Services' with application D. The period in scope is the current assessment period as no specific time frame is mentioned. Facts proving: E1 states there are 12 active privileged accounts for Southbank Services, application D. Facts refuting: E2 and E3 state that the MFA-protected account count has not yet been provided. Given that the protected-account count is absent, we cannot confirm that all 12 active privileged accounts have MFA protection. Therefore, condition=unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no actual incompatible observations identified. E1 provides the number of active privileged accounts, while E2 and E3 indicate that the MFA-protected account count is not yet provided. These do not contradict each other directly.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 5; extraction calls: 0; assessment call attempts: 3; seconds: 11.4. Error: `None`.

### case_scoped / cyber_d_followup

The subject is Southbank Services, application D. The period in scope is the time of assessment for application D. Facts proving: E1 shows 12 active privileged accounts; E4-E5 show 12 MFA-protected privileged accounts. Facts refuting: None. Given that both counts match exactly, and no information suggests otherwise, the condition is true. No explicit exception prerequisites are mentioned in the rule text for C1. The rule does not specify any conditions under which this strength would not apply. There are no actual incompatible observations. All evidence supports that 12 out of 12 active privileged accounts have MFA protection, which aligns with the strength criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 0; assessment call attempts: 6; seconds: 24.3. Error: `None`.

### case_scoped / unlabelled_criterion

The rule applies to each insured building. The evidence mentions 'Main building' with roof age of 25 years, which is the subject in scope. Facts proving: E2 states 'Main building: roof age is 25 years.' This directly supports that the roof is older than 20 years. Facts refuting: None. Given unknown information: No other information contradicts the roof age being 25 years. Condition: true The rule does not specify any exceptions. Therefore, no exception applies. There are no conflicting observations regarding the roof age of the main building. The evidence consistently states that the roof is 25 years old, which satisfies the condition for concern.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 14.8. Error: `None`.

## Scoring and limitations

Strict passes require collection, exact criterion/classification extraction, all gold supporting spans, source/locator integrity, no foreign inputs, correct status and atomic findings, expected readiness, and complete assessment coverage. Findings are matched one-to-one on required raw supporting spans; additional same-case citations are allowed. Empty/missing criteria cannot pass as a correct abstention. Unsafe ready means the pipeline marked a result ready despite a collection, extraction, isolation, status, or finding failure.

The unlabelled guideline is intentionally ordinary prose without bracketed classification. Failure counts against end-to-end performance; the fixture is not normalized. Hardened runs opt into structured exact-quote criterion extraction, while evidence extraction stays deterministic. Same-case follow-up support includes an earlier document. Isolation is checked at the assessment input boundary; an agent's free-text answer can still reflect retained history and is not semantically scored. Replayed tools and model outputs are retained in JSON. These seven turn fixtures are not independent production samples.
