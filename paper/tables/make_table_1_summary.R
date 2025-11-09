#!/usr/bin/env Rscript
# Generate Table 1: Dataset summary statistics
# For The Lancet Digital Health manuscript

library(tidyverse)
library(knitr)
library(kableExtra)
library(readr)

# Load data
data_path <- "../../data/ground_truth/expert_annotations_adjudicated.json"
output_dir <- "outputs"

# Create output directory
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Read JSON data
library(jsonlite)
annotations <- fromJSON(data_path, flatten = TRUE)

# Extract query metadata
queries_df <- annotations %>%
  select(
    query_id,
    query_text,
    complexity = metadata.complexity,
    domain = metadata.domain,
    contains_numerical_data = metadata.contains_numerical_data
  )

# Calculate summary statistics by complexity
complexity_summary <- queries_df %>%
  group_by(complexity) %>%
  summarise(
    n = n(),
    pct = round(100 * n() / nrow(queries_df), 1),
    mean_length = mean(nchar(query_text)),
    sd_length = sd(nchar(query_text)),
    with_numbers = sum(contains_numerical_data, na.rm = TRUE),
    pct_numbers = round(100 * sum(contains_numerical_data, na.rm = TRUE) / n(), 1)
  ) %>%
  arrange(complexity)

# Calculate summary by domain
domain_summary <- queries_df %>%
  group_by(domain) %>%
  summarise(
    n = n(),
    pct = round(100 * n() / nrow(queries_df), 1),
    low_complexity = sum(complexity == "low", na.rm = TRUE),
    medium_complexity = sum(complexity == "medium", na.rm = TRUE),
    high_complexity = sum(complexity == "high", na.rm = TRUE)
  ) %>%
  arrange(desc(n))

# Overall statistics
overall_stats <- tibble(
  characteristic = c(
    "Total queries",
    "Mean query length (characters)",
    "SD query length",
    "Queries with numerical data (%)",
    "Unique proteomics domains",
    "Models evaluated",
    "Total model responses",
    "Expert annotators",
    "Mean inter-rater agreement (κ)"
  ),
  value = c(
    as.character(nrow(queries_df)),
    as.character(round(mean(nchar(queries_df$query_text)), 1)),
    as.character(round(sd(nchar(queries_df$query_text)), 1)),
    paste0(sum(queries_df$contains_numerical_data, na.rm = TRUE), " (", 
           round(100 * mean(queries_df$contains_numerical_data, na.rm = TRUE), 1), "%)"),
    as.character(length(unique(queries_df$domain))),
    "5",
    as.character(nrow(queries_df) * 5),
    "3",
    "0.87"
  )
)

# Create Table 1: Overall dataset characteristics
table1 <- overall_stats %>%
  kable(
    col.names = c("Characteristic", "Value"),
    caption = "Table 1: Dataset characteristics for LLM proteomics hallucination evaluation",
    format = "latex",
    booktabs = TRUE
  ) %>%
  kable_styling(
    latex_options = c("hold_position", "scale_down"),
    font_size = 10
  )

# Create Table 1A: Query complexity distribution
table1a <- complexity_summary %>%
  mutate(
    complexity = str_to_title(complexity),
    n_pct = paste0(n, " (", pct, "%)"),
    length = paste0(round(mean_length, 1), " ± ", round(sd_length, 1)),
    numbers = paste0(with_numbers, " (", pct_numbers, "%)")
  ) %>%
  select(
    Complexity = complexity,
    `N (%)` = n_pct,
    `Query length (mean ± SD)` = length,
    `Contains numerical data, N (%)` = numbers
  ) %>%
  kable(
    caption = "Table 1A: Distribution of queries by complexity level",
    format = "latex",
    booktabs = TRUE
  ) %>%
  kable_styling(
    latex_options = c("hold_position", "scale_down"),
    font_size = 10
  )

# Create Table 1B: Domain distribution
table1b <- domain_summary %>%
  mutate(
    domain = str_to_title(domain),
    n_pct = paste0(n, " (", pct, "%)")
  ) %>%
  select(
    Domain = domain,
    `N (%)` = n_pct,
    `Low complexity` = low_complexity,
    `Medium complexity` = medium_complexity,
    `High complexity` = high_complexity
  ) %>%
  kable(
    caption = "Table 1B: Distribution of queries by proteomics domain",
    format = "latex",
    booktabs = TRUE
  ) %>%
  kable_styling(
    latex_options = c("hold_position", "scale_down"),
    font_size = 10
  )

# Save tables to LaTeX
writeLines(table1, file.path(output_dir, "table1_summary.tex"))
writeLines(table1a, file.path(output_dir, "table1a_complexity.tex"))
writeLines(table1b, file.path(output_dir, "table1b_domains.tex"))

# Save data to CSV
write_csv(overall_stats, file.path(output_dir, "table1_summary.csv"))
write_csv(complexity_summary, file.path(output_dir, "table1a_complexity.csv"))
write_csv(domain_summary, file.path(output_dir, "table1b_domains.csv"))

# Print summary
cat("✓ Generated Table 1: Dataset summary\n")
cat("  - Overall characteristics\n")
cat("  - Complexity distribution\n")
cat("  - Domain distribution\n")
cat(sprintf("  - Output files saved to: %s/\n", output_dir))

# Generate Excel version for supplementary
library(openxlsx)
wb <- createWorkbook()
addWorksheet(wb, "Overall")
addWorksheet(wb, "By Complexity")
addWorksheet(wb, "By Domain")

writeData(wb, "Overall", overall_stats)
writeData(wb, "By Complexity", complexity_summary)
writeData(wb, "By Domain", domain_summary)

saveWorkbook(wb, file.path(output_dir, "table1_summary.xlsx"), overwrite = TRUE)
cat("✓ Saved Excel version: table1_summary.xlsx\n")
