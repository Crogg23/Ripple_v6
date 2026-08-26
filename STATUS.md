# RIPPLE STATUS — 2026-08-25 — Visualization options map delivered (60 picture ideas, 30 tools, no pick made); spine rebuild is STILL the gate

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

## DONE (this session)

- **Built the visualization options menu Chris asked for.** Not a
  recommendation and no shortlist — deliberately. Covers the nine groups of
  warehouse-audit numbers (overall size, per-database split, the 847→178→267
  registration correction, the entity-graph scale chain, the 24,011 measured
  overlaps, the docket trust split, the dead weight, the four-step pipeline,
  the key trust tiers) with **6-7 different picture ideas per group — 60 in
  total, plus 6 deliberately wild ones**, each scored on the same nine
  dimensions (page weight, build hours, interactivity, design ceiling, scale
  fit, accessibility, theme flexibility, self-regeneration, differentiation).
- **Compared 30 tools** with versions and licenses checked live against current
  documentation, not recalled. Written up in
  `reports/VIZ_OPTIONS_MAP_2026-08-25.md` (964 lines).
- **Published a browsable version** so the menu can actually be used to choose:
  filter by group, sort by any dimension, hide the ideas already built, star
  picks into a shortlist that persists. Local original:
  `reports/viz/options_board_2026-08-25.html`. Rendered and screenshot-verified
  in headless Chrome — all three tabs.
- **Checked what's actually on this Mac** rather than assuming: plotly, altair,
  pandas, numpy, networkx, pydeck, dash, Pillow and duckdb are installed;
  **matplotlib is NOT** (which blocks seaborn, plotnine, PyWaffle and part of
  Datashader without an install first). **Node IS installed** (v22.23.2 via
  nvm) — this corrects a standing note in memory that said there was none.
- **Flagged one licensing trap**: the friendly wrapper around the fastest
  big-graph renderer (Cosmograph) is non-commercial-only; the underlying engine
  (cosmos.gl) is MIT and unrestricted. Also flagged that the most common
  interactive chart library adds ~318KB gzipped to a page — heavier than every
  hand-rolled option in the map combined.

## BROKE

- **Nothing broke this session.** No warehouse writes, no code changes, no
  tests run (none were touched).

Carried forward, unchanged from 2026-08-24 — these are still true:

- **The full spine rebuild still has NOT run.** The 90 tables wired on 08-24
  (11 federal + 79 portal samples) are registered but not live until it does.
  Session permission guards block it; Chris runs it himself.
- **The USAspending contracts re-pull is stalled**, not growing — last write
  08-23 21:43 PDT, stopped at FY2021, 63.7M rows. It runs on the Windows box.
- Other loads with unknown completion state: FEMA housing registrations
  (23.97M rows, last write 08-23), SAM exclusions (168,328 rows, looks
  complete), Senate lobbying filings (273,821 rows, stopped 08-22).
- **Nothing is committed.** The 08-24 registry edits, the wiring plan, the
  audit updates, and this session's two new files are all uncommitted
  (standing rule: Chris confirms before commit/push).
- Still no Snowflake billing visibility.
- One test file (the staging-model normalizer parity check) hangs for minutes
  on this Mac — pre-existing, looks like the iCloud-evicted-files problem.

## YOUR MOVE (Chris)

1. **Pick from the menu.** Open the options board, star what you like. That's
   the taste call this session deliberately didn't make.
2. **Full spine rebuild** (~$10-15, the standing parked money item) — still the
   gate on 90 wired tables going live.
3. Contracts re-pull: restart on the Windows box, or call FY2007-2021 good
   enough.
4. Two USAspending contract tables (20M and 6.3M rows) are now redundant with
   the re-pull — drop from the spine or keep. Flagged, not decided.
5. Still open from before: corporate bridge; security fix; roll-call scope;
   CourtListener bulk pull; dead-database cleanup; billing access.

## NEXT (for the session picking this up)

1. If Chris has starred picks, the next job is building them — not re-opening
   the menu. The map's own note applies: the biggest fork is static vs.
   interactive vs. illustrated, not which library.
2. Anything illustrated (the metaphor concepts) does NOT regenerate itself when
   the audit re-runs. That's a knowing cost, not an oversight to fix later.
3. Six of the nine number-groups need no charting library at all — typography,
   SVG, and one canvas loop. Only the graph-scale and browse-the-data ideas
   actually need one.
4. If a static-image route gets picked, matplotlib and kaleido both need
   installing first; if a Vega/Altair route gets picked, vl-convert-python does
   (it needs no Node or browser).
5. After the full spine rebuild: re-run the audit's overlap pass to turn
   "90 tables wired" into "N new real connections" — every number in the
   options map moves when that happens.

**Cost note:** Claude session cost not metered. **Zero Snowflake compute this
session** — no queries were run; every number came from the audit CSVs already
on disk. Roughly a dozen web searches/fetches for library verification.
