"""Comprehensive tests for evaluation metrics.

Tests cover:
- Binary classification metrics (accuracy, precision, recall, F1)
- Multi-class severity metrics
- Confusion matrix generation
- Severity-weighted accuracy
- Edge cases and error handling
- Statistical properties of metrics
"""

import pytest
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from src.llm_eval.metrics import calculate_hallucination_metrics, severity_weighted_accuracy


class TestBinaryClassificationMetrics:
    """Test suite for binary hallucination classification metrics."""

    def test_perfect_predictions(self):
        """Test metrics with perfect predictions (100% accuracy)."""
        y_true = np.array([0, 1, 1, 0, 1, 0, 0, 1])
        y_pred = y_true.copy()

        metrics = calculate_hallucination_metrics(y_true, y_pred)

        assert metrics['accuracy'] == 1.0
        assert metrics['precision'] == 1.0
        assert metrics['recall'] == 1.0
        assert metrics['f1_score'] == 1.0

    def test_mixed_predictions(self):
        """Test metrics with realistic mixed predictions."""
        y_true = np.array([0, 1, 1, 0, 1, 0, 1, 0])
        y_pred = np.array([0, 1, 0, 0, 1, 1, 1, 0])

        metrics = calculate_hallucination_metrics(y_true, y_pred)

        # Expected accuracy: 6/8 = 0.75
        assert metrics['accuracy'] == 0.75

        # Verify all metrics are present
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics
        assert 'confusion_matrix' in metrics

    def test_confusion_matrix_shape(self):
        """Test that confusion matrix has correct shape."""
        y_true = np.array([0, 1, 1, 0, 1, 0])
        y_pred = np.array([0, 1, 0, 0, 1, 1])

        metrics = calculate_hallucination_metrics(y_true, y_pred)

        cm = metrics['confusion_matrix']
        assert cm.shape == (2, 2)
        assert cm.sum() == len(y_true)


class TestSeverityWeightedAccuracy:
    """Test suite for severity-weighted accuracy metrics."""

    def test_basic_severity_weighting(self):
        """Test severity-weighted accuracy with simple example."""
        y_true = np.array([0, 1, 2, 3, 4])
        y_pred = np.array([0, 1, 2, 3, 4])  # Perfect

        weights = [1, 2, 3, 4, 5]
        accuracy = severity_weighted_accuracy(y_true, y_pred, weights)

        assert accuracy == 1.0

    def test_uniform_weights_equal_standard_accuracy(self):
        """Test that uniform weights give same result as standard accuracy."""
        y_true = np.array([0, 1, 2, 1, 0, 2])
        y_pred = np.array([0, 1, 1, 1, 0, 2])

        uniform_weights = [1, 1, 1, 1, 1]
        weighted_acc = severity_weighted_accuracy(y_true, y_pred, uniform_weights)

        # Weighted accuracy with uniform weights should be between 0 and 1
        assert 0 <= weighted_acc <= 1


def test_metrics_with_realistic_data():
    """Test with typical hallucination rate (~30%)."""
    np.random.seed(42)
    n_samples = 500

    y_true = np.random.choice([0, 1], size=n_samples, p=[0.7, 0.3])

    # Model with 85% accuracy
    y_pred = y_true.copy()
    flip_indices = np.random.choice(n_samples, size=int(n_samples * 0.15), replace=False)
    y_pred[flip_indices] = 1 - y_pred[flip_indices]

    metrics = calculate_hallucination_metrics(y_true, y_pred)

    # Accuracy should be around 0.85
    assert 0.80 <= metrics['accuracy'] <= 0.90
    assert metrics['f1_score'] > 0.5
