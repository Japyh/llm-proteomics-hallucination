# Research Ethics Protocol

Ethics documentation for the LLM proteomics hallucination study.

---

## Ethics Approval

**Institution**: Institutional Review Board
**Protocol Number**: 2025-IRB-1101
**Approval Date**: October 28, 2025
**Principal Investigator**: Olaf Yunus Laitinen Imanov

**Study Title**: Hallucination risks of large language models in clinical proteomics: a prospective evaluation study

**Study Period**: November 1 - December 15, 2025

---

## Pre-registration

**Platform**: Open Science Framework (OSF)
**Registration ID**: osf.io/x7mk9
**Registration Date**: October 25, 2025
**Status**: Public

---

## Ethical Framework

This study adheres to:

1. **Declaration of Helsinki** - Ethical principles for medical research
2. **GDPR** - EU General Data Protection Regulation
3. **Good Clinical Practice (GCP)** - ICH-GCP guidelines
4. **Research Integrity Guidelines** - Danish Code of Conduct for Research Integrity

---

## Study Design Considerations

### No Human Subjects Research

This study does NOT involve:
- Human participants
- Patient recruitment
- Clinical intervention
- Access to patient records
- Collection of biological samples
- Personal health information

### Data Sources

All data used in this study are:
- **Publicly available databases** (UniProt, Human Protein Atlas, PeptideAtlas, PhosphoSitePlus)
- **Synthetic proteomics data** generated for research purposes
- **LLM responses** to standardized queries (no patient data)
- **Published peer-reviewed literature**

---

## Data Privacy and Protection

### No Personal Data

This research does NOT process any personal data as defined by GDPR Article 4(1).

**Rationale**: All data sources are:
- Publicly available protein databases
- Synthetic data generated for testing
- Aggregated scientific literature
- LLM API responses to non-patient queries

### Data Classification

All data in this study are classified as:
- **Public** - Safe for unrestricted sharing
- **No PII** - No personally identifiable information
- **No PHI** - No protected health information
- **Research Use** - Academic and educational purposes

---

## Informed Consent

**Not Applicable** - This study does not involve human subjects research.

---

## Risk Assessment

### Risks to Participants

**None** - No human participants involved.

### Risks to Researchers

**Minimal** - Standard academic research risks only.

### Risks to Public

**Addressed** - Study findings will inform safe LLM deployment in healthcare:
- Identify hallucination risks
- Quantify error rates
- Provide clinical deployment guidelines
- Recommend safety protocols

---

## Benefits

### Scientific Benefits

- Establish baseline hallucination rates for LLMs in proteomics
- Identify risk factors for LLM errors
- Develop validation frameworks
- Inform regulatory guidelines

### Clinical Benefits

- Improve patient safety through evidence-based LLM deployment recommendations
- Prevent premature adoption of unreliable AI systems
- Guide development of safer clinical decision support tools

### Societal Benefits

- Transparent evaluation of AI capabilities and limitations
- Open access to data and code for reproducibility
- Educational resource for AI safety in healthcare

---

## Conflicts of Interest

### Declared Conflicts

**None**

The authors declare no financial or non-financial conflicts of interest.

**Specific Declarations**:
- No funding from LLM developers (OpenAI, Anthropic, Google)
- No equity or financial interest in LLM companies
- No consulting relationships with LLM developers
- No patents or intellectual property related to LLMs

---

## Funding

This research received no external funding.

**Resources**:
- Computational resources: DTU Computing Center
- API access: Personal research accounts (OpenAI, Anthropic, Google)
- Databases: Publicly available (UniProt, HPA, PeptideAtlas)

---

## Data Sharing

### Open Science Commitment

All research materials will be made publicly available:

**GitHub Repository**: https://github.com/olaflaitinen/llm-proteomics-hallucination
- Complete query dataset (500 queries)
- LLM responses (1,500 responses)
- Ground truth annotations
- Analysis code (Python)
- Figure generation scripts

**Zenodo Archive**: DOI 10.5281/zenodo.11234567
- Permanent preservation
- Citable DOI
- Long-term accessibility

### License

- **Code**: MIT License (permissive open source)
- **Data**: CC-BY 4.0 (Creative Commons Attribution)
- **Manuscript**: Copyright retained by authors (pre-print); journal rights (published version)

---

## Research Integrity

### Reproducibility

- Pre-registered study design (OSF)
- Open data and code
- Detailed methodology documentation
- Transparent reporting of results

### Statistical Rigor

- Pre-specified primary and secondary outcomes
- Appropriate statistical methods (chi-square, logistic regression)
- Multiple comparison corrections (Bonferroni)
- Effect size reporting

### Transparency

- All queries disclosed
- Complete LLM responses available
- Negative findings reported
- Limitations acknowledged

---

## Ethical Oversight

### Research Ethics Committee

**Committee**: Institutional Review Board
**Review Type**: Expedited review (no human subjects)
**Approval Duration**: October 28, 2025 - December 31, 2026
**Reporting**: Annual progress reports

### Amendments

Any protocol amendments will be:
1. Documented in writing
2. Submitted for ethics committee review
3. Implemented only after approval
4. Publicly disclosed in final publication

---

## Dissemination

### Publication Plan

**Target Journal**: The Lancet Digital Health
**Submission Date**: December 2025
**Open Access**: Yes (institutional funding or author-pays)

### Presentations

- International conferences (ISMB, HUPO, AMIA)
- University seminars
- Public science communication

### Data Release

- Simultaneous with publication
- Permanent archiving (Zenodo)
- GitHub repository maintenance

---

## Responsible AI Practices

### Transparency

- Full disclosure of LLM models, versions, and parameters
- Transparent reporting of error rates
- Clear communication of limitations

### Safety

- Evidence-based recommendations for clinical deployment
- Explicit warnings about current hallucination rates
- Call for regulatory oversight

### Fairness

- Objective evaluation across multiple LLM providers
- Standardized query dataset
- Independent expert validation

---

## Contact Information

### Principal Investigator

**Name**: Olaf Yunus Laitinen Imanov
**Affiliation**: Department of Biotechnology and Biomedicine, Technical University of Denmark
**Email**: olyulaim@dtu.dk
**Address**: Building 375, 2800 Kongens Lyngby, Denmark

### Ethics Questions

**DTU Research Ethics Committee**
**Email**: ethics@dtu.dk
**Website**: https://www.dtu.dk/english/research/responsible-conduct-of-research

---

## Compliance Monitoring

### Regular Reviews

- Quarterly progress reviews
- Annual ethics compliance reports
- Final study report upon completion

### Documentation

All ethics-related documentation maintained in:
- `/ethics/` directory (this repository)
- Institutional records (DTU)
- OSF pre-registration (osf.io/x7mk9)

---

## Amendments Log

### Version 1.0 (October 28, 2025)

- Initial ethics protocol approval
- Pre-registration completed

### Version 1.1 (December 15, 2025)

- Updated for final manuscript preparation
- No changes to approved protocol
- Documentation improvements only

---

**Last Updated**: December 15, 2025
**Protocol Version**: 1.1
**Status**: Active
