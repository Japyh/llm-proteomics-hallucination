"""
Batch processing utilities for large-scale LLM evaluation.

This module provides tools for efficiently processing large batches of queries
with parallel execution, checkpointing, and error recovery.
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
import hashlib

from .clients import BaseLLMClient
from .prompts import PromptTemplate


logger = logging.getLogger(__name__)


@dataclass
class BatchJob:
    """Represents a batch evaluation job."""
    job_id: str
    model_name: str
    total_queries: int
    completed_queries: int
    failed_queries: int
    start_time: str
    last_checkpoint: str
    status: str  # pending, running, completed, failed


class BatchProcessor:
    """Process large batches of queries with checkpointing and recovery."""

    def __init__(
        self,
        checkpoint_dir: Path,
        checkpoint_interval: int = 50,
        max_workers: int = 1,  # Sequential by default for API rate limits
        rate_limit_delay: float = 2.0
    ):
        """
        Initialize batch processor.

        Args:
            checkpoint_dir: Directory for saving checkpoints
            checkpoint_interval: Save checkpoint every N queries
            max_workers: Maximum concurrent workers
            rate_limit_delay: Delay between requests (seconds)
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        self.checkpoint_interval = checkpoint_interval
        self.max_workers = max_workers
        self.rate_limit_delay = rate_limit_delay

        self.current_job: Optional[BatchJob] = None
        self.processed_query_hashes = set()

    def process_batch(
        self,
        queries: List[PromptTemplate],
        client: BaseLLMClient,
        model_name: str,
        job_id: Optional[str] = None,
        resume: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Process a batch of queries with checkpointing.

        Args:
            queries: List of PromptTemplate objects
            client: Initialized LLM client
            model_name: Model identifier
            job_id: Optional job ID (auto-generated if not provided)
            resume: Whether to resume from checkpoint

        Returns:
            List of results dictionaries
        """
        # Generate or load job
        if job_id and resume:
            self.current_job = self._load_checkpoint(job_id)
            if self.current_job:
                logger.info(f"Resuming job {job_id} from checkpoint")

        if not self.current_job:
            job_id = job_id or self._generate_job_id(model_name)
            self.current_job = BatchJob(
                job_id=job_id,
                model_name=model_name,
                total_queries=len(queries),
                completed_queries=0,
                failed_queries=0,
                start_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                last_checkpoint="",
                status="running"
            )

        results = []

        try:
            # Process queries
            if self.max_workers == 1:
                # Sequential processing (respects rate limits)
                results = self._process_sequential(queries, client, model_name)
            else:
                # Parallel processing
                results = self._process_parallel(queries, client, model_name)

            self.current_job.status = "completed"
            self._save_checkpoint()

        except Exception as e:
            logger.error(f"Batch processing failed: {e}", exc_info=True)
            self.current_job.status = "failed"
            self._save_checkpoint()
            raise

        return results

    def _process_sequential(
        self,
        queries: List[PromptTemplate],
        client: BaseLLMClient,
        model_name: str
    ) -> List[Dict[str, Any]]:
        """Process queries sequentially."""
        results = []

        for idx, query in enumerate(queries, 1):
            # Skip if already processed
            query_hash = self._hash_query(query)
            if query_hash in self.processed_query_hashes:
                logger.info(f"Skipping already processed query {idx}/{len(queries)}")
                continue

            try:
                # Generate response
                result = self._generate_response(query, client, model_name, idx)
                results.append(result)

                self.processed_query_hashes.add(query_hash)
                self.current_job.completed_queries += 1

                # Checkpoint
                if idx % self.checkpoint_interval == 0:
                    self._save_checkpoint()
                    logger.info(f"Checkpoint saved at query {idx}/{len(queries)}")

                # Rate limiting
                time.sleep(self.rate_limit_delay)

            except Exception as e:
                logger.error(f"Error processing query {idx}: {e}", exc_info=True)
                self.current_job.failed_queries += 1
                results.append({
                    "query_index": idx,
                    "status": "failed",
                    "error": str(e)
                })

        return results

    def _process_parallel(
        self,
        queries: List[PromptTemplate],
        client: BaseLLMClient,
        model_name: str
    ) -> List[Dict[str, Any]]:
        """Process queries in parallel."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all queries
            future_to_query = {
                executor.submit(
                    self._generate_response, query, client, model_name, idx
                ): (idx, query)
                for idx, query in enumerate(queries, 1)
            }

            # Collect results as they complete
            for future in as_completed(future_to_query):
                idx, query = future_to_query[future]
                try:
                    result = future.result()
                    results.append(result)

                    query_hash = self._hash_query(query)
                    self.processed_query_hashes.add(query_hash)
                    self.current_job.completed_queries += 1

                    if idx % self.checkpoint_interval == 0:
                        self._save_checkpoint()

                except Exception as e:
                    logger.error(f"Query {idx} failed: {e}", exc_info=True)
                    self.current_job.failed_queries += 1
                    results.append({
                        "query_index": idx,
                        "status": "failed",
                        "error": str(e)
                    })

        return results

    def _generate_response(
        self,
        query: PromptTemplate,
        client: BaseLLMClient,
        model_name: str,
        index: int
    ) -> Dict[str, Any]:
        """Generate response for a single query."""
        start_time = time.time()

        response_data = client.generate(
            prompt=query.format_prompt(),
            system_prompt=query.get_system_prompt()
        )

        end_time = time.time()

        return {
            "query_index": index,
            "query_text": query.query_text,
            "domain": query.domain,
            "complexity": query.complexity,
            "protein_prevalence": query.protein_prevalence,
            "model": model_name,
            "response": response_data["response"],
            "latency_seconds": end_time - start_time,
            "status": "success",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            **response_data.get("usage", {}),
            "metadata": response_data.get("metadata", {})
        }

    def _save_checkpoint(self):
        """Save current job state to checkpoint file."""
        if not self.current_job:
            return

        checkpoint_file = self.checkpoint_dir / f"{self.current_job.job_id}.checkpoint.json"

        checkpoint_data = {
            "job": asdict(self.current_job),
            "processed_queries": list(self.processed_query_hashes)
        }

        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)

        self.current_job.last_checkpoint = time.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"Checkpoint saved to {checkpoint_file}")

    def _load_checkpoint(self, job_id: str) -> Optional[BatchJob]:
        """Load job state from checkpoint file."""
        checkpoint_file = self.checkpoint_dir / f"{job_id}.checkpoint.json"

        if not checkpoint_file.exists():
            logger.info(f"No checkpoint found for job {job_id}")
            return None

        try:
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)

            job = BatchJob(**checkpoint_data["job"])
            self.processed_query_hashes = set(checkpoint_data["processed_queries"])

            logger.info(
                f"Loaded checkpoint: {job.completed_queries}/{job.total_queries} completed"
            )
            return job

        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}", exc_info=True)
            return None

    def _hash_query(self, query: PromptTemplate) -> str:
        """Generate hash for query deduplication."""
        query_str = f"{query.query_text}|{query.domain}|{query.complexity}"
        return hashlib.sha256(query_str.encode()).hexdigest()[:16]

    def _generate_job_id(self, model_name: str) -> str:
        """Generate unique job ID."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return f"{model_name}_{timestamp}"

    def get_job_status(self) -> Optional[Dict[str, Any]]:
        """Get current job status."""
        if not self.current_job:
            return None

        return {
            **asdict(self.current_job),
            "progress_percentage": (
                self.current_job.completed_queries / self.current_job.total_queries * 100
                if self.current_job.total_queries > 0 else 0
            )
        }
