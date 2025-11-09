# Data Directory

Complete data for the LLM proteomics hallucination study submitted to The Lancet Digital Health.

---

## Overview

This directory contains all query datasets, ground truth annotations, LLM responses, and analysis results for evaluating hallucination risks of GPT-4 Turbo, Claude 3 Sonnet, and Gemini Pro 1.5 in clinical proteomics.

**Study Period**: March 1 - June 30, 2024
**Total Queries**: 500 unique queries
**Total Responses**: 1,500 (500 per model)
**Ground Truth Sources**: UniProt 2024_01, Human Protein Atlas 23.0, PeptideAtlas 2024-01, PhosphoSitePlus

---

## Directory Structure

```
data/
├── queries/                # Query datasets
│   └── queries_all.json    # 500 unique proteomics queries
├── ground_truth/           # Expert-validated annotations
│   ├── protein_annotations.json
│   ├── expert_ratings.csv
│   └── validation_metadata.json
├── llm_responses/          # LLM response data
│   ├── gpt4_responses.json
│   ├── claude_responses.json
│   └── gemini_responses.json
├── results/                # Analysis results
│   ├── hallucination_rates.csv
│   ├── severity_classifications.csv
│   ├── statistical_analysis.csv
│   └── model_comparison.csv
├── proteins/               # Protein sequences (FASTA)
│   ├── common_proteins.fasta
│   ├── moderate_proteins.fasta
│   └── rare_proteins.fasta
├── mass_spectrometry/      # MS/MS spectra (MGF)
│   └── example_spectra.mgf
├── structured/             # Protein annotations (JSON)
│   └── protein_database_entries.json
└── generators/             # Data generation scripts
    ├── generate_query_dataset.py
    ├── generate_protein_sequences.py
    └── generate_ms_spectra.py
```

---

## Query Dataset

### queries_all.json

**Format**: JSON array with 500 query objects
**Study Design**: Stratified by complexity and protein prevalence

**Stratification**:
- **Complexity**: Simple (167), Intermediate (166), Complex (167)
- **Prevalence**: Common proteins (250), Moderate (125), Rare (125)

**Query Domains**:
- Protein identification (n=100)
- Quantitative expression (n=100)
- Post-translational modifications (n=150)
- Protein interactions (n=75)
- Clinical interpretation (n=75)

**Schema**:
```json
{
  "query_id": "Q001",
  "query_text": "What is the primary function of...",
  "domain": "protein_identification",
  "complexity": "simple",
  "protein_prevalence": "common",
  "protein_id": "P68871",
  "gene_name": "HBB",
  "expected_answer": "Ground truth answer",
  "key_facts": ["Fact 1", "Fact 2"],
  "common_errors": ["Error type 1"]
}
```

**Generation**: See `generators/generate_query_dataset.py`

---

## Ground Truth Data

### Ground Truth Establishment

**Multi-step validation process**:

1. **Database Cross-Reference**:
   - UniProt Knowledgebase 2024_01 (protein sequences, functions)
   - Human Protein Atlas 23.0 (tissue expression, localization)
   - PeptideAtlas 2024-01 (MS/MS evidence)
   - PhosphoSitePlus (post-translational modifications)
   - PubMed (peer-reviewed literature)

2. **Expert Consensus**:
   - Two independent expert raters
   - Cohen's kappa = 0.89 (ground truth agreement)
   - Discrepancies resolved through discussion

3. **Quality Control**:
   - All answers verified against primary literature
   - Quantitative values cross-checked across databases
   - PTM sites confirmed through experimental evidence

### protein_annotations.json

**Format**: JSON with comprehensive protein annotations
**Source**: Integrated from UniProt, HPA, PeptideAtlas
**Proteins**: 250 human proteins covering common to rare

### expert_ratings.csv

**Format**: CSV with hallucination severity ratings
**Raters**: Two independent expert evaluators
**Inter-rater Reliability**: Cohen's kappa = 0.87

