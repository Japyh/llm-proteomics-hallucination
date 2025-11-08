"""Generate synthetic proteomics data for testing."""

import numpy as np
import pandas as pd


class SyntheticDataGenerator:
    """Generate realistic synthetic protein data."""

    def __init__(self, seed: int = 42):
        """Initialize generator."""
        np.random.seed(seed)

    def generate_protein_dataset(self, n_proteins: int = 100) -> pd.DataFrame:
        """Generate synthetic protein dataset."""
        data = {
            "protein_id": [f"SYN{i:04d}" for i in range(n_proteins)],
            "molecular_weight": np.random.normal(50000, 20000, n_proteins),
            "expression_level": np.random.choice(
                ["low", "medium", "high"], n_proteins
            ),
        }
        return pd.DataFrame(data)
