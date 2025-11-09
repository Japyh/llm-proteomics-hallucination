"""Unified wrappers for different LLM APIs."""
from abc import ABC, abstractmethod

class LLMWrapper(ABC):
    """Base class for LLM API wrappers."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt."""
        pass
    
    @abstractmethod
    def get_embedding(self, text: str) -> list:
        """Get text embedding."""
        pass

class GPT4Wrapper(LLMWrapper):
    """Wrapper for GPT-4 API."""
    
    def __init__(self, api_key: str):
        import openai
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    def get_embedding(self, text: str) -> list:
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
