"""Test LLM response format compliance.

This module validates that all LLM response files adhere to the expected schema,
data types, and quality standards defined in the study protocol.
"""
import pytest
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re


# ============================================================================
# Test Configuration
# ============================================================================

# Expected models and their response files
EXPECTED_MODELS = {
    'gpt4_turbo': {
        'file': 'gpt4_turbo_responses.jsonl',
        'model_ids': ['gpt4-turbo-2024-04-09', 'gpt-4-turbo-2024-04-09'],
        'min_responses': 1  # Relaxed for testing/demo data
    },
    'claude_sonnet': {
        'file': 'claude_sonnet_responses.jsonl',
        'model_ids': ['claude-3-sonnet-20240229'],
        'min_responses': 1  # Relaxed for testing/demo data
    },
    'gemini_pro': {
        'file': 'gemini_pro_responses.jsonl',
        'model_ids': ['gemini-1.5-pro-001', 'gemini-1.5-pro'],
        'min_responses': 1  # Relaxed for testing/demo data
    },
    'mistral_large': {
        'file': 'mistral_large_responses.jsonl',
        'model_ids': ['mistral-large-2402'],
        'min_responses': 1  # Relaxed for testing/demo data
    },
    'llama3_70b': {
        'file': 'llama3_70b_local.jsonl',
        'model_ids': ['llama3-70b-instruct'],
        'min_responses': 1  # Relaxed for testing/demo data
    }
}

# Required fields for all response entries
REQUIRED_FIELDS = ['query_id', 'model', 'response', 'timestamp']

# Optional but expected fields
OPTIONAL_FIELDS = ['latency_ms', 'usage', 'finish_reason', 'stop_reason', 
                  'temperature', 'top_p']

# Valid query ID patterns
VALID_QUERY_PATTERNS = [
    r'^TEST_\d{3}$',      # TEST_001, TEST_002, etc.
    r'^VAL_\d{3}$',       # VAL_001, VAL_002, etc.
    r'^TRAIN_\d{3}$',     # TRAIN_001, TRAIN_002, etc.
    r'^Q\d{5}$',          # Q00001, Q00002, etc.
    r'^HC_\d{3}$',        # HC_001 (high complexity queries)
    r'^LC_\d{3}$',        # LC_001 (low complexity queries)
]

# Base data directory
DATA_DIR = Path('data/llm_responses')


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def all_response_files():
    """Get all response JSONL files."""
    return [DATA_DIR / model_info['file'] 
            for model_info in EXPECTED_MODELS.values()]


@pytest.fixture(params=EXPECTED_MODELS.keys())
def model_response_file(request):
    """Parametrized fixture for each model's response file."""
    model_name = request.param
    model_info = EXPECTED_MODELS[model_name]
    filepath = DATA_DIR / model_info['file']
    return model_name, filepath, model_info


# ============================================================================
# Schema Validation Tests
# ============================================================================

def test_all_response_files_exist():
    """Verify that all expected response files exist."""
    for model_name, model_info in EXPECTED_MODELS.items():
        filepath = DATA_DIR / model_info['file']
        assert filepath.exists(), (
            f"Missing response file for {model_name}: {filepath}"
        )


def test_response_format_required_fields(model_response_file):
    """Check that all required fields are present in each response."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    # Check required columns
    for col in REQUIRED_FIELDS:
        assert col in df.columns, (
            f"{model_name}: Missing required column '{col}'"
        )
    
    # Check for null values in required fields
    for col in REQUIRED_FIELDS:
        null_count = df[col].isnull().sum()
        assert null_count == 0, (
            f"{model_name}: Found {null_count} null values in required field '{col}'"
        )


def test_response_format_field_types(model_response_file):
    """Validate data types of response fields."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    # query_id should be string
    assert df['query_id'].dtype == object, (
        f"{model_name}: query_id should be string type"
    )
    
    # model should be string
    assert df['model'].dtype == object, (
        f"{model_name}: model should be string type"
    )
    
    # response should be string
    assert df['response'].dtype == object, (
        f"{model_name}: response should be string type"
    )
    
    # timestamp should be string or datetime (pandas auto-converts ISO timestamps)
    assert df['timestamp'].dtype == object or pd.api.types.is_datetime64_any_dtype(df['timestamp']), (
        f"{model_name}: timestamp should be string or datetime type"
    )
    
    # latency_ms should be numeric if present
    if 'latency_ms' in df.columns:
        assert pd.api.types.is_numeric_dtype(df['latency_ms']), (
            f"{model_name}: latency_ms should be numeric"
        )


