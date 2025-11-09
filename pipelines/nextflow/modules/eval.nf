// Nextflow module for LLM evaluation
// Queries LLM APIs and collects responses

process QUERY_LLM {
    tag "$model-$query_batch"
    
    publishDir "${params.outdir}/llm_responses/${model}", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    container "${ workflow.containerEngine == 'docker' ? 'llm-proteomics:latest' : null }"
    
    input:
    tuple val(model), path(query_file), val(query_batch)
    
    output:
    tuple val(model), path("${model}_responses_${query_batch}.jsonl")
    
    script:
    """
    python ${projectDir}/src/llm_eval/run_evaluation.py \\
        --model ${model} \\
        --queries ${query_file} \\
        --output ${model}_responses_${query_batch}.jsonl \\
        --temperature ${params.temperature} \\
        --max_tokens ${params.max_tokens} \\
        --api_key_env ${params.api_key_env}
    """
}

process SCORE_RESPONSES {
    tag "$model"
    
    publishDir "${params.outdir}/scores", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    tuple val(model), path(responses)
    path(ground_truth)
    
    output:
    tuple val(model), path("${model}_scores.csv")
    
    script:
    """
    python ${projectDir}/src/llm_eval/scoring.py \\
        --responses ${responses} \\
        --ground_truth ${ground_truth} \\
        --output ${model}_scores.csv \\
        --metrics hallucination,severity,clinical_safety
    """
}

process CALIBRATION_ANALYSIS {
    tag "$model"
    
    publishDir "${params.outdir}/calibration", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    tuple val(model), path(scores)
    
    output:
    tuple val(model), path("${model}_calibration.json"), path("${model}_calibration_curve.png")
    
    script:
    """
    python ${projectDir}/src/analysis/calibration.py \\
        --scores ${scores} \\
        --output_json ${model}_calibration.json \\
        --output_plot ${model}_calibration_curve.png \\
        --n_bins ${params.calibration_bins}
    """
}

process AGGREGATE_RESULTS {
    publishDir "${params.outdir}/final", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(all_scores)
    path(all_calibration)
    
    output:
    path("model_comparison_metrics.csv")
    path("aggregated_results.json")
    
    script:
    """
    python ${projectDir}/src/analysis/aggregate.py \\
        --scores_dir . \\
        --calibration_dir . \\
        --output_csv model_comparison_metrics.csv \\
        --output_json aggregated_results.json
    """
}

workflow EVALUATE_MODELS {
    take:
    queries_ch
    ground_truth
    
    main:
    // Query all models
    responses_ch = QUERY_LLM(queries_ch)
    
    // Score responses
    scores_ch = SCORE_RESPONSES(responses_ch, ground_truth)
    
    // Calibration analysis
    calibration_ch = CALIBRATION_ANALYSIS(scores_ch)
    
    // Aggregate results
    all_scores = scores_ch.map { model, scores -> scores }.collect()
    all_calibration = calibration_ch.map { model, json, plot -> json }.collect()
    
    AGGREGATE_RESULTS(all_scores, all_calibration)
    
    emit:
    scores = scores_ch
    calibration = calibration_ch
}
