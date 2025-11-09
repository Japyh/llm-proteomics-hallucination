# Container Documentation

This directory contains Docker configurations for the LLM Proteomics Hallucination Evaluation project.

## Available Containers

### 1. GPU-Enabled Container (`Dockerfile.gpu`)

High-performance container with CUDA support for running LLM inference and evaluation pipelines.

**Features:**
- NVIDIA CUDA 12.1 with cuDNN 8
- PyTorch with GPU acceleration
- vLLM for efficient LLM serving
- Complete proteomics analysis stack
- Supports multi-GPU inference

**Build:**
```bash
docker build -f containers/Dockerfile.gpu -t llm-proteomics-gpu .
```

**Run Examples:**

Start vLLM server:
```bash
docker run --gpus all -p 8000:8000 \
  -v /path/to/models:/workspace/models \
  llm-proteomics-gpu \
  vllm serve /workspace/models/llama3-70b-instruct \
  --host 0.0.0.0 --port 8000 --tensor-parallel-size 2
```

Run evaluation pipeline:
```bash
docker run --gpus all \
  -v $(pwd):/workspace \
  -v /path/to/models:/workspace/models \
  llm-proteomics-gpu \
  python pipelines/run_evaluation.py --config configs/evaluation/default.yaml
```

Interactive shell:
```bash
docker run --gpus all -it \
  -v $(pwd):/workspace \
  llm-proteomics-gpu /bin/bash
```

**GPU Requirements:**
- NVIDIA GPU with compute capability 7.0+
- NVIDIA Driver 535.86.05+
- 40GB+ VRAM for 70B models (2x A100 recommended)
- 16GB+ VRAM for 7B-13B models

### 2. Jupyter Notebooks Container (`notebooks_container.Dockerfile`)

Lightweight container optimized for interactive analysis and visualization.

**Features:**
- JupyterLab 4.x
- Complete data science stack (NumPy, Pandas, SciPy, scikit-learn)
- Advanced visualization libraries (Plotly, Seaborn, Altair)
- Proteomics-specific tools (Pyteomics, Biopython)
- Pre-configured extensions and themes

**Build:**
```bash
docker build -f containers/notebooks_container.Dockerfile -t llm-proteomics-notebooks .
```

**Run:**
```bash
docker run -p 8888:8888 \
  -v $(pwd):/home/jovyan/work \
  llm-proteomics-notebooks
```

Access JupyterLab at: http://localhost:8888

**With GPU Support:**
```bash
docker run --gpus all -p 8888:8888 \
  -v $(pwd):/home/jovyan/work \
  llm-proteomics-notebooks
```

## Docker Compose

For orchestrating multiple services, use Docker Compose:

```yaml
# docker-compose.yml
version: '3.8'

services:
  vllm-server:
    build:
      context: .
      dockerfile: containers/Dockerfile.gpu
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    ports:
      - "8000:8000"
    volumes:
      - ./models:/workspace/models
      - ./logs:/workspace/logs
    command: >
      vllm serve /workspace/models/llama3-70b-instruct
      --host 0.0.0.0 --port 8000
      --tensor-parallel-size 2

  notebooks:
    build:
      context: .
      dockerfile: containers/notebooks_container.Dockerfile
    ports:
      - "8888:8888"
    volumes:
      - .:/home/jovyan/work
    environment:
      - JUPYTER_TOKEN=""

  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.10.2
    ports:
      - "5000:5000"
    volumes:
      - ./mlruns:/mlflow/mlruns
    command: >
      mlflow server
      --host 0.0.0.0
      --port 5000
      --backend-store-uri sqlite:///mlflow/mlflow.db
      --default-artifact-root /mlflow/mlruns
```

Start all services:
```bash
docker-compose up -d
```

## Software Bill of Materials (SBOM)

The `sbom/` directory contains CycloneDX SBOM files documenting all dependencies.

View SBOM:
```bash
cat containers/sbom/bom.cyclonedx.xml
```

