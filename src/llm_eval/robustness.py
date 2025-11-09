"""Robustness testing via perturbations."""
import random

class RobustnessTest:
    """Test model robustness via input perturbations."""
    
    def paraphrase_query(self, query: str) -> str:
        """Simple paraphrasing (placeholder for T5/GPT-based)."""
        # In practice, use a paraphrasing model
        return query.replace("What is", "Can you tell me about")
    
    def add_typos(self, text: str, prob: float = 0.05) -> str:
        """Inject random typos."""
        chars = list(text)
        for i in range(len(chars)):
            if random.random() < prob and chars[i].isalpha():
                chars[i] = random.choice('abcdefghijklmnopqrstuvwxyz')
        return ''.join(chars)
    
    def swap_words(self, text: str, prob: float = 0.1) -> str:
        """Randomly swap adjacent words."""
        words = text.split()
        for i in range(len(words)-1):
            if random.random() < prob:
                words[i], words[i+1] = words[i+1], words[i]
        return ' '.join(words)
