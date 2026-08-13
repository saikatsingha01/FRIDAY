import os
import time
import threading
from typing import Dict, List, Optional, Type, Any
from dataclasses import dataclass, field
from enum import Enum

from src.skills.web_search_pkg.providers.base import (
    SearchProvider,
    SearchProviderError,
    RateLimitError,
    QuotaExhaustedError,
    AuthenticationError,
    ProviderUnavailableError,
)
from src.skills.web_search_pkg.providers import SearchProvider as ProviderBase


class KeyState(Enum):
    HEALTHY = "healthy"
    COOLDOWN = "cooldown"
    QUARANTINED = "quarantined"
    EXHAUSTED = "exhausted"


@dataclass
class KeyInfo:
    """Information about an API key."""
    key_id: str
    provider_name: str
    api_key: str
    config: Dict[str, Any] = field(default_factory=dict)
    state: KeyState = KeyState.HEALTHY
    last_used: float = 0.0
    last_error: Optional[SearchProviderError] = None
    consecutive_failures: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    cooldown_until: float = 0.0
    total_requests: int = 0
    
    def is_available(self) -> bool:
        if self.state == KeyState.QUARANTINED:
            return False
        if self.state == KeyState.EXHAUSTED:
            return False
        if self.state == KeyState.COOLDOWN:
            if time.time() >= self.cooldown_until:
                return True
            return False
        return self.state == KeyState.HEALTHY


