"""
Input/Output utilities for loading and saving data files.
"""

import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Union
import pandas as pd


def load_json(file_path: Union[str, Path]) -> Union[Dict, List]:
    """
    Load data from JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data (dict or list)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Union[Dict, List], file_path: Union[str, Path], indent: int = 2):
    """
    Save data to JSON file.

    Args:
        data: Data to save
        file_path: Output file path
        indent: JSON indentation level
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_jsonl(file_path: Union[str, Path]) -> List[Dict]:
    """
    Load data from JSONL (JSON Lines) file.

    Args:
        file_path: Path to JSONL file

    Returns:
        List of dictionaries
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def save_jsonl(data: List[Dict], file_path: Union[str, Path]):
    """
    Save data to JSONL (JSON Lines) file.

    Args:
        data: List of dictionaries to save
        file_path: Output file path
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def load_csv(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
    """
    Load CSV file into pandas DataFrame.

    Args:
        file_path: Path to CSV file
        **kwargs: Additional arguments for pd.read_csv

    Returns:
        DataFrame
    """
    return pd.read_csv(file_path, **kwargs)


def save_csv(df: pd.DataFrame, file_path: Union[str, Path], **kwargs):
    """
    Save pandas DataFrame to CSV file.

    Args:
        df: DataFrame to save
        file_path: Output file path
        **kwargs: Additional arguments for df.to_csv
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(file_path, **kwargs)


def ensure_dir(directory: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if necessary.

    Args:
        directory: Directory path

    Returns:
        Path object
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


# Aliases for consistency
ensure_directory = ensure_dir
write_json = save_json
read_json = load_json
write_jsonl = save_jsonl
read_jsonl = load_jsonl
