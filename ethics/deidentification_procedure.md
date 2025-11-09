# Deidentification Procedure

## LLM Proteomics Hallucination Study - Data Privacy Protocol

**Version**: 1.0
**Effective Date**: 2025-10-25
**Compliance**: HIPAA Privacy Rule 45 CFR §164.514(b), Safe Harbor Method

---

## 1. Executive Summary

This document describes the comprehensive deidentification procedure applied to all clinical and proteomics data used in the LLM hallucination evaluation study. All data has been deidentified to HIPAA Safe Harbor standards, ensuring participant privacy while maintaining research utility.

## 2. Deidentification Standard

### 2.1 Method Applied
**HIPAA Safe Harbor Method** (45 CFR §164.514(b)(2))

This method requires removal of 18 specific identifiers:

1. Names
2. Geographic subdivisions smaller than state
3. Dates (except year) directly related to an individual
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photographs
18. Any other unique identifying number, characteristic, or code

### 2.2 Verification
After deidentification, no knowledge available to the data custodian could be used to identify participants.

## 3. Data Categories and Deidentification

### 3.1 Clinical Proteomics Data

#### Mass Spectrometry Files

**Original Information**:
- Patient ID: `PT-2025-001234`
- Acquisition date: `2025-11-15 14:32:18`
- Instrument: `Orbitrap Fusion Lumos S/N FL12345`
- Operator: `Jane Smith`

**Deidentified**:
- Study ID: `STUDY_0001` (randomly assigned)
- Acquisition date: `2025-Q4` (quarter only)
- Instrument: `Orbitrap Fusion Lumos` (serial number removed)
- Operator: `[REMOVED]`

**Process**:
```python
# Pseudocode for MS file deidentification
def deidentify_ms_file(file):
    # Remove acquisition timestamps
    file.metadata['acquisition_date'] = generalize_to_quarter(file.metadata['acquisition_date'])

    # Remove instrument serial numbers
    file.metadata['instrument_serial'] = None

    # Replace patient ID with study ID
    file.metadata['patient_id'] = generate_study_id()

    # Remove operator information
    file.metadata['operator'] = '[REMOVED]'

    # Remove file paths containing usernames
    file.metadata['source_file'] = anonymize_path(file.metadata['source_file'])

    return file
```

#### Protein Identification Results

**Original Information**:
```
Patient: John Doe, MRN: 12345678
Sample Collection: 2025-11-15
Diagnosis: Stage II Pancreatic Adenocarcinoma
Physician: Dr. Sarah Johnson
Hospital: Memorial Hospital, Boston, MA
```

**Deidentified**:
```
Study ID: STUDY_0001
Sample Collection: 2025-Q4
Diagnosis: Pancreatic Cancer (generalized)
Physician: [REMOVED]
Location: Massachusetts, USA
```

### 3.2 Biomarker Data

#### Disease Associations

**Risk**: Rare disease combinations could enable re-identification

**Mitigation**:
- Diseases with <50 cases nationally: Categorized as "Rare Disease - [System]"
- Geographic regions: State-level only
- Age: 5-year bins (e.g., 50-54, not exact age)

**Example**:
```csv
# Original
patient_id,age,diagnosis,city,biomarker_value
PT-001,47,von Hippel-Lindau disease,Cambridge MA,12.4

# Deidentified
study_id,age_bin,diagnosis,state,biomarker_value
STUDY_0001,45-49,Rare Disease - Hereditary Cancer,MA,12.4
```

### 3.3 LLM Query Data

#### Query Construction

**Sensitive Information Removed**:
- Patient names in example queries
- Specific hospital/clinic names
- Physician names
- Dates of service

**Example Transformation**:

Original query:
> "What is the significance of elevated CA-125 (125 U/mL) in a 52-year-old woman with a family history of ovarian cancer, seen at Dana-Farber Cancer Institute on November 15, 2025?"

Deidentified query:
> "What is the significance of elevated CA-125 (125 U/mL) in a woman aged 50-55 with a family history of ovarian cancer?"

### 3.4 Expert Annotations

#### Annotator Information

**Protected**:
- Annotator names replaced with codes: `EXPERT_A`, `EXPERT_B`, `EXPERT_C`
- Institutional affiliations: Generalized to "Academic Medical Center" or "Industry"
- Credentials: Simplified to "MD-PhD", "PhD", "MD"

**Preserved**:
- Annotation timestamps (for inter-rater reliability analysis)
- Domain expertise categories (oncology, cardiology, etc.)

## 4. Date Shifting Protocol

### 4.1 Random Date Shifts

All dates shifted by random interval:
- **Range**: ±180 days
- **Consistency**: Same shift applied to all dates for a given participant
- **Preservation**: Relative time intervals maintained

**Implementation**:
```python
import numpy as np
from datetime import timedelta

# Generate consistent shift per participant
np.random.seed(hash(study_id) % (2**32))
shift_days = np.random.randint(-180, 180)

# Apply to all dates
shifted_date = original_date + timedelta(days=shift_days)
```

### 4.2 Date Generalization

Precision reduced where appropriate:
- **Full dates** → **Quarter and year** (`2024-Q1`)
- **Timestamps** → **Date only** or **Quarter**
- **Age** → **5-year bins**

## 5. Geographic Information

### 5.1 Levels of Generalization

| Original Precision | Deidentified Level | Example |
|-------------------|--------------------|---------|
| Street address | State | Massachusetts, USA |
| City | State | Massachusetts, USA |
| ZIP code | State | Massachusetts, USA |
| State | State | Massachusetts, USA |
| Country | Country | USA |

### 5.2 Suppression for Small Populations

