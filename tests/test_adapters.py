import asyncio
import copy
import json
import threading
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
from tiny_skill_agent.assessment import PredicateDraft
from tiny_skill_agent.evidence import EvidenceMetadataMiddleware, tag_tool
from tiny_skill_agent.middleware import AssessmentMiddleware


def matched(payload):
    if payload["stage"] == "decision_review":
        return predicate(payload)
    return [{"criterion_id": key, "status": "matched", "evidence_ids": list(payload["evidence_spans"]),
             "basis": "condition_met", "conflict": "none",
             "findings": [{"subject": "Service", "evidence_ids": list(payload["evidence_spans"]),
                           "reason": "The observation explicitly satisfies the stated criterion."}],
             "reason": "The observation explicitly satisfies the stated criterion."} for key in payload["criteria"]]


def predicate(payload):
    return [{"criterion_id": key, "condition_quote": payload["criteria"][key]["text"],
             "scope_reason": "The supplied service is within the stated scope.",
             "scope": "in_scope", "condition_reason": "The observation explicitly satisfies the stated criterion.",
             "condition": "true", "exception_reason": "There is no exception in the supplied criterion.",
             "exception": "does_not_apply", "evidence_ids": list(payload["evidence_spans"]), "conflict": "none",
             "conflict_reason": "No incompatible observations are present in this evidence.",
             "findings": [{"subject": "Service", "evidence_ids": list(payload["evidence_spans"]),
                           "reason": "The observation explicitly satisfies the stated criterion."}]} for key in payload["criteria"]]


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
                    "parsed": schema.model_validate(predicate(payload)), "parsing_error": self.parsing_error}
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
        self.assertIs(model.schema, PredicateDraft)
        self.assertEqual(model.options, {"include_raw": True, "method": "json_schema"})
        self.assertEqual(len(result.findings), 1)
        self.assertTrue(result.coverage["decision_ready"])
        for broken in (StructuredModel(metadata={"done_reason": "length"}), StructuredModel(parsing_error="bad JSON")):
            failed = assess(criteria=inputs.criteria, evidence=inputs.evidence,
                            model=make_langchain_assessor(broken), config={"max_retries": 0})
            self.assertEqual(failed.findings, [])
            self.assertEqual(len(failed.coverage["errors"]), 3)

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


