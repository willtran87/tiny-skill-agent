# Research library: evidence-grounded underwriting agents

Last reviewed: 2026-09-25. This is a working bibliography for the agent described in [DESIGN.md](DESIGN.md). It prioritizes original papers, published proceedings, and official evaluation or insurance guidance. Paper findings are summarized briefly; the **application** notes are proposed uses for this project, not results established by those papers.

## Research question

Can an agent recover the concerns and strengths that underwriters would identify from loose source data, apply the relevant criteria, and provide supportable source attribution? The current notebook validates that quoted text appeared in observed sources and tracks criterion coverage. We still need to measure **finding recall, judgment correctness, multi-source synthesis, and explanation support** against expert review.

The insurance papers below are relevant but do not directly answer that question. In particular, **UNDERWRITE** evaluates outcomes of commercial property and casualty underwriting tasks. Our starter's reserves, payments, debt-to-income, and income examples resemble credit underwriting. Results should not be transferred between those domains without a task-specific evaluation.

## Read first

1. **UNDERWRITE** for a realistic tool-using underwriting agent environment and its evaluation pitfalls.
2. **AttributionBench** and **ALCE** for the difference between an existing citation and a citation that supports a claim.
3. **MEBench** and the cross-document retrieval paper for findings that require combining sources.
4. **Agentic Benchmark Checklist** and **Evidence-Centered Benchmark Design** before designing our own gold set.

## Insurance and underwriting

### 1. UNDERWRITE: Benchmarking Agents in Insurance Underwriting Environments

