"""
Correlation network analysis for feature relationships.
"""

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr
from typing import Optional, Tuple, List


class CorrelationNetwork:
    """Build and analyze correlation networks."""

    def __init__(self, data: pd.DataFrame, method: str = 'spearman'):
        """
        Initialize correlation network.

        Args:
            data: DataFrame with numeric features
            method: Correlation method ('spearman' or 'pearson')
        """
        self.data = data
        self.method = method
        self.corr_matrix = None
        self.graph = None

    def compute_correlations(self, threshold: float = 0.5) -> pd.DataFrame:
        """
        Compute correlation matrix.

        Args:
            threshold: Minimum correlation to include

        Returns:
            Correlation matrix
        """
        if self.method == 'spearman':
            self.corr_matrix = self.data.corr(method='spearman')
        else:
            self.corr_matrix = self.data.corr(method='pearson')

        # Apply threshold
        self.corr_matrix[np.abs(self.corr_matrix) < threshold] = 0

        return self.corr_matrix

    def build_network(self, threshold: float = 0.5):
        """
        Build networkx graph from correlations.

        Args:
            threshold: Minimum correlation for edge creation
        """
        if self.corr_matrix is None:
            self.compute_correlations(threshold)

        self.graph = nx.Graph()

        # Add nodes
        for feature in self.corr_matrix.columns:
            self.graph.add_node(feature)

        # Add edges
        for i, feat1 in enumerate(self.corr_matrix.columns):
            for j, feat2 in enumerate(self.corr_matrix.columns):
                if i < j:
                    corr = self.corr_matrix.iloc[i, j]
                    if abs(corr) >= threshold:
                        self.graph.add_edge(
                            feat1, feat2,
                            weight=abs(corr),
                            correlation=corr
                        )

    def get_central_features(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Identify central features using degree centrality.

        Args:
            top_n: Number of top features to return

        Returns:
            List of (feature, centrality_score) tuples
        """
        if self.graph is None:
            self.build_network()

        centrality = nx.degree_centrality(self.graph)
        sorted_features = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

        return sorted_features[:top_n]

    def plot_network(
        self,
        save_path: Optional[str] = None,
        node_size: int = 1000,
        figsize: Tuple[int, int] = (12, 10)
    ):
        """
        Visualize correlation network.

        Args:
            save_path: Path to save figure
            node_size: Size of nodes
            figsize: Figure dimensions
        """
        if self.graph is None:
            self.build_network()

        fig, ax = plt.subplots(figsize=figsize)

        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)

        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph, pos,
            node_color='lightblue',
            node_size=node_size,
            alpha=0.8,
            ax=ax
        )

        # Draw edges
        edges = self.graph.edges()
        weights = [self.graph[u][v]['weight'] for u, v in edges]

        nx.draw_networkx_edges(
            self.graph, pos,
            width=[w * 3 for w in weights],
            alpha=0.5,
            ax=ax
        )

        # Draw labels
        nx.draw_networkx_labels(
            self.graph, pos,
            font_size=10,
            font_weight='bold',
            ax=ax
        )

        ax.set_title(f'Feature Correlation Network ({self.method.capitalize()})',
                    fontsize=14, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
