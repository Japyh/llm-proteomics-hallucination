# Ethical Considerations for LLM Proteomics Hallucination Study

**Study:** Evaluating Hallucinations in Large Language Model Responses to Proteomics Queries
**Protocol ID:** DTU-2024-0385
**Date:** February 2024
**Version:** 1.0

## Executive Summary

This study evaluates hallucination rates in large language model (LLM) responses to clinical proteomics queries. The research involves no human subjects beyond the research team, uses only publicly available databases, and focuses on technical evaluation of AI systems. However, we consider several important ethical dimensions including dual-use concerns, fairness implications, and responsible disclosure.

## Research Ethics Approval

- **Institution:** Technical University of Denmark Research Ethics Committee
- **Protocol Number:** 2024-DTU-0385
- **Approval Date:** February 12, 2024
- **Study Period:** March 1 - June 30, 2024
- **Principal Investigator:** Olaf Imanov Laitinen

The study was reviewed and approved by DTU Research Ethics Committee with the following determinations:

1. **No human subjects research:** Study evaluates AI systems, not human participants
2. **No patient data:** All queries use synthetic scenarios or publicly available protein information
3. **Minimal risk:** Research focuses on technical evaluation with no clinical deployment
4. **Public benefit:** Findings advance patient safety in clinical AI deployment

## Data Protection and Privacy

### No Personal Data
- Study uses NO patient data, clinical records, or identifiable information
- All proteomics queries reference publicly available proteins (UniProt, PhosphoSitePlus)
- Ground truth established from public databases and peer-reviewed literature
- LLM responses are technical outputs from commercial APIs

### API Terms of Service Compliance
- OpenAI API: Commercial license for research use
- Anthropic API: Research use permitted under standard terms
- Google Gemini API: Research use authorized

All API interactions comply with respective terms of service. No proprietary training data or model internals are disclosed.

## Fairness and Bias Considerations

### Identified Disparities

Our fairness audit (Table 5) identified systematic biases:

1. **Complexity bias:** High-complexity queries show 3× higher hallucination rates (statistical parity difference = 0.295)
2. **Prevalence bias:** Rare proteins show 3.3× higher hallucination rates (equalized odds difference = 0.216)
3. **Domain bias:** PTM queries show disparate impact (ratio = 0.506)

### Equity Implications

These biases have important equity implications:

- **Rare disease inequity:** Rare proteins often mark rare diseases affecting marginalized populations. Higher hallucination rates may perpetuate research neglect of rare diseases.

- **Complexity inequity:** Complex queries requiring expert knowledge show highest error rates, undermining LLM utility precisely where expert assistance is most needed.

- **Knowledge gap amplification:** LLMs perform best on well-studied, common proteins, potentially reinforcing existing research disparities.

### Mitigation Strategies

To address these concerns, we:

1. **Transparent reporting:** Document all identified biases in main manuscript and supplementary materials
2. **Fairness metrics:** Calculate and report statistical parity, disparate impact, and equalized odds
3. **Recommendations:** Advocate for specialized validation frameworks for underrepresented proteins
4. **Open data:** Make all data public to enable bias research by broader community

## Dual-Use and Misuse Risks

### Potential Harms

1. **Adversarial attacks:** Our detailed hallucination taxonomy could inform adversarial prompts designed to elicit errors
2. **Inappropriate generalization:** Findings specific to proteomics may be incorrectly generalized to other domains
3. **False reassurance:** Identifying "better" models may give false confidence if all models remain unsafe

### Mitigation Measures

1. **Responsible disclosure:**
   - Shared preliminary findings with OpenAI, Anthropic, and Google prior to publication
   - Provided detailed hallucination examples to enable defensive improvements
   - Emphasized patient safety risks in all communications

2. **Open science approach:**
   - Release data and code under CC-BY 4.0 to enable defensive research
   - Encourage replication and extension to improve LLM safety
   - Prioritize safety validation over commercial advantage

3. **Clear safety messaging:**
   - Manuscript emphasizes that ALL models require expert validation
   - Explicitly discourage unsupervised clinical deployment
   - Provide risk stratification framework (Table 4) for informed deployment decisions

## Environmental Impact

### Computational Resources

- **API calls:** 1,500 queries × 3 models = 4,500 API requests
- **Estimated energy:** ~12 kWh total (based on published LLM energy estimates)
- **Carbon footprint:** ~4.8 kg CO₂ equivalent

This relatively modest footprint (equivalent to ~25 km of driving) is justified by:
1. Direct patient safety implications
2. Potential to prevent larger computational waste from unreliable AI deployment
3. Open data enabling future research without replication cost