Validate SBOM:
```bash
cyclonedx-cli validate --input-file containers/sbom/bom.cyclonedx.xml
```

## Environment Variables

### GPU Container

| Variable | Description | Default |
|----------|-------------|---------|
| `CUDA_VISIBLE_DEVICES` | GPU devices to use | `all` |
| `VLLM_WORKER_MULTIPROC_METHOD` | Multiprocessing method | `spawn` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `GOOGLE_API_KEY` | Google AI API key | - |
| `MISTRAL_API_KEY` | Mistral API key | - |
| `MLFLOW_TRACKING_URI` | MLflow server URI | `http://localhost:5000` |
| `WANDB_API_KEY` | Weights & Biases API key | - |

### Notebooks Container

| Variable | Description | Default |
|----------|-------------|---------|
| `JUPYTER_TOKEN` | Jupyter authentication token | `""` (disabled) |
| `JUPYTER_ENABLE_LAB` | Enable JupyterLab interface | `yes` |

## Volume Mounts

Recommended volume mounts for development:

```bash
docker run --gpus all -it \
  -v $(pwd):/workspace \
  -v /data/models:/workspace/models \
  -v /data/cache:/workspace/cache \
  -v /data/outputs:/workspace/outputs \
  llm-proteomics-gpu /bin/bash
```

## Security Considerations

### API Keys
- Never commit API keys to version control
- Use environment variables or Docker secrets
- Mount secrets as read-only volumes

```bash
docker run --gpus all \
  -e OPENAI_API_KEY_FILE=/run/secrets/openai_key \
  -v /path/to/secrets:/run/secrets:ro \
  llm-proteomics-gpu
```

### Network Isolation
- Use Docker networks for service-to-service communication
- Don't expose unnecessary ports
- Use reverse proxy (nginx) for production

### Resource Limits
```bash
docker run --gpus all \
  --memory=64g \
  --cpus=16 \
  --shm-size=16g \
  llm-proteomics-gpu
```

## Troubleshooting

### CUDA Out of Memory
```bash
# Reduce batch size or sequence length
docker run --gpus all \
  -e VLLM_GPU_MEMORY_UTILIZATION=0.85 \
  llm-proteomics-gpu
```

### Slow Model Loading
```bash
# Use shared memory for faster model loading
docker run --gpus all --shm-size=16g llm-proteomics-gpu
```

### Permission Errors
```bash
# Run as current user
docker run --gpus all \
  --user $(id -u):$(id -g) \
  -v $(pwd):/workspace \
  llm-proteomics-gpu
```

## Performance Optimization

### Multi-GPU Inference
```bash
docker run --gpus '"device=0,1"' \
  llm-proteomics-gpu \
  vllm serve model --tensor-parallel-size 2
```

### CPU Pinning
```bash
docker run --gpus all \
  --cpuset-cpus="0-15" \
  llm-proteomics-gpu
```

### Persistent Storage
```bash
# Use named volumes for better I/O performance
docker volume create models-cache
docker run --gpus all \
  -v models-cache:/workspace/models \
  llm-proteomics-gpu
```

## Registry and Deployment

### Push to Registry
```bash
# Tag image
docker tag llm-proteomics-gpu registry.example.com/llm-proteomics-gpu:v1.0.0

# Push to registry
docker push registry.example.com/llm-proteomics-gpu:v1.0.0
```

### Pull and Run
```bash
docker pull registry.example.com/llm-proteomics-gpu:v1.0.0
docker run --gpus all registry.example.com/llm-proteomics-gpu:v1.0.0
```

## CI/CD Integration

Containers are automatically built and tested in GitHub Actions. See `.github/workflows/` for CI configuration.

## License

Containers inherit the project license. See [LICENSE](../LICENSE) for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/llm-proteomics-hallucination/issues
- Documentation: https://llm-proteomics-docs.readthedocs.io/

## References

- [Docker Documentation](https://docs.docker.com/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/)
- [vLLM Documentation](https://docs.vllm.ai/)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)
