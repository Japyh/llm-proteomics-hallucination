// Nextflow module for publication figure generation
// Creates high-resolution figures for The Lancet Digital Health

process FIGURE_1_HALLUCINATION_RATES {
    publishDir "${params.outdir}/figures", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(model_metrics)
    
    output:
    path("fig1_hallucination_rate_vs_complexity.png")
    path("fig1_hallucination_rate_vs_complexity_600dpi.tiff")
    
    script:
    """
    python ${projectDir}/src/analysis/figures.py \\
        --figure_type hallucination_rates \\
        --data ${model_metrics} \\
        --output_png fig1_hallucination_rate_vs_complexity.png \\
        --output_tiff fig1_hallucination_rate_vs_complexity_600dpi.tiff \\
        --dpi 600 \\
        --style lancet
    """
}

process FIGURE_2_SEVERITY_HEATMAP {
    publishDir "${params.outdir}/figures", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(domain_breakdown)
    
    output:
    path("fig2_heatmap_severity.png")
    
    script:
    """
    python ${projectDir}/src/analysis/figures.py \\
        --figure_type severity_heatmap \\
        --data ${domain_breakdown} \\
        --output_png fig2_heatmap_severity.png \\
        --dpi 600 \\
        --style lancet
    """
}

process FIGURE_3_CONFUSION_MATRIX {
    publishDir "${params.outdir}/figures", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(scores)
    
    output:
    path("fig3_confusion_matrix.png")
    
    script:
    """
    python ${projectDir}/src/analysis/figures.py \\
        --figure_type confusion_matrix \\
        --data ${scores} \\
        --output_png fig3_confusion_matrix.png \\
        --dpi 600 \\
        --style lancet
    """
}

process FIGURE_4_CALIBRATION_CURVES {
    publishDir "${params.outdir}/figures", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(calibration_data)
    
    output:
    path("fig4_calibration_curve.png")
    path("fig4_calibration_curve_600dpi.tiff")
    
    script:
    """
    python ${projectDir}/src/analysis/figures.py \\
        --figure_type calibration_curves \\
        --data ${calibration_data} \\
        --output_png fig4_calibration_curve.png \\
        --output_tiff fig4_calibration_curve_600dpi.tiff \\
        --dpi 600 \\
        --style lancet
    """
}

process FIGURE_5_DOMAIN_BREAKDOWN {
    publishDir "${params.outdir}/figures", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(domain_data)
    
    output:
    path("fig5_domain_breakdown.png")
    path("fig5_domain_breakdown_600dpi.tiff")
    
    script:
    """
    python ${projectDir}/src/analysis/figures.py \\
        --figure_type domain_breakdown \\
        --data ${domain_data} \\
        --output_png fig5_domain_breakdown.png \\
        --output_tiff fig5_domain_breakdown_600dpi.tiff \\
        --dpi 600 \\
        --style lancet
    """
}

process FIGURE_6_ROBUSTNESS {
    publishDir "${params.outdir}/figures", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(robustness_data)
    
    output:
    path("fig6_robustness_analysis.png")
    
    script:
    """
    python ${projectDir}/src/analysis/figures.py \\
        --figure_type robustness \\
        --data ${robustness_data} \\
        --output_png fig6_robustness_analysis.png \\
        --dpi 600 \\
        --style lancet
    """
}

process SUPPLEMENTARY_FIGURES {
    publishDir "${params.outdir}/figures/supplementary", mode: 'copy'
    
    conda "${projectDir}/conda_env.yaml"
    
    input:
    path(all_data)
    
    output:
    path("supplementary_*.png")
    
    script:
    """
    Rscript ${projectDir}/paper/tables/figures_from_tables.R \\
        --data ${all_data} \\
        --output_dir .
    """
}

process CONVERT_TO_HIGHRES_TIFF {
    publishDir "${params.outdir}/figures/highres_tiff", mode: 'copy'
    
    container 'biocontainers/imagemagick:v7.0.11-0-deb_cv1'
    
    input:
    path(png_figure)
    
    output:
    path("${png_figure.baseName}_600dpi.tiff")
    
    script:
    """
    convert ${png_figure} \\
        -density 600 \\
        -compress lzw \\
        ${png_figure.baseName}_600dpi.tiff
    """
}

workflow GENERATE_FIGURES {
    take:
    model_metrics
    domain_data
    calibration_data
    scores
    robustness_data
    
    main:
    // Main manuscript figures
    fig1 = FIGURE_1_HALLUCINATION_RATES(model_metrics)
    fig2 = FIGURE_2_SEVERITY_HEATMAP(domain_data)
    fig3 = FIGURE_3_CONFUSION_MATRIX(scores)
    fig4 = FIGURE_4_CALIBRATION_CURVES(calibration_data)
    fig5 = FIGURE_5_DOMAIN_BREAKDOWN(domain_data)
    fig6 = FIGURE_6_ROBUSTNESS(robustness_data)
    
    // Supplementary figures
    all_data = model_metrics.mix(domain_data, calibration_data, scores).collect()
    supp_figs = SUPPLEMENTARY_FIGURES(all_data)
    
    emit:
    main_figures = fig1.mix(fig2, fig3, fig4, fig5, fig6)
    supplementary = supp_figs
}
