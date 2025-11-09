/*
 * Nextflow modules for data preparation
 */

process VALIDATE_QUERIES {
    tag "validate_queries"
    label 'low_compute'
    publishDir "${params.output_dir}/qc", mode: 'copy'

    input:
    path queries

    output:
    path "query_validation_report.json", emit: report

    script:
    """
    python ${projectDir}/../../scripts/validate_data.py \
        --input ${queries} \
        --schema ${projectDir}/../../data/schemas/query_schema.json \
        --output query_validation_report.json
    """
}

process SPLIT_DATASET {
    tag "split_dataset"
    label 'low_compute'
    publishDir "${params.output_dir}/queries", mode: 'copy'

    input:
    path queries

    output:
    path "train.json", emit: train
    path "validation.json", emit: validation
    path "test.json", emit: test

    script:
    """
    python ${projectDir}/../../scripts/split_dataset.py \
        --input ${queries} \
        --train train.json \
        --validation validation.json \
        --test test.json \
        --test-size ${params.test_size} \
        --seed ${params.random_seed}
    """
}

process PREPARE_GROUND_TRUTH {
    tag "prepare_ground_truth"
    label 'low_compute'
    publishDir "${params.output_dir}/annotations", mode: 'copy'

    output:
    path "ground_truth_validated.json", emit: ground_truth
    path "annotation_validation_report.json", emit: report

    script:
    """
    python ${projectDir}/../../scripts/validate_annotations.py \
        --input ${projectDir}/../../data/annotations/expert_annotations.json \
        --schema ${projectDir}/../../data/schemas/annotation_schema.json \
        --output ground_truth_validated.json \
        --report annotation_validation_report.json
    """
}
