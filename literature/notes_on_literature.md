# Literature Review Notes

## LLM Proteomics Hallucination Study

**Last Updated**: 2025-01-15

---

## 1. LLM Hallucination Research

### Ji et al. (2023) - Survey of Hallucination in NLG
**Citation**: Ji, Z., et al. (2023). Survey of Hallucination in Natural Language Generation. *ACM Computing Surveys*, 55(12), 1-38.

**Key Points**:
- Comprehensive taxonomy of hallucination types: intrinsic vs. extrinsic
- Intrinsic: Output contradicts source
- Extrinsic: Output cannot be verified from source
- Proposes detection methods: fact-checking, uncertainty quantification

**Relevance**: Foundation for our hallucination taxonomy; we extend to domain-specific (proteomics) hallucinations

**Notes**:
- Their categorization doesn't account for scientific/technical domains
- Need to adapt for factual errors in protein nomenclature, PTMs, etc.

---

### Zhang et al. (2023) - Siren's Song Survey
**Citation**: Zhang, Y., et al. (2023). Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models. *arXiv:2309.01219*.

**Key Points**:
- Focus on LLMs specifically (vs. general NLG)
- Causes: data quality, model architecture, decoding strategy
- Mitigation: retrieval augmentation, fact-checking, human feedback

**Relevance**: Directly applicable to our GPT-4/Claude/Gemini evaluation

**Notes**:
- Emphasizes importance of domain-specific evaluation (supports our approach)
- Suggests calibration analysis (which we include)

---

## 2. LLMs in Healthcare/Biomedicine

### Singhal et al. (2023) - Med-PaLM
**Citation**: Singhal, K., et al. (2023). Large language models encode clinical knowledge. *Nature*, 620, 172-180.

**Key Points**:
- Med-PaLM achieves expert-level performance on medical questions
- BUT: 18.7% hallucination rate even with RLHF
- Calibration analysis shows overconfidence
- Safety concerns for clinical deployment

**Relevance**: Demonstrates need for domain-specific evaluation (medicine → proteomics)

**Comparison to Our Work**:
- They focus on clinical Q&A; we focus on proteomics
- They use multiple-choice; we use free-form responses
- Both emphasize safety implications

**Notes**:
- Their calibration methodology (ECE, reliability diagrams) → we adopt
- Their annotator training protocol → adapted for our expert annotators

---

### Thirunavukarasu et al. (2023) - LLMs in Medicine Review
**Citation**: Thirunavukarasu, A. J., et al. (2023). Large language models in medicine. *Nature Medicine*, 29, 1930-1940.

**Key Points**:
- Comprehensive review of LLM applications in medicine
- Identifies hallucination as primary barrier to clinical adoption
- Calls for rigorous evaluation frameworks

**Relevance**: Motivates our work; proteomics is understudied compared to clinical medicine

**Gaps Identified**:
- No mention of proteomics/omics applications
- Limited discussion of laboratory medicine
- Our study fills this gap

---

### Azamfirei et al. (2023) - Perils of Hallucinations
**Citation**: Azamfirei, R., et al. (2023). Large language models and the perils of their hallucinations. *Critical Care Medicine*, 51(8), 1026-1028.

**Key Points**:
- Case study of ChatGPT generating false medical references
- Warns against uncritical acceptance of LLM outputs
- Calls for verification mechanisms

**Relevance**: Motivates our verification framework (expert annotation)

---

## 3. LLMs in Proteomics/Bioinformatics

### Abell-Hart et al. (2023) - Proteins, Pathways, Phenotypes
**Citation**: Abell-Hart, K., et al. (2023). Proteins, Pathways, and Phenotypes: Evaluating Large Language Models on Proteomics Tasks. *bioRxiv* 2023.08.30.555625.

**Key Points**:
- First study evaluating LLMs on proteomics tasks
- Tests GPT-4, GPT-3.5 on protein function prediction, pathway analysis
- Finds reasonable performance but limited to well-studied proteins

