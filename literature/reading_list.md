# Research Literature

Key references for the LLM proteomics hallucination study.

---

## Primary References

### 1. LLM Hallucinations

**Survey of hallucination in natural language generation**
- Ji Z, Lee N, Frieske R, et al. ACM Computing Surveys. 2023;55(12):1-38.
- Comprehensive taxonomy of hallucination types and evaluation approaches

**Siren's song in the AI ocean: A survey on hallucination in large language models**
- Zhang Y, Li Y, Cui L, et al. arXiv:2309.01219. 2023.
- Recent survey specific to LLMs including GPT-4 and Claude

---

### 2. Clinical AI Safety

**High-performance medicine: the convergence of human and artificial intelligence**
- Topol EJ. Nature Medicine. 2019;25(1):44-56.
- Vision for AI in clinical practice and safety considerations

**Machine learning in medicine**
- Rajkomar A, Dean J, Kohane I. New England Journal of Medicine. 2019;380(14):1347-1358.
- Clinical deployment challenges and regulatory considerations

**Challenges to the reproducibility of machine learning models in health care**
- Beam AL, Manrai AK, Ghassemi M. JAMA. 2020;323(4):305-306.
- Reproducibility crisis in medical AI

---

### 3. Proteomics Fundamentals

**Mass spectrometry-based proteomics**
- Aebersold R, Mann M. Nature. 2003;422(6928):198-207.
- Classic foundational paper on MS-based proteomics

**Protein biomarker discovery and validation: the long and uncertain path to clinical utility**
- Rifai N, Gillette MA, Carr SA. Nature Biotechnology. 2006;24(8):971-983.
- Clinical validation challenges for protein biomarkers

**The human proteome in 2023**
- Uhlen M, Karlsson MJ, Zhong W, et al. Nucleic Acids Research. 2023;51(D1):D1301-D1310.
- Human Protein Atlas comprehensive proteome mapping

---

### 4. AI Ethics in Healthcare

**Implementing machine learning in health care - addressing ethical challenges**
- Char DS, Shah NH, Magnus D. New England Journal of Medicine. 2018;378(11):981-983.
- Key ethical frameworks and practical guidance

**The ethics of AI in health care: A mapping review**
- Morley J, Machado CCV, Burr C, et al. Social Science & Medicine. 2020;260:113172.
- Comprehensive ethical landscape for AI in healthcare

**Dissecting racial bias in an algorithm used to manage health populations**
- Obermeyer Z, Powers B, Vogeli C, Mullainathan S. Science. 2019;366(6464):447-453.
- Real-world example of algorithmic bias in healthcare

---

### 5. Statistical Methods

**Interrater reliability: the kappa statistic**
- McHugh ML. Biochemia Medica. 2012;22(3):276-282.
- Statistical methods for inter-rater agreement

**Multiple comparisons in clinical trials**
- Perneger TV. BMJ. 1998;316(7139):1236-1238.
- Bonferroni correction and multiple testing

---

## Secondary References

### LLM Technical Papers

**Language models are few-shot learners** (GPT-3)
- Brown TB, Mann B, Ryder N, et al. NeurIPS. 2020;33:1877-1901.

**Training language models to follow instructions with human feedback**
- Ouyang L, Wu J, Jiang X, et al. NeurIPS. 2022.

**Constitutional AI: Harmlessness from AI feedback**
- Bai Y, Kadavath S, Kundu S, et al. arXiv:2212.08073. 2022.

---

### Proteomics Analysis

**Andromeda: a peptide search engine integrated into the MaxQuant environment**
- Cox J, Neuhauser N, Michalski A, et al. Journal of Proteome Research. 2011;10(4):1794-1805.

**Protein analysis by shotgun/bottom-up proteomics**
- Zhang Y, Fonslow BR, Shan B, et al. Chemical Reviews. 2013;113(4):2343-2394.

**Plasma proteome profiling to assess human health and disease**
- Geyer PE, Holdt LM, Teupser D, Mann M. Cell Systems. 2017;4(3):185-197.

---

### AI Interpretability

**Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead**
- Rudin C. Nature Machine Intelligence. 2019;1(5):206-215.

**A unified approach to interpreting model predictions** (SHAP)
- Lundberg SM, Lee SI. NeurIPS. 2017:4765-4774.

---

### Data Privacy

**The EU general data protection regulation (GDPR)**
- Voigt P, Von dem Bussche A. Springer International Publishing. 2017.

**Privacy in the age of medical big data**
- Price WN, Cohen IG. Nature Medicine. 2019;25(1):37-43.

---

## Database References

### UniProt

**UniProt: the universal protein knowledgebase in 2023**
- The UniProt Consortium. Nucleic Acids Research. 2023;51(D1):D523-D531.
- Release 2024_01 used in this study

### Human Protein Atlas

**The human protein atlas: a spatial map of the human proteome**
- Uhlen M, Fagerberg L, Hallstrom BM, et al. Science. 2015;347(6220):1260419.
- Version 23.0 used in this study

### PeptideAtlas

**The PeptideAtlas project**
- Desiere F, Deutsch EW, King NL, et al. Nucleic Acids Research. 2006;34(Database issue):D655-D658.
- Release 2024-01 used in this study

### PhosphoSitePlus

**PhosphoSitePlus, 2014: mutations, PTMs and recalibrations**
- Hornbeck PV, Zhang B, Murray B, et al. Nucleic Acids Research. 2015;43(D1):D512-D520.

---

## Search Strategy

### Databases Searched

- PubMed/MEDLINE
- Google Scholar
- arXiv (cs.AI, cs.CL, cs.LG)
- bioRxiv
- medRxiv

### Search Terms

**Primary**:
- "hallucination" AND "large language model"
- "LLM" AND "healthcare" AND "safety"
- "proteomics" AND "machine learning"
- "clinical decision support" AND "AI"

**Secondary**:
- "factual consistency" AND "language models"
- "biomarker discovery" AND "artificial intelligence"
- "medical AI" AND "errors"
- "protein identification" AND "neural networks"

---

## Citation Management

**Primary Tool**: BibTeX (see `literature/bibliography.bib`)
**Style**: Vancouver (numerical superscript)
**Management**: Zotero/Mendeley compatible

---

## Research Gaps Identified

1. **No specific studies on LLM hallucinations in proteomics**
   - This study addresses this gap directly
   - Establishes baseline error rates

2. **Limited evaluation of clinical impact in specialized domains**
   - Focus on patient safety implications
   - Domain-specific risk assessment

3. **Lack of standardized evaluation frameworks**
   - Develop rigorous ground truth validation
   - Multi-expert consensus approach

4. **Unclear regulatory pathway for LLM-based clinical tools**
   - Inform FDA/EMA guidance development
   - Propose safety thresholds

---

## Related Systematic Reviews

**Artificial intelligence in clinical proteomics: A systematic review**
- Planned future work
- PROSPERO registration pending

**Hallucination detection methods for language models: A systematic review and meta-analysis**
- Related ongoing work in AI safety community

---

## Contact

For literature recommendations or collaboration:
- Email: olyulaim@dtu.dk
- BibTeX file: `literature/bibliography.bib`

---

**Last Updated**: November 9, 2024
**Total References**: 34 primary + supplementary materials
