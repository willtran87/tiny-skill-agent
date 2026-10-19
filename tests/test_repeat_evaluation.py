from copy import deepcopy
import unittest

from evals.repeat import signature, summarize


def sample(status="insufficient_evidence", ready=False):
    correct = status == "insufficient_evidence"
    return {"id": "case", "category": "missing", "expected": {"status": "insufficient_evidence", "decision_ready": False},
            "score": {"actual_status": status, "passed": correct and not ready,
                      "status_correct": correct, "readiness_correct": not ready,
                      "false_positive_findings": 0, "required_evidence_covered": True,
                      "atomic_findings_correct": True, "reference_integrity": True, "coverage_complete": True},
            "result": {"criterion_assessments": {"C1": {"status": status}}, "findings": [],
                       "coverage": {"decision_ready": ready, "complete": True, "errors": []}},
            "calls": [], "elapsed_seconds": 1}


def report(case):
    return {"state": "completed", "cases": [case]}


class RepeatEvaluationTests(unittest.TestCase):
    def test_stable_wrong_answer_is_consistent_not_accurate(self):
        result = summarize([report(sample("no_match", True)) for _ in range(3)])
        self.assertEqual(result["status_agreement_cases"], 1)
        self.assertEqual(result["decision_agreement_cases"], 1)
        self.assertEqual(result["all_runs_passed_cases"], 0)
        self.assertEqual(result["consistently_wrong_status_cases"], ["case"])
        self.assertEqual(result["runs"][0]["ready_despite_expected_abstention"], 1)

    def test_variable_status_and_readiness_are_not_agreement(self):
        result = summarize([report(sample()), report(sample("no_match", True)), report(sample())])
        self.assertEqual(result["status_agreement_cases"], 0)
        self.assertEqual(result["decision_agreement_cases"], 0)
        self.assertEqual(result["cases"][0]["strict_passes"], 2)
        self.assertEqual(result["consistently_wrong_status_cases"], [])

    def test_signature_ignores_wording_order_but_not_citation_groups(self):
        left = sample("matched", True)
        left["result"]["findings"] = [{"criterion_id": "C1", "reason": "First explanation", "facts": [{"evidence_id": "E1"}, {"evidence_id": "E2"}]}]
        right = deepcopy(left)
        right["result"]["findings"][0]["facts"].reverse()
        right["result"]["findings"][0]["reason"] = "Different wording"
        self.assertEqual(signature(left), signature(right))
        right["result"]["findings"][0]["facts"].pop()
        self.assertNotEqual(signature(left), signature(right))

    def test_incomplete_or_mismatched_reports_rejected(self):
        with self.assertRaises(ValueError):
            summarize([])
        with self.assertRaises(ValueError):
            summarize([{"state": "running", "cases": [sample()]}])
        with self.assertRaises(ValueError):
            summarize([report(sample()), report({**sample(), "id": "different"})])


if __name__ == "__main__":
    unittest.main()
