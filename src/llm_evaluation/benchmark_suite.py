"""
Benchmark Suite for evaluating LLM performance on proteomics tasks.

This module orchestrates comprehensive evaluation of multiple LLM providers across
various proteomics interpretation tasks including protein function prediction,
mass spectrometry interpretation, and clinical biomarker assessment.

Authors:
    Olaf Yunus Laitinen Imanov <olyulaim@dtu.dk>
    Derya Umut Kulali <d_u_k@ogr.eskisehir.edu.tr>
"""

import asyncio
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from .hallucination_detector import HallucinationDetector
from .llm_client import LLMClient
from .prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkQuery:
    """A single benchmark query."""
    query_id: str
    category: str  # protein_function, mass_spec, clinical, ptm, rare_disease
    difficulty: str  # easy, medium, hard, expert
    prompt: str
    ground_truth: Dict[str, Any]
    metadata: Dict[str, Any] = None


@dataclass
class BenchmarkResult:
    """Result of running benchmark on one model."""
    query_id: str
    model: str
    provider: str
    response: str
    tokens_used: int
    cost_usd: float
    latency_seconds: float
    hallucination_result: Optional[Dict[str, Any]] = None
    timestamp: str = None


class BenchmarkSuite:
    """
    Orchestrate LLM evaluation across multiple models and tasks.

    This class manages the complete benchmark evaluation pipeline:
    1. Load test queries from configuration
    2. Execute queries against multiple LLM providers
    3. Detect hallucinations in responses
    4. Aggregate and analyze results
    5. Generate comprehensive reports

    Args:
        models: List of (provider, model_name) tuples to evaluate
        output_dir: Directory for saving results
        enable_hallucination_detection: Run hallucination detection on responses
        max_concurrent: Maximum concurrent API requests

    Example:
        >>> suite = BenchmarkSuite(
        ...     models=[('openai', 'gpt-4'), ('anthropic', 'claude-3-opus')],
        ...     output_dir='results/benchmark'
        ... )
        >>> results = await suite.run()
        >>> suite.save_results(results)
    """

    def __init__(
        self,
        models: List[tuple] = None,
        output_dir: str = 'results/benchmark',
        enable_hallucination_detection: bool = True,
        max_concurrent: int = 5,
        query_file: Optional[str] = None,
    ):
        """Initialize benchmark suite."""
        # Default models if not specified
        self.models = models or [
            ('openai', 'gpt-4'),
            ('anthropic', 'claude-3-opus-20240229'),
            ('google', 'gemini-pro'),
        ]

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.enable_hallucination_detection = enable_hallucination_detection
        self.max_concurrent = max_concurrent
        self.query_file = query_file

        # Initialize clients
        self.clients = {}
        for provider, model in self.models:
            try:
                client = LLMClient(provider=provider, model=model)
                self.clients[f"{provider}/{model}"] = client
                logger.info(f"Initialized client for {provider}/{model}")
            except Exception as e:
                logger.error(f"Failed to initialize {provider}/{model}: {e}")

        # Initialize hallucination detector
        if self.enable_hallucination_detection:
            self.detector = HallucinationDetector()

        # Load queries
        self.queries = self.load_queries()

        logger.info(f"Benchmark suite initialized with {len(self.queries)} queries")

    def load_queries(self) -> List[BenchmarkQuery]:
        """
        Load benchmark queries from configuration.

        Returns:
            List of BenchmarkQuery objects

        Note:
            If query_file is provided, loads from that file.
            Otherwise, generates default query set.
        """
        if self.query_file and Path(self.query_file).exists():
            return self._load_queries_from_file(self.query_file)
        else:
            return self._generate_default_queries()

    def _load_queries_from_file(self, filepath: str) -> List[BenchmarkQuery]:
        """Load queries from JSON file."""
        with open(filepath) as f:
            data = json.load(f)

        queries = []
        for item in data:
            queries.append(BenchmarkQuery(**item))

        logger.info(f"Loaded {len(queries)} queries from {filepath}")
        return queries

    def _generate_default_queries(self) -> List[BenchmarkQuery]:
        """Generate default set of benchmark queries."""
        queries = []

        # Protein function queries (easy)
        protein_ids = ['P04637', 'P53', 'BRCA1', 'EGFR', 'HER2']
        for i, pid in enumerate(protein_ids):
            queries.append(BenchmarkQuery(
                query_id=f"pf_easy_{i:03d}",
                category="protein_function",
                difficulty="easy",
                prompt=PromptTemplates.protein_function(pid),
                ground_truth={'protein_id': pid, 'category': 'well_characterized'},
                metadata={'protein_id': pid}
            ))

        # Mass spectrometry queries (medium)
        ms_queries = [
            "Interpret the following MS peaks: m/z 887.4, 1774.8, 2662.2",
            "What protein is indicated by peaks at m/z 432.2, 864.4, 1296.6?",
            "Analyze this mass spectrum: major peaks at 500-1500 Da range",
        ]
        for i, query in enumerate(ms_queries):
            queries.append(BenchmarkQuery(
                query_id=f"ms_medium_{i:03d}",
                category="mass_spec",
                difficulty="medium",
                prompt=query,
                ground_truth={'category': 'mass_spectrometry'},
                metadata={'query_type': 'peak_interpretation'}
            ))

        # Clinical relevance queries (hard)
        clinical_queries = [
            "What is the clinical significance of elevated alpha-fetoprotein levels?",
            "How does troponin I relate to myocardial infarction diagnosis?",
            "Explain the role of PSA as a prostate cancer biomarker",
        ]
        for i, query in enumerate(clinical_queries):
            queries.append(BenchmarkQuery(
                query_id=f"clinical_hard_{i:03d}",
                category="clinical",
                difficulty="hard",
                prompt=query,
                ground_truth={'category': 'clinical_biomarker'},
                metadata={'query_type': 'biomarker_interpretation'}
            ))

        # Expert level - ambiguous/edge cases
        expert_queries = [
            "What is the function of protein XYZ-9999?",  # Non-existent
            "How does the novel biomarker FAKE123 correlate with disease?",  # Fake
            "Interpret peaks at exactly m/z 123.456789012",  # Unrealistic precision
        ]
        for i, query in enumerate(expert_queries):
            queries.append(BenchmarkQuery(
                query_id=f"expert_{i:03d}",
                category="edge_case",
                difficulty="expert",
                prompt=query,
                ground_truth={'expected_hallucination': True},
                metadata={'query_type': 'hallucination_test'}
            ))

        logger.info(f"Generated {len(queries)} default queries")
        return queries

    async def run(self) -> List[BenchmarkResult]:
        """
        Run complete benchmark evaluation.

        Returns:
            List of BenchmarkResult objects

        Raises:
            Exception: If benchmark execution fails
        """
        logger.info(f"Starting benchmark with {len(self.queries)} queries across {len(self.clients)} models")

        all_results = []

        for model_key, client in self.clients.items():
            logger.info(f"Evaluating {model_key}...")

            # Process queries with concurrency control
            semaphore = asyncio.Semaphore(self.max_concurrent)

            async def process_query(query: BenchmarkQuery) -> BenchmarkResult:
                async with semaphore:
                    return await self._evaluate_query(query, client, model_key)

            # Run queries concurrently
            tasks = [process_query(q) for q in self.queries]
            model_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter out exceptions
            valid_results = [r for r in model_results if isinstance(r, BenchmarkResult)]
            errors = [r for r in model_results if isinstance(r, Exception)]

            if errors:
                logger.warning(f"{len(errors)} queries failed for {model_key}")

            all_results.extend(valid_results)
            logger.info(f"Completed {len(valid_results)} queries for {model_key}")

        return all_results

    async def _evaluate_query(
        self,
        query: BenchmarkQuery,
        client: LLMClient,
        model_key: str
    ) -> BenchmarkResult:
        """Evaluate a single query."""
        try:
            # Query LLM
            response = await client.query(
                query.prompt,
                temperature=0.7,  # Moderate temperature for balanced output
                max_tokens=500,
            )

            # Detect hallucinations
            hallucination_result = None
            if self.enable_hallucination_detection:
                hall_result = self.detector.detect(
                    response.content,
                    context=query.ground_truth
                )
                hallucination_result = {
                    'is_hallucination': hall_result.is_hallucination,
                    'types': [ht.value for ht in hall_result.hallucination_types],
                    'confidence': hall_result.confidence,
                    'evidence': hall_result.evidence
                }

            # Create result
            result = BenchmarkResult(
                query_id=query.query_id,
                model=model_key.split('/')[1],
                provider=model_key.split('/')[0],
                response=response.content,
                tokens_used=response.tokens_used,
                cost_usd=response.cost_usd,
                latency_seconds=response.latency_seconds,
                hallucination_result=hallucination_result,
                timestamp=datetime.now().isoformat()
            )

            return result

        except Exception as e:
            logger.error(f"Error evaluating {query.query_id} with {model_key}: {e}")
            raise

    def save_results(self, results: List[BenchmarkResult], filename: str = None):
        """
        Save benchmark results to file.

        Args:
            results: List of BenchmarkResult objects
            filename: Optional custom filename (auto-generated if not provided)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"

        output_path = self.output_dir / filename

        # Convert to dictionaries
        results_data = [asdict(r) for r in results]

        # Save as JSON
        with open(output_path, 'w') as f:
            json.dump(results_data, f, indent=2)

        logger.info(f"Saved {len(results)} results to {output_path}")

        # Also save as CSV for easy analysis
        csv_path = output_path.with_suffix('.csv')
        df = pd.DataFrame(results_data)
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved CSV to {csv_path}")

    def analyze_results(self, results: List[BenchmarkResult]) -> Dict[str, Any]:
        """
        Analyze benchmark results and generate statistics.

        Args:
            results: List of BenchmarkResult objects

        Returns:
            Dictionary with analysis statistics
        """
        df = pd.DataFrame([asdict(r) for r in results])

        analysis = {
            'total_queries': len(results),
            'total_cost_usd': df['cost_usd'].sum(),
            'total_tokens': df['tokens_used'].sum(),
            'avg_latency_seconds': df['latency_seconds'].mean(),
        }

        # Per-model statistics
        model_stats = {}
        for model in df['model'].unique():
            model_df = df[df['model'] == model]

            # Count hallucinations
            hall_count = 0
            if self.enable_hallucination_detection:
                hall_count = model_df['hallucination_result'].apply(
                    lambda x: x.get('is_hallucination', False) if isinstance(x, dict) else False
                ).sum()

            model_stats[model] = {
                'total_queries': len(model_df),
                'hallucination_count': hall_count,
                'hallucination_rate': hall_count / len(model_df) if len(model_df) > 0 else 0,
                'avg_cost_usd': model_df['cost_usd'].mean(),
                'total_cost_usd': model_df['cost_usd'].sum(),
                'avg_latency': model_df['latency_seconds'].mean(),
            }

        analysis['per_model'] = model_stats

        return analysis

    def generate_report(self, results: List[BenchmarkResult], output_file: str = None):
        """
        Generate comprehensive benchmark report.

        Args:
            results: List of BenchmarkResult objects
            output_file: Optional output file path
        """
        analysis = self.analyze_results(results)

        report = f"""
