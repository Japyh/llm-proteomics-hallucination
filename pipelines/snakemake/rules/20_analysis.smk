"""
Snakemake rules for statistical analysis
"""

rule compute_hallucination_rates:
    """Compute overall and per-model hallucination rates"""
    input:
        detections = expand("data/results/{model}_hallucinations.json", model=MODELS)
    output:
        rates = "data/results/hallucination_rates.csv",
        confidence_intervals = "data/results/confidence_intervals.csv"
    params:
        confidence_level = config.get("evaluation", {}).get("confidence_level", 0.95),
        n_bootstrap = config.get("evaluation", {}).get("n_bootstrap", 1000)
    log:
        "logs/compute_hallucination_rates.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/compute_rates.py \
            --inputs {input.detections} \
            --rates {output.rates} \
            --confidence-intervals {output.confidence_intervals} \
            --confidence-level {params.confidence_level} \
            --n-bootstrap {params.n_bootstrap} \
            2> {log}
        """

rule statistical_tests:
    """Run statistical tests (chi-square, logistic regression)"""
    input:
        hallucinations = "data/results/hallucination_rates.csv",
        queries = "data/queries/queries_all.json"
    output:
        chi_square = "data/results/chi_square_tests.csv",
        logistic_regression = "data/results/logistic_regression.csv",
        bonferroni = "data/results/bonferroni_correction.csv"
    log:
        "logs/statistical_tests.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/statistical_tests.py \
            --hallucinations {input.hallucinations} \
            --queries {input.queries} \
            --chi-square {output.chi_square} \
            --logistic-regression {output.logistic_regression} \
            --bonferroni {output.bonferroni} \
            2> {log}
        """

rule model_comparison:
    """Compare performance across models"""
    input:
        metrics = expand("data/results/{model}_metrics.json", model=MODELS)
    output:
        comparison = "data/results/model_comparison.csv",
        pairwise = "data/results/pairwise_comparisons.csv"
    log:
        "logs/model_comparison.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/compare_models.py \
            --inputs {input.metrics} \
            --comparison {output.comparison} \
            --pairwise {output.pairwise} \
            2> {log}
        """

rule severity_classification:
    """Classify hallucinations by severity"""
    input:
        hallucinations = expand("data/results/{model}_hallucinations.json", model=MODELS)
    output:
        classifications = "data/results/severity_classifications.csv",
        distribution = "data/results/severity_distribution.csv"
    log:
        "logs/severity_classification.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/classify_severity.py \
            --inputs {input.hallucinations} \
            --classifications {output.classifications} \
            --distribution {output.distribution} \
            2> {log}
        """

rule calibration_analysis:
    """Analyze model calibration and confidence"""
    input:
        responses = expand("data/llm_responses/{model}_responses.jsonl", model=MODELS),
        ground_truth = "data/annotations/ground_truth_validated.json"
    output:
        calibration = "data/results/calibration_curves.csv",
        ece = "data/results/expected_calibration_error.csv"
    log:
        "logs/calibration_analysis.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/calibration.py \
            --responses {input.responses} \
            --ground-truth {input.ground_truth} \
            --calibration {output.calibration} \
            --ece {output.ece} \
            2> {log}
        """

rule compile_statistical_report:
    """Compile comprehensive statistical analysis report"""
    input:
        rates = "data/results/hallucination_rates.csv",
        chi_square = "data/results/chi_square_tests.csv",
        logistic = "data/results/logistic_regression.csv",
        comparison = "data/results/model_comparison.csv",
        severity = "data/results/severity_classifications.csv"
    output:
        report = "data/results/statistical_analysis.csv",
        summary = "data/results/analysis_summary.json"
    log:
        "logs/compile_statistical_report.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/compile_report.py \
            --rates {input.rates} \
            --chi-square {input.chi_square} \
            --logistic {input.logistic} \
            --comparison {input.comparison} \
            --severity {input.severity} \
            --report {output.report} \
            --summary {output.summary} \
            2> {log}
        """
