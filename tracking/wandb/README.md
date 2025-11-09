# Weights & Biases (W&B) Tracking

Alternative to MLflow with rich visualization.

## Setup

```bash
wandb login
```

## Usage

```python
import wandb

wandb.init(project="llm-proteomics-hallucination", entity="your-team")

wandb.config.update({
    "model": "gpt-4-turbo",
    "temperature": 0.3
})

wandb.log({"hallucination_rate": 0.334})
```
