#!/usr/bin/env python3
"""
Unit tests for GeminiSearchProvider with mocked API responses.
Tests the parsing logic without requiring real API keys.
"""

import json
from src.skills.web_search_pkg.providers.gemini import GeminiSearchProvider
from src.skills.web_search_pkg.providers.base import SearchResult


def test_parse_results_with_grounding_chunks():
    """Test parsing response with grounding metadata."""
    provider = GeminiSearchProvider(api_key="test_key", key_id="test_1")
    
    # Mock response with grounding metadata (similar to real API response)
    mock_response = {
        "candidates": [{
            "content": {
                "parts": [{
                    "text": "Spain won Euro 2024, defeating England 2-1 in the final. This victory marks Spain's record fourth European Championship title."
                }],
                "role": "model"
            },
            "groundingMetadata": {
                "webSearchQueries": ["UEFA Euro 2024 winner", "who won euro 2024"],
                "searchEntryPoint": {"renderedContent": ""},
                "groundingChunks": [
                    {"web": {"uri": "https://www.aljazeera.com/sports/euro-2024-final", "title": "aljazeera.com"}},
                    {"web": {"uri": "https://www.uefa.com/euro2024/news/spain-wins-euro-2024", "title": "uefa.com"}}
                ],
                "groundingSupports": [
                    {
                        "segment": {
                            "startIndex": 0,
                            "endIndex": 56,
                            "text": "Spain won Euro 2024, defeating England 2-1 in the final."
                        },
                        "groundingChunkIndices": [0]
                    },
                    {
                        "segment": {
                            "startIndex": 57,
                            "endIndex": 150,
                            "text": "This victory marks Spain's record fourth European Championship title."
                        },
                        "groundingChunkIndices": [0, 1]
                    }
                ]
            }
        }]
    }
    
    results = provider._parse_results(mock_response, max_results=5)
    
    assert len(results) == 2, f"Expected 2 results, got {len(results)}"
    
    # Check first result
    assert results[0].title == "aljazeera.com"
    assert results[0].url == "https://www.aljazeera.com/sports/euro-2024-final"
    assert "Spain won Euro 2024" in results[0].snippet
    assert results[0].source == "gemini"
    
    # Check second result
    assert results[1].title == "uefa.com"
    assert results[1].url == "https://www.uefa.com/euro2024/news/spain-wins-euro-2024"
    assert "fourth European Championship" in results[1].snippet
    
    print("[OK] test_parse_results_with_grounding_chunks passed")


def test_parse_results_without_grounding_chunks():
    """Test parsing response when no grounding chunks but has text."""
    provider = GeminiSearchProvider(api_key="test_key", key_id="test_1")
    
    mock_response = {
        "candidates": [{
            "content": {
                "parts": [{
                    "text": "The current weather in Siliguri is 28°C with partly cloudy skies."
                }],
                "role": "model"
            },
            "groundingMetadata": {
                "webSearchQueries": ["current weather Siliguri"],
                "groundingChunks": [],
                "groundingSupports": []
            }
        }]
    }
    
    results = provider._parse_results(mock_response, max_results=5)
    
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"
    assert "weather in Siliguri" in results[0].snippet
    assert results[0].source == "gemini"
    assert results[0].url == ""
    
    print("[OK] test_parse_results_without_grounding_chunks passed")


def test_parse_results_empty_candidates():
    """Test parsing response with empty candidates."""
    provider = GeminiSearchProvider(api_key="test_key", key_id="test_1")
    
    mock_response = {"candidates": []}
    
    results = provider._parse_results(mock_response, max_results=5)
    
    assert len(results) == 0, f"Expected 0 results, got {len(results)}"
    
    print("[OK] test_parse_results_empty_candidates passed")


