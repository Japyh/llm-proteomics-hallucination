# Complete Tutorial: LLM Proteomics Hallucination Detection

This tutorial walks you through the complete workflow of evaluating LLM hallucinations in clinical proteomics interpretation.

## Table of Contents

1. [Setup and Installation](#setup)
2. [Data Exploration](#data-exploration)
3. [Running LLM Queries](#running-llm-queries)
4. [Detecting Hallucinations](#detecting-hallucinations)
5. [Statistical Analysis](#statistical-analysis)
6. [Visualization](#visualization)
7. [Full Benchmark](#full-benchmark)

---

## 1. Setup and Installation {#setup}

### Install Dependencies

```bash
# Clone repository
git clone https://github.com/olaflaitinen/llm-proteomics-hallucination.git
cd llm-proteomics-hallucination

# Create conda environment
conda env create -f environment.yml
conda activate llm-proteomics-hallucination

# Or use pip
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure API Keys

```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...
```

### Verify Installation

```python
from src.llm_evaluation import LLMClient, HallucinationDetector
from src.data_processing import SyntheticDataGenerator
from src.analysis import StatisticalTests, Visualization

print("All modules imported successfully!")
```

---

## 2. Data Exploration {#data-exploration}

### Load Synthetic Protein Data

```python
import pandas as pd

# Load pre-generated synthetic proteins
df = pd.read_csv('data/synthetic/example_proteins.csv')

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(df.head())
```

### Generate Custom Synthetic Data

```python
from src.data_processing import SyntheticDataGenerator

# Initialize generator
generator = SyntheticDataGenerator(seed=42)

# Generate 50 proteins with medium difficulty
df = generator.generate_protein_dataset(
    n_proteins=50,
    include_rare=True,
    difficulty='medium'
)

# Save for later use
df.to_csv('data/synthetic/custom_proteins.csv', index=False)
```

---

## 3. Running LLM Queries {#running-llm-queries}

### Single Query Example

```python
import asyncio
from src.llm_evaluation import LLMClient

async def query_example():
    # Initialize OpenAI client
    client = LLMClient(provider='openai', model='gpt-4')
    
    # Query about a protein
    response = await client.query(
        "What is the biological function of protein P53?",
        temperature=0.7,
        max_tokens=300
    )
    
    print(f"Response: {response.content}")
    print(f"Cost: ${response.cost_usd:.4f}")
    print(f"Tokens: {response.tokens_used}")
    
    # Check usage stats
    stats = client.get_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Total cost: ${stats['total_cost_usd']:.4f}")

# Run async function
asyncio.run(query_example())
```

### Compare Multiple Providers

```python
async def compare_providers():
    # Initialize clients for different providers
    providers = [
        ('openai', 'gpt-4'),
        ('anthropic', 'claude-3-opus-20240229'),
        ('google', 'gemini-pro')
    ]
    
    clients = {f"{p}/{m}": LLMClient(provider=p, model=m) 
               for p, m in providers}
    
    # Same query to all providers
    query = "What is hemoglobin and what is its function?"
    
    results = {}
    for name, client in clients.items():
        response = await client.query(query, temperature=0.7)
        results[name] = {
            'response': response.content[:200] + '...',  # First 200 chars
            'cost': response.cost_usd,
            'tokens': response.tokens_used
        }
    
    # Print comparison
    for name, data in results.items():
        print(f"\n{name}:")
        print(f"  Response: {data['response']}")
        print(f"  Cost: ${data['cost']:.4f}")
        print(f"  Tokens: {data['tokens']}")

asyncio.run(compare_providers())
```

---

## 4. Detecting Hallucinations {#detecting-hallucinations}

### Basic Hallucination Detection

```python
from src.llm_evaluation import HallucinationDetector

# Initialize detector
detector = HallucinationDetector()

# Test with an obvious hallucination
response = """
Protein FAKE123 is a novel kinase discovered in 2023. It has a molecular 
weight of 5000 kDa and is involved in cancer progression. The protein 
interacts with GO:9999999 and is located in the mitochondria.
"""

result = detector.detect(response)

print(f"Is hallucination: {result.is_hallucination}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Types: {[t.value for t in result.hallucination_types]}")
print(f"Evidence: {result.evidence}")
```

### Detect Hallucinations in LLM Response

```python
async def detect_in_llm_response():
    # Get LLM response
    client = LLMClient(provider='openai', model='gpt-4')
    response = await client.query(
        "Tell me about protein XYZ-9999 and its role in disease"
    )
    
    # Detect hallucinations
    detector = HallucinationDetector()
    result = detector.detect(response.content)
    
    print(f"LLM Response:\n{response.content}\n")
    print(f"Hallucination detected: {result.is_hallucination}")
    if result.is_hallucination:
        print(f"Types: {[t.value for t in result.hallucination_types]}")
        print(f"Evidence: {result.evidence}")

asyncio.run(detect_in_llm_response())
```

### Batch Detection

```python
# Multiple responses to check
responses = [
    "Hemoglobin is an oxygen-transport protein in red blood cells.",
    "Protein FAKE999 is involved in DNA repair.",
    "P53 is a tumor suppressor with GO:0004672 function."
]

detector = HallucinationDetector()
results = detector.detect_batch(responses)

for i, result in enumerate(results):
    print(f"\nResponse {i+1}:")
    print(f"  Hallucination: {result.is_hallucination}")
    print(f"  Confidence: {result.confidence:.2f}")

# Calculate overall statistics
stats = detector.calculate_hallucination_rate(results)
print(f"\nOverall hallucination rate: {stats['hallucination_rate']:.1%}")
```

---

## 5. Statistical Analysis {#statistical-analysis}

### Inter-Rater Reliability

```python
from src.analysis import StatisticalTests

# Simulate expert ratings (0 = no hallucination, 1 = hallucination)
expert1_ratings = [0, 0, 1, 0, 1, 1, 0, 1, 0, 0]
expert2_ratings = [0, 0, 1, 1, 1, 1, 0, 1, 0, 0]

# Calculate Cohen's kappa
kappa = StatisticalTests.cohens_kappa(expert1_ratings, expert2_ratings)
print(f"Cohen's kappa: {kappa:.3f}")

# Interpretation
if kappa > 0.75:
    print("Excellent agreement")
elif kappa > 0.60:
    print("Substantial agreement")
elif kappa > 0.40:
    print("Moderate agreement")
else:
    print("Fair to poor agreement")
```

### Compare Hallucination Rates

```python
import numpy as np
from scipy import stats

# Hallucination counts for different models
gpt4_hallucinations = 23  # out of 100
claude_hallucinations = 18
gemini_hallucinations = 31

total_queries = 100

# Chi-square test
observed = np.array([gpt4_hallucinations, claude_hallucinations, gemini_hallucinations])
expected = np.array([total_queries/3] * 3)

chi2, p_value = stats.chisquare(observed, expected)
print(f"Chi-square statistic: {chi2:.2f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("Significant difference between models (p < 0.05)")
else:
    print("No significant difference between models")
```

---

## 6. Visualization {#visualization}

### Plot Hallucination Rates

```python
from src.analysis import Visualization
import matplotlib.pyplot as plt

# Hallucination rates by model
rates = {
    'GPT-4': 0.234,
    'Claude 3 Opus': 0.187,
    'Claude 3 Sonnet': 0.212,
    'Gemini Pro': 0.315
}

# Generate plot
Visualization.plot_hallucination_rates(
    rates,
    output_path='results/figures/hallucination_comparison.pdf'
)
```

### Custom Visualization

```python
import seaborn as sns
import pandas as pd

# Create dataset
data = {
    'Model': ['GPT-4']*3 + ['Claude']*3 + ['Gemini']*3,
    'Category': ['Function', 'MS', 'Clinical']*3,
    'Rate': [0.18, 0.31, 0.25, 0.15, 0.25, 0.19, 0.29, 0.38, 0.33]
}
df = pd.DataFrame(data)

# Create grouped bar plot
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Category', y='Rate', hue='Model')
plt.title('Hallucination Rates by Task Category and Model')
plt.ylabel('Hallucination Rate')
plt.xlabel('Task Category')
plt.legend(title='Model', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('results/figures/category_comparison.pdf', dpi=300)
plt.show()
```

---

## 7. Full Benchmark {#full-benchmark}

### Run Complete Benchmark

```python
from src.llm_evaluation import BenchmarkSuite
import asyncio

async def run_full_benchmark():
    # Initialize benchmark suite
    suite = BenchmarkSuite(
        models=[
            ('openai', 'gpt-4'),
            ('anthropic', 'claude-3-opus-20240229'),
            ('google', 'gemini-pro')
        ],
        output_dir='results/benchmark',
        enable_hallucination_detection=True,
        max_concurrent=5
    )
    
    # Run benchmark (this will take a while!)
    print("Starting benchmark evaluation...")
    results = await suite.run()
    
    # Save results
    suite.save_results(results)
    
    # Generate report
    report = suite.generate_report(results, 'benchmark_report.md')
    print(report)
    
    # Analyze results
    analysis = suite.analyze_results(results)
    print(f"\nTotal cost: ${analysis['total_cost_usd']:.2f}")
    print(f"Total queries: {analysis['total_queries']}")
    
    for model, stats in analysis['per_model'].items():
        print(f"\n{model}:")
        print(f"  Hallucination rate: {stats['hallucination_rate']:.1%}")
        print(f"  Cost: ${stats['total_cost_usd']:.2f}")

# Run benchmark
asyncio.run(run_full_benchmark())
```

### Command Line Usage

```bash
# Run benchmark from command line
python -m src.llm_evaluation.benchmark_suite \
    --models openai/gpt-4 anthropic/claude-3-opus-20240229 \
    --output results/my_benchmark \
    --queries config/custom_queries.json

# View results
cat results/my_benchmark/benchmark_report.md
```

---

## Complete Example: End-to-End Workflow

```python
import asyncio
import pandas as pd
from src.llm_evaluation import LLMClient, HallucinationDetector
from src.data_processing import SyntheticDataGenerator
from src.analysis import StatisticalTests, Visualization

async def complete_workflow():
    """Complete end-to-end analysis workflow."""
    
    # 1. Generate synthetic data
    print("Step 1: Generating synthetic data...")
    generator = SyntheticDataGenerator(seed=42)
    proteins = generator.generate_protein_dataset(n_proteins=10)
    print(f"Generated {len(proteins)} proteins\n")
    
    # 2. Query LLMs
    print("Step 2: Querying LLMs...")
    client = LLMClient(provider='openai', model='gpt-4')
    
    results = []
    for _, protein in proteins.head(3).iterrows():  # Test with 3 proteins
        query = f"What is the function of protein {protein['protein_id']}?"
        response = await client.query(query)
        results.append({
            'protein_id': protein['protein_id'],
            'query': query,
            'response': response.content,
            'cost': response.cost_usd
        })
    
    print(f"Completed {len(results)} queries\n")
    
    # 3. Detect hallucinations
    print("Step 3: Detecting hallucinations...")
    detector = HallucinationDetector()
    
    for result in results:
        hall_result = detector.detect(result['response'])
        result['is_hallucination'] = hall_result.is_hallucination
        result['confidence'] = hall_result.confidence
    
    # 4. Analyze results
    print("Step 4: Analyzing results...")
    df = pd.DataFrame(results)
    hallucination_rate = df['is_hallucination'].mean()
    total_cost = df['cost'].sum()
    
    print(f"Hallucination rate: {hallucination_rate:.1%}")
    print(f"Total cost: ${total_cost:.4f}\n")
    
    # 5. Save results
    print("Step 5: Saving results...")
    df.to_csv('results/example_analysis.csv', index=False)
    print("Results saved to results/example_analysis.csv")
    
    return df

# Run complete workflow
df = asyncio.run(complete_workflow())
print("\nWorkflow complete!")
print(df[['protein_id', 'is_hallucination', 'confidence']])
```

---

## Next Steps

1. **Scale Up**: Run full benchmark with 1000+ queries
2. **Expert Evaluation**: Get clinical experts to validate results
3. **Statistical Analysis**: Perform comprehensive statistical tests
4. **Visualization**: Create publication-quality figures
5. **Manuscript**: Write up findings for journal submission

## Additional Resources

- [API Reference](api_reference.md)
- [FAQ](faq.md)
- [Contributing Guide](contributing_guide.md)
- [GitHub Repository](https://github.com/olaflaitinen/llm-proteomics-hallucination)

---

**Authors**: Olaf Yunus Laitinen Imanov, Derya Umut Kulali

**Last Updated**: January 2024
