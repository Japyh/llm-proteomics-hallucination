# Analysis Module

Statistical analysis and visualization tools.

---

## Modules

### metrics.py

Calculate performance metrics.

**Functions**:
- `hallucination_rate()`: Calculate hallucination rate
- `cohen_kappa()`: Inter-rater reliability
- `confusion_matrix()`: Classification metrics

### statistical_tests.py

Statistical hypothesis testing.

**Functions**:
- `chi_square_test()`: Chi-square test for independence
- `logistic_regression()`: Multivariable regression
- `bonferroni_correction()`: Multiple comparison correction

### visualization.py

Plotting and visualization functions.

**Functions**:
- `plot_hallucination_rates()`: Bar plots by model/complexity
- `plot_severity_heatmap()`: Heatmap visualization
- `plot_calibration()`: Calibration plots

---

**Usage**:
```python
from src.analysis.statistical_tests import chi_square_test

result = chi_square_test(data, group1='GPT-4', group2='Claude')
print(f"p-value: {result['p_value']}")
```
