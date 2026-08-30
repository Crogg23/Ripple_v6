---
name: question-ladder-and-graph-truths-2026-08-12
description: "The question ladder deliverable exists (reports/question_ladder_2026-08-12.md, 1,832 questions, post-audit); plus durable graph facts learned building it — CORROBORATED tier is name@zip not hard-ID, only STEEL (14 key families) is SOLID, politics has zero verified graph joins"
metadata: 
  node_type: memory
  type: project
  originSessionId: fa91fb37-1bc3-4fe2-b17f-a27c3de8389f
  modified: 2026-08-12T15:49:38.607Z
---

**The question ladder shipped 2026-08-12:** `reports/question_ladder_2026-08-12.md`
(~1 MB, uncommitted at close). 1,832 deduplicated questions tiered by source
count (1,172 / 475 / 150 / 35), each tier-2+ entry carrying join basis,
SOLID/FUZZY grade, harm line, trust caveat; plus a 40-item "unlock list", 19
structurally-dark sources, 16 broken-model bugs. Built by an 11-agent recon +
8-agent merge + 2-critic audit; ~21 duplicates removed and all counts
machine-recounted post-audit. Chris's tiered replacement for the orphaned
2,873-row viz-brainstorm CSV.

**Durable graph truths found doing it (verify against `outputs/connect_graph.json`):**

- **The graph's CORROBORATED tier (2,606 of 4,538 edges) is NAME@ZIP / NAME@FIPS
  name-and-address matching, NOT hard IDs.** Any doc or prompt that treats
  CORROBORATED as hard-ID inflates solidity. Only STEEL (1,121 edges) is hard-ID.
- **The 14 STEEL key families:** EIN, NPI, FRS_ID, CIK, CCN, PWSID, LEI,
  FEC_CAND_ID, UEI, BIOGUIDE, FEC_CMTE_ID, DUNS, ICPSR, MINE_ID. Nothing else —
  not FIPS, not NPDES_ID (hard permit ID but never promoted), not CourtListener
  internal IDs.
- **Politics runs entirely off the verified graph:** FEC↔Congress families have
  no cross-family edge; one check of the FEC candidate-ID column already in the
  legislator roster would flip the money-to-votes lane to SOLID.
- **Harm-heaviest sources are graph dark matter (zero edges):** ARCOS (178M
  rows), sanctions lists, ICIJ, ICE detention, MAUDE, NPDB, NHTSA, all
  CourtListener dockets (71.7M).
- **527↔exempt-org EIN edges exist and are STEEL** (tiny match rates — the tiny
  dual-status overlap is itself a finding); measured directly this session.

Related: [[spine-connection-audit-2026-08-11]], [[bridge-fuel-reality]].
