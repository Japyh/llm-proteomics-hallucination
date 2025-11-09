"""
Configuration loading utilities.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, Union
from copy import deepcopy


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from YAML or JSON file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary

    Raises:
        ValueError: If file format not supported
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    suffix = config_path.suffix.lower()

    if suffix in ['.yaml', '.yml']:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    elif suffix == '.json':
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        raise ValueError(f"Unsupported config format: {suffix}")


def merge_configs(base_config: Dict, override_config: Dict) -> Dict:
    """
    Merge two configuration dictionaries recursively.

    Args:
        base_config: Base configuration
        override_config: Configuration to override base

    Returns:
        Merged configuration dictionary
    """
    merged = deepcopy(base_config)

    for key, value in override_config.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = deepcopy(value)

    return merged


def save_config(config: Dict[str, Any], output_path: Union[str, Path]):
    """
    Save configuration to file.

    Args:
        config: Configuration dictionary
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = output_path.suffix.lower()

    if suffix in ['.yaml', '.yml']:
        with open(output_path, 'w') as f:
            yaml.safe_dump(config, f, indent=2, default_flow_style=False)
    elif suffix == '.json':
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
    else:
        raise ValueError(f"Unsupported config format: {suffix}")