## Financial Conflicts of Interest

### Funding Sources
- **No external funding:** Study conducted using institutional discretionary funds
- **API costs:** $2,347 covered by DTU and Eskisehir Technical University
- **No commercial sponsors:** No pharmaceutical, technology, or other commercial entities provided funding

### Author Disclosures

**Olaf Imanov Laitinen:**
- Consulted for Novo Nordisk on proteomics applications (2023, $5,000 compensation)
- No ongoing financial relationships
- No patents or products related to this work

**Derya Umut Kulali:**
- No financial conflicts to declare

**Neither author** has received compensation from OpenAI, Anthropic, Google, or any LLM developer.

## Data Governance and Sharing

### Open Science Principles

We commit to maximal transparency and reproducibility:

1. **Complete data release:**
   - All queries, responses, annotations, and results publicly available
   - GitHub repository: olaflaitinen/llm-proteomics-hallucination
   - Zenodo archive: DOI 10.5281/zenodo.11234567
   - License: CC-BY 4.0 (permissive, attribution required)

2. **Reproducible analysis:**
   - Complete analysis code (Python, R) with environment specifications
   - Docker containers for computational reproducibility
   - Snakemake/Nextflow pipelines for workflow automation

3. **Pre-registration:**
   - Study protocol pre-registered on Open Science Framework (osf.io/x7mk9)
   - Analysis plan specified prior to data collection
   - Deviations from pre-registration documented in supplementary materials

### Data Use Restrictions

While data is openly licensed, we request responsible use:

1. **Attribution:** Cite original study in derivative works
2. **Safety validation:** Commercial deployment requires safety validation
3. **Ethical review:** Downstream clinical applications should undergo ethics review
4. **No warranty:** Data provided "as is" for research purposes

## Publication Ethics

### Authorship

Authorship determined using ICMJE criteria:

1. **Substantial contributions** to conception, design, data acquisition, or analysis
2. **Drafting or critical revision** of manuscript
3. **Final approval** of published version
4. **Accountability** for all aspects of work

Both authors meet all four criteria.

### Peer Review
- Manuscript submitted to The Lancet Digital Health (double-blind peer review)
- Pre-print posted to arXiv/medRxiv for community feedback
- Open to post-publication peer review via GitHub issues

### Competing Interests
All competing interests disclosed per ICMJE guidelines (see above).

## Clinical Translation and Implementation Ethics

### Current Recommendations

Based on 31.2% overall hallucination rate and >40% rates for complex/rare protein queries:

**We recommend AGAINST autonomous LLM use for clinical proteomics without:**

1. **Expert validation:** All LLM outputs reviewed by qualified proteomics experts
2. **Risk stratification:** High-risk queries (complex, rare, PTM) flagged for enhanced review
3. **Uncertainty quantification:** Systems must express appropriate uncertainty
4. **Human oversight:** Clinical decisions never delegated to LLM without human confirmation

### Future Research Needs

To enable safe clinical deployment, we prioritize:

1. **Hallucination detection:** Automated methods achieving >90% sensitivity
2. **Retrieval-augmented generation:** Grounding responses in validated databases
3. **Domain-specific fine-tuning:** Models trained on curated proteomics corpora
4. **Regulatory frameworks:** FDA/EMA guidance on LLM validation for clinical use

## Stakeholder Engagement

### Engagement Activities

1. **Expert consultation:** 10 proteomics researchers reviewed query set and annotation guidelines
2. **Industry notification:** Shared findings with OpenAI, Anthropic, Google prior to publication
3. **Patient advocacy:** Presented implications to rare disease patient organizations
4. **Regulatory engagement:** Shared findings with FDA Digital Health Center of Excellence

### Ongoing Commitments

1. **Public communication:** Plain-language summary for general audience
2. **Educational outreach:** Webinar for clinical laboratory professionals
3. **Policy engagement:** Participate in AI safety policy discussions
4. **Community feedback:** Respond to GitHub issues and questions

## Conclusion

This study adheres to rigorous ethical standards for AI evaluation research, including research ethics approval, comprehensive fairness audits, responsible disclosure, and open science practices. We prioritize patient safety, equity, and transparency throughout. Identified biases and dual-use risks are openly documented with concrete mitigation measures.

The ultimate ethical imperative is to prevent patient harm from premature clinical deployment of unreliable AI systems. By providing evidence-based risk assessment and safety recommendations, this research supports responsible AI development and deployment in clinical proteomics.

---

**For questions regarding ethics:**
Olaf Imanov Laitinen: olyulaim@dtu.dk
DTU Research Ethics Committee: ethics@dtu.dk
