# Manuscript Directory

LaTeX source files for the academic paper.

## Compilation

```bash
cd manuscript
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or use latexmk:
```bash
latexmk -pdf main.tex
```
