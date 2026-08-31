@echo off
REM Double-click this file to start Ripple.
REM It opens automatically in your web browser at http://127.0.0.1:8890

cd /d "C:\Code\Ripple_v6"

echo Starting Ripple... this window must stay open while you use it.
echo.

pip install -q -r reading_room\requirements.txt

echo.
echo Ready. Opening in your browser now...
echo (If it doesn't open, go to http://127.0.0.1:8890 yourself)
echo.
echo The Reading Room opens at http://127.0.0.1:8890  (review desks)
echo The Playground runs at    http://127.0.0.1:8502  (explore + chart)
echo.
echo To stop: close this window, or press Ctrl+C.
echo.

start "Ripple Playground" cmd /c "streamlit run playground\app.py --server.port 8502 --server.address 127.0.0.1 --browser.gatherUsageStats false --server.headless true"
streamlit run reading_room\app.py --server.port 8890 --server.address 127.0.0.1 --browser.gatherUsageStats false

pause
