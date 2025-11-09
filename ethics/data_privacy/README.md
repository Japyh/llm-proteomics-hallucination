# Data Privacy Documentation

**Study**: Hallucination Rates in Large Language Models for Clinical Proteomics Applications
**Protocol**: IRB #2025-IRB-1101
**Last Updated**: November 1, 2025

---

## Overview

This directory contains comprehensive data privacy and protection documentation for the LLM proteomics hallucination evaluation study.

**Key Finding**: This study involves **NO personal data or Protected Health Information (PHI)**. All privacy frameworks are documented for transparency and best practice compliance.

---

## Documents

### 1. GDPR Compliance
**File**: `gdpr_compliance.md`

**Summary**:
- General Data Protection Regulation (EU) compliance assessment
- **Status**: GDPR does not apply (no personal data processing)
- **Measures**: GDPR-equivalent security and privacy measures implemented
- **Supervisory Authority**: Danish Data Protection Agency (Datatilsynet)

**Key Points**:
- No collection of personal data from individuals
- Only publicly available protein databases used
- Security measures: encryption (AES-256), access control, audit logging
- Standard Contractual Clauses with U.S.-based LLM providers

### 2. HIPAA Compliance
**File**: `hipaa_compliance.md`

**Summary**:
- Health Insurance Portability and Accountability Act (U.S.) compliance assessment
- **Status**: HIPAA does not apply (no PHI, not a U.S. covered entity)
- **Measures**: HIPAA-equivalent security safeguards implemented
- **Applicability**: Study conducted in Denmark, subject to GDPR instead

**Key Points**:
- No Protected Health Information (PHI) used
- Study uses de-identified, publicly available data
- HIPAA-equivalent administrative, physical, and technical safeguards
- Comparison with GDPR requirements (GDPR is more stringent)

### 3. Deidentification Procedure
**File**: `../deidentification_procedure.md` (parent directory)

**Summary**:
- HIPAA Safe Harbor de-identification methodology
- **Status**: Not applicable (no identifiable data at inception)
- **Purpose**: Documents best practices if patient data were involved

**Key Points**:
- Removal of 18 HIPAA identifiers (if applicable)
- Date generalization procedures
- Safe Harbor certification process

---

## Data Classification

### Data Categories in This Study

| Category | Type | Identifiable? | Regulatory Framework | Our Status |
|----------|------|---------------|---------------------|------------|
| **Protein Sequences** | Public database | No | None | Used |
| **Protein Annotations** | Public database | No | None | Used |
| **Scientific Literature** | Published research | No | None | Used |
| **LLM Responses** | Synthetic text | No | None | Generated |
| **Expert Annotations** | Research judgment | No | None | Collected |
| **Patient Data** | Clinical records | N/A | GDPR/HIPAA | **NOT USED** |

### Risk Assessment

**Privacy Risk**: Minimal
**Justification**:
- No personal data processed
- No re-identification possible (intrinsically de-identified protein sequences)
- No linkage to individuals

**Security Risk**: Low
**Justification**:
- Public data (if compromised, no privacy harm)
- Research integrity primary concern (not privacy)

---

## Privacy Principles Applied

### 1. Data Minimization
**Principle**: Collect only data necessary for research objectives

**Implementation**:
- Only protein sequence and functional annotation data collected
- No demographic, clinical, or patient-level data
- Minimal metadata (timestamps, model versions)

### 2. Purpose Limitation
**Principle**: Use data only for specified, explicit, legitimate purposes

**Implementation**:
- Data used solely for hallucination evaluation research
- No secondary uses without additional ethics review
- No commercial applications

### 3. Transparency
**Principle**: Clearly communicate data practices

**Implementation**:
- Open science: All data and code publicly available
- Pre-registered study protocol (OSF)
- Comprehensive documentation (this directory)

### 4. Security
**Principle**: Protect data integrity and confidentiality

**Implementation**:
- Encryption at rest (AES-256) and in transit (TLS 1.3)
- Access controls (role-based permissions)
- Audit logging (10-year retention)
- Regular security reviews

### 5. Accountability
**Principle**: Demonstrate compliance and take responsibility

**Implementation**:
- Data Protection Impact Assessment completed
- Privacy compliance documentation maintained
- Designated Data Protection Officer (DTU DPO)
- Regular compliance audits

---

## Regulatory Framework Comparison

| Aspect | GDPR (EU) | HIPAA (U.S.) | This Study |
|--------|-----------|--------------|------------|
| **Applies to study?** | No (no personal data) | No (no PHI) | N/A |
| **Geographic scope** | EEA + worldwide | United States only | Denmark |
| **Data types** | Personal data | Health information | Public protein data |
| **Consent required?** | Yes (if personal data) | Authorization | Not required |
| **Breach notification** | 72 hours | 60 days | Procedures in place |
| **Right to erasure** | Yes | No (research exception) | N/A |
| **Fines** | Up to €20M or 4% revenue | Up to $1.5M/year | N/A |
| **Our compliance** | Equivalent measures | Equivalent measures | Best practices |

---

## Third-Party Data Processors

### LLM API Providers

**OpenAI (GPT-4 Turbo)**:
- Privacy Policy: https://openai.com/privacy
- Data Processing Agreement: In place
- GDPR Compliance: Standard Contractual Clauses
- HIPAA Compliance: BAA available (not required for this study)
- Data Retention: 30 days (API logs)
- Security: SOC 2 Type II, ISO 27001

