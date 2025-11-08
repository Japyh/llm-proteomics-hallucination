# Data Directory

This directory contains data for the LLM proteomics hallucination research project.

## Directory Structure

```
data/
├── proteins/              # Protein sequence data (FASTA format)
├── mass_spectrometry/     # MS/MS spectra (MGF format)
├── results/               # Proteomics analysis results (CSV)
├── structured/            # Structured annotations (JSON)
├── database_snapshots/    # UniProt/GO database excerpts
├── generators/            # Python scripts to regenerate data
├── queries/               # LLM test queries
├── ground_truth/          # Expert-validated annotations
├── llm_responses/         # LLM-generated responses
├── raw/                   # Raw data (NEVER commit patient data)
├── processed/             # Processed and cleaned datasets
└── synthetic/             # Synthetic test data (safe to commit)
```

## Proteomics Data Formats

### Protein Sequences (`proteins/`)

**Format**: FASTA (standard biological sequence format)

**Files**:
- `high_coverage_proteins.fasta` - 20 well-characterized human proteins
- `low_coverage_proteins.fasta` - 5 poorly-annotated proteins

**Source**: UniProt Knowledgebase Release 2024_03

**Usage Example (Python)**:
```python
from Bio import SeqIO

# Parse FASTA file
for record in SeqIO.parse("data/proteins/high_coverage_proteins.fasta", "fasta"):
    print(f"ID: {record.id}")
    print(f"Description: {record.description}")
    print(f"Sequence length: {len(record.seq)}")
```

**Usage Example (R)**:
```r
library(seqinr)

# Read FASTA file
sequences <- read.fasta("data/proteins/high_coverage_proteins.fasta")
seq_lengths <- sapply(sequences, length)
```

**Format Specification**:
- Header line starts with `>` followed by UniProt accession
- Format: `>sp|ACCESSION|ENTRY_NAME Description OS=Organism OX=TaxID GN=Gene`
- Sequence lines: 60 characters per line (standard convention)
- Standard amino acid one-letter codes (A-Z excluding B, J, O, U, Z)

### Mass Spectrometry Data (`mass_spectrometry/`)

**Format**: MGF (Mascot Generic Format)

**Files**:
- `example_spectra.mgf` - 20 MS/MS spectra with realistic peptide identifications

**Characteristics**:
- Retention times: 1234-4123 seconds
- Charge states: 2+ and 3+
- Mass accuracy: <2 ppm mass error
- Post-translational modifications: Carbamidomethylation (C), Oxidation (M)

**Usage Example (Python)**:
```python
import pyteomics.mgf

# Read MGF file
with pyteomics.mgf.MGF("data/mass_spectrometry/example_spectra.mgf") as spectra:
    for spectrum in spectra:
        print(f"Title: {spectrum['params']['title']}")
        print(f"Precursor m/z: {spectrum['params']['pepmass'][0]}")
        print(f"Charge: {spectrum['params']['charge'][0]}")
        print(f"Number of peaks: {len(spectrum['m/z array'])}")
```

**Usage Example (R)**:
```r
library(MSnbase)

# Read MGF file
ms_data <- readMgfData("data/mass_spectrometry/example_spectra.mgf")
print(ms_data)
precursor_mz <- precursorMz(ms_data)
```

**Format Specification**:
```
BEGIN IONS
TITLE=Spectrum identifier and description
RTINSECONDS=retention_time
PEPMASS=precursor_mz intensity
CHARGE=charge_state
SCANS=scan_number
m/z_1 intensity_1
m/z_2 intensity_2
...
END IONS
```

### Proteomics Results (`results/`)

**Format**: CSV (Comma-Separated Values)

**Files**:
1. `protein_identifications.csv` - 25 identified proteins
2. `peptide_matches.csv` - 25 peptide-spectrum matches
3. `quantification_results.csv` - Label-free quantification data
4. `hallucination_rates.csv` - LLM hallucination analysis

