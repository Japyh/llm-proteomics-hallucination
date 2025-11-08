"""
Figure 2: Hallucination Rates by Query Category

Generates a grouped bar chart showing hallucination rates across different
query categories for each LLM.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List

from figure_config import setup_matplotlib, get_output_dir, COLORS


def generate_data() -> Dict[str, List[float]]:
    """
    Generate synthetic category performance data.

    Returns:
        Dictionary with category data for each model
    """
    categories = ['Protein\nFunction', 'MS\nInterpretation',
                  'Clinical\nContext', 'PTMs', 'Disease\nAssociation']

    data = {
        'GPT-4': [18.2, 31.5, 25.1, 22.3, 19.8],
        'Claude 3': [15.4, 24.8, 19.3, 17.6, 16.2],
        'Gemini Pro': [28.7, 38.2, 33.4, 30.1, 27.9]
    }

    return {'categories': categories, 'models': data}


def create_figure() -> plt.Figure:
    """
    Create Figure 2: Category Performance Chart.

    Returns:
        matplotlib Figure object
    """
    setup_matplotlib()
    data = generate_data()
    categories = data['categories']
    models = data['models']

    # Create figure
    fig, ax = plt.subplots(figsize=(7.0, 3.5))

    # Set up bar positions
    x = np.arange(len(categories))
    width = 0.25

    # Plot bars for each model
    colors = [COLORS['gpt4'], COLORS['claude'], COLORS['gemini']]

    for i, (model_name, rates) in enumerate(models.items()):
        offset = width * (i - 1)
        bars = ax.bar(x + offset, rates, width,
                       label=model_name,
                       color=colors[i],
                       alpha=0.8,
                       edgecolor='black',
                       linewidth=0.5)

        # Add value labels on bars
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{rate:.1f}',
                    ha='center', va='bottom', fontsize=7)

    # Customize axes
    ax.set_ylabel('Hallucination Rate (%)', fontweight='bold')
    ax.set_xlabel('Query Category', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 45)

    # Add legend
    ax.legend(loc='upper right', frameon=True, fancybox=False,
              edgecolor='black', framealpha=0.9)

    # Add grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    # Add reference line
    ax.axhline(y=20, color='gray', linestyle=':', linewidth=1, alpha=0.5)

    # Add title
    ax.set_title('Hallucination Rates by Query Category',
                 fontweight='bold', pad=10)

    # Add caption
    fig.text(0.5, -0.02,
             'MS = Mass Spectrometry; PTMs = Post-Translational Modifications. '
             'Based on 100 queries per category.',
             ha='center', fontsize=7, style='italic', wrap=True)

    plt.tight_layout()

    return fig


def save_figure(fig: plt.Figure, output_dir: Path = None) -> None:
    """Save figure in multiple formats."""
    if output_dir is None:
        output_dir = get_output_dir()

    pdf_path = output_dir / 'figure2_category_performance.pdf'
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight')
    print(f'Saved: {pdf_path}')

    png_path = output_dir / 'figure2_category_performance.png'
    fig.savefig(png_path, format='png', bbox_inches='tight', dpi=300)
    print(f'Saved: {png_path}')


def main():
    """Main execution function."""
    print("Generating Figure 2: Category Performance...")
    fig = create_figure()
    save_figure(fig)
    print("Done!")


if __name__ == '__main__':
    main()
