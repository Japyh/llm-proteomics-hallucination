# Source Code

Python package for LLM proteomics hallucination evaluation.

---

## Modules

### llm_evaluation/

LLM client implementations and hallucination detection.

- `llm_client.py`: API clients for OpenAI, Anthropic, Google
- `hallucination_detector.py`: Hallucination detection framework
- `benchmark_suite.py`: Benchmarking tools
- `prompt_templates.py`: Query templates

### analysis/

Statistical analysis and visualization.

- `metrics.py`: Performance metrics
- `statistical_tests.py`: Statistical testing
- `visualization.py`: Plotting functions

### data_processing/

Data loading and processing.

- `protein_database.py`: Protein database interface
- `synthetic_data_generator.py`: Synthetic data generation

### utils/

Utility functions and helpers.

- `config.py`: Configuration management
- `logger.py`: Logging setup
- `validators.py`: Data validation
- `helpers.py`: Helper functions

---

## Usage

```python
from src.llm_evaluation import LLMClient
from src.analysis import metrics

# Initialize client
client = LLMClient(model="gpt-4")

# Query
response = client.query("What is HBB?")

# Calculate metrics
score = metrics.hallucination_score(response, ground_truth)
```

---

**See individual module READMEs for details**
