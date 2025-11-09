"""Data transformation utilities."""
import pandas as pd
import numpy as np

def normalize_scores(scores: np.ndarray, method: str = 'minmax') -> np.ndarray:
    """Normalize scores to [0, 1] range."""
    if method == 'minmax':
        return (scores - scores.min()) / (scores.max() - scores.min())
    elif method == 'zscore':
        return (scores - scores.mean()) / scores.std()
    return scores

def encode_categorical(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """One-hot encode categorical variables."""
    return pd.get_dummies(df, columns=columns, drop_first=True)

def bin_continuous(values: np.ndarray, n_bins: int = 10) -> np.ndarray:
    """Bin continuous values into discrete categories."""
    return pd.cut(values, bins=n_bins, labels=False)
