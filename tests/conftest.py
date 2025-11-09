"""Pytest configuration and shared fixtures for LLM proteomics hallucination tests.

This module provides common fixtures, test data, and configuration for the test suite.
Fixtures are shared across unit, integration, and data quality tests.
"""

import sys
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Any

import pytest
import numpy as np
import pandas as pd


# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# ============================================================================
# Test Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "data_quality: marks tests as data quality tests"
    )
    config.addinivalue_line(
        "markers", "requires_api: marks tests that require API credentials"
    )


# ============================================================================
# Random Seed Control
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def set_random_seeds():
    """Set random seeds for reproducibility across all tests."""
    np.random.seed(42)
    import random
    random.seed(42)

    # Set torch seed if available
    try:
        import torch
        torch.manual_seed(42)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(42)
    except ImportError:
        pass


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_query():
    """Provide a sample proteomics query."""
    return {
        "query_id": "Q001",
        "query_text": "What is the molecular weight of TP53 protein?",
        "complexity": "simple",
        "prevalence": "common",
        "query_type": "protein_identification",
        "ground_truth": "TP53 has a molecular weight of approximately 53 kDa"
    }


@pytest.fixture
def sample_queries():
    """Provide multiple sample queries for batch testing."""
    return [
        {
            "query_id": f"Q{i:03d}",
            "query_text": f"Sample query {i}",
            "complexity": ["simple", "intermediate", "complex"][i % 3],
            "prevalence": ["common", "moderate", "rare"][i % 3],
            "query_type": "protein_identification",
            "ground_truth": f"Ground truth for query {i}"
        }
        for i in range(1, 11)
    ]


@pytest.fixture
def sample_llm_response():
    """Provide a sample LLM response."""
    return {
        "query_id": "Q001",
        "model": "gpt-4-turbo",
        "response_text": "TP53 protein has a molecular weight of 53 kDa.",
        "tokens_used": 15,
        "timestamp": "2025-11-15T10:30:00Z",
        "confidence": 0.95
    }


@pytest.fixture
def sample_annotation():
    """Provide a sample expert annotation."""
    return {
        "query_id": "Q001",
        "annotator_id": "EXP001",
        "is_hallucination": False,
        "severity": 0,
        "error_type": None,
        "confidence": 5,
        "notes": "Factually accurate"
    }


@pytest.fixture
def sample_protein_data():
    """Provide sample protein metadata."""
    return {
        "uniprot_id": "P04637",
        "gene_name": "TP53",
        "protein_name": "Cellular tumor antigen p53",
        "organism": "Homo sapiens",
        "sequence_length": 393,
        "molecular_weight": 43653.0,  # Daltons
        "function": "Tumor suppressor",
        "subcellular_location": "Nucleus",
        "expression_level": "high"
    }


# ============================================================================
# Data Quality Fixtures
# ============================================================================

@pytest.fixture
def mock_queries_dataset(tmp_path):
    """Create a mock queries dataset file."""
    queries = [
        {
            "query_id": f"Q{i:03d}",
            "query_text": f"Test query {i}",
            "complexity": ["simple", "intermediate", "complex"][i % 3],
            "prevalence": ["common", "moderate", "rare"][i % 3],
            "query_type": ["protein_identification", "quantitative_expression",
                          "ptm", "interactions", "clinical"][i % 5]
        }
        for i in range(1, 21)
    ]

    filepath = tmp_path / "mock_queries.json"
    with open(filepath, "w") as f:
        json.dump(queries, f, indent=2)

    return filepath


@pytest.fixture
def mock_responses_dataset(tmp_path):
    """Create a mock LLM responses dataset file."""
    responses = []
    for i in range(1, 21):
        for model in ["gpt-4-turbo", "claude-3-sonnet", "gemini-1.5-pro"]:
            responses.append({
                "query_id": f"Q{i:03d}",
                "model": model,
                "response_text": f"Response from {model} to query {i}",
                "tokens_used": np.random.randint(10, 100),
                "timestamp": f"2025-11-{15 + (i-1)//10:02d}T10:30:00Z"
            })

    filepath = tmp_path / "mock_responses.jsonl"
    with open(filepath, "w") as f:
        for resp in responses:
            f.write(json.dumps(resp) + "\n")

    return filepath


@pytest.fixture
def mock_annotations_dataset(tmp_path):
    """Create a mock annotations dataset file."""
    annotations = []
    for i in range(1, 21):
        annotations.append({
            "query_id": f"Q{i:03d}",
            "annotator_id": "EXP001",
            "is_hallucination": bool(i % 3 == 0),  # Every 3rd query is hallucination
            "severity": (i % 5),  # 0-4 severity
            "confidence": np.random.randint(3, 6),
            "notes": f"Annotation for query {i}"
        })

    filepath = tmp_path / "mock_annotations.json"
    with open(filepath, "w") as f:
        json.dump(annotations, f, indent=2)

    return filepath


