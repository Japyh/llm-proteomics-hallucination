# Effect Size Analysis for Hallucination Study
# Calculate Cohen's d, odds ratios, and other effect sizes

library(effsize)
library(pwr)
library(tidyverse)

#' Calculate Cohen's d for hallucination rate differences
#'
#' @param group1 Hallucination rates for group 1
#' @param group2 Hallucination rates for group 2
#' @return Cohen's d effect size
calculate_cohens_d <- function(group1, group2) {
  cohen.d(group1, group2, hedges.correction = TRUE)
}

#' Calculate odds ratio for binary outcomes
#'
#' @param exposure Binary exposure variable
#' @param outcome Binary outcome variable
#' @return Odds ratio with 95% CI
calculate_odds_ratio <- function(exposure, outcome) {
  table_2x2 <- table(exposure, outcome)
  
  or <- (table_2x2[1,1] * table_2x2[2,2]) / (table_2x2[1,2] * table_2x2[2,1])
  
  # Calculate 95% CI using logistic regression
  model <- glm(outcome ~ exposure, family = binomial())
  ci <- confint(model, level = 0.95)
  
  list(
    odds_ratio = or,
    log_or = coef(model)[2],
    ci_lower = exp(ci[2,1]),
    ci_upper = exp(ci[2,2])
  )
}

#' Interpret effect size magnitude
#'
#' @param d Cohen's d value
#' @return Interpretation string
interpret_effect_size <- function(d) {
  abs_d <- abs(d)
  
  if (abs_d < 0.2) {
    "negligible"
  } else if (abs_d < 0.5) {
    "small"
  } else if (abs_d < 0.8) {
    "medium"
  } else {
    "large"
  }
}

# Example analysis
if (FALSE) {
  # Load data
  data <- read.csv("data/results/hallucination_rates.csv")
  
  # Calculate effect sizes between models
  gpt4_rates <- data %>% filter(model == "GPT-4") %>% pull(hallucination_rate)
  claude_rates <- data %>% filter(model == "Claude") %>% pull(hallucination_rate)
  
  effect_size <- calculate_cohens_d(gpt4_rates, claude_rates)
  
  print(paste("Cohen's d:", round(effect_size$estimate, 3)))
  print(paste("Interpretation:", interpret_effect_size(effect_size$estimate)))
}
