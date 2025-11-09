"""Local vLLM server client."""
import requests

class LocalVLLMClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2048) -> dict:
        response = requests.post(
            f"{self.base_url}/v1/completions",
            json={
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        data = response.json()
        return {
            "content": data["choices"][0]["text"],
            "tokens_used": data["usage"]["total_tokens"],
            "model": "local-vllm"
        }
