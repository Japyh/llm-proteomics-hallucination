"""
Evaluation runner for LLM proteomics evaluation.

This module orchestrates the evaluation process, managing query submission,
response collection, and result logging.
"""

import logging
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd

from .clients import BaseLLMClient, create_client
from .prompts import PromptTemplate


logger = logging.getLogger(__name__)


class EvaluationRunner:
    """Orchestrates LLM evaluation across multiple queries and models."""

    def __init__(
        self,
        output_dir: Path,
        rate_limit_delay: float = 2.0,
        save_every: int = 10,
        log_level: str = "INFO"
    ):
        """
        Initialize evaluation runner.

        Args:
            output_dir: Directory for saving results
            rate_limit_delay: Delay between API calls (seconds)
            save_every: Save results every N queries
            log_level: Logging level
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.rate_limit_delay = rate_limit_delay
        self.save_every = save_every

        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Results storage
        self.results = []
        self.start_time = None
        self.end_time = None

    def run_evaluation(
        self,
        queries: List[PromptTemplate],
        client: BaseLLMClient,
        model_name: str,
        session_id: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Run evaluation on a list of queries.

        Args:
            queries: List of PromptTemplate objects
            client: Initialized LLM client
            model_name: Name of the model being evaluated
            session_id: Optional session identifier

        Returns:
            DataFrame with evaluation results
        """
        session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"Starting evaluation session {session_id} with {len(queries)} queries")

        self.start_time = datetime.now()
        self.results = []

        for idx, prompt_template in enumerate(queries, 1):
            logger.info(f"Processing query {idx}/{len(queries)}")

            try:
                result = self._evaluate_single_query(
                    prompt_template=prompt_template,
                    client=client,
                    model_name=model_name,
                    query_index=idx
                )
                self.results.append(result)

                # Save intermediate results
                if idx % self.save_every == 0:
                    self._save_results(session_id, model_name, intermediate=True)

                # Rate limiting
                if idx < len(queries):
                    time.sleep(self.rate_limit_delay)

            except Exception as e:
                logger.error(f"Error processing query {idx}: {e}", exc_info=True)
                # Log failed query
                self.results.append({
                    "query_index": idx,
                    "query_text": prompt_template.query_text,
                    "model": model_name,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                continue

        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        logger.info(
            f"Evaluation completed: {len(self.results)} queries processed in {duration:.1f}s"
        )

        # Save final results
        df = self._save_results(session_id, model_name, intermediate=False)
        return df

    def _evaluate_single_query(
        self,
        prompt_template: PromptTemplate,
        client: BaseLLMClient,
        model_name: str,
        query_index: int
    ) -> Dict[str, Any]:
        """
        Evaluate a single query.

        Args:
            prompt_template: The prompt template
            client: LLM client
            model_name: Model identifier
            query_index: Index of query in batch

        Returns:
            Dictionary with query results
        """
        start_time = time.time()

        # Generate response
        response_data = client.generate(
            prompt=prompt_template.format_prompt(),
            system_prompt=prompt_template.get_system_prompt()
        )

        end_time = time.time()
        latency = end_time - start_time

        # Compile result
        result = {
            "query_index": query_index,
            "query_text": prompt_template.query_text,
            "domain": prompt_template.domain,
            "complexity": prompt_template.complexity,
            "protein_prevalence": prompt_template.protein_prevalence,
            "model": model_name,
            "response": response_data["response"],
            "latency_seconds": latency,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            **response_data.get("usage", {}),
            "metadata": {
                **prompt_template.metadata,
                **response_data.get("metadata", {})
            }
        }

        return result

    def _save_results(
        self,
        session_id: str,
        model_name: str,
        intermediate: bool = False
    ) -> pd.DataFrame:
        """
        Save results to disk.

        Args:
            session_id: Session identifier
            model_name: Model name
            intermediate: Whether this is an intermediate save

        Returns:
            DataFrame of results
        """
        df = pd.DataFrame(self.results)

        # Save as CSV
        suffix = "_intermediate" if intermediate else ""
        csv_path = self.output_dir / f"{session_id}_{model_name}_results{suffix}.csv"
        df.to_csv(csv_path, index=False)

        # Save as JSONL
        jsonl_path = self.output_dir / f"{session_id}_{model_name}_results{suffix}.jsonl"
        with open(jsonl_path, 'w') as f:
            for result in self.results:
                f.write(json.dumps(result) + '\n')

        logger.info(f"Results saved to {csv_path} and {jsonl_path}")
        return df

    def load_queries_from_json(self, json_path: Path) -> List[PromptTemplate]:
        """
        Load queries from JSON file.

        Args:
            json_path: Path to JSON file with queries

        Returns:
            List of PromptTemplate objects
        """
        with open(json_path, 'r') as f:
            queries_data = json.load(f)

        prompts = []
        for query_data in queries_data:
            prompt = PromptTemplate(
                query_text=query_data["query_text"],
                domain=query_data["domain"],
                complexity=query_data["complexity"],
                protein_prevalence=query_data["protein_prevalence"],
                metadata=query_data.get("metadata", {})
            )
            prompts.append(prompt)

        logger.info(f"Loaded {len(prompts)} queries from {json_path}")
        return prompts

    def generate_summary_report(self, model_name: str) -> Dict[str, Any]:
        """
        Generate summary statistics for evaluation run.

        Args:
            model_name: Model name

        Returns:
            Dictionary with summary statistics
        """
        if not self.results:
            return {}

        df = pd.DataFrame(self.results)

        successful = df[df["status"] == "success"]
        failed = df[df["status"] == "failed"]

        summary = {
            "model": model_name,
            "total_queries": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(self.results) if self.results else 0,
            "mean_latency": successful["latency_seconds"].mean() if len(successful) > 0 else None,
            "median_latency": successful["latency_seconds"].median() if len(successful) > 0 else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": (
                (self.end_time - self.start_time).total_seconds()
                if self.start_time and self.end_time else None
            ),
        }

        # Domain breakdown
        if len(successful) > 0:
            domain_counts = successful["domain"].value_counts().to_dict()
            summary["queries_by_domain"] = domain_counts

            # Complexity breakdown
            complexity_counts = successful["complexity"].value_counts().to_dict()
            summary["queries_by_complexity"] = complexity_counts

        # Save summary
        summary_path = self.output_dir / f"{model_name}_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Summary report saved to {summary_path}")
        return summary
