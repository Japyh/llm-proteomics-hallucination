# Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     LLM Proteomics Study                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  Data Layer  │───▶│ Processing   │───▶│   Analysis   │ │
│  │              │    │   Layer      │    │    Layer     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                   │          │
│         ▼                    ▼                   ▼          │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              LLM Evaluation Framework                 │ │
│  └──────────────────────────────────────────────────────┘ │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────────────────────────────────────────┐ │
│  │         Results, Figures, Manuscript                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Data Layer
- **Queries**: Proteomics questions stratified by complexity
- **Ground Truth**: Expert-validated annotations
- **LLM Responses**: API responses from GPT-4, Claude, Gemini
- **Proteins**: UniProt sequences, MS/MS spectra

### Processing Layer
- **Loaders**: Data ingestion and validation
- **Transformers**: Feature engineering, normalization
- **Quality Control**: Missing value handling, outlier detection

### Analysis Layer
- **Statistical Tests**: Chi-square, logistic regression, Bonferroni
- **Metrics**: Hallucination rates, Cohen's kappa, calibration
- **Visualization**: Matplotlib figures for manuscript

### LLM Evaluation
- **Clients**: OpenAI, Anthropic, Google API wrappers
- **Prompts**: Standardized query templates
- **Scoring**: Automated hallucination detection
- **Caching**: Response caching for reproducibility

## Data Flow

1. **Queries** → LLM APIs → **Responses**
2. **Responses** + **Ground Truth** → **Hallucination Detection**
3. **Detection Results** → **Statistical Analysis**
4. **Analysis** → **Figures & Tables**
5. **Assets** → **Manuscript Compilation**

## Technology Stack

- **Python**: 3.11+
- **Key Libraries**: pandas, numpy, scipy, scikit-learn, matplotlib
- **LLM APIs**: OpenAI, Anthropic, Google
- **Workflow**: Snakemake, Make
- **Containers**: Docker, docker-compose
- **Tracking**: MLflow, Weights & Biases

---
**Version**: 1.0.0
**Last Updated**: November 9, 2024
