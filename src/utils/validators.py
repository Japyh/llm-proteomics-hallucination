"""Input validation functions."""


def validate_protein_id(protein_id: str) -> bool:
    """Validate protein ID format."""
    return len(protein_id) > 0 and protein_id.isalnum()
