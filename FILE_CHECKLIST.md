# File Status Checklist

**Total Required:** 300  
**Existing:** 84 (✓)  
**Missing:** 216 (✗)  
**Completion:** 28.0%

---

## ✓ Existing Files (84/300)

- [x] .gitattributes
- [x] .gitignore
- [x] ARCHITECTURE.md
- [x] CHANGELOG.md
- [x] CITATION.cff
- [x] CODE_OF_CONDUCT.md
- [x] CONTRIBUTING.md
- [x] LICENSE
- [x] Makefile
- [x] README.md
- [x] ROADMAP.md
- [x] configs/default.yaml
- [x] configs/hydra.yaml
- [x] configs/models/claude_sonnet_3_5.yaml
- [x] configs/models/gpt4_turbo_2024_03.yaml
- [x] configs/pipelines.yaml
- [x] containers/Dockerfile
- [x] containers/docker-compose.yml
- [x] containers/sbom/sbom.spdx.json
- [x] data/README.md
- [x] data/queries/queries_all.json
- [x] data/registry.yaml
- [x] data/results/hallucination_rates.csv
- [x] data/results/model_comparison.csv
- [x] data/schemas/annotation_schema.json
- [x] data/schemas/llm_response_schema.json
- [x] data/schemas/msms_schema.json
- [x] data/schemas/protein_schema.json
- [x] data/schemas/query_schema.json
- [x] environment.yml
- [x] ethics/data_management_plan.md
- [x] ethics/ethics_protocol.md
- [x] literature/bibliography.bib
- [x] literature/reading_list.md
- [x] notebooks/00_setup_and_verification.ipynb
- [x] notebooks/01_data_exploration.ipynb
- [x] notebooks/02_llm_benchmark.ipynb
- [x] notebooks/03_hallucination_analysis.ipynb
- [x] notebooks/04_statistical_analysis.ipynb
- [x] paper/COMPILATION_GUIDE.md
- [x] paper/figures/figure_style.mplstyle
- [x] paper/figures/generate_figure_1.py
- [x] paper/figures/generate_figure_2.py
- [x] paper/figures/generate_figure_3.py
- [x] paper/figures/generate_figure_4.py
- [x] paper/figures/generate_figure_5.py
- [x] paper/figures/generate_figure_6.py
- [x] paper/figures/templates/color_palette.json
- [x] paper/figures/templates/dpi_settings.yaml
- [x] paper/figures/templates/grid_style.yaml
- [x] paper/figures/templates/lancet_fonts.rc
- [x] paper/journal_checklists/CONSORT_extension_AI.md
- [x] paper/journal_checklists/EQUATOR_compliance.md
- [x] paper/latex/macros.tex
- [x] paper/latex/notation.tex
- [x] paper/latex/packages.tex
- [x] paper/latex/references.bib
- [x] paper/manuscript.tex
- [x] paper/tables/make_table_3_domainwise.R
- [x] paper/tables/make_table_4_multivariable.R
- [x] paper/tables/make_table_5_bias_audit.R
- [x] pipelines/nextflow/main.nf
- [x] pipelines/nextflow/modules/analysis.nf
- [x] pipelines/snakemake/Snakefile
- [x] pipelines/snakemake/rules/00_prepare.smk
- [x] pipelines/snakemake/rules/10_llm_eval.smk
- [x] pipelines/snakemake/rules/20_analysis.smk
- [x] pipelines/snakemake/rules/30_visualization.smk
- [x] pipelines/snakemake/rules/40_bias_audit.smk
- [x] pipelines/snakemake/rules/50_paper_assets.smk
- [x] provenance/metadata.json
- [x] pyproject.toml
- [x] requirements.txt
- [x] setup.cfg
- [x] src/__init__.py
- [x] src/analysis/stats_models.py
- [x] src/llm_eval/__init__.py
- [x] src/llm_eval/runner.py
- [x] src/utils/config.py
- [x] src/utils/io.py
- [x] tests/unit/test_hallucination_detector.py
- [x] tests/unit/test_llm_client.py
- [x] tracking/mlflow/config.yaml
- [x] zenodo.json

---

## ✗ Missing Files (216/300)

### ci/github/workflows/
- [ ] ci/github/workflows/codeql.yml
- [ ] ci/github/workflows/docs.yml
- [ ] ci/github/workflows/lint.yml
- [ ] ci/github/workflows/release.yml
- [ ] ci/github/workflows/test.yml

### configs/
- [ ] configs/logging.yaml

