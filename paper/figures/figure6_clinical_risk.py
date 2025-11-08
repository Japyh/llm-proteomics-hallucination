"""
Figure 6: Clinical Risk Assessment of Hallucinations

Stacked bar chart showing the distribution of clinical risk levels
(low, moderate, high, severe) for hallucinated responses.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman'],
                     'font.size': 10, 'figure.dpi': 300, 'savefig.dpi': 300})

COLORS = {'low': '#228833', 'moderate': '#CCBB44',
          'high': '#EE8866', 'severe': '#CC3311'}


def generate_data():
    models = ['GPT-4', 'Claude 3', 'Gemini Pro']
    low = [45.2, 52.3, 38.7]
    moderate = [28.4, 26.1, 30.2]
    high = [18.7, 15.3, 22.8]
    severe = [7.7, 6.3, 8.3]
    return models, low, moderate, high, severe


def create_figure():
    models, low, mod, high, sev = generate_data()
    fig, ax = plt.subplots(figsize=(5.0, 3.5))

    x = np.arange(len(models))
    width = 0.6

    p1 = ax.bar(x, low, width, label='Low Risk',
                color=COLORS['low'], alpha=0.9, edgecolor='black', linewidth=0.5)
    p2 = ax.bar(x, mod, width, bottom=low, label='Moderate Risk',
                color=COLORS['moderate'], alpha=0.9, edgecolor='black', linewidth=0.5)
    bottom_high = [l + m for l, m in zip(low, mod)]
    p3 = ax.bar(x, high, width, bottom=bottom_high, label='High Risk',
                color=COLORS['high'], alpha=0.9, edgecolor='black', linewidth=0.5)
    bottom_sev = [l + m + h for l, m, h in zip(low, mod, high)]
    p4 = ax.bar(x, sev, width, bottom=bottom_sev, label='Severe Risk',
                color=COLORS['severe'], alpha=0.9, edgecolor='black', linewidth=0.5)

    ax.set_ylabel('Percentage of Hallucinations (%)', fontweight='bold')
    ax.set_xlabel('Large Language Model', fontweight='bold')
    ax.set_title('Clinical Risk Distribution of Hallucinations', fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace(' ', '\n') for m in models])
    ax.legend(loc='upper right', frameon=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    return fig


def save_figure(fig, output_dir=None):
    if output_dir is None:
        output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / 'figure6_clinical_risk.pdf', format='pdf', bbox_inches='tight')
    fig.savefig(output_dir / 'figure6_clinical_risk.png', format='png', bbox_inches='tight', dpi=300)
    print('Saved: figure6_clinical_risk.pdf/.png')


def main():
    print("Generating Figure 6: Clinical Risk Assessment...")
    fig = create_figure()
    save_figure(fig)
    print("Done!")


if __name__ == '__main__':
    main()
