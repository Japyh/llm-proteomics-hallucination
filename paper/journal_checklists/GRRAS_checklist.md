# GRRAS Checklist
## Guidelines for Reporting Reliability and Agreement Studies

**Study Title:** Evaluating Hallucinations in Large Language Model Responses to Proteomics Queries

**Journal:** The Lancet Digital Health

**Assessment:** Inter-rater reliability of hallucination annotations

---

## A. INTRODUCTION

| Item | Recommendation | Status | Location |
|------|----------------|--------|----------|
| A1 | Describe what was rated, the rating scale(s), and the construct(s) the ratings are supposed to measure | ✓ | Methods, Annotation Protocol |
| A2 | Describe how the sample of subjects or objects was selected | ✓ | Methods, Sampling |
| A3 | Describe how the sample of raters was selected | ✓ | Methods, Expert Raters |
| A4 | Explain how the number of subjects, objects, or raters was chosen | ✓ | Methods, Sample Size |

**Evidence:**

**A1 - What was rated:**
- LLM responses to proteomics queries (n=1,500 responses)
- Binary rating: hallucination present (yes/no)
- Multi-class severity: minor, moderate, severe, critical
- Hallucination type: factual error, fabricated protein, fabricated PTM, fabricated citation, etc.

**A2 - Subject selection:**
- Stratified random sampling of 500 proteomics queries
- Queries spanning 5 domains: protein identification, quantitative expression, PTMs, interactions, clinical interpretation
- Complexity stratification: low (n=200), medium (n=200), high (n=100)

**A3 - Rater selection:**
- Two independent expert raters
- Rater 1: PhD in proteomics, 8 years experience in mass spectrometry
- Rater 2: MD-PhD, clinical proteomics specialist, 6 years experience
- Both raters completed training module on hallucination taxonomy

**A4 - Sample size justification:**
- Target Cohen's kappa ≥ 0.80 for acceptable reliability
- Based on power calculation: n=500 queries for 95% CI width ≤ 0.10
- Each rater annotated all 1,500 responses (3 models × 500 queries)

---

## B. METHODS - Study Design

| Item | Recommendation | Status | Location |
|------|----------------|--------|----------|
| B1 | Describe how many measurements were obtained and their timing | ✓ | Methods, Annotation |
| B2 | Explain whether the sample of rated subjects, objects, or scenes is the same as the sample used to assess reliability | ✓ | Methods, Design |
| B3 | Describe the rater qualifications, their training, and their level of expertise | ✓ | Methods, Expert Raters |
| B4 | Describe the intended use of the measure and the measurement procedure | ✓ | Methods, Annotation Protocol |

**Evidence:**

**B1 - Measurements:**
- Single annotation round per rater (April 1-15, 2024)
- 1,500 responses annotated by each rater independently
- No re-rating or adjudication until after independent completion
- Annotation timeline: 2 weeks (approximately 110 responses per day per rater)

**B2 - Sample consistency:**
- Same 1,500 responses rated by both raters
- No separate reliability subsample
- Complete overlap between reliability assessment and main study sample

**B3 - Rater qualifications:**
- **Rater 1:** PhD (Protein Chemistry), 15 peer-reviewed publications in proteomics, certified clinical mass spectrometry specialist
- **Rater 2:** MD-PhD (Clinical Chemistry), board-certified pathologist, 12 publications in clinical proteomics
- **Training:** Both completed 4-hour training module with 50 practice annotations

**B4 - Intended use and procedure:**
- Purpose: Establish ground truth for LLM hallucination detection
- Procedure:
  1. Read query
  2. Read LLM response
  3. Verify facts against reference databases (UniProt, PubMed)
  4. Classify hallucination (yes/no)
  5. If yes, specify type and severity
  6. Record confidence (1-5 scale)

---

## C. METHODS - Statistical Analysis

| Item | Recommendation | Status | Location |
|------|----------------|--------|----------|
| C1 | State the statistical model and describe how it represents the reliability/agreement data structure | ✓ | Methods, Statistics |
| C2 | State the index/parameter to be estimated and justify its choice | ✓ | Methods, Reliability Metric |
| C3 | Describe methods of point and interval estimation of the index | ✓ | Methods, Analysis Plan |
| C4 | Describe the handling of missing or excluded data | ✓ | Methods, Missing Data |

**Evidence:**

**C1 - Statistical model:**
- Cohen's kappa for inter-rater agreement on binary classification
- Weighted kappa for ordinal severity ratings (quadratic weights)
- Percentage agreement for descriptive statistics
- McNemar's test for systematic disagreement

**C2 - Index justification:**
- Cohen's kappa chosen as primary metric (accounts for chance agreement)
- Interpretation: κ < 0.40 (poor), 0.40-0.59 (fair), 0.60-0.74 (good), 0.75-1.00 (excellent)
- Weighted kappa for severity preserves ordinality

**C3 - Estimation methods:**
- Point estimate: Maximum likelihood estimator
- 95% CI: Bootstrap method with 10,000 resamples
- Statistical software: Python scikit-learn v1.3.0, R irr package v0.84.1

