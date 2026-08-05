"""
Generate fully random test data for the FRIDAY memory system.

- Backs up memory.json / episodes.json / memory_history.json first.
- Replaces the store with random memories + episodes (or appends with --keep).
- Prints an inventory so you can quiz FRIDAY on known random facts.

Usage:
    python generate_random_test_data.py [--memories 30] [--episodes 12]
                                        [--seed 42] [--keep]
"""

import argparse
import json
import random
import shutil
import os
from datetime import datetime, timedelta

PROJECT = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(PROJECT, "src", "memory")
BACKUP_DIR = os.path.join(
    os.environ.get("TEMP", PROJECT),
    "opencode",
    "memory_backup",
)

FILES = ["memory.json", "episodes.json", "memory_history.json"]


# =========================================================
# RANDOM CONTENT POOLS  (per-category, coherent)
# =========================================================

THINGS = [
    "movies", "books", "coffee", "music", "tea", "weather",
    "hiking", "photography", "cooking", "sports", "anime",
    "history", "space", "robotics", "writing", "chess",
]

FOODS = ["butter chicken", "pizza", "sushi", "tacos", "biryani",
         "dal makhani", "fried rice", "ramen", "pancakes", "lasagna"]
GAMES = ["Hades II", "Elden Ring", "Zelda", "Cyberpunk 2077",
         "Stardew Valley", "Rimworld", "Sekiro", "Baldur's Gate 3"]
LANGS = ["Python", "Rust", "Go", "TypeScript", "C++", "Kotlin", "Julia"]
TOOLS = ["VS Code", "Neovim", "Docker", "Git", "Jupyter", "Postman"]
DEVICES = ["iPhone 15", "Samsung Galaxy", "ThinkPad X1", "MacBook Air",
           "Dell XPS", "Pixel 9"]
MUSIC = ["jazz", "classical", "indie rock", "lo-fi", "synthwave", "hip-hop"]
COLORS = ["navy blue", "teal", "olive green", "burgundy", "charcoal", "coral"]
CITIES = ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Kolkata"]
NAMES = ["Aarav", "Maya", "Rohan", "Ananya", "Vikram", "Priya", "Sam"]
COURSES = ["B.Tech Computer Science", "MBA", "Data Science", "Physics",
           "Computer Engineering", "Economics", "Biotech"]
EXAMS = ["JEE", "GATE", "GRE", "CAT", "NEET", "UPSC"]
PLANS = ["learn Rust", "finish a marathon", "build a portfolio site",
         "learn guitar", "save for a trip", "start a youtube channel"]
PETS = ["dog", "cat", "parrot", "goldfish", "hamster"]
PETNAMES = ["Simba", "Milo", "Luna", "Ziggy", "Tofu", "Coco"]
EMOTIONS = ["great", "stressed", "excited", "anxious", "calm", "tired"]
ACTIVITIES = ["go to the gym", "play chess", "watch anime", "read",
              "go for long walks", "play basketball"]
TIMES = ["5:30", "6:00", "6:45", "7:15", "8:00", "9:30"]
SCIENCE_TOPICS = ["black holes", "genome editing", "quantum computing",
                  "deep sea life", "volcanoes", "the solar system"]
PROJECTS = ["a habit tracker app", "a recipe website", "a chess bot",
            "a portfolio site", "a home server", "a data dashboard"]


def _pick(pool, rng):
    return rng.choice(pool)


