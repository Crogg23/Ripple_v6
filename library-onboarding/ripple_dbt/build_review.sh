#!/usr/bin/env bash
# The ONLY sanctioned way to rebuild the review marts (POSIX twin of
# build_review.bat — see that file for the audit-F1 encoding rationale).
# PYTHONUTF8=1 forces dbt's file reads to UTF-8 so em-dashes in model
# literals survive; assert_no_mojibake.sql fails any mis-encoded build.
set -euo pipefail
cd "$(dirname "$0")"
PYTHONUTF8=1 dbt build --select marts.review "$@"