def test_parse_results_missing_fields():
    """Test parsing response with missing optional fields."""
    provider = GeminiSearchProvider(api_key="test_key", key_id="test_1")
    
    # Minimal response
    mock_response = {
        "candidates": [{
            "content": {
                "parts": [{"text": "Test response"}]
            }
        }]
    }
    
    results = provider._parse_results(mock_response, max_results=5)
    
    assert len(results) == 1
    assert "Test response" in results[0].snippet
    
    print("[OK] test_parse_results_missing_fields passed")


def test_extract_snippet_for_source():
    """Test snippet extraction for specific grounding chunk."""
    provider = GeminiSearchProvider(api_key="test_key", key_id="test_1")
    
    response_text = "Spain won Euro 2024, defeating England 2-1. This is their fourth title."
    grounding_supports = [
        {
            "segment": {"startIndex": 0, "endIndex": 40, "text": "Spain won Euro 2024, defeating England 2-1"},
            "groundingChunkIndices": [0]
        },
        {
            "segment": {"startIndex": 41, "endIndex": 65, "text": "This is their fourth title"},
            "groundingChunkIndices": [0, 1]
        }
    ]
    web_sources = [
        {"uri": "https://example.com/1", "title": "Source 1"},
        {"uri": "https://example.com/2", "title": "Source 2"}
    ]
    
    # Test chunk 0
    snippet = provider._extract_snippet_for_source(response_text, grounding_supports, 0, web_sources)
    assert "Spain won Euro 2024" in snippet
    assert "fourth title" in snippet
    
    # Test chunk 1 (only in second support)
    snippet = provider._extract_snippet_for_source(response_text, grounding_supports, 1, web_sources)
    assert "fourth title" in snippet
    
    print("[OK] test_extract_snippet_for_source passed")


def test_error_classification():
    """Test error classification logic."""
    provider = GeminiSearchProvider(api_key="test_key", key_id="test_1")
    
    # Test that error patterns are defined
    assert hasattr(provider, 'QUOTA_PATTERNS')
    assert hasattr(provider, 'AUTH_PATTERNS')
    assert hasattr(provider, 'RATE_LIMIT_PATTERNS')
    assert "quota" in provider.QUOTA_PATTERNS
    assert "invalid" in provider.AUTH_PATTERNS
    assert "rate limit" in provider.RATE_LIMIT_PATTERNS
    
    print("[OK] test_error_classification passed")


def test_provider_initialization():
    """Test provider initializes with correct defaults."""
    provider = GeminiSearchProvider(api_key="test_key", key_id="test_1")
    
    assert provider.PROVIDER_NAME == "gemini"
    assert provider.get_key_id() == "test_1"
    assert provider.model == "gemini-2.5-flash"
    assert provider.is_healthy() == True
    
    # Test with custom model
    provider2 = GeminiSearchProvider(api_key="test_key", key_id="test_2", model="gemini-2.5-flash")
    assert provider2.model == "gemini-2.5-flash"
    
    print("[OK] test_provider_initialization passed")


def test_health_tracking():
    """Test health tracking methods."""
    from src.skills.web_search_pkg.providers.base import SearchProviderError
    
    provider = GeminiSearchProvider(api_key="test_key", key_id="test_1")
    
    assert provider.is_healthy() == True
    assert provider.get_last_error() is None
    
    # Mark unhealthy
    error = SearchProviderError("Test error", "test", "gemini", "test_1")
    provider.mark_unhealthy(error)
    
    assert provider.is_healthy() == True  # Still healthy after 1 failure
    assert provider.get_last_error() == error
    
    # Mark healthy again
    provider.mark_healthy()
    assert provider.is_healthy() == True
    assert provider.get_last_error() is None
    
    print("[OK] test_health_tracking passed")


if __name__ == "__main__":
    test_provider_initialization()
    test_parse_results_with_grounding_chunks()
    test_parse_results_without_grounding_chunks()
    test_parse_results_empty_candidates()
    test_parse_results_missing_fields()
    test_extract_snippet_for_source()
    test_error_classification()
    test_health_tracking()
    print("\nAll unit tests passed!")