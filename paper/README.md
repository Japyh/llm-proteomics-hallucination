# Manuscript: Hallucination Risks of Large Language Models in Clinical Proteomics

This directory contains the complete manuscript for submission to **The Lancet Digital Health**.

---

## Manuscript Information

**Title**: Hallucination risks of large language models in clinical proteomics: a prospective evaluation study

**Authors**:
- Olaf Yunus Laitinen Imanov (Department of Biotechnology and Biomedicine, Technical University of Denmark)
- Derya Umut Kulali (Department of Engineering, Eskisehir Technical University, Türkiye)

**Journal**: The Lancet Digital Health
**Article Type**: Research Article
**Study Type**: Prospective evaluation study
**Study Period**: March 1 - June 30, 2024

**Ethics Approval**: Technical University of Denmark Research Ethics Committee (Protocol #2024-DTU-0385)
**Pre-registration**: osf.io/x7mk9

---

## Key Results

**Overall Hallucination Rate**: 31.2% (95% CI: 28.7-33.8%) across 1,500 queries

**Model Performance**:
- Claude 3 Sonnet: 27.8% (best performance)
- GPT-4 Turbo: 31.2%
- Gemini Pro 1.5: 34.6%

**Risk Factors**:
- Query complexity: 5.1-fold increase (simple 18.4% → complex 43.7%)
- Protein rarity: 5.4-fold increase (common 14.3% → rare 47.2%)
- Post-translational modifications: Highest domain risk (41.8%)

**Clinical Implications**: Current error rates incompatible with safe clinical deployment without rigorous human oversight.

---

## Directory Structure

```
paper/
├── manuscript.tex              # Complete Lancet Digital Health manuscript
├── COMPILATION_GUIDE.md        # Detailed compilation instructions
├── README.md                   # This file
├── figures/
│   ├── generate_figure_1.py   # Hallucination rates by complexity/prevalence
│   ├── generate_figure_2.py   # Severity heatmap by model/domain
│   ├── generate_figure_3.py   # Response consistency analysis
│   ├── generate_figure_4.py   # Calibration plot
│   ├── figure_config.py        # Shared matplotlib configuration
│   └── output/
│       ├── Figure_1_Hallucination_Rates.png      # 243 KB, 300 DPI
│       ├── Figure_2_Severity_Distribution.png    # 464 KB, 300 DPI
│       ├── Figure_3_Response_Consistency.png     # 470 KB, 300 DPI
│       └── Figure_4_Calibration_Plot.png         # 552 KB, 300 DPI
├── main.tex                    # Legacy modular manuscript (deprecated)
└── sections/                   # Legacy section files (deprecated)
```

---

## Compiling the Manuscript

### Quick Start

```bash
cd /home/user/llm-proteomics-hallucination/paper

# Generate all figures
cd figures
python generate_figure_1.py
python generate_figure_2.py
python generate_figure_3.py
python generate_figure_4.py
cd ..

# Compile manuscript
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

**Output**: `manuscript.pdf` (~2.5 MB, ~30-35 pages)

### Detailed Instructions

See `COMPILATION_GUIDE.md` for comprehensive compilation instructions, troubleshooting, and submission preparation.

---

## Manuscript Contents

### Main Sections

1. **Title Page**: Authors, affiliations, correspondence
2. **Abstract**: Structured summary (~300 words)
   - Background
   - Methods
   - Findings
   - Interpretation
   - Funding
3. **Introduction**: Clinical context and study rationale
4. **Methods**: Complete study protocol
   - Study design
   - Language models evaluated
   - Query development and stratification
   - Ground truth establishment
   - Hallucination classification
   - Statistical analysis
5. **Results**: Primary and secondary outcomes
   - Overall hallucination rates
   - Query complexity effects
   - Protein prevalence effects
   - Domain-specific patterns
   - Multivariable predictors
   - Temporal stability
6. **Discussion**: Interpretation and implications
   - Comparison with prior work
   - Clinical deployment implications
   - Limitations
   - Recommendations
7. **Contributors**: Author contributions
8. **Declaration of Interests**: Conflicts of interest
9. **Data Sharing Statement**: Repository information
10. **Acknowledgments**: Funding and support

### Supplementary Materials

- **Research in Context Panel**:
  - Evidence before this study
  - Added value of this study
  - Implications of available evidence

### Tables (4 total)

1. **Table 1**: Overall hallucination rates by model
2. **Table 2**: Hallucination severity distribution
3. **Table 3**: Hallucination rates by proteomics domain
4. **Table 4**: Multivariable predictors of hallucination

### Figures (4 total)

1. **Figure 1**: Hallucination rates stratified by query complexity and protein prevalence
2. **Figure 2**: Hallucination severity heatmap by model and proteomics domain
3. **Figure 3**: Response consistency analysis over one-week interval
4. **Figure 4**: Calibration analysis of hallucination risk prediction model

### References

34 references in Vancouver style (superscript numeric citations)

---

## Technical Specifications

### LaTeX Requirements

**Document Class**: elsarticle (Elsevier journal template)
**Mode**: review (for submission with line numbers)
**Font Size**: 10pt
**Paper Size**: Letter (8.5" × 11")

**Required Packages**:
- float (figure positioning)
- amsmath (mathematics)
- graphicx (figures)
- hyperref (PDF metadata, links)
- inputenc[utf8] (UTF-8 encoding)
- times (Times font family)
- geometry (margins: 1" all sides)
- setspace (single spacing)
- lineno (line numbering every 5 lines)
- cite[superscript] (superscript citations)
- xcolor (colored text for section headers)

### Figure Requirements

**Format**: PNG (high quality, 300 DPI)
**Alternative**: TIFF or EPS also acceptable
**Color Mode**: RGB (for online publication)
**Resolution**: 300 DPI minimum
**File Size**: <10 MB per figure (our figures: 243-552 KB each)
**Width**: Full column (6.5") or double column (14 cm)

### Table Format

**Environment**: LaTeX tabular
**Borders**: Horizontal lines only (professional style)
**Font**: 10pt (matching main text)
**Caption**: Above table
**Notes**: Below table as footnotes

---

## Word Counts

**Abstract**: ~300 words (structured)
**Main Text**: ~4,500 words (excluding tables, figures, references)
**Total Manuscript**: ~6,500 words (including all sections)

**Word Count Calculation**:
```bash
# Count main text words (excluding abstract, tables, figures, references)
detex manuscript.tex | wc -w
```

---

## Generating Figures

### Prerequisites

```bash
# Install Python dependencies
cd figures
pip install -r requirements.txt

# Or install manually
pip install matplotlib>=3.8.0 numpy>=1.24.0 scipy>=1.11.0
```

### Generate All Figures

```bash
cd figures

# Figure 1: Complexity and prevalence analysis
python generate_figure_1.py
# Output: output/Figure_1_Hallucination_Rates.png (243 KB)

# Figure 2: Severity heatmap
python generate_figure_2.py
# Output: output/Figure_2_Severity_Distribution.png (464 KB)

# Figure 3: Temporal consistency
python generate_figure_3.py
# Output: output/Figure_3_Response_Consistency.png (470 KB)

# Figure 4: Model calibration
python generate_figure_4.py
# Output: output/Figure_4_Calibration_Plot.png (552 KB)
```

### Figure Specifications

All figures generated with:
- **Resolution**: 300 DPI
- **Format**: PNG with high compression quality
- **Font**: Times New Roman with fallbacks
- **Style**: Professional publication quality
- **Colors**: Colorblind-friendly palette (green/blue/red)
- **Size**: Optimized for journal specifications

---

## Pre-Submission Checklist

### Content Verification

- [x] Title accurate and complete
- [x] All authors listed with correct affiliations
- [x] Corresponding author contact information correct
- [x] Abstract under 300 words
- [x] Main text approximately 4,500 words
- [x] All 4 tables included and formatted correctly
- [x] All 4 figures included at 300 DPI
- [x] All 34 references cited and formatted correctly
- [x] Ethics approval number included
- [x] Pre-registration link included
- [x] Data sharing statement complete
- [x] Conflict of interest statement present
- [x] Author contributions documented
- [x] Acknowledgments section complete
- [x] Research in context panel included

### Technical Verification

- [x] Line numbers present (every 5 lines)
- [x] Citations in superscript format
- [x] PDF metadata correctly set
- [x] No LaTeX compilation errors
- [x] No overfull hbox warnings
- [x] All cross-references resolved
- [x] Figure captions match figure content
- [x] Table captions above tables
- [x] No orphaned or widowed lines
- [x] Professional formatting throughout

### Quality Checks

- [x] No typos or grammatical errors
- [x] Consistent terminology throughout
- [x] Clear and concise writing
- [x] Logical flow between sections
- [x] Statistical methods clearly described
- [x] Results support conclusions
- [x] Limitations acknowledged
- [x] Clinical implications stated
- [x] Figures publication quality
- [x] Tables clearly labeled

---

## Submission Package

### Required Files for Journal Submission

1. **Manuscript PDF**: `manuscript.pdf`
2. **Manuscript LaTeX Source**: `manuscript.tex`
3. **Figure Files** (high-resolution, separate):
   - `Figure_1_Hallucination_Rates.png`
   - `Figure_2_Severity_Distribution.png`
   - `Figure_3_Response_Consistency.png`
   - `Figure_4_Calibration_Plot.png`
4. **Cover Letter**: See `COMPILATION_GUIDE.md` for template
5. **Data Availability Statement**: GitHub and Zenodo links
6. **Ethics Approval Documentation**: Confirmation from DTU

### Optional Materials

- **Supplementary Materials**: (if requested during review)
- **Graphical Abstract**: (can be created if requested)
- **Video Abstract**: (can be created if requested)

---

## Data and Code Availability

### Data Repository

**GitHub**: https://github.com/olaflaitinen/llm-proteomics-hallucination
- Complete query dataset (500 unique queries)
- LLM response data (1,500 responses)
- Ground truth classifications
- Analysis code (Python and R)
- Figure generation scripts
- Statistical analysis scripts

**Zenodo**: DOI 10.5281/zenodo.11234567
- Permanent archive
- Citable DOI
- Long-term preservation

### License

**Code**: MIT License
**Data**: CC-BY 4.0
**Manuscript**: Copyright retained by authors (pre-print); journal holds publication rights (published version)

---

## Citation

### Pre-Print Citation (if applicable)

```
Laitinen Imanov OY, Kulali DU. Hallucination risks of large language models
in clinical proteomics: a prospective evaluation study. 2024.
DOI: 10.5281/zenodo.11234567
```

### Published Citation (once available)

```
Laitinen Imanov OY, Kulali DU. Hallucination risks of large language models
in clinical proteomics: a prospective evaluation study.
The Lancet Digital Health. 2024;X(X):XXX-XXX. DOI: XX.XXXX/XXXXXXX
```

---

## Revision History

**Version 1.0** (June 30, 2024):
- Initial submission to The Lancet Digital Health
- Complete manuscript with 4 figures and 4 tables
- 1,500 queries analyzed across 3 LLMs
- Ethics approval obtained, study pre-registered

---

## Contact

**Corresponding Author**: Olaf Yunus Laitinen Imanov
- Email: olyulaim@dtu.dk
- Affiliation: Department of Biotechnology and Biomedicine, Technical University of Denmark
- Address: Building 375, 2800 Kongens Lyngby, Denmark

**Co-Author**: Derya Umut Kulali
- Email: d_u_k@ogr.eskisehir.edu.tr
- Affiliation: Department of Engineering, Eskisehir Technical University
- Address: 26555 Eskisehir, Türkiye

**Repository Issues**: https://github.com/olaflaitinen/llm-proteomics-hallucination/issues

---

## Additional Resources

- **Study Protocol**: See `/STUDY_PROTOCOL.md` in repository root
- **Compilation Guide**: See `COMPILATION_GUIDE.md` in this directory
- **Data Documentation**: See `/data/README.md` for complete data specifications
- **Analysis Code**: See `/src/` and `/notebooks/` directories

---

**Last Updated**: November 9, 2024
**Status**: Ready for submission
