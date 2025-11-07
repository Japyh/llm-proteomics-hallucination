# Data Directory

This directory contains data for the LLM proteomics hallucination research project.

## Directory Structure

```
data/
├── raw/                # Raw data files (NEVER commit real patient data)
├── processed/          # Processed and cleaned datasets
└── synthetic/          # Synthetic test data (safe to commit)
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
