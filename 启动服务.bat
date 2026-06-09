@echo off
chcp 65001 > nul
title AI Travel Assistant
cd /d "%~dp0"
set PYTHONPATH=%~dp0
echo Starting AI Travel Assistant...
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