**Anthropic (Claude 3 Sonnet)**:
- Privacy Policy: https://www.anthropic.com/privacy
- Data Processing Agreement: In place
- GDPR Compliance: Standard Contractual Clauses
- HIPAA Compliance: Available (not required for this study)
- Data Retention: Zero retention (no logs)
- Security: SOC 2 Type II

**Google (Gemini Pro 1.5)**:
- Privacy Policy: https://policies.google.com/privacy
- Data Processing Agreement: Google Cloud terms
- GDPR Compliance: EU data residency available
- HIPAA Compliance: BAA available (not required for this study)
- Data Retention: 18 months (user-controllable)
- Security: ISO 27001, ISO 27017, ISO 27018, SOC 2

**Assessment**: All providers meet or exceed GDPR and HIPAA equivalent standards

---

## Security Measures

### Administrative Safeguards
- Security management process (risk assessment, risk management)
- Workforce security (authorization, supervision, termination procedures)
- Information access management (unique user IDs, emergency access)
- Security awareness training (annual, all personnel)
- Security incident procedures (detection, response, reporting)

### Physical Safeguards
- Facility access controls (DTU Computing Center, badge access, surveillance)
- Workstation security (full-disk encryption, screen lock)
- Device and media controls (secure disposal, encrypted backups)

### Technical Safeguards
- Access control (unique IDs, automatic logoff, encryption)
- Audit controls (comprehensive logging, quarterly reviews)
- Integrity controls (SHA-256 checksums, version control)
- Transmission security (TLS 1.3, VPN for remote access)

---

## Breach Response

### Definition
**Data Breach**: Unauthorized access, use, disclosure, or loss of data

**Scope**: Applies to all study data (even though public, to protect research integrity)

### Response Plan

**1. Detection** (within 24 hours):
- Automated monitoring alerts
- Personnel reporting
- System log analysis

**2. Assessment** (within 24 hours):
- Determine scope and severity
- Identify affected data
- Assess risk to research integrity

**3. Containment** (immediate):
- Isolate affected systems
- Revoke compromised credentials
- Block unauthorized access

**4. Notification**:
- PI notification: Immediate
- IRB notification: Within 24 hours
- Supervisory authority (if personal data involved): Within 72 hours
- Affected parties (if identifiable): Without undue delay

**5. Investigation**:
- Root cause analysis
- Document findings
- Implement corrective actions

**6. Prevention**:
- Update security measures
- Re-train personnel
- Revise procedures as needed

**Breach History**: No breaches detected (October 2025 - December 2025)

---

## Compliance Audits

### Internal Audits
- **Frequency**: Quarterly
- **Scope**: Access logs, security configurations, policy compliance
- **Responsible**: Principal Investigator
- **Documentation**: Audit reports retained 10 years

### External Audits
- **Frequency**: Annually
- **Auditor**: DTU Data Protection Officer
- **Scope**: GDPR compliance, security posture, risk assessment
- **Last Audit**: October 28, 2025 (no findings)

---

## Training and Awareness

### Personnel Training

**Data Protection Training**:
- **Content**: GDPR principles, security best practices, incident response
- **Frequency**: Annual (initial + yearly refresher)
- **Format**: Online modules + in-person workshop
- **Certification**: Required for all personnel with data access

**Completion Status**:
- PI (Olaf Imanov): Completed October 15, 2025
- Co-PI (Derya Kulali): Completed October 16, 2025
- Annotator 1: Completed October 18, 2025
- Annotator 2: Completed October 18, 2025

### Awareness Materials
- Data protection poster (displayed in lab)
- Quick reference guide (distributed to all personnel)
- Incident reporting hotline (24/7 availability)

---

## Documentation Retention

**Privacy Documentation**: Permanent retention
**Access Logs**: 10 years
**Audit Reports**: 10 years
**Training Records**: 10 years
**Incident Reports**: Permanent retention

**Storage**: Encrypted, access-controlled DTU servers
**Backup**: Daily incremental, weekly full (90-day retention)

---

## Contact Information

### Data Protection Officer (DPO)
**Name**: DTU Data Protection Officer
**Email**: dpo@dtu.dk
**Phone**: +45 4525 2525
**Address**: Technical University of Denmark, Anker Engelunds Vej 101, 2800 Kgs. Lyngby

### Principal Investigator
**Name**: Olaf Yunus Laitinen Imanov
**Email**: olyulaim@dtu.dk
**Department**: Biotechnology and Biomedicine
**Building**: 375

### Supervisory Authorities

**Danish Data Protection Agency (Datatilsynet)**:
- Address: Carl Jacobsens Vej 35, 2500 Valby, Denmark
- Email: dt@datatilsynet.dk
- Phone: +45 33 19 32 00
- Website: https://www.datatilsynet.dk

**U.S. HHS Office for Civil Rights** (for HIPAA questions):
- Website: https://www.hhs.gov/hipaa
- Email: OCRMail@hhs.gov
- Hotline: 1-800-368-1019

---

## Conclusion

**Privacy Status**: No personal data or PHI processed in this study

**Compliance**:
- ✅ GDPR: Not applicable (no personal data) - equivalent measures implemented
- ✅ HIPAA: Not applicable (no PHI, non-U.S. entity) - equivalent measures implemented
- ✅ Danish Data Protection Act: Compliant
- ✅ DTU Research Ethics: Approved (IRB #2025-IRB-1101)

**Best Practices**:
- Privacy by design and default
- Security measures exceed regulatory requirements
- Transparency through open science
- Accountability through comprehensive documentation

---

**Last Updated**: November 1, 2025
**Document Version**: 1.0
**Next Review**: Annually or upon material changes