# ============================================================================
# Statistical Test Fixtures
# ============================================================================

@pytest.fixture
def binary_classification_data():
    """Provide binary classification test data."""
    np.random.seed(42)
    n_samples = 100

    # Generate ground truth (30% hallucinations)
    y_true = np.random.choice([0, 1], size=n_samples, p=[0.7, 0.3])

    # Generate predictions (85% accuracy)
    y_pred = y_true.copy()
    flip_indices = np.random.choice(n_samples, size=int(n_samples * 0.15), replace=False)
    y_pred[flip_indices] = 1 - y_pred[flip_indices]

    return {"y_true": y_true, "y_pred": y_pred}


@pytest.fixture
def multiclass_severity_data():
    """Provide multiclass severity classification test data."""
    np.random.seed(42)
    n_samples = 100

    # Generate severity scores (0-4)
    y_true = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.5, 0.2, 0.15, 0.1, 0.05])

    # Generate predictions with some error
    y_pred = y_true + np.random.randint(-1, 2, size=n_samples)
    y_pred = np.clip(y_pred, 0, 4)

    return {"y_true": y_true, "y_pred": y_pred}


# ============================================================================
# API Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {
        "choices": [{
            "message": {
                "content": "TP53 is a tumor suppressor protein with molecular weight 53 kDa."
            }
        }],
        "usage": {
            "total_tokens": 20,
            "prompt_tokens": 10,
            "completion_tokens": 10
        },
        "model": "gpt-4-turbo-2024-04-09"
    }


@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response."""
    return {
        "content": [{
            "text": "TP53 is a tumor suppressor protein with molecular weight 53 kDa."
        }],
        "usage": {
            "input_tokens": 10,
            "output_tokens": 10
        },
        "model": "claude-3-sonnet-20240229"
    }


# ============================================================================
# Database Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_uniprot_data():
    """Mock UniProt database query results."""
    return {
        "P04637": {
            "entry_name": "P53_HUMAN",
            "protein_names": "Cellular tumor antigen p53",
            "gene_names": "TP53 P53",
            "organism": "Homo sapiens (Human)",
            "sequence_length": 393,
            "sequence": "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIE...",
            "function": ["Acts as a tumor suppressor in many tumor types"],
            "subcellular_location": ["Nucleus", "Cytoplasm"],
            "ptms": ["Phosphorylation", "Acetylation", "Ubiquitination"]
        }
    }


# ============================================================================
# Temporary Directory Fixtures
# ============================================================================

@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory with subdirectories."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    (data_dir / "queries").mkdir()
    (data_dir / "ground_truth").mkdir()
    (data_dir / "llm_responses").mkdir()
    (data_dir / "results").mkdir()

    return data_dir


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary configuration file."""
    config = {
        "models": {
            "gpt4": {"temperature": 0.3, "max_tokens": 2048},
            "claude": {"temperature": 0.3, "max_tokens": 2048},
            "gemini": {"temperature": 0.3, "max_tokens": 2048}
        },
        "evaluation": {
            "seed": 42,
            "batch_size": 10,
            "timeout": 30
        }
    }

    config_file = tmp_path / "test_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    return config_file


# ============================================================================
# Performance Benchmarking Fixtures
# ============================================================================

@pytest.fixture
def benchmark_queries():
    """Provide queries for performance benchmarking."""
    return [
        {"query_id": f"BENCH{i:04d}", "query_text": f"Benchmark query {i}"}
        for i in range(1, 101)
    ]


# ============================================================================
# Cleanup and Teardown
# ============================================================================

@pytest.fixture(scope="function", autouse=True)
def reset_global_state():
    """Reset global state before each test."""
    yield
    # Cleanup code here if needed


# ============================================================================
# Custom Assertions
# ============================================================================

def assert_valid_query(query: Dict[str, Any]):
    """Assert that a query has valid structure."""
    required_fields = ["query_id", "query_text", "complexity", "prevalence", "query_type"]
    for field in required_fields:
        assert field in query, f"Missing required field: {field}"

    assert query["complexity"] in ["simple", "intermediate", "complex"]
    assert query["prevalence"] in ["common", "moderate", "rare"]
    assert query["query_type"] in [
        "protein_identification", "quantitative_expression", "ptm",
        "interactions", "clinical"
    ]


def assert_valid_response(response: Dict[str, Any]):
    """Assert that an LLM response has valid structure."""
    required_fields = ["query_id", "model", "response_text"]
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"

    assert len(response["response_text"]) > 0, "Response text cannot be empty"


def assert_valid_annotation(annotation: Dict[str, Any]):
    """Assert that an annotation has valid structure."""
    required_fields = ["query_id", "is_hallucination", "severity", "confidence"]
    for field in required_fields:
        assert field in annotation, f"Missing required field: {field}"

    assert isinstance(annotation["is_hallucination"], bool)
    assert 0 <= annotation["severity"] <= 4
    assert 1 <= annotation["confidence"] <= 5
