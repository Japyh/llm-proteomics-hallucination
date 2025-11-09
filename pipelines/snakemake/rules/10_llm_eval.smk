rule evaluate_llms:
    input:
        queries="data/queries/queries_all.json",
        config="configs/models/{model}.yaml"
    output:
        "data/llm_responses/{model}_responses.jsonl"
    shell:
        "python src/llm_eval/runner.py --model {wildcards.model}"