class APIKeyRouter:
    """
    Universal API key router with health tracking, cooldown, and fallback.
    
    Features:
    - Multiple keys per provider
    - Per-key health tracking
    - Automatic cooldown on rate limits
    - Quarantine on auth failures
    - Exhaustion detection
    - Bounded retries with fallback
    - Thread-safe
    """
    
    def __init__(
        self,
        provider_class: Type[SearchProvider],
        provider_name: str,
        default_cooldown: float = 60.0,
        max_consecutive_failures: int = 3,
        max_retries_per_key: int = 1,
    ):
        self.provider_class = provider_class
        self.provider_name = provider_name
        self.default_cooldown = default_cooldown
        self.max_consecutive_failures = max_consecutive_failures
        self.max_retries_per_key = max_retries_per_key
        
        self._keys: Dict[str, KeyInfo] = {}
        self._providers: Dict[str, SearchProvider] = {}
        self._lock = threading.RLock()
        self._last_key_index = 0
    
    def add_key(self, key_id: str, api_key: str, **config) -> None:
        """Add an API key to the pool."""
        with self._lock:
            if key_id in self._keys:
                return
            
            info = KeyInfo(
                key_id=key_id,
                provider_name=self.provider_name,
                api_key=api_key,
                config=config,
            )
            self._keys[key_id] = info
            
            # Create provider instance
            provider = self.provider_class(api_key=api_key, key_id=key_id, **config)
            self._providers[key_id] = provider
    
    def load_keys_from_env(self, prefix: str = "") -> int:
        """
        Load API keys from environment variables.
        
        Expected format:
        - {PREFIX}_API_KEY or {PREFIX}_API_KEY_1, {PREFIX}_API_KEY_2, ...
        - {PREFIX}_CSE_ID or {PREFIX}_CSE_ID_1, {PREFIX}_CSE_ID_2, ... (optional)
        
        Returns number of keys loaded.
        """
        loaded = 0
        
        # Check for single key (no number suffix)
        base_key = f"{prefix}_API_KEY" if prefix else "GEMINI_API_KEY"
        base_cse = f"{prefix}_CSE_ID" if prefix else "GEMINI_CSE_ID"
        
        if base_key in os.environ:
            cse_id = os.environ.get(base_cse, "")
            self.add_key(f"{self.provider_name}_1", os.environ[base_key], cse_id=cse_id)
            loaded += 1
        
        # Check for numbered keys
        for i in range(1, 100):
            key_name = f"{base_key}_{i}" if i > 1 else base_key
            cse_name = f"{base_cse}_{i}" if i > 1 else base_cse
            
            if key_name not in os.environ:
                if i == 1 and loaded > 0:
                    continue
                break
            
            cse_id = os.environ.get(cse_name, "")
            key_id = f"{self.provider_name}_{i}"
            
            if key_id not in self._keys:
                self.add_key(key_id, os.environ[key_name], cse_id=cse_id)
                loaded += 1
        
        return loaded
    
    def get_available_keys(self) -> List[KeyInfo]:
        """Get all currently available keys."""
        with self._lock:
            return [k for k in self._keys.values() if k.is_available()]
    
    def get_provider(self, key_id: str) -> Optional[SearchProvider]:
        """Get provider instance for a key."""
        with self._lock:
            return self._providers.get(key_id)
    
    def execute_with_fallback(
        self,
        query: str,
        max_results: int,
        operation: str = "search"
    ) -> List[Any]:
        """
        Execute an operation with automatic fallback across keys.
        
        Returns results from the first successful key.
        Raises the last error if all keys fail.
        """
        last_error: Optional[Exception] = None
        
        for attempt in range(self.max_retries_per_key + 1):
            available_keys = self.get_available_keys()
            
            if not available_keys:
                raise SearchProviderError(
                    f"No available API keys for {self.provider_name}",
                    "no_keys_available",
                    self.provider_name
                )
            
            # Round-robin selection among healthy keys
            key_info = self._select_key(available_keys)
            provider = self.get_provider(key_info.key_id)
            
            if not provider:
                continue
            
            try:
                if operation == "search":
                    results = provider.search(query, max_results)
                else:
                    raise ValueError(f"Unknown operation: {operation}")
                
                # Success - update stats
                with self._lock:
                    key_info.successful_requests += 1
                    key_info.total_requests += 1
                    key_info.last_used = time.time()
                    key_info.consecutive_failures = 0
                    if key_info.state == KeyState.COOLDOWN:
                        key_info.state = KeyState.HEALTHY
                        key_info.cooldown_until = 0
                
                return results
                
            except RateLimitError as e:
                last_error = e
                self._handle_rate_limit(key_info, e)
                
            except QuotaExhaustedError as e:
                last_error = e
                self._handle_quota_exhausted(key_info)
                
            except AuthenticationError as e:
                last_error = e
                self._handle_auth_error(key_info)
                
            except ProviderUnavailableError as e:
                last_error = e
                self._handle_provider_error(key_info, e)
                
            except SearchProviderError as e:
                last_error = e
                self._handle_generic_error(key_info, e)
                
            except Exception as e:
                last_error = e
                self._handle_generic_error(key_info, SearchProviderError(
                    f"Unexpected error: {type(e).__name__}: {e}",
                    "unexpected",
                    self.provider_name,
                    key_info.key_id
                ))
            
            # Small delay before retry/fallback
            if attempt < self.max_retries_per_key:
                time.sleep(0.5)
        
        # All attempts failed
        raise last_error or SearchProviderError(
            "All API keys exhausted",
            "all_keys_failed",
            self.provider_name
        )
    
    def _select_key(self, available_keys: List[KeyInfo]) -> KeyInfo:
        """Select a key using round-robin among available keys."""
        with self._lock:
            if not available_keys:
                raise SearchProviderError("No available keys", "no_keys", self.provider_name)
            
            # Prefer keys with fewer recent failures
            available_keys.sort(key=lambda k: (k.consecutive_failures, -k.successful_requests))
            
            # Round-robin among equally healthy keys
            best_failure_count = available_keys[0].consecutive_failures
            best_keys = [k for k in available_keys if k.consecutive_failures == best_failure_count]
            
            selected = best_keys[self._last_key_index % len(best_keys)]
            self._last_key_index += 1
            
            return selected
    
    def _handle_rate_limit(self, key_info: KeyInfo, error: RateLimitError):
        with self._lock:
            key_info.failed_requests += 1
            key_info.total_requests += 1
            key_info.last_error = error
            key_info.consecutive_failures += 1
            
            cooldown = error.retry_after or self.default_cooldown
            key_info.state = KeyState.COOLDOWN
            key_info.cooldown_until = time.time() + cooldown
    
    def _handle_quota_exhausted(self, key_info: KeyInfo):
        with self._lock:
            key_info.failed_requests += 1
            key_info.total_requests += 1
            key_info.consecutive_failures += 1
            key_info.state = KeyState.EXHAUSTED
    
    def _handle_auth_error(self, key_info: KeyInfo):
        with self._lock:
            key_info.failed_requests += 1
            key_info.total_requests += 1
            key_info.consecutive_failures += 1
            key_info.state = KeyState.QUARANTINED
    
    def _handle_provider_error(self, key_info: KeyInfo, error: ProviderUnavailableError):
        with self._lock:
            key_info.failed_requests += 1
            key_info.total_requests += 1
            key_info.last_error = error
            key_info.consecutive_failures += 1
            
            if key_info.consecutive_failures >= self.max_consecutive_failures:
                key_info.state = KeyState.COOLDOWN
                key_info.cooldown_until = time.time() + self.default_cooldown
    
    def _handle_generic_error(self, key_info: KeyInfo, error: SearchProviderError):
        with self._lock:
            key_info.failed_requests += 1
            key_info.total_requests += 1
            key_info.last_error = error
            key_info.consecutive_failures += 1
    
    def get_key_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all keys."""
        with self._lock:
            return {
                key_id: {
                    "state": info.state.value,
                    "successful_requests": info.successful_requests,
                    "failed_requests": info.failed_requests,
                    "total_requests": info.total_requests,
                    "consecutive_failures": info.consecutive_failures,
                    "last_used": info.last_used,
                    "cooldown_remaining": max(0, info.cooldown_until - time.time()) if info.state == KeyState.COOLDOWN else 0,
                    "last_error": str(info.last_error) if info.last_error else None,
                }
                for key_id, info in self._keys.items()
            }
    
    def reset_key(self, key_id: str) -> bool:
        """Manually reset a key to healthy state."""
        with self._lock:
            if key_id not in self._keys:
                return False
            
            info = self._keys[key_id]
            info.state = KeyState.HEALTHY
            info.consecutive_failures = 0
            info.cooldown_until = 0
            info.last_error = None
            
            if key_id in self._providers:
                provider = self._providers[key_id]
                if hasattr(provider, 'mark_healthy'):
                    provider.mark_healthy()
            
            return True
    
    def get_all_keys(self) -> List[KeyInfo]:
        with self._lock:
            return list(self._keys.values())