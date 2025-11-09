"""Test evaluation metrics."""
from src.llm_eval.metrics import calculate_hallucination_metrics
import numpy as np

def test_hallucination_metrics():
    """Test metric calculation."""
    y_true = np.array([0, 1, 1, 0, 1])
    y_pred = np.array([0, 1, 0, 0, 1])
    
    metrics = calculate_hallucination_metrics(y_true, y_pred)
    
    assert 'accuracy' in metrics
    assert 'f1_score' in metrics
