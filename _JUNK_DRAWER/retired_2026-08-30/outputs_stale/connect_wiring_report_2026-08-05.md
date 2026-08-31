# Connect wiring report — 2026-08-05 ingestion sweep → map

Session goal: wire the ~40 sources landed in the 2026-08-05 ingestion sweep into
the entity spine / connection map using the established pipeline. Everything below
was measured live, never assumed.

## Headline numbers (before → after)

| Metric | Before | After | Delta |
|---|---|---|---|
| Entities (ENTITY_MAP) | 22,623,285 | **31,851,428** | **+9,228,143** |
| Nodes (CONNECT_NODES) | 37,223,830 | 69,404,285 | +32,180,455 |
| Match pairs (MATCH_PAIRS) | 31,104,982 | 106,218,114 | +75,113,132 |
| Map edges (CONNECT_EDGES) | 2,694 | 3,276 | +582 (5,406 flukes gated) |
| Leads (LEADS) | 17,307 | 17,307 | 0 — see below |
| Tables in spine scope | 80 | 128 | +48 |
| Key axes | 15 | 16 | +COMPANY_NO |

Entities by type after: organization 16.19M · provider 9.61M · facility 6.01M ·
person 39.3K · vessel 8.7K. Multi-source entities: 15,468,968.

## What was done (in order)

1. **Registry key backfill** — `scripts/backfill_join_keys_std.py --apply`:
   142 sources gained MEASURED join keys (94 STEEL top-tier). D20-guarded
   (provisional rows only), registry snapshot
   `_SOURCE_REGISTRY_BAK_JOINKEYS_20260805_193951` + rollback SQL in outputs/.
   (Fixed 3 crash sites in the script that indexed `KEY_TOKENS` directly and
   died on the new connect-local key.)
2. **New COMPANY_NO key axis** (connect/keys.py) — UK Companies House company
   number, the PSC beneficial-ownership bridge. Implemented as a connect-local
   EXACT-token-set rule so the shared portal tagger is untouched (a pair-rule
   there would mis-tag any table having both a company column and a *_NUMBER
   column). Verified live before wiring: both landing sides uniformly 8-char
   ('SC316600', '00000133'); normalizer `fixed 8`; only two columns in the whole
   warehouse tokenize to {company, number} exactly.
3. **Spine wave 3** — `scripts/gen_spine_specs.py --all` → 46 verified specs
   pasted into DISPLAY_SPECS (evidence: outputs/spine_wiring_evidence.csv;
   15 rejects in _rejects.csv). Excluded FED_SEC_EDGAR / FED_US_SEC_EDGAR per
   the 2026-07-28 "stale test loads, not wired" ruling. Plus hand-written,
   live-verified specs for UK_COMPANIES_HOUSE_PSC and INT_UK_COMPANIES_HOUSE
   (PSC deliberately contributes NO org name — its NAME column is the OWNER,
   not the company; wiring it as org would label companies with their owners'
   names in the golden record).
4. **Orphan quarantine** — the 11 unregistered duplicate twin tables (the 6
   documented + 5 more found live: all ICIJ_OFFSHORE_LEAKS_* copies and
   FED_IRS_527_ORGS) added to fingerprint SKIP_TABLES so the map never counts
   a source twice. They still need Chris's manual DROP.
5. **Full rebuild** — fingerprint (resume: 98 new tables; INT_UK_COMPANIES_HOUSE
   evicted to pick up COMPANY_NO) → discover → spine → explore. Clean exit;
   incremental state self-synced (SPINE_KEYSET_LIVE + CONNECT_WATERMARK).
   Log: outputs/connect_rebuild_20260805.log.
6. **Leads** — `python -m connect leads --job all --run`: all 8 jobs re-ran,
   totals unchanged (773/236/53/12/10/4/3 + OSHA cohort). **Zero new leads is
   the honest result**: every existing detector is keyed on NPI/UEI/IMO/EIN
   intersections that tonight's data doesn't feed; the new populations
   (UK companies, EPA facility suites, IRS 527 orgs) have no detectors yet —
   that's a design decision for Chris, not a bug.

## Verification (trap checks)

- **COMPANY_NO stress**: 2,335,951 entities span BOTH UK tables — exactly equal
  to the pre-build raw-join probe (independent check). Zero all-zero/degenerate
  values. Single namespace by construction (only the two UK CH tables carry it).
- **Grain**: CH registry contributes 5,734,779 distinct (1 row per company —
  it IS the registry); PSC 5,107,915 distinct from 7M rows.
- **Masked-key trap**: every wired key measured with COUNT(DISTINCT) + value
  sample via the spine's own normalizer (gen_spine_specs discipline). Rejected
  e.g. FED_CMS_MAIN NPI (normalizes to NULL on every row — sentinel).
- **Orphans**: confirmed absent from CONNECT_NODES after rebuild.
- **ICE person-level / sex-offender data**: confirmed NOT in the warehouse
  (registry log's "building now" note never landed); nothing wired.
- **Name-match false positives**: name edges still gated at 300k rows and
  PROBABILISTIC tier; no change to that discipline tonight.

## Notable finds along the way

- **`XC_EPA_CORPORATE_CROSSWALK` measures live FRS_ID + LEI + UEI** — this is
  the EPA↔contracts hard-ID bridge the 2026-07-31 "MAPPED" entry proved didn't
  exist in loaded sources. It exists now. Wiring it into the spine (it's not
  modeled yet, so gen_spine_specs skipped it) would connect EPA enforcement to
  federal money by hard ID for the first time.
- **HMDA-historic carries RESPONDENT_ID, not LEI** (LEI is the modern vintage
  only) — the registry's LEI claim for `fed_cfpb_hmda` is true only of the
  already-wired table.
- **NPDB PUF is de-identified** — no NPI at all; connects at practitioner level
  by nothing. Registry claim of NPI is wrong for this product.
- **ATF FFL** has no single license-number column (six USER_LIC_* components);
  no other source carries FFL numbers, so composite-key wiring would bridge
  nothing today. It connects via name/ZIP (77K rows, under the name cap).
- The pre-existing incremental-vs-backstop test failure earlier tonight was the
  stale keyset twins (56M unseen values from the sweep) — resolved by this
  full rebuild's self-sync.

## Files changed

- `connect/keys.py` — EXACT_TOKEN_KEYS + COMPANY_NO norm rule + key_tier()
- `connect/entity_index_specs.py` — +48 specs, COMPANY_NO entity type
- `connect/fingerprint.py` — SKIP_TABLES orphan quarantine
- `scripts/backfill_join_keys_std.py` — key_tier() at 3 crash sites
- `outputs/` — evidence CSVs, rebuild/leads logs, this report
