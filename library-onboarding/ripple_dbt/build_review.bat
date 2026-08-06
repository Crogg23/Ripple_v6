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
REM
REM ENGINE PIN (audit 2026-08-05, finding "two dbt binaries share the name"):
REM bare `dbt` on PATH resolves to the global dbt-fusion 2.0 preview, not the
REM project's dbt-core venv. This wrapper always runs the venv engine.
REM ============================================================================
setlocal
set PYTHONUTF8=1
cd /d "%~dp0"
set DBT_BIN=%~dp0..\..\.dbt-venv\Scripts\dbt.exe
if not exist "%DBT_BIN%" (
  echo ERROR: pinned dbt engine not found at %DBT_BIN% >&2
  exit /b 1
)
"%DBT_BIN%" build --select marts.review %*
endlocal
