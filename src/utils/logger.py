"""Logging setup."""

import logging
import sys


def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """Set up logger with handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
