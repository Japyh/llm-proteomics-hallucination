/*
 * Nextflow modules for paper asset generation
 */

process GENERATE_TABLES {
    tag "generate_tables"
    label 'low_compute'
    publishDir "${params.output_dir}/../paper/tables/outputs", mode: 'copy'

    input:
    path rates
    path logistic_regression
    path comparison

    output:
    path "table_*.csv", emit: tables
    path "table_*.tex", emit: latex_tables

    script:
    """
    # Table 1: Baseline characteristics
    Rscript ${projectDir}/../../paper/tables/generate_table_1.R \
        --queries ${projectDir}/../../data/queries/queries_all.json \
        --responses ${projectDir}/../../data/llm_responses/all_responses.jsonl \
        --output-csv table_1_baseline.csv \
        --output-latex table_1_baseline.tex

    # Table 2: Hallucination rates
    Rscript ${projectDir}/../../paper/tables/generate_table_2.R \
        --rates ${rates} \
        --confidence-intervals ${projectDir}/../../data/results/confidence_intervals.csv \
        --output-csv table_2_hallucination_rates.csv \
        --output-latex table_2_hallucination_rates.tex

    # Table 3: Statistical tests
    Rscript ${projectDir}/../../paper/tables/generate_table_3.R \
        --chi-square ${projectDir}/../../data/results/chi_square_tests.csv \
        --logistic ${logistic_regression} \
        --bonferroni ${projectDir}/../../data/results/bonferroni_correction.csv \
        --output-csv table_3_statistical_tests.csv \
        --output-latex table_3_statistical_tests.tex
    """
}

process COMPILE_MANUSCRIPT {
    tag "compile_manuscript"
    label 'low_compute'
    publishDir "${params.output_dir}/../paper", mode: 'copy'

    input:
    path figures
    path tables

    output:
    path "manuscript.pdf", emit: manuscript

    script:
    """
    cd ${projectDir}/../../paper
    pdflatex manuscript.tex
    bibtex manuscript
    pdflatex manuscript.tex
    pdflatex manuscript.tex
    cp manuscript.pdf ${params.output_dir}/../paper/
    """
}
