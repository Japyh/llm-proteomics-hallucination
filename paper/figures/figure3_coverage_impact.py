"""
Figure 3: Impact of Database Coverage on Hallucination Rates

Generates a stacked bar chart showing how hallucination rates vary
with database coverage levels (well-covered vs poorly-covered proteins).
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, Tuple

from figure_config import setup_matplotlib, get_output_dir, COLORS


def generate_data() -> Dict[str, Dict[str, float]]:
    """
    Generate synthetic coverage impact data.

    Returns:
        Dictionary with coverage data for each model
    """
    data = {
        'GPT-4': {
            'Well-Covered\n(>1000 refs)': 12.3,
            'Moderate\n(100-1000 refs)': 23.7,
            'Poorly-Covered\n(<100 refs)': 41.2
        },
        'Claude 3': {
            'Well-Covered\n(>1000 refs)': 9.8,
            'Moderate\n(100-1000 refs)': 18.4,
            'Poorly-Covered\n(<100 refs)': 32.1
        },
        'Gemini Pro': {
            'Well-Covered\n(>1000 refs)': 18.5,
            'Moderate\n(100-1000 refs)': 31.2,
            'Poorly-Covered\n(<100 refs)': 51.7
        }
    }

    return data


def create_figure() -> plt.Figure:
    """
    Create Figure 3: Coverage Impact Chart.

    Returns:
        matplotlib Figure object
    """
    setup_matplotlib()
    data = generate_data()

    # Prepare data for plotting
    models = list(data.keys())
    coverage_levels = list(data['GPT-4'].keys())

    # Extract rates for each coverage level
    well_covered = [data[model][coverage_levels[0]] for model in models]
    moderate = [data[model][coverage_levels[1]] for model in models]
    poorly_covered = [data[model][coverage_levels[2]] for model in models]

    # Create figure
    fig, ax = plt.subplots(figsize=(4.0, 3.5))

    # Set up bar positions
    x = np.arange(len(models))
    width = 0.6

    # Create grouped bars
    p1 = ax.bar(x, well_covered, width,
                label='Well-Covered (>1000 refs)',
                color=COLORS['well_covered'],
                alpha=0.9,
                edgecolor='black',
                linewidth=0.5)

    p2 = ax.bar(x, moderate, width,
                bottom=well_covered,
                label='Moderate (100-1000 refs)',
                color=COLORS['moderate'],
                alpha=0.9,
                edgecolor='black',
                linewidth=0.5)

    bottom_for_poor = [wc + mod for wc, mod in zip(well_covered, moderate)]
    p3 = ax.bar(x, poorly_covered, width,
                bottom=bottom_for_poor,
                label='Poorly-Covered (<100 refs)',
                color=COLORS['poorly_covered'],
                alpha=0.9,
                edgecolor='black',
                linewidth=0.5)

    # Add value labels
    for bars, rates in zip([p1, p2, p3],
                            [well_covered, moderate, poorly_covered]):
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            y_pos = bar.get_y() + height / 2
            ax.text(bar.get_x() + bar.get_width() / 2, y_pos,
                    f'{rate:.1f}%',
                    ha='center', va='center',
                    fontsize=7, fontweight='bold',
                    color='white' if height > 10 else 'black')

    # Customize axes
    ax.set_ylabel('Cumulative Hallucination Rate (%)', fontweight='bold')
    ax.set_xlabel('Large Language Model', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace(' ', '\n') for m in models])
    ax.set_ylim(0, 110)

    # Add legend
    ax.legend(loc='upper left', frameon=True, fancybox=False,
              edgecolor='black', framealpha=0.95)

    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    # Add title
    ax.set_title('Database Coverage Impact on Hallucination Rates',
                 fontweight='bold', pad=10)

    # Add caption
    fig.text(0.5, -0.05,
             'Stacked bars show hallucination rates for proteins with different '
             'levels of database coverage. Coverage measured by UniProt citations.',
             ha='center', fontsize=7, style='italic', wrap=True)

    plt.tight_layout()

    return fig


def save_figure(fig: plt.Figure, output_dir: Path = None) -> None:
    """Save figure in multiple formats."""
    if output_dir is None:
        output_dir = get_output_dir()

    pdf_path = output_dir / 'figure3_coverage_impact.pdf'
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight')
    print(f'Saved: {pdf_path}')

    png_path = output_dir / 'figure3_coverage_impact.png'
    fig.savefig(png_path, format='png', bbox_inches='tight', dpi=300)
    print(f'Saved: {png_path}')


def main():
    """Main execution function."""
    print("Generating Figure 3: Coverage Impact...")
    fig = create_figure()
    save_figure(fig)
    print("Done!")


if __name__ == '__main__':
    main()
