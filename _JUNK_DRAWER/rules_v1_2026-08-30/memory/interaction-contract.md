---
name: interaction-contract
description: "CLAUDE.md §8 is live (2026-08-06) plus 8 mechanical guardrails (hooks/settings) — chat is the interface, never send Chris to files"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 914dcfe5-32a0-4dc2-8235-7fdc75c3585a
  modified: 2026-08-06T16:42:40.669Z
---

On 2026-08-06 Chris approved the Interaction Contract as CLAUDE.md section 8,
plus 8 concrete guardrails that turn it from words into mechanics:

1. **Cost/lines statusline** (global `~/.claude/settings.json`, script at
   `~/.claude/statusline-cost.py`) — always-visible cost so Chris is never
   "in the dark" on spend again.
2. **breakReminder** (global, 45 min interval) and 3. **quietHours** (global,
   23:00–07:00 placeholder — ask Chris for his real window if it ever comes up).
4. **Permission allowlist cleanup** (project `.claude/settings.json`) — added
   read-only git (status/log/diff/show/branch --list) and test runners
   (pytest, dbt test/build) so routine safe commands stop prompting.
5. **Git safety net** — `.claude/hooks/block-dangerous-git.sh`, a PreToolUse
   hook on Bash that blocks `git reset --hard`, `clean -f(d)`, `branch -D`,
   `checkout .`/`restore .`, and anything with `--force`. Deliberately does
   **not** block plain `git push` — Ripple's build relies on normal pushes.
6. **SessionStart auto-brief** — `.claude/hooks/session-brief.sh` dumps
   STATUS.md + real git log/status/unpushed-commits into context at boot,
   so the session can verify claims and brief Chris without him asking.
7. **Spend reminder** — PreToolUse hook on Agent/Workflow tool calls, nudges
   toward showing a price tag before big fan-outs (contract 8.7).
8. **PreCompact snapshot** — `.claude/hooks/precompact-save.sh` saves
   STATUS.md + git state to `.claude/compact-snapshots/last-compact.md`
   right before long-session context compaction, so nothing gets lost.

**Important build note:** Claude Code's own auto-mode classifier hard-blocks
edits that look like an agent granting itself broad new shell permissions —
it rejected a blanket `"Bash(git *)"` allow-rule twice, even after Chris typed
explicit approval in chat ("I approve"). The fix was scoping to read-only git
verbs instead of the wildcard. **Future sessions: don't propose broad
`Bash(<tool> *)` allow-rules — they will be blocked regardless of user
say-so; scope permission additions narrowly (specific subcommands) instead.**

**Why:** Chris (burnt out, ADHD-C, solo, day job) named cost-blindness and
interaction exhaustion as compounding problems in the same session — see
[[monetization-goal-and-paths]] for the burnout/quit-job context. He wants
ease of access without slowing the actual build (his words: "without
derailing or drastically slowing down my build").

**How to apply:** the chat is the interface — explain everything IN chat,
never point Chris at a file to understand or decide. 5-sentence updates, no
codenames, bad news first and exempt from caps, one decision per message,
quiet long work with heartbeats, DONE/BROKE/YOUR MOVE/NEXT + cost note at
every close, rewrite STATUS.md every session. Chris's control words: "brief
me" / "walk me through it" / "just go" / "open the hood" / "contract" (=
you slipped, strip back, log it, don't defend). Never shrink work to shorten
reports — see [[feedback-avoid-narrow-fixation]] and
[[feedback-open-brief-means-range]].
