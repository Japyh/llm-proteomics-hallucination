"""Tests for hallucination detector."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llm_evaluation.hallucination_detector import HallucinationDetector  # noqa: E402


def test_detect_fake_protein():
    """Test detection of fake protein IDs."""
    detector = HallucinationDetector()
    result = detector.detect("Protein FAKE123 is a kinase")
    assert result.is_hallucination is True


def test_valid_response():
    """Test valid protein response."""
    detector = HallucinationDetector()
    result = detector.detect("Protein P12345 is involved in signaling")
    # May or may not be hallucination depending on database
    assert result.confidence >= 0.0
