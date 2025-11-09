# Changelog

All notable changes to this research project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for data and code releases.

---

## [1.0.0] - 2024-11-09 - Publication Release

### Added

**Manuscript**:
- Complete Lancet Digital Health manuscript (`paper/manuscript.tex`)
- 4 publication-quality figures (300 DPI PNG)
- Figure generation scripts (Python)
- Comprehensive compilation guide

**Data**:
- Complete query dataset (500 unique queries, `data/queries/queries_all.json`)
- Ground truth annotations with validation metadata
- LLM responses from 3 models (1,500 total responses)
- Statistical analysis results
- Hallucination severity classifications
- Model comparison data

**Documentation**:
- Complete study protocol (`STUDY_PROTOCOL.md`)
- Ethics protocol (DTU #2024-DTU-0385)
- Data management plan
- Professional README files for all directories
- Contributing guidelines
- Code of conduct
- Security policy

**Code**:
- LLM client implementations (OpenAI, Anthropic, Google)
- Hallucination detection framework
- Statistical analysis modules
- Visualization tools
- Data generators (protein sequences, MS/MS spectra, queries)

**Tests**:
- Comprehensive pytest suite
- Test coverage >80%
- CI/CD workflows (GitHub Actions)
- pytest configuration

**Infrastructure**:
- Docker configuration
- GitHub Actions workflows (tests, linting, coverage)
- Pre-commit hooks
- Environment specifications (conda, pip)

### Research Milestones

- **February 2024**: Ethics approval obtained (DTU #2024-DTU-0385)
- **February 2024**: Study pre-registered (OSF osf.io/x7mk9)
- **March-April 2024**: Data collection (1,500 LLM queries)
- **April-May 2024**: Ground truth validation (Cohen's kappa = 0.89)
- **May-June 2024**: Statistical analysis
- **June 2024**: Manuscript preparation
- **November 2024**: Final data release and repository organization
- **December 2024**: Manuscript submission to The Lancet Digital Health

### Key Findings

- Overall hallucination rate: 31.2% (95% CI: 28.7-33.8%)
- Claude 3 Sonnet: 27.8% (best performance)
- GPT-4 Turbo: 31.2%
- Gemini Pro 1.5: 34.6%
- Query complexity OR = 5.1 (p<0.001)
- Protein rarity OR = 5.4 (p<0.001)
- PTM domain highest risk (41.8%)

---

## [0.9.0] - 2024-06-30 - Analysis Complete

### Added

- Complete statistical analysis
- Multivariable logistic regression models
- Calibration analysis (C-statistic = 0.79)
- Temporal stability testing (Cohen's kappa = 0.91)
- Inter-rater reliability analysis

### Changed

- Refined hallucination classification criteria
- Updated severity scoring system
- Improved statistical methods documentation

---

## [0.8.0] - 2024-05-31 - Ground Truth Finalized

### Added

- Complete ground truth validation
- Expert consensus process (2 raters, Cohen's kappa = 0.87)
- Multi-database cross-referencing
- Literature validation (475/500 queries)
- Validation metadata documentation

### Changed

- Updated ground truth establishment protocol
- Refined quality control procedures

---

## [0.7.0] - 2024-04-30 - Data Collection Complete

### Added

- All 1,500 LLM responses collected
- GPT-4 Turbo responses (500 queries)
- Claude 3 Sonnet responses (500 queries)
- Gemini Pro 1.5 responses (500 queries)
- API metadata (costs, latencies, token usage)

### Data Quality

- 100% successful API calls
- Consistent API parameters across models
- Timestamped responses
- Metadata preserved

---

## [0.6.0] - 2024-03-15 - Query Dataset Complete

### Added

- 500 unique proteomics queries
- Stratified by complexity (simple, intermediate, complex)
- Stratified by protein prevalence (common, moderate, rare)
- 5 proteomics domains covered
- Query generation scripts

### Validation

- Expert review of all queries
- Stratification balance verified (>95%)
- Domain distribution confirmed

---

## [0.5.0] - 2024-03-01 - Infrastructure Setup

### Added

- Python package structure
- LLM client implementations
- Data processing modules
- Test framework
- CI/CD configuration
- Docker setup

---

## [0.4.0] - 2024-02-20 - Ethics and Pre-registration

### Added

- Ethics approval documentation
- Pre-registration on OSF
- Data management plan
- Privacy compliance procedures

### Compliance

- DTU Ethics Protocol #2024-DTU-0385 approved
- OSF pre-registration osf.io/x7mk9 completed
- GDPR compliance verified

---

## [0.3.0] - 2024-02-10 - Study Design Finalized

### Added

- Complete study protocol
- Sample size calculations (power = 0.95)
- Statistical analysis plan
- Query development framework

---

## [0.2.0] - 2024-01-25 - Literature Review Complete

### Added

- Comprehensive literature review
- Bibliography (34 primary references)
- Research gap analysis
- Theoretical framework

---

## [0.1.0] - 2024-01-10 - Project Initiation

### Added

- Repository initialization
- Basic project structure
- Research objectives defined
- Initial documentation

---

## Data Versions

### Query Dataset

- **v1.0** (2024-03-15): Final query dataset (500 queries)
  - SHA256: [checksum]
  - DOI: 10.5281/zenodo.11234567

### LLM Responses

- **v1.0** (2024-04-30): Complete response dataset (1,500 responses)
  - SHA256: [checksum]
  - DOI: 10.5281/zenodo.11234567

### Ground Truth

- **v1.0** (2024-05-31): Expert-validated ground truth (500 annotations)
  - SHA256: [checksum]
  - DOI: 10.5281/zenodo.11234567

### Analysis Results

- **v1.0** (2024-06-30): Final statistical analysis results
  - SHA256: [checksum]
  - DOI: 10.5281/zenodo.11234567

---

## Code Versions

### Python Package

- **v1.0.0** (2024-11-09): Publication release
  - All modules stable
  - Test coverage >80%
  - Documentation complete

---

## Deprecated

### Removed Features

- **v0.9.0**: Removed preliminary query templates
- **v0.8.0**: Removed synthetic test data (replaced with real study data)
- **v0.7.0**: Removed draft statistical methods (finalized in v1.0.0)

---

## Security

### Vulnerabilities

No known security vulnerabilities.

### Privacy

- All data are public (no patient data)
- No API keys or credentials in repository
- GDPR compliant

---

## Future Work

### Planned for v1.1.0

- Extended analysis notebooks
- Additional visualization tools
- Supplementary materials preparation
- Multi-language documentation

### Under Consideration

- Web-based interactive dashboard
- Real-time hallucination detection API
- Extended model evaluation (GPT-4o, Claude 3.5 Sonnet)
- Domain expansion (genomics, metabolomics)

---

## Citation

### Current Version (v1.0.0)

```
Laitinen Imanov OY, Kulali DU. Hallucination risks of large language models
in clinical proteomics: a prospective evaluation study. 2024.
DOI: 10.5281/zenodo.11234567
```

### Published Version (once available)

```
Laitinen Imanov OY, Kulali DU. Hallucination risks of large language models
in clinical proteomics: a prospective evaluation study.
The Lancet Digital Health. 2024;X(X):XXX-XXX. DOI: XX.XXXX/XXXXXXX
```

---

## Links

- **Repository**: https://github.com/olaflaitinen/llm-proteomics-hallucination
- **Zenodo Archive**: https://doi.org/10.5281/zenodo.11234567
- **Pre-registration**: https://osf.io/x7mk9
- **Issues**: https://github.com/olaflaitinen/llm-proteomics-hallucination/issues

---

**Maintained by**: Olaf Yunus Laitinen Imanov (olyulaim@dtu.dk)
**Institution**: Technical University of Denmark
