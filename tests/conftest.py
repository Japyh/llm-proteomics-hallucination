"""Pytest fixtures."""

import pytest


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
