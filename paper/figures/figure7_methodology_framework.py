"""
Figure 7: Four-Stage Hallucination Detection Methodology Framework

Flow diagram showing the four stages of the detection pipeline.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

plt.rcParams.update({'font.family': 'serif', 'font.size': 10,
                     'figure.dpi': 300, 'savefig.dpi': 300})


def create_figure():
    fig, ax = plt.subplots(figsize=(7.0, 4.5))

    # Stage boxes
    stages = [
        ("Stage 1:\nDatabase\nValidation", 0.15, 0.7),
        ("Stage 2:\nLogical\nConsistency", 0.40, 0.7),
        ("Stage 3:\nMulti-Response\nAnalysis", 0.65, 0.7),
        ("Stage 4:\nCombined\nPipeline", 0.90, 0.7),
    ]

    colors = ['#4477AA', '#EE6677', '#228833', '#CCBB44']

    for i, (label, x, y) in enumerate(stages):
        rect = mpatches.FancyBboxPatch((x-0.1, y-0.12), 0.2, 0.24,
                                        boxstyle="round,pad=0.01",
                                        facecolor=colors[i], edgecolor='black',
                                        linewidth=2, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')

        # Add arrows between stages
        if i < len(stages) - 1:
            ax.annotate('', xy=(stages[i+1][1]-0.12, y),
                        xytext=(x+0.12, y),
                        arrowprops=dict(arrowstyle='->', lw=2, color='black'))

    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Four-Stage Hallucination Detection Framework',
                 fontweight='bold', fontsize=12, pad=20)

    plt.tight_layout()
    return fig


def save_figure(fig, output_dir=None):
    if output_dir is None:
        output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / 'figure7_methodology_framework.pdf',
                format='pdf', bbox_inches='tight')
    fig.savefig(output_dir / 'figure7_methodology_framework.png',
                format='png', bbox_inches='tight', dpi=300)
    print('Saved: figure7_methodology_framework.pdf/.png')


def main():
    print("Generating Figure 7: Methodology Framework...")
    fig = create_figure()
    save_figure(fig)
    print("Done!")


if __name__ == '__main__':
    main()
