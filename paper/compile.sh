#!/bin/bash
# Compile LaTeX paper

set -e

echo "Compiling paper..."

# Compile main.tex
echo "Step 1/4: First pdflatex pass..."
pdflatex -interaction=nonstopmode main.tex > /dev/null

echo "Step 2/4: Running bibtex..."
bibtex main > /dev/null

echo "Step 3/4: Second pdflatex pass..."
pdflatex -interaction=nonstopmode main.tex > /dev/null

echo "Step 4/4: Final pdflatex pass..."
pdflatex -interaction=nonstopmode main.tex > /dev/null

echo "Done! Output: main.pdf"

# Clean up auxiliary files
echo "Cleaning up auxiliary files..."
rm -f *.aux *.log *.bbl *.blg *.out *.toc *.lof *.lot

echo "Compilation complete!"
