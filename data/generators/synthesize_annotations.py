#!/usr/bin/env python3
"""
Synthesize expert annotations for LLM responses.

This script generates realistic expert annotations with inter-rater agreement
patterns for validating the hallucination detection framework.
"""

import json
import random
from typing import List, Dict, Tuple
from pathlib import Path

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


class AnnotationSynthesizer:
    """Generate synthetic expert annotations with realistic agreement patterns."""

    def __init__(self, inter_rater_agreement: float = 0.87):
        """
        Args:
            inter_rater_agreement: Target Cohen's kappa (default 0.87 = good agreement)
        """
        self.target_kappa = inter_rater_agreement
        self.severity_scale = {
            0: "No hallucination",
            1: "Minor hallucination",
            2: "Moderate hallucination",
            3: "Severe hallucination",
        }

    def simulate_expert_annotation(
        self,
        query_id: str,
        ground_truth_level: int,
        annotator_id: int,
        expertise_level: float = 0.9
    ) -> Dict:
        """
        Simulate a single expert annotation.

        Args:
            query_id: Query identifier
            ground_truth_level: True hallucination level (0-3)
            annotator_id: Annotator identifier
            expertise_level: Expert accuracy (0-1), higher = more accurate
        """
        # Simulate annotation accuracy based on expertise
        if random.random() < expertise_level:
            # Expert gets it right
            hallucination_level = ground_truth_level
            confidence = random.uniform(0.85, 1.0)
        else:
            # Expert makes an error (typically off by 1 level)
            if ground_truth_level == 0:
                hallucination_level = random.choice([0, 1])
            elif ground_truth_level == 3:
                hallucination_level = random.choice([2, 3])
            else:
                hallucination_level = random.choice([
                    ground_truth_level - 1,
                    ground_truth_level,
                    ground_truth_level + 1
                ])
            hallucination_level = max(0, min(3, hallucination_level))
            confidence = random.uniform(0.5, 0.85)

        # Simulate annotation time (harder cases take longer)
        base_time = random.uniform(8, 15)
        complexity_factor = 1 + (ground_truth_level * 0.5)
        annotation_time = base_time * complexity_factor

        # Generate free-text justification
        justifications = {
            0: [
                "Response is factually accurate based on UniProt database.",
                "All claims verified against current literature.",
                "No fabricated information detected.",
            ],
            1: [
                "Minor numerical inaccuracy in mass/charge value.",
                "Slightly incorrect residue position, but overall concept correct.",
                "Database accession number has one digit wrong.",
            ],
            2: [
                "Incorrect protein function attribution.",
                "Wrong subcellular localization mentioned.",
                "Misidentified interaction partner.",
            ],
            3: [
                "Completely fabricated protein properties not found in any database.",
                "Claims protein function in species where it doesn't exist.",
                "Severe factual errors that would mislead researchers.",
            ],
        }

        return {
            "query_id": query_id,
            "annotator_id": annotator_id,
            "hallucination_level": hallucination_level,
            "severity_label": self.severity_scale[hallucination_level],
            "confidence": round(confidence, 2),
            "annotation_time_seconds": int(annotation_time),
            "justification": random.choice(justifications[hallucination_level]),
        }

    def simulate_dual_annotation(
        self,
        query_id: str,
        ground_truth_level: int
    ) -> Tuple[Dict, Dict, bool]:
        """
        Simulate two annotators with controlled agreement.

        Returns:
            (annotation_1, annotation_2, requires_adjudication)
        """
        # First annotator (slightly more experienced)
        ann1 = self.simulate_expert_annotation(query_id, ground_truth_level, 1, expertise_level=0.92)

        # Second annotator agreement probability based on target kappa
        # Simplified: high kappa means high probability of exact agreement
        agreement_prob = 0.7 + (self.target_kappa - 0.7) * 0.5

        if random.random() < agreement_prob:
            # Annotators agree
            ann2 = self.simulate_expert_annotation(query_id, ground_truth_level, 2, expertise_level=0.88)
            # Force agreement
            ann2["hallucination_level"] = ann1["hallucination_level"]
            ann2["severity_label"] = ann1["severity_label"]
            requires_adjudication = False
        else:
            # Annotators disagree
            ann2 = self.simulate_expert_annotation(query_id, ground_truth_level, 2, expertise_level=0.88)
            # Ensure they actually disagree
            while ann2["hallucination_level"] == ann1["hallucination_level"]:
                ann2 = self.simulate_expert_annotation(query_id, ground_truth_level, 2, expertise_level=0.88)
            requires_adjudication = abs(ann2["hallucination_level"] - ann1["hallucination_level"]) > 1

        return ann1, ann2, requires_adjudication

    def generate_annotation_round(self, responses: List[Dict], round_number: int) -> List[Dict]:
        """Generate annotations for one round."""
        annotations = []

        for response in responses:
            query_id = response["query_id"]
            ground_truth = response.get("ground_truth_hallucination_level", 0)

            ann1, ann2, requires_adj = self.simulate_dual_annotation(query_id, ground_truth)

            agreement = "full" if ann1["hallucination_level"] == ann2["hallucination_level"] else "partial"

            annotation_entry = {
                "query_id": query_id,
                "round": round_number,
                "annotator_1": ann1,
                "annotator_2": ann2,
                "agreement": agreement,
                "requires_adjudication": requires_adj,
            }

            annotations.append(annotation_entry)

        return annotations

    def adjudicate_disagreements(self, round1: List[Dict], round2: List[Dict]) -> List[Dict]:
        """Generate adjudicated labels for disagreements."""
        adjudicated = []

        for r1, r2 in zip(round1, round2):
            query_id = r1["query_id"]

            # Collect all annotations
            all_levels = [
                r1["annotator_1"]["hallucination_level"],
                r1["annotator_2"]["hallucination_level"],
                r2["annotator_1"]["hallucination_level"],
                r2["annotator_2"]["hallucination_level"],
            ]

            # Adjudication: use majority vote or median
            from collections import Counter
            vote_counts = Counter(all_levels)
            most_common = vote_counts.most_common(1)[0][0]

            # Calculate confidence based on consensus
            consensus_strength = vote_counts[most_common] / len(all_levels)

            adjudicated.append({
                "query_id": query_id,
                "adjudicated_level": most_common,
                "severity_label": self.severity_scale[most_common],
                "consensus_strength": round(consensus_strength, 2),
                "annotation_votes": dict(vote_counts),
                "adjudicator_notes": f"Resolved via {consensus_strength*100:.0f}% consensus.",
            })

        return adjudicated


