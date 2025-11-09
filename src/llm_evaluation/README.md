# LLM Evaluation Module

LLM client implementations and hallucination detection framework.

---

## Modules

### llm_client.py

API clients for different LLM providers.

**Classes**:
- `LLMClient`: Base client class
- `GPT4Client`: OpenAI GPT-4 client
- `ClaudeClient`: Anthropic Claude client
- `GeminiClient`: Google Gemini client

**Usage**:
```python
from src.llm_evaluation.llm_client import GPT4Client

client = GPT4Client(api_key=os.getenv('OPENAI_API_KEY'))
response = client.query("What is the function of insulin?")
```

### hallucination_detector.py

Detect and classify hallucinations in LLM responses.

**Classes**:
- `HallucinationDetector`: Main detector class

**Usage**:
```python
from src.llm_evaluation.hallucination_detector import HallucinationDetector

detector = HallucinationDetector()
result = detector.detect(query, response, ground_truth)
print(result['is_hallucination'], result['severity'])
```

### benchmark_suite.py

Benchmarking tools for evaluating LLM performance.

### prompt_templates.py

Standardized prompt templates for consistent evaluation.

---

**For detailed API documentation, see parent [API.md](../../API.md)**
