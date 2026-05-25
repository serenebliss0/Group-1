@echo off
setlocal enabledelayedexpansion

echo.
echo  ================================
echo   What Remains? -- Build Script
echo  ================================
echo.

:: ── Check Python ──
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Make sure Python is in your PATH.
    pause & exit /b 1
)

:: ── Check venv ──
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] venv not found. Run: python -m venv venv
    pause & exit /b 1
)

:: ── Activate venv ──
echo [1/5] Activating virtual environment...
call venv\Scripts\activate.bat

:: ── Install dependencies ──
echo [2/5] Installing dependencies...
pip install -r requirements.txt --quiet
pip install pyinstaller --quiet

:: ── Clean previous build ──
echo [3/5] Cleaning previous build...
if exist "dist\WhatRemains" rmdir /s /q "dist\WhatRemains"
if exist "build\WhatRemains"  rmdir /s /q "build\WhatRemains"

:: ── Run PyInstaller ──
echo [4/5] Building with PyInstaller...
pyinstaller WhatRemains.spec --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller failed. Check the output above.
    pause & exit /b 1
)

:: ── Copy .env if it exists ──
echo [5/5] Copying runtime files...
set ENV_SRC=the-app\src\the-app-name\.env
if exist "%ENV_SRC%" (
    copy "%ENV_SRC%" "dist\WhatRemains\.env" >nul
    echo        .env copied
) else (
    echo        [WARN] No .env found -- Supabase won't work without it
)

:: ── Done ──
echo.
echo  ================================
echo   Build complete!
echo   Output: dist\WhatRemains\
echo   Run:    dist\WhatRemains\WhatRemains.exe
echo  ================================
echo.
pause
