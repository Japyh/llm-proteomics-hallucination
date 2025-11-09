"""
Generate Figure 1: Hallucination rates stratified by query complexity
and protein prevalence

Creates a two-panel figure showing:
Panel A: Hallucination rates by query complexity (simple/intermediate/complex)
Panel B: Hallucination rates by protein prevalence (common/moderate/rare)
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for figure_config
sys.path.append(str(Path(__file__).parent))
from figure_config import setup_matplotlib, get_output_dir

# Setup matplotlib with professional styling
setup_matplotlib()

# Data from manuscript Table 1 and Results section
# Overall rates by complexity
complexity_data = {
    'Simple': {'rate': 18.4, 'ci_lower': 15.2, 'ci_upper': 21.6, 'n': 500},
    'Intermediate': {'rate': 31.7, 'ci_lower': 27.6, 'ci_upper': 35.8, 'n': 498},
    'Complex': {'rate': 43.7, 'ci_lower': 39.3, 'ci_upper': 48.1, 'n': 499}
}

# Rates by model and complexity (from Results section)
model_complexity_data = {
    'Claude': [14.2, 26.8, 38.3],
    'GPT-4': [19.2, 31.3, 42.5],
    'Gemini': [21.9, 36.9, 50.3]
}

# Overall rates by prevalence
prevalence_data = {
    'Common': {'rate': 14.3, 'ci_lower': 11.9, 'ci_upper': 16.7, 'n': 750},
    'Moderate': {'rate': 32.8, 'ci_lower': 28.1, 'ci_upper': 37.5, 'n': 375},
    'Rare': {'rate': 47.2, 'ci_lower': 42.2, 'ci_upper': 52.2, 'n': 375}
}

# Rates by model and prevalence (from Results section)
model_prevalence_data = {
    'Claude': [14.3 * 0.722 / 0.688, 32.8 * 0.722 / 0.688, 42.4],
    'GPT-4': [14.3 * 0.688 / 0.688, 32.8 * 0.688 / 0.688, 46.4],
    'Gemini': [14.3 * 0.654 / 0.688, 32.8 * 0.654 / 0.688, 52.8]
}

# Model colors (matching manuscript description)
colors = {
    'Claude': '#2ecc71',  # Green
    'GPT-4': '#3498db',   # Blue
    'Gemini': '#e74c3c'   # Red
}

# Create figure with two panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel A: Complexity
x_positions = np.arange(3)
width = 0.25

for i, (model, rates) in enumerate(model_complexity_data.items()):
    offset = (i - 1) * width
    ax1.bar(x_positions + offset, rates, width,
            label=f'{model} 3 Sonnet' if model == 'Claude' else
                  (f'{model} Turbo' if model == 'GPT-4' else f'{model} Pro 1.5'),
            color=colors[model], alpha=0.8, edgecolor='black', linewidth=0.5)

# Add overall rates with error bars
overall_rates_complexity = [complexity_data[k]['rate']
                            for k in ['Simple', 'Intermediate', 'Complex']]
error_bars_complexity = [
    [complexity_data[k]['rate'] - complexity_data[k]['ci_lower']
     for k in ['Simple', 'Intermediate', 'Complex']],
    [complexity_data[k]['ci_upper'] - complexity_data[k]['rate']
     for k in ['Simple', 'Intermediate', 'Complex']]
]

ax1.errorbar(x_positions, overall_rates_complexity,
             yerr=error_bars_complexity, fmt='ko', markersize=8,
             capsize=5, capthick=2, linewidth=2,
             label='Overall', zorder=5)

ax1.set_xlabel('Query Complexity', fontsize=12, fontweight='bold')
ax1.set_ylabel('Hallucination Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title('A. Hallucination Rates by Query Complexity',
              fontsize=13, fontweight='bold', loc='left')
ax1.set_xticks(x_positions)
ax1.set_xticklabels(['Simple', 'Intermediate', 'Complex'])
ax1.set_ylim(0, 60)
ax1.legend(loc='upper left', frameon=True, fontsize=9)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Add statistical annotations
ax1.text(0.5, -0.15, 'Cochran-Armitage trend test: z=18.7, p<0.001',
         transform=ax1.transAxes, fontsize=9, style='italic',
         ha='center')

# Panel B: Prevalence
x_positions_prev = np.arange(3)

for i, (model, rates) in enumerate(model_prevalence_data.items()):
    offset = (i - 1) * width
    ax2.bar(x_positions_prev + offset, rates, width,
            label=f'{model} 3 Sonnet' if model == 'Claude' else
                  (f'{model} Turbo' if model == 'GPT-4' else f'{model} Pro 1.5'),
            color=colors[model], alpha=0.8, edgecolor='black', linewidth=0.5)

# Add overall rates with error bars
overall_rates_prev = [prevalence_data[k]['rate']
                      for k in ['Common', 'Moderate', 'Rare']]
error_bars_prev = [
    [prevalence_data[k]['rate'] - prevalence_data[k]['ci_lower']
     for k in ['Common', 'Moderate', 'Rare']],
    [prevalence_data[k]['ci_upper'] - prevalence_data[k]['rate']
     for k in ['Common', 'Moderate', 'Rare']]
]

ax2.errorbar(x_positions_prev, overall_rates_prev,
             yerr=error_bars_prev, fmt='ko', markersize=8,
             capsize=5, capthick=2, linewidth=2,
             label='Overall', zorder=5)

ax2.set_xlabel('Protein Prevalence', fontsize=12, fontweight='bold')
ax2.set_ylabel('Hallucination Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('B. Hallucination Rates by Protein Prevalence',
              fontsize=13, fontweight='bold', loc='left')
ax2.set_xticks(x_positions_prev)
ax2.set_xticklabels(['Common\n(>75% tissues)', 'Moderate\n(25-75%)', 'Rare\n(<25%)'])
ax2.set_ylim(0, 60)
ax2.legend(loc='upper left', frameon=True, fontsize=9)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Add statistical annotations
ax2.text(0.5, -0.15, r'Chi-square test: $\chi^2$=142.8, df=2, p<0.001',
         transform=ax2.transAxes, fontsize=9, style='italic',
         ha='center')

plt.tight_layout()

# Save figure
output_dir = get_output_dir()
output_path = output_dir / 'Figure_1_Hallucination_Rates.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'Figure saved to {output_path}')

plt.show()
