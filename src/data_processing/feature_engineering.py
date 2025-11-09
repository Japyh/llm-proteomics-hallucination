"""Feature engineering for LLM hallucination prediction."""
import pandas as pd
import numpy as np

def create_query_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer features from query text."""
    df['query_length'] = df['query_text'].str.len()
    df['query_word_count'] = df['query_text'].str.split().str.len()
    df['has_protein_mention'] = df['query_text'].str.contains(r'[A-Z]{2,}[0-9]', regex=True)
    df['has_modification'] = df['query_text'].str.contains('phospho|acetyl|methyl|ubiquitin')
    return df

def create_response_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer features from LLM responses."""
    df['response_length'] = df['response'].str.len()
    df['has_hedging'] = df['response'].str.contains('might|maybe|possibly|likely')
    df['has_citation'] = df['response'].str.contains('PMID|doi|et al')
    df['confidence_words'] = df['response'].str.count('certain|definitely|absolutely')
    return df

def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create interaction features between variables."""
    df['complexity_x_length'] = df['complexity_level'] * df['query_length']
    return df
