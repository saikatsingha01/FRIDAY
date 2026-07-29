import json
import os
from datetime import datetime

EPISODE_FILE = os.path.join(
    os.path.dirname(__file__),
    "episodes.json"
)


def load_episodes():

    if not os.path.exists(EPISODE_FILE):

        return {
            "episodes": []
        }

    with open(
        EPISODE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_episodes(data):

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


def add_episode(summary, keywords, importance=5):

    data = load_episodes()

    episode = {

        "id": len(data["episodes"]) + 1,

        "summary": summary,

        "keywords": keywords,

        "importance": importance,

        "timestamp": datetime.now().isoformat()

    }

    data["episodes"].append(episode)

    save_episodes(data)

    return episode


def get_all_episodes():

    return load_episodes()["episodes"]


def delete_episode(episode_id):

    data = load_episodes()

    old_count = len(data["episodes"])

    data["episodes"] = [

        ep

        for ep in data["episodes"]

        if ep["id"] != episode_id

    ]

    save_episodes(data)

    return len(data["episodes"]) != old_count


def episode_count():

    return len(load_episodes()["episodes"])