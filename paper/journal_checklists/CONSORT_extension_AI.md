# CONSORT-AI Extension Checklist
## Consolidated Standards of Reporting Trials - Artificial Intelligence Extension

**Study Title:** Evaluating Hallucinations in Large Language Model Responses to Proteomics Queries: A Prospective Study

**Journal:** The Lancet Digital Health

**Study Type:** Prospective observational evaluation study (adapted CONSORT-AI principles)

**Note:** This study is not a randomized controlled trial but applies CONSORT-AI principles for AI intervention reporting.

---

## SECTION 1: TITLE AND ABSTRACT

| Item | CONSORT-AI Recommendation | Status | Location |
|------|--------------------------|--------|----------|
| 1a | Identification as an AI intervention study in the title | ✓ | Title |
| 1b | Structured abstract with AI intervention details | ✓ | Abstract |

**Evidence:**
- Title includes "Large Language Models" explicitly identifying AI intervention
- Abstract structured with: Background, Methods (AI systems specified), Results, Interpretation
- AI models clearly identified: GPT-4 Turbo, Claude 3 Sonnet, Gemini Pro 1.5

---

## SECTION 2: INTRODUCTION

| Item | CONSORT-AI Recommendation | Status | Location |
|------|--------------------------|--------|----------|
| 2a-AI | Scientific background and rationale for the AI intervention | ✓ | Introduction, paragraphs 1-3 |
| 2b-AI | Specific objectives and hypotheses for AI intervention | ✓ | Introduction, paragraph 4 |

**Evidence:**
- Background: Clinical proteomics increasingly using LLMs for interpretation
- Rationale: Growing concern about factual errors in AI-generated medical information
- Objective: Quantify and characterize hallucination rates in proteomics LLM responses
- Hypothesis: Hallucination rates differ by model, query complexity, and domain

---

## SECTION 3: METHODS - AI Intervention

| Item | CONSORT-AI Recommendation | Status | Location |
|------|--------------------------|--------|----------|
| 3a-AI | Description of the AI intervention | ✓ | Methods, LLM Evaluation |
| 3b-AI | Specify the AI model version and algorithm | ✓ | Methods, AI Models |
| 3c-AI | Describe the AI development and validation | ✓ | Methods, Model Details |
| 3d-AI | Specify the intended use and clinical context | ✓ | Methods, Study Context |

**Evidence:**

### 3a - AI Intervention Description
**Intervention:** Large language models evaluated for factual accuracy in proteomics query responses

**Models tested:**
1. GPT-4 Turbo (gpt-4-0125-preview)
2. Claude 3 Sonnet (claude-3-sonnet-20240229)
3. Gemini Pro 1.5 (gemini-1.5-pro)

**Input:** Standardized proteomics queries (n=500)

**Output:** Free-text responses to queries

**Evaluation:** Binary hallucination classification by expert raters

### 3b - Model Specifications

| Model | Version | Release Date | Parameters | Context Window |
|-------|---------|--------------|------------|----------------|
| GPT-4 Turbo | gpt-4-0125-preview | Jan 2024 | ~1.7T (estimated) | 128k tokens |
| Claude 3 Sonnet | claude-3-sonnet-20240229 | Feb 2024 | Undisclosed | 200k tokens |
| Gemini Pro 1.5 | gemini-1.5-pro | Feb 2024 | Undisclosed | 1M tokens |

**Inference parameters:**
- Temperature: 0.7 (all models)
- Max tokens: 500 (all models)
- Top-p: 0.9 (all models)
- Frequency penalty: 0
- Presence penalty: 0

### 3c - AI Development and Validation
**Developer information:**
- GPT-4 Turbo: OpenAI (San Francisco, CA, USA)
- Claude 3 Sonnet: Anthropic (San Francisco, CA, USA)
- Gemini Pro 1.5: Google DeepMind (London, UK)

**Training data:**
- All models trained on public internet data up to knowledge cutoff dates
- GPT-4 Turbo: September 2023 cutoff
- Claude 3 Sonnet: August 2023 cutoff
- Gemini Pro 1.5: November 2023 cutoff

**Prior validation:**
- All models evaluated on general medical benchmarks (MedQA, USMLE)
- No prior domain-specific validation in proteomics

**Access:** Commercial API access (paid tier, no fine-tuning)

### 3d - Intended Use
**Clinical context:**
- Decision support for proteomics data interpretation
- Literature synthesis for protein function queries
- Educational tool for proteomics trainees

**Scope of evaluation:**
- Protein identification and quantification
- Post-translational modification analysis
- Protein-protein interactions
- Clinical biomarker interpretation
- Mass spectrometry data interpretation

