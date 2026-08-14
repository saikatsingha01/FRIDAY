def sentence_case(text):

    if not text:

        return ""

    text = text.strip()

    return text[0].upper() + text[1:]


# ==========================================================
# TRIVIAL RESPONSE TEMPLATES
#
# Used by brain.py's triage fast-path: zero LLM calls on trivial
# social messages (hello/bye/thanks/etc). Each category has a few
# natural variants selected randomly so replies are not robotic.
# ==========================================================

import random
import re as _re
import os

TRIVIAL_TEMPLATES = {

    "greeting": [
        "Hey! Good to see you. What can I do for you?",
        "Hello! What are we working on today?",
        "Hi there! How can I help?",
        "Hey! I'm ready when you are.",
    ],

    "farewell": [
        "Take care! See you soon.",
        "Goodbye! I'll be here whenever you need me.",
        "Bye for now. Talk soon!",
    ],

    "gratitude": [
        "You're welcome!",
        "Anytime. That's what I'm here for.",
        "Happy to help!",
        "No problem at all.",
    ],

    "affirmation": [
        "Got it.",
        "Sounds good.",
        "Alright, understood.",
        "On it.",
    ],

    "small_talk": [
        "I'm doing well, thanks for asking. What about you?",
        "All good on my end! What's on your mind?",
        "Everything's running smoothly. What do you need?",
    ],

}


def generate_trivial_response(category: str, message: str = "") -> str:
    """
    Returns a template response for a trivial triage category.
    Raises KeyError when the category has no templates — the caller
    must fall back to the full pipeline (fail-open).
    """

    templates = TRIVIAL_TEMPLATES[category]

    return random.choice(templates)


# ==========================================================
# MEMORY FORMATTING
# ==========================================================
def format_memory(memory):

    text = sentence_case(
        memory["text"]
    )

    category = memory.get(
        "category",
        "general"
    )

    if category == "identity":

        return text + "."

    if category == "device":

        return text + "."

    if category == "project":

        return text + "."

    if category == "preference":

        return text + "."

    if category == "emotional":

        return text + "."

    return text + "."


# ==========================================================
# MAIN
# ==========================================================

def generate_response(data):

    # --------------------------------------
    # None
    # --------------------------------------

    if data is None:

        return None

    # --------------------------------------
    # Already a response
    # --------------------------------------

    if isinstance(data, str):

        return data

    # --------------------------------------
    # Single Memory
    # --------------------------------------

    if isinstance(data, dict):

        if "text" in data:

            return format_memory(data)

        return str(data)

    # --------------------------------------
    # Memory List
    # --------------------------------------

    if isinstance(data, list):

        if len(data) == 0:

            return "I couldn't find anything relevant."

        if len(data) == 1:

            return format_memory(data[0])

        response = []

        for memory in data:

            response.append(
                format_memory(memory)
            )

        return "\n".join(response)

    # --------------------------------------
    # Fallback
    # --------------------------------------

    return str(data)


# ==========================================================
# FILESYSTEM ANSWER GUARD
#
# Deterministic safety net for filesystem answers. The final
# response LLM must never be the source of file or folder
# names: only the TOOL RESULTS may supply them. Prompt rules
# alone are not enough (a small local model can still wander),
# so the guard verifies the final reply against the actual
# tool data and replaces any unsafe reply with one built
# directly from the ground truth.
# ==========================================================

