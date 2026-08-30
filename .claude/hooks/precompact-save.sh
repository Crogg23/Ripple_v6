#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || true
mkdir -p .claude/compact-snapshots
STAMP_FILE=".claude/compact-snapshots/last-compact.md"
{
  echo "# Snapshot taken right before context compaction"
  echo
  echo "## Working tree at compaction time"
  git status -sb 2>/dev/null
  echo
  echo "## Recent commits"
  git log -5 --oneline 2>/dev/null
  echo
  echo "## Session greenlights"
  ls .claude/state/*.greenlight 2>/dev/null || echo "none"
} > "$STAMP_FILE"
echo "Saved pre-compaction snapshot to $STAMP_FILE"
