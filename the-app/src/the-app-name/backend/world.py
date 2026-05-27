"""World layout: obstacles, interactables, and draw helpers."""

from .theme import (
    ASH,
    BUILDING,
    DIM,
    EMBER,
    MAP_HEIGHT,
    MAP_WIDTH,
    MUTED_GREEN,
    ROAD,
    TOXIC,
    TRASH,
    WATER_CLEAN,
    WATER_TOXIC,
)

# (x, y, w, h) obstacle blocks — buildings, walls
OBSTACLES = [
    {"x": 200, "y": 180, "w": 280, "h": 200},
    {"x": 520, "y": 320, "w": 180, "h": 140},
    {"x": 780, "y": 150, "w": 220, "h": 260},
    {"x": 1100, "y": 400, "w": 300, "h": 180},
    {"x": 1500, "y": 200, "w": 240, "h": 220},
    {"x": 1850, "y": 350, "w": 200, "h": 280},
    {"x": 2100, "y": 120, "w": 260, "h": 200},
    {"x": 400, "y": 700, "w": 350, "h": 160},
    {"x": 900, "y": 650, "w": 280, "h": 200},
    {"x": 1300, "y": 750, "w": 320, "h": 170},
    {"x": 1750, "y": 680, "w": 240, "h": 190},
    {"x": 2050, "y": 800, "w": 300, "h": 150},
    {"x": 250, "y": 1100, "w": 200, "h": 180},
    {"x": 600, "y": 1050, "w": 260, "h": 220},
    {"x": 1000, "y": 1200, "w": 300, "h": 200},
    {"x": 1450, "y": 1100, "w": 220, "h": 240},
    {"x": 1800, "y": 1150, "w": 280, "h": 180},
    {"x": 2200, "y": 1050, "w": 200, "h": 200},
    {"x": 300, "y": 1500, "w": 280, "h": 200},
    {"x": 750, "y": 1600, "w": 240, "h": 180},
    {"x": 1200, "y": 1550, "w": 300, "h": 220},
    {"x": 1650, "y": 1500, "w": 260, "h": 200},
    {"x": 2050, "y": 1450, "w": 220, "h": 250},
    {"x": 500, "y": 1900, "w": 400, "h": 180},
    {"x": 1100, "y": 1900, "w": 350, "h": 200},
    {"x": 1700, "y": 1850, "w": 300, "h": 220},
]

# Interactables: scenario_id links to scenarios.csv
INTERACTABLES = [
    {"id": "river", "scenario_id": 1, "x": 1180, "y": 920, "w": 120, "h": 80, "event_id": "river"},
    {"id": "pipe", "scenario_id": 2, "x": 680, "y": 540, "w": 60, "h": 60, "event_id": "pipe"},
    {"id": "tree", "scenario_id": 3, "x": 1580, "y": 1280, "w": 70, "h": 90, "event_id": "tree"},
    {"id": "purifier", "scenario_id": 4, "x": 1920, "y": 620, "w": 90, "h": 70, "event_id": "purifier"},
    {"id": "drone", "scenario_id": 5, "x": 420, "y": 1280, "w": 55, "h": 55, "event_id": "drone"},
    {"id": "terminal", "scenario_id": 6, "x": 1380, "y": 480, "w": 80, "h": 60, "event_id": "terminal"},
    {"id": "garbage", "scenario_id": 7, "x": 820, "y": 1780, "w": 140, "h": 100, "event_id": "garbage"},
    {"id": "lights", "scenario_id": 8, "x": 2280, "y": 1380, "w": 50, "h": 120, "event_id": "lights"},
    {"id": "sign", "scenario_id": 9, "x": 1050, "y": 380, "w": 50, "h": 70, "event_id": "sign"},
    {"id": "memory", "scenario_id": 10, "x": 520, "y": 920, "w": 40, "h": 40, "event_id": "memory"},
    {"id": "fountain", "scenario_id": 12, "x": 1220, "y": 1180, "w": 80, "h": 60, "event_id": "fountain"},
    {"id": "billboard", "scenario_id": 13, "x": 2180, "y": 480, "w": 100, "h": 80, "event_id": "billboard"},
    {"id": "journal", "scenario_id": 14, "x": 350, "y": 750, "w": 50, "h": 40, "event_id": "journal"},
    {"id": "tv", "scenario_id": 15, "x": 1550, "y": 950, "w": 70, "h": 50, "event_id": "tv"},
    {"id": "home", "scenario_id": 16, "x": 950, "y": 350, "w": 90, "h": 70, "event_id": "home"},
    {"id": "filter", "scenario_id": 17, "x": 350, "y": 1680, "w": 80, "h": 90, "event_id": "filter"},
    {"id": "factory", "scenario_id": 18, "x": 280, "y": 1700, "w": 120, "h": 100, "event_id": "factory"},
]

# Visual layers updated by world_flags
VISUAL_LAYERS = {
    "river": {"tag": "river", "clean_fill": WATER_CLEAN, "dirty_fill": WATER_TOXIC},
    "pipe": {"tag": "pipe_leak", "clean_fill": DIM, "dirty_fill": TOXIC},
    "tree": {"tag": "tree", "clean_fill": MUTED_GREEN, "dirty_fill": ASH},
    "purifier": {"tag": "purifier", "clean_fill": MUTED_GREEN, "dirty_fill": BUILDING},
    "lights": {"tag": "streetlights", "clean_fill": "#8a7a50", "dirty_fill": DIM},
    "garbage": {"tag": "garbage", "clean_fill": ROAD, "dirty_fill": TRASH},
}


def load_scenarios():
    import csv
    from pathlib import Path

    path = Path(__file__).resolve().parent.parent / "assets" / "scenarios.csv"
    scenarios = {}
    if not path.exists():
        return scenarios
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            scenarios[int(row["id"])] = row
    return scenarios
