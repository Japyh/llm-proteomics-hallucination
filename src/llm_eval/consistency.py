"""Consistency analysis across multiple responses."""
import numpy as np
from sentence_transformers import SentenceTransformer

class ConsistencyAnalyzer:
    """Analyze consistency of LLM responses."""
    
    def __init__(self, model_name='all-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
        emb1 = self.model.encode([text1])[0]
        emb2 = self.model.encode([text2])[0]
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    
    def consistency_score(self, responses: list) -> float:
        """Calculate pairwise consistency across multiple responses."""
        if len(responses) < 2:
            return 1.0
        
        similarities = []
        for i in range(len(responses)):
            for j in range(i+1, len(responses)):
                sim = self.semantic_similarity(responses[i], responses[j])
                similarities.append(sim)
        
        return np.mean(similarities)
