# HIPAA Compliance Statement

**Study**: Hallucination Rates in Large Language Models for Clinical Proteomics Applications
**Date**: November 1, 2025
**Protocol**: IRB #2025-IRB-1101

---

## Executive Summary

**HIPAA Applicability**: Not applicable to this study
**Justification**: Study uses publicly available protein database information with no Protected Health Information (PHI)

---

## 1. HIPAA Overview

### 1.1 What is HIPAA?

**Health Insurance Portability and Accountability Act (HIPAA)**:
- U.S. federal law enacted in 1996
- Establishes national standards for protection of health information
- Applies to "covered entities" and "business associates"

### 1.2 Protected Health Information (PHI)

**Definition** (45 CFR 160.103):
Individually identifiable health information transmitted or maintained in any form or medium by a covered entity or business associate

**18 HIPAA Identifiers**:
1. Names
2. Geographic subdivisions smaller than state
3. Dates (birth, admission, discharge, death)
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers
13. Device identifiers/serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers (fingerprints, voiceprints)
17. Full-face photographs
18. Any other unique identifying number, characteristic, or code

---

## 2. Applicability Assessment

### 2.1 Is This Study Subject to HIPAA?

**Assessment**: No

**Rationale**:

**Covered Entity Status**:
- **Question**: Is the research organization a covered entity (healthcare provider, health plan, or healthcare clearinghouse)?
- **Answer**: No. Technical University of Denmark is an academic research institution, not a U.S. covered entity.

**Protected Health Information**:
- **Question**: Does the study use, create, or disclose PHI?
- **Answer**: No. Study uses only publicly available protein sequence data from curated databases (UniProt, Human Protein Atlas, PeptideAtlas, PhosphoSitePlus).

**Human Subjects**:
- **Question**: Does the study involve identifiable human subjects?
- **Answer**: No. Study evaluates LLM responses to proteomics queries; no patient recruitment or clinical data collection.

### 2.2 Data Sources

**All Data Sources are De-identified or Public**:

1. **UniProt** (www.uniprot.org): Publicly available protein sequences
2. **Human Protein Atlas** (www.proteinatlas.org): Public tissue expression data
3. **PeptideAtlas** (www.peptideatlas.org): Public MS/MS spectra
4. **PhosphoSitePlus** (www.phosphosite.org): Public PTM database
5. **Scientific Literature**: Peer-reviewed publications (PubMed)

**No clinical records, patient charts, or individually identifiable health data are used.**

---

## 3. De-identification Standards

### 3.1 HIPAA Safe Harbor Method

**45 CFR 164.514(b)(2)**: De-identification by removal of 18 identifiers

**Our Approach**:
- **Not applicable**: Study does not begin with identifiable data
- All protein data are non-identifiable by nature
- No re-identification risk

### 3.2 Expert Determination Method

**45 CFR 164.514(b)(1)**: De-identification by expert statistical analysis

**Not applicable**: Study uses intrinsically non-identifiable protein sequences

---

## 4. Data Security (HIPAA-Equivalent Measures)

Although HIPAA does not apply, we implement equivalent security measures:

### 4.1 Administrative Safeguards (164.308)

**Security Management Process**:
- Risk assessment conducted (October 20, 2025)
- Risk management plan implemented
- Security incident procedures established
- Regular security evaluations

**Workforce Security**:
- Access authorization procedures
- Role-based access control
- Termination procedures (access revocation)

**Information Access Management**:
- Unique user identification
- Automatic logoff after 15 minutes inactivity
- Encryption of data at rest and in transit

**Security Awareness and Training**:
- All personnel trained on data security
- Annual refresher training
- Incident response drills

### 4.2 Physical Safeguards (164.310)

**Facility Access Controls**:
- DTU Computing Center: Restricted access, badge-controlled entry
- 24/7 video surveillance
- Access logs maintained

**Workstation Security**:
- Full-disk encryption (FileVault/BitLocker)
- Screen lock after 5 minutes
- No data on personal devices

**Device and Media Controls**:
- Secure disposal of storage media (shredding, degaussing)
- Encrypted backups
- Chain of custody for physical media

### 4.3 Technical Safeguards (164.312)

**Access Control**:
- Unique user IDs for all personnel
- Emergency access procedure (break-glass accounts)
- Automatic logoff after 15 minutes
- Encryption and decryption (AES-256)

**Audit Controls**:
- All access logged (who, what, when, where)
- Logs retained for 10 years
- Quarterly log reviews

**Integrity Controls**:
- SHA-256 checksums for all data files
- File modification monitoring
- Version control (Git)

**Transmission Security**:
- TLS 1.3 for all network transmission
- VPN required for remote access
- No unencrypted email transmission

---

## 5. Hypothetical HIPAA Compliance (If Applicable)

If this study involved PHI, the following would be required:

### 5.1 Privacy Rule Compliance

**Authorization** (45 CFR 164.508):
- Written authorization from individuals
- Specific description of information to be used
- Right to revoke authorization

**Minimum Necessary** (45 CFR 164.502):
- Use/disclose only minimum necessary PHI
- Periodic review of policies

**Notice of Privacy Practices** (45 CFR 164.520):
- Provide notice to individuals
- Describe uses and disclosures
- Individual rights outlined

### 5.2 Security Rule Compliance

