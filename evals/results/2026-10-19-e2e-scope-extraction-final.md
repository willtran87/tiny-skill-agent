# End-to-end document and case-isolation evaluation

State: **completed**. Model: `qwen3-coder:30b`.

Live ReAct agent, raw text/Markdown/JSON documents, registered tool provenance, production extraction and completion assessment. Two profiles use separate checkpointed conversations with the same turn order. Gold is excluded from model inputs. Synthetic, short, non-expert-labeled cases; no OCR, PDF layout, or semantic explanation judging.

| Profile | Turns | Strict passes | Collected | Criteria extracted | Gold spans extracted | Isolated inputs | Correct statuses | Correct findings | Ready | Unsafe ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retained_history | 7 | 3 | 7 | 4 | 5/11 | 4 | 4 | 3 | 2 | 0 |
| case_scoped | 7 | 3 | 7 | 4 | 5/11 | 4 | 4 | 4 | 2 | 0 |

Hardened integration: `retained_history` uses the production middleware's scope_from_context and optional prose extractor. `case_scoped` retains the previous custom mapper, with the same extraction and production scope guard. Both use application-owned source IDs supplied afresh in invocation context; agent conversation history is retained.

| Profile | Turn | Expected → actual | Findings actual/expected | Isolated | Ready | Strict |
| --- | --- | --- | --- | --- | --- | --- |
| retained_history | property_a | matched → matched | 2/2 | True | False | FAIL |
| retained_history | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| retained_history | property_b_followup | no_match → no_match | 0/0 | True | True | PASS |
| retained_history | cyber_c | matched → missing | 0/1 | False | False | FAIL |
| retained_history | cyber_d_missing | insufficient_evidence → missing | 0/0 | False | False | FAIL |
| retained_history | cyber_d_followup | matched → missing | 0/1 | False | False | FAIL |
| retained_history | unlabelled_criterion | matched → matched | 1/1 | True | True | PASS |
| case_scoped | property_a | matched → matched | 2/2 | True | False | FAIL |
| case_scoped | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| case_scoped | property_b_followup | no_match → no_match | 0/0 | True | True | PASS |
| case_scoped | cyber_c | matched → missing | 0/1 | False | False | FAIL |
| case_scoped | cyber_d_missing | insufficient_evidence → missing | 0/0 | False | False | FAIL |
| case_scoped | cyber_d_followup | matched → missing | 0/1 | False | False | FAIL |
| case_scoped | unlabelled_criterion | matched → matched | 1/1 | True | True | PASS |

## Diagnostics

### retained_history / property_a

The rule applies separately to each insured building. The evidence shows two buildings (Warehouse 1 and Warehouse 2) under the same application A, each with stated roof ages. Facts proving: Warehouse 1 has a roof age of 24 years (E1); Warehouse 2 has a roof age of 29 years (E3). Facts refuting: None. Given the roof ages are explicitly stated and exceed 20 years, the condition is true. No explicit exception prerequisites or validity dates mentioned in the rule text. No actual incompatible observations found. Both warehouses have roof ages exceeding 20 years, which aligns with the rule's trigger.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 13.0. Error: `None`.

### retained_history / property_b_missing

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The period in scope is the current application. The quoted trigger states that a building with a roof older than 20 years is a concern. Facts proving this would be a roof age value greater than 20 years. Facts refuting it would be a roof age value less than or equal to 20 years, or a missing roof age value. In this case, the roof_age_years field is null, and the note indicates 'Roof age has not been supplied.' This leaves the condition unknown because there is insufficient information to determine if the roof age exceeds 20 years. There are no explicit exception prerequisites mentioned in the rule text for C1. Therefore, the exception status is 'does_not_apply'. There are no actual incompatible observations. The roof age is not provided, which does not create a contradiction with any other evidence.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 11.4. Error: `None`.

### retained_history / property_b_followup

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The period in scope is the current application period as indicated by the guideline. The initial evidence (E1-E5) shows that the roof age for Warehouse 1 was not supplied, indicated by 'null' in E4 and note 'Roof age has not been supplied.' in E5. However, subsequent evidence (E6-E10) provides a verified roof age of 5 years for Warehouse 1. Since 5 years is less than 20 years, the condition is false. There are no explicit exception prerequisites mentioned in the rule text that would apply here. There is no actual incompatible observation. The initial lack of roof age information was resolved with a verified age of 5 years, which does not meet the condition for concern.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 17.1. Error: `None`.

### retained_history / cyber_c

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 3; extraction calls: 1; assessment call attempts: 0; seconds: 2.5. Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`.

### retained_history / cyber_d_missing

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 3; extraction calls: 1; assessment call attempts: 0; seconds: 2.3. Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`.

