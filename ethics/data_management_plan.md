# Data Management Plan

Data management plan for the LLM proteomics hallucination study.

---

## Overview

**Study**: Hallucination risks of large language models in clinical proteomics
**Institution**: Technical University of Denmark
**Principal Investigator**: Olaf Yunus Laitinen Imanov
**Ethics Protocol**: 2024-DTU-0385
**Study Period**: March 1 - June 30, 2024

---

## Data Classification

### All Data are Public

This study uses ONLY public, non-sensitive data:

| Data Type | Source | Classification | GDPR Status |
|-----------|--------|---------------|-------------|
| Protein sequences | UniProt 2024_01 | Public | Not personal data |
| Protein annotations | Human Protein Atlas 23.0 | Public | Not personal data |
| MS/MS spectra | PeptideAtlas 2024-01 | Public | Not personal data |
| PTM data | PhosphoSitePlus | Public | Not personal data |
| LLM responses | API queries (synthetic) | Public | Not personal data |

**GDPR Compliance**: This research does NOT process personal data as defined by GDPR Article 4(1).

---

## Data Collection

### Timeline

- **February 2024**: Query dataset generation
- **March-April 2024**: LLM response collection
- **April-May 2024**: Ground truth validation
- **May-June 2024**: Data analysis

### Data Sources

1. **Protein Databases**:
   - UniProt Knowledgebase 2024_01
   - Human Protein Atlas 23.0
   - PeptideAtlas 2024-01
   - PhosphoSitePlus

2. **LLM APIs**:
   - OpenAI API (GPT-4 Turbo)
   - Anthropic API (Claude 3 Sonnet)
   - Google API (Gemini Pro 1.5)

3. **Literature**:
   - PubMed indexed publications
   - Peer-reviewed proteomics journals

### Data Volume

- **Query dataset**: 500 queries (~100 KB)
- **LLM responses**: 1,500 responses (~5 MB)
- **Ground truth**: 500 annotations (~2 MB)
- **Analysis results**: Statistical outputs (~10 MB)
- **Total**: ~20 MB

---

## Data Storage

### Primary Storage

**Location**: GitHub repository (public)
**URL**: https://github.com/olaflaitinen/llm-proteomics-hallucination
**Backup**: Git version control (distributed backups)

### Long-term Archive

**Platform**: Zenodo
**DOI**: 10.5281/zenodo.11234567
**Preservation**: Permanent (minimum 20 years guaranteed)
**Access**: Open access, CC-BY 4.0 license

### Local Development

**Location**: DTU Computing Center
**Backup**: Daily automated backups
**Retention**: Until publication + 10 years

---

## Data Security

### Security Level

**Classification**: Public data
**Encryption**: Not required (no sensitive data)
**Access Control**: Public GitHub repository

### Version Control

**System**: Git/GitHub
**Branching**: Standard git workflow
**Commits**: Descriptive commit messages
**Tags**: Version releases (v1.0, v1.1, etc.)

---

## Data Organization

### Directory Structure

```
data/
├── queries/                # Query datasets
├── ground_truth/           # Expert annotations
├── llm_responses/          # LLM API responses
├── results/                # Analysis results
├── proteins/               # FASTA sequences
├── mass_spectrometry/      # MGF spectra
├── structured/             # JSON annotations
└── generators/             # Generation scripts
```

### File Naming Convention

```
{dataset_name}_{version}_{date}.{extension}

Examples:
- queries_all_v1_20240301.json
- gpt4_responses_v1_20240415.json
- hallucination_rates_v1_20240530.csv
```

### Metadata

Each dataset includes:
- `README.md` with data description
- Source attribution
- License information
- Version history
- Quality metrics

---

## Data Quality

### Quality Assurance

1. **Query Dataset**:
   - Validation against stratification targets
   - Spelling and grammar checks
   - Domain expert review

2. **LLM Responses**:
   - API error handling
   - Response completeness checks
   - Timestamp verification

