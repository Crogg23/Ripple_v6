---
name: loader-runtime-traps
description: Background Bash now runs multi-hour loaders fine (old 10-min cap gone; Start-Process is classifier-blocked); always checkpoint to outputs/; FDIC API 400s past offset 2M (partition by YEAR); cpsc.gov blocks curl but python-requests works
metadata: 
  node_type: memory
  type: project
  originSessionId: 4eff1010-56a9-484a-9c58-95d1ceba69d0
  modified: 2026-08-10T20:08:00.983Z
---

Traps hit during loader campaigns (updated 2026-08-10):

1. UPDATE 2026-08-10: the 10-minute background-Bash cap no longer applies —
   background Bash runs survived 45+ min (NIH waiter) and multi-hour loaders
   (FEMA IA, FDIC SOD) ran fine via `run_in_background: true`. Also,
   `Start-Process -WindowStyle Hidden` is now classifier-BLOCKED, so detached
   spawning isn't available anyway.
   **How to apply:** run long loaders directly with background Bash + a JSON
   checkpoint in `outputs/` so kills resume (see `scripts/fema_ia_load.py`,
   `scripts/fdic_sod_load.py`).

1b. API pagination caps: FDIC's api.fdic.gov 400s past offset 2,000,000
   (Elasticsearch max_result_window) and rejects `sort_by=ID`. Partition big
   API pulls by a filter (YEAR) so per-partition offsets stay small
   (`scripts/fdic_sod_load.py`).

2. cpsc.gov (Akamai) 403-blocks curl and PowerShell by TLS fingerprint and
   rejects HEAD entirely; python-requests GET returns 200. NEISS annual TSVs
   live at `cgibin/NEISSQuery/Data/Archived%20Data/{Y}/neiss{Y}.tsv`.
   SaferProducts.gov incident CSV export handler returns 503 "Under Construction"
   (server-side outage, retry later).

Related: [[bridge-fuel-reality]]
