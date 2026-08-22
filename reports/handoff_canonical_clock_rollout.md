# Handoff — finish the "which date is real" work (canonical clock rollout)

**Queued 2026-08-21 by Chris as a dedicated build session — not started.**

## Why this exists

Every FLOW/lead-lag claim in Ripples depends on knowing, per table, which date
column is the real event date vs paperwork vs a load stamp. That classification
was mostly done 2026-08-20 (see `reports/time_index/`) but has three real gaps.
Chris's framing: "the accuracy of a timeline, a flow, a RIPPLE is crucial" —
this is foundational, not cosmetic.

## The three gaps, in build order

### 1. Finish the classification (cheap, read-only, ~15 min / $1-2)
- 229 of 482 tables got a full adversarial review (health, justice, economics,
  environment). The other **253 — politics, labor, energy, housing, finance,
  transport, immigration, corporate registry — never got reviewed.** Their
  counts in the existing reports are floors, not verified totals.
  (`reports/time_index/CLOCK_FINDINGS.md`, "Read this before the numbers.")
- Re-run the merge/review step without truncation (the doc names this as the
  one outstanding task from last time).

### 2. Add a genuinely new clock category: "planned / future"
- The existing classification has 5 buckets: happened, reported, decided,
  span_start, span_end (plus ingest and not_a_date). **None of these is "a date
  that hasn't happened yet and might change"** — a proposed rule's effective
  date, a scheduled hearing, an upcoming compliance deadline.
- Right now a future date either gets read as a normal event (wrong) or
  survives only because it happens to sit in a legitimate open-ended span
  field (e.g. `9999-12-31` sentinels, contract end dates — already handled
  correctly per `CLOCK_FINDINGS.md` Mechanism B note). A **standalone planned
  date on a standalone record** is not yet a recognized category.
- Needs: a rule that flags "this value is in the future AND this column isn't
  already a known open-ended span field" → tag it `planned`, not `happened`.
  Any FLOW rule must default to excluding `planned` dates from "what occurred"
  analysis unless explicitly asking about upcoming/scheduled events.

### 3. Roll out the canonical column (the big one — real dbt build, most tables)
- Today the classification lives in a report (`clock_index.csv`), not in the
  data. Nothing stops a query from grabbing the wrong date column by accident.
- Build: every mart table exposes one standard column — the real event date
  for that noun — tagged with its clock type (happened/reported/decided/
  planned/span) and grain (day/month/quarter/year).
- This is explicitly flagged as "NOT done" / "the next build" in
  `reports/time_index/README.md` already — that note predates today, this
  just adds the `planned` category to what gets rolled out.
- Add a tripwire test: fail loud if any rule/chart reads a `planned` or
  `reported` column where a `happened` column exists and should have been
  used instead.

## What NOT to relitigate
- The parsing standard, the calendar table, and the sentinel-repair work from
  2026-08-20 are done and correct — this is about finishing coverage and
  wiring the guardrail in, not redoing that work.

## Landmine to fold into docs/RIPPLES.md while here (Chris's call, still open)
From this session's pilot rule: shared administrative scheduling (e.g. one
state inspector visiting several same-owner facilities back-to-back) can fake
a neighbor signal that looks like real correlated behavior. Worth a 5th
landmine or folding into landmine 1.