class CompletionMiddlewareTests(unittest.TestCase):
    def inputs(self):
        return AssessmentInputs(
            criteria=[Criterion(id="C1", text="Service must be available.", source_id="policy", classification="pass")],
            evidence=[Evidence(id="E1", source_id="monitor", quote="Available", locator="line:1")],
        )

    def test_real_agent_tool_loop_sync_and_async(self):
        for asynchronous in (False, True):
            with self.subTest(asynchronous=asynchronous):
                events = []
                @tool
                def observations() -> str:
                    """Return service observations."""
                    events.append("tool")
                    return "Service is available."
                tag_tool(observations, "data")
                def assessment_model(payload):
                    events.append(payload["stage"])
                    return matched(payload)
                middleware = AssessmentMiddleware(
                    assessment_model, tools=[observations],
                    system_prompt="[strength] Service must be available.",
                )
                agent = create_agent(
                    ToolModel(responses=[
                        AIMessage(content="", tool_calls=[{"name": "observations", "args": {}, "id": "call1"}]),
                        AIMessage(content="Finished normally."),
                    ]), tools=[observations],
                    middleware=[EvidenceMetadataMiddleware([observations]), middleware],
                )
                state = {"messages": [{"role": "user", "content": "Check service."}]}
                output = asyncio.run(agent.ainvoke(state)) if asynchronous else agent.invoke(state)
                self.assertEqual(events, ["tool", "source", "case", "decision_review"])
                self.assertEqual(output["messages"][-1].content, "Finished normally.")
                self.assertEqual(len(output["messages"]), 4)
                self.assertEqual(output["assessment"]["findings"][0]["facts"][0]["source"], "tool:observations#call1")
                self.assertTrue(output["assessment"]["coverage"]["decision_ready"])
                self.assertIsNone(output["assessment_error"])
                json.dumps(output["assessment"])

    def test_custom_mapper_preserves_state_and_structured_response(self):
        state = {"messages": [AIMessage(content="Done")], "structured_response": {"answer": 42},
                 "custom": self.inputs(), "assessment": {"old": True}}
        original = copy.deepcopy(state)
        wrapper = AssessmentMiddleware(matched, input_mapper=lambda s: s["custom"])
        update = wrapper.after_agent(state, None)
        self.assertEqual(state, original)
        self.assertEqual(set(update), {"assessment", "assessment_error"})
        self.assertTrue(update["assessment"]["coverage"]["decision_ready"])

    def test_checkpointed_next_turn_replaces_success_with_error_and_recovers(self):
        fail = False
        def mapper(state):
            if fail:
                raise ValueError("Extraction failed")
            return self.inputs()
        wrapper = AssessmentMiddleware(matched, input_mapper=mapper)
        agent = create_agent(ToolModel(responses=[AIMessage(content="Done") for _ in range(3)]),
                             middleware=[wrapper], checkpointer=InMemorySaver())
        config = {"configurable": {"thread_id": "completion"}}
        invoke = lambda: agent.invoke({"messages": [{"role": "user", "content": "Check"}]}, config)
        self.assertTrue(invoke()["assessment"]["coverage"]["decision_ready"])
        fail = True
        failed = invoke()
        self.assertIsNone(failed["assessment"])
        self.assertEqual(failed["assessment_error"]["type"], "ValueError")
        self.assertEqual(failed["messages"][-1].content, "Done")
        self.assertIsNone(agent.get_state(config).values["assessment"])
        fail = False
        recovered = invoke()
        self.assertIsNone(recovered["assessment_error"])
        self.assertTrue(recovered["assessment"]["coverage"]["decision_ready"])

    def test_provider_errors_remain_in_non_ready_assessment(self):
        def broken(payload):
            raise RuntimeError("Provider unavailable")
        wrapper = AssessmentMiddleware(broken, input_mapper=lambda _: self.inputs(), config={"max_retries": 0})
        output = wrapper.after_agent({"messages": []}, None)
        self.assertIsNone(output["assessment_error"])
        self.assertFalse(output["assessment"]["coverage"]["decision_ready"])
        self.assertEqual(len(output["assessment"]["coverage"]["errors"]), 3)

    def test_raise_mode_and_empty_inputs(self):
        wrapper = AssessmentMiddleware(matched, input_mapper=lambda _: {}, on_error="raise")
        with self.assertRaises(ValueError):
            wrapper.after_agent({"messages": []}, None)
        with self.assertRaises(ValueError):
            AssessmentMiddleware(matched, on_error="ignore")
        def unexpected(payload):
            self.fail("Empty inputs must not invoke the model")
        empty = AssessmentMiddleware(unexpected).after_agent({"messages": []}, None)
        self.assertFalse(empty["assessment"]["coverage"]["decision_ready"])

    def test_async_assessment_uses_worker_thread(self):
        main_thread = threading.get_ident()
        calls = []
        def model(payload):
            calls.append(threading.get_ident())
            return matched(payload)
        wrapper = AssessmentMiddleware(model, input_mapper=lambda _: self.inputs())
        asyncio.run(wrapper.aafter_agent({"messages": []}, None))
        self.assertTrue(calls)
        self.assertTrue(all(thread != main_thread for thread in calls))

    def test_interruption_clears_stale_result_and_defers_assessment_until_resume(self):
        calls = []
        def model(payload):
            calls.append(payload["stage"])
            return matched(payload)
        wrapper = AssessmentMiddleware(model, input_mapper=lambda _: self.inputs())
        agent = create_agent(ToolModel(responses=[AIMessage(content="Done")]),
                             middleware=[wrapper], checkpointer=InMemorySaver(), interrupt_before=["model"])
        config = {"configurable": {"thread_id": "interrupt"}}
        paused = agent.invoke({"messages": [{"role": "user", "content": "Check"}],
                               "assessment": {"old": True}}, config)
        self.assertIsNone(paused["assessment"])
        self.assertEqual(calls, [])
        completed = agent.invoke(Command(resume=True), config)
        self.assertTrue(completed["assessment"]["coverage"]["decision_ready"])
        self.assertEqual(calls, ["source", "case", "decision_review"])


if __name__ == "__main__":
    unittest.main()
