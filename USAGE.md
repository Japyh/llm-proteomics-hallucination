# Usage Guide

Quick start guide for using the LLM Proteomics Hallucination Study codebase.

---

## Quick Examples

### Load and Explore Query Dataset

```python
import json
import pandas as pd

# Load queries
with open('data/queries/queries_all.json') as f:
    queries = json.load(f)

print(f"Total queries: {len(queries)}")
print(f"First query: {queries[0]['query_text']}")

# Analyze stratification
df = pd.DataFrame(queries)
print(df['complexity'].value_counts())
print(df['protein_prevalence'].value_counts())
```

### Query an LLM

```python
from src.llm_evaluation.llm_client import LLMClient

# Initialize client
client = LLMClient(model="gpt-4-0125-preview", api_key="your_key")

# Send query
response = client.query("What is the function of hemoglobin beta?")
print(response)
```

### Detect Hallucinations

```python
from src.llm_evaluation.hallucination_detector import HallucinationDetector

# Initialize detector
detector = HallucinationDetector()

# Check response
result = detector.detect(
    query="What is the function of HBB?",
    response="HBB encodes hemoglobin...",
    ground_truth="Hemoglobin subunit beta..."
)

print(f"Hallucination detected: {result['is_hallucination']}")
print(f"Severity: {result['severity']}")
```

### Generate Figures

```bash
cd paper/figures

# Generate Figure 1
python generate_figure_1.py

# Generate all figures
for i in {1..4}; do
    python generate_figure_${i}.py
done

# Check outputs
ls -lh output/
```

### Run Statistical Analysis

```python
from src.analysis.statistical_tests import StatisticalAnalyzer

# Load data
analyzer = StatisticalAnalyzer('data/results/hallucination_rates.csv')

# Chi-square test
result = analyzer.chi_square_test(
    group1='GPT-4 Turbo',
    group2='Claude 3 Sonnet'
)

print(f"p-value: {result['p_value']:.4f}")
print(f"Significant: {result['significant']}")

# Logistic regression
model = analyzer.logistic_regression(
    outcome='hallucination',
    predictors=['complexity', 'prevalence', 'model']
)

print(model.summary())
```

---

## Common Tasks

### 1. Reproduce Main Results

```bash
# Run all analysis notebooks
jupyter nbconvert --execute --to html notebooks/*.ipynb

# Or run interactively
jupyter lab notebooks/
```

### 2. Generate New Queries

```bash
cd data/generators

# Generate query dataset
python generate_query_dataset.py --output ../queries/queries_new.json

# Generate protein sequences
python generate_protein_sequences.py

# Generate MS/MS spectra
python generate_ms_spectra.py
```

### 3. Compile Manuscript

```bash
cd paper

# Generate figures first
cd figures && python generate_figure_1.py && cd ..

# Compile manuscript
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex

# View PDF
open manuscript.pdf
```

### 4. Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific tests
pytest tests/test_hallucination_detector.py -v

# Skip slow tests
pytest -m "not slow"
```

---

## Jupyter Notebooks Workflow

### Recommended Order

1. **00_setup_and_verification.ipynb** - Verify environment
2. **01_data_exploration.ipynb** - Explore query dataset
3. **02_llm_benchmark.ipynb** - Query LLMs (requires API keys)
4. **03_hallucination_analysis.ipynb** - Detect hallucinations
5. **04_statistical_analysis.ipynb** - Statistical tests
6. **05_results_visualization.ipynb** - Generate figures

### Running Notebooks

```bash
# Start Jupyter Lab
jupyter lab

# Or run all non-interactively
jupyter nbconvert --execute --to html notebooks/*.ipynb
```

---

## API Usage

### OpenAI (GPT-4)

```python
from src.llm_evaluation.llm_client import GPT4Client

client = GPT4Client(api_key=os.getenv('OPENAI_API_KEY'))
response = client.query(
    prompt="What is the function of insulin?",
    max_tokens=500,
    temperature=0.7
)
```

### Anthropic (Claude)

```python
from src.llm_evaluation.llm_client import ClaudeClient

client = ClaudeClient(api_key=os.getenv('ANTHROPIC_API_KEY'))
response = client.query(
    prompt="What is the function of insulin?",
    max_tokens=500
)
```

### Google (Gemini)

```python
from src.llm_evaluation.llm_client import GeminiClient

client = GeminiClient(api_key=os.getenv('GOOGLE_API_KEY'))
response = client.query(
    prompt="What is the function of insulin?"
)
```

---

## Data Processing

### Load Ground Truth

```python
import json

# Load protein annotations
with open('data/ground_truth/protein_annotations.json') as f:
    annotations = json.load(f)

# Access protein data
for protein in annotations:
    print(f"{protein['gene_name']}: {protein['function'][:50]}...")
```

### Load Results

```python
import pandas as pd

# Load hallucination rates
rates = pd.read_csv('data/results/hallucination_rates.csv')

# Calculate overall rate
overall = rates['hallucination_rate'].mean()
print(f"Overall hallucination rate: {overall:.1f}%")

# By model
by_model = rates.groupby('model')['hallucination_rate'].mean()
print(by_model)
```

---

## Visualization

### Create Custom Plots

```python
import matplotlib.pyplot as plt
import pandas as pd

# Load data
data = pd.read_csv('data/results/hallucination_rates.csv')

# Create plot
fig, ax = plt.subplots(figsize=(10, 6))
data.groupby('model')['hallucination_rate'].mean().plot(kind='bar', ax=ax)
ax.set_ylabel('Hallucination Rate (%)')
ax.set_title('Hallucination Rates by Model')
plt.tight_layout()
plt.savefig('custom_plot.png', dpi=300)
```

---

## Command-Line Tools

### Generate Data

```bash
# Generate all data files
make data

# Or individually
python data/generators/generate_query_dataset.py
python data/generators/generate_protein_sequences.py
python data/generators/generate_ms_spectra.py
```

### Run Analysis

```bash
# Run complete analysis pipeline
make analysis

# Or step-by-step
python src/analysis/calculate_metrics.py
python src/analysis/statistical_tests.py
python src/analysis/generate_tables.py
```

---

## Docker Usage

```bash
# Build image
docker build -t llm-proteomics .

# Run container
docker run -it --rm \
  -v $(pwd):/workspace \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  llm-proteomics bash

# Run specific command
docker run -it --rm llm-proteomics pytest
```

---

## Best Practices

### API Rate Limiting

```python
import time

for query in queries:
    response = client.query(query['query_text'])
    time.sleep(1)  # Rate limiting
```

### Error Handling

```python
from src.llm_evaluation.llm_client import LLMClient, APIError

try:
    response = client.query(prompt)
except APIError as e:
    print(f"API error: {e}")
    # Handle error appropriately
```

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting analysis...")
```

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed troubleshooting guide.

### Quick Fixes

**Import Error**:
```bash
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

**API Error**:
```bash
# Check API keys
echo $OPENAI_API_KEY | head -c 10
```

**Test Failure**:
```bash
pytest -vv --tb=long
```

---

## Further Reading

- [Installation Guide](INSTALLATION.md)
- [Development Guide](DEVELOPMENT.md)
- [API Reference](API.md)
- [FAQ](FAQ.md)

---

**Last Updated**: November 9, 2024
