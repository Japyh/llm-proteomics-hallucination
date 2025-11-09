"""OpenAI API client wrapper"""
from typing import Dict, Any
import openai

class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, temperature: float = 0.1, 
                max_tokens: int = 500) -> Dict[str, Any]:
        """Generate response from OpenAI model"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return {
            "text": response.choices[0].message.content,
            "model": self.model,
            "usage": response.usage.total_tokens
        }
