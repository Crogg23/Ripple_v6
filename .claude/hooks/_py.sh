#!/bin/bash
# Shared interpreter resolver for every hook in this folder.
#
# Why this exists: the hooks were written on Windows where `python` is on PATH.
# A stock macOS has `python3` and NO `python` at all, so every hook that called
# `python` died with 127 and the gate it guarded silently stopped existing. The
# git guard is one of those. Nothing announced it.
#
# Two traps this avoids:
#   1. `command -v python3` succeeds on Windows but resolves to the Store stub,
#      which exits 127 instead of running. So each candidate must PROVE it runs.
#   2. A missing interpreter must never be silent, whichever way the hook fails.
#
# Usage:  source "$(dirname "${BASH_SOURCE[0]}")/_py.sh"   then use "$PY".
#         $PY is empty when nothing works. The hook decides what that means:
#         safety gates fail CLOSED and say so; conveniences fail OPEN and say so.

PY=""
# Test seam. A no-interpreter machine cannot be faked with PATH alone on
# Windows, because py.EXE lives in C:\WINDOWS and that folder cannot be
# dropped. The tests set this to prove the fail-closed and fail-open paths.
if [ "$RIPPLE_HOOKS_FAKE_NO_PYTHON" = "1" ]; then
  _cand=""
else
for _cand in python3 python py; do
  if command -v "$_cand" >/dev/null 2>&1 && "$_cand" -c "pass" >/dev/null 2>&1; then
    PY="$_cand"
    break
  fi
done
fi
unset _cand

# A safety gate with no interpreter must block, not wave things through.
py_or_block() {
  [ -n "$PY" ] && return 0
  echo "$1 cannot run: no working python found. Install python3, or say 'hooks off' to work without the gates." >&2
  exit 2
}

# A convenience hook with no interpreter should get out of the way, out loud.
py_or_skip() {
  [ -n "$PY" ] && return 0
  echo "$1 is OFF: no working python found on this machine." >&2
  exit 0
}
