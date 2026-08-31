#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/_py.sh"
py_or_block "the git guard"
INPUT=$(cat)
COMMAND=$("$PY" -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" <<< "$INPUT")

DANGEROUS_PATTERNS=(
  "git reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \."
  "git restore \."
  "git .*\-\-force"
  "git push"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches dangerous pattern '$pattern'. The user has prevented you from doing this — ask Chris directly if this is really needed." >&2
    exit 2
  fi
done

exit 0
