"""Caching backend for LLM API responses."""
import json
import hashlib
from pathlib import Path

class ResponseCache:
    """Cache LLM responses to reduce API costs."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _hash_key(self, prompt: str, model: str) -> str:
        """Generate cache key from prompt and model."""
        key_str = f"{model}:{prompt}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, prompt: str, model: str):
        """Retrieve cached response."""
        key = self._hash_key(prompt, model)
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return None
    
    def set(self, prompt: str, model: str, response: dict):
        """Cache a response."""
        key = self._hash_key(prompt, model)
        cache_file = self.cache_dir / f"{key}.json"
        with open(cache_file, 'w') as f:
            json.dump(response, f)
