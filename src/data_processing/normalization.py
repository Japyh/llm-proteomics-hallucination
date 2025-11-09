"""Normalization methods for proteomics data."""
import numpy as np
import pandas as pd

def quantile_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Quantile normalization across samples."""
    rank_mean = df.stack().groupby(df.rank(method='first').stack().astype(int)).mean()
    return df.rank(method='min').stack().astype(int).map(rank_mean).unstack()

def median_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Median normalization."""
    medians = df.median()
    global_median = medians.median()
    scaling_factors = global_median / medians
    return df * scaling_factors

def log_transform(df: pd.DataFrame, base: float = 2.0, offset: float = 1.0) -> pd.DataFrame:
    """Log transformation with pseudocount."""
    return np.log(df + offset) / np.log(base)
