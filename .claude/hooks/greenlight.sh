#!/bin/bash
# Records a session greenlight when Chris types "greenlight <kind>" on a line by itself
# (kind = spine | rebuild | destroy | spend). "do NOT greenlight spine" does not count.
INPUT=$(cat)
PROMPT=$(python -c "import json,sys; print(json.load(sys.stdin).get('prompt',''))" <<< "$INPUT")
SESSION=$(python -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))" <<< "$INPUT")
STATE="$CLAUDE_PROJECT_DIR/.claude/state"
mkdir -p "$STATE"
for kind in spine rebuild destroy spend; do
  if echo "$PROMPT" | grep -qiE "^[[:space:]]*greenlight[[:space:]]+$kind[[:space:]]*[.!]?[[:space:]]*$"; then
    touch "$STATE/$SESSION.$kind.greenlight"
    echo "Greenlight recorded for '$kind' — lasts this session."
  fi
done
exit 0
