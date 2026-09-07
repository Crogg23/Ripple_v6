# V4 system-instructions gap analysis — 2026-09-07

Phase 1 baseline and Phase 2 gaps. Nothing modified. Awaiting Chris's approval for Phase 3.

## What was checked

| Surface | File | Role today |
|---|---|---|
| Project rules | CLAUDE.md | the system prompt; Chris owns it |
| Corrections | .claude/corrections.md | injected every prompt by chris-words.sh, last 40 lines |
| Traps | .claude/traps.md | data columns that lie; 40+ lines |
| Output style | .claude/output-styles/scannable.md | headline / numbers / bullets / call shape |
| Countable gate | .claude/hooks/shape_check.py | Stop hook; counts words, parens, dashes, paths; never blocks |
| Prompt reader | .claude/hooks/chris-words.sh | mode, greenlights, carry-forward of last turn's violations |
| Skeptic | .claude/agents/skeptic.md | fresh-context reviewer before any "done" |
| Commands | .claude/commands/*.md | riff build skeptic wrap price doors drift correction |
| Warehouse gates | warehouse-gate.sh, block-dangerous-git.sh | spend / spine / destroy / git guard |

## Measurements

Scale line in the V4 text says 1.25 billion rows, 589 tables.

| Figure | V4 says | Repo says now | Source |
|---|---|---|---|
| tables | 589 | 676 base tables in LIBRARY_MARTS | reports/warehouse_topo_map_2026-09-05.md, which itself flags 589 as "stale figure from an August report" |
| rows | 1.25B | 2.33 billion | reports/HANDOFF_backfills_2026-09-06.md; 1.25B appears in reports/verification_audit_2026-08-30.md |

Banned-jargon scan, live surfaces only: CLAUDE.md README.md connect/ scripts/ docs/ dbt models .claude/.
Excludes _JUNK_DRAWER and reports/.

| Term | Files hit | Verdict |
|---|---|---|
| AI-driven, lakehouse, microservice, serverless, next-gen, hyper-scalable, democratize, single pane of glass, actionable insights, holistic | 0 | clean |
| paradigm | 2 docs, 7 lines | docs/DEEPFIELD_ATLAS_BLUEPRINT.md:22,280 and docs/HANDOFF_deepfield_reset.md:21,31,98,120,271. Used as "interaction mode". Handoff is a historical record. |
| leverage | 1 doc, 2 SQL | docs/The_Laboratory.md:109 uses it as the physics word. Two stg_portal_soc_connecticut SQL hits are quoted source column names starting AMOUNT_LE… — source data, never touch. |
| any of the above | 11 files in reports/ | historical reports; leave |

Reading of the jargon result: the ban is already obeyed in practice. It is not enforced anywhere. Nothing counts it.

## Gap table

| Component | Current state | Identified gap | Proposed action |
|---|---|---|---|
| system_context scale | not in repo rules; V4 hardcodes 1.25B / 589 | both numbers stale; topo report already calls 589 stale | do not hardcode. One line in CLAUDE.md: "current size lives in the newest warehouse_topo_map report" |
| persona | CLAUDE.md: solo vibe project, BAR SPEAK register | V4 "Uncompromising Senior Systems Architect, mechanical voice" collides with bar speak and the 2026-08-31 register correction | keep BAR SPEAK as the voice. Take the substance: mechanics first, ambiguity is a hazard. Two lines in CLAUDE.md |
| anti_sycophancy | CLAUDE.md: "honest opinions and criticism are wanted" | no rule against validating a bad premise; no format for the correction | add to CLAUDE.md Forks section: a flawed premise gets rejected first, in the shape premise ➔ why it breaks ➔ right mechanic |
| blind_spot / perimeter scan | only the "parked:" line at message bottom | no pre-build scan for what X quietly breaks; parked line is post-hoc and capped at one | add to build.md and CLAUDE.md Building mode: before code, one line naming the adjacent thing X can break, or "nothing adjacent" |
| anti_bullshit banned terms | practice is clean; no enforcement; shape_check.py counts words/parens/dashes/paths only | banned list lives nowhere the machine reads | add a BANNED_TERMS list to shape_check.py; hits carry forward like the other violations; never blocks |
| translation mandates | none written | "call a join a join" has no home | one line in CLAUDE.md methodology block |
| conversational filler | style bans "process narration"; nothing counts openers | "Certainly", "Let's dive in", "Here is" uncounted | add FILLER_OPENERS to shape_check.py, first-line check only |
| micro-chunking, left-anchoring, tables over prose | already in scannable.md and corrections, stricter than V4 | none | leave alone |
| spatial flows ➔ | not written anywhere | arrow chains for data transforms are absent; the ➔ glyph is not counted as a dash by the checker, verified against the regex | one line in scannable.md devices table: `[raw] ➔ [transform] ➔ [what it means]` for data flow |
| code isolation | not written anywhere | reprinting 50 lines for a 2-line change is unbanned | one line in CLAUDE.md Building: show only the lines that changed |
| operational_philosophy | CLAUDE.md methodology block already says it | none; V4 restates "through simplicity, comes complexity" | leave alone |
| "clinical reality" first principles | traps.md is the live mechanism | none | leave alone |
| V4 XML as a whole | would be a second system prompt beside CLAUDE.md | duplicates 60% of CLAUDE.md, contradicts it on voice, its own examples use parentheses the corrections ban | do not paste the XML. Fold the seven gaps above in; drop the rest |

## Regression risk of each proposed edit

| Edit | Touches logic? | Risk |
|---|---|---|
| CLAUDE.md lines | prose only | none |
| build.md line | prose only | none |
| scannable.md line | prose only | none |
| shape_check.py banned terms + openers | one list, one loop, same carry path | low; tests/test_shape_gate.py exists, gets two new cases |

## Open question for Chris

The persona line is the one real fork. Everything else is additive.

## Phase 3 delta log — executed 2026-09-07, uncommitted

| File | Change | Lines |
|---|---|---|
| CLAUDE.md | methodology: mechanics first, ambiguity is a hazard, call a join a join, size lives in newest topo map | +4 |
| CLAUDE.md | Building mode: pre-code blast-radius line; show only changed lines | +2 |
| CLAUDE.md | Forks: reject a flawed premise first, shape premise ➔ breaks ➔ mechanic | +2 |
| .claude/commands/build.md | pre-code blast-radius line | 1 edited |
| .claude/output-styles/scannable.md | devices table: `[raw] ➔ [transform] ➔ [what it means]` | +1 |
| .claude/hooks/shape_check.py | BANNED_TERMS with inflections, FILLER_OPENERS first prose line, table rows scanned for jargon | +55, 0 removed |
| tests/test_shape_gate.py | six new cases: jargon, plain words, filler, clean opener, inflections, table cells | +43 |

Verification: `python -m pytest tests/test_shape_gate.py -q` = 30 passed.
Stop hook run end to end on "Certainly! We leverage the lakehouse." parks three findings, exit 0.

Skeptic pass: AGREE. Two real holes it found are fixed above, inflections and table rows.
Minor notes left open, Chris's call:
- "Sure", "Let me", "Here's" as first word fire even in a headline. First line only, one finding max.
- A quoted report title containing "leverage" fires. Cost is one carry line, never a block.
- ➔ U+2794 sits inside the repo's EMOJI_RE range in shape_check.py. Nothing flags it today. `→` would not.
