import unittest

from tiny_skill_agent import assess


class NoMatchReviewTests(unittest.TestCase):
    def run_case(self, verdict="supported", config=None, invalid=False):
        calls = []
        def model(payload):
            calls.append(payload)
            if payload["stage"] == "no_match_review":
                return [{"criterion_id": "C1", "verdict": verdict,
                         "evidence_ids": ["invented" if invalid else "E1"],
                         "reason": "The focused review identifies whether the underlying fact is known."}]
            return [{"criterion_id": "C1", "reason": "The initial model proposes a negative decision on the supplied facts.",
                     "evidence_ids": ["E1"], "conflict": "none", "basis": "condition_not_met",
                     "status": "no_match", "findings": []}]
        result = assess(criteria=[{"id": "C1", "text": "All operators completed training.", "source_id": "policy", "classification": "strength"}],
                        evidence=[{"id": "E1", "source_id": "records", "quote": "Records not provided.", "locator": "line:1"}],
                        model=model, config={"review_decisions": False, **(config or {})})
        return result, calls

    def test_missing_evidence_downgrades_and_preserves_proposal(self):
        result, calls = self.run_case("missing_evidence")
        self.assertEqual(result.criterion_assessments["C1"].status, "insufficient_evidence")
        self.assertEqual(result.criterion_assessments["C1"].basis, "missing_evidence")
        self.assertEqual(result.pre_review_assessments["C1"].status, "no_match")
        self.assertEqual(result.coverage["review_downgraded"], ["C1"])
        self.assertFalse(result.coverage["decision_ready"])
        self.assertTrue(result.coverage["complete"])
        self.assertEqual(len(calls), 3)
        self.assertNotIn("source_assessments", calls[-1])
        self.assertNotIn("proposed_assessment", calls[-1])

    def test_disabled_review_cannot_make_negative_decision_ready(self):
        result, calls = self.run_case(config={"confirm_no_match": False})
        self.assertEqual(len(calls), 2)
        self.assertTrue(result.coverage["complete"])
        self.assertEqual(result.coverage["unverified_no_match"], ["C1"])
        self.assertFalse(result.coverage["decision_ready"])

    def test_failed_review_cannot_confirm_negative_decision(self):
        result, calls = self.run_case(invalid=True, config={"max_retries": 1})
        self.assertEqual(len(calls), 4)
        self.assertIn("validation_feedback", calls[-1])
        self.assertFalse(result.coverage["complete"])
        self.assertFalse(result.coverage["decision_ready"])
        self.assertEqual(result.no_match_reviews, {})

    def test_inconclusive_review_blocks_readiness(self):
        result, _ = self.run_case("needs_reassessment")
        self.assertEqual(result.criterion_assessments["C1"].status, "no_match")
        self.assertEqual(result.coverage["unverified_no_match"], ["C1"])
        self.assertFalse(result.coverage["decision_ready"])

    def test_conflicting_review_abstains(self):
        result, _ = self.run_case("unresolved_conflict")
        self.assertEqual(result.coverage["unresolved_conflicts"], ["C1"])
        self.assertEqual(result.criterion_assessments["C1"].status, "insufficient_evidence")
        self.assertFalse(result.coverage["decision_ready"])

    def test_supported_review_records_confirmation(self):
        result, _ = self.run_case()
        self.assertFalse(result.coverage["decision_ready"])  # Legacy negative-only review is insufficient.
        self.assertEqual(result.coverage["unverified_no_match"], [])
        self.assertEqual(result.no_match_reviews["C1"].verdict, "supported")


if __name__ == "__main__":
    unittest.main()
