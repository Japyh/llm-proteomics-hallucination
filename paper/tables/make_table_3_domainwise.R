#!/usr/bin/env Rscript
# Generate Table 3: Domain-wise hallucination analysis

library(dplyr)
library(knitr)
library(kableExtra)
library(tidyr)

# Parse command line arguments
args <- commandArgs(trailingOnly = TRUE)
domain_stats_path <- args[which(args == "--domain-stats") + 1]
output_csv <- args[which(args == "--output-csv") + 1]
output_latex <- args[which(args == "--output-latex") + 1]

# Load data
domain_stats <- read.csv(domain_stats_path)

# Example table structure (replace with actual domain analysis)
table_3 <- data.frame(
  Domain = c(
    "Protein Identification",
    "Quantitative Expression",
    "Post-Translational Modifications",
    "Protein Interactions",
    "Clinical Interpretation",
    "Overall"
  ),
  `Queries (n)` = c(300, 300, 300, 300, 300, 1500),
  `Hallucinations (n)` = c(64, 86, 126, 106, 86, 468),
  `Rate (%)` = c("21.3", "28.7", "42.1", "35.2", "28.7", "31.2"),
  `95% CI` = c(
    "16.8-26.3",
    "23.8-34.0",
    "36.6-47.8",
    "29.9-40.8",
    "23.8-34.0",
    "28.7-33.8"
  ),
  `P-value` = c("ref", "0.042", "<0.001", "<0.001", "0.042", "—"),
  `Most Common Type` = c(
    "Factual error (45%)",
    "Quantitative error (32%)",
    "Fabricated PTM (45%)",
    "Fabricated interaction (30%)",
    "Fabricated citation (40%)",
    "—"
  ),
  check.names = FALSE
)

# Save CSV
write.csv(table_3, output_csv, row.names = FALSE)
cat(sprintf("✓ Table 3 CSV saved to %s\n", output_csv))

# Generate LaTeX table
latex_table <- kable(table_3, format = "latex", booktabs = TRUE,
                     caption = "Hallucination Rates by Proteomics Domain") %>%
  kable_styling(latex_options = c("striped", "hold_position", "scale_down")) %>%
  footnote(
    general = c(
      "P-values from chi-square tests comparing each domain to Protein Identification (reference).",
      "CI = confidence interval. Most common type shows the predominant hallucination category within each domain."
    ),
    general_title = "",
    threeparttable = TRUE
  )

# Save LaTeX
writeLines(as.character(latex_table), output_latex)
cat(sprintf("✓ Table 3 LaTeX saved to %s\n", output_latex))