# LLM Proteomics Benchmark Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- Total Queries: {analysis['total_queries']}
- Total Cost: ${analysis['total_cost_usd']:.2f}
- Total Tokens: {analysis['total_tokens']:,}
- Average Latency: {analysis['avg_latency_seconds']:.2f}s

## Model Performance

"""

        for model, stats in analysis['per_model'].items():
            report += f"""
### {model}

- Queries Evaluated: {stats['total_queries']}
- Hallucination Rate: {stats['hallucination_rate']:.1%}
- Total Cost: ${stats['total_cost_usd']:.2f}
- Average Latency: {stats['avg_latency']:.2f}s

"""

        if output_file:
            output_path = self.output_dir / output_file
            with open(output_path, 'w') as f:
                f.write(report)
            logger.info(f"Report saved to {output_path}")
        else:
            print(report)

        return report


# CLI entry point
async def main():
    """Run benchmark from command line."""
    import argparse

    parser = argparse.ArgumentParser(description='Run LLM proteomics benchmark')
    parser.add_argument('--models', nargs='+', help='Models to evaluate (provider/model format)')
    parser.add_argument('--output', default='results/benchmark', help='Output directory')
    parser.add_argument('--queries', help='Path to queries JSON file')
    parser.add_argument('--no-hallucination-detection', action='store_true',
                        help='Disable hallucination detection')

    args = parser.parse_args()

    # Parse models
    models = []
    if args.models:
        for model_str in args.models:
            provider, model = model_str.split('/')
            models.append((provider, model))

    # Create and run benchmark
    suite = BenchmarkSuite(
        models=models if models else None,
        output_dir=args.output,
        enable_hallucination_detection=not args.no_hallucination_detection,
        query_file=args.queries,
    )

    results = await suite.run()
    suite.save_results(results)
    suite.generate_report(results, 'benchmark_report.md')

    print(f"\nBenchmark complete! Results saved to {suite.output_dir}")


if __name__ == '__main__':
    asyncio.run(main())
