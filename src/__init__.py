"""
LLM Proteomics Hallucination Research Package

A comprehensive framework for evaluating hallucination risks when using Large Language
Models to interpret clinical proteomics and mass spectrometry data.

Authors:
    Olaf Yunus Laitinen Imanov (olyulaim@dtu.dk)
    Technical University of Denmark

    Derya Umut Kulali (d_u_k@ogr.eskisehir.edu.tr)
    Eskisehir Technical University

Modules:
    data_processing: Data parsing, generation, and anonymization
    llm_evaluation: LLM client and evaluation tools
    analysis: Statistical analysis and visualization
    utils: Utility functions and helpers

Example:
    >>> from src.llm_evaluation import LLMClient, HallucinationDetector
    >>> client = LLMClient(provider='openai', model='gpt-4')
    >>> detector = HallucinationDetector()
"""

__version__ = "0.1.0"
__author__ = "Olaf Yunus Laitinen Imanov, Derya Umut Kulali"
__email__ = "olyulaim@dtu.dk"
__license__ = "MIT"
__copyright__ = "Copyright 2024, Technical University of Denmark & Eskisehir Technical University"

# Package metadata
__all__ = ['__version__', '__author__', '__email__']
