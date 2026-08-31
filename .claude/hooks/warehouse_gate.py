"""Classifier for warehouse-gate.sh — prints spine/rebuild/destroy or nothing."""
import json, re, sys

c = json.loads(sys.argv[1]).get('tool_input', {}).get('command', '')

# Heredoc bodies are scanned too (SQL hides there). Commit messages: use -F <file>, not inline prose.
c = re.sub(r'''-m\s+("[^"]*"|'[^']*')''', '-m MSG', c)

segs = [s.strip() for s in re.split(r'&&|\|\||;|\||\n', c) if s.strip()]
exempt = re.compile(r'^(echo|printf|grep|rg|cat|ls|head|tail|wc|sort|uniq|git (log|show|status|diff|branch)|python3? -c "import json)\b')
rules = [
  ('spine',   r'(^|\s)(python3?\s+(-m\s+)?)?connect[ ./](spine|all|seed|entity-index|apply-config|connect-one|connect-changed|discover|harvest)\b|spine_rebuild|gen_spine_specs|spine_wiring_prep|add_spine_columns'),
  ('rebuild', r'(^|\s)dbt(\.exe)?\s+(-\S+\s+)*(run|build|seed|snapshot|retry)\b|dbt\.cli\.main|rebuild_frozen_marts|--full-refresh|full_refresh'),
  ('destroy', r'\b(DROP\s+(TABLE|VIEW|SCHEMA|DATABASE)|TRUNCATE|DELETE\s+FROM|INSERT\s+OVERWRITE|CREATE\s+OR\s+REPLACE\s+TABLE|ALTER\s+TABLE\s+\S+\s+DROP)\b|write_pandas\([^)]*overwrite\s*=\s*True|rm\s+-rf?\s+(data|outputs|logs)\b'),
]
for s in segs:
    if exempt.match(s):
        continue
    for kind, rx in rules:
        if re.search(rx, s, re.I):
            print(kind)
            sys.exit(0)
print('')
