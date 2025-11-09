"""
Snakemake rules for data preparation and validation
"""

rule validate_queries:
    """Validate query dataset against JSON schema"""
    input:
        queries = "data/queries/queries_all.json",
        schema = "data/schemas/query_schema.json"
    output:
        report = "data/qc/query_validation_report.json"
    log:
        "logs/validate_queries.log"
    conda:
        "../envs/data_processing.yaml"
    shell:
        """
        python scripts/validate_data.py \
            --input {input.queries} \
            --schema {input.schema} \
            --output {output.report} \
            2> {log}
        """

rule split_dataset:
    """Split queries into train/validation/test sets"""
    input:
        queries = "data/queries/queries_all.json"
    output:
        train = "data/queries/train.json",
        validation = "data/queries/validation.json",
        test = "data/queries/test.json"
    params:
        seed = config.get("random_seed", 42),
        test_size = config.get("evaluation", {}).get("test_size", 0.2)
    log:
        "logs/split_dataset.log"
    conda:
        "../envs/data_processing.yaml"
    shell:
        """
        python scripts/split_dataset.py \
            --input {input.queries} \
            --train {output.train} \
            --validation {output.validation} \
            --test {output.test} \
            --test-size {params.test_size} \
            --seed {params.seed} \
            2> {log}
        """

rule prepare_ground_truth:
    """Prepare and validate ground truth annotations"""
    input:
        annotations = "data/annotations/expert_annotations.json",
        schema = "data/schemas/annotation_schema.json"
    output:
        validated = "data/annotations/ground_truth_validated.json",
        report = "data/qc/annotation_validation_report.json"
    log:
        "logs/prepare_ground_truth.log"
    conda:
        "../envs/data_processing.yaml"
    shell:
        """
        python scripts/validate_annotations.py \
            --input {input.annotations} \
            --schema {input.schema} \
            --output {output.validated} \
            --report {output.report} \
            2> {log}
        """

rule compute_checksums:
    """Compute SHA256 checksums for all data files"""
    input:
        queries = "data/queries/queries_all.json",
        annotations = "data/annotations/expert_annotations.json",
        proteins = "data/proteins/uniprot_sequences.fasta"
    output:
        checksums = "provenance/checksums/data_checksums.txt"
    log:
        "logs/compute_checksums.log"
    shell:
        """
        echo "Computing checksums..." > {log}
        sha256sum {input.queries} {input.annotations} {input.proteins} > {output.checksums} 2>> {log}
        """

rule prepare_protein_database:
    """Prepare protein database for MS/MS analysis"""
    input:
        sequences = "data/proteins/uniprot_sequences.fasta"
    output:
        indexed = "data/proteins/uniprot_indexed.db"
    log:
        "logs/prepare_protein_database.log"
    conda:
        "../envs/proteomics.yaml"
    shell:
        """
        python scripts/index_proteins.py \
            --input {input.sequences} \
            --output {output.indexed} \
            2> {log}
        """
