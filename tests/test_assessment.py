import unittest

from tiny_skill_agent import AssessmentConfig, Criterion, Evidence, assess


def row(status="matched", ids=None, criterion_id="rule"):
    return {"criterion_id": criterion_id, "status": status,
            "evidence_ids": ["fact"] if ids is None else ids,
            "reason": "The cited observation supports this assessment of the supplied criterion."}


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.rule = Criterion(id="rule", text="A service must be available.", source_id="policy:v1", classification="pass")
        self.fact = Evidence(id="fact", source_id="monitor:1", quote="Available: true", locator="line:1")

    def run_assessment(self, model, **kwargs):
        return assess(criteria=[self.rule], evidence=[self.fact], model=model, **kwargs)

    def test_framework_independent_callable_and_arbitrary_classification(self):
        calls = []
        def model(payload):
            calls.append(payload)
            return [row()]
        result = self.run_assessment(model)
        self.assertEqual([call["stage"] for call in calls], ["source", "case"])
        self.assertEqual(result.findings[0].classification, "pass")
        self.assertEqual(result.findings[0].facts[0].source, "monitor:1")
        self.assertEqual(result.findings[0].facts[0].quote, self.fact.quote)
        self.assertTrue(result.coverage["decision_ready"])

    def test_case_can_combine_sources_while_source_calls_cannot(self):
        second = Evidence(id="second", source_id="monitor:2", quote="Confirmed", locator="line:2")
        def model(payload):
            if payload["stage"] == "case":
                return [row(ids=["fact", "second"])]
            ids = list(payload["evidence_spans"])
            self.assertEqual(len(ids), 1)
            return [row(ids=ids)]
        result = assess(criteria=[self.rule], evidence=[self.fact, second], model=model)
        self.assertEqual(len(result.findings[0].facts), 2)
        self.assertEqual(result.source_coverage["expected_pairs"], 2)
        bad = assess(criteria=[self.rule], evidence=[self.fact, second],
                     model=lambda _: [row(ids=["fact", "second"])],
                     config={"max_retries": 0})
        self.assertFalse(bad.coverage["complete"])
        self.assertEqual(len(bad.source_coverage["missing"]), 2)

    def test_case_overturns_source_match_and_keeps_audit(self):
        result = self.run_assessment(
            lambda p: [row("matched" if p["stage"] == "source" else "no_match")]
        )
        self.assertEqual(result.findings, [])
        self.assertEqual(result.criterion_assessments["rule"].status, "no_match")
        self.assertEqual(result.source_assessments["monitor:1"]["rule"].status, "matched")
        self.assertEqual(len(result.disagreements), 1)
        self.assertTrue(result.coverage["complete"])
        self.assertFalse(result.coverage["decision_ready"])

    def test_missing_case_never_promotes_source_match(self):
        result = self.run_assessment(lambda p: [row()] if p["stage"] == "source" else [], config={"max_retries": 0})
        self.assertEqual(result.findings, [])
        self.assertEqual(result.coverage["missing"], ["rule"])

    def test_unknown_citations_retry_and_fail_closed(self):
        calls = []
        def model(payload):
            calls.append(payload)
            return [row(ids=["invented"])]
        result = self.run_assessment(model, config={"max_retries": 1})
        self.assertEqual(len(calls), 4)
        self.assertEqual(result.findings, [])
        self.assertEqual(len(result.coverage["errors"]), 4)
        self.assertFalse(result.coverage["complete"])

    def test_retry_recovers_missing_ids(self):
        calls = 0
        def model(payload):
            nonlocal calls
            calls += 1
            return [] if calls == 1 else [row()]
        result = self.run_assessment(model, config={"max_retries": 1})
        self.assertTrue(result.coverage["complete"])
        self.assertEqual(calls, 3)

    def test_negative_confirmation_and_abstention(self):
        result = self.run_assessment(lambda _: [row("no_match")], config={"max_retries": 0})
        self.assertEqual(result.coverage["unconfirmed_no_match"], ["rule"])
        self.assertFalse(result.coverage["complete"])
        for status in ("no_match", "not_applicable", "insufficient_evidence"):
            with self.subTest(status=status):
                result = self.run_assessment(lambda _: [row(status, [] if status == "insufficient_evidence" else ["fact"])])
                self.assertEqual(result.coverage[status], ["rule"])
                self.assertEqual(result.findings, [])
                self.assertTrue(result.coverage["complete"])
                self.assertEqual(result.coverage["decision_ready"], status != "insufficient_evidence")

    def test_bad_inputs_rejected_and_empty_inputs_do_not_call_model(self):
        def never(_):
            raise AssertionError("Model should not be called")
        with self.assertRaisesRegex(ValueError, "Duplicate Criterion"):
            assess(criteria=[self.rule, self.rule], evidence=[self.fact], model=never)
        with self.assertRaisesRegex(ValueError, "Duplicate Evidence"):
            assess(criteria=[self.rule], evidence=[self.fact, self.fact], model=never)
        with self.assertRaises(ValueError):
            AssessmentConfig(batch_size=0)
        empty = assess(criteria=[self.rule], evidence=[], model=never)
        self.assertEqual(empty.coverage["insufficient_evidence"], ["rule"])
        self.assertFalse(empty.coverage["decision_ready"])
        no_rules = assess(criteria=[], evidence=[self.fact], model=never)
        self.assertFalse(no_rules.coverage["decision_ready"])

    def test_duplicate_response_ids_rejected(self):
        result = self.run_assessment(lambda _: [row(), row()], config={"max_retries": 0})
        self.assertFalse(result.coverage["complete"])
        self.assertEqual(result.findings, [])


if __name__ == "__main__":
    unittest.main()
