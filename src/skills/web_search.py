# ==========================================================
# WEB SEARCH TOOL
#
# Phase 5 — live web search via universal provider architecture.
# Includes universal retrieval-evaluation-refinement loop with
# multi-provider/key fallback for robust results.
# ==========================================================

import html
import re
import urllib.parse
import urllib.request
import datetime
import ssl
import random
import gzip
import json

from src.contracts.tool import (
    ToolRequest,
    ToolResult,
    ToolMetadata,
    ToolPermission,
)
from src.skills.skill_registry import register
from src.skills.tool_base import BaseTool
from src.skills.web_search_pkg.orchestrator import (
    get_orchestrator,
    initialize_orchestrator,
)
from src.skills.web_search_pkg.providers.base import SearchResult


# ==========================================================
# SSL CONTEXT (for deep retrieval)
# ==========================================================

_SSL_CONTEXT = ssl.create_default_context()
_SSL_CONTEXT.check_hostname = False
_SSL_CONTEXT.verify_mode = ssl.CERT_NONE


# ==========================================================
# REGEX PATTERNS
# ==========================================================

# Filler words to strip from queries
_QUERY_FILLER_WORDS = {
    "google", "search", "find", "look up", "look for", "tell me", "what is",
    "what are", "what's", "whats", "who is", "who's", "how to", "how do",
    "can you", "could you", "please", "kindly", "the", "a", "an", "for",
    "about", "on", "in", "at", "to", "of", "with", "from", "by", "my",
    "your", "our", "their", "his", "her", "its", "me", "i", "we", "you",
}

# Current intent patterns
_CURRENT_INTENT_PATTERNS = [
    re.compile(r"\b(current|latest|today|now|recent|live|real.?time|right now)\b", re.IGNORECASE),
    re.compile(r"\b(price|cost|weather|forecast|stock|rate|score)\b", re.IGNORECASE),
]

# Maximum number of search refinement attempts
_MAX_SEARCH_RETRIES = 2

# Maximum number of deep retrieval attempts per search
_MAX_DEEP_RETRIEVALS = 2

# Maximum total web operations (search + deep retrieval)
_MAX_TOTAL_WEB_OPS = 5

# HTTP headers for deep retrieval
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def _strip_query_filler(query: str) -> str:
    """Remove filler words from a query to get core keywords."""
    words = query.lower().split()
    filtered = [w for w in words if w not in _QUERY_FILLER_WORDS]
    return " ".join(filtered) if filtered else query


def _extract_core_keywords(query: str) -> list:
    """Extract core meaningful keywords from a query."""
    stripped = _strip_query_filler(query)
    keywords = [w for w in re.findall(r"[a-z0-9]+", stripped.lower()) if len(w) >= 2]
    return keywords


def _has_current_intent(query: str) -> bool:
    """Check if query is asking for current/real-time information."""
    for pattern in _CURRENT_INTENT_PATTERNS:
        if pattern.search(query):
            return True
    return False


# ==========================================================
# CLAIM EXTRACTION
# ==========================================================

