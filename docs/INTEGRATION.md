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

`model` is a synchronous callable. For `stage="source"` or `"case"`, it returns `CoverageDraft` or a list of assessments. Its payload contains `stage`, `scope`, `user_request`, `criteria`, and `evidence_spans`; case calls also receive `source_assessments` and evidence IDs in `conflict_candidates`. The standard LangChain adapter omits provisional source opinions from its provider request; custom callable payloads remain compatible. For `stage="decision_review"`, it returns `PredicateDraft` or a list of predicate assessments. That payload contains only original `criteria`, all `evidence_spans`, stage/scope, and optional validation feedback. Previous judgments and the user request are omitted. The payload's `scope` identifies the evidence batch; it is not a rule applicability restriction.

The LangChain adapter requests `PredicateDraft` for source, case, and review calls. It uses `PREDICATE_PROMPT` for source/case and a separately worded `DECISION_REVIEW_PROMPT` for the independent review. Source/case predicate responses are converted with `row.assessment()` into the existing `CoverageDraft` API contract. `status` and `basis` are derived from the predicates instead of being separately selected by the model. Custom adapters may retain `CoverageDraft` for source/case but must implement `PredicateDraft` for review. No global state is used.

`AssessmentConfig` controls `batch_size`, `retry_batch_size`, `max_retries`, `review_decisions`, `confirm_no_match`, and `review_consistency` (all default true). Every criterion receives a separate predicate review, including abstentions and missing case responses. Final `no_match` results additionally receive the existing focused `no_match_review` challenge using `NoMatchReviewDraft` / `NO_MATCH_REVIEW_PROMPT`. This narrower check tests whether affirmative evidence refutes the condition, because two general passes can repeat the same absence-of-proof error. Unknown evidence, wrong-source citations, invalid criterion quotes, malformed output, duplicate or unrequested IDs reject that response. Retries are bounded; errors remain recorded after recovery. Disabling all-outcome review always prevents readiness; disabling the focused negative check prevents readiness for `no_match` decisions.

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

## Optional agent-completion middleware