**Risk Analysis** (45 CFR 164.308(a)(1)(ii)(A)):
- Assess threats and vulnerabilities
- Document security measures
- Annual review and updates

**Business Associate Agreements** (45 CFR 164.308(b)):
- Written agreements with LLM providers
- HIPAA obligations flow down
- Breach notification requirements

### 5.3 Breach Notification Rule

**45 CFR 164.400-414**: Notification requirements for PHI breaches

**Notification to Individuals**:
- Within 60 days of discovery
- Description of breach
- Steps to protect from harm

**Notification to HHS**:
- Within 60 days (if <500 individuals affected)
- Immediately (if ≥500 individuals affected)

**Media Notification**:
- If breach affects ≥500 individuals in a jurisdiction

---

## 6. International Considerations

### 6.1 HIPAA Jurisdiction

**Geographic Scope**: HIPAA applies to U.S. covered entities and business associates

**This Study**:
- Conducted in Denmark (European Economic Area)
- Not subject to HIPAA jurisdiction
- Subject to GDPR instead (see `gdpr_compliance.md`)

### 6.2 Equivalent International Standards

**GDPR** (EU General Data Protection Regulation):
- More stringent than HIPAA in many respects
- Applies to this study (see separate compliance document)

**Danish Data Protection Act**:
- Implements GDPR in Denmark
- Additional national requirements

---

## 7. Comparison: HIPAA vs. GDPR

| Aspect | HIPAA | GDPR | This Study |
|--------|-------|------|------------|
| **Scope** | Health information (U.S.) | All personal data (EEA) | N/A (no personal data) |
| **Geographic** | United States | European Economic Area | Denmark (GDPR applies) |
| **Penalties** | Up to $1.5M per year | Up to €20M or 4% revenue | N/A |
| **Consent** | Authorization for research | Explicit consent required | Not required (no personal data) |
| **Right to Access** | Yes (within 30 days) | Yes (within 1 month) | N/A |
| **Right to Erasure** | No (research exception) | Yes ("right to be forgotten") | N/A |
| **Breach Notification** | 60 days | 72 hours | Procedures established |
| **Data Minimization** | Minimum necessary | Principle of data minimization | Implemented |

---

## 8. Best Practices (HIPAA-Inspired)

Although not required, we follow HIPAA-equivalent best practices:

### 8.1 Privacy Practices

- **Minimum necessary**: Use only data needed for research objectives
- **Purpose limitation**: Data used only for stated research purpose
- **Access controls**: Role-based permissions
- **Audit trails**: All access logged and reviewed

### 8.2 Security Practices

- **Encryption**: Data encrypted at rest (AES-256) and in transit (TLS 1.3)
- **Authentication**: Multi-factor authentication for sensitive systems
- **Logging**: Comprehensive audit logs retained 10 years
- **Incident response**: Documented procedures for security incidents

### 8.3 Training Practices

- **Annual training**: All personnel complete data protection training
- **Incident reporting**: Clear procedures for reporting security concerns
- **Sanctions**: Policy violations subject to disciplinary action

---

## 9. Documentation and Accountability

### 9.1 Policies and Procedures

**Security Policies**:
- Access control policy
- Encryption policy
- Incident response plan
- Backup and recovery procedures

**Privacy Policies**:
- Data collection and use policy
- Data retention and disposal policy
- Third-party sharing policy

### 9.2 Training Records

- All personnel training documented
- Certifications retained
- Annual refresher completion tracked

### 9.3 Audit Logs

- System access logs: 10 years retention
- Data modification logs: 10 years retention
- Security incident logs: Permanent retention

---

## 10. Third-Party Compliance

### 10.1 LLM API Providers

Although not required, we verified HIPAA-equivalent compliance:

**OpenAI**:
- SOC 2 Type II certified
- HIPAA-compliant (for healthcare customers)
- Business Associate Agreement available

**Anthropic**:
- SOC 2 Type II certified
- HIPAA-compliant options available
- Security whitepaper published

**Google Cloud (Gemini)**:
- HIPAA-compliant infrastructure
- BAA available
- ISO 27001, 27017, 27018 certified

**Note**: HIPAA compliance not required for this study as no PHI is transmitted

---

## 11. Contact Information

**For Privacy/Security Questions**:

**Principal Investigator**:
Olaf Yunus Laitinen Imanov
Department of Biotechnology and Biomedicine
Technical University of Denmark
Email: olyulaim@dtu.dk

**DTU Data Protection Officer**:
Email: dpo@dtu.dk
Phone: +45 4525 2525

**U.S. HHS Office for Civil Rights** (for HIPAA guidance):
Website: https://www.hhs.gov/hipaa
Email: OCRMail@hhs.gov
Hotline: 1-800-368-1019

---

## 12. Conclusion

**HIPAA Status**: Not applicable to this study

**Rationale**:
1. Study does not involve a U.S. covered entity
2. No Protected Health Information (PHI) is collected, used, or disclosed
3. Study uses only publicly available protein sequences and literature

**Compliance Posture**:
- HIPAA-equivalent security measures implemented
- GDPR compliance ensures higher privacy standards
- Best practices exceed what would be required under HIPAA

**Certification**: Non-applicability confirmed by DTU Research Ethics Committee (October 28, 2025)

---

**Document Version**: 1.0
**Last Updated**: November 1, 2025
**Next Review**: Annually