def _extract_answerable_claims(text: str) -> set:
    """Extract concrete, verifiable factual claims from text."""
    claims = set()
    text_lower = text.lower()
    
    # Numeric values with units
    for m in re.finditer(r"\b\d+(?:[.,]\d+)?\s*(?:[€$£₹¥]|usd|eur|gbp|inr|usd|cad|aud|°[cfk]|degrees?|celsius|fahrenheit|kelvin|mph|kmh|kph|knots|m/s|hpa|mb|mmhg|inhg|%\s*(?:humidity|rh))\b", text_lower):
        claims.add(("measurement", m.group(0).strip()))
    
    # Version numbers
    for m in re.finditer(r"\b\d+(?:\.\d+)+(?:[a-z]?)\b", text_lower):
        claims.add(("version", m.group(0).strip()))
    
    # Dates
    for m in re.finditer(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b", text_lower):
        claims.add(("date", m.group(0).strip()))
    
    # Scores (sports)
    for m in re.finditer(r"\b\d+[-:]\d+\b", text_lower):
        claims.add(("score", m.group(0).strip()))
    
    # Explicit current/recent indicators
    for m in re.finditer(r"\b(current|latest|today|now|recent|live|as of)\s+\S+", text_lower):
        claims.add(("current_marker", m.group(0).strip()))
    
    # Named entities with values
    for m in re.finditer(r"\b[a-z]{3,}\s+\$\s?\d[\d,.]*\b", text_lower):
        claims.add(("entity_value", m.group(0).strip()))
    
    return claims


def _query_asks_for(query: str) -> dict:
    """Analyze what type of information the query is asking for."""
    q = query.lower()
    return {
        "wants_measurement": any(w in q for w in ["temperature", "temp", "weather", "forecast", "humidity", "pressure", "wind", "rain", "snow", "sunny", "cloudy"]),
        "wants_price": any(w in q for w in ["price", "cost", "costs", "pricing", "rate", "worth", "value"]),
        "wants_version": any(w in q for w in ["version", "release", "latest version", "update", "build"]),
        "wants_spec": any(w in q for w in ["spec", "specification", "specs", "specifications", "features"]),
        "wants_stock": any(w in q for w in ["stock", "share", "market", "nasdaq", "nyse", "ticker", "trading"]),
        "wants_score": any(w in q for w in ["score", "result", "match", "game", "won", "lost", "beat", "defeated"]),
        "wants_news": any(w in q for w in ["news", "headline", "breaking", "latest news", "current events", "announcement"]),
        "wants_person": any(w in q for w in ["who is", "who's", "ceo", "president", "director", "founder", "leader", "head of"]),
        "wants_location": any(w in q for w in ["where", "location", "address", "where is", "where are"]),
        "wants_time": any(w in q for w in ["when", "time", "date", "schedule", "deadline"]),
        "wants_definition": any(w in q for w in ["what is", "what are", "define", "definition", "meaning", "explain"]),
        "wants_howto": any(w in q for w in ["how to", "how do", "tutorial", "guide", "steps", "instructions"]),
        "wants_comparison": any(w in q for w in ["vs", "versus", "compare", "difference", "better", "best", "worst"]),
    }


# ==========================================================
# SEARCH RESULT EVALUATION
# ==========================================================

def _evaluate_search_results(query: str, results: list, max_results: int) -> dict:
    """Universal evaluation of search result sufficiency."""
    if not results:
        return {"sufficient": False, "reason": "no_results", "missing_info": "No search results returned", "promising_results": []}

    query_lower = query.lower()
    query_keywords = set(_extract_core_keywords(query))
    query_intent = _query_asks_for(query)

    relevant_count = 0
    all_claims = set()
    
    for r in results:
        snippet = (r.get("snippet") or "").lower()
        title = (r.get("title") or "").lower()
        
        claims = _extract_answerable_claims(snippet + " " + title)
        all_claims.update(claims)
        
        deep_claims = r.get("deep_claims")
        if deep_claims:
            all_claims.update(deep_claims)
        
        matched = sum(1 for kw in _extract_core_keywords(query) if kw in snippet or kw in title)
        if matched >= max(1, len(_extract_core_keywords(query)) // 2):
            relevant_count += 1

    relevance_ratio = relevant_count / len(results) if results else 0
    query_intent = _query_asks_for(query)
    has_current_intent = any(kw in query.lower() for kw in ["current", "latest", "today", "now", "recent", "live", "real-time", "right now"])

    missing_evidence = []
    evidence_found = False
    
    if query_intent["wants_measurement"]:
        if any(c[0] == "measurement" for c in all_claims):
            evidence_found = True
        else:
            missing_evidence.append("measurement data (temperature, humidity, wind, etc.)")
    
    if query_intent["wants_price"]:
        if any(c[0] in ("measurement", "entity_value") for c in all_claims):
            evidence_found = True
        else:
            missing_evidence.append("price/cost information")
    
    if query_intent["wants_version"]:
        if any(c[0] == "version" for c in all_claims):
            evidence_found = True
        else:
            missing_evidence.append("version number")
    
    if query_intent["wants_score"]:
        if any(c[0] == "score" for c in all_claims):
            evidence_found = True
        else:
            missing_evidence.append("score or match result")
    
    if query_intent["wants_news"]:
        if any(c[0] == "date" for c in all_claims):
            evidence_found = True
        else:
            missing_evidence.append("recent news with dates")
    
    if query_intent["wants_version"]:
        if any(c[0] == "version" for c in all_claims):
            evidence_found = True
        else:
            missing_evidence.append("version number")
    
    if query_intent["wants_person"]:
        if any("ceo" in c[1].lower() or "president" in c[1].lower() or "director" in c[1].lower() for c in all_claims):
            evidence_found = True
        else:
            missing_evidence.append("current role/position information")
    
    if query_intent["wants_definition"]:
        if len(all_claims) > 0:
            evidence_found = True
        else:
            missing_evidence.append("definitional information")
    
    if not any(query_intent.values()):
        if relevance_ratio >= 0.5 and len(all_claims) > 0:
            evidence_found = True
        else:
            missing_evidence.append("relevant factual information")
    
    if has_current_intent and not evidence_found:
        missing_evidence.append("current/recent information")
    
    if relevance_ratio < 0.3:
        missing_evidence.insert(0, "relevant search results")
    
    sufficient = evidence_found and relevance_ratio >= 0.3
    
    if sufficient:
        return {"sufficient": True, "reason": "sufficient_evidence", "missing_info": "", "promising_results": []}
    else:
        promising_results = []
        for r in results:
            snippet = (r.get("snippet") or "").lower()
            title = (r.get("title") or "").lower()
            url = r.get("url", "")
            if not url:
                continue
            
            is_promising = False
            if query_intent.get("wants_measurement", False) and any(w in title.lower() for w in ["weather", "forecast", "current", "live", "temperature", "conditions"]):
                is_promising = True
            if query_intent.get("wants_price", False) and any(w in title.lower() for w in ["price", "cost", "pricing", "rate", "buy"]):
                is_promising = True
            if query_intent.get("wants_measurement", False) and any(w in title.lower() for w in ["weather", "forecast", "temperature", "conditions", "current", "live", "today"]):
                is_promising = True
            if query_intent.get("wants_version", False) and any(w in title.lower() for w in ["version", "release", "latest", "download"]):
                is_promising = True
            if query_intent.get("wants_price", False) and any(w in title.lower() for w in ["price", "cost", "buy", "pricing"]):
                is_promising = True
            
            if is_promising and r.get("url"):
                promising_results.append({"url": r.get("url", ""), "title": r.get("title", ""), "snippet": r.get("snippet", "")[:200]})
        
        return {"sufficient": False, "reason": "insufficient_evidence", "missing_info": "; ".join(missing_evidence) if missing_evidence else "insufficient relevant information", "promising_results": promising_results}


def _refine_query(original_query: str, previous_results: list, missing_info: str) -> str:
    """Generate a refined search query based on what was missing."""
    keywords = _extract_core_keywords(original_query)
    missing_lower = missing_info.lower()
    additions = []
    
    if "measurement" in missing_info:
        additions.extend(["temperature", "conditions", "forecast"])
    if "price" in missing_info or "cost" in missing_info:
        additions.append("price")
    if "version" in missing_info or "number" in missing_info:
        additions.append("version")
    if "current" in missing_info or "recent" in missing_info or "latest" in missing_info:
        additions.extend(["current", "latest"])
    if "recent" in missing_info:
        additions.append("recent")
    if "specific" in missing_info:
        additions.append("specific")
    if "score" in missing_info or "result" in missing_info:
        additions.extend(["score", "result"])
    if "date" in missing_info:
        additions.append("date")
    if "specific" in missing_info or "information" in missing_info:
        additions.append("details")
    
    current_year = str(datetime.datetime.now().year)
    if current_year not in original_query:
        additions.append(current_year)
    
    refined_parts = _extract_core_keywords(original_query) + additions
    seen = set()
    unique_parts = []
    for part in refined_parts:
        if part not in seen:
            seen.add(part)
            unique_parts.append(part)
    return " ".join(unique_parts)


# ==========================================================
# DEEP RETRIEVAL
# ==========================================================

def _fetch_page(url: str, timeout: int = 10) -> str:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CONTEXT) as resp:
            raw = resp.read()
            if resp.headers.get('Content-Encoding') == 'gzip':
                raw = gzip.decompress(raw)
            return raw.decode("utf-8", errors="replace")
    except Exception:
        return ""


def _extract_main_content(page: str) -> str:
    if not page:
        return ""
    stripped = page.strip()
    if stripped.startswith('{') or stripped.startswith('['):
        return page
    
    page = re.sub(r"<script[^>]*>.*?</script>", "", page, flags=re.DOTALL | re.IGNORECASE)
    page = re.sub(r"<style[^>]*>.*?</style>", "", page, flags=re.DOTALL | re.IGNORECASE)
    page = re.sub(r"<(nav|header|footer|aside|script|style|nosvg)[^>]*>.*?</\1>", "", page, flags=re.DOTALL | re.IGNORECASE)
    
    block_tags = ["div", "p", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "td", "th", "section", "article", "p"]
    for tag in block_tags:
        page = re.sub(f"</{tag}>", "\n", page, flags=re.IGNORECASE)
        page = re.sub(f"<{tag}[^>]*>", "", page, flags=re.IGNORECASE)
    
    page = re.sub(r"<[^>]+>", " ", page)
    page = html.unescape(page)
    page = re.sub(r"\s+", " ", page)
    page = re.sub(r"\n\s*\n", "\n", page)
    return page.strip()


def _extract_claims_from_page(page: str) -> set:
    claims = set()
    text_lower = page.lower()
    
    stripped = page.strip()
    if stripped.startswith('{') or stripped.startswith('['):
        try:
            data = json.loads(page)
            claims.update(_extract_claims_from_json(data))
            return claims
        except:
            pass
    
    text_lower = page.lower()
    
    for m in re.finditer(r"\b\d+(?:[.,]\d+)?\s*(?:[€$£₹¥]|usd|eur|gbp|inr|usd|cad|aud|°[cfk]|degrees?|celsius|fahrenheit|kelvin|mph|kmh|kph|knots|m/s|hpa|mb|mmhg|inhg|%\s*(?:humidity|rh))\b", text_lower):
        claims.add(("measurement", m.group(0).strip()))
    
    for m in re.finditer(r"\b\d+(?:\.\d+)+(?:[a-z]?)\b", text_lower):
        claims.add(("version", m.group(0).strip()))
    
    for m in re.finditer(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b", text_lower):
        claims.add(("date", m.group(0).strip()))
    
    for m in re.finditer(r"\b\d+[-:]\d+\b", text_lower):
        claims.add(("score", m.group(0).strip()))
    
    for m in re.finditer(r"\b(current|latest|today|now|recent|live|as of)\s+\S+", text_lower):
        claims.add(("current_marker", m.group(0).strip()))
    
    for m in re.finditer(r"\b[a-z]{3,}\s+\$\s?\d[\d,.]*\b", text_lower):
        claims.add(("entity_value", m.group(0).strip()))
    
    for m in re.finditer(r"\b(?:price|cost|price is|costs?)\s*[:\-]?\s*[€$£₹¥]\s?\d[\d,.]*\b", text_lower):
        claims.add(("price", m.group(0).strip()))
    
    for m in re.finditer(r'"temp_c"\s*:\s*"?(\d+)"?', page):
        claims.add(("temperature", f"{m.group(1)}°C"))
    for m in re.finditer(r'"temp_f"\s*:\s*"?(\d+)"?', page):
        claims.add(("temperature", f"{m.group(1)}°F"))
    for m in re.finditer(r'"temp_c"\s*:\s*"?(\d+)"?', page):
        claims.add(("temperature", f"{m.group(1)}°C"))
    
    return claims


def _extract_claims_from_json(data: any, path: str = "") -> set:
    claims = set()
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            key_lower = key.lower()
            
            if key_lower in ('temp_c', 'temp_f', 'temp', 'temperature', 'temp_c', 'temp_f'):
                claims.add(("temperature", f"{value}°C" if key_lower.endswith('_c') else f"{value}°F" if key_lower.endswith('_f') else str(value)))
            elif key_lower in ('feelslike_c', 'feelslike_f', 'feels_like_c', 'feels_like_f', 'heatindex_c', 'heatindex_f', 'windchill_c', 'windchill_f'):
                claims.add(("temperature", f"{value}°C" if 'c' in key_lower else f"{value}°F"))
            elif key_lower in ('weatherdesc', 'weather_desc', 'description', 'condition', 'weather', 'weatherdesc'):
                if isinstance(value, list):
                    for v in value:
                        if isinstance(v, dict) and 'value' in v:
                            claims.add(("weather", v['value']))
                        elif isinstance(v, str):
                            claims.add(("weather", v))
                elif isinstance(value, str):
                    claims.add(("weather", value))
            elif 'humid' in key_lower:
                claims.add(("humidity", f"{value}%"))
            elif 'wind' in key_lower and ('speed' in key_lower or 'kph' in key_lower or 'mph' in key_lower):
                claims.add(("wind", f"{value} km/h"))
            elif 'pressure' in key_lower:
                claims.add(("pressure", f"{value} hPa"))
            elif key_lower == 'humidity':
                claims.add(("humidity", f"{value}%"))
            elif 'uv' in key_lower and 'index' in key_lower:
                claims.add(("uv_index", str(value)))
            elif 'precip' in key_lower or 'rain' in key_lower:
                claims.add(("precipitation", f"{value} mm"))
            elif 'cloud' in key_lower:
                claims.add(("cloud_cover", f"{value}%"))
            elif key_lower in ('weathercode', 'weather_code', 'condition'):
                claims.add(("weather_code", str(value)))
            
            claims.update(_extract_claims_from_json(value, new_path))
    
    elif isinstance(data, list):
        for i, item in enumerate(data):
            claims.update(_extract_claims_from_json(item, f"{path}[{i}]"))
    
    return claims


def _fetch_page_with_claims(url: str) -> dict:
    try:
        page = _fetch_page(url)
        if not page:
            return {"url": url, "success": False, "claims": set(), "content": "", "error": "Empty page"}
        
        content = _extract_main_content(page)
        if not content or len(content) < 100:
            return {"url": url, "success": False, "claims": set(), "content": "", "error": "Insufficient content"}
        
        claims = _extract_claims_from_page(content)
        return {"url": url, "success": True, "claims": claims, "content": content, "error": None}
    except Exception as e:
        return {"url": url, "success": False, "claims": set(), "content": "", "error": str(e)}


# ==========================================================
# SEARCH EXECUTION (uses universal orchestrator)
# ==========================================================

def _search_via_orchestrator(query: str, max_results: int) -> list:
    """Execute search using the universal orchestrator."""
    orchestrator = get_orchestrator()
    results = orchestrator.search(query, max_results)
    # Convert SearchResult objects to dict format expected by existing pipeline
    return [r.to_dict() for r in results]


# ==========================================================
# WEB SEARCH TOOL
# ==========================================================

class WebSearchTool(BaseTool):
    metadata = ToolMetadata(
        name="web_search",
        description=("Search the web for current, real-time information "
                     "(news, weather, prices, facts that change)."),
        capabilities=["web"],
        permission=ToolPermission.SAFE,
        actions={
            "search": {
                "input": {
                    "query": "str — structured search terms built from understanding entities",
                    "max_results": "int (optional, default 5)",
                },
                "output": {
                    "results": "list of {title, url, snippet}",
                },
            },
        },
        needs_network=True,
        errors=["network_error", "empty_query", "no_results"],
    )

    def execute(self, request: ToolRequest) -> ToolResult:
        action = request.action
        if action != "search":
            return self.fail(request, f"unsupported_action: {action}")

        query = str(request.parameters.get("query") or "").strip()
        if not query:
            return self.fail(request, "empty_query")

        try:
            results = self._search_with_refinement(
                query,
                int(request.parameters.get("max_results") or 5),
            )
        except Exception as exc:
            return self.fail(request, f"network_error: {type(exc).__name__}: {exc}")

        if not results:
            return self.fail(request, "no_results")

        return self.ok(request, data={"results": results})

    def _search(self, query: str, max_results: int) -> list:
        """Single search attempt via orchestrator."""
        return _search_via_orchestrator(query, max_results)

    def _search_with_refinement(self, query: str, max_results: int) -> list:
        current_query = query
        all_results = []
        seen_urls = set()
        total_web_ops = 0

        for attempt in range(_MAX_SEARCH_RETRIES + 1):
            results = self._search(current_query, max_results)

            new_results = []
            for r in results:
                url = r.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    new_results.append(r)

            if new_results:
                all_results.extend(new_results)
            total_web_ops += len(new_results)

            evaluation = _evaluate_search_results(current_query, all_results, max_results)

            if evaluation["sufficient"]:
                return all_results[:max_results]

            if attempt >= _MAX_SEARCH_RETRIES:
                break

            if attempt < _MAX_SEARCH_RETRIES and total_web_ops < _MAX_TOTAL_WEB_OPS:
                promising = evaluation.get("promising_results", [])
                deep_retrievals = 0
                for pr in promising:
                    if deep_retrievals >= _MAX_DEEP_RETRIEVALS:
                        break
                    if total_web_ops >= _MAX_TOTAL_WEB_OPS:
                        break
                    url = pr.get("url", "")
                    if not url:
                        continue
                    page_result = _fetch_page_with_claims(pr.get("url", ""))
                    total_web_ops += 1
                    deep_retrievals += 1
                    if page_result.get("success"):
                        page_claims = page_result.get("claims", set())
                        if page_claims:
                            all_results.append({
                                "title": f"[Deep] {pr.get('title', '')}",
                                "url": url,
                                "snippet": f"[Deep retrieval] {page_result.get('content', '')[:500]}",
                                "deep_claims": page_claims,
                            })

            evaluation = _evaluate_search_results(current_query, all_results, max_results)
            if evaluation["sufficient"]:
                return all_results[:max_results]

            if attempt >= _MAX_SEARCH_RETRIES:
                break

            missing_info = evaluation.get("missing_info", "")
            if missing_info:
                current_query = _refine_query(current_query, all_results, missing_info)
            else:
                current_query = _strip_query_filler(current_query) + " current latest"

        return all_results[:max_results]


# ==========================================================
# INITIALIZATION
# ==========================================================

# Initialize the universal orchestrator with default providers
_initialize_done = False

def _ensure_initialized():
    global _initialize_done
    if not _initialize_done:
        initialize_orchestrator()
        _initialize_done = True

# Ensure initialization happens on import
_ensure_initialized()


# ==========================================================
# REGISTRATION
# ==========================================================

web_search_tool = WebSearchTool()
register(web_search_tool)