def random_fact(rng):
    """
    Builds one coherent random fact. Each category has its own
    templates and value pools so the text reads like a real user
    statement (no cross-category nonsense).
    """
    def tpl():
        return {
            "thing": rng.choice(THINGS),
            "food": rng.choice(FOODS),
            "game": rng.choice(GAMES),
            "lang": rng.choice(LANGS),
            "tool": rng.choice(TOOLS),
            "device": rng.choice(DEVICES),
            "music": rng.choice(MUSIC),
            "color": rng.choice(COLORS),
            "name": rng.choice(NAMES),
            "age": rng.randint(18, 45),
            "city": rng.choice(CITIES),
            "year": rng.randint(1, 4),
            "course": rng.choice(COURSES),
            "exam": rng.choice(EXAMS),
            "plan": rng.choice(PLANS),
            "pet": rng.choice(PETS),
            "petname": rng.choice(PETNAMES),
            "emotion": rng.choice(EMOTIONS),
            "activity": rng.choice(ACTIVITIES),
            "time": rng.choice(TIMES),
            "topic": rng.choice(SCIENCE_TOPICS),
            "project": rng.choice(PROJECTS),
        }

    POOLS = {
        "preference": [
            "My favorite {music} genre is {music}",
            "I love {thing}",
            "My favorite color is {color}",
            "I prefer {food} over {food}",
            "I really enjoy {music}",
        ],
        "programming": [
            "I code in {lang}",
            "I am learning {lang}",
            "My go-to language is {lang}",
            "I use {tool} for my projects",
            "I am comfortable with {lang} and {lang}",
        ],
        "hardware": [
            "My phone is a {device}",
            "I have a {device} laptop",
            "I use a {device} for gaming",
            "My daily driver is a {device}",
        ],
        "gaming": [
            "My favorite game is {game}",
            "I play {game}",
            "I am currently hooked on {game}",
            "I finished {game} last week",
            "I am going for 100 percent in {game}",
        ],
        "food": [
            "My favorite food is {food}",
            "I love {food} for dinner",
            "My go-to comfort food is {food}",
            "I cook {food} on weekends",
            "I would eat {food} every day",
        ],
        "identity": [
            "My name is {name}",
            "I am {age} years old",
            "I am from {city}",
            "My hometown is {city}",
            "I was born in {city}",
        ],
        "project": [
            "I am building {project}",
            "My current project is {project}",
            "I want to create {project}",
            "I am working on {project}",
            "My goal is to finish {project}",
        ],
        "science": [
            "I find {topic} fascinating",
            "I read about {topic} often",
            "My favorite topic is {topic}",
            "I am curious about {topic}",
        ],
        "education": [
            "I study {course}",
            "I am pursuing {course}",
            "I am in my {year} year of {course}",
            "My major is {course}",
            "I am preparing for {exam}",
        ],
        "planning": [
            "I plan to {plan}",
            "I am scheduling time to {plan}",
            "I want to {plan} next month",
            "I have a plan to {plan}",
        ],
        "memory": [
            "I remember that my favorite food is {food}",
            "I told you before that I play {game}",
            "Remember that I study {course}",
        ],
        "social": [
            "My best friend is {name}",
            "I have a {pet} named {petname}",
            "My friend {name} lives in {city}",
            "I usually hang out with {name}",
        ],
        "emotional": [
            "I feel {emotion} about my exams",
            "I get nervous before {exam}",
            "I am excited about {plan}",
            "I find {topic} relaxing",
        ],
        "general": [
            "I usually {activity} on weekends",
            "I wake up at {time}",
            "It takes me an hour to travel to work",
            "I read before bed",
            "I go for a walk every morning",
        ],
    }

    category = rng.choice(list(POOLS.keys()))
    template = rng.choice(POOLS[category])
    subs = tpl()
    text = template.format(**subs)

    tags = []
    for w in text.split():
        wl = w.strip(".,").lower()
        if len(wl) > 4 and wl not in tags:
            tags.append(wl)
    tags = tags[:4]

    return {
        "category": category,
        "text": text,
        "tags": tags,
        "value_words": [str(subs[k]).lower() for k in subs],
    }


def build_memory(rng, mem_id, fact, now):
    return {
        "id": mem_id,
        "text": fact["text"],
        "category": fact["category"],
        "importance": rng.randint(1, 10),
        "confidence": rng.randint(30, 100),
        "persistence": rng.choice(
            ["permanent", "permanent", "transient", "unknown"]
        ),
        "tags": fact["tags"],
        "source_text": fact["text"],
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "confidence_breakdown": {
            "stt": round(rng.uniform(0.8, 1.0), 2),
            "understanding": round(rng.uniform(0.8, 1.0), 2),
            "canonicalization": round(rng.uniform(0.8, 1.0), 2),
            "memory": round(rng.uniform(0.8, 1.0), 2),
            "retrieval": round(rng.uniform(0.8, 1.0), 2),
        },
        "retrieval_confidence": round(rng.uniform(0.3, 1.0), 2),
    }


EPISODE_TOPICS = [
    "discussed {food} and how my cooking experiment went",
    "talked about {course} and exam prep",
    "shared my progress on {plan}",
    "reviewed {game} strategy",
    "brainstormed ideas for {project}",
    "went over {topic} and what I learned about it",
    "we compared notes on {music} music",
    "chatted about my favorite {thing}",
    "walked through a {lang} problem together",
    "planned out my {plan}",
]


