#!/usr/bin/env python3
"""
Generate realistic MS/MS spectra in MGF format for LLM proteomics hallucination study.

This script generates synthetic MS/MS spectra with realistic m/z values, intensities,
and metadata for peptides derived from common human proteins.

Author: Olaf Yunus Laitinen Imanov
Institution: Technical University of Denmark
Date: 2024-03-01
"""

import random
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict


class MSSpectraGenerator:
    """Generate realistic MS/MS spectra in MGF format."""

    def __init__(self, output_dir: str = "../mass_spectrometry"):
        """
        Initialize the generator.

        Args:
            output_dir: Directory to save MGF files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Common peptides from well-known proteins
        self.peptides = [
            {"sequence": "VNVDEVGGEALGR", "protein": "HBB", "charge": 2},
            {"sequence": "LLVVYPWTQR", "protein": "HBB", "charge": 2},
            {"sequence": "FFESFGDLSTPDAVMGNPK", "protein": "HBB", "charge": 3},
            {"sequence": "LVNEVTEFAK", "protein": "ALB", "charge": 2},
            {"sequence": "YLYEIAR", "protein": "ALB", "charge": 2},
            {"sequence": "RHPDYSVVLLLR", "protein": "ALB", "charge": 3},
            {"sequence": "GIVEQCCTSICSLYGQLENYCN", "protein": "INS", "charge": 3},
            {"sequence": "FVNQHLCGSHLVEALYLVCGER", "protein": "INS", "charge": 3},
            {"sequence": "YLYEIAR", "protein": "ALB", "charge": 2},
            {"sequence": "AEFVEVTK", "protein": "ALB", "charge": 2},
            {"sequence": "LAKEYEATLEECCAK", "protein": "ALB", "charge": 2},
            {"sequence": "ATEEQLK", "protein": "ALB", "charge": 2},
            {"sequence": "QTALVELLK", "protein": "ALB", "charge": 2},
            {"sequence": "VPQVSTPTLVEVSR", "protein": "ALB", "charge": 2},
            {"sequence": "DLGEEHFK", "protein": "ALB", "charge": 2},
            {"sequence": "SLHTLFGDELCK", "protein": "ALB", "charge": 2},
            {"sequence": "DDPHACYSTVFDK", "protein": "ALB", "charge": 2},
            {"sequence": "LVAASQAALGL", "protein": "ALB", "charge": 2},
            {"sequence": "KVPQVSTPTLVEVSR", "protein": "ALB", "charge": 2},
            {"sequence": "LKPDPNTLCDEFK", "protein": "ALB", "charge": 2},
        ]

        # Amino acid masses (monoisotopic)
        self.aa_masses = {
            "A": 71.03711,
            "C": 103.00919,  # +57.02146 for carbamidomethylation
            "D": 115.02694,
            "E": 129.04259,
            "F": 147.06841,
            "G": 57.02146,
            "H": 137.05891,
            "I": 113.08406,
            "K": 128.09496,
            "L": 113.08406,
            "M": 131.04049,  # +15.99491 for oxidation
            "N": 114.04293,
            "P": 97.05276,
            "Q": 128.05858,
            "R": 156.10111,
            "S": 87.03203,
            "T": 101.04768,
            "V": 99.06841,
            "W": 186.07931,
            "Y": 163.06333,
        }

    def calculate_peptide_mass(self, sequence: str, modifications: Dict = None) -> float:
        """
        Calculate monoisotopic mass of peptide.

        Args:
            sequence: Peptide amino acid sequence
            modifications: Dict of position:mass modifications

        Returns:
            Monoisotopic mass in Daltons
        """
        mass = 18.01056  # Water (H2O)

        for aa in sequence:
            mass += self.aa_masses.get(aa, 0)

        if modifications:
            for mod_mass in modifications.values():
                mass += mod_mass

        return mass

    def generate_spectrum_peaks(
        self, peptide_mass: float, charge: int, num_peaks: int = 15
    ) -> List[Tuple[float, float]]:
        """
        Generate realistic b and y ion peaks for MS/MS spectrum.

        Args:
            peptide_mass: Precursor peptide mass
            charge: Precursor charge state
            num_peaks: Number of fragment peaks to generate

        Returns:
            List of (m/z, intensity) tuples
        """
        peaks = []

        # Generate b and y ions
        for i in range(num_peaks):
            fragment_mass = peptide_mass * random.uniform(0.1, 0.9)
            fragment_charge = random.choice([1, 2])
            mz = (fragment_mass + fragment_charge * 1.00728) / fragment_charge

            # Realistic intensity distribution
            intensity = np.random.lognormal(mean=10, sigma=1.5)

            peaks.append((mz, intensity))

        # Sort by m/z
        peaks.sort(key=lambda x: x[0])

        return peaks

    def write_mgf_spectrum(
        self, f, spectrum_id: int, peptide: Dict, retention_time: float
    ):
        """
        Write a single spectrum to MGF file.

        Args:
            f: File handle
            spectrum_id: Spectrum identifier
            peptide: Peptide information dict
            retention_time: Retention time in seconds
        """
        # Calculate peptide mass
        peptide_mass = self.calculate_peptide_mass(peptide["sequence"])

        # Calculate precursor m/z
        charge = peptide["charge"]
        precursor_mz = (peptide_mass + charge * 1.00728) / charge

        # Add realistic mass error (<2 ppm)
        mass_error_ppm = random.uniform(-1.5, 1.5)
        precursor_mz += precursor_mz * mass_error_ppm / 1e6

        # Generate fragment peaks
        peaks = self.generate_spectrum_peaks(peptide_mass, charge)

        # Write MGF entry
        f.write("BEGIN IONS\n")
        f.write(
            f"TITLE=Spectrum_{spectrum_id:04d}_{peptide['protein']}_{peptide['sequence']}\n"
        )
        f.write(f"RTINSECONDS={retention_time:.1f}\n")
        f.write(f"PEPMASS={precursor_mz:.4f} {random.uniform(50000, 500000):.0f}\n")
        f.write(f"CHARGE={charge}+\n")
        f.write(f"SCANS={spectrum_id}\n")

        # Write peaks
        for mz, intensity in peaks:
            f.write(f"{mz:.4f} {intensity:.1f}\n")

        f.write("END IONS\n\n")

    def generate_mgf_file(self, output_file: str = "example_spectra.mgf", num_spectra: int = 20):
        """
        Generate MGF file with multiple spectra.

        Args:
            output_file: Output MGF filename
            num_spectra: Number of spectra to generate
        """
        output_path = self.output_dir / output_file

        with open(output_path, "w") as f:
            for i in range(num_spectra):
                # Random retention time (20-70 minutes)
                retention_time = random.uniform(1200, 4200)

                # Select random peptide
                peptide = random.choice(self.peptides)

                # Write spectrum
                self.write_mgf_spectrum(f, i + 1, peptide, retention_time)

        print(f"Generated {num_spectra} spectra in {output_path}")

    def generate_all_spectra(self):
        """Generate all MS/MS spectra files."""
        print("Generating example MS/MS spectra...")
        self.generate_mgf_file("example_spectra.mgf", num_spectra=20)
        print("\nMS/MS spectra generation complete!")


def main():
    """Main function."""
    generator = MSSpectraGenerator()
    generator.generate_all_spectra()


if __name__ == "__main__":
    main()
