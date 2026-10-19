# Repeated evaluation of newly authored underwriting cases

Model: `qwen3-coder:30b`. **3/3 completed runs**, 32 unique synthetic cases per run.

Same temperature (0), seed (42), case order, model, and implementation each run. No production changes were made between runs. This measures repeatability at the configured settings, not robustness across temperatures, seeds, or models. Cases are synthetic and not underwriter-validated. They were frozen before the first model run.

| Run | Strict pass | Correct status | Correct readiness | False-positive findings | Ready despite expected abstention | Calls | Seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 17/32 | 20/32 | 24/32 | 2 | 1 | 120 | 230.4 |
| 2 | 16/32 | 19/32 | 24/32 | 2 | 1 | 121 | 215.7 |
| 3 | 16/32 | 19/32 | 24/32 | 2 | 1 | 121 | 224.6 |

## Consistency

- Same final status in all completed runs: **31/32**.
- Same status, finding citation groups, and readiness in all runs: **31/32**.
- Passed every completed run: **16/32**.
- Consistently wrong final status: **12/32**.

Agreement excludes explanation wording, subject-label wording, citation order, and generated finding IDs. Consistency is not correctness. Repeated judgments on the same cases are not independent samples of real-world accuracy.

## Category results

| Category | Strict passes / case-runs | Correct status / case-runs |
| --- | --- | --- |
| cross_source_synthesis | 0/12 | 3/12 |
| documentation_vs_activity | 9/12 | 9/12 |
| entity_and_period_alignment | 6/12 | 6/12 |
| exceptions_and_scope | 3/12 | 3/12 |
| missing_information | 10/12 | 10/12 |
| multiple_and_corroborated_findings | 9/12 | 9/12 |
| quantitative_boundaries | 9/12 | 9/12 |
| temporal_and_corrections | 0/6 | 3/6 |
| unresolved_conflict | 3/6 | 6/6 |

## Per-case outcomes

| Case | Expected | Actual status by run | Strict passes | Readiness by run | Decision agreement |
| --- | --- | --- | --- | --- | --- |
| cyber_remote_access_unknown | insufficient_evidence | insufficient_evidence, missing, missing | 1/3 | False, False, False | False |
| property_pump_service_unknown | insufficient_evidence | insufficient_evidence, insufficient_evidence, insufficient_evidence | 3/3 | False, False, False | True |
| auto_driver_screening_unknown | insufficient_evidence | insufficient_evidence, insufficient_evidence, insufficient_evidence | 3/3 | False, False, False | True |
| gl_subcontract_limit_unknown | insufficient_evidence | insufficient_evidence, insufficient_evidence, insufficient_evidence | 3/3 | False, False, False | True |
| auto_incident_rate_calculation | matched | insufficient_evidence, insufficient_evidence, insufficient_evidence | 0/3 | False, False, False | True |
| property_reserves_exact_threshold | matched | matched, matched, matched | 3/3 | True, True, True | True |
| property_roof_exact_boundary | no_match | no_match, no_match, no_match | 3/3 | True, True, True | True |
| cyber_patch_coverage_boundary | matched | matched, matched, matched | 3/3 | True, True, True | True |
| property_alarm_equal_reports | insufficient_evidence | insufficient_evidence, insufficient_evidence, insufficient_evidence | 0/3 | False, False, False | True |
| cyber_backup_immutability_conflict | insufficient_evidence | insufficient_evidence, insufficient_evidence, insufficient_evidence | 3/3 | False, False, False | True |
| auto_mileage_corrected_denominator | no_match | matched, matched, matched | 0/3 | True, True, True | True |
| property_later_repair_does_not_rewrite_history | matched | matched, matched, matched | 0/3 | True, True, True | True |
| property_electrical_exception | no_match | matched, matched, matched | 0/3 | True, True, True | True |
| cyber_service_account_exception | no_match | missing, missing, missing | 0/3 | False, False, False | True |
| gl_hot_work_scope_exclusion | not_applicable | insufficient_evidence, insufficient_evidence, insufficient_evidence | 0/3 | False, False, False | True |
| auto_passenger_scope_exclusion | not_applicable | not_applicable, not_applicable, not_applicable | 3/3 | True, True, True | True |
| property_multiple_warehouse_concerns | matched | matched, matched, matched | 3/3 | True, True, True | True |
| auto_multiple_expired_licences | matched | missing, missing, missing | 0/3 | False, False, False | True |
| cyber_multiple_restore_strengths | matched | matched, matched, matched | 3/3 | True, True, True | True |
| property_corroboration_not_two_events | matched | matched, matched, matched | 3/3 | True, True, True | True |
| gl_sister_company_evidence | insufficient_evidence | insufficient_evidence, insufficient_evidence, insufficient_evidence | 3/3 | False, False, False | True |
| cyber_prior_year_does_not_prove_current | insufficient_evidence | insufficient_evidence, insufficient_evidence, insufficient_evidence | 3/3 | False, False, False | True |
| property_building_specific_scope | not_applicable | no_match, no_match, no_match | 0/3 | True, True, True | True |
| wc_partial_payroll_period | insufficient_evidence | not_applicable, not_applicable, not_applicable | 0/3 | True, True, True | True |
| gl_document_submission_condition | no_match | no_match, no_match, no_match | 3/3 | True, True, True | True |
| wc_document_absence_is_concern | matched | no_match, no_match, no_match | 0/3 | True, True, True | True |
| wc_activity_explicitly_not_performed | no_match | no_match, no_match, no_match | 3/3 | True, True, True | True |
| property_inspection_date_unknown | insufficient_evidence | insufficient_evidence, insufficient_evidence, insufficient_evidence | 3/3 | False, False, False | True |
| property_cross_source_alarm_and_value | matched | no_match, no_match, no_match | 0/3 | False, False, False | True |
| gl_loss_aggregation_without_duplicate | matched | matched, matched, matched | 0/3 | False, False, False | True |
| cyber_restore_duration_cross_midnight | no_match | insufficient_evidence, insufficient_evidence, insufficient_evidence | 0/3 | False, False, False | True |
| property_expired_exception_certificate | matched | no_match, no_match, no_match | 0/3 | True, True, True | True |

