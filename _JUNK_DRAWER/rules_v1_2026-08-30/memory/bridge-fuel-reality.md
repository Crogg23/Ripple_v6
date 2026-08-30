---
name: bridge-fuel-reality
description: "Masked ID columns are the recurring bridge trap — NPPES EIN/TIN and FCC ULS EIN are 100% populated but carry ~1 distinct value; always COUNT(DISTINCT) before trusting an ID column as fuel"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4e8ea272-9dad-4a28-8606-149ba3ffb5e0
  modified: 2026-07-23T14:45:06.299Z
---

Verified live 2026-06-24. The build-state framed the bridge layer as "fuel-gated: the 1.9M-pair NPPES NPI↔EIN crosswalk fires zero because non-NPPES EINs don't overlap it." **That framing is wrong.** The real cause is deeper:

- `FED_CMS_NPPES.EMPLOYER_IDENTIFICATION_NUMBER__EIN` = **`<UNAVAIL>` / '' only (2 distinct over 9.6M rows)**. CMS masks EIN in the public NPPES dissemination file. `PARENT_ORGANIZATION_TIN` is masked the same way. So **NPPES carries NO usable per-provider EIN** — the "NPI↔EIN crosswalk" never existed.
- `FED_CMS_NURSING_HOME` has `NPI` + `PROVIDER_NUMBER` columns but both are **empty** (1 distinct = ''). Only its CCN is live.
- The ONLY real entity crosswalks we hold are two tiny LA County portal samples (CCN↔NPI, ≤998 distinct). They drive all 14 current BRIDGE edges.

**Implication:** a public NPI↔EIN *hard* crosswalk mostly doesn't exist (EIN is PII-masked in provider files) — that linkage is really an entity-resolution (name+place) job for the corroboration layer. The achievable, high-value bridge is **CCN↔NPI** (a national CMS provider crosswalk would connect NURSING_HOME/HCRIS CCNs to NPPES + banned-provider LEIE NPIs — directly serving "banned but still operating", see [[connection-lenses]]).

**THE GENERAL RULE (2nd instance confirmed 2026-07-23, key-coverage hunt).** Masking is not an NPPES quirk — it is the
default failure mode of public ID columns, and it is invisible to any column-name scan (including the portal-index
tagger and `INFORMATION_SCHEMA` sweeps). Second confirmed case: `FED_FCC_LICENSING.EIN` is **100% non-null across
1,689,338 rows and has exactly 1 distinct value — the empty string** (FCC redacts EIN in public ULS files). It reads
as a perfect telecom→EIN-spine bridge in a column listing and delivers nothing. Same table's `FRN` is genuinely real
(1,198,926 distinct), so the trap is per-column, not per-table.

**Before costing or building on any newly found ID column: `COUNT(*)`, `COUNT(col)`, `COUNT(DISTINCT col)`.**
"Not null" is not the test — distinct-value count is. Cheap query, saves a build cycle.

**How a bridge fires:** a source must carry TWO hard IDs (NPI/EIN/CCN/CIK/DUNS/UEI/LEI/IMO/MMSI) with many distinct UNMASKED values in the same rows; `_valuable()` requires BOTH ends be HARD (no ZIP/NAICS); `FANOUT_MAX=40` kills any value mapping to >40 targets (this is what also kills the masked 1-distinct EIN). So fuel must be unmasked + high-cardinality, and its values must overlap two different tables we already hold. Serves [[platform-vision]].

**RESOLVED 2026-06-24 — bridge ACTIVATED.** Poured `FED_CMS_FACILITY_AFFILIATION` (CMS Doctors & Clinicians, dataset `27ea-46a8`) — a real, current, 2.24M-row CCN↔NPI crosswalk (938k NPIs × 41k CCNs, 0 masked) + 7 CCN facility sets (POS + Care Compare). Bridge edges 14 → 59; every CMS facility type now reaches NPPES (9.6M providers) on CCN→NPI (HOME_HEALTH↔NPPES 60,526 matched, NURSING_HOME 35,813, etc.). Loaded LLM-free via `scripts/bridge_fuel_load.py` (ANTHROPIC_API_KEY is missing from `.env`). Two gotchas learned: (1) the tagger only detects the literal `ccn`/`npi` token, so the loader **aliases** verified id columns per-source; (2) facility↔LEIE "banned but operating" bridges don't surface as graph edges — fanout-gated (big hospitals >40 NPIs) + deduped behind a weak direct ZIP edge — so that flagship lens lives in a targeted crosswalk×LEIE query (38 affiliations of 11 excluded providers, name-corroborated). EIN bridges still blocked (no public NPI↔EIN crosswalk). See [[connection-lenses]] — the bad-actor lens is now computable.
