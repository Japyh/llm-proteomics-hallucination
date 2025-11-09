# Installation Guide

Complete installation instructions for the LLM Proteomics Hallucination Study.

---

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Detailed Installation](#detailed-installation)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Advanced Options](#advanced-options)

---

## System Requirements

### Minimum Requirements

- **OS**: Linux, macOS, or Windows 10/11
- **Python**: 3.11 or higher
- **RAM**: 8 GB
- **Disk Space**: 5 GB free space
- **Internet**: Required for API calls and package installation

### Recommended Requirements

- **OS**: Ubuntu 22.04 LTS or macOS 13+
- **Python**: 3.11.5
- **RAM**: 16 GB
- **Disk Space**: 20 GB free space
- **CPU**: 4+ cores
- **GPU**: Not required (but helpful for local models)

### Software Dependencies

- Git 2.30+
- Conda or virtualenv
- LaTeX distribution (for manuscript compilation)

---

## Quick Start

For experienced users:

```bash
# Clone repository
git clone https://github.com/olaflaitinen/llm-proteomics-hallucination.git
cd llm-proteomics-hallucination

# Create environment (choose one)
conda env create -f environment.yml && conda activate llm-proteomics
# OR
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Verify installation
python -c "import src; print('Installation successful')"
pytest tests/test_llm_client.py -v
```

---

## Detailed Installation

### Step 1: Install System Prerequisites

#### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev

# Install Git
sudo apt install git

# Install LaTeX (for manuscript compilation)
sudo apt install texlive-full

# Install build tools
sudo apt install build-essential
```

#### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Install Git
brew install git

# Install LaTeX
brew install --cask mactex

# Install build tools (Xcode Command Line Tools)
xcode-select --install
```

#### Windows

1. **Install Python 3.11**:
   - Download from https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

2. **Install Git**:
   - Download from https://git-scm.com/download/win
   - Use default settings

3. **Install LaTeX**:
   - Download MiKTeX from https://miktex.org/download
   - Use default settings

---

### Step 2: Clone Repository

```bash
# Clone the repository
git clone https://github.com/olaflaitinen/llm-proteomics-hallucination.git

# Navigate to directory
cd llm-proteomics-hallucination

# Verify repository
ls -la
```

---

### Step 3: Create Python Environment

#### Option A: Conda (Recommended)

```bash
# Install Miniconda (if not installed)
# Linux/macOS:
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Create environment from file
conda env create -f environment.yml

# Activate environment
conda activate llm-proteomics

# Verify environment
conda list
```

#### Option B: venv (Alternative)

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

---

### Step 4: Install Package Dependencies

#### Production Dependencies

```bash
# Install main requirements
pip install -r requirements.txt
```

**Core packages**:
- `numpy>=1.24.0` - Numerical computing
- `pandas>=2.0.0` - Data manipulation
- `matplotlib>=3.8.0` - Visualization
- `scipy>=1.11.0` - Scientific computing
- `scikit-learn>=1.3.0` - Machine learning
- `openai>=1.0.0` - OpenAI API client
- `anthropic>=0.7.0` - Anthropic API client
- `google-generativeai>=0.3.0` - Google API client

#### Development Dependencies

```bash
# Install development requirements
pip install -r requirements-dev.txt
```

**Development packages**:
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `black>=23.0.0` - Code formatting
- `isort>=5.12.0` - Import sorting
- `flake8>=6.0.0` - Linting
- `mypy>=1.5.0` - Type checking
- `pre-commit>=3.3.0` - Git hooks

---

### Step 5: Configure API Keys

#### Create .env File

```bash
# Copy example file
cp .env.example .env

# Edit with your API keys
nano .env  # or use your preferred editor
```

#### Add API Keys

```bash
# .env file content
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here

# Optional: Logging level
LOG_LEVEL=INFO
```

**Security Note**: Never commit .env file to version control.

#### Obtain API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google**: https://makersuite.google.com/app/apikey

---

### Step 6: Install Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

---

## Verification

### Verify Python Installation

```bash
# Check Python version
python --version
# Should show: Python 3.11.x

# Check pip version
pip --version

# Check environment
which python
# Should point to your virtual environment
```

### Verify Package Installation

```bash
# Import main modules
python -c "import src; print('Success')"

# Check specific modules
python -c "from src.llm_evaluation import LLMClient; print('LLM module OK')"
python -c "from src.analysis import metrics; print('Analysis module OK')"
python -c "from src.data_processing import protein_database; print('Data module OK')"
```

### Run Basic Tests

```bash
# Run quick tests
pytest tests/test_llm_client.py -v

# Run all tests (skip slow tests)
pytest -m "not slow" -v

# Check test coverage
pytest --cov=src --cov-report=term-missing
```

### Verify Data Files

```bash
# Check data directory
ls data/

# Verify query file
python -c "import json; data = json.load(open('data/queries/queries_all.json')); print(f'Loaded {len(data)} queries')"

# Verify FASTA files
ls data/proteins/*.fasta
```

---

## Troubleshooting

### Common Issues

#### Issue: Python version mismatch

```bash
# Error: Python 3.11 required
# Solution: Install correct version
conda install python=3.11
# OR
pyenv install 3.11.5
pyenv global 3.11.5
```

#### Issue: Package installation fails

```bash
# Error: Cannot install requirements
# Solution: Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Then retry
pip install -r requirements.txt
```

#### Issue: API keys not found

```bash
# Error: API key not set
# Solution: Check .env file
cat .env | grep API_KEY

# Ensure file is in correct location
ls -la .env
```

#### Issue: Import errors

```bash
# Error: ModuleNotFoundError
# Solution: Install package in development mode
pip install -e .

# OR ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

#### Issue: LaTeX not found

```bash
# Error: pdflatex not found
# Solution: Install LaTeX
# Ubuntu:
sudo apt install texlive-full
# macOS:
brew install --cask mactex
# Windows: Install MiKTeX
```

#### Issue: Test failures

```bash
# Error: Tests failing
# Solution: Check environment
pytest -v --tb=long

# Skip API tests
pytest -m "not api" -v

# Check specific test
pytest tests/test_llm_client.py::test_specific_function -vv
```

---

## Advanced Options

### Docker Installation

```bash
# Build Docker image
docker build -t llm-proteomics .

# Run container
docker run -it --rm \
  -v $(pwd):/workspace \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  llm-proteomics

# Using docker-compose
docker-compose up -d
```

### GPU Support

```bash
# Install CUDA (if available)
# Check GPU
nvidia-smi

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU
python -c "import torch; print(torch.cuda.is_available())"
```

### Development Installation

```bash
# Install in editable mode
pip install -e .

# Install all development tools
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run code formatters
black src/ tests/
isort src/ tests/
```

### Jupyter Notebook Setup

```bash
# Install Jupyter
pip install jupyter jupyterlab

# Register kernel
python -m ipykernel install --user --name=llm-proteomics

# Start Jupyter
jupyter lab

# Or open specific notebook
jupyter notebook notebooks/01_data_exploration.ipynb
```

---

## Environment Variables

### Available Configuration

```bash
# API Keys
OPENAI_API_KEY=xxx
ANTHROPIC_API_KEY=xxx
GOOGLE_API_KEY=xxx

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Data paths
DATA_DIR=./data
RESULTS_DIR=./data/results

# API settings
OPENAI_MODEL=gpt-4-0125-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229
GOOGLE_MODEL=gemini-1.5-pro-001

# Rate limiting
MAX_REQUESTS_PER_MINUTE=60
```

---

## Platform-Specific Notes

### Linux

- Use system package manager for dependencies
- Virtual environments recommended
- Check permissions for data directories

### macOS

- Xcode Command Line Tools required
- Use Homebrew for package management
- May need to configure certificates for API calls

### Windows

- Use PowerShell or Git Bash
- Path separators: Use / or \\
- Some scripts may need WSL (Windows Subsystem for Linux)

---

## Next Steps

After successful installation:

1. **Explore Data**: `cd data && cat README.md`
2. **Run Notebooks**: `jupyter lab`
3. **Generate Figures**: `cd paper/figures && python generate_figure_1.py`
4. **Run Analysis**: `pytest tests/`
5. **Read Documentation**: See [USAGE.md](USAGE.md)

---

## Support

If you encounter issues:

1. **Check FAQ**: See [FAQ.md](FAQ.md)
2. **Search Issues**: https://github.com/olaflaitinen/llm-proteomics-hallucination/issues
3. **Open Issue**: Provide detailed error information
4. **Contact**: olyulaim@dtu.dk

---

**Last Updated**: November 9, 2024
**Tested On**: Ubuntu 22.04, macOS 13, Windows 11
**Python Version**: 3.11.5
