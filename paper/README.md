# Manuscript: Hallucination Rates in Large Language Models for Clinical Proteomics Applications

**Target Journal**: The Lancet Digital Health
**Manuscript Type**: Original Research Article
**Submission Date**: December 15, 2025
**Word Count**: 3,847 (excluding abstract, references, tables, and figures)

## Authors

**Olaf Yunus Laitinen Imanov** (Corresponding Author)
Department of Biotechnology and Biomedicine, Technical University of Denmark
Email: olyulaim@dtu.dk

**Derya Umut Kulali**
Department of Engineering, Eskisehir Technical University, Türkiye
Email: d_u_k@ogr.eskisehir.edu.tr

---

## Abstract

**File**: `abstract.tex`
**Word Count**: 250 words (structured format)
**Sections**: Background, Methods, Findings, Interpretation, Funding

---

## Manuscript Structure

### Main Document
- **File**: `manuscript.tex`
- **Compilation**: See `COMPILATION_GUIDE.md` for detailed instructions
- **Document Class**: `lancetdigitalhealth.cls` (custom Lancet class)
- **Bibliography**: BibTeX format (`latex/references.bib`)

### LaTeX Components

Located in `latex/` directory:
- `lancetdigitalhealth.cls` - Custom Lancet Digital Health document class
- `packages.tex` - Required LaTeX packages
- `macros.tex` - Custom macros and abbreviations
- `notation.tex` - Mathematical notation definitions
- `references.bib` - Complete bibliography (97 references)

### Supplementary Materials

Located in `supplementary/` directory:
- `extended_methods.md` - Extended methodology section
- `analysis_plan.md` - Statistical analysis plan
- `TRIPOD_AI_checklist.pdf` - TRIPOD-AI reporting checklist

---

## Figures

All figures are generated programmatically using Python scripts in `figures/` directory:

| Figure | Script | Description | Format |
|--------|--------|-------------|--------|
| Figure 1 | `generate_figure_1.py` | Hallucination rates by query complexity and protein prevalence | PNG (300 DPI) + TIFF (600 DPI) |
| Figure 2 | `generate_figure_2.py` | Severity heatmap across models and query types | PNG (300 DPI) + TIFF (600 DPI) |
| Figure 3 | `generate_figure_3.py` | Response consistency matrix | PNG (300 DPI) + TIFF (600 DPI) |
| Figure 4 | `generate_figure_4.py` | Calibration curves for hallucination prediction | PNG (300 DPI) + TIFF (600 DPI) |
| Figure 5 | `generate_figure_5.py` | Domain-wise error breakdown | PNG (300 DPI) |
| Figure 6 | `generate_figure_6.py` | Bayesian posterior distributions | PNG (300 DPI) |

**Output directories**:
- `figures/output/` - PNG figures for manuscript (300 DPI)
- `figures/output/highres_tiff/` - High-resolution TIFF for print (600 DPI)

**Style configuration**:
- `figure_style.mplstyle` - Matplotlib style sheet (Lancet formatting)
- `templates/color_palette.json` - Consistent color scheme
- `templates/lancet_fonts.rc` - Font configuration
- `templates/grid_style.yaml` - Grid and axis styling
- `templates/dpi_settings.yaml` - Resolution settings

### Figure Generation

```bash
cd paper/figures

# Generate all figures
python generate_figure_1.py
python generate_figure_2.py
python generate_figure_3.py
python generate_figure_4.py
python generate_figure_5.py
python generate_figure_6.py

# Or use the generation script
python generate_all_figures.py
```

---

## Tables

All tables are generated using R scripts in `tables/` directory:

| Table | Script | Description |
|-------|--------|-------------|
| Table 1 | `make_table_1_summary.R` | Study characteristics and query distribution |
| Table 2 | `make_table_2_model_perf.R` | Model performance metrics with 95% CIs |
| Table 3 | `make_table_3_domainwise.R` | Domain-specific hallucination rates |
| Table 4 | `make_table_4_multivariable.R` | Multivariable logistic regression results |
| Table 5 | `make_table_5_bias_audit.R` | Bias and fairness metrics |

**Output directory**: `tables/outputs/`
- Individual CSV files for each table
- `combined_tables.xlsx` - All tables in Excel format

### Table Generation

```bash
cd paper/tables

# Generate all tables
Rscript make_table_1_summary.R
Rscript make_table_2_model_perf.R
Rscript make_table_3_domainwise.R
Rscript make_table_4_multivariable.R
Rscript make_table_5_bias_audit.R

# Generate figures from table data
Rscript figures_from_tables.R
```