**Usage Example (Python)**:
```python
import pandas as pd

# Load protein identifications
proteins_df = pd.read_csv("data/results/protein_identifications.csv")
print(f"Identified proteins: {len(proteins_df)}")
print(f"Average coverage: {proteins_df['Coverage_Percent'].mean():.1f}%")

# Load quantification results
quant_df = pd.read_csv("data/results/quantification_results.csv")
significant = quant_df[quant_df['Significant'] == 'Yes']
print(f"Significantly regulated proteins: {len(significant)}")

# Load peptide matches
peptides_df = pd.read_csv("data/results/peptide_matches.csv")
high_confidence = peptides_df[peptides_df['Confidence'] == 'High']
print(f"High-confidence PSMs: {len(high_confidence)}")
```

**Usage Example (R)**:
```r
library(tidyverse)

# Load protein identifications
proteins <- read_csv("data/results/protein_identifications.csv")
summary(proteins$Coverage_Percent)

# Load quantification results
quant <- read_csv("data/results/quantification_results.csv")
significant <- quant %>% filter(Significant == "Yes")

# Load peptide matches
peptides <- read_csv("data/results/peptide_matches.csv")
```

**Column Specifications**:

*protein_identifications.csv*:
- `Protein_ID`: UniProt accession (e.g., P68871)
- `Gene_Name`: HGNC gene symbol (e.g., HBB)
- `Protein_Name`: Full protein name
- `Score`: Identification score (higher = better)
- `Coverage_Percent`: Sequence coverage (0-100%)
- `Unique_Peptides`: Number of unique peptides
- `Total_PSMs`: Total peptide-spectrum matches
- `MW_kDa`: Molecular weight in kilodaltons
- `pI`: Isoelectric point
- `Database_Coverage`: High/Medium/Low annotation quality

*peptide_matches.csv*:
- `Spectrum_ID`: Unique spectrum identifier
- `Peptide_Sequence`: Unmodified peptide sequence
- `Modified_Sequence`: Sequence with PTM notation
- `Protein_ID`: Parent protein UniProt accession
- `Charge`: Peptide charge state
- `MZ_Observed`: Observed m/z value
- `MZ_Theoretical`: Theoretical m/z value
- `Mass_Error_ppm`: Mass accuracy in parts per million
- `Score`: Match quality score
- `Confidence`: High/Medium/Low confidence level
- `PTMs`: Post-translational modifications

*quantification_results.csv*:
- `Protein_ID`: UniProt accession
- `Sample_ID`: Sample identifier (Control/Treatment)
- `Abundance_Log2`: Log2-transformed abundance
- `Abundance_Raw`: Raw abundance value
- `CV_Percent`: Coefficient of variation (%)
- `Normalized_Abundance`: Normalized intensity value
- `Regulation`: Upregulated/Downregulated/Unchanged
- `Fold_Change`: Expression ratio (treatment/control)
- `P_Value`: Statistical significance (t-test)
- `Adjusted_P_Value`: FDR-corrected p-value
- `Significant`: Yes/No (threshold: adj. p < 0.05, |FC| > 1.5)

### Structured Annotations (`structured/`)

**Format**: JSON (JavaScript Object Notation)

**Files**:
- `protein_database_entries.json` - 5 proteins with comprehensive annotations

**Source**: UniProt, Gene Ontology Consortium, OMIM

**Usage Example (Python)**:
```python
import json

# Load protein annotations
with open("data/structured/protein_database_entries.json") as f:
    proteins = json.load(f)

for protein in proteins:
    print(f"\nProtein: {protein['protein_name']}")
    print(f"UniProt ID: {protein['uniprot_id']}")
    print(f"Gene: {protein['gene_name']}")
    print(f"Function: {protein['function']}")

    # Print GO terms
    print("GO terms:")
    for go_term in protein['go_terms']:
        print(f"  - {go_term['term']} ({go_term['id']})")

    # Print disease associations
    if protein['disease_associations']:
        print("Disease associations:")
        for disease in protein['disease_associations']:
            print(f"  - {disease['disease']} ({disease['omim']})")
```

**Usage Example (R)**:
```r
library(jsonlite)

# Load protein annotations
proteins <- fromJSON("data/structured/protein_database_entries.json")

# Access protein properties
protein_names <- proteins$protein_name
gene_names <- proteins$gene_name

# Extract GO terms
go_terms <- proteins$go_terms
```

