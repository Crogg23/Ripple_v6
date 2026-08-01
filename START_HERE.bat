@echo off
REM Double-click this file to start Ripple.
REM It opens automatically in your web browser at http://127.0.0.1:8890

cd /d "%~dp0"

echo Starting Ripple... this window must stay open while you use it.
echo.

pip install -q -r reading_room\requirements.txt

echo.
echo Ready. Opening in your browser now...
echo (If it doesn't open, go to http://127.0.0.1:8890 yourself)
echo.
echo To stop: close this window, or press Ctrl+C.
echo.

streamlit run reading_room\app.py --server.port 8890 --server.address 127.0.0.1 --browser.gatherUsageStats false

pause
