@echo off
title HR Records Manager – Server
cd /d "%~dp0"
echo.
echo  Starting HR Records Manager server...
echo.

python --version >nul 2>&1
if %errorlevel% == 0 (
    python server_demo.py
    goto end
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    py server_demo.py
    goto end
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    python3 server_demo.py
    goto end
)

echo  ERROR: Python is not installed or not in PATH.
echo.
echo  Download Python at: https://www.python.org/downloads/
echo  During installation, check "Add Python to PATH"
echo.

:end
echo.
echo  Server stopped.
pause
