#!/usr/bin/env nextflow
/*
 * LLM Proteomics Hallucination Study - Nextflow Pipeline
 *
 * Main workflow for evaluating hallucinations in LLM responses to proteomics queries
 */

nextflow.enable.dsl = 2

// Import modules
include { VALIDATE_QUERIES } from './modules/prepare'
include { SPLIT_DATASET } from './modules/prepare'
include { PREPARE_GROUND_TRUTH } from './modules/prepare'
include { RUN_LLM_EVALUATION } from './modules/llm_eval'
include { VALIDATE_RESPONSES } from './modules/llm_eval'
include { DETECT_HALLUCINATIONS } from './modules/llm_eval'
include { COMPUTE_HALLUCINATION_RATES } from './modules/analysis'
include { STATISTICAL_TESTS } from './modules/analysis'
include { MODEL_COMPARISON } from './modules/analysis'
include { GENERATE_FIGURES } from './modules/visualization'
include { GENERATE_TABLES } from './modules/paper_assets'
include { COMPILE_MANUSCRIPT } from './modules/paper_assets'

// Print pipeline header
log.info """\
    ====================================
    LLM PROTEOMICS HALLUCINATION STUDY
    ====================================
    queries     : ${params.queries}
    models      : ${params.models.join(', ')}
    output_dir  : ${params.output_dir}
    random_seed : ${params.random_seed}
    ====================================
    """
    .stripIndent()

/*
 * Main workflow
 */
workflow {
    // Channel for input queries
    queries_ch = Channel.fromPath(params.queries, checkIfExists: true)

    // Channel for models
    models_ch = Channel.from(params.models)

    // Step 1: Validate and prepare data
    VALIDATE_QUERIES(queries_ch)
    SPLIT_DATASET(queries_ch)
    PREPARE_GROUND_TRUTH()

    // Step 2: Run LLM evaluation for each model
    RUN_LLM_EVALUATION(
        queries_ch.combine(models_ch)
    )

    // Step 3: Validate responses
    VALIDATE_RESPONSES(
        RUN_LLM_EVALUATION.out.responses
    )

    // Step 4: Detect hallucinations
    DETECT_HALLUCINATIONS(
        RUN_LLM_EVALUATION.out.responses,
        PREPARE_GROUND_TRUTH.out.ground_truth
    )

    // Step 5: Statistical analysis
    hallucinations_ch = DETECT_HALLUCINATIONS.out.detections.collect()

    COMPUTE_HALLUCINATION_RATES(hallucinations_ch)

    STATISTICAL_TESTS(
        COMPUTE_HALLUCINATION_RATES.out.rates,
        queries_ch
    )

    MODEL_COMPARISON(
        DETECT_HALLUCINATIONS.out.metrics.collect()
    )

    // Step 6: Generate visualizations
    GENERATE_FIGURES(
        COMPUTE_HALLUCINATION_RATES.out.rates,
        COMPUTE_HALLUCINATION_RATES.out.confidence_intervals,
        STATISTICAL_TESTS.out.chi_square,
        MODEL_COMPARISON.out.comparison
    )

    // Step 7: Generate tables
    GENERATE_TABLES(
        COMPUTE_HALLUCINATION_RATES.out.rates,
        STATISTICAL_TESTS.out.logistic_regression,
        MODEL_COMPARISON.out.comparison
    )

    // Step 8: Compile manuscript
    COMPILE_MANUSCRIPT(
        GENERATE_FIGURES.out.figures.collect(),
        GENERATE_TABLES.out.tables.collect()
    )
}

/*
 * Workflow completion handler
 */
workflow.onComplete {
    log.info """\
        ====================================
        Pipeline execution summary
        ====================================
        Completed at : ${workflow.complete}
        Duration     : ${workflow.duration}
        Success      : ${workflow.success}
        Work Dir     : ${workflow.workDir}
        Exit status  : ${workflow.exitStatus}
        ====================================
        """
        .stripIndent()
}

workflow.onError {
    log.error "Pipeline execution failed!"
    log.error "Error: ${workflow.errorMessage}"
}
