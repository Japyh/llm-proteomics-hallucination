"""
Figure 4: Hallucination Rate Distribution by Error Taxonomy

Generates a horizontal bar chart showing the distribution of hallucination
types across the taxonomy (factual errors, confabulation, inconsistency, etc.).
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from figure_config import setup_matplotlib, get_output_dir

COLORS = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377']


def generate_data():
    categories = [
        'Factual Errors\n(Incorrect Info)',
        'Confabulation\n(Invented Details)',
        'Inconsistency\n(Self-Contradiction)',
        'Attribution Errors\n(Wrong Source)',
        'Omission\n(Missing Critical Info)',
        'Overgeneralization'
    ]
    rates = [35.2, 28.4, 18.7, 12.3, 3.8, 1.6]
    return categories, rates


def create_figure():
    setup_matplotlib()
    categories, rates = generate_data()
    fig, ax = plt.subplots(figsize=(6.0, 4.0))

    y_pos = np.arange(len(categories))
    bars = ax.barh(y_pos, rates, color=COLORS,
                    alpha=0.8, edgecolor='black', linewidth=0.5)

    # Add value labels
    for i, (bar, rate) in enumerate(zip(bars, rates)):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{rate:.1f}%',
                ha='left', va='center', fontsize=9, fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.set_xlabel('Percentage of Hallucinations (%)', fontweight='bold')
    ax.set_title('Distribution of Hallucination Types', fontweight='bold', pad=10)
    ax.set_xlim(0, max(rates) + 10)
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    return fig


def save_figure(fig, output_dir=None):
    if output_dir is None:
        output_dir = get_output_dir()

    fig.savefig(output_dir / 'figure4_taxonomy_distribution.pdf',
                format='pdf', bbox_inches='tight')
    fig.savefig(output_dir / 'figure4_taxonomy_distribution.png',
                format='png', bbox_inches='tight', dpi=300)
    print(f'Saved: figure4_taxonomy_distribution.pdf/.png')


def main():
    print("Generating Figure 4: Taxonomy Distribution...")
    fig = create_figure()
    save_figure(fig)
    print("Done!")


if __name__ == '__main__':
    main()
