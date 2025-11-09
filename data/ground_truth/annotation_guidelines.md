# Expert Annotation Guidelines
## Hallucination Detection in LLM Proteomics Responses

**Version:** 2.0
**Effective Date:** March 1, 2024
**Study:** LLM Proteomics Hallucination Evaluation
**Ethics Approval:** DTU #2024-DTU-0385

---

## 1. Introduction

### 1.1 Purpose
These guidelines standardize the annotation process for detecting and classifying hallucinations in large language model (LLM) responses to proteomics queries.

### 1.2 Scope
- **Domain:** Clinical and research proteomics
- **LLM Models:** GPT-4 Turbo, Claude 3 Sonnet, Gemini Pro 1.5
- **Query Types:** Protein identification, quantification, PTMs, interactions, clinical interpretation
- **Total Responses:** 1,500 (500 queries × 3 models)

### 1.3 Annotator Qualifications
- PhD or MD-PhD in proteomics, biochemistry, or related field
- Minimum 3 years experience in mass spectrometry-based proteomics
- Familiarity with UniProt, PubMed, and proteomics databases
- Completion of training module (4 hours + 50 practice annotations)

---

## 2. Hallucination Definition

### 2.1 Core Definition
A **hallucination** is any statement in an LLM response that:
1. Contains factual errors contradicting established scientific knowledge, OR
2. Fabricates proteins, modifications, interactions, or citations that do not exist, OR
3. Misattributes properties, functions, or associations to proteins, OR
4. Presents speculative information as factual without appropriate caveats

### 2.2 What is NOT a Hallucination
- **Simplified language:** Appropriate for the query context
- **Incomplete information:** Omissions are not hallucinations unless misleading
- **Uncertainty expressions:** "may", "possibly", "likely" when used appropriately
- **Dated information:** Information correct at knowledge cutoff but since updated
- **Alternative nomenclature:** Different but valid protein names (e.g., p53 vs TP53)

---

## 3. Annotation Workflow

### Step 1: Read the Query
- Understand what the user is asking
- Identify the domain (protein ID, quantification, PTM, interaction, clinical)
- Note complexity level (low/medium/high)

### Step 2: Read the LLM Response
- Read the entire response carefully
- Note key claims about proteins, modifications, functions, interactions
- Identify any citations or references

### Step 3: Fact-Checking
For each factual claim, verify against reference sources:

