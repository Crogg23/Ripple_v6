# Handoff: Data Coverage Expansion — 2026-07-25

## STATUS: Phase 1 + Phase 2 COMPLETE (desktop session ran the live pipeline)

The laptop wrote the code (Phase 1.1/1.2/2.1) but was blocked on an expired PAT.
The desktop session had a working connection and ran the full pipeline end-to-end.

---

## What the desktop session did

### Ran the live pipeline (was blocked on laptop)
`fingerprint` (242 core -> 906 tables, +664 connectable portals) -> `discover` ->
`spine` -> `incremental seed` -> `validate` (all 6 PASS) -> terrain map. 480 tests green.

### Found + fixed a portal noise explosion
First discover after portal activation jumped 1,506 -> 13,477 edges. Investigation:
- ~1,560 were REAL new portal hard-ID/composite edges (the win)
- 1,991 were junk DOCKET edges (court-local `cv-00001` collides across districts)
- ~9,340 were ZIP geographic co-occurrence (harmless: filtered from map, not in spine)

**User decision: gate DOCKET, keep the rest; keep bare-NAME gated.**

### DOCKET gate added (discover.py `_build_keysets`)
Portal tables now skip the DOCKET key. Curated federal court sources (Oyez/SCDB,
which use globally-unique SCOTUS dockets) still match — that legit edge survives
(FED_OYEZ<->FED_SCDB, 22 matched, conf 0.92). Killed 1,991 portal DOCKET junk edges.

---

## Final state

- **CONNECT_EDGES: 11,486 edges** (verified DB count == run output, no accumulation)
  - by tier: GEO=9,567, CORROBORATED=1,185, STEEL=527, BRIDGE=206, STRONG=1
  - hard-ID + composite (STEEL+CORROBORATED+BRIDGE): **1,918** (up from 357 baseline)
- **Spine unchanged: 16.2M golden, 22.8M nodes** — portals feed the GRAPH, not the
  entity spine (spine only draws from curated DISPLAY_SPECS / hard IDs). Correct + safe.
- **Terrain map: 80/242 core tables connected** (down from 105 — bare-NAME gate dropped
  25 core tables whose ONLY links were low-confidence name matches; deliberate tradeoff).
- **Spot-check verified:** FED_CMS_NPPES <-> California open data = 3,487 NPIs,
  recomputed from source = 3,487 exact. Portal connections are real and provable.

## Verified portal wins (examples)
- CMS NPPES <-> California / SF / Harris County (Houston) health data: 1,100-3,500 NPIs each
- Portal EIN/CCN/PATENT/DUNS links into IRS, CMS, USPTO, USASpending

---

## GOTCHAS hit this session (for next time)

1. **Never pipe `discover` through `Select-Object`/head.** PowerShell ^C on a pipe leaves
   the Python child alive; it writes on top of the next run and DOUBLES CONNECT_EDGES
   (saw 11,486 -> 34,906). Run to a log file, no pipe, verify DB COUNT == reported count.
   Check `Get-Process python` for zombies before re-running. (This is audit HIGH #3:
   CONNECT_EDGES uses non-atomic TRUNCATE-then-INSERT.)
2. **PAT expires mid-session** on long spine/discover runs. `seed` failed once on token
   expiry; re-running with a fresh connection worked. If it recurs, regenerate the PAT.

---

## What's next: Phase 3 (not started)

Loader campaign for the 769 cataloged-but-unloaded sources:
- Triage by ACCESS_METHOD + PRIORITY_TIER (379 Tier-1)
- ~600 are spec-able (append dicts to `server_side_specs.py`) — API/bulk/CSV/zip/json
- ~132 portal-only -> route through `portal_loader.py` connectable mode
- Batch Tier-1, load + verify + incremental `connect-one` after each batch
- Track coverage per batch

## Optional follow-ups
- Portal ZIP-GEO edges (9,340) are harmless but bloat CONNECT_EDGES — could drop if desired
- Fix the CONNECT_EDGES non-atomic write (audit HIGH #3): staging + SWAP

## Key files changed this session
- `connect/discover.py` — DOCKET portal gate (in addition to laptop's fanout cap + NAME gate)
- `outputs/terrain_map.html` — regenerated

## Baselines to verify against
- `LIBRARY_META.CONNECT.CONNECT_EDGES` = **11,486 rows**
- `pytest -q -m "not snowflake"` -> 480 passed, 7 deselected
