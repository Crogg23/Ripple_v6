#!/bin/bash
# Gate on hard-to-undo warehouse work and spine commands (CLAUDE.md — Don't do damage).
# Blocks unless a session greenlight marker exists for the matching kind.
source "$(dirname "${BASH_SOURCE[0]}")/_py.sh"
[ -f "$CLAUDE_PROJECT_DIR/.claude/state/hooks.off" ] && exit 0
py_or_block "the warehouse gate"
INPUT=$(cat)
SESSION=$("$PY" -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))" <<< "$INPUT")
STATE="$CLAUDE_PROJECT_DIR/.claude/state"

# Classification lives in warehouse_gate.py — macOS bash 3.2 can't parse
# a quoted heredoc inside $(), so the python stays in its own file.
KIND=$("$PY" "$CLAUDE_PROJECT_DIR/.claude/hooks/warehouse_gate.py" "$INPUT")

[ -z "$KIND" ] && exit 0
if [ -f "$STATE/$SESSION.$KIND.greenlight" ]; then exit 0; fi
echo "GATED ($KIND). Ask Chris first with a one-line price tag (scripts/price_it.py). If he types 'greenlight $KIND' on its own line it's open for the rest of this session." >&2
exit 2
