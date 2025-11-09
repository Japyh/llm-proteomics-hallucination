# MLflow Tracking Server

Track experiments, models, and metrics.

## Setup

```bash
mlflow server --backend-store-uri sqlite:///experiments.db --host 0.0.0.0 --port 5000
```

## Usage

```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("llm-hallucination-eval")

with mlflow.start_run():
    mlflow.log_param("model", "gpt-4-turbo")
    mlflow.log_metric("hallucination_rate", 0.334)
```
