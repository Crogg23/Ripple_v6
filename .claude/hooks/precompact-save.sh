#!/bin/bash
mkdir -p .claude/compact-snapshots
STAMP_FILE=".claude/compact-snapshots/last-compact.md"
{
  echo "# Snapshot taken right before context compaction"
  echo
  echo "## STATUS.md at compaction time"
  cat STATUS.md 2>/dev/null
  echo
  echo "## Working tree at compaction time"
  git status -sb 2>/dev/null
  echo
  echo "## Recent commits"
  git log -5 --oneline 2>/dev/null
} > "$STAMP_FILE"
echo "Saved pre-compaction snapshot to $STAMP_FILE"
