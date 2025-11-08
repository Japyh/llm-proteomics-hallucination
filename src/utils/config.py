"""Configuration management."""

import yaml
from pathlib import Path


class Config:
    """Load and manage configuration."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """Load configuration from file."""
        self.config_path = Path(config_path)
        self.config = self.load()

    def load(self) -> dict:
        """Load YAML config."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        return {}

    def get(self, key: str, default=None):
        """Get config value."""
        return self.config.get(key, default)
