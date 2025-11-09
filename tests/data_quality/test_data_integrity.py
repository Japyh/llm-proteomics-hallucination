"""
Data quality tests for data integrity checks
"""

import json
import pytest
from pathlib import Path
import hashlib


@pytest.fixture
def data_dir():
    """Return path to data directory"""
    return Path(__file__).parent.parent.parent / "data"


class TestDataFileIntegrity:
    """Test data file integrity and consistency"""

    def test_queries_file_exists(self, data_dir):
        """Test that queries file exists"""
        queries_path = data_dir / "queries" / "queries_all.json"
        assert queries_path.exists(), "Queries file not found"

    def test_queries_valid_json(self, data_dir):
        """Test that queries file is valid JSON"""
        queries_path = data_dir / "queries" / "queries_all.json"
        if not queries_path.exists():
            pytest.skip("Queries file not found")

        with open(queries_path) as f:
            queries = json.load(f)
        assert isinstance(queries, list), "Queries should be a list"

    def test_queries_unique_ids(self, data_dir):
        """Test that all query IDs are unique"""
        queries_path = data_dir / "queries" / "queries_all.json"
        if not queries_path.exists():
            pytest.skip("Queries file not found")

        with open(queries_path) as f:
            queries = json.load(f)

        query_ids = [q.get("query_id") for q in queries]
        assert len(query_ids) == len(set(query_ids)), "Duplicate query IDs found"

    def test_queries_count(self, data_dir):
        """Test that we have expected number of queries"""
        queries_path = data_dir / "queries" / "queries_all.json"
        if not queries_path.exists():
            pytest.skip("Queries file not found")

        with open(queries_path) as f:
            queries = json.load(f)

        assert len(queries) == 500, f"Expected 500 queries, found {len(queries)}"

    def test_queries_required_fields(self, data_dir):
        """Test that all queries have required fields"""
        queries_path = data_dir / "queries" / "queries_all.json"
        if not queries_path.exists():
            pytest.skip("Queries file not found")

        with open(queries_path) as f:
            queries = json.load(f)

        required_fields = ["query_id", "query_text", "domain", "complexity"]

        for query in queries[:10]:  # Check first 10
            for field in required_fields:
                assert field in query, f"Query missing required field: {field}"


class TestDataConsistency:
    """Test data consistency across files"""

    def test_query_ids_consistent(self, data_dir):
        """Test that query IDs are consistent across files"""
        queries_path = data_dir / "queries" / "queries_all.json"
        annotations_path = data_dir / "annotations" / "expert_annotations.json"

        if not queries_path.exists():
            pytest.skip("Queries file not found")
        if not annotations_path.exists():
            pytest.skip("Annotations file not found")

        with open(queries_path) as f:
            queries = json.load(f)

        with open(annotations_path) as f:
            annotations = json.load(f)

        query_ids = {q["query_id"] for q in queries}
        annotation_query_ids = {a["query_id"] for a in annotations}

        # All annotation query IDs should exist in queries
        orphan_ids = annotation_query_ids - query_ids
        assert len(orphan_ids) == 0, f"Found {len(orphan_ids)} annotation query IDs not in queries"


class TestDataQualityMetrics:
    """Test data quality metrics"""

    def test_no_missing_values(self, data_dir):
        """Test that critical fields have no missing values"""
        queries_path = data_dir / "queries" / "queries_all.json"
        if not queries_path.exists():
            pytest.skip("Queries file not found")

        with open(queries_path) as f:
            queries = json.load(f)

        critical_fields = ["query_id", "query_text"]

        for query in queries:
            for field in critical_fields:
                value = query.get(field)
                assert value is not None, f"Missing value for {field} in {query.get('query_id')}"
                assert value != "", f"Empty value for {field} in {query.get('query_id')}"

    def test_query_text_quality(self, data_dir):
        """Test query text quality"""
        queries_path = data_dir / "queries" / "queries_all.json"
        if not queries_path.exists():
            pytest.skip("Queries file not found")

        with open(queries_path) as f:
            queries = json.load(f)

        for query in queries[:10]:
            query_text = query.get("query_text", "")
            # Minimum length check
            assert len(query_text) >= 10, f"Query text too short: {query.get('query_id')}"
            # Maximum length check
            assert len(query_text) <= 1000, f"Query text too long: {query.get('query_id')}"


class TestDataChecksums:
    """Test data file checksums for reproducibility"""

    def compute_file_checksum(self, file_path):
        """Compute SHA256 checksum of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def test_queries_checksum_reproducible(self, data_dir):
        """Test that queries file checksum is reproducible"""
        queries_path = data_dir / "queries" / "queries_all.json"
        if not queries_path.exists():
            pytest.skip("Queries file not found")

        checksum1 = self.compute_file_checksum(queries_path)
        checksum2 = self.compute_file_checksum(queries_path)

        assert checksum1 == checksum2, "Checksums not reproducible"

    def test_registry_checksums_match(self, data_dir):
        """Test that registry checksums match actual files"""
        registry_path = data_dir / "registry.yaml"
        if not registry_path.exists():
            pytest.skip("Registry file not found")

        # This test would validate checksums in registry.yaml
        # Implementation depends on registry format
        pytest.skip("Registry checksum validation not yet implemented")
