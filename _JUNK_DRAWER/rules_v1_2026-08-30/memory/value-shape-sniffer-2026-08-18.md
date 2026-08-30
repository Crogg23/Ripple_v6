---
name: value-shape-sniffer-2026-08-18
description: "Value-shape key sniffer run 2026-08-18 — 18 confirmed hidden-ID columns (FEC positional-header tables are the headline), zero hidden EINs, sequence-ID/Luhn/ORI traps documented"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3f26ad90-03f6-4705-a08b-735907f57e2a
  modified: 2026-08-19T01:41:28.642Z
---

Full run of the value-shape key sniffer (2026-08-18), report:
`reports/value_shape_findings_2026-08-18.md`. Scanned all 11,547 non-portal
landing columns (302 tables), ~$2-4 spend.

**OUTCOME (same evening, Chris approved):** all 18 wired (specs + table-scoped
graph keys), full spine rebuild ran clean — 33.31M entities / 178 sources, map
4,899 edges (STEEL 1,249→1,375), incremental re-seeded with --reseed, all 6
validation checks green. Bonus: a spine-vs-map visibility audit found 4 OLDER
map-blind spine columns (SAM exclusions UEI, SEC insider CIK, leadership-PAC
cmte, NCUA merging charter) — wired, and tests/test_spine_map_visibility.py
now pins "every spine key_col must be name- or table-resolvable" forever.
Correct post-rebuild order (from the 08-18 repair session, reused here):
spine -> re-profile changed tables (drop stale fingerprint entries, resume) ->
discover -> seed --reseed (plain seed silently keeps stale twins) -> validate.

**Confirmed 18 (as found, pre-wiring):**
- The 4 multi-cycle FEC history tables (FED_FEC_COMMITTEES / _CANDIDATES /
  _CAND_CMTE_LINKAGE / _PAC_SUMMARY) load with POSITIONAL headers (C1/C4/C10/
  C15) holding FEC committee/candidate IDs — invisible to all name detection,
  and they are BIGGER than their wired single-cycle twins (78k vs 20k
  committees). Consider header repair at load rather than wiring C1 into specs.
- Candidate↔committee crosswalk columns on wired tables: CAND_PCC, leadership-
  PAC FEC_CANDIDATE_ID, independent-expenditure spe_id, OTHER_ID.
- FED_CONGRESS_LEGISLATORS.FEC_IDS single-ID rows match live (830) — flatten
  build still right for multi-ID rows.
- EPA: ICIS enforcement-case facilities FACILITY_UIN = 100% FRS_ID (105k);
  ECHO SDWA_IDS = 99.3% of the whole live PWSID world (431k).
- CMS POS other-facilities: 4 parent/related/cross-ref columns are live CCNs.

**Negatives on the record (do not re-try):** zero hidden EIN/DUNS/LEI/UEI/DEA
columns exist; Senate LDA registrant IDs ≠ SEC CIKs (below chance); FBI ORI
IDs shape-collide with PWSID/NPDES (2-letter-state+7-digit) but are unrelated;
Open Payments RECORD_ID / FAERS ISR+DRUG_SEQ look NPI-shaped at 100% but only
~11% pass the NPI Luhn check digit (real NPI columns ≈100%) — the check-digit
test is the definitive kill for 10-digit sequence columns.

**Machinery lessons:** the confidence scorer's STEEL fast-path (matched>=25
skips collision math) passes junk for name-sniffed columns — apply the 5x
chance gate + mechanism review on top. The packet's ENTITY_MAP table does not
exist; the live Stage-2 reference is LIBRARY_META."CONNECT".SPINE_KEYSET_LIVE
(83.7M rows, 22 key families). Snowflake aggregate queries: compute normalized
expressions ONCE in an inner projection — recomputing inside each aggregate
was 6x slower. 182 columns still hold literal 'nan' text
(reports/value_shape_nan_trap_columns_2026-08-18.json).

Related: [[courtlistener-key-registration-2026-08-17]],
[[spine-connection-audit-2026-08-11]], [[bridge-fuel-reality]]