**Relevance**: MOST DIRECTLY RELATED WORK

**Differences from Our Study**:
1. They focus on protein function prediction; we focus on hallucinations
2. They use structured tasks; we use free-form queries
3. They evaluate GPT-3.5/4 only; we include Claude, Gemini, Mistral, Llama
4. They don't analyze hallucination severity or clinical safety

**Complementarity**:
- Their work shows LLMs can do proteomics tasks
- Our work evaluates safety and reliability

**Notes**:
- Collaborate? Cite prominently as related work
- Their dataset could complement ours (different query types)

---

### Taylor et al. (2022) - Galactica
**Citation**: Taylor, R., et al. (2022). Galactica: A Large Language Model for Science. *arXiv:2211.09085*.

**Key Points**:
- Science-focused LLM trained on papers, datasets, code
- Includes proteomics literature in training
- Withdrawn after public criticism for hallucinations

**Relevance**: Cautionary tale; science-specific training ≠ hallucination-free

**Notes**:
- Galactica controversy highlights need for evaluation (like ours)
- Consider evaluating if model becomes available again

---

## 4. Proteomics Methods (for context)

### Cox & Mann (2008) - MaxQuant
**Citation**: Cox, J., & Mann, M. (2008). MaxQuant enables high peptide identification rates. *Nature Biotechnology*, 26, 1367-1372.

**Relevance**: Standard tool for proteomics; queries may reference MaxQuant workflows

### Röst et al. (2016) - OpenMS
**Citation**: Röst, H. L., et al. (2016). OpenMS: a flexible open-source software platform. *Nature Methods*, 13, 741-748.

**Relevance**: Another standard tool; used in our query generation

---

## 5. LLM Evaluation Methodologies

### Lin et al. (2022) - TruthfulQA
**Citation**: Lin, S., et al. (2022). TruthfulQA: Measuring How Models Mimic Human Falsehoods. *ACL 2022*.

**Key Points**:
- Benchmark for evaluating truthfulness
- LLMs often mimic human misconceptions
- Human evaluation necessary (automated metrics insufficient)

**Relevance**: Justifies our expert annotation approach

**Adaptation**:
- TruthfulQA uses crowd workers; we use domain experts
- TruthfulQA is general knowledge; we're domain-specific

---

### Guo et al. (2017) - Calibration of Neural Networks
**Citation**: Guo, C., et al. (2017). On Calibration of Modern Neural Networks. *ICML 2017*.

**Key Points**:
- Modern neural networks poorly calibrated (overconfident)
- Proposes temperature scaling for recalibration
- ECE (Expected Calibration Error) as metric

**Relevance**: Framework for our calibration analysis

**Methods We Adopt**:
- ECE calculation
- Reliability diagrams
- Temperature scaling (if applicable)

---

## 6. Clinical Proteomics and Biomarkers

### Rifai et al. (2006) - Protein Biomarker Discovery
**Citation**: Rifai, N., et al. (2006). Protein biomarker discovery and validation. *Nature Biotechnology*, 24, 971-983.

**Key Points**:
- Long path from discovery to clinical utility
- Importance of rigorous validation
- Many candidate biomarkers fail in validation

**Relevance**: Context for clinical safety hallucinations in our study

**Connection**:
- If LLM hallucinates biomarker performance, could mislead research
- Emphasizes need for accuracy in biomarker queries

---

## 7. AI/ML in Clinical Decision Support

### Rajkomar et al. (2019) - Machine Learning in Medicine
**Citation**: Rajkomar, A., et al. (2019). Machine Learning in Medicine. *NEJM*, 380, 1347-1358.

**Key Points**:
- ML shows promise but faces deployment challenges
- Need for validation, interpretability, bias mitigation
- Regulatory considerations

**Relevance**: Broader context for LLM deployment in healthcare

---

## 8. Reporting Guidelines

### Collins et al. (2024) - TRIPOD-AI
**Citation**: Collins, G. S., et al. (2024). TRIPOD-AI statement. *BMJ*, 385, e078378.