**Schema**:
```json
{
  "uniprot_id": "UniProt accession",
  "gene_name": "HGNC gene symbol",
  "protein_name": "Full protein name",
  "organism": "Homo sapiens",
  "organism_id": 9606,
  "length": 147,
  "molecular_weight_da": 15867,
  "isoelectric_point": 6.81,
  "sequence": "Amino acid sequence",
  "function": "Functional description",
  "subcellular_location": ["Location1", "Location2"],
  "tissue_specificity": ["Tissue1", "Tissue2"],
  "disease_associations": [
    {
      "disease": "Disease name",
      "omim": "OMIM identifier",
      "variant": "Mutation description",
      "clinical_significance": "Pathogenic/Benign"
    }
  ],
  "database_coverage": "High/Medium/Low",
  "pubmed_citations": 15234,
  "uniprot_date": "2024-03-20",
  "go_terms": [
    {
      "id": "GO:0005344",
      "term": "oxygen carrier activity",
      "category": "molecular_function"
    }
  ],
  "interactions": ["P69905", "P69891"],
  "domains": ["Globin"],
  "signal_peptide": false,
  "transmembrane": false
}
```

## Data Provenance

### Primary Sources

**UniProt Knowledgebase**:
- Release: 2024_03 (March 2024)
- URL: https://www.uniprot.org/
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Citation: The UniProt Consortium. UniProt: the universal protein knowledgebase in 2023. Nucleic Acids Res. 51:D523-D531 (2023)

**Gene Ontology**:
- Release: 2024-03-01
- URL: http://geneontology.org/
- License: Creative Commons Attribution 4.0 International
- Citation: The Gene Ontology Consortium. The Gene Ontology resource: enriching a GOld mine. Nucleic Acids Res. 49:D325-D334 (2021)

**OMIM (Online Mendelian Inheritance in Man)**:
- URL: https://www.omim.org/
- License: Research use only (restrictions apply)
- Citation: Hamosh A, et al. Online Mendelian Inheritance in Man (OMIM). Hum Mutat. 15:57-61 (2000)

### Data Quality Metrics

**Protein Sequences**:
- Total proteins: 25 (20 high coverage + 5 low coverage)
- Sequence source: 100% from UniProt reviewed entries (Swiss-Prot)
- Organisms: 100% Homo sapiens
- Median sequence length: 335 amino acids
- Median molecular weight: 36.0 kDa

**Mass Spectrometry Data**:
- Total spectra: 20
- Precursor mass accuracy: <2 ppm
- Charge states: 2+ (85%), 3+ (15%)
- Retention time range: 1234-4123 seconds
- Average peaks per spectrum: 7-9
- PTM coverage: Carbamidomethylation (50%), Oxidation (30%), None (20%)

**Protein Identifications**:
- Total identifications: 25
- Median sequence coverage: 73.2%
- Median unique peptides: 13
- Score range: 38.9-456.7
- Database coverage distribution: High (68%), Medium (24%), Low (8%)

**Quantification Data**:
- Total measurements: 36 (18 control + 18 treatment)
- Median CV: 8.9%
- Significantly regulated proteins: 11/18 (61%)
- Median fold change (significant): 2.48
- P-value threshold: 0.05 (FDR-corrected)

## Data Validation

### Quality Control Checks

**FASTA Files**:
```python
from Bio import SeqIO

def validate_fasta(fasta_file):
    """Validate FASTA file quality."""
    valid_aa = set("ACDEFGHIKLMNPQRSTVWY")

    for record in SeqIO.parse(fasta_file, "fasta"):
        seq_str = str(record.seq).upper()

        # Check for invalid characters
        invalid = set(seq_str) - valid_aa
        if invalid:
            print(f"Warning: Invalid amino acids in {record.id}: {invalid}")

        # Check length
        if len(record.seq) < 50:
            print(f"Warning: Short sequence in {record.id}: {len(record.seq)} aa")

        # Check for unusual composition
        x_count = seq_str.count('X')
        if x_count > 0:
            print(f"Warning: {x_count} unknown residues (X) in {record.id}")

validate_fasta("data/proteins/high_coverage_proteins.fasta")
```

