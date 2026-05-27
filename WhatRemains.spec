# -*- mode: python ; coding: utf-8 -*-
# What Remains? — PyInstaller spec file
# Run with: pyinstaller WhatRemains.spec

from pathlib import Path

ROOT    = Path(SPECPATH)
APP_DIR = ROOT / "the-app" / "src" / "the-app-name"

a = Analysis(
    [str(APP_DIR / "main.py")],
    pathex=[str(APP_DIR)],
    binaries=[],
    datas=[
        (str(APP_DIR / "assets"),                    "assets"),
        (str(APP_DIR / "backend" / "keybinds.json"), "backend"),
        (str(APP_DIR / "backend" / "game.db"),       "backend"),
        (str(APP_DIR / "assets" / "scenarios.csv"), "."),
        (str(APP_DIR / "assets" / "scenarios.json"), "."),

    ],
    hiddenimports=[
        # PIL
        "PIL._tkinter_finder",
        "PIL.Image",
        "PIL.ImageTk",
        # pygame
        "pygame",
        "pygame.mixer",
        "pygame.mixer.music",
        # supabase stack — must all be present
        "supabase",
        "postgrest",
        "postgrest._sync.client",
        "postgrest._async.client",
        "gotrue",
        "gotrue._sync.client",
        "gotrue._async.client",
        "storage3",
        "storage3._sync.client",
        "storage3._async.client",
        "storage3._async.analytics",
        "realtime",
        "supabase_functions",
        # pyiceberg — pulled in by storage3, cannot be excluded
        "pyiceberg",
        "pyiceberg.catalog",
        "pyiceberg.serializers",
        "pyiceberg.table",
        "pyiceberg.expressions",
        "pyiceberg.expressions.parser",
        "pyparsing",
        "pyparsing.testing",
        # unittest — pulled in by pyparsing
        "unittest",
        "unittest.mock",
        # http
        "httpx",
        "httpcore",
        "h2",
        "hpack",
        "hyperframe",
        # other deps
        "dotenv",
        "python_dotenv",
        "bcrypt",
        "plyer",
        "plyer.platforms.win.notification",
        "cryptography",
        "jwt",
        "pydantic",
        "pydantic_core",
        "anyio",
        "anyio._backends._asyncio",
        "anyio._backends._trio",
        "sniffio",
        "websockets",
    ],
    hookspath=[],
    hooksconfig={},
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

pyz = PYZ(a.pure)

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
    icon="the-app/src/the-app-name/assets/images/icon-cream.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="WhatRemains",
)
