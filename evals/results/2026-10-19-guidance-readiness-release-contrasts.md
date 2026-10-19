# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T07:09:09.939021+00:00. State: **completed**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **4/4** (planned: 4).
- Correct case statuses: **4/4**.
- Required gold evidence cited: **3/3**.
- Reference/provenance checks: **8/8**.
- False-positive findings in the 4 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| missing_inspection_records | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| explicit_activity_did_not_occur | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| explicit_documentation_requirement | no_match | no_match | 0 / 0 | 1 / 1 | PASS |
| measured_below_threshold | no_match | no_match | 0 / 0 | 1 / 1 | PASS |

## Reasons and diagnostics

### missing_inspection_records

**Expected:** Missing records do not establish that inspections did not occur. This criterion evaluates inspection activity, not submission of records.

**Model:** The rule applies to elevators and requires annual safety inspections during 2025. The subject is elevators, and the period in scope is 2025. The evidence (E1) states that 'No elevator inspection records were supplied with the application. Whether inspections occurred is not known.' This means there is no supporting evidence that inspections occurred during 2025, and no refuting evidence either. The lack of records does not confirm absence of inspections, but it also does not confirm their occurrence. Therefore, based on the available information, it cannot be determined whether every elevator received its annual safety inspection during 2025. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations regarding elevator inspections in the provided evidence. The only observation (E1) indicates a lack of inspection records, which does not constitute a contradiction but rather an absence of information.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 4; elapsed: 9.7s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence (E1) states that 'No elevator inspection records were supplied with the application. Whether inspections occurred is not known.' This means there is no supporting evidence that inspections occurred during 2025, and no refuting evidence either. The lack of records does not confirm absence of inspections, but it also does not confirm their occurrence. Therefore, based on the available information, it cannot be determined whether every elevator received its annual safety inspection during 2025. There are no explicit exception prerequisites mentioned in the rule text for C1.

### explicit_activity_did_not_occur

**Expected:** An explicit statement that the activity did not occur disproves the all-elevators condition, unlike absent records.

**Model:** The rule applies to all elevators in the building and requires that each received an inspection during 2025. The subject is Elevator A, which is within the scope of the policy. The evidence states that 'Elevator A did not receive a safety inspection at any time during 2025.' This directly contradicts the requirement that every elevator received its annual safety inspection during 2025. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule for C1. The rule does not specify any conditions under which an elevator might be exempt from the annual safety inspection requirement. There is no conflicting evidence provided that would create an unresolved contradiction with the stated fact about Elevator A. The only observation directly contradicts the condition, but does not introduce a conflict requiring resolution.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 10.9s.

**Negative-evidence review (C1):** `supported`. The criterion requires that every elevator received its annual safety inspection during 2025. Evidence E1 directly states that Elevator A did not receive a safety inspection at any time during 2025, which contradicts the condition of the criterion. This is a decisive observation that establishes the criterion's condition as false.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that 'Elevator A did not receive a safety inspection at any time during 2025.' This directly contradicts the requirement that every elevator received its annual safety inspection during 2025. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule for C1. The rule does not specify any conditions under which an elevator might be exempt from the annual safety inspection requirement.

### explicit_documentation_requirement

**Expected:** The criterion explicitly evaluates document submission. Confirmed absence of submitted certificates disproves that condition without implying that inspections did not occur.

**Model:** The subject is the application and the period is the time of application submission. The evidence batch covers the application submission period. The evidence E1 states that 'The application administrator confirms that no elevator inspection certificates were supplied with the application.' This directly supports the trigger condition that certificates were not supplied, making the condition false. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations regarding the submission of elevator inspection certificates in the provided evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 9.7s.

**Negative-evidence review (C1):** `supported`. The criterion requires that inspection certificates for all elevators be supplied with the application. Evidence E1 directly states that 'no elevator inspection certificates were supplied with the application.' This explicit statement supports a negative decision that the criterion is not met.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence E1 states that 'The application administrator confirms that no elevator inspection certificates were supplied with the application.' This directly supports the trigger condition that certificates were not supplied, making the condition false. There are no explicit exception prerequisites mentioned in the rule text for C1.

### measured_below_threshold

**Expected:** The supplied age for the correct building and date is below the threshold, directly disproving the concern condition.

**Model:** The rule applies to Building A's roof, and the evidence provides information about the age of Building A's roof as of 2025-07-01. The evidence states that 'Building A's roof is 5 years old as of 2025-07-01.' Since 5 years is not more than 20 years, the condition is false. The rule requires the roof to be more than 20 years old to flag a concern, which is not met. There are no explicit exception prerequisites mentioned in the rule. There are no conflicting observations regarding the age of Building A's roof as of 2025-07-01.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 11.4s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining if Building A's roof is more than 20 years old as of 2025-07-01. Evidence E1 explicitly states that the roof is 5 years old as of that date. Since 5 years is not more than 20 years, the condition of the criterion is false.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that 'Building A's roof is 5 years old as of 2025-07-01.' Since 5 years is not more than 20 years, the condition is false. The rule requires the roof to be more than 20 years old to flag a concern, which is not met. There are no explicit exception prerequisites mentioned in the rule.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
