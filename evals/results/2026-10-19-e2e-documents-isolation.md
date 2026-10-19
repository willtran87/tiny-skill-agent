# End-to-end document and case-isolation evaluation

State: **failed**. Model: `qwen3-coder:30b`.

Live ReAct agent, raw text/Markdown/JSON documents, registered tool provenance, production extraction and completion assessment. Two profiles use separate checkpointed conversations with the same turn order. Gold is excluded from model inputs. Synthetic, short, non-expert-labeled cases; no OCR, PDF layout, or semantic explanation judging.

| Profile | Turns | Strict passes | Collected | Criteria extracted | Gold spans extracted | Isolated inputs | Correct statuses | Correct findings | Ready | Unsafe ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retained_history | 2 | 0 | 2 | 2 | 3/3 | 1 | 1 | 1 | 0 | 0 |
| case_scoped | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 |

`retained_history` is the unmodified default extractor. `case_scoped` is an evaluation integration example selecting tool results by application-owned document IDs. It does not change production extraction or assessment, and the agent still sees prior conversation history.

| Profile | Turn | Expected → actual | Findings actual/expected | Isolated | Ready | Strict |
| --- | --- | --- | --- | --- | --- | --- |
| retained_history | property_a | matched → matched | 2/2 | True | False | FAIL |
| retained_history | property_b_missing | insufficient_evidence → matched | 2/0 | False | False | FAIL |

## Diagnostics

### retained_history / property_a

The rule applies separately to each insured building. The evidence contains information about two buildings (Warehouse 1 and Warehouse 2) within the same application A, so both are in scope. Facts proving: Warehouse 1 roof age is 24 years (E1); Warehouse 2 roof age is 29 years (E3). Facts refuting: None. Given unknown information, it's possible that other buildings may have roof ages <= 20 years, but this does not affect the existing evidence. Condition is true because both buildings exceed the 20-year threshold. No explicit exceptions mentioned in the rule text. The rule does not specify any conditions under which this concern would not apply. There are no conflicting observations regarding the roof ages of Warehouse 1 or Warehouse 2. All evidence consistently reports the roof ages as 24 and 29 years respectively, which are both greater than 20 years.

Foreign input sources: `[]`. Foreign cited sources: `[]`.

LLM responses (agent + assessment): 5; assessment call attempts: 3; seconds: 39.7. Error: `None`.

### retained_history / property_b_missing

The rule applies to each insured building. The subject is the roof age of individual buildings. The period in scope is the current application as per the guideline. Facts proving: E1 and E2 show that Warehouse 1 has a roof age of 24 years, and E3 shows that Warehouse 2 has a roof age of 29 years. Both exceed 20 years. Facts refuting: None directly refute the trigger; all buildings mentioned have roof ages exceeding 20 years. Given unknown information: Since no other buildings are mentioned in the evidence for application A, we cannot determine if there are additional buildings with roof ages ≤ 20 years. However, the existing evidence supports that at least two buildings (Warehouse 1 and Warehouse 2) meet the condition. Therefore, condition = true. There are no explicit exception prerequisites mentioned in the rule text for C1. The guideline does not list any exceptions to this concern. Exception = does_not_apply. There are no actual incompatible observations in the evidence provided. All evidence points to roof ages exceeding 20 years for the buildings mentioned, which aligns with the trigger condition. Conflict = none.

Foreign input sources: `['doc:property-a.md']`. Foreign cited sources: `['doc:property-a.md']`.

LLM responses (agent + assessment): 6; assessment call attempts: 4; seconds: 15.8. Error: `None`.

## Scoring and limitations

Strict passes require collection, exact criterion/classification extraction, all gold supporting spans, source/locator integrity, no foreign inputs, correct status and atomic findings, expected readiness, and complete assessment coverage. Findings are matched one-to-one on required raw supporting spans; additional same-case citations are allowed. Empty/missing criteria cannot pass as a correct abstention. Unsafe ready means the pipeline marked a result ready despite a collection, extraction, isolation, status, or finding failure.

The unlabelled guideline is intentionally ordinary prose without the current extractor's bracketed classification convention. Failure counts against end-to-end performance; it is not silently normalized. Same-case follow-up support includes an earlier document. This tests the existing deterministic text/JSON extractor, not a new LLM parser. Isolation is checked at the assessment input boundary; an agent's free-text answer can still reflect retained history and is not semantically scored. Replayed tools and all model outputs are retained in JSON. These seven turn fixtures are not independent production samples.
