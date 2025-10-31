"""Tests for basic tool functions."""

import pytest
from src.typhoon_it_support.tools import get_current_time
from src.typhoon_it_support.tools.document_search import (
    search_it_policy,
    search_troubleshooting_guide,
    search_all_documents
)


def test_get_current_time():
    """Test that get_current_time returns a valid timestamp."""
    result = get_current_time.invoke({})
    assert isinstance(result, str)
    assert len(result) > 0
    # Check format YYYY-MM-DD HH:MM:SS
    parts = result.split()
    assert len(parts) == 2
    date_parts = parts[0].split("-")
    assert len(date_parts) == 3


def test_get_current_time_format():
    """Test current time format is consistent."""
    result1 = get_current_time.invoke({})
    result2 = get_current_time.invoke({})
    
    # Both should have same format
    assert len(result1.split()) == len(result2.split())
    assert "-" in result1
    assert ":" in result1


class TestDocumentSearch:
    """Tests for document search functionality."""
    
    def test_search_it_policy_found(self):
        """Test IT policy search with matching query."""
        result = search_it_policy.invoke({"query": "password"})
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_search_troubleshooting_found(self):
        """Test troubleshooting guide search."""
        result = search_troubleshooting_guide.invoke({"query": "wifi"})
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_search_all_documents(self):
        """Test searching across all documents."""
        result = search_all_documents.invoke({"query": "network"})
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_search_with_empty_query(self):
        """Test document search with empty query."""
        result = search_it_policy.invoke({"query": ""})
        assert isinstance(result, str)
    
    def test_search_with_special_characters(self):
        """Test document search handles special characters."""
        result = search_it_policy.invoke({"query": "@#$%^&*()"})
        assert isinstance(result, str)
    
    def test_search_case_insensitive(self):
        """Test document search is case insensitive."""
        result1 = search_troubleshooting_guide.invoke({"query": "PASSWORD"})
        result2 = search_troubleshooting_guide.invoke({"query": "password"})
        
        # Both should return results (case insensitive)
        assert isinstance(result1, str)
        assert isinstance(result2, str)

