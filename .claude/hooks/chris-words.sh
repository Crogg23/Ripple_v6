#!/bin/bash
# Runs on every prompt. Reads Chris's words for the few that change machine state,
# and injects the corrections file so Tuesday's correction still fires on Friday.
#   greenlight <kind>   (spine|rebuild|destroy|spend) — only if a price was shown this hour
#   riff / build        — sets the mode marker (also /riff, /build)
#   hooks off / hooks on — kill switch for the command hooks (git guard stays on)
source "$(dirname "${BASH_SOURCE[0]}")/_py.sh"
py_or_skip "the prompt reader"
INPUT=$(cat)
PROMPT=$("$PY" -c "import json,sys; print(json.load(sys.stdin).get('prompt',''))" <<< "$INPUT")
SESSION=$("$PY" -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))" <<< "$INPUT")
STATE="$CLAUDE_PROJECT_DIR/.claude/state"
mkdir -p "$STATE"

line() { echo "$PROMPT" | grep -qiE "$1"; }

if line '^[[:space:]]*hooks[[:space:]]+off[[:space:]]*$'; then touch "$STATE/hooks.off"; echo "Command hooks OFF (gate, drawer guard). Git guard stays on. 'hooks on' restores."; fi
if line '^[[:space:]]*hooks[[:space:]]+on[[:space:]]*$';  then rm -f "$STATE/hooks.off"; echo "Command hooks ON."; fi

if line '^[[:space:]]*/?riff\b';  then echo riff  > "$STATE/mode"; echo "MODE: riff — argue, add angles, chase tangents. No plans, no prices."; fi
if line '^[[:space:]]*/?build\b'; then echo build > "$STATE/mode"; echo "MODE: build — execute, ask at forks, skeptic before done."; fi

for kind in spine rebuild destroy spend; do
  if line "^[[:space:]]*greenlight[[:space:]]+$kind[[:space:]]*[.!]?[[:space:]]*$"; then
    if [ -f "$STATE/last_priced" ] && [ $(( $(date +%s) - $(cat "$STATE/last_priced") )) -lt 3600 ]; then
      touch "$STATE/$SESSION.$kind.greenlight"
      echo "Greenlight recorded for '$kind' — lasts this session."
    else
      echo "Greenlight for '$kind' NOT recorded: no price tag shown in the last hour. Run scripts/price_it.py (or /price) first, then say it again."
    fi
  fi
done

if [ -s "$CLAUDE_PROJECT_DIR/.claude/corrections.md" ]; then
  echo "=== Chris's corrections (newest last; these are rules) ==="
  grep -vE '^\s*(#|$)' "$CLAUDE_PROJECT_DIR/.claude/corrections.md" | tail -40
fi
[ -f "$STATE/mode" ] && echo "MODE: $(cat "$STATE/mode")"
exit 0
