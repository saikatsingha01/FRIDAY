import time
from typing import List, Dict, Any, Optional, Type
from dataclasses import dataclass, field

from src.skills.web_search_pkg.providers.base import SearchProvider, SearchResult, SearchProviderError
from src.skills.web_search_pkg.key_router import APIKeyRouter, KeyState


@dataclass
class SearchMetrics:
    """Metrics for a search operation."""
    provider: str = ""
    key_id: str = ""
    query: str = ""
    results_count: int = 0
    duration_ms: float = 0.0
    success: bool = False
    error: Optional[str] = None
    retries: int = 0
    fallback_used: bool = False


class UniversalSearchOrchestrator:
    """
    Universal search orchestrator that manages multiple providers and keys.
    
    Features:
    - Multiple provider support (Gemini, Brave, etc.)
    - Per-provider key pools
    - Automatic provider fallback
    - Health-aware routing
    - Metrics collection
    """
    
    def __init__(self):
        self._routers: Dict[str, APIKeyRouter] = {}
        self._provider_classes: Dict[str, Type[SearchProvider]] = {}
        self._provider_configs: Dict[str, Dict[str, Any]] = {}
        self._default_provider: Optional[str] = None
        self._metrics: List[SearchMetrics] = []
        self._max_metrics = 1000
    
    def register_provider(
        self,
        provider_name: str,
        provider_class: Type[SearchProvider],
        default: bool = False,
        **default_config
    ):
        """Register a search provider class."""
        self._provider_classes[provider_name] = provider_class
        self._provider_configs[provider_name] = default_config
        
        # Create router for this provider
        router = APIKeyRouter(
            provider_class=provider_class,
            provider_name=provider_name,
        )
        self._routers[provider_name] = router
        
        if default or self._default_provider is None:
            self._default_provider = provider_name
    
    def load_provider_keys(self, provider_name: str, env_prefix: str = "") -> int:
        """Load API keys for a provider from environment."""
        router = self._routers.get(provider_name)
        if not router:
            return 0
        return router.load_keys_from_env(env_prefix)
    
    def add_key(self, provider_name: str, key_id: str, api_key: str, **config) -> bool:
        """Manually add an API key."""
        router = self._routers.get(provider_name)
        if not router:
            return False
        router.add_key(key_id, api_key, **config)
        return True
    
    def search(
        self,
        query: str,
        max_results: int = 5,
        provider: Optional[str] = None,
        max_provider_retries: int = 1
    ) -> List[SearchResult]:
        """
        Execute search with automatic provider and key fallback.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            provider: Specific provider to use (None = use default with fallback)
            max_provider_retries: Max retries per provider before fallback
            
        Returns:
            List of normalized SearchResult objects
        """
        if not query.strip():
            return []
        
        providers_to_try = self._get_provider_order(provider)
        
        last_error: Optional[Exception] = None
        
        for provider_name in providers_to_try:
            router = self._routers.get(provider_name)
            if not router:
                continue
            
            available_keys = router.get_available_keys()
            if not available_keys:
                continue
            
            start_time = time.time()
            metrics = SearchMetrics(provider=provider_name, query=query)
            
            try:
                # Try with current provider
                results = router.execute_with_fallback(
                    query=query,
                    max_results=max_results,
                    operation="search"
                )
                
                metrics.success = True
                metrics.results_count = len(results)
                metrics.duration_ms = (time.time() - start_time) * 1000
                metrics.key_id = self._get_last_used_key(router)
                
                self._record_metrics(metrics)
                return results
                
            except SearchProviderError as e:
                metrics.success = False
                metrics.error = str(e)
                metrics.duration_ms = (time.time() - start_time) * 1000
                metrics.key_id = self._get_last_used_key(router)
                last_error = e
                
                self._record_metrics(metrics)
                
                # Continue to next provider
                continue
            
            except Exception as e:
                metrics.success = False
                metrics.error = f"{type(e).__name__}: {e}"
                metrics.duration_ms = (time.time() - start_time) * 1000
                last_error = e
                
                self._record_metrics(metrics)
                continue
        
        # All providers failed
        raise last_error or SearchProviderError(
            "All search providers exhausted",
            "all_providers_failed",
            "orchestrator"
        )
    
    def _get_provider_order(self, preferred: Optional[str]) -> List[str]:
        """Determine provider fallback order."""
        if preferred and preferred in self._routers:
            # Preferred first, then others
            others = [p for p in self._routers if p != preferred]
            return [preferred] + others
        
        # Default order
        if self._default_provider and self._default_provider in self._routers:
            others = [p for p in self._routers if p != self._default_provider]
            return [self._default_provider] + others
        
        return list(self._routers.keys())
    
    def _get_last_used_key(self, router: APIKeyRouter) -> str:
        """Get the key_id of the most recently used key."""
        keys = router.get_all_keys()
        if not keys:
            return ""
        keys.sort(key=lambda k: k.last_used, reverse=True)
        return keys[0].key_id if keys[0].last_used > 0 else ""
    
    def _record_metrics(self, metrics: SearchMetrics):
        self._metrics.append(metrics)
        if len(self._metrics) > self._max_metrics:
            self._metrics = self._metrics[-self._max_metrics:]
    
    def get_metrics(self, limit: int = 100) -> List[SearchMetrics]:
        return self._metrics[-limit:]
    
    def get_provider_stats(self) -> Dict[str, Any]:
        """Get statistics for all providers and keys."""
        return {
            provider: router.get_key_stats()
            for provider, router in self._routers.items()
        }
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get overall health summary."""
        total_keys = 0
        healthy_keys = 0
        by_provider = {}
        
        for provider, router in self._routers.items():
            keys = router.get_all_keys()
            provider_healthy = sum(1 for k in keys if k.is_available())
            total_keys += len(keys)
            healthy_keys += provider_healthy
            by_provider[provider] = {
                "total": len(keys),
                "healthy": provider_healthy,
                "keys": {
                    k.key_id: {
                        "state": k.state.value,
                        "success_rate": (
                            k.successful_requests / k.total_requests
                            if k.total_requests > 0 else 0
                        )
                    }
                    for k in keys
                }
            }
        
        return {
            "total_keys": total_keys,
            "healthy_keys": healthy_keys,
            "providers": by_provider,
            "default_provider": self._default_provider,
        }
    
    def reset_key(self, provider_name: str, key_id: str) -> bool:
        """Reset a specific key to healthy."""
        router = self._routers.get(provider_name)
        if not router:
            return False
        return router.reset_key(key_id)
    
    def list_providers(self) -> List[str]:
        return list(self._routers.keys())


# Global orchestrator instance
_orchestrator: Optional[UniversalSearchOrchestrator] = None


def get_orchestrator() -> UniversalSearchOrchestrator:
    """Get or create the global search orchestrator with providers initialized."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = initialize_orchestrator()
    return _orchestrator


def initialize_orchestrator() -> UniversalSearchOrchestrator:
    """Initialize the global orchestrator with default providers."""
    global _orchestrator
    _orchestrator = UniversalSearchOrchestrator()
    
    # Register Gemini provider
    from src.skills.web_search_pkg.providers import GeminiSearchProvider
    _orchestrator.register_provider(
        "gemini",
        GeminiSearchProvider,
        default=True,
    )
    
    # Load keys from environment
    _orchestrator.load_provider_keys("gemini", "GEMINI")
    
    return _orchestrator