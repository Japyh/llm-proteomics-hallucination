# Troubleshooting Guide

Solutions to common problems.

---

## Installation Issues

### Python Version Error

**Problem**: "Python 3.11 required"

**Solution**:
```bash
# Check version
python --version

# Install correct version
conda install python=3.11
# or
pyenv install 3.11.5
```

### Package Installation Fails

**Problem**: Cannot install requirements

**Solution**:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Permission Denied

**Problem**: Cannot write to directory

**Solution**:
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Import Errors

### ModuleNotFoundError

**Problem**: Module not found

**Solution**:
```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Or install in development mode
pip install -e .
```

### Import from src fails

**Problem**: Cannot import from src

**Solution**:
```bash
# Check __init__.py exists
ls src/__init__.py

# Install package
pip install -e .
```

---

## API Issues

### API Key Not Found

**Problem**: API key missing

**Solution**:
```bash
# Check .env file
cat .env | grep API_KEY

# Ensure file exists
cp .env.example .env
nano .env  # Add your keys
```

### Rate Limit Exceeded

**Problem**: Too many API requests

**Solution**:
```python
import time

for query in queries:
    response = client.query(query)
    time.sleep(1)  # Rate limiting
```

### API Authentication Failed

**Problem**: Invalid API key

**Solution**:
```bash
# Verify key is correct
echo $OPENAI_API_KEY | head -c 10

# Test API connection
python -c "import openai; openai.api_key='your_key'; print('OK')"
```

---

## Test Failures

### All Tests Fail

**Problem**: pytest not finding tests

**Solution**:
```bash
# Check pytest installation
pytest --version

# Run from project root
cd /path/to/llm-proteomics-hallucination
pytest
```

### Specific Test Fails

**Problem**: One test failing

**Solution**:
```bash
# Run with verbose output
pytest tests/test_file.py -vv --tb=long

# Run specific test
pytest tests/test_file.py::test_function -vv
```

### Import errors in tests

**Problem**: Tests cannot import modules

**Solution**:
```bash
# Install package in editable mode
pip install -e .

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

---

## Data Issues

### File Not Found

**Problem**: Cannot load data file

**Solution**:
```bash
# Check file exists
ls data/queries/queries_all.json

# Check from correct directory
pwd  # Should be project root
```

### JSON Parse Error

**Problem**: Cannot parse JSON

**Solution**:
```python
import json

try:
    with open('file.json') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error at line {e.lineno}: {e.msg}")
```

---

## Notebook Issues

### Kernel Dies

**Problem**: Jupyter kernel crashes

**Solution**:
```bash
# Increase memory limit
# Reduce batch size in code
# Close other applications
```

### Cannot Connect to Kernel

**Problem**: Kernel won't start

**Solution**:
```bash
# Reinstall kernel
python -m ipykernel install --user --name=llm-proteomics

# Restart Jupyter
jupyter lab --no-browser
```

---

## Performance Issues

### Slow Execution

**Problem**: Code runs slowly

**Solution**:
- Use vectorized operations (NumPy/Pandas)
- Reduce data size for testing
- Use multiprocessing for parallel tasks
- Profile code to find bottlenecks

### Memory Errors

**Problem**: Out of memory

**Solution**:
```python
# Process in chunks
for chunk in pd.read_csv('large_file.csv', chunksize=1000):
    process(chunk)

# Or use Dask for large datasets
import dask.dataframe as dd
df = dd.read_csv('large_file.csv')
```

---

## LaTeX/Manuscript Issues

### pdflatex Not Found

**Problem**: LaTeX not installed

**Solution**:
```bash
# Ubuntu
sudo apt install texlive-full

# macOS
brew install --cask mactex

# Windows: Install MiKTeX
```

### Compilation Errors

**Problem**: LaTeX compilation fails

**Solution**:
```bash
# Check error message
pdflatex manuscript.tex | grep Error

# Clean auxiliary files
rm *.aux *.log *.out

# Recompile
pdflatex manuscript.tex
```

---

## Git Issues

### Cannot Push

**Problem**: Push rejected

**Solution**:
```bash
# Pull first
git pull --rebase origin main

# Then push
git push origin main
```

### Merge Conflicts

**Problem**: Merge conflicts

**Solution**:
```bash
# Check conflicts
git status

# Resolve manually, then
git add .
git commit -m "Resolve conflicts"
```

---

## Docker Issues

### Build Fails

**Problem**: Docker build fails

**Solution**:
```bash
# Clean build
docker build --no-cache -t llm-proteomics .

# Check Dockerfile syntax
docker build -t llm-proteomics .
```

### Container Won't Start

**Problem**: Container exits immediately

**Solution**:
```bash
# Check logs
docker logs container_id

# Run interactively
docker run -it llm-proteomics bash
```

---

## Still Having Issues?

1. **Check FAQ**: [FAQ.md](FAQ.md)
2. **Search Issues**: https://github.com/olaflaitinen/llm-proteomics-hallucination/issues
3. **Open Issue**: Provide detailed error information
4. **Contact**: olyulaim@dtu.dk

**Last Updated**: November 9, 2024
