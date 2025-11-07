#!/bin/bash
# Run LLM benchmark suite

echo "Running LLM benchmark..."
python -m src.llm_evaluation.benchmark_suite --config config/experiment_config.yaml
