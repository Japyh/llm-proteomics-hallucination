# Container Documentation

## Building Images

```bash
docker build -f containers/Dockerfile -t llm-proteomics:latest .
```

## Running

```bash
docker-compose -f containers/docker-compose.yml up
```

## GPU Support

```bash
docker build -f containers/Dockerfile.gpu -t llm-proteomics:gpu .
docker run --gpus all llm-proteomics:gpu
```
