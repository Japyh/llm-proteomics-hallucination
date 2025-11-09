# STARD 2015 Checklist
## Standards for Reporting of Diagnostic Accuracy Studies

**Study Title:** Evaluating Hallucinations in Large Language Model Responses to Proteomics Queries: A Prospective Study

**Journal:** The Lancet Digital Health

**Submission Date:** December 2024

---

## TITLE/ABSTRACT

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 1 | Identify the article as a study of diagnostic accuracy (recommend MeSH heading 'sensitivity and specificity'). | 1 | Title |
| 2 | Structured abstract including study design, methods, results, and conclusions. | 1 | Abstract |

**Status:** ✓ COMPLETE

**Evidence:** Title explicitly identifies this as an evaluation/diagnostic accuracy study of LLM hallucination detection. Abstract follows structured format.

---

## INTRODUCTION

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 3 | Scientific and clinical background, including the intended use and clinical role of the index test | 2-3 | Introduction |
| 4 | Study objectives and hypotheses | 3 | Introduction, end |

**Status:** ✓ COMPLETE

**Evidence:**
- Background covers clinical proteomics context and LLM adoption risks
- Index test (hallucination detection) clearly defined
- Primary objective: quantify hallucination rates across three LLMs
- Secondary objectives: identify risk factors, assess severity

---

## METHODS - Study Design

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 5 | Whether data collection was planned before the index test and reference standard were performed (prospective study) or after (retrospective study) | 4 | Methods, Study Design |
| 6 | Eligibility criteria | 4 | Methods, Participants |
| 7 | On what basis potentially eligible participants were identified | 4 | Methods, Query Generation |
| 8 | Where and when potentially eligible participants were identified | 4 | Methods, Query Generation |
| 9 | Whether participants formed a consecutive, random, or convenience series | 4-5 | Methods, Sampling |

**Status:** ✓ COMPLETE

**Evidence:**
- Prospective design: queries generated before LLM evaluation
- Pre-registered on OSF (osf.io/x7mk9) on 2024-02-10
- Eligibility: proteomics queries spanning 5 domains, stratified by complexity
- Sampling: stratified random sampling, n=500 queries
- Recruitment period: March-April 2024

---

## METHODS - Test Methods

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 10a | Description of the index test, in sufficient detail to allow replication | 5-6 | Methods, LLM Evaluation |
| 10b | Description of the reference standard, in sufficient detail to allow replication | 6 | Methods, Ground Truth |
| 11 | Rationale for choosing the reference standard (if alternatives exist) | 6 | Methods, Ground Truth |
| 12a | Definition of and rationale for test positivity cut-offs or result categories of the index test | 6-7 | Methods, Hallucination Criteria |
| 12b | Definition of and rationale for test positivity cut-offs or result categories of the reference standard | 7 | Methods, Annotation Protocol |
| 13a | Whether clinical information and reference standard results were available to the performers/readers of the index test | 7 | Methods, Blinding |
| 13b | Whether clinical information and index test results were available to the assessors of the reference standard | 7 | Methods, Blinding |

**Status:** ✓ COMPLETE

**Evidence:**
- Index test (LLMs): GPT-4 Turbo, Claude 3 Sonnet, Gemini Pro 1.5
- Parameters specified: temperature=0.7, max_tokens=500
- Reference standard: dual expert annotation (proteomics specialists)
- Cut-offs: binary hallucination classification, 4-level severity
- Blinding: expert raters blinded to model identity
- No clinical information provided to LLMs (synthetic queries)

---

## METHODS - Statistical Analysis

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 14 | Methods for estimating or comparing measures of diagnostic accuracy | 7-8 | Methods, Statistical Analysis |
| 15 | How indeterminate index test or reference standard results were handled | 8 | Methods, Missing Data |
| 16 | How missing data on the index test and reference standard were handled | 8 | Methods, Missing Data |
| 17 | Any analyses of variability in diagnostic accuracy, distinguishing pre-specified from exploratory | 8-9 | Methods, Subgroup Analysis |
| 18 | Intended sample size and how it was determined | 5 | Methods, Sample Size |

**Status:** ✓ COMPLETE

**Evidence:**
- Primary outcome: hallucination rate with 95% CI (bootstrap, n=1000)
- Chi-square tests for model comparison
- Logistic regression for risk factors (complexity, domain, prevalence)
- Bonferroni correction for multiple comparisons
- Inter-rater reliability: Cohen's kappa
- Missing data: complete case analysis (no missing responses)
- Pre-specified subgroups: domain, complexity, prevalence
- Sample size: n=500 queries for 80% power to detect 10% difference

