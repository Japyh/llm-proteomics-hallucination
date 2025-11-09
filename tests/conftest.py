"""Pytest fixtures and configuration for LLM Proteomics Hallucination Study tests."""

import pytest
from pathlib import Path


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "requires_api: marks tests that require API access"
    )
    config.addinivalue_line(
        "markers", "requires_docker: marks tests that require Docker"
    )


@pytest.fixture
def project_root():
    """Return path to project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture
def data_dir(project_root):
    """Return path to data directory"""
    return project_root / "data"


@pytest.fixture
def schemas_dir(data_dir):
    """Return path to schemas directory"""
    return data_dir / "schemas"


@pytest.fixture
def mock_llm_response():
    """Mock LLM response."""
    return "Hemoglobin is an oxygen-transport protein."


@pytest.fixture
def sample_protein_data():
    """Sample protein data for testing."""
    return {
        "protein_id": "P12345",
        "name": "Test Protein",
        "molecular_weight": 50000,
    }


@pytest.fixture
def sample_query():
    """Sample query for testing"""
    return {
        "query_id": "Q001",
        "query_text": "What is the function of insulin?",
        "domain": "protein_identification",
        "complexity": "low",
        "prevalence": "common"
    }


@pytest.fixture
def sample_annotation():
    """Sample annotation for testing"""
    return {
        "annotation_id": "A0001",
        "query_id": "Q001",
        "response_id": "R0001",
        "rater_id": "RATER1",
        "timestamp": "2024-03-15T10:00:00Z",
        "is_hallucination": False,
        "hallucination_type": None,
        "severity": None,
        "confidence": 5
    }


@pytest.fixture
def sample_llm_response_data():
    """Sample LLM response data for testing"""
    return {
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
