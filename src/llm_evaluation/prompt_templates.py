"""Standardized prompt templates for LLM evaluation."""


class PromptTemplates:
    """Collection of prompt templates for proteomics queries."""

    @staticmethod
    def protein_function(protein_id: str) -> str:
        """Query protein function."""
        return f"What is the biological function of protein {protein_id}? Provide a concise, factual answer."

    @staticmethod
    def mass_spec_interpretation(peaks: str) -> str:
        """Interpret mass spectrometry results."""
        return f"Interpret these mass spectrometry peaks: {peaks}. Identify likely proteins."

    @staticmethod
    def clinical_relevance(protein: str, condition: str) -> str:
        """Assess clinical relevance."""
        return f"What is the clinical relevance of {protein} in {condition}?"
