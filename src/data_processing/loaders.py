"""Data loading utilities for proteomics data."""
import pandas as pd
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional

class DataLoader:
    """Load and parse various data formats."""
    
    def load_queries(self, file_path: Path) -> List[Dict]:
        """Load query data from JSON."""
        with open(file_path) as f:
            return json.load(f)
    
    def load_responses(self, file_path: Path) -> pd.DataFrame:
        """Load LLM responses from JSONL."""
        return pd.read_json(file_path, lines=True)
    
    def load_protein_data(self, file_path: Path) -> pd.DataFrame:
        """Load protein identification data."""
        return pd.read_csv(file_path)
    
    def load_msms_metadata(self, file_path: Path) -> Dict:
        """Load MS/MS run metadata from YAML."""
        with open(file_path) as f:
            return yaml.safe_load(f)
