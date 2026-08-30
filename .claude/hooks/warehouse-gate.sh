#!/bin/bash
# Gate on hard-to-undo warehouse work and spine commands (CLAUDE.md — Don't do damage).
# Blocks unless a session greenlight marker exists for the matching kind.
[ -f "$CLAUDE_PROJECT_DIR/.claude/state/hooks.off" ] && exit 0
INPUT=$(cat)
SESSION=$(python -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))" <<< "$INPUT")
STATE="$CLAUDE_PROJECT_DIR/.claude/state"

# Normalise: replace -m "..." commit messages, then split into segments on && || ; | newline
# (heredoc bodies included — SQL hides in them).
# Segments that are pure read/print (echo, grep, rg, cat, ls, head, tail, git log/show/status/diff) are exempt,
# so mentioning "dbt build" in a message doesn't trip the gate.
KIND=$(python - "$INPUT" <<'PYEOF'
import json, re, sys
c = json.loads(sys.argv[1]).get('tool_input', {}).get('command', '')

# Heredoc bodies are scanned too (SQL hides there). Commit messages: use -F <file>, not inline prose.
c = re.sub(r'''-m\s+("[^"]*"|'[^']*')''', '-m MSG', c)

segs = [s.strip() for s in re.split(r'&&|\|\||;|\||\n', c) if s.strip()]
exempt = re.compile(r'^(echo|printf|grep|rg|cat|ls|head|tail|wc|sort|uniq|git (log|show|status|diff|branch)|python -c "import json)\b')
rules = [
  ('spine',   r'(^|\s)(python3?\s+(-m\s+)?)?connect[ ./](spine|all|seed|entity-index|apply-config|connect-one|connect-changed|discover|harvest)\b|spine_rebuild|gen_spine_specs|spine_wiring_prep'),
  ('rebuild', r'(^|\s)dbt(\.exe)?\s+(-\S+\s+)*(run|build|seed|snapshot|retry)\b|dbt\.cli\.main|rebuild_frozen_marts|--full-refresh|full_refresh'),
  ('destroy', r'\b(DROP\s+(TABLE|VIEW|SCHEMA|DATABASE)|TRUNCATE|DELETE\s+FROM|INSERT\s+OVERWRITE|CREATE\s+OR\s+REPLACE\s+TABLE|ALTER\s+TABLE\s+\S+\s+DROP)\b|write_pandas\([^)]*overwrite\s*=\s*True|rm\s+-rf?\s+(data|outputs|logs)\b'),
]
for s in segs:
    if exempt.match(s): continue
    for kind, rx in rules:
        if re.search(rx, s, re.I):
            print(kind); sys.exit(0)
print('')
PYEOF
)

[ -z "$KIND" ] && exit 0
if [ -f "$STATE/$SESSION.$KIND.greenlight" ]; then exit 0; fi
echo "GATED ($KIND). Ask Chris first with a one-line price tag (scripts/price_it.py). If he types 'greenlight $KIND' on its own line it's open for the rest of this session." >&2
exit 2
