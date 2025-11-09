"""
Prompt templates and system prompts for LLM evaluation.

This module defines standardized prompts used across all models
to ensure consistency in evaluation.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class SystemPrompts:
    """Collection of system prompts for different evaluation scenarios."""

    STANDARD = """You are an expert clinical proteomics consultant. Provide accurate, evidence-based answers to proteomics questions. Cite specific databases (UniProt, PhosphoSitePlus, Human Protein Atlas) and peer-reviewed literature when applicable. If you are uncertain about any aspect of your answer, explicitly state your uncertainty. Do not fabricate protein names, modification sites, or literature citations."""

    PROTEIN_IDENTIFICATION = """You are a specialist in protein identification and mass spectrometry. Provide precise information about protein sequences, accession numbers, isoforms, and post-translational modifications. Always cite UniProt accession numbers and verify information against the UniProt database. If a protein or isoform does not exist, state this clearly rather than guessing."""

    QUANTITATIVE_ANALYSIS = """You are an expert in quantitative proteomics and differential expression analysis. Provide accurate information about protein abundance, fold changes, statistical significance, and normalization methods. Be specific about experimental conditions and biological context. Acknowledge limitations and sources of variability."""

    PTM_ANALYSIS = """You are a post-translational modification specialist. Provide precise information about phosphorylation sites, kinases, glycosylation patterns, and other modifications. Always cite PhosphoSitePlus or similar databases. Do not fabricate modification sites or kinase-substrate relationships. If a modification is not validated, state this explicitly."""

    CLINICAL_INTERPRETATION = """You are a clinical proteomics consultant specializing in biomarker discovery and clinical translation. Provide evidence-based interpretations of proteomics findings, including disease associations, clinical utility, and validation status. Always cite peer-reviewed literature. Clearly distinguish between validated biomarkers and investigational findings."""


class PromptTemplate:
    """Template for constructing prompts with metadata."""

    def __init__(
        self,
        query_text: str,
        domain: str,
        complexity: str,
        protein_prevalence: str,
        metadata: Optional[Dict] = None
    ):
        """
        Initialize prompt template.

        Args:
            query_text: The proteomics query
            domain: Domain category (protein_id, quantitative, ptm, interaction, clinical)
            complexity: Complexity level (low, medium, high)
            protein_prevalence: Protein prevalence (common, moderate, rare)
            metadata: Additional metadata dictionary
        """
        self.query_text = query_text
        self.domain = domain
        self.complexity = complexity
        self.protein_prevalence = protein_prevalence
        self.metadata = metadata or {}

    def get_system_prompt(self) -> str:
        """
        Get appropriate system prompt based on domain.

        Returns:
            System prompt string
        """
        domain_prompts = {
            "protein_identification": SystemPrompts.PROTEIN_IDENTIFICATION,
            "quantitative_expression": SystemPrompts.QUANTITATIVE_ANALYSIS,
            "ptm": SystemPrompts.PTM_ANALYSIS,
            "protein_interactions": SystemPrompts.STANDARD,
            "clinical_interpretation": SystemPrompts.CLINICAL_INTERPRETATION,
        }
        return domain_prompts.get(self.domain, SystemPrompts.STANDARD)

    def format_prompt(self, include_context: bool = False) -> str:
        """
        Format the complete prompt.

        Args:
            include_context: Whether to include additional context

        Returns:
            Formatted prompt string
        """
        prompt = self.query_text

        if include_context and self.metadata:
            context_parts = []
            if "experimental_context" in self.metadata:
                context_parts.append(f"Experimental context: {self.metadata['experimental_context']}")
            if "data_provided" in self.metadata:
                context_parts.append(f"Data: {self.metadata['data_provided']}")

            if context_parts:
                context = "\n".join(context_parts)
                prompt = f"{context}\n\nQuery: {prompt}"

        return prompt

    def to_dict(self) -> Dict:
        """
        Convert prompt to dictionary representation.

        Returns:
            Dictionary with all prompt information
        """
        return {
            "query_text": self.query_text,
            "domain": self.domain,
            "complexity": self.complexity,
            "protein_prevalence": self.protein_prevalence,
            "metadata": self.metadata,
            "system_prompt": self.get_system_prompt(),
            "formatted_prompt": self.format_prompt(),
        }


class PromptBuilder:
    """Utility class for building complex prompts."""

    @staticmethod
    def build_protein_identification_prompt(
        protein_name: Optional[str] = None,
        uniprot_id: Optional[str] = None,
        peptide_sequence: Optional[str] = None,
        question_type: str = "accession"
    ) -> str:
        """
        Build protein identification prompt.

        Args:
            protein_name: Human-readable protein name
            uniprot_id: UniProt accession ID
            peptide_sequence: Peptide sequence from MS/MS
            question_type: Type of question (accession, isoform, function)

        Returns:
            Formatted prompt string
        """
        if question_type == "accession" and protein_name:
            return f"What is the UniProt accession number for human {protein_name}?"
        elif question_type == "isoform" and uniprot_id:
            return f"What are the major protein isoforms of {uniprot_id} detected in human tissues?"
        elif question_type == "peptide" and peptide_sequence:
            return f"Based on peptide sequence {peptide_sequence}, what is the most likely protein identification?"
        else:
            raise ValueError("Invalid combination of parameters for protein ID prompt")

    @staticmethod
    def build_quantitative_prompt(
        protein_name: str,
        condition: str,
        fold_change: Optional[float] = None,
        p_value: Optional[float] = None,
        question_type: str = "expression"
    ) -> str:
        """
        Build quantitative expression prompt.

        Args:
            protein_name: Protein name or ID
            condition: Biological condition or disease
            fold_change: Observed fold change
            p_value: Statistical significance
            question_type: Type of question

        Returns:
            Formatted prompt string
        """
        if question_type == "expression":
            return f"Is {protein_name} typically upregulated or downregulated in {condition}?"
        elif question_type == "interpretation" and fold_change and p_value:
            return (f"In a proteomics experiment, {protein_name} shows {fold_change:.1f}-fold "
                   f"change in {condition} (p={p_value:.3f}). Is this likely biologically "
                   f"significant and what validation would you recommend?")
        else:
            raise ValueError("Invalid parameters for quantitative prompt")

    @staticmethod
    def build_ptm_prompt(
        protein_name: str,
        modification_type: str = "phosphorylation",
        site: Optional[str] = None,
        question_type: str = "sites"
    ) -> str:
        """
        Build post-translational modification prompt.

        Args:
            protein_name: Protein name or ID
            modification_type: Type of PTM (phosphorylation, glycosylation, etc.)
            site: Specific modification site
            question_type: Type of question

        Returns:
            Formatted prompt string
        """
        if question_type == "sites":
            return f"What are the known {modification_type} sites on {protein_name}?"
        elif question_type == "kinase" and site:
            return f"Which kinases phosphorylate {protein_name} at {site}?"
        elif question_type == "function" and site:
            return f"What is the functional significance of {modification_type} at {site} on {protein_name}?"
        else:
            raise ValueError("Invalid parameters for PTM prompt")

    @staticmethod
    def build_clinical_prompt(
        protein_name: str,
        disease: str,
        question_type: str = "biomarker"
    ) -> str:
        """
        Build clinical interpretation prompt.

        Args:
            protein_name: Protein name or ID
            disease: Disease or condition
            question_type: Type of question

        Returns:
            Formatted prompt string
        """
        if question_type == "biomarker":
            return f"Is {protein_name} a validated biomarker for {disease}?"
        elif question_type == "therapeutic":
            return f"Is {protein_name} a therapeutic target in {disease}? What drugs target it?"
        elif question_type == "mechanism":
            return f"What is the role of {protein_name} in {disease} pathogenesis?"
        else:
            raise ValueError("Invalid question_type for clinical prompt")
