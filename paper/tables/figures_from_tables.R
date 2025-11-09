#!/usr/bin/env Rscript
# Generate figures from table data
# Supplementary visualizations

library(tidyverse)
library(ggplot2)
library(patchwork)

output_dir <- "outputs"
fig_dir <- "../figures/output"

# Load table data
model_perf <- read_csv(file.path(output_dir, "table2_model_performance.csv"), 
                      show_col_types = FALSE)
complexity <- read_csv(file.path(output_dir, "table2a_complexity.csv"),
                      show_col_types = FALSE)

# Set theme
theme_set(theme_minimal(base_size = 10))

# Figure: Model performance comparison
p1 <- model_perf %>%
  mutate(
    Model = factor(Model, levels = Model),
    hall_rate = as.numeric(str_extract(`Hallucination rate (%)`, "^[0-9.]+"))
  ) %>%
  ggplot(aes(x = Model, y = hall_rate, fill = Model)) +
  geom_col(alpha = 0.8) +
  geom_text(aes(label = sprintf("%.1f%%", hall_rate)), 
            vjust = -0.5, size = 3) +
  labs(
    title = "Hallucination Rates by Model",
    x = NULL,
    y = "Hallucination Rate (%)"
  ) +
  scale_fill_brewer(palette = "Set2") +
  theme(
    legend.position = "none",
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

# Figure: Complexity impact
p2 <- complexity %>%
  pivot_longer(
    cols = starts_with("complexity_"),
    names_to = "complexity",
    values_to = "rate",
    names_prefix = "complexity_"
  ) %>%
  mutate(
    complexity = factor(complexity, levels = c("low", "medium", "high")),
    Model = factor(Model, levels = unique(Model))
  ) %>%
  ggplot(aes(x = complexity, y = rate, color = Model, group = Model)) +
  geom_line(size = 1) +
  geom_point(size = 3) +
  labs(
    title = "Impact of Query Complexity",
    x = "Query Complexity",
    y = "Hallucination Rate (%)"
  ) +
  scale_color_brewer(palette = "Set1") +
  theme(legend.position = "bottom")

# Combine
combined <- p1 / p2 + plot_annotation(
  title = "Model Performance Summary",
  tag_levels = "A"
)

ggsave(
  file.path(fig_dir, "supplementary_model_comparison.png"),
  combined,
  width = 10, height = 8, dpi = 300
)

cat("✓ Generated supplementary figures from tables\n")
