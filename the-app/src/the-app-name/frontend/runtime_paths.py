# runtime_paths.py
# Drop this file in the-app/src/the-app-name/
# Import it at the top of main.py:
#   from runtime_paths import BASE_DIR, ASSETS_DIR, SCENARIOS_PATH

import sys
from pathlib import Path


def _get_base_dir() -> Path:
    """
    Returns the correct base directory whether running:
    - normally (python main.py)
    - as a PyInstaller bundle (WhatRemains.exe)
    """
    if getattr(sys, "frozen", False):
        # Running inside PyInstaller bundle
        return Path(sys._MEIPASS)
    else:
        # Running normally
        return Path(__file__).resolve().parent


BASE_DIR = _get_base_dir()
ASSETS_DIR = BASE_DIR / "assets"
BACKEND_DIR = BASE_DIR / "backend"
SCENARIOS_PATH = BASE_DIR / "scenarios.csv"
SOUNDS_DIR = ASSETS_DIR / "sounds"
IMAGES_DIR = ASSETS_DIR / "images"
FONTS_DIR = ASSETS_DIR / "fonts"
KEYBINDS_PATH = BACKEND_DIR / "keybinds.json"
DB_PATH = BACKEND_DIR / "game.db"