**C4 - Missing data:**
- No missing annotations (complete data for all 1,500 responses)
- Uncertain ratings (confidence <3) retained in main analysis
- Sensitivity analysis excluding uncertain ratings (n=73, 4.9%)

---

## D. RESULTS - Sample

| Item | Recommendation | Status | Location |
|------|----------------|--------|----------|
| D1 | Report the sampling method used to obtain subjects, objects, and raters | ✓ | Results, Participants |
| D2 | Report the sample size of subjects/objects and raters | ✓ | Results, Sample Size |
| D3 | Report the number of measurements obtained | ✓ | Results, Measurements |
| D4 | Report the number and proportion of missing or excluded data | ✓ | Results, Data Completeness |

**Evidence:**

**D1 - Sampling:**
- Subjects: Stratified random sampling of proteomics queries
- Raters: Purposive sampling of proteomics experts
- Geographic: Both raters affiliated with Technical University of Denmark

**D2 - Sample size:**
- Queries: n=500
- LLM responses: n=1,500 (3 models)
- Raters: n=2 independent experts
- Pairwise comparisons: 1,500 response pairs

**D3 - Measurements:**
- Total annotations: 3,000 (1,500 per rater)
- Binary classifications: 3,000
- Severity ratings: 937 (responses classified as hallucinations)
- Type classifications: 937

**D4 - Completeness:**
- Missing data: 0 (0%)
- Excluded: 0 (0%)
- Uncertain ratings (confidence <3): 73 (4.9%)
- Data completeness: 100%

---

## E. RESULTS - Estimates

| Item | Recommendation | Status | Location |
|------|----------------|--------|----------|
| E1 | Report point estimates of the reliability/agreement index | ✓ | Results, Reliability |
| E2 | Report interval estimates of the reliability/agreement index | ✓ | Results, Table 3 |
| E3 | If relevant, report results of all subgroups | ✓ | Results, Subgroup Reliability |

**Evidence:**

**E1 - Point estimates:**
- **Binary hallucination:** Cohen's κ = 0.89
- **Severity rating:** Weighted κ = 0.84
- **Hallucination type:** Multi-rater κ = 0.81
- **Percentage agreement:** 94.3%

**E2 - Interval estimates:**
- Binary κ: 0.89 (95% CI: 0.86-0.92)
- Severity κ: 0.84 (95% CI: 0.80-0.88)
- Type κ: 0.81 (95% CI: 0.77-0.85)
- Agreement: 94.3% (95% CI: 93.1-95.4%)

**E3 - Subgroup analysis:**

| Subgroup | Cohen's κ | 95% CI |
|----------|-----------|--------|
| GPT-4 Turbo | 0.87 | 0.83-0.91 |
| Claude 3 Sonnet | 0.90 | 0.86-0.93 |
| Gemini Pro 1.5 | 0.88 | 0.84-0.92 |
| Low complexity | 0.91 | 0.88-0.94 |
| High complexity | 0.85 | 0.80-0.89 |
| Protein ID domain | 0.92 | 0.89-0.95 |
| PTM domain | 0.84 | 0.79-0.88 |

---

## F. DISCUSSION

| Item | Recommendation | Status | Location |
|------|----------------|--------|----------|
| F1 | Interpret the results in the context of previous studies | ✓ | Discussion, Comparison |
| F2 | Discuss the implications of the results for the use of the measurement | ✓ | Discussion, Implications |
| F3 | Identify limitations and suggest future research | ✓ | Discussion, Limitations |

**Evidence:**

**F1 - Context:**
- Our inter-rater reliability (κ=0.89) exceeds typical medical annotation studies (median κ=0.70)
- Comparable to expert pathology concordance (κ=0.85-0.90)
- Surpasses prior LLM evaluation studies in medicine (κ=0.65-0.75)

**F2 - Implications:**
- High reliability validates ground truth for LLM evaluation
- Supports use of single expert rater for future proteomics LLM studies
- Annotation protocol can be standardized for multi-site studies

**F3 - Limitations:**
- Two raters only; larger panel would strengthen confidence
- Both raters from same institution (potential shared biases)
- Limited to English language responses
- Future: develop automated pre-screening to reduce annotation burden

---

## OVERALL COMPLIANCE

**Total Items:** 18
**Completed:** 18/18 (100%)
**Status:** ✓ FULLY COMPLIANT

**Primary Reliability Metric:** Cohen's κ = 0.89 (95% CI: 0.86-0.92)
**Interpretation:** Excellent inter-rater agreement

**Reviewer:** Olaf Yunus Laitinen Imanov
**Date:** November 9, 2024
**Version:** 1.0

---

## REFERENCES

1. Kottner J, Audigé L, Brorson S, et al. Guidelines for Reporting Reliability and Agreement Studies (GRRAS) were proposed. J Clin Epidemiol. 2011;64(1):96-106.
2. Landis JR, Koch GG. The measurement of observer agreement for categorical data. Biometrics. 1977;33(1):159-174.
