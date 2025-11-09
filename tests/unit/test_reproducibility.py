"""Test reproducibility"""
import pytest
import numpy as np

def test_random_seed():
    """Test that random seed works consistently"""
    np.random.seed(42)
    sample1 = np.random.rand(10)
    
    np.random.seed(42)
    sample2 = np.random.rand(10)
    
    assert np.allclose(sample1, sample2)
