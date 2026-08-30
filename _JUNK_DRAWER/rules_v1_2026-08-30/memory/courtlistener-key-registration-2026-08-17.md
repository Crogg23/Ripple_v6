---
name: courtlistener-key-registration-2026-08-17
description: "The 2026-08 spine batch: court keys + 39 verified spec tables + 3 new families (water permits, credit unions, ICE) staged behind connect/keys.py ENABLE_SPINE_BATCH_2026_08=False; flipping the flag freezes incremental until a full spine rebuild, so flip ONLY in the rebuild session"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3ab43dbd-d3b2-4d61-b3b2-69fd90b2d321
  modified: 2026-08-18T04:33:13.176Z
---

2026-08-17, Chris's "just go" after the census-grid fill: the court tables'
internal IDs are registered as two staged spine key axes — CL_PERSON_ID
(judge, person) and CL_COURT_ID (court, organization).

**Measured first** (`reports/census_grid_2026-08-12/fill/courtlistener_edges.json`,
script `scripts/census/courtlistener_edge_verification.py`): 19 of 20 join
surfaces at 99.2–100% referential match — court→docket 100% on all 71.7M
dockets, judge→assigned docket 100% on 32.4M, judge→disclosure 99.8%,
disclosure money chain 99.4–99.6%. **POSITIONS.APPOINTER_ID is NOT a person
reference** — 47.2% match, deliberately excluded from wiring. JUDGES has 394
alias rows (thin duplicate entities, accepted). COURTS.FJC_COURT_ID (200 rows)
is a future bridge out of the CourtListener namespace.

**The staging mechanism (the trap to remember):** any change to NORM_RULES or
DISPLAY_SPECS changes the incremental-config fingerprint and
`incremental._guard_config` then refuses connect-one/connect-changed until a
FULL `python -m connect spine` re-pins it. So the ENTIRE 2026-08 batch is
gated behind `connect/keys.py: ENABLE_SPINE_BATCH_2026_08 = False` (specs in
`entity_index_specs.COURTLISTENER_DISPLAY_SPECS` +
`SPINE_BATCH_2026_08_DISPLAY_SPECS`; ENTITY_TYPE_BY_KEY and discover
KEY_DOMAIN entries are unconditional/inert). **Flip the flag in the same
session that runs the full rebuild (~$10-15, parked with Chris), never
before** — verified both ways: flag off = fingerprint unchanged
(c64073b9...), flag on = 173 spec tables / 196 (table,key) pairs.

**Batch contents ("no bits and pieces", Chris 2026-08-17):** 39 new spec
tables on existing axes (IRS EO BMF 1.98M charities golden names; 527 family;
both PBGC pension tables + Schedule SB; PECOS 2.5M; Open Payments profiles
1.7M; DME suppl/refer; HRSA sites; Medicare hospital price books; NIH +
SBIR/STTR with UEI+DUNS extra_keys — the spine's FIRST DUNS entities; PCAOB
issuer CIK; SEC fund registry + ticker map; ISO MIC LEI; UK sanctions IMO;
EPA FRS registry 3.28M + ICIS air + GHGRP + TRI 2023) plus 3 new families:
NPDES_ID (7 event tables, 100% referential), NCUA_CHARTER, ICE_FACILITY.
Verification evidence: `reports/census_grid_2026-08-12/fill/
spine_batch_verification.jsonl`. **Rejected on evidence** (don't re-add): FCC
EIN masked, FDIC LEI empty, TRI_FACILITY FRS dead, FED_US_SEC_EDGAR ~25
companies only, XC_EPA_CORPORATE_CROSSWALK is fuzzy name-matching (overlay,
never spine), RETIRED-schema tables, IRS527_8871 twin. **Parked:**
legislators' FEC_IDS is a JSON array per row (needs flatten build); banking
FDIC-CERT/RSSD family. Also backfilled COMPANY_NO's missing KEY_DOMAIN entry.

Also: entity_index_specs is imported both as a package module and bare
(spine_entity.py path-hack), so imports inside it need a relative-then-bare
fallback.

Related: [[census-grid-built-2026-08-12]], [[spine-connection-audit-2026-08-11]],
[[question-ladder-and-graph-truths-2026-08-12]].
