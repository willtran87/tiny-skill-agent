import unittest

from tiny_skill_agent import AssessmentConfig, Criterion, Evidence, assess as assess_api
from tiny_skill_agent.assessment import CoverageDraft


def assess(**kwargs):
    """Exercise source/case and legacy review separately from the new review tests."""
    kwargs["config"] = {"review_decisions": False, **kwargs.get("config", {})}
    return assess_api(**kwargs)


def row(status="matched", ids=None, criterion_id="rule", conflict="none", basis=None, findings=None):
    ids = ["fact"] if ids is None else ids
    reason = "The cited observation supports this assessment of the supplied criterion."
    return {"criterion_id": criterion_id, "status": status,
            "basis": basis or {"matched": "condition_met", "no_match": "condition_not_met", "not_applicable": "scope_excluded", "insufficient_evidence": "missing_evidence"}[status],
            "evidence_ids": ids, "reason": reason, "conflict": conflict,
            "findings": findings if findings is not None else ([{"subject": "Service", "evidence_ids": ids, "reason": reason}] if status == "matched" else [])}


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.rule = Criterion(id="rule", text="A service must be available.", source_id="policy:v1", classification="pass")
        self.fact = Evidence(id="fact", source_id="monitor:1", quote="Available: true", locator="line:1")

    def run_assessment(self, model, review=True, **kwargs):
        def with_review(payload):
            if review and payload["stage"] == "no_match_review":
                return [{"criterion_id": "rule", "verdict": "supported", "evidence_ids": ["fact"],
                         "reason": "Fixed sufficiency response for assessment orchestration tests."}]
            return model(payload)
        return assess(criteria=[self.rule], evidence=[self.fact], model=with_review, **kwargs)

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
        self.assertFalse(result.coverage["decision_ready"])  # All-outcome review is disabled here.

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
            lambda p: [row("matched")] if p["stage"] == "source" else [row("no_match", conflict="resolved")]
        )
        self.assertEqual(result.findings, [])
        self.assertEqual(result.criterion_assessments["rule"].status, "no_match")
        self.assertEqual(result.source_assessments["monitor:1"]["rule"].status, "matched")
        self.assertEqual(len(result.disagreements), 1)
        self.assertTrue(result.coverage["complete"])
        self.assertFalse(result.coverage["decision_ready"])
        self.assertEqual(result.disagreements[0]["review"], "resolved")

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
        result = self.run_assessment(lambda _: [row("no_match")], review=False, config={"max_retries": 0})
        self.assertEqual(result.coverage["unconfirmed_no_match"], ["rule"])
        self.assertFalse(result.coverage["complete"])
        for status in ("no_match", "not_applicable", "insufficient_evidence"):
            with self.subTest(status=status):
                result = self.run_assessment(lambda _: [row(status, [] if status == "insufficient_evidence" else ["fact"])])
                self.assertEqual(result.coverage[status], ["rule"])
                self.assertEqual(result.findings, [])
                self.assertTrue(result.coverage["complete"])
                self.assertFalse(result.coverage["decision_ready"])

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

    def test_multiple_findings_keep_independent_citations_and_reasons(self):
        second = Evidence(id="second", source_id="monitor:2", quote="Other service available", locator="line:1")
        def model(payload):
            ids = list(payload["evidence_spans"])
            findings = [{"subject": eid, "evidence_ids": [eid],
                         "reason": f"Observation {eid} independently establishes availability for this service."} for eid in ids]
            return [row(ids=ids, findings=findings)]
        result = assess(criteria=[self.rule], evidence=[self.fact, second], model=model)
        self.assertEqual([f.finding_id for f in result.findings], ["rule:F1", "rule:F2"])
        self.assertEqual([f.subject for f in result.findings], ["fact", "second"])
        self.assertEqual([[c.evidence_id for c in f.facts] for f in result.findings], [["fact"], ["second"]])
        self.assertNotEqual(result.findings[0].reason, result.findings[1].reason)
        self.assertFalse(result.coverage["decision_ready"])

    def test_schema_rejects_inconsistent_status_and_finding_shapes(self):
        invalid = [row("no_match", basis="scope_excluded"),
                   row("matched", findings=[]),
                   row("matched", conflict="unresolved"),
                   row("insufficient_evidence", basis="unresolved_conflict"),
                   {**row("no_match"), "findings": row()["findings"]},
                   {**row(), "findings": row()["findings"] * 2},
                   {**row(), "findings": row(ids=["invented"])["findings"]}]
        for response in invalid:
            with self.subTest(response=response), self.assertRaises(ValueError):
                CoverageDraft.model_validate([response])

    def test_case_match_cannot_ignore_opposing_source(self):
        second = Evidence(id="second", source_id="monitor:2", quote="Unavailable", locator="line:1")
        for case in (row(), row(conflict="resolved"), row(ids=["fact", "second"])):
            def model(payload):
                if payload["stage"] == "case":
                    self.assertEqual(payload["conflict_candidates"]["rule"], ["fact", "second"])
                    return [case]
                return [row("matched" if payload["scope"] == "monitor:1" else "no_match", ids=list(payload["evidence_spans"]))]
            result = assess(criteria=[self.rule], evidence=[self.fact, second], model=model, config={"max_retries": 0})
            self.assertFalse(result.coverage["decision_ready"])
            self.assertEqual(result.findings, [])
            self.assertEqual(result.coverage["missing"], ["rule"])
            self.assertIn("opposing source judgments", result.coverage["errors"][0]["error"])

    def test_complementary_evidence_does_not_require_a_fabricated_conflict(self):
        second = Evidence(id="second", source_id="monitor:2", quote="Complementary observation", locator="line:1")
        def model(payload):
            if payload["stage"] == "case":
                self.assertIn("source_assessments", payload)
                return [row(ids=["fact", "second"])]
            return [row("no_match" if payload["scope"] == "monitor:1" else "insufficient_evidence",
                        ids=list(payload["evidence_spans"]))]
        result = assess(criteria=[self.rule], evidence=[self.fact, second], model=model)
        self.assertTrue(result.coverage["complete"])
        self.assertEqual(result.criterion_assessments["rule"].conflict, "none")
        self.assertFalse(result.coverage["decision_ready"])  # Review gates still apply.

    def test_unresolved_conflict_abstains_and_tracks_both_directions(self):
        second = Evidence(id="second", source_id="monitor:2", quote="Unavailable", locator="line:1")
        def model(payload):
            if payload["stage"] == "case":
                return [row("insufficient_evidence", ids=["fact", "second"], conflict="unresolved", basis="unresolved_conflict")]
            return [row("matched" if payload["scope"] == "monitor:1" else "no_match", ids=list(payload["evidence_spans"]))]
        result = assess(criteria=[self.rule], evidence=[self.fact, second], model=model)
        self.assertEqual(result.coverage["unresolved_conflicts"], ["rule"])
        self.assertEqual(len(result.disagreements), 2)
        self.assertTrue(result.coverage["complete"])
        self.assertFalse(result.coverage["decision_ready"])
        self.assertEqual(result.findings, [])

    def test_different_subjects_can_resolve_status_disagreement(self):
        second = Evidence(id="second", source_id="monitor:2", quote="Another service unavailable", locator="line:1")
        def model(payload):
            if payload["stage"] == "case":
                return [row(ids=["fact", "second"], findings=row()["findings"], conflict="different_scope")]
            return [row("matched" if payload["scope"] == "monitor:1" else "no_match", ids=list(payload["evidence_spans"]))]
        result = assess(criteria=[self.rule], evidence=[self.fact, second], model=model)
        self.assertFalse(result.coverage["decision_ready"])
        self.assertEqual(result.disagreements[0]["source_status"], "no_match")
        self.assertEqual(result.disagreements[0]["case_status"], "matched")
        self.assertEqual([f.evidence_id for f in result.findings[0].facts], ["fact"])

    def test_retry_receives_validation_feedback_and_can_resolve(self):
        calls = []
        def model(payload):
            calls.append(payload)
            if payload["stage"] == "source":
                return [row("insufficient_evidence", conflict="unresolved", basis="unresolved_conflict")]
            if "validation_feedback" not in payload:
                return [row()]
            self.assertIn("opposing source", payload["validation_feedback"]["rule"])
            return [row(conflict="resolved")]
        result = self.run_assessment(model)
        self.assertTrue(result.coverage["complete"])
        self.assertEqual(len(calls), 3)
        self.assertEqual(len(result.coverage["errors"]), 1)
        self.assertEqual(result.disagreements[0]["review"], "resolved")

    def test_unresolved_within_source_requires_case_review(self):
        def model(payload):
            if payload["stage"] == "source":
                return [row("insufficient_evidence", conflict="unresolved", basis="unresolved_conflict")]
            self.assertEqual(payload["conflict_candidates"]["rule"], ["fact"])
            return [row()]
        result = self.run_assessment(model, config={"max_retries": 0})
        self.assertFalse(result.coverage["complete"])
        self.assertEqual(result.findings, [])


if __name__ == "__main__":
    unittest.main()
