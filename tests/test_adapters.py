import asyncio
import copy
import json
import unittest
from types import SimpleNamespace
from typing import TypedDict

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from tiny_skill_agent import AssessmentInputs, Criterion, Evidence, assess
from tiny_skill_agent.adapters import inputs_from_messages, make_assessment_node, make_langchain_assessor
from tiny_skill_agent.assessment import CoverageDraft
from tiny_skill_agent.evidence import EvidenceMetadataMiddleware, tag_tool


def matched(payload):
    return [{"criterion_id": key, "status": "matched", "evidence_ids": list(payload["evidence_spans"]),
             "reason": "The observation explicitly satisfies the stated criterion."} for key in payload["criteria"]]


class ToolModel(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


class StructuredModel:
    def __init__(self, metadata=None, parsing_error=None):
        self.metadata = metadata or {}
        self.parsing_error = parsing_error

    def with_structured_output(self, schema, **kwargs):
        self.schema, self.options = schema, kwargs
        def invoke(messages):
            payload = json.loads(messages[-1][1])
            return {"raw": AIMessage(content="", response_metadata=self.metadata),
                    "parsed": schema.model_validate(matched(payload)), "parsing_error": self.parsing_error}
        return RunnableLambda(invoke)


class GraphState(TypedDict, total=False):
    observations: dict
    input_prompt: str
    result: dict


class AdapterTests(unittest.TestCase):
    def inputs(self):
        return AssessmentInputs(
            criteria=[Criterion(id="C1", text="Service must be available.", source_id="policy", classification="pass")],
            evidence=[Evidence(id="E1", source_id="monitor", quote="Available", locator="line:1")],
        )

    def test_actual_create_agent_messages_to_assessment(self):
        @tool
        def observations() -> str:
            """Return service observations."""
            return "Service is available."
        tag_tool(observations, "data")
        model = ToolModel(responses=[
            AIMessage(content="", tool_calls=[{"name": "observations", "args": {}, "id": "call1"}]),
            AIMessage(content="Retrieved observations."),
        ])
        agent = create_agent(model, tools=[observations], middleware=[EvidenceMetadataMiddleware([observations])])
        output = agent.invoke({"messages": [{"role": "user", "content": "Check service."}]})
        inputs = inputs_from_messages(output["messages"], [observations],
                                      system_prompt="[pass] Service must be available.", labels=("pass",))
        self.assertEqual(inputs.criteria[0].classification, "pass")
        self.assertEqual(inputs.evidence[0].source_id, "tool:observations#call1")
        result = assess(criteria=inputs.criteria, evidence=inputs.evidence, model=matched)
        self.assertEqual(result.findings[0].classification, "pass")
        self.assertTrue(result.coverage["complete"])

    def test_langchain_structured_model_and_truncation(self):
        model = StructuredModel()
        inputs = self.inputs()
        result = assess(criteria=inputs.criteria, evidence=inputs.evidence,
                        model=make_langchain_assessor(model, method="json_schema"))
        self.assertIs(model.schema, CoverageDraft)
        self.assertEqual(model.options, {"include_raw": True, "method": "json_schema"})
        self.assertEqual(len(result.findings), 1)
        for broken in (StructuredModel(metadata={"done_reason": "length"}), StructuredModel(parsing_error="bad JSON")):
            failed = assess(criteria=inputs.criteria, evidence=inputs.evidence,
                            model=make_langchain_assessor(broken), config={"max_retries": 0})
            self.assertEqual(failed.findings, [])
            self.assertEqual(len(failed.coverage["errors"]), 2)

    def test_compiled_langgraph_custom_state_and_checkpoint(self):
        inputs = self.inputs().model_dump(mode="json")
        state = {"observations": inputs, "input_prompt": "Review service"}
        original = copy.deepcopy(state)
        node = make_assessment_node(matched, input_mapper=lambda state: state["observations"], output_key="result")
        builder = StateGraph(GraphState)
        builder.add_node("assess", node)
        builder.add_edge(START, "assess")
        builder.add_edge("assess", END)
        graph = builder.compile(checkpointer=InMemorySaver())
        config = {"configurable": {"thread_id": "test"}}
        output = graph.invoke(state, config)
        self.assertEqual(state, original)
        self.assertEqual(output["result"]["findings"][0]["classification"], "pass")
        json.dumps(output["result"])
        self.assertEqual(graph.get_state(config).values["result"], output["result"])
        async_output = asyncio.run(graph.ainvoke(state, {"configurable": {"thread_id": "async-test"}}))
        self.assertTrue(async_output["result"]["coverage"]["complete"])

    def test_default_state_contract_and_no_mutation(self):
        state = {"assessment_input": self.inputs().model_dump(mode="json")}
        original = copy.deepcopy(state)
        self.assertIn("assessment", make_assessment_node(matched)(state))
        self.assertEqual(state, original)
        with self.assertRaises(ValueError):
            make_assessment_node(matched, output_key="assessment_input")

    def test_block_content_requires_explicit_extraction(self):
        @tool
        def observations() -> str:
            """Return observations."""
            return "Available"
        tag_tool(observations, "data")
        with self.assertRaisesRegex(ValueError, "Extract block"):
            inputs_from_messages([
                ToolMessage(content=[{"type": "text", "text": "Available"}], tool_call_id="call1", name="observations")
            ], [observations])

    def test_command_metadata_preserves_control_and_other_updates(self):
        @tool
        def observations() -> str:
            """Return observations."""
            return "Available"
        tag_tool(observations, "data")
        middleware = EvidenceMetadataMiddleware([observations])
        call = {"id": "call1", "name": "observations", "args": {}}
        message = ToolMessage(content="Available", tool_call_id="call1")
        other = ToolMessage(content="Other", tool_call_id="call2")
        command = Command(update={"messages": [message, other], "custom": 7}, goto="next")
        result = middleware.wrap_tool_call(SimpleNamespace(tool_call=call), lambda _: command)
        self.assertEqual(result.goto, "next")
        self.assertEqual(result.update["custom"], 7)
        self.assertEqual(result.update["messages"][0].artifact["_meta"]["kind"], "data")
        self.assertIsNone(message.artifact)
        self.assertIs(result.update["messages"][1], other)
        inputs = inputs_from_messages([AIMessage(content="", tool_calls=[call]), result.update["messages"][0]], [observations])
        self.assertEqual(len(inputs.evidence), 1)
        with self.assertRaisesRegex(ValueError, "matching ToolMessage"):
            middleware.wrap_tool_call(SimpleNamespace(tool_call=call), lambda _: Command(update={"custom": 7}))


if __name__ == "__main__":
    unittest.main()
