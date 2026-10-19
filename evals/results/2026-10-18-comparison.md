# Assessment changes and evaluation comparison

## Implementation

- One criterion assessment now contains a list of independent findings. Each finding has a subject, supporting evidence IDs, and its own explanation. Postprocessing assigns result-local finding IDs and expands the exact citations and criterion classification.
- Status must agree with an explicit basis. Scope exclusion, missing evidence, negative evidence, an applicable exception, a match, and unresolved conflict have distinct bases. Matched assessments require findings; nonmatched assessments forbid them.
- Case reconciliation receives conflict candidates from differing decisive source judgments and source-reported unresolved conflicts. Both directions are covered. A case decision changing a decisive source judgment also triggers review. Required opposing evidence cannot be omitted from the case citations.
- Reviews distinguish unresolved conflict, supported resolution, and different subject/time scope. Unresolved conflict abstains for the entire criterion and emits no findings. Resolved/different-scope reviews remain in the audit trail. Invalid responses receive feedback during bounded retries.
- The final prompt reinforces removal of superseded findings and asks for the evidence-based conclusion before classification. No additional dependencies or model calls beyond existing bounded retries were introduced.

Custom model callables must migrate to the required `basis`, `findings`, and `conflict` fields. The LangChain adapter automatically uses the new schema; the LangGraph state contract and assessment input records are unchanged. See [integration guidance](../../docs/INTEGRATION.md#structured-output-migration).

## Controlled comparison

All runs used the same eight cases, gold labels, scoring function, local Ollama model digest (`qwen3-coder:30b`, Q4_K_M), temperature 0, seed 42, context limit 8,192, output cap 4,096, and assessment retry configuration. The dataset SHA-256 is `634b4acbb3c1083584409b71cf2fc944b210f324adee90dd9e88a8d502970fc7`. Prompt/schema/implementation changes were the intervention. The updated traces include implementation hashes as well as prompt/model metadata. These cases informed the changes and are a development set, not a held-out benchmark.

| Metric | Original baseline | First update | Final implementation |
| --- | ---: | ---: | ---: |
| Strict cases passed | 3/8 | 7/8 | **7/8** |
| Correct final statuses | 3/8 | 7/8 | **7/8** |
| Required gold evidence cited | 5/10 | 10/10 | **10/10** |
| Accepted reference/provenance checks | 18/18 | 38/38 | **36/36** |
| False-positive findings in six nonmatched gold cases | 1 | 2 | **0** |
| Correct independent findings in the two matched cases | 0/4 | 4/4 | **4/4** |
| Complete source/case coverage | 6/8 | 8/8 | **8/8** |
| Rejected responses | 9 | 0 | **2, both recovered** |
| Model calls | 30 | 21 | **25** |
| Elapsed model/assessment time | 73.2s | 51.2s | **40.3s** |

Latency includes differing model warm-up/cache conditions and is not a controlled performance benchmark. Reference-check denominators vary with accepted citations; passing them does not prove correctness.

| Category | Baseline | Final | Final observation |
| --- | ---: | ---: | --- |
| Unrelated evidence | 1/2 | 1/2 | Financial evidence correctly abstains; missing training records still incorrectly produce `no_match`. |
| Contradictions | 1/2 | 2/2 | Unresolved conflict cites both sides, abstains, and is not decision ready; an explicit correction resolves the concern. |
| Exceptions | 1/2 | 2/2 | Correctly applies the roof exception and identifies the fryer scope exclusion as `not_applicable`. |
| Multiple findings per criterion | 0/2 | 2/2 | Two independent concerns from one source and two independent strengths across sources, with separate citations. |

## What remains unresolved

The final failed training case says missing records mean the condition cannot be satisfied, incorrectly choosing `condition_not_met`/`no_match`. Both fields agree, so structural validation accepts it and `decision_ready` remains true. The explanation is a semantic error that reference and enum validation cannot detect.

The first update passed the training case but mishandled the explicit correction: it correctly described supersession while emitting two findings, including an invalid finding based on operational equipment. The final prompt/schema-order refinement fixed that case but regressed training. Both runs are retained to avoid implying that the seven successes are stable across prompt variants.

Two final-run validation failures recovered through existing bounded retries: a source returned a basis inconsistent with its status, and the roof-exception case initially omitted an explicit conflict review. The trace retains both failures.

Conflict detection uses source judgments and cannot deterministically discover a contradiction that all model assessments miss. A claimed resolution remains a model judgment even when both sides are cited. Multiple findings are representable, but semantic duplicate detection, completeness, and interpretation still require evaluation. Material unresolved conflict conservatively suppresses all findings for its criterion, including any otherwise unaffected partial matches.

All **46 tests pass**, including seven new API tests for independent findings, schema consistency, bidirectional review, unresolved conflicts, compatible different subjects, retry feedback, and within-source conflict review. Unit tests use fixed responses; the eight recorded scenarios use the actual local model. Next validation should use independent underwriter-reviewed cases and repeated runs rather than further treating these eight cases as an accuracy estimate.

## Preserved artifacts

- [Original baseline report](2026-10-18-qwen3-coder-30b.md) and [trace](2026-10-18-qwen3-coder-30b.json)
- [First update report](2026-10-18-qwen3-coder-30b-updated.md) and [trace](2026-10-18-qwen3-coder-30b-updated.json)
- [Final report](2026-10-18-qwen3-coder-30b-final.md) and [trace](2026-10-18-qwen3-coder-30b-final.json)
