"""Join multiple data sources for integrated analysis."""
import pandas as pd

class DataJoiner:
    """Join proteomics, LLM, and metadata."""
    
    def join_queries_responses(self, queries: pd.DataFrame, responses: pd.DataFrame) -> pd.DataFrame:
        """Join queries with LLM responses."""
        return queries.merge(responses, on='query_id', how='inner')
    
    def join_with_ground_truth(self, df: pd.DataFrame, ground_truth: pd.DataFrame) -> pd.DataFrame:
        """Join with expert annotations."""
        return df.merge(ground_truth, on='query_id', how='left')
    
    def join_protein_metadata(self, df: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
        """Join with protein annotations."""
        return df.merge(metadata, on='uniprot_id', how='left')
    
    def create_analysis_dataset(
        self,
        queries: pd.DataFrame,
        responses: pd.DataFrame,
        ground_truth: pd.DataFrame,
        metadata: pd.DataFrame
    ) -> pd.DataFrame:
        """Create complete analysis dataset."""
        df = self.join_queries_responses(queries, responses)
        df = self.join_with_ground_truth(df, ground_truth)
        df = self.join_protein_metadata(df, metadata)
        return df