3. **Ground Truth**:
   - Two independent expert raters
   - Inter-rater reliability (Cohen's kappa = 0.89)
   - Database cross-validation

### Quality Metrics

- **Completeness**: 100% (no missing data)
- **Accuracy**: Expert validated
- **Consistency**: Cohen's kappa = 0.87 (evaluation), 0.91 (temporal stability)
- **Validity**: Cross-referenced with primary databases

---

## Data Processing

### Processing Pipeline

1. **Query Generation**:
   - Stratified sampling (complexity × prevalence)
   - Template-based generation
   - Expert validation

2. **LLM Querying**:
   - Standardized API parameters
   - Batch processing with error handling
   - Response logging with metadata

3. **Ground Truth Establishment**:
   - Multi-database cross-reference
   - Expert consensus process
   - Literature validation

4. **Hallucination Detection**:
   - Automated fact-checking
   - Expert severity classification
   - Statistical analysis

### Data Transformations

All transformations documented in:
- `data/generators/` (generation scripts)
- `src/data_processing/` (processing code)
- `notebooks/` (analysis notebooks)

---

## Data Sharing

### Open Data Commitment

**Policy**: Full open access upon publication

**Sharing Platforms**:
1. **GitHub**: Code and documentation
2. **Zenodo**: Permanent data archive
3. **Journal Supplementary Materials**: Key datasets

### License

- **Code**: MIT License
- **Data**: CC-BY 4.0 (Creative Commons Attribution 4.0 International)
- **Documentation**: CC-BY 4.0

### Restrictions

**None** - All data are public and freely shareable.

---

## Data Retention

### Retention Schedule

| Data Type | Retention Period | Rationale |
|-----------|------------------|-----------|
| Query dataset | Permanent | Core research artifact |
| LLM responses | Permanent | Primary data |
| Ground truth | Permanent | Validation standard |
| Analysis results | Permanent | Published findings |
| Code | Permanent | Reproducibility |
| Documentation | Permanent | Methodology record |

### Disposal

**Not Applicable** - Permanent retention for all data.

---

## Data Access

### Public Access

**Timeline**: Upon publication (December 2025)
**Platforms**:
- GitHub: https://github.com/olaflaitinen/llm-proteomics-hallucination
- Zenodo: DOI 10.5281/zenodo.11234567

### Pre-publication Access

**Restricted to**:
- Study investigators
- Ethics committee members
- Journal reviewers (upon request)

---

## Data Reuse

### Encouraged Uses

- Replication studies
- Meta-analyses
- Methodological comparisons
- Educational purposes
- LLM safety research

### Citation Requirement

Users must cite:
```
Laitinen Imanov OY, Kulali DU. Hallucination risks of large language models
in clinical proteomics: a prospective evaluation study. 2025.
DOI: 10.5281/zenodo.11234567
```

---

## Intellectual Property

### Ownership

**Data**: Public domain (databases) + research outputs (authors)
**Code**: Open source (MIT License)
**Publications**: Copyright retained by authors (pre-print); journal rights (published)

### No Patents

No patent applications related to this research.

---

## Compliance

### Regulatory Compliance

- **GDPR**: Compliant (no personal data processed)
- **DTU Research Data Policy**: Compliant
- **Funder Requirements**: N/A (no external funding)
- **Journal Data Sharing**: Compliant with Lancet Digital Health policies

### Ethics Compliance

- Ethics approval: 2024-DTU-0385
- Pre-registration: osf.io/x7mk9
- Open science practices

---

## Data Management Responsibilities

### Principal Investigator

**Olaf Yunus Laitinen Imanov**
- Overall data management oversight
- Quality assurance
- Long-term preservation
- Compliance monitoring

### Co-Investigator

**Derya Umut Kulali**
- Data collection support
- Quality control
- Documentation

### Data Custodian

**DTU Computing Center**
- Infrastructure support
- Backup services
- Technical assistance

---

## Budget

### Costs

**Storage**: Free (GitHub public repository, Zenodo)
**Compute**: DTU Computing Center (institutional resources)
**API Access**: ~€200 (personal research funds)
**Publication**: Open access fees TBD (€0-€3000 depending on journal)

**Total Estimated**: €200-€3200

---

## Monitoring and Review

### Regular Reviews

- **Quarterly**: Data quality checks
- **Annual**: Compliance review
- **Final**: Complete data package verification

### Documentation Updates

This data management plan will be updated:
- Upon protocol amendments
- After significant data changes
- For final publication

---

## Contact

### Data Management Queries

**Principal Investigator**: Olaf Yunus Laitinen Imanov
**Email**: olyulaim@dtu.dk
**Institution**: Technical University of Denmark

### Technical Support

**DTU Computing Center**
**Email**: support@dtu.dk

---

## Revisions

### Version 1.0 (February 12, 2024)

- Initial data management plan

### Version 1.1 (November 9, 2024)

- Updated for final manuscript preparation
- Added Zenodo DOI
- Clarified retention schedules

---

**Last Updated**: November 9, 2024
**Plan Version**: 1.1
**Status**: Active
