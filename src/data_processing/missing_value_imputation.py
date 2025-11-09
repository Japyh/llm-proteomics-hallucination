"""Missing value imputation strategies."""
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer

class MissingValueImputer:
    """Handle missing values in datasets."""
    
    def impute_mean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute using mean values."""
        imputer = SimpleImputer(strategy='mean')
        return pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)
    
    def impute_median(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute using median values."""
        imputer = SimpleImputer(strategy='median')
        return pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)
    
    def impute_knn(self, df: pd.DataFrame, n_neighbors: int = 5) -> pd.DataFrame:
        """Impute using k-nearest neighbors."""
        imputer = KNNImputer(n_neighbors=n_neighbors)
        return pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)
    
    def impute_min(self, df: pd.DataFrame, fraction: float = 0.5) -> pd.DataFrame:
        """Impute with fraction of minimum (for proteomics LOD)."""
        mins = df.min()
        return df.fillna(mins * fraction)