**Safety considerations:**
- Not intended for direct clinical decision-making without expert review
- Evaluated for potential patient harm from inaccurate information

---

## SECTION 4: METHODS - Study Design

| Item | CONSORT-AI Recommendation | Status | Location |
|------|--------------------------|--------|----------|
| 4a-AI | Describe study design and AI workflow integration | ✓ | Methods, Study Design |
| 4b-AI | Explain human oversight and intervention points | ✓ | Methods, Expert Annotation |

**Evidence:**

### 4a - Study Design
**Type:** Prospective observational evaluation study

**Workflow:**
1. Query generation (stratified sampling)
2. LLM response collection (automated API calls)
3. Expert annotation (dual independent raters)
4. Ground truth establishment (consensus)
5. Statistical analysis

**Timeline:** February-June 2024

**Pre-registration:** OSF osf.io/x7mk9 (registered 2024-02-10)

### 4b - Human Oversight
**Level 1:** Query design and validation (authors)
**Level 2:** Response collection monitoring (automated + manual audit)
**Level 3:** Expert annotation (2 independent raters, PhD-level proteomics experts)
**Level 4:** Adjudication (consensus meeting for discrepancies)
**Level 5:** Statistical analysis review (senior statistician)

**Human-AI interaction:** No interactive prompting; single-shot query-response pairs only

---

## SECTION 5: METHODS - Data Handling

| Item | CONSORT-AI Recommendation | Status | Location |
|------|--------------------------|--------|----------|
| 5a-AI | Describe data preprocessing and quality control | ✓ | Methods, Data Processing |
| 5b-AI | Explain handling of AI errors and failures | ✓ | Methods, Error Handling |
| 5c-AI | Describe data augmentation or synthetic data | ✓ | Methods, Query Generation |

**Evidence:**

### 5a - Preprocessing
**Query preprocessing:**
- Manual review for clarity and specificity
- Validation against proteomics knowledge base
- Deduplication check
- Complexity scoring by two authors independently

**Response preprocessing:**
- Extraction from JSON API responses
- Text normalization (Unicode, whitespace)
- Length validation (20-2000 characters)
- Encoding check (UTF-8)

**Quality control:**
- API call success rate: 99.8% (3 failures in 1,503 calls)
- Response completeness: 100% (all responses within token limit)
- Annotation completeness: 100% (dual rating for all responses)

### 5b - Error Handling
**API failures (n=3):**
- Cause: Temporary rate limiting
- Resolution: Retry after 60s delay
- All queries successfully completed

**Malformed responses (n=0):** None detected

**Refusals (n=2):**
- GPT-4 Turbo refused 1 query (perceived medical advice)
- Claude 3 Sonnet refused 1 query (perceived harmful content)
- Handling: Recorded as "refusal" (separate category from hallucination)

### 5c - Data Generation
**Synthetic queries:** All 500 queries synthetically generated by authors

**Method:**
- Template-based generation with domain expert review
- Stratified by complexity (low/medium/high)
- Stratified by domain (5 proteomics subdomains)
- Stratified by prevalence (common/rare proteins)

**No data augmentation:** Original responses used without modification

---

## SECTION 6: METHODS - Statistical Analysis

| Item | CONSORT-AI Recommendation | Status | Location |
|------|--------------------------|--------|----------|
| 6a-AI | Specify AI performance metrics | ✓ | Methods, Outcomes |
| 6b-AI | Describe statistical methods for AI evaluation | ✓ | Methods, Statistical Analysis |
| 6c-AI | Explain handling of multiplicity | ✓ | Methods, Multiple Comparisons |

**Evidence:**

### 6a - Performance Metrics
**Primary outcome:** Hallucination rate (proportion of responses containing factual errors)

**Secondary outcomes:**
- Hallucination severity distribution (minor/moderate/severe/critical)
- Hallucination type frequency (fabrication/misattribution/quantitative error)
- Model calibration (confidence vs. accuracy)
- Consistency across repeated queries

**Diagnostic accuracy metrics:**
- Sensitivity: Proportion of true hallucinations detected
- Specificity: Proportion of accurate responses correctly identified
- Cohen's kappa: Inter-rater agreement

### 6b - Statistical Methods
**Inference:**
- Chi-square tests for model comparison
- Logistic regression for risk factors (complexity, domain, prevalence)
- Bootstrap confidence intervals (n=1,000 iterations)
- McNemar's test for paired comparisons

**Effect sizes:**
- Odds ratios with 95% CI
- Cohen's d for continuous outcomes
- Cramér's V for categorical associations

**Software:** Python 3.11 (scikit-learn 1.3, statsmodels 0.14), R 4.3 (irr 0.84.1)