### configs/evaluation/
- [ ] configs/evaluation/bias_categories.yaml
- [ ] configs/evaluation/calibration_thresholds.yaml
- [ ] configs/evaluation/query_splits.yaml
- [ ] configs/evaluation/robustness_matrix.yaml
- [ ] configs/evaluation/scoring_rules.yaml

### configs/models/
- [ ] configs/models/gemini_1_5_pro.yaml
- [ ] configs/models/llama3_70b.yaml
- [ ] configs/models/local_vllm.yaml
- [ ] configs/models/mistral_large_2.yaml

### containers/
- [ ] containers/Dockerfile.gpu
- [ ] containers/notebooks_container.Dockerfile
- [ ] containers/readme.md

### containers/sbom/
- [ ] containers/sbom/bom.cyclonedx.xml

### data/
- [ ] data/metadata.json

### data/backup/
- [ ] data/backup/2025-10-20_data_snapshot.tar.gz
- [ ] data/backup/2025-11-01_incremental_backup.tar.gz

### data/generators/
- [ ] data/generators/augment_protein_sequences.py
- [ ] data/generators/generate_synthetic_msms.py
- [ ] data/generators/random_seed_control.py
- [ ] data/generators/simulate_llm_responses.py
- [ ] data/generators/simulate_queries.py
- [ ] data/generators/synthesize_annotations.py

### data/ground_truth/
- [ ] data/ground_truth/adjudicated_labels.json
- [ ] data/ground_truth/annotation_guidelines.pdf
- [ ] data/ground_truth/annotator_metadata.csv
- [ ] data/ground_truth/expert_annotations_round1.json
- [ ] data/ground_truth/expert_annotations_round2.json
- [ ] data/ground_truth/interrater_reliability.csv
- [ ] data/ground_truth/severity_scale.csv

### data/llm_responses/
- [ ] data/llm_responses/claude_sonnet_responses.jsonl
- [ ] data/llm_responses/gemini_pro_responses.jsonl
- [ ] data/llm_responses/gpt4_turbo_responses.jsonl
- [ ] data/llm_responses/human_baseline_answers.jsonl
- [ ] data/llm_responses/llama3_70b_local.jsonl
- [ ] data/llm_responses/mistral_large_responses.jsonl
- [ ] data/llm_responses/model_metadata.yaml
- [ ] data/llm_responses/response_audit_log.csv

### data/mass_spectrometry/
- [ ] data/mass_spectrometry/ms_run_info.yaml
- [ ] data/mass_spectrometry/peptide_identifications.csv
- [ ] data/mass_spectrometry/protein_inference_results.csv
- [ ] data/mass_spectrometry/qc_metrics.json
- [ ] data/mass_spectrometry/spectra_metadata.csv

### data/mass_spectrometry/mzML/
- [ ] data/mass_spectrometry/mzML/patient001_runA.mzML
- [ ] data/mass_spectrometry/mzML/patient002_runA.mzML

### data/mass_spectrometry/raw_msms_files/
- [ ] data/mass_spectrometry/raw_msms_files/blanks_control.mgf
- [ ] data/mass_spectrometry/raw_msms_files/patient001_runA.mgf
- [ ] data/mass_spectrometry/raw_msms_files/patient001_runB.mgf
- [ ] data/mass_spectrometry/raw_msms_files/patient002_runA.mgf
- [ ] data/mass_spectrometry/raw_msms_files/patient002_runB.mgf
- [ ] data/mass_spectrometry/raw_msms_files/reference_mix.mgf

### data/mass_spectrometry/spectra_plots/
- [ ] data/mass_spectrometry/spectra_plots/ms1_chromatogram_patient001.png
- [ ] data/mass_spectrometry/spectra_plots/ms2_fragmentation_patient001.png

### data/proteins/
- [ ] data/proteins/differential_expression.csv
- [ ] data/proteins/go_annotations.csv
- [ ] data/proteins/identified_proteins.csv
- [ ] data/proteins/peptide_sequences.fasta
- [ ] data/proteins/protein_complexes.json
- [ ] data/proteins/protein_domains.json
- [ ] data/proteins/protein_embeddings.h5
- [ ] data/proteins/protein_metadata.yaml
- [ ] data/proteins/ptm_sites.csv

### data/proteins/qc/
- [ ] data/proteins/qc/missing_values_heatmap.png
- [ ] data/proteins/qc/outlier_report.txt
- [ ] data/proteins/qc/qc_metrics.csv

