#!/bin/bash
# Gate on hard-to-undo warehouse work and spine commands (CLAUDE.md — Don't do damage).
# Blocks unless a session greenlight marker exists for the matching kind.
INPUT=$(cat)
# Inspect the command itself, not prose inside it: drop heredoc bodies and -m "..." messages.
COMMAND=$(python -c "
import json,sys,re
c=json.load(sys.stdin).get('tool_input',{}).get('command','')
c=c.split('<<',1)[0]
c=re.sub(r'''-m\s+(\"[^\"]*\"|'[^']*')''','-m MSG',c)
print(c)" <<< "$INPUT")
SESSION=$(python -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))" <<< "$INPUT")
STATE="$CLAUDE_PROJECT_DIR/.claude/state"

check() {  # $1 = kind, $2 = regex
  if echo "$COMMAND" | grep -qiE "$2"; then
    if [ -f "$STATE/$SESSION.$1.greenlight" ]; then
      exit 0
    fi
    echo "GATED ($1): '$COMMAND'. Ask Chris first with a one-line price tag. If he says 'greenlight $1' it's open for the rest of this session." >&2
    exit 2
  fi
}

check spine     "connect (spine|apply-config|connect-one|connect-changed|discover|harvest)|spine_rebuild|gen_spine_specs"
check rebuild   "dbt (run|build)|rebuild_frozen_marts|--full-refresh"
check destroy   "\b(DROP|TRUNCATE|DELETE FROM|ALTER TABLE .* DROP)\b|write_pandas.*overwrite"
exit 0