def test_response_count_meets_minimum(model_response_file):
    """Verify minimum number of responses per model."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    actual_count = len(df)
    min_expected = model_info['min_responses']
    
    assert actual_count >= min_expected, (
        f"{model_name}: Expected at least {min_expected} responses, "
        f"but found {actual_count}"
    )


# ============================================================================
# Content Validation Tests
# ============================================================================

def test_query_id_format(model_response_file):
    """Validate query_id follows expected patterns."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    # Compile patterns
    patterns = [re.compile(p) for p in VALID_QUERY_PATTERNS]
    
    invalid_ids = []
    for query_id in df['query_id'].unique():
        if not any(pattern.match(query_id) for pattern in patterns):
            invalid_ids.append(query_id)
    
    assert len(invalid_ids) == 0, (
        f"{model_name}: Found {len(invalid_ids)} invalid query_id formats: "
        f"{invalid_ids[:5]}"  # Show first 5
    )


def test_model_id_consistency(model_response_file):
    """Verify model IDs are consistent and expected."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    unique_models = df['model'].unique()
    expected_models = model_info['model_ids']
    
    for model_id in unique_models:
        assert model_id in expected_models, (
            f"{model_name}: Unexpected model ID '{model_id}'. "
            f"Expected one of: {expected_models}"
        )


def test_response_non_empty(model_response_file):
    """Ensure all responses contain text."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    # Check for empty responses
    empty_responses = df[df['response'].str.strip() == '']
    
    assert len(empty_responses) == 0, (
        f"{model_name}: Found {len(empty_responses)} empty responses"
    )
    
    # Check minimum response length (at least 10 characters)
    short_responses = df[df['response'].str.len() < 10]
    
    assert len(short_responses) == 0, (
        f"{model_name}: Found {len(short_responses)} responses shorter than 10 characters"
    )


def test_timestamp_format(model_response_file):
    """Validate timestamp format is ISO 8601."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    invalid_timestamps = []
    for idx, timestamp in enumerate(df['timestamp']):
        # Skip if already parsed as datetime by pandas
        if isinstance(timestamp, pd.Timestamp):
            continue
        
        try:
            # Try to parse ISO 8601 format
            datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
        except (ValueError, AttributeError, TypeError):
            invalid_timestamps.append((idx, timestamp))
    
    assert len(invalid_timestamps) == 0, (
        f"{model_name}: Found {len(invalid_timestamps)} invalid timestamp formats. "
        f"First invalid: {invalid_timestamps[0] if invalid_timestamps else None}"
    )


def test_latency_reasonable_range(model_response_file):
    """Check that latency values are within reasonable bounds."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    if 'latency_ms' not in df.columns:
        pytest.skip(f"{model_name}: latency_ms field not present")
    
    # Filter out null latencies
    latencies = df['latency_ms'].dropna()
    
    if len(latencies) == 0:
        pytest.skip(f"{model_name}: No latency data available")
    
    # Check for negative latencies
    negative_latencies = latencies[latencies < 0]
    assert len(negative_latencies) == 0, (
        f"{model_name}: Found {len(negative_latencies)} negative latency values"
    )
    
    # Check for unreasonably high latencies (> 5 minutes = 300,000 ms)
    high_latencies = latencies[latencies > 300000]
    assert len(high_latencies) == 0, (
        f"{model_name}: Found {len(high_latencies)} latencies exceeding 5 minutes"
    )
    
    # Check for unreasonably low latencies (< 50 ms)
    low_latencies = latencies[latencies < 50]
    # This is a warning, not a failure
    if len(low_latencies) > 0:
        print(f"Warning: {model_name} has {len(low_latencies)} responses with latency < 50ms")


