import json
import urllib.parse
import urllib.request
import ssl
import time
from typing import List, Dict, Any, Optional

from src.skills.web_search_pkg.providers.base import (
    SearchProvider,
    SearchResult,
    SearchProviderError,
    RateLimitError,
    QuotaExhaustedError,
    AuthenticationError,
    ProviderUnavailableError,
)


class GeminiSearchProvider(SearchProvider):
    """
    Gemini API with Google Search Grounding provider.

    Uses the official Gemini API (generativelanguage.googleapis.com) with the
    `google_search` tool for grounded search results. This is the current
    supported approach (not the deprecated Custom Search JSON API).

    Required environment variable:
    - GEMINI_API_KEY: Your Gemini API key (from Google AI Studio)

    Multiple keys supported via:
    - GEMINI_API_KEY, GEMINI_API_KEY_1, GEMINI_API_KEY_2, etc.

    NO CSE ID REQUIRED - uses Gemini API key directly.
    """

    PROVIDER_NAME = "gemini"
    DEFAULT_MODEL = "gemini-1.5-flash"
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/"

    # Error message patterns for classification
    QUOTA_PATTERNS = ["quota", "limit exceeded", "billing", "exceeded"]
    AUTH_PATTERNS = ["invalid", "unauthorized", "forbidden", "api key", "permission denied", "authentication"]
    RATE_LIMIT_PATTERNS = ["rate limit", "too many requests", "quota exceeded", "resource exhausted"]

    def __init__(
        self,
        api_key: str,
        key_id: str,
        model: str = "",
        **kwargs
    ):
        super().__init__(api_key, key_id, **kwargs)
        self.model = model or kwargs.get("model", self.DEFAULT_MODEL)
        self._ssl_context = ssl.create_default_context()
        self._ssl_context.check_hostname = False
        self._ssl_context.verify_mode = ssl.CERT_NONE
        self._healthy = True
        self._last_error: Optional[SearchProviderError] = None
        self._consecutive_failures = 0
        self._max_consecutive_failures = 3

    def is_healthy(self) -> bool:
        return self._healthy and self._consecutive_failures < self._max_consecutive_failures

    def get_last_error(self) -> Optional[SearchProviderError]:
        return self._last_error

    def mark_unhealthy(self, error: SearchProviderError):
        self._last_error = error
        self._consecutive_failures += 1
        if self._consecutive_failures >= self._max_consecutive_failures:
            self._healthy = False

    def mark_healthy(self):
        self._consecutive_failures = 0
        self._healthy = True
        self._last_error = None

    def search(self, query: str, max_results: int) -> List[SearchResult]:
        self._rate_limit()

        # Build request for Gemini API with google_search tool
        url = f"{self.BASE_URL}{self.model}:generateContent"
        params = {"key": self.api_key}
        full_url = url + "?" + urllib.parse.urlencode(params)

        request_body = {
            "contents": [
                {
                    "parts": [
                        {"text": query}
                    ]
                }
            ],
            "tools": [
                {"google_search": {}}
            ],
            "generationConfig": {
                "temperature": 1.0,
                "maxOutputTokens": 8192,
            }
        }

        try:
            req = urllib.request.Request(
                full_url,
                data=json.dumps(request_body).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "FRIDAY/1.0",
                },
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=30, context=self._ssl_context) as resp:
                raw = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    import gzip
                    raw = gzip.decompress(raw)
                data = json.loads(raw.decode("utf-8", errors="replace"))

            self.mark_healthy()
            return self._parse_results(data, max_results, query)

        except urllib.error.HTTPError as e:
            error = self._handle_gemini_error(e)
            self.mark_unhealthy(error)
            raise error

        except urllib.error.URLError as e:
            error = ProviderUnavailableError(
                f"Network error: {e.reason}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )
            self.mark_unhealthy(error)
            raise error

        except Exception as e:
            error = ProviderUnavailableError(
                f"Unexpected error: {type(e).__name__}: {e}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )
            self.mark_unhealthy(error)
            raise error

    def _handle_gemini_error(self, error: urllib.error.HTTPError) -> SearchProviderError:
        """Parse Gemini API error response and classify."""
        try:
            raw = error.read()
            if error.headers.get("Content-Encoding") == "gzip":
                import gzip
                raw = gzip.decompress(raw)
            error_data = json.loads(raw.decode("utf-8", errors="replace"))
            error_info = error_data.get("error", {})
            message = error_info.get("message", str(error))
            message_lower = message.lower()
            status = error_info.get("status", "")

            # Classify error based on status and message
            if error.code == 429 or "rate limit" in message_lower or "resource exhausted" in message_lower:
                retry_after = None
                if "retry-after" in error.headers:
                    try:
                        retry_after = float(error.headers["retry-after"])
                    except ValueError:
                        pass
                # Also check for retry_delay in error details
                for detail in error_info.get("details", []):
                    if "@type" in detail and "RetryInfo" in detail["@type"]:
                        retry_delay = detail.get("retryDelay", "")
                        if retry_delay.endswith("s"):
                            try:
                                retry_after = float(retry_delay[:-1])
                            except ValueError:
                                pass
                return RateLimitError(
                    f"Rate limited: {message}",
                    provider=self.PROVIDER_NAME,
                    key_id=self.key_id,
                    retry_after=retry_after
                )

            elif error.code in (401, 403) or any(p in message_lower for p in self.AUTH_PATTERNS):
                return AuthenticationError(
                    f"Authentication failed: {message}",
                    provider=self.PROVIDER_NAME,
                    key_id=self.key_id
                )

            elif any(p in message_lower for p in self.QUOTA_PATTERNS) and "rate" not in message_lower:
                return QuotaExhaustedError(
                    f"Quota exhausted: {message}",
                    provider=self.PROVIDER_NAME,
                    key_id=self.key_id
                )

            elif error.code >= 500:
                return ProviderUnavailableError(
                    f"Gemini API error {error.code}: {message}",
                    provider=self.PROVIDER_NAME,
                    key_id=self.key_id
                )

            elif error.code == 400:
                # Check for specific 400 errors
                if "google_search" in message_lower and ("json" in message_lower or "controlled generation" in message_lower or "schema" in message_lower):
                    return SearchProviderError(
                        f"Unsupported configuration: {message}",
                        "unsupported_config",
                        self.PROVIDER_NAME,
                        self.key_id
                    )
                return SearchProviderError(
                    f"Bad request: {message}",
                    "bad_request",
                    self.PROVIDER_NAME,
                    self.key_id
                )

            return SearchProviderError(
                f"Gemini API error {error.code}: {message}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )

        except Exception:
            return SearchProviderError(
                f"HTTP {error.code}: {error.reason}",
                provider=self.PROVIDER_NAME,
                key_id=self.key_id
            )

    def _parse_results(self, data: Dict[str, Any], max_results: int, query: str = "") -> List[SearchResult]:
        """Parse Gemini API generateContent response with grounding metadata."""
        results = []

        candidates = data.get("candidates", [])
        if not candidates:
            return results

        candidate = candidates[0]
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        grounding_metadata = candidate.get("groundingMetadata", {})

        # Extract main response text
        response_text = ""
        for part in parts:
            if "text" in part:
                response_text += part["text"]

        # Extract grounding chunks (sources)
        grounding_chunks = grounding_metadata.get("groundingChunks", [])
        web_sources = []
        for chunk in grounding_chunks:
            web = chunk.get("web", {})
            uri = web.get("uri", "")
            title = web.get("title", "")
            if uri:
                web_sources.append({"uri": uri, "title": title or uri})

        # Extract grounding supports (citations mapping text to sources)
        grounding_supports = grounding_metadata.get("groundingSupports", [])

        # Extract search queries used
        search_queries = grounding_metadata.get("webSearchQueries", [])

        # If we have grounding chunks, create results from them
        if web_sources:
            for i, source in enumerate(web_sources[:max_results]):
                uri = source["uri"]
                title = source["title"]

                # Find relevant snippet from grounding supports
                snippet = self._extract_snippet_for_source(
                    response_text, grounding_supports, i, web_sources
                )

                # Fallback: use search query or response text
                if not snippet and search_queries:
                    snippet = f"Search query: {search_queries[0]}"
                elif not snippet and response_text:
                    snippet = response_text[:300]

                results.append(SearchResult(
                    title=title,
                    url=uri,
                    snippet=snippet,
                    source=self.PROVIDER_NAME,
                    raw_data={
                        "grounding_chunk_index": i,
                        "search_queries": search_queries,
                        "response_text": response_text,
                    }
                ))
        elif response_text:
            # No grounding chunks but have response - create a single result
            results.append(SearchResult(
                title=f"Gemini: {query[:50]}",
                url="",
                snippet=response_text[:500],
                source=self.PROVIDER_NAME,
                raw_data={
                    "search_queries": search_queries,
                    "response_text": response_text,
                }
            ))

        return results

    def _extract_snippet_for_source(
        self,
        response_text: str,
        grounding_supports: List[Dict],
        chunk_index: int,
        web_sources: List[Dict]
    ) -> str:
        """Extract relevant text snippet for a specific grounding source."""
        if not grounding_supports or not response_text:
            return ""

        # Find supports that reference this chunk index
        relevant_segments = []
        for support in grounding_supports:
            chunk_indices = support.get("groundingChunkIndices", [])
            if chunk_index in chunk_indices:
                segment = support.get("segment", {})
                start = segment.get("startIndex", 0)
                end = segment.get("endIndex", 0)
                text = segment.get("text", "")
                if text:
                    relevant_segments.append(text)
                elif start < end and end <= len(response_text):
                    relevant_segments.append(response_text[start:end])

        if relevant_segments:
            return " ".join(relevant_segments)[:500]

        return ""