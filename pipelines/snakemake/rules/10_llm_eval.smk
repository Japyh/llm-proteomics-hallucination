"""
Snakemake rules for LLM evaluation
"""

MODELS = ["gpt4_turbo", "claude_sonnet", "gemini_pro"]

rule run_llm_evaluation:
    """Run LLM evaluation for a specific model"""
    input:
        queries = "data/queries/queries_all.json",
        config = "configs/models/{model}_config.yaml"
    output:
        responses = "data/llm_responses/{model}_responses.jsonl",
        metadata = "data/llm_responses/{model}_metadata.json"
    params:
        model_name = lambda wildcards: wildcards.model
    log:
        "logs/llm_eval_{model}.log"
    conda:
        "../envs/llm_evaluation.yaml"
    resources:
        api_calls = 1  # Limit concurrent API calls
    shell:
        """
        python src/llm_evaluation/runner.py \
            --queries {input.queries} \
            --config {input.config} \
            --output {output.responses} \
            --metadata {output.metadata} \
            --model {params.model_name} \
            2> {log}
        """

rule validate_llm_responses:
    """Validate LLM responses against schema"""
    input:
        responses = "data/llm_responses/{model}_responses.jsonl",
        schema = "data/schemas/llm_response_schema.json"
    output:
        report = "data/qc/{model}_response_validation.json"
    log:
        "logs/validate_responses_{model}.log"
    conda:
        "../envs/data_processing.yaml"
    shell:
        """
        python scripts/validate_responses.py \
            --input {input.responses} \
            --schema {input.schema} \
            --output {output.report} \
            2> {log}
        """

rule aggregate_llm_responses:
    """Aggregate responses from all models"""
    input:
        expand("data/llm_responses/{model}_responses.jsonl", model=MODELS)
    output:
        aggregated = "data/llm_responses/all_responses.jsonl",
        summary = "data/llm_responses/response_summary.csv"
    log:
        "logs/aggregate_responses.log"
    conda:
        "../envs/data_processing.yaml"
    shell:
        """
        python scripts/aggregate_responses.py \
            --inputs {input} \
            --output {output.aggregated} \
            --summary {output.summary} \
            2> {log}
        """

rule detect_hallucinations:
    """Detect hallucinations by comparing responses to ground truth"""
    input:
        responses = "data/llm_responses/{model}_responses.jsonl",
        ground_truth = "data/annotations/ground_truth_validated.json"
    output:
        detections = "data/results/{model}_hallucinations.json",
        metrics = "data/results/{model}_metrics.json"
    log:
        "logs/detect_hallucinations_{model}.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/hallucination_detector.py \
            --responses {input.responses} \
            --ground-truth {input.ground_truth} \
            --detections {output.detections} \
            --metrics {output.metrics} \
            2> {log}
        """

rule compute_inter_rater_reliability:
    """Compute Cohen's kappa for inter-rater reliability"""
    input:
        rater1 = "data/annotations/rater1_annotations.json",
        rater2 = "data/annotations/rater2_annotations.json"
    output:
        kappa = "data/results/inter_rater_kappa.json"
    log:
        "logs/inter_rater_reliability.log"
    conda:
        "../envs/analysis.yaml"
    shell:
        """
        python src/analysis/compute_kappa.py \
            --rater1 {input.rater1} \
            --rater2 {input.rater2} \
            --output {output.kappa} \
            2> {log}
        """
