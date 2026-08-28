@echo off
rem Auto-retry wrapper for the USAspending subawards full pull.
rem Safe to run any time: the loader resumes from checkpoint.json and exits 0 when done.
cd /d c:\Code\Ripple_v6
:loop
python -u scripts\usaspending_subawards_full_load.py --run >> data\usaspending_subawards\_stdout.log 2>&1
if errorlevel 1 (
  timeout /t 120 /nobreak >nul
  goto loop
)
