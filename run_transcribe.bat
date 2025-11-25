@echo off
cd /d "%~dp0"
.venv\Scripts\python.exe src\transcribe.py
pause
