"""Test results data contracts."""
def test_results_schema():
    """Verify results files have required fields."""
    import pandas as pd
    df = pd.read_csv('data/results/hallucination_rates.csv')
    assert 'model' in df.columns
    assert 'hallucination_rate' in df.columns
