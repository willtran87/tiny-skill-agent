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

`model` is a synchronous callable. For `stage="source"` or `"case"`, it returns `CoverageDraft` or a list of assessments. Its payload contains `stage`, `scope`, `user_request`, `criteria`, and `evidence_spans`; case calls also receive `source_assessments` and `conflict_candidates`. For `stage="decision_review"`, it returns `PredicateDraft` or a list of predicate assessments. That payload contains only original `criteria`, all `evidence_spans`, stage/scope, and optional validation feedback. Previous judgments and the user request are omitted. The payload's `scope` identifies the evidence batch; it is not a rule applicability restriction.

The LangChain adapter requests `PredicateDraft` for source, case, and review calls. It uses `PREDICATE_PROMPT` for source/case and a separately worded `DECISION_REVIEW_PROMPT` for the independent review. Source/case predicate responses are converted with `row.assessment()` into the existing `CoverageDraft` API contract. `status` and `basis` are derived from the predicates instead of being separately selected by the model. Custom adapters may retain `CoverageDraft` for source/case but must implement `PredicateDraft` for review. No global state is used.

`AssessmentConfig` controls `batch_size`, `retry_batch_size`, `max_retries`, `review_decisions`, and `confirm_no_match` (both reviews default true). Every criterion receives a separate predicate review, including abstentions and missing case responses. Final `no_match` results additionally receive the existing focused `no_match_review` challenge using `NoMatchReviewDraft` / `NO_MATCH_REVIEW_PROMPT`. This narrower check tests whether affirmative evidence refutes the condition, because two general passes can repeat the same absence-of-proof error. Unknown evidence, wrong-source citations, invalid criterion quotes, malformed output, duplicate or unrequested IDs reject that response. Retries are bounded; errors remain recorded after recovery. Disabling all-outcome review always prevents readiness; disabling the focused negative check prevents readiness for `no_match` decisions.

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

- `findings`: separate accepted case findings, with generated finding ID, subject, criterion ID, caller-supplied classification, exact supplied evidence quotes, source IDs, and locators. Multiple entries may share a criterion ID.
- `criterion_assessments`: one accepted final assessment per criterion, including status, basis, nested findings, and conflict review disposition.
- `source_assessments`: provisional source-level assessments retained for inspection.
- `pre_review_assessments`: original case proposals for all statuses, before independent review.
- `decision_reviews`: accepted independent predicate reviews, including exact criterion trigger quotes and separate scope/condition/exception explanations.
- `no_match_reviews`: focused sufficiency checks on final negative decisions, with verdict, citations and reason.
- `disagreements`: decisive source/case status differences in both directions, and source unresolved conflicts changed by the case; each retains the case review disposition.
- `coverage` and `source_coverage`: missing assessments, unreviewed criteria, review disagreements, unconfirmed negative statuses, and errors.
- `inputs`: the criterion and evidence registries used for this assessment.

The independent review supplies the final assessment when valid; otherwise the original accepted case proposal remains visible and unreviewed. A changed status or finding citation grouping is recorded in `coverage.review_disagreements` and blocks readiness. A recovered missing case also requires manual resolution. Thus a reviewer can correct an output without silently making it ready. Findings returned with `decision_ready=False` are provisional and require review. Original proposals and reviewer outputs are retained; neither is independent factual truth.

`decision_ready` requires a nonempty criterion set, complete source/case/review coverage, no insufficient evidence, agreement between case and predicate review on status and the multiset of finding citation groups, and a supported focused review for every `no_match`. The focused check can downgrade a negative to `insufficient_evidence`; `needs_reassessment` or failure leaves it unverified. Exact finding-group comparison is deliberately conservative: alternative valid corroborating citations may require manual resolution. Agreement does not compare explanation wording or prove semantic equivalence. Different source statuses remain review candidates, not proof of factual contradiction. Source coverage failures still block readiness. No evidence yields deterministic `insufficient_evidence` without a model call. The caller owns any human-review workflow.

### Structured-output migration

Custom assessment callables must retain the `basis`, `findings`, and `conflict` fields for source/case assessments, handle `stage="decision_review"` with `PredicateDraft`, and retain `stage="no_match_review"` with `NoMatchReviewDraft`. Old callables that do not implement these checks fail closed for readiness. The supplied LangChain adapter migrates automatically; the LangGraph state interface and `assess` arguments are unchanged. Legacy helpers in `evidence.py` retain their previous contract.

```python
assessment = {
    "criterion_id": "C1", "status": "matched", "basis": "condition_met",
    "evidence_ids": ["E1"], "conflict": "none",
    "reason": "The applicant's cash reserves exceed the six-month threshold.",
    "findings": [{
        "subject": "Applicant", "evidence_ids": ["E1"],
        "reason": "Eight months of reserves exceeds the six-month threshold.",
    }],
}
```

Use one nested finding per independent event/entity, with multiple citations for corroboration of the same finding. Nonmatched assessments require `findings=[]`. Basis/status mappings and conflict handling are detailed in [DESIGN.md](DESIGN.md). Final finding IDs such as `C1:F1` are assigned by code and only identify entries within a result. This revision strengthens structural validation; model-declared status bases and conflict resolutions are still semantic judgments.

A review returns the following shape (all fields required):

```python
review = [{
    "criterion_id": "C1",
    "condition_quote": "Cash reserves of at least six months",
    "scope_reason": "The evidence concerns the applicant and current reserves.",
    "scope": "in_scope",  # or out_of_scope / unknown
    "condition_reason": "Eight months is greater than or equal to six months.",
    "condition": "true",  # or false / unknown
    "exception_reason": "The criterion specifies no exception to this condition.",
    "exception": "does_not_apply",  # or applies / unknown
    "evidence_ids": ["E1"], "conflict": "none",
    "conflict_reason": "No incompatible observations are present in this evidence.",
    "findings": assessment["findings"],
}]
```

The condition quote must be an exact substring of `criterion.text`. Scope exclusion yields `not_applicable`; unresolved conflict or unknown scope yields `insufficient_evidence`; an applicable exception or proven false condition yields `no_match`; unknown condition/exception yields `insufficient_evidence`; otherwise a true condition yields `matched`. Nonmatched records must have no findings. The model is asked to show calculations, date handling, and exception reasoning explicitly, but arithmetic and semantic interpretation are still model judgments—not a deterministic calculator or formal rule engine.

Caller-supplied records are trusted inputs. Direct API use does not authenticate documents or independently verify quotes against an external store. The message adapter adds observed-tool provenance checks. Neither path proves semantic support, upstream truth, or underwriting correctness. Nested line-of-business routing remains a separate future extension.

The notebook now delegates to this API. It retains `result["structured_response"]` as a top-level Pydantic findings list for display; other fields match `AssessmentResult.model_dump()`. The old notebook's `criterion_inventory`, `source_catalog`, and `evidence_spans` result keys are replaced by the portable `inputs.criteria` and `inputs.evidence` records. Low-level legacy helpers in `evidence.py` remain available for existing callers.
