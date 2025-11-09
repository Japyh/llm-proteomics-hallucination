"""Test LLM response format compliance."""
import pytest
import pandas as pd

def test_response_format():
    """Check response JSONL format."""
    df = pd.read_json('data/llm_responses/gpt4_turbo_responses.jsonl', lines=True)
    
    required_cols = ['query_id', 'model', 'response', 'timestamp']
    for col in required_cols:
        assert col in df.columns, f"Missing column: {col}"