`AssessmentMiddleware` invokes the same `assess` API from LangChain's
[`after_agent` hook](https://reference.langchain.com/python/langchain/agents/middleware/types/after_agent).
It adds two state fields without updating messages, `structured_response`, tools,
or routing. Import it explicitly; existing agents do not enable it automatically.

```python
from tiny_skill_agent.middleware import AssessmentMiddleware

# tools, prompt, chat_model, and assessment_model are from the example above.
# assessment_model is the callable returned by make_langchain_assessor, not
# the raw chat model. With Ollama use method="json_schema" for that adapter.
agent = create_agent(
    model=chat_model,
    tools=tools,
    system_prompt=prompt,
    middleware=[
        EvidenceMetadataMiddleware(tools),
        AssessmentMiddleware(
            assessment_model,
            tools=tools,
            system_prompt=prompt,
            request="Assess the observed facts against the supplied guidelines.",
        ),
    ],
)
run = agent.invoke({"messages": [{"role": "user", "content": "Review this case."}]})
result = run.get("assessment")
ready = bool(result and result["coverage"]["decision_ready"])
error = run.get("assessment_error")
# The agent's original response remains in run["messages"].
```

Reserve `assessment` and `assessment_error` for this middleware. The former is
the JSON-serializable `AssessmentResult`, or `None` when unavailable. The latter
is `None` or an error with `type` and `message`. Both are cleared in `before_agent`
on a fresh invocation so a previous turn's result cannot appear current after a
failure or interruption. Normal completion runs assessment once; interrupted,
cancelled, or failed agent execution does not guarantee completion assessment.
Inspect the final state/update when streaming; model tokens can arrive earlier.

By default, extraction and other wrapper errors are recorded and the agent
response remains available. Set `on_error="raise"` to propagate those errors.
Provider/parsing failures already handled by `assess` remain in the result's
`coverage.errors`, with the existing readiness gates; `on_error="raise"` does not
turn those recorded failures into exceptions. An absent assessment is never ready.

The default extractor uses **all retained messages**, the registered tools, and
the supplied static system prompt. This includes earlier turns in checkpointed
conversations. Use a separate thread per case, or provide `input_mapper(state)`
to select the intended evidence and criteria. A custom mapper returns
`AssessmentInputs` or an equivalent dictionary and can support different labels,
criterion-source allowlists, dynamic prompts, or other data formats using the
existing extraction API. Its state is read-only by convention: do not mutate it.
Custom state inputs must be declared in the agent's state schema.

```python
completion = AssessmentMiddleware(
    assessment_model,
    input_mapper=lambda state: state["assessment_input"],
    config=AssessmentConfig(batch_size=1),
)
```

The wrapper does not register or collect tools itself. Pair it with
`EvidenceMetadataMiddleware` for the default message extractor; explicit-record
mappers do not require that collector. Supply the actual prompt used by your
agent, since runtime prompt changes are not captured automatically. Keep the
wrapper first in the middleware list if other completion hooks transform state
that it must see: LangChain executes completion hooks in reverse list order.

`ainvoke`/`astream` run the synchronous assessment in a worker thread, so it does
not block the event loop. The callable and custom mapper must support that use.
Assessment still completes before the invocation returns; this is not a background
job. Cancelling the await cannot stop an already-running synchronous provider
call. Checkpoint replay of the completion hook can repeat model calls. There is
no per-call checkpointing or exactly-once guarantee, and no additional model
calls beyond the existing assessment pipeline.

For a custom LangGraph graph, retain `make_assessment_node` below. This middleware
uses the lifecycle of `create_agent`; arbitrary graphs do not invoke its hooks.

### Explicit case isolation and prose guidelines

For a conversation that can switch cases, enable `scope_from_context`. It reads
an `AssessmentScope` from application-supplied invocation context, rather than
checkpointed state or model-generated text. Context is supplied afresh on every
invocation, including resume. The application owns the mapping from case ID to
source IDs. Use immutable, globally unique document/version IDs; reusing the same
source ID for different applicants would defeat that mapping. Shared guidelines
may intentionally appear in more than one case scope.

```python
from tiny_skill_agent.middleware import AssessmentMiddleware, AssessmentScope
from tiny_skill_agent.adapters import make_langchain_criterion_extractor

# These tools accept a document_id argument; choose prefixes matching your IDs.
tag_tool(data_tool, "data", source_arg="document_id", source_prefix="doc:")
tag_tool(guidelines_tool, "directive", source_arg="document_id", source_prefix="guide:")
tools = [data_tool, guidelines_tool]
completion = AssessmentMiddleware(
    assessment_model,
    tools=tools,
    system_prompt=prompt,
    scope_from_context=lambda context: context,
    criterion_extractor=make_langchain_criterion_extractor(
        assessment_chat_model, method="json_schema",
    ),
)
agent = create_agent(
    chat_model, tools=tools, system_prompt=prompt, context_schema=AssessmentScope,
    middleware=[EvidenceMetadataMiddleware(tools), completion],
)
run = agent.invoke(
    {"messages": [{"role": "user", "content": "Review application-123 using property:v2."}]},
    context=AssessmentScope(
        case_id="application-123",
        source_ids=["doc:application-123:v1", "guide:property:v2"],
    ),
)
```

`scope_from_context` can also select a nested scope from your existing context
object. It must return a valid `AssessmentScope` or matching dictionary. Omitted
or invalid scope cannot fall back to the previous case: assessment is unavailable
and `assessment_error` is populated (or raised with `on_error="raise"`).

The default message adapter validates provenance, then filters the run-local
ledger **before** source deduplication, criterion extraction, or assessment.
Every declared source must have an observed result, or extraction fails. Include
all desired evidence and guideline sources; include `system_prompt` explicitly
when it supplies criteria. Earlier observations for the same case remain eligible.
There is no automatic scope inference when `scope_from_context` is omitted;
legacy callers retain their existing behavior.

Custom input mappers are also checked against the supplied scope: foreign or
missing expected source IDs reject their output before assessment. They remain
responsible for accurate source provenance. Configure their extraction inside
the mapper, not simultaneously through the wrapper's `criterion_extractor` option.
Direct adapter callers can use `source_scope_ids` for the same ledger filtering;
the older `allowed_source_ids` parameter restricts only criterion sources.

The optional `criterion_extractor` makes one structured call for each permitted
directive source with nonempty lines beyond its already extracted bracketed rules.
It reads all remaining text, including rules without explicit classification
words. Every remaining line receives a `reviewed_lines` entry linking its rule
quotes, or an empty list for context and mappings. A dynamic schema fixes the review count;
code checks exact IDs, complete coverage, and links between rule lines and quotes.
Already labelled rules retain their deterministic coverage and classification.

An implicit rule can use a separate, exact `classification_quote` from the **same
source**, such as a definition mapping referral to concern. The criterion's `text`
stays the exact rule; the mapping is stored separately on `Criterion`. Code checks
that the mapping occurs in the source and names the allowed classification.
The semantic connection between outcome and label is still a model judgment.
There is no built-in assumption that particular underwriting verbs imply a label.
Explicitly labelled rules need no mapping; redundant proposed mappings for them
are discarded. Unknown mappings or declared ambiguities fail extraction.

Code assigns IDs and source labels, preserves the entire source as context, and
rejects altered rule quotations, unapproved labels, overlapping rules, conflicting
reclassification, missing line reviews, and declared incompleteness. Definitions
and operational instructions must not become assessment rules. No applicant facts
are supplied to this extraction stage; data tools cannot become guideline sources.

The structured extractor callable makes one call. The message adapter allows one
explicit repair attempt for invalid structure/quotes by default, passing
`validation_feedback` to the extractor. Set `extraction_max_retries=0` on
`inputs_from_messages` to disable repair, or configure a bounded value in a custom
mapper. Every attempt invokes the same callable and is visible to tracing.
Declared incompleteness/ambiguity fails immediately without a repair attempt.
There are no new dependencies. Failure makes assessment unavailable.
A model can still misclassify a substantive line as context, or read a
mapping incorrectly: structural line coverage does not prove semantic completeness.
Custom labels and criterion-source allowlists remain available through a mapper.

These options isolate **assessment inputs**. They preserve agent messages and
do not enforce document access permissions, remove history from the agent's
context, or validate the agent's free-text answer. Keep authorization at the tool
boundary. Invocation context follows the standard
[LangChain runtime interface](https://docs.langchain.com/oss/python/langchain/runtime).

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
- `superseded_decision_reviews`: earlier reviews whose decisions were subsequently downgraded by the focused negative review; retained as history, outside the active explanation.
- `consistency_reviews`: final checks of scope, status, findings, and explanation consistency, with references to original explanation section IDs and supporting reasons.
- `no_match_reviews`: focused sufficiency checks on final negative decisions, with verdict, citations and reason.
- `disagreements`: decisive source/case status differences in both directions, and source unresolved conflicts changed by the case; each retains the case review disposition.
- `coverage` and `source_coverage`: missing assessments, unreviewed criteria, review disagreements, unconfirmed negative statuses, and errors.
- `inputs`: the criterion and evidence registries used for this assessment.

The independent review supplies the final assessment when valid; otherwise the original accepted case proposal remains visible and unreviewed. A changed status or finding citation grouping is recorded in `coverage.review_disagreements` and blocks readiness. A recovered missing case also requires manual resolution. Thus a reviewer can correct an output without silently making it ready. Findings returned with `decision_ready=False` are provisional and require review. Original proposals and reviewer outputs are retained; neither is independent factual truth.

`decision_ready` requires a nonempty criterion set, complete source/case/review coverage, no insufficient evidence, agreement between case and predicate review on status and the multiset of finding citation groups, and a supported focused review for every `no_match`. The focused check can downgrade a negative to `insufficient_evidence`; `needs_reassessment` or failure leaves it unverified. Exact finding-group comparison is deliberately conservative: alternative valid corroborating citations may require manual resolution. Agreement does not compare explanation wording or prove semantic equivalence. Different source statuses remain review candidates, not proof of factual contradiction. Source coverage failures still block readiness. No evidence yields deterministic `insufficient_evidence` without a model call. The caller owns any human-review workflow.

### Structured-output migration

The latest contract also requires `stage="consistency_review"` responses using
`ConsistencyDraft`. It receives the original criteria/evidence and final candidates
with their written explanations. This check is deliberately allowed to inspect
the candidate; the earlier `decision_review` remains independent of it. The
LangChain adapter handles the additional stage automatically. A custom callable
that does not support it leaves consistency unverified and cannot make results ready.

`AssessmentConfig.review_consistency` defaults to true. With independent decision
review enabled, it adds one final call per assessed criterion, with the existing
bounded retries for invalid responses. It reports defects without changing the
candidate or agent output. `coverage.unverified_consistency` and
`coverage.inconsistent_explanations` both block readiness. Disabling this check
also blocks readiness; an uncertain or unavailable critique cannot certify a result.
It is skipped when independent decision review is disabled, because readiness is
already unavailable. No new dependencies, orchestration service, or global state.

The critique quotes scope/exception clauses from the criterion or its same-source
context and references problematic explanation
sections by IDs such as `assessment.reason`, `finding:1.reason`, and
`decision_review.condition_reason`. Code validates those IDs against the original
text; the critic does not regenerate explanation quotations. Simple English
`only`, `unless`, and `except` anchors require clause
acknowledgment; they do not decide applicability. Semantic support still depends
on the model, including when the critique returns supported. There is no guarantee
that all explanation errors or shared model mistakes will be detected.

The review also reports `scope_applies`: true for population membership, false for
explicit exclusion, null for unknown membership. Code requires excluded subjects
to have `not_applicable` and unknown membership to have `insufficient_evidence`;
an otherwise supported verdict cannot override a mismatch. The applicability
judgment itself remains model-derived, so this is a consistency constraint rather
than a deterministic underwriting rule engine.

Custom criterion extractors must now provide `reviewed_lines` and each proposed
rule's `classification_quote` (empty for explicit labels). The supplied LangChain
extractor adapts its schema to the input line count. These are model-call contract
changes; the `assess` entry point and agent integration remain unchanged.

For example, the source `A referral denotes a concern.\nRefer unguarded presses.`
can yield this extraction (the adapter assigns the eventual criterion/source IDs):

```json
{
  "complete": true,
  "criteria": [{
    "quote": "Refer unguarded presses.",
    "classification": "concern",
    "classification_quote": "A referral denotes a concern."
  }],
  "issues": [],
  "reviewed_lines": [
    {"line_id": "L1", "rule_quotes": []},
    {"line_id": "L2", "rule_quotes": ["Refer unguarded presses."]}
  ]
}
```

`coverage.complete` retains its source/case/independent-review coverage meaning.
Consistency verification is reported separately and is an additional requirement
for `decision_ready`, even when the coverage count is otherwise complete.

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


### Whole-source review and complementary evidence

The LangChain extraction adapter reviews every nonempty source line, including
known labelled rules. Each line receives a context, outcome-rule, or unresolved
disposition before any criterion is emitted. The provider schema uses required source-line keys and an enum of caller-supplied labels to prevent skipped lines and invented classifications. Code converts this provider response
to the existing `CriterionExtraction` contract and deduplicates known rules.
Operational guidance stays in each criterion's full source context. Ambiguous
outcome rules, missing lines, invalid quotations and unsupported classifications
still fail extraction. Custom extractor call signatures remain unchanged.

The LangChain assessment adapter describes the evidence batch separately from
rule applicability. Case inference reads original evidence and conflict-candidate
IDs; provisional source opinions remain available in the result audit trail.
A changed status after combining complementary sources does not itself require
a conflict label. Required review citations are still enforced; mixed conclusive
source judgments and explicitly unresolved source conflicts still require
resolution. Independent status/finding agreement, full source coverage, negative
evidence review, and final explanation consistency remain readiness requirements.
The consistency schema requests its reasoning before its verdict; contradictory
or uncertain reviews continue to block readiness. No additional model stage or
production dependency is introduced.


The standard negative-evidence review also emits `requirement_kind` (underlying
fact, record existence, or explicit record receipt) and `observation_kind`
(affirmative fact, confirmed absence, nonreceipt only, unavailable, or conflicting).
A supported negative based only on nonreceipt cannot refute an underlying fact or
record existence: code downgrades it to missing evidence and archives the rejected
active explanation. Nonreceipt may refute an explicit submission requirement.
These two fields are optional for legacy custom callables and required by the
standard LangChain provider schema. Custom callables should populate them to use
this guard. The categories are model judgments; citation checks do not prove
that the selected category is semantically correct. No extra review stage is added.
