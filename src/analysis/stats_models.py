"""
Statistical modeling functions for hallucination analysis.

Implements chi-square tests, logistic regression, Bayesian models,
and confidence interval calculations.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import stats
from scipy.stats import beta
from statsmodels.stats.proportion import proportion_confint
import statsmodels.api as sm
import statsmodels.formula.api as smf
from dataclasses import dataclass


@dataclass
class HallucinationRateResult:
    """Results of hallucination rate calculation."""
    rate: float
    count: int
    total: int
    ci_lower: float
    ci_upper: float
    method: str


def calculate_hallucination_rates(
    df: pd.DataFrame,
    groupby: Optional[List[str]] = None,
    ci_method: str = "wilson"
) -> pd.DataFrame:
    """
    Calculate hallucination rates with confidence intervals.

    Args:
        df: DataFrame with hallucination labels
        groupby: Columns to group by (e.g., ['model', 'domain'])
        ci_method: CI calculation method ('wilson', 'agresti_coull', 'beta')

    Returns:
        DataFrame with rates and confidence intervals
    """
    if groupby:
        grouped = df.groupby(groupby)
    else:
        grouped = [(None, df)]

    results = []

    for group_key, group_df in grouped:
        total = len(group_df)
        hallucinations = group_df['has_hallucination'].sum()
        rate = hallucinations / total if total > 0 else 0

        # Calculate confidence interval
        ci_lower, ci_upper = proportion_confint(
            hallucinations,
            total,
            alpha=0.05,
            method=ci_method
        )

        result = {
            'total': total,
            'hallucinations': hallucinations,
            'rate': rate,
            'rate_percent': rate * 100,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'ci_lower_percent': ci_lower * 100,
            'ci_upper_percent': ci_upper * 100,
        }

        if groupby:
            if isinstance(group_key, tuple):
                for i, col in enumerate(groupby):
                    result[col] = group_key[i]
            else:
                result[groupby[0]] = group_key

        results.append(result)

    return pd.DataFrame(results)


def chi_square_test(
    df: pd.DataFrame,
    group_col: str,
    outcome_col: str = 'has_hallucination',
    bonferroni_correction: bool = False
) -> Dict:
    """
    Perform chi-square test for group differences.

    Args:
        df: DataFrame with data
        group_col: Column defining groups
        outcome_col: Binary outcome column
        bonferroni_correction: Apply Bonferroni correction

    Returns:
        Dictionary with test results
    """
    # Create contingency table
    contingency = pd.crosstab(df[group_col], df[outcome_col])

    # Chi-square test
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

    # Calculate effect size (Cramér's V)
    n = contingency.sum().sum()
    min_dim = min(contingency.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0

    # Pairwise comparisons
    pairwise = []
    groups = df[group_col].unique()
    n_comparisons = len(groups) * (len(groups) - 1) // 2

    for i, group1 in enumerate(groups):
        for group2 in groups[i+1:]:
            subset = df[df[group_col].isin([group1, group2])]
            cont_subset = pd.crosstab(subset[group_col], subset[outcome_col])

            if cont_subset.shape == (2, 2):
                chi2_pair, p_pair, _, _ = stats.chi2_contingency(cont_subset)

                # Bonferroni correction
                if bonferroni_correction:
                    p_adjusted = min(p_pair * n_comparisons, 1.0)
                else:
                    p_adjusted = p_pair

                pairwise.append({
                    'group1': group1,
                    'group2': group2,
                    'chi2': chi2_pair,
                    'p_value': p_pair,
                    'p_adjusted': p_adjusted,
                    'significant': p_adjusted < 0.05
                })

    return {
        'chi2': chi2,
        'p_value': p_value,
        'dof': dof,
        'cramers_v': cramers_v,
        'n': n,
        'contingency_table': contingency,
        'pairwise_comparisons': pairwise
    }


def logistic_regression(
    df: pd.DataFrame,
    outcome: str = 'has_hallucination',
    predictors: Optional[List[str]] = None,
    formula: Optional[str] = None
) -> Dict:
    """
    Fit logistic regression model.

    Args:
        df: DataFrame with data
        outcome: Binary outcome variable
        predictors: List of predictor variables
        formula: Optional R-style formula (overrides predictors)

    Returns:
        Dictionary with model results
    """
    if formula:
        model = smf.logit(formula, data=df).fit()
    elif predictors:
        X = df[predictors]
        X = sm.add_constant(X)
        X = pd.get_dummies(X, drop_first=True)  # One-hot encode categoricals
        y = df[outcome]
        model = sm.Logit(y, X).fit()
    else:
        raise ValueError("Must provide either formula or predictors")

    # Extract coefficients and odds ratios
    params = model.params
    conf_int = model.conf_int()
    p_values = model.pvalues

    # Odds ratios
    odds_ratios = np.exp(params)
    or_ci = np.exp(conf_int)

    results_table = pd.DataFrame({
        'coefficient': params,
        'odds_ratio': odds_ratios,
        'or_ci_lower': or_ci[0],
        'or_ci_upper': or_ci[1],
        'p_value': p_values,
        'significant': p_values < 0.05
    })

    # Model diagnostics
    diagnostics = {
        'aic': model.aic,
        'bic': model.bic,
        'log_likelihood': model.llf,
        'pseudo_r2': model.prsquared,
        'n_obs': model.nobs
    }

    return {
        'model': model,
        'results_table': results_table,
        'diagnostics': diagnostics,
        'summary': model.summary()
    }


def calculate_confidence_intervals(
    successes: int,
    trials: int,
    confidence: float = 0.95,
    method: str = "wilson"
) -> Tuple[float, float]:
    """
    Calculate confidence interval for proportion.

    Args:
        successes: Number of successes
        trials: Total number of trials
        confidence: Confidence level (default 0.95)
        method: Method for CI calculation

    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    alpha = 1 - confidence

    ci_lower, ci_upper = proportion_confint(
        successes,
        trials,
        alpha=alpha,
        method=method
    )

    return ci_lower, ci_upper


