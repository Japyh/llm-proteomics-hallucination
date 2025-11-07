# Notebooks Directory

Jupyter notebooks for exploratory data analysis, LLM evaluation, and results generation.

## Notebook Workflow

Execute notebooks in the following order:

1. **00_setup_and_verification.ipynb** - Environment setup and verification
2. **01_data_exploration.ipynb** - Exploratory data analysis
3. **02_llm_benchmark.ipynb** - LLM testing and evaluation
4. **03_hallucination_analysis.ipynb** - Hallucination detection and analysis
5. **04_statistical_analysis.ipynb** - Statistical testing and significance
6. **05_results_visualization.ipynb** - Generate paper-ready figures

## Execution Environment

### Required Packages
All packages from `requirements.txt` should be installed:
```bash
pip install -r requirements.txt
```

### API Keys
Create `.env` file with API keys before running notebooks 02 and 03:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### GPU Support (Optional)
For faster LLM inference with local models:
```bash
# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"
```

## Notebook Descriptions

### 00_setup_and_verification.ipynb
**Purpose**: Verify environment setup and dependencies

**Contents**:
- Import all required libraries
- Check library versions
- Verify GPU availability (if applicable)
- Test database connections
- Load sample data
- Confirm API connectivity (without actual API calls)

**Expected Runtime**: < 2 minutes

**Outputs**: Environment report

---

### 01_data_exploration.ipynb
**Purpose**: Explore and understand the synthetic protein dataset

**Contents**:
- Load synthetic protein data
- Display dataset statistics
- Visualize protein distributions
- Analyze protein properties (molecular weight, sequence length, etc.)
- Check data quality (missing values, outliers)
- Generate summary statistics
- Export cleaned dataset

**Expected Runtime**: 5-10 minutes

**Outputs**:
- Summary statistics CSV
- Exploratory plots (PNG)
- Cleaned dataset

---

### 02_llm_benchmark.ipynb
**Purpose**: Test LLM performance on proteomics queries

**Contents**:
- Initialize LLM clients (OpenAI, Anthropic, Google)
- Load benchmark questions
- Query each LLM with standardized prompts
- Collect responses
- Track API costs and latencies
- Save results for analysis

**Expected Runtime**: 30-60 minutes (depends on number of queries)

**Outputs**:
- LLM responses JSON
- Performance metrics CSV
- Cost tracking report

**Requirements**:
- Valid API keys in `.env`
- Sufficient API credits

---

### 03_hallucination_analysis.ipynb
**Purpose**: Detect and categorize hallucinations in LLM responses

**Contents**:
- Load LLM responses from notebook 02
- Cross-reference with UniProt database
- Identify invented proteins
- Detect incorrect functions
- Flag inconsistent information
- Categorize hallucination types
- Calculate hallucination rates per model
- Generate hallucination examples

**Expected Runtime**: 20-40 minutes

**Outputs**:
- Hallucination detection results CSV
- Categorized errors JSON
- Example cases for paper

---

### 04_statistical_analysis.ipynb
**Purpose**: Perform statistical tests on results

**Contents**:
- Load hallucination rates and expert evaluations
- Calculate inter-rater reliability (Cohen's kappa, Fleiss' kappa)
- Compare models (chi-square, McNemar test)
- Significance testing (t-tests, ANOVA)
- Effect size calculations
- Multiple comparison corrections (Bonferroni, FDR)
- Power analysis
- Generate statistical tables

**Expected Runtime**: 10-20 minutes

**Outputs**:
- Statistical test results CSV
- Significance tables for manuscript
- Effect size calculations

---

### 05_results_visualization.ipynb
**Purpose**: Create publication-ready figures

**Contents**:
- Generate figure 1: Hallucination rates by model
- Generate figure 2: Error type distributions
- Generate figure 3: Clinical relevance scores
- Generate figure 4: Expert agreement heatmap
- Generate supplementary figures
- Create tables for manuscript
- Export in multiple formats (PNG, PDF, SVG)
- Apply journal formatting requirements

**Expected Runtime**: 15-25 minutes

**Outputs**:
- Figures for manuscript (PNG, PDF)
- LaTeX tables
- Supplementary figures

---

## Coding Conventions

### Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

### Structure
Each notebook should have:

1. **Title and Description** (Markdown cell)
2. **Imports** (Code cell)
3. **Configuration** (Code cell)
4. **Main Analysis** (Multiple cells)
5. **Results Summary** (Markdown cell)
6. **Next Steps** (Markdown cell)

