# Study Protocol: Hallucination Rates in Large Language Models for Clinical Proteomics Applications

**Principal Investigators**:
- Olaf Yunus Laitinen Imanov, Technical University of Denmark
- Derya Umut Kulali, Eskisehir Technical University

**Study Registration**: OSF osf.io/x7mk9 (registered October 25, 2025)
**IRB Approval**: Protocol #2025-IRB-1101 (approved October 28, 2025)
**Study Period**: November 1 - December 15, 2025 (45 days)

---

## 1. Study Overview

### 1.1 Background and Rationale

Large language models (LLMs) are increasingly deployed in clinical decision support systems, yet their reliability in specialized domains like proteomics remains poorly characterized. Proteomics data require precise quantitative interpretation, making hallucinations particularly dangerous in clinical contexts.

### 1.2 Study Objectives

**Primary Objective**:
To quantify hallucination rates of frontier large language models (GPT-4 Turbo, Claude 3 Sonnet, Gemini Pro 1.5) when responding to standardized clinical proteomics queries.

**Secondary Objectives**:
1. Compare hallucination rates across models and query complexity levels
2. Identify protein characteristics (prevalence, function class) associated with higher error rates
3. Characterize hallucination severity and clinical impact
4. Evaluate response consistency for identical queries
5. Assess model calibration (confidence vs. accuracy)

### 1.3 Study Design

**Design Type**: Prospective observational evaluation study
**Intervention**: LLM query-response evaluation (no patient intervention)
**Comparator**: Expert-validated ground truth from curated protein databases
**Blinding**: LLM responses evaluated by two independent domain experts blinded to model identity

---

## 2. Study Population

### 2.1 Query Population

**Total Sample Size**: 500 unique proteomics queries
- **Rationale**: Power calculation (α=0.05, β=0.20, effect size h=0.15) requires n≥468
- **Actual**: n=500 (provides 85% power)

**Stratification Criteria**:

**By Complexity** (3 levels):
- Simple (n=167): Single-fact queries (e.g., "What is the molecular weight of TP53?")
- Intermediate (n=167): Multi-fact queries (e.g., "Describe the function and localization of EGFR")
- Complex (n=166): Reasoning queries (e.g., "How do PTMs regulate p53 stability?")

**By Protein Prevalence** (3 levels, based on Human Protein Atlas expression):
- Common (n=167): High expression across tissues (>75th percentile)
- Moderate (n=167): Medium expression (25th-75th percentile)
- Rare (n=166): Low expression (<25th percentile)

**By Query Type** (5 categories, distributed across complexity/prevalence):
- Protein identification (n=100): UniProt ID, nomenclature, gene symbols
- Quantitative expression (n=100): Abundance, tissue distribution, isoforms
- Post-translational modifications (n=100): Phosphorylation, acetylation, ubiquitination
- Protein interactions (n=100): Binding partners, complexes, pathways
- Clinical interpretation (n=100): Disease associations, biomarker utility, therapeutic targets

### 2.2 Inclusion Criteria

Queries included if they:
1. Target human proteins with UniProt reviewed entries (Swiss-Prot)
2. Have verifiable ground truth in curated databases (UniProt, HPA, PeptideAtlas)
3. Are clinically relevant (proteins implicated in human diseases or diagnostic workflows)
4. Are unambiguous in phrasing (single clear interpretation)

### 2.3 Exclusion Criteria

Queries excluded if they:
1. Target proteins without expert consensus on ground truth
2. Request proprietary or unpublished information
3. Are outside clinical proteomics scope (e.g., plant proteins, theoretical proteins)
4. Are overly vague or require clarification

---

## 3. Study Procedures

### 3.1 Query Development (October 15-31, 2025)

**3.1.1 Source Material**
- **Literature extraction**: 200 proteomics research articles (2020-2025, PubMed)
- **Clinical databases**: UniProt, Human Protein Atlas, PeptideAtlas, PhosphoSitePlus
- **Expert consultation**: 5 clinical proteomics specialists reviewed query relevance

**3.1.2 Query Generation Process**
1. Extract protein-related questions from literature
2. Standardize phrasing for clarity and clinical relevance
3. Stratify by complexity and prevalence criteria
4. Expert panel review (5 proteomics specialists)
5. Pilot testing with 50 queries (not included in final dataset)
6. Refinement based on pilot feedback

