"""
Snakemake rules for figure generation
"""

rule generate_figure_1:
    """Generate Figure 1: Study flow diagram"""
    input:
        queries = "data/queries/queries_all.json",
        responses = "data/llm_responses/all_responses.jsonl"
    output:
        figure = "paper/figures/output/figure_1_study_flow.pdf",
        highres = "paper/figures/output/highres_tiff/figure_1.tiff"
    log:
        "logs/generate_figure_1.log"
    conda:
        "../envs/visualization.yaml"
    shell:
        """
        python paper/figures/generate_figure_1.py \
            --queries {input.queries} \
            --responses {input.responses} \
            --output {output.figure} \
            --highres {output.highres} \
            2> {log}
        """

rule generate_figure_2:
    """Generate Figure 2: Hallucination rates by model"""
    input:
        rates = "data/results/hallucination_rates.csv",
        ci = "data/results/confidence_intervals.csv"
    output:
        figure = "paper/figures/output/figure_2_hallucination_rates.pdf",
        highres = "paper/figures/output/highres_tiff/figure_2.tiff"
    log:
        "logs/generate_figure_2.log"
    conda:
        "../envs/visualization.yaml"
    shell:
        """
        python paper/figures/generate_figure_2.py \
            --rates {input.rates} \
            --confidence-intervals {input.ci} \
            --output {output.figure} \
            --highres {output.highres} \
            2> {log}
        """

rule generate_figure_3:
    """Generate Figure 3: Hallucination rates by query complexity"""
    input:
        hallucinations = "data/results/hallucination_rates.csv",
        queries = "data/queries/queries_all.json"
    output:
        figure = "paper/figures/output/figure_3_complexity_analysis.pdf",
        highres = "paper/figures/output/highres_tiff/figure_3.tiff"
    log:
        "logs/generate_figure_3.log"
    conda:
        "../envs/visualization.yaml"
    shell:
        """
        python paper/figures/generate_figure_3.py \
            --hallucinations {input.hallucinations} \
            --queries {input.queries} \
            --output {output.figure} \
            --highres {output.highres} \
            2> {log}
        """

rule generate_figure_4:
    """Generate Figure 4: Model calibration curves"""
    input:
        calibration = "data/results/calibration_curves.csv",
        ece = "data/results/expected_calibration_error.csv"
    output:
        figure = "paper/figures/output/figure_4_calibration.pdf",
        highres = "paper/figures/output/highres_tiff/figure_4.tiff"
    log:
        "logs/generate_figure_4.log"
    conda:
        "../envs/visualization.yaml"
    shell:
        """
        python paper/figures/generate_figure_4.py \
            --calibration {input.calibration} \
            --ece {input.ece} \
            --output {output.figure} \
            --highres {output.highres} \
            2> {log}
        """

rule generate_supplementary_figures:
    """Generate supplementary figures"""
    input:
        severity = "data/results/severity_classifications.csv",
        pairwise = "data/results/pairwise_comparisons.csv"
    output:
        severity_fig = "paper/figures/output/supplementary_figure_1_severity.pdf",
        pairwise_fig = "paper/figures/output/supplementary_figure_2_pairwise.pdf"
    log:
        "logs/generate_supplementary_figures.log"
    conda:
        "../envs/visualization.yaml"
    shell:
        """
        python paper/figures/generate_supplementary_figures.py \
            --severity {input.severity} \
            --pairwise {input.pairwise} \
            --severity-output {output.severity_fig} \
            --pairwise-output {output.pairwise_fig} \
            2> {log}
        """

rule compile_all_figures:
    """Compile all figures for manuscript"""
    input:
        expand("paper/figures/output/figure_{n}*.pdf", n=[1, 2, 3, 4]),
        expand("paper/figures/output/supplementary_figure_{n}*.pdf", n=[1, 2])
    output:
        manifest = "paper/figures/figure_manifest.json"
    log:
        "logs/compile_all_figures.log"
    shell:
        """
        echo "Compiling figure manifest..." > {log}
        python -c "
import json
import os
figures = {os.path.basename(f): os.path.getsize(f) for f in {input!r}}
with open('{output.manifest}', 'w') as out:
    json.dump({{'figures': figures, 'count': len(figures)}}, out, indent=2)
        " 2>> {log}
        """
