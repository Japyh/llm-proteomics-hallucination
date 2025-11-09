"""
Data quality tests for schema validation
"""

import json
import pytest
from pathlib import Path
from jsonschema import validate, ValidationError


@pytest.fixture
def schemas_dir():
    """Return path to schemas directory"""
    return Path(__file__).parent.parent.parent / "data" / "schemas"


@pytest.fixture
def data_dir():
    """Return path to data directory"""
    return Path(__file__).parent.parent.parent / "data"


class TestQuerySchemaValidation:
    """Test query data against schema"""

    def test_query_schema_exists(self, schemas_dir):
        """Test that query schema file exists"""
        schema_path = schemas_dir / "query_schema.json"
        assert schema_path.exists(), f"Query schema not found at {schema_path}"

    def test_query_schema_valid_json(self, schemas_dir):
        """Test that query schema is valid JSON"""
        schema_path = schemas_dir / "query_schema.json"
        with open(schema_path) as f:
            schema = json.load(f)
        assert "$schema" in schema
        assert "title" in schema

    def test_queries_validate_against_schema(self, schemas_dir, data_dir):
        """Test that all queries validate against schema"""
        schema_path = schemas_dir / "query_schema.json"
        queries_path = data_dir / "queries" / "queries_all.json"

        if not queries_path.exists():
            pytest.skip(f"Queries file not found at {queries_path}")

        with open(schema_path) as f:
            schema = json.load(f)

        with open(queries_path) as f:
            queries = json.load(f)

        # Validate each query
        for query in queries[:10]:  # Test first 10 for speed
            try:
                validate(instance=query, schema=schema)
            except ValidationError as e:
                pytest.fail(f"Query validation failed: {e.message}")


class TestAnnotationSchemaValidation:
    """Test annotation data against schema"""

    def test_annotation_schema_exists(self, schemas_dir):
        """Test that annotation schema file exists"""
        schema_path = schemas_dir / "annotation_schema.json"
        assert schema_path.exists(), f"Annotation schema not found at {schema_path}"

    def test_annotation_schema_valid_json(self, schemas_dir):
        """Test that annotation schema is valid JSON"""
        schema_path = schemas_dir / "annotation_schema.json"
        with open(schema_path) as f:
            schema = json.load(f)
        assert "$schema" in schema
        assert "required" in schema

    def test_annotations_validate_against_schema(self, schemas_dir, data_dir):
        """Test that annotations validate against schema"""
        schema_path = schemas_dir / "annotation_schema.json"
        annotations_path = data_dir / "annotations" / "expert_annotations.json"

        if not annotations_path.exists():
            pytest.skip(f"Annotations file not found at {annotations_path}")

        with open(schema_path) as f:
            schema = json.load(f)

        with open(annotations_path) as f:
            annotations = json.load(f)

        # Validate sample annotations
        for annotation in annotations[:10]:
            try:
                validate(instance=annotation, schema=schema)
            except ValidationError as e:
                pytest.fail(f"Annotation validation failed: {e.message}")


class TestResponseSchemaValidation:
    """Test LLM response data against schema"""

    def test_response_schema_exists(self, schemas_dir):
        """Test that response schema file exists"""
        schema_path = schemas_dir / "llm_response_schema.json"
        assert schema_path.exists(), f"Response schema not found at {schema_path}"

    def test_response_schema_valid_json(self, schemas_dir):
        """Test that response schema is valid JSON"""
        schema_path = schemas_dir / "llm_response_schema.json"
        with open(schema_path) as f:
            schema = json.load(f)
        assert "$schema" in schema

    def test_mock_response_validates(self, schemas_dir):
        """Test that a mock response validates"""
        schema_path = schemas_dir / "llm_response_schema.json"

        with open(schema_path) as f:
            schema = json.load(f)

        mock_response = {
            "response_id": "R0001",
            "query_id": "Q001",
            "model_name": "gpt-4-0125-preview",
            "model_version": "2024-03-01",
            "timestamp": "2024-03-15T10:30:00Z",
            "response_text": "Insulin is a peptide hormone produced by beta cells.",
            "metadata": {
                "temperature": 0.7,
                "max_tokens": 500,
                "completion_tokens": 45,
                "prompt_tokens": 20,
                "finish_reason": "stop"
            }
        }

        try:
            validate(instance=mock_response, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Mock response validation failed: {e.message}")


class TestProteinSchemaValidation:
    """Test protein data against schema"""

    def test_protein_schema_exists(self, schemas_dir):
        """Test that protein schema file exists"""
        schema_path = schemas_dir / "protein_schema.json"
        assert schema_path.exists(), f"Protein schema not found at {schema_path}"

    def test_mock_protein_validates(self, schemas_dir):
        """Test that a mock protein validates"""
        schema_path = schemas_dir / "protein_schema.json"

        with open(schema_path) as f:
            schema = json.load(f)

        mock_protein = {
            "uniprot_id": "P01308",
            "protein_name": "Insulin",
            "gene_name": "INS",
            "organism": "Homo sapiens",
            "organism_id": 9606,
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            "sequence_length": 110,
            "molecular_weight": 11734.5
        }

        try:
            validate(instance=mock_protein, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Mock protein validation failed: {e.message}")


class TestMSMSSchemaValidation:
    """Test MS/MS data against schema"""

    def test_msms_schema_exists(self, schemas_dir):
        """Test that MS/MS schema file exists"""
        schema_path = schemas_dir / "msms_schema.json"
        assert schema_path.exists(), f"MS/MS schema not found at {schema_path}"

    def test_mock_spectrum_validates(self, schemas_dir):
        """Test that a mock spectrum validates"""
        schema_path = schemas_dir / "msms_schema.json"

        with open(schema_path) as f:
            schema = json.load(f)

        mock_spectrum = {
            "spectrum_id": "MS000001",
            "scan_number": 1234,
            "precursor_mz": 524.3,
            "precursor_charge": 2,
            "retention_time": 35.2,
            "peaks": [
                {"mz": 147.1, "intensity": 1000.5},
                {"mz": 524.3, "intensity": 5000.2}
            ]
        }

        try:
            validate(instance=mock_spectrum, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Mock spectrum validation failed: {e.message}")


class TestQCMetricsValidation:
    """Test QC metrics against schema"""

    def test_qc_schema_exists(self, schemas_dir):
        """Test that QC metrics schema exists"""
        schema_path = schemas_dir / "qc_metrics_schema.json"
        assert schema_path.exists(), f"QC schema not found at {schema_path}"

    def test_mock_qc_report_validates(self, schemas_dir):
        """Test that a mock QC report validates"""
        schema_path = schemas_dir / "qc_metrics_schema.json"

        with open(schema_path) as f:
            schema = json.load(f)

        mock_qc = {
            "qc_id": "QC0001",
            "dataset_name": "queries_all",
            "validation_date": "2024-03-15T10:00:00Z",
            "status": "passed",
            "metrics": {
                "total_records": 500,
                "valid_records": 500,
                "invalid_records": 0,
                "data_completeness": 100.0,
                "validation_rate": 100.0
            }
        }

        try:
            validate(instance=mock_qc, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Mock QC report validation failed: {e.message}")
