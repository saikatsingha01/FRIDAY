import json
import os
from datetime import datetime

EPISODE_FILE = os.path.join(
    os.path.dirname(__file__),
    "episodes.json"
)


def load_episodes():
    """
    Loads all episodic memories.
    """

    if not os.path.exists(EPISODE_FILE):
        return {"episodes": []}

    try:
        with open(
            EPISODE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if "episodes" not in data:
            data["episodes"] = []

        return data

    except Exception:
        return {"episodes": []}


def save_episodes(data):
    """
    Saves episodic memories.
    """

    with open(
        EPISODE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_episode(
    summary,
    keywords,
    importance=5,
    session_id=None,
    semantic_ids=None,
    entities=None,
    topic_clusters=None,
    start_time=None,
    end_time=None,
):
    """
    Creates a new episode.

    Extended schema (Issue 6): an episode represents one session of
    conversation. Topic/entity fields are retrieval keys; semantic_ids
    reference the semantic memories this session touched.
    """

    data = load_episodes()

    episodes = data["episodes"]

    episode = {

        "id": (
            max(
                [ep["id"] for ep in episodes],
                default=0
            ) + 1
        ),

        "summary": summary.strip(),

        "keywords": sorted(
            list(
                set(
                    word.lower()
                    for word in keywords
                    if word
                )
            )
        ),

        "importance": max(
            1,
            min(10, importance)
        ),

        "timestamp": datetime.now().isoformat()
    }

    if session_id:
        episode["session_id"] = session_id

    if semantic_ids:
        episode["semantic_ids"] = list(semantic_ids)

    if entities:
        episode["entities"] = list(entities)

    if topic_clusters:
        episode["topic_clusters"] = list(topic_clusters)

    if start_time:
        episode["start_time"] = start_time

    if end_time:
        episode["end_time"] = end_time

    episodes.append(episode)

    save_episodes(data)

    return episode


def get_all_episodes():

    return load_episodes()["episodes"]


def get_episode(episode_id):

    for episode in get_all_episodes():

        if episode["id"] == episode_id:
            return episode

    return None


def delete_episode(episode_id):

    data = load_episodes()

    before = len(data["episodes"])

    data["episodes"] = [

        episode

        for episode in data["episodes"]

        if episode["id"] != episode_id

    ]

    save_episodes(data)

    return len(data["episodes"]) != before


def clear_episodes():

    save_episodes({
        "episodes": []
    })


def episode_count():

    return len(
        get_all_episodes()
    )