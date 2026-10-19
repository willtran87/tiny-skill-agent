"""Readiness requires a valid independent review of every decision type."""
import unittest

from tiny_skill_agent import assess
from tiny_skill_agent.assessment import PredicateAssessment


def predicate(**updates):
    data = dict(criterion_id="C1", condition_quote="the required document is missing",
                scope_reason="The observation concerns the subject named in the rule.",
                scope="in_scope", condition_reason="The observed fact establishes the condition in this rule.",
                condition="true", exception_reason="The supplied rule has no applicable exception.",
                exception="does_not_apply", evidence_ids=["E1"], conflict="none",
                conflict_reason="No incompatible observations are present in this evidence.",
                findings=[dict(subject="One event", evidence_ids=["E1"],
                               reason="This event meets the stated condition on the evidence.")])
    data.update(updates)
    return data


class DecisionReviewTests(unittest.TestCase):
    def run_case(self, proposed=None, reviewed=None, config=None, negative_verdict="supported"):
        proposed = predicate() if proposed is None else proposed
        reviewed = proposed if reviewed is None else reviewed
        calls = []
        def model(payload):
            calls.append(payload)
            if payload["stage"] == "decision_review":
                return [reviewed] if reviewed else []
            if payload["stage"] == "no_match_review":
                return [dict(criterion_id="C1", verdict=negative_verdict, evidence_ids=["E1"],
                             reason="The focused challenge checks affirmative refutation separately.")]
            return [PredicateAssessment.model_validate(proposed).assessment()] if proposed else []
        result = assess(
            criteria=[dict(id="C1", text="Flag a concern when the required document is missing.",
                           source_id="policy", classification="concern")],
            evidence=[dict(id="E1", source_id="submission", quote="Required document is missing.", locator="line:1")],
            model=model, config={"max_retries": 0, **(config or {})})
        return result, calls

    def test_all_conclusive_statuses_require_independent_review(self):
        for record, status in [(predicate(), "matched"),
                               (predicate(condition="false", findings=[]), "no_match"),
                               (predicate(scope="out_of_scope", findings=[]), "not_applicable")]:
            with self.subTest(status=status):
                result, calls = self.run_case(record)
                self.assertTrue(result.coverage["decision_ready"])
                self.assertEqual(result.criterion_assessments["C1"].status, status)
                stages = ["source", "case", "decision_review"] + (["no_match_review"] if status == "no_match" else [])
                self.assertEqual([c["stage"] for c in calls], stages)
                for call in calls[2:]:
                    self.assertNotIn("source_assessments", call)
                    self.assertNotIn("proposed_assessment", call)

    def test_missing_or_invalid_review_blocks_all_conclusive_decisions(self):
        for reviewed in ({}, predicate(evidence_ids=["invented"], findings=[] ,condition="false")):
            for proposed in (predicate(), predicate(condition="false", findings=[]), predicate(scope="out_of_scope", findings=[])):
                result, _ = self.run_case(proposed, reviewed)
                self.assertFalse(result.coverage["decision_ready"])
                self.assertFalse(result.coverage["complete"])
                self.assertEqual(result.coverage["unreviewed"], ["C1"])

    def test_false_match_is_corrected_but_not_silently_ready(self):
        result, _ = self.run_case(reviewed=predicate(exception="applies", findings=[]))
        self.assertEqual(result.criterion_assessments["C1"].status, "no_match")
        self.assertEqual(result.pre_review_assessments["C1"].status, "matched")
        self.assertEqual(result.findings, [])
        self.assertTrue(result.coverage["complete"])
        self.assertEqual(result.coverage["review_disagreements"], ["C1"])
        self.assertFalse(result.coverage["decision_ready"])

    def test_missing_period_is_unknown_not_scope_exclusion(self):
        result, _ = self.run_case(predicate(scope="out_of_scope", findings=[]),
                                  predicate(condition="unknown", findings=[]))
        self.assertEqual(result.criterion_assessments["C1"].status, "insufficient_evidence")
        self.assertFalse(result.coverage["decision_ready"])

    def test_unknown_scope_exception_or_conflict_abstains(self):
        for data in (predicate(scope="unknown", findings=[]),
                     predicate(exception="unknown", findings=[]),
                     predicate(conflict="unresolved", findings=[])):
            result, _ = self.run_case(data)
            self.assertEqual(result.criterion_assessments["C1"].status, "insufficient_evidence")
            self.assertFalse(result.coverage["decision_ready"])

    def test_missing_document_concern_is_a_match_without_classification_inversion(self):
        result, _ = self.run_case()
        self.assertEqual(result.findings[0].classification, "concern")
        self.assertEqual(result.criterion_assessments["C1"].status, "matched")

    def test_different_atomic_findings_block_readiness_even_with_same_status(self):
        record = predicate()
        record["findings"].append({**record["findings"][0], "subject": "Duplicate claimed event"})
        result, _ = self.run_case(record, predicate())
        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.coverage["review_disagreements"], ["C1"])
        self.assertFalse(result.coverage["decision_ready"])

    def test_review_disabled_is_never_ready(self):
        result, calls = self.run_case(config={"review_decisions": False})
        self.assertTrue(result.coverage["complete"])
        self.assertFalse(result.coverage["decision_ready"])
        self.assertEqual(len(calls), 2)

    def test_review_recovers_missing_case_but_requires_manual_resolution(self):
        result, _ = self.run_case({}, predicate())
        self.assertEqual(result.criterion_assessments["C1"].status, "matched")
        self.assertFalse(result.coverage["decision_ready"])
        self.assertFalse(result.source_coverage["complete"])

    def test_schema_rejects_findings_defeated_by_exception(self):
        with self.assertRaises(ValueError):
            PredicateAssessment.model_validate(predicate(exception="applies"))

    def test_invented_criterion_quote_cannot_pass_review(self):
        result, _ = self.run_case(reviewed=predicate(condition_quote="a different rule entirely"))
        self.assertFalse(result.coverage["decision_ready"])
        self.assertEqual(result.decision_reviews, {})

    def test_agreed_negative_still_requires_affirmative_evidence(self):
        result, calls = self.run_case(predicate(condition="false", findings=[]), negative_verdict="missing_evidence")
        self.assertEqual(result.criterion_assessments["C1"].status, "insufficient_evidence")
        self.assertEqual(result.decision_reviews["C1"].condition, "false")
        self.assertEqual(result.no_match_reviews["C1"].verdict, "missing_evidence")
        self.assertFalse(result.coverage["decision_ready"])

    def test_negative_challenge_cannot_be_disabled_to_bypass_readiness(self):
        result, _ = self.run_case(predicate(condition="false", findings=[]), config={"confirm_no_match": False})
        self.assertTrue(result.coverage["complete"])
        self.assertEqual(result.coverage["unverified_no_match"], ["C1"])
        self.assertFalse(result.coverage["decision_ready"])

    def test_failed_negative_challenge_blocks_even_when_general_review_agrees(self):
        result, _ = self.run_case(predicate(condition="false", findings=[]), negative_verdict="invalid")
        self.assertFalse(result.coverage["complete"])
        self.assertFalse(result.coverage["decision_ready"])


if __name__ == "__main__":
    unittest.main()
