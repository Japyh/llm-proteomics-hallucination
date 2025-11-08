"""Statistical testing functions."""

import numpy as np
from scipy import stats
from typing import Tuple


class StatisticalTests:
    """Collection of statistical test methods."""

    @staticmethod
    def cohens_kappa(ratings1: list, ratings2: list) -> float:
        """Calculate Cohen's kappa."""
        from sklearn.metrics import cohen_kappa_score

        return cohen_kappa_score(ratings1, ratings2)

    @staticmethod
    def mcnemar_test(contingency_table: np.ndarray) -> Tuple[float, float]:
        """Perform McNemar's test."""
        return stats.mcnemar(contingency_table)
