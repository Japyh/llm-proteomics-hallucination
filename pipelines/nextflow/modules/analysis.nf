/*
 * Nextflow modules for statistical analysis
 */

process COMPUTE_HALLUCINATION_RATES {
    tag "hallucination_rates"
    label 'medium_compute'
    publishDir "${params.output_dir}/results", mode: 'copy'

    input:
    path hallucinations

    output:
    path "hallucination_rates.csv", emit: rates
    path "confidence_intervals.csv", emit: confidence_intervals

    script:
    """
    python ${projectDir}/../../src/analysis/compute_rates.py \
        --inputs ${hallucinations} \
        --rates hallucination_rates.csv \
        --confidence-intervals confidence_intervals.csv \
        --confidence-level ${params.confidence_level} \
        --n-bootstrap ${params.n_bootstrap}
    """
}

process STATISTICAL_TESTS {
    tag "statistical_tests"
    label 'medium_compute'
    publishDir "${params.output_dir}/results", mode: 'copy'

    input:
    path hallucinations
    path queries

    output:
    path "chi_square_tests.csv", emit: chi_square
    path "logistic_regression.csv", emit: logistic_regression
    path "bonferroni_correction.csv", emit: bonferroni

    script:
    """
    python ${projectDir}/../../src/analysis/statistical_tests.py \
        --hallucinations ${hallucinations} \
        --queries ${queries} \
        --chi-square chi_square_tests.csv \
        --logistic-regression logistic_regression.csv \
        --bonferroni bonferroni_correction.csv
    """
}

process MODEL_COMPARISON {
    tag "model_comparison"
    label 'medium_compute'
    publishDir "${params.output_dir}/results", mode: 'copy'

    input:
    path metrics

    output:
    path "model_comparison.csv", emit: comparison
    path "pairwise_comparisons.csv", emit: pairwise

    script:
    """
    python ${projectDir}/../../src/analysis/compare_models.py \
        --inputs ${metrics} \
        --comparison model_comparison.csv \
        --pairwise pairwise_comparisons.csv
    """
}
