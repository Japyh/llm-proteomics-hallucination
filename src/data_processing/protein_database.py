"""Interface to protein databases."""


class ProteinDatabase:
    """Query protein databases."""

    def __init__(self):
        """Initialize database connection."""
        pass

    def lookup_protein(self, protein_id: str) -> dict:
        """Look up protein by ID."""
        # Stub for actual database query
        return {"id": protein_id, "name": "Unknown"}
