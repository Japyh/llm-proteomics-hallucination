"""Scoring functions for hallucination severity."""

def score_hallucination(response: str, ground_truth: str, severity_rules: dict) -> int:
    """Score hallucination severity based on rules."""
    # Simplified scoring logic
    if response.strip().lower() == ground_truth.strip().lower():
        return 0  # No hallucination
    elif any(keyword in response.lower() for keyword in severity_rules.get('minor', [])):
        return 1  # Minor
    elif any(keyword in response.lower() for keyword in severity_rules.get('moderate', [])):
        return 2  # Moderate
    else:
        return 3  # Severe

def aggregate_scores(scores: list, method: str = 'mean') -> float:
    """Aggregate multiple hallucination scores."""
    if method == 'mean':
        return sum(scores) / len(scores) if scores else 0
    elif method == 'max':
        return max(scores) if scores else 0
    elif method == 'median':
        return sorted(scores)[len(scores)//2] if scores else 0
    return 0
