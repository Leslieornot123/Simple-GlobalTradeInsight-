@echo off
set PYTHONOPTIMIZE=1
set PYTHONUNBUFFERED=1
set PYTHONDONTWRITEBYTECODE=1
set PYTHONFAULTHANDLER=1

REM Add Python to PATH if not already there
set PATH=%PATH%;C:\Users\M S I\AppData\Local\Programs\Python\Python313

REM Run the script with optimizations
python -O %* 