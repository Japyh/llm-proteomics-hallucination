# Data Directory

## Structure

- `queries/` - Proteomics query datasets
- `ground_truth/` - Expert annotations and adjudicated labels
- `llm_responses/` - Model responses from all evaluated LLMs
- `results/` - Analysis results and summary statistics
- `proteins/` - Protein databases and metadata
- `mass_spectrometry/` - MS/MS validation data
- `structured/` - Ontologies and structured knowledge
- `generators/` - Synthetic data generation scripts
- `schemas/` - JSON schemas for data validation

## Data Privacy

This directory may contain sensitive research data. See `data_management_plan.md` in `/ethics/` for handling procedures.

## Reproducibility

All data generation uses random seed 42. See individual generator scripts for details.