**Key Points**:
- Reporting guideline for AI prediction models
- Extends TRIPOD to AI/ML context
- Emphasizes transparency, reproducibility

**Relevance**: We follow TRIPOD-AI for reporting

**Checklist**: See `paper/supplementary/TRIPOD_AI_checklist.pdf`

---

## Research Gaps Identified

1. **Proteomics underrepresented** in LLM evaluation literature
   - Most work on general medicine, few on laboratory/omics
   - Our study addresses this gap

2. **Hallucination severity** not well-studied
   - Most work reports binary (hallucination yes/no)
   - We use 4-level severity scale

3. **Clinical safety implications** underexplored
   - Need to distinguish trivial errors from dangerous ones
   - Our clinical safety rating addresses this

4. **Multi-model comparison** limited
   - Most studies evaluate 1-2 models
   - We evaluate 5 models (proprietary + open-source)

5. **Calibration in domain-specific contexts** understudied
   - General calibration studied, but not for specialized domains
   - We analyze calibration specifically for proteomics

---

## Future Directions from Literature

1. **Retrieval-Augmented Generation (RAG)**
   - Many papers suggest RAG to reduce hallucinations
   - Future work: Evaluate RAG for proteomics (UniProt, PDB retrieval)

2. **Fine-tuning on proteomics corpora**
   - Could domain-specific fine-tuning reduce hallucinations?
   - Requires large proteomics text dataset

3. **Multimodal models**
   - Proteomics involves figures, spectra, structures
   - Evaluate multimodal LLMs (GPT-4V, Gemini Pro Vision)

4. **Real-time fact-checking**
   - Integrate LLM with knowledge bases for real-time verification
   - Challenge: Knowledge base incompleteness

5. **Human-AI collaboration**
   - Don't replace experts, augment them
   - Study expert+LLM performance vs. expert alone

---

## Key Takeaways for Our Paper

**Introduction**:
- Position in context of LLM healthcare applications (cite Singhal, Thirunavukarasu)
- Emphasize proteomics gap (cite Abell-Hart as related but different)
- Motivate with hallucination concerns (cite Ji, Zhang, Azamfirei)

**Methods**:
- Justify expert annotation (cite Lin - TruthfulQA)
- Explain calibration metrics (cite Guo)
- Follow reporting guidelines (cite Collins - TRIPOD-AI)

**Discussion**:
- Compare to Med-PaLM hallucination rates
- Discuss implications for clinical proteomics
- Propose future directions (RAG, fine-tuning, multimodal)

**Limitations**:
- Acknowledge single-timepoint evaluation (models evolving)
- English-only queries
- Expert availability for annotation

---

## Citation Network Insights

**Central papers** (most cited/relevant):
1. Guo et al. (2017) - Calibration [3421 citations]
2. Singhal et al. (2023) - Med-PaLM [897 citations]
3. Ji et al. (2023) - Hallucination survey [542 citations]

**Emerging papers** (recent, directly relevant):
1. Abell-Hart et al. (2023) - Proteomics + LLMs [15 citations]
2. Zhang et al. (2023) - LLM hallucination [318 citations]

**Foundational proteomics** (for context):
1. Cox & Mann (2008) - MaxQuant [15234 citations]
2. Röst et al. (2016) - OpenMS [2134 citations]

---

## Reading List for Team

**Must Read** (for all team members):
- [ ] Ji et al. (2023) - Hallucination survey
- [ ] Singhal et al. (2023) - Med-PaLM
- [ ] Abell-Hart et al. (2023) - Proteomics + LLMs

**Recommended** (for specific roles):
- Annotators: TruthfulQA methodology, Med-PaLM annotation protocol
- Statisticians: Guo et al. calibration, TRIPOD-AI guidelines
- Proteomics experts: Cox & Mann, Röst et al. (for query generation)

---

**Maintained by**: [Name]
**Next review**: 2025-02-15