_FAB_TOK_RE = _re.compile(
    r"(?<![\w.])("
    r"[A-Za-z0-9](?:[A-Za-z0-9_.\-]*[A-Za-z0-9_\-])?\.(?:\d|[A-Za-z]{1,5})"
    r")"
    r"(?!\w|\.\w)",
    _re.IGNORECASE,
)
_CONN_RE = _re.compile(
    r"\b(?:and|including|like|the|a|an|plus|with|there|are|also|has|"
    r"have|such|as|was|were|is|s|named?|called|some|other|files|"
    r"found|listed|below|here|only|just)\b",
    _re.IGNORECASE,
)
_EXT_RE = _re.compile(r"\.(?:\d|[a-z]{1,5})$")
_GRANT_RE = _re.compile(r"\bgrant\w*\b", _re.IGNORECASE)
_PERM_RE = _re.compile(r"\bpermission\b", _re.IGNORECASE)
_NOTFOUND_RE = _re.compile(
    r"(not found|not sure|cannot find|can'?t find|couldn'?t find|"
    r"could not find|couldn'?t locate|could not locate|unable to find|"
    r"doesn'?t exist|does not exist|doesn'?t seem to (?:be|exist)|"
    r"don'?t know|i couldn't locate|no folder|no such)",
    _re.IGNORECASE,
)
_DENIAL_RE = _re.compile(
    r"\b(couldn'?t|could not|can'?t|cannot|unable to)\s+"
    r"(?:find|access|see|look(?: it)? up|open|read|list)\w*",
    _re.IGNORECASE,
)
_INSIDE_UNKNOWN_RE = _re.compile(
    r"don'?t\s+know\s+(?:what'?s|what is)\s+inside",
    _re.IGNORECASE,
)
_NOINFO_RE = _re.compile(
    r"no\s+information\s+about\s+the\s+contents?|"
    r"we\s+just\s+started\s+our\s+conversation",
    _re.IGNORECASE,
)

