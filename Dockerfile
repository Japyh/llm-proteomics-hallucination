# Dockerfile for LLM Proteomics Hallucination Research
# Provides a complete environment for running all code and compiling the paper

FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-bibtex-extra \
    biber \
    git \
    wget \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements first (for better caching)
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy the entire project
COPY . .

# Install the package in development mode
RUN pip install -e .

# Create output directories
RUN mkdir -p \
    paper/figures/output \
    results/figures \
    results/tables \
    results/logs \
    data/queries \
    data/ground_truth \
    data/llm_responses \
    data/results

# Set permissions
RUN chmod +x scripts/*.sh paper/compile.sh 2>/dev/null || true

# Default command
CMD ["/bin/bash"]
