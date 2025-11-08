"""
Common configuration for all figure generation scripts.
Handles font fallback and path resolution for both script and Jupyter usage.
"""

import os
import matplotlib.pyplot as plt
from pathlib import Path


# Colorblind-friendly palette (Paul Tol)
COLORS = {
    'gpt4': '#4477AA',
    'claude': '#EE6677',
    'gemini': '#228833',
    'baseline': '#CCBB44',
    'well_covered': '#44AA99',
    'moderate': '#DDCC77',
    'poorly_covered': '#CC6677',
    'low': '#228833',
    'high': '#EE8866',
    'severe': '#CC3311',
    'precision': '#4477AA',
    'recall': '#EE6677',
    'f1': '#228833'
}


def setup_matplotlib():
    """
    Configure matplotlib with publication-quality settings.
    Uses fallback fonts if Times New Roman not available.
    """
    plt.rcParams.update({
        # Try Times New Roman, fall back to any serif font
        'font.family': 'serif',
        'font.serif': [
            'Times New Roman',
            'DejaVu Serif',
            'Bitstream Vera Serif',
            'Computer Modern Roman',
            'New Century Schoolbook',
            'Century Schoolbook L',
            'Utopia',
            'ITC Bookman',
            'Bookman',
            'Nimbus Roman No9 L',
            'Times',
            'Palatino',
            'Charter',
            'serif'
        ],
        'font.size': 10,
        'axes.labelsize': 10,
        'axes.titlesize': 11,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1
    })


def get_output_dir():
    """
    Get the output directory for saving figures.
    Handles both script execution and Jupyter notebook usage.

    Returns:
        Path: Output directory path
    """
    try:
        # Try to use __file__ if available (script execution)
        script_dir = Path(__file__).parent
    except NameError:
        # __file__ not defined (Jupyter/interactive)
        script_dir = Path.cwd()
        # If we're in a subdirectory, try to find figures directory
        if not (script_dir / 'output').exists():
            # Check if we're in the repository root
            if (script_dir / 'paper' / 'figures').exists():
                script_dir = script_dir / 'paper' / 'figures'
            # Check if we're in paper directory
            elif (script_dir / 'figures').exists():
                script_dir = script_dir / 'figures'

    output_dir = script_dir / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
