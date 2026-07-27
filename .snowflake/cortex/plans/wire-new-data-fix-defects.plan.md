# Plan: Wire New Data + Fix Defects

## Context

We just loaded several major new datasets (SEC 13F, CPSC NEISS, DEA ARCOS, Senate LDA). None are wired into the Connection Engine yet — they're sitting in the warehouse generating zero cross-database links. Meanwhile, we have 20 open defects (1 blocker, 6 high, 10 medium, 3 low) that need triage.

## Part A: Wire New Data into Connection Engine

### How the engine works (summary)

1. **`entity_index_specs.py`** declares which tables carry which hard keys and how to extract a name/address
2. **`spine.py`** reads those specs, scans the declared tables, and builds the entity graph (CONNECT_NODES → MATCH_PAIRS → ENTITY_MAP → ENTITY_GOLDEN)
3. **`keys.py`** defines how to detect and normalize each key type (NPI pad-10, EIN pad-9, CIK pad-10, etc.)
4. A table not in DISPLAY_SPECS can still participate via `KEYSET_LIVE` / `backfill_join_keys_std.py` — but to get golden-record names and proper authority ranking, it needs a spec.

### New tables to wire

| Table | Key | Column | What it adds |
|-------|-----|--------|-------------|
| `FED_SEC_13F_SUBMISSIONS` | CIK | `CIK` | 336K filing submissions linked to CIK entities. Bridges 13F holdings to the corporate spine. |
| `FED_DEA_ARCOS_FULL` | DEA_NO (new) | `REPORTER_DEA_NO` + `BUYER_DEA_NO` | 380M opioid transactions. Creates a brand-new key axis: DEA registrant numbers linking distributors to pharmacies/hospitals. |
| `FED_CPSC_NEISS` | None | N/A | No hard entity ID (product injury reports keyed by case number). Skip spine wiring — useful for aggregate analytics but not entity resolution. |
| `FED_SENATE_LDA_FILINGS` | Future | REGISTRANT_ID (numeric) | Senate-issued lobbying firm IDs. Not a standard hard key yet — needs name-bridge to EIN. Park for Phase 2. |

### DEA_NO: Adding a new key type

This requires changes in 3 places:
1. **`portal_recon/tag_portal_index.py`** — add `"DEA_NO": ("STEEL", {"dea"})` to `KEY_TOKENS`
2. **`connect/keys.py`** — add `"DEA_NO": ("pad", 9)` to `NORM_RULES` (DEA numbers are 9-character alphanumeric: 2 letters + 7 digits)
3. **`connect/entity_index_specs.py`** — add DISPLAY_SPECS entries for `FED_DEA_ARCOS_FULL`

DEA_NO normalization: alphanumeric, upper-cased, 9 characters. Format is like `AB1234567`. We'll use `("alnum_upper", 0)` since DEA numbers don't zero-pad — they're opaque 9-char identifiers.

### SEC 13F: Adding to existing CIK axis

Straightforward — CIK already exists as a key type. Just add a DISPLAY_SPECS entry for `FED_SEC_13F_SUBMISSIONS` with `key_col="CIK"`.

---

## Part B: Fix Defects (prioritized)

### BLOCKER (must fix first)

| ID | Title | Fix |
|----|-------|-----|
| `8c90a7a...` | Leaked ACCOUNTADMIN PATs still ACTIVE | **Requires Snowsight:** revoke THE_LIBRARY and Ripple_v6 PATs. Walk user through it. |

### HIGH (6 items)

| ID | Title | Fix type |
|----|-------|----------|
| `c049f02...` | resolve.py broken by NPPES column rename | **Code fix** — change double underscore to single in resolve.py:55 |
| `397182...` | OP-2022 mislogged (13.25M rows, ledger says error/0) | **SQL fix** — UPDATE the ingest run status + row count |
| `ead2969...` | IRS_EO_BMF is exact 2x duplicate of IRS_BMF | **SQL fix** — DROP or RENAME to LIBRARY_RAW.LANDING.ZZ_RETIRED_FED_IRS_EO_BMF |
| `e24840b...` | V_CONNECTIONS_CORE view doesn't exist | **Script run** — `python scripts/build_v_connections_core.py` |
| `88bea5c...` | build-state.md is hand-typed, not generated | **Script run** — `python scripts/gen_build_state.py` |
| `f3c8ffe...` | No scoped write PAT exists | **Requires Snowsight** — mint a PAT scoped to RIPPLE_TRANSFORM_RW |
| `d07b2d0...` | No ladder regression tests | **Defer** — requires Move 4 (test framework design), not a quick fix |
| `ba757e7...` | evidence.dev read lane is dark | **Requires** the READER token from Close the Loop — skip for now |

### MEDIUM (10 items — batch)

Most are monitoring/hygiene. We'll fix what we can programmatically:
- FHFA lifecycle misgrade → SQL UPDATE
- <=3 row sources → investigate, likely valid edge cases (CDC Wonder etc. return small tables)
- Missing staging views → generate with existing script
- Missing API keys → restore to .env
- V_CONNECTIONS_CORE → covered by high fix above

### LOW (3 items — defer)

- HTML CDN references (cosmetic)
- Stale overlay (regenerate after spine rebuild)
- 3 reading-room zero-cast views (trivial)

---

## Execution Order

1. **Fix the blocker first** (PAT revocation — needs Chris in Snowsight)
2. **Code fixes** (resolve.py column name, entity_index_specs additions, keys.py DEA_NO)
3. **SQL fixes** (OP-2022 status, IRS_EO_BMF quarantine, FHFA lifecycle)
4. **Run build scripts** (build_v_connections_core, gen_build_state)
5. **Rebuild spine** (picks up SEC 13F + DEA ARCOS)
6. **Verify** (re-run evidence SQL, close defects)

Steps 2-6 can run without blocking on step 1.
