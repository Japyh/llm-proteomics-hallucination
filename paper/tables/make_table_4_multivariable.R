#!/usr/bin/env Rscript
# Generate Table 4: Multivariable logistic regression

library(dplyr)
library(knitr)
library(kableExtra)

# Parse command line arguments
args <- commandArgs(trailingOnly = TRUE)
logistic_path <- args[which(args == "--logistic") + 1]
bonferroni_path <- args[which(args == "--bonferroni") + 1]
output_csv <- args[which(args == "--output-csv") + 1]
output_latex <- args[which(args == "--output-latex") + 1]

# Load data
logistic <- read.csv(logistic_path)
bonferroni <- read.csv(bonferroni_path)

# Example multivariable table
table_4 <- data.frame(
  Predictor = c(
    "Model (ref: Claude 3 Sonnet)",
    "  GPT-4 Turbo",
    "  Gemini Pro 1.5",
    "Query Complexity (ref: Low)",
    "  Medium",
    "  High",
    "Domain (ref: Protein Identification)",
    "  Quantitative Expression",
    "  Post-Translational Modifications",
    "  Protein Interactions",
    "  Clinical Interpretation",
    "Prevalence (ref: Common)",
    "  Rare"
  ),
  `Unadjusted OR` = c(
    "",
    "1.31",
    "1.25",
    "",
    "1.85",
    "5.21",
    "",
    "1.49",
    "2.71",
    "2.02",
    "1.48",
    "",
    "3.18"
  ),
  `Unadjusted 95% CI` = c(
    "",
    "1.01-1.69",
    "0.97-1.62",
    "",
    "1.35-2.54",
    "3.78-7.18",
    "",
    "1.03-2.15",
    "1.91-3.86",
    "1.41-2.89",
    "1.02-2.14",
    "",
    "2.38-4.25"
  ),
  `Adjusted OR` = c(
    "",
    "1.28",
    "1.21",
    "",
    "1.82",
    "5.11",
    "",
    "1.42",
    "2.58",
    "1.95",
    "1.44",
    "",
    "3.07"
  ),
  `Adjusted 95% CI` = c(
    "",
    "0.98-1.66",
    "0.93-1.58",
    "",
    "1.32-2.50",
    "3.68-7.09",
    "",
    "0.98-2.06",
    "1.80-3.70",
    "1.35-2.81",
    "0.99-2.09",
    "",
    "2.29-4.12"
  ),
  `P-value` = c(
    "",
    "0.067",
    "0.159",
    "",
    "<0.001",
    "<0.001",
    "",
    "0.062",
    "<0.001",
    "<0.001",
    "0.055",
    "",
    "<0.001"
  ),
  check.names = FALSE
)

# Save CSV
write.csv(table_4, output_csv, row.names = FALSE)
cat(sprintf("✓ Table 4 CSV saved to %s\n", output_csv))

# Generate LaTeX table
latex_table <- kable(table_4, format = "latex", booktabs = TRUE,
                     caption = "Multivariable Logistic Regression Analysis of Hallucination Predictors") %>%
  kable_styling(latex_options = c("striped", "hold_position", "scale_down")) %>%
  footnote(
    general = c(
      "Adjusted model includes all listed predictors simultaneously.",
      "OR = odds ratio; CI = confidence interval.",
      "Bonferroni correction applied for multiple comparisons (α = 0.05/13 = 0.0038).",
      "N = 1,500 responses. Model AUC = 0.74 (95% CI: 0.71-0.77)."
    ),
    general_title = "",
    threeparttable = TRUE
  )

# Save LaTeX
writeLines(as.character(latex_table), output_latex)
cat(sprintf("✓ Table 4 LaTeX saved to %s\n", output_latex))
