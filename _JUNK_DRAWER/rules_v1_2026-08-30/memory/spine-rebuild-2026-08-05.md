---
name: spine-rebuild-2026-08-05
description: "2026-08-05 ingestion sweep wired into the map — 31.8M entities, COMPANY_NO axis, registry key backfill; leads unchanged (no detectors on new populations)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e55a2997-4bb3-4830-9df9-66fd1639cd6d
  modified: 2026-08-06T04:10:14.698Z
---

2026-08-05 evening: the ingestion-sweep sources were wired into the connect map.
Entities 22.6M → 31.8M, edges 2,694 → 3,276, spine scope 80 → 128 tables, leads
unchanged at 17,307 (no detector touches the new populations — open red-lane call).

Non-obvious facts for future sessions:
- **The spine's gate is `connect/entity_index_specs.py` DISPLAY_SPECS, not
  SOURCE_REGISTRY** — an unlisted table is not in the spine regardless of keys.
  The established wiring chain: `scripts/backfill_join_keys_std.py` (measure +
  register keys, D20-guarded) → `scripts/gen_spine_specs.py --all` (live-verified
  spec block) → paste → `python -m connect all` → `connect leads --job all --run`.
- New key axis COMPANY_NO (UK company number, fixed-8) lives in connect/keys.py
  `EXACT_TOKEN_KEYS` (exact token-set match) because 'company' is a NAME token in
  the shared portal tagger — a pair rule there would mis-tag broadly. Any future
  connect-local key should use the same mechanism, and `key_tier()` not
  `KEY_TOKENS[k][0]` (three scripts crashed on that).
- `XC_EPA_CORPORATE_CROSSWALK` carries live FRS_ID+LEI+UEI — the EPA↔federal-money
  hard-ID bridge previously believed absent. Unwired as of 2026-08-05.
- HMDA-historic has RESPONDENT_ID not LEI; NPDB PUF is de-identified (no NPI);
  ATF FFL's license number is split across six USER_LIC_* columns.
- 11 orphan duplicate landing tables (6 documented + 5 ICIJ copies +
  FED_IRS_527_ORGS) are quarantined in fingerprint SKIP_TABLES pending Chris's
  manual DROP. See [[bridge-fuel-reality]], [[warehouse-data-traps]].
