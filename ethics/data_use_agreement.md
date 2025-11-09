# Data Use Agreement

## LLM Proteomics Hallucination Evaluation Study

**Version**: 1.0
**Effective Date**: 2025-10-25
**Institution**: Technical University of Denmark
**Principal Investigator**: Olaf Yunus Laitinen Imanov

---

## 1. Purpose

This Data Use Agreement (DUA) governs the use of datasets for evaluating hallucinations in Large Language Model (LLM) responses to proteomics queries. This research aims to improve the safety and reliability of AI systems in clinical proteomics.

## 2. Data Sources

### 2.1 Proteomics Data
- **Mass Spectrometry Files**: LC-MS/MS data in MGF and mzML formats
- **Protein Databases**: Human, mouse, and yeast proteomes (UniProt)
- **Annotations**: Gene Ontology (GO) terms, disease associations

### 2.2 Clinical Data
- **Biomarker Information**: FDA-approved and experimental biomarkers
- **Disease Categories**: Cancer, cardiovascular, neurological, metabolic
- **Status**: All data fully deidentified per HIPAA Safe Harbor method

### 2.3 LLM Response Data
- **Models Evaluated**: GPT-4 Turbo, Claude 3 Sonnet, Gemini 1.5 Pro, Mistral Large 2, Llama 3 70B
- **Query-Response Pairs**: 1,000 proteomics queries with model responses
- **Annotations**: Expert hallucination severity ratings (0-3 scale)

## 3. Permitted Uses

### 3.1 Research Activities
Data may be used for:
- Evaluating LLM hallucination rates in proteomics domain
- Developing hallucination detection methods
- Statistical analysis of model performance
- Publication in peer-reviewed journals
- Presentation at scientific conferences
- Educational purposes (graduate/postgraduate training)

### 3.2 Prohibited Uses
Data may NOT be used for:
- Re-identification of participants
- Commercial product development without separate agreement
- Training proprietary LLM models without attribution
- Sharing with unauthorized third parties
- Clinical decision-making (research use only)

## 4. Data Protection Obligations

### 4.1 Security Measures
Data users must:
- Store data on encrypted devices or secure servers
- Use strong passwords and multi-factor authentication
- Limit access to authorized research personnel only
- Maintain access logs for audit purposes
- Report any data breaches within 24 hours

### 4.2 Deidentification
All clinical data has been deidentified:
- No direct identifiers (names, MRNs, dates)
- Dates shifted by random intervals
- Geographic locations generalized to state/country level
- Rare diseases/variants aggregated or excluded

### 4.3 Retention and Disposal
- **Retention Period**: 7 years post-publication (NIH policy)
- **Disposal Method**: Secure deletion (DoD 5220.22-M standard)
- **Archival**: Deidentified data deposited to Zenodo/OSF for reproducibility

## 5. Attribution and Citation

### 5.1 Required Citation
Publications using this data must cite:
```
[Author List]. (2025). Evaluating Hallucinations in Large Language Model
Responses to Proteomics Queries. The Lancet Digital Health.
DOI: [Add DOI when available]
```

### 5.2 Data Repository
Publicly released data available at:
- **Zenodo**: [Add DOI]
- **OSF**: [Add OSF project link]
- **GitHub**: https://github.com/[username]/llm-proteomics-hallucination

## 6. Compliance

### 6.1 Regulatory Compliance
This research complies with:
- **HIPAA Privacy Rule**: 45 CFR Part 164
- **Common Rule**: 45 CFR Part 46 (Human Subjects Protection)
- **NIH Data Management and Sharing Policy**
- **GDPR** (if applicable to EU participants)

### 6.2 Institutional Review Board
- **IRB Approval**: [Add IRB number]
- **Approval Date**: [Add date]
- **Expiration**: [Add expiration]
- **Modification History**: See `ethics/consent_and_irb/IRB_approval.pdf`

## 7. Third-Party Data Sharing

### 7.1 External Collaborators
Sharing with collaborators requires:
- Written approval from Principal Investigator
- Execution of separate DUA
- IRB approval if scope changes

### 7.2 Public Data Release
Subset of data released publicly:
- **Ground Truth Annotations**: Expert ratings (deidentified)
- **LLM Responses**: Model outputs to proteomics queries
- **Metadata**: Dataset statistics, model configurations
- **Exclusions**: No raw clinical data, no PHI

## 8. LLM API Data Usage

### 8.1 API Provider Policies
When using commercial LLM APIs:
- **OpenAI**: Data not used for model training (Enterprise API)
- **Anthropic**: Zero data retention policy selected
- **Google**: Data processed in compliance with HIPAA BAA
- **Mistral**: Data retention limited to 30 days

### 8.2 Local Model Deployment
For self-hosted models (Llama 3 70B):
- All data processed on institutional servers
- No external transmission of proteomics data
- Logs retained per institutional policy

## 9. Intellectual Property

### 9.1 Data Ownership
- **Proteomics Data**: Public domain (UniProt, GO) or institutional
- **LLM Responses**: Generated for research, no IP claims
- **Analysis Code**: MIT License (open source)
- **Derived Works**: Must acknowledge original data sources

### 9.2 Patent Rights
Researchers retain rights to inventions/discoveries made using this data, subject to institutional policies.

## 10. Liability and Warranty

### 10.1 Data Provided "As-Is"
Data provided without warranty of:
- Completeness
- Accuracy
- Fitness for particular purpose
- Non-infringement

### 10.2 Limitation of Liability
Data providers not liable for:
- Direct, indirect, or consequential damages
- Results obtained from data use
- Third-party claims

## 11. Termination

This DUA terminates:
- Upon completion of research project
- Upon written notice by either party
- Immediately upon data breach or violation

Upon termination:
- Destroy all data copies
- Provide written certification of destruction
- Return any physical media

## 12. Amendments

This DUA may be amended by:
- Written agreement of both parties
- IRB-mandated modifications
- Changes in regulatory requirements

## 13. Signatures

### Principal Investigator
**Name**: ___________________________
**Title**: ___________________________
**Date**: ___________________________
**Signature**: ___________________________

### Data User
**Name**: ___________________________
**Title**: ___________________________
**Institution**: ___________________________
**Date**: ___________________________
**Signature**: ___________________________

### Institutional Official
**Name**: ___________________________
**Title**: ___________________________
**Date**: ___________________________
**Signature**: ___________________________

---

## Contact Information

**For Questions About This DUA**:
- **Email**: [Add contact email]
- **Phone**: [Add phone]
- **Address**: [Add institutional address]

**For Data Breach Reporting**:
- **Security Office**: [Add security contact]
- **IRB Office**: [Add IRB contact]
- **PI Emergency Contact**: [Add emergency contact]

---

**Document Version**: 1.0
**Last Reviewed**: 2025-10-25
**Next Review**: 2026-10-25
