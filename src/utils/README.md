# Utilities Module

Helper functions and utilities.

---

## Modules

### config.py

Configuration management.

**Functions**:
- `load_config()`: Load configuration
- `get_api_key()`: Get API keys from environment

### logger.py

Logging setup and utilities.

**Usage**:
```python
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing started")
```

### validators.py

Data validation functions.

**Functions**:
- `validate_query()`: Validate query format
- `validate_protein_id()`: Validate UniProt ID
- `validate_response()`: Validate LLM response

### helpers.py

General helper functions.

**Functions**:
- `load_json()`: Load JSON with error handling
- `save_results()`: Save results to CSV
- `format_duration()`: Format time durations
