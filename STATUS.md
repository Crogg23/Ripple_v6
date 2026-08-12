# RIPPLE STATUS — 2026-08-12 (session 3) — Direction change: build the measurement grammar over the whole warehouse

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new.** The roll-call vote mart still disagrees with its
Python-built twin (113,512 vs 3,364 rows) — standing, untouched.

---

## THE HEADLINE: a correction to the last session, and a new direction

**1. The pension data was never blocked. The last session looked in the wrong
subject area.** It searched the economics area, found only PBGC's aggregate Data
Book statistics, and concluded the plan-level table "doesn't exist here or was
never cataloged." It exists, in the labor area, built 2026-08-09: one row per
failed pension plan, with employer tax ID, plan number, sponsor name, plan
termination date, government-takeover date and participant count. Two of the ten
findings were retired early on a wrong-place answer.

**NOT yet verified:** whether that tax ID column is actually populated. The model
tests the case number and sponsor name but not the tax ID, and sentinel-masked ID
columns have fooled this platform twice. One distinct-count plus a value sample
settles it, and it unblocks the sharpest harm chain on the platform (injury logs →
SEC filings → failed pension → insider filings, all on one tax ID).

**2. Direction change, Chris's call, after a long working session:** stop leading
with curated harm cases. Build the **measurement grammar** — an unbiased, complete
description of every source in one language, so extraordinary things announce
themselves instead of waiting for someone's hunch.

His reasoning, in his words: leading with ten curated findings is *"dipping a 5
gallon bucket in the ocean and then saying we didn't catch a whale, must be
nothing out there."* And the harder point: 82% of chronic violators facing no
enforcement is currently **uninterpretable** — nobody knows if that's the worst
number in American regulation or completely ordinary, because there's no baseline.
The census creates the baseline; the existing findings become readable cells in it.

**The model:** every row is a NOUN (persists, denominator), an EVENT (dated,
numerator), a LINK (a relationship between two nouns — the roads), or a CODE
(vocabulary). Every measure is events per noun, cut by codes, along links. Same
model as Chris's day-job emergency-department analytics — multiple fact tables at
their own grains, conformed dimensions, metric library defined once.

**First deliverable:** the grid (~50+ things × ~30 display slots, on the order of
1,500 surface views) plus the parking lot **with a tally** — a branch parked forty
times across forty things is the ranked build roadmap, decided by vote count
instead of instinct.

**The unique output nobody else on earth can produce:** the same six ratios for
every domain in identical units on one page — how much ever gets looked at, how
much is wrong when someone looks, whether being caught means anything, whether it
costs anything, whether findings predict harm, how many people are exposed per
institution.

---

## PROCESS CHANGE — now enforced by hook, not by memory

Chris had to push three separate times in one afternoon to get range out of a
session. The breadth-first method is now injected on **every prompt** via
`.claude/contract-reminder.md`: start at the tippy top, surface pass per thing,
park branches in one line and return, cover everything before deepening anything,
three altitudes on open asks, caveats only at the end while exploring, a smallness
check before sending, never treat a prior artifact as the ceiling.

This same feedback already existed three times in memory and never fired. That's
why it's in the hook now. **CLAUDE.md was not edited — that file is Chris's.**

---

## Live/open items

- **Verify the failed-pension table's tax ID column** — top of the cheap-fix list.
- Handoff written for the next session (measurement grammar, with an
  additive-only ratchet: widen freely, never narrow). Path in Chris's chat.
- Roll-call mart rebuild via Python builder still owed (standing).
- Identity-map full rebuild decision (~4.5h, ~$10-15) still parked with Chris.
- CourtListener citation-network load retry still pending.
- Patch the earlier ladder corrections into the ladder doc (yellow-lane, not done).
- **Everything from all three of today's sessions is uncommitted:** the ladder
  report and receipts, the rankings, the perspective doc, the updated hook, this
  file. Chris has not ruled on committing.

## Coverage read from today (context for the next session)

Checked the ten findings against current published coverage. Two are settled
ground and were done better elsewhere with data this warehouse doesn't have
(drug-level payment linkage). One walks into a twenty-year prepared corporate
defense. Three sit on beats that are hot right now. Three appear genuinely
uncovered. Full detail: `reports/perspective_2026-08-12.md`.

**YOUR MOVE:**
1. Say whether to commit today's work (report, receipts, perspective doc, hook).
2. Paste the handoff prompt into a fresh session when ready.

**NEXT SESSION:**
1. Boot trust check against this file and git log.
2. Independent read on the measurement-grammar design — widen it, never narrow it.
3. Then build the grid and the parking-lot tally, from table metadata (near-zero
   warehouse spend; price tag before any real compute).

**Tests:** not run (no platform code changed — new files only: reports, memory,
hook, STATUS). Last known: offline suite 3,034 passing, 2 skipped, 1 pre-existing
failure (roll-call mart).

**COST:** this session ~$2-3 — file reads, six web searches, no subagents, no
warehouse queries.
