# End-to-end document and case-isolation evaluation

State: **interrupted**. Model: `qwen3-coder:30b`.

Live ReAct agent, raw text/Markdown/JSON documents, registered tool provenance, production extraction and completion assessment. Two profiles use separate checkpointed conversations with the same turn order. Gold is excluded from model inputs. Synthetic, short, non-expert-labeled cases; no OCR, PDF layout, or semantic explanation judging.

| Profile | Turns | Strict passes | Collected | Criteria extracted | Gold spans extracted | Isolated inputs | Correct statuses | Correct findings | Ready | Unsafe ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retained_history | 5 | 2 | 5 | 3 | 8/8 | 5 | 5 | 3 | 1 | 0 |
| case_scoped | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 |

Hardened integration: `retained_history` uses the production middleware's scope_from_context and optional prose extractor. `case_scoped` retains the previous custom mapper, with the same extraction and production scope guard. Both use application-owned source IDs supplied afresh in invocation context; agent conversation history is retained.

| Profile | Turn | Expected → actual | Findings actual/expected | Isolated | Ready | Strict |
| --- | --- | --- | --- | --- | --- | --- |
| retained_history | property_a | matched → matched | 2/2 | True | False | FAIL |
| retained_history | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| retained_history | property_b_followup | no_match → no_match | 0/0 | True | True | PASS |
| retained_history | cyber_c | matched → matched | 3/1 | True | False | FAIL |
| retained_history | cyber_d_missing | insufficient_evidence → insufficient_evidence | 1/0 | True | False | FAIL |

## Diagnostics

### retained_history / property_a

The rule applies separately to each insured building. The evidence contains information about two buildings (Warehouse 1 and Warehouse 2) within the same application A, so both are in scope. Facts proving: Warehouse 1 roof age is 24 years (E1); Warehouse 2 roof age is 29 years (E3). Facts refuting: None. Given unknown information, it's possible that other buildings may have roof ages <= 20 years, but this does not affect the existing evidence. Condition is true because both buildings exceed the 20-year threshold. No explicit exceptions mentioned in the rule text. The rule does not specify any conditions under which this concern would not apply. There are no conflicting observations regarding the roof ages of Warehouse 1 or Warehouse 2. All evidence consistently states the ages as 24 and 29 years respectively.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 35.5. Error: `None`.

### retained_history / property_b_missing

The rule applies to each insured building. The subject is 'Warehouse 1' which is an insured building. The quoted trigger states that a building with a roof older than 20 years is a concern. Facts proving this would be a roof age value greater than 20 years. Facts refuting it would be a roof age value less than or equal to 20 years, or a missing roof age value. In this case, the roof_age_years field is null, and the note indicates 'Roof age has not been supplied.' This means we do not have sufficient information to determine if the roof age exceeds 20 years. Therefore, the condition is unknown. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations regarding the roof age of Warehouse 1. The evidence only indicates that the roof age has not been supplied, which does not create an incompatible observation.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 11.8. Error: `None`.

### retained_history / property_b_followup

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics' application B. The initial evidence (E4) shows that the roof age for Warehouse 1 was null, indicating no information was provided. However, a subsequent update (E9) provides a verified roof age of 5 years. Since 5 years is not greater than 20 years, the condition that the roof is older than 20 years is false. There are no explicit exception prerequisites mentioned in the rule text for C1. There is no actual incompatible observation. The initial null value for roof age was later corrected to 5 years, which does not meet the condition of being older than 20 years.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 17.2. Error: `None`.

### retained_history / cyber_c

The subject is 'Northbank Services, application C' and the period is not specified, but the evidence covers the current state of the applicant's accounts. The scope is in_scope as the evidence directly relates to the applicant's privileged account status. Facts that PROVE this quoted trigger: E1 shows 'Active privileged accounts: 8', and E2 shows 'MFA-protected privileged accounts: 8'. These indicate that all active privileged accounts are protected by MFA. Facts that REFUTE it: None provided. Given the information, it is possible that all active privileged accounts are protected by MFA, so the condition is true. There are no explicit exception prerequisites mentioned in the rule for C1. The rule does not specify any conditions under which this strength would not apply. Therefore, exception=does_not_apply. There are no actual incompatible observations in the evidence provided. All documents support that all active privileged accounts are protected by MFA. Conflict=none.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 13; extraction calls: 1; assessment call attempts: 10; seconds: 38.1. Error: `None`.

### retained_history / cyber_d_missing

The subject is 'Southbank Services, application D' and the period is unspecified but covers the current assessment period. The evidence shows 12 active privileged accounts. Facts proving: E1 shows 12 active privileged accounts for Southbank Services, application D. Facts refuting: E3 states that the MFA-protected account count has not yet been provided. Given unknown information (the MFA protection status of the 12 accounts), it cannot be confirmed whether all are protected. Condition is unknown because the required MFA protection data is missing. No explicit exception prerequisites or validity dates mentioned in the rule text. There are no actual incompatible observations. E1 and E2 support the existence of 12 active accounts, while E3 indicates that MFA protection data is not yet provided. These do not contradict each other directly.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 12; extraction calls: 1; assessment call attempts: 9; seconds: 33.6. Error: `None`.

## Scoring and limitations

Strict passes require collection, exact criterion/classification extraction, all gold supporting spans, source/locator integrity, no foreign inputs, correct status and atomic findings, expected readiness, and complete assessment coverage. Findings are matched one-to-one on required raw supporting spans; additional same-case citations are allowed. Empty/missing criteria cannot pass as a correct abstention. Unsafe ready means the pipeline marked a result ready despite a collection, extraction, isolation, status, or finding failure.

The unlabelled guideline is intentionally ordinary prose without bracketed classification. Failure counts against end-to-end performance; the fixture is not normalized. Hardened runs opt into structured exact-quote criterion extraction, while evidence extraction stays deterministic. Same-case follow-up support includes an earlier document. Isolation is checked at the assessment input boundary; an agent's free-text answer can still reflect retained history and is not semantically scored. Replayed tools and model outputs are retained in JSON. These seven turn fixtures are not independent production samples.
