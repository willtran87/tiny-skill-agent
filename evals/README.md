# Assessment evaluation

For the larger fresh set and repeated-run results, see [UNSEEN_EVALUATION.md](UNSEEN_EVALUATION.md): 32 additional synthetic scenarios, three evaluations with fixed settings, and separate accuracy/readiness/consistency metrics.

Eight small, hand-authored synthetic cases exercise the reusable assessment API:

| Category | Cases | Expected behavior |
| --- | --- | --- |
| Unrelated evidence | Financials unrelated to training; lexical overlap with wrong training population | `insufficient_evidence`, zero findings |
| Contradictions | Equally authoritative conflicting inspections; explicit correction | Abstain on unresolved conflict; honor a documented correction |
| Exceptions | Roof-age exception; explicit equipment scope exclusion | Distinguish `no_match` from `not_applicable` |
| Multiple findings per criterion | Two roofs in one source; two protected warehouses across sources | Preserve two independent concern/strength records |

The criteria are invented for testing, not actual underwriting guidance. Gold labels were authored before the model run and have not been reviewed by an underwriter. These cases are a regression starting point, not a production accuracy estimate.

## Run

From the repository root, using the existing project environment and a running Ollama instance:

```powershell
.venv\Scripts\python -m evals.run --model qwen3-coder:30b
```

Options: `--base-url`, `--cases`, and `--output evals/results/new-run.json`. Existing result files are never overwritten. The default creates timestamped JSON and Markdown reports. Each completed case is saved incrementally; an interrupted report remains marked `running`. Model/parse failures are handled by the API's bounded retries and appear in coverage errors and the call trace.

The runner uses temperature 0, seed 42, an 8,192-token context, a 4,096-token output cap, and the production assessment prompt/configuration. These settings reduce variability but do not guarantee deterministic model inference. Every case is independent. Gold expectations and rationale are used only by the scorer, never sent to the model.

## Scoring and audit trail

- **Status accuracy:** final case status against the gold label.
- **Required evidence coverage:** whether final case citations include the gold supporting spans. This is an ID-based check, not proof of semantic support.
- **Atomic findings:** exact citation sets of distinct final finding records against the gold records. For these deliberately simple fixtures, each qualifying building/warehouse has one distinct supporting span. Combined records, extra findings, missing records, or extra citations fail this strict check. Broader real-world fixtures may require alternative acceptable evidence sets.
- **Reference integrity:** accepted case/source citation IDs, source boundaries, and deterministic finding source/quote/locator/classification expansion. Invalid model attempts remain visible in the trace even if retries recover.
- **Strict pass:** all of the above plus complete API coverage, and expected readiness when the dataset labels it. The original eight cases and four contrast cases have no readiness gold; the 32-case set does. A correct status held for manual review can therefore fail the larger set's strict check.

The saved JSON includes inputs, gold expectations, final results, per-call payloads and structured outputs/errors, elapsed times, model tag/digest/settings, Ollama/package versions, Git revision/worktree status, dataset hash, and assessment prompt hash. Markdown includes expected rationales and model explanations for human review. Explanations are not automatically graded for semantic correctness.

This suite bypasses ReAct gathering, tool metadata, source extraction, and document parsing. It does not test long-context recall, missing tool calls, arbitrary document normalization, or real underwriting outcomes. The original schema allowed only one finding per criterion; the updated API supports a nested list. Gold cases and scoring remain unchanged across the recorded runs. The eight cases have informed development, so later scores are development-set regression results, not held-out accuracy.

## Recorded run

See [the baseline report](results/2026-10-18-qwen3-coder-30b.md) and [full JSON trace](results/2026-10-18-qwen3-coder-30b.json).

### Updated implementation results

The [all-outcome review comparison](results/2026-10-18-review-comparison.md) covers the subsequent readiness changes and repeated larger evaluation. It also retains diagnostic iterations and explains the added manual-review holds.

The earlier [evidence-sufficiency comparison](results/2026-10-18-sufficiency-comparison.md) records **8/8** original cases passing, plus **4/4** additional contrast cases. The previously incorrect missing-records negative was downgraded by a focused review to `insufficient_evidence` with `decision_ready=False`. Affirmative negative evidence remained `no_match` and decision ready. These prior runs remain preserved.

See [the final report](results/2026-10-18-qwen3-coder-30b-final.md), [final JSON trace](results/2026-10-18-qwen3-coder-30b-final.json), and [comparison](results/2026-10-18-comparison.md). The final implementation passed **7/8**, up from **3/8**, with both multiple-finding cases passing and zero false-positive findings in the six nonmatched gold cases. The model still misclassified missing training records as `no_match` instead of `insufficient_evidence`; that wrong status also remained decision ready. Structural validation does not establish semantic correctness.

The [first updated run](results/2026-10-18-qwen3-coder-30b-updated.md) is also preserved. It passed 7/8 but incorrectly emitted two concerns after recognizing an explicit correction. The final revision strengthened removal of superseded findings and requested an explanation before status assignment. It fixed the correction case but regressed the missing-records case. This sensitivity reinforces the need for independent cases, repeat runs, and human review before estimating production accuracy.

### Baseline observations

The local `qwen3-coder:30b` run passed **3/8** strict fixtures, with **3/8** correct final statuses and **5/10** required gold evidence references. It made 30 model calls in approximately 73 seconds, including initial model loading. All 18 checks on accepted references/provenance passed; nine responses were rejected for duplicate criterion IDs.

| Category | Strict passes | Observation |
| --- | --- | --- |
| Unrelated evidence | 1/2 | Correctly abstained on financials; incorrectly treated missing forklift training records as proof the strength condition was not met. |
| Contradictions | 1/2 | Honored an explicit correction; ignored the equally authoritative opposing inspection in the unresolved case and emitted a concern. |
| Exceptions | 1/2 | Applied the roof exception; described the scope exclusion correctly but labeled it `no_match` instead of `not_applicable`. |
| Multiple findings | 0/2 | Identified the independent qualifying buildings/warehouses in raw responses, but repeated C1. The API rejected those responses and returned zero findings for both cases. |

Human review of the stored explanations confirms the three passing cases' intended reasoning. The failed scope case has a reasonable explanation paired with the wrong status; the unrelated training case explicitly mistakes missing records for contradictory evidence. These observations are a manual review of this run, not a separate blinded semantic evaluation.

In the original baseline, the unresolved contradiction was marked `decision_ready=True`, as were the two incorrect `no_match` cases. The original disagreement flag only caught source matches overturned by a nonmatched case decision; it did not flag a case match ignoring a conflicting source nonmatch. The corrected inspection case was appropriately adjudicated but retained `decision_ready=False` because its source match was overturned. Consequently the readiness flag must not be interpreted as correctness or semantic confidence.

The baseline suggested multiple atomic findings inside one criterion assessment, conflict detection in both directions, and stronger status distinctions. Those changes are implemented in the updated API; the original baseline files are preserved.

Scorer tests run with the normal test suite:

```powershell
.venv\Scripts\python -m unittest discover -s tests
```

The additional contrast set is run separately so the original eight-case comparison stays unchanged:

```powershell
.venv\Scripts\python -m evals.run --cases evals/sufficiency_cases.json
```
