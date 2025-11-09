"""Test query data schema compliance."""
import pytest
import json

def test_query_schema():
    """Validate query JSON schema."""
    with open('data/queries/queries_test.json') as f:
        queries = json.load(f)
    
    required_fields = ['query_id', 'query_text', 'complexity']
    for query in queries:
        for field in required_fields:
            assert field in query, f"Missing {field}"
