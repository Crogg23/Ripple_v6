@echo off
REM ============================================================================
REM The sanctioned way to run the dbt test suite on Windows.
REM
REM WHY (verification 2026-08-11, defect class 12): 505/607 marts declared
REM uniqueness tests but there was NO evidence the suite had ever been run --
REM no artifacts, last dbt log predating two weeks of rebuilds. Unverified
REM guards are not guards. First full run 2026-08-11: 1,173 pass / 9 fail /
REM 2 error out of 1,186 unique tests (log: logs/dbt_unique_test_run_2026-08-11.log).
REM
REM Same engine pin + UTF-8 rationale as build_review.bat.
REM Default selection is the unique tests (the grain guards); pass extra args
REM to widen, e.g.:  run_tests.bat            (unique tests only)
REM                  run_tests.bat --select test_type:generic
REM ============================================================================
setlocal
set PYTHONUTF8=1
cd /d "%~dp0"
set DBT_BIN=%~dp0..\..\.dbt-venv\Scripts\dbt.exe
if not exist "%DBT_BIN%" (
  echo ERROR: pinned dbt engine not found at %DBT_BIN% >&2
  exit /b 1
)
if "%~1"=="" (
  "%DBT_BIN%" test --select test_name:unique
) else (
  "%DBT_BIN%" test %*
)
endlocal
