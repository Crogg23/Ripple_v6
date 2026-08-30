#!/bin/bash
# Boot brief source. Git only — no status file. Claude turns this into a
# chief-of-staff walk-in brief (live / broken / open) and ends it with
# "I think we're working on X — right?"
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || true
echo "=== Last 15 commits ==="
git log -15 --format='%ad  %s' --date=short 2>/dev/null
echo
echo "=== Working tree (uncommitted) ==="
git status -sb 2>/dev/null
echo
echo "=== Unpushed ==="
git log origin/main..HEAD --oneline 2>/dev/null
echo
echo "=== Files touched in the last 3 days ==="
git log --since='3 days ago' --name-only --format='' 2>/dev/null | sort | uniq -c | sort -rn | head -25
echo
echo "=== Session greenlight ==="
ls .claude/state/*.greenlight 2>/dev/null || echo "none"
echo
echo "Past transcripts live in ~/.claude/projects/c--Code-Ripple-v6/ — look things up there when Chris mentions them; don't ask him to re-explain."
