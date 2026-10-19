"""Exercise the benchmark's scoring independently of any model/provider."""

from copy import deepcopy
import json
from pathlib import Path
import unittest

from evals.run import score_case, validate_cases
from tiny_skill_agent import assess


class EvaluationScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads((Path(__file__).resolve().parents[1] / "evals/cases.json").read_text(encoding="utf-8"))
        cls.cases = {c["id"]: c for c in cls.dataset["cases"]}

    def result(self, case, status, ids):
        def model(payload):
            if payload["stage"] == "no_match_review":
                return [{"criterion_id": "C1", "verdict": "supported", "evidence_ids": ids,
                         "reason": "Fixed supported response for evaluation scorer testing."}]
            evidence_ids = [eid for eid in ids if eid in payload["evidence_spans"]]
            reason = "A fixed response used only to test benchmark scoring."
            return [{"criterion_id": "C1", "status": status,
                     "basis": {"matched": "condition_met", "no_match": "condition_not_met", "not_applicable": "scope_excluded", "insufficient_evidence": "missing_evidence"}[status],
                     "evidence_ids": evidence_ids, "conflict": "none",
                     "findings": [{"subject": "Test subject", "evidence_ids": evidence_ids, "reason": reason}] if status == "matched" else [],
                     "reason": reason}]
        return assess(criteria=case["criteria"], evidence=case["evidence"], model=model,
                      config={"review_decisions": False}).model_dump(mode="json")

    def test_gold_references_are_valid_and_bad_gold_is_rejected(self):
        validate_cases(self.dataset)
        bad = deepcopy(self.dataset)
        bad["cases"][0]["expected"]["required_evidence_ids"] = ["invented"]
        with self.assertRaisesRegex(ValueError, "Unknown gold"):
            validate_cases(bad)

    def test_combined_record_cannot_pass_as_two_atomic_findings(self):
        case = self.cases["multiple_concerns_one_source"]
        result = self.result(case, "matched", ["E1", "E2"])
        score = score_case(case, result)
        self.assertTrue(score["status_correct"])
        self.assertTrue(score["required_evidence_covered"])
        self.assertFalse(score["atomic_findings_correct"])
        self.assertFalse(score["passed"])
        combined = result["findings"][0]
        result["findings"] = [{**combined, "facts": [fact]} for fact in combined["facts"]]
        self.assertTrue(score_case(case, result)["passed"])
        result["findings"].append(deepcopy(result["findings"][0]))
        self.assertFalse(score_case(case, result)["atomic_findings_correct"])

    def test_wrong_status_cannot_pass_on_valid_citations(self):
        case = self.cases["unrelated_financials"]
        score = score_case(case, self.result(case, "matched", ["E1"]))
        self.assertTrue(score["reference_integrity"])
        self.assertFalse(score["status_correct"])
        self.assertEqual(score["false_positive_findings"], 1)
        self.assertFalse(score["passed"])

    def test_missing_response_does_not_pass_as_correct_abstention(self):
        case = self.cases["unrelated_financials"]
        result = self.result(case, "insufficient_evidence", [])
        self.assertTrue(score_case(case, result)["passed"])
        result["criterion_assessments"] = {}
        self.assertFalse(score_case(case, result)["passed"])

    def test_missing_conflict_evidence_is_reported(self):
        case = self.cases["contradiction_unresolved"]
        score = score_case(case, self.result(case, "insufficient_evidence", ["E1"]))
        self.assertTrue(score["status_correct"])
        self.assertFalse(score["required_evidence_covered"])
        self.assertEqual(score["missing_required_evidence"], ["E2"])

    def test_tampered_quote_and_unknown_reference_fail_integrity(self):
        case = self.cases["multiple_concerns_one_source"]
        result = self.result(case, "matched", ["E1", "E2"])
        result["findings"][0]["facts"][0]["quote"] = "Invented quotation"
        self.assertFalse(score_case(case, result)["reference_integrity"])

    def test_predeclared_alternatives_allow_corroboration_not_duplicates(self):
        case = deepcopy(self.cases["multiple_concerns_one_source"])
        case["expected"]["findings"] = [{"id": "single", "evidence_ids": ["E1"],
                                          "acceptable_evidence_sets": [["E1"], ["E2"], ["E1", "E2"]]}]
        result = self.result(case, "matched", ["E1", "E2"])
        self.assertTrue(score_case(case, result)["atomic_findings_correct"])
        result["findings"].append(deepcopy(result["findings"][0]))
        self.assertFalse(score_case(case, result)["atomic_findings_correct"])

    def test_labeled_readiness_is_part_of_strict_score(self):
        case = deepcopy(self.cases["unrelated_financials"])
        case["expected"]["decision_ready"] = False
        result = self.result(case, "insufficient_evidence", [])
        self.assertTrue(score_case(case, result)["passed"])
        result["coverage"]["decision_ready"] = True
        self.assertFalse(score_case(case, result)["readiness_correct"])
        self.assertFalse(score_case(case, result)["passed"])
        result = self.result(case, "matched", ["E1", "E2"])
        result["criterion_assessments"]["C1"]["evidence_ids"].append("invented")
        self.assertFalse(score_case(case, result)["reference_integrity"])


if __name__ == "__main__":
    unittest.main()
