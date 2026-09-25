import unittest

from tiny_skill_agent.evidence import (
    SourceCatalog,
    build_fact_spans,
    evidence_assessment_coverage,
    expand_evidence_findings,
    source_assessment_coverage,
    validate_evidence_assessment_batch,
)


class AtomicAssessmentTests(unittest.TestCase):
    def setUp(self):
        self.catalog = SourceCatalog({
            "S1": {
                "source_id": "skill:liquidity", "source_kind": "skill",
                "label": "Skill: liquidity",
                "directive_lines": ["[strength] Treat eight months of reserves as a strength."],
            },
            "S2": {
                "source_id": "tool:balances#b1", "source_kind": "tool",
                "label": "Tool: balances (S2)",
                "fact_content": '{"cash":{"months":8,"as_of":"2026-01-01"},"income":null}',
            },
            "S3": {
                "source_id": "tool:notes#n1", "source_kind": "tool",
                "label": "Tool: notes (S3)",
                "fact_content": "Reserves: 8 months\nAs of: 2026-01-01\n\nIncome: unverified",
            },
        })
        self.inventory = {
            "C1": {
                "criterion": "[strength] Treat eight months of reserves as a strength.",
                "criterion_source_id": "S1",
            }
        }
        self.spans = build_fact_spans(self.catalog)

    def test_spans_preserve_locator_and_context(self):
        self.assertEqual(self.spans["E1"]["locator"], "json:/cash/months")
        self.assertEqual(self.spans["E1"]["quote"], "8")
        self.assertIn('"as_of": "2026-01-01"', self.spans["E1"]["context"])
        self.assertEqual(self.spans["E3"]["quote"], "null")
        self.assertEqual(self.spans["E4"]["locator"], "line:1")
        self.assertIn("As of: 2026-01-01", self.spans["E4"]["context"])
        self.assertEqual(self.spans["E6"]["context"], "Income: unverified")

    def test_atomic_source_restricts_evidence_and_case_can_combine(self):
        matched = {
            "criterion_id": "C1", "status": "matched",
            "evidence_ids": ["E1", "E4"],
            "reason": "The cash record and notes both show eight months of reserves.",
        }
        with self.assertRaisesRegex(ValueError, "outside the requested source"):
            validate_evidence_assessment_batch(
                [matched], ["C1"], self.spans, allowed_source_ids=["S2"]
            )
        accepted = validate_evidence_assessment_batch([matched], ["C1"], self.spans)
        findings = expand_evidence_findings(accepted, self.inventory, self.spans, self.catalog)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["classification"], "strength")
        self.assertEqual([fact["source"] for fact in findings[0]["facts"]], [
            "tool:balances#b1", "tool:notes#n1",
        ])
        self.assertEqual(findings[0]["facts"][0]["locator"], "json:/cash/months")

    def test_nonmatched_statuses_are_distinct_and_grounded(self):
        base = {
            "criterion_id": "C1",
            "reason": "The observed data does not establish this rule.",
        }
        for status in ("no_match", "not_applicable"):
            with self.subTest(status=status), self.assertRaisesRegex(ValueError, "requires cited evidence"):
                validate_evidence_assessment_batch(
                    [{**base, "status": status, "evidence_ids": []}], ["C1"], self.spans
                )
            accepted = validate_evidence_assessment_batch(
                [{**base, "status": status, "evidence_ids": ["E1"]}], ["C1"], self.spans
            )
            self.assertEqual(accepted["C1"]["status"], status)
        accepted = validate_evidence_assessment_batch(
            [{**base, "status": "insufficient_evidence", "evidence_ids": []}],
            ["C1"], self.spans,
        )
        report = evidence_assessment_coverage(accepted, self.inventory)
        self.assertTrue(report["complete"])
        self.assertFalse(report["decision_ready"])

    def test_source_coverage_counts_every_source_criterion_pair(self):
        report = source_assessment_coverage({"S2": {"C1": {}}}, ["S2", "S3"], ["C1"])
        self.assertEqual(report["expected_pairs"], 2)
        self.assertEqual(report["missing"], [{"source_id": "S3", "criterion_id": "C1"}])
        self.assertFalse(report["complete"])

    def test_case_coverage_separates_all_four_statuses(self):
        inventory = {f"C{number}": {} for number in range(1, 5)}
        assessments = {
            f"C{number}": {"status": status}
            for number, status in enumerate((
                "matched", "no_match", "insufficient_evidence", "not_applicable"
            ), start=1)
        }
        report = evidence_assessment_coverage(assessments, inventory)
        self.assertEqual(report["matched"], ["C1"])
        self.assertEqual(report["no_match"], ["C2"])
        self.assertEqual(report["insufficient_evidence"], ["C3"])
        self.assertEqual(report["not_applicable"], ["C4"])
        self.assertEqual(report["unconfirmed_no_match"], ["C2"])
        self.assertFalse(report["complete"])
        confirmed = evidence_assessment_coverage(
            assessments, inventory, confirmed_no_match=["C2"]
        )
        self.assertTrue(confirmed["complete"])
        self.assertFalse(confirmed["decision_ready"])


if __name__ == "__main__":
    unittest.main()
