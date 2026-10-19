# Case isolation and prose extraction: before/after

## Results

Seven identical synthetic turns ran under each integration profile. The previous
retained-history profile now enables the production middleware's explicit scope;
the custom-mapper profile retains its earlier filtering and adds the production
scope guard. Both enable the optional prose extractor. The agent still retains
conversation history. These are configuration-aware integration comparisons,
not a claim that unconfigured legacy middleware automatically isolates cases.

| Metric | Retained history → production scope | Custom mapper → mapper + scope guard/extractor |
| --- | --- | --- |
| Documents collected | 7/7 → 7/7 | 7/7 → 7/7 |
| Expected criteria extracted | 6/7 → **7/7** | 6/7 → **7/7** |
| Key raw evidence spans extracted | 11/11 → 11/11 | 11/11 → 11/11 |
| Turns with valid raw-source/locator checks | 7/7 → 7/7 | 7/7 → 7/7 |
| Isolated assessment inputs | 3/7 → **7/7** | 7/7 → 7/7 |
| Cross-case turns without foreign evidence | 0/4 → **4/4** | 4/4 → 4/4 |
| Turns citing foreign-case evidence | 4/7 → **0/7** | 0/7 → 0/7 |
| Correct statuses | 3/7 → **7/7** | 6/7 → **7/7** |
| Correct atomic finding sets | 2/7 → **7/7** | 6/7 → **7/7** |
| Strict end-to-end passes | 1/7 → **5/7** | 4/7 → **5/7** |
| Complete assessment coverage | 6/7 → 7/7 | 7/7 → 6/7 |
| Decision-ready results | 1/7 → 3/7 | 2/7 → 3/7 |
| Unsafe-ready results under fixture scoring | 0 → 0 | 0 → 0 |
| Assessment call attempts | 30 → 24 | 22 → 28 |
| Prose extraction calls | 0 → **1** | 0 → **1** |
| Observed elapsed time | 127.7s → 91.4s | 83.9s → 118.7s |

Model: local `qwen3-coder:30b`, temperature 0, seed 42, 16,384-token context,
4,096-token output limit. Timing includes local execution effects and retries;
it is not a controlled latency benchmark. The extra extractor ran only for the
ordinary-prose guideline. Classified-only sources incurred no extraction call.

## What changed

### Application-owned case scope

`AssessmentScope` carries the case ID and expected source IDs through fresh
invocation context. `scope_from_context` enables the middleware boundary. The
message adapter validates provenance and scopes the ledger before deduplication
and extraction. Missing expected sources fail instead of silently using whatever
history happens to be available. Missing context cannot reuse a previous case's
scope. Custom mappers are checked for foreign or missing expected source IDs.

The source IDs must be immutable and unique across cases/versions; the application
owns that mapping. Shared guidelines can be explicitly included in multiple
scopes. Same-case prior observations remain available: the cyber follow-up still
uses the earlier inventory count and the new protection count together.

This isolates assessment inputs, preserves agent messages and routing, and does
not implement tool authorization or isolate the agent's free-text answer. Those
remain application responsibilities. Legacy behavior is retained when scope is
not configured.

### Conservative prose extraction

Bracketed criteria remain deterministic. With an optional `criterion_extractor`,
additional lines explicitly containing an allowed classification word/phrase
become extraction candidates. A structured model call selects exact quotations;
code checks source membership, allowed and explicitly named classifications,
overlap/reclassification, completeness declarations, and output parsing/truncation.
Source IDs, criterion IDs, labels and full source context are assigned/preserved
by code. Applicant evidence is not supplied to this extraction stage.

The previously missed rule, `A building with a roof older than 20 years is a
concern.`, now retains its exact unbracketed source wording and produces the
expected concern. Both runs marked that correct result ready.

This supports explicit outcome labels in prose, not arbitrary implicit category
inference. A guideline saying only “decline this risk” is not automatically mapped
to `concern`. A wholly implicit source produces no criteria and cannot become
ready; implicit rules inside a mixed source are outside the supported extraction
contract. A model can still omit or misinterpret eligible rules. Exact quotation
and its claimed completeness do not establish semantic completeness.

No dependencies, databases, retrieval systems, or assessment review layers were
added. The assessment core and its readiness gates are unchanged. Extraction is
optional, has no hidden retries, and failures leave assessment unavailable through
the existing middleware error contract.

## Remaining failures

Both profiles held `property_a` and `cyber_d_followup` as non-ready because the
initial case assessment and independent review disagreed on finding citation
groups. Their final statuses and atomic finding sets passed the fixture checks.
The custom-mapper `property_a` run also exhausted source-stage retries, leaving
source coverage incomplete. This is why strict passes remain 5/7 despite correct
final outcomes on all seven turns. Readiness gates were not relaxed to improve
the benchmark score.

## Verification and development traces

- **97 tests pass**, including sync/async checkpointed scope changes, missing
  context, custom-mapper escape rejection, scope-before-deduplication, mixed prose
  and labelled rules, invalid quotations/classifications, incomplete extraction,
  definitions with no eligible candidates, and truncation/parse failures.
- All 14 final results revalidated against `AssessmentResult`; all saved scores
  recomputed exactly; extraction quotations matched their source text.
- Final file hashes matched after the run. Original document/gold bytes, turn
  order, model digest/settings, agent prompt, assessment configuration and core
  assessment module were unchanged from baseline. The scorer function's AST was
  identical to the archived baseline runner. Gold was not sent to either model.
- [First diagnostic](2026-10-19-e2e-scope-extraction.md): interrupted after five
  saved turns because the broad extractor invented concerns from definitions.
- [Second diagnostic](2026-10-19-e2e-scope-extraction-final.md): a completed
  intermediate run, despite its filename. Explicit-label validation correctly
  rejected those inventions but made cyber assessments unavailable. This led to
  deterministic candidate selection and skipping sources with no additional
  eligible prose. Neither diagnostic is included in the final comparison.
- No fixture, gold label, scorer, or assessment readiness condition was changed
  to fit the new outputs. These fixtures now inform development, so the results
  are regression evidence, not held-out underwriting accuracy.

## Artifacts and reproduction

- [Previous report](2026-10-19-e2e-documents-isolation-final.md)
- [Updated report](2026-10-19-e2e-explicit-scope-prose.md)
- [Updated full traces and metadata](2026-10-19-e2e-explicit-scope-prose.json)
- [Integration examples](../../docs/INTEGRATION.md)

From the repository root:

```powershell
.venv\Scripts\python -m evals.e2e --hardened --output evals/results/new-scope-prose-run.json
```

This was one completed final run per profile, not a repeatability study. Seven
short synthetic turn fixtures do not establish production recall, long-document
robustness, OCR quality, or safety. Zero unsafe-ready cases among six ready
outputs is a small-sample observation, not a guarantee.
