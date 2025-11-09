"""Anthropic Claude API client."""
import anthropic

class AnthropicClient:
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2048) -> dict:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "content": response.content[0].text,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            "model": self.model
        }
