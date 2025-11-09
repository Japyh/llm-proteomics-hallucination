# Jupyter Notebooks

Analysis notebooks for the LLM proteomics hallucination study.

---

## Notebook Workflow

Execute notebooks in the following order:

1. **00_setup_and_verification.ipynb** - Environment setup and verification
2. **01_data_exploration.ipynb** - Query dataset exploratory analysis
3. **02_llm_benchmark.ipynb** - LLM query execution (GPT-4, Claude, Gemini)
4. **03_hallucination_analysis.ipynb** - Hallucination detection and classification
5. **04_statistical_analysis.ipynb** - Statistical testing and regression analysis
6. **05_results_visualization.ipynb** - Generate manuscript figures and tables

---

## Environment Setup

### Install Dependencies

```bash
# Activate environment
conda activate llm-proteomics

# Install all requirements
pip install -r requirements.txt
```

### Configure API Keys

Create `.env` file with API keys for notebooks 02-03:

```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

---

## Notebook Descriptions

### 00_setup_and_verification.ipynb

**Purpose**: Verify environment and dependencies

**Key Tasks**:
- Check library versions
- Test database connections
- Verify data file integrity
- Confirm API connectivity

**Runtime**: < 2 minutes
**Outputs**: Environment report

---

### 01_data_exploration.ipynb

**Purpose**: Explore query dataset and proteomics data

**Key Tasks**:
- Load 500 queries from `data/queries/queries_all.json`
- Analyze stratification (complexity, prevalence)
- Visualize protein properties
- Generate summary statistics

**Runtime**: 5-10 minutes
**Outputs**:
- Summary statistics CSV
- Exploratory plots (PNG)

---

### 02_llm_benchmark.ipynb

**Purpose**: Query LLMs and collect responses

**Key Tasks**:
- Initialize LLM clients (OpenAI, Anthropic, Google)
- Execute 500 queries per model (1,500 total)
- Track API costs and latencies
- Save responses to `data/llm_responses/`

**Runtime**: 30-60 minutes (API-dependent)
**Outputs**:
- LLM responses JSON (gpt4_responses.json, claude_responses.json, gemini_responses.json)
- Performance metrics CSV
- Cost tracking report

**Requirements**: Valid API keys, sufficient API credits

---

### 03_hallucination_analysis.ipynb

**Purpose**: Detect and classify hallucinations

**Key Tasks**:
- Load LLM responses
- Cross-reference with ground truth (UniProt, HPA, PeptideAtlas)
- Classify hallucinations (4-level severity scale)
- Calculate hallucination rates per model
- Identify hallucination patterns

**Runtime**: 20-40 minutes
**Outputs**:
- `data/results/hallucination_rates.csv`
- `data/results/severity_classifications.csv`
- Example hallucinations for manuscript

---

### 04_statistical_analysis.ipynb

**Purpose**: Perform statistical tests

**Key Tasks**:
- Calculate inter-rater reliability (Cohen's kappa = 0.87)
- Compare models (chi-square tests, Bonferroni correction)
- Multivariable logistic regression (risk factors)
- Effect size calculations
- Generate statistical tables for manuscript

**Runtime**: 10-20 minutes
**Outputs**:
- `data/results/statistical_analysis.csv`
- `data/results/model_comparison.csv`
- Tables 1-4 for manuscript

---

### 05_results_visualization.ipynb

**Purpose**: Create publication-ready figures

**Key Tasks**:
- Generate Figure 1: Hallucination rates by complexity/prevalence
- Generate Figure 2: Severity heatmap by model/domain
- Generate Figure 3: Response consistency analysis
- Generate Figure 4: Calibration plot
- Export at 300 DPI (PNG format)

**Runtime**: 15-25 minutes
**Outputs**:
- Figures 1-4 for manuscript (300 DPI PNG)
- LaTeX-formatted tables

---

## Coding Standards

### Structure

Each notebook follows this structure:

1. **Title and Description** (Markdown)
2. **Imports** (Code)
3. **Configuration** (Code)
4. **Main Analysis** (Code cells)
5. **Results Summary** (Markdown)

### Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions
- Comment complex logic

### Example

```python
# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration
DATA_PATH = '../data/queries/'
RESULTS_PATH = '../data/results/'

# Load data
queries = pd.read_json(f'{DATA_PATH}/queries_all.json')

# Analysis
complexity_dist = queries['complexity'].value_counts()
print(complexity_dist)
```

---

## Best Practices

### Before Running

- Activate conda environment
- Install all dependencies
- Configure API keys (for notebooks 02-03)
- Ensure previous notebooks completed (if dependencies exist)

### During Execution

- Run cells in sequential order
- Check for errors after each cell
- Save intermediate results
- Monitor API costs (notebook 02)

### After Completion

- Clear cell outputs before committing
- Verify all output files created
- Document any issues encountered

---

## Output Management

### Output Directories

- Figures: `../data/results/figures/`
- Tables: `../data/results/tables/`
- Processed data: `../data/processed/`

### File Naming Convention

```
{notebook_number}_{description}_{date}.{extension}

Examples:
- 01_protein_distribution_20240315.png
- 03_hallucination_results_20240315.csv
- 05_figure1_hallucination_rates_20240315.png
```

---

## Reproducibility

### Random Seeds

Set random seeds for reproducibility:

```python
import random
import numpy as np

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
```

### Environment Documentation

```bash
# Export exact environment
pip freeze > requirements_exact.txt
conda env export > environment_exact.yml
```

---

## Troubleshooting

### Common Issues

**ModuleNotFoundError**:
```bash
pip install -r requirements.txt
```

**API Authentication Error**:
- Check `.env` file has valid API keys
- Verify API quotas not exceeded

**Memory Error**:
- Process data in chunks
- Increase available memory
- Close other applications

**Kernel Crash**:
- Reduce batch size
- Check memory usage
- Restart kernel

---

## Jupyter Tips

### Useful Magic Commands

```python
%time         # Time single statement
%timeit       # Time repeated execution
%load_ext autoreload
%autoreload 2  # Auto-reload modules
%matplotlib inline    # Show plots inline
```

### Keyboard Shortcuts

- `Shift + Enter`: Run cell and advance
- `Ctrl + Enter`: Run cell without advancing
- `A`: Insert cell above
- `B`: Insert cell below
- `D + D`: Delete cell
- `M`: Change to markdown
- `Y`: Change to code

---

## Version Control

### What to Commit

- Notebook files (.ipynb)
- README updates
- Small example outputs only

### What NOT to Commit

- Large output files (> 1MB)
- API responses with sensitive data
- Cell execution outputs (clear before commit)

### Clear Outputs

```bash
# Clear all notebook outputs
jupyter nbconvert --clear-output --inplace *.ipynb
```

---

**Last Updated**: November 9, 2024
**Status**: Ready for analysis
