/*
 * Nextflow modules for visualization
 */

process GENERATE_FIGURES {
    tag "generate_figures"
    label 'medium_compute'
    publishDir "${params.output_dir}/../paper/figures/output", mode: 'copy'

    input:
    path rates
    path confidence_intervals
    path chi_square
    path comparison

    output:
    path "figure_*.pdf", emit: figures
    path "highres_tiff/*.tiff", emit: highres

    script:
    """
    mkdir -p highres_tiff

    # Figure 1: Study flow diagram
    python ${projectDir}/../../paper/figures/generate_figure_1.py \
        --queries ${projectDir}/../../data/queries/queries_all.json \
        --responses ${projectDir}/../../data/llm_responses/all_responses.jsonl \
        --output figure_1_study_flow.pdf \
        --highres highres_tiff/figure_1.tiff

    # Figure 2: Hallucination rates
    python ${projectDir}/../../paper/figures/generate_figure_2.py \
        --rates ${rates} \
        --confidence-intervals ${confidence_intervals} \
        --output figure_2_hallucination_rates.pdf \
        --highres highres_tiff/figure_2.tiff

    # Figure 3: Complexity analysis
    python ${projectDir}/../../paper/figures/generate_figure_3.py \
        --hallucinations ${rates} \
        --queries ${projectDir}/../../data/queries/queries_all.json \
        --output figure_3_complexity_analysis.pdf \
        --highres highres_tiff/figure_3.tiff

    # Figure 4: Model calibration
    python ${projectDir}/../../paper/figures/generate_figure_4.py \
        --calibration ${projectDir}/../../data/results/calibration_curves.csv \
        --ece ${projectDir}/../../data/results/expected_calibration_error.csv \
        --output figure_4_calibration.pdf \
        --highres highres_tiff/figure_4.tiff
    """
}
