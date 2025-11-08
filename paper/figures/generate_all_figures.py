"""
Master script to generate all 9 figures for the paper.

This script runs all individual figure generation scripts and creates
all publication-quality figures in both PDF and PNG formats.
"""

import subprocess
import sys
from pathlib import Path
from typing import List


def run_figure_script(script_name: str) -> bool:
    """
    Run a single figure generation script.

    Args:
        script_name: Name of the Python script to run

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\n{'='*60}")
        print(f"Running: {script_name}")
        print('='*60)

        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(result.stdout)
            print(f"SUCCESS: {script_name}")
            return True
        else:
            print(f"ERROR in {script_name}:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: {script_name} took too long to execute")
        return False
    except Exception as e:
        print(f"EXCEPTION in {script_name}: {e}")
        return False


def main():
    """Main execution function."""
    print("="*60)
    print("GENERATING ALL PAPER FIGURES")
    print("="*60)
    print(f"Output directory: {Path(__file__).parent / 'output'}")
    print()

    # List of all figure scripts
    figure_scripts = [
        'figure1_hallucination_rates.py',
        'figure2_category_performance.py',
        'figure3_coverage_impact.py',
        'figure4_taxonomy_distribution.py',
        'figure5_detection_performance.py',
        'figure6_clinical_risk.py',
        'figure7_methodology_framework.py',
        'figure8_ethical_framework.py',
        'figure9_implementation_timeline.py',
    ]

    # Track results
    results = {}
    total = len(figure_scripts)
    successful = 0

    # Run each script
    for script in figure_scripts:
        success = run_figure_script(script)
        results[script] = success
        if success:
            successful += 1

    # Print summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)

    for script, success in results.items():
        status = "OK" if success else "FAILED"
        symbol = "+" if success else "X"
        print(f"[{symbol}] {script:45s} {status}")

    print("="*60)
    print(f"Successful: {successful}/{total}")
    print(f"Failed: {total - successful}/{total}")

    if successful == total:
        print("\nALL FIGURES GENERATED SUCCESSFULLY!")
        print(f"Figures saved to: {Path(__file__).parent / 'output'}")
        return 0
    else:
        print(f"\nWARNING: {total - successful} figures failed to generate")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
