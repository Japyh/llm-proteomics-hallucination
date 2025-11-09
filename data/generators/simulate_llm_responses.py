#!/usr/bin/env python3
"""
Simulate LLM responses to proteomics queries.

This script generates synthetic LLM responses with varying levels of accuracy
and hallucination for testing the evaluation framework.
"""

import json
import random
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime, timedelta

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


class ResponseSimulator:
    """Generate synthetic LLM responses with controlled hallucination rates."""

    def __init__(self, hallucination_rate: float = 0.3):
        self.hallucination_rate = hallucination_rate
        self.models = {
            "gpt4-turbo": {"mean_latency": 1500, "std_latency": 300},
            "claude-sonnet": {"mean_latency": 1200, "std_latency": 250},
            "gemini-pro": {"mean_latency": 1400, "std_latency": 280},
            "mistral-large": {"mean_latency": 1100, "std_latency": 200},
            "llama3-70b": {"mean_latency": 2000, "std_latency": 400},
        }

    def generate_correct_response(self, query: Dict) -> str:
        """Generate a factually correct response."""
        complexity = query.get("complexity", "medium")

        correct_responses = {
            "low": [
                "The UniProt accession number for human hemoglobin subunit beta (HBB) is P68871.",
                "TP53 functions as a tumor suppressor protein with roles in apoptosis and cell cycle regulation.",
                "EGFR is located primarily in the plasma membrane and endosomal compartments.",
            ],
            "medium": [
                "TP53 undergoes multiple post-translational modifications including phosphorylation at Ser15, Ser20, and acetylation at Lys382, which regulate its stability and transcriptional activity.",
                "EGFR interacts with GRB2, SOS1, and PI3K in lung adenocarcinoma, mediating downstream MAPK and AKT signaling pathways.",
            ],
            "high": [
                "Based on the 3.2-fold upregulation and phosphorylation at Ser123, this suggests activation of upstream kinases such as ATM or ATR. The q-value of 0.001 indicates high statistical confidence. Downstream effects likely include cell cycle checkpoint activation.",
                "With 15 unique peptides and 42% sequence coverage, this protein identification meets high-confidence criteria (typically >2 peptides and >10% coverage), suggesting reliable identification.",
            ],
        }

        return random.choice(correct_responses.get(complexity, correct_responses["medium"]))

    def inject_hallucination(self, correct_response: str, severity: str = "minor") -> str:
        """Inject hallucinations into correct responses."""
        hallucination_types = {
            "minor": [
                lambda x: x.replace("P68871", "P68872"),  # Wrong accession
                lambda x: x.replace("Ser15", "Ser16"),    # Wrong residue number
                lambda x: x.replace("42%", "38%"),        # Slight numeric error
            ],
            "moderate": [
                lambda x: x.replace("tumor suppressor", "oncogene"),  # Functional misattribution
                lambda x: x.replace("plasma membrane", "mitochondria"),  # Wrong localization
                lambda x: x.replace("ATM or ATR", "CDK2 or CDK4"),  # Wrong kinase family
            ],
            "severe": [
                lambda x: "This protein has not been characterized in humans and is only found in yeast.",
                lambda x: "Based on recent studies, this protein is involved in photosynthesis in plant cells.",
                lambda x: "The UniProt database does not contain any information about this protein.",
            ],
        }

        if severity == "severe":
            return random.choice(hallucination_types["severe"])(correct_response)

        mutations = hallucination_types.get(severity, hallucination_types["minor"])
        return random.choice(mutations)(correct_response)

    def generate_response(self, query: Dict, model_name: str, inject_error: bool = None) -> Dict:
        """Generate a single model response."""
        if inject_error is None:
            inject_error = random.random() < self.hallucination_rate

        correct_response = self.generate_correct_response(query)

        if inject_error:
            severity = random.choices(
                ["minor", "moderate", "severe"],
                weights=[0.6, 0.3, 0.1]
            )[0]
            response_text = self.inject_hallucination(correct_response, severity)
            hallucination_level = {"minor": 1, "moderate": 2, "severe": 3}[severity]
        else:
            response_text = correct_response
            hallucination_level = 0

        # Simulate latency
        model_config = self.models[model_name]
        latency = int(random.gauss(model_config["mean_latency"], model_config["std_latency"]))
        latency = max(100, latency)  # Minimum 100ms

        # Simulate token usage
        prompt_tokens = len(query["query_text"].split()) * 1.3
        completion_tokens = len(response_text.split()) * 1.3

        timestamp = datetime.now() - timedelta(days=random.randint(1, 30))

        return {
            "query_id": query["query_id"],
            "model": model_name,
            "response": response_text,
            "timestamp": timestamp.isoformat() + "Z",
            "latency_ms": latency,
            "usage": {
                "prompt_tokens": int(prompt_tokens),
                "completion_tokens": int(completion_tokens),
                "total_tokens": int(prompt_tokens + completion_tokens),
            },
            "ground_truth_hallucination_level": hallucination_level,  # For evaluation
        }

    def generate_responses_for_queries(self, queries: List[Dict], model_name: str) -> List[Dict]:
        """Generate responses for all queries from a specific model."""
        responses = []
        for query in queries:
            response = self.generate_response(query, model_name)
            responses.append(response)
        return responses

    def save_responses(self, responses: List[Dict], output_path: Path):
        """Save responses in JSONL format."""
        with open(output_path, 'w') as f:
            for response in responses:
                # Remove ground truth before saving
                response_copy = {k: v for k, v in response.items() if k != "ground_truth_hallucination_level"}
                f.write(json.dumps(response_copy) + '\n')
        print(f"Saved {len(responses)} responses to {output_path}")


def main():
    """Main execution function."""
    # Load queries
    queries_dir = Path(__file__).parent.parent / "queries"
    output_dir = Path(__file__).parent.parent / "llm_responses"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load all queries
    all_queries = []
    for query_file in ["queries_train.json", "queries_validation.json", "queries_test.json"]:
        with open(queries_dir / query_file) as f:
            all_queries.extend(json.load(f))

    print(f"Loaded {len(all_queries)} queries")

    # Generate responses for each model
    models_hallucination_rates = {
        "gpt4-turbo": 0.334,
        "claude-sonnet": 0.278,
        "gemini-pro": 0.324,
        "mistral-large": 0.298,
        "llama3-70b": 0.356,
    }

    for model_name, hallucination_rate in models_hallucination_rates.items():
        print(f"\nGenerating responses for {model_name} (hallucination rate: {hallucination_rate})...")
        simulator = ResponseSimulator(hallucination_rate=hallucination_rate)
        responses = simulator.generate_responses_for_queries(all_queries, model_name)

        output_file = output_dir / f"{model_name.replace('-', '_')}_responses.jsonl"
        simulator.save_responses(responses, output_file)


if __name__ == "__main__":
    main()
