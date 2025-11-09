# Development Guide

Guide for developers contributing to this project.

---

## Development Setup

```bash
# Clone and setup
git clone https://github.com/olaflaitinen/llm-proteomics-hallucination.git
cd llm-proteomics-hallucination

# Create environment
conda env create -f environment.yml
conda activate llm-proteomics

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Install package in editable mode
pip install -e .
```

---

## Code Style

### Python

Follow PEP 8 style guide.

**Tools**:
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

**Pre-commit hooks** automatically format code on commit.

###Type Hints

Use type hints for all functions:
```python
def process_query(query: str, model: str = "gpt-4") -> Dict[str, Any]:
    """Process a single query."""
    ...
```

### Docstrings

Use Google style docstrings:
```python
def function(arg1: int, arg2: str) -> bool:
    """Short description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input
    """
    ...
```

---

## Testing

### Writing Tests

```python
import pytest
from src.module import function

def test_function():
    """Test function with normal input."""
    result = function(input="test")
    assert result == expected

def test_function_error():
    """Test function with invalid input."""
    with pytest.raises(ValueError):
        function(input="invalid")
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_hallucination_detector.py

# With coverage
pytest --cov=src --cov-report=html

# Verbose
pytest -vv

# Skip slow tests
pytest -m "not slow"
```

### Test Organization

- Unit tests: `tests/`
- Integration tests: `tests/integration/`
- Fixtures: `tests/conftest.py`

---

## Git Workflow

### Branching

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes
git add .
git commit -m "feat: description"

# Push
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### Commit Messages

Use conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples**:
```
feat(llm): Add support for GPT-4o

Implement client for new GPT-4o model with improved
hallucination detection capabilities.

Closes #123
```

---

## Code Review

All pull requests require review:

1. **Create PR** with clear description
2. **CI passes** (tests, linting)
3. **Code review** by maintainer
4. **Address feedback**
5. **Approved and merged**

---

## Release Process

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create git tag
4. Push to GitHub
5. Create GitHub release
6. Publish to PyPI (if applicable)

---

## Documentation

Update docs when adding features:

- Code comments for complex logic
- Docstrings for all public functions
- README if adding major features
- API.md for new API endpoints

---

## Performance

Profile code before optimizing:

```python
import cProfile

cProfile.run('expensive_function()')
```

Use appropriate data structures:
- Lists for ordered data
- Sets for membership testing
- Dicts for key-value pairs

---

## Debugging

```python
# Use pdb
import pdb; pdb.set_trace()

# Or ipdb for better interface
import ipdb; ipdb.set_trace()

# Logging instead of print
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

---

## CI/CD

GitHub Actions run automatically:

- **Tests**: On all pushes and PRs
- **Linting**: Check code style
- **Coverage**: Ensure >80% coverage

See `.github/workflows/` for configuration.

---

## Questions?

See [CONTRIBUTING.md](CONTRIBUTING.md) or contact olyulaim@dtu.dk

**Last Updated**: November 9, 2024
