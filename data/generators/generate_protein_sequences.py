#!/usr/bin/env python3
"""
Generate protein sequence FASTA files for LLM proteomics hallucination study.

This script retrieves protein sequences from UniProt API and generates FASTA files
stratified by database coverage (high, moderate, rare).

Author: Olaf Yunus Laitinen Imanov
Institution: Technical University of Denmark
Date: 2024-03-01
"""

import json
import requests
import time
from pathlib import Path
from typing import List, Dict


class ProteinSequenceGenerator:
    """Generate FASTA files with protein sequences from UniProt."""

    def __init__(self, output_dir: str = "../proteins"):
        """
        Initialize the generator.

        Args:
            output_dir: Directory to save FASTA files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.uniprot_api = "https://rest.uniprot.org/uniprotkb"

    def fetch_protein_sequence(self, uniprot_id: str) -> Dict:
        """
        Fetch protein sequence and metadata from UniProt.

        Args:
            uniprot_id: UniProt accession (e.g., "P68871")

        Returns:
            Dict with protein data
        """
        url = f"{self.uniprot_api}/{uniprot_id}.json"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            return {
                "accession": uniprot_id,
                "entry_name": data.get("uniProtkbId", ""),
                "protein_name": data.get("proteinDescription", {})
                .get("recommendedName", {})
                .get("fullName", {})
                .get("value", ""),
                "gene_name": data.get("genes", [{}])[0].get("geneName", {}).get("value", ""),
                "organism": data.get("organism", {}).get("scientificName", ""),
                "organism_id": data.get("organism", {}).get("taxonId", 0),
                "sequence": data.get("sequence", {}).get("value", ""),
                "length": data.get("sequence", {}).get("length", 0),
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {uniprot_id}: {e}")
            return None

    def write_fasta(self, proteins: List[Dict], output_file: str):
        """
        Write protein sequences to FASTA file.

        Args:
            proteins: List of protein data dicts
            output_file: Output FASTA filename
        """
        output_path = self.output_dir / output_file

        with open(output_path, "w") as f:
            for protein in proteins:
                if not protein or not protein.get("sequence"):
                    continue

                # Write FASTA header
                header = (
                    f">sp|{protein['accession']}|{protein['entry_name']} "
                    f"{protein['protein_name']} "
                    f"OS={protein['organism']} "
                    f"OX={protein['organism_id']} "
                    f"GN={protein['gene_name']}"
                )
                f.write(header + "\n")

                # Write sequence (60 characters per line)
                sequence = protein["sequence"]
                for i in range(0, len(sequence), 60):
                    f.write(sequence[i : i + 60] + "\n")

        print(f"Wrote {len(proteins)} sequences to {output_path}")

    def generate_all_sequences(self):
        """Generate all protein sequence FASTA files."""
        # High coverage proteins (common, well-annotated)
        high_coverage_ids = [
            "P68871",  # HBB - Hemoglobin subunit beta
            "P02768",  # ALB - Serum albumin
            "P01308",  # INS - Insulin
            "P01023",  # A2M - Alpha-2-macroglobulin
            "P02787",  # TRFE - Transferrin
            "P00450",  # CP - Ceruloplasmin
            "P02671",  # FGA - Fibrinogen alpha chain
            "P02675",  # FGB - Fibrinogen beta chain
            "P02679",  # FGG - Fibrinogen gamma chain
            "P00738",  # HP - Haptoglobin
            "P01009",  # A1AT - Alpha-1-antitrypsin
            "P02647",  # APOA1 - Apolipoprotein A-I
            "P04264",  # K2C1 - Keratin, type II cytoskeletal 1
            "P13645",  # K1C10 - Keratin, type I cytoskeletal 10
            "P35908",  # K22E - Keratin, type II cytoskeletal 2 epidermal
            "P02533",  # K1C14 - Keratin, type I cytoskeletal 14
            "P04083",  # ANXA1 - Annexin A1
            "P07355",  # ANXA2 - Annexin A2
            "P08758",  # ANXA5 - Annexin A5
            "P60709",  # ACTB - Actin, cytoplasmic 1
        ]

        # Low coverage proteins (rare, poorly-annotated)
        low_coverage_ids = [
            "Q9Y6K9",  # NRG3 - Pro-neuregulin-3
            "Q8N2K0",  # ABCA13 - ATP-binding cassette sub-family A member 13
            "Q9H4B4",  # PLXNA3 - Plexin-A3
            "Q8IWY4",  # FAM83H - Protein FAM83H
            "Q6ZSZ6",  # OBSCN - Obscurin
        ]

        print("Fetching high coverage protein sequences...")
        high_coverage_proteins = []
        for uniprot_id in high_coverage_ids:
            protein = self.fetch_protein_sequence(uniprot_id)
            if protein:
                high_coverage_proteins.append(protein)
            time.sleep(0.5)  # Rate limiting

        print("Fetching low coverage protein sequences...")
        low_coverage_proteins = []
        for uniprot_id in low_coverage_ids:
            protein = self.fetch_protein_sequence(uniprot_id)
            if protein:
                low_coverage_proteins.append(protein)
            time.sleep(0.5)  # Rate limiting

        # Write FASTA files
        self.write_fasta(high_coverage_proteins, "high_coverage_proteins.fasta")
        self.write_fasta(low_coverage_proteins, "low_coverage_proteins.fasta")

        print("\nSequence generation complete!")
        print(f"High coverage proteins: {len(high_coverage_proteins)}")
        print(f"Low coverage proteins: {len(low_coverage_proteins)}")


def main():
    """Main function."""
    generator = ProteinSequenceGenerator()
    generator.generate_all_sequences()


if __name__ == "__main__":
    main()
