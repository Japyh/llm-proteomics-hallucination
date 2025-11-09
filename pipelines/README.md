# Analysis Pipelines

This directory contains workflow orchestration for the LLM Proteomics Hallucination evaluation.

## Available Pipelines

### 1. Nextflow Pipeline

**Location**: `nextflow/`

Modern, portable workflow management system.

**Usage**:
```bash
cd nextflow
nextflow run main.nf -profile docker
```

**Modules**:
- `eval.nf`: LLM evaluation and response collection
- `bias_audit.nf`: Systematic bias analysis
- `figures.nf`: Publication figure generation

### 2. Snakemake Pipeline

**Location**: `snakemake/`

Python-based workflow management with make-like syntax.

**Usage**:
```bash
cd snakemake
snakemake --cores 8 --use-conda
```

**Rules**:
- `00_prepare.smk`: Data preparation
- `10_llm_eval.smk`: Model evaluation
- `20_analysis.smk`: Statistical analysis
- `30_visualization.smk`: Figure generation
- `40_bias_audit.smk`: Bias assessment
- `50_paper_assets.smk`: Paper outputs

## Configuration

Both pipelines use YAML configuration files:
- Nextflow: `nextflow/nextflow.config`
- Snakemake: `snakemake/config.yaml`

## Resource Requirements

### Minimal
- CPU: 8 cores
- RAM: 32 GB
- Storage: 100 GB

### Recommended
- CPU: 32 cores
- RAM: 128 GB
- GPU: 2× NVIDIA A100 (for local LLM inference)
- Storage: 500 GB

## Execution Time

- Full pipeline: ~48 hours (with API rate limits)
- LLM evaluation: ~36 hours
- Statistical analysis: ~4 hours
- Figure generation: ~2 hours

## Outputs

All pipelines produce:
- `results/model_comparison_metrics.csv`
- `results/calibration/`
- `figures/output/`
- `provenance/build_logs/`

## Troubleshooting

### Common Issues

**API Rate Limits**:
```bash
# Adjust in config
rate_limit_rpm: 60
```

**Out of Memory**:
```bash
# Increase batch size
batch_size: 5  # Lower for less memory
```

**Docker Permissions**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER
```

## Contact

For pipeline questions:
- Issues: https://github.com/olaflaitinen/llm-proteomics-hallucination/issues
- Email: olyulaim@dtu.dk
