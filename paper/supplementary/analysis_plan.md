# Statistical Analysis Plan

## LLM Proteomics Hallucination Study

**Version**: 1.0  
**Date**: 2025-01-15  
**Pre-registered**: OSF (osf.io/[project-id])

---

## 1. Primary Outcome

**Hallucination Rate** (binary): Proportion of LLM responses containing any hallucination (severity ≥ 1).

**Primary Analysis**:
- Generalized Linear Mixed Model (GLMM) with logit link
- Fixed effects: Model, Complexity, Domain
- Random effects: Query (nested within Domain)
- Statistical significance: α = 0.01 (Bonferroni-corrected for 5 models)

## 2. Secondary Outcomes

1. **Hallucination Severity** (ordinal 0-3)
   - Proportional odds logistic regression
   - Compute Cohen's d for effect sizes

2. **Calibration** (continuous)
   - Expected Calibration Error (ECE)
   - Maximum Calibration Error (MCE)
   - Brier score

3. **Clinical Safety Impact** (ordinal low/medium/high)
   - Kruskal-Wallis test across models
   - Post-hoc Dunn's test with FDR correction

## 3. Exploratory Analyses

- Correlation between model size and performance
- Prompt engineering experiments
- Domain-specific error patterns
- Temporal consistency of responses

## 4. Multiple Testing Correction

- Primary comparisons: Bonferroni (α = 0.05/5 = 0.01)
- Secondary comparisons: Benjamini-Hochberg FDR at q = 0.05
- Exploratory: No correction, clearly labeled

## 5. Missing Data

- Mechanism: Assumed Missing Completely at Random (MCAR)
- Strategy: Multiple imputation with chained equations (MICE, m=10)
- Sensitivity: Complete-case analysis as sensitivity check

## 6. Sample Size and Power

- Target: n = 1,000 queries
- Power: >90% to detect medium effect size (Cohen's h = 0.3)
- Alpha: 0.01 (Bonferroni-corrected)

## 7. Software

- R version 4.3.2
- Python 3.10.12
- Stan 2.32.2 (Bayesian models)
- All analyses reproducible with seed=42
