# Statistical Power Analysis for Study Design
# Calculate required sample sizes and achieved power

library(pwr)
library(ggplot2)

#' Calculate required sample size for proportion test
#'
#' @param p1 Expected proportion in group 1
#' @param p2 Expected proportion in group 2
#' @param power Desired statistical power (default 0.80)
#' @param alpha Significance level (default 0.05)
#' @return Required sample size per group
sample_size_proportion <- function(p1, p2, power = 0.80, alpha = 0.05) {
  h <- ES.h(p1, p2)  # Effect size
  
  result <- pwr.2p.test(
    h = h,
    sig.level = alpha,
    power = power
  )
  
  ceiling(result$n)
}

#' Calculate achieved power for given sample size
#'
#' @param n Sample size per group
#' @param p1 Proportion in group 1
#' @param p2 Proportion in group 2
#' @param alpha Significance level
#' @return Achieved statistical power
achieved_power <- function(n, p1, p2, alpha = 0.05) {
  h <- ES.h(p1, p2)
  
  result <- pwr.2p.test(
    n = n,
    h = h,
    sig.level = alpha
  )
  
  result$power
}

#' Plot power curve
#'
#' @param p1 Proportion in group 1
#' @param p2 Proportion in group 2
#' @param n_range Range of sample sizes to plot
plot_power_curve <- function(p1, p2, n_range = 50:500) {
  powers <- sapply(n_range, function(n) achieved_power(n, p1, p2))
  
  df <- data.frame(
    sample_size = n_range,
    power = powers
  )
  
  ggplot(df, aes(x = sample_size, y = power)) +
    geom_line(size = 1.2, color = "steelblue") +
    geom_hline(yintercept = 0.80, linetype = "dashed", color = "red") +
    labs(
      title = "Power Curve for Hallucination Rate Comparison",
      x = "Sample Size (per group)",
      y = "Statistical Power",
      caption = paste("Effect size: h =", round(ES.h(p1, p2), 3))
    ) +
    theme_minimal() +
    theme(plot.title = element_text(face = "bold"))
}

# Study-specific power analysis
hallucination_power_analysis <- function() {
  # Expected hallucination rates
  p_gpt4 <- 0.33
  p_claude <- 0.28
  
  # Calculate required sample size for 80% power
  n_required <- sample_size_proportion(p_gpt4, p_claude, power = 0.80)
  
  cat("=== Power Analysis Results ===\n")
  cat(sprintf("Expected hallucination rate GPT-4: %.1f%%\n", p_gpt4 * 100))
  cat(sprintf("Expected hallucination rate Claude: %.1f%%\n", p_claude * 100))
  cat(sprintf("Required sample size per model: %d\n", n_required))
  cat(sprintf("Total queries needed: %d\n", n_required * 2))
  
  # Check achieved power with current sample size
  current_n <- 500
  power_achieved <- achieved_power(current_n, p_gpt4, p_claude)
  cat(sprintf("\nAchieved power with n=%d: %.3f\n", current_n, power_achieved))
}

# Run analysis
hallucination_power_analysis()
