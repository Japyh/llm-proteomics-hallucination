# Paper Directory

This directory contains the LaTeX manuscript and all associated files for the publication.

## Structure

- `main.tex` - Main LaTeX document
- `sections/` - Individual paper sections
- `figures/` - Figure generation scripts and outputs
- `tables/` - LaTeX table files
- `references.bib` - Bibliography
- `supplementary/` - Supplementary materials

## Compiling the Paper

### Option 1: Using pdflatex

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Option 2: Using latexmk

```bash
cd paper
latexmk -pdf main.tex
```

### Option 3: Using the compile script

```bash
cd paper
./compile.sh
```

### Option 4: Using Docker

```bash
docker-compose run latex-compile
```

## Adding complete_paper.tex

If you have a complete standalone paper file (complete_paper.tex), place it in this directory.
You can compile it with:

```bash
pdflatex complete_paper.tex
bibtex complete_paper
pdflatex complete_paper.tex
pdflatex complete_paper.tex
```

## Figure Generation

All figures are generated programmatically using Python scripts in the `figures/` directory.

To generate all figures:

```bash
cd paper/figures
python generate_all_figures.py
```

To generate individual figures:

```bash
python figure1_hallucination_rates.py
python figure2_category_performance.py
python figure3_coverage_impact.py
# ... etc
```

Figures are saved to `figures/output/` in both PDF (vector) and PNG (raster) formats.

## Requirements

- LaTeX distribution (TeX Live or MiKTeX)
- Python 3.10+ with matplotlib, seaborn, numpy, pandas
- BibTeX for bibliography compilation

## Notes

- All figures are generated at 300 DPI for publication quality
- Use colorblind-friendly palettes throughout
- Figures match paper specifications exactly
- Vector formats (PDF) preferred for publication