def bayesian_beta_binomial(
    successes: int,
    trials: int,
    prior_alpha: float = 1.0,
    prior_beta: float = 1.0,
    n_samples: int = 10000
) -> Dict:
    """
    Bayesian Beta-Binomial analysis for hallucination rates.

    Args:
        successes: Number of hallucinations
        trials: Total queries
        prior_alpha: Beta prior alpha parameter
        prior_beta: Beta prior beta parameter
        n_samples: Number of posterior samples

    Returns:
        Dictionary with posterior statistics and samples
    """
    # Posterior parameters
    post_alpha = prior_alpha + successes
    post_beta = prior_beta + (trials - successes)

    # Generate samples
    posterior_samples = beta.rvs(post_alpha, post_beta, size=n_samples)

    # Calculate statistics
    posterior_mean = post_alpha / (post_alpha + post_beta)
    posterior_mode = (post_alpha - 1) / (post_alpha + post_beta - 2) if post_alpha > 1 and post_beta > 1 else None

    # Credible interval
    credible_interval = (
        np.percentile(posterior_samples, 2.5),
        np.percentile(posterior_samples, 97.5)
    )

    return {
        'posterior_mean': posterior_mean,
        'posterior_mode': posterior_mode,
        'posterior_median': np.median(posterior_samples),
        'credible_interval_95': credible_interval,
        'posterior_samples': posterior_samples,
        'posterior_alpha': post_alpha,
        'posterior_beta': post_beta
    }


def compare_models_bayesian(
    model1_successes: int,
    model1_trials: int,
    model2_successes: int,
    model2_trials: int,
    n_samples: int = 10000
) -> Dict:
    """
    Bayesian comparison of hallucination rates between two models.

    Args:
        model1_successes: Model 1 hallucinations
        model1_trials: Model 1 total queries
        model2_successes: Model 2 hallucinations
        model2_trials: Model 2 total queries
        n_samples: Number of posterior samples

    Returns:
        Dictionary with comparison results
    """
    # Get posterior distributions
    posterior1 = bayesian_beta_binomial(model1_successes, model1_trials, n_samples=n_samples)
    posterior2 = bayesian_beta_binomial(model2_successes, model2_trials, n_samples=n_samples)

    samples1 = posterior1['posterior_samples']
    samples2 = posterior2['posterior_samples']

    # Calculate probability that model1 has lower hallucination rate
    prob_model1_better = np.mean(samples1 < samples2)

    # Difference in rates
    rate_diff = samples1 - samples2
    mean_diff = np.mean(rate_diff)
    credible_interval_diff = (
        np.percentile(rate_diff, 2.5),
        np.percentile(rate_diff, 97.5)
    )

    return {
        'prob_model1_lower': prob_model1_better,
        'prob_model2_lower': 1 - prob_model1_better,
        'mean_difference': mean_diff,
        'credible_interval_difference': credible_interval_diff,
        'posterior1': posterior1,
        'posterior2': posterior2
    }


def cochran_armitage_trend_test(
    df: pd.DataFrame,
    ordered_group_col: str,
    outcome_col: str = 'has_hallucination'
) -> Dict:
    """
    Cochran-Armitage trend test for ordered categorical variable.

    Args:
        df: DataFrame with data
        ordered_group_col: Ordered categorical column (e.g., complexity: low, medium, high)
        outcome_col: Binary outcome

    Returns:
        Dictionary with test results
    """
    # Create contingency table
    contingency = pd.crosstab(df[ordered_group_col], df[outcome_col])

    # Assign scores to categories (0, 1, 2, ...)
    categories = sorted(df[ordered_group_col].unique())
    scores = {cat: idx for idx, cat in enumerate(categories)}

    # Calculate trend statistic
    n = len(df)
    n_pos = df[outcome_col].sum()
    n_neg = n - n_pos

    # Calculate trend statistic manually
    numerator = 0
    denominator_sum_x = 0
    denominator_sum_x2 = 0

    for cat in categories:
        subset = df[df[ordered_group_col] == cat]
        n_i = len(subset)
        r_i = subset[outcome_col].sum()
        x_i = scores[cat]

        numerator += x_i * r_i
        denominator_sum_x += x_i * n_i
        denominator_sum_x2 += (x_i ** 2) * n_i

    numerator = numerator - (n_pos * denominator_sum_x / n)

    variance = (n_pos * n_neg / (n * (n - 1))) * (
        denominator_sum_x2 - (denominator_sum_x ** 2 / n)
    )

    z_score = numerator / np.sqrt(variance) if variance > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    return {
        'z_score': z_score,
        'p_value': p_value,
        'trend_direction': 'increasing' if z_score > 0 else 'decreasing',
        'significant': p_value < 0.05,
        'contingency_table': contingency
    }
