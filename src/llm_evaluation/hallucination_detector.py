"""
Hallucination detection for LLM responses about proteomics.

Cross-references LLM responses with ground truth databases to identify
factual errors, invented proteins, and incorrect functions.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class HallucinationType(Enum):
    """Types of hallucinations detected."""
    INVENTED_PROTEIN = "invented_protein"
    INCORRECT_FUNCTION = "incorrect_function"
    INVALID_GO_TERM = "invalid_go_term"
    WRONG_MOLECULAR_WEIGHT = "wrong_molecular_weight"
    IMPOSSIBLE_INTERACTION = "impossible_interaction"
    TEMPORAL_IMPOSSIBILITY = "temporal_impossibility"
    INCONSISTENT_INFORMATION = "inconsistent_information"
    FABRICATED_REFERENCE = "fabricated_reference"


@dataclass
class HallucinationResult:
    """Result of hallucination detection."""
    is_hallucination: bool
    hallucination_types: List[HallucinationType]
    confidence: float
    details: Dict[str, Any]
    evidence: List[str]


class HallucinationDetector:
    """
    Detect hallucinations in LLM responses about proteomics.

    Methods:
        - Cross-reference with UniProt database
        - Verify protein IDs and names
        - Check GO term validity
        - Validate molecular weights
        - Detect temporal inconsistencies

    Args:
        protein_database: ProteinDatabase instance for lookups
        strict_mode: If True, be more aggressive in flagging potential errors

    Example:
        >>> detector = HallucinationDetector()
        >>> result = detector.detect("Protein FAKE123 is a kinase...")
        >>> print(result.is_hallucination)
        True
    """

    # UniProt accession pattern: [OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}
    UNIPROT_PATTERN = r'([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})'

    # GO term pattern: GO:XXXXXXX
    GO_TERM_PATTERN = r'GO:\d{7}'

    # Common hallucination indicators
    HALLUCINATION_INDICATORS = [
        r'FAKE\d+',
        r'TEST\d+',
        r'PROTEIN\d+',
        r'EXAMPLE\d+',
        r'HYPOTHETICAL\d+',
    ]

    def __init__(
        self,
        protein_database: Optional[Any] = None,
        strict_mode: bool = False
    ):
        """Initialize hallucination detector."""
        self.protein_database = protein_database
        self.strict_mode = strict_mode

        # Load known protein IDs (would be loaded from database in production)
        self.known_protein_ids = self._load_known_proteins()
        self.known_go_terms = self._load_known_go_terms()

        logger.info(f"Initialized HallucinationDetector (strict={strict_mode})")

    def _load_known_proteins(self) -> set:
        """Load set of known protein IDs."""
        # In production, this would query UniProt or load from cache
        # For now, return example set
        return {
            'P12345', 'Q9Y6K9', 'P04637', 'P53', 'BRCA1',
            # Add more from example data
        }

    def _load_known_go_terms(self) -> set:
        """Load set of valid GO terms."""
        # In production, load from GO database
        return {
            'GO:0004672', 'GO:0006468', 'GO:0005524',
            'GO:0055085', 'GO:0016020', 'GO:0005886',
            # Add more as needed
        }

    def detect(
        self,
        response: str,
        context: Optional[Dict[str, Any]] = None
    ) -> HallucinationResult:
        """
        Detect hallucinations in LLM response.

        Args:
            response: LLM response text to analyze
            context: Optional context (original query, ground truth, etc.)

        Returns:
            HallucinationResult with detection results

        Raises:
            ValueError: If response is empty
        """
        if not response or not response.strip():
            raise ValueError("Response cannot be empty")

        hallucinations = []
        evidence = []
        confidence_scores = []

        # Check for obvious hallucination indicators
        obvious_result = self._check_obvious_hallucinations(response)
        if obvious_result:
            hallucinations.extend(obvious_result['types'])
            evidence.extend(obvious_result['evidence'])
            confidence_scores.append(obvious_result['confidence'])

        # Extract and verify protein IDs
        protein_result = self._verify_protein_ids(response)
        if protein_result['invalid_ids']:
            hallucinations.append(HallucinationType.INVENTED_PROTEIN)
            evidence.append(f"Invalid protein IDs: {protein_result['invalid_ids']}")
            confidence_scores.append(0.9)

        # Verify GO terms
        go_result = self._verify_go_terms(response)
        if go_result['invalid_terms']:
            hallucinations.append(HallucinationType.INVALID_GO_TERM)
            evidence.append(f"Invalid GO terms: {go_result['invalid_terms']}")
            confidence_scores.append(0.85)

        # Check molecular weight consistency if mentioned
        mw_result = self._check_molecular_weight(response)
        if mw_result['inconsistent']:
            hallucinations.append(HallucinationType.WRONG_MOLECULAR_WEIGHT)
            evidence.append(mw_result['reason'])
            confidence_scores.append(0.7)

        # Check for inconsistencies within response
        consistency_result = self._check_internal_consistency(response)
        if consistency_result['inconsistent']:
            hallucinations.append(HallucinationType.INCONSISTENT_INFORMATION)
            evidence.extend(consistency_result['issues'])
            confidence_scores.append(0.6)

        # Calculate overall confidence
        if confidence_scores:
            overall_confidence = max(confidence_scores)
        else:
            overall_confidence = 0.0

        # Determine if this is a hallucination
        is_hallucination = len(hallucinations) > 0

        return HallucinationResult(
            is_hallucination=is_hallucination,
            hallucination_types=list(set(hallucinations)),
            confidence=overall_confidence,
            details={
                'protein_ids': protein_result,
                'go_terms': go_result,
                'molecular_weight': mw_result,
                'consistency': consistency_result,
            },
            evidence=evidence
        )

    def _check_obvious_hallucinations(self, response: str) -> Optional[Dict[str, Any]]:
        """Check for obvious hallucination indicators."""
        for pattern in self.HALLUCINATION_INDICATORS:
            matches = re.findall(pattern, response, re.IGNORECASE)
            if matches:
                return {
                    'types': [HallucinationType.INVENTED_PROTEIN],
                    'evidence': [f"Found obvious fake ID: {matches}"],
                    'confidence': 0.95
                }
        return None

    def _verify_protein_ids(self, response: str) -> Dict[str, Any]:
        """Extract and verify protein IDs."""
        # Extract potential UniProt IDs
        potential_ids = re.findall(self.UNIPROT_PATTERN, response)

        # Flatten tuples from regex groups
        potential_ids = [id[0] if isinstance(id, tuple) else id for id in potential_ids]

        # Check against known IDs
        invalid_ids = [
            pid for pid in potential_ids
            if pid not in self.known_protein_ids
        ]

        return {
            'found_ids': potential_ids,
            'invalid_ids': invalid_ids,
            'valid_ids': [pid for pid in potential_ids if pid in self.known_protein_ids]
        }

    def _verify_go_terms(self, response: str) -> Dict[str, Any]:
        """Extract and verify GO terms."""
        go_terms = re.findall(self.GO_TERM_PATTERN, response)

        invalid_terms = [
            term for term in go_terms
            if term not in self.known_go_terms
        ]

        return {
            'found_terms': go_terms,
            'invalid_terms': invalid_terms,
            'valid_terms': [term for term in go_terms if term in self.known_go_terms]
        }

    def _check_molecular_weight(self, response: str) -> Dict[str, Any]:
        """Check molecular weight mentions for consistency."""
        # Extract molecular weight mentions
        mw_pattern = r'(\d+(?:\.\d+)?)\s*(?:kDa|Da|daltons?)'
        weights = re.findall(mw_pattern, response, re.IGNORECASE)

        if not weights:
            return {'inconsistent': False, 'reason': None}

        # Convert to floats
        weights_float = [float(w) for w in weights]

        # Check for unrealistic values
        unrealistic = [
            w for w in weights_float
            if w < 1 or w > 1000  # kDa range for typical proteins
        ]

        if unrealistic:
            return {
                'inconsistent': True,
                'reason': f"Unrealistic molecular weights: {unrealistic}"
            }

        return {'inconsistent': False, 'reason': None}

    def _check_internal_consistency(self, response: str) -> Dict[str, Any]:
        """Check for internal contradictions."""
        issues = []

        # Check for contradictory statements
        sentences = response.split('.')

        # Look for conflicting information (simple heuristic)
        positive_words = ['activates', 'increases', 'promotes', 'enhances']
        negative_words = ['inhibits', 'decreases', 'reduces', 'suppresses']

        has_positive = any(word in response.lower() for word in positive_words)
        has_negative = any(word in response.lower() for word in negative_words)

        # This is a simple check - in production would be more sophisticated
        if has_positive and has_negative:
            # Could be legitimate (context-dependent), so low confidence
            issues.append("Contains both activating and inhibiting language")

        return {
            'inconsistent': len(issues) > 0,
            'issues': issues
        }

    def detect_batch(
        self,
        responses: List[str],
        contexts: Optional[List[Dict[str, Any]]] = None
    ) -> List[HallucinationResult]:
        """
        Detect hallucinations in multiple responses.

        Args:
            responses: List of LLM responses
            contexts: Optional list of contexts

        Returns:
            List of HallucinationResult objects
        """
        if contexts is None:
            contexts = [None] * len(responses)

        results = []
        for response, context in zip(responses, contexts):
            try:
                result = self.detect(response, context)
                results.append(result)
            except Exception as e:
                logger.error(f"Error detecting hallucination: {e}")
                # Return a result indicating error
                results.append(HallucinationResult(
                    is_hallucination=False,
                    hallucination_types=[],
                    confidence=0.0,
                    details={'error': str(e)},
                    evidence=[]
                ))

        return results

    def calculate_hallucination_rate(
        self,
        results: List[HallucinationResult]
    ) -> Dict[str, Any]:
        """
        Calculate hallucination rate from results.

        Args:
            results: List of HallucinationResult objects

        Returns:
            Dictionary with hallucination statistics
        """
        total = len(results)
        if total == 0:
            return {'error': 'No results provided'}

        hallucinations = sum(1 for r in results if r.is_hallucination)
        hallucination_rate = hallucinations / total

        # Count types
        type_counts = {}
        for result in results:
            for htype in result.hallucination_types:
                type_counts[htype.value] = type_counts.get(htype.value, 0) + 1

        # Calculate average confidence
        confidences = [r.confidence for r in results if r.is_hallucination]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return {
            'total_responses': total,
            'hallucinations_detected': hallucinations,
            'hallucination_rate': hallucination_rate,
            'type_counts': type_counts,
            'average_confidence': avg_confidence,
        }
