---
name: exhaustive-id-sweep-2026-08-05
description: "2026-08-05 25-domain exhaustive ID-standard sweep: 747 real candidate join keys catalogued; MSHA controller/violator/contractor bridge and DOL Form5500 SPONS_DFE_PN verified live and unused; whole-domain gaps confirmed (energy, agriculture, insurance, SSA)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3a7d2947-f999-4d94-a06a-6e48f9099917
  modified: 2026-08-05T15:00:09.136Z
---

Ran a 25-domain, 50-agent exhaustive sweep (`outputs/exhaustive_id_sweep_synthesis_2026-08-05.md`,
full detail in `outputs/full_id_standard_catalog_2026-08-05.md`) answering "what identifier
standards could Ripple join on that it doesn't know about yet" — a much deeper follow-up to
[[coverage-sweep-2026-08-05]]'s external survey. 756 raw candidates → 747 real (9 were
classification codes wrongly tiered as entity keys, same shape as banned NAICS/SIC).

**Verified live with my own SQL (not just agent claims), ready to wire with zero new data:**
- `FED_MSHA_MINES/VIOLATIONS/ACCIDENTS` already carry `CONTROLLER_ID`/`VIOLATOR_ID`/`OPERATOR_ID`
  (93-99% filled) and `CONTRACTOR_ID` (only 6-10% filled, thin) — a parent-company/contractor
  bridge nobody has wired up. Values are quote-wrapped like the known MINE_ID trap. 4,686
  distinct controllers cross-match between accidents and mines in a real join.
- `FED_DOL_FORM5500.PLAN_NUM` is a **new trap — 0% filled**, despite looking like the obvious
  ERISA plan-number column. The real one is `SPONS_DFE_PN` (100% filled, 266 distinct, 3-digit).
- `FED_DOL_OFLC.CASE_NUMBER` is 100% filled, 664,616 distinct — real H-1B/PERM/H-2A case key.
- `INTL_OPENSANCTIONS` (71,011 rows, landed 2026-06-26) already blends OFAC+UN+EU+UK+PEP lists —
  confirms Ripple's sanctions coverage is NOT US-only, contradicting what one research agent
  assumed from the agency list alone.

**Confirmed whole-domain gaps** (zero data, not just under-indexed): FERC/EIA/NRC/PHMSA
(energy), USDA/FSIS/APHIS (agriculture), NAIC (insurance), Social Security Administration.

**Process note:** my own first filtering pass had a bug — naive substring match on "atc"
wrongly excluded "FATCA GIIN" and "Retraction Watch" (matched inside "f-ATC-a" and "w-ATC-h").
Caught by spot-checking before the report shipped. Lesson: word-boundary regex, not `in`
substring checks, when filtering candidate name lists.

Full catalog has 74 near-term acquisition candidates (STEEL tier, free bulk) and 40
"likely already hiding in existing tables" candidates (agent-judged, unverified except the
four above) — see [[warehouse-data-traps]] for the trap-column discipline this all depends on.