### data/proteins/uniprot_reference/
- [ ] data/proteins/uniprot_reference/human_proteome.fasta
- [ ] data/proteins/uniprot_reference/metadata.txt
- [ ] data/proteins/uniprot_reference/mouse_proteome.fasta
- [ ] data/proteins/uniprot_reference/yeast_proteome.fasta

### data/queries/
- [ ] data/queries/queries_high_complexity.json
- [ ] data/queries/queries_low_complexity.json
- [ ] data/queries/queries_test.json
- [ ] data/queries/queries_train.json
- [ ] data/queries/queries_validation.json
- [ ] data/queries/query_metadata.csv

### data/results/
- [ ] data/results/bayesian_posteriors.csv
- [ ] data/results/bias_metrics.csv
- [ ] data/results/calibration_scores.csv
- [ ] data/results/consistency_matrix.csv
- [ ] data/results/domain_error_profiles.csv
- [ ] data/results/report_combined_results.xlsx
- [ ] data/results/robustness_scores.csv
- [ ] data/results/severity_distribution.csv
- [ ] data/results/summary_statistics.json

### data/schemas/
- [ ] data/schemas/ontology_schema.json
- [ ] data/schemas/qc_schema.json

### data/structured/
- [ ] data/structured/biomarker_list.csv
- [ ] data/structured/disease_categories.csv
- [ ] data/structured/evidence_codes.tsv
- [ ] data/structured/go_terms.csv
- [ ] data/structured/mapping_uniprot_to_go.csv
- [ ] data/structured/ontology.json

### ethics/
- [ ] ethics/data_use_agreement.md
- [ ] ethics/deidentification_procedure.md
- [ ] ethics/reproducibility_statement.md
- [ ] ethics/risk_register.csv
- [ ] ethics/transparency_checklist.md

### ethics/consent_and_irb/
- [ ] ethics/consent_and_irb/IRB_approval.pdf
- [ ] ethics/consent_and_irb/consent_template.docx
- [ ] ethics/consent_and_irb/osf_preregistration.txt
- [ ] ethics/consent_and_irb/participant_information_leaflet.pdf

### literature/
- [ ] literature/bibtex_to_json.py
- [ ] literature/citation_network.graphml
- [ ] literature/notes_on_literature.md
- [ ] literature/related_studies.csv

### notebooks/
- [ ] notebooks/05_calibration_and_ci.ipynb
- [ ] notebooks/06_protein_level_inference.ipynb
- [ ] notebooks/07_msms_validation.ipynb
- [ ] notebooks/08_bias_audit.ipynb
- [ ] notebooks/09_robustness_tests.ipynb
- [ ] notebooks/10_cross_model_agreement.ipynb
- [ ] notebooks/11_bayesian_inference.ipynb
- [ ] notebooks/12_generate_figures.ipynb
- [ ] notebooks/13_reproducibility_report.ipynb
- [ ] notebooks/14_appendix_validation.ipynb

### paper/
- [ ] paper/manuscript.pdf
- [ ] paper/supplementary_material.pdf

### paper/figures/output/
- [ ] paper/figures/output/fig1_hallucination_rate_vs_complexity.png
- [ ] paper/figures/output/fig2_heatmap_severity.png
- [ ] paper/figures/output/fig3_consistency_matrix.png
- [ ] paper/figures/output/fig4_calibration_curve.png
- [ ] paper/figures/output/fig5_domain_breakdown.png
- [ ] paper/figures/output/fig6_bayesian_posterior.png

### paper/figures/output/highres_tiff/
- [ ] paper/figures/output/highres_tiff/fig1_600dpi.tiff
- [ ] paper/figures/output/highres_tiff/fig2_600dpi.tiff
- [ ] paper/figures/output/highres_tiff/fig3_600dpi.tiff

### paper/journal_checklists/
- [ ] paper/journal_checklists/GRRAS_checklist.pdf
- [ ] paper/journal_checklists/Lancet_submission_form.pdf
- [ ] paper/journal_checklists/STARD_checklist.pdf

### paper/latex/
- [ ] paper/latex/lancetdigitalhealth.cls

### paper/tables/
- [ ] paper/tables/figures_from_tables.R
- [ ] paper/tables/make_table_1_summary.R
- [ ] paper/tables/make_table_2_model_perf.R

### paper/tables/outputs/
- [ ] paper/tables/outputs/combined_tables.xlsx
- [ ] paper/tables/outputs/table1_summary.csv
- [ ] paper/tables/outputs/table2_model_perf.csv
- [ ] paper/tables/outputs/table3_domainwise.csv
- [ ] paper/tables/outputs/table4_multivariable.csv
- [ ] paper/tables/outputs/table5_bias_audit.csv

