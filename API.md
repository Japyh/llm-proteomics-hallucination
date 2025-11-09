# API Reference

Complete API documentation for the LLM Proteomics Hallucination Study package.

---

## LLM Clients

### src.llm_evaluation.llm_client

#### LLMClient

Base class for LLM clients.

```python
class LLMClient:
    def __init__(self, model: str, api_key: str):
        """Initialize LLM client."""
        
    def query(self, prompt: str, **kwargs) -> str:
        """Send query to LLM."""
```

#### GPT4Client

```python
from src.llm_evaluation.llm_client import GPT4Client

client = GPT4Client(api_key=os.getenv('OPENAI_API_KEY'))
response = client.query(
    prompt="What is the function of insulin?",
    max_tokens=500,
    temperature=0.7
)
```

#### ClaudeClient

```python
from src.llm_evaluation.llm_client import ClaudeClient

client = ClaudeClient(api_key=os.getenv('ANTHROPIC_API_KEY'))
response = client.query(
    prompt="What is the function of insulin?",
    max_tokens=500
)
```

#### GeminiClient

```python
from src.llm_evaluation.llm_client import GeminiClient

client = GeminiClient(api_key=os.getenv('GOOGLE_API_KEY'))
response = client.query(
    prompt="What is the function of insulin?"
)
```

---

## Hallucination Detection

### src.llm_evaluation.hallucination_detector

#### HallucinationDetector

```python
class HallucinationDetector:
    def detect(
        self,
        query: str,
        response: str,
        ground_truth: str
    ) -> Dict[str, Any]:
        """
        Detect hallucinations in LLM response.
        
        Args:
            query: Original query text
            response: LLM response
            ground_truth: Validated correct answer
            
        Returns:
            Dict with:
                - is_hallucination: bool
                - severity: int (0-3)
                - explanation: str
        """
```

**Example**:
```python
from src.llm_evaluation.hallucination_detector import HallucinationDetector

detector = HallucinationDetector()
result = detector.detect(
    query="What is the function of HBB?",
    response="HBB encodes hemoglobin beta...",
    ground_truth="Hemoglobin subunit beta is involved in oxygen transport..."
)

print(result['is_hallucination'])  # False
print(result['severity'])  # 0
```

---

## Statistical Analysis

### src.analysis.statistical_tests

#### chi_square_test

```python
def chi_square_test(
    data: pd.DataFrame,
    group1: str,
    group2: str
) -> Dict[str, float]:
    """
    Perform chi-square test.
    
    Returns:
        Dict with p_value, statistic, significant
    """
```

#### logistic_regression

```python
def logistic_regression(
    data: pd.DataFrame,
    outcome: str,
    predictors: List[str]
) -> RegressionResult:
    """Multivariable logistic regression."""
```

**Example**:
```python
from src.analysis.statistical_tests import chi_square_test

result = chi_square_test(
    data=df,
    group1='GPT-4 Turbo',
    group2='Claude 3 Sonnet'
)

print(f"p-value: {result['p_value']:.4f}")
print(f"Significant: {result['significant']}")
```

---

## Metrics

### src.analysis.metrics

#### hallucination_rate

```python
def hallucination_rate(
    predictions: List[bool],
    ci_level: float = 0.95
) -> Dict[str, float]:
    """
    Calculate hallucination rate with confidence interval.
    
    Returns:
        Dict with rate, ci_lower, ci_upper
    """
```

#### cohen_kappa

```python
def cohen_kappa(
    rater1: List[int],
    rater2: List[int]
) -> float:
    """Calculate Cohen's kappa for inter-rater reliability."""
```

---

## Data Processing

### src.data_processing.protein_database

#### UniProtClient

```python
class UniProtClient:
    def get_protein(self, uniprot_id: str) -> Dict[str, Any]:
        """Fetch protein data from UniProt."""
        
    def search_proteins(self, query: str) -> List[Dict]:
        """Search UniProt database."""
```

