/*
 * Nextflow modules for LLM evaluation
 */

process RUN_LLM_EVALUATION {
    tag "${model}"
    label 'api_call'
    publishDir "${params.output_dir}/llm_responses", mode: 'copy'

    input:
    tuple path(queries), val(model)

    output:
    path "${model}_responses.jsonl", emit: responses
    path "${model}_metadata.json", emit: metadata

    script:
    """
    python ${projectDir}/../../src/llm_evaluation/runner.py \
        --queries ${queries} \
        --config ${projectDir}/../../configs/models/${model}_config.yaml \
        --output ${model}_responses.jsonl \
        --metadata ${model}_metadata.json \
        --model ${model}
    """
}

process VALIDATE_RESPONSES {
    tag "${responses.baseName}"
    label 'low_compute'
    publishDir "${params.output_dir}/qc", mode: 'copy'

    input:
    path responses

    output:
    path "*_response_validation.json", emit: report

    script:
    def model = responses.baseName.replaceAll('_responses', '')
    """
    python ${projectDir}/../../scripts/validate_responses.py \
        --input ${responses} \
        --schema ${projectDir}/../../data/schemas/llm_response_schema.json \
        --output ${model}_response_validation.json
    """
}

process DETECT_HALLUCINATIONS {
    tag "${responses.baseName}"
    label 'medium_compute'
    publishDir "${params.output_dir}/hallucinations", mode: 'copy'

    input:
    path responses
    path ground_truth

    output:
    path "*_hallucinations.json", emit: detections
    path "*_metrics.json", emit: metrics

    script:
    def model = responses.baseName.replaceAll('_responses', '')
    """
    python ${projectDir}/../../src/analysis/hallucination_detector.py \
        --responses ${responses} \
        --ground-truth ${ground_truth} \
        --detections ${model}_hallucinations.json \
        --metrics ${model}_metrics.json
    """
}
