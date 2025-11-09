"""Confidence calibration for LLM predictions."""
import numpy as np
from sklearn.calibration import calibration_curve

def compute_ece(y_true, y_pred_proba, n_bins=10):
    """Compute Expected Calibration Error."""
    prob_true, prob_pred = calibration_curve(y_true, y_pred_proba, n_bins=n_bins, strategy='uniform')
    
    bin_edges = np.linspace(0, 1, n_bins+1)
    ece = 0
    for i in range(n_bins):
        mask = (y_pred_proba >= bin_edges[i]) & (y_pred_proba < bin_edges[i+1])
        if mask.sum() > 0:
            acc = y_true[mask].mean()
            conf = y_pred_proba[mask].mean()
            ece += abs(acc - conf) * mask.mean()
    return ece

def temperature_scaling(logits, temperature):
    """Apply temperature scaling for calibration."""
    return logits / temperature
