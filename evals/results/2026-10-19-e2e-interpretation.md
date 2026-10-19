# Raw-document extraction and multi-turn case isolation

## Scope

Seven synthetic turns were run under each of two configurations with local
`qwen3-coder:30b`: 14 evaluated turns total. The live agent retrieved raw documents
through tagged tools, then the production extractor and completion middleware
ran the assessment. No pre-extracted criteria/evidence or gold labels were passed
to either model stage. No production code or assessment prompts were changed.

The fixtures cover Markdown applications, prose reports, nested JSON, a tool
guideline, a skill guideline, two independent findings, missing evidence, case
switches, and follow-up evidence that needs an earlier same-case document. A
separate ordinary-prose guideline deliberately lacks bracketed classification.
These are short invented examples, not actual insurance guidelines or
independently labeled underwriting cases.

## Results

| Metric | Default retained history | Explicit case-scoped mapper |
| --- | --- | --- |
| Documents collected | 7/7 | 7/7 |
| Expected criterion extracted | 6/7 | 6/7 |
| Key raw evidence spans extracted | 11/11 | 11/11 |
| Turns with valid raw-source/locator checks | 7/7 | 7/7 |
| Turns with isolated assessment inputs | 3/7 | 7/7 |
| Turns after a switch without foreign evidence | 0/4 | 4/4 |
| Turns citing another case's evidence | 4/7 | 0/7 |
| Correct final status | 3/7 | 6/7 |
| Correct atomic finding sets | 2/7 | 6/7 |
| Strict end-to-end pass | 1/7 | 4/7 |
| Decision-ready results | 1/7 | 2/7 |
| Unsafe ready under this scorer | 0 | 0 |
| Assessment call attempts | 30 | 22 |
| Measured time | 127.7 seconds | 83.9 seconds |

The profiles use separate checkpointed conversations and live model executions.
This is an integration comparison, not a controlled estimate of model accuracy
or speed. The mapper's reduced evidence also changes the assessment payloads.
The 16,384-token context differs from the earlier assessment-only benchmark.

## What failed and why

### Default extraction has no automatic case boundary

On both case switches, earlier applicant documents remained in assessment inputs
and were cited in final assessments/findings. The default profile incorrectly
returned `matched` for both new applicants with missing data, and retained
foreign findings after follow-ups. Those provisional outputs were non-ready,
but the incorrect findings still existed. Citation validity did not protect
against citing the wrong applicant's authentic evidence.

This is a documented integration requirement, now demonstrated end to end:
the default middleware reads retained messages. It does not infer a trusted case
boundary from the latest user message. Merely clearing the old `assessment`
state field does not clear or isolate the underlying evidence.

### Explicit selection isolated assessment and retained useful history

The evaluation's `scoped_messages` mapper selects tool results by application-owned
document IDs. It excludes other cases while retaining earlier documents of the
active case. The protected-account follow-up correctly cited both the original
12-account inventory and the new 12-account protection count. The roof follow-up
correctly changed missing evidence to `no_match` once a five-year roof age arrived.

All six classified-guideline turns had correct statuses and atomic finding sets
under this configuration. The property multiple-finding turn and cyber follow-up
were held as non-ready because the initial assessment and reviewer used different
finding citation groups. Thus only four turns passed the strict score, which also
requires expected readiness. Those conservative holds are distinct from wrong
underwriting findings.

This mapper is an evaluation integration example, not an automatically enabled
production feature. It filters assessment inputs, not the agent's conversation
history or free-text response. Tools separately enforce the active document
allowlist. The application owns the case/document mapping.

### Arbitrary prose criteria are not extracted

Both profiles retrieved the ordinary-prose guideline but extracted zero criteria:
`build_criterion_inventory` currently recognizes classified lines such as
`[concern] ...`. The missing criterion caused no finding and a non-ready result.
This remains a failed end-to-end case, not a correct abstention. The suite did not
insert labels or introduce an LLM parser to hide this limitation.

## Verification and audit

- All 14 saved results validated against `AssessmentResult`.
- All saved scores recomputed exactly from the raw documents and fixture gold.
- Dataset, document, and implementation hashes were unchanged throughout the
  completed run and verified afterward.
- All 85 unit/integration/scoring tests passed.
- The initial diagnostic run stopped after two saved turns because the Windows
  console could not print a model-generated Unicode character. Its failed report
  is preserved. Logging was made ASCII-safe before the complete restart; no
  fixture, gold label, assessment prompt, or production code was altered.
- After completion, a reporting label was corrected: LangChain callbacks include
  nested assessment responses. The historical JSON key `agent_calls` therefore
  contains **all successful LLM responses**, not just ReAct calls. The corrected
  renderer labels these accurately; new runs use `model_responses`. Saved model
  outputs and scores are unchanged. The exact runner used for the completed run
  is preserved as `2026-10-19-e2e-frozen-runner.py.txt` for hash verification.

## Interpretation limits

This demonstrates real integration failures and a successful explicit isolation
strategy on a small fixture set. It does not establish production accuracy,
general natural-language criterion extraction, OCR/PDF parsing, long-context
recall, or isolation of the agent's generated prose. Supporting-span recall is
measured at extraction; final findings require their gold supporting spans, but
nonmatched explanations are not semantically judged. Zero unsafe-ready cases
among only three ready outputs is not a safety guarantee.

The next changes justified by these results are an explicit application-owned
case boundary in integration, and a separately validated extraction path for
ordinary-prose guidelines. More review calls alone would not fix either boundary.

## Artifacts

- [Completed report](2026-10-19-e2e-documents-isolation-final.md)
- [Completed JSON traces](2026-10-19-e2e-documents-isolation-final.json)
- [Failed diagnostic report](2026-10-19-e2e-documents-isolation.md)
- [Frozen runner](2026-10-19-e2e-frozen-runner.py.txt)
