# Reusable assessment API

The library accepts observed criteria and evidence independently of an agent, message history, notebook, or model provider. `assess` lives in `tiny_skill_agent.assessment` and depends only on Python and Pydantic. The installed distribution still includes LangChain and the notebook's provider integrations.

## Direct API

```python
from tiny_skill_agent import AssessmentConfig, Criterion, Evidence, assess
from tiny_skill_agent.adapters import make_langchain_assessor
from langchain_ollama import ChatOllama

criteria = [Criterion(
    id="C1",
    text="Cash reserves of at least six months are a strength.",
    source_id="guidelines:liquidity:v1",
    source_label="Liquidity guideline",
    classification="strength",
)]
evidence = [Evidence(
    id="E1", source_id="application:123", source_label="Application 123",
    quote="Cash reserves: 8 months", locator="line:12",
    context="Applicant reserves as of the application date.",
)]
model = make_langchain_assessor(
    ChatOllama(model="qwen3-coder:30b", temperature=0), method="json_schema",
)
result = assess(
    criteria=criteria, evidence=evidence, model=model,
    config=AssessmentConfig(batch_size=1, max_retries=2),
    request="Review liquidity.",
)
print(result.model_dump_json(indent=2))
```

Plain dictionaries matching these records are accepted too. IDs must be nonempty and unique within each registry. Classification is caller supplied and may use any domain's vocabulary. The message adapter defaults to `[strength]` and `[concern]`, but the core does not require bracketed labels or a particular ID prefix.

`model` is a synchronous callable: `payload -> CoverageDraft | list[assessment]`. Its payload contains `stage`, `scope`, `user_request`, `criteria`, and `evidence_spans`; case calls also receive relevant `source_assessments`. A custom provider adapter can use `CoverageDraft.model_json_schema()` and `ASSESSMENT_PROMPT`. No global variables or print/display calls are used inside the assessment API.

`AssessmentConfig` controls `batch_size`, `retry_batch_size`, `max_retries`, and `confirm_no_match`. Retries are bounded per scope. Unknown evidence, evidence from the wrong source, malformed output, duplicate or unrequested criterion IDs reject that response batch. Missing criteria are retried. Errors remain recorded even when later calls recover.

## LangChain messages

Keep your existing agent and tools. Register each evidence tool and attach the middleware:

```python
from langchain.agents import create_agent
from tiny_skill_agent import assess
from tiny_skill_agent.adapters import inputs_from_messages, make_langchain_assessor
from tiny_skill_agent.evidence import EvidenceMetadataMiddleware, tag_tool

# chat_model, assessment_chat_model, data_tool, and guidelines_tool are supplied by your app.
tools = [tag_tool(data_tool, "data"), tag_tool(guidelines_tool, "directive")]
prompt = "Use the supplied guidelines and observed facts."
agent = create_agent(
    model=chat_model, tools=tools, system_prompt=prompt,
    middleware=[EvidenceMetadataMiddleware(tools)],
)
run = agent.invoke({"messages": [{"role": "user", "content": "Review this case."}]})
inputs = inputs_from_messages(run["messages"], tools, system_prompt=prompt)
assessment_model = make_langchain_assessor(assessment_chat_model)
result = assess(criteria=inputs.criteria, evidence=inputs.evidence, model=assessment_model)
```

For Ollama, pass `method="json_schema"` when constructing the assessment callable. Other models use their provider default or an explicitly supported method. The adapter requests raw output alongside parsed output so it can detect reported truncation and parsing failures.

`inputs_from_messages` checks registered tools, observed calls, runtime metadata, and criterion-source allowlists. Its optional `labels`, `allowed_source_kinds`, and `allowed_source_ids` arguments control criterion extraction. Pass the actual system prompt used by the application; dynamic prompt history is not reconstructed automatically.

The middleware handles ordinary `ToolMessage` results and `Command` results whose mapping `update["messages"]` contains a matching `ToolMessage`. It preserves other state updates and routing. Unsupported tagged evidence commands fail explicitly. A custom `ToolNode` does not automatically run `create_agent` middleware: record typed observations directly or wrap the execution boundary with the middleware. Text/JSON tool output is supported; multimodal or block content must be extracted first.

## LangGraph state

Use one assessment node in an existing graph. The default contract reads `state["assessment_input"]` and writes a JSON-serializable result under `state["assessment"]`:

```python
from typing import TypedDict
from langgraph.graph import START, END, StateGraph
from tiny_skill_agent import AssessmentInputs
from tiny_skill_agent.adapters import make_assessment_node

class State(TypedDict, total=False):
    assessment_input: dict
    input_prompt: str
    assessment: dict

builder = StateGraph(State)
builder.add_node("assess", make_assessment_node(model))  # model is the assessment callable above
builder.add_edge(START, "assess")
builder.add_edge("assess", END)
graph = builder.compile()
result = graph.invoke({
    "assessment_input": AssessmentInputs(criteria=criteria, evidence=evidence).model_dump(),
    "input_prompt": "Review liquidity.",
})
```

For an existing dictionary state, pass `input_mapper`, `output_key`, and `request_key`. For example, a graph retaining tagged tool messages can use:

```python
node = make_assessment_node(
    assessment_model,
    input_mapper=lambda state: inputs_from_messages(
        state["messages"], tools, system_prompt=prompt,
    ),
    output_key="underwriting_review",
)
```

The node returns only its output update and does not mutate incoming state. It is synchronous and works with `invoke` or LangGraph's `ainvoke`; model calls within the node remain sequential and synchronous. Checkpoints occur at the node boundary. Resuming an interrupted assessment node may repeat its model calls. Native asynchronous assessment, per-call checkpointing, retrieval, and parallel scheduling are outside this lightweight adapter.

## Output and reconciliation

`AssessmentResult` contains:

- `findings`: accepted case matches, with criterion ID, caller-supplied classification, exact supplied evidence quotes, source IDs, and locators.
- `criterion_assessments`: all accepted final case statuses.
- `source_assessments`: provisional source-level assessments retained for inspection.
- `disagreements`: source matches that the case pass changed to another status.
- `coverage` and `source_coverage`: missing assessments, unconfirmed negative statuses, and errors.
- `inputs`: the criterion and evidence registries used for this assessment.

The case pass is authoritative. Source matches are not automatically promoted if case reconciliation fails or disagrees. Disagreements keep `decision_ready` false for review. An empty criterion set is not decision ready; no evidence yields `insufficient_evidence` without calling a model. A complete report describes only supplied observations and criteria, not source discovery or exhaustive finding recall.

Caller-supplied records are trusted inputs. Direct API use does not authenticate documents or independently verify quotes against an external store. The message adapter adds observed-tool provenance checks. Neither path proves semantic support, upstream truth, or underwriting correctness. Nested line-of-business routing remains a separate future extension.

The notebook now delegates to this API. It retains `result["structured_response"]` as a top-level Pydantic findings list for display; other fields match `AssessmentResult.model_dump()`. The old notebook's `criterion_inventory`, `source_catalog`, and `evidence_spans` result keys are replaced by the portable `inputs.criteria` and `inputs.evidence` records. Low-level legacy helpers in `evidence.py` remain available for existing callers.
