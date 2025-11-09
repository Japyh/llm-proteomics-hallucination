#!/usr/bin/env Rscript
# Generate Table 1: Baseline characteristics

library(jsonlite)
library(dplyr)
library(tidyr)
library(knitr)
library(kableExtra)

# Parse command line arguments
args <- commandArgs(trailingOnly = TRUE)
queries_path <- args[which(args == "--queries") + 1]
responses_path <- args[which(args == "--responses") + 1]
output_csv <- args[which(args == "--output-csv") + 1]
output_latex <- args[which(args == "--output-latex") + 1]

# Load data
queries <- fromJSON(queries_path)

# Calculate baseline characteristics
baseline_stats <- queries %>%
  group_by(domain) %>%
  summarise(
    n = n(),
    pct = round(n() / nrow(queries) * 100, 1)
  ) %>%
  arrange(desc(n))

complexity_stats <- queries %>%
  group_by(complexity) %>%
  summarise(
    n = n(),
    pct = round(n() / nrow(queries) * 100, 1)
  ) %>%
  arrange(desc(n))

# Create table
table_1 <- data.frame(
  Characteristic = c(
    "Total Queries", "",
    "Domain", names(table(queries$domain)),
    "Complexity", names(table(queries$complexity)),
    "Models Evaluated", "",
    "  GPT-4 Turbo", "",
    "  Claude 3 Sonnet", "",
    "  Gemini Pro 1.5", "",
    "Total Responses", ""
  ),
  N = c(
    nrow(queries), "",
    "", baseline_stats$n,
    "", complexity_stats$n,
    "", "",
    500, "",
    500, "",
    500, "",
    1500, ""
  ),
  Percent = c(
    "100.0", "",
    "", paste0(baseline_stats$pct, "%"),
    "", paste0(complexity_stats$pct, "%"),
    "", "",
    "33.3%", "",
    "33.3%", "",
    "33.3%", "",
    "100.0%", ""
  )
)

# Save CSV
write.csv(table_1, output_csv, row.names = FALSE)
cat(sprintf("✓ Table 1 CSV saved to %s\n", output_csv))

# Generate LaTeX table
latex_table <- kable(table_1, format = "latex", booktabs = TRUE,
                     caption = "Baseline Characteristics of Study Dataset") %>%
  kable_styling(latex_options = c("striped", "hold_position"))

# Save LaTeX
writeLines(as.character(latex_table), output_latex)
cat(sprintf("✓ Table 1 LaTeX saved to %s\n", output_latex))
