# End-to-end document and case-isolation evaluation

State: **interrupted**. Model: `qwen3-coder:30b`.

Live ReAct agent, raw text/Markdown/JSON documents, registered tool provenance, production extraction and completion assessment. Two profiles use separate checkpointed conversations with the same turn order. Gold is excluded from model inputs. Synthetic, short, non-expert-labeled cases; no OCR, PDF layout, or semantic explanation judging.

| Profile | Turns | Strict passes | Collected | Criteria extracted | Gold spans extracted | Isolated inputs | Correct statuses | Correct findings | Ready | Unsafe ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retained_history | 7 | 1 | 7 | 4 | 5/11 | 4 | 3 | 3 | 0 | 0 |
| case_scoped | 2 | 1 | 2 | 2 | 3/3 | 2 | 2 | 1 | 0 | 0 |

Hardened integration: `retained_history` uses the production middleware's scope_from_context and optional prose extractor. `case_scoped` retains the previous custom mapper, with the same extraction and production scope guard. Both use application-owned source IDs supplied afresh in invocation context; agent conversation history is retained.

| Profile | Turn | Expected → actual | Findings actual/expected | Isolated | Ready | Strict |
| --- | --- | --- | --- | --- | --- | --- |
| retained_history | property_a | matched → matched | 2/2 | True | False | FAIL |
| retained_history | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |
| retained_history | property_b_followup | no_match → insufficient_evidence | 0/0 | True | False | FAIL |
| retained_history | cyber_c | matched → missing | 0/1 | False | False | FAIL |
| retained_history | cyber_d_missing | insufficient_evidence → missing | 0/0 | False | False | FAIL |
| retained_history | cyber_d_followup | matched → missing | 0/1 | False | False | FAIL |
| retained_history | unlabelled_criterion | matched → matched | 1/1 | True | False | FAIL |
| case_scoped | property_a | matched → matched | 2/2 | True | False | FAIL |
| case_scoped | property_b_missing | insufficient_evidence → insufficient_evidence | 0/0 | True | False | PASS |

## Diagnostics

### retained_history / property_a

The rule applies separately to each insured building. The subject buildings are Warehouse 1 and Warehouse 2, both from application A. Warehouse 1 has a roof age of 24 years, which is greater than 20 years. Warehouse 2 has a roof age of 29 years, which is also greater than 20 years. Both buildings meet the condition. There are no explicit exceptions mentioned in the rule. No conflicting observations were found. Both buildings have roof ages that exceed 20 years as required by the rule.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 34.4. Error: `None`.

### retained_history / property_b_missing

The rule applies separately to each insured building. The subject is 'Warehouse 1' which is an insured building. The roof age for 'Warehouse 1' is stated as null in the application, indicating that the roof age has not been supplied. There are no observations supporting or refuting that the roof is older than 20 years. Therefore, it cannot be determined whether the condition is true or false based on available evidence. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations regarding the roof age of 'Warehouse 1'. The only information provided is that the roof age has not been supplied, which does not contradict the trigger condition.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 16.4. Error: `None`.

### retained_history / property_b_followup

The criterion states that a building with a roof older than 20 years is a concern. In the initial evidence (E1-E5), the roof age for Warehouse 1 is listed as null with a note stating 'Roof age has not been supplied.' This lack of information means it is unknown whether the roof age exceeds 20 years. Since there is missing evidence regarding the roof age, we cannot definitively conclude that the condition is met or not met.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 12; extraction calls: 1; assessment call attempts: 9; seconds: 27.4. Error: `None`.

### retained_history / cyber_c

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 6.6. Error: `{'type': 'ValueError', 'message': "Implicit criterion 'Compare counts for the same applicant. All privileged accounts means the protected count equals the active inventory count.' does not contain the label 'strength'. Supply classification_quote as the exact source sentence defining that label for this outcome. Do not leave it empty. If no source mapping exists, declare incomplete."}`.

### retained_history / cyber_d_missing

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 6.4. Error: `{'type': 'ValueError', 'message': 'Classification mapping must be an exact source quote naming the classification'}`.

### retained_history / cyber_d_followup

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 6.4. Error: `{'type': 'ValueError', 'message': 'Classification mapping must be an exact source quote naming the classification'}`.

### retained_history / unlabelled_criterion

The rule applies to each insured building individually, as stated in the context: 'Apply this rule separately to each insured building.' The evidence E1 and E2 describe the main building's roof age as 25 years, which is the subject of evaluation. The evidence shows that the main building has a roof that is 25 years old. Since 25 years is greater than 20 years, the condition 'roof older than 20 years' is met. Therefore, the trigger is true. There are no explicit exception prerequisites mentioned in the rule text that would apply to this case. The rule does not contain any conditional language such as 'unless' or 'except' that would indicate an exception. There are no conflicting observations in the provided evidence. Both E1 and E2 refer to the same building's roof age, and there is no contradictory information.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 18.3. Error: `None`.

### case_scoped / property_a

The rule applies separately to each insured building. The evidence includes two buildings (Warehouse 1 and Warehouse 2) from the same application A. Warehouse 1 has a roof age of 24 years, which is greater than 20 years. Warehouse 2 has a roof age of 29 years, which is also greater than 20 years. Both buildings meet the condition. There are no explicit exceptions mentioned in the rule text. There are no conflicting observations regarding the roof ages of the buildings. Both warehouses have clearly stated roof ages that satisfy the condition.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 10; extraction calls: 1; assessment call attempts: 7; seconds: 21.6. Error: `None`.

### case_scoped / property_b_missing

The rule applies separately to each insured building. The subject is 'Warehouse 1' which is an insured building. The evidence shows that the roof age for 'Warehouse 1' is null, indicating that the roof age has not been supplied. There are no observations supporting or refuting that the roof is older than 20 years. Therefore, it cannot be determined whether the condition is true or false based on available information. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations regarding the roof age of 'Warehouse 1'. The only information provided is that the roof age has not been supplied, which does not contradict the trigger condition.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 17.3. Error: `None`.

## Scoring and limitations

Strict passes require collection, exact criterion/classification extraction, all gold supporting spans, source/locator integrity, no foreign inputs, correct status and atomic findings, expected readiness, and complete assessment coverage. Findings are matched one-to-one on required raw supporting spans; additional same-case citations are allowed. Empty/missing criteria cannot pass as a correct abstention. Unsafe ready means the pipeline marked a result ready despite a collection, extraction, isolation, status, or finding failure.

The unlabelled guideline is intentionally ordinary prose without bracketed classification. Failure counts against end-to-end performance; the fixture is not normalized. Hardened runs opt into structured exact-quote criterion extraction, while evidence extraction stays deterministic. Same-case follow-up support includes an earlier document. Isolation is checked at the assessment input boundary; an agent's free-text answer can still reflect retained history and is not semantically scored. Replayed tools and model outputs are retained in JSON. These seven turn fixtures are not independent production samples.
