"""End-to-end integration tests for complete evaluation pipeline.

Tests cover:
- Full data pipeline (query → response → annotation → analysis)
- Data loader integration
- LLM client mock integration
- Metrics calculation pipeline
- Export functionality
- Error handling and edge cases
"""

import pytest
import json
import tempfile
from pathlib import Path
import pandas as pd
import numpy as np

from src.data_processing.loaders import DataLoader
from src.llm_eval.metrics import calculate_hallucination_metrics, severity_weighted_accuracy
from src.utils.io import ensure_directory, write_json, read_json


class TestEndToEndPipeline:
    """Integration tests for complete evaluation pipeline."""

    def test_full_pipeline_query_to_results(self, tmp_path):
        """Test complete pipeline from queries to final results."""
        # Step 1: Create mock query data
        queries_file = tmp_path / "queries.json"
        queries = [
            {
                "query_id": f"Q{i:03d}",
                "query_text": f"What is protein {i}?",
                "complexity": ["simple", "intermediate", "complex"][i % 3],
                "prevalence": ["common", "moderate", "rare"][i % 3],
                "query_type": "protein_identification"
            }
            for i in range(1, 21)
        ]

        with open(queries_file, "w") as f:
            json.dump(queries, f)

        # Step 2: Load queries using DataLoader
        loader = DataLoader()
        loaded_queries = loader.load_queries(queries_file)
        assert len(loaded_queries) == 20
        assert loaded_queries[0]["query_id"] == "Q001"

        # Step 3: Mock LLM responses
        responses_file = tmp_path / "responses.jsonl"
        responses = []
        for query in loaded_queries:
            responses.append({
                "query_id": query["query_id"],
                "model": "gpt-4-turbo",
                "response_text": f"Mock response for {query['query_id']}",
                "tokens_used": np.random.randint(10, 100),
                "timestamp": "2025-11-15T10:30:00Z"
            })

        with open(responses_file, "w") as f:
            for resp in responses:
                f.write(json.dumps(resp) + "\n")

        # Step 4: Load responses
        loaded_responses = loader.load_responses(responses_file)
        assert len(loaded_responses) == 20
        assert "query_id" in loaded_responses.columns

        # Step 5: Mock annotations
        np.random.seed(42)
        y_true = np.random.choice([0, 1], size=20, p=[0.7, 0.3])
        y_pred = y_true.copy()

        # Introduce some errors
        error_indices = np.random.choice(20, size=3, replace=False)
        y_pred[error_indices] = 1 - y_pred[error_indices]

        # Step 6: Calculate metrics
        metrics = calculate_hallucination_metrics(y_true, y_pred)

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics
        assert 0 <= metrics["accuracy"] <= 1

        # Step 7: Export results
        results_file = tmp_path / "results.json"
        write_json(results_file, metrics)

        # Verify export
        loaded_results = read_json(results_file)
        assert loaded_results["accuracy"] == metrics["accuracy"]

    def test_pipeline_with_multiple_models(self, tmp_path):
        """Test pipeline with multiple LLM models."""
        queries_file = tmp_path / "queries.json"
        queries = [
            {"query_id": f"Q{i:03d}", "query_text": f"Query {i}"}
            for i in range(1, 11)
        ]

        with open(queries_file, "w") as f:
            json.dump(queries, f)

        models = ["gpt-4-turbo", "claude-3-sonnet", "gemini-1.5-pro"]
        all_metrics = {}

        for model in models:
            # Mock responses
            responses_file = tmp_path / f"{model}_responses.jsonl"
            with open(responses_file, "w") as f:
                for query in queries:
                    f.write(json.dumps({
                        "query_id": query["query_id"],
                        "model": model,
                        "response_text": f"{model} response"
                    }) + "\n")

            # Mock evaluation
            np.random.seed(hash(model) % 2**32)
            y_true = np.random.choice([0, 1], size=10, p=[0.7, 0.3])
            y_pred = y_true.copy()

            # Each model has different error rate
            error_count = {"gpt-4-turbo": 1, "claude-3-sonnet": 2, "gemini-1.5-pro": 1}[model]
            error_indices = np.random.choice(10, size=error_count, replace=False)
            y_pred[error_indices] = 1 - y_pred[error_indices]

            metrics = calculate_hallucination_metrics(y_true, y_pred)
            all_metrics[model] = metrics

        # Verify all models were evaluated
        assert len(all_metrics) == 3
        for model in models:
            assert model in all_metrics
            assert "accuracy" in all_metrics[model]

    def test_severity_weighted_evaluation(self, tmp_path):
        """Test severity-weighted accuracy calculation in pipeline."""
        # Mock severity annotations
        np.random.seed(42)
        n_samples = 50

        y_true = np.random.choice([0, 1, 2, 3, 4], size=n_samples,
                                   p=[0.5, 0.2, 0.15, 0.1, 0.05])
        y_pred = y_true + np.random.randint(-1, 2, size=n_samples)
        y_pred = np.clip(y_pred, 0, 4)

        # Calculate severity-weighted accuracy
        weights = [1, 2, 3, 4, 5]
        weighted_acc = severity_weighted_accuracy(y_true, y_pred, weights)

        assert 0 <= weighted_acc <= 1
        assert isinstance(weighted_acc, (float, np.floating))

    def test_error_handling_in_pipeline(self, tmp_path):
        """Test pipeline error handling with malformed data."""
        # Test with missing file
        loader = DataLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_queries(tmp_path / "nonexistent.json")

        # Test with empty file
        empty_file = tmp_path / "empty.json"
        with open(empty_file, "w") as f:
            f.write("")

        with pytest.raises(json.JSONDecodeError):
            loader.load_queries(empty_file)

        # Test with invalid JSON
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, "w") as f:
            f.write("{invalid json")

        with pytest.raises(json.JSONDecodeError):
            loader.load_queries(invalid_file)

    def test_data_consistency_across_pipeline(self, tmp_path):
        """Test data consistency through all pipeline stages."""
        # Create consistent dataset
        query_ids = [f"Q{i:03d}" for i in range(1, 16)]

        # Stage 1: Queries
        queries_file = tmp_path / "queries.json"
        queries = [{"query_id": qid, "query_text": f"Query {qid}"} for qid in query_ids]
        with open(queries_file, "w") as f:
            json.dump(queries, f)

        # Stage 2: Responses (must match query IDs)
        responses_file = tmp_path / "responses.jsonl"
        with open(responses_file, "w") as f:
            for qid in query_ids:
                f.write(json.dumps({
                    "query_id": qid,
                    "response_text": f"Response for {qid}"
                }) + "\n")

        # Stage 3: Verify consistency
        loader = DataLoader()
        loaded_queries = loader.load_queries(queries_file)
        loaded_responses = loader.load_responses(responses_file)

        query_ids_from_queries = {q["query_id"] for q in loaded_queries}
        query_ids_from_responses = set(loaded_responses["query_id"].values)

        assert query_ids_from_queries == query_ids_from_responses
        assert len(query_ids_from_queries) == 15

    def test_batch_processing_pipeline(self, tmp_path):
        """Test pipeline with batch processing."""
        batch_size = 5
        total_queries = 25

        queries_file = tmp_path / "queries.json"
        queries = [
            {"query_id": f"Q{i:03d}", "query_text": f"Query {i}"}
            for i in range(1, total_queries + 1)
        ]
        with open(queries_file, "w") as f:
            json.dump(queries, f)

        loader = DataLoader()
        all_queries = loader.load_queries(queries_file)

        # Process in batches
        batches = [all_queries[i:i+batch_size] for i in range(0, len(all_queries), batch_size)]

        assert len(batches) == 5
        assert len(batches[0]) == 5
        assert len(batches[-1]) == 5

        # Verify all queries processed
        total_processed = sum(len(batch) for batch in batches)
        assert total_processed == total_queries


