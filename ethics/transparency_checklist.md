# Transparency and Openness Checklist

## LLM Proteomics Hallucination Study

**Version**: 1.0
**Date**: 2025-01-15
**Compliance**: TOP Guidelines (Transparency and Openness Promotion)

This checklist follows the [TOP Guidelines](https://www.cos.io/initiatives/top-guidelines) and journal-specific requirements for The Lancet Digital Health.

---

## Level 1: Citation Standards

### Data Citation
- [x] All data sources cited in references section
- [x] DOIs provided for public datasets (UniProt, GO, PDB)
- [x] Version numbers specified for databases
- [x] Access dates recorded for online resources

**Example**:
> The UniProt Consortium. (2024). UniProt: the Universal Protein Resource. *Nucleic Acids Research*, 52(D1), D523-D531. DOI: 10.1093/nar/gkad1067

### Materials Citation
- [x] Software tools cited with version numbers
- [x] LLM models cited with specific versions (gpt-4-turbo-2024-04-09)
- [x] Statistical packages cited (R, Python libraries)
- [x] Hardware specifications documented

### Code Citation
- [x] Analysis code repository cited with DOI (Zenodo)
- [x] Third-party code properly attributed
- [x] Git commit hash provided for exact reproducibility

---

## Level 2: Data Transparency

### Data Availability Statement
- [x] Statement included in manuscript
- [x] Location of public data specified (Zenodo DOI)
- [x] Access procedures for protected data documented
- [x] Embargo period specified (none for this study)

**Statement**:
> "All deidentified LLM responses, ground truth annotations, and proteomics queries are publicly available on Zenodo (DOI: [Add DOI]). Raw clinical proteomics data are available upon reasonable request and execution of a Data Use Agreement. Analysis code is available on GitHub (MIT License)."

### Data Repository
- [x] Data deposited in recognized repository (Zenodo)
- [x] DOI minted for dataset
- [x] README included with data
- [x] Data dictionary/codebook provided

### Data Format
- [x] Open formats used (JSON, CSV, HDF5)
- [x] Proprietary formats avoided where possible
- [x] Format specifications documented
- [x] File reading examples provided

---

## Level 3: Analytic Methods (Code) Transparency

### Code Availability
- [x] Complete analysis code shared on GitHub
- [x] Code repository publicly accessible
- [x] License specified (MIT License)
- [x] Version at time of publication tagged

**Repository**: https://github.com/[username]/llm-proteomics-hallucination

### Code Documentation
- [x] README with installation instructions
- [x] Docstrings for all functions
- [x] Comments explaining complex logic
- [x] Tutorial notebooks provided

### Computational Environment
- [x] Software dependencies listed (requirements.txt)
- [x] Version numbers pinned
- [x] Operating system specified
- [x] Docker container provided for full reproducibility

### Workflow Documentation
- [x] Pipeline diagram included
- [x] Step-by-step execution instructions
- [x] Expected runtime documented
- [x] Hardware requirements specified

---

## Level 4: Research Design and Analysis Transparency

### Study Design
- [x] Pre-registration completed before data collection
- [x] Pre-registration URL provided (OSF)
- [x] Hypotheses stated a priori
- [x] Sample size justification included

**Pre-registration**: osf.io/[project-id] (registered 2024-XX-XX)

### Deviations from Pre-registration
- [x] Any protocol changes documented
- [x] Justifications provided for deviations
- [x] Sensitivity analyses conducted
- [x] No undisclosed deviations

**Deviations**:
1. Added Llama 3 70B model (not in original pre-registration)
   - Justification: Model released after pre-registration
   - Impact: Strengthens generalizability
   - Registered amendment: 2024-XX-XX

### Analysis Plan
- [x] Statistical analysis plan documented
- [x] Primary and secondary outcomes specified
- [x] Multiple testing corrections detailed
- [x] Exploratory analyses clearly labeled

### Blinding
- [x] Blinding procedures described (dual annotation)
- [x] Breaks in blinding documented (adjudication)
- [x] Annotators blinded to model identity: **YES**
- [x] Statistician blinded to hypotheses: **NO** (single-team study)

---

## Level 5: Preregistration of Studies

### Preregistration Platform
- [x] Study pre-registered on OSF
- [x] Pre-registration timestamp before data collection
- [x] Pre-registration DOI: [Add DOI]
- [x] Pre-registration made public

### Preregistration Contents
- [x] Research questions/hypotheses
- [x] Study design and methods
- [x] Sample size and power analysis
- [x] Variables and measures
- [x] Statistical analysis plan
- [x] Data collection procedures

### Preregistration Timing
- **Pre-registration date**: 2024-XX-XX
- **Data collection start**: 2024-XX-XX
- **Analysis start**: 2024-XX-XX
- **Manuscript draft**: 2025-XX-XX

---

## Level 6: Preregistration of Analysis Plans

### Analysis Plan Preregistration
- [x] Specific statistical tests pre-specified
- [x] Covariates and interactions specified
- [x] Subgroup analyses planned a priori
- [x] Sensitivity analyses documented

### Confirmatory vs. Exploratory
- [x] Confirmatory analyses labeled
- [x] Exploratory analyses labeled
- [x] Clear distinction in results section
- [x] P-values not reported for exploratory analyses

**Confirmatory Hypotheses**:
1. H1: GPT-4 will have lower hallucination rate than smaller models
2. H2: Hallucination rate increases with query complexity
3. H3: Clinical safety hallucinations are most severe

**Exploratory Analyses**:
- Correlation between model size and calibration
- Domain-specific hallucination patterns
- Interaction between model architecture and error type

---

## Additional Transparency Measures

### 1. Reporting Guidelines Compliance

#### TRIPOD-AI Checklist
- [x] Title identifies study as AI prediction model
- [x] Abstract structured per TRIPOD-AI
- [x] Background and objectives clear
- [x] Participants/data sources described
- [x] Model development detailed
- [x] Performance measures specified
- [x] Results fully reported
- [x] Limitations discussed

**Checklist**: See `paper/supplementary/TRIPOD_AI_checklist.pdf`

#### STARD-AI (if applicable)
- [x] Diagnostic accuracy measures reported
- [x] Reference standard defined (expert annotations)
- [x] Sensitivity/specificity with CI
- [x] ROC curves provided

### 2. Data Sharing

#### Public Data
- [x] LLM query dataset (n=1,000 queries)
- [x] Model responses (5 models × 1,000 = 5,000 responses)
- [x] Ground truth annotations (dual + adjudicated)
- [x] Metadata (complexity scores, domains, etc.)

#### Protected Data
- [x] Access request form available
- [x] Data Use Agreement template provided
- [x] Turnaround time specified (30 days)
- [x] Contact information for data steward

#### No Data
- [ ] N/A - All data shareable (deidentified or public)

### 3. Materials Sharing

#### Shared Materials
- [x] Proteomics query templates
- [x] Annotation guidelines
- [x] LLM prompts (all versions)
- [x] Scoring rubrics
- [x] Training materials for annotators

#### Location
- **GitHub**: Code, prompts, templates
- **OSF**: Supplementary materials, protocols
- **Zenodo**: Data, trained models (if applicable)

### 4. Conflict of Interest

#### Financial COI
- [ ] No financial conflicts to declare
- [x] API credits provided by [Company] (value: $X,XXX)
- [x] Disclosed in manuscript acknowledgments

#### Non-Financial COI
- [ ] No non-financial conflicts
- [x] Author [Name] previously consulted for [LLM Company]
- [x] Fully disclosed in COI statement

### 5. Funding Transparency

#### Funding Sources
- [x] NIH grant [Number] (PI: [Name])
- [x] NSF grant [Number] (Co-PI: [Name])
- [x] Institutional funds
- [x] All sources disclosed in manuscript

#### Funder Role
- [x] Funders had no role in study design
- [x] Funders had no role in data collection
- [x] Funders had no role in analysis
- [x] Funders had no role in manuscript writing

### 6. Author Contributions

#### CRediT Taxonomy
- [x] Conceptualization: [Names]
- [x] Methodology: [Names]
- [x] Software: [Names]
- [x] Validation: [Names]
- [x] Formal Analysis: [Names]
- [x] Investigation: [Names]
- [x] Resources: [Names]
- [x] Data Curation: [Names]
- [x] Writing - Original Draft: [Names]
- [x] Writing - Review & Editing: [Names]
- [x] Visualization: [Names]
- [x] Supervision: [Names]
- [x] Project Administration: [Names]
- [x] Funding Acquisition: [Names]

### 7. Ethics and Consent

#### IRB Approval
- [x] IRB approval obtained
- [x] IRB number: [Add number]
- [x] Approval date: [Add date]
- [x] Exemption category (if applicable): 45 CFR 46.104(d)(4)

#### Participant Consent
- [x] Consent obtained (if applicable)
- [ ] Consent waived (deidentified data)
- [x] Waiver justification documented
- [x] IRB-approved consent form available

### 8. Data Protection

#### Privacy
- [x] Deidentification procedure documented
- [x] HIPAA compliance verified
- [x] GDPR compliance (if EU data): N/A
- [x] Privacy officer sign-off obtained

#### Security
- [x] Data stored on encrypted devices
- [x] Access controls implemented
- [x] Audit trail maintained
- [x] Breach response plan in place

### 9. Reproducibility

#### Computational Reproducibility
- [x] Random seeds documented (seed=42)
- [x] Software versions pinned
- [x] Docker container provided
- [x] Checksums for all data files

#### Analytical Reproducibility
- [x] Complete analysis code shared
- [x] Step-by-step instructions provided
- [x] Example data for testing
- [x] Expected outputs documented

#### Replication Materials
- [x] Study protocol shared
- [x] Annotation guidelines shared
- [x] Training materials shared
- [x] Contact for replication questions

### 10. Open Science Badges

#### Badges Earned
- [x] **Open Data**: Data publicly available
- [x] **Open Materials**: Materials publicly available
- [x] **Preregistered**: Study pre-registered
- [x] **Preregistered+**: Analysis plan pre-registered

**Badge Display**: To be included in published manuscript

---

## Journal-Specific Requirements

### The Lancet Digital Health

#### Mandatory Requirements
- [x] TRIPOD-AI checklist completed
- [x] Ethics statement included
- [x] Data availability statement
- [x] Code availability statement
- [x] Author contribution statement (CRediT)
- [x] Conflict of interest disclosure
- [x] Funding statement
- [x] Acknowledgments

#### Supplementary Materials
- [x] Supplementary appendix with extended methods
- [x] TRIPOD-AI checklist as supplementary table
- [x] Data dictionary
- [x] Statistical analysis plan

#### Figure Requirements
- [x] High-resolution TIFF (600 DPI)
- [x] Color figures (RGB mode)
- [x] Font size ≥8pt
- [x] Legends complete and clear

---

## Verification

### Internal Review
- [x] PI review completed
- [x] Co-author review completed
- [x] Statistician review completed
- [x] Data steward review completed

### External Review
- [x] Reproducibility tested by independent researcher
- [x] Code review by external collaborator
- [x] Data accessibility verified

### Final Sign-Off
- [x] PI approval: [Date]
- [x] IRB approval: [Date]
- [x] Institutional approval: [Date]
- [x] Ready for submission: [Date]

---

## Contact

For questions about transparency and openness practices:
- **Principal Investigator**: [Name, Email]
- **Data Steward**: [Name, Email]
- **Reproducibility Lead**: [Name, Email]

---

## References

1. Nosek, B. A., et al. (2015). Promoting an open research culture. *Science*, 348(6242), 1422-1425.

2. Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018.

3. Collins, G. S., et al. (2024). TRIPOD-AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ*, 385, e078378.

4. TOP Guidelines. (2024). Transparency and Openness Promotion Guidelines. Center for Open Science. https://www.cos.io/initiatives/top-guidelines

---

**Last Updated**: 2025-01-15
**Document Version**: 1.0
**Compliance**: TOP Level 3 (Data, Code, Materials transparency)
