# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-18T23:33:25.291725+00:00. State: **completed**.

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

**Model:** The evidence indicates that no elevator inspection records were provided with the application, making it impossible to determine whether annual safety inspections occurred during 2025 for any elevator. Since there is insufficient information to confirm compliance with the criterion, the condition cannot be evaluated.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 2; elapsed: 2.2s.

### explicit_activity_did_not_occur

**Expected:** An explicit statement that the activity did not occur disproves the all-elevators condition, unlike absent records.

**Model:** The criterion requires that every elevator received its annual safety inspection during 2025. However, the evidence shows that Elevator A did not receive a safety inspection at any time during 2025. Since the condition is not met for all elevators, the strength cannot be recorded.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 3.4s.

**Negative-evidence review (C1):** `supported`. The criterion requires that every elevator received its annual safety inspection during 2025. Evidence E1 explicitly states that Elevator A did not receive a safety inspection at any time during 2025, which directly contradicts the condition of the criterion. This decisive observation establishes that the criterion's condition is false.

### explicit_documentation_requirement

**Expected:** The criterion explicitly evaluates document submission. Confirmed absence of submitted certificates disproves that condition without implying that inspections did not occur.

**Model:** The criterion requires that inspection certificates for all elevators be supplied with the application to record a strength. However, the evidence shows that the application administrator confirms no elevator inspection certificates were supplied with the application. This directly contradicts the condition necessary for satisfying the criterion.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 3.4s.

**Negative-evidence review (C1):** `supported`. The criterion requires that inspection certificates for all elevators be supplied with the application. Evidence E1 explicitly states that 'no elevator inspection certificates were supplied with the application.' This directly supports a negative decision as it establishes that the documentation requirement was not met.

### measured_below_threshold

**Expected:** The supplied age for the correct building and date is below the threshold, directly disproving the concern condition.

**Model:** The assessment concludes that Building A's roof is not more than 20 years old as of 2025-07-01, since the evidence indicates it is only 5 years old. This means the condition for flagging a concern is not met.

Coverage complete: `True`; decision ready: `True`; source/case disagreements: 0; captured call errors: 0; model calls: 3; elapsed: 3.5s.

**Negative-evidence review (C1):** `supported`. The criterion requires determining if Building A's roof is more than 20 years old as of 2025-07-01. Evidence E1 explicitly states that the roof is 5 years old as of 2025-07-01, which is significantly less than the 20-year threshold. This decisive observation directly contradicts the condition in the criterion.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, and complete coverage. Atomic records are checked against exact gold citation sets in these small fixtures. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
