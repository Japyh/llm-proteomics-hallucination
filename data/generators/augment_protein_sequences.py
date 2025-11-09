#!/usr/bin/env python3
"""
Augment protein sequence databases with variants and modifications.

This script generates protein sequence variants (mutations, PTMs) for
comprehensive LLM testing scenarios.
"""

import random
from typing import List, Dict, Tuple
from pathlib import Path

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


class ProteinAugmenter:
    """Generate protein sequence variants and modifications."""

    AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

    PTM_TYPES = {
        "Phosphorylation": ["S", "T", "Y"],
        "Acetylation": ["K"],
        "Methylation": ["K", "R"],
        "Ubiquitination": ["K"],
        "Glycosylation": ["N", "S", "T"],
    }

    def __init__(self):
        self.variant_counter = 0

    def introduce_point_mutation(self, sequence: str, position: int = None) -> Tuple[str, Dict]:
        """Introduce a single amino acid substitution."""
        if position is None:
            position = random.randint(0, len(sequence) - 1)

        original_aa = sequence[position]
        # Choose different amino acid
        new_aa = random.choice([aa for aa in self.AMINO_ACIDS if aa != original_aa])

        mutated_sequence = sequence[:position] + new_aa + sequence[position+1:]

        mutation_info = {
            "type": "point_mutation",
            "position": position + 1,  # 1-indexed
            "original": original_aa,
            "mutant": new_aa,
            "notation": f"{original_aa}{position+1}{new_aa}",
        }

        return mutated_sequence, mutation_info

    def introduce_deletion(self, sequence: str, start: int = None, length: int = 3) -> Tuple[str, Dict]:
        """Introduce a deletion."""
        if start is None:
            start = random.randint(0, len(sequence) - length - 1)

        deleted_region = sequence[start:start+length]
        mutated_sequence = sequence[:start] + sequence[start+length:]

        deletion_info = {
            "type": "deletion",
            "start": start + 1,
            "end": start + length,
            "deleted_sequence": deleted_region,
            "notation": f"del{start+1}_{start+length}",
        }

        return mutated_sequence, deletion_info

    def introduce_insertion(self, sequence: str, position: int = None, insert_length: int = 3) -> Tuple[str, Dict]:
        """Introduce an insertion."""
        if position is None:
            position = random.randint(0, len(sequence) - 1)

        inserted_sequence = ''.join(random.choices(self.AMINO_ACIDS, k=insert_length))
        mutated_sequence = sequence[:position] + inserted_sequence + sequence[position:]

        insertion_info = {
            "type": "insertion",
            "position": position + 1,
            "inserted_sequence": inserted_sequence,
            "notation": f"ins{position+1}_{inserted_sequence}",
        }

        return mutated_sequence, insertion_info

    def add_ptm_annotation(self, sequence: str, ptm_type: str = None) -> Dict:
        """Generate PTM site annotation."""
        if ptm_type is None:
            ptm_type = random.choice(list(self.PTM_TYPES.keys()))

        # Find sites that can have this PTM
        target_residues = self.PTM_TYPES[ptm_type]
        sites = [i for i, aa in enumerate(sequence) if aa in target_residues]

        if not sites:
            # No valid site for this PTM
            return None

        site = random.choice(sites)

        ptm_info = {
            "type": "ptm",
            "modification": ptm_type,
            "position": site + 1,
            "residue": sequence[site],
            "notation": f"{ptm_type}_{sequence[site]}{site+1}",
        }

        return ptm_info

    def generate_disease_variant(self, protein_info: Dict) -> Dict:
        """Generate a clinically relevant variant."""
        sequence = protein_info["sequence"]

        # Common disease-causing mutation types
        variant_type = random.choice(["point_mutation", "deletion", "insertion"])

        if variant_type == "point_mutation":
            mutated_seq, mutation = self.introduce_point_mutation(sequence)
            pathogenicity = random.choice(["pathogenic", "likely_pathogenic", "uncertain_significance"])
        elif variant_type == "deletion":
            mutated_seq, mutation = self.introduce_deletion(sequence, length=random.randint(1, 9))
            pathogenicity = random.choice(["pathogenic", "likely_pathogenic"])
        else:  # insertion
            mutated_seq, mutation = self.introduce_insertion(sequence, insert_length=random.randint(1, 6))
            pathogenicity = random.choice(["pathogenic", "uncertain_significance"])

        self.variant_counter += 1

        variant = {
            "variant_id": f"VAR_{self.variant_counter:06d}",
            "protein_name": protein_info["name"],
            "gene": protein_info["gene"],
            "uniprot_id": protein_info["uniprot_id"],
            "original_sequence": sequence,
            "variant_sequence": mutated_seq,
            "mutation": mutation,
            "pathogenicity": pathogenicity,
            "disease_association": protein_info.get("disease", "Unknown"),
            "frequency": random.choice(["rare", "uncommon", "common"]),
        }

        return variant

    def generate_ptm_profile(self, protein_info: Dict, n_ptms: int = 3) -> List[Dict]:
        """Generate multiple PTM sites for a protein."""
        sequence = protein_info["sequence"]
        ptm_profile = []

        used_positions = set()

        for _ in range(n_ptms):
            ptm = self.add_ptm_annotation(sequence)
            if ptm and ptm["position"] not in used_positions:
                ptm_profile.append({
                    "protein_name": protein_info["name"],
                    "gene": protein_info["gene"],
                    "uniprot_id": protein_info["uniprot_id"],
                    **ptm,
                })
                used_positions.add(ptm["position"])

        return ptm_profile


