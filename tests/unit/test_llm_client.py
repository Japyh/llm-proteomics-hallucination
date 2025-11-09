"""Unit tests for LLM clients"""
import pytest
from src.llm_eval.clients.openai_client import OpenAIClient

def test_openai_client_initialization():
    """Test OpenAI client initialization"""
    client = OpenAIClient(api_key="test-key", model="gpt-4-turbo")
    assert client.model == "gpt-4-turbo"

def test_response_format():
    """Test response format"""
    # Mock test - would use actual mocking in production
    pass