## Failure diagnostics

- **cyber_remote_access_unknown**: run 2: status_correct, required_evidence_covered, coverage_complete; run 3: status_correct, required_evidence_covered, coverage_complete.
- **auto_incident_rate_calculation**: run 1: status_correct, atomic_findings_correct, coverage_complete, readiness_correct; run 2: status_correct, atomic_findings_correct, coverage_complete, readiness_correct; run 3: status_correct, atomic_findings_correct, coverage_complete, readiness_correct.
- **property_alarm_equal_reports**: run 1: coverage_complete; run 2: coverage_complete; run 3: coverage_complete.
- **auto_mileage_corrected_denominator**: run 1: status_correct, atomic_findings_correct; run 2: status_correct, atomic_findings_correct; run 3: status_correct, atomic_findings_correct.
- **property_later_repair_does_not_rewrite_history**: run 1: atomic_findings_correct; run 2: atomic_findings_correct; run 3: atomic_findings_correct.
- **property_electrical_exception**: run 1: status_correct, atomic_findings_correct; run 2: status_correct, atomic_findings_correct; run 3: status_correct, atomic_findings_correct.
- **cyber_service_account_exception**: run 1: status_correct, required_evidence_covered, coverage_complete, readiness_correct; run 2: status_correct, required_evidence_covered, coverage_complete, readiness_correct; run 3: status_correct, required_evidence_covered, coverage_complete, readiness_correct.
- **gl_hot_work_scope_exclusion**: run 1: status_correct, readiness_correct; run 2: status_correct, readiness_correct; run 3: status_correct, readiness_correct.
- **auto_multiple_expired_licences**: run 1: status_correct, required_evidence_covered, atomic_findings_correct, coverage_complete, readiness_correct; run 2: status_correct, required_evidence_covered, atomic_findings_correct, coverage_complete, readiness_correct; run 3: status_correct, required_evidence_covered, atomic_findings_correct, coverage_complete, readiness_correct.
- **property_building_specific_scope**: run 1: status_correct; run 2: status_correct; run 3: status_correct.
- **wc_partial_payroll_period**: run 1: status_correct, readiness_correct; run 2: status_correct, readiness_correct; run 3: status_correct, readiness_correct.
- **wc_document_absence_is_concern**: run 1: status_correct, atomic_findings_correct; run 2: status_correct, atomic_findings_correct; run 3: status_correct, atomic_findings_correct.
- **property_cross_source_alarm_and_value**: run 1: status_correct, atomic_findings_correct, coverage_complete, readiness_correct; run 2: status_correct, atomic_findings_correct, coverage_complete, readiness_correct; run 3: status_correct, atomic_findings_correct, coverage_complete, readiness_correct.
- **gl_loss_aggregation_without_duplicate**: run 1: coverage_complete, readiness_correct; run 2: coverage_complete, readiness_correct; run 3: coverage_complete, readiness_correct.
- **cyber_restore_duration_cross_midnight**: run 1: status_correct, readiness_correct; run 2: status_correct, readiness_correct; run 3: status_correct, readiness_correct.
- **property_expired_exception_certificate**: run 1: status_correct, atomic_findings_correct; run 2: status_correct, atomic_findings_correct; run 3: status_correct, atomic_findings_correct.

## Method and limits

Gold statuses, readiness, required evidence, findings, and any acceptable citation alternatives were authored before inference. Strict scoring checks status, one-to-one finding citation groups, required references, reference integrity, complete coverage, and labeled readiness. It does not automatically prove the explanation's semantic correctness. Alternative citation sets are predeclared; the scorer does not invent them after seeing outputs.

Each case has one criterion and a small set of already-extracted prose observations. The scenarios include realistic operational detail but do not represent complete submissions, independent expert labels, document extraction, multi-criterion batches, or large-context performance. The set was authored by the same assistant that developed the system. It is fresh regression evidence, not a blinded external benchmark. Identical temperature/seed runs may repeat exactly due to deterministic inference. Warm model/cache conditions affect latency.

See `manifest.json` for frozen hashes and run settings, `summary.json` for metrics, and each `run-NN.json` / `.md` for complete inputs, model calls, proposals, reviews, and reasons. Logs preserve execution progress. No model call receives gold expectations.