def main():
    """Main execution function."""
    # Sample proteins
    sample_proteins = [
        {
            "name": "Tumor protein p53",
            "gene": "TP53",
            "uniprot_id": "P04637",
            "sequence": "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELPPGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPGGSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD",
            "disease": "Various cancers",
        },
        {
            "name": "Hemoglobin subunit beta",
            "gene": "HBB",
            "uniprot_id": "P68871",
            "sequence": "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH",
            "disease": "Sickle cell anemia",
        },
    ]

    augmenter = ProteinAugmenter()

    # Generate disease variants
    print("Generating disease variants...")
    variants = []
    for protein in sample_proteins:
        for _ in range(3):  # 3 variants per protein
            variant = augmenter.generate_disease_variant(protein)
            variants.append(variant)

    print(f"Generated {len(variants)} disease variants")

    # Generate PTM profiles
    print("\nGenerating PTM profiles...")
    ptm_profiles = []
    for protein in sample_proteins:
        ptms = augmenter.generate_ptm_profile(protein, n_ptms=5)
        ptm_profiles.extend(ptms)

    print(f"Generated {len(ptm_profiles)} PTM sites")

    # Display examples
    print("\n--- Example Disease Variant ---")
    example_var = variants[0]
    print(f"Protein: {example_var['protein_name']} ({example_var['gene']})")
    print(f"Mutation: {example_var['mutation']['notation']}")
    print(f"Pathogenicity: {example_var['pathogenicity']}")
    print(f"Disease: {example_var['disease_association']}")

    print("\n--- Example PTM Sites ---")
    for ptm in ptm_profiles[:3]:
        print(f"{ptm['gene']}: {ptm['modification']} at {ptm['residue']}{ptm['position']}")

    # Save to files
    output_dir = Path(__file__).parent.parent / "proteins"
    output_dir.mkdir(parents=True, exist_ok=True)

    import csv

    # Save variants
    with open(output_dir / "disease_variants.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "variant_id", "gene", "uniprot_id", "mutation_notation",
            "pathogenicity", "disease_association", "frequency"
        ])
        writer.writeheader()
        for var in variants:
            writer.writerow({
                "variant_id": var["variant_id"],
                "gene": var["gene"],
                "uniprot_id": var["uniprot_id"],
                "mutation_notation": var["mutation"]["notation"],
                "pathogenicity": var["pathogenicity"],
                "disease_association": var["disease_association"],
                "frequency": var["frequency"],
            })

    print(f"\nSaved variants to {output_dir / 'disease_variants.csv'}")

    # Save PTMs
    with open(output_dir / "ptm_sites_augmented.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "gene", "uniprot_id", "position", "residue", "modification"
        ])
        writer.writeheader()
        for ptm in ptm_profiles:
            writer.writerow({
                "gene": ptm["gene"],
                "uniprot_id": ptm["uniprot_id"],
                "position": ptm["position"],
                "residue": ptm["residue"],
                "modification": ptm["modification"],
            })

    print(f"Saved PTMs to {output_dir / 'ptm_sites_augmented.csv'}")


if __name__ == "__main__":
    main()
