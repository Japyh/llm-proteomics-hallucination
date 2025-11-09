"""
Calibration analysis for LLM confidence scores.

This module provides tools for evaluating and improving the calibration
of LLM confidence scores relative to actual accuracy.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.calibration import calibration_curve
from sklearn.isotonic import IsotonicRegression
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt


class CalibrationAnalyzer:
    """Analyze and improve model calibration."""

    def __init__(self, n_bins: int = 10):
        self.n_bins = n_bins
        self.calibration_results = {}

    def compute_ece(
        self, y_true: np.ndarray, y_pred_proba: np.ndarray, n_bins: int = 10
    ) -> float:
        """
        Compute Expected Calibration Error (ECE).

        Args:
            y_true: Ground truth binary labels
            y_pred_proba: Predicted probabilities
            n_bins: Number of bins for calibration

        Returns:
            ECE score (lower is better)
        """
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]

        ece = 0.0
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            in_bin = (y_pred_proba > bin_lower) & (y_pred_proba <= bin_upper)
            prop_in_bin = in_bin.mean()

            if prop_in_bin > 0:
                accuracy_in_bin = y_true[in_bin].mean()
                avg_confidence_in_bin = y_pred_proba[in_bin].mean()
                ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

        return ece

    def compute_mce(
        self, y_true: np.ndarray, y_pred_proba: np.ndarray, n_bins: int = 10
    ) -> float:
        """
        Compute Maximum Calibration Error (MCE).

        Args:
            y_true: Ground truth binary labels
            y_pred_proba: Predicted probabilities
            n_bins: Number of bins

        Returns:
            MCE score (lower is better)
        """
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]

        mce = 0.0
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            in_bin = (y_pred_proba > bin_lower) & (y_pred_proba <= bin_upper)
            prop_in_bin = in_bin.mean()

            if prop_in_bin > 0:
                accuracy_in_bin = y_true[in_bin].mean()
                avg_confidence_in_bin = y_pred_proba[in_bin].mean()
                calibration_error = np.abs(avg_confidence_in_bin - accuracy_in_bin)
                mce = max(mce, calibration_error)

        return mce

    def temperature_scaling(
        self, logits: np.ndarray, y_true: np.ndarray, search_range: Tuple[float, float] = (0.1, 5.0)
    ) -> float:
        """
        Find optimal temperature for temperature scaling calibration.

        Args:
            logits: Model logits (pre-softmax)
            y_true: Ground truth labels
            search_range: Range of temperatures to search

        Returns:
            Optimal temperature value
        """
        from scipy.optimize import minimize_scalar

        def negative_log_likelihood(temperature):
            scaled_logits = logits / temperature
            probs = 1 / (1 + np.exp(-scaled_logits))
            eps = 1e-10
            probs = np.clip(probs, eps, 1 - eps)
            nll = -np.mean(y_true * np.log(probs) + (1 - y_true) * np.log(1 - probs))
            return nll

        result = minimize_scalar(negative_log_likelihood, bounds=search_range, method='bounded')
        return result.x

    def platt_scaling(self, y_pred_proba: np.ndarray, y_true: np.ndarray) -> Tuple[float, float]:
        """
        Perform Platt scaling (logistic regression calibration).

        Args:
            y_pred_proba: Uncalibrated probabilities
            y_true: Ground truth labels

        Returns:
            Tuple of (slope, intercept) for calibration
        """
        from sklearn.linear_model import LogisticRegression

        # Convert probabilities to logits
        eps = 1e-10
        y_pred_proba = np.clip(y_pred_proba, eps, 1 - eps)
        logits = np.log(y_pred_proba / (1 - y_pred_proba))

        lr = LogisticRegression(C=1e5, max_iter=1000)
        lr.fit(logits.reshape(-1, 1), y_true)

        return lr.coef_[0][0], lr.intercept_[0]

    def plot_calibration_curve(
        self,
        y_true: np.ndarray,
        y_pred_proba: np.ndarray,
        model_name: str = "Model",
        save_path: Optional[str] = None
    ):
        """
        Plot calibration curve (reliability diagram).

        Args:
            y_true: Ground truth labels
            y_pred_proba: Predicted probabilities
            model_name: Name for the model
            save_path: Path to save figure (optional)
        """
        prob_true, prob_pred = calibration_curve(y_true, y_pred_proba, n_bins=self.n_bins)

        fig, ax = plt.subplots(figsize=(8, 8))

        # Plot calibration curve
        ax.plot(prob_pred, prob_true, marker='o', linewidth=2, label=model_name)

        # Plot perfect calibration
        ax.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfect Calibration')

        # Compute and display ECE
        ece = self.compute_ece(y_true, y_pred_proba, self.n_bins)
        ax.text(0.05, 0.95, f'ECE: {ece:.4f}', transform=ax.transAxes,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat'))

        ax.set_xlabel('Mean Predicted Probability', fontsize=12)
        ax.set_ylabel('Fraction of Positives', fontsize=12)
        ax.set_title(f'Calibration Curve - {model_name}', fontsize=14)
        ax.legend(loc='lower right')
        ax.grid(alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    def evaluate_calibration(
        self, y_true: np.ndarray, y_pred_proba: np.ndarray, model_name: str = "Model"
    ) -> Dict:
        """
        Comprehensive calibration evaluation.

        Args:
            y_true: Ground truth labels
            y_pred_proba: Predicted probabilities
            model_name: Model identifier

        Returns:
            Dictionary with calibration metrics
        """
        ece = self.compute_ece(y_true, y_pred_proba, self.n_bins)
        mce = self.compute_mce(y_true, y_pred_proba, self.n_bins)

        # Brier score
        brier = np.mean((y_pred_proba - y_true) ** 2)

        # Calibration slope and intercept
        prob_true, prob_pred = calibration_curve(y_true, y_pred_proba, n_bins=self.n_bins)
        slope, intercept, r_value, p_value, std_err = stats.linregress(prob_pred, prob_true)

        results = {
            'model': model_name,
            'ece': ece,
            'mce': mce,
            'brier_score': brier,
            'calibration_slope': slope,
            'calibration_intercept': intercept,
            'r_squared': r_value ** 2
        }

        self.calibration_results[model_name] = results
        return results
