---
name: official-id-inventory-2026-08-29
description: The master have-vs-missing list of official ID systems (26 wired / ~50 held-unregistered / ~30 not held) and where it lives
metadata: 
  node_type: memory
  type: project
  originSessionId: ae3d683b-a240-40da-be51-79975a87c0ff
  modified: 2026-08-29T14:22:18.532Z
---

On 2026-08-29 a repo-only inventory of every official/government ID that can connect public data
was written to `reports/recon/official_id_inventory_2026-08-29.md` (scan CSV alongside it).

**Three buckets:**
- A: 26 hard-ID families wired in the spine; 5 dead/one-sided (PATENT, IMO, MMSI, DEA, DUNS).
- B: ~50 ID systems already in mart columns but unregistered — CAGE, award keys, PECOS enrollment,
  EIA plant IDs (the "dead" ENERGY domain actually has keys), FDIC cert + RSSD, NDC, FDA FEI/510k,
  CAS/UNII, ticker, HMDA respondent, OSHA establishment, DOL plan #, LDA IDs, FJC NID.
- C: ~30 not held at all; only USCG vessel registry, PatentsView, FMCSA census cheaply revive dead axes.

**Why:** Chris asked for the full have-vs-still-out-there list; prior recon lists (08-18 sniffer,
08-28 catalog recon) were samples, not the boundary.

**How to apply:** treat this file as the reference before proposing any new key family or source —
check whether the ID is already in bucket B (wire it) before landing a bucket-C source. Presence in
bucket B is name-scan only unless marked verified. Related: [[courtlistener-key-registration-2026-08-17]],
[[value-shape-sniffer-2026-08-18]], [[spine-connection-audit-2026-08-11]].
