"""Data processing module for proteomics data handling."""

from .protein_database import ProteinDatabase
from .synthetic_data_generator import SyntheticDataGenerator

__all__ = ["SyntheticDataGenerator", "ProteinDatabase"]
