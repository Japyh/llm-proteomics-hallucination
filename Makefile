.PHONY: help setup test lint format clean data paper all

help:
	@echo "LLM Proteomics Hallucination Study - Make commands"
	@echo ""
	@echo "  make setup      - Setup environment"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make data       - Generate data"
	@echo "  make paper      - Compile manuscript"
	@echo "  make all        - Run complete pipeline"

setup:
	conda env create -f environment.yml
	conda activate llm-proteomics
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .coverage htmlcov

data:
	python data/generators/generate_query_dataset.py
	python data/generators/generate_protein_sequences.py
	python data/generators/generate_ms_spectra.py

paper:
	cd paper && \
	python figures/generate_figure_1.py && \
	python figures/generate_figure_2.py && \
	python figures/generate_figure_3.py && \
	python figures/generate_figure_4.py && \
	pdflatex manuscript.tex && \
	bibtex manuscript && \
	pdflatex manuscript.tex && \
	pdflatex manuscript.tex

all: data test paper
