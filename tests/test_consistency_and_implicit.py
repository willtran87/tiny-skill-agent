"""Source-backed implicit classifications and final semantic readiness gates."""
import unittest
import json

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from tiny_skill_agent import assess
from tiny_skill_agent.assessment import PredicateAssessment
from tiny_skill_agent.adapters import inputs_from_messages, make_langchain_criterion_extractor
from tiny_skill_agent.criteria import SourceLineDecision
from tests.test_decision_review import predicate
from tests import test_scope_and_extraction as extraction_fixtures


class ImplicitCriterionTests(unittest.TestCase):
    def test_whole_source_review_preserves_context_and_deduplicates_known_rules(self):
        rule = "[concern] Refer a vessel above the permitted pressure."
        context = "Compare measurements in the same units."
        tools, messages = extraction_fixtures.ScopeAndExtractionTests().fixtures(rule + "\n" + context)
        parent = self
        class Model:
            def with_structured_output(self, schema, **kwargs):
                def invoke(messages):
                    payload = json.loads(messages[-1][1])
                    parent.assertEqual(payload["source_lines"], {"L1": rule, "L2": context})
                    result = {"lines": {
                        "L1": {"role": "outcome_rule", "reason": "Directs a concern.",
                         "criteria": [{"quote": rule, "classification": "concern", "classification_quote": ""}]},
                        "L2": {"role": "context", "reason": "Guidance for applying the rule.", "criteria": []}}}
                    return {"raw": AIMessage(content=""), "parsed": schema.model_validate(result)}
                return RunnableLambda(invoke)
        inputs = inputs_from_messages(messages, tools,
            criterion_extractor=make_langchain_criterion_extractor(Model()))
        self.assertEqual([c.text for c in inputs.criteria], [rule])
        self.assertIn(context, inputs.criteria[0].context)

    def test_context_and_unresolved_roles_cannot_emit_findings(self):
        for role in ("context", "unresolved"):
            with self.subTest(role=role), self.assertRaises(ValueError):
                SourceLineDecision(role=role, reason="Context only", criteria=[
                    {"quote": "A source line", "classification": "concern", "classification_quote": ""}])
        with self.assertRaises(ValueError):
            SourceLineDecision(role="outcome_rule", reason="Outcome", criteria=[])

    def test_provider_ambiguity_and_missing_lines_fail_closed(self):
        text = "Refer operations using an unguarded press."
        tools, messages = extraction_fixtures.ScopeAndExtractionTests().fixtures(text)
        for role, line_id in (("unresolved", "L1"), ("context", "invented")):
            class Model:
                def with_structured_output(self, schema, **kwargs):
                    return RunnableLambda(lambda _: {"raw": AIMessage(content=""), "parsed": {
                        "lines": {line_id: {"role": role,
                                   "reason": "An outcome is present but its classification is undefined.", "criteria": []}}}})
            with self.subTest(role=role), self.assertRaises(ValueError):
                inputs_from_messages(messages, tools,
                    criterion_extractor=make_langchain_criterion_extractor(Model()), extraction_max_retries=0)

    def test_provider_schema_binds_arbitrary_allowed_labels(self):
        class Model:
            def with_structured_output(self, schema, **kwargs):
                return RunnableLambda(lambda _: {"raw": AIMessage(content=""), "parsed": {"lines": {
                    "L1": {"role": "outcome_rule", "reason": "Direct outcome.", "criteria": [
                        {"quote": "Refer the operation.", "classification": "concern", "classification_quote": ""}]}}}})
        extract = make_langchain_criterion_extractor(Model())
        with self.assertRaises(ValueError):
            extract({"text": "Refer the operation.", "source_lines": {"L1": "Refer the operation."},
                     "labels": ["favorable", "adverse"]})

    def fixture(self):
        mapping = "A referral denotes a concern."
        rule = "Refer operations using an unguarded press."
        tools, messages = extraction_fixtures.ScopeAndExtractionTests().fixtures(mapping + "\n" + rule)
        output = {"complete": True, "issues": [], "criteria": [{"quote": rule, "classification": "concern", "classification_quote": mapping}],
                  "reviewed_lines": [{"line_id": "L1", "rule_quotes": []},
                                     {"line_id": "L2", "rule_quotes": [rule]}]}
        return tools, messages, output

    def test_implicit_quote_and_mapping_remain_separate_and_source_bound(self):
        tools, messages, output = self.fixture()
        inputs = inputs_from_messages(messages, tools, criterion_extractor=lambda _: output)
        self.assertEqual(inputs.criteria[0].text, output["criteria"][0]["quote"])
        self.assertEqual(inputs.criteria[0].classification_quote, "A referral denotes a concern.")
        self.assertEqual(inputs.criteria[0].source_id, "guide:policy")

    def test_mapping_cannot_be_invented_omitted_or_assign_an_unstated_label(self):
        for mapping, label in [("Invented concern mapping", "concern"), ("", "concern"), ("A referral denotes a concern.", "strength")]:
            tools, messages, output = self.fixture()
            output["criteria"][0].update(classification_quote=mapping, classification=label)
            with self.subTest(mapping=mapping), self.assertRaises(ValueError):
                inputs_from_messages(messages, tools, criterion_extractor=lambda _: output)

    def test_claimed_complete_cannot_skip_a_source_line(self):
        tools, messages, output = self.fixture()
        output["reviewed_lines"].pop()
        with self.assertRaisesRegex(ValueError, "every source line"):
            inputs_from_messages(messages, tools, criterion_extractor=lambda _: output)

    def test_rule_disposition_cannot_omit_its_extracted_rule(self):
        tools, messages, output = self.fixture()
        output["criteria"] = []
        with self.assertRaisesRegex(ValueError, "covering that source line"):
            inputs_from_messages(messages, tools, criterion_extractor=lambda _: output)

    def test_extraction_receives_all_lines_even_without_label_words(self):
        tools, messages = extraction_fixtures.ScopeAndExtractionTests().fixtures("Reject the operation if the press is unguarded.")
        seen = []
        def ambiguous(payload):
            seen.append(payload["source_lines"])
            return {"complete": False, "criteria": [], "issues": ["No source-backed classification mapping"], "reviewed_lines": []}
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            inputs_from_messages(messages, tools, criterion_extractor=ambiguous)
        self.assertEqual(len(seen), 1)

    def test_one_bounded_structural_repair_receives_validation_feedback(self):
        tools, messages, output = self.fixture()
        calls = []
        def repair(payload):
            calls.append(payload)
            if len(calls) == 1:
                return {**output, "reviewed_lines": []}
            return output
        result = inputs_from_messages(messages, tools, criterion_extractor=repair)
        self.assertEqual(len(result.criteria), 1)
        self.assertEqual(len(calls), 2)
        self.assertIn("every source line", calls[-1]["validation_feedback"])

    def test_structural_repair_can_be_disabled_and_has_a_fixed_bound(self):
        for retries in (0, 1):
            tools, messages, output = self.fixture()
            calls = []
            def invalid(payload):
                calls.append(payload)
                return {**output, "reviewed_lines": []}
            with self.assertRaises(ValueError):
                inputs_from_messages(messages, tools, criterion_extractor=invalid, extraction_max_retries=retries)
            self.assertEqual(len(calls), retries + 1)


