"""Export results in various formats."""
import pandas as pd
import json
from pathlib import Path

def export_to_csv(results: pd.DataFrame, output_path: Path):
    """Export results to CSV."""
    results.to_csv(output_path, index=False)

def export_to_json(results: dict, output_path: Path):
    """Export results to JSON."""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

def export_to_latex(df: pd.DataFrame, output_path: Path):
    """Export table to LaTeX format."""
    latex = df.to_latex(index=False, escape=False)
    with open(output_path, 'w') as f:
        f.write(latex)
