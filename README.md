# LLM Hallucination Risks in Clinical Proteomics Data Interpretation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/olaflaitinen/llm-proteomics-hallucination/workflows/tests/badge.svg)](https://github.com/olaflaitinen/llm-proteomics-hallucination/actions)

## Research Overview

This repository contains the complete research framework for analyzing hallucination risks when using Large Language Models (LLMs) to interpret mass spectrometry and proteomics data in clinical settings. This is a collaborative academic research project between olaflaitinen and Japyh, focusing on AI safety and ethics in healthcare applications.

### Problem Statement

Large Language Models (GPT-4, Claude, Gemini) are increasingly being explored for clinical decision support systems. However, their tendency to "hallucinate" - generating confident but factually incorrect information - poses significant risks when interpreting complex proteomics data. This research systematically evaluates:

- **Hallucination frequency** across different LLM providers
- **Types of errors** in protein function prediction and mass spectrometry interpretation
- **Clinical impact** of hallucinated information on diagnostic decisions
- **Mitigation strategies** for safe deployment in healthcare settings

### Research Objectives

1. Develop a comprehensive benchmark suite for evaluating LLM performance on proteomics tasks
2. Quantify hallucination rates across different LLM providers (OpenAI, Anthropic, Google)
3. Categorize types of factual errors (invented proteins, incorrect functions, false clinical associations)
4. Assess clinical relevance and potential patient harm from hallucinated information
5. Propose ethical frameworks and technical safeguards for clinical AI deployment
6. Publish findings in Q1-level academic journal (DergiPark or TÜBİTAK ULAKBİM TR Dizin)

## Project Structure

```
llm-proteomics-hallucination/
├── data/                      # Data storage (synthetic only)
│   ├── raw/                   # Raw data (never commit patient data)
│   ├── processed/             # Processed datasets
│   └── synthetic/             # Synthetic test data
├── literature/                # Academic papers and bibliography
├── notebooks/                 # Jupyter notebooks for analysis
├── src/                       # Source code
│   ├── data_processing/       # Data parsing and generation
│   ├── llm_evaluation/        # LLM testing and evaluation
│   ├── analysis/              # Statistical analysis and metrics
│   └── utils/                 # Utility functions
├── tests/                     # Unit and integration tests
├── results/                   # Analysis outputs and figures
├── manuscript/                # LaTeX manuscript files
├── ethics/                    # Ethics documentation and protocols
├── config/                    # Configuration files
├── scripts/                   # Automation scripts
└── docs/                      # Documentation

```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Conda (recommended) or pip
- API keys for OpenAI, Anthropic, and Google AI (optional for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/olaflaitinen/llm-proteomics-hallucination.git
   cd llm-proteomics-hallucination
   ```

2. **Create and activate virtual environment**

   Using Conda (recommended):
   ```bash
   conda env create -f environment.yml
   conda activate llm-proteomics-hallucination
   ```

   Using pip:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (DO NOT commit this file)
   ```

4. **Run setup verification**
   ```bash
   python scripts/setup_project.sh
   jupyter notebook notebooks/00_setup_and_verification.ipynb
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test module
pytest tests/test_hallucination_detector.py
```

### Running Analysis

```bash
# Execute notebooks in order
jupyter lab notebooks/01_data_exploration.ipynb

# Or run full benchmark
bash scripts/run_benchmark.sh
```

## Key Features

### 1. Comprehensive LLM Evaluation Framework
- Unified client for multiple LLM providers (OpenAI, Anthropic, Google)
- Standardized prompt templates for proteomics tasks
- Automated hallucination detection and classification
- Cost tracking and rate limiting

### 2. Synthetic Data Generation
- Realistic protein sequences and mass spectrometry data
- Configurable difficulty levels (easy, medium, hard, expert)
- GDPR-compliant synthetic clinical contexts
- Edge cases and ambiguous scenarios

### 3. Hallucination Detection
- Cross-reference with UniProt, PDB, and GO databases
- Identify invented proteins, functions, and interactions
- Detect temporal inconsistencies and impossible claims
- Confidence scoring for each validation

### 4. Statistical Analysis
- Inter-rater reliability (Cohen's kappa, Fleiss' kappa)
- Significance testing (t-tests, ANOVA, chi-square)
- Effect size calculations
- Multiple comparison corrections

### 5. Ethics and Privacy
- GDPR compliance guidelines
- Data anonymization tools
- IRB protocol templates
- Patient consent form templates

## Research Methodology

### Phase 1: Literature Review (Month 1-2)
- Systematic review of LLM hallucination research
- Clinical AI safety literature
- Proteomics bioinformatics standards

### Phase 2: Data Collection & Tool Development (Month 2-4)
- Develop synthetic proteomics datasets
- Implement LLM evaluation framework
- Create hallucination detection algorithms

### Phase 3: Empirical Evaluation (Month 4-6)
- Benchmark LLMs on proteomics tasks
- Collect expert evaluations
- Quantify hallucination rates

### Phase 4: Analysis & Interpretation (Month 6-8)
- Statistical analysis of results
- Clinical impact assessment
- Comparative analysis across LLM providers

### Phase 5: Manuscript Preparation (Month 8-12)
- Write academic paper
- Prepare visualizations
- Submit to target journal

## Contributing

We welcome contributions from the research community. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### For Project Team Members

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes and commit: `git commit -m "Description of changes"`
3. Push to your branch: `git push origin feature/your-feature-name`
4. Create a Pull Request for review

## Code Quality Standards

- **Style**: Follow PEP 8, enforced by Black
- **Type hints**: Required for all functions
- **Docstrings**: Google-style docstrings for all public APIs
- **Testing**: Minimum 70% code coverage
- **Linting**: Pass flake8 and mypy checks

## Data Privacy and Ethics

**CRITICAL**: This repository must NEVER contain:
- Real patient data
- Personal health information (PHI)
- Personally identifiable information (PII)
- Actual clinical records
- Real API keys or credentials

All data analysis must use synthetic or properly anonymized datasets. See [ethics/data_management_plan.md](ethics/data_management_plan.md) for details.

## Citation

If you use this research or code, please cite:

```bibtex
@article{llm_proteomics_hallucination_2024,
  title={Hallucination Risks in Large Language Model Interpretation of Clinical Proteomics Data},
  author={Laitinen, Olaf and [Co-author Name]},
  journal={[Target Journal]},
  year={2024},
  note={In preparation}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Research collaboration between olaflaitinen and Japyh
- Target publication: DergiPark or TÜBİTAK ULAKBİM TR Dizin indexed journals
- Compliance with Helsinki Declaration principles

## Contact

- **Project Lead**: olaflaitinen
- **Collaborator**: Japyh
- **Issues**: Please use GitHub Issues for bug reports and feature requests
- **Security**: See [SECURITY.md](SECURITY.md) for vulnerability reporting

## Status

**Current Status**: Initial Setup
**Last Updated**: 2024-01-15
**Version**: 0.1.0-alpha

See [ROADMAP.md](ROADMAP.md) for project timeline and milestones.

## Links

- [Documentation](docs/index.md)
- [Project Plan](PROJECT_PLAN.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
