"""
Hallucination scoring and classification.

This module provides tools for scoring LLM responses for hallucinations,
using both automated checks and manual annotation frameworks.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass


logger = logging.getLogger(__name__)


class HallucinationLevel(Enum):
    """Hallucination severity levels."""
    NO_HALLUCINATION = 0
    MINOR_ERROR = 1
    MAJOR_ERROR = 2
    FABRICATION = 3


class HallucinationType(Enum):
    """Types of hallucinations observed in proteomics responses."""
    FACTUAL_ERROR = "factual_error"
    FABRICATED_PROTEIN = "fabricated_protein"
    FABRICATED_PTM = "fabricated_ptm"
    FABRICATED_CITATION = "fabricated_citation"
    QUANTITATIVE_ERROR = "quantitative_error"
    FABRICATED_INTERACTION = "fabricated_interaction"
    WRONG_ISOFORM = "wrong_isoform"
    INCORRECT_LOCALIZATION = "incorrect_localization"


@dataclass
class HallucinationAnnotation:
    """Annotation of a hallucination in an LLM response."""
    hallucination_level: HallucinationLevel
    hallucination_types: List[HallucinationType]
    evidence: str
    confidence: float  # Annotator confidence 0-1
    annotator_id: str
    notes: Optional[str] = None


class HallucinationScorer:
    """Score LLM responses for hallucinations."""

    def __init__(
        self,
        protein_database: Optional[Dict] = None,
        ptm_database: Optional[Dict] = None,
        citation_database: Optional[Dict] = None
    ):
        """
        Initialize hallucination scorer.

        Args:
            protein_database: Dictionary of valid proteins (UniProt)
            ptm_database: Dictionary of validated PTMs (PhosphoSitePlus)
            citation_database: Dictionary of valid citations (PubMed)
        """
        self.protein_database = protein_database or {}
        self.ptm_database = ptm_database or {}
        self.citation_database = citation_database or {}

    def score_response(
        self,
        response: str,
        ground_truth: str,
        query_context: Dict
    ) -> Dict:
        """
        Score a response for hallucinations.

        Args:
            response: LLM response text
            ground_truth: Known correct answer
            query_context: Dictionary with query metadata

        Returns:
            Dictionary with hallucination score and details
        """
        # Automated checks
        protein_check = self._check_protein_validity(response)
        citation_check = self._check_citations(response)
        ptm_check = self._check_ptm_validity(response, query_context)

        # Combine checks
        has_hallucination = (
            not protein_check["valid"] or
            not citation_check["valid"] or
            not ptm_check["valid"]
        )

        hallucination_types = []
        if not protein_check["valid"]:
            hallucination_types.append(HallucinationType.FABRICATED_PROTEIN)
        if not citation_check["valid"]:
            hallucination_types.append(HallucinationType.FABRICATED_CITATION)
        if not ptm_check["valid"]:
            hallucination_types.append(HallucinationType.FABRICATED_PTM)

        # Determine severity
        if not has_hallucination:
            level = HallucinationLevel.NO_HALLUCINATION
        elif any([ptm_check.get("fabricated"), citation_check.get("fabricated")]):
            level = HallucinationLevel.FABRICATION
        else:
            # Determine based on impact
            level = self._assess_severity(response, ground_truth, hallucination_types)

        return {
            "has_hallucination": has_hallucination,
            "hallucination_level": level.value,
            "hallucination_level_name": level.name,
            "hallucination_types": [ht.value for ht in hallucination_types],
            "automated_checks": {
                "protein_check": protein_check,
                "citation_check": citation_check,
                "ptm_check": ptm_check,
            },
            "requires_manual_review": self._requires_manual_review(
                level, hallucination_types
            )
        }

    def _check_protein_validity(self, response: str) -> Dict:
        """
        Check if proteins mentioned in response are valid.

        Args:
            response: Response text

        Returns:
            Dictionary with validation results
        """
        # Extract UniProt IDs (simple regex, improve as needed)
        uniprot_pattern = r'\b[OPQ][0-9][A-Z0-9]{3}[0-9]\b|\b[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}\b'
        mentioned_ids = re.findall(uniprot_pattern, response)

        invalid_ids = []
        if self.protein_database:
            for protein_id in mentioned_ids:
                if protein_id not in self.protein_database:
                    invalid_ids.append(protein_id)

        return {
            "valid": len(invalid_ids) == 0,
            "mentioned_ids": mentioned_ids,
            "invalid_ids": invalid_ids,
            "count": len(mentioned_ids)
        }

    def _check_citations(self, response: str) -> Dict:
        """
        Check if citations in response are valid.

        Args:
            response: Response text

        Returns:
            Dictionary with citation validation results
        """
        # Extract PubMed IDs
        pmid_pattern = r'PMID:\s*(\d+)|PubMed\s+ID:\s*(\d+)'
        pmids = re.findall(pmid_pattern, response, re.IGNORECASE)
        pmids = [p[0] or p[1] for p in pmids]

        # Extract DOIs
        doi_pattern = r'\b10\.\d{4,}/[-._;()/:a-zA-Z0-9]+\b'
        dois = re.findall(doi_pattern, response)

        fabricated_pmids = []
        fabricated_dois = []

        if self.citation_database:
            for pmid in pmids:
                if pmid not in self.citation_database.get("pmids", []):
                    fabricated_pmids.append(pmid)

            for doi in dois:
                if doi not in self.citation_database.get("dois", []):
                    fabricated_dois.append(doi)

        has_fabrication = len(fabricated_pmids) > 0 or len(fabricated_dois) > 0

        return {
            "valid": not has_fabrication,
            "fabricated": has_fabrication,
            "pmids": pmids,
            "fabricated_pmids": fabricated_pmids,
            "dois": dois,
            "fabricated_dois": fabricated_dois
        }

    def _check_ptm_validity(self, response: str, query_context: Dict) -> Dict:
        """
        Check if PTMs mentioned are valid.

        Args:
            response: Response text
            query_context: Query metadata

        Returns:
            Dictionary with PTM validation results
        """
        # Extract phosphorylation sites (e.g., Ser123, S123, Thr456)
        phospho_pattern = r'(Ser|Thr|Tyr|S|T|Y)(\d+)'
        mentioned_sites = re.findall(phospho_pattern, response)
        mentioned_sites = [f"{aa}{pos}" for aa, pos in mentioned_sites]

        fabricated_sites = []
        protein = query_context.get("protein")

        if protein and self.ptm_database:
            validated_sites = self.ptm_database.get(protein, {}).get("phosphorylation", [])
            for site in mentioned_sites:
                if site not in validated_sites:
                    fabricated_sites.append(site)

        return {
            "valid": len(fabricated_sites) == 0,
            "fabricated": len(fabricated_sites) > 0,
            "mentioned_sites": mentioned_sites,
            "fabricated_sites": fabricated_sites
        }

    def _assess_severity(
        self,
        response: str,
        ground_truth: str,
        hallucination_types: List[HallucinationType]
    ) -> HallucinationLevel:
        """
        Assess hallucination severity based on types and context.

        Args:
            response: LLM response
            ground_truth: Correct answer
            hallucination_types: List of identified hallucination types

        Returns:
            HallucinationLevel enum
        """
        # High severity hallucinations
        severe_types = {
            HallucinationType.FABRICATED_PROTEIN,
            HallucinationType.FABRICATED_CITATION,
            HallucinationType.FABRICATED_PTM
        }

        if any(ht in severe_types for ht in hallucination_types):
            return HallucinationLevel.FABRICATION

        # Major errors
        major_types = {
            HallucinationType.FACTUAL_ERROR,
            HallucinationType.QUANTITATIVE_ERROR
        }

        if any(ht in major_types for ht in hallucination_types):
            return HallucinationLevel.MAJOR_ERROR

        # Default to minor error
        return HallucinationLevel.MINOR_ERROR

    def _requires_manual_review(
        self,
        level: HallucinationLevel,
        hallucination_types: List[HallucinationType]
    ) -> bool:
        """
        Determine if response requires manual expert review.

        Args:
            level: Hallucination severity level
            hallucination_types: Types of hallucinations detected

        Returns:
            True if manual review needed
        """
        # Always review fabrications
        if level == HallucinationLevel.FABRICATION:
            return True

        # Review major errors
        if level == HallucinationLevel.MAJOR_ERROR:
            return True

        # Review quantitative errors (subtle)
        if HallucinationType.QUANTITATIVE_ERROR in hallucination_types:
            return True

        return False

    def create_manual_annotation(
        self,
        hallucination_level: HallucinationLevel,
        hallucination_types: List[HallucinationType],
        evidence: str,
        confidence: float,
        annotator_id: str,
        notes: Optional[str] = None
    ) -> HallucinationAnnotation:
        """
        Create manual hallucination annotation.

        Args:
            hallucination_level: Severity level
            hallucination_types: List of hallucination types
            evidence: Supporting evidence
            confidence: Annotator confidence (0-1)
            annotator_id: Identifier for annotator
            notes: Optional additional notes

        Returns:
            HallucinationAnnotation object
        """
        return HallucinationAnnotation(
            hallucination_level=hallucination_level,
            hallucination_types=hallucination_types,
            evidence=evidence,
            confidence=confidence,
            annotator_id=annotator_id,
            notes=notes
        )

    @staticmethod
    def calculate_inter_rater_agreement(
        annotations1: List[HallucinationAnnotation],
        annotations2: List[HallucinationAnnotation]
    ) -> Dict:
        """
        Calculate inter-rater agreement (Cohen's kappa).

        Args:
            annotations1: Annotations from first rater
            annotations2: Annotations from second rater

        Returns:
            Dictionary with agreement metrics
        """
        if len(annotations1) != len(annotations2):
            raise ValueError("Annotation lists must have same length")

        n = len(annotations1)
        if n == 0:
            return {"kappa": None, "agreement": None}

        # Calculate observed agreement
        agreements = sum(
            1 for a1, a2 in zip(annotations1, annotations2)
            if a1.hallucination_level == a2.hallucination_level
        )
        po = agreements / n

        # Calculate expected agreement
        levels1 = [a.hallucination_level for a in annotations1]
        levels2 = [a.hallucination_level for a in annotations2]

        pe = 0
        for level in HallucinationLevel:
            p1 = levels1.count(level) / n
            p2 = levels2.count(level) / n
            pe += p1 * p2

        # Cohen's kappa
        kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0

        return {
            "kappa": kappa,
            "observed_agreement": po,
            "expected_agreement": pe,
            "n": n,
            "interpretation": _interpret_kappa(kappa)
        }


def _interpret_kappa(kappa: float) -> str:
    """Interpret Cohen's kappa value."""
    if kappa < 0:
        return "Poor"
    elif kappa < 0.20:
        return "Slight"
    elif kappa < 0.40:
        return "Fair"
    elif kappa < 0.60:
        return "Moderate"
    elif kappa < 0.80:
        return "Substantial"
    else:
        return "Almost Perfect"
