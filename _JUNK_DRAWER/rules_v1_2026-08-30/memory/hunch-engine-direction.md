---
name: hunch-engine-direction
description: "Chris green-lit the Hunch Engine (2026-08-01) — open-ended surprise discovery, explicitly NOT a menu of N hypothesis shapes; pattern-grain publishing now exists"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9a0c0f48-5e58-4de7-b36a-c0956df0b5e7
  modified: 2026-08-01T22:13:19.540Z
---

2026-08-01: Chris ruled patterns publish FIRST (systemic finding is the
headline; individual leads are receipts, publish separately) — built
scripts/publish_pattern.py + provision_pattern_publish.sql (cohort 'published'
inherits to members only as 'confirmed', never PUBLISHED).

He then green-lit ("full send, best work yet") the **Hunch Engine**: a
build-time discovery layer + third Playground room that finds *places to look*.
Critical taste ruling: NO predefined question taxonomy — he explicitly rejected
"one of N shapes." One primitive only: exhaustive comparable-pairing lattice
from spine + COLUMN_CATALOG metadata, one surprise score vs a boring null
model, no editorializing, blind spots reported. Hard problems flagged: fluke
control (reuse spine score-against-chance), trap contamination (wire
[[warehouse-data-traps]]), compute cost = red-lane budget. Build order: lattice
census (free) → null-model note → hand calibration → sieve. Handoff doc written
to the session scratchpad (HANDOFF_hunch_engine.md).

**Why:** "You constantly think too narrow" — he wants open-endedness preserved.
**How to apply:** never reintroduce a category menu into the Hunch Engine;
patterns emerge from the one primitive. See [[playground-and-two-desk-state]].

Build state (later same day, this session): census/scorer/sieve built as
hunch/ package (census.py, score.py, sieve.py — pure, offline-tested) +
scripts/hunch_census.py + scripts/hunch_sieve.py + infra/ddl/
07_hypothesis_catalog.sql (DDL pending Chris in Snowsight; verdict rows are
sacred on rewrite). Census: 7,174 comparable pairs, 78% name-only, 593
verified. Calibration: verified >= +2.7 S, chance ~0; two absence traps found
and fixed — CCN partitions on MIDDLE digits (leading 2 = state!), so absence
needs fmt-2 range/prefix data PLUS a measure-time bucket-histogram check.
fingerprint.py upgraded to fmt-2 (min/max/prefixes, checkpoint+resume);
Chris approved ~$8 full re-sweep incl. 133 dark core tables (482M rows: ARCOS,
13F, CourtListener, FAERS...). Key repo trick: connect_fingerprints.json +
connect_graph.json + registry views give a zero-cost metadata census; bridge
relations derive from dual-hard-ID tables (connect/bridge.py HARD), NOT from
xref_bridges.csv.
