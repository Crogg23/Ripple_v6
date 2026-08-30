#!/bin/bash
# Self-test for warehouse-gate.sh + greenlight.sh. Run: bash .claude/hooks/test-gate.sh
export CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
H="$CLAUDE_PROJECT_DIR/.claude/hooks"
S="gatetest"
rm -f "$CLAUDE_PROJECT_DIR/.claude/state/$S."*
fail=0
run() { python -c "import json,sys; print(json.dumps({'session_id':'$S','tool_input':{'command':sys.argv[1]}}))" "$1" | bash "$H/warehouse-gate.sh" 2>/dev/null; echo $?; }
t() { r=$(run "$2"); if [ "$r" = "$1" ]; then echo "ok   ($1) $3"; else echo "FAIL (got $r want $1) $3"; fail=1; fi; }
gl() { python -c "import json,sys; print(json.dumps({'session_id':'$S','prompt':sys.argv[1]}))" "$1" | bash "$H/greenlight.sh" >/dev/null; }

echo "--- should block"
t 2 'python -m connect spine' "spine cmd"
t 2 'python -m connect.spine' "spine module form"
t 2 'python connect/spine.py' "spine file form"
t 2 'python -m connect all' "connect all"
t 2 'dbt build --select x' "dbt build"
t 2 'dbt  run' "dbt run, two spaces"
t 2 'dbt --no-partial-parse build' "dbt flag then build"
t 2 'dbt seed' "dbt seed"
t 2 'python -m dbt.cli.main run' "dbt via module"
t 2 $'cat <<EOF\nhello\nEOF\ndbt build' "dangerous cmd after heredoc"
t 2 $'python - <<EOF\nconn.execute("DROP TABLE X")\nEOF' "SQL inside a heredoc body"
t 2 'python -c "x" <<< "a" && dbt build' "herestring then dbt build"
t 2 'git commit -m "x" && dbt build' "commit message then dbt build"
t 2 'python -c "cur.execute(\"TRUNCATE T\")"' "truncate in python string"
t 2 'rm -rf data/' "rm -rf data"
echo "--- should pass"
t 0 'git status' "git status"
t 0 'echo "we will delete from the list"' "prose in echo"
t 0 'grep -rn "dbt build" scripts' "grep mentioning dbt build"
t 0 'git log --oneline | head' "git log"
t 0 'dbt test --select x' "dbt test"
t 0 'dbt list' "dbt list"
t 0 'python scripts/price_it.py --like "%x%"' "price_it"
echo "--- greenlight"
gl "do NOT greenlight spine"
t 2 'python -m connect spine' "negated greenlight must not open"
gl "greenlight spine"
t 0 'python -m connect spine' "after greenlight spine"
t 2 'dbt build' "rebuild still gated after spine greenlight"
rm -f "$CLAUDE_PROJECT_DIR/.claude/state/$S."*
[ $fail = 0 ] && echo "ALL PASS" || echo "SOME FAILED"
exit $fail
