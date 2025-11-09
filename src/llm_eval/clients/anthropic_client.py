"""Anthropic API client wrapper"""
from typing import Dict, Any
import anthropic

class AnthropicClient:
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, temperature: float = 0.1,
                max_tokens: int = 500) -> Dict[str, Any]:
        """Generate response from Anthropic model"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "text": message.content[0].text,
            "model": self.model,
            "usage": message.usage.input_tokens + message.usage.output_tokens
        }