class ConsistencyGateTests(unittest.TestCase):
    def run_case(self, check=None, config=None, rule=None, negative=False, context="", negative_review=None):
        candidate = predicate(condition="false", findings=[]) if negative else predicate()
        recorded = []
        def model(payload):
            recorded.append(payload)
            if payload["stage"] == "consistency_review":
                if isinstance(check, Exception):
                    raise check
                return [{"criterion_id": "C1", "scope_quote": "", "scope_applies": True, "exception_quote": "", "issues": [],
                         "reason": "All written predicates and the final decision are consistent with the cited facts.",
                         "verdict": "supported", **(check or {})}]
            if payload["stage"] == "decision_review":
                return [candidate]
            if payload["stage"] == "no_match_review":
                return [{"criterion_id": "C1", "verdict": "missing_evidence", "evidence_ids": ["E1"],
                         "reason": "The missing records leave the underlying activity unknown, not disproven.",
                         **(negative_review or {})}]
            return [PredicateAssessment.model_validate(candidate).assessment()]
        result = assess(criteria=[dict(id="C1", text=rule or "Flag a concern when the required document is missing.", source_id="policy", classification="concern", context=context)],
                        evidence=[dict(id="E1", source_id="data", locator="line:1", quote="The required document is missing.")],
                        model=model, config={"max_retries": 0, **(config or {})})
        return result, recorded

    def test_critical_issue_blocks_agreement_without_mutating_findings(self):
        result, _ = self.run_case({"verdict": "needs_review", "issues": [{"explanation_id": "decision_review.exception_reason",
            "reason": "This fixture simulates an explanation that contradicts an applicable exception."}]})
        self.assertEqual(len(result.findings), 1)
        self.assertFalse(result.coverage["decision_ready"])
        self.assertEqual(result.coverage["inconsistent_explanations"], ["C1"])

    def test_nonreceipt_cannot_refute_activity_or_record_existence(self):
        for kind in ("underlying_fact", "record_existence"):
            result, _ = self.run_case(negative=True, negative_review={
                "verdict": "supported", "requirement_kind": kind, "observation_kind": "nonreceipt_only"})
            self.assertEqual(result.criterion_assessments["C1"].status, "insufficient_evidence")
            self.assertEqual(result.no_match_reviews["C1"].verdict, "missing_evidence")
            self.assertIn("C1", result.superseded_decision_reviews)
            self.assertFalse(result.coverage["decision_ready"])

    def test_explicit_receipt_and_confirmed_absence_can_support_negative(self):
        for requirement, observation in (("record_receipt", "nonreceipt_only"),
                                          ("record_existence", "confirmed_absence"),
                                          ("underlying_fact", "affirmative_fact")):
            result, _ = self.run_case(negative=True, negative_review={
                "verdict": "supported", "requirement_kind": requirement, "observation_kind": observation})
            self.assertEqual(result.criterion_assessments["C1"].status, "no_match")
            self.assertTrue(result.coverage["decision_ready"])

    def test_unknown_failed_and_disabled_consistency_reviews_never_ready(self):
        for check, config in [({"verdict": "uncertain"}, {}), (ValueError("Provider failed"), {}), ({}, {"review_consistency": False})]:
            result, _ = self.run_case(check, config)
            self.assertFalse(result.coverage["decision_ready"])

    def test_unknown_explanation_section_id_is_rejected(self):
        result, _ = self.run_case({"verdict": "needs_review", "issues": [{"explanation_id": "invented",
            "reason": "The judge cannot invent an excerpt to justify a defect."}]})
        self.assertEqual(result.coverage["unverified_consistency"], ["C1"])
        self.assertFalse(result.coverage["decision_ready"])

    def test_explicit_scope_and_exception_clauses_must_be_acknowledged(self):
        for suffix in (" unless a current waiver applies.", " This applies only to licensed operations."):
            result, _ = self.run_case(rule="Flag a concern when the required document is missing" + suffix)
            self.assertEqual(result.coverage["unverified_consistency"], ["C1"])
            self.assertFalse(result.coverage["decision_ready"])

    def test_downgraded_review_is_archived_and_not_in_active_explanation(self):
        result, calls = self.run_case(negative=True)
        self.assertEqual(result.criterion_assessments["C1"].status, "insufficient_evidence")
        self.assertIn("C1", result.superseded_decision_reviews)
        self.assertNotIn("C1", result.decision_reviews)
        final = "\n".join(calls[-1]["candidates"]["C1"]["explanation"].values())
        self.assertIn("underlying activity unknown", final)
        self.assertNotIn("condition_reason:", final)

    def test_clean_supported_review_can_still_be_ready(self):
        result, _ = self.run_case()
        self.assertTrue(result.coverage["decision_ready"])
        self.assertEqual(result.coverage["unverified_consistency"], [])

    def test_scope_quote_can_use_same_source_context_but_not_other_text(self):
        scope = "Applies separately to each insured operation."
        good, _ = self.run_case({"scope_quote": scope}, context=scope)
        self.assertTrue(good.coverage["decision_ready"])
        bad, _ = self.run_case({"scope_quote": scope}, context="A different guideline statement.")
        self.assertFalse(bad.coverage["decision_ready"])
        self.assertEqual(bad.coverage["unverified_consistency"], ["C1"])

    def test_supported_verdict_cannot_override_excluded_or_unknown_scope(self):
        for applies in (False, None):
            result, _ = self.run_case({"scope_applies": applies, "verdict": "supported"})
            self.assertFalse(result.coverage["decision_ready"])
            self.assertEqual(result.consistency_reviews["C1"].verdict, "needs_review")


if __name__ == "__main__":
    unittest.main()