**Columns**:
- `query_id`: Query identifier
- `model`: LLM model name
- `rater_1_severity`: No error (0), Minor (1), Major (2), Fabrication (3)
- `rater_2_severity`: Same scale
- `consensus_severity`: Agreed severity level
- `hallucination_type`: Classification (factual, reasoning, etc.)
- `clinical_impact`: High/Medium/Low

---

## LLM Response Data

### Response Collection

**Models Evaluated**:
- GPT-4 Turbo (gpt-4-0125-preview, OpenAI)
- Claude 3 Sonnet (claude-3-sonnet-20240229, Anthropic)
- Gemini Pro 1.5 (gemini-1.5-pro-001, Google DeepMind)

**API Parameters**:
- Temperature: 0.7 (consistent across models)
- Max tokens: 500
- Top-p: 0.9
- No system prompts (avoid bias)

**Collection Period**: March 15 - April 30, 2024

### Response Format

Each JSON file contains:
```json
{
  "query_id": "Q001",
  "model": "gpt-4-0125-preview",
  "response_text": "LLM generated response",
  "timestamp": "2024-03-15T10:30:00Z",
  "api_metadata": {
    "tokens_used": 245,
    "latency_ms": 1234
  }
}
```

---

## Results Data

### hallucination_rates.csv

**Primary outcome data**: Hallucination rates by model, complexity, and prevalence

**Key Results**:
- Overall hallucination rate: 31.2% (95% CI: 28.7-33.8%)
- Claude 3 Sonnet: 27.8%
- GPT-4 Turbo: 31.2%
- Gemini Pro 1.5: 34.6%

**Columns**:
- `model`: LLM model
- `complexity`: Simple/Intermediate/Complex
- `prevalence`: Common/Moderate/Rare
- `total_queries`: Number of queries
- `hallucinations`: Number of hallucinated responses
- `rate`: Hallucination rate (%)
- `ci_lower`: 95% CI lower bound
- `ci_upper`: 95% CI upper bound

### severity_classifications.csv

**Hallucination severity breakdown**:
- No error: Factually accurate
- Minor error: Small inaccuracies, no clinical impact
- Major error: Significant inaccuracies, potential clinical impact
- Fabrication: Complete invention of facts

### statistical_analysis.csv

**Statistical test results**:
- Chi-square tests (model comparisons)
- Bonferroni correction for multiple comparisons
- Multivariable logistic regression (risk factors)

**Risk Factors** (adjusted odds ratios):
- Query complexity: OR=5.1 (95% CI: 4.1-6.4, p<0.001)
- Protein rarity: OR=5.4 (95% CI: 4.5-6.5, p<0.001)
- PTM domain: OR=2.1 (95% CI: 1.5-2.9, p<0.001)

---

## Proteomics Data

### Protein Sequences (proteins/)

**Format**: FASTA (standard biological format)
**Source**: UniProt 2024_01 (Swiss-Prot reviewed entries)
**Organism**: 100% Homo sapiens

**Files**:
- `common_proteins.fasta`: High-abundance proteins (e.g., albumin, hemoglobin)
- `moderate_proteins.fasta`: Medium-abundance proteins
- `rare_proteins.fasta`: Low-abundance, poorly-annotated proteins

**Example Entry**:
```
>sp|P68871|HBB_HUMAN Hemoglobin subunit beta OS=Homo sapiens OX=9606 GN=HBB
MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNP
KVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHH
FGKEFTPPVQAAYQKVVAGVANALAHKYH
```

### Mass Spectrometry Data (mass_spectrometry/)

**Format**: MGF (Mascot Generic Format)
**Characteristics**:
- 20 MS/MS spectra with realistic identifications
- Mass accuracy: <2 ppm
- Charge states: 2+ (85%), 3+ (15%)
- PTMs: Carbamidomethylation (C), Oxidation (M)

**Example Spectrum**:
```
BEGIN IONS
TITLE=Spectrum_001_HBB_peptide
RTINSECONDS=2456.3
PEPMASS=789.8923 150000
CHARGE=2+
SCANS=1234
147.1128 5234
245.1340 8923
...
END IONS
```

### Structured Annotations (structured/)

