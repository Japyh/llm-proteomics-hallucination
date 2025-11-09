"""Parse and extract metadata from various sources."""
import yaml
import json
from pathlib import Path
from typing import Dict

def parse_yaml_metadata(file_path: Path) -> Dict:
    """Parse YAML metadata file."""
    with open(file_path) as f:
        return yaml.safe_load(f)

def parse_json_metadata(file_path: Path) -> Dict:
    """Parse JSON metadata file."""
    with open(file_path) as f:
        return json.load(f)

def extract_msms_metadata(mgf_file: Path) -> Dict:
    """Extract metadata from MGF file headers."""
    metadata = {}
    with open(mgf_file) as f:
        for line in f:
            if line.startswith('TITLE='):
                metadata['title'] = line.split('=')[1].strip()
            elif line.startswith('PEPMASS='):
                metadata['precursor_mz'] = float(line.split('=')[1].split()[0])
            elif line.startswith('CHARGE='):
                metadata['charge'] = line.split('=')[1].strip()
            elif line.startswith('BEGIN IONS'):
                break
    return metadata
