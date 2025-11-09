# Test Suite

Automated tests for the LLM proteomics hallucination study codebase.

---

## Running Tests

### Quick Start

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_llm_client.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "hallucination"
```

---

## Test Structure

```
tests/
├── conftest.py                      # Pytest configuration and fixtures
├── test_llm_client.py               # LLM client tests
├── test_hallucination_detector.py   # Hallucination detection tests
├── test_data_processing.py          # Data processing tests
├── test_statistical_analysis.py     # Statistical analysis tests
└── README.md                        # This file
```

---

## Test Coverage

### Target Coverage

- **Minimum**: 80% code coverage
- **Goal**: 90% code coverage for core modules

### Current Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=term-missing
```

---

## Test Categories

### Unit Tests

Test individual functions and classes in isolation.

**Example**: `test_llm_client.py`
- Test LLM API client initialization
- Test response parsing
- Test error handling

### Integration Tests

Test interactions between components.

**Example**: `test_hallucination_detector.py`
- Test hallucination detection pipeline
- Test database integration
- Test cross-reference validation

### Data Validation Tests

Ensure data quality and consistency.

**Example**: `test_data_processing.py`
- Validate query dataset structure
- Check ground truth completeness
- Verify protein annotations

---

## Writing Tests

### Test Structure

```python
import pytest
from src.llm_evaluation.llm_client import LLMClient

def test_llm_client_initialization():
    """Test that LLM client initializes correctly."""
    client = LLMClient(model="gpt-4-0125-preview")
    assert client.model == "gpt-4-0125-preview"
    assert client.is_ready()

def test_llm_response_parsing():
    """Test that LLM responses are parsed correctly."""
    client = LLMClient(model="gpt-4-0125-preview")
    response = client.parse_response(mock_response)
    assert "response_text" in response
    assert "timestamp" in response
```

### Pytest Fixtures

Use fixtures in `conftest.py` for common test data:

```python
import pytest

@pytest.fixture
def sample_queries():
    """Provide sample queries for testing."""
    return [
        {
            "query_id": "Q001",
            "query_text": "What is the function of HBB?",
            "domain": "protein_identification"
        }
    ]

@pytest.fixture
def mock_llm_response():
    """Provide mock LLM response for testing."""
    return {
        "query_id": "Q001",
        "response_text": "HBB encodes hemoglobin...",
        "timestamp": "2024-03-15T10:30:00Z"
    }
```

### Test Naming Conventions

- Test files: `test_<module_name>.py`
- Test functions: `test_<functionality>_<expected_behavior>`
- Test classes: `Test<ClassName>`

**Examples**:
- `test_validate_query_structure()`
- `test_detect_hallucination_returns_true_for_fabrication()`
- `class TestHallucinationDetector`

---

## Continuous Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Nightly builds

See `.github/workflows/tests.yml` for CI configuration.

---

## Test Configuration

### conftest.py

Contains pytest configuration and shared fixtures:

```python
import pytest
import os

@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory."""
    return os.path.join(os.path.dirname(__file__), "test_data")

@pytest.fixture
def disable_api_calls(monkeypatch):
    """Disable real API calls during testing."""
    def mock_api_call(*args, **kwargs):
        return {"response": "mocked"}
    monkeypatch.setattr("openai.ChatCompletion.create", mock_api_call)
```

### pytest.ini

Configure pytest behavior:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --cov=src
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    api: marks tests that require API access
    integration: marks integration tests
```

---

## Mocking External Services

### Mock LLM API Calls

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls."""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {
            'choices': [{'message': {'content': 'Mocked response'}}]
        }
        yield mock

def test_query_gpt4(mock_openai):
    """Test GPT-4 query with mocked API."""
    from src.llm_evaluation.llm_client import query_gpt4
    response = query_gpt4("Test query")
    assert response == 'Mocked response'
    mock_openai.assert_called_once()
```

### Mock Database Queries

```python
@pytest.fixture
def mock_uniprot():
    """Mock UniProt database queries."""
    with patch('src.data_processing.database.query_uniprot') as mock:
        mock.return_value = {
            'protein_id': 'P68871',
            'gene_name': 'HBB',
            'function': 'Oxygen transport'
        }
        yield mock
```

---

## Performance Testing

### Benchmark Tests

```python
import pytest

@pytest.mark.slow
def test_hallucination_detection_performance():
    """Benchmark hallucination detection speed."""
    from src.llm_evaluation.hallucination_detector import detect_hallucinations

    queries = load_test_queries(n=100)

    import time
    start = time.time()
    detect_hallucinations(queries)
    duration = time.time() - start

    assert duration < 60, f"Detection took {duration}s (expected <60s)"
```

---

## Test Data

### Test Data Location

```
tests/test_data/
├── sample_queries.json
├── sample_responses.json
├── sample_ground_truth.json
└── sample_proteins.fasta
```

### Test Data Guidelines

- Keep test data small (<100 KB per file)
- Use synthetic data only
- Include edge cases
- Document test data provenance

---

## Troubleshooting

### Tests Failing Locally

```bash
# Clear pytest cache
pytest --cache-clear

# Run tests in verbose mode
pytest -vv

# Run specific failing test
pytest tests/test_llm_client.py::test_specific_function -vv
```

### Import Errors

```bash
# Ensure src is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Or install package in development mode
pip install -e .
```

### API Tests Failing

```bash
# Skip API tests
pytest -m "not api"

# Set test API keys
export OPENAI_API_KEY="test_key"
export ANTHROPIC_API_KEY="test_key"
```

---

## Best Practices

### Test-Driven Development

1. Write failing test first
2. Implement minimum code to pass
3. Refactor while keeping tests green

### Code Coverage

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Open report
open htmlcov/index.html
```

### Test Documentation

- Add docstrings to all test functions
- Explain what is being tested
- Document expected behavior

---

## Running Specific Test Categories

```bash
# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration

# Run tests excluding API tests
pytest -m "not api"
```

---

## Continuous Integration

Tests run automatically via GitHub Actions on every push and pull request.

**CI Workflow**:
1. Install dependencies
2. Run pytest with coverage
3. Upload coverage to Codecov
4. Fail if coverage <80%

---

**Last Updated**: November 9, 2024
**Test Framework**: pytest 7.4.0+