**MGF Files**:
```python
import pyteomics.mgf

def validate_mgf(mgf_file):
    """Validate MGF file quality."""
    with pyteomics.mgf.MGF(mgf_file) as spectra:
        for i, spectrum in enumerate(spectra):
            # Check required fields
            required = ['title', 'pepmass', 'charge']
            missing = [f for f in required if f not in spectrum['params']]
            if missing:
                print(f"Spectrum {i}: Missing fields {missing}")

            # Check peak count
            if len(spectrum['m/z array']) < 3:
                print(f"Spectrum {i}: Too few peaks ({len(spectrum['m/z array'])})")

            # Check m/z ordering
            if not all(spectrum['m/z array'][i] <= spectrum['m/z array'][i+1]
                      for i in range(len(spectrum['m/z array'])-1)):
                print(f"Spectrum {i}: m/z values not sorted")

validate_mgf("data/mass_spectrometry/example_spectra.mgf")
```

**CSV Files**:
```python
import pandas as pd

def validate_protein_ids(csv_file):
    """Validate protein identifications CSV."""
    df = pd.read_csv(csv_file)

    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        print(f"Missing values:\n{missing[missing > 0]}")

    # Validate coverage percentages
    invalid_coverage = df[(df['Coverage_Percent'] < 0) |
                          (df['Coverage_Percent'] > 100)]
    if not invalid_coverage.empty:
        print(f"Invalid coverage values: {len(invalid_coverage)}")

    # Validate UniProt IDs
    import re
    uniprot_pattern = re.compile(r'^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$')
    invalid_ids = df[~df['Protein_ID'].str.match(uniprot_pattern)]
    if not invalid_ids.empty:
        print(f"Invalid UniProt IDs: {invalid_ids['Protein_ID'].tolist()}")

validate_protein_ids("data/results/protein_identifications.csv")
```

## Data Organization Guidelines

### Raw Data (`raw/`)

**Purpose**: Store unprocessed data files
**Privacy Level**: MAXIMUM - Assume all files contain sensitive information

**CRITICAL**: This directory should NEVER contain real patient data in version control. See `raw/WARNING.md` for details.

For local development with real data:
1. Store on encrypted local drive only
2. Never commit to git
3. Use synthetic data for testing and development
4. Follow anonymization procedures before any processing

### Processed Data (`processed/`)

**Purpose**: Store cleaned, transformed, and analyzed datasets

**Guidelines**:
- Only commit synthetic or fully anonymized data
- Include data processing documentation
- Maintain data lineage (track transformations)
- Include checksums for data integrity

### Synthetic Data (`synthetic/`)

**Purpose**: Safe-to-share synthetic datasets for development and testing

**Available Datasets**:
- `example_proteins.csv` - 50+ synthetic protein entries with realistic properties
- Additional synthetic datasets will be added as needed

**Characteristics**:
- Realistic statistical properties
- No relation to real patients
- Safe for version control
- Suitable for testing and development

## Data Privacy and GDPR Compliance

### Legal Requirements

This research must comply with:
- **GDPR** (General Data Protection Regulation)
- **HIPAA** (if working with US patient data)
- **Local data protection laws**
- **Institutional review board (IRB)** requirements

### Data Classification

| Level | Description | Storage | Version Control |
|-------|-------------|---------|-----------------|
| Public | Synthetic, no PII | Any | YES - Safe to commit |
| Internal | Anonymized research data | Secure server | NO |
| Confidential | Pseudonymized clinical data | Encrypted storage | NO |
| Restricted | Real patient data | Air-gapped encrypted | NO |

### Anonymization Guidelines

Before processing any real data:

1. **Remove Direct Identifiers**:
   - Names
   - Addresses
   - Medical record numbers
   - Device identifiers
   - Social security numbers
   - Account numbers
   - License/registration numbers
   - URLs
   - IP addresses
   - Biometric identifiers
   - Photographs
   - Any other unique identifying number or code

