"""
Figure 5: Detection Framework Performance Metrics

Grouped bar chart showing precision, recall, and F1 scores for the
four-stage hallucination detection framework.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from figure_config import setup_matplotlib, get_output_dir, COLORS


def generate_data():
    stages = ['Database\nValidation', 'Logical\nConsistency',
              'Multi-Response\nAnalysis', 'Combined\nPipeline']
    precision = [0.92, 0.68, 0.75, 0.87]
    recall = [0.61, 0.84, 0.79, 0.76]
    f1 = [0.73, 0.75, 0.77, 0.81]
    return stages, precision, recall, f1


def create_figure():
    setup_matplotlib()
    stages, precision, recall, f1 = generate_data()
    fig, ax = plt.subplots(figsize=(6.0, 3.5))

    x = np.arange(len(stages))
    width = 0.25

    ax.bar(x - width, precision, width, label='Precision',
           color=COLORS['precision'], alpha=0.8, edgecolor='black', linewidth=0.5)
    ax.bar(x, recall, width, label='Recall',
           color=COLORS['recall'], alpha=0.8, edgecolor='black', linewidth=0.5)
    ax.bar(x + width, f1, width, label='F1 Score',
           color=COLORS['f1'], alpha=0.8, edgecolor='black', linewidth=0.5)

    ax.set_ylabel('Score', fontweight='bold')
    ax.set_xlabel('Detection Stage', fontweight='bold')
    ax.set_title('Hallucination Detection Performance', fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(stages)
    ax.set_ylim(0, 1.0)
    ax.legend(loc='upper right', frameon=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    return fig


def save_figure(fig, output_dir=None):
    if output_dir is None:
        output_dir = get_output_dir()
    fig.savefig(output_dir / 'figure5_detection_performance.pdf',
                format='pdf', bbox_inches='tight')
    fig.savefig(output_dir / 'figure5_detection_performance.png',
                format='png', bbox_inches='tight', dpi=300)
    print('Saved: figure5_detection_performance.pdf/.png')


def main():
    print("Generating Figure 5: Detection Performance...")
    fig = create_figure()
    save_figure(fig)
    print("Done!")


if __name__ == '__main__':
    main()
