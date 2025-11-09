"""
Snakemake rules for generating paper assets (tables, supplementary materials)
"""

rule generate_table_1:
    """Generate Table 1: Baseline characteristics"""
    input:
        queries = "data/queries/queries_all.json",
        responses = "data/llm_responses/all_responses.jsonl"
    output:
        table = "paper/tables/outputs/table_1_baseline.csv",
        latex = "paper/tables/outputs/table_1_baseline.tex"
    log:
        "logs/generate_table_1.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        Rscript paper/tables/generate_table_1.R \
            --queries {input.queries} \
            --responses {input.responses} \
            --output-csv {output.table} \
            --output-latex {output.latex} \
            2> {log}
        """

rule generate_table_2:
    """Generate Table 2: Hallucination rates by model"""
    input:
        rates = "data/results/hallucination_rates.csv",
        ci = "data/results/confidence_intervals.csv"
    output:
        table = "paper/tables/outputs/table_2_hallucination_rates.csv",
        latex = "paper/tables/outputs/table_2_hallucination_rates.tex"
    log:
        "logs/generate_table_2.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        Rscript paper/tables/generate_table_2.R \
            --rates {input.rates} \
            --confidence-intervals {input.ci} \
            --output-csv {output.table} \
            --output-latex {output.latex} \
            2> {log}
        """

rule generate_table_3:
    """Generate Table 3: Statistical test results"""
    input:
        chi_square = "data/results/chi_square_tests.csv",
        logistic = "data/results/logistic_regression.csv",
        bonferroni = "data/results/bonferroni_correction.csv"
    output:
        table = "paper/tables/outputs/table_3_statistical_tests.csv",
        latex = "paper/tables/outputs/table_3_statistical_tests.tex"
    log:
        "logs/generate_table_3.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        Rscript paper/tables/generate_table_3.R \
            --chi-square {input.chi_square} \
            --logistic {input.logistic} \
            --bonferroni {input.bonferroni} \
            --output-csv {output.table} \
            --output-latex {output.latex} \
            2> {log}
        """

rule generate_supplementary_tables:
    """Generate supplementary tables"""
    input:
        severity = "data/results/severity_classifications.csv",
        comparison = "data/results/model_comparison.csv",
        calibration = "data/results/calibration_curves.csv"
    output:
        severity_table = "paper/tables/outputs/supplementary_table_1_severity.csv",
        comparison_table = "paper/tables/outputs/supplementary_table_2_comparison.csv",
        calibration_table = "paper/tables/outputs/supplementary_table_3_calibration.csv"
    log:
        "logs/generate_supplementary_tables.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        Rscript paper/tables/generate_supplementary_tables.R \
            --severity {input.severity} \
            --comparison {input.comparison} \
            --calibration {input.calibration} \
            --severity-output {output.severity_table} \
            --comparison-output {output.comparison_table} \
            --calibration-output {output.calibration_table} \
            2> {log}
        """

rule compile_supplementary_materials:
    """Compile supplementary materials PDF"""
    input:
        figures = expand("paper/figures/output/supplementary_figure_{n}*.pdf", n=[1, 2]),
        tables = expand("paper/tables/outputs/supplementary_table_{n}*.csv", n=[1, 2, 3]),
        methods = "paper/supplementary/extended_methods.tex"
    output:
        pdf = "paper/supplementary_materials.pdf"
    log:
        "logs/compile_supplementary_materials.log"
    conda:
        "../envs/latex.yaml"
    shell:
        """
        cd paper && \
        pdflatex supplementary_materials.tex && \
        pdflatex supplementary_materials.tex && \
        mv supplementary_materials.pdf ../{output.pdf} \
        2> ../{log}
        """

rule compile_manuscript:
    """Compile main manuscript PDF"""
    input:
        main = "paper/manuscript.tex",
        figures = expand("paper/figures/output/figure_{n}*.pdf", n=[1, 2, 3, 4]),
        tables = expand("paper/tables/outputs/table_{n}*.tex", n=[1, 2, 3]),
        references = "paper/references.bib"
    output:
        pdf = "paper/manuscript.pdf"
    log:
        "logs/compile_manuscript.log"
    conda:
        "../envs/latex.yaml"
    shell:
        """
        cd paper && \
        pdflatex manuscript.tex && \
        bibtex manuscript && \
        pdflatex manuscript.tex && \
        pdflatex manuscript.tex && \
        mv manuscript.pdf ../{output.pdf} \
        2> ../{log}
        """

rule create_submission_package:
    """Create complete submission package for journal"""
    input:
        manuscript = "paper/manuscript.pdf",
        supplementary = "paper/supplementary_materials.pdf",
        figures = expand("paper/figures/output/highres_tiff/figure_{n}.tiff", n=[1, 2, 3, 4]),
        tables = expand("paper/tables/outputs/table_{n}*.csv", n=[1, 2, 3]),
        cover_letter = "paper/submission/cover_letter.pdf"
    output:
        archive = "paper/submission/lancet_digital_health_submission.zip"
    log:
        "logs/create_submission_package.log"
    shell:
        """
        cd paper/submission && \
        zip -r lancet_digital_health_submission.zip \
            ../manuscript.pdf \
            ../supplementary_materials.pdf \
            ../figures/output/highres_tiff/*.tiff \
            ../tables/outputs/*.csv \
            cover_letter.pdf \
            checklist_lancet.pdf \
            author_declaration.pdf \
        2> ../../{log}
        """
