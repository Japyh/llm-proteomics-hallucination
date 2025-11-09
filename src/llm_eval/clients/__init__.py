"""LLM API clients for the evaluation framework."""

# Optional imports - clients may have missing dependencies in test environments
try:
    from .openai_client import OpenAIClient
except Exception:
    OpenAIClient = None

try:
    from .anthropic_client import AnthropicClient
except Exception:
    AnthropicClient = None

try:
    from .gemini_client import GeminiClient
except Exception:
    GeminiClient = None

try:
    from .mistral_client import MistralClient
except Exception:
    MistralClient = None

try:
    from .local_vllm_client import LocalVLLMClient
except Exception:
    LocalVLLMClient = None

# Provide alias names for backward compatibility and clarity
GPT4Client = OpenAIClient
ClaudeClient = AnthropicClient

__all__ = [
    "OpenAIClient",
    "AnthropicClient",
    "GeminiClient",
    "MistralClient",
    "LocalVLLMClient",
    "GPT4Client",
    "ClaudeClient",
]