### Example Structure
```python
# %% [markdown]
# # Notebook Title
# Description of notebook purpose

# %% [code]
# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% [code]
# Configuration
DATA_PATH = '../data/synthetic/'
RESULTS_PATH = '../results/'

# %% [code]
# Load data
df = pd.read_csv(f'{DATA_PATH}/example_proteins.csv')

# %% [code]
# Analysis
# ... analysis code ...

# %% [markdown]
# ## Results Summary
# Key findings from this notebook

# %% [markdown]
# ## Next Steps
# - Run next notebook
# - Additional analysis needed
```

## Best Practices

### Before Running
- [ ] Environment activated
- [ ] All dependencies installed
- [ ] API keys configured (for notebooks 02-03)
- [ ] Previous notebooks completed (if dependencies exist)

### During Execution
- Run cells in order (don't skip cells)
- Check for errors after each cell
- Save intermediate results
- Monitor API costs (for notebook 02)
- Document unexpected findings in markdown cells

### After Completion
- Clear cell outputs before committing (unless example outputs)
- Verify all output files created
- Check results make sense
- Document any issues encountered

## Output Management

### Where Outputs Go
- Figures: `../results/figures/`
- Tables: `../results/tables/`
- Intermediate data: `../data/processed/`
- Logs: `../results/logs/`

### File Naming Convention
```
{notebook_number}_{description}_{date}.{extension}

Examples:
- 01_protein_distribution_20240115.png
- 03_hallucination_results_20240115.csv
- 05_figure1_hallucination_rates_20240115.pdf
```

## Troubleshooting

### Common Issues

**Issue**: ModuleNotFoundError
**Solution**: Ensure all requirements installed: `pip install -r requirements.txt`

**Issue**: API authentication error
**Solution**: Check `.env` file has valid API keys

**Issue**: Memory error with large datasets
**Solution**: Process data in chunks or use Dask for large datasets

**Issue**: Plots not showing
**Solution**: Add `%matplotlib inline` at top of notebook

**Issue**: Kernel dies during execution
**Solution**: Reduce batch size or increase available memory

### Getting Help
- Check error messages carefully
- Review previous successful runs
- Consult package documentation
- Open GitHub issue if bug suspected

## Version Control

### What to Commit
- Notebook files (.ipynb)
- README updates
- Example outputs (small files only)

### What NOT to Commit
- Large output files (> 1MB)
- API responses with sensitive data
- Temporary files
- Cell execution outputs (clear before commit)

### Clearing Outputs
```bash
# Using jupyter nbconvert
jupyter nbconvert --clear-output --inplace *.ipynb

# Or in JupyterLab: Cell > All Output > Clear
```

## Reproducibility

### Random Seeds
Set random seeds for reproducibility:
```python
import random
import numpy as np
import torch

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)
```

### Environment Export
Document exact environment:
```bash
pip freeze > requirements_exact.txt
conda env export > environment_exact.yml
```

### Data Versioning
- Track dataset versions
- Include checksums
- Document any data modifications

## Performance Tips

### Speed Up Execution
1. Use vectorized operations (NumPy, Pandas)
2. Avoid loops when possible
3. Cache expensive computations
4. Use multiprocessing for parallel tasks
5. Profile code to find bottlenecks

### Memory Management
1. Delete large variables when done: `del large_df`
2. Use generators for large datasets
3. Process data in chunks
4. Monitor memory usage: `%memit` magic command

## Collaboration

### For Team Members
- Add markdown cells explaining your analysis
- Use descriptive variable names
- Comment non-obvious code
- Save intermediate checkpoints
- Communicate major changes

### Code Review
- Review notebook outputs before PR
- Check for hardcoded paths
- Verify reproducibility
- Ensure no sensitive data exposed

---

## Jupyter Tips

### Useful Magic Commands
```python
%time         # Time single statement
%timeit       # Time repeated execution
%memit        # Memory usage
%load_ext autoreload  # Auto-reload modules
%autoreload 2
%matplotlib inline    # Show plots inline
%config InlineBackend.figure_format = 'retina'  # High-res plots
```

### Keyboard Shortcuts
- `Shift + Enter`: Run cell
- `Ctrl + Enter`: Run cell without advancing
- `A`: Insert cell above
- `B`: Insert cell below
- `D + D`: Delete cell
- `M`: Change to markdown
- `Y`: Change to code
- `Ctrl + Shift + -`: Split cell

---

Last Updated: 2024-01-15