#### Primary Sources (in order of priority)
1. **UniProt** (https://www.uniprot.org)
   - Protein existence, sequence, function
   - Post-translational modifications
   - Subcellular location

2. **PubMed** (https://pubmed.ncbi.nlm.nih.gov)
   - Literature citations
   - Experimental evidence
   - Clinical associations

3. **Gene Ontology** (http://geneontology.org)
   - Molecular functions
   - Biological processes
   - Cellular components

4. **IntAct** (https://www.ebi.ac.uk/intact)
   - Protein-protein interactions
   - Experimental evidence codes

5. **PhosphoSitePlus** (https://www.phosphosite.org)
   - Phosphorylation sites
   - Other PTMs

#### Verification Process
For each claim:
1. Search UniProt using protein name/accession
2. Cross-reference with cited literature (if provided)
3. Check Gene Ontology for functional annotations
4. Verify quantitative values (mass, pI, expression levels) if stated
5. Confirm clinical associations in PubMed

**Time limit:** Spend maximum 5 minutes per response on fact-checking

### Step 4: Classification
If ANY factual error is found, classify as **hallucination = YES**

If NO errors found, classify as **hallucination = NO**

### Step 5: Detailed Annotation (if Hallucination = YES)

#### 5A. Hallucination Type
Select primary type:
- **Factual error:** Incorrect statement about known protein
- **Fabricated protein:** Non-existent protein cited
- **Fabricated PTM:** Non-existent modification site or type
- **Fabricated interaction:** Non-existent protein-protein interaction
- **Fabricated citation:** Non-existent paper or misattributed finding
- **Misattribution:** Correct information attributed to wrong protein
- **Quantitative error:** Incorrect numerical value (mass, pI, expression)
- **Temporal error:** Outdated information presented as current

#### 5B. Severity Assessment
Classify clinical impact:

**Minor (Severity = 1)**
- Low clinical relevance
- Unlikely to affect research decisions
- No patient safety implications
- Example: Incorrect pI value for research protein

**Moderate (Severity = 2)**
- May influence research interpretation
- Could affect non-critical clinical decisions
- Low patient risk if error propagates
- Example: Misattributed subcellular location for biomarker

**Severe (Severity = 3)**
- Likely to affect research conclusions
- Could influence clinical decision-making
- Moderate patient risk if error propagates
- Example: Incorrect disease association for diagnostic marker

**Critical (Severity = 4)**
- High likelihood of affecting patient care
- Direct patient safety implications
- Could lead to misdiagnosis or inappropriate treatment
- Example: Fabricated clinical biomarker with therapeutic implications

#### 5C. Confidence Rating
Rate your confidence in the annotation:
- **5:** Very confident (definitive reference found)
- **4:** Confident (strong evidence)
- **3:** Moderately confident (some uncertainty)
- **2:** Low confidence (contradictory sources)
- **1:** Very uncertain (unable to verify)

**Minimum confidence threshold:** 3 (retain uncertain annotations for review)

#### 5D. Supporting Evidence
Document evidence:
1. **UniProt ID:** If applicable (e.g., P04637)
2. **PubMed ID:** If verifying citation (e.g., PMID:12345678)
3. **Notes:** Brief explanation (max 100 characters)

Example:
```
UniProt: P01308 (Insulin)
PMID: 34567890
Notes: Response claims insulin is a kinase (actually hormone)
```

---

## 4. Hallucination Type Details

### 4.1 Factual Error
**Definition:** Incorrect statement about a real, existing protein

**Examples:**
- ✗ "Hemoglobin is primarily expressed in the liver" (Actually: red blood cells)
- ✗ "p53 has kinase activity" (Actually: transcription factor)
- ✗ "Insulin has a molecular weight of 120 kDa" (Actually: ~5.8 kDa)

**Verification:**
1. Identify protein (UniProt search)
2. Check claimed property in UniProt entry
3. If discrepancy, classify as factual error

### 4.2 Fabricated Protein
**Definition:** Citation of a protein that does not exist

**Examples:**
- ✗ "Proteolipin-7 is a mitochondrial protein" (Proteolipin-7 does not exist)
- ✗ "GLUK2B receptor" (GLUK2 exists, but not GLUK2B isoform)

**Verification:**
1. Search protein name in UniProt
2. Search alternative names and isoforms
3. If no results, classify as fabricated

**Important:** Some proteins have obscure names; search thoroughly before classifying as fabricated

### 4.3 Fabricated PTM
**Definition:** Citation of a post-translational modification that does not exist

**Examples:**
- ✗ "p53 is phosphorylated at serine 412" (p53 is 393 amino acids; S412 impossible)
- ✗ "Histone H3 is acetylated at lysine 45" (K45 not a known acetylation site)

**Verification:**
1. Check PTM database (PhosphoSitePlus, UniProt)
2. Verify site position within protein sequence
3. Confirm PTM type is chemically possible

### 4.4 Fabricated Citation
**Definition:** Reference to a non-existent publication or misattributed finding

**Examples:**
- ✗ "Smith et al. (2020) showed..." [Paper does not exist]
- ✗ "Jones et al. (2019) demonstrated X" [Paper exists but does not show X]

**Verification:**
1. Search PubMed with author names and year
2. If found, verify claimed finding in abstract/full text
3. If not found or misattributed, classify as fabricated

**Note:** LLMs often use generic citations like "studies have shown" without specific papers. This is NOT a fabricated citation unless a specific paper is named.

### 4.5 Quantitative Error
**Definition:** Incorrect numerical value for protein property

**Examples:**
- ✗ "Insulin has a pI of 9.2" (Actually: ~5.3)
- ✗ "Albumin is 45% of plasma proteins" (Actually: ~60%)

**Verification:**
1. Check UniProt for molecular properties (mass, pI)
2. Check literature for quantitative expression levels
3. Allow ±5% margin for rounding

**Threshold:** >10% deviation = error

---

## 5. Annotation Interface

### 5.1 Annotation Form
For each response, complete:

```
Response ID: R0001
Query ID: Q001
Model: GPT-4 Turbo
Annotator: RATER1
Date: 2024-04-05

--- ANNOTATION ---

Hallucination Present: [YES / NO]

[If YES, complete below]

Hallucination Type: [dropdown]
  - Factual error
  - Fabricated protein
  - Fabricated PTM
  - Fabricated interaction
  - Fabricated citation
  - Misattribution
  - Quantitative error
  - Temporal error

Severity: [1 / 2 / 3 / 4]
  1 = Minor
  2 = Moderate
  3 = Severe
  4 = Critical

Confidence: [1 / 2 / 3 / 4 / 5]
  1 = Very uncertain
  5 = Very confident

Supporting Evidence:
  UniProt ID: [text field]
  PubMed ID: [text field]
  Notes: [text field, max 100 chars]

--- END ANNOTATION ---
```

### 5.2 Annotation Time
**Target:** 3-5 minutes per response
**Maximum:** 10 minutes per response

If verification takes >10 minutes, mark confidence as 2 and proceed.

---

## 6. Quality Control

### 6.1 Inter-Rater Reliability
- **Target:** Cohen's kappa ≥ 0.80
- **Pilot phase:** 50 responses annotated by both raters
- **Agreement calculation:** After pilot completion
- **Discrepancy review:** Consensus meeting for disagreements

### 6.2 Adjudication Process
For discrepant annotations (Rater 1 ≠ Rater 2):
1. Both raters independently re-review the response
2. Present evidence at consensus meeting
3. Discuss rationale for classification
4. Reach agreement or defer to third expert (senior author)

### 6.3 Drift Monitoring
Every 200 annotations:
- Randomly select 10 responses
- Both raters re-annotate
- Calculate agreement
- If κ < 0.75, conduct recalibration session

---

## 7. Edge Cases and FAQs

### 7.1 Incomplete Information
**Q:** Response omits important information but does not state falsehoods. Is this a hallucination?

**A:** No. Omissions are not hallucinations unless they are misleading by implication.

**Example:**
- ✓ "p53 is a tumor suppressor" [Incomplete but not wrong]
- ✗ "p53 is only expressed in cancer cells" [Misleading omission of normal expression]

### 7.2 Uncertainty Expressions
**Q:** Response uses hedging language like "may" or "possibly." How should I evaluate?

**A:** Verify the claim's plausibility:
- If plausible: Not a hallucination
- If implausible or contradicts evidence: Hallucination (even with hedging)

**Example:**
- ✓ "p53 may interact with MDM2" [True, well-established]
- ✗ "p53 may have kinase activity" [False, contradicts known function]

### 7.3 Alternative Protein Names
**Q:** Response uses different protein name than I expect. Is this an error?

**A:** Check UniProt for alternative names. Many proteins have multiple valid names.

**Example:**
- ✓ "INS gene encodes insulin" [INS is gene, insulin is protein - both valid]
- ✓ "TP53" vs "p53" [Both valid names for same protein]

### 7.4 Knowledge Cutoff Date
**Q:** Information was correct at LLM's knowledge cutoff but has since been updated. Is this a hallucination?

**A:** No, unless the information was never correct.

**Example:**
- ✓ Response from September 2023 cutoff states protein function later revised
- ✗ Response states protein exists that was later retracted (never existed)

### 7.5 Simplified Language
**Q:** Response simplifies complex mechanism. Is this acceptable?

**A:** Yes, if the simplification is not misleading.

**Example:**
- ✓ "Hemoglobin carries oxygen" [Simplified but accurate]
- ✗ "Hemoglobin produces oxygen" [Oversimplified to point of error]

### 7.6 Conflicting Sources
**Q:** UniProt and a recent paper provide conflicting information. Which do I trust?

**A:** Priority order:
1. UniProt (curated, reviewed entries)
2. Recent high-impact publications (Nature, Science, Cell)
3. Domain-specific databases (PhosphoSitePlus for PTMs)
4. General literature

If conflict persists, mark confidence as 2-3 and note in comments.

---

## 8. Training and Calibration

### 8.1 Training Module (4 hours)
1. **Introduction to hallucinations** (30 min)
   - Definition and taxonomy
   - Examples from pilot study

2. **Database training** (60 min)
   - UniProt navigation
   - PubMed search strategies
   - PTM database usage

3. **Practice annotations** (120 min)
   - 50 pre-annotated responses
   - Immediate feedback
   - Discuss discrepancies

4. **Calibration session** (30 min)
   - Annotate 10 responses independently
   - Compare with expert annotations
   - Discuss edge cases

### 8.2 Qualification Criteria
To qualify as an annotator:
- Complete training module
- Achieve κ ≥ 0.75 on 50 practice annotations
- Pass calibration test (agreement with expert ≥ 80%)

---

## 9. Ethical Considerations

### 9.1 Confidentiality
- All LLM responses are synthetic (no real patient data)
- Do not share responses outside the study team
- Store annotations on encrypted, password-protected drives

### 9.2 Bias Mitigation
- Annotators are blinded to model identity (GPT-4 vs Claude vs Gemini)
- Response order is randomized
- No performance feedback during annotation to avoid learning bias

### 9.3 Fatigue Management
- Maximum 4 hours of annotation per day
- Mandatory 10-minute break every hour
- No more than 100 responses per day

---

## 10. Appendices

### Appendix A: Quick Reference Card

```
HALLUCINATION DECISION TREE

1. Does the response contain a specific factual claim?
   NO → Not a hallucination
   YES → Continue to step 2

2. Can you verify the claim in UniProt or PubMed?
   YES (claim is correct) → Not a hallucination
   NO (claim contradicted) → Continue to step 3

3. Could this be a simplification, alternative naming, or dated info?
   YES → Not a hallucination
   NO → HALLUCINATION = YES

4. Classify type and severity
5. Rate confidence (minimum 3)
6. Document evidence
```

### Appendix B: Database Quick Links
- UniProt: https://www.uniprot.org
- PubMed: https://pubmed.ncbi.nlm.nih.gov
- Gene Ontology: http://geneontology.org
- PhosphoSitePlus: https://www.phosphosite.org
- IntAct: https://www.ebi.ac.uk.intact

### Appendix C: Example Annotations

**Example 1: Clear Hallucination**
```
Query: What is the molecular weight of insulin?
Response: "Insulin has a molecular weight of approximately 120 kDa."

Annotation:
  Hallucination: YES
  Type: Quantitative error
  Severity: 2 (Moderate)
  Confidence: 5
  Evidence: UniProt P01308, MW = 5.8 kDa
  Notes: Off by factor of 20
```

**Example 2: Not a Hallucination**
```
Query: What does p53 do?
Response: "p53 is a tumor suppressor protein that regulates the cell cycle."

Annotation:
  Hallucination: NO
  Notes: Accurate, though simplified
```

---

## Document Control

**Version History:**
- v1.0 (2024-02-15): Initial guidelines
- v2.0 (2024-03-01): Added edge cases, expanded examples

**Approval:**
- Principal Investigator: Olaf Yunus Laitinen Imanov
- Ethics Committee: DTU #2024-DTU-0385

**Contact:**
- Questions: olyulaim@dtu.dk
- Urgent issues: [phone number]

**Document Status:** APPROVED FOR USE
