# First-use document holdout

## Scope and separation

This suite adds six synthetic accounts, 18 expected criteria, and 12 Markdown
documents. It was authored after the production implementation was merged at
`9d746491033df9db6c2aaebc35aeb10d2498439c`. No production code or prompt was
changed to fit these cases. It is held out from implementation tuning at its
first run; it is not independently authored or labeled by underwriters.
After inspecting its results, treat it as a regression set for future changes.

Each application is 1,419–1,452 words; each guideline is 618–642 words. Each
packet contains 2,042–2,084 words. Shared application form prose is
intentional administrative boilerplate, with case-specific facts placed early,
in the middle, and late. This tests a modest increase in document length and
distractors, not book-length contexts, OCR, tables, or production file parsing.

| Case | Guideline form | Main distinctions |
| --- | --- | --- |
| Property | Two bracketed rules, one explicit prose rule | Multiple buildings, replacement exception, approval exception |
| Cyber | Two explicit rules, one implicit rule | 23/24 is not all; date window; adverse referral |
| Fleet | Two bracketed rules, one implicit rule | Unresolved inspection conflict, missing register, rate calculation |
| Manufacturing | Three implicit rules | Active unguarded press, complete hot-work records, dispensing exception |
| Hospitality | Two bracketed rules, one explicit prose rule | Strict boundary, out-of-scope pool, liquidity calculation |
| Contractor | One bracketed rule, two implicit rules | Complete certificates, contractual exception, missing drill records |

There are **11 explicit and seven implicit rules**. The manuals define positive
credit/favorable treatment as strength and referral/adverse treatment/decline as
concern. This mapping is present in the source document, not secretly supplied
to the assessment model as gold. Implicit rule lines do not themselves name the
allowed classification. They intentionally test a documented extraction limit.

## Execution

```powershell
.venv\Scripts\python -m evals.holdout --output evals/results/new-holdout.json
```

The runner uses the existing local `qwen3-coder:30b`, temperature 0, seed 42,
32,768-token context, and 8,192-token output limit. These larger limits accommodate
longer evidence and the evaluation judge; they differ from the earlier short
document run. Existing production assessment defaults, reviews, and retries are
unchanged. No production dependency is added.

Each case gets a fresh agent and explicit application-owned source scope. A live
ReAct agent retrieves raw documents through registered tools; the production
completion middleware performs extraction and assessment. This suite measures
document behavior rather than repeating the earlier checkpointed isolation test.

Gold inventories, expected statuses, support spans, finding groups, and
explanation rationales live in `holdout/cases.json`. They are never sent to the
agent, extractor, or assessor. The runner persists hashes of the corpus, scorer,
tests, and production modules before its first inference and verifies them during
and after execution. Reports refuse overwrites and preserve raw responses,
structured call traces, model digest/settings, package versions, timing, and
errors. The deterministic authoring script is `build_holdout.py`; the evaluator
reads saved documents and does not regenerate them.

## Scoring

### Criterion completeness

The denominator is the full prewritten inventory, including implicit rules.
A criterion must quote the entire expected rule verbatim, retain its expected
classification and source, and remain a separate record. Extra surrounding
context is allowed. Partial rules, duplicates, unrelated extracted rules, and
joined independent rules cannot satisfy complete inventory coverage.

Coverage measures **usable criteria reaching the assessment result**. If the
extractor rejects a source as ambiguous/incomplete and assessment is unavailable,
the end-to-end count is zero; the extraction trace preserves what was proposed.
Thus a failed extraction is distinguishable from a successful empty extraction.

### Decisions, evidence, and readiness

Statuses and atomic finding sets are checked for every expected criterion.
Missing criteria cannot count as correct negatives or abstentions. Mandatory raw
evidence spans must be extracted. Findings match gold support groups one-to-one,
allowing extra corroborating citations. Evidence quotations and locators resolve
against the original documents; enriched finding fields must match the registry.

`unsafe_ready_objective` means production marked a result ready despite failing
document collection, full inventory coverage, source integrity, supporting-span
extraction, status, or finding checks. It can detect a ready assessment of an
incomplete criterion subset even when the production coverage flag is true.
Readiness is also compared with gold: cases with insufficient evidence require a
hold. Correct but conservatively held decisions can fail strict scoring.

### Explanation quality

After saving the untouched assessment, a separate structured evaluation call sees
the prewritten rule, expected status, mandatory evidence, reference rationale,
candidate status, cited evidence, and written explanation. Explanation includes
the final assessment reason, finding reasons, and the review's scope, condition,
exception, and conflict explanations. The judge does not see readiness, pass
flags, earlier attempts, or development results.

Five dimensions receive 0 (wrong/absent), 1 (partial), or 2 (adequate):

1. Correct rule and threshold application.
2. Factual grounding in cited evidence.
3. Treatment of scope, exceptions, contradictions, and uncertainty.
4. Logical connection from facts to conclusion, including necessary arithmetic.
5. Absence of unsupported claims.

A rubric pass requires at least 8/10 and no zero dimension. The judge supplies
exact candidate excerpts and justifications; code validates excerpts and complete
ID/dimension coverage. Explanations absent because no assessment was produced
contribute zero to end-to-end coverage, but are reported separately from poor
produced explanations. Judge errors remain ungraded and cannot produce a strict
pass. Report both passes/all expected criteria and passes/graded explanations.

The judge is the **same local model in a separate call**, not an independent
expert or independent source of truth. Shared errors and leniency are possible.
Saved outputs support a separate qualitative review, which must not silently
replace frozen automatic scores. Explanation failure and unknown grading on ready
outputs are reported separately from objective unsafe-ready failures.

### Strict pass

Requires all objective checks, all explanation passes, complete production
coverage, and correct readiness. The unit tests challenge missing/partial/merged
criteria, forged quotes, combined findings, invalid judge excerpts, missing
dimensions, and an incorrect explanation paired with a correct status.

## Results

The first frozen run and subsequent interpretation are linked from the evaluation
README. This protocol defines the scoring before inspecting live results. Six
accounts are too few to estimate production accuracy or safety, and no repeated
inference claim is made.
