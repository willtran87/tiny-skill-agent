# End-to-end document and case-isolation evaluation

State: **completed**. Model: `qwen3-coder:30b`.

Live ReAct agent, raw text/Markdown/JSON documents, registered tool provenance, production extraction and completion assessment. Two profiles use separate checkpointed conversations with the same turn order. Gold is excluded from model inputs. Synthetic, short, non-expert-labeled cases; no OCR, PDF layout, or semantic explanation judging.

| Profile | Turns | Strict passes | Collected | Criteria extracted | Gold spans extracted | Isolated inputs | Correct statuses | Correct findings | Ready | Unsafe ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retained_history | 7 | 3 | 7 | 4 | 5/11 | 4 | 4 | 3 | 2 | 0 |
| case_scoped | 7 | 3 | 7 | 4 | 5/11 | 4 | 4 | 3 | 2 | 0 |

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

The rule applies separately to each insured building. The evidence includes two buildings (Warehouse 1 and Warehouse 2) from the same application A. Warehouse 1 has a roof age of 24 years, which is greater than 20 years. Warehouse 2 has a roof age of 29 years, which is also greater than 20 years. Both buildings meet the condition. There are no explicit exceptions mentioned in the rule text. No conflicting observations were found. Both buildings have documented roof ages that satisfy the condition.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 16.2. Error: `None`.

### retained_history / property_b_missing

The criterion states that a building with a roof older than 20 years is a concern. However, the evidence shows that the roof age for Warehouse 1 is null and explicitly noted as 'Roof age has not been supplied.' Since there is no information indicating the roof age, it cannot be determined whether the roof is older than 20 years. Therefore, the condition cannot be evaluated based on the provided evidence.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 13.3. Error: `None`.

### retained_history / property_b_followup

The rule applies separately to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics' application B. The roof age for Warehouse 1 was initially reported as null ('Roof age has not been supplied'). However, a follow-up document (E6-E10) provides a verified roof age of 5 years. Since 5 years is not greater than 20 years, the condition that the roof is older than 20 years is false. There are no explicit exception prerequisites mentioned in the rule text for C1. There is no actual incompatible observation. The initial null roof age was corrected to 5 years, which does not meet the condition of being older than 20 years.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 17.8. Error: `None`.

### retained_history / cyber_c

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 5.5. Error: `{'type': 'ValueError', 'message': 'Line review must link to an extracted rule covering that source line'}`.

### retained_history / cyber_d_missing

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 6.6. Error: `{'type': 'ValueError', 'message': 'Line review must link to an extracted rule covering that source line'}`.

### retained_history / cyber_d_followup

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 6.4. Error: `{'type': 'ValueError', 'message': 'Line review must link to an extracted rule covering that source line'}`.

### retained_history / unlabelled_criterion

The rule applies to each insured building individually, as stated in the context: 'Apply this rule separately to each insured building.' The evidence includes information about one main building. The evidence shows that the main building has a roof age of 25 years. Since 25 years is greater than 20 years, the condition 'roof older than 20 years' is true. The supporting fact is E2: 'Main building: roof age is 25 years.' There are no explicit exceptions mentioned in the rule text for C1. Therefore, the exception does not apply. There are no conflicting observations in the provided evidence that would create an unresolved contradiction regarding the roof age of the building. Both pieces of evidence refer to the same building and support the same conclusion about the roof age.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 16.9. Error: `None`.

### case_scoped / property_a

The rule applies separately to each insured building. The evidence contains information about two buildings (Warehouse 1 and Warehouse 2) under the same application A, so both are in scope. Warehouse 1 has a roof age of 24 years, which is greater than 20 years. Warehouse 2 has a roof age of 29 years, which is also greater than 20 years. Both buildings meet the condition. There are no explicit exceptions mentioned in the rule text. There are no conflicting observations regarding the roof ages of the buildings. Both warehouses have clearly stated roof ages that satisfy the condition.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 16.0. Error: `None`.

### case_scoped / property_b_missing

The criterion states that a building with a roof older than 20 years is a concern. However, the evidence shows that the roof age for Warehouse 1 is null and explicitly noted as 'Roof age has not been supplied.' Since there is no information indicating the roof age, it cannot be determined whether the roof is older than 20 years. Therefore, the condition cannot be evaluated based on the provided evidence.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 8; extraction calls: 1; assessment call attempts: 5; seconds: 14.5. Error: `None`.

### case_scoped / property_b_followup

The rule applies separately to each insured building. The subject is 'Warehouse 1' under 'Maple Logistics' application B. The roof age for Warehouse 1 was initially reported as null ('Roof age has not been supplied'). However, a follow-up document (E6-E10) provides a verified roof age of 5 years. Since 5 years is not greater than 20 years, the condition that the roof is older than 20 years is false. There are no explicit exception prerequisites mentioned in the rule text for C1. There is no actual incompatible observation. The initial null roof age was corrected to 5 years, which does not meet the condition of being older than 20 years.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 9; extraction calls: 1; assessment call attempts: 6; seconds: 18.5. Error: `None`.

### case_scoped / cyber_c

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 5.1. Error: `{'type': 'ValueError', 'message': 'Line review must link to an extracted rule covering that source line'}`.

### case_scoped / cyber_d_missing

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 6.6. Error: `{'type': 'ValueError', 'message': 'Line review must link to an extracted rule covering that source line'}`.

### case_scoped / cyber_d_followup

No assessment of the expected criterion.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 4; extraction calls: 2; assessment call attempts: 0; seconds: 6.4. Error: `{'type': 'ValueError', 'message': 'Line review must link to an extracted rule covering that source line'}`.

### case_scoped / unlabelled_criterion

The rule applies to each insured building individually, as stated in the context: 'Apply this rule separately to each insured building.' The evidence includes information about one main building. The evidence shows that the main building has a roof age of 25 years. Since 25 years is greater than 20 years, the condition 'roof older than 20 years' is true. The supporting fact is E2: 'Main building: roof age is 25 years.' There are no explicit exceptions mentioned in the rule text for C1. Therefore, the exception does not apply. There are no conflicting observations in the provided evidence that would create an unresolved contradiction regarding the roof age of the building. Both pieces of evidence refer to the same building and support the same conclusion about the roof age.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + extraction + assessment): 7; extraction calls: 1; assessment call attempts: 4; seconds: 15.1. Error: `None`.

## Scoring and limitations

Strict passes require collection, exact criterion/classification extraction, all gold supporting spans, source/locator integrity, no foreign inputs, correct status and atomic findings, expected readiness, and complete assessment coverage. Findings are matched one-to-one on required raw supporting spans; additional same-case citations are allowed. Empty/missing criteria cannot pass as a correct abstention. Unsafe ready means the pipeline marked a result ready despite a collection, extraction, isolation, status, or finding failure.

The unlabelled guideline is intentionally ordinary prose without bracketed classification. Failure counts against end-to-end performance; the fixture is not normalized. Hardened runs opt into structured exact-quote criterion extraction, while evidence extraction stays deterministic. Same-case follow-up support includes an earlier document. Isolation is checked at the assessment input boundary; an agent's free-text answer can still reflect retained history and is not semantically scored. Replayed tools and model outputs are retained in JSON. These seven turn fixtures are not independent production samples.
