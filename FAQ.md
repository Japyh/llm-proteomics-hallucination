# Frequently Asked Questions (FAQ)

Common questions about the LLM Proteomics Hallucination Study.

---

## General Questions

### What is this project about?

This is a research study evaluating hallucination risks when using large language models (GPT-4, Claude, Gemini) for clinical proteomics data interpretation. We tested 1,500 queries and found an overall hallucination rate of 31.2%.

### Who should use this repository?

- Researchers studying LLM safety and reliability
- Proteomics researchers interested in AI applications
- Clinicians evaluating AI tools for proteomics
- Students learning about AI in healthcare
- Developers building clinical decision support systems

### Is this ready for clinical use?

**No.** Our findings show hallucination rates of 27.8-34.6% are incompatible with safe clinical deployment. This is a research tool to understand risks, not a clinical application.

---

## Data Questions

### Where can I get the data?

All data are available in this repository:
- Queries: `data/queries/queries_all.json`
- Results: `data/results/`
- Ground truth: `data/ground_truth/`

Full dataset also archived on Zenodo: DOI 10.5281/zenodo.11234567

### Can I use this data for my research?

Yes! Data are released under CC-BY 4.0 license. Please cite:
```
Laitinen Imanov OY, Kulali DU. Hallucination risks of large language models
in clinical proteomics: a prospective evaluation study. 2024.
DOI: 10.5281/zenodo.11234567
```

### Does this contain patient data?

No. All data are public and synthetic. No patient data were used.

### How was ground truth established?

Multi-step validation:
1. Cross-reference with UniProt, Human Protein Atlas, PeptideAtlas
2. Literature search (PubMed)
3. Expert consensus (2 raters, Cohen's kappa = 0.89)

---

## Technical Questions

### What Python version is required?

Python 3.11 or higher. Tested on 3.11.5.

### Do I need API keys?

Only if you want to query LLMs yourself. For reproducing our analysis, all LLM responses are already included in `data/llm_responses/`.

### What are the API costs?

Approximate costs for 500 queries:
- GPT-4 Turbo: ~$45
- Claude 3 Sonnet: ~$25
- Gemini Pro 1.5: ~$18

### Can I run this without internet?

Yes, for data analysis. No, for querying LLMs (requires API access).

### What hardware do I need?

Minimum: 8GB RAM, 5GB disk space
Recommended: 16GB RAM, 20GB disk space
GPU not required.

---

## Results Questions

### What was the main finding?

Overall hallucination rate of 31.2% across 1,500 queries, with rates increasing dramatically for complex queries about rare proteins (>50%).

### Which model performed best?

Claude 3 Sonnet (27.8%), followed by GPT-4 Turbo (31.2%) and Gemini Pro 1.5 (34.6%). However, all models exceeded 40% error rates for complex queries.

### What factors increase hallucination risk?

- Query complexity (OR=5.1)
- Protein rarity (OR=5.4)
- Post-translational modification domain (41.8% rate)

### Are the results statistically significant?

Yes. All key findings significant at p<0.001 level with Bonferroni correction for multiple comparisons.

---

## Usage Questions

### How do I reproduce the main results?

```bash
# Install environment
conda env create -f environment.yml
conda activate llm-proteomics

# Run analysis notebooks
jupyter lab notebooks/

# Generate figures
cd paper/figures && python generate_figure_1.py
```

### How do I run the tests?

```bash
pytest                    # All tests
pytest -m "not slow"     # Skip slow tests
pytest --cov=src         # With coverage
```

### Can I add new queries?

Yes! See `data/generators/generate_query_dataset.py` for template.

### How do I query a different LLM?

Extend `src/llm_evaluation/llm_client.py` with your model's API.

---

## Manuscript Questions

### Where is the manuscript?

`paper/manuscript.tex` - Complete LaTeX source for The Lancet Digital Health submission.

### How do I compile the manuscript?

```bash
cd paper
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

### Has this been peer-reviewed?

Manuscript is prepared for submission to The Lancet Digital Health (December 2024). Not yet peer-reviewed.

### Can I cite this work?

Yes, cite the Zenodo archive:
```
Laitinen Imanov OY, Kulali DU. Hallucination risks of large language models
in clinical proteomics: a prospective evaluation study. 2024.
DOI: 10.5281/zenodo.11234567
```

---

## Ethics Questions

### Was this study ethically approved?

Yes. DTU Ethics Protocol #2024-DTU-0385, approved February 12, 2024.

### Was it pre-registered?

Yes. OSF pre-registration: osf.io/x7mk9

### Does it comply with GDPR?

Yes. No personal data processed (all data public/synthetic).

---

## Contributing Questions

### How can I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Quick summary:
1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

### What kinds of contributions are welcome?

- Bug fixes
- Documentation improvements
- Test additions
- Code optimizations
- New analysis methods
- Extended evaluations

### Do I need to sign a CLA?

No. Contributions under MIT License (code) and CC-BY 4.0 (data).

---

## Troubleshooting Questions

### Tests are failing

```bash
# Check environment
python --version  # Should be 3.11+
pytest --version

# Run with verbose output
pytest -vv --tb=long

# Check specific test
pytest tests/test_llm_client.py -v
```

### Import errors

```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Or install in development mode
pip install -e .
```

### API calls failing

```bash
# Check API keys
cat .env | grep API_KEY

# Test connection
python -c "import openai; print('OK')"
```

### Out of memory errors

Reduce batch size or use data chunking:
```python
for chunk in pd.read_csv('data.csv', chunksize=1000):
    process(chunk)
```

---

## License Questions

### What license is this under?

- **Code**: MIT License
- **Data**: CC-BY 4.0
- **Manuscript**: Copyright retained by authors

### Can I use this commercially?

Code: Yes (MIT License)
Data: Yes with attribution (CC-BY 4.0)
Manuscript: Contact authors

### Do I need to attribute?

Yes. Please cite our work appropriately (see above).

---

## Contact Questions

### How do I report a bug?

Open GitHub issue: https://github.com/olaflaitinen/llm-proteomics-hallucination/issues

### How do I ask a question?

1. Check this FAQ first
2. Search existing GitHub issues
3. Open new GitHub Discussion
4. Email: olyulaim@dtu.dk (for private matters)

### How quickly will I get a response?

- GitHub issues: Within 7 days
- Pull requests: Within 14 days
- Email: Within 5 business days

---

## Future Plans

### Will you test newer models?

Potentially, if warranted by scientific interest and resources available.

### Will you extend to other domains?

Under consideration: genomics, metabolomics, other omics domains.

### Will you create a web interface?

Possibly, if there is sufficient community interest.

---

## More Questions?

If your question isn't answered here:

1. **Check documentation**: [README.md](README.md), [INSTALLATION.md](INSTALLATION.md), [USAGE.md](USAGE.md)
2. **Search issues**: https://github.com/olaflaitinen/llm-proteomics-hallucination/issues
3. **Open discussion**: https://github.com/olaflaitinen/llm-proteomics-hallucination/discussions
4. **Email**: olyulaim@dtu.dk

---

**Last Updated**: November 9, 2024
**Maintainer**: Olaf Yunus Laitinen Imanov
