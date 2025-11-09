# GDPR Compliance Statement

**Study**: Hallucination Rates in Large Language Models for Clinical Proteomics Applications
**Date**: November 1, 2025
**Protocol**: IRB #2025-IRB-1101
**Data Controller**: Technical University of Denmark

---

## 1. Data Protection Impact Assessment

### 1.1 Nature of Data Processing

**Type of Processing**: Evaluation of publicly available protein database information
**Personal Data Involved**: None
**Special Category Data**: None (no patient-identifiable information)

### 1.2 Risk Assessment

**Risk Level**: Minimal
**Justification**:
- No collection of personal data from individuals
- No patient-level clinical data
- Only publicly available protein sequences and annotations from curated databases
- LLM API queries contain no personally identifiable information

### 1.3 GDPR Applicability

**Assessment**: GDPR does not apply to this study
**Rationale**:
- Article 2(1) GDPR: Regulation applies to processing of personal data
- Article 4(1) GDPR: Personal data means information relating to an identified or identifiable natural person
- **This study processes only protein sequence data and scientific literature, not personal data**

---

## 2. Data Minimization

### 2.1 Principle

**GDPR Article 5(1)(c)**: Personal data shall be adequate, relevant and limited to what is necessary

**Implementation**:
- No collection of data beyond protein sequences and functional annotations
- No demographic information
- No patient identifiers
- No clinical outcomes linked to individuals

### 2.2 Data Retention

**Storage Duration**: 10 years (scientific records retention policy)
**Justification**: Required for research reproducibility and verification
**Deletion Policy**: Automated deletion after retention period expires

---

## 3. Security Measures

### 3.1 Technical Safeguards

**Data Storage**:
- Encrypted at rest (AES-256)
- Encrypted in transit (TLS 1.3)
- Access control via SSH keys and role-based permissions

**Infrastructure**:
- DTU Computing Center secure servers
- ISO 27001 certified data center
- Regular security audits

**Backup**:
- Daily incremental backups
- Weekly full backups
- Encrypted backup storage
- 90-day retention

### 3.2 Organizational Safeguards

**Access Control**:
- Principle of least privilege
- Role-based access (PI, co-PI, annotators only)
- Authentication via institutional credentials
- Access logs maintained

**Personnel Training**:
- Data protection training for all personnel
- Confidentiality agreements signed
- Regular updates on security procedures

---

## 4. Third-Party Data Processors

### 4.1 LLM API Providers

**OpenAI (GPT-4 Turbo)**:
- Data Processing Agreement: In place
- Data Location: United States (Privacy Shield Framework successor)
- Data Retention: 30 days (API logs), then deleted
- Security: SOC 2 Type II certified

**Anthropic (Claude 3 Sonnet)**:
- Data Processing Agreement: In place
- Data Location: United States
- Data Retention: No retention (zero-retention policy for API requests)
- Security: SOC 2 Type II certified

**Google (Gemini Pro 1.5)**:
- Data Processing Agreement: Google Cloud terms
- Data Location: European Economic Area (EEA)
- Data Retention: 18 months (service improvement), user-controllable
- Security: ISO 27001, ISO 27017, ISO 27018 certified

### 4.2 Data Sharing Agreements

All third-party processors:
- Comply with GDPR Article 28 (Processor obligations)
- Provide adequate security measures
- Notify of data breaches within 72 hours
- Delete or return data upon request

---

## 5. Data Subject Rights

### 5.1 Applicability

**Assessment**: No data subjects in this study
**Justification**: Study uses publicly available protein databases, not personal data from individuals

### 5.2 Hypothetical Rights (if applicable)

If personal data were involved, the following rights would apply:

**Right to Access** (Article 15): Data subjects can request copy of their data
**Right to Rectification** (Article 16): Correction of inaccurate data
**Right to Erasure** (Article 17): "Right to be forgotten"
**Right to Restrict Processing** (Article 18): Limit how data is used
**Right to Data Portability** (Article 20): Receive data in machine-readable format
**Right to Object** (Article 21): Object to processing for specific purposes

---

## 6. Data Breach Notification

### 6.1 Breach Definition

**Personal Data Breach**: Accidental or unlawful destruction, loss, alteration, unauthorized disclosure of, or access to, personal data (Article 4(12))

### 6.2 Notification Procedures

**To Supervisory Authority** (Article 33):
- Within 72 hours of becoming aware of breach
- Notification to Danish Data Protection Agency (Datatilsynet)

**To Data Subjects** (Article 34):
- Without undue delay if high risk to rights and freedoms
- Direct communication to affected individuals

