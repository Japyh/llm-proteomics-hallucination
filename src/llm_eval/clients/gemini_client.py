"""Google Gemini API client."""
import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
    
    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2048) -> dict:
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )
        return {
            "content": response.text,
            "model": "gemini-1.5-pro"
        }