**Citation:** Amanda Dsouza, Ramya Ramakrishnan, Charles Dickens, Bhavishya Pohani, and Christopher M. Glaze. 2026. [*Benchmarking Agents in Insurance Underwriting Environments*](https://arxiv.org/abs/2602.00456). arXiv:2602.00456v1, preprint. [Full text](https://arxiv.org/html/2602.00456v1).

**What it studies:** An expert-designed, multi-turn commercial property and casualty underwriting environment. It includes proprietary-style free-text guidelines, tables, tool metadata, noisy interfaces, imperfect simulated users, and tasks such as appetite and qualification decisions. The authors evaluate 13 frontier models on 300 tasks, including answer correctness, tool errors, and inappropriate questions. They report domain-knowledge hallucinations despite tool access and reliability gaps across repeated runs.

**Application to this project:** Use its environment design and error taxonomy when building realistic agent tests. Keep tool behavior, guideline access, and user follow-up quality in scope, alongside final findings. The paper's task outcome score is **not** a measure of recall for individual strengths and concerns; we need that measure separately.

**Transfer limit:** Commercial insurance task decisions, synthetic applicants, and simulated users differ from our current example and from real case files. Publication status is a preprint as of this review.

### 2. CUFEInse: an insurance LLM evaluation framework

**Citation:** Hua Zhou, Bing Ma, Yufei Zhang, and Yi Zhao. 2025. [*Design, Results and Industry Implications of the World's First Insurance Large Language Model Evaluation Benchmark*](https://arxiv.org/abs/2511.07794). arXiv:2511.07794v1, preprint.

**What it studies:** CUFEInse v1.0 covers five dimensions, 54 sub-indicators, and 14,430 questions spanning insurance knowledge, industry understanding, compliance, agent application, and reasoning; the authors evaluate 11 models.

**Application:** A reference for a broader evaluation taxonomy, especially reasoning and compliance dimensions that a citation-only test misses. Examine task definitions before borrowing scores or items.

**Transfer limit:** Broad insurance knowledge evaluation, not a validated benchmark of finding-level recall from messy application files.

### 3. AEPC-QA: insurance knowledge with and without retrieval

**Citation:** David Beauchemin and Richard Khoury. 2026. [*Benchmarking Large Language Models for Quebec Insurance: From Closed-Book to Retrieval-Augmented Generation*](https://arxiv.org/abs/2603.07825). arXiv:2603.07825v1; workshop paper noted on arXiv.

**What it studies:** A private gold set of 807 multiple-choice questions derived from Quebec insurance certification handbooks, comparing 51 models in closed-book and retrieval-augmented settings. The paper reports that retrieval helps some models and distracts others.

**Application:** Test whether adding guidelines actually improves our model's criterion use, rather than assuming that more source context helps. Compare identical cases with and without the relevant guideline evidence.

**Transfer limit:** Insurance knowledge questions and a private dataset, not end-to-end underwriting findings.

### 4. Document extraction followed by case synthesis in insurance claims

**Citation:** Robert D. Lieberthal and colleagues. 2026. [*Leveraging LLMs for Unstructured Claims Data Analysis*](https://arxiv.org/abs/2606.06089). arXiv:2606.06089v1, preprint. [Author-linked code](https://github.com/mdsight/llm-claims-analysis).

**What it studies:** A proof of concept separating document-level extraction from claim-level synthesis, with an audit trail and expert review of selected variables. The paper reports a limited validation on synthetic claims and real claims documents.

**Application:** Closest insurance-domain architectural analogue to our **per-source assessment → case-level synthesis** flow. Compare its intermediate records and audit trail with our `EvidenceLedger` and findings schema.

**Transfer limit:** Claims/actuarial variable extraction is different from underwriting strengths and concerns; the reported validation is small.

## Attribution and citation support

### 5. ALCE: answers with citations

**Citation:** Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen. 2023. [*Enabling Large Language Models to Generate Text with Citations*](https://aclanthology.org/2023.emnlp-main.398/). EMNLP 2023. DOI: [10.18653/v1/2023.emnlp-main.398](https://doi.org/10.18653/v1/2023.emnlp-main.398).

**What it studies:** An end-to-end retrieval and citation benchmark with separate measures for fluency, answer correctness, and citation quality. Its results show that plausible answers may lack complete citation support.

**Application:** Keep **finding correctness** and **citation support** as separate metrics. An exact quote and source ID can be valid while the criterion–fact match is wrong.

### 6. AttributionBench: evaluating whether a cited source supports a claim

**Citation:** Yifei Li, Xiang Yue, Zeyi Liao, and Huan Sun. 2024. [*AttributionBench: How Hard is Automatic Attribution Evaluation?*](https://aclanthology.org/2024.findings-acl.886/). Findings of ACL 2024. DOI: [10.18653/v1/2024.findings-acl.886](https://doi.org/10.18653/v1/2024.findings-acl.886).

**What it studies:** Benchmarks automatic judgments of whether cited evidence fully supports generated claims. The authors report substantial errors even for strong model-based attribution evaluators, often involving nuanced information.

**Application:** If we add a semantic support checker, evaluate it against human judgments. Do not treat an automated entailment score as deterministic proof that a reason follows from its criterion and fact.

### 7. LAB: attribution in long documents

**Citation:** Jan Buchmann, Xiao Liu, and Iryna Gurevych. 2024. [*Attribute or Abstain: Large Language Models as Long Document Assistants*](https://aclanthology.org/2024.emnlp-main.463/). EMNLP 2024. DOI: [10.18653/v1/2024.emnlp-main.463](https://doi.org/10.18653/v1/2024.emnlp-main.463).

**What it studies:** Six long-document tasks with attribution. The authors compare citation during generation with retrieval-supported approaches and find that evidence quality is less predictive of answer quality for complex responses.

**Application:** Evaluate whether our model should select evidence before composing a reason. A well-formed citation alone should not stand in for a correct, substantive explanation.

### 8. Select evidence before writing

**Citation:** Aviv Slobodkin, Eran Hirsch, Arie Cattan, Tal Schuster, and Ido Dagan. 2024. [*Attribute First, then Generate: Locally-attributable Grounded Text Generation*](https://aclanthology.org/2024.acl-long.182/). ACL 2024. DOI: [10.18653/v1/2024.acl-long.182](https://doi.org/10.18653/v1/2024.acl-long.182).

**What it studies:** A pipeline that first selects source segments, then plans and generates text grounded in those segments. It reports more concise attribution and less human verification effort on summarization and long-form QA.

**Application:** A candidate pattern for underwriting: select criterion and fact spans first, validate them, then generate the reason. This would make the reason depend on chosen evidence more explicitly than a single free-form synthesis call.

### 9. Multiple sources supporting one answer

**Citation:** Nilay Patel, Shivashankar Subramanian, Siddhant Garg, Pratyay Banerjee, and Amita Misra. 2024. [*Towards Improved Multi-Source Attribution for Long-Form Answer Generation*](https://aclanthology.org/2024.naacl-long.216/). NAACL 2024. DOI: [10.18653/v1/2024.naacl-long.216](https://doi.org/10.18653/v1/2024.naacl-long.216).

**What it studies:** Attribution for answers that require reasoning over more than one evidence source, including multiple citations for a sentence.

**Application:** Our current finding schema supports multiple evidence citations per record. Benchmark whether the model selects every source needed for cross-document discrepancies and whether derived facts need an explicit transformation record.

## Long context and cross-source reasoning

### 10. Lost in the Middle

**Citation:** Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024. [*Lost in the Middle: How Language Models Use Long Contexts*](https://aclanthology.org/2024.tacl-1.9/). TACL 12. DOI: [10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638).

**What it studies:** In multi-document QA and key-value retrieval, model performance often worsens when relevant information is in the middle of long input.

**Application:** A reason to benchmark our per-source pass and case-level reconciliation against a single full-context pass, not proof that atomic processing improves underwriting recall.

### 11. Context length can hurt despite perfect retrieval

**Citation:** Yufeng Du and colleagues. 2025. [*Context Length Alone Hurts LLM Performance Despite Perfect Retrieval*](https://aclanthology.org/2025.findings-emnlp.1264/). Findings of EMNLP 2025.

**What it studies:** Controlled experiments on five models found performance degradation as input length grew even when relevant information was supplied. The tested tasks were math, QA, and coding.

**Application:** Measure both input length and finding recall. Supplying every source inside a supported context window does not by itself guarantee use of every source.

### 12. MEBench: cross-document completeness and attribution

**Citation:** Teng Lin, Yuyu Luo, Honglin Zhang, Jicheng Zhang, Chunlin Liu, Kaishun Wu, and Nan Tang. 2025. [*MEBench: Benchmarking Large Language Models for Cross-Document Multi-Entity Question Answering*](https://aclanthology.org/2025.emnlp-main.77/). EMNLP 2025. DOI: [10.18653/v1/2025.emnlp-main.77](https://doi.org/10.18653/v1/2025.emnlp-main.77).

**What it studies:** Questions requiring comparison, statistics, and relationships across documents. It proposes an entity-attributed measure that considers both extraction completeness and attribution validity.

**Application:** Model our case-level evaluation on separate axes: did we find all relevant inputs, combine them correctly, and cite every input needed for the conclusion?

### 13. Multi-hop evidence retrieval across documents

**Citation:** Keming Lu, I-Hung Hsu, Wenxuan Zhou, Mingyu Derek Ma, and Muhao Chen. 2023. [*Multi-hop Evidence Retrieval for Cross-document Relation Extraction*](https://aclanthology.org/2023.findings-acl.657/). Findings of ACL 2023. DOI: [10.18653/v1/2023.findings-acl.657](https://doi.org/10.18653/v1/2023.findings-acl.657).

**What it studies:** Relations that are not stated in one document and need retrieved evidence paths spanning documents.

**Application:** Supports adding a second pass over collected facts for contradictions, derived ratios, and exceptions. An atomic per-tool pass cannot resolve those relationships alone.

## Designing and governing our evaluation

### 14. Agentic Benchmark Checklist

**Citation:** Yuxuan Zhu and colleagues. 2025. [*Establishing Best Practices in Building Rigorous Agentic Benchmarks*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/f316275b44ee2de533102913828a8107-Abstract-Datasets_and_Benchmarks_Track.html). NeurIPS 2025, Datasets and Benchmarks Track. DOI: [10.52202/085713-5547](https://doi.org/10.52202/085713-5547).

**What it studies:** Benchmark setup and reward-design failures that can misstate agent performance; proposes the Agentic Benchmark Checklist.

**Application:** Audit our scoring code and failure handling. In particular, do not count an empty finding list or `coverage.complete` as success merely because every criterion received a `no_match` status.

### 15. Evidence-Centered Benchmark Design

**Citation:** Yu Lu Liu, Su Lin Blodgett, Jackie Cheung, Q. Vera Liao, Alexandra Olteanu, and Ziang Xiao. 2024. [*ECBD: Evidence-Centered Benchmark Design for NLP*](https://aclanthology.org/2024.acl-long.861/). ACL 2024. DOI: [10.18653/v1/2024.acl-long.861](https://doi.org/10.18653/v1/2024.acl-long.861).

**What it studies:** A framework for making explicit which capability a benchmark claims to measure and what evidence a task and score provide for that claim.

**Application:** Define the constructs separately: source discovery, criterion applicability, fact extraction, finding classification, reasoning, citation support, and workflow reliability. Avoid using one aggregate score to imply all of them work.

### 16. NIST AI Risk Management Framework, Measure function

**Citation:** National Institute of Standards and Technology. 2023. [*AI Risk Management Framework 1.0: Core, Measure*](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/). Official framework.

**What it says:** Test sets and methods should be documented; performance should be measured in conditions similar to deployment, with domain-expert input and ongoing monitoring.

**Application:** Use a representative, held-out case set, record models/prompts/guidelines/tool versions, and repeat evaluation after changes. This is evaluation guidance, not an underwriting recall estimate.

### 17. NAIC Model Bulletin on AI use by insurers

**Citation:** National Association of Insurance Commissioners. Adopted December 4, 2023. [*Model Bulletin: Use of Artificial Intelligence Systems by Insurers*](https://content.naic.org/sites/default/files/inline-files/2023-12-4%20Model%20Bulletin_Adopted_0.pdf). Official model bulletin.

**What it says:** Describes regulators' expectations for insurer AI governance, testing, validation, documentation, and compliance when AI supports consumer-impacting decisions.

**Application:** If this project is used in insurance, retain source records, validation results, model/configuration versions, and human review decisions. The bulletin is a **model** for jurisdictions to adopt or adapt, not itself a claim that every jurisdiction has the same legal requirement.

## Proposed evaluation for this repository

The following is a research plan derived from the collection above, **not a performance claim**:

1. **Define a gold finding.** Have domain experts label each case with the applicable criterion, classification, supporting fact spans and source IDs, required calculations or cross-source links, and a short reason. Mark whether each finding is single-source or multi-source. Adjudicate disagreements and retain them as uncertainty data.
2. **Measure recall and precision separately.** Report finding-level recall and precision, plus recall for high-severity concerns, single-source versus multi-source findings, and each source type. An exact citation should be scored separately from whether the fact satisfies the criterion and whether the explanation follows.
3. **Measure the whole workflow.** Include skill/tool discovery, incorrect or missing tool calls, `no_match` false negatives, incomplete coverage, repeated-run stability, latency, and cost. Track invalid and unavailable upstream data as their own failure class.
4. **Compare architectures.** On the same held-out cases, compare a single full-context assessment, per-source atomic assessment, and the current per-source assessment followed by case-level synthesis. Use identical guidelines, data, model, and scoring rules.
5. **Keep the test set realistic.** Include missing documents, conflicting sources, stale facts, ambiguous policy language, exception rules, tables, and calculations. Have underwriters check whether the cases and findings resemble their actual work.

### Open questions to revisit

- What underwriting line and product are we targeting? This determines which research and gold cases transfer.
- Does the current multi-citation finding schema capture the needed relationships, or do derived values need explicit calculation records?
- Does the model reliably distinguish `not_applicable`, `insufficient_evidence`, and `no_match` on expert-labeled cases?
- What is the minimum acceptable recall for serious concerns, and how should disagreements between underwriters affect scoring?
- Which exact source locator is needed for loose text, nested JSON, tables, and document pages?

When adding a source, record its original link, year, publication status, exact task and population, metric, main result, transfer limit, and the question it helps us answer. Do not treat model leaderboard scores or citation validity as underwriter finding recall.
