#!/bin/bash
# Stop hook. Runs the countable-rule counter over the message Chris is about to
# read. Not a judge — it only counts words, parentheses, dashes and paths. The
# prompt reader that runs after this handles the rules that need judgment.
#   hooks off  → this gate goes quiet, same as the other command hooks.
STATE="$CLAUDE_PROJECT_DIR/.claude/state"
INPUT=$(cat)
[ -f "$STATE/hooks.off" ] && exit 0
source "$(dirname "${BASH_SOURCE[0]}")/_py.sh"
py_or_skip "the shape gate"

CHECKER="$CLAUDE_PROJECT_DIR/.claude/hooks/shape_check.py"
if [ ! -f "$CHECKER" ]; then
  echo "shape gate is OFF: the counter script is missing." >&2
  exit 0
fi

echo "$INPUT" | "$PY" "$CHECKER"
