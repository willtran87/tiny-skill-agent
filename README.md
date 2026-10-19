# Tiny skill agent

A small LangChain `create_agent` / LangGraph ReAct example with local Markdown skills, tagged tools, and an optional provenance-aware underwriting assessment. No database or vector store is required.

## Repository layout

```text
src/tiny_skill_agent/
  agent.py               ReAct agent, skill tools, and CLI
  assessment.py          Portable criteria/evidence API, schemas, reconciliation
  adapters.py            LangChain messages/models and LangGraph state node
  evidence.py            Tool metadata, provenance, evidence spans, validation
  sample_skills/         Bundled example SKILL.md files
notebooks/
  agent_starter.ipynb    Configurable Ollama/OpenAI underwriting example
docs/
  DESIGN.md              Data structures, flow, and trust boundaries
  INTEGRATION.md         Direct API and framework integration examples
  RESEARCH.md            Related papers and evaluation guidance
tests/                   Provenance and assessment tests
evals/                   Synthetic cases, local-model runner, and saved results
```

## Install and run

From the repository root:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python -m pip install -e ".[notebook]"
.venv\Scripts\tiny-agent --provider ollama --model llama3.1:latest "Count the words in: local models can call tools"
```

The CLI defaults to OpenAI (`gpt-4.1-mini`); set `OPENAI_API_KEY` for that provider. Set `OPENAI_MODEL` or `OLLAMA_MODEL`, or pass `--model`, to choose another model. Run `tiny-agent` without a prompt for interactive chat. `python -m tiny_skill_agent` is equivalent to the CLI.

Open [notebooks/agent_starter.ipynb](notebooks/agent_starter.ipynb) with the project's `.venv` kernel. It works when launched from the repository root or the `notebooks` folder. Ollama must be running and the configured models must be installed. The example uses `llama3.1:latest` for tool gathering and `qwen3-coder:30b` for structured assessments. Set `MODEL_CONFIG["assessment_model"] = None` to reuse the tool model.

## Underwriting output

The notebook assigns short IDs to observed sources (`S`), labeled criteria (`C`), and data evidence spans (`E`). It assesses each observed data source against each observed criterion, then reconciles the case. Each assessment has a reason, evidence IDs, and one of four statuses:

| Status | Meaning |
| --- | --- |
| `matched` | Evidence supports a strength or concern criterion. |
| `no_match` | Relevant evidence shows an applicable criterion is not met. |
| `insufficient_evidence` | Available evidence cannot decide the criterion. |
| `not_applicable` | Evidence shows the criterion's stated scope excludes the case. |

`result["structured_response"]` contains accepted case findings with one or more resolved fact citations. One criterion assessment can contain multiple findings, each with its own subject, citations, and reason. `result["criterion_assessments"]` contains all four statuses plus a validated decision basis. Source assessments are provisional; case reconciliation reviews opposing judgments in both directions and retains them in `disagreements`. Coverage exposes missing assessments and unresolved conflicts. `decision_ready` is false when coverage is incomplete, evidence is insufficient, criteria are absent, or conflicts remain unreviewed/unresolved. Citation and consistency checks do not prove the model's interpretation, conflict resolution, or upstream data is correct. Custom model callables need the updated response fields described in [INTEGRATION.md](docs/INTEGRATION.md#structured-output-migration).

See [docs/DESIGN.md](docs/DESIGN.md) for the schema and flow, and [docs/RESEARCH.md](docs/RESEARCH.md) for related research.

Every criterion receives an independent review of the original evidence, including matches, exclusions, and abstentions. The model quotes the criterion trigger and evaluates scope, condition truth, and exceptions; code derives status. Missing/invalid reviews and disagreements about status or finding citation groups block `decision_ready`. The reviewer can correct the displayed result, but a changed result requires manual resolution. Inspect `pre_review_assessments`, `decision_reviews`, and `coverage.review_disagreements`; findings are provisional whenever readiness is false. This uses the same model with a separate prompt and adds no dependencies. Agreement is not a guarantee of correctness.

Final `no_match` judgments retain a focused evidence-sufficiency challenge: missing information must not become a confirmed negative just because two general passes agree. Its verdict appears in `no_match_reviews`; failed, inconclusive, or disabled negative checks block readiness for those decisions.

## Use in an existing application

The notebook delegates to a reusable API with no notebook globals:

```python
from tiny_skill_agent import AssessmentConfig, assess

result = assess(
    criteria=criteria, evidence=evidence, model=assessment_callable,
    config=AssessmentConfig(batch_size=1), request="Review this case.",
)
```

`criteria` and `evidence` are typed records or matching dictionaries; `model` is a callable accepting a payload and returning structured assessments. Classification labels are supplied by the caller. `inputs_from_messages` converts observed LangChain tool messages, `make_langchain_assessor` wraps structured chat models, and `make_assessment_node` adapts the API to dictionary state in a LangGraph. See [docs/INTEGRATION.md](docs/INTEGRATION.md) for complete examples and compatibility boundaries. No additional orchestration framework is introduced.

## Add a skill or tool

The included examples live in [src/tiny_skill_agent/sample_skills](src/tiny_skill_agent/sample_skills). Each skill is a directory containing a `SKILL.md` with `name` and `description` frontmatter. Use `--skills-dir` for your own skills. In the notebook, set `SKILLS_DIR` before creating the tools.

Decorate a typed Python function with `@tool`, declare how its output should be used, and include it in the agent's tool list:

```python
from langchain.agents import create_agent
from tiny_skill_agent.evidence import EvidenceMetadataMiddleware, tag_tool

tag_tool(my_data_tool, "data")
tag_tool(my_guideline_tool, "directive")
tools = [my_data_tool, my_guideline_tool]
agent = create_agent(model, tools=tools, middleware=[EvidenceMetadataMiddleware(tools)])
```

The middleware adds `_meta` to successful tool results. `collect_evidence` checks the observed call and registered tag before accepting a result as data or a directive. A classified criterion can come from a skill, directive tool, or system prompt.

## Verify

See [evals/README.md](evals/README.md) for the eight-case assessment evaluation covering unrelated evidence, contradictions, exceptions, and multiple findings per criterion, including a saved local-model baseline. Run it against Ollama with `.venv\Scripts\python -m evals.run`.

The larger [32-case repeated evaluation](evals/UNSEEN_EVALUATION.md) adds fresh synthetic scenarios and three fixed-setting runs. It exposes substantial accuracy/readiness gaps beyond the small development set; full traces and a manual failure analysis are preserved.

See the subsequent [all-outcome review comparison](evals/results/2026-10-18-review-comparison.md) for the readiness changes, repeated regression runs, remaining errors, and inference-cost tradeoff.

```powershell
.venv\Scripts\python -m unittest discover -s tests
```
