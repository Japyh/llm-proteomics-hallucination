"""Main evaluation runner"""
from typing import List, Dict, Any
import pandas as pd
from pathlib import Path

def run_evaluation(queries: List[Dict], models: List[Any], 
                   output_path: Path) -> pd.DataFrame:
    """Run LLM evaluation on queries
    
    Args:
        queries: List of query dictionaries
        models: List of model client instances
        output_path: Path to save results
        
    Returns:
        DataFrame with evaluation results
    """
    results = []
    
    for query in queries:
        for model in models:
            response = model.generate(query['text'])
            results.append({
                'query_id': query['query_id'],
                'model': model.model,
                'response': response['text'],
                'tokens': response['usage']
            })
    
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)
    return df
