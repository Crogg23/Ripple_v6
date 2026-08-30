# Skeptic pass on the new rulebook — 2026-08-30

Fresh-context adversarial review of CLAUDE.md (48 lines), the junk drawer, the setup survey, and the existing hooks. Read-only.

## Verdict up front
The rulebook is a decent preference sheet, but as built today it is ~90% prose (the thing that drifted last time), the git state would ship a repo with no CLAUDE.md at all, and the permission allowlist pre-approves the two things the old rules screamed about (spine runs, dbt rebuilds) with no cost gate.

## BLOCKERS

**B1. New CLAUDE.md is untracked; git thinks the rulebook moved to the junk drawer.**
`git status`: `R CLAUDE.md -> _JUNK_DRAWER/rules_v1_2026-08-30/CLAUDE.md` staged, `?? CLAUDE.md` untracked. Same for `.claude/contract-reminder.md`. Junk drawer `rules_v1/` (79 files) untracked. Fix: `git add CLAUDE.md .claude/contract-reminder.md _JUNK_DRAWER/`.

**B2. Permission allowlist auto-runs spine + warehouse spend, bypassing "wait for go".**
`.claude/settings.json` lines 15–27, 37: `python3 -m connect spine`, `connect discover/harvest`, `dbt run *`, `dbt build *` pre-allowed. Spend hook only fires on Agent|Workflow. Fix: remove those entries; add a PreToolUse Bash gate that returns `ask` on `connect spine|apply-config|connect-one|connect-changed|dbt (run|build)|DROP|TRUNCATE` unless a session-greenlight marker exists.

**B3. "Accurate cost from the query log" has zero tooling; warehouse connection currently dead.**
No QUERY_HISTORY / METERING usage anywhere in scripts/ connect/ bench/. Snowflake MCP PAT rejected. A pre-run Snowflake cost is only approximable: price past identical runs by query tag, or bytes scanned on EXPLAIN. Query history lags minutes and needs ACCOUNT_USAGE grants. Fix: `scripts/price_it.py` — tag runs, read QUERY_HISTORY by tag, print p50 credits × $/credit, or "no real number for this". Fix the PAT first.

## REAL

**R1. Internal contradictions in CLAUDE.md**

| Lines | Conflict | Bites when |
|---|---|---|
| 16 vs 22 | "ask on what next" vs "his to-do list is his" | every close |
| 12 vs 16 | riff "no plans" vs forks "what next" | mid-riff |
| 23 vs 16 | a hole/easier path is "parked, one line" but also a direction fork → "stop and ask" | every discovered problem |
| 38 vs 22 | boot brief = live/broken/open, which is what he already knows | every boot |
| 8 vs 38/40 | "tables, bold, never dense" vs "free-form" open/close | reader flags the brief |
| 33–35 | greenlight lasts the session — for what scope? | a $2 go becomes a $15 pass |
| 41 vs 38 | save only corrections + traps, yet brief must know broken/open | chat-only decisions lost |

Fix: one precedence line (forks beat parked; riff suppresses what-next forks; brief is exempt from presence) + greenlight scope (per command class, this session).

**R2. Message reader is feasible but fires AFTER Chris sees the message.**
Stop hook gets `last_assistant_message` + transcript path; prompt-type hooks run a fast model; `stop_hook_active` is the loop guard. Nothing intercepts pre-display — "one bounce" means Chris sees draft 1 then draft 2. Intermediate text between tool calls never checked. Reader can't know riff vs build mode. +2–8 s and one small-model call per turn. Fix: treat as post-hoc note; gate on a mode marker; `systemMessage` for style, `block` only on unverified done.

**R3. "Every real done" undefined; skeptic inherits effortLevel: low.**
`~/.claude/settings.json` has `"effortLevel": "low"`; subagents inherit unless pinned. Low-effort skeptic = rubber stamp. To catch "built the wrong thing" it needs Chris's verbatim words, not Claude's paraphrase. Fix: `.claude/agents/skeptic.md` with high effort, read-only tools, input = verbatim last user request + git diff + claim; trigger on commit/done wording.

**R4. "Greenlight lasts the session" is prose.**
Nothing records a go. UserPromptSubmit could write `.claude/state/<session_id>.go` on a literal token; regex on bare "go" false-fires. Fix: require "greenlight" or "go $".

**R5. Boot brief from git + transcripts — no cheap generator.**
123 transcripts, 767 MB, recent 0.4–3.7 MB each. A command hook can git log; summarizing transcripts needs a model call: raw tail = bloat; `claude -p` = 20–60 s boot; episodic-memory summarizer calls Haiku via API key = real money, Windows support unstated, sqlite-vec native build is painful. What STATUS.md gave that git can't: broke list, uncommitted decisions, waiting-on-Chris — and line 41 forbids saving them. Fix: one tiny machine-written file at close (`.claude/state/last-close.md`, hook-written, not a human doc); brief = git + that file.

**R6. Old hooks inject retired vocabulary every boot.**
session-brief.sh cats STATUS.md (60+ lines of red-lane banners); precompact-save.sh same; spend-reminder cites "CLAUDE.md 8.7" which no longer exists; UserPromptSubmit cats a 0-byte file. Fix: session-brief git-only; drop the UserPromptSubmit entry; reword spend-reminder.

**R7. Junk drawer leaks back into context.**
Untracked but not ignored; Grep/Glob honor .gitignore/.ignore only; no .ignore exists. MEMORY.md hands every session the path. `connect/` has 146 importers (51 tests, 9 scripts), lives at root, has a pre-approved spine command — CLAUDE.md line 49 says the spine is in the drawer; it isn't. Leftover README at the old `reports/_JUNK_DRAWER_not_the_handbook/` path. Fix: root `.ignore` with `_JUNK_DRAWER/`; fix line 49 to "connect/ stays live code, spine commands are gated."

**R8. Legal/safety rules lost, now only implied.**
Gone: human sign-off before publish; no publish nudging; DROP/destructive ops; spine commands need asking; COUNT(DISTINCT) before trusting a key. Publishing has no gate (Artifact tool unrestricted). Fix: 3 lines under Money + the PreToolUse gate.

## MINOR

| # | Finding | Fix |
|---|---|---|
| M1 | block-dangerous-git.sh blocks any Bash containing `--force` | anchor to `git .*--force` |
| M2 | `python3` allowlist resolves to WindowsApps alias | use `python` |
| M3 | hooks use relative paths; break in worktree sessions | prefix `$CLAUDE_PROJECT_DIR` |
| M4 | attention-span style mandates arrows; real fight is arrows vs tables | write the style from scratch (~20 lines) |
| M5 | karanb192 hooks are Node-only, no Windows statement | test one before installing five |
| M6 | "3 hours" excludes PAT repair, cost script, greenlight marker, Windows testing — realistically a day | re-estimate |
| M7 | the session that built this still has the OLD rules loaded; its own verdict came from the old brain | restart before trusting self-review |

## The 3 things most likely to make this fail like the old one
1. It's still prose. Only the spend gate and the reader are hook-shaped, and neither is built; the harness enforces nothing new and pre-approves the dangerous commands.
2. The contradictions are already in the 48 lines (R1), with no precedence rule.
3. Memory is write-only: chat-only decisions evaporate at close; the next session re-derives them wrong, Chris corrects, the pile of corrections becomes the next 76-file rulebook.
