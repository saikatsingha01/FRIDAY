from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class SearchResult:
    """Normalized search result across all providers."""
    title: str
    url: str
    snippet: str
    source: str = ""
    raw_data: Dict[str, Any] = field(default_factory=dict)
    deep_claims: Optional[set] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
        }
        if self.source:
            d["source"] = self.source
        if self.deep_claims:
            d["deep_claims"] = self.deep_claims
        return d


class SearchProviderError(Exception):
    """Base exception for search provider errors."""
    def __init__(self, message: str, error_type: str = "unknown", provider: str = "", key_id: str = ""):
        super().__init__(message)
        self.error_type = error_type
        self.provider = provider
        self.key_id = key_id


class RateLimitError(SearchProviderError):
    def __init__(self, message: str, provider: str = "", key_id: str = "", retry_after: Optional[float] = None):
        super().__init__(message, "rate_limit", provider, key_id)
        self.retry_after = retry_after


class QuotaExhaustedError(SearchProviderError):
    def __init__(self, message: str, provider: str = "", key_id: str = ""):
        super().__init__(message, "quota_exhausted", provider, key_id)


class AuthenticationError(SearchProviderError):
    def __init__(self, message: str, provider: str = "", key_id: str = ""):
        super().__init__(message, "authentication", provider, key_id)


class ProviderUnavailableError(SearchProviderError):
    def __init__(self, message: str, provider: str = "", key_id: str = ""):
        super().__init__(message, "provider_unavailable", provider, key_id)


class SearchProvider(ABC):
    """Abstract base class for search providers."""

    PROVIDER_NAME: str = "base"

    def __init__(self, api_key: str, key_id: str, **kwargs):
        self.api_key = api_key
        self.key_id = key_id
        self.config = kwargs
        self._last_request_time = 0.0
        self._min_request_interval = 0.1

    @abstractmethod
    def search(self, query: str, max_results: int) -> List[SearchResult]:
        """Execute a search query and return normalized results."""
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if the provider/key is currently healthy."""
        pass

    def get_provider_name(self) -> str:
        return self.PROVIDER_NAME

    def get_key_id(self) -> str:
        return self.key_id

    def _rate_limit(self):
        """Enforce minimum request interval."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.time()

    def _handle_http_error(self, status_code: int, response_text: str) -> SearchProviderError:
        """Map HTTP status codes to provider-specific errors."""
        if status_code == 429:
            return RateLimitError(
                f"Rate limited: {response_text}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )
        elif status_code == 401 or status_code == 403:
            return AuthenticationError(
                f"Authentication failed: {response_text}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )
        elif status_code == 404:
            return ProviderUnavailableError(
                f"Endpoint not found: {response_text}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )
        elif status_code >= 500:
            return ProviderUnavailableError(
                f"Provider error {status_code}: {response_text}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )
        else:
            return SearchProviderError(
                f"HTTP {status_code}: {response_text}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )