"""
Snakemake rules for bias audit and fairness analysis
"""

rule analyze_domain_bias:
    """Analyze hallucination bias across proteomics domains"""
    input:
        hallucinations = expand("data/results/{model}_hallucinations.json", model=MODELS),
        queries = "data/queries/queries_all.json"
    output:
        domain_analysis = "data/results/domain_bias_analysis.csv",
        chi_square = "data/results/domain_chi_square.csv"
    log:
        "logs/analyze_domain_bias.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/domain_bias.py \
            --hallucinations {input.hallucinations} \
            --queries {input.queries} \
            --output {output.domain_analysis} \
            --chi-square {output.chi_square} \
            2> {log}
        """

rule analyze_complexity_bias:
    """Analyze bias related to query complexity"""
    input:
        hallucinations = "data/results/hallucination_rates.csv",
        queries = "data/queries/queries_all.json"
    output:
        complexity_analysis = "data/results/complexity_bias_analysis.csv",
        odds_ratios = "data/results/complexity_odds_ratios.csv"
    log:
        "logs/analyze_complexity_bias.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/complexity_bias.py \
            --hallucinations {input.hallucinations} \
            --queries {input.queries} \
            --analysis {output.complexity_analysis} \
            --odds-ratios {output.odds_ratios} \
            2> {log}
        """

rule analyze_prevalence_bias:
    """Analyze bias related to disease/protein prevalence"""
    input:
        hallucinations = expand("data/results/{model}_hallucinations.json", model=MODELS),
        queries = "data/queries/queries_all.json"
    output:
        prevalence_analysis = "data/results/prevalence_bias_analysis.csv"
    log:
        "logs/analyze_prevalence_bias.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/prevalence_bias.py \
            --hallucinations {input.hallucinations} \
            --queries {input.queries} \
            --output {output.prevalence_analysis} \
            2> {log}
        """

rule analyze_temporal_consistency:
    """Analyze temporal consistency of LLM responses"""
    input:
        responses = expand("data/llm_responses/{model}_responses.jsonl", model=MODELS)
    output:
        consistency = "data/results/temporal_consistency.csv"
    log:
        "logs/analyze_temporal_consistency.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/temporal_consistency.py \
            --responses {input.responses} \
            --output {output.consistency} \
            2> {log}
        """

rule fairness_metrics:
    """Compute fairness metrics across subgroups"""
    input:
        hallucinations = "data/results/hallucination_rates.csv",
        queries = "data/queries/queries_all.json"
    output:
        fairness = "data/results/fairness_metrics.csv",
        disparities = "data/results/group_disparities.csv"
    log:
        "logs/fairness_metrics.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/fairness.py \
            --hallucinations {input.hallucinations} \
            --queries {input.queries} \
            --fairness {output.fairness} \
            --disparities {output.disparities} \
            2> {log}
        """

rule compile_bias_audit_report:
    """Compile comprehensive bias audit report"""
    input:
        domain = "data/results/domain_bias_analysis.csv",
        complexity = "data/results/complexity_bias_analysis.csv",
        prevalence = "data/results/prevalence_bias_analysis.csv",
        fairness = "data/results/fairness_metrics.csv"
    output:
        report = "data/results/bias_audit_report.json",
        summary = "data/results/bias_summary.csv"
    log:
        "logs/compile_bias_audit_report.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/compile_bias_report.py \
            --domain {input.domain} \
            --complexity {input.complexity} \
            --prevalence {input.prevalence} \
            --fairness {input.fairness} \
            --report {output.report} \
            --summary {output.summary} \
            2> {log}
        """
