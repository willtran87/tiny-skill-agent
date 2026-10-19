# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T00:33:38.533858+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **3/4** (planned: 4).
- Correct case statuses: **3/4**.
- Required gold evidence cited: **3/3**.
- Reference/provenance checks: **8/8**.
- False-positive findings in the 4 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| missing_inspection_records | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| explicit_activity_did_not_occur | no_match | insufficient_evidence | 0 / 0 | 1 / 1 | FAIL |
| explicit_documentation_requirement | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| measured_below_threshold | no_match | no_match | 0 / 0 | 1 / 1 | PASS |

## Reasons and diagnostics

### missing_inspection_records

**Expected:** Missing records do not establish that inspections did not occur. This criterion evaluates inspection activity, not submission of records.

**Model:** The criterion requires that every elevator received its annual safety inspection during 2025. However, the only evidence provided (E1) states that no elevator inspection records were supplied with the application and that whether inspections occurred is not known. Since there is no information confirming that inspections took place, and the absence of records does not prove that inspections did not occur, the condition cannot be evaluated as true or false based on the available evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 9.2s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that every elevator received its annual safety inspection during 2025. However, the only evidence provided (E1) states that no elevator inspection records were supplied with the application and that whether inspections occurred is not known. Since there is no information confirming that inspections took place, and the absence of records does not prove that inspections did not occur, the condition cannot be evaluated as true or false based on the available evidence.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The quoted trigger requires that every elevator received its annual safety inspection during 2025. The evidence E1 states 'No elevator inspection records were supplied with the application. Whether inspections occurred is not known.' This directly refutes the condition by indicating that there is no information confirming whether inspections occurred. Since there is no confirmation of inspections and no evidence to prove they took place, the condition cannot be established as true. The lack of evidence does not confirm the absence of inspections, but it also does not confirm their presence. Therefore, given the available information, the condition is false. There are no explicit exception prerequisites mentioned in the rule text for C1.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### explicit_activity_did_not_occur

**Expected:** An explicit statement that the activity did not occur disproves the all-elevators condition, unlike absent records.

**Model:** The rule concerns elevator safety inspections during the year 2025. The evidence E1 mentions Elevator A and states it did not receive an inspection during 2025. Facts that PROVE the quoted trigger: None directly prove the trigger because the rule requires ALL elevators to have received inspections, but only one elevator's status is mentioned. Facts that REFUTE it: E1 states that Elevator A did not receive a safety inspection at any time during 2025, which contradicts the requirement for annual inspection. Given unknown information about other elevators, the condition could still be true if all other elevators received inspections, but since we know at least one elevator failed to meet the requirement, the overall condition is false. Therefore, condition=true is not met; condition=false. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which the annual safety inspection requirement might be waived or altered. There is an actual incompatible observation: E1 states that Elevator A did not receive a safety inspection during 2025, which directly contradicts the requirement in the rule that every elevator must receive its annual safety inspection during 2025. This creates a conflict between the evidence and the rule's trigger.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 3; elapsed: 8.0s.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. Facts that PROVE the quoted trigger: None directly prove the trigger because the rule requires ALL elevators to have received inspections, but only one elevator's status is mentioned. Facts that REFUTE it: E1 states that Elevator A did not receive a safety inspection at any time during 2025, which contradicts the requirement for annual inspection. Given unknown information about other elevators, the condition could still be true if all other elevators received inspections, but since we know at least one elevator failed to meet the requirement, the overall condition is false. Therefore, condition=true is not met; condition=false. There are no explicit exception prerequisites mentioned in the rule text for C1. The rule does not specify any conditions under which the annual safety inspection requirement might be waived or altered.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### explicit_documentation_requirement

**Expected:** The criterion explicitly evaluates document submission. Confirmed absence of submitted certificates disproves that condition without implying that inspections did not occur.

**Model:** The subject is elevator inspection certificates and the period is the application submission. The evidence (E1) states that 'The application administrator confirms that no elevator inspection certificates were supplied with the application.' This directly proves that inspection certificates for elevators were not supplied with the application. There are no facts that refute this statement. Given this conclusive evidence, the condition is false. The rule does not specify any exceptions that would apply to this situation. There are no conflicting observations in the evidence that would create an unresolved conflict regarding whether elevator inspection certificates were supplied with the application.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 1; captured call errors: 0; model calls: 4; elapsed: 7.6s.

**Negative-evidence review (C1):** `supported`. The criterion requires that inspection certificates for all elevators be supplied with the application. Evidence E1 explicitly states that 'no elevator inspection certificates were supplied with the application.' This directly supports a negative decision as it establishes that the documentation requirement was not met.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence (E1) states that 'The application administrator confirms that no elevator inspection certificates were supplied with the application.' This directly proves that inspection certificates for elevators were not supplied with the application. There are no facts that refute this statement. Given this conclusive evidence, the condition is false. The rule does not specify any exceptions that would apply to this situation.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### measured_below_threshold

**Expected:** The supplied age for the correct building and date is below the threshold, directly disproving the concern condition.

**Model:** The subject is Building A's roof, and the period in scope is as of 2025-07-01. The evidence states that 'Building A's roof is 5 years old as of 2025-07-01.' This directly contradicts the trigger condition which requires the roof to be more than 20 years old. Since 5 years is not more than 20 years, the condition is false. There are no explicit exception prerequisites mentioned in the rule. There is no conflicting evidence. The single piece of evidence directly contradicts the trigger condition, establishing that the roof is not more than 20 years old.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 9.0s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining if Building A's roof is more than 20 years old as of 2025-07-01. Evidence E1 explicitly states that the roof is 5 years old as of 2025-07-01, which is significantly less than the 20-year threshold. This decisive observation directly contradicts the condition in the criterion.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that 'Building A's roof is 5 years old as of 2025-07-01.' This directly contradicts the trigger condition which requires the roof to be more than 20 years old. Since 5 years is not more than 20 years, the condition is false. There are no explicit exception prerequisites mentioned in the rule.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
