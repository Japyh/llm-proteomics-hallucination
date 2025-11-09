# Manuscript Compilation Guide

This document provides detailed instructions for compiling the manuscript "Hallucination risks of large language models in clinical proteomics: a prospective evaluation study" for submission to The Lancet Digital Health.

---

## Requirements

### LaTeX Distribution

**Recommended**: TeX Live 2023 or later

**Installation (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

**Installation (macOS)**:
```bash
brew install --cask mactex
```

**Installation (Windows)**:
Download and install MiKTeX from: https://miktex.org/download

### Required LaTeX Packages

The manuscript requires the following packages (all included in TeX Live Full):
- elsarticle (Elsevier document class)
- float (figure positioning)
- amsmath (mathematical typesetting)
- graphicx (figure inclusion)
- hyperref (PDF metadata and links)
- inputenc (UTF-8 encoding)
- times (Times font family)
- geometry (page layout)
- setspace (line spacing)
- lineno (line numbering)
- cite (superscript citations)
- xcolor (colored text)

### Python Requirements for Figures

**Version**: Python 3.11+

**Install Dependencies**:
```bash
cd paper/figures
pip install -r requirements.txt
```

**Required Packages**:
- matplotlib>=3.8.0
- numpy>=1.24.0
- scipy>=1.11.0

---

## Compilation Instructions

### Step 1: Generate All Figures

Navigate to the figures directory and run all generation scripts:

```bash
cd paper/figures

# Generate Figure 1 (Hallucination rates by complexity and prevalence)
python generate_figure_1.py

# Generate Figure 2 (Severity heatmap)
python generate_figure_2.py

# Generate Figure 3 (Response consistency)
python generate_figure_3.py

# Generate Figure 4 (Calibration plot)
python generate_figure_4.py
```

**Expected Output**:
- `output/Figure_1_Hallucination_Rates.png` (243 KB, 300 DPI)
- `output/Figure_2_Severity_Distribution.png` (464 KB, 300 DPI)
- `output/Figure_3_Response_Consistency.png` (470 KB, 300 DPI)
- `output/Figure_4_Calibration_Plot.png` (552 KB, 300 DPI)

**Verification**:
```bash
ls -lh output/*.png
# All files should be present with sizes matching above
```

### Step 2: Compile Manuscript PDF

Navigate to the paper directory:

```bash
cd /home/user/llm-proteomics-hallucination/paper
```

#### Method 1: Standard LaTeX Compilation (Recommended)

```bash
# First pass: Process document structure
pdflatex manuscript.tex

# Process bibliography
bibtex manuscript

# Second pass: Resolve references
pdflatex manuscript.tex

# Third pass: Final resolution of all cross-references
pdflatex manuscript.tex
```

**Expected Output**: `manuscript.pdf` (~2.5 MB)

#### Method 2: Using latexmk (Alternative)

```bash
latexmk -pdf -interaction=nonstopmode manuscript.tex
```

This automatically runs all necessary passes.

#### Method 3: Using pdflatex with shell escape (if needed)

```bash
pdflatex -shell-escape manuscript.tex
bibtex manuscript
pdflatex -shell-escape manuscript.tex
pdflatex -shell-escape manuscript.tex
```

### Step 3: Verify PDF Output

**Check PDF Properties**:
- Title: "Hallucination risks of large language models in clinical proteomics"
- Authors: Olaf Yunus Laitinen Imanov, Derya Umut Kulali
- Page count: ~30-35 pages
- All 4 figures included and properly positioned
- All 4 tables included with correct formatting
- Line numbers present
- Citations formatted as superscripts

**Visual Inspection**:
1. Open manuscript.pdf
2. Verify all figures display correctly at high resolution
3. Check tables are properly formatted
4. Ensure no overflow text or formatting errors
5. Verify bibliography is complete (34 references)

### Step 4: Clean Up Auxiliary Files (Optional)

```bash
# Remove LaTeX auxiliary files
rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot

# Or use latexmk to clean
latexmk -c
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Missing Package Errors

**Error**: `! LaTeX Error: File 'elsarticle.cls' not found.`

**Solution**:
```bash
# Update package database
sudo tlmgr update --self

# Install elsarticle
sudo tlmgr install elsarticle

# Or install all required packages
sudo tlmgr install elsarticle float amsmath graphicx hyperref times geometry setspace lineno cite xcolor
```

#### Issue 2: Figure Not Found

**Error**: `! LaTeX Error: File 'figures/output/Figure_1_Hallucination_Rates.png' not found.`

**Solution**:
1. Verify figures were generated:
```bash
ls -l figures/output/Figure_*.png
```

2. If missing, regenerate figures:
```bash
cd figures
python generate_figure_1.py
# ... repeat for all figures
```

3. Check path in manuscript.tex matches actual file location

#### Issue 3: Bibliography Not Updating

**Solution**:
1. Delete auxiliary files:
```bash
rm manuscript.aux manuscript.bbl manuscript.blg
```

2. Recompile from scratch:
```bash
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

#### Issue 4: Font Warnings

**Warning**: `Font shape 'OT1/times/m/n' undefined`

**Solution**:
```bash
# Install Times font package
sudo tlmgr install times

# Alternative: Install complete font collection
sudo tlmgr install collection-fontsrecommended
```

#### Issue 5: Figures Appear Low Resolution

**Solution**:
1. Verify figures generated at 300 DPI:
```python
# In generate_figure_*.py, check:
plt.savefig(output_path, dpi=300, bbox_inches='tight')
```

2. Regenerate figures if necessary

3. Ensure PDF viewer is not downscaling (zoom to 100%)

#### Issue 6: Line Numbers Not Appearing

**Solution**:
Verify lineno package is loaded and enabled in manuscript.tex:
```latex
\usepackage{lineno}
\modulolinenumbers[5]
\linenumbers
```

---

## File Structure

```
paper/
├── manuscript.tex              # Main manuscript file
├── figures/
│   ├── generate_figure_1.py   # Figure 1 generation script
│   ├── generate_figure_2.py   # Figure 2 generation script
│   ├── generate_figure_3.py   # Figure 3 generation script
│   ├── generate_figure_4.py   # Figure 4 generation script
│   ├── figure_config.py        # Shared matplotlib configuration
│   └── output/
│       ├── Figure_1_Hallucination_Rates.png
│       ├── Figure_2_Severity_Distribution.png
│       ├── Figure_3_Response_Consistency.png
│       └── Figure_4_Calibration_Plot.png
├── COMPILATION_GUIDE.md        # This file
└── README.md                   # Paper directory overview
```

---

## Manuscript Specifications

### Journal Requirements (The Lancet Digital Health)

**Format**: Research Article
**Document Class**: elsarticle (review mode, 10pt)
**Page Limits**: No strict limit for online-only articles
**Word Count**: ~4,500 words (excluding abstract, tables, figures, references)
**Abstract**: ~300 words (structured)
**References**: Vancouver style (numeric superscripts)
**Figures**: Maximum 6 (we use 4)
**Tables**: Maximum 6 (we use 4)

### Formatting Specifications

**Margins**:
- Top: 1 inch
- Bottom: 1 inch
- Left: 1 inch
- Right: 1.06 inches

**Line Spacing**: Single-spaced

**Line Numbers**: Every 5 lines (modulo 5)

**Font**: Times (10pt)

**Section Formatting**:
- Sections: Large, bold, sans-serif
- Subsections: Normal size, bold, sans-serif
- Subsubsections: Small, bold, sans-serif

**Citations**: Superscript numbers in square brackets

### Figure Specifications

**Resolution**: 300 DPI minimum
**Format**: PNG (high quality) or TIFF
**Width**: Full column width (6.5 inches) or double column (14 cm)
**Color**: Color figures accepted for online publication
**File Size**: <10 MB per figure (our figures: 243-552 KB each)

### Table Specifications

**Format**: LaTeX tabular environment
**Width**: Fit within text width
**Font**: Match main text (10pt)
**Borders**: Horizontal lines only (toprule, midrule, bottomrule)
**Captions**: Above table
**Footnotes**: Below table

---

## Quality Checks

### Pre-Submission Checklist

- [ ] All 4 figures generated at 300 DPI
- [ ] All 4 tables formatted correctly
- [ ] Line numbers present throughout
- [ ] All citations in superscript format
- [ ] Bibliography contains all 34 references
- [ ] No orphaned or widowed lines
- [ ] No overfull hbox warnings
- [ ] PDF metadata correctly set
- [ ] Abstract under 300 words
- [ ] Main text ~4,500 words
- [ ] All author affiliations correct
- [ ] Ethics approval number present
- [ ] Pre-registration link included
- [ ] Data sharing statement complete
- [ ] Conflict of interest statement present
- [ ] Author contributions documented
- [ ] No typos or grammatical errors

### Automated Checks

```bash
# Count words in main text (excluding tables, figures, references)
detex manuscript.tex | wc -w

# Count references
grep "bibitem" manuscript.tex | wc -l

# Check for overfull boxes
grep "Overfull" manuscript.log

# Check for undefined references
grep "undefined" manuscript.log
```

---

## Submission Preparation

### Files to Prepare for Submission

1. **Manuscript PDF**: `manuscript.pdf`
2. **Manuscript Source**: `manuscript.tex`
3. **Figure Files** (separate, high-resolution):
   - `Figure_1_Hallucination_Rates.png`
   - `Figure_2_Severity_Distribution.png`
   - `Figure_3_Response_Consistency.png`
   - `Figure_4_Calibration_Plot.png`
4. **Supplementary Materials** (if applicable):
   - Supplementary tables
   - Supplementary figures
   - Code repository link
   - Data repository link

### Cover Letter Template

```
Dear Editors of The Lancet Digital Health,

We submit for your consideration our research article titled "Hallucination risks of large language models in clinical proteomics: a prospective evaluation study."

This prospective evaluation study provides the first systematic assessment of hallucination rates in frontier large language models (GPT-4 Turbo, Claude 3 Sonnet, Gemini Pro 1.5) when queried about clinical proteomics data. Using 1,500 standardized queries, we demonstrate overall hallucination rates of 27.8-34.6%, escalating to over 50% for complex queries about rare proteins.

Our findings have immediate implications for patient safety and AI deployment in specialized clinical domains. We identify critical risk factors including query complexity (OR=5.1) and protein rarity (OR=5.4), and demonstrate that current error rates are incompatible with safe clinical deployment without rigorous human oversight.

This work addresses a critical gap in understanding LLM reliability for clinical decision support in specialized medical domains and provides an evidence-based framework for regulatory evaluation and clinical deployment strategies.

We confirm that this manuscript has not been published elsewhere and is not under consideration by another journal. All authors have approved the manuscript and agree with its submission to The Lancet Digital Health.

Sincerely,
Olaf Yunus Laitinen Imanov, Ph.D. Candidate
Corresponding Author
```

---

## Revision Workflow

### After Peer Review

1. **Track Changes**:
```bash
# Create revision branch
git checkout -b revision-lancet-1

# Make changes to manuscript.tex
# Commit changes with clear messages
git commit -m "revision: Address reviewer 1 comment 3"
```

2. **Generate Change-Marked PDF**:
```bash
# Use latexdiff for change tracking
latexdiff manuscript-original.tex manuscript-revised.tex > manuscript-diff.tex
pdflatex manuscript-diff.tex
```

3. **Response to Reviewers**:
Create detailed point-by-point response document

4. **Resubmission Package**:
- Revised manuscript PDF
- Marked-up manuscript PDF (with changes highlighted)
- Response to reviewers document
- Updated figure files (if modified)

---

## Contact for Assistance

**Technical Issues**:
- GitHub Issues: https://github.com/olaflaitinen/llm-proteomics-hallucination/issues

**Manuscript Questions**:
- Corresponding Author: olyulaim@dtu.dk

**LaTeX Support**:
- TeX Stack Exchange: https://tex.stackexchange.com/
- Overleaf Documentation: https://www.overleaf.com/learn

---

**Last Updated**: November 9, 2024
**Document Version**: 1.0
