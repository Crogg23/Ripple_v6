# Pre-made Claude Code setups vs. the 7 wants (2026-08-30)

The 7 wants decided today: (1) boot brief from git + transcripts, (2) ask at forks in plain English with "I'd do X because Y; other ways A/B", (3) skeptic pass on every "done" + session close, (4) accurate price tag + go before spend, (5) scannable output, (6) presence — never remind of known things, "parked:" line for new, (7) junk drawer + ledger.

Legend: D = direct, P = partial, – = no.

## Candidates

| # | Name | What | Covers | Install | Fights prefs |
|---|---|---|---|---|---|
| 1 | [Official hooks](https://code.claude.com/docs/en/hooks) | the primitive: command / prompt / agent hooks on SessionStart, Stop, PreToolUse etc. | 1 P, 3 P, 4 D | edit settings.json | none |
| 2 | [Official best practices](https://code.claude.com/docs/en/best-practices) | "cut CLAUDE.md to what prevents mistakes"; adversarial reviewer = fresh subagent given only diff + criteria | 3 D (pattern), 2 P, 5 P | reading | none |
| 3 | [Output styles](https://code.claude.com/docs/en/output-styles) | built-in Concise, or a custom .md style always-on | 5 D/P, 6 P | 1 line / 1 file | main convo only; needs /clear |
| 4 | [attention-span](https://github.com/alexgreensh/attention-span) | 3 ADHD output styles (answer first, spaced, bold) | 5 D, 1 P | copy 1 md | arrows/emoji markers; no table rule |
| 5 | [fcakyon adhd skill](https://github.com/fcakyon/claude-codex-settings/tree/main/plugins/adhd-output-style/skills/adhd-output-style) | skill: answer first, ≤5 items | 5 P, 6 P | clone | not always-on; "restate progress" opposes want 6 |
| 6 | [karanb192 hooks](https://github.com/karanb192/claude-code-hooks) | ~20 local hooks: standup-autopilot (transcript mining), dead-end-registry, protect-tests, guard-pack, dead-rules-audit | 1 P, 3 P, 4 P, 7 P | plugin marketplace | gamification noise; Node on Windows |
| 7 | [episodic-memory](https://github.com/obra/episodic-memory) | all past conversations searchable locally | 1 P, 6 P | plugin | background sync; prose output |
| 8 | [claude-mem](https://github.com/thedotmack/claude-mem) | auto-captured observations injected at start | 1 P | heavy (Node, Bun, uv, worker) | heaviest footprint; pick 7 or 8 |
| 9 | [superpowers](https://github.com/obra/superpowers) | methodology skills: brainstorm, verify-before-complete | 3 P, 2 P | marketplace | mandatory TDD/plan ceremony |
| 10 | [adversarial-review](https://github.com/ng/adversarial-review) | Optimizer vs Skeptic agents over a diff | 3 P | marketplace | diff-shaped, auto-fixes |
| 11 | [prompt-improver](https://github.com/severity1/claude-code-prompt-improver) | ask-user-question nudge routes real forks through menus | 2 P | marketplace | "improve" nudge nags — disable |
| 12 | [official plugins](https://github.com/anthropics/claude-plugins-official) | hookify (plain-English hooks), claude-md-management, code-review | 4 P, 3 P | plugin | regex-only guards |
| 13 | [Altimate dbt+Snowflake skills](https://github.com/AltimateAI/data-engineering-skills) | dbt + Snowflake skills incl. finding expensive queries | 4 P, domain D | marketplace | none |

Seen, not recommended: everything-claude-code (68 agents / 286 skills — the contradiction problem scaled up), hex/claude-sessions (no Windows), HumanLayer "Writing a good CLAUDE.md" (<60 lines, good read), Stop-hook-won't-let-Claude-lie article (recipe), awesome-claude-code lists (browse only).

## Coverage grid

| Want | Best pre-made | Grade |
|---|---|---|
| 1 Boot brief | SessionStart hook + episodic-memory + standup-autopilot | P — assembly |
| 2 Ask at forks | prompt-improver nudge | P — wrong format |
| 3 Skeptic | official subagent + best-practices reviewer prompt | D pattern, no packaged plugin |
| 4 Price tag | PreToolUse ask (+ hookify) | P — gate yes, accurate cost no |
| 5 Output | Concise / attention-span | D |
| 6 Presence | — | none |
| 7 Junk drawer | dead-end-registry | P — in-repo version is hand-made |

## What to assemble

| # | Piece | Covers | Effort |
|---|---|---|---|
| 1 | attention-span "Attention-kind" as custom output style, edited (tables rule, parked: line, drop emoji) | 5, 6 | 15 min |
| 2 | hand-written SessionStart hook: git log since last session + episodic-memory query → free-form brief | 1 | ~1 hr |
| 3 | hand-written skeptic subagent (.claude/agents/skeptic.md, fresh context, read-only, takes asked/built/claimed) + Stop prompt hook refusing "done" without a receipt | 3 | ~1 hr |
| 4 | karanb192: guard-pack (ask mode), protect-tests, dead-end-registry, dead-rules-audit | 3, 4, 7 | 10 min |
| 5 | Altimate dbt + snowflake skills | domain | 5 min |

Hand-build only: want 2 format (CLAUDE.md block), want 4 accuracy (script reading Snowflake query history before the ask fires; session greenlight = marker file), want 6 presence (prompt rule), want 7 ledger hook.

Warning: bloated CLAUDE.md is why rules stop sticking. Keep it under ~60 lines; anything that must happen every time is a hook, not a sentence.
