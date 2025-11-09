# CONSORT-AI Extension Checklist

## AI Algorithm Specification

### Algorithm Details
- **Name**: Multi-model LLM evaluation framework
- **Version**: GPT-4 Turbo (gpt-4-turbo-2024-04-09), Claude-3 Sonnet, Gemini-1.5 Pro
- **Intended Use**: Hallucination detection in clinical proteomics queries

### Training and Validation
- [x] Algorithm training data described: Not applicable (pre-trained models)
- [x] Validation approach: Expert annotation with adjudication
- [x] Performance metrics: Hallucination rate, accuracy, precision, recall

### Deployment
- [x] Hardware/software requirements specified
- [x] Model accessibility: API-based
- [x] Reproducibility: Random seed 42, temperature 0.1

### Ethics and Bias
- [x] Bias assessment conducted across domains, complexity, prevalence
- [x] Fairness metrics evaluated (disparate impact, 80% rule)
- [x] Limitations clearly stated
- [x] IRB approval obtained (#2025-IRB-1101)

## Human-AI Interaction
- [x] Expert annotation process described
- [x] Inter-rater reliability reported (Cohen's Kappa)
- [x] Adjudication protocol defined
