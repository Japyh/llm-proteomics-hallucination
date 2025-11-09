"""Mistral AI API client."""
from mistralai.client import MistralClient as MistralAPI

class MistralClient:
    def __init__(self, api_key: str, model: str = "mistral-large-2407"):
        self.client = MistralAPI(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2048) -> dict:
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
            "model": self.model
        }
