#!/bin/bash
echo "=== STATUS.md (rewritten each session close — trust but verify against git below) ==="
cat STATUS.md 2>/dev/null
echo
echo "=== Actual recent commits ==="
git log -5 --oneline 2>/dev/null
echo
echo "=== Actual working tree state ==="
git status -sb 2>/dev/null
echo
echo "=== Unpushed commits ==="
git log origin/main..HEAD --oneline 2>/dev/null