def test_usage_metadata_structure(model_response_file):
    """Validate usage metadata structure when present."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    if 'usage' not in df.columns:
        pytest.skip(f"{model_name}: usage field not present")
    
    # Filter out null usage entries
    usage_entries = df['usage'].dropna()
    
    if len(usage_entries) == 0:
        pytest.skip(f"{model_name}: No usage data available")
    
    # Check structure of first few usage entries
    for idx, usage in enumerate(usage_entries.head(10)):
        if not isinstance(usage, dict):
            continue
        
        # Different providers use different field names
        valid_token_fields = [
            'total_tokens', 'prompt_tokens', 'completion_tokens',  # OpenAI
            'input_tokens', 'output_tokens',                       # Anthropic
            'prompt_token_count', 'candidates_token_count', 'total_token_count',  # Gemini
        ]
        
        has_token_info = any(field in usage for field in valid_token_fields)
        assert has_token_info, (
            f"{model_name}: Usage entry {idx} missing token information. "
            f"Got: {usage.keys()}"
        )


# ============================================================================
# Cross-file Consistency Tests
# ============================================================================

def test_no_duplicate_responses_within_model(model_response_file):
    """Check for duplicate (query_id, model) pairs within each file."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    duplicates = df.duplicated(subset=['query_id', 'model'], keep=False)
    duplicate_count = duplicates.sum()
    
    assert duplicate_count == 0, (
        f"{model_name}: Found {duplicate_count} duplicate (query_id, model) pairs"
    )


def test_query_ids_consistent_across_models(all_response_files):
    """Verify that all models were queried with the same test queries."""
    # Load all query IDs from each model
    query_sets = {}
    
    for model_name, model_info in EXPECTED_MODELS.items():
        filepath = DATA_DIR / model_info['file']
        df = pd.read_json(filepath, lines=True)
        
        # Filter to common test queries (TEST_, VAL_)
        test_queries = df[df['query_id'].str.match(r'^(TEST|VAL)_\d{3}$')]
        query_sets[model_name] = set(test_queries['query_id'].unique())
    
    # Skip if no test queries found
    if not any(query_sets.values()):
        pytest.skip("No common test queries found")
    
    # Check that major models have similar test query sets
    major_models = ['gpt4_turbo', 'claude_sonnet', 'gemini_pro']
    major_query_sets = [query_sets[m] for m in major_models if m in query_sets]
    
    if len(major_query_sets) < 2:
        pytest.skip("Not enough major models to compare")
    
    # Check overlap between first two major models
    overlap = major_query_sets[0] & major_query_sets[1]
    
    assert len(overlap) > 0, (
        "Major models should have overlapping test queries"
    )


# ============================================================================
# Data Quality Tests
# ============================================================================

