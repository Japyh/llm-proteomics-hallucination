"""Test data transformations."""
from src.data_processing.transforms import normalize_scores
import numpy as np

def test_normalization():
    """Test score normalization."""
    scores = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    normalized = normalize_scores(scores, method='minmax')
    
    assert normalized.min() == 0.0
    assert normalized.max() == 1.0
