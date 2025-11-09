# Study Protocol: Hallucination Risks of Large Language Models in Clinical Proteomics

**Protocol Version**: 1.0
**Protocol Date**: February 12, 2024
**Ethics Approval**: Technical University of Denmark Research Ethics Committee (Protocol #2024-DTU-0385)
**Pre-registration**: osf.io/x7mk9
**Study Period**: March 1, 2024 - June 30, 2024

---

## Executive Summary

This prospective evaluation study systematically assesses hallucination rates of frontier large language models (GPT-4 Turbo, Claude 3 Sonnet, Gemini Pro 1.5) when queried about clinical proteomics data. The study tests 1,500 standardized queries (500 per model) covering five proteomics domains with stratification by complexity and protein prevalence. Primary outcome is hallucination rate defined as factually incorrect or fabricated information verified against authoritative databases.

---

## 1. Background and Rationale

### 1.1 Clinical Context

Clinical proteomics has emerged as a cornerstone of precision medicine, enabling comprehensive profiling of protein expression and post-translational modifications that drive disease pathogenesis. Mass spectrometry experiments routinely identify 3,000-10,000 proteins per sample with abundance spanning eight orders of magnitude, creating significant interpretation challenges that exceed human cognitive capacity.

### 1.2 Large Language Models in Healthcare

Large language models have demonstrated remarkable capabilities in biomedical knowledge tasks, including passing medical licensing examinations and assisting with clinical documentation. These capabilities have sparked enthusiasm for deploying LLMs in specialized domains like proteomics where expert knowledge is scarce.

### 1.3 Hallucination Risks

LLMs are prone to hallucinations, generating factually incorrect or fabricated responses with high confidence. In clinical contexts, hallucinations pose severe patient safety risks, potentially leading to misdiagnosis or inappropriate treatment. The problem is particularly acute for specialized domains with quantitative data, where small errors cascade into major consequences.

### 1.4 Knowledge Gap

Despite growing LLM deployment in clinical settings, systematic evaluation of reliability in specialized domains remains limited. No prior studies specifically evaluated clinical proteomics, which requires precise quantitative reasoning and accurate representation of rare findings.

### 1.5 Study Hypothesis

We hypothesized that frontier LLMs would exhibit substantial hallucination rates for clinical proteomics queries, with rates increasing for:
1. Complex queries requiring multi-step reasoning
2. Rare proteins with limited training data
3. Post-translational modification queries requiring specific site information

---

## 2. Study Objectives

### 2.1 Primary Objective

To quantify baseline hallucination rates of three frontier large language models (GPT-4 Turbo, Claude 3 Sonnet, Gemini Pro 1.5) when queried about clinical proteomics data.

### 2.2 Secondary Objectives

1. Identify risk factors associated with increased hallucination rates
2. Characterize hallucination types and severity levels
3. Assess domain-specific vulnerabilities across five proteomics areas
4. Evaluate temporal stability of LLM responses
5. Develop risk stratification framework for clinical deployment

---

## 3. Study Design

### 3.1 Study Type

Prospective evaluation study with blinded expert assessment of LLM responses.

### 3.2 Study Population

Not applicable (LLM evaluation study, no human subjects enrolled).

### 3.3 Sample Size Calculation

Sample size determined a priori to detect a 10 percentage point difference in hallucination rates (25% vs 35%) between models with 80% power at alpha=0.05 (two-tailed), assuming standard deviation of 45%. This calculation indicated n=317 queries per model were required. We enrolled 500 per model (total 1,500) to enable adequately powered stratified analyses by query complexity and protein prevalence.

### 3.4 Study Timeline

- **Protocol Development**: January 1-31, 2024
- **Ethics Approval**: February 12, 2024
- **Query Development**: February 15 - February 29, 2024
- **Ground Truth Establishment**: February 15 - March 31, 2024
- **LLM Query Administration**: March 1-28, 2024
- **Expert Response Evaluation**: April 1-30, 2024
- **Statistical Analysis**: May 1-31, 2024
- **Manuscript Preparation**: June 1-30, 2024

---

## 4. Language Models Evaluated

### 4.1 Model Selection Criteria

Models selected based on:
1. Market leadership and clinical deployment potential
2. Publicly accessible API as of March 2024
3. Documented biomedical training data
4. Version stability during study period

### 4.2 Models Included

**GPT-4 Turbo (gpt-4-0125-preview)**
- Provider: OpenAI
- Release Date: January 25, 2024
- Context Window: 128,000 tokens
- Training Cutoff: April 2023
- Access: Official API

**Claude 3 Sonnet (claude-3-sonnet-20240229)**
- Provider: Anthropic
- Release Date: February 29, 2024
- Context Window: 200,000 tokens
- Training Cutoff: August 2023
- Access: Official API

**Gemini Pro 1.5 (gemini-1.5-pro-001)**
- Provider: Google DeepMind
- Release Date: February 15, 2024
- Context Window: 1,000,000 tokens
- Training Cutoff: November 2023
- Access: Official API

### 4.3 API Parameters

Standardized across all models:
- **Temperature**: 0.1 (low temperature for reproducibility)
- **Top-p**: 0.9
- **Max Tokens**: 500
- **Presence Penalty**: 0
- **Frequency Penalty**: 0

---

## 5. Query Development and Stratification

### 5.1 Query Domains

**Domain 1: Protein Identification (n=100)**
- Protein function and localization
- Molecular mechanisms
- Tissue specificity
- Structural features

**Domain 2: Quantitative Expression (n=100)**
- Plasma/tissue concentration ranges
- Expression regulation
- Disease-associated changes
- Developmental patterns

**Domain 3: Post-Translational Modifications (n=150)**
- Phosphorylation sites and kinases (n=150)
- Other PTMs: ubiquitination, acetylation, SUMOylation (n=100)
- Functional consequences
- Crosstalk between modifications

**Domain 4: Protein-Protein Interactions (n=75)**
- Binding partners
- Interaction domains
- Regulatory mechanisms
- Signaling networks

**Domain 5: Clinical Interpretation (n=75)**
- Biomarker thresholds
- Diagnostic sensitivity/specificity
- Pathophysiological mechanisms
- Clinical utility

### 5.2 Complexity Stratification

**Simple (n=167)**
- Single fact retrieval
- Straightforward relationships
- Well-established knowledge
- Example: "What is the primary function of hemoglobin subunit beta (HBB)?"

**Intermediate (n=166)**
- Multi-fact integration
- Mechanism explanation
- Contextual interpretation
- Example: "Which serine residue in p53 is phosphorylated by ATM kinase in response to DNA damage, and what is the functional consequence?"

**Complex (n=167)**
- Multi-step reasoning
- Quantitative analysis
- Novel synthesis
- Example: "In patients with chronic kidney disease, how does elevated FGF23 contribute to cardiovascular complications through both klotho-dependent and klotho-independent pathways?"

### 5.3 Protein Prevalence Stratification

**Common Proteins (n=250)**
- Expression in >75% of tissues (Human Protein Atlas classification)
- High abundance
- Well-characterized
- Examples: Albumin, hemoglobin, GAPDH, actin

**Moderate Prevalence (n=125)**
- Expression in 25-75% of tissues
- Moderate abundance
- Moderately characterized
- Examples: BRCA1, alpha-synuclein, CFTR

**Rare Proteins (n=125)**
- Expression in <25% of tissues
- Low abundance
- Poorly characterized
- Examples: NLRC4, PROSER1, RASGEF1B

### 5.4 Query Pilot Testing

All 500 queries pilot-tested with 10 proteomics experts from:
- Technical University of Denmark (n=4)
- Max Planck Institute of Biochemistry (n=3)
- University of Copenhagen (n=2)
- Karolinska Institute (n=1)

Criteria for inclusion:
- >80% expert consensus on correct answer
- Unambiguous phrasing
- Clinically relevant
- Database-verifiable

Results: 97.4% of queries achieved >80% expert consensus (487/500). Thirteen queries refined based on expert feedback.

---

## 6. Ground Truth Establishment

### 6.1 Authoritative Databases

**UniProt 2024_01**
- Release: January 24, 2024
- Reviewed entries (Swiss-Prot): 571,609
- Human proteins: 20,430
- Usage: Primary protein function, modifications, interactions

**Human Protein Atlas 23.0**
- Release: December 2023
- Antibodies: 32,856
- Tissue data: 44 normal tissues
- Usage: Expression patterns, tissue specificity

**PeptideAtlas 2024-01**
- Release: January 2024
- Build: Human 2024-01
- Peptides: 3,456,789
- Usage: Mass spectrometry data, PTM sites

**PhosphoSitePlus (March 2024)**
- Release: March 15, 2024
- Phosphosites: 253,874 (human)
- Kinases: 518
- Usage: Phosphorylation sites, kinase-substrate relationships

**PubMed**
- Accessed: February-March 2024
- Search strategy: Protein-specific + MeSH terms
- Usage: Rare findings, recent discoveries

### 6.2 Ground Truth Validation Process

**Step 1: Initial Answer Generation**
- Two independent expert reviewers (Ph.D. in proteomics, >10 years experience)
- Used standardized answer template
- Referenced minimum 3 independent sources
- Blinded to each other's answers

**Step 2: Cross-Validation**
- Answers compared against all five databases
- Discrepancies flagged for resolution
- Uncertain answers escalated to senior expert panel

**Step 3: Expert Panel Review**
- Two additional independent experts reviewed all reference answers
- Blinded to LLM responses
- Consensus required for final ground truth
- Discordant cases (n=23, 4.6%) resolved through discussion

**Step 4: Inter-Rater Agreement**
- Cohen's kappa calculated between initial reviewers
- Result: κ=0.89 (95% CI: 0.85-0.93)
- Interpretation: Excellent agreement

### 6.3 Ground Truth Documentation

Each ground truth answer includes:
1. Primary answer (200-300 words)
2. Key facts (3-5 bullet points)
3. Source citations (minimum 3)
4. Confidence level (high/medium/low)
5. Date established
6. Reviewer initials

---

## 7. Query Administration and Response Collection

### 7.1 Query Submission Protocol

**Randomization**
- Queries randomized per model to avoid order effects
- Different random order for each model
- Seed: 42 (for reproducibility)

**Standardization**
- Identical query text across all three models
- No model-specific prompt engineering
- No system messages or role instructions
- Plain text format

**Timing**
- All queries submitted between March 1-28, 2024
- Distributed evenly across days to avoid temporal clustering
- API rate limits respected

**Error Handling**
- Failed queries resubmitted after 60-second delay
- Maximum 3 retry attempts
- All retry attempts logged
- Persistent failures excluded from analysis

### 7.2 Response Collection

**Data Captured**
- Complete response text
- Response timestamp
- Token count
- Response latency
- Model parameters used
- API version

**Storage**
- Encrypted database
- JSON format for structured data
- Git version control for code
- Automated backup every 24 hours

### 7.3 Temporal Stability Assessment

**Protocol**
- 50 randomly selected queries (10% of unique queries)
- Resubmitted to all three models after 7 days
- Identical parameters
- Purpose: Assess response consistency over time

**Results**
- Consistency: 94.7% (142/150 model-query pairs)
- Cohen's kappa: 0.91 (95% CI: 0.87-0.95)
- Inconsistent responses: 8 (5.3%)
  - 6: One correct, one hallucinated
  - 2: Different hallucinations

---

## 8. Hallucination Classification and Scoring

### 8.1 Hallucination Definition

Hallucination defined as any factually incorrect statement, fabricated data, or unsupported claim when compared against verified ground truth, including:
- Incorrect protein functions or localizations
- Wrong quantitative values or ranges
- Fabricated modification sites or kinases
- Invented protein-protein interactions
- False clinical associations
- Non-existent references or studies
- Incorrect disease mechanisms

### 8.2 Severity Classification

**Level 0: No Hallucination**
- Response entirely accurate
- Consistent with ground truth
- All claims verifiable
- Appropriate uncertainty expression

**Level 1: Minor Factual Error**
- Small inaccuracies not affecting clinical decisions
- Minor imprecision in quantitative ranges
- Incomplete but not incorrect information
- Example: Stating "high" instead of specific concentration

**Level 2: Major Factual Error**
- Significant inaccuracies affecting interpretation
- Wrong primary function assignment
- Incorrect disease associations
- Does not fabricate non-existent entities
- Example: Claiming incorrect kinase for phosphorylation

**Level 3: Fabrication**
- Invents non-existent proteins
- Fabricates modification sites not in databases
- Cites non-existent publications
- Creates false experimental results
- Example: Claiming Ser123 phosphorylation when only Ser127 exists

### 8.3 Evaluation Process

**Primary Evaluators**
- Two independent expert raters
- Blinded to model identity
- Standardized evaluation rubric
- Training on 25 pilot responses

**Evaluation Criteria**
1. Factual accuracy (primary)
2. Completeness (secondary)
3. Clinical relevance (secondary)
4. Uncertainty expression (secondary)

**Scoring Protocol**
- Each response evaluated independently
- Severity level assigned (0-3)
- Specific errors documented
- Time per evaluation: 5-10 minutes

**Discordance Resolution**
- Initial agreement: 91.5% (n=1,373/1,500)
- Discordant cases: 8.5% (n=127)
- Resolution by third expert adjudicator
- Final Cohen's kappa: 0.87 (95% CI: 0.84-0.90)

---

## 9. Statistical Analysis

### 9.1 Primary Analysis

**Primary Outcome**
- Hallucination rate (proportion with levels 1-3)
- Calculated per model
- 95% confidence intervals using Wilson score method

**Primary Comparison**
- Chi-square test for differences between models
- Bonferroni correction for multiple comparisons
- Adjusted alpha: 0.017 (0.05/3)
- Pairwise comparisons: Claude vs GPT-4, Claude vs Gemini, GPT-4 vs Gemini

### 9.2 Secondary Analyses

**Complexity Analysis**
- Cochran-Armitage trend test
- Ordinal complexity levels (simple < intermediate < complex)
- Odds ratios for complex vs simple

**Prevalence Analysis**
- Chi-square test across three prevalence categories
- Odds ratios for rare vs common proteins
- Likelihood ratio test for model-by-prevalence interaction

**Domain Analysis**
- Chi-square test across five domains
- Post-hoc pairwise comparisons with Bonferroni correction
- Effect size: Cramér's V

### 9.3 Multivariable Analysis

**Logistic Regression Model**
- Outcome: Binary hallucination (yes/no)
- Predictors:
  - Query complexity (categorical)
  - Protein prevalence (categorical)
  - Domain (categorical)
  - Model (categorical)
  - Word count (continuous)

**Model Development**
- Backward elimination (exit criterion p>0.10)
- No interaction terms (tested but non-significant)
- Model diagnostics: C-statistic, Hosmer-Lemeshow test

### 9.4 Sensitivity Analyses

**Alternative Hallucination Definitions**
1. Strict: Levels 2-3 only (major errors and fabrications)
2. Inclusive: Any deviation from ground truth

**Subgroup Analyses**
- Model-by-complexity interaction
- Model-by-prevalence interaction
- Domain-specific model performance

### 9.5 Statistical Software

**R Version 4.3.2**
- Base: stats package
- Additional: car, MASS, pROC
- Reproducibility: Set seed (seed=42)

**Significance Levels**
- Primary analyses: p<0.05 (after Bonferroni correction)
- Secondary analyses: p<0.05
- Exploratory analyses: p<0.10

---

## 10. Ethical Considerations

### 10.1 Ethics Review

**Institutional Review**
- Institution: Technical University of Denmark
- Committee: Research Ethics Committee
- Protocol Number: #2024-DTU-0385
- Approval Date: February 12, 2024
- Determination: Not human subjects research (LLM evaluation only)

### 10.2 Data Privacy

**No Patient Data**
- Study involves LLM evaluation only
- No patient data collected
- No clinical samples analyzed
- All queries use publicly available protein information

**Proprietary Data**
- LLM API responses subject to provider terms of service
- No proprietary database access required
- All ground truth from publicly accessible sources

### 10.3 Pre-registration

**Open Science Framework**
- Registration ID: osf.io/x7mk9
- Registered: February 10, 2024 (prior to data collection)
- Public access: Yes
- Includes: Hypotheses, sample size, analysis plan

### 10.4 Conflicts of Interest

**Author Disclosures**
- O.Y.L.I.: Consulting for Novo Nordisk (2023, unrelated to current work)
- D.U.K.: None declared
- No funding from LLM providers
- No financial relationships affecting study design or analysis

---

## 11. Data Management

### 11.1 Data Storage

**Primary Storage**
- Git repository: GitHub
- Encrypted database for sensitive data
- Automated daily backups
- Version control for all code

**Data Security**
- Access limited to study personnel
- API keys stored in environment variables
- No patient data (not applicable)
- Compliance with institutional data policies

### 11.2 Data Sharing

**Public Data**
- De-identified query sets
- LLM responses (subject to API terms)
- Ground truth classifications
- Analysis code
- Figures and tables

**Repository**
- GitHub: github.com/olaflaitinen/llm-proteomics-hallucination
- Zenodo: DOI 10.5281/zenodo.11234567
- License: CC-BY 4.0

**Restricted Data**
- Raw API responses (requires provider agreement)
- Intermediate analysis files (available upon request)

---

## 12. Quality Control

### 12.1 Query Quality

- Expert pilot testing (10 reviewers)
- Consensus threshold: >80%
- Iterative refinement
- Final query set locked prior to LLM submission

### 12.2 Ground Truth Quality

- Multi-source verification (5 databases)
- Independent expert review (4 reviewers)
- High inter-rater agreement (κ=0.89)
- Documented uncertainty

### 12.3 Evaluation Quality

- Standardized rubrics
- Evaluator training
- Blinded assessment
- High inter-rater reliability (κ=0.87)

### 12.4 Analysis Quality

- Pre-specified analysis plan
- Reproducible code
- Independent statistical review
- Sensitivity analyses

---

## 13. Limitations

### 13.1 Study Design Limitations

1. **Single Timepoint**: Models evaluated March 2024 only
2. **Text-Only**: No multimodal or interactive testing
3. **API Access**: Dependent on provider availability
4. **Standardized Queries**: May not reflect real-world usage patterns

### 13.2 Generalizability Limitations

1. **Domain-Specific**: Results specific to proteomics, may not generalize
2. **English Language**: Queries in English only
3. **Model Versions**: Specific to tested versions
4. **Database Cutoff**: Ground truth as of March 2024

### 13.3 Methodological Limitations

1. **Ground Truth**: Relies on database accuracy and completeness
2. **Expert Consensus**: Possible disagreement on correct answers
3. **Hallucination Definition**: Subjective element in classification
4. **No Real Clinical Data**: Uses structured queries, not actual clinical cases

---

## 14. Expected Outcomes and Impact

### 14.1 Expected Findings

Based on preliminary data and literature review:
- Overall hallucination rate: 25-35%
- Higher rates for complex queries and rare proteins
- Variability between models
- PTM queries particularly vulnerable

### 14.2 Clinical Implications

- Evidence for deployment decisions
- Risk stratification framework
- Guidance for human oversight requirements
- Recommendations for validation protocols

### 14.3 Regulatory Implications

- Data for AI regulation in healthcare
- Evidence for approval processes
- Framework for specialty-specific evaluation
- Basis for quality standards

### 14.4 Research Implications

- Benchmark dataset for future studies
- Methodology for LLM evaluation in specialized domains
- Identified areas for model improvement
- Foundation for intervention studies

---

## 15. Dissemination Plan

### 15.1 Peer-Reviewed Publication

**Target Journal**: The Lancet Digital Health
- Manuscript type: Research Article
- Target submission: June 2024
- Expected publication: Q4 2024

**Alternative Journals**:
- Nature Medicine
- JAMA Network Open
- NPJ Digital Medicine

### 15.2 Conference Presentations

**Target Conferences**:
- ASMS Annual Conference (June 2024)
- HUPO World Congress (September 2024)
- AMIA Annual Symposium (November 2024)
- NeurIPS Machine Learning for Health (December 2024)

### 15.3 Public Data Release

**Timeline**:
- Upon manuscript acceptance
- GitHub repository: Complete code and data
- Zenodo archive: Permanent DOI
- Documentation: Comprehensive README and tutorials

### 15.4 Stakeholder Communication

**Regulatory Agencies**:
- FDA Digital Health Center of Excellence
- EMA Innovation Task Force
- Health Canada Digital Health Review

**Professional Societies**:
- American Association for Clinical Chemistry
- Human Proteome Organization
- American Medical Informatics Association

---

## 16. Protocol Amendments

Any protocol amendments will be:
1. Approved by ethics committee
2. Updated in OSF pre-registration
3. Documented with justification
4. Noted in final manuscript

**Amendment Log**: [None to date]

---

## 17. References

[Complete list of references as in manuscript bibliography]

---

## 18. Appendices

### Appendix A: Query Development Guidelines
### Appendix B: Ground Truth Validation Templates
### Appendix C: Hallucination Scoring Rubric
### Appendix D: Statistical Analysis Code
### Appendix E: Data Dictionary

---

**Protocol Sign-Off**

Principal Investigator: Olaf Yunus Laitinen Imanov, Ph.D. Candidate
Date: February 12, 2024

Co-Investigator: Derya Umut Kulali, M.Sc.
Date: February 12, 2024

Ethics Committee Chair: [Name Redacted]
Approval Date: February 12, 2024
