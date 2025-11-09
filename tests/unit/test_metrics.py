"""Unit tests for metrics"""
import pytest
import numpy as np
from src.llm_eval.metrics import calculate_metrics

def test_calculate_metrics():
    """Test metrics calculation"""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 1, 1])
    
    metrics = calculate_metrics(y_true, y_pred)
    
    assert 'accuracy' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert metrics['accuracy'] == 0.75