# Regex to detect specific factual claims (prices, dates, versions, specs)
# that should be grounded in web search snippets.
_PRICE_RE = _re.compile(r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?")
_VERSION_RE = _re.compile(r"\b\d+(?:\.\d+)+(?:[a-z]?)\b")
_DATE_RE = _re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b", _re.IGNORECASE)
_SPEC_RE = _re.compile(r"\b(?:rtx|gtx|rx|ryzen|core|i\d|ryzen)\s*\d{3,4}\b", _re.IGNORECASE)
# Temperature/weather patterns (Celsius, Fahrenheit, Kelvin, degree symbols)
# Also accept quotation marks (U+201C/U+201D) which some search engines use as degree symbols
_TEMP_RE = _re.compile(r"\b\d+(?:\.\d+)?\s*(?:[°\"\u201c\u201d][cfk]|degrees?\s*(?:celsius|fahrenheit|kelvin)|[cfk])\b", _re.IGNORECASE)
# Weather condition patterns
_WEATHER_CONDITION_RE = _re.compile(r"\b(?:sunny|cloudy|rainy|snowy|windy|humid|clear|overcast|partly\s+cloudy|mostly\s+(?:sunny|cloudy)|scattered\s+(?:showers|thunderstorms)|chance\s+of\s+(?:rain|snow|thunderstorms))\b", _re.IGNORECASE)
# Humidity/pressure/wind patterns
_HUMIDITY_RE = _re.compile(r"\b\d+(?:\.\d+)?\s*%\s*(?:humidity|rh\b)", _re.IGNORECASE)
_PRESSURE_RE = _re.compile(r"\b\d+(?:\.\d+)?\s*(?:hpa|mb|mmhg|inhg)\b", _re.IGNORECASE)
_WIND_RE = _re.compile(r"\b\d+(?:\.\d+)?\s*(?:mph|kmh|kph|knots|m/s)\b", _re.IGNORECASE)

# Factual claim patterns that require grounding
_FACTUAL_CLAIM_RE = _re.compile(
    r"(?:price|cost|msrp|release|launch|version|spec|specification|"
    r"speed|capacity|memory|storage|battery|display|screen|"
    r"resolution|refresh|ghz|mhz|gb|tb|mb|watts?|w\b|"
    r"temperature|temp|degree|weather|humidity|pressure|wind|"
    r"rain|snow|sunny|cloudy|forecast)",
    _re.IGNORECASE,
)


def _listing_tokens(text):
    """File-like tokens (extension-bearing) mentioned in a reply."""
    tokens = []
    for m in _FAB_TOK_RE.finditer(str(text)):
        low = m.group(1).lower().strip(" \t,.;:'\"`()[]{}")
        if not low or ". " in low:
            continue
        for piece in _re.split(r"\s+-\s+", low):
            piece = _re.sub(r"^\s*(?:\(?\d+[\)).:]?\s+|[a-z][\)).]\s+)", "", piece)
            parts = piece.split()
            while parts and _CONN_RE.fullmatch(parts[0]):
                parts.pop(0)
            while parts and _CONN_RE.fullmatch(parts[-1]):
                parts.pop()
            if not parts:
                continue
            token = " ".join(parts)
            if _EXT_RE.search(token) and token not in tokens:
                tokens.append(token)
    return tokens


def _fabricated_in(response, allowed):
    allowed_low = [str(n).lower() for n in (allowed or [])]
    fake = []
    for token in _listing_tokens(response):
        if (token in allowed_low
                or any(n.startswith(token) for n in allowed_low)
                or any(token in n for n in allowed_low)
                or any(n in token for n in allowed_low)):
            continue
        fake.append(token)
    return fake


def _deterministic_listing(data):
    entries = (data or {}).get("entries") or []
    parts = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        if not name:
            continue
        kind = entry.get("type") or "item"
        label = "folder" if kind == "dir" else (
            "file" if kind == "file" else "item")
        parts.append(f"{name} ({label})")
    if not parts:
        return "The folder is empty — it contains no files or subfolders."
    return "I found these in the folder: " + ", ".join(parts) + "."


def _deterministic_not_found():
    return (
        "I couldn't find that folder or file on the computer. It may "
        "not exist right now, or the name may be different. Could you "
        "name the exact folder or file again?"
    )


def _deterministic_not_found_named(requested):
    return (
        f"I couldn't find \"{requested}\" on the computer. It may not "
        "exist right now, or the name may be different. Could you name "
        "the exact folder or file again?"
    )


def _deterministic_failure():
    return (
        "I couldn't look that up — I need the exact folder or file "
        "name. Could you name it again?"
    )


def _deterministic_no_local_path():
    return (
        "I couldn't find that on your computer. The search only "
        "returned internet information, not a location on this "
        "machine. If you name the exact folder or file, I can search "
        "your computer again."
    )


def _kind_label(kind):
    return "folder" if kind == "dir" else (
        "file" if kind == "file" else "item")


def _deterministic_locate(data):
    """
    Ground-truth LOCATE reply built only from a successful current
    locate result. Distinguishes exact / normalized / fuzzy matches
    and reports every real candidate, so the response model can never
    "improve" a found path into something that does not exist.
    """
    requested = data.get("requested")
    kind_label = _kind_label(data.get("kind"))
    path = data.get("path")
    match = data.get("match")
    candidates = data.get("candidates") or []
    if isinstance(candidates, list) and len(candidates) > 1:
        lines = ["I found multiple matches for that:"]
        for cand in candidates:
            if not isinstance(cand, dict) or not cand.get("path"):
                continue
            label = _kind_label(cand.get("kind"))
            note = {
                "exact": "exact match",
                "normalized": "normalized match",
                "fuzzy": "closest match",
            }.get(cand.get("match"), "match")
            lines.append(
                f"- {cand['path']} ({label}) — {note}"
            )
        return "\n".join(lines)
    if not path:
        return _deterministic_not_found()
    if match == "fuzzy":
        return (
            f"I couldn't find \"{requested}\" exactly. The closest "
            f"match I found is a {kind_label} at {path}."
        )
    if match == "normalized":
        return (
            f"I found a {kind_label} at {path} — the name only differs "
            f"in spelling from \"{requested}\", so this is a "
            f"normalized match."
        )
    return f"I found a {kind_label} at {path} — an exact match."


# A local-location ask in the user's own words ("where is X", "location
# of X", "path of X", "locate X"). Used by guard_path_response only when
# NO file_manager result exists: if the reply still speaks an absolute
# path, that path was fabricated (from a web page or memory) and is
# replaced with an honest no-local-path statement.
_LOCATE_ASK_RE = _re.compile(
    r"(where\s+(?:is|are|'s)|location\s+of|locate\b|"
    r"what'?s\s+the\s+(?:location|path)|"
    r"tell\s+me\s+(?:the\s+)?(?:location|where|path)|"
    r"path\s+of\b)",
    _re.IGNORECASE,
)

# Absolute-path tokens in a reply ("C:\...", "\\server\..."). Spaces are
# allowed INSIDE a path ("C:\project friday"); quotes, commas, semicolons
# and angle brackets end it. Trailing punctuation is stripped afterward.
_DRIVE_PATH_RE = _re.compile(r"[A-Za-z]:[\\/][^\r\n\t\"',;<>]*")
_UNC_PATH_RE = _re.compile(r"\\\\[^\r\n\t\"',;<>]*")


def _spoken_paths(response):
    text = str(response or "")
    out = []
    for pattern in (_DRIVE_PATH_RE, _UNC_PATH_RE):
        for m in pattern.finditer(text):
            token = m.group(0).rstrip(".,!?)]};:")
            # A path can be followed by a note on the same line
            # ("C:\...\gur exact.txt — an exact match"). That note is
            # not part of the path, so truncate there before comparing
            # against the current tool results. Only a dash with
            # whitespace on BOTH sides is a separator — a bare hyphen
            # inside a path ("Godot_v4.6.3-stable_win64.exe.zip") is
            # part of the name and must survive.
            token = _re.split(r"\s+[\u2014\u2013-]\s+", token)[0].strip()
            token = _re.sub(r"\s*\([^)]*\)\s*$", "", token).strip()
            if token:
                out.append(token)
    return out


def _norm_path(path):
    try:
        return os.path.normcase(os.path.normpath(str(path)))
    except Exception:
        return str(path)


def _allowed_paths(tool_results):
    """
    Every absolute path a successful CURRENT local file_manager result
    produced (locate target, listing entries, candidates). This is the
    only evidence a reply may restate as a local path.
    """
    allowed = set()
    for result in tool_results or []:
        if getattr(result, "tool_name", "") != "file_manager":
            continue
        if getattr(result, "status", "") != "success":
            continue
        data = getattr(result, "data", None)
        if not isinstance(data, dict):
            continue
        for key in ("path", "location"):
            value = data.get(key)
            if isinstance(value, str) and value:
                allowed.add(_norm_path(value))
        for entry in (data.get("entries") or []):
            if isinstance(entry, dict) and entry.get("path"):
                allowed.add(_norm_path(entry["path"]))
        for candidate in (data.get("candidates") or []):
            if isinstance(candidate, dict) and candidate.get("path"):
                allowed.add(_norm_path(candidate["path"]))
    return allowed


def _claims_mostly_empty(text):
    """True when a reply asserts the listed folder is (nearly) empty
    ("empty", "nothing inside", "no files/folders", "only one",
    "except one", "a single ...") unless the assertion is negated
    ("not empty", "isn't empty", "non-empty"). Guards against the LLM
    echoing a stale stored listing ("the folder is empty, except one
    subfolder") that contradicts the real non-empty TOOL RESULTS.
    """
    low = _re.sub(r"[\u2018\u2019]", "'", str(text).lower())
    low = _re.sub(r"[^a-z0-9'\s]", " ", low)
    low = _re.sub(r"\s+", " ", low).strip()
    for pat in (
        r"\bempty\b",
        r"\bnothing\b",
        r"\bno (?:files?|folders?|items?|entries|contents|subfolders?|"
        r"subdirs?|files|subdirectories)\b",
        r"\bonly one\b",
        r"\bjust one\b",
        r"\bexcept one\b",
        r"\bexactly one\b",
        r"\bonly a single\b",
        r"\bjust a single\b",
        r"\ba single (?:file|folder|subfolder|item|entry|thing)\b",
    ):
        m = _re.search(pat, low)
        if not m:
            continue
        prefix = low[max(0, m.start() - 24):m.start()]
        if _re.search(
            r"(?:^|\s)(?:not|no|non|never|without|isn'?t|aren'?t|wasn'?t|"
            r"weren'?t|don'?t|doesn'?t|didn'?t|rather than|instead of)\s*$",
            prefix,
        ):
            continue
        return True
    return False


def _extract_snippet_claims(snippets):
    """
    Extracts verifiable factual claims from web search snippets.
    Returns a set of normalized claim strings (prices, versions, dates, specs, temps, weather).
    """
    claims = set()
    for snippet in snippets:
        if not isinstance(snippet, str):
            continue
        low = snippet.lower()
        # Prices
        for m in _PRICE_RE.finditer(snippet):
            claims.add(("price", m.group(0).lower()))
        # Versions
        for m in _VERSION_RE.finditer(snippet):
            claims.add(("version", m.group(0).lower()))
        # Dates
        for m in _DATE_RE.finditer(snippet):
            claims.add(("date", m.group(0).lower()))
        # Specs (GPU models, etc.)
        for m in _SPEC_RE.finditer(snippet):
            claims.add(("spec", m.group(0).lower()))
        # Temperature/weather
        for m in _TEMP_RE.finditer(snippet):
            claims.add(("temp", m.group(0).lower()))
        for m in _WEATHER_CONDITION_RE.finditer(snippet):
            claims.add(("weather", m.group(0).lower()))
        for m in _HUMIDITY_RE.finditer(snippet):
            claims.add(("humidity", m.group(0).lower()))
        for m in _PRESSURE_RE.finditer(snippet):
            claims.add(("pressure", m.group(0).lower()))
        for m in _WIND_RE.finditer(snippet):
            claims.add(("wind", m.group(0).lower()))
        # Other factual phrases near numbers
        for m in _re.finditer(r"\b\d+(?:\.\d+)?\s*(?:ghz|mhz|gb|tb|mb|watts?|w\b)", low):
            claims.add(("spec", m.group(0).lower()))
    return claims


def _extract_response_claims(response):
    """
    Extracts factual claims made in the response that require grounding.
    Returns a set of (claim_type, claim_text) tuples.
    """
    claims = set()
    low = response.lower()
    # Prices
    for m in _PRICE_RE.finditer(response):
        claims.add(("price", m.group(0).lower()))
    # Versions
    for m in _VERSION_RE.finditer(response):
        claims.add(("version", m.group(0).lower()))
    # Dates
    for m in _DATE_RE.finditer(response):
        claims.add(("date", m.group(0).lower()))
    # Specs
    for m in _SPEC_RE.finditer(response):
        claims.add(("spec", m.group(0).lower()))
    # Temperature/weather
    for m in _TEMP_RE.finditer(response):
        claims.add(("temp", m.group(0).lower()))
    for m in _WEATHER_CONDITION_RE.finditer(response):
        claims.add(("weather", m.group(0).lower()))
    for m in _HUMIDITY_RE.finditer(response):
        claims.add(("humidity", m.group(0).lower()))
    for m in _PRESSURE_RE.finditer(response):
        claims.add(("pressure", m.group(0).lower()))
    for m in _WIND_RE.finditer(response):
        claims.add(("wind", m.group(0).lower()))
    # Other numeric specs
    for m in _re.finditer(r"\b\d+(?:\.\d+)?\s*(?:ghz|mhz|gb|tb|mb|watts?|w\b)", low):
        claims.add(("spec", m.group(0).lower()))
    return claims


def _is_claim_grounded(claim, snippet_claims, threshold=0.8):
    """
    Checks if a response claim is grounded in snippet claims.
    Uses exact matching for prices, fuzzy matching for versions/specs/weather/temp.
    """
    claim_type, claim_text = claim
    for s_type, s_text in snippet_claims:
        if s_type != claim_type:
            continue
        if claim_type == "price":
            # Normalize prices for comparison
            c_norm = _re.sub(r"[\$,]", "", claim_text)
            s_norm = _re.sub(r"[\$,]", "", s_text)
            if c_norm == s_norm:
                return True
        else:
            # Fuzzy match for versions/specs/temp/weather/humidity/pressure/wind
            if _levenshtein_ratio(claim_text, s_text) >= threshold:
                return True
    return False


def _levenshtein_ratio(a: str, b: str) -> float:
    """Normalized Levenshtein similarity ratio (0.0 to 1.0)."""
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    if len(b) - len(a) > len(b) * 0.4:
        return 0.0
    previous_row = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        current_row = [i + 1]
        for j, cb in enumerate(b):
            insert_cost = current_row[j] + 1
            delete_cost = previous_row[j + 1] + 1
            replace_cost = previous_row[j] + (ca != cb)
            current_row.append(min(insert_cost, delete_cost, replace_cost))
        previous_row = current_row
    distance = previous_row[-1]
    max_len = max(len(a), len(b))
    return 1.0 - (distance / max_len)


def _deterministic_web_fallback(response, raw_text):
    """
    Honest fallback when web search claims are ungrounded.
    """
    low = (raw_text or "").lower()
    if _PRICE_RE.search(response):
        return ("I found some search results, but they don't contain a "
                "verified current price. The snippets show product pages "
                "but not the actual pricing. You may need to check a "
                "specific retailer for the latest price.")
    if _TEMP_RE.search(response) or _WEATHER_CONDITION_RE.search(response):
        return ("I found some search results, but they don't contain "
                "verified current weather information. The snippets show "
                "general pages about the location but not the current "
                "temperature or conditions. You may need to check a "
                "weather service for the latest forecast.")
    if _HUMIDITY_RE.search(response) or _PRESSURE_RE.search(response) or _WIND_RE.search(response):
        return ("The search results mention the location but don't "
                "contain verified current humidity, pressure, or wind data. "
                "You may need to check a weather service for those details.")
    if _VERSION_RE.search(response) or _SPEC_RE.search(response):
        return ("The search results mention the product but don't "
                "contain a verified version or specification number. "
                "I can't confirm the exact details from the snippets.")
    return "I found some search results but couldn't extract a verified answer from them."


def guard_listing_response(response, tool_results):
    """
    Returns a reply that is guaranteed to name only the file/folder
    names the tool results actually produced.

    - A successful listing whose LLM reply names any file not in the
      listing is replaced with a deterministic ground-truth listing.
    - A not_found result whose reply asks for permission (or fails to
      admit it was not found) is replaced with an honest not-found.
    - Anything else is returned unchanged.
    """
    if not response or not tool_results:
        return response

    results = [r for r in tool_results
               if getattr(r, "tool_name", "") == "file_manager"]
    if not results:
        return response

    has_success_listing = any(
        getattr(r, "status", "") == "success"
        and isinstance(getattr(r, "data", None), dict)
        and "entries" in (getattr(r, "data") or {})
        for r in results
    )

    if has_success_listing:
        first_listing = None
        for r in results:
            if getattr(r, "status", "") != "success":
                continue
            data = getattr(r, "data", None)
            if not isinstance(data, dict) or "entries" not in data:
                continue
            if first_listing is None:
                first_listing = data
            allowed = [
                e.get("name") for e in (data.get("entries") or [])
                if isinstance(e, dict) and e.get("name")
            ]
            if _fabricated_in(response, allowed):
                return _deterministic_listing(data)
        # A successful listing is a SAFE read-only action: permission
        # language is never correct here and must not reach the user.
        if first_listing is not None and (
                _GRANT_RE.search(response) or _PERM_RE.search(response)):
            return _deterministic_listing(first_listing)
        # A successful listing whose reply denies the success (claims it
        # could not find / could not access / does not know what is
        # inside) contradicts the actual outcome.
        if first_listing is not None and (
                _DENIAL_RE.search(response)
                or _INSIDE_UNKNOWN_RE.search(response)):
            return _deterministic_listing(first_listing)
        # A content-state assertion ("empty", "only one ...") that
        # contradicts a non-empty first listing means the LLM echoed a
        # stored listing instead of the fresh TOOL RESULTS.
        if first_listing is not None:
            entries = [
                e.get("name") for e in (first_listing.get("entries") or [])
                if isinstance(e, dict) and e.get("name")
            ]
            if entries and _claims_mostly_empty(response):
                return _deterministic_listing(first_listing)
        return response

    if any(getattr(r, "status", "") == "not_found" for r in results):
        if (_GRANT_RE.search(response) or _PERM_RE.search(response)
                or not _NOTFOUND_RE.search(response)):
            return _deterministic_not_found()

    if any(getattr(r, "status", "") == "failure" for r in results):
        # A failed file operation produced no names and no outcome:
        # permission language, any file name, or a denial/unknown
        # response in the reply are all wrong here.
        if (_GRANT_RE.search(response) or _PERM_RE.search(response)
                or _fabricated_in(response, [])
                or _DENIAL_RE.search(response)
                or _INSIDE_UNKNOWN_RE.search(response)
                or _NOINFO_RE.search(response)):
            return _deterministic_failure()

    return response


def guard_path_response(response, tool_results, raw_text=None):
    """
    Universal local-path truth guard. Guarantees the final reply only
    ever reports a local path that a SUCCESSFUL file_manager result on
    the CURRENT turn actually produced — never a web result, never a
    memory/LLM guess, never an "improved" version of a found path.

    - A locate result is the answer itself: the reply is regenerated
      deterministically from the tool result, so the path, its kind,
      the match type (exact / normalized / fuzzy), and every real
      multiple match are stated exactly and nothing else is invented.
    - A non-locate file turn that speaks an absolute path not present
      in the current results is a fabrication and is replaced with the
      deterministic listing / honest not-found.
    - A turn with NO local result (web-only or zero results) that is a
      local-location ask and still speaks an absolute path is replaced
      with an honest "not on your computer" statement, so a web page
      can never masquerade as a local location.
    """
    if not response or not str(response).strip():
        return response

    results = list(tool_results or [])
    fm = [
        r for r in results
        if getattr(r, "tool_name", "") == "file_manager"
    ]

    # ---- LOCATE branch: the location IS the tool result. ----------
    locate_results = [
        r for r in fm if getattr(r, "action", "") == "locate"
    ]
    if locate_results:
        result = locate_results[-1]
        data = getattr(result, "data", None)
        if not isinstance(data, dict):
            data = {}
        if getattr(result, "status", "") == "success" and data.get("found"):
            return _deterministic_locate(data)
        requested = (getattr(result, "metadata", None) or {}).get(
            "requested"
        )
        if not requested:
            requested = data.get("requested")
        if requested:
            return _deterministic_not_found_named(requested)
        return _deterministic_not_found()

    # ---- Other file turns: an absolute path outside the current
    # successful results is fabricated. -----------------------------
    if fm:
        spoken = _spoken_paths(response)
        if spoken:
            allowed = _allowed_paths(results)
            fabricated = [
                p for p in spoken if _norm_path(p) not in allowed
            ]
            if fabricated:
                for r in fm:
                    data = getattr(r, "data", None)
                    if (getattr(r, "status", "") == "success"
                            and isinstance(data, dict)
                            and "entries" in data):
                        return _deterministic_listing(data)
                if any(getattr(r, "status", "") == "not_found"
                       for r in fm):
                    return _deterministic_not_found()
                return _deterministic_failure()
        return response

    # ---- No local result: a local-location ask that still speaks an
    # absolute path was built from web info or memory. ---------------
    if _LOCATE_ASK_RE.search(str(raw_text or "")):
        if _spoken_paths(response):
            return _deterministic_no_local_path()

    return response


def guard_web_response(response, tool_results, raw_text=None):
    """
    Web search grounding guard. Ensures factual claims in the response
    (prices, versions, dates, specs) are actually present in the web
    search snippets. Ungrounded claims are replaced with an honest fallback.
    """
    if not response or not str(response).strip():
        return response

    results = list(tool_results or [])
    web_results = [
        r for r in results
        if getattr(r, "tool_name", "") == "web_search"
        and getattr(r, "status", "") == "success"
    ]
    if not web_results:
        return response

    # Collect all snippets from successful web search results
    snippets = []
    for result in web_results:
        data = getattr(result, "data", None)
        if isinstance(data, dict):
            res_list = data.get("results")
            if isinstance(res_list, list):
                for item in res_list:
                    if isinstance(item, dict):
                        snippet = item.get("snippet")
                        if snippet:
                            snippets.append(snippet)

    if not snippets:
        return response

    # Extract claims from snippets and response
    snippet_claims = _extract_snippet_claims(snippets)
    response_claims = _extract_response_claims(response)

    # Check each response claim for grounding
    ungrounded = []
    for claim in response_claims:
        if not _is_claim_grounded(claim, snippet_claims):
            ungrounded.append(claim)

    if ungrounded:
        # Response contains ungrounded factual claims - replace with honest fallback
        return _deterministic_web_fallback(response, raw_text)

    return response