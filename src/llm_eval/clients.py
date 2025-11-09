"""
LLM API clients for GPT-4, Claude, and Gemini.

This module provides unified interfaces to different LLM APIs with
standardized parameters, error handling, and retry logic.
"""

import time
import logging
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import openai
import anthropic
import google.generativeai as genai


logger = logging.getLogger(__name__)


class BaseLLMClient(ABC):
    """Abstract base class for LLM API clients."""

    def __init__(
        self,
        api_key: str,
        temperature: float = 0.3,
        top_p: float = 0.9,
        max_tokens: int = 2048,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        """
        Initialize LLM client.

        Args:
            api_key: API key for the LLM service
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens in response
            max_retries: Maximum number of retry attempts
            retry_delay: Initial retry delay in seconds (exponential backoff)
        """
        self.api_key = api_key
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response from LLM.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            **kwargs: Additional model-specific parameters

        Returns:
            Dictionary containing response and metadata
        """
        pass

    def _retry_with_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry logic."""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed after {self.max_retries} attempts: {e}")
                    raise
                delay = self.retry_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                time.sleep(delay)


class GPT4Client(BaseLLMClient):
    """Client for OpenAI GPT-4 Turbo API."""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-2024-04-09", **kwargs):
        """Initialize GPT-4 client."""
        super().__init__(api_key, **kwargs)
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response from GPT-4."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        def _call_api():
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
                **kwargs
            )
            return response

        response = self._retry_with_backoff(_call_api)

        return {
            "response": response.choices[0].message.content,
            "model": self.model,
            "finish_reason": response.choices[0].finish_reason,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "metadata": {
                "id": response.id,
                "created": response.created,
                "model": response.model,
            }
        }


class ClaudeClient(BaseLLMClient):
    """Client for Anthropic Claude API."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-sonnet-20240229",
        **kwargs
    ):
        """Initialize Claude client."""
        super().__init__(api_key, **kwargs)
        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response from Claude."""
        def _call_api():
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                system=system_prompt if system_prompt else "",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response

        response = self._retry_with_backoff(_call_api)

        return {
            "response": response.content[0].text,
            "model": self.model,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            "metadata": {
                "id": response.id,
                "model": response.model,
                "role": response.role,
            }
        }


class GeminiClient(BaseLLMClient):
    """Client for Google Gemini API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-1.5-pro-001",
        **kwargs
    ):
        """Initialize Gemini client."""
        super().__init__(api_key, **kwargs)
        self.model = model
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response from Gemini."""
        # Combine system and user prompts for Gemini
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        generation_config = {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_output_tokens": self.max_tokens,
        }

        def _call_api():
            response = self.client.generate_content(
                full_prompt,
                generation_config=generation_config,
                **kwargs
            )
            return response

        response = self._retry_with_backoff(_call_api)

        return {
            "response": response.text,
            "model": self.model,
            "finish_reason": response.candidates[0].finish_reason if response.candidates else None,
            "usage": {
                "prompt_token_count": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
                "candidates_token_count": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None,
                "total_token_count": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None,
            },
            "metadata": {
                "model": self.model,
            }
        }


def create_client(model_name: str, api_key: str, **kwargs) -> BaseLLMClient:
    """
    Factory function to create appropriate LLM client.

    Args:
        model_name: Name of the model ("gpt4", "claude", "gemini")
        api_key: API key for the service
        **kwargs: Additional parameters for client initialization

    Returns:
        Initialized LLM client

    Raises:
        ValueError: If model_name is not recognized
    """
    clients = {
        "gpt4": GPT4Client,
        "claude": ClaudeClient,
        "gemini": GeminiClient,
    }

    model_name_lower = model_name.lower()
    if model_name_lower not in clients:
        raise ValueError(
            f"Unknown model: {model_name}. "
            f"Choose from: {', '.join(clients.keys())}"
        )

    return clients[model_name_lower](api_key=api_key, **kwargs)
