"""Evaluation metrics."""

from typing import List


class Metrics:
    """Calculate evaluation metrics."""

    @staticmethod
    def hallucination_rate(predictions: List[bool]) -> float:
        """Calculate hallucination rate."""
        return sum(predictions) / len(predictions) if predictions else 0.0

    @staticmethod
    def accuracy(y_true: List, y_pred: List) -> float:
        """Calculate accuracy."""
        correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        return correct / len(y_true) if y_true else 0.0
