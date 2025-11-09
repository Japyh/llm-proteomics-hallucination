"""Evaluation metrics for LLM hallucination detection.

This module provides comprehensive metrics for evaluating hallucination detection
in LLM responses to proteomics queries, including:
- Binary classification metrics (accuracy, precision, recall, F1)
- Multi-class severity metrics
- Calibration metrics
- Confusion matrices
- Per-class performance metrics
- Statistical significance tests
"""

import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Union, Any
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    cohen_kappa_score,
    matthews_corrcoef,
    classification_report
)
from scipy import stats


logger = logging.getLogger(__name__)


def calculate_hallucination_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Calculate comprehensive hallucination detection metrics.

    Args:
        y_true: Ground truth binary labels (0=no hallucination, 1=hallucination)
        y_pred: Predicted binary labels
        y_prob: Predicted probabilities (optional, for AUC metrics)
        labels: Class labels for reporting (optional)

    Returns:
        Dictionary containing all evaluation metrics

    Raises:
        ValueError: If input arrays have mismatched shapes
    """
    if len(y_true) != len(y_pred):
        raise ValueError(f"Shape mismatch: y_true {len(y_true)} vs y_pred {len(y_pred)}")

    # Basic classification metrics
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average='weighted', zero_division=0
    )

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Cohen's kappa (inter-rater agreement)
    kappa = cohen_kappa_score(y_true, y_pred)

    # Matthews correlation coefficient
    mcc = matthews_corrcoef(y_true, y_pred)

    metrics = {
        'accuracy': float(acc),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'confusion_matrix': cm,
        'cohen_kappa': float(kappa),
        'mcc': float(mcc),
        'n_samples': len(y_true),
    }

    # Add per-class metrics
    precision_per_class, recall_per_class, f1_per_class, support_per_class = \
        precision_recall_fscore_support(y_true, y_pred, average=None, zero_division=0)

    metrics['precision_per_class'] = precision_per_class.tolist()
    metrics['recall_per_class'] = recall_per_class.tolist()
    metrics['f1_per_class'] = f1_per_class.tolist()
    metrics['support_per_class'] = support_per_class.tolist()

    # Add probability-based metrics if available
    if y_prob is not None:
        try:
            if y_prob.ndim == 1:
                # Binary classification with single probability
                auc_roc = roc_auc_score(y_true, y_prob)
                avg_precision = average_precision_score(y_true, y_prob)
            else:
                # Multi-class with probability matrix
                auc_roc = roc_auc_score(y_true, y_prob, multi_class='ovr', average='weighted')
                avg_precision = average_precision_score(y_true, y_prob[:, 1] if y_prob.shape[1] == 2 else y_prob)

            metrics['auc_roc'] = float(auc_roc)
            metrics['avg_precision'] = float(avg_precision)
        except Exception as e:
            logger.warning(f"Could not calculate probability-based metrics: {e}")

    # Add classification report as string
    if labels is not None:
        report = classification_report(y_true, y_pred, target_names=labels)
        metrics['classification_report'] = report

    logger.info(f"Calculated metrics: accuracy={acc:.3f}, precision={precision:.3f}, recall={recall:.3f}, f1={f1:.3f}")

    return metrics


def severity_weighted_accuracy(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    severity_weights: Optional[List[float]] = None
) -> float:
    """
    Calculate accuracy weighted by hallucination severity.

    Assigns higher weight to more severe errors, making the metric
    more sensitive to critical hallucinations.

    Args:
        y_true: Ground truth severity labels (0-4)
        y_pred: Predicted severity labels (0-4)
        severity_weights: Weight for each severity level (default: [1,2,3,4,5])

    Returns:
        Weighted accuracy score (0-1)

    Raises:
        ValueError: If arrays have different lengths
    """
    if len(y_true) != len(y_pred):
        raise ValueError(f"Shape mismatch: y_true {len(y_true)} vs y_pred {len(y_pred)}")

    if severity_weights is None:
        severity_weights = [1, 2, 3, 4, 5]

    # Map severity levels to weights
    weights = np.array([severity_weights[int(y)] for y in y_true])

    # Calculate weighted accuracy
    correct = (y_true == y_pred).astype(float)
    weighted_acc = np.average(correct, weights=weights)

    return float(weighted_acc)


def calculate_calibration_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10
) -> Dict[str, Any]:
    """
    Calculate calibration metrics for probability predictions.

    Args:
        y_true: Ground truth binary labels
        y_prob: Predicted probabilities
        n_bins: Number of bins for calibration curve

    Returns:
        Dictionary with calibration metrics
    """
    from sklearn.calibration import calibration_curve

    # Calculate calibration curve
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy='uniform')

    # Expected Calibration Error (ECE)
    bin_counts = np.histogram(y_prob, bins=n_bins, range=(0, 1))[0]
    bin_indices = np.digitize(y_prob, bins=np.linspace(0, 1, n_bins + 1)[:-1]) - 1
    bin_indices = np.clip(bin_indices, 0, n_bins - 1)

    ece = 0.0
    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            bin_acc = y_true[mask].mean()
            bin_conf = y_prob[mask].mean()
            bin_weight = mask.sum() / len(y_true)
            ece += bin_weight * abs(bin_acc - bin_conf)

    # Brier score
    brier_score = np.mean((y_prob - y_true) ** 2)

    return {
        'expected_calibration_error': float(ece),
        'brier_score': float(brier_score),
        'calibration_curve_true': prob_true.tolist(),
        'calibration_curve_pred': prob_pred.tolist(),
    }


def calculate_confidence_interval(
    metric_values: np.ndarray,
    confidence: float = 0.95
) -> Tuple[float, float, float]:
    """
    Calculate confidence interval for a metric using bootstrap.

    Args:
        metric_values: Array of metric values from bootstrap samples
        confidence: Confidence level (default: 0.95)

    Returns:
        Tuple of (mean, lower_bound, upper_bound)
    """
    mean = np.mean(metric_values)
    alpha = 1 - confidence
    lower = np.percentile(metric_values, 100 * alpha / 2)
    upper = np.percentile(metric_values, 100 * (1 - alpha / 2))

    return float(mean), float(lower), float(upper)


def compare_models(
    y_true: np.ndarray,
    predictions_dict: Dict[str, np.ndarray],
    metric: str = 'accuracy'
) -> Dict[str, Any]:
    """
    Compare multiple models using specified metric.

    Args:
        y_true: Ground truth labels
        predictions_dict: Dictionary mapping model names to predictions
        metric: Metric to use for comparison

    Returns:
        Dictionary with comparison results
    """
    results = {}

    for model_name, y_pred in predictions_dict.items():
        if metric == 'accuracy':
            score = accuracy_score(y_true, y_pred)
        elif metric == 'f1':
            _, _, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
            score = f1
        else:
            raise ValueError(f"Unsupported metric: {metric}")

        results[model_name] = float(score)

    # Rank models
    ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return {
        'scores': results,
        'ranked': ranked,
        'best_model': ranked[0][0] if ranked else None,
        'best_score': ranked[0][1] if ranked else None
    }


def mcnemar_test(
    y_true: np.ndarray,
    y_pred1: np.ndarray,
    y_pred2: np.ndarray
) -> Dict[str, float]:
    """
    Perform McNemar's test to compare two models.

    Args:
        y_true: Ground truth labels
        y_pred1: Predictions from model 1
        y_pred2: Predictions from model 2

    Returns:
        Dictionary with test statistic and p-value
    """
    # Create contingency table
    correct1 = (y_pred1 == y_true)
    correct2 = (y_pred2 == y_true)

    # Count disagreements
    n01 = np.sum(~correct1 & correct2)  # Model 1 wrong, Model 2 correct
    n10 = np.sum(correct1 & ~correct2)  # Model 1 correct, Model 2 wrong

    # McNemar's test
    if n01 + n10 == 0:
        return {'statistic': 0.0, 'p_value': 1.0}

    statistic = (abs(n01 - n10) - 1) ** 2 / (n01 + n10)
    p_value = 1 - stats.chi2.cdf(statistic, df=1)

    return {
        'statistic': float(statistic),
        'p_value': float(p_value),
        'n01': int(n01),
        'n10': int(n10)
    }
