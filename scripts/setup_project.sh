#!/bin/bash
# Setup project environment

echo "Setting up LLM Proteomics Hallucination Research Project..."

# Create directories
mkdir -p data/{raw,processed,synthetic}
mkdir -p results/{figures,tables,logs}
mkdir -p models

# Check Python version
python --version

# Install dependencies
pip install -r requirements.txt

echo "Setup complete!"