### 6.3 Breach Response Plan

**Detection**: Automated monitoring and logging
**Assessment**: Risk evaluation within 24 hours
**Containment**: Immediate isolation of affected systems
**Notification**: Follow Article 33/34 timelines
**Remediation**: Corrective actions to prevent recurrence
**Documentation**: Breach register maintained

**Current Status**: No breaches detected during study period (Nov 1 - Dec 15, 2025)

---

## 7. Cross-Border Data Transfers

### 7.1 Data Transfers Outside EEA

**LLM API Queries** (to United States):
- OpenAI API: United States-based processing
- Anthropic API: United States-based processing
- Gemini API: EEA-based processing (Google Cloud EU regions)

### 7.2 Adequacy and Safeguards

**Standard Contractual Clauses** (Article 46(2)(c)):
- In place with OpenAI and Anthropic
- Approved by European Commission (Decision 2021/914)

**Supplementary Measures**:
- Encryption in transit and at rest
- Pseudonymization (though no personal data involved)
- Access controls and logging

**Assessment**: Adequate level of protection ensured

---

## 8. Privacy by Design and Default

### 8.1 Privacy by Design (Article 25(1))

**Implementation**:
- No collection of personal data (design decision)
- Minimal data processing
- Automated deletion after retention period
- Security measures from inception

### 8.2 Privacy by Default (Article 25(2))

**Implementation**:
- Default access: Denied (explicit grant required)
- Default retention: Minimum necessary
- Default sharing: None (explicit approval required)

---

## 9. Accountability

### 9.1 Documentation

**Records of Processing Activities** (Article 30):
- Maintained in `ethics/data_privacy/processing_record.md`
- Includes purposes, categories, recipients, retention, security

**Data Protection Impact Assessment** (Article 35):
- Completed October 20, 2025
- Available in `ethics/data_privacy/dpia.md`

### 9.2 Data Protection Officer (DPO)

**DPO**: Technical University of Denmark DPO
**Contact**: dpo@dtu.dk
**Responsibilities**:
- Monitor GDPR compliance
- Advise on data protection
- Cooperate with supervisory authority

---

## 10. Supervisory Authority

### 10.1 Danish Data Protection Agency

**Name**: Datatilsynet
**Address**: Carl Jacobsens Vej 35, 2500 Valby, Denmark
**Email**: dt@datatilsynet.dk
**Phone**: +45 33 19 32 00
**Website**: https://www.datatilsynet.dk

### 10.2 Lodging Complaints

Data subjects have the right to lodge a complaint with Datatilsynet if they believe their rights have been infringed (Article 77)

---

## 11. Compliance Checklist

- [x] **Article 5**: Principles of processing (lawfulness, fairness, transparency)
- [x] **Article 6**: Lawful basis for processing (scientific research, legitimate interest)
- [x] **Article 13/14**: Information to be provided (not applicable - no data subjects)
- [x] **Article 15-22**: Data subject rights (not applicable - no personal data)
- [x] **Article 24**: Responsibility of controller (accountability demonstrated)
- [x] **Article 25**: Data protection by design and default (implemented)
- [x] **Article 28**: Processor agreements (in place with LLM providers)
- [x] **Article 30**: Records of processing activities (maintained)
- [x] **Article 32**: Security of processing (encryption, access control, logging)
- [x] **Article 33/34**: Breach notification procedures (established)
- [x] **Article 35**: Data protection impact assessment (completed)
- [x] **Article 44-50**: International transfers (SCCs in place)

---

## 12. Review and Updates

**Last Review**: November 1, 2025
**Next Review**: Annually or upon material changes
**Responsible**: Principal Investigator (Olaf Yunus Laitinen Imanov)

**Change Log**:
| Date | Version | Changes | Reviewer |
|------|---------|---------|----------|
| 2025-10-20 | 1.0 | Initial GDPR assessment | OYL Imanov |
| 2025-11-01 | 1.1 | Updated for study commencement | OYL Imanov |

---

## 13. Contact for Privacy Matters

**Data Controller**:
Technical University of Denmark
Department of Biotechnology and Biomedicine
Building 375, 2800 Kongens Lyngby, Denmark

**Principal Investigator**:
Olaf Yunus Laitinen Imanov
Email: olyulaim@dtu.dk

**DTU Data Protection Officer**:
Email: dpo@dtu.dk
Phone: +45 4525 2525

---

**Conclusion**: This study is GDPR-compliant. No personal data is processed. All data protection principles are upheld through technical and organizational measures.

**Certification**: Compliance verified by DTU Data Protection Officer (October 28, 2025)
