# Architecture

## System Overview

This repository implements a comprehensive evaluation framework for assessing hallucinations in large language models applied to clinical proteomics.

## Directory Structure

```
.
├── notebooks/          # Jupyter notebooks for analysis
├── src/               # Source code
│   ├── llm_eval/      # LLM evaluation modules
│   ├── analysis/      # Statistical analysis
│   └── data_processing/ # Data processing utilities
├── data/              # Datasets and results
├── paper/             # Manuscript and figures
├── tests/             # Unit and integration tests
└── configs/           # Configuration files
```

## Key Components

### 1. LLM Evaluation Pipeline
- Multi-model client wrappers (OpenAI, Anthropic, Google)
- Prompt management and versioning
- Response caching and logging

### 2. Analysis Framework
- Statistical modeling (frequentist and Bayesian)
- Bias detection and measurement
- Robustness testing

### 3. Data Management
- Query generation and management
- Expert annotation workflow
- MS/MS validation integration

## Design Principles

1. **Reproducibility**: All analyses use seed 42
2. **Transparency**: Full audit logs and provenance tracking
3. **Modularity**: Loosely coupled components
4. **Testability**: Comprehensive unit and integration tests
