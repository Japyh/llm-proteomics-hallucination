// Nextflow module for bias and fairness auditing
// Analyzes systematic biases in LLM hallucinations

process DOMAIN_BIAS_ANALYSIS {
    tag "$model"
    
    publishDir "${params.outdir}/bias/domain", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    tuple val(model), path(scores)
    
    output:
    tuple val(model), path("${model}_domain_bias.csv"), path("${model}_domain_bias.png")
    
    script:
    """
    python ${projectDir}/src/analysis/bias_audit.py \\
        --scores ${scores} \\
        --bias_type domain \\
        --output_csv ${model}_domain_bias.csv \\
        --output_plot ${model}_domain_bias.png \\
        --statistical_test chi_square
    """
}

process COMPLEXITY_BIAS_ANALYSIS {
    tag "$model"
    
    publishDir "${params.outdir}/bias/complexity", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    tuple val(model), path(scores)
    
    output:
    tuple val(model), path("${model}_complexity_bias.csv"), path("${model}_complexity_trend.png")
    
    script:
    """
    python ${projectDir}/src/analysis/bias_audit.py \\
        --scores ${scores} \\
        --bias_type complexity \\
        --output_csv ${model}_complexity_bias.csv \\
        --output_plot ${model}_complexity_trend.png \\
        --statistical_test cochran_armitage
    """
}

process SUBGROUP_FAIRNESS {
    tag "$model"
    
    publishDir "${params.outdir}/bias/fairness", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    tuple val(model), path(scores)
    
    output:
    tuple val(model), path("${model}_fairness_metrics.json")
    
    script:
    """
    python ${projectDir}/src/analysis/fairness.py \\
        --scores ${scores} \\
        --subgroups ${params.fairness_subgroups} \\
        --output ${model}_fairness_metrics.json \\
        --metrics demographic_parity,equalized_odds,calibration_by_group
    """
}

process SYSTEMATIC_ERROR_PATTERNS {
    tag "$model"
    
    publishDir "${params.outdir}/bias/error_patterns", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    tuple val(model), path(responses)
    path(ground_truth)
    
    output:
    tuple val(model), path("${model}_error_patterns.json"), path("${model}_error_heatmap.png")
    
    script:
    """
    python ${projectDir}/src/analysis/error_patterns.py \\
        --responses ${responses} \\
        --ground_truth ${ground_truth} \\
        --output_json ${model}_error_patterns.json \\
        --output_plot ${model}_error_heatmap.png \\
        --pattern_types fabrication,omission,contradiction,misattribution
    """
}

process AGGREGATE_BIAS_REPORT {
    publishDir "${params.outdir}/bias/reports", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(domain_bias)
    path(complexity_bias)
    path(fairness_metrics)
    path(error_patterns)
    
    output:
    path("bias_audit_summary.html")
    path("bias_audit_summary.pdf")
    path("bias_audit_data.json")
    
    script:
    """
    Rscript ${projectDir}/src/analysis/generate_bias_report.R \\
        --domain_bias ${domain_bias} \\
        --complexity_bias ${complexity_bias} \\
        --fairness ${fairness_metrics} \\
        --error_patterns ${error_patterns} \\
        --output_html bias_audit_summary.html \\
        --output_pdf bias_audit_summary.pdf \\
        --output_json bias_audit_data.json
    """
}

workflow BIAS_AUDIT {
    take:
    scores_ch
    responses_ch
    ground_truth
    
    main:
    // Domain bias analysis
    domain_bias_ch = DOMAIN_BIAS_ANALYSIS(scores_ch)
    
    // Complexity bias analysis
    complexity_bias_ch = COMPLEXITY_BIAS_ANALYSIS(scores_ch)
    
    // Fairness metrics
    fairness_ch = SUBGROUP_FAIRNESS(scores_ch)
    
    // Error pattern analysis
    error_patterns_ch = SYSTEMATIC_ERROR_PATTERNS(responses_ch, ground_truth)
    
    // Aggregate into report
    all_domain = domain_bias_ch.map { model, csv, plot -> csv }.collect()
    all_complexity = complexity_bias_ch.map { model, csv, plot -> csv }.collect()
    all_fairness = fairness_ch.map { model, json -> json }.collect()
    all_errors = error_patterns_ch.map { model, json, plot -> json }.collect()
    
    AGGREGATE_BIAS_REPORT(all_domain, all_complexity, all_fairness, all_errors)
    
    emit:
    domain_bias = domain_bias_ch
    complexity_bias = complexity_bias_ch
    fairness = fairness_ch
    error_patterns = error_patterns_ch
}