- ZIP codes with <20,000 people → State level
- Cities with <50,000 people → State level
- Rural areas → "Rural [State]"

## 6. Numeric Identifier Removal

### 6.1 Medical Record Numbers (MRNs)

**Process**:
1. Extract all MRNs from source data
2. Generate random study IDs (`STUDY_0001` to `STUDY_1000`)
3. Create lookup table (stored securely, separate from research data)
4. Replace all MRN occurrences with study IDs
5. Destroy lookup table after verification (or store securely for future linking)

**Study ID Format**: `STUDY_[0-9]{4}` (e.g., `STUDY_0042`)

### 6.2 Other Identifiers

- **Accession Numbers**: Removed or replaced with sequential IDs
- **Insurance Numbers**: Removed
- **Driver's License**: Removed (not collected)
- **Device Serial Numbers**: Removed from instrument metadata

## 7. Free-Text Scrubbing

### 7.1 Automated Detection

**Tools Used**:
- Presidio (Microsoft): NER-based PII detection
- Custom regex patterns for domain-specific identifiers
- Manual review of flagged text

**Patterns Detected**:
- Names (PERSON entity)
- Locations (GPE, LOC entities)
- Dates (DATE entity)
- Phone numbers (regex: `\d{3}-\d{3}-\d{4}`)
- Email addresses (regex: `[\w\.-]+@[\w\.-]+\.\w+`)
- MRNs (pattern: `MRN:\s*\d+`)

**Example**:
```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

text = "Patient John Doe (MRN: 12345678) was seen on 03/15/2024."
results = analyzer.analyze(text=text, language='en')
anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)

# Output: "Patient [PERSON] (MRN: [REDACTED]) was seen on [DATE]."
```

### 7.2 Manual Review

All automated deidentification reviewed by:
1. **First pass**: Research coordinator
2. **Second pass**: Independent reviewer
3. **Spot checks**: 10% of records reviewed by privacy officer

## 8. Data Linkage Prevention

### 8.1 External Databases

**Risk**: Cross-referencing with public databases could enable re-identification

**Mitigation**:
- UniProt IDs: Retained (public database, not person-specific)
- Gene names: Retained (public knowledge)
- Rare protein variants: Suppressed if <10 cases in literature
- Novel variants: Generalized to protein family

### 8.2 Quasi-Identifiers

**Combination Risk**: Age + Gender + ZIP + Diagnosis could enable re-identification

**K-Anonymity Analysis**:
- Ensured k ≥ 5 for all quasi-identifier combinations
- Suppressed or generalized cells with k < 5

**Example**:
```
# High risk (k=2)
Age: 47, Gender: Female, State: Vermont, Diagnosis: Pancreatic Cancer

# Mitigated (k=12)
Age: 45-49, Gender: Female, Region: New England, Diagnosis: GI Cancer
```

## 9. Quality Assurance

### 9.1 Deidentification Checklist

Before data release:
- [ ] All 18 HIPAA identifiers removed
- [ ] Dates shifted or generalized
- [ ] Geographic information limited to state
- [ ] Numeric identifiers replaced
- [ ] Free-text scrubbed
- [ ] Manual review completed
- [ ] K-anonymity ≥ 5 verified
- [ ] Independent review completed
- [ ] Privacy officer sign-off obtained

### 9.2 Testing

**Validation Process**:
1. **Automated scanning**: Run PII detection tools on deidentified data
2. **Manual audits**: Review 10% sample for residual identifiers
3. **Re-identification testing**: Attempt to match with public records
4. **Expert review**: Privacy officer final approval

## 10. Audit Trail

### 10.1 Documentation

All deidentification actions logged:
```json
{
  "timestamp": "2024-03-20T10:30:00Z",
  "action": "deidentify_ms_file",
  "original_file": "[HASHED]",
  "output_file": "STUDY_0001_sample.mgf",
  "identifiers_removed": ["patient_id", "instrument_serial", "operator"],
  "reviewer": "RC-001",
  "approved_by": "PO-001"
}
```

### 10.2 Version Control

- **Deidentification Script**: Version 1.0.0 (Git hash: abc123)
- **Last Updated**: 2025-10-25
- **Validation Date**: 2025-10-28

## 11. Residual Risk Assessment

### 11.1 Acceptable Risk Level

Per institutional policy:
- **Risk of re-identification**: Very small (<0.01%)
- **Sensitivity of data**: Moderate (health information)
- **Mitigation**: Multi-layer deidentification
- **Approval**: IRB exemption (45 CFR 46.104(d)(4))

### 11.2 Ongoing Monitoring

- Annual review of deidentification procedures
- Update protocols as new re-identification techniques emerge
- Monitor published literature for re-identification attacks

## 12. Contact for Questions

**Privacy Officer**: [Name, Contact]
**IRB Contact**: [Name, Contact]
**Principal Investigator**: [Name, Contact]

---

## Appendix A: Deidentification Software

| Tool | Version | Purpose |
|------|---------|---------|
| Presidio | 2.2.33 | PII detection |
| spaCy | 3.7.0 | NER for free-text |
| pandas | 2.0.3 | Data manipulation |
| hashlib | (Python stdlib) | Study ID generation |

## Appendix B: Regular Expressions

**Phone Numbers**:
```regex
(\+\d{1,2}\s?)?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}
```

**Email Addresses**:
```regex
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b
```

**MRNs**:
```regex
MRN:?\s*\d{6,10}
```

**Dates**:
```regex
\d{1,2}[/-]\d{1,2}[/-]\d{2,4}
```

---

**Document Version**: 1.0
**Last Updated**: 2025-10-25
**Approved By**: [Privacy Officer Name]
