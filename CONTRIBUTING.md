# Contributing Guidelines

Thank you for your interest in contributing to the LLM Proteomics Hallucination research project!

## Project Team

This is a collaborative academic research project between:
- **olaflaitinen** - Project Lead
- **Japyh** - Research Collaborator

External contributions are welcome with prior discussion.

## Getting Started

1. **Fork the repository** (for external contributors)
2. **Clone your fork** or the main repository
3. **Create a feature branch** from `main`
4. **Make your changes** following our coding standards
5. **Submit a pull request** for review

## Branch Strategy

### For Project Team Members

- `main` - Stable branch, protected
- `develop` - Integration branch for ongoing work
- `feature/*` - Feature development branches
- `bugfix/*` - Bug fix branches
- `experiment/*` - Experimental analysis branches

### Workflow

```bash
# Create a new feature branch
git checkout -b feature/your-feature-name

# Make changes and commit regularly
git add .
git commit -m "Descriptive commit message"

# Push to remote
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## Commit Message Guidelines

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style/formatting (no logic changes)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `data`: Data processing or generation
- `analysis`: Statistical analysis updates
- `paper`: Manuscript changes

### Examples

```
feat(llm_client): Add support for Google Gemini API

Implemented GeminiClient class with async support, rate limiting,
and error handling. Includes token counting and cost estimation.

Closes #23
```

```
fix(hallucination_detector): Correct UniProt ID validation

Fixed regex pattern for UniProt accession numbers to handle
isoform variants correctly.
```

```
analysis: Add inter-rater reliability calculations

Implemented Cohen's kappa and Fleiss' kappa for expert
evaluation agreement analysis.
```

## Code Quality Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) for code formatting
- Maximum line length: 88 characters (Black default)
- Use [isort](https://pycqa.github.io/isort/) for import sorting

### Type Hints

All functions must include type hints:

```python
def calculate_hallucination_rate(
    responses: List[str],
    ground_truth: Dict[str, Any],
    threshold: float = 0.5
) -> Tuple[float, Dict[str, int]]:
    """Calculate hallucination rate for LLM responses.

    Args:
        responses: List of LLM response strings
        ground_truth: Dictionary of correct answers
        threshold: Confidence threshold for detection

    Returns:
        Tuple of (hallucination_rate, error_counts)

    Raises:
        ValueError: If responses list is empty
    """
    pass
```

### Docstrings

Use Google-style docstrings for all public functions and classes:

```python
def validate_protein_id(protein_id: str, database: str = "uniprot") -> bool:
    """Validate protein identifier format against database standards.

    This function checks if a protein ID conforms to the format
    requirements of the specified database (UniProt, PDB, etc.).

    Args:
        protein_id: Protein identifier string to validate
        database: Target database name (default: "uniprot")
            Supported values: "uniprot", "pdb", "ensembl"

    Returns:
        True if the ID format is valid, False otherwise

    Raises:
        ValueError: If database name is not supported

    Examples:
        >>> validate_protein_id("P12345", "uniprot")
        True
        >>> validate_protein_id("INVALID", "uniprot")
        False
    """
    pass
```

### Testing Requirements

- Write tests for all new features
- Maintain minimum 70% code coverage
- Use pytest for testing
- Include both unit and integration tests

```python
# tests/test_hallucination_detector.py
import pytest
from src.llm_evaluation.hallucination_detector import detect_hallucination

def test_detect_invented_protein():
    """Test detection of completely invented protein names."""
    response = "The protein FAKE123 is involved in..."
    result = detect_hallucination(response)
    assert result['invented_protein'] is True
    assert result['confidence'] > 0.9

@pytest.mark.parametrize("protein_id,expected", [
    ("P12345", False),
    ("FAKE999", True),
    ("Q9Y6K9", False),
])
def test_protein_validation(protein_id, expected):
    """Test protein ID validation with multiple cases."""
    result = detect_hallucination(f"Protein {protein_id}")
    assert result['invented_protein'] == expected
```

### Pre-commit Checks

Before committing, ensure:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
pytest --cov=src
```

Or use pre-commit hooks (recommended):

```bash
pip install pre-commit
pre-commit install
```

## Code Review Process

### For Pull Requests

1. **Self-review**: Review your own changes before requesting review
2. **Tests pass**: Ensure all CI checks pass
3. **Documentation**: Update docs if adding new features
4. **Description**: Provide clear PR description with context
5. **Small PRs**: Keep PRs focused and reasonably sized

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No sensitive data or API keys
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] No breaking changes (or documented)

## Project-Specific Guidelines

### Data Files

- **NEVER commit** real patient data
- Use synthetic data only
- Add large data files to `.gitignore`
- Store example datasets in `data/synthetic/`

### API Keys and Secrets

- Store in `.env` file (gitignored)
- Use `.env.example` as template
- Never hardcode in source files
- Use environment variables

### Notebooks

- Clear output before committing
- Use `nbconvert` or JupyterLab "Clear All Outputs"
- Include markdown documentation cells
- Keep notebooks focused on one task

### Literature and Citations

- Add papers to `literature/papers/`
- Update `literature/bibliography.bib`
- Follow citation standards

## Communication

### Issues

- Use GitHub Issues for:
  - Bug reports
  - Feature requests
  - Questions and discussions
  - Task tracking

### Issue Templates

Use provided templates:
- Bug Report: Include reproduction steps and environment
- Feature Request: Describe use case and expected behavior

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No sensitive data included
```

## Academic Integrity

### Research Ethics

- Follow Helsinki Declaration principles
- Maintain data privacy (GDPR compliance)
- Ensure reproducibility
- Document methodology clearly
- Cite sources appropriately

### Authorship

- Significant contributions may warrant co-authorship
- Discuss with project leads before major contributions
- Acknowledge all contributors

## Questions?

- Open a GitHub Issue for questions
- Contact project leads: olaflaitinen, Japyh
- Review [Code of Conduct](CODE_OF_CONDUCT.md)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to advancing AI safety in healthcare!
