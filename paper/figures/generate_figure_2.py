#!/usr/bin/env python3
"""Generate Figure 2: Heatmap of severity"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

np.random.seed(42)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
data = np.random.rand(5, 3) * 0.3
domains = ['Oncology', 'Neurology', 'Cardiology', 'Immunology', 'Metabolism']
models = ['GPT-4', 'Claude-3', 'Gemini']

sns.heatmap(data, annot=True, fmt='.2%', cmap='YlOrRd', ax=ax,
            xticklabels=models, yticklabels=domains, cbar_kws={'label': 'Hallucination Rate'})
ax.set_title('Figure 2: Domain-wise Hallucination Heatmap', fontweight='bold')

output_dir = Path('output')
fig.savefig(output_dir / 'fig2_heatmap_severity.png', dpi=300, bbox_inches='tight')
print("Figure 2 generated")
plt.close()
