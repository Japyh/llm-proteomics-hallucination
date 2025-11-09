FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY notebooks/ notebooks/
COPY configs/ configs/

# Set environment
ENV PYTHONPATH=/app

CMD ["python", "-m", "src.llm_eval.runner"]
