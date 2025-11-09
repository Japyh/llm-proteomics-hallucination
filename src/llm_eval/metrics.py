"""Evaluation metrics for LLM hallucination detection."""
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

def calculate_hallucination_metrics(y_true, y_pred):
    """Calculate comprehensive hallucination detection metrics."""
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
    cm = confusion_matrix(y_true, y_pred)
    
    return {
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm
    }

def severity_weighted_accuracy(y_true, y_pred, severity_weights=[1, 2, 3, 4]):
    """Calculate accuracy weighted by hallucination severity."""
    weights = np.array([severity_weights[int(y)] for y in y_true])
    correct = (y_true == y_pred).astype(float)
    return np.average(correct, weights=weights)