---

## Journal Compliance Checklists

Located in `journal_checklists/` directory:

- **CONSORT-AI**: `CONSORT_extension_AI.md` - AI intervention reporting
- **TRIPOD-AI**: `../supplementary/TRIPOD_AI_checklist.pdf` - Prediction model reporting
- **STARD**: `STARD_checklist.pdf` - Diagnostic accuracy studies
- **EQUATOR**: `EQUATOR_compliance.md` - Overall reporting guidelines compliance
- **GRRAS**: `GRRAS_checklist.pdf` - Generalizability and replicability
- **Lancet Submission**: `Lancet_submission_form.pdf` - Journal-specific requirements

---

## Manuscript Compilation

### Prerequisites

```bash
# LaTeX distribution (TeX Live 2024 or later)
sudo apt-get install texlive-latex-extra texlive-bibtex-extra biber

# Python dependencies for figures
pip install matplotlib numpy seaborn pandas scipy

# R dependencies for tables
Rscript -e "install.packages(c('tidyverse', 'gt', 'gtsummary', 'writexl'))"
```

### Compilation Steps

```bash
cd paper

# Step 1: Generate figures
cd figures && python generate_all_figures.py && cd ..

# Step 2: Generate tables
cd tables && Rscript make_all_tables.R && cd ..

# Step 3: Compile LaTeX
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex

# Output: manuscript.pdf
```

**See `COMPILATION_GUIDE.md` for detailed instructions and troubleshooting.**

---

## Submission Requirements

### The Lancet Digital Health Requirements

✓ **Word count**: 3,500-4,000 words (main text)
✓ **Abstract**: 250 words maximum (structured)
✓ **References**: No limit (97 references included)
✓ **Figures**: Maximum 6 (we have 6)
✓ **Tables**: Maximum 5 (we have 5)
✓ **Supplementary materials**: Allowed (extended methods included)

### Pre-submission Checklist

- [x] CONSORT-AI checklist completed
- [x] TRIPOD-AI checklist completed
- [x] STARD checklist completed
- [x] EQUATOR compliance verified
- [x] Ethics approval obtained (IRB #2025-IRB-1101)
- [x] Data availability statement included
- [x] Code availability statement included
- [x] Conflicts of interest declared (none)
- [x] Author contributions specified
- [x] Funding sources listed

---

## File Organization

```
paper/
├── manuscript.tex              # Main manuscript
├── abstract.tex                # Structured abstract
├── COMPILATION_GUIDE.md        # Compilation instructions
├── README.md                   # This file
│
├── latex/                      # LaTeX components
│   ├── lancetdigitalhealth.cls
│   ├── packages.tex
│   ├── macros.tex
│   ├── notation.tex
│   └── references.bib
│
├── figures/                    # Figure generation
│   ├── generate_figure_[1-6].py
│   ├── figure_style.mplstyle
│   ├── templates/
│   │   ├── color_palette.json
│   │   ├── lancet_fonts.rc
│   │   ├── grid_style.yaml
│   │   └── dpi_settings.yaml
│   └── output/
│       ├── *.png (300 DPI)
│       └── highres_tiff/*.tiff (600 DPI)
│
├── tables/                     # Table generation
│   ├── make_table_[1-5].R
│   ├── figures_from_tables.R
│   └── outputs/
│       ├── table[1-5]_*.csv
│       └── combined_tables.xlsx
│
├── journal_checklists/         # Compliance documentation
│   ├── CONSORT_extension_AI.md
│   ├── EQUATOR_compliance.md
│   ├── STARD_checklist.pdf
│   ├── GRRAS_checklist.pdf
│   └── Lancet_submission_form.pdf
│
└── supplementary/              # Supplementary materials
    ├── extended_methods.md
    ├── analysis_plan.md
    └── TRIPOD_AI_checklist.pdf
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-01 | Initial manuscript draft |
| 1.1 | 2025-11-15 | Added extended methods and bias analysis |
| 1.2 | 2025-11-30 | Completed all figures and tables |
| 1.3 | 2025-12-10 | Final revisions based on internal review |
| 1.4 | 2025-12-15 | Submission-ready version |

---

## Contact

For questions about the manuscript or analysis:

**Olaf Yunus Laitinen Imanov**
Department of Biotechnology and Biomedicine
Technical University of Denmark
Building 375, 2800 Kongens Lyngby, Denmark
Email: olyulaim@dtu.dk

---

## License

This manuscript and associated materials are licensed under CC-BY-4.0.
See repository LICENSE file for details.