### 6c - Multiplicity
**Correction method:** Bonferroni correction for family-wise error rate

**Comparisons:**
- 3 pairwise model comparisons (α = 0.05/3 = 0.0167)
- 5 domain comparisons (α = 0.05/5 = 0.01)
- Pre-specified subgroups only (no data-driven exploration)

---

## SECTION 7: RESULTS - AI Performance

| Item | CONSORT-AI Recommendation | Status | Location |
|------|--------------------------|--------|----------|
| 7a-AI | Report AI performance with precision estimates | ✓ | Results, Main Findings |
| 7b-AI | Report subgroup analyses | ✓ | Results, Subgroup Analysis |
| 7c-AI | Report adverse events or safety issues | ✓ | Results, Safety |

**Evidence:**

### 7a - Overall Performance

| Model | Hallucination Rate | 95% CI | Refusals |
|-------|-------------------|--------|----------|
| GPT-4 Turbo | 33.4% (167/500) | 29.9-37.0% | 1 (0.2%) |
| Claude 3 Sonnet | 27.8% (139/500) | 24.4-31.3% | 1 (0.2%) |
| Gemini Pro 1.5 | 32.4% (162/500) | 28.9-36.0% | 0 (0%) |
| **Overall** | **31.2% (468/1500)** | **28.7-33.8%** | **2 (0.1%)** |

**Statistical comparison:**
- Claude vs GPT-4: χ² = 4.21, p = 0.040 (significant after Bonferroni)
- Gemini vs GPT-4: χ² = 0.13, p = 0.72 (not significant)
- Claude vs Gemini: χ² = 3.02, p = 0.082 (not significant)

### 7b - Subgroup Performance

**By Complexity:**
- Low: 18.3% (55/300)
- Medium: 29.0% (174/600)
- High: 47.8% (239/500)
- High vs Low OR = 5.1 (95% CI: 3.8-6.9), p < 0.001

**By Domain:**
- Protein identification: 21.3% (64/300)
- Quantitative expression: 28.7% (86/300)
- PTMs: 42.1% (126/300)
- Protein interactions: 35.2% (106/300)
- Clinical interpretation: 28.7% (86/300)

### 7c - Safety Issues
**Severity classification:**
- Minor (low clinical impact): 33.3% (156/468)
- Moderate (may affect decisions): 40.4% (189/468)
- Severe (likely affects decisions): 20.9% (98/468)
- Critical (patient safety risk): 5.3% (25/468)

**Potentially harmful responses:** 123/1,500 (8.2%)
- Definition: Severe or critical severity + clinical interpretation domain

**No actual patient harm:** Synthetic queries, no real clinical use

---

## SECTION 8: DISCUSSION

| Item | CONSORT-AI Recommendation | Status | Location |
|------|--------------------------|--------|----------|
| 8a-AI | Interpret results in context of AI capabilities and limitations | ✓ | Discussion |
| 8b-AI | Discuss generalizability to other AI systems and settings | ✓ | Discussion, Generalizability |
| 8c-AI | Discuss clinical implications and implementation | ✓ | Discussion, Implications |

**Evidence:**

### 8a - Interpretation
- All three frontier LLMs exhibit substantial hallucination rates (28-33%)
- Claude 3 Sonnet performs best but still produces errors in 1 in 4 responses
- Performance degrades sharply with query complexity
- PTM domain particularly challenging (42% error rate)

### 8b - Generalizability
**Limitations:**
- Evaluated at single time point (model versions evolve)
- English-language queries only
- Synthetic queries (may not reflect real clinical complexity)
- Proteomics-specific (may not generalize to other medical domains)

**Strengths:**
- Three major LLM providers evaluated
- Broad coverage of proteomics domains
- Stratified sampling ensures representativeness

### 8c - Clinical Implications
**Recommendations:**
1. Do not use LLMs for unsupervised clinical proteomics interpretation
2. Implement mandatory expert review for all LLM-generated reports
3. Display uncertainty warnings on LLM interfaces in medical contexts
4. Develop automated hallucination detection systems
5. Establish regulatory oversight for medical AI chatbots

---

## OVERALL COMPLIANCE

**Total CONSORT-AI Items:** 21
**Applicable to This Study:** 21
**Completed:** 21/21 (100%)
**Status:** ✓ FULLY COMPLIANT

**Reviewer:** Olaf Yunus Laitinen Imanov
**Date:** November 9, 2024
**Version:** 1.0

---

## REFERENCES

1. Liu X, Cruz Rivera S, Moher D, et al. Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension. Nat Med. 2020;26(9):1364-1374.
2. Cruz Rivera S, Liu X, Chan AW, et al. Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension. Lancet Digit Health. 2020;2(10):e549-e560.
