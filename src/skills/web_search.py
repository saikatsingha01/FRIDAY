# ==========================================================
# WEB SEARCH TOOL
#
# Phase 5 — live web search via DuckDuckGo HTML (no API key,
# stdlib urllib only). Never decides whether to run; never sees
# raw user text. Executes a ToolRequest with a structured query
# parameter built by the ToolRouter from understanding entities.
# ==========================================================

import html
import re
import urllib.parse
import urllib.request

from src.contracts.tool import (
    ToolRequest,
    ToolResult,
    ToolMetadata,
    ToolPermission,
)
from src.skills.skill_registry import register
from src.skills.tool_base import BaseTool


_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

# DuckDuckGo HTML result markup:
#   <a rel="nofollow" class="result__a" href="...">Title</a>
#   <a class="result__snippet" ...>Snippet text</a>
_TITLE_RE = re.compile(
    r'class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>'
)
_SNIPPET_RE = re.compile(
    r'class="result__snippet"[^>]*>(?P<snippet>.*?)</a>'
)


class WebSearchTool(BaseTool):

    metadata = ToolMetadata(
        name="web_search",
        description=(
            "Search the web for current, real-time information "
            "(news, weather, prices, facts that change)."
        ),
        capabilities=["web"],
        permission=ToolPermission.SAFE,
        actions={
            "search": {
                "input": {
                    "query": "str — structured search terms "
                             "built from understanding entities",
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
            return self.fail(
                request,
                f"unsupported_action: {action}",
            )

        query = str(request.parameters.get("query") or "").strip()

        if not query:
            return self.fail(request, "empty_query")

        try:
            results = self._search(
                query,
                int(request.parameters.get("max_results") or 5),
            )
        except Exception as exc:
            return self.fail(
                request,
                f"network_error: {type(exc).__name__}: {exc}",
            )

        if not results:
            return self.fail(request, "no_results")

        return self.ok(request, data={"results": results})

    def _search(self, query: str, max_results: int) -> list:

        url = (
            "https://duckduckgo.com/html/?q="
            + urllib.parse.quote(query)
        )

        req = urllib.request.Request(url, headers=_HEADERS)

        with urllib.request.urlopen(req, timeout=15) as resp:
            page = resp.read().decode("utf-8", errors="replace")

        titles = list(_TITLE_RE.finditer(page))
        snippets = list(_SNIPPET_RE.finditer(page))

        results = []

        for index, match in enumerate(titles[:max_results]):

            title = html.unescape(
                re.sub(r"<[^>]+>", "", match.group("title"))
            ).strip()

            href = match.group("href")

            # DuckDuckGo wraps real links in a redirect param.
            real = re.search(
                r"uddg=([^&]+)", href
            )
            if real:
                href = urllib.parse.unquote(real.group(1))

            snippet = ""
            if index < len(snippets):
                snippet = html.unescape(
                    re.sub(
                        r"<[^>]+>", "",
                        snippets[index].group("snippet"),
                    )
                ).strip()

            if title:
                results.append({
                    "title": title,
                    "url": href,
                    "snippet": snippet,
                })

        return results


web_search_tool = WebSearchTool()

register(web_search_tool)
