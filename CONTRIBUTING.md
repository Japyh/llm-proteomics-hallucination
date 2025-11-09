# Contributing to LLM Proteomics Hallucination Study

Thank you for your interest in contributing to this research project.

---

## Overview

This repository contains research materials for a study evaluating hallucination risks of large language models in clinical proteomics, submitted to The Lancet Digital Health.

**Principal Investigator**: Olaf Yunus Laitinen Imanov (Technical University of Denmark)

---

## How to Contribute

### Research Collaboration

If you are interested in research collaboration:

1. **Contact the Principal Investigator**: Email olyulaim@dtu.dk with:
   - Your background and expertise
   - Specific areas of interest
   - Proposed collaboration approach

2. **Review the Study Protocol**: Read `STUDY_PROTOCOL.md` to understand the research design

3. **Ethics Compliance**: All contributions must comply with DTU Ethics Protocol #2024-DTU-0385

### Code Contributions

We welcome contributions to improve code quality, documentation, and reproducibility.

#### Before Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Read existing documentation**: Familiarize yourself with the codebase
4. **Check open issues**: See if your contribution addresses an existing issue

#### Code Standards

**Python Code**:
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Maintain test coverage >80%

**Style Tools**:
```bash
# Format code with black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Check with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

**Testing**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

#### Commit Messages

Use conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

**Example**:
```
feat(analysis): Add calibration plot generation

Implement calibration analysis for hallucination risk prediction
model using observed vs predicted probabilities.

Closes #42
```

#### Pull Request Process

1. **Update documentation**: Ensure README and relevant docs are updated
2. **Add tests**: All new code must have corresponding tests
3. **Run test suite**: Ensure all tests pass
4. **Update CHANGELOG**: Add entry describing your changes
5. **Create pull request**: Use the PR template
6. **Code review**: Address reviewer feedback
7. **Merge**: Maintainers will merge after approval

### Documentation Contributions

Improvements to documentation are highly valued:

- Fix typos or unclear explanations
- Add examples and tutorials
- Improve API documentation
- Translate documentation (contact first)

### Bug Reports

**Before submitting**:
1. Check if the issue already exists
2. Verify the bug is reproducible
3. Collect relevant information

**Bug Report Template**:
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.5]
- Package versions: [paste requirements.txt]

## Additional Context
Screenshots, logs, etc.
```

### Feature Requests

**Before requesting**:
1. Check if similar requests exist
2. Ensure alignment with research goals
3. Consider implementation feasibility

**Feature Request Template**:
```markdown
## Feature Description
Clear description of proposed feature

## Motivation
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've considered

## Additional Context
Any other relevant information
```

---

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- Conda or virtualenv

### Installation

```bash
# Clone repository
git clone https://github.com/olaflaitinen/llm-proteomics-hallucination.git
cd llm-proteomics-hallucination

# Create environment
conda env create -f environment.yml
conda activate llm-proteomics

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_hallucination_detector.py

# With coverage
pytest --cov=src --cov-report=html

# Skip slow tests
pytest -m "not slow"
```

### Building Documentation

```bash
# Generate API documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

---

## Code Review Process

All contributions undergo code review:

1. **Automated checks**: CI/CD runs tests and linters
2. **Peer review**: At least one maintainer reviews code
3. **Feedback**: Address all comments and suggestions
4. **Approval**: Maintainer approves after satisfactory review
5. **Merge**: Maintainer merges to main branch

**Review Criteria**:
- Code quality and style
- Test coverage
- Documentation completeness
- Alignment with research goals
- Performance impact

---

## Research Ethics

All contributions must comply with:

- **DTU Ethics Protocol** #2024-DTU-0385
- **GDPR** (General Data Protection Regulation)
- **Research integrity guidelines**

**Critical Rules**:
- **Never** commit real patient data
- **Never** include API keys or credentials
- **Always** use synthetic data for testing
- **Always** respect privacy and confidentiality

---

## Communication

### Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: olyulaim@dtu.dk (research collaboration)

### Response Time

- Issues: Within 7 days
- Pull requests: Within 14 days
- Email: Within 5 business days

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Attribution

Contributors will be acknowledged in:
- `AUTHORS.md` file
- Publication acknowledgments (for significant contributions)
- Git commit history

### Significant Contributions

Contributions that may warrant co-authorship:
- Major algorithmic improvements
- Substantial code contributions (>500 lines)
- Critical bug fixes affecting results
- Significant documentation improvements

**Co-authorship criteria** follow ICMJE guidelines. Contact PI to discuss.

---

## License

By contributing, you agree that your contributions will be licensed under:
- **Code**: MIT License
- **Data**: CC-BY 4.0

See [LICENSE](LICENSE) for details.

---

## Questions?

If you have questions about contributing:
- Check [FAQ.md](FAQ.md)
- Open a GitHub Discussion
- Email: olyulaim@dtu.dk

---

## Acknowledgments

Thank you for contributing to improving AI safety in clinical proteomics!

---

**Last Updated**: November 9, 2024
**Maintainer**: Olaf Yunus Laitinen Imanov (olyulaim@dtu.dk)
