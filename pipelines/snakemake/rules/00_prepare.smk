rule prepare_data:
    input:
        "data/raw/queries.json"
    output:
        "data/queries/queries_all.json"
    shell:
        "python data/generators/simulate_queries.py"
