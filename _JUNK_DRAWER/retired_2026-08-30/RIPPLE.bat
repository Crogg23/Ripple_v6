@echo off
REM ============================================================================
REM Double-click this to open Ripple. One door.
REM
REM Opens at http://127.0.0.1:8500 with three rooms:
REM   Findings  - every cross-source pattern the Library already connects
REM   Look up   - any company/person/ship, and everything held on them
REM   Explore   - links to the SQL room, the review desk, the chart bench
REM
REM The older START_HERE.bat still works and opens the review desk + SQL room
REM directly; this one is the front door.
REM ============================================================================
cd /d "C:\Code\Ripple_v6"

echo Starting Ripple... keep this window open while you use it.
echo.
echo   Ripple opens at http://127.0.0.1:8500
echo.
echo To stop: close this window, or press Ctrl+C.
echo.

streamlit run home\app.py --server.port 8500 --server.address 127.0.0.1 --browser.gatherUsageStats false

pause
