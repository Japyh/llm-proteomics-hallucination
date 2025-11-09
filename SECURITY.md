# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of this research project seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Publicly Disclose

Please do not publicly disclose the vulnerability until we have had a chance to address it.

### 2. Contact Us

Report security vulnerabilities by emailing:
- **Email**: [security contact - add institutional email]
- **Subject**: [SECURITY] LLM Proteomics Hallucination Project

Include the following in your report:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (optional)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity (critical issues within 30 days)

## Security Considerations for This Research

### Data Privacy

1. **Protected Health Information (PHI)**: This research may involve deidentified clinical data
   - All patient data has been deidentified per HIPAA Safe Harbor standards
   - Direct identifiers removed before analysis
   - See `ethics/deidentification_procedure.md` for full protocol

2. **API Keys**: Never commit API keys to the repository
   - Use `.env` files (already in `.gitignore`)
   - Rotate keys regularly
   - Use least-privilege access

### LLM API Security

1. **Rate Limiting**: Implement rate limits to prevent abuse
2. **Input Validation**: Sanitize all inputs to LLM APIs
3. **Output Filtering**: Review LLM outputs for potential information leakage
4. **Cost Controls**: Set usage limits on all API accounts

### Container Security

Our Docker containers follow security best practices:

- Base images regularly updated (Ubuntu 22.04 LTS)
- Non-root user execution where possible
- Minimal package installation
- SBOM provided (`containers/sbom/bom.cyclonedx.xml`)

### Dependency Security

We use:
- **Dependabot**: Automated dependency updates (GitHub Actions)
- **CodeQL**: Static security scanning (`.github/workflows/codeql.yml`)
- **Bandit**: Python security linting (`.github/workflows/lint.yml`)

### Known Security Considerations

#### 1. Proteomics Data
- Mass spectrometry data may contain metadata that could be used for re-identification
- Retention time information sanitized
- Instrument serial numbers removed

#### 2. LLM Responses
- May inadvertently generate sensitive information
- All outputs reviewed before publication
- Potential for prompt injection attacks (mitigated via input sanitization)

#### 3. Model Weights
- Local model weights (Llama 3 70B) require secure storage
- Access controls on GPU servers
- Model served via vLLM with authentication

## Compliance

This research complies with:
- **HIPAA**: For deidentified clinical data
- **GDPR**: For EU participant data (if applicable)
- **NIH Data Sharing Policy**: For publicly funded research
- **Institutional Review Board (IRB)**: See `ethics/consent_and_irb/IRB_approval.pdf`

## Security Audit Trail

All security-relevant events are logged:
- API access (see `configs/logging.yaml`)
- Data processing steps (see `provenance/`)
- Model inference requests (MLflow tracking)

## Third-Party Services

We use the following third-party services:
- **OpenAI API**: GPT-4 inference (SOC 2 Type II compliant)
- **Anthropic API**: Claude inference (SOC 2 Type II compliant)
- **Google Vertex AI**: Gemini inference (ISO 27001 certified)
- **Mistral API**: Mistral Large 2 inference
- **MLflow**: Self-hosted (PostgreSQL backend with encryption)
- **Weights & Biases**: Cloud experiment tracking (encrypted in transit/at rest)

## Reproducibility and Integrity

To ensure research integrity:
- **Checksums**: All data files have SHA-256 checksums (`provenance/checksums/`)
- **Provenance**: Full lineage tracking via in-toto (`provenance/provenance.intoto.jsonl`)
- **Version Control**: All code changes tracked via Git
- **Seed Control**: Reproducible random number generation (`data/generators/random_seed_control.py`)

## Incident Response

In the event of a security incident:
1. Immediately contain the threat
2. Notify the research team and institutional security office
3. Document the incident in `provenance/build_logs/`
4. Conduct post-incident review
5. Update security measures as needed

## Contact

For security questions or concerns:
- **Primary Contact**: [Add primary investigator contact]
- **Institutional Security**: [Add institutional security office]
- **IRB Contact**: [Add IRB contact for ethical concerns]

---

**Last Updated**: 2025-01-15
**Version**: 1.0.0
