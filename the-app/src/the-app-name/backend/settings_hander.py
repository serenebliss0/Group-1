import json
from pathlib import Path

KEYBINDS_FILE = Path("_keybinds.json")


def load_keybinds() -> dict:
    if not KEYBINDS_FILE.exists():
        return {}
    with open(KEYBINDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_keybinds(keybinds: dict):
    with open(KEYBINDS_FILE, "w", encoding="utf-8") as f:
        json.dump(keybinds, f, indent=4)


def update_keybind(action: str, new_key: str):
    keybinds = load_keybinds()
    keybinds[action] = new_key
    save_keybinds(keybinds)


def get_keybind(action: str, default: str = "") -> str:
    return load_keybinds().get(action, default)


def reset_keybinds(defaults: dict):
    save_keybinds(defaults)