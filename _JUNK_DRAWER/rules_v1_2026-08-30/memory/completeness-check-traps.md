---
name: completeness-check-traps
description: Two ways a completeness-vs-publisher check lies (VARIANT chunk tables; wrong publisher totals) — found in the 2026-08-11 repair arc
metadata: 
  node_type: memory
  type: project
  originSessionId: 51ae13dd-f4e4-468d-974d-822f54e81cb3
  modified: 2026-08-11T16:29:58.033Z
---

Two false-alarm classes from the 2026-08-11 verification, worth checking
before ever declaring a source SHORT/OVER again:

1. **VARIANT chunk landing tables**: the openFDA family lands JSON in chunks —
   one ROW is a `{"results": [~2,000 records]}` bundle. INFORMATION_SCHEMA
   row counts count chunks, so an 88-row table can hold 175k records. Detect
   via a single `RAW VARIANT` column or the `split_json:` / `json:` tag in the
   ingest-run log; count with `SUM(ARRAY_SIZE(RAW:results))`.
2. **Publisher totals are themselves wrong or a different measure**: FEMA's
   community-status API metadata.count said 32,436 but its own full CSV ends
   at 25,125; GLEIF's stats page said 658k "relationships" but the golden-copy
   RR file holds 484,142; ransomware.live prunes history (46,405 shrank to
   30,661); EPA's "1.5M+ facilities" is ad copy vs 3.14M real. Treat a
   SHORT/OVER verdict as a hypothesis — re-derive the publisher number from
   the actual downloadable artifact before repairing anything.

Related: [[bridge-fuel-reality]], [[warehouse-verification-2026-08-11]].
