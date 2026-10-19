"""Check raw-document gold and isolation scoring without an LLM judge."""

from copy import deepcopy
import json
from pathlib import Path
import unittest

from langchain_core.messages import AIMessage, ToolMessage

from evals.e2e import DOCUMENTS, raw_quote, scoped_messages, score_turn, validate_dataset


class EndToEndScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads((Path(__file__).resolve().parents[1] / "evals/e2e_cases.json").read_text(encoding="utf-8"))
        cls.documents = {p.name: p.read_text(encoding="utf-8") for p in DOCUMENTS.iterdir() if p.is_file()}

    def fixture(self):
        sequence = self.dataset["sequences"][0]
        turn = sequence["turns"][0]
        rule = {"id": "C1", "text": turn["expected"]["criterion"], "source_id": "guide:property-guideline.md", "classification": "concern"}
        evidence = [{"id": f"E{i}", "source_id": "doc:" + doc, "source_label": doc, "locator": loc, "quote": quote, "context": quote}
                    for i, (doc, loc, quote) in enumerate(turn["expected"]["support"], 1)]
        findings = [{"criterion_id": "C1", "criterion": rule["text"], "criterion_source": rule["source_id"], "classification": "concern",
                     "facts": [{"evidence_id": e["id"], "source": e["source_id"], **{k: e[k] for k in ("source_label", "locator", "quote", "context")}}]}
                    for e in evidence]
        output = {"assessment": {"inputs": {"criteria": [rule], "evidence": evidence}, "findings": findings,
                  "criterion_assessments": {"C1": {"status": "matched", "evidence_ids": [e["id"] for e in evidence], "reason": "Synthetic scorer fixture."}},
                  "coverage": {"complete": True, "decision_ready": True}}}
        fetched = turn["documents"] + [sequence["guideline"]]
        return turn, sequence, output, fetched

    def score(self, fixture):
        turn, sequence, output, fetched = fixture
        return score_turn(turn, sequence, self.documents, output, fetched)

    def test_gold_resolves_to_raw_document_bytes(self):
        validate_dataset(self.dataset, self.documents)
        invalid = deepcopy(self.dataset)
        invalid["sequences"][0]["turns"][0]["expected"]["support"][0][2] = "Invented"
        with self.assertRaises(ValueError):
            validate_dataset(invalid, self.documents)
        self.assertEqual(raw_quote(self.documents["property-b.json"], "json:/buildings/0/roof_age_years"), "null")

    def test_good_atomic_findings_pass_but_combined_and_duplicate_do_not(self):
        fixture = self.fixture()
        self.assertTrue(self.score(fixture)["passed"])
        findings = fixture[2]["assessment"]["findings"]
        findings[0]["facts"] += findings.pop()["facts"]
        self.assertFalse(self.score(fixture)["findings_correct"])
        fixture = self.fixture()
        fixture[2]["assessment"]["findings"].append(deepcopy(fixture[2]["assessment"]["findings"][0]))
        self.assertFalse(self.score(fixture)["findings_correct"])

    def test_foreign_uncited_input_fails_isolation_even_with_correct_status(self):
        fixture = self.fixture()
        fixture[2]["assessment"]["inputs"]["evidence"].append({"id": "E9", "source_id": "doc:cyber-b.txt", "locator": "line:2", "quote": "Active privileged accounts: 12."})
        score = self.score(fixture)
        self.assertTrue(score["status_correct"])
        self.assertTrue(score["raw_source_integrity"])
        self.assertFalse(score["input_isolation"])
        self.assertTrue(score["unsafe_ready"])

    def test_missing_criteria_does_not_pass_as_abstention(self):
        fixture = self.fixture()
        fixture[2]["assessment"]["inputs"]["criteria"] = []
        score = self.score(fixture)
        self.assertFalse(score["criterion_extracted"])
        self.assertEqual(score["actual_status"], "missing")
        self.assertFalse(score["passed"])

    def test_forged_quote_fails_raw_integrity(self):
        fixture = self.fixture()
        fixture[2]["assessment"]["inputs"]["evidence"][0]["quote"] = "Roof age 1 year"
        self.assertFalse(self.score(fixture)["raw_source_integrity"])

    def test_mapper_retains_earlier_same_case_results_and_calls_only(self):
        call = AIMessage(content="", tool_calls=[{"name": "read_document", "args": {"document_id": "a"}, "id": "call1"}])
        foreign = ToolMessage(content="foreign", tool_call_id="call1", artifact={"_meta": {"source": "doc:a"}})
        earlier = ToolMessage(content="original", tool_call_id="call2", artifact={"_meta": {"source": "doc:b"}})
        later = ToolMessage(content="follow-up", tool_call_id="call3", artifact={"_meta": {"source": "doc:b-update"}})
        messages = [call, foreign, earlier, later]
        original = list(messages)
        selected = scoped_messages(messages, {"doc:b", "doc:b-update"})
        self.assertEqual(selected, [call, earlier, later])
        self.assertEqual(messages, original)


if __name__ == "__main__":
    unittest.main()
