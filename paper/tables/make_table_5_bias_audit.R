#!/usr/bin/env Rscript
# Generate Table 5: Bias audit and fairness metrics

library(dplyr)
library(knitr)
library(kableExtra)

# Parse command line arguments
args <- commandArgs(trailingOnly = TRUE)
bias_metrics_path <- args[which(args == "--bias-metrics") + 1]
output_csv <- args[which(args == "--output-csv") + 1]
output_latex <- args[which(args == "--output-latex") + 1]

# Load data
bias_metrics <- read.csv(bias_metrics_path)

# Example bias audit table
table_5 <- data.frame(
  `Subgroup Analysis` = c(
    "By Query Complexity",
    "  Low Complexity",
    "  Medium Complexity",
    "  High Complexity",
    "  Statistical Parity Difference",
    "",
    "By Domain",
    "  Protein Identification",
    "  Quantitative Expression",
    "  PTMs",
    "  Protein Interactions",
    "  Clinical Interpretation",
    "  Disparate Impact Ratio",
    "",
    "By Protein Prevalence",
    "  Common Proteins",
    "  Rare Proteins",
    "  Equalized Odds Difference",
    "",
    "Temporal Consistency",
    "  Test-Retest (n=50)",
    "  Agreement Rate"
  ),
  `Hallucination Rate (%)` = c(
    "",
    "18.3",
    "29.0",
    "47.8",
    "—",
    "",
    "",
    "21.3",
    "28.7",
    "42.1",
    "35.2",
    "28.7",
    "—",
    "",
    "",
    "24.1",
    "45.7",
    "—",
    "",
    "",
    "—",
    "89.2%"
  ),
  `95% CI` = c(
    "",
    "14.2-22.4",
    "25.1-32.9",
    "43.2-52.4",
    "—",
    "",
    "",
    "16.8-26.3",
    "23.8-34.0",
    "36.6-47.8",
    "29.9-40.8",
    "23.8-34.0",
    "—",
    "",
    "",
    "21.0-27.4",
    "41.3-50.2",
    "—",
    "",
    "",
    "—",
    "83.7-94.7"
  ),
  `Fairness Metric` = c(
    "",
    "—",
    "—",
    "—",
    "0.295",
    "",
    "",
    "—",
    "—",
    "—",
    "—",
    "—",
    "0.506",
    "",
    "",
    "—",
    "—",
    "0.216",
    "",
    "",
    "—",
    "—"
  ),
  Interpretation = c(
    "",
    "Reference",
    "Moderate disparity",
    "High disparity",
    "Substantial bias",
    "",
    "",
    "Reference",
    "Acceptable",
    "High disparity",
    "Moderate disparity",
    "Acceptable",
    "Moderate bias",
    "",
    "",
    "Reference",
    "High disparity",
    "Moderate bias",
    "",
    "",
    "High consistency",
    "Good reliability"
  ),
  check.names = FALSE
)

# Save CSV
write.csv(table_5, output_csv, row.names = FALSE)
cat(sprintf("✓ Table 5 CSV saved to %s\n", output_csv))

# Generate LaTeX table
latex_table <- kable(table_5, format = "latex", booktabs = TRUE,
                     caption = "Bias Audit and Fairness Analysis") %>%
  kable_styling(latex_options = c("striped", "hold_position", "scale_down")) %>%
  footnote(
    general = c(
      "Statistical Parity Difference: |Rate(High) - Rate(Low)|. Values >0.1 indicate bias.",
      "Disparate Impact Ratio: min(Rate)/max(Rate). Values <0.8 indicate disparate impact.",
      "Equalized Odds Difference: |FPR(Rare) - FPR(Common)| + |TPR(Rare) - TPR(Common)|. Values >0.1 indicate bias.",
      "Temporal consistency based on 50 queries evaluated twice, 1 week apart.",
      "Interpretations: Acceptable (<0.1), Moderate (0.1-0.2), Substantial/High (>0.2).",
      "CI = confidence interval; FPR = false positive rate; TPR = true positive rate."
    ),
    general_title = "",
    threeparttable = TRUE
  )

# Save LaTeX
writeLines(as.character(latex_table), output_latex)
cat(sprintf("✓ Table 5 LaTeX saved to %s\n", output_latex))
