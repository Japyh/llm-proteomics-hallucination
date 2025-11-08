"""
Complete Example: LLM Proteomics Hallucination Detection

This script demonstrates the complete workflow from data generation
through LLM evaluation to hallucination detection and analysis.

Authors:
    Olaf Yunus Laitinen Imanov <olyulaim@dtu.dk>
    Derya Umut Kulali <d_u_k@ogr.eskisehir.edu.tr>

Usage:
    python examples/complete_example.py
"""

import asyncio
import sys
from pathlib import Path

import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing import SyntheticDataGenerator  # noqa: E402
from src.llm_evaluation import HallucinationDetector, LLMClient  # noqa: E402


async def main():
    """Run complete example workflow."""

    print("=" * 80)
    print("LLM Proteomics Hallucination Detection - Complete Example")
    print("=" * 80)
    print()

    # Step 1: Generate Synthetic Data
    print("Step 1: Generating Synthetic Protein Data")
    print("-" * 80)

    generator = SyntheticDataGenerator(seed=42)
    proteins = generator.generate_protein_dataset(
        n_proteins=5,
        include_rare=True,
        difficulty='medium'
    )

    print(f"Generated {len(proteins)} synthetic proteins:")
    print(proteins[['protein_id', 'protein_name', 'molecular_weight']].to_string())
    print()

    # Step 2: Initialize LLM Client
    print("Step 2: Initializing LLM Client")
    print("-" * 80)

    try:
        client = LLMClient(provider='openai', model='gpt-4')
        print("✓ OpenAI GPT-4 client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        print("  Make sure you have set OPENAI_API_KEY in your .env file")
        return
    print()

    # Step 3: Query LLMs with Protein Questions
    print("Step 3: Querying LLM with Protein Function Questions")
    print("-" * 80)

    results = []

    for idx, protein in proteins.head(3).iterrows():  # Test with first 3 proteins
        query = f"What is the biological function of protein {protein['protein_id']}?"

        print(f"\nQuery {idx+1}: {query}")

        try:
            response = await client.query(
                query,
                temperature=0.7,
                max_tokens=200
            )

            print(f"Response (first 150 chars):")
            print(f"  {response.content[:150]}...")
            print(f"  Cost: ${response.cost_usd:.4f} | Tokens: {response.tokens_used}")

            results.append({
                'protein_id': protein['protein_id'],
                'query': query,
                'response': response.content,
                'cost': response.cost_usd,
                'tokens': response.tokens_used
            })

        except Exception as e:
            print(f"  Error: {e}")

    print()

    # Step 4: Detect Hallucinations
    print("Step 4: Detecting Hallucinations in Responses")
    print("-" * 80)

    detector = HallucinationDetector()

    for result in results:
        hall_result = detector.detect(result['response'])

        result['is_hallucination'] = hall_result.is_hallucination
        result['confidence'] = hall_result.confidence
        result['hallucination_types'] = [t.value for t in hall_result.hallucination_types]
        result['evidence'] = hall_result.evidence

        print(f"\nProtein: {result['protein_id']}")
        print(f"  Hallucination Detected: {hall_result.is_hallucination}")
        if hall_result.is_hallucination:
            print(f"  Confidence: {hall_result.confidence:.2f}")
            print(f"  Types: {[t.value for t in hall_result.hallucination_types]}")
            print(f"  Evidence: {hall_result.evidence}")
        else:
            print(f"  Response appears factually sound")

    print()

    # Step 5: Calculate Metrics
    print("Step 5: Calculating Performance Metrics")
    print("-" * 80)

    df = pd.DataFrame(results)

    hallucination_rate = df['is_hallucination'].mean()
    total_cost = df['cost'].sum()
    avg_tokens = df['tokens'].mean()

    print(f"\nResults Summary:")
    print(f"  Total Queries: {len(results)}")
    print(f"  Hallucination Rate: {hallucination_rate:.1%}")
    print(f"  Total Cost: ${total_cost:.4f}")
    print(f"  Average Tokens per Query: {avg_tokens:.0f}")

    # Get client stats
    client_stats = client.get_stats()
    print(f"\nClient Statistics:")
    print(f"  Total Requests: {client_stats['total_requests']}")
    print(f"  Total Tokens: {client_stats['total_tokens']}")
    print(f"  Total Cost: ${client_stats['total_cost_usd']:.4f}")
    print(f"  Cache Size: {client_stats['cache_size']}")
    print()

    # Step 6: Save Results
    print("Step 6: Saving Results")
    print("-" * 80)

    output_dir = Path('results/examples')
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / 'complete_example_results.csv'
    df.to_csv(output_file, index=False)

    print(f"✓ Results saved to: {output_file}")
    print()

    # Step 7: Summary
    print("=" * 80)
    print("Example Complete!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Review results in:", output_file)
    print("  2. Run full benchmark with: python -m src.llm_evaluation.benchmark_suite")
    print("  3. Explore Jupyter notebooks in: notebooks/")
    print("  4. Read full tutorial at: docs/tutorial.md")
    print()
    print("For more information:")
    print("  - Documentation: docs/index.md")
    print("  - Repository: https://github.com/olaflaitinen/llm-proteomics-hallucination")
    print("  - Contact: olyulaim@dtu.dk")
    print()


if __name__ == '__main__':
    # Run the async main function
    asyncio.run(main())