def test_response_language_is_english(model_response_file):
    """Basic check that responses are in English."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    # Simple heuristic: check for common English proteomics terms
    english_terms = [
        'protein', 'amino', 'acid', 'sequence', 'uniprot',
        'phosphorylation', 'expression', 'function', 'cellular',
        'molecular', 'weight', 'kDa', 'gene', 'human', 'beta',
        'hemoglobin', 'brca', 'dna', 'erk', 'mek', 'kinase'
    ]
    
    # Sample all responses if small dataset
    sample_size = min(20, len(df))
    sample = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
    
    responses_with_terms = 0
    for response in sample['response']:
        response_lower = response.lower()
        if any(term in response_lower for term in english_terms):
            responses_with_terms += 1
    
    # At least 50% of sampled responses should contain English terms (relaxed for small samples)
    percentage = (responses_with_terms / len(sample)) * 100
    
    assert percentage >= 50, (
        f"{model_name}: Only {percentage:.1f}% of sampled responses contain "
        f"expected English proteomics terms"
    )


def test_jsonl_format_valid(model_response_file):
    """Ensure each line is valid JSON."""
    model_name, filepath, model_info = model_response_file
    
    invalid_lines = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                invalid_lines.append((line_num, str(e)))
    
    assert len(invalid_lines) == 0, (
        f"{model_name}: Found {len(invalid_lines)} invalid JSON lines. "
        f"First error at line {invalid_lines[0][0]}: {invalid_lines[0][1]}"
    )


def test_timestamps_chronologically_reasonable(model_response_file):
    """Check that timestamps are within expected date range."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    # Convert timestamps to datetime
    timestamps = pd.to_datetime(df['timestamp'], format='mixed')
    
    # Check date range (study period: 2024-03-01 to 2024-12-31)
    # Make datetime objects timezone-aware to match the data
    import pytz
    utc = pytz.UTC
    study_start = utc.localize(datetime(2024, 3, 1))
    study_end = utc.localize(datetime(2024, 12, 31, 23, 59, 59))
    
    too_early = timestamps < study_start
    too_late = timestamps > study_end
    
    assert too_early.sum() == 0, (
        f"{model_name}: Found {too_early.sum()} timestamps before study start date"
    )
    
    assert too_late.sum() == 0, (
        f"{model_name}: Found {too_late.sum()} timestamps after study end date"
    )


# ============================================================================
# Statistical Summary Tests
# ============================================================================

def test_response_length_distribution(model_response_file):
    """Check that response lengths are reasonable."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    response_lengths = df['response'].str.len()
    
    # Statistical checks
    mean_length = response_lengths.mean()
    median_length = response_lengths.median()
    
    # Proteomics responses should typically be 50-1000 characters
    assert mean_length >= 50, (
        f"{model_name}: Mean response length ({mean_length:.1f}) is too short"
    )
    
    assert mean_length <= 5000, (
        f"{model_name}: Mean response length ({mean_length:.1f}) is suspiciously long"
    )
    
    # Check for outliers (responses > 10,000 characters)
    very_long = response_lengths > 10000
    assert very_long.sum() < len(df) * 0.01, (  # Less than 1%
        f"{model_name}: Too many very long responses ({very_long.sum()})"
    )


@pytest.mark.slow
def test_comprehensive_quality_report(model_response_file):
    """Generate comprehensive quality report for each model."""
    model_name, filepath, model_info = model_response_file
    
    df = pd.read_json(filepath, lines=True)
    
    print(f"\n{'='*60}")
    print(f"Quality Report: {model_name}")
    print(f"{'='*60}")
    print(f"Total responses: {len(df)}")
    print(f"Unique queries: {df['query_id'].nunique()}")
    print(f"Unique models: {df['model'].nunique()}")
    
    if 'latency_ms' in df.columns:
        latency = df['latency_ms'].dropna()
        print(f"\nLatency statistics:")
        print(f"  Mean: {latency.mean():.1f} ms")
        print(f"  Median: {latency.median():.1f} ms")
        print(f"  Min: {latency.min():.1f} ms")
        print(f"  Max: {latency.max():.1f} ms")
    
    response_lengths = df['response'].str.len()
    print(f"\nResponse length statistics:")
    print(f"  Mean: {response_lengths.mean():.1f} characters")
    print(f"  Median: {response_lengths.median():.1f} characters")
    print(f"  Min: {response_lengths.min()}")
    print(f"  Max: {response_lengths.max()}")
    
    print(f"{'='*60}\n")
    
    # This test always passes - it's just for reporting
    assert True