def test_metrics_integration_with_real_data(binary_classification_data):
    """Test metrics calculation with realistic binary classification data."""
    y_true = binary_classification_data["y_true"]
    y_pred = binary_classification_data["y_pred"]

    metrics = calculate_hallucination_metrics(y_true, y_pred)

    # Verify all expected metrics are present
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "confusion_matrix" in metrics

    # Verify metric values are valid
    assert 0 <= metrics["accuracy"] <= 1
    assert 0 <= metrics["precision"] <= 1
    assert 0 <= metrics["recall"] <= 1
    assert 0 <= metrics["f1_score"] <= 1

    # Confusion matrix should sum to total samples
    cm = metrics["confusion_matrix"]
    assert cm.sum() == len(y_true)


def test_io_utilities_integration(tmp_path):
    """Test I/O utilities integration."""
    # Test ensure_directory
    test_dir = tmp_path / "test_output" / "nested" / "dir"
    ensure_directory(test_dir)
    assert test_dir.exists()
    assert test_dir.is_dir()

    # Test write_json and read_json
    test_data = {
        "model": "gpt-4-turbo",
        "accuracy": 0.95,
        "queries": ["Q001", "Q002", "Q003"]
    }

    json_file = test_dir / "test.json"
    write_json(json_file, test_data)

    loaded_data = read_json(json_file)
    assert loaded_data == test_data
    assert loaded_data["accuracy"] == 0.95
    assert len(loaded_data["queries"]) == 3
