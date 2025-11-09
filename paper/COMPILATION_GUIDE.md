# Paper Compilation Guide

## Prerequisites

```bash
# LaTeX distribution (TeX Live or MiKTeX)
sudo apt-get install texlive-full

# Python for figure generation
pip install matplotlib seaborn pandas numpy
```

## Compiling the Manuscript

```bash
cd paper/
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

## Generating Figures

```bash
cd paper/figures/
python generate_figure_1.py
python generate_figure_2.py
python generate_figure_3.py
python generate_figure_4.py
python generate_figure_5.py
python generate_figure_6.py
```

## Generating Tables

```bash
cd paper/tables/
Rscript make_table_1_summary.R
Rscript make_table_2_model_perf.R
Rscript make_table_3_domainwise.R
Rscript make_table_4_multivariable.R
Rscript make_table_5_bias_audit.R
```

## Complete Build

```bash
make paper
```

## Output Files

- `manuscript.pdf` - Main manuscript
- `supplementary_material.pdf` - Supplementary materials
- `figures/output/*.png` - Figures (300 DPI)
- `tables/outputs/*.csv` - Tables
