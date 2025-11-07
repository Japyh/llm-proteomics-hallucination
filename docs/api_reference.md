# API Reference

## LLM Evaluation Module

### LLMClient
Main client for interacting with LLM APIs.

```python
from src.llm_evaluation import LLMClient

client = LLMClient(provider='openai', model='gpt-4')
response = await client.query("What is hemoglobin?")
```

### HallucinationDetector
Detect hallucinations in LLM responses.

```python
from src.llm_evaluation import HallucinationDetector

detector = HallucinationDetector()
result = detector.detect(response.content)
```

## Data Processing Module

### SyntheticDataGenerator
Generate synthetic proteomics data.

```python
from src.data_processing import SyntheticDataGenerator

generator = SyntheticDataGenerator(seed=42)
df = generator.generate_protein_dataset(n_proteins=100)
```

## Analysis Module

### StatisticalTests
Perform statistical analyses.

```python
from src.analysis import StatisticalTests

kappa = StatisticalTests.cohens_kappa(ratings1, ratings2)
```
