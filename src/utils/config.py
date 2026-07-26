import json
from pathlib import Path

CONFIG_PATH = Path("config/settings.json")


def load_settings():
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print("[ERROR] Configuration file not found.")
        return None