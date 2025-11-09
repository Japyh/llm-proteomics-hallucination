"""Data loading utilities for proteomics data and LLM evaluation datasets.

This module provides comprehensive data loading functionality for:
- Query datasets (JSON)
- LLM response files (JSONL)
- Annotation data (JSON/CSV)
- Protein identification data (CSV)
- MS/MS metadata (YAML)
- Configuration files (YAML/JSON)
"""

import pandas as pd
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import numpy as np


logger = logging.getLogger(__name__)


class DataLoader:
    """Load and parse various data formats for LLM proteomics evaluation.

    This class provides methods to load queries, responses, annotations,
    and proteomics data from multiple file formats with validation.

    Attributes:
        base_path: Base directory path for relative file loading
        validate: Whether to validate data after loading
    """

    def __init__(
        self,
        base_path: Optional[Path] = None,
        validate: bool = True
    ):
        """
        Initialize DataLoader.

        Args:
            base_path: Base directory for relative paths (default: current directory)
            validate: Enable data validation after loading
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.validate = validate
        logger.info(f"DataLoader initialized with base_path: {self.base_path}")

    def _resolve_path(self, file_path: Union[str, Path]) -> Path:
        """
        Resolve file path relative to base_path if not absolute.

        Args:
            file_path: File path to resolve

        Returns:
            Resolved Path object
        """
        file_path = Path(file_path)
        if not file_path.is_absolute():
            file_path = self.base_path / file_path
        return file_path

    def load_queries(
        self,
        file_path: Union[str, Path],
        filter_complexity: Optional[str] = None,
        filter_prevalence: Optional[str] = None
    ) -> List[Dict]:
        """
        Load query data from JSON file.

        Args:
            file_path: Path to JSON file with queries
            filter_complexity: Filter by complexity level (simple/intermediate/complex)
            filter_prevalence: Filter by prevalence (common/moderate/rare)

        Returns:
            List of query dictionaries

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file is not valid JSON
        """
        file_path = self._resolve_path(file_path)
        logger.info(f"Loading queries from {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            queries = json.load(f)

        # Apply filters if specified
        if filter_complexity:
            queries = [q for q in queries if q.get('complexity') == filter_complexity]
            logger.info(f"Filtered to {len(queries)} queries with complexity={filter_complexity}")

        if filter_prevalence:
            queries = [q for q in queries if q.get('prevalence') == filter_prevalence]
            logger.info(f"Filtered to {len(queries)} queries with prevalence={filter_prevalence}")

        logger.info(f"Loaded {len(queries)} queries")
        return queries

    def load_responses(
        self,
        file_path: Union[str, Path],
        model_filter: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load LLM responses from JSONL file.

        Args:
            file_path: Path to JSONL file with responses
            model_filter: Filter by model name

        Returns:
            DataFrame with response data

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path = self._resolve_path(file_path)
        logger.info(f"Loading responses from {file_path}")

        df = pd.read_json(file_path, lines=True)

        # Apply model filter if specified
        if model_filter and 'model' in df.columns:
            df = df[df['model'] == model_filter]
            logger.info(f"Filtered to {len(df)} responses for model={model_filter}")

        logger.info(f"Loaded {len(df)} responses")
        return df

    def load_annotations(
        self,
        file_path: Union[str, Path],
        format: str = 'auto'
    ) -> Union[List[Dict], pd.DataFrame]:
        """
        Load annotation data from JSON or CSV file.

        Args:
            file_path: Path to annotation file
            format: File format ('json', 'csv', or 'auto')

        Returns:
            List of dictionaries (JSON) or DataFrame (CSV)

        Raises:
            ValueError: If format is not recognized
        """
        file_path = self._resolve_path(file_path)
        logger.info(f"Loading annotations from {file_path}")

        # Auto-detect format from extension
        if format == 'auto':
            suffix = file_path.suffix.lower()
            if suffix == '.json':
                format = 'json'
            elif suffix == '.csv':
                format = 'csv'
            else:
                raise ValueError(f"Cannot auto-detect format from extension: {suffix}")

        if format == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                annotations = json.load(f)
            logger.info(f"Loaded {len(annotations)} annotations from JSON")
            return annotations
        elif format == 'csv':
            annotations = pd.read_csv(file_path)
            logger.info(f"Loaded {len(annotations)} annotations from CSV")
            return annotations
        else:
            raise ValueError(f"Unsupported format: {format}")

    def load_protein_data(
        self,
        file_path: Union[str, Path],
        id_column: str = 'uniprot_id'
    ) -> pd.DataFrame:
        """
        Load protein identification data from CSV.

        Args:
            file_path: Path to CSV file with protein data
            id_column: Column name for protein IDs

        Returns:
            DataFrame with protein data
        """
        file_path = self._resolve_path(file_path)
        logger.info(f"Loading protein data from {file_path}")

        df = pd.read_csv(file_path)

        if id_column not in df.columns:
            logger.warning(f"Expected ID column '{id_column}' not found in protein data")

        logger.info(f"Loaded {len(df)} protein records")
        return df

    def load_msms_metadata(
        self,
        file_path: Union[str, Path]
    ) -> Dict:
        """
        Load MS/MS run metadata from YAML file.

        Args:
            file_path: Path to YAML file

        Returns:
            Dictionary with metadata
        """
        file_path = self._resolve_path(file_path)
        logger.info(f"Loading MS/MS metadata from {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            metadata = yaml.safe_load(f)

        logger.info("MS/MS metadata loaded successfully")
        return metadata

    def load_config(
        self,
        file_path: Union[str, Path],
        format: str = 'auto'
    ) -> Dict:
        """
        Load configuration from YAML or JSON file.

        Args:
            file_path: Path to config file
            format: File format ('yaml', 'json', or 'auto')

        Returns:
            Configuration dictionary
        """
        file_path = self._resolve_path(file_path)
        logger.info(f"Loading config from {file_path}")

        # Auto-detect format
        if format == 'auto':
            suffix = file_path.suffix.lower()
            if suffix in ['.yaml', '.yml']:
                format = 'yaml'
            elif suffix == '.json':
                format = 'json'
            else:
                raise ValueError(f"Cannot auto-detect config format from: {suffix}")

        if format == 'yaml':
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        elif format == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {format}")

        logger.info("Configuration loaded successfully")
        return config

    def load_ground_truth(
        self,
        file_path: Union[str, Path]
    ) -> Dict[str, Any]:
        """
        Load ground truth data for evaluation.

        Args:
            file_path: Path to ground truth file

        Returns:
            Dictionary mapping query IDs to ground truth
        """
        file_path = self._resolve_path(file_path)
        logger.info(f"Loading ground truth from {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            ground_truth = json.load(f)

        logger.info(f"Loaded ground truth for {len(ground_truth)} items")
        return ground_truth

    def load_batch(
        self,
        file_paths: List[Union[str, Path]],
        loader_func: str = 'load_queries'
    ) -> List[Any]:
        """
        Load multiple files in batch.

        Args:
            file_paths: List of file paths to load
            loader_func: Name of loader method to use

        Returns:
            List of loaded data
        """
        results = []
        loader = getattr(self, loader_func)

        for file_path in file_paths:
            try:
                data = loader(file_path)
                results.append(data)
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")
                continue

        logger.info(f"Batch loaded {len(results)}/{len(file_paths)} files")
        return results
