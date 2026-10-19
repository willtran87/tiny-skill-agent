# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T05:30:03.179909+00:00. State: **completed**.

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

**Model:** The criterion requires that every elevator received its annual safety inspection during 2025. However, no elevator inspection records were supplied with the application, and it is not known whether inspections occurred. Since there is missing evidence regarding the occurrence of inspections, the condition cannot be determined to be true or false based on the available information.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 1; model calls: 6; elapsed: 13.4s.

**Rejected responses:** Scope/exception quotations must occur in the original criterion

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that every elevator received its annual safety inspection during 2025. However, no elevator inspection records were supplied with the application, and it is not known whether inspections occurred. Since there is missing evidence regarding the occurrence of inspections, the condition cannot be determined to be true or false based on the available information.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### explicit_activity_did_not_occur

**Expected:** An explicit statement that the activity did not occur disproves the all-elevators condition, unlike absent records.

**Model:** The rule applies to all elevators in the building for the year 2025. The evidence mentions Elevator A specifically, but does not indicate whether other elevators were inspected. The trigger requires that every elevator received its annual safety inspection during 2025. Evidence E1 states that 'Elevator A did not receive a safety inspection at any time during 2025.' This directly contradicts the requirement for all elevators to be inspected. Since there is at least one elevator (Elevator A) that was not inspected, the condition is false. There are no explicit exceptions mentioned in the rule text that would apply to this situation. There is a direct contradiction between the requirement that all elevators be inspected and the fact that Elevator A was not inspected. No other evidence contradicts this observation.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 12.3s.

**Negative-evidence review (C1):** `supported`. The criterion requires that every elevator received its annual safety inspection during 2025. Evidence E1 explicitly states that Elevator A did not receive a safety inspection at any time during 2025, which directly contradicts the condition of the criterion. This decisive observation establishes that the criterion's condition is false.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The trigger requires that every elevator received its annual safety inspection during 2025. Evidence E1 states that 'Elevator A did not receive a safety inspection at any time during 2025.' This directly contradicts the requirement for all elevators to be inspected. Since there is at least one elevator (Elevator A) that was not inspected, the condition is false. There are no explicit exceptions mentioned in the rule text that would apply to this situation.

### explicit_documentation_requirement

**Expected:** The criterion explicitly evaluates document submission. Confirmed absence of submitted certificates disproves that condition without implying that inspections did not occur.

**Model:** The subject is the submission of elevator inspection certificates with the application. The period in scope is the time of application submission. The evidence E1 states that 'The application administrator confirms that no elevator inspection certificates were supplied with the application.' This directly supports the trigger condition by confirming that inspection certificates were not provided, which means the strength is not recorded. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule text for C1. There are no conflicting observations in the evidence provided that would create an unresolved conflict regarding the submission of elevator inspection certificates.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 1; model calls: 6; elapsed: 11.8s.

**Rejected responses:** Scope/exception quotations must occur in the original criterion

**Negative-evidence review (C1):** `supported`. The criterion requires that inspection certificates for all elevators be supplied with the application. Evidence E1 explicitly states that 'no elevator inspection certificates were supplied with the application.' This directly supports a negative decision as it establishes that the documentation requirement was not met.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence E1 states that 'The application administrator confirms that no elevator inspection certificates were supplied with the application.' This directly supports the trigger condition by confirming that inspection certificates were not provided, which means the strength is not recorded. Therefore, the condition is false. There are no explicit exception prerequisites mentioned in the rule text for C1.

### measured_below_threshold

**Expected:** The supplied age for the correct building and date is below the threshold, directly disproving the concern condition.

**Model:** The subject is Building A, and the period in scope is as of 2025-07-01. The evidence states that 'Building A's roof is 5 years old as of 2025-07-01.' Since 5 years is not more than 20 years, the condition is false. The supporting fact directly contradicts the trigger. The rule does not specify any exceptions. There are no conflicting observations regarding Building A's roof age as of 2025-07-01. The single piece of evidence clearly states the roof is 5 years old, which does not meet the condition of being more than 20 years old.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 11.7s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining if Building A's roof is more than 20 years old as of 2025-07-01. Evidence E1 explicitly states that the roof is 5 years old as of that date. Since 5 years is not more than 20 years, the condition is false.

**Independent review (C1):** scope `in_scope`, condition `false`, exception `does_not_apply`. The evidence states that 'Building A's roof is 5 years old as of 2025-07-01.' Since 5 years is not more than 20 years, the condition is false. The supporting fact directly contradicts the trigger. The rule does not specify any exceptions.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
