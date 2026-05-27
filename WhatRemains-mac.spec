# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import sys

ROOT = Path(SPECPATH)
APP_DIR = ROOT / "the-app" / "src" / "the-app-name"

block_cipher = None


a = Analysis(
    [str(APP_DIR / "main.py")],
    pathex=[str(APP_DIR)],
    binaries=[],
    datas=[
        (str(APP_DIR / "assets"), "assets"),
        (str(APP_DIR / "backend" / "keybinds.json"), "backend"),
        (str(APP_DIR / "assets" / "scenarios.csv"), "assets"),
        (str(APP_DIR / "assets" / "scenarios.json"), "assets"),
    ],
    hiddenimports=[
        "PIL._tkinter_finder",
        "PIL.Image",
        "PIL.ImageTk",

        "pygame",
        "pygame.mixer",
        "pygame.mixer.music",

        "supabase",
        "postgrest",
        "gotrue",
        "storage3",
        "realtime",

        "pyparsing",
        "unittest",
        "httpx",
        "httpcore",
        "h2",
        "hpack",
        "hyperframe",

        "dotenv",
        "python_dotenv",
        "bcrypt",
        "plyer",

        "cryptography",
        "jwt",
        "pydantic",
        "anyio",
        "sniffio",
        "websockets",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "IPython",
        "jupyter",
        "notebook",
        "tkinter.test",
        "test",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="WhatRemains",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon="the-app/src/the-app-name/assets/images/icon-cream.icns",
)


coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="WhatRemains",
)