def build_episode(rng, ep_id, now):
    fact = random_fact(rng)
    summary = _pick(EPISODE_TOPICS, rng).format(**{
        "food": _pick(FOODS, rng),
        "course": _pick(COURSES, rng),
        "plan": _pick(PLANS, rng),
        "game": _pick(GAMES, rng),
        "project": _pick(PROJECTS, rng),
        "topic": _pick(SCIENCE_TOPICS, rng),
        "music": _pick(MUSIC, rng),
        "thing": _pick(THINGS, rng),
        "lang": _pick(LANGS, rng),
    })

    return {
        "id": ep_id,
        "summary": "Conversation: " + summary,
        "keywords": list(dict.fromkeys(fact["tags"])) or ["chat"],
        "entities": [],
        "importance": rng.randint(3, 9),
        "timestamp": now.isoformat(),
        "session_id": f"session-random-{ep_id}",
        "start_time": (now - timedelta(minutes=rng.randint(3, 30))).isoformat(),
        "end_time": now.isoformat(),
    }


def build_history(rng, old, new, now):
    return {
        "old_memory": {
            "id": old["id"], "text": old["text"],
            "category": old["category"],
            "importance": old["importance"],
            "confidence": old["confidence"],
        },
        "new_memory": new,
        "changed_at": now.isoformat(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memories", type=int, default=30)
    parser.add_argument("--episodes", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--keep", action="store_true",
                        help="append instead of replacing")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for name in FILES:
        src = os.path.join(MEMORY_DIR, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(
                BACKUP_DIR, f"{name}.randomtest.{stamp}.bak"))
    print("backed up to", BACKUP_DIR)

    # ---------------- memories ----------------
    old_memories = []
    mem_path = os.path.join(MEMORY_DIR, "memory.json")
    with open(mem_path, encoding="utf-8") as fh:
        old_memories = json.load(fh).get("memories", [])

    next_id = max([m.get("id", 0) for m in old_memories] or [0]) + 1

    memories = list(old_memories) if args.keep else []
    generated = []
    seen_mem_texts = {m["text"] for m in memories}
    for _ in range(args.memories):
        fact = random_fact(rng)
        for _try in range(60):
            if fact["text"] not in seen_mem_texts:
                break
            fact = random_fact(rng)
        seen_mem_texts.add(fact["text"])
        now = datetime.now() - timedelta(days=rng.randint(0, 60),
                                         hours=rng.randint(0, 23))
        mem = build_memory(rng, next_id, fact, now)
        memories.append(mem)
        generated.append(mem)
        next_id += 1

    with open(mem_path, "w", encoding="utf-8") as fh:
        json.dump({"memories": memories}, fh, indent=1, ensure_ascii=False)

    # ---------------- episodes ----------------
    ep_path = os.path.join(MEMORY_DIR, "episodes.json")
    with open(ep_path, encoding="utf-8") as fh:
        old_episodes = json.load(fh).get("episodes", [])

    next_ep_id = max([e.get("id", 0) for e in old_episodes] or [0]) + 1

    episodes = list(old_episodes) if args.keep else []
    generated_eps = []
    seen_ep_texts = {e["summary"] for e in episodes}
    for _ in range(args.episodes):
        now = datetime.now() - timedelta(days=rng.randint(0, 14),
                                         hours=rng.randint(0, 23))
        ep = build_episode(rng, next_ep_id, now)
        for _try in range(60):
            if ep["summary"] not in seen_ep_texts:
                break
            ep = build_episode(rng, next_ep_id, now)
        seen_ep_texts.add(ep["summary"])
        episodes.append(ep)
        generated_eps.append(ep)
        next_ep_id += 1

    with open(ep_path, "w", encoding="utf-8") as fh:
        json.dump({"episodes": episodes}, fh, indent=1, ensure_ascii=False)

    # ---------------- history trail ----------------
    if not args.keep:
        hist_path = os.path.join(MEMORY_DIR, "memory_history.json")
        with open(hist_path, encoding="utf-8") as fh:
            history = json.load(fh).get("history", [])

        now = datetime.now()
        for _ in range(6):
            old = build_memory(
                rng, next_id - rng.randint(1, 4),
                random_fact(rng),
                now - timedelta(days=rng.randint(5, 30)),
            )
            new = build_memory(
                rng, next_id - rng.randint(1, 4),
                random_fact(rng),
                now,
            )
            if old["text"] == new["text"]:
                continue
            history.append(build_history(rng, old, new, now))

        with open(hist_path, "w", encoding="utf-8") as fh:
            json.dump({"history": history}, fh, indent=1, ensure_ascii=False)

    # ---------------- inventory ----------------
    print(f"\n=== MEMORIES ({len(generated)}) ===")
    for m in generated:
        print(f"  [{m['id']}] ({m['category']:11s}) imp={m['importance']} "
              f"{m['text']}")
    print(f"\n=== EPISODES ({len(generated_eps)}) ===")
    for e in generated_eps:
        print(f"  [{e['id']}] imp={e['importance']} {e['summary']}")
    print(f"\nnext memory id will be: {next_id}")


if __name__ == "__main__":
    main()
