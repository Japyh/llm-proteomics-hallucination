"""Test JSON schema validation."""
def test_schema_validation():
    """Test schema validation functions."""
    from src.data_processing.validators import DataValidator
    
    validator = DataValidator()
    
    # Simple test schema
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    data = {"name": "TP53"}
    
    assert validator.validate_json_schema(data, schema)
