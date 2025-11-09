"""Test calibration methods."""
import numpy as np
from src.analysis.calibration import CalibrationAnalyzer

def test_ece_calculation():
    """Test Expected Calibration Error."""
    y_true = np.array([1, 1, 0, 0, 1])
    y_pred = np.array([0.9, 0.8, 0.3, 0.2, 0.7])
    
    analyzer = CalibrationAnalyzer()
    ece = analyzer.compute_ece(y_true, y_pred, n_bins=5)
    
    assert 0 <= ece <= 1, "ECE should be in [0, 1]"
