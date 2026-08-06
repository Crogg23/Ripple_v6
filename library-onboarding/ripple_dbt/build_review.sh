#!/usr/bin/env bash
# The ONLY sanctioned way to rebuild the review marts (POSIX twin of
# build_review.bat — see that file for the audit-F1 encoding rationale).
# PYTHONUTF8=1 forces dbt's file reads to UTF-8 so em-dashes in model
# literals survive; assert_no_mojibake.sql fails any mis-encoded build.
set -euo pipefail
cd "$(dirname "$0")"
# ENGINE PIN: bare `dbt` on PATH may resolve to the global dbt-fusion preview.
# Always run the project's dbt-core venv engine (see build_review.bat).
DBT_BIN="$(pwd)/../../.dbt-venv/Scripts/dbt.exe"
[ -x "$DBT_BIN" ] || { echo "ERROR: pinned dbt engine not found at $DBT_BIN" >&2; exit 1; }
PYTHONUTF8=1 "$DBT_BIN" build --select marts.review "$@"
