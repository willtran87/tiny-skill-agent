# Synthetic assessment evaluation

Model: `qwen3-coder:30b`. Started: 2026-10-19T07:26:11.568301+00:00. State: **running**.

Hand-authored synthetic cases, not expert-validated. This tests the assessment API with supplied criteria/evidence, excluding tool gathering and source extraction. Gold labels are never sent to the model.

- Strict fixture passes: **4/4** (planned: 32).
- Correct case statuses: **4/4**.
- Required gold evidence cited: **0/0**.
- Reference/provenance checks: **16/16**.
- False-positive findings in the 4 nonmatched gold cases: **0**.

| Case | Expected status | Actual status | Findings actual / expected | Required evidence | Strict result |
| --- | --- | --- | --- | --- | --- |
| cyber_remote_access_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| property_pump_service_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| auto_driver_screening_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |
| gl_subcontract_limit_unknown | insufficient_evidence | insufficient_evidence | 0 / 0 | 0 / 0 | PASS |

## Reasons and diagnostics

### cyber_remote_access_unknown

**Expected:** Administrator MFA does not establish workforce MFA; blank or unavailable records do not prove absence of the control.

**Model:** The subject is 'remote workforce login' to Harbor Analytics. The period in scope is 'as of 2025-09-01'. The evidence indicates that MFA is enabled for all four cloud administrators (E1), but there is no information about ordinary workforce remote access or VPN authentication. The questionnaire does not specify whether the workforce uses VPN or remote desktop, and the broker's email states that a VPN configuration report was not available (E2). Since there is insufficient evidence to confirm that MFA protects ALL remote workforce logins, the condition cannot be confirmed as true. However, it also cannot be definitively proven false due to missing data about ordinary workforce access. Therefore, the truth of the trigger is unknown. There are no explicit exception prerequisites mentioned in the rule that would apply here. There is no actual incompatible observation. The lack of information about workforce remote access does not create a contradiction with the presence of MFA for administrators.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 2; captured call errors: 0; model calls: 5; elapsed: 28.1s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence indicates that MFA is enabled for all four cloud administrators (E1), but there is no information about ordinary workforce remote access or VPN authentication. The questionnaire does not specify whether the workforce uses VPN or remote desktop, and the broker's email states that a VPN configuration report was not available (E2). Since there is insufficient evidence to confirm that MFA protects ALL remote workforce logins, the condition cannot be confirmed as true. However, it also cannot be definitively proven false due to missing data about ordinary workforce access. Therefore, the truth of the trigger is unknown. There are no explicit exception prerequisites mentioned in the rule that would apply here.

### property_pump_service_unknown

**Expected:** Unlocated records and a visual inspection cannot establish a missed service visit.

**Model:** Subject is the fire pump at Cedar Components; period in scope is calendar 2025 The evidence does not contain any record of fire pump servicing occurring in 2025. E1 states that the maintenance binder was held off site and unavailable, which implies no accessible service records. E2 indicates that the pump contractor's 2025 service invoice cannot be located, and there is no confirmation of whether the visit took place. There are no positive assertions confirming that servicing occurred in 2025. Therefore, it cannot be established that the fire pump was serviced during calendar 2025. There are no explicit exception prerequisites mentioned in the rule that would apply to this case. There are no contradictory observations regarding the fire pump's servicing status in 2025. The lack of service records does not constitute a contradiction but rather an absence of evidence supporting the servicing occurred.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 5; elapsed: 13.2s.

**Independent review (C1):** scope `in_scope`, condition `unknown`, exception `does_not_apply`. The evidence does not contain any record of fire pump servicing occurring in 2025. E1 states that the maintenance binder was held off site and unavailable, which implies no accessible service records. E2 indicates that the pump contractor's 2025 service invoice cannot be located, and there is no confirmation of whether the visit took place. There are no positive assertions confirming that servicing occurred in 2025. Therefore, it cannot be established that the fire pump was serviced during calendar 2025. There are no explicit exception prerequisites mentioned in the rule that would apply to this case.

### auto_driver_screening_unknown

**Expected:** Neither the interview process nor missing files establishes whether all MVR reviews occurred.

**Model:** The criterion requires that motor vehicle records be reviewed for every employed driver before hire. While E1 indicates that hiring includes an interview and a route test, it does not confirm whether MVR reviews were conducted. E2 states that driver files have not been provided and there is no confirmation or denial of pre-hire MVR reviews. Since there is no evidence confirming that MVR reviews were performed for all employed drivers before hire, and the absence of documentation does not prove the activity did not occur, the condition cannot be confirmed as true.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 6; elapsed: 12.9s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that motor vehicle records be reviewed for every employed driver before hire. While E1 indicates that hiring includes an interview and a route test, it does not confirm whether MVR reviews were conducted. E2 states that driver files have not been provided and there is no confirmation or denial of pre-hire MVR reviews. Since there is no evidence confirming that MVR reviews were performed for all employed drivers before hire, and the absence of documentation does not prove the activity did not occur, the condition cannot be confirmed as true.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

### gl_subcontract_limit_unknown

**Expected:** Unspecified insurance limits cannot satisfy or disprove the $2 million requirement.

**Model:** The criterion requires that every active roofing subcontractor maintains at least $2 million of general liability limits. While the evidence shows that both subcontractors are marked as insured in the vendor register (E1), it does not provide information about their actual liability limits. Additionally, certificates requesting the limits have not been received (E2). Since there is no confirmation of the specific liability limits for either subcontractor, and the absence of this information prevents determining whether the condition is met, the decision cannot be definitively negative based on the provided evidence.

Coverage complete: `True`; decision ready: `False`; source/case disagreements: 0; captured call errors: 0; model calls: 6; elapsed: 14.8s.

**Negative-evidence review (C1):** `missing_evidence`. The criterion requires that every active roofing subcontractor maintains at least $2 million of general liability limits. While the evidence shows that both subcontractors are marked as insured in the vendor register (E1), it does not provide information about their actual liability limits. Additionally, certificates requesting the limits have not been received (E2). Since there is no confirmation of the specific liability limits for either subcontractor, and the absence of this information prevents determining whether the condition is met, the decision cannot be definitively negative based on the provided evidence.

**Readiness blocked:** initial case and independent review disagree on status or finding citation groups.

## Interpretation limits

Strict pass requires the expected status, required citations, separate gold finding records, valid references, complete coverage, and expected readiness when labeled. Atomic records are matched one-to-one against exact gold citation sets or predeclared acceptable alternatives. Required-evidence coverage alone does not establish that each independent finding was reported.

Reference integrity proves that accepted citations resolve to supplied content; it does not establish truth or semantic support. Reasons are preserved for human review and are not scored by an LLM judge. The runtime can reject invalid attempts and recover; inspect the JSON call trace and coverage errors for those attempts.

This is one run on short synthetic cases. It estimates neither production recall nor robustness on long, noisy inputs. Decision readiness is the API's own flag, not a benchmark correctness score. The evaluation runner does not alter production prompts or API behavior.
