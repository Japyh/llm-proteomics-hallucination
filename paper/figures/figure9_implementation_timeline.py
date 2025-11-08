"""
Figure 9: Implementation and Validation Timeline

Gantt-style timeline showing the phases of the research study.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

plt.rcParams.update({'font.family': 'serif', 'font.size': 10,
                     'figure.dpi': 300, 'savefig.dpi': 300})


def create_figure():
    fig, ax = plt.subplots(figsize=(7.0, 4.0))

    phases = [
        ('Dataset Preparation', 0, 2, '#4477AA'),
        ('LLM Evaluation', 1.5, 3, '#EE6677'),
        ('Detection Development', 3, 2.5, '#228833'),
        ('Expert Validation', 4.5, 2, '#CCBB44'),
        ('Statistical Analysis', 5.5, 1.5, '#66CCEE'),
        ('Manuscript Writing', 6, 2, '#AA3377'),
    ]

    y_pos = range(len(phases))

    for i, (label, start, duration, color) in enumerate(phases):
        ax.barh(i, duration, left=start, height=0.6,
                color=color, alpha=0.7, edgecolor='black', linewidth=1)
        ax.text(start + duration/2, i, label,
                ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')

    ax.set_yticks([])
    ax.set_xlabel('Months', fontweight='bold')
    ax.set_xlim(0, 8.5)
    ax.set_title('Research Study Timeline',
                 fontweight='bold', fontsize=12, pad=10)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    return fig


def save_figure(fig, output_dir=None):
    if output_dir is None:
        output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / 'figure9_implementation_timeline.pdf',
                format='pdf', bbox_inches='tight')
    fig.savefig(output_dir / 'figure9_implementation_timeline.png',
                format='png', bbox_inches='tight', dpi=300)
    print('Saved: figure9_implementation_timeline.pdf/.png')


def main():
    print("Generating Figure 9: Implementation Timeline...")
    fig = create_figure()
    save_figure(fig)
    print("Done!")


if __name__ == '__main__':
    main()
