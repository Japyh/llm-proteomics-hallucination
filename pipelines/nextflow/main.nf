#!/usr/bin/env nextflow

params.queries = "data/queries/queries_all.json"
params.models = ["gpt4", "claude", "gemini"]
params.output = "results/"

process evaluateLLM {
    publishDir "${params.output}/llm_responses", mode: 'copy'
    
    input:
    val model
    
    output:
    path "${model}_responses.jsonl"
    
    script:
    """
    python src/llm_eval/runner.py --model ${model} --input ${params.queries} --output ${model}_responses.jsonl
    """
}

process analyzeResults {
    publishDir "${params.output}", mode: 'copy'
    
    input:
    path responses
    
    output:
    path "hallucination_rates.csv"
    
    script:
    """
    python src/analysis/stats_models.py --input ${responses} --output hallucination_rates.csv
    """
}

workflow {
    models = Channel.fromList(params.models)
    responses = evaluateLLM(models)
    analyzeResults(responses.collect())
}
