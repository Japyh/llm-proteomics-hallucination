"""Systematic prompt variation testing."""

class PromptSweeper:
    """Test different prompt formulations."""
    
    def __init__(self, base_prompt: str):
        self.base_prompt = base_prompt
    
    def generate_variations(self):
        """Generate prompt variations."""
        variations = [
            self.base_prompt,
            f"Please {self.base_prompt.lower()}",
            f"{self.base_prompt} Provide detailed explanation.",
            f"As an expert, {self.base_prompt.lower()}",
        ]
        return variations
    
    def add_few_shot_examples(self, examples: list) -> str:
        """Add few-shot examples to prompt."""
        examples_text = "\n\n".join([f"Q: {ex['q']}\nA: {ex['a']}" for ex in examples])
        return f"{examples_text}\n\nQ: {self.base_prompt}\nA:"
