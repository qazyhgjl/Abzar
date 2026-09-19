@echo off
setlocal
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python main.py