def main():
    """Main execution function."""
    # Load LLM responses (which contain ground truth)
    responses_dir = Path(__file__).parent.parent / "llm_responses"
    output_dir = Path(__file__).parent.parent / "ground_truth"
    output_dir.mkdir(parents=True, exist_ok=True)

    # For demo, create synthetic responses with ground truth
    print("Generating synthetic expert annotations...")

    synthesizer = AnnotationSynthesizer(inter_rater_agreement=0.87)

    # Simulate 100 responses
    sample_responses = []
    for i in range(100):
        sample_responses.append({
            "query_id": f"TEST_{i+1:03d}",
            "ground_truth_hallucination_level": random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0],
        })

    # Generate two rounds of annotations
    print("Generating Round 1 annotations...")
    round1 = synthesizer.generate_annotation_round(sample_responses, round_number=1)

    print("Generating Round 2 annotations...")
    round2 = synthesizer.generate_annotation_round(sample_responses, round_number=2)

    # Generate adjudicated labels
    print("Generating adjudicated labels...")
    adjudicated = synthesizer.adjudicate_disagreements(round1, round2)

    # Save outputs
    with open(output_dir / "expert_annotations_round1.json", 'w') as f:
        json.dump(round1, f, indent=2)
    print(f"Saved {len(round1)} Round 1 annotations")

    with open(output_dir / "expert_annotations_round2.json", 'w') as f:
        json.dump(round2, f, indent=2)
    print(f"Saved {len(round2)} Round 2 annotations")

    with open(output_dir / "adjudicated_labels.json", 'w') as f:
        json.dump(adjudicated, f, indent=2)
    print(f"Saved {len(adjudicated)} adjudicated labels")

    # Calculate inter-rater reliability
    agreements = sum(1 for r in round1 if r["agreement"] == "full")
    kappa = agreements / len(round1)  # Simplified kappa
    print(f"\nInter-rater agreement (simplified kappa): {kappa:.3f}")


if __name__ == "__main__":
    main()
