---
name: coverage-sweep-2026-08-05
description: "2026-08-05 coverage sweep results: warehouse compute back alive; 895 blind spot = all portal crawl; 299 pairs opened; NDC/EPA-case/CUSIP new key families verified; HCRIS is hospitals-only"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3a7d2947-f999-4d94-a06a-6e48f9099917
  modified: 2026-08-05T14:01:49.463Z
---

The 2026-08-05 key & join coverage sweep (`outputs/coverage_sweep_findings_2026-08-05.md`) established:

- **Warehouse compute is back** — COMPUTE_WH ran real queries 2026-08-05 (quota apparently reset Aug 1). The "SERVE_MON exhausted = compute dead" state from early August no longer holds, though it can recur.
- **There are no unknown federal landing tables.** All 895 unfingerprinted landing tables are portal crawl samples (892 PORTAL_CKA 10k-row city open-data samples + 3 others). All 375 non-portal landing tables are fingerprinted.
- **New key families verified by real joins, not yet in the spine:** NDC (FED_DEA_ARCOS_FULL 178M rows, FED_CMS_NADAC, Open Payments NDC_1-5 — needs 5-4-2 segment padding, naive dash-strip gives 0%), EPA enforcement case number (ECHO ↔ ICIS_FEC case tables, `0X-YYYY-NNNN`), CUSIP (internal to the 13F trio, no external bridge yet), disguised CCN columns (POS_OTHER PARENT/CROSS_REF_PROVIDER_NUMBER = ownership chains at 74%/34%, HOSPITAL_COMPARE.FACILITY_ID at 100%).
- **FED_CMS_HCRIS is hospital cost reports only** (STH/CAH/PH/RH/LTCH, 6,103 rows) — 0.0% CCN overlap with nursing homes in both directions. The old A-4 "facilities hiding cost reports" lead is a population artifact; the real gap is the never-ingested SNF/HHA/Hospice HCRIS files (external acquisition).
- The 299 (not 285) share-key-no-edge pairs were all measured: 58 joinable-sparse (hits are leads), 5 CIK zero-padding fixable, 74 blocked by capped tables (see [[warehouse-data-traps]] sorted-truncation trap), 174 genuinely disjoint (incl. all cross-type CCN — namespace artifact empirically confirmed).