### retained_history / cyber_d_followup

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 3; extraction calls: 1; assessment call attempts: 0; seconds: 2.4. Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`.

### retained_history / unlabelled_criterion

The subject is a building (specifically the main building) and the period is not specified, so scope is in_scope. Facts proving: E2 states 'Main building: roof age is 25 years.' This directly proves that the roof age exceeds 20 years. Facts refuting: None. Given unknown information: No other information contradicts this fact. Condition is true because the roof age (25 years) is greater than 20 years. The rule does not specify any exceptions, so exception=does_not_apply. There are no conflicting observations regarding the roof age of the main building. The evidence consistently states that the roof is 25 years old, which satisfies the condition for a concern.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 13.4. Error: `None`.

### case_scoped / property_a

The rule applies separately to each insured building. The evidence contains information about two buildings (Warehouse 1 and Warehouse 2) within the same application A, so both are in scope. Facts proving: Warehouse 1 roof age is 24 years (E1, E2); Warehouse 2 roof age is 29 years (E2, E3). Facts refuting: None. Given the known ages, both buildings exceed the 20-year threshold. The condition is true because both buildings have roofs older than 20 years. The rule does not specify any exceptions. There are no explicit exception prerequisites or validity dates mentioned. There are no conflicting observations regarding the roof ages of Warehouse 1 or Warehouse 2. All evidence consistently reports the ages as 24 and 29 years respectively.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 14.9. Error: `None`.

### case_scoped / property_b_missing

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The period in scope is the current application. The quoted trigger states that a building with a roof older than 20 years is a concern. Facts proving this would be a roof age value greater than 20 years. Facts refuting it would be a roof age value less than or equal to 20 years, or a missing roof age value. In this case, the roof_age_years field is null, and the note indicates 'Roof age has not been supplied.' This leaves the condition unknown because there is insufficient information to determine if the roof age exceeds 20 years. There are no explicit exception prerequisites mentioned in the rule text for C1. Therefore, the exception status is 'does_not_apply'. There are no actual incompatible observations. The roof age is not provided, which does not create a contradiction with any other evidence.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 11.3. Error: `None`.

### case_scoped / property_b_followup

The rule applies to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics'. The period in scope is the current application period as indicated by the guideline. The initial evidence (E1-E5) shows that the roof age for Warehouse 1 was not supplied, indicated by 'null' in E4 and note 'Roof age has not been supplied.' in E5. However, subsequent evidence (E6-E10) provides a verified roof age of 5 years for Warehouse 1. Since 5 years is less than 20 years, the condition is false. There are no explicit exception prerequisites mentioned in the rule text that would apply here. There is no actual incompatible observation. The initial lack of roof age information was resolved with a verified age of 5 years, which does not meet the condition for concern.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 16.5. Error: `None`.

### case_scoped / cyber_c

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 3; extraction calls: 1; assessment call attempts: 0; seconds: 2.8. Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`.

### case_scoped / cyber_d_missing

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 3; extraction calls: 1; assessment call attempts: 0; seconds: 2.6. Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`.

### case_scoped / cyber_d_followup

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 3; extraction calls: 1; assessment call attempts: 0; seconds: 2.6. Error: `{'type': 'ValueError', 'message': 'Extracted prose criterion must explicitly name its classification in the quote'}`.

### case_scoped / unlabelled_criterion

The subject is a building (specifically the main building) and the period is not specified, so scope is in_scope. Facts proving: E2 states 'Main building: roof age is 25 years.' This directly proves that the roof age exceeds 20 years. Facts refuting: None. Given unknown information: No other information contradicts this fact. Condition is true because the roof age (25 years) is greater than 20 years. The rule does not specify any exceptions, so exception=does_not_apply. There are no conflicting observations regarding the roof age of the main building. The evidence consistently states that the roof is 25 years old, which satisfies the condition for a concern.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 6; extraction calls: 1; assessment call attempts: 3; seconds: 13.6. Error: `None`.

## Scoring and limitations

Strict passes require collection, exact criterion/classification extraction, all gold supporting spans, source/locator integrity, no foreign inputs, correct status and atomic findings, expected readiness, and complete assessment coverage. Findings are matched one-to-one on required raw supporting spans; additional same-case citations are allowed. Empty/missing criteria cannot pass as a correct abstention. Unsafe ready means the pipeline marked a result ready despite a collection, extraction, isolation, status, or finding failure.

The unlabelled guideline is intentionally ordinary prose without bracketed classification. Failure counts against end-to-end performance; the fixture is not normalized. Hardened runs opt into structured exact-quote criterion extraction, while evidence extraction stays deterministic. Same-case follow-up support includes an earlier document. Isolation is checked at the assessment input boundary; an agent's free-text answer can still reflect retained history and is not semantically scored. Replayed tools and model outputs are retained in JSON. These seven turn fixtures are not independent production samples.
