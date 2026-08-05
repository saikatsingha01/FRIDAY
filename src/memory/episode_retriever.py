from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from src.memory.episode_manager import get_all_episodes
from src.ai.llm_interface import llm


@dataclass
class EpisodeQuery:
    """
    A structured episodic retrieval instruction built from
    LanguageUnderstanding. The retriever never sees raw user text;
    it only sees entities, category signals and a scope flag.
    """

    keywords: List[str] = field(default_factory=list)
    # content words from Understanding entities

    categories: List[str] = field(default_factory=list)
    # category signals from Understanding (weak boost, never a gate)

    scope: str = "current"
    # "current" | "history"

    query_text: Optional[str] = None
    # Used ONLY for embedding scoring — never parsed.

    max_results: int = 3


def build_episode_query(understanding) -> EpisodeQuery:
    """
    Builds an EpisodeQuery from a LanguageUnderstanding object.
    Raw user text is only embedded for semantic scoring, never parsed.
    """
    query = EpisodeQuery()

    if understanding is None:
        return query

    scope = (understanding.memory.memory_scope or "current").lower()
    if scope in ("history", "episodic"):
        query.scope = "history"

    category = (
        understanding.semantic.category or ""
    ).lower().strip()

    if category:
        query.categories = [category]

    keywords = []

    for entity in understanding.semantic.entities:
        if hasattr(entity, "text"):
            text = entity.text.lower()
        elif isinstance(entity, dict):
            text = entity.get("text", "").lower()
        else:
            continue
        for word in text.split():
            if len(word) > 2:
                keywords.append(word)

    # When no entity survives (a sparse understanding of a topic
    # question like "what did we plan for the internship"), the
    # category still names the domain. Its representative keywords
    # are a weak, generic retrieval boost — never a meaning decision,
    # and never a gate (they only add score on top of embedding).
    if category:
        try:
            from src.memory.memory_query_builder import CATEGORY_KEYWORDS
            keywords += CATEGORY_KEYWORDS.get(category, [])
        except Exception:
            pass

    query.keywords = list(set(keywords))

    if understanding.raw_text:
        query.query_text = understanding.raw_text

    return query


STOP_WORDS = {

    "the",
    "a",
    "an",

    "is",
    "are",
    "was",
    "were",

    "i",
    "me",
    "my",
    "you",
    "your",

    "what",
    "who",
    "where",
    "when",
    "why",
    "how",

    "do",
    "does",
    "did",

    "remember",
    "recall",

    "conversation",
    "chat",
    "previous",
    "last",

    "please"

}


def extract_keywords(text):

    words = []

    for word in (text or "").lower().split():

        word = word.strip(".,?!")

        if len(word) < 3:
            continue

        if word in STOP_WORDS:
            continue

        words.append(word)

    return words


def _get_embedding(text):

    try:
        provider = llm.get_provider()
        if provider is None or not hasattr(provider, "embed"):
            return None
        return provider.embed(text)
    except Exception:
        return None


def _cosine(a, b):

    if not a or not b or len(a) != len(b):
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = (sum(x * x for x in a) ** 0.5) or 1.0
    norm_b = (sum(y * y for y in b) ** 0.5) or 1.0

    return dot / (norm_a * norm_b)


def retrieve_relevant_episodes(query, max_results=None):
    """
    Retrieves episodic memories using a structured EpisodeQuery.

    Legacy callers may still pass a raw string; it is converted
    with extract_keywords. The main pipeline passes EpisodeQuery.
    """

    if isinstance(query, str):
        keywords = extract_keywords(query)
        query_obj = EpisodeQuery(
            keywords=keywords,
            query_text=query,
        )
    else:
        query_obj = query

    limit = max_results or query_obj.max_results

    episodes = get_all_episodes()

    if not episodes:
        return []

    query_vec = None
    if query_obj.query_text:
        query_vec = _get_embedding(query_obj.query_text)

    episode_vecs = {}
    if query_vec is not None:
        for episode in episodes:
            vec = _get_embedding(episode.get("summary", ""))
            if vec is not None:
                episode_vecs[id(episode)] = vec

    scored = []

    for episode in episodes:

        score = 0

        summary = episode.get("summary", "").lower()
        keywords = [
            k.lower()
            for k in episode.get("keywords", [])
        ]
        entities = [
            str(e).lower()
            for e in episode.get("entities", [])
        ]

        # Keyword overlap against structured query keywords.
        overlap = 0
        for word in query_obj.keywords:
            if word in summary or word in keywords or word in " ".join(entities):
                overlap += 1
        score += overlap * 20

        # History scope: any prior episode is relevant for
        # "what was before" questions — no phrase matching needed.
        if query_obj.scope == "history":
            score += 25

        # Recency bonus for history-scope recall: a question about what
        # was discussed refers most strongly to the most recent
        # conversation. Decays with age so old but important episodes
        # still rank fairly alongside fresh ones.
        if query_obj.scope == "history":
            ts = episode.get("timestamp", "")
            if ts:
                try:
                    age_hours = (
                        datetime.now()
                        - datetime.fromisoformat(ts)
                    ).total_seconds() / 3600.0
                    if age_hours <= 24:
                        score += 20
                    elif age_hours <= 72:
                        score += 10
                    elif age_hours <= 168:
                        score += 5
                except ValueError:
                    pass

        # Semantic similarity — cross-vocabulary recall with a
        # 0.5 floor / 0.7 ramp like the semantic memory retriever.
        vec = episode_vecs.get(id(episode))
        if vec is not None:
            sim = _cosine(query_vec, vec)
            if sim > 0.5:
                score += int(60 * min(1.0, (sim - 0.5) / 0.2))

        score += episode.get("importance", 0)

        if score >= 30:
            scored.append((score, episode))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        episode
        for _, episode in scored[:limit]
    ]
