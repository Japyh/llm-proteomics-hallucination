# Extended Methods

## Evaluating Hallucinations in LLM Proteomics Responses

---

## 1. Query Development

### 1.1 Source Material
Queries were derived from three sources:
1. **Published literature** (n=400): Extracted from 200 proteomics research articles published 2020-2024
2. **Expert-generated** (n=300): Created by three proteomics experts to cover key domains
3. **Clinical cases** (n=300): Deidentified clinical proteomics questions from academic medical centers

### 1.2 Complexity Classification
Queries classified into three complexity levels:
- **Low** (n=330): Single-concept factual questions (e.g., "What is the mass of trypsin?")
- **Medium** (n=340): Multi-concept integration (e.g., "How does phosphorylation affect protein stability in LC-MS/MS?")
- **High** (n=330): Complex reasoning or problem-solving (e.g., "Design an experiment to validate a novel biomarker for early-stage pancreatic cancer using targeted proteomics")

### 1.3 Domain Distribution
- Mass spectrometry methods: 20%
- Post-translational modifications: 15%
- Biomarker discovery/validation: 20%
- Bioinformatics/databases: 15%
- Clinical applications: 20%
- Other: 10%

## 2. LLM Configuration

### 2.1 Model Versions
- GPT-4 Turbo: `gpt-4-turbo-2024-04-09`
- Claude 3 Sonnet: `claude-3-sonnet-20240229`
- Gemini 1.5 Pro: `gemini-1.5-pro`
- Mistral Large 2: `mistral-large-2407`
- Llama 3 70B: `Meta-Llama-3-70B-Instruct` (self-hosted via vLLM)

### 2.2 Inference Parameters
- Temperature: 0.3 (reduced for determinism)
- Top-p: 0.9
- Max tokens: 2,048
- Frequency penalty: 0
- Presence penalty: 0
- Stop sequences: None

### 2.3 Prompt Engineering
All models received identical prompts with the following structure:
```
You are a proteomics expert. Please answer the following question accurately and concisely.

Question: [QUERY TEXT]

Provide your answer with supporting reasoning where appropriate.
```

## 3. Annotation Protocol

### 3.1 Annotator Selection
Three expert annotators:
- Annotator A: PhD in proteomics, 15 years experience
- Annotator B: MD-PhD, clinical proteomics, 10 years experience
- Annotator C: PhD in bioinformatics, 12 years proteomics

### 3.2 Training
- 50-query pilot phase
- Calibration meetings to align on severity scale
- Achieved κ > 0.80 before main annotation phase

### 3.3 Annotation Process
1. **Round 1**: Annotators A and B independently annotate all responses
2. **Disagreement identification**: Identify cases where severity scores differ by ≥2
3. **Adjudication**: Annotator C reviews disagreements and provides final rating
4. **Quality control**: 10% random re-annotation to monitor drift

### 3.4 Severity Scale
- **0 (No hallucination)**: Response is accurate and complete
- **1 (Minor)**: Trivial errors that don't affect interpretation (e.g., typo, minor nomenclature inconsistency)
- **2 (Moderate)**: Significant errors that could mislead but unlikely to cause immediate harm
- **3 (Severe)**: Critical errors with potential for patient harm or major research misdirection

## 4. Statistical Methods

### 4.1 Bayesian Beta-Binomial Model
For each model, hallucination rate θ modeled as:
```
y_i ~ Binomial(n_i, θ_i)
θ_i ~ Beta(α, β)
```
Weakly informative priors: α = 1, β = 1 (uniform)

MCMC: 4 chains × 2,000 iterations (1,000 warmup)
Convergence: R-hat < 1.01 for all parameters

### 4.2 Effect Size Calculation
Cohen's h for proportion differences:
```
h = 2 × [arcsin(√p1) - arcsin(√p2)]
```
Interpretation: small (0.2), medium (0.5), large (0.8)

### 4.3 Calibration Metrics
Expected Calibration Error (ECE):
```
ECE = Σ (|acc(B_m) - conf(B_m)| × |B_m|/n)
```
where B_m are bins of predicted confidence, n=10 bins

## 5. Reproducibility

### 5.1 Random Seed Control
- Global seed: 42
- Module-specific seeds derived via MD5 hash
- All stochastic processes logged

### 5.2 Version Control
- Git commit hash recorded for all analyses
- Docker containers provided for full environment reproduction
- Software Bill of Materials (SBOM) in CycloneDX format

### 5.3 Data Provenance
- in-toto attestations for all pipeline steps
- SHA-256 checksums for all data files
- Complete audit trail in `provenance/`

## 6. Ethical Considerations

### 6.1 Data Privacy
- All clinical data deidentified per HIPAA Safe Harbor
- IRB approval: [Number]
- Data Use Agreement required for access

### 6.2 AI Ethics
- No patient-facing deployment
- Research use only
- Prominent disclaimers on all LLM outputs
- Bias audit conducted

## 7. Limitations

1. **Temporal**: Single timepoint evaluation; LLMs continuously updated
2. **Language**: English-only queries
3. **Scope**: Proteomics-specific; may not generalize to other biomedical domains
4. **Ground truth**: Expert consensus as proxy for absolute truth
5. **API limitations**: Some models don't support confidence scores
