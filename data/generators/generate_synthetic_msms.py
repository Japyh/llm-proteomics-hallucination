#!/usr/bin/env python3
"""
Generate synthetic MS/MS spectra for proteomics testing.

This script creates realistic-looking mass spectrometry data in MGF and mzML formats
for use in LLM evaluation experiments.
"""

import random
import math
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


class MSMSGenerator:
    """Generate synthetic MS/MS spectra."""

    AMINO_ACID_MASSES = {
        'A': 71.04, 'C': 103.01, 'D': 115.03, 'E': 129.04, 'F': 147.07,
        'G': 57.02, 'H': 137.06, 'I': 113.08, 'K': 128.09, 'L': 113.08,
        'M': 131.04, 'N': 114.04, 'P': 97.05, 'Q': 128.06, 'R': 156.10,
        'S': 87.03, 'T': 101.05, 'V': 99.07, 'W': 186.08, 'Y': 163.06,
    }

    def __init__(self):
        self.h2o_mass = 18.015
        self.proton_mass = 1.007

    def calculate_peptide_mass(self, sequence: str) -> float:
        """Calculate theoretical peptide mass."""
        mass = sum(self.AMINO_ACID_MASSES[aa] for aa in sequence)
        mass += self.h2o_mass  # Add water
        return mass

    def generate_b_ions(self, sequence: str) -> List[Tuple[float, float]]:
        """Generate b-ion series (N-terminal fragments)."""
        ions = []
        cumulative_mass = 0.0

        for i, aa in enumerate(sequence[:-1], 1):
            cumulative_mass += self.AMINO_ACID_MASSES[aa]
            mz = cumulative_mass + self.proton_mass
            intensity = random.uniform(100, 5000) * (1.0 / (i * 0.5))  # Decay with fragment number
            ions.append((mz, intensity))

        return ions

    def generate_y_ions(self, sequence: str) -> List[Tuple[float, float]]:
        """Generate y-ion series (C-terminal fragments)."""
        ions = []
        cumulative_mass = self.h2o_mass

        for i, aa in enumerate(reversed(sequence[1:]), 1):
            cumulative_mass += self.AMINO_ACID_MASSES[aa]
            mz = cumulative_mass + self.proton_mass
            intensity = random.uniform(200, 10000) * (1.0 / (i * 0.4))  # Y-ions typically more intense
            ions.append((mz, intensity))

        return ions

    def add_noise(self, ions: List[Tuple[float, float]], noise_level: float = 0.05) -> List[Tuple[float, float]]:
        """Add random noise peaks to spectrum."""
        noisy_ions = list(ions)

        # Add random noise peaks
        n_noise_peaks = int(len(ions) * noise_level * 10)
        for _ in range(n_noise_peaks):
            mz = random.uniform(100, 2000)
            intensity = random.uniform(50, 500)
            noisy_ions.append((mz, intensity))

        return sorted(noisy_ions, key=lambda x: x[0])

    def generate_spectrum(self, peptide_sequence: str, spectrum_id: int, charge: int = 2) -> Dict:
        """Generate a complete MS/MS spectrum for a peptide."""
        # Generate fragment ions
        b_ions = self.generate_b_ions(peptide_sequence)
        y_ions = self.generate_y_ions(peptide_sequence)

        # Combine and add noise
        all_ions = b_ions + y_ions
        all_ions = self.add_noise(all_ions, noise_level=0.1)

        # Calculate precursor m/z
        peptide_mass = self.calculate_peptide_mass(peptide_sequence)
        precursor_mz = (peptide_mass + charge * self.proton_mass) / charge

        # Find most intense peak
        max_intensity = max(ion[1] for ion in all_ions)

        return {
            "spectrum_id": spectrum_id,
            "peptide_sequence": peptide_sequence,
            "precursor_mz": precursor_mz,
            "charge": charge,
            "retention_time": random.uniform(10, 90),  # minutes
            "peaks": all_ions,
            "base_peak_intensity": max_intensity,
        }

    def write_mgf(self, spectra: List[Dict], output_path: Path):
        """Write spectra to MGF format."""
        with open(output_path, 'w') as f:
            for spectrum in spectra:
                f.write("BEGIN IONS\n")
                f.write(f"TITLE=Spectrum {spectrum['spectrum_id']}\n")
                f.write(f"PEPMASS={spectrum['precursor_mz']:.4f} {spectrum['base_peak_intensity']:.1f}\n")
                f.write(f"CHARGE={spectrum['charge']}+\n")
                f.write(f"RTINSECONDS={spectrum['retention_time']*60:.2f}\n")
                f.write(f"SCANS={spectrum['spectrum_id']}\n")

                # Write peaks
                for mz, intensity in spectrum['peaks']:
                    f.write(f"{mz:.4f} {intensity:.1f}\n")

                f.write("END IONS\n\n")

        print(f"Wrote {len(spectra)} spectra to {output_path}")

    def write_mzml_minimal(self, spectra: List[Dict], output_path: Path):
        """Write minimal mzML format (placeholder)."""
        with open(output_path, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<indexedmzML xmlns="http://psi.hupo.org/ms/mzml">\n')
            f.write('  <mzML version="1.1.0">\n')
            f.write('    <cvList count="1">\n')
            f.write('      <cv id="MS" fullName="PSI-MS" version="4.1.0" URI="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo"/>\n')
            f.write('    </cvList>\n')
            f.write(f'    <run id="synthetic_run" startTimeStamp="{datetime.now().isoformat()}">\n')
            f.write('      <spectrumList count="{}">\n'.format(len(spectra)))

            for spectrum in spectra:
                f.write(f'        <spectrum id="scan={spectrum["spectrum_id"]}" index="{spectrum["spectrum_id"]-1}">\n')
                f.write(f'          <cvParam cvRef="MS" accession="MS:1000511" name="ms level" value="2"/>\n')
                f.write(f'          <cvParam cvRef="MS" accession="MS:1000744" name="selected ion m/z" value="{spectrum["precursor_mz"]:.4f}"/>\n')
                f.write(f'          <cvParam cvRef="MS" accession="MS:1000041" name="charge state" value="{spectrum["charge"]}"/>\n')
                f.write('        </spectrum>\n')

            f.write('      </spectrumList>\n')
            f.write('    </run>\n')
            f.write('  </mzML>\n')
            f.write('</indexedmzML>\n')

        print(f"Wrote minimal mzML with {len(spectra)} spectra to {output_path}")


def main():
    """Main execution function."""
    output_dir_mgf = Path(__file__).parent.parent / "mass_spectrometry" / "raw_msms_files"
    output_dir_mzml = Path(__file__).parent.parent / "mass_spectrometry" / "mzML"

    output_dir_mgf.mkdir(parents=True, exist_ok=True)
    output_dir_mzml.mkdir(parents=True, exist_ok=True)

    generator = MSMSGenerator()

    # Sample peptides from known proteins
    sample_peptides = [
        "SLADQWSR",       # TP53
        "DLGEGHFK",       # TP53
        "LLGRNSFEVR",     # HBB
        "VNVDEVGGEALGR",  # HBB
        "GIVDQSQQAYQEAGR", # INS
        "FVNQHLCGSHLVEALYLVCGER", # INS
        "SLYNTVATLGCVLPR",  # EGFR
        "IPVAIKTSPK",       # AKT1
    ]

    # Generate 6 MGF files (sample runs)
    for run_id in range(1, 7):
        spectra = []
        for i, peptide in enumerate(sample_peptides, start=1):
            spectrum_id = (run_id - 1) * len(sample_peptides) + i
            charge = random.choice([2, 3])
            spectrum = generator.generate_spectrum(peptide, spectrum_id, charge)
            spectra.append(spectrum)

        output_file = output_dir_mgf / f"sample_run_{run_id}.mgf"
        generator.write_mgf(spectra, output_file)

    # Generate 2 mzML files
    for run_id in range(1, 3):
        spectra = []
        for i, peptide in enumerate(sample_peptides[:4], start=1):
            spectrum_id = (run_id - 1) * 4 + i
            spectrum = generator.generate_spectrum(peptide, spectrum_id, charge=2)
            spectra.append(spectrum)

        output_file = output_dir_mzml / f"sample_run_{run_id}.mzML"
        generator.write_mzml_minimal(spectra, output_file)

    print("\nMS/MS spectrum generation complete!")


if __name__ == "__main__":
    main()