2. **Remove Quasi-Identifiers**:
   - Exact dates (use year or quarter instead)
   - Geographic subdivisions smaller than state
   - Exact ages over 89 (use 90+ category)
   - Rare diagnoses
   - Unusual combinations of common features

3. **Apply k-Anonymity**:
   - Ensure each record is indistinguishable from at least k-1 other records
   - Use generalization and suppression techniques
   - Verify no individual can be identified

4. **Document Process**:
   - Record all anonymization steps
   - Maintain (separate) mapping for potential re-identification if legally required
   - Store anonymization logs securely

### Data Usage Protocol

```python
# Example: Loading data safely
import pandas as pd
from src.data_processing.data_anonymizer import load_safe_data

# CORRECT: Load synthetic data
df = pd.read_csv('data/synthetic/example_proteins.csv')

# CORRECT: Load real data with anonymization
df = load_safe_data('local_secure_path/real_data.csv', anonymize=True)

# INCORRECT: Never do this
df = pd.read_csv('data/raw/patient_records.csv')  # DANGEROUS!
```

## Data Quality Standards

### Required Metadata

Each dataset should include:
- **Source**: Where the data came from
- **Date**: When it was created/collected
- **Version**: Dataset version number
- **Format**: File format and schema
- **Size**: Number of records and features
- **Quality**: Completeness, accuracy assessment
- **Processing**: Transformations applied
- **License**: Usage restrictions

### Data Validation

Before using any dataset:
1. Check for missing values
2. Verify data types
3. Validate ranges (e.g., molecular weights within expected bounds)
4. Check for duplicates
5. Verify referential integrity
6. Run quality control scripts

## File Naming Conventions

```
{dataset_name}_{version}_{date}_{description}.{extension}

Examples:
- synthetic_proteins_v1_20240115_initial.csv
- ms_results_processed_v2_20240120_cleaned.parquet
- hallucination_test_cases_v1_20240125_expert_validated.json
```

## Supported Data Formats

### Preferred Formats
- **Tabular**: CSV, Parquet (for large datasets)
- **Hierarchical**: JSON, YAML
- **Binary**: HDF5 (for numerical arrays)
- **Mass Spec**: mzML, mzXML (standard formats)

### Format Selection Guide
- Small datasets (<100MB): CSV
- Large datasets (>100MB): Parquet or HDF5
- Nested structures: JSON
- Time series: HDF5
- Mass spec raw: mzML

## Data Access and Permissions

### Local Development
- All team members have read access to synthetic data
- Real data access requires IRB approval
- Document all data access in lab notebook

### Sharing Data
- Synthetic data: Can be shared publicly
- Anonymized data: Requires data sharing agreement
- Real patient data: NEVER share without explicit consent and legal approval

## Data Retention and Destruction

### Retention Policy
- Synthetic data: Permanent (part of research artifacts)
- Anonymized research data: 10 years post-publication
- Real patient data: Follow institutional policy (typically 7-25 years)
- Temporary analysis files: Delete after analysis completion

### Destruction Procedure
When data must be destroyed:
1. Securely delete files (use secure deletion tools)
2. Remove backups
3. Document destruction in data management log
4. Verify deletion completion

## Troubleshooting

### Large Files
If data files are too large for git:
```bash
# Use Git LFS for large files
git lfs track "*.parquet"
git add .gitattributes

# Or use external storage and document location
echo "Large dataset stored at: /secure/storage/path" > data/processed/large_dataset.location
```

### Data Not Loading
1. Check file permissions
2. Verify file path
3. Check data format consistency
4. Review error messages
5. Validate against schema

## Resources

- [GDPR Guidelines](https://gdpr.eu/)
- [HIPAA Compliance](https://www.hhs.gov/hipaa/)
- [Data Anonymization Handbook](../ethics/anonymization_guidelines.md)
- [IRB Protocol](../ethics/ethics_protocol.md)

## Contact

For questions about data handling:
- Data privacy: See `/ethics/data_management_plan.md`
- Technical issues: Open GitHub issue
- Ethical concerns: Contact IRB coordinator

---

**Remember**: When in doubt about data privacy, ask first. It's better to be overly cautious than to risk a data breach.
