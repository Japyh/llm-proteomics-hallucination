# Manuscript Compilation Guide

## LLM Proteomics Hallucination Study - The Lancet Digital Health

---

## Prerequisites

### Required Software
- LaTeX distribution (TeX Live 2023 or later)
- Python 3.10+ (for figure generation)
- R 4.3+ (for table generation)
- Make (for automation)

### LaTeX Packages
All required packages are specified in `latex/packages.tex`. Key packages:
- `lancetdigitalhealth.cls` (journal class file)
- `graphicx`, `booktabs`, `natbib`
- `hyperref`, `cleveref`

## Compilation Steps

### Method 1: Using Makefile (Recommended)

```bash
# From repository root
make paper

# Or step by step
make figures    # Generate all figures
make tables     # Generate all tables
make manuscript # Compile PDF
```

### Method 2: Manual Compilation

#### Step 1: Generate Figures
```bash
cd paper/figures
python generate_figure_1.py
python generate_figure_2.py
python generate_figure_3.py
python generate_figure_4.py
python generate_figure_5.py
python generate_figure_6.py
```

#### Step 2: Generate Tables
```bash
cd paper/tables
Rscript make_table_1_summary.R
Rscript make_table_2_model_perf.R
Rscript make_table_3_domainwise.R
Rscript make_table_4_multivariable.R
Rscript make_table_5_bias_audit.R
```

#### Step 3: Compile LaTeX
```bash
cd paper/latex
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex  # Second pass for references
```

### Method 3: Using Overleaf

1. Upload all files to Overleaf project
2. Set compiler to `pdfLaTeX`
3. Main document: `manuscript.tex`
4. Compile (Ctrl+S or ⌘S)

## File Structure

```
paper/
├── manuscript.tex          # Main manuscript
├── abstract.tex            # Abstract (included)
├── latex/
│   ├── lancetdigitalhealth.cls
│   ├── macros.tex
│   ├── packages.tex
│   ├── notation.tex
│   └── references.bib
├── figures/
│   └── output/            # All figures must be here
├── tables/
│   └── outputs/           # All table CSVs/Excel
└── supplementary/
    └── supplementary.tex  # Supplementary material
```

## Figure Requirements

### Format Specifications (The Lancet Digital Health)
- **Main figures**: TIFF, 600 DPI, RGB color
- **Minimum width**: 85 mm (single column) or 170 mm (double column)
- **Font size**: ≥8 pt in final size
- **File size**: <10 MB per figure

### Our Figures
All figures generated at 600 DPI in both PNG (preview) and TIFF (submission):

| Figure | Filename | Description |
|--------|----------|-------------|
| 1 | fig1_hallucination_rate_vs_complexity | Bar chart by model and complexity |
| 2 | fig2_heatmap_severity | Heatmap of severity by domain |
| 3 | fig3_consistency_matrix | Confusion matrix |
| 4 | fig4_calibration_curve | Calibration curves |
| 5 | fig5_domain_breakdown | Domain-specific error profiles |
| 6 | fig6_bayesian_posterior | Posterior distributions |

## Table Requirements

- **Format**: Should be editable (not images)
- **Size**: Maximum width 170 mm
- **Font**: Arial, 10 pt minimum
- **Numbers**: Rounded appropriately (2-3 decimal places)
- **Statistical values**: Report with 95% CI where applicable

## Common Issues

### Issue 1: Missing Figures
```
LaTeX Error: File 'fig1_hallucination_rate_vs_complexity.png' not found
```
**Solution**: Run figure generation scripts first.

### Issue 2: Bibliography Not Updating
**Solution**: Run BibTeX, then pdfLaTeX twice:
```bash
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

### Issue 3: Overfull hbox
**Solution**: LaTeX cannot break lines properly. Add `\sloppy` or manual line breaks.

### Issue 4: Unicode Characters
**Solution**: Use `\usepackage[utf8]{inputenc}` and ensure text editor saves as UTF-8.

## Submission Checklist

Before submission to The Lancet Digital Health:

- [ ] Manuscript compiled without errors
- [ ] All 6 figures included (TIFF, 600 DPI)
- [ ] All 5 tables included (editable format)
- [ ] References formatted (Vancouver style)
- [ ] Word count ≤4,000 words (excluding abstract, refs, tables)
- [ ] Abstract ≤300 words, structured
- [ ] Supplementary material compiled separately
- [ ] TRIPOD-AI checklist completed
- [ ] Author contributions (CRediT)
- [ ] Conflicts of interest declared
- [ ] Funding statement included
- [ ] Data availability statement
- [ ] Code availability statement
- [ ] Ethics approval documented

## Contact

For compilation issues:
- GitHub Issues: [Add repository URL]
- Email: [Add contact]

---

**Last Updated**: 2025-01-15
**Document Version**: 1.0
