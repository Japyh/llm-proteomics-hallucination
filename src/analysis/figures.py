"""
Figure generation for publication.

This module creates publication-ready figures for The Lancet Digital Health submission.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Tuple


# Set publication style
def set_publication_style():
    """Configure matplotlib for publication-quality figures."""
    # The Lancet Digital Health style
    plt.style.use('seaborn-v0_8-paper')

    mpl.rcParams['font.family'] = 'Arial'
    mpl.rcParams['font.size'] = 10
    mpl.rcParams['axes.labelsize'] = 11
    mpl.rcParams['axes.titlesize'] = 12
    mpl.rcParams['xtick.labelsize'] = 9
    mpl.rcParams['ytick.labelsize'] = 9
    mpl.rcParams['legend.fontsize'] = 9
    mpl.rcParams['figure.titlesize'] = 13
    mpl.rcParams['figure.dpi'] = 300
    mpl.rcParams['savefig.dpi'] = 600
    mpl.rcParams['savefig.format'] = 'tiff'
    mpl.rcParams['axes.linewidth'] = 0.8
    mpl.rcParams['grid.linewidth'] = 0.5
    mpl.rcParams['lines.linewidth'] = 1.5


class FigureGenerator:
    """Generate publication-ready figures."""

    def __init__(self, output_dir: Path, style: str = 'lancet'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        set_publication_style()

    def figure_1_hallucination_rates(
        self,
        data: pd.DataFrame,
        save_name: str = 'fig1_hallucination_rate_vs_complexity.png'
    ):
        """
        Figure 1: Hallucination rates by model and query complexity.

        Args:
            data: DataFrame with columns ['model', 'complexity', 'hallucination_rate']
            save_name: Output filename
        """
        fig, ax = plt.subplots(figsize=(8, 6))

        # Bar plot with error bars
        models = data['model'].unique()
        complexity_levels = ['low', 'medium', 'high']

        x = np.arange(len(complexity_levels))
        width = 0.15
        colors = sns.color_palette("colorblind", n_colors=len(models))

        for i, model in enumerate(models):
            model_data = data[data['model'] == model]
            rates = [
                model_data[model_data['complexity'] == c]['hallucination_rate'].mean()
                for c in complexity_levels
            ]
            ax.bar(x + i * width, rates, width, label=model, color=colors[i], alpha=0.8)

        ax.set_xlabel('Query Complexity', fontweight='bold')
        ax.set_ylabel('Hallucination Rate', fontweight='bold')
        ax.set_title('Hallucination Rates by Model and Query Complexity')
        ax.set_xticks(x + width * (len(models) - 1) / 2)
        ax.set_xticklabels(complexity_levels)
        ax.legend(loc='upper left', frameon=True)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / save_name, dpi=600, bbox_inches='tight')
        plt.close()

    def figure_2_severity_heatmap(
        self,
        data: pd.DataFrame,
        save_name: str = 'fig2_heatmap_severity.png'
    ):
        """
        Figure 2: Heatmap of hallucination severity by model and category.

        Args:
            data: DataFrame pivot table [models x categories]
            save_name: Output filename
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.heatmap(
            data,
            annot=True,
            fmt='.2f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Mean Severity Score'},
            linewidths=0.5,
            ax=ax
        )

        ax.set_title('Hallucination Severity by Model and Domain', fontweight='bold')
        ax.set_xlabel('Domain Category', fontweight='bold')
        ax.set_ylabel('Model', fontweight='bold')

        plt.tight_layout()
        plt.savefig(self.output_dir / save_name, dpi=600, bbox_inches='tight')
        plt.close()

    def figure_3_calibration_curve(
        self,
        y_true_dict: Dict[str, np.ndarray],
        y_pred_dict: Dict[str, np.ndarray],
        save_name: str = 'fig4_calibration_curve.png'
    ):
        """
        Figure 4: Calibration curves for all models.

        Args:
            y_true_dict: Dict of {model_name: true_labels}
            y_pred_dict: Dict of {model_name: predicted_probs}
            save_name: Output filename
        """
        from sklearn.calibration import calibration_curve

        fig, ax = plt.subplots(figsize=(8, 8))

        colors = sns.color_palette("colorblind", n_colors=len(y_true_dict))

        for i, (model, y_true) in enumerate(y_true_dict.items()):
            y_pred = y_pred_dict[model]
            prob_true, prob_pred = calibration_curve(y_true, y_pred, n_bins=10)

            ax.plot(prob_pred, prob_true, marker='o', linewidth=2,
                   label=model, color=colors[i])

        # Perfect calibration line
        ax.plot([0, 1], [0, 1], 'k--', linewidth=1.5, label='Perfect Calibration')

        ax.set_xlabel('Mean Predicted Probability', fontweight='bold')
        ax.set_ylabel('Fraction of Positives', fontweight='bold')
        ax.set_title('Calibration Curves by Model', fontweight='bold')
        ax.legend(loc='lower right', frameon=True)
        ax.grid(alpha=0.3)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

        plt.tight_layout()
        plt.savefig(self.output_dir / save_name, dpi=600, bbox_inches='tight')
        plt.close()

    def figure_5_domain_breakdown(
        self,
        data: pd.DataFrame,
        save_name: str = 'fig5_domain_breakdown.png'
    ):
        """
        Figure 5: Domain-specific error profiles.

        Args:
            data: DataFrame with domain error rates
            save_name: Output filename
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.ravel()

        domains = data['domain'].unique()[:4]

        for idx, domain in enumerate(domains):
            domain_data = data[data['domain'] == domain]

            axes[idx].barh(
                domain_data['error_type'],
                domain_data['frequency'],
                color=sns.color_palette("Set2")[idx]
            )

            axes[idx].set_title(f'{domain}', fontweight='bold')
            axes[idx].set_xlabel('Frequency (%)')
            axes[idx].grid(axis='x', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / save_name, dpi=600, bbox_inches='tight')
        plt.close()

    def save_highres_tiff(self, figure_name: str):
        """
        Convert PNG to high-resolution TIFF for journal submission.

        Args:
            figure_name: Name of the figure file (without extension)
        """
        from PIL import Image

        png_path = self.output_dir / f"{figure_name}.png"
        tiff_path = self.output_dir / "highres_tiff" / f"{figure_name}_600dpi.tiff"
        tiff_path.parent.mkdir(exist_ok=True)

        if png_path.exists():
            img = Image.open(png_path)
            img.save(tiff_path, dpi=(600, 600), compression='tiff_lzw')
            print(f"Saved high-res TIFF: {tiff_path}")
