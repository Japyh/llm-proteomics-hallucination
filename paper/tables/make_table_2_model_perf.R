#!/usr/bin/env Rscript
# Generate Table 2: Model performance metrics
# For The Lancet Digital Health manuscript

library(tidyverse)
library(knitr)
library(kableExtra)
library(readr)

output_dir <- "outputs"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Load results data
results_path <- "../../data/results/model_comparison_metrics.csv"
results_df <- read_csv(results_path, show_col_types = FALSE)

# Calculate performance metrics by model
model_performance <- results_df %>%
  group_by(model) %>%
  summarise(
    total_queries = n(),
    hallucination_rate = mean(hallucination_present) * 100,
    hallucination_se = sqrt(hallucination_rate * (100 - hallucination_rate) / n()),
    mean_severity = mean(severity_score),
    severity_sd = sd(severity_score),
    severe_rate = mean(severity_score == 3) * 100,
    ece = first(expected_calibration_error),
    accuracy = mean(severity_score == 0) * 100,
    .groups = "drop"
  ) %>%
  arrange(hallucination_rate)

# Format for publication
table2 <- model_performance %>%
  mutate(
    Model = case_when(
      model == "gpt4-turbo" ~ "GPT-4 Turbo",
      model == "claude-sonnet" ~ "Claude 3 Sonnet",
      model == "gemini-pro" ~ "Gemini 1.5 Pro",
      model == "mistral-large-2" ~ "Mistral Large 2",
      model == "llama3-70b" ~ "Llama 3 70B",
      TRUE ~ model
    ),
    `Accuracy (%)` = sprintf("%.1f (%.1f–%.1f)", 
                            accuracy, 
                            accuracy - 1.96 * hallucination_se,
                            accuracy + 1.96 * hallucination_se),
    `Hallucination rate (%)` = sprintf("%.1f (%.1f–%.1f)", 
                                      hallucination_rate,
                                      hallucination_rate - 1.96 * hallucination_se,
                                      hallucination_rate + 1.96 * hallucination_se),
    `Mean severity` = sprintf("%.2f ± %.2f", mean_severity, severity_sd),
    `Severe hallucinations (%)` = sprintf("%.1f", severe_rate),
    `ECE` = sprintf("%.3f", ece)
  ) %>%
  select(Model, `Accuracy (%)`, `Hallucination rate (%)`, 
         `Mean severity`, `Severe hallucinations (%)`, ECE)

# Create LaTeX table
latex_table <- table2 %>%
  kable(
    caption = "Table 2: Model performance on proteomics hallucination evaluation",
    format = "latex",
    booktabs = TRUE,
    align = c("l", "c", "c", "c", "c", "c")
  ) %>%
  kable_styling(
    latex_options = c("hold_position", "scale_down"),
    font_size = 9
  ) %>%
  add_header_above(c(" " = 1, "Overall Performance" = 2, "Hallucination Severity" = 2, "Calibration" = 1)) %>%
  footnote(
    general = "Values shown as estimate (95% CI) or mean ± SD. ECE = Expected Calibration Error. Lower ECE indicates better calibration.",
    threeparttable = TRUE
  )

# Performance by complexity
complexity_perf <- results_df %>%
  group_by(model, complexity) %>%
  summarise(
    hallucination_rate = mean(hallucination_present) * 100,
    .groups = "drop"
  ) %>%
  pivot_wider(
    names_from = complexity,
    values_from = hallucination_rate,
    names_prefix = "complexity_"
  ) %>%
  mutate(
    Model = case_when(
      model == "gpt4-turbo" ~ "GPT-4 Turbo",
      model == "claude-sonnet" ~ "Claude 3 Sonnet",
      model == "gemini-pro" ~ "Gemini 1.5 Pro",
      model == "mistral-large-2" ~ "Mistral Large 2",
      model == "llama3-70b" ~ "Llama 3 70B",
      TRUE ~ model
    )
  ) %>%
  select(Model, starts_with("complexity_"))

table2_complexity <- complexity_perf %>%
  kable(
    caption = "Table 2A: Hallucination rates by query complexity",
    col.names = c("Model", "Low (%)", "Medium (%)", "High (%)"),
    format = "latex",
    booktabs = TRUE,
    digits = 1
  ) %>%
  kable_styling(
    latex_options = c("hold_position"),
    font_size = 9
  )

# Save outputs
writeLines(latex_table, file.path(output_dir, "table2_model_performance.tex"))
writeLines(table2_complexity, file.path(output_dir, "table2a_complexity.tex"))

write_csv(table2, file.path(output_dir, "table2_model_performance.csv"))
write_csv(complexity_perf, file.path(output_dir, "table2a_complexity.csv"))

# Excel version
library(openxlsx)
wb <- createWorkbook()
addWorksheet(wb, "Overall Performance")
addWorksheet(wb, "By Complexity")

writeData(wb, "Overall Performance", table2)
writeData(wb, "By Complexity", complexity_perf)

saveWorkbook(wb, file.path(output_dir, "table2_model_performance.xlsx"), overwrite = TRUE)

cat("✓ Generated Table 2: Model performance\n")
cat("  - Overall metrics\n")
cat("  - Performance by complexity\n")
cat(sprintf("  - Output files saved to: %s/\n", output_dir))
