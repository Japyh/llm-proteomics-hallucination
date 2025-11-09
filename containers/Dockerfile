# LLM Proteomics Hallucination Study - Production Container
# Python 3.11 base image
FROM python:3.11-slim as base

LABEL maintainer="Olaf Yunus Laitinen Imanov <olyulaim@dtu.dk>"
LABEL description="Container for LLM Proteomics Hallucination Study"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements
COPY requirements.txt .
COPY requirements-dev.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy source code
COPY . .

# Install package
RUN pip install -e .

# Run tests
RUN pytest tests/ -v

# Default command
CMD ["bash"]