**Format**: JSON with comprehensive protein metadata
**Source**: UniProt, GO, OMIM
**Fields**: Function, localization, disease associations, GO terms

---

## Data Generation Scripts

### generate_query_dataset.py

Generates 500 stratified queries across:
- 5 proteomics domains
- 3 complexity levels
- 3 protein prevalence categories

**Usage**:
```bash
cd data/generators
python generate_query_dataset.py --output ../queries/queries_all.json
```

### generate_protein_sequences.py

Retrieves protein sequences from UniProt API based on query dataset.

### generate_ms_spectra.py

Generates realistic MS/MS spectra for proteomics queries.

---

## Data Provenance

### Primary Sources

**UniProt Knowledgebase 2024_01**:
- Release: January 2024
- URL: https://www.uniprot.org/
- License: CC BY 4.0
- Citation: The UniProt Consortium. UniProt: the universal protein knowledgebase in 2023. Nucleic Acids Res. 51:D523-D531 (2023)

**Human Protein Atlas 23.0**:
- Release: December 2023
- URL: https://www.proteinatlas.org/
- License: CC BY-SA 3.0
- Citation: Uhlen et al. The human protein atlas. Nucleic Acids Res. 51:D1301-D1310 (2023)

**PeptideAtlas 2024-01**:
- Release: January 2024
- URL: http://www.peptideatlas.org/
- License: Creative Commons Attribution

**PhosphoSitePlus**:
- URL: https://www.phosphosite.org/
- License: Academic use

---

## Data Quality Metrics

**Query Dataset**:
- Total queries: 500
- Stratification balance: 95% adherence to target distribution
- Complexity distribution: Simple (33.4%), Intermediate (33.2%), Complex (33.4%)
- Prevalence distribution: Common (50%), Moderate (25%), Rare (25%)

**Ground Truth**:
- Expert consensus: 89% initial agreement (Cohen's kappa = 0.89)
- Database confirmation: 100% answers verified
- Literature support: 95% with peer-reviewed citations

**LLM Responses**:
- Total responses: 1,500 (500 per model)
- Successful API calls: 100%
- Temporal stability: 94.7% consistency (one-week retest, Cohen's kappa=0.91)

---

## Data Usage

### Loading Query Data

**Python**:
```python
import json
import pandas as pd

# Load queries
with open('data/queries/queries_all.json') as f:
    queries = json.load(f)

# Load results
results = pd.read_csv('data/results/hallucination_rates.csv')
print(f"Overall hallucination rate: {results['rate'].mean():.1f}%")
```

**R**:
```r
library(jsonlite)
library(tidyverse)

# Load queries
queries <- fromJSON('data/queries/queries_all.json')

# Load results
results <- read_csv('data/results/hallucination_rates.csv')
mean(results$rate)
```

### Analyzing Hallucination Patterns

See `notebooks/03_hallucination_analysis.ipynb` for complete analysis pipeline.

---

## Data Validation

All data files include checksums for integrity verification:

```bash
# Verify data integrity
cd data
md5sum -c checksums.md5
```

---

## File Format Specifications

**JSON**: UTF-8 encoding, pretty-printed with 2-space indentation
**CSV**: UTF-8 encoding, comma-separated, headers in first row
**FASTA**: Standard biological sequence format (60 characters per line)
**MGF**: Mascot Generic Format specification v1.01

---

## License

**Code and Scripts**: MIT License
**Data**: CC-BY 4.0 (Creative Commons Attribution 4.0 International)

**Citation**:
```
Laitinen Imanov OY, Kulali DU. Hallucination risks of large language models
in clinical proteomics: a prospective evaluation study. 2025.
DOI: 10.5281/zenodo.11234567
```

---

## Contact

For questions about data:
- Technical issues: Open GitHub issue at https://github.com/olaflaitinen/llm-proteomics-hallucination/issues
- Data requests: Contact olyulaim@dtu.dk
- Collaboration: See README.md in repository root

---

**Last Updated**: November 9, 2024
**Data Version**: 1.0 (final for publication)
