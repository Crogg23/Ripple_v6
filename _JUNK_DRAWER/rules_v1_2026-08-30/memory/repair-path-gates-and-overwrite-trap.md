---
name: repair-path-gates-and-overwrite-trap
description: "What warehouse repairs sessions CAN run vs Chris-gated (2026-08-11 repair arc), plus the write_pandas overwrite schema trap"
metadata: 
  node_type: memory
  type: project
  originSessionId: 51ae13dd-f4e4-468d-974d-822f54e81cb3
  modified: 2026-08-11T16:29:51.151Z
---

Learned 2026-08-11 during the repair arc:

- The permission classifier blocks CREATE TABLE AS / SWAP / CREATE OR REPLACE
  on landing tables even when wrapped in a reviewed script with guard rails
  (`scripts/dedupe_landing_exact.py --run` was denied). UPDATEs through
  established repair tools (`scripts/repair_nan_text.py`) DO run. Plan repairs
  as: fix marts/staging in dbt (allowed), land NEW tables via loaders
  (allowed), queue every swap/drop/delete as a Chris one-liner
  (precedent file: reports/repair_session_chris_gates_2026-08-11.md).
- `write_pandas(overwrite=True)` on snowflake-connector 3.18 TRUNCATEs and
  KEEPS the old table schema. If the new pull has different columns/types,
  in-place refresh is structurally impossible without DROP — land a `_FULL`
  new table and repoint the dbt source instead.
- Mart dedupe subtlety: landing-level distinct ≠ mart-level distinct. Casts
  (to_double/to_date) collapse formatting variants ("1.0" vs "1"), so dedupe
  the PROJECTED cast values (SELECT DISTINCT in the mart), not just the raw
  landing columns — the mortgage DB was 11,648 raw-distinct but 7,204 true rows.

Related: [[feedback-stale-commands-are-live-ammo]], [[loader-runtime-traps]].
