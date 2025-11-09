"""
LLM Evaluation Module for Proteomics Hallucination Study.

This module provides infrastructure for evaluating large language models
on proteomics queries, including client interfaces, prompt management,
evaluation pipelines, and hallucination scoring.
"""

__version__ = "1.0.0"
__author__ = "Olaf Imanov Laitinen, Derya Umut Kulali"
__license__ = "CC-BY-4.0"

# Optional imports - may fail in test environments with missing dependencies
try:
    from .clients import GPT4Client, ClaudeClient, GeminiClient
except Exception:
    GPT4Client = ClaudeClient = GeminiClient = None

try:
    from .runner import EvaluationRunner
except Exception:
    EvaluationRunner = None

# The following imports are commented out until the modules are implemented:
# from .prompts import PromptTemplate, SystemPrompts
# from .hallucination_scorer import HallucinationScorer
# from .batch_processor import BatchProcessor

__all__ = [
    "GPT4Client",
    "ClaudeClient",
    "GeminiClient",
    "EvaluationRunner",
    # "PromptTemplate",
    # "SystemPrompts",
    # "HallucinationScorer",
    # "BatchProcessor",
]
