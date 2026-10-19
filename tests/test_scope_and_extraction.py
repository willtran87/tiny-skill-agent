import asyncio
from copy import deepcopy
from types import SimpleNamespace
import unittest

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.memory import InMemorySaver

from tiny_skill_agent.adapters import inputs_from_messages, make_langchain_criterion_extractor
from tiny_skill_agent.criteria import CriterionExtraction
from tiny_skill_agent.evidence import EvidenceMetadataMiddleware, tag_tool
from tiny_skill_agent.middleware import AssessmentMiddleware, AssessmentScope


class ToolModel(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


class ScopeAndExtractionTests(unittest.TestCase):
    def fixtures(self, text="A roof older than 20 years is a concern."):
        @tool
        def guideline(document_id: str) -> str:
            """Read a guideline."""
            return text
        @tool
        def document(document_id: str) -> str:
            """Read an application."""
            return "Roof age: 25 years."
        tools = [tag_tool(guideline, "directive", source_arg="document_id", source_prefix="guide:"),
                 tag_tool(document, "data", source_arg="document_id", source_prefix="doc:")]
        middleware = EvidenceMetadataMiddleware(tools)
        messages = []
        for i, (name, doc, content) in enumerate((("guideline", "policy", text), ("document", "A", "Roof age: 25 years."),
                                                ("document", "B", "Roof age: 5 years."))):
            call = {"id": str(i), "name": name, "args": {"document_id": doc}}
            messages.extend([AIMessage(content="", tool_calls=[call]), middleware.wrap_tool_call(
                SimpleNamespace(tool_call=call), lambda _, content=content, i=i: ToolMessage(content=content, tool_call_id=str(i)))])
        return tools, messages

    def extractor(self, payload):
        return {"complete": True, "criteria": [{"quote": "A roof older than 20 years is a concern.", "classification": "concern"}], "issues": []}

    def test_prose_source_quote_and_context_are_preserved(self):
        tools, messages = self.fixtures()
        original = deepcopy(messages)
        inputs = inputs_from_messages(messages, tools, source_scope_ids=["guide:policy", "doc:B"], criterion_extractor=self.extractor)
        self.assertEqual(messages, original)
        self.assertEqual(inputs.criteria[0].text, "A roof older than 20 years is a concern.")
        self.assertEqual(inputs.criteria[0].context, inputs.criteria[0].text)
        self.assertEqual(inputs.criteria[0].source_id, "guide:policy")
        self.assertEqual({e.source_id for e in inputs.evidence}, {"doc:B"})

    def test_mixed_guideline_preserves_labelled_rule_and_adds_prose(self):
        tools, messages = self.fixtures("[strength] All buildings are sprinklered.\nA roof older than 20 years is a concern.")
        inputs = inputs_from_messages(messages, tools, criterion_extractor=self.extractor)
        self.assertEqual([c.id for c in inputs.criteria], ["C1", "C2"])
        self.assertEqual([c.classification for c in inputs.criteria], ["strength", "concern"])

    def test_scope_precedes_deduplication_of_identical_case_documents(self):
        tools, messages = self.fixtures()
        messages[-1] = messages[-1].model_copy(update={"content": "Roof age: 25 years."})
        inputs = inputs_from_messages(messages, tools, source_scope_ids=["guide:policy", "doc:B"], criterion_extractor=self.extractor)
        self.assertEqual({e.source_id for e in inputs.evidence}, {"doc:B"})
        self.assertEqual(inputs.evidence[0].quote, "Roof age: 25 years.")

    def test_incomplete_extraction_never_reaches_assessment(self):
        tools, messages = self.fixtures()
        wrapper = AssessmentMiddleware(lambda _: self.fail("No partial assessment allowed"), tools=tools,
            criterion_extractor=lambda _: {"complete": False, "criteria": [], "issues": ["Uncertain rule"]})
        output = wrapper.after_agent({"messages": messages}, None)
        self.assertIsNone(output["assessment"])
        self.assertIn("Incomplete criterion extraction", output["assessment_error"]["message"])

    def test_invalid_incomplete_or_ambiguous_extraction_fails_closed(self):
        tools, messages = self.fixtures()
        valid = self.extractor({})
        variants = [dict(valid, complete=False), dict(valid, issues=["Ambiguous label"]),
                    dict(valid, criteria=[{"quote": "Invented rule", "classification": "concern"}]),
                    dict(valid, criteria=[{"quote": "A roof older than 20 years is a concern.", "classification": "invented"}])]
        for response in variants:
            with self.subTest(response=response), self.assertRaises(ValueError):
                inputs_from_messages(messages, tools, criterion_extractor=lambda _: response)

    def test_source_allowlist_prevents_extraction_from_untrusted_directives(self):
        tools, messages = self.fixtures()
        def unexpected(payload):
            self.fail("Disallowed sources must not be sent to the extractor")
        inputs = inputs_from_messages(messages, tools, allowed_source_ids=[], criterion_extractor=unexpected)
        self.assertEqual(inputs.criteria, [])
        with self.assertRaisesRegex(ValueError, "not been observed"):
            inputs_from_messages(messages, tools, source_scope_ids=["doc:missing"])

    def test_known_classification_cannot_be_changed(self):
        text = "[concern] A roof older than 20 years is a concern."
        tools, messages = self.fixtures(text + "\nFull sprinklers are a strength.")
        def reclassify(payload):
            return {"complete": True, "criteria": [{"quote": text, "classification": "strength"}], "issues": []}
        with self.assertRaisesRegex(ValueError, "classification|reclassifies"):
            inputs_from_messages(messages, tools, criterion_extractor=reclassify)

    def test_explanatory_text_cannot_be_assigned_an_invented_classification(self):
        text = "[strength] All buildings are sprinklered.\nBuilding count means the total active inventory.\nUnrepaired damage is a concern."
        tools, messages = self.fixtures(text)
        def invalid(payload):
            return {"complete": True, "criteria": [{"quote": "Building count means the total active inventory.", "classification": "concern"}], "issues": []}
        with self.assertRaisesRegex(ValueError, "explicitly name"):
            inputs_from_messages(messages, tools, criterion_extractor=invalid)

    def test_known_rules_and_definitions_need_no_extraction_call(self):
        tools, messages = self.fixtures("[strength] All buildings are sprinklered.\nBuilding count means the total active inventory.")
        def unexpected(payload):
            self.fail("No unlabelled candidate names an allowed outcome")
        inputs = inputs_from_messages(messages, tools, criterion_extractor=unexpected)
        self.assertEqual(len(inputs.criteria), 1)

    def test_case_scope_validation_and_custom_mapper_cannot_bypass_scope(self):
        for scope in ({"case_id": "", "source_ids": ["a"]}, {"case_id": "B", "source_ids": []},
                      {"case_id": "B", "source_ids": ["a", "a"]}):
            with self.assertRaises(ValueError):
                AssessmentScope.model_validate(scope)
        tools, messages = self.fixtures()
        wrapper = AssessmentMiddleware(lambda _: self.fail("Must reject before assessment"),
            input_mapper=lambda _: inputs_from_messages(messages, tools, criterion_extractor=self.extractor),
            scope_from_context=lambda context: context)
        result = wrapper.after_agent({"messages": messages}, SimpleNamespace(context={"case_id": "B", "source_ids": ["doc:B", "guide:policy"]}))
        self.assertIsNone(result["assessment"])
        self.assertIn("escape case B", result["assessment_error"]["message"])

    def test_runtime_scope_is_fresh_in_sync_async_checkpointed_agent(self):
        for asynchronous in (False, True):
            with self.subTest(asynchronous=asynchronous):
                tools, messages = self.fixtures()
                seen = []
                def model(payload):
                    seen.append(set(e["source_id"] for e in payload["evidence_spans"].values()))
                    raise RuntimeError("Deliberate failure to avoid a fake semantic judgment")
                wrapper = AssessmentMiddleware(model, tools=tools, criterion_extractor=self.extractor,
                    scope_from_context=lambda c: c, config={"max_retries": 0})
                agent = create_agent(ToolModel(responses=[AIMessage(content="Done") for _ in range(4)]),
                    tools=tools, middleware=[wrapper], checkpointer=InMemorySaver(), context_schema=AssessmentScope)
                config = {"configurable": {"thread_id": "scope-test"}}
                def invoke(state, context=None):
                    return asyncio.run(agent.ainvoke(state, config, context=context)) if asynchronous else agent.invoke(state, config, context=context)
                output = invoke({"messages": messages}, {"case_id": "A", "source_ids": ["guide:policy", "doc:A"]})
                self.assertEqual({e["source_id"] for e in output["assessment"]["inputs"]["evidence"]}, {"doc:A"})
                seen.clear()
                output = invoke({"messages": [{"role": "user", "content": "Case B"}]}, {"case_id": "B", "source_ids": ["guide:policy", "doc:B"]})
                self.assertEqual({e["source_id"] for e in output["assessment"]["inputs"]["evidence"]}, {"doc:B"})
                self.assertTrue(all(s == {"doc:B"} for s in seen))
                output = invoke({"messages": [{"role": "user", "content": "No scope supplied"}]})
                self.assertIsNone(output["assessment"])
                self.assertIsNotNone(output["assessment_error"])

    def test_structured_extraction_adapter_rejects_truncation_and_parse_failure(self):
        parent = self
        class Model:
            def __init__(self, metadata=None, error=None):
                self.metadata, self.error = metadata or {}, error
            def with_structured_output(self, schema, **kwargs):
                parent.assertIs(schema, CriterionExtraction)
                return RunnableLambda(lambda _: {"raw": AIMessage(content="", response_metadata=self.metadata),
                    "parsed": parent.extractor({}), "parsing_error": self.error})
        self.assertTrue(make_langchain_criterion_extractor(Model())({}).complete)
        for model in (Model({"done_reason": "length"}), Model(error="Invalid JSON")):
            with self.assertRaises(ValueError):
                make_langchain_criterion_extractor(model)({})


if __name__ == "__main__":
    unittest.main()
