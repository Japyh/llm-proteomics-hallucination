"""
Figure 8: Ethical Framework Pentagon

Pentagon diagram showing the five key ethical considerations.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from figure_config import setup_matplotlib, get_output_dir


def create_figure():
    setup_matplotlib()
    fig, ax = plt.subplots(figsize=(5.0, 5.0))

    # Pentagon vertices
    angles = np.linspace(0, 2*np.pi, 6)
    x = np.cos(angles - np.pi/2)
    y = np.sin(angles - np.pi/2)

    # Draw pentagon
    ax.plot(x, y, 'k-', linewidth=2)
    ax.fill(x, y, color='#4477AA', alpha=0.2)

    # Labels
    labels = ['Patient\nSafety', 'Data\nPrivacy', 'Transparency',
              'Accountability', 'Beneficence']

    for i, label in enumerate(labels):
        ax.text(x[i]*1.25, y[i]*1.25, label,
                ha='center', va='center',
                fontsize=10, fontweight='bold')

    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.8, 1.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Ethical Framework for Clinical AI',
                 fontweight='bold', fontsize=12, pad=20)

    plt.tight_layout()
    return fig


def save_figure(fig, output_dir=None):
    if output_dir is None:
        output_dir = get_output_dir()
    fig.savefig(output_dir / 'figure8_ethical_framework.pdf',
                format='pdf', bbox_inches='tight')
    fig.savefig(output_dir / 'figure8_ethical_framework.png',
                format='png', bbox_inches='tight', dpi=300)
    print('Saved: figure8_ethical_framework.pdf/.png')


def main():
    print("Generating Figure 8: Ethical Framework...")
    fig = create_figure()
    save_figure(fig)
    print("Done!")


if __name__ == '__main__':
    main()
