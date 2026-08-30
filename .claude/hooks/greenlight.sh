#!/bin/bash
# Records a session greenlight when Chris types "greenlight <kind>" (kind = spine | rebuild | destroy | spend).
# The warehouse gate reads the marker. Markers are per session; stale ones are harmless.
INPUT=$(cat)
PROMPT=$(python -c "import json,sys; print(json.load(sys.stdin).get('prompt',''))" <<< "$INPUT")
SESSION=$(python -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))" <<< "$INPUT")
STATE="$CLAUDE_PROJECT_DIR/.claude/state"
mkdir -p "$STATE"
for kind in spine rebuild destroy spend; do
  if echo "$PROMPT" | grep -qiE "greenlight[[:space:]]+$kind"; then
    touch "$STATE/$SESSION.$kind.greenlight"
    echo "Greenlight recorded for '$kind' — lasts this session."
  fi
done
exit 0
