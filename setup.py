"""Setup configuration for llm-proteomics-hallucination package."""
from pathlib import Path

from setuptools import find_packages, setup

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    with open(readme_file, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]
else:
    requirements = []

setup(
    name="llm-proteomics-hallucination",
    version="0.1.0",
    author="Olaf Yunus Laitinen Imanov, Derya Umut Kulali",
    author_email="olyulaim@dtu.dk",
    description="Research framework for evaluating LLM hallucination risks in clinical proteomics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olaflaitinen/llm-proteomics-hallucination",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "llm-benchmark=src.llm_evaluation.benchmark_suite:main",
        ],
    },
)
