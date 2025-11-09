"""Quality control for proteomics and LLM data."""
import pandas as pd
import numpy as np

class QualityControl:
    """Perform QC checks on experimental data."""
    
    def check_fdr(self, df: pd.DataFrame, fdr_column: str = 'fdr', threshold: float = 0.01) -> pd.DataFrame:
        """Filter by false discovery rate."""
        return df[df[fdr_column] <= threshold]
    
    def check_outliers(self, values: np.ndarray, method: str = 'iqr') -> np.ndarray:
        """Detect outliers using IQR method."""
        Q1 = np.percentile(values, 25)
        Q3 = np.percentile(values, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (values >= lower_bound) & (values <= upper_bound)
    
    def calculate_qc_metrics(self, df: pd.DataFrame) -> dict:
        """Calculate comprehensive QC metrics."""
        return {
            'n_samples': len(df),
            'missing_rate': df.isnull().mean().mean(),
            'duplicate_rate': df.duplicated().mean(),
            'outlier_rate': (~self.check_outliers(df.select_dtypes(include=[np.number]).values.flatten())).mean()
        }
