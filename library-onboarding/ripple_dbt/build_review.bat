@echo off
REM ============================================================================
REM The ONLY sanctioned way to rebuild the review marts on Windows.
REM
REM WHY THIS WRAPPER EXISTS (audit F1, 2026-08-01): a bare `dbt build` on
REM Windows read the UTF-8 model files as cp1252 and shipped every em-dash to
REM analysts as mojibake, in 792 headlines and every caveat. PYTHONUTF8=1
REM forces Python (and therefore dbt's file reads) to UTF-8. If someone runs
REM a bare build anyway, tests/assert_no_mojibake.sql fails the build.
REM
REM POLICY no_selectorless_dbt_build: this wrapper always selects marts.review.
REM ============================================================================
setlocal
set PYTHONUTF8=1
cd /d "%~dp0"
dbt build --select marts.review %*
endlocal
