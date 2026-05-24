"""Lightweight quest / event registry."""

EVENTS = {
    "river": {
        "label": "Dead River",
        "score_good": 12,
        "score_bad": -10,
        "flag": "river_clean",
    },
    "pipe": {
        "label": "Toxic Pipe",
        "score_good": 10,
        "score_bad": -8,
        "flag": "pipe_sealed",
    },
    "tree": {
        "label": "Dying Tree",
        "score_good": 8,
        "score_bad": -5,
        "flag": "tree_planted",
    },
    "purifier": {
        "label": "Water Purifier",
        "score_good": 15,
        "score_bad": -12,
        "flag": "purifier_on",
    },
    "drone": {
        "label": "Broken Drone",
        "score_good": 6,
        "score_bad": -4,
        "flag": "drone_logged",
    },
    "terminal": {
        "label": "Abandoned Terminal",
        "score_good": 7,
        "score_bad": -3,
        "flag": "logs_recovered",
    },
    "garbage": {
        "label": "Garbage Mountain",
        "score_good": 14,
        "score_bad": -15,
        "flag": "waste_cleared",
    },
    "lights": {
        "label": "Broken Streetlights",
        "score_good": 5,
        "score_bad": -2,
        "flag": "lights_on",
    },
    "sign": {
        "label": "Warning Sign",
        "score_good": 3,
        "score_bad": -6,
        "flag": "sign_read",
    },
    "memory": {
        "label": "Memory Fragment",
        "score_good": 4,
        "score_bad": 0,
        "flag": "memory_found",
    },
    "fountain": {"label": "Ruined Fountain", "score_good": 5, "score_bad": -3, "flag": "fountain_clear"},
    "billboard": {"label": "Cracked Billboard", "score_good": 4, "score_bad": -4, "flag": "billboard_read"},
    "journal": {"label": "Old Journal", "score_good": 6, "score_bad": -2, "flag": "journal_read"},
    "tv": {"label": "Broken TV", "score_good": 3, "score_bad": -5, "flag": "tv_checked"},
    "home": {"label": "Forgotten Home", "score_good": 9, "score_bad": -7, "flag": "home_entered"},
    "filter": {"label": "Air Filtration", "score_good": 12, "score_bad": -9, "flag": "filter_on"},
    "factory": {"label": "Abandoned Factory", "score_good": 8, "score_bad": -11, "flag": "factory_logged"},
}


def choice_delta(choice_index, scenario_row):
    """Map choice_a/b/c to score column or event defaults."""
    keys = ("score_a", "score_b", "score_c")
    col = keys[choice_index] if choice_index < len(keys) else "score_a"
    raw = scenario_row.get(col, "0")
    try:
        return int(raw)
    except (TypeError, ValueError):
        return 0


def resolve_choice(choice_index, scenario_row, game_state):
    delta = choice_delta(choice_index, scenario_row)
    event_id = scenario_row.get("event_id", "").strip()
    if event_id and event_id in EVENTS:
        ev = EVENTS[event_id]
        if delta >= 0:
            delta = max(delta, ev["score_good"] // 2)
        else:
            delta = min(delta, -abs(ev["score_bad"] // 2))
    game_state.apply_choice(delta, event_id if event_id else None)
    if scenario_row.get("memory") == "1":
        game_state.memory_fragments += 1
    return delta
