"""Data harmonization across different sources."""
import pandas as pd

def harmonize_gene_names(df: pd.DataFrame, name_column: str = 'gene_name') -> pd.DataFrame:
    """Standardize gene nomenclature."""
    # Convert to uppercase
    df[name_column] = df[name_column].str.upper()
    # Remove whitespace
    df[name_column] = df[name_column].str.strip()
    return df

def harmonize_protein_ids(df: pd.DataFrame, id_column: str = 'protein_id') -> pd.DataFrame:
    """Standardize protein identifiers to UniProt format."""
    # Extract UniProt accessions
    df[id_column] = df[id_column].str.extract(r'([A-Z][0-9][A-Z0-9]{3}[0-9]|[OPQ][0-9][A-Z0-9]{3}[0-9])')
    return df

def merge_datasets(dfs: list, on: str, how: str = 'inner') -> pd.DataFrame:
    """Merge multiple datasets on common key."""
    result = dfs[0]
    for df in dfs[1:]:
        result = result.merge(df, on=on, how=how)
    return result