**Example**:
```python
from src.data_processing.protein_database import UniProtClient

client = UniProtClient()
protein = client.get_protein('P68871')  # HBB

print(protein['gene_name'])  # HBB
print(protein['function'])   # Oxygen transport...
```

---

## Utilities

### src.utils.config

#### load_config

```python
def load_config(config_file: str = None) -> Dict[str, Any]:
    """Load configuration from file or environment."""
```

#### get_api_key

```python
def get_api_key(provider: str) -> str:
    """
    Get API key for provider.
    
    Args:
        provider: 'openai', 'anthropic', or 'google'
        
    Returns:
        API key string
        
    Raises:
        ValueError: If key not found
    """
```

### src.utils.logger

#### get_logger

```python
def get_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """Get configured logger."""
```

**Example**:
```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing started")
logger.debug("Debug information")
```

---

## Data Models

### Query

```python
class Query:
    query_id: str
    query_text: str
    domain: str
    complexity: str
    protein_prevalence: str
    expected_answer: str
```

### Response

```python
class Response:
    query_id: str
    model: str
    response_text: str
    timestamp: str
    metadata: Dict
```

### HallucinationResult

```python
class HallucinationResult:
    query_id: str
    is_hallucination: bool
    severity: int  # 0-3
    explanation: str
    confidence: float
```

---

## Error Handling

### Exceptions

```python
class APIError(Exception):
    """Raised when API call fails."""

class ValidationError(Exception):
    """Raised when data validation fails."""

class ConfigError(Exception):
    """Raised when configuration is invalid."""
```

**Usage**:
```python
from src.llm_evaluation.llm_client import LLMClient, APIError

try:
    response = client.query(prompt)
except APIError as e:
    logger.error(f"API error: {e}")
    # Handle error
```

---

## Constants

```python
# src/utils/constants.py

MODELS = {
    'gpt-4': 'gpt-4-0125-preview',
    'claude': 'claude-3-sonnet-20240229',
    'gemini': 'gemini-1.5-pro-001'
}

SEVERITY_LEVELS = {
    0: 'No error',
    1: 'Minor error',
    2: 'Major error',
    3: 'Fabrication'
}

DOMAINS = [
    'protein_identification',
    'quantitative_expression',
    'post_translational_modifications',
    'protein_interactions',
    'clinical_interpretation'
]
```

---

## Type Hints

```python
from typing import Dict, List, Any, Optional, Union

QueryDict = Dict[str, Any]
ResponseDict = Dict[str, Any]
MetricsDict = Dict[str, float]
```

---

## Configuration

### Environment Variables

```bash
# API Keys
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key

# Logging
LOG_LEVEL=INFO

# Paths
DATA_DIR=./data
RESULTS_DIR=./data/results
```

### Configuration File

```python
# config.yaml
models:
  gpt4:
    model: gpt-4-0125-preview
    temperature: 0.7
    max_tokens: 500
  claude:
    model: claude-3-sonnet-20240229
    max_tokens: 500
    
analysis:
  confidence_level: 0.95
  bonferroni_correction: true
```

---

## Full Example

```python
import os
from src.llm_evaluation.llm_client import GPT4Client
from src.llm_evaluation.hallucination_detector import HallucinationDetector
from src.analysis.metrics import hallucination_rate

# Initialize
client = GPT4Client(api_key=os.getenv('OPENAI_API_KEY'))
detector = HallucinationDetector()

# Load queries
with open('data/queries/queries_all.json') as f:
    queries = json.load(f)

# Process
results = []
for query in queries[:10]:  # First 10
    response = client.query(query['query_text'])
    result = detector.detect(
        query=query['query_text'],
        response=response,
        ground_truth=query['expected_answer']
    )
    results.append(result['is_hallucination'])

# Analyze
rate = hallucination_rate(results)
print(f"Hallucination rate: {rate['rate']:.1f}%")
print(f"95% CI: [{rate['ci_lower']:.1f}, {rate['ci_upper']:.1f}]")
```

---

**For more examples, see**: `examples/complete_example.py`

**Last Updated**: November 9, 2024