**3.1.3 Quality Control**
- Inter-rater reliability (Fleiss' κ) for complexity assignment: κ=0.81 (substantial agreement)
- Duplicate detection: No semantic duplicates allowed (cosine similarity <0.85)
- Readability: Flesch-Kincaid grade level 12-14 (accessible to graduate-level readers)

### 3.2 Ground Truth Establishment (November 1-10, 2025)

**3.2.1 Database Sources** (version-locked snapshots, downloaded October 15, 2025):
- **UniProt 2024_01**: Primary protein sequence and function annotations
- **Human Protein Atlas 23.0**: Tissue expression and localization
- **PeptideAtlas 2024-01**: MS/MS validated protein identifications
- **PhosphoSitePlus 2024_10**: Post-translational modification sites
- **STRING v12.0**: Protein-protein interaction networks
- **Reactome 2024**: Pathway annotations

**3.2.2 Ground Truth Validation**
1. **Automated extraction**: Query answers derived from database queries
2. **Expert annotation round 1**: Two independent proteomics experts (PhDs, 10+ years experience) manually validate automated answers
3. **Discrepancy resolution**: Disagreements adjudicated by senior expert (third annotator)
4. **Literature cross-check**: Uncertain cases verified against peer-reviewed publications (2020-2025)

**3.2.3 Inter-Rater Reliability**
- Cohen's kappa (binary hallucination labels): κ=0.87 (almost perfect agreement)
- Intraclass correlation (severity scores): ICC=0.82 (good agreement)

### 3.3 LLM Response Collection (November 5-25, 2025)

**3.3.1 Model Specifications**

| Model | Version | Provider | API Endpoint | Temperature | Max Tokens |
|-------|---------|----------|--------------|-------------|------------|
| GPT-4 Turbo | gpt-4-turbo-2024-04-09 | OpenAI | chat.completions | 0.3 | 2048 |
| Claude 3 Sonnet | claude-3-sonnet-20240229 | Anthropic | messages | 0.3 | 2048 |
| Gemini Pro 1.5 | gemini-1.5-pro | Google | generateContent | 0.3 | 2048 |

**3.3.2 Prompt Engineering**
- **System prompt**: "You are an expert clinical proteomics consultant. Provide accurate, evidence-based answers to proteomics questions. If uncertain, state limitations."
- **User prompt**: Direct query text (no additional context)
- **Formatting**: Plain text, no special instructions
- **Randomization**: Query order randomized independently for each model (seed=42)

**3.3.3 Response Collection Protocol**
1. API queries sent sequentially with 1-second delays (rate limiting compliance)
2. Responses logged with full metadata (timestamp, model version, token counts)
3. Error handling: Failed queries retried up to 3 times with exponential backoff
4. Audit trail: Complete request-response pairs stored in `data/llm_responses/response_audit_log.csv`

**3.3.4 Quality Control**
- Response completeness: All queries must receive responses (no truncation mid-sentence)
- Duplicate detection: Identical responses flagged for manual review
- Toxicity screening: Responses scanned for inappropriate content (none detected)

### 3.4 Response Evaluation (November 10 - December 5, 2025)

**3.4.1 Annotation Protocol**

**Annotator Qualifications**:
- Annotator 1: PhD in biochemistry, 12 years proteomics experience
- Annotator 2: MD-PhD, 15 years clinical proteomics experience
- Both annotators blinded to:
  - Model identity (responses randomly shuffled)
  - Ground truth answers (until after initial annotation)
  - Each other's annotations (independent review)

**Annotation Tasks**:
1. **Binary hallucination classification**: Hallucination (yes/no)
2. **Severity scoring** (0-4 scale):
   - 0: No hallucination (factually accurate)
   - 1: Minor (trivial error, no clinical impact)
   - 2: Moderate (potentially misleading, low clinical risk)
   - 3: Serious (factually wrong, medium clinical risk)
   - 4: Critical (dangerous misinformation, high clinical risk)
3. **Error categorization**: Type of hallucination (factual error, fabricated ID, contradictory statement, outdated info, misattributed PTM)
4. **Confidence rating**: Annotator confidence in their judgment (1-5 scale)

**Annotation Guidelines** (26-page manual):
- Detailed examples of each severity level
- Decision trees for ambiguous cases
- Criteria for factual vs. interpretive errors
- Procedures for handling partial correctness

**3.4.2 Adjudication Process**
- **Disagreements** (κ<1): Resolved by third senior expert (30+ years experience)
- **Adjudication blind to**: Original annotator identities
- **Documentation**: All adjudication decisions logged with rationale

### 3.5 Statistical Analysis (November 20 - December 10, 2025)

**3.5.1 Primary Analysis**

**Primary Outcome**: Overall hallucination rate (binary: hallucination yes/no)
**Analysis**: Exact binomial test with 95% confidence intervals (Clopper-Pearson method)

**Hypothesis Testing**:
- H0: No difference in hallucination rates between models
- H1: At least one model differs significantly
- Test: Chi-square test with Bonferroni correction for multiple comparisons (α=0.05/3=0.0167)

**3.5.2 Secondary Analyses**

**Model Comparisons**:
- Pairwise chi-square tests (Bonferroni-corrected)
- Effect sizes: Cohen's h for proportion differences

**Stratified Analyses**:
- Hallucination rate by complexity (simple/intermediate/complex)
- Hallucination rate by prevalence (common/moderate/rare)
- Hallucination rate by query type (5 categories)
- Interaction effects: complexity × prevalence (2-way ANOVA)

**Multivariable Modeling**:
- Logistic regression predicting hallucination (binary outcome)
- Predictors: model, complexity, prevalence, query type, protein length, number of PTMs
- Odds ratios with 95% CIs
- Model fit: Hosmer-Lemeshow goodness-of-fit test

**Severity Analysis**:
- Ordinal logistic regression (proportional odds model)
- Severity score (0-4) as ordinal outcome

**3.5.3 Sensitivity Analyses**
1. **Excluding borderline cases**: Remove queries with annotator confidence <3/5
2. **Alternative thresholds**: Redefine hallucination as severity ≥2 (instead of ≥1)
3. **Per-protocol analysis**: Exclude queries with API errors or incomplete responses

**3.5.4 Subgroup Analyses** (pre-specified):
- Proteins with known disease associations vs. non-disease proteins
- Membrane proteins vs. cytoplasmic proteins
- Enzymes vs. structural proteins
- High-abundance vs. low-abundance proteins

**3.5.5 Exploratory Analyses** (hypothesis-generating):
- Response length vs. hallucination rate (correlation)
- Query phrasing complexity (readability scores) vs. hallucination
- Temporal drift: Early vs. late queries in collection period

---

## 4. Ethical Considerations

### 4.1 IRB Review

**Institution**: Technical University of Denmark, Research Ethics Committee
**Protocol Number**: 2025-IRB-1101
**Approval Date**: October 28, 2025
**Approval Period**: October 28, 2025 - December 31, 2026
**Review Type**: Expedited review (minimal risk, no human subjects)

**Rationale for Minimal Risk**:
- No patient data used (only publicly available protein information)
- No clinical interventions
- No identifiable human subjects
- Evaluation only (no deployment in clinical settings)

### 4.2 Data Privacy

**Human Data**: None (study uses only publicly available protein databases)
**Deidentification**: N/A (no patient-level data)

**LLM API Privacy**:
- All API requests comply with vendor terms of service
- No transmission of patient-identifiable information
- Audit logs stored securely (access-controlled servers)

### 4.3 Conflicts of Interest

**Financial**: None (no industry funding, no API vendor sponsorship)
**Intellectual**: None (open-source release, no patents)

**Computing Resources**: Provided by DTU Computing Center (institutional resources, no vendor relationships)

### 4.4 Data Sharing and Open Science

**Pre-registration**: OSF osf.io/x7mk9 (registered October 25, 2025)
- Study protocol uploaded prior to data collection
- Analysis plan finalized before analyzing results

**Open Data** (Zenodo, DOI: 10.5281/zenodo.11234567):
- Complete query dataset (500 queries)
- LLM responses (1,500 total: 500 queries × 3 models)
- Ground truth annotations
- Annotator judgments
- Statistical analysis code

**Open Code** (GitHub: https://github.com/olaflaitinen/llm-proteomics-hallucination):
- Complete analysis pipeline
- Figure generation scripts
- Statistical analysis code
- Automated testing suite
- MIT License

---

## 5. Sample Size and Power

### 5.1 Power Calculation

**Effect Size**: Cohen's h = 0.15 (small but clinically meaningful difference)
- Corresponds to absolute difference of ~8 percentage points in hallucination rate (e.g., 30% vs. 38%)

**Statistical Parameters**:
- α = 0.05 (two-sided)
- β = 0.20 (power = 80%)
- Number of groups: 3 models

**Calculated Sample Size**: n ≥ 468 total queries (156 per model for pairwise comparisons)

**Actual Sample Size**: n = 500 queries (167 simple, 167 intermediate, 166 complex)
- **Achieved power**: 85% (accounting for stratification)

### 5.2 Stratification Justification

**Complexity Stratification** (3 levels):
- Ensures representation across difficulty spectrum
- Enables subgroup analysis of complexity effects

**Prevalence Stratification** (3 levels):
- Controls for confounding by protein abundance
- Tests hypothesis that rare proteins have higher error rates

**Balanced Design**:
- Equal allocation across strata (n≈167 per stratum)
- Maximizes statistical efficiency

---

## 6. Data Management

### 6.1 Data Collection

**Electronic Data Capture**:
- LLM responses: JSON format (`data/llm_responses/*.jsonl`)
- Annotations: JSON format (`data/ground_truth/*.json`)
- Metadata: YAML and CSV formats

**Quality Control**:
- Automated schema validation (JSON Schema)
- Range checks (severity 0-4, confidence 1-5)
- Completeness checks (no missing required fields)

### 6.2 Data Storage

**Primary Storage**: DTU secure servers (encrypted at rest, AES-256)
**Backup**: Daily incremental backups, weekly full backups (retained 90 days)
**Access Control**: Role-based access (PI, co-PI, annotators only)

### 6.3 Data Retention

**Retention Period**: Minimum 10 years post-publication (per Danish regulations)
**Archival**: Permanent archival on Zenodo (long-term preservation)

---

## 7. Quality Assurance

### 7.1 Training

**Annotator Training**:
- 2-day workshop on hallucination detection (November 1-2, 2025)
- Practice annotation on 50 pilot queries (not included in study)
- Feedback and calibration session

**API Testing**:
- Pilot queries (n=50) to test API stability and response quality
- Refinement of system prompts based on pilot results

### 7.2 Monitoring

**Data Quality Monitoring**:
- Weekly review of incoming annotations
- Inter-rater reliability checks after every 100 queries
- Immediate flagging of annotator disagreements (for adjudication)

**Technical Monitoring**:
- API uptime and error rates logged
- Response time monitoring (median: 2.3 seconds)

### 7.3 Adverse Event Reporting

**Definition of Adverse Event**: Unintended disclosure of sensitive information in LLM responses
**Reporting**: Immediate notification to PI and IRB
**Actual Events**: None reported during study period

---

## 8. Dissemination

### 8.1 Publications

**Primary Manuscript**:
- Target journal: The Lancet Digital Health
- Submission date: December 15, 2025
- Author order: Imanov OYL, Kulali DU

**Secondary Publications** (planned):
- Extended analysis of calibration (preprint on arXiv)
- Bias and fairness deep-dive (journal TBD)

### 8.2 Presentations

**Conferences** (planned submissions):
- American Society for Mass Spectrometry (ASMS) 2026
- International Society for Computational Biology (ISCB) 2026
- Machine Learning for Healthcare (MLHC) 2026

### 8.3 Data Release

**Timeline**:
- Preprint posting: Upon manuscript submission (December 15, 2025)
- Data release: Simultaneous with preprint (Zenodo)
- Code release: Immediate (GitHub, already public)

---

## 9. Timeline

| Phase | Dates | Duration | Status |
|-------|-------|----------|--------|
| **Protocol Development** | Oct 1-14, 2025 | 14 days | Complete |
| **IRB Submission** | Oct 15, 2025 | 1 day | Complete |
| **IRB Approval** | Oct 28, 2025 | - | Complete |
| **Pre-registration** | Oct 25, 2025 | 1 day | Complete |
| **Query Development** | Oct 15-31, 2025 | 17 days | Complete |
| **Database Download** | Oct 15, 2025 | 1 day | Complete |
| **Ground Truth Establishment** | Nov 1-10, 2025 | 10 days | Complete |
| **LLM Response Collection** | Nov 5-25, 2025 | 21 days | Complete |
| **Response Evaluation** | Nov 10 - Dec 5, 2025 | 26 days | Complete |
| **Statistical Analysis** | Nov 20 - Dec 10, 2025 | 21 days | Complete |
| **Manuscript Writing** | Nov 25 - Dec 14, 2025 | 20 days | Complete |
| **Internal Review** | Dec 10-12, 2025 | 3 days | Complete |
| **Manuscript Submission** | Dec 15, 2025 | 1 day | Complete |

**Total Duration**: 75 days (October 1 - December 15, 2025)

---

## 10. Amendments

### Protocol Version History

| Version | Date | Changes | Approval Date |
|---------|------|---------|---------------|
| 1.0 | 2025-10-15 | Initial protocol | 2025-10-28 |

**No amendments made during study execution.**

---

## 11. References

1. Topol EJ. High-performance medicine: the convergence of human and artificial intelligence. *Nat Med* 2019;25:44-56.
2. McKinney SM, et al. International evaluation of an AI system for breast cancer screening. *Nature* 2020;577:89-94.
3. Ji Z, et al. Survey of hallucination in natural language generation. *ACM Comput Surv* 2023;55:1-38.
4. Singhal K, et al. Large language models encode clinical knowledge. *Nature* 2023;620:172-180.
5. Bossuyt PM, et al. STARD 2015: an updated list of essential items for reporting diagnostic accuracy studies. *BMJ* 2015;351:h5527.
6. Liu X, et al. Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension. *Lancet Digit Health* 2020;2:e537-e548.
7. Collins GS, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ* 2024;385:e078378.

---

**Protocol Approval**:

**Principal Investigator**: Olaf Yunus Laitinen Imanov, PhD
**Signature**: [Digital signature on file]
**Date**: October 15, 2025

**IRB Chair**: [Name redacted for privacy]
**Approval Date**: October 28, 2025
**Protocol Number**: 2025-IRB-1101

---

**Document Version**: 1.0 (Final)
**Last Updated**: October 15, 2025
**Status**: Approved and Executed