---

## RESULTS - Participants

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 19 | Flow of participants, using a diagram | 10 | Results, Figure 1 |
| 20 | Baseline demographic and clinical characteristics of participants | 10-11 | Results, Table 1 |
| 21a | Distribution of severity of disease in those with the target condition | 11 | Results, Query Characteristics |
| 21b | Distribution of alternative diagnoses in those without the target condition | N/A | - |
| 22 | Time interval and any clinical interventions between index test and reference standard | 11 | Results, Timeline |

**Status:** ✓ COMPLETE (21b N/A - not applicable to this study design)

**Evidence:**
- Flow diagram: 500 queries → 1,500 responses → dual annotation → 468 hallucinations
- Baseline: Table 1 shows query distribution across domains and complexity
- Severity distribution: 156 minor, 189 moderate, 98 severe, 25 critical
- Timeline: LLM responses collected March 15-30, 2024; annotations April 1-15, 2024

---

## RESULTS - Test Results

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 23 | Cross tabulation of the index test results by the reference standard results | 12 | Results, Table 2 |
| 24 | Estimates of diagnostic accuracy and their precision (such as 95% confidence intervals) | 12-13 | Results, Main Findings |
| 25 | Any adverse events from performing the index test or the reference standard | N/A | - |

**Status:** ✓ COMPLETE (25 N/A - no adverse events in observational study)

**Evidence:**
- Table 2: hallucination rates by model with 95% CI
- Overall: 31.2% (95% CI: 28.7-33.8%)
- GPT-4 Turbo: 33.4% (29.9-37.0%)
- Claude 3 Sonnet: 27.8% (24.4-31.3%)
- Gemini Pro 1.5: 32.4% (28.9-36.0%)

---

## RESULTS - Subgroup Analysis

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 26 | Estimates of variability in diagnostic accuracy between subgroups of participants, readers, or centers, if done | 13-14 | Results, Subgroup Analysis |
| 27 | Estimates of test reproducibility, if done | 14 | Results, Consistency |

**Status:** ✓ COMPLETE

**Evidence:**
- Complexity: High complexity OR=5.1 (95% CI: 3.8-6.9), p<0.001
- Domain: Highest rates in PTM identification (42.1%), lowest in protein ID (21.3%)
- Prevalence: Rare entities OR=3.2 (95% CI: 2.4-4.3)
- Reproducibility: Test-retest consistency 89.2% (n=50 repeated queries)

---

## DISCUSSION

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 28 | Study limitations, including sources of potential bias, statistical uncertainty, and generalisability | 15-16 | Discussion, Limitations |
| 29 | Implications for practice, including the intended use and clinical role of the index test | 16-17 | Discussion, Implications |

**Status:** ✓ COMPLETE

**Evidence:**
- Limitations: synthetic queries may not reflect real clinical complexity, English-only, no multi-turn conversations
- Generalizability: findings may not extend to other medical domains
- Clinical implications: LLM-assisted proteomics interpretation requires human oversight
- Recommendations: implement hallucination detection systems, user warnings

---

## OTHER INFORMATION

| Item | Recommendation | Page | Location |
|------|----------------|------|----------|
| 30 | Registration number and name of registry | 1 | Title page footnote |
| 31 | Where the full study protocol can be accessed | 1 | Title page footnote |
| 32 | Sources of funding and other support; role of funders | 17 | Acknowledgments |

**Status:** ✓ COMPLETE

**Evidence:**
- Pre-registration: OSF osf.io/x7mk9 (registered 2024-02-10)
- Protocol: Available at OSF repository
- Funding: Technical University of Denmark internal funding
- Ethics: DTU Research Ethics Committee #2024-DTU-0385

---

## OVERALL COMPLIANCE

**Total Items:** 32 (30 applicable, 2 N/A)
**Completed:** 30/30 (100%)
**Status:** ✓ FULLY COMPLIANT

**Reviewer:** Olaf Yunus Laitinen Imanov
**Date:** November 9, 2024
**Version:** 1.0

---

## REFERENCES

1. Bossuyt PM, Reitsma JB, Bruns DE, et al. STARD 2015: an updated list of essential items for reporting diagnostic accuracy studies. BMJ. 2015;351:h5527.
2. Cohen JF, Korevaar DA, Altman DG, et al. STARD 2015 guidelines for reporting diagnostic accuracy studies: explanation and elaboration. BMJ Open. 2016;6:e012799.
