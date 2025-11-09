"""
Reproducibility utilities including random seed management and version tracking.
"""

import random
import numpy as np
import subprocess
from pathlib import Path
from typing import Optional
import logging


logger = logging.getLogger(__name__)


def set_random_seed(seed: int = 42):
    """
    Set random seeds for reproducibility across Python, NumPy, and other libraries.

    Args:
        seed: Random seed value
    """
    random.seed(seed)
    np.random.seed(seed)

    # Try to set torch seed if available
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        logger.info(f"PyTorch random seed set to {seed}")
    except ImportError:
        pass

    logger.info(f"Random seed set to {seed} for Python and NumPy")


def get_git_commit_hash(repo_path: Optional[Path] = None) -> Optional[str]:
    """
    Get current git commit hash for provenance tracking.

    Args:
        repo_path: Path to git repository (default: current directory)

    Returns:
        Commit hash string, or None if not a git repository
    """
    try:
        if repo_path:
            cmd = ['git', '-C', str(repo_path), 'rev-parse', 'HEAD']
        else:
            cmd = ['git', 'rev-parse', 'HEAD']

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        commit_hash = result.stdout.strip()
        return commit_hash

    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("Could not retrieve git commit hash")
        return None


def get_git_status(repo_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Get git repository status for reproducibility documentation.

    Args:
        repo_path: Path to git repository

    Returns:
        Dictionary with git status information
    """
    info = {
        'commit_hash': get_git_commit_hash(repo_path),
        'branch': None,
        'is_dirty': None,
        'remote_url': None
    }

    try:
        if repo_path:
            base_cmd = ['git', '-C', str(repo_path)]
        else:
            base_cmd = ['git']

        # Get branch
        result = subprocess.run(
            base_cmd + ['rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        info['branch'] = result.stdout.strip()

        # Check if dirty
        result = subprocess.run(
            base_cmd + ['status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )
        info['is_dirty'] = len(result.stdout.strip()) > 0

        # Get remote URL
        result = subprocess.run(
            base_cmd + ['config', '--get', 'remote.origin.url'],
            capture_output=True,
            text=True,
            check=True
        )
        info['remote_url'] = result.stdout.strip()

    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("Could not retrieve full git status")

    return info
