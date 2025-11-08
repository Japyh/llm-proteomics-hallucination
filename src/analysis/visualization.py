"""Visualization functions for results."""

import matplotlib.pyplot as plt
import seaborn as sns


class Visualization:
    """Generate plots and figures."""

    @staticmethod
    def plot_hallucination_rates(rates: dict, output_path: str = None):
        """Plot hallucination rates by model."""
        plt.figure(figsize=(10, 6))
        plt.bar(rates.keys(), rates.values())
        plt.xlabel("Model")
        plt.ylabel("Hallucination Rate")
        plt.title("Hallucination Rates by LLM Provider")
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.show()
