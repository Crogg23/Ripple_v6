#!/bin/bash
# Self-test for warehouse-gate.sh + greenlight.sh. Run: bash .claude/hooks/test-gate.sh
export CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
H="$CLAUDE_PROJECT_DIR/.claude/hooks"
S="gatetest"
rm -f "$CLAUDE_PROJECT_DIR/.claude/state/$S."*
run() { echo "{\"session_id\":\"$S\",\"tool_input\":{\"command\":\"$1\"}}" | bash "$H/warehouse-gate.sh" 2>/dev/null; echo $?; }
echo "spine cmd, no greenlight (want 2): $(run 'python -m connect spine')"
echo "dbt build, no greenlight (want 2): $(run 'dbt build --select x')"
echo "git status (want 0):              $(run 'git status')"
echo "{\"session_id\":\"$S\",\"prompt\":\"greenlight spine\"}" | bash "$H/greenlight.sh"
echo "spine cmd, after greenlight (want 0): $(run 'python -m connect spine')"
echo "dbt build, after spine greenlight only (want 2): $(run 'dbt build --select x')"
rm -f "$CLAUDE_PROJECT_DIR/.claude/state/$S."*
