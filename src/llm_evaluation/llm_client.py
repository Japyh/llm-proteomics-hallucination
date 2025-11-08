"""
LLM Client for interacting with multiple LLM providers.

Supports OpenAI, Anthropic, and Google AI APIs with unified interface,
rate limiting, retries, and cost tracking.
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# API clients
try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


@dataclass
class LLMResponse:
    """Container for LLM response with metadata."""

    content: str
    provider: str
    model: str
    tokens_used: int
    cost_usd: float
    latency_seconds: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class LLMClient:
    """
    Unified client for interacting with multiple LLM providers.

    Features:
        - Support for OpenAI, Anthropic, and Google APIs
        - Exponential backoff retry logic
        - Rate limiting per API
        - Token counting and cost estimation
        - Response caching
        - Comprehensive error handling
        - Async support

    Args:
        provider: LLM provider to use ('openai', 'anthropic', or 'google')
        model: Specific model name (e.g., 'gpt-4', 'claude-3-opus')
        api_key: API key (if None, loaded from environment)
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens in response
        enable_cache: Whether to cache responses

    Example:
        >>> client = LLMClient(provider='openai', model='gpt-4')
        >>> response = await client.query("What is hemoglobin?")
        >>> print(response.content)
    """

    # Pricing per 1000 tokens (input, output) - update as needed
    PRICING = {
        "gpt-4": (0.03, 0.06),
        "gpt-4-turbo": (0.01, 0.03),
        "gpt-3.5-turbo": (0.0005, 0.0015),
        "claude-3-opus": (0.015, 0.075),
        "claude-3-sonnet": (0.003, 0.015),
        "claude-3-haiku": (0.00025, 0.00125),
        "gemini-pro": (0.00025, 0.0005),
        "gemini-1.5-pro": (0.0035, 0.0105),
    }

    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        enable_cache: bool = True,
        max_retries: int = 3,
    ):
        """Initialize LLM client."""
        self.provider = LLMProvider(provider)
        self.model = model or self._get_default_model()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.enable_cache = enable_cache
        self.max_retries = max_retries

        # Initialize API client
        self.api_key = api_key or self._load_api_key()
        self.client = self._initialize_client()

        # Cache for responses
        self._cache: Dict[str, LLMResponse] = {}

        # Stats tracking
        self.total_requests = 0
        self.total_tokens = 0
        self.total_cost = 0.0

        logger.info(
            f"Initialized {self.provider.value} client with model {self.model}"
        )

    def _get_default_model(self) -> str:
        """Get default model for provider."""
        defaults = {
            LLMProvider.OPENAI: "gpt-4",
            LLMProvider.ANTHROPIC: "claude-3-sonnet-20240229",
            LLMProvider.GOOGLE: "gemini-pro",
        }
        return defaults[self.provider]

    def _load_api_key(self) -> str:
        """Load API key from environment."""
        env_vars = {
            LLMProvider.OPENAI: "OPENAI_API_KEY",
            LLMProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
            LLMProvider.GOOGLE: "GOOGLE_API_KEY",
        }

        key = os.getenv(env_vars[self.provider])
        if not key:
            raise ValueError(
                f"API key not found. Set {env_vars[self.provider]} "
                "environment variable."
            )
        return key

    def _initialize_client(self) -> Any:
        """Initialize the appropriate API client."""
        if self.provider == LLMProvider.OPENAI:
            if openai is None:
                raise ImportError("openai package not installed")
            return openai.OpenAI(api_key=self.api_key)

        elif self.provider == LLMProvider.ANTHROPIC:
            if anthropic is None:
                raise ImportError("anthropic package not installed")
            return anthropic.Anthropic(api_key=self.api_key)

        elif self.provider == LLMProvider.GOOGLE:
            if genai is None:
                raise ImportError("google-generativeai package not installed")
            genai.configure(api_key=self.api_key)
            return genai.GenerativeModel(self.model)

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _get_cache_key(self, prompt: str) -> str:
        """Generate cache key for prompt."""
        import hashlib

        key_str = (
            f"{self.provider.value}:{self.model}:{prompt}:{self.temperature}"
        )
        return hashlib.md5(key_str.encode()).hexdigest()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
    )
    async def query(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """
        Query the LLM with a prompt.

        Args:
            prompt: User prompt/question
            temperature: Override default temperature
            max_tokens: Override default max tokens
            system_prompt: System prompt (if supported)

        Returns:
            LLMResponse object with content and metadata

        Raises:
            Exception: If API call fails after retries
        """
        # Check cache
        cache_key = self._get_cache_key(prompt)
        if self.enable_cache and cache_key in self._cache:
            logger.debug("Returning cached response")
            return self._cache[cache_key]

        # Use provided or default values
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens

        # Track timing
        start_time = time.time()

        try:
            # Call appropriate provider
            if self.provider == LLMProvider.OPENAI:
                response = await self._query_openai(
                    prompt, temp, max_tok, system_prompt
                )
            elif self.provider == LLMProvider.ANTHROPIC:
                response = await self._query_anthropic(
                    prompt, temp, max_tok, system_prompt
                )
            elif self.provider == LLMProvider.GOOGLE:
                response = await self._query_google(prompt, temp, max_tok)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

            # Calculate latency
            latency = time.time() - start_time

            # Update stats
            self.total_requests += 1
            self.total_tokens += response.tokens_used
            self.total_cost += response.cost_usd

            # Cache response
            if self.enable_cache:
                self._cache[cache_key] = response

            logger.info(
                f"Query completed: {response.tokens_used} tokens, "
                f"${response.cost_usd:.4f}, {latency:.2f}s"
            )

            return response

        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            raise

    async def _query_openai(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str],
    ) -> LLMResponse:
        """Query OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        cost = self.calculate_cost(
            response.usage.prompt_tokens, response.usage.completion_tokens
        )

        return LLMResponse(
            content=content,
            provider=self.provider.value,
            model=self.model,
            tokens_used=tokens,
            cost_usd=cost,
            latency_seconds=0,  # Will be set by caller
            metadata={
                "finish_reason": response.choices[0].finish_reason,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
            },
        )

    async def _query_anthropic(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str],
    ) -> LLMResponse:
        """Query Anthropic API."""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)

        content = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        cost = self.calculate_cost(
            response.usage.input_tokens, response.usage.output_tokens
        )

        return LLMResponse(
            content=content,
            provider=self.provider.value,
            model=self.model,
            tokens_used=tokens,
            cost_usd=cost,
            latency_seconds=0,
            metadata={
                "stop_reason": response.stop_reason,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
        )

    async def _query_google(
        self, prompt: str, temperature: float, max_tokens: int
    ) -> LLMResponse:
        """Query Google API."""
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        response = self.client.generate_content(
            prompt, generation_config=generation_config
        )

        content = response.text
        # Google doesn't provide token counts directly, estimate
        tokens = len(prompt.split()) + len(content.split())
        cost = self.calculate_cost(len(prompt.split()), len(content.split()))

        return LLMResponse(
            content=content,
            provider=self.provider.value,
            model=self.model,
            tokens_used=tokens,
            cost_usd=cost,
            latency_seconds=0,
            metadata={
                "finish_reason": "stop",
            },
        )

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate API cost for token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        if self.model in self.PRICING:
            input_price, output_price = self.PRICING[self.model]
            cost = (input_tokens / 1000 * input_price) + (
                output_tokens / 1000 * output_price
            )
            return cost
        else:
            logger.warning(f"Pricing not available for model {self.model}")
            return 0.0

    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics.

        Returns:
            Dictionary with usage stats
        """
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "total_cost_usd": self.total_cost,
            "average_tokens_per_request": (
                self.total_tokens / self.total_requests
                if self.total_requests > 0
                else 0
            ),
            "cache_size": len(self._cache),
        }

    def clear_cache(self):
        """Clear response cache."""
        self._cache.clear()
        logger.info("Cache cleared")


# Synchronous wrapper for convenience
class SyncLLMClient:
    """Synchronous wrapper for LLMClient."""

    def __init__(self, *args, **kwargs):
        """Initialize with same args as LLMClient."""
        self.async_client = LLMClient(*args, **kwargs)

    def query(self, *args, **kwargs) -> LLMResponse:
        """Synchronous query method."""
        return asyncio.run(self.async_client.query(*args, **kwargs))

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self.async_client.get_stats()

    def clear_cache(self):
        """Clear response cache."""
        self.async_client.clear_cache()
