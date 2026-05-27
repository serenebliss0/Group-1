"""Runtime and persisted game state (environment score, events, saves)."""

import json
from datetime import datetime
from pathlib import Path

from .theme import MAP_HEIGHT, MAP_WIDTH

SAVE_DIR = Path(__file__).resolve().parent / "saves"
SETTINGS_PATH = Path(__file__).resolve().parent / "settings.json"

DEFAULT_SETTINGS = {
    "music_volume": 0.6,
    "sfx_volume": 0.8,
    "text_speed": 35,
    "fullscreen": False,
    "reduced_motion": False,
    "tutorial_seen": False,
}


class GameState:
    """Singleton-style state shared across screens."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reset_run()
        return cls._instance

    def reset_run(self):
        self.env_score = 50
        self.completed_events = set()
        self.world_flags = {}
        self.triggered_interactables = set()
        self.memory_fragments = 0
        self.run_id = None
        self.playtime_seconds = 0
        self.player_x = MAP_WIDTH // 2
        self.player_y = MAP_HEIGHT // 2
        self._play_start = None

    def restoration_percent(self):
        return max(0, min(100, int(self.env_score)))

    def apply_choice(self, score_delta, event_id=None):
        self.env_score = max(0, min(100, self.env_score + score_delta))
        if event_id:
            self.completed_events.add(event_id)
            self.world_flags[event_id] = True

    def mark_interactable(self, obj_id):
        self.triggered_interactables.add(obj_id)

    def ending_key(self):
        if self.env_score >= 70:
            return "good"
        if self.env_score >= 40:
            return "neutral"
        return "bad"

    def to_save_dict(self):
        return {
            "env_score": self.env_score,
            "completed_events": list(self.completed_events),
            "world_flags": self.world_flags,
            "triggered_interactables": list(self.triggered_interactables),
            "memory_fragments": self.memory_fragments,
            "player_x": self.player_x,
            "player_y": self.player_y,
            "playtime_seconds": self.playtime_seconds,
            "saved_at": datetime.now().isoformat(),
        }

    def load_from_dict(self, data):
        if not data:
            return False
        self.env_score = data.get("env_score", 50)
        self.completed_events = set(data.get("completed_events", []))
        self.world_flags = data.get("world_flags", {})
        self.triggered_interactables = set(data.get("triggered_interactables", []))
        self.memory_fragments = data.get("memory_fragments", 0)
        self.player_x = data.get("player_x", MAP_WIDTH // 2)
        self.player_y = data.get("player_y", MAP_HEIGHT // 2)
        self.playtime_seconds = data.get("playtime_seconds", 0)
        return True


def _save_path(username):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in (username or "guest"))
    return SAVE_DIR / f"{safe}.json"


def save_game(username, state: GameState):
    path = _save_path(username)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state.to_save_dict(), f, indent=2)
    return path


def load_game(username):
    path = _save_path(username)
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def has_save(username):
    return _save_path(username).exists()


def load_settings():
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
