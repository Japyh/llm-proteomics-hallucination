"""Test reproducibility with fixed seeds."""
from src.utils.seeds import set_seed
import numpy as np

def test_seed_reproducibility():
    """Verify random seed works."""
    set_seed(42)
    arr1 = np.random.rand(10)
    
    set_seed(42)
    arr2 = np.random.rand(10)
    
    assert np.allclose(arr1, arr2), "Seeds not reproducing same values"