### pipelines/nextflow/modules/
- [ ] pipelines/nextflow/modules/bias_audit.nf
- [ ] pipelines/nextflow/modules/eval.nf
- [ ] pipelines/nextflow/modules/figures.nf

### provenance/
- [ ] provenance/provenance.intoto.jsonl

### provenance/build_logs/
- [ ] provenance/build_logs/run_2025-10-21T12:30.log
- [ ] provenance/build_logs/run_2025-10-21T12:30_summary.json

### provenance/checksums/
- [ ] provenance/checksums/analysis_hashes.txt
- [ ] provenance/checksums/data_hashes.txt
- [ ] provenance/checksums/figures_hashes.txt
- [ ] provenance/checksums/paper_hash.txt

### src/analysis/
- [ ] src/analysis/bayesian_modeling.ipynb
- [ ] src/analysis/calibration.py
- [ ] src/analysis/correlation_network.py
- [ ] src/analysis/effect_size_analysis.R
- [ ] src/analysis/figures.py
- [ ] src/analysis/power_analysis.R

### src/data_processing/
- [ ] src/data_processing/feature_engineering.py
- [ ] src/data_processing/harmonization.py
- [ ] src/data_processing/joiner.py
- [ ] src/data_processing/loaders.py
- [ ] src/data_processing/metadata_parser.py
- [ ] src/data_processing/missing_value_imputation.py
- [ ] src/data_processing/normalization.py
- [ ] src/data_processing/quality_control.py
- [ ] src/data_processing/transforms.py
- [ ] src/data_processing/validators.py

### src/llm_eval/
- [ ] src/llm_eval/cache_backend.py
- [ ] src/llm_eval/calibration.py
- [ ] src/llm_eval/consistency.py
- [ ] src/llm_eval/export.py
- [ ] src/llm_eval/metrics.py
- [ ] src/llm_eval/model_wrappers.py
- [ ] src/llm_eval/prompt_sweeper.py
- [ ] src/llm_eval/robustness.py
- [ ] src/llm_eval/scoring.py

### src/llm_eval/clients/
- [ ] src/llm_eval/clients/anthropic_client.py
- [ ] src/llm_eval/clients/gemini_client.py
- [ ] src/llm_eval/clients/local_vllm_client.py
- [ ] src/llm_eval/clients/mistral_client.py
- [ ] src/llm_eval/clients/openai_client.py

### src/llm_eval/prompts/
- [ ] src/llm_eval/prompts/base_prompt.txt
- [ ] src/llm_eval/prompts/clinical_safety_prompt.txt
- [ ] src/llm_eval/prompts/hallucination_detection_prompt.txt
- [ ] src/llm_eval/prompts/prompt_metadata.yaml
- [ ] src/llm_eval/prompts/proteomics_prompt_v1.txt
- [ ] src/llm_eval/prompts/stress_test_prompts.md

### src/utils/
- [ ] src/utils/decorators.py
- [ ] src/utils/logging.py
- [ ] src/utils/seeds.py
- [ ] src/utils/timer.py
- [ ] src/utils/visualization.py

### tests/data_quality/
- [ ] tests/data_quality/test_annotations_consistency.py
- [ ] tests/data_quality/test_llm_responses_format.py
- [ ] tests/data_quality/test_msms_qc.py
- [ ] tests/data_quality/test_protein_metadata.py
- [ ] tests/data_quality/test_queries_schema.py
- [ ] tests/data_quality/test_results_contracts.py

### tests/integration/
- [ ] tests/integration/test_end_to_end.py
- [ ] tests/integration/test_pipeline_makefile.py
- [ ] tests/integration/test_snakefile_rules.py

### tests/unit/
- [ ] tests/unit/test_calibration.py
- [ ] tests/unit/test_metrics.py
- [ ] tests/unit/test_reproducibility.py
- [ ] tests/unit/test_schemas.py
- [ ] tests/unit/test_transformations.py

### tracking/mlflow/
- [ ] tracking/mlflow/README.md
- [ ] tracking/mlflow/experiments.db

### tracking/mlflow/server/
- [ ] tracking/mlflow/server/Dockerfile
- [ ] tracking/mlflow/server/app.py

### tracking/wandb/
- [ ] tracking/wandb/README.md
- [ ] tracking/wandb/config.yaml
- [ ] tracking/wandb/credentials_template.yaml

