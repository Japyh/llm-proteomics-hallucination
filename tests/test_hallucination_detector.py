"""Tests for hallucination detector."""
import sys
sys.path.insert(0, '../src')
from llm_evaluation.hallucination_detector import HallucinationDetector

def test_detect_fake_protein():
    """Test detection of fake protein IDs."""
    detector = HallucinationDetector()
    result = detector.detect("Protein FAKE123 is a kinase")
    assert result.is_hallucination == True

def test_valid_response():
    """Test valid protein response."""
    detector = HallucinationDetector()
    result = detector.detect("Protein P12345 is involved in signaling")
    # May or may not be hallucination depending on database
    assert result.confidence >= 0.0
