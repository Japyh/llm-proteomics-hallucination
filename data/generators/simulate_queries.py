#!/usr/bin/env python3
"""
Simulate proteomics queries for LLM hallucination evaluation.

This script generates synthetic queries across different complexity levels
and protein prevalence categories for testing LLM performance.
"""

import json
import random
from typing import List, Dict
from pathlib import Path

# Seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)


class QuerySimulator:
    """Generate synthetic proteomics queries."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.complexity_levels = ['low', 'medium', 'high']
        self.protein_prevalence = ['common', 'uncommon', 'rare']

    def generate_low_complexity_query(self, query_id: str, protein: str) -> Dict:
        """Generate a simple factual query."""
        templates = [
            f"What is the UniProt accession number for {protein}?",
            f"What is the molecular function of {protein}?",
            f"In which cellular compartment is {protein} located?",
            f"What is the gene name for {protein}?",
        ]

        return {
            "query_id": query_id,
            "query_text": random.choice(templates),
            "complexity": "low",
            "protein_prevalence": random.choice(self.protein_prevalence),
            "expected_answer_type": "factual",
            "required_databases": ["UniProt", "GO"],
        }

    def generate_medium_complexity_query(self, query_id: str) -> Dict:
        """Generate a query requiring integration of multiple facts."""
        templates = [
            "What are the known post-translational modifications of TP53 and their functional implications?",
            "Which proteins interact with EGFR in lung adenocarcinoma and what are their roles?",
            "What is the subcellular localization of insulin receptor and how does it change upon ligand binding?",
            "What are the protein domains in AKT1 and their respective functions?",
        ]

        return {
            "query_id": query_id,
            "query_text": random.choice(templates),
            "complexity": "medium",
            "protein_prevalence": random.choice(self.protein_prevalence),
            "expected_answer_type": "multi_fact",
            "required_databases": ["UniProt", "GO", "IntAct", "Pfam"],
        }

    def generate_high_complexity_query(self, query_id: str) -> Dict:
        """Generate a complex query requiring reasoning and integration."""
        templates = [
            "Given a TMT-labeled proteomics experiment showing 3.2-fold upregulation of protein X (UniProt: P12345, q-value=0.001) with concurrent phosphorylation at Ser123, what are the likely downstream signaling effects?",
            "In a SILAC experiment comparing cancer vs normal cells, protein Y shows 2.8-fold increase with phosphorylation at Thr456. What kinase is likely responsible and what are the therapeutic implications?",
            "A mass spectrometry study identified protein Z with 15 unique peptides and 42% sequence coverage. What level of confidence can we assign to this identification?",
        ]

        return {
            "query_id": query_id,
            "query_text": random.choice(templates),
            "complexity": "high",
            "protein_prevalence": random.choice(self.protein_prevalence),
            "expected_answer_type": "reasoning",
            "required_databases": ["UniProt", "GO", "PhosphoSitePlus", "STRING", "DrugBank"],
        }

    def generate_query_set(self, n_low: int = 100, n_medium: int = 100, n_high: int = 100) -> List[Dict]:
        """Generate a balanced set of queries."""
        queries = []

        # Common proteins
        common_proteins = ["TP53", "EGFR", "AKT1", "INS", "HBB"]

        # Low complexity
        for i in range(n_low):
            query_id = f"LOW_{i+1:03d}"
            protein = random.choice(common_proteins)
            queries.append(self.generate_low_complexity_query(query_id, protein))

        # Medium complexity
        for i in range(n_medium):
            query_id = f"MED_{i+1:03d}"
            queries.append(self.generate_medium_complexity_query(query_id))

        # High complexity
        for i in range(n_high):
            query_id = f"HIGH_{i+1:03d}"
            queries.append(self.generate_high_complexity_query(query_id))

        return queries

    def save_queries(self, queries: List[Dict], filename: str):
        """Save queries to JSON file."""
        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            json.dump(queries, f, indent=2)
        print(f"Saved {len(queries)} queries to {output_path}")


def main():
    """Main execution function."""
    output_dir = Path(__file__).parent.parent / "queries"
    output_dir.mkdir(parents=True, exist_ok=True)

    simulator = QuerySimulator(output_dir)

    # Generate train/validation/test splits
    print("Generating query sets...")

    train_queries = simulator.generate_query_set(n_low=60, n_medium=60, n_high=60)
    val_queries = simulator.generate_query_set(n_low=20, n_medium=20, n_high=20)
    test_queries = simulator.generate_query_set(n_low=20, n_medium=20, n_high=20)

    simulator.save_queries(train_queries, "queries_train.json")
    simulator.save_queries(val_queries, "queries_validation.json")
    simulator.save_queries(test_queries, "queries_test.json")

    print(f"\nTotal queries generated: {len(train_queries) + len(val_queries) + len(test_queries)}")


if __name__ == "__main__":
    main()
