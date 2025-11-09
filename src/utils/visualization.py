"""Visualization utilities."""
import matplotlib.pyplot as plt
import seaborn as sns

def set_plot_style(style='seaborn-v0_8-paper'):
    """Set consistent plot style."""
    plt.style.use(style)
    sns.set_palette("colorblind")

def save_figure(fig, filename, dpi=300):
    """Save figure with consistent settings."""
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
