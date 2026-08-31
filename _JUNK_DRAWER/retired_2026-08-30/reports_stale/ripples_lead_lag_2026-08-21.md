# The lead-lag pass — every stream against every stream (2026-08-21)

**What this is:** Boxes 3 and 4 of the flow ladder (docs/RIPPLES.md), run
impartially: every qualifying pair of streams got the identical treatment —
no pair pre-picked. 271 streams qualified (207 monthly with >=36 common
months after trimming the incomplete tail, 64 yearly with >=10 common
years), giving **19,387 tested pairs**. Zero warehouse cost — computed
entirely from the 2026-08-20 trend sweep's series file.

Script: `scripts/ripples/lead_lag_pass.py`
Raw outputs: `reports/ripples_lead_lag_2026-08-21.json` (run 1, raw),
`reports/ripples_lead_lag_deseasonalized_2026-08-21.json` (run 2, final).

## Method

- Signal = month-over-month (or year-over-year) change in log count.
- Per pair: correlation at every offset from −12 to +12 months (−3..+3
  years); the best offset is the candidate lead.
- **Null check (landmine 2):** the observed best correlation must beat the
  95th percentile of every circular rotation of one series — rotations
  preserve each stream's own autocorrelation, so this is a hard null, not a
  soft one. Plus a floor: |corr| >= 0.3.
- **Ragged-clock guard (landmine 1):** where both tables have a measured
  median reporting lag, a "lead" smaller than the lag difference is flagged
  `fax_machine_suspect` — kept and labelled, never dropped.

## What happened, run by run — this is the finding

**Run 1 (raw changes): 2,751 of 19,387 pairs beat the hard null — and the
top of the list was semantically absurd.** Supreme Court decision counts
"leading" Texas lobby filings; a place-names gazetteer "leading" judicial
appointments. Diagnosis: the government runs on one shared calendar —
fiscal-year ends, court terms, filing seasons, election cycles — and an
honest null can't kill a rhythm both streams genuinely share.

**Run 2 (month-of-year rhythm removed first): 1,830 survive.** A third of
all "significant" co-movement in the warehouse was the shared federal
calendar. The remainder is dominated by a second confound the pass can
name but not remove: **the shared macro tide** — smooth multi-decade global
trends (fertility vs. CO2 at r=0.90) and shared coverage windows (a 2025
campaign-contribution table "co-moving" with device registrations because
both simply grow across the same two years).

## The honest headline

> **An untargeted numbers-only sweep cannot tell mechanism from tide. What
> it CAN do — and did — is measure the tide itself and hand over a queue.**

Concretely, per the resemblance doctrine (Ripple 2): these 1,830 pairs are
a **queue, never findings**. The loop that makes one publishable is wiring:
a pair survives as a lead only if the two streams are also connected in the
entity spine (same place, same owner, same regulated universe) — which is
exactly the next deepening, and it is a join, not a statistic.

## What is worth pulling from the queue first

Pairs whose two streams share an obvious real-world pipeline (candidate
mechanism, not proof):

| leader → follower | offset | corr | plausible pipe |
|---|---:|---:|---|
| Federal single-audit acceptances → federal criminal filings | +4 months | +0.75 | audit findings feeding prosecutions |
| FDA device approvals ↔ Federal Register documents | same month | +0.84 | the regulatory pipeline moving as one |
| Vehicle-safety complaint failure dates → complaint filings | (see fax flags) | | the classic happened→reported pipe |

32 pairs carry the `fax_machine_suspect` flag — their "lead" is smaller
than the difference in the two tables' reporting speeds. Kept and
labelled: a fake lead caused by filing speed is a fact about the filing
speeds.

## Junk this sweep surfaced as a side effect

- A drinking-water service-area table is catalogued under the IMMIGRATION
  domain (its twin sits correctly in ENVIRONMENT) — a mislabelled domain in
  the catalog, worth a one-line fix.
- The NYC 2025 campaign-contribution table co-moves with dozens of
  unrelated streams purely because its two-year coverage window overlaps
  everything that also grew in 2024–25 — short-window tables should carry a
  minimum-span bar before being read in any pair result.

## Where this leaves the flow ladder

- Box 0 (staleness): measured (2026-08-20 lag sweep).
- Box 1–2 (does it flow / heartbeat): measured (2026-08-20 trend sweep).
- **Box 3 (co-movement): now measured, warehouse-wide, this pass.**
- **Box 4 (who moves first): now measured; survivors are a queue pending
  wiring confirmation.**
- Box 5 (where the wave breaks): unbuilt — needs cross-table joins on the
  entity spine, the natural next tick.
