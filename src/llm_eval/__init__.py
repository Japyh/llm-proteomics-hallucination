"""
LLM Evaluation Module for Proteomics Hallucination Study.

This module provides infrastructure for evaluating large language models
on proteomics queries, including client interfaces, prompt management,
evaluation pipelines, and hallucination scoring.
"""

__version__ = "1.0.0"
__author__ = "Olaf Imanov Laitinen, Derya Umut Kulali"
__license__ = "CC-BY-4.0"

from .clients import GPT4Client, ClaudeClient, GeminiClient
from .prompts import PromptTemplate, SystemPrompts
from .runner import EvaluationRunner
from .hallucination_scorer import HallucinationScorer
from .batch_processor import BatchProcessor

__all__ = [
    "GPT4Client",
    "ClaudeClient",
    "GeminiClient",
    "PromptTemplate",
    "SystemPrompts",
    "EvaluationRunner",
    "HallucinationScorer",
    "BatchProcessor",
]
