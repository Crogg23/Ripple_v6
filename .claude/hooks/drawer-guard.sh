#!/bin/bash
# Reading the junk drawer should sting. Turns any Read/Glob into _JUNK_DRAWER into an "ask Chris".
[ -f "$CLAUDE_PROJECT_DIR/.claude/state/hooks.off" ] && exit 0
INPUT=$(cat)
TARGET=$(python -c "
import json,sys
t=json.load(sys.stdin).get('tool_input',{})
print(t.get('file_path') or t.get('path') or t.get('pattern') or '')" <<< "$INPUT")
case "$TARGET" in
  *_JUNK_DRAWER*)
    python -c "import json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'ask','permissionDecisionReason':'This is the junk drawer — retired attempts, reference only. Never build from it. Still want to open it?'}}))"
    ;;
esac
exit 0
