"""Evaluation integrity checks; no production changes or live model calls."""
from copy import deepcopy
import json
import unittest

from evals.holdout import (ROOT, DIMENSIONS, JudgeOutput, atomic_match,
                          finalize_score, match_criteria, score_case,
                          validate_dataset, validate_judgment)


class HoldoutScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
        cls.documents = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / "documents").iterdir()}

    def fixture(self, index=0):
        case = self.dataset["cases"][index]
        rules, evidence, rows = [], [], {}
        for g in case["expected"]:
            cid = "C" + g["id"][1:]
            rules.append(dict(id=cid, text=g["quote"], source_id="guide:" + case["guideline"], classification=g["classification"]))
            eids = []
            for doc, loc, quote in g["support"]:
                eid = f"E{len(evidence)+1}"
                evidence.append(dict(id=eid, source_id="doc:" + doc, source_label=doc, locator=loc, quote=quote, context=quote))
                eids.append(eid)
            rows[cid] = dict(status=g["status"], reason=g["rationale"], evidence_ids=eids,
                findings=[dict(evidence_ids=[eids[i] for i in group], reason=g["rationale"]) for group in g["finding_groups"]])
        return case, dict(inputs=dict(criteria=rules, evidence=evidence), criterion_assessments=rows,
                          findings=[], coverage=dict(complete=True, decision_ready=True))

    def score(self, case, result):
        return score_case(case, self.documents, result, [case["guideline"], *case["documents"]])

    def test_gold_spans_and_nontrivial_lengths(self):
        validate_dataset(self.dataset, self.documents)
        self.assertEqual(sum(len(c["expected"]) for c in self.dataset["cases"]), 18)
        self.assertEqual(sum(g["implicit"] for c in self.dataset["cases"] for g in c["expected"]), 7)
        self.assertTrue(all(len(text.split()) >= 600 for text in self.documents.values()))
        broken = deepcopy(self.dataset)
        broken["cases"][0]["expected"][0]["support"][0][2] = "invented"
        with self.assertRaises(ValueError):
            validate_dataset(broken, self.documents)

    def test_missing_implicit_rule_makes_ready_subset_unsafe(self):
        case, result = self.fixture(1)
        result["inputs"]["criteria"].pop()
        result["criterion_assessments"].pop("C3")
        score, candidates = self.score(case, result)
        self.assertEqual(score["criteria_extracted"], 2)
        self.assertTrue(score["unsafe_ready_objective"])
        self.assertFalse(score["criteria"][2]["status_correct"])
        self.assertEqual(score["criteria"][2]["explanation_state"], "missing")
        self.assertEqual(len(candidates), 2)

    def test_missing_output_cannot_pass_as_correct_abstention(self):
        case, _ = self.fixture(2)
        score, candidates = self.score(case, None)
        self.assertEqual(score["criteria_extracted"], 0)
        self.assertFalse(score["strict_pass"])
        self.assertFalse(any(r["status_correct"] for r in score["criteria"]))
        self.assertFalse(candidates)

    def test_partial_combined_wrong_source_and_duplicate_rules_fail_coverage(self):
        case, result = self.fixture()
        original = result["inputs"]["criteria"]
        for mutate in (lambda r: r[0].update(text=r[0]["text"].split(" unless")[0]),
                       lambda r: r[0].update(text=r[0]["text"] + "\n" + r[1]["text"]),
                       lambda r: r[0].update(source_id="guide:other"),
                       lambda r: r.append(deepcopy(r[0]))):
            rules = deepcopy(original)
            mutate(rules)
            result["inputs"]["criteria"] = rules
            score, _ = self.score(case, result)
            self.assertFalse(score["criterion_inventory_complete"])

    def test_one_to_one_atomic_support(self):
        self.assertTrue(atomic_match([{1}, {2}], [{1, 3}, {2}]))
        self.assertFalse(atomic_match([{1}, {2}], [{1, 2}]))
        self.assertFalse(atomic_match([{1}, {2}], [{1}, {1}]))

    def test_raw_forgery_fails_even_with_correct_labels(self):
        case, result = self.fixture()
        result["inputs"]["evidence"][0]["quote"] = "invented"
        score, _ = self.score(case, result)
        self.assertFalse(score["raw_integrity"])
        self.assertTrue(score["unsafe_ready_objective"])

    def judge(self, score=2, excerpt="A valid explanation"):
        return JudgeOutput.model_validate(dict(explanations=[dict(gold_id="G1", grades=[
            dict(dimension=d, score=score, excerpt=excerpt, justification="rubric fixture") for d in DIMENSIONS])]))

    def test_judge_cannot_invent_excerpts_or_skip_dimensions(self):
        candidates = [dict(gold_id="G1", candidate_explanation="A valid explanation")]
        self.assertTrue(validate_judgment(self.judge(), candidates)["G1"]["passed"])
        with self.assertRaises(ValueError):
            validate_judgment(self.judge(excerpt="invented"), candidates)
        broken = self.judge()
        broken.explanations[0].grades.pop()
        with self.assertRaises(ValueError):
            validate_judgment(broken, candidates)
        broken = self.judge()
        broken.explanations.append(deepcopy(broken.explanations[0]))
        with self.assertRaises(ValueError):
            validate_judgment(broken, candidates)

    def test_good_label_does_not_override_bad_or_missing_explanation(self):
        case, result = self.fixture()
        score, candidates = self.score(case, result)
        self.assertFalse(score["strict_pass"])
        for row in score["criteria"]:
            row.update(explanation_state="graded", explanation_grade=dict(total=10, passed=True))
        finalize_score(score)
        self.assertTrue(score["strict_pass"])
        score["criteria"][0]["explanation_grade"] = dict(total=0, passed=False)
        finalize_score(score)
        self.assertFalse(score["strict_pass"])
        self.assertTrue(score["ready_with_failed_explanation"])


if __name__ == "__main__":
    unittest.main()
