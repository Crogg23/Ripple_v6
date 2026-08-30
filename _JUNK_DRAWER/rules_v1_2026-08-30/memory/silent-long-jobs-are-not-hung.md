---
name: silent-long-jobs-are-not-hung
description: "2026-08-11 — the connection-engine reseed prints ONE line at the end; two hours of silence is normal, not a hang. Verify with warehouse query history before killing anything."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2abe330a-1107-4aec-8937-200e6edcd021
  modified: 2026-08-11T14:10:50.825Z
---

`python -m connect.incremental seed --reseed` emits a **single** print at the
very end (`seed: SPINE_KEYSET_LIVE=...`). It runs for **hours** producing zero
bytes of output while doing thousands of ~1s MERGE statements against
`LIBRARY_META.CONNECT.CONNECT_WATERMARK`, one per table.

The 2026-08-10 session read ~20 minutes of that silence as "produced zero output,
probably dead" and killed a perfectly healthy job, leaving the connection engine
in an unknown state and burning the next session's boot time re-running it.

**Why:** empty stdout is not evidence of a hung process, and for this job it is
the *expected* state. The only reliable liveness signal is the warehouse itself.

**How to apply:** before killing any long-running warehouse job, check what it is
actually doing:

```sql
SELECT START_TIME, EXECUTION_STATUS, TOTAL_ELAPSED_TIME/1000, LEFT(QUERY_TEXT,110)
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(RESULT_LIMIT=>25))
ORDER BY START_TIME DESC
```

Steady recent SUCCESS rows = alive, leave it alone. Also prefer a per-item
checkpoint file as the progress signal where one exists — the FEMA loader writes
`outputs/_fema_ia_checkpoint.json` every page, which tells you progress even
though its log only prints every 10 pages. Related: [[loader-runtime-traps]],
[[stale-commands-are-live-ammo]].
