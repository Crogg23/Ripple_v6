# Compass handoff — Phase 0 receipts, 2026-09-23

Read-only. Nothing in the warehouse changed.

## Where the 659-table catalog comes from

- Built 2026-09-23 03:07 UTC by two inline heredoc scripts in session `e8dc9438`.
  Neither script was saved to the repo. Only the outputs were committed, in 2d7cc8d2:
  `outputs/catalog/raw.json`, `outputs/catalog/catalog.json`, `outputs/catalog/index.html`.
- Script 1 → `raw.json`: `LIBRARY_MARTS.information_schema.columns` + `.tables`,
  skipping schemas `INFORMATION_SCHEMA, TIMELINE, _RESTORE_20260907, REVIEW, PUBLIC`.
- Script 2 → `catalog.json`: 17 regexes on the column NAME, first match wins.
  No values are read. Grades strong/medium/weak are hand-typed in that list.

Offending rules, verbatim:

```
ORG_NAME  weak    NAME$|^NAME_|SPONSOR_NAME|ISSUER_NAME|FACILITY
FEC_ID    strong  ^CMTE_ID$|^CAND_ID$|^SUB_ID$
FRS/EPA   strong  REGISTRY_ID|^FRS_ID|NPDES|^EPA_
COUNTY_FIPS medium FIPS
```

- `NAME$` catches DRUG_NAME, PRODUCT_NAME, any *_NAME.
- `FACILITY` catches any column containing the word.
- `SUB_ID` is FEC's per-row record number, not a committee or candidate.
- `FIPS` catches state FIPS and place FIPS as county.

## What the 659 are

```
LIBRARY_MARTS live, 2026-09-23     base tables  views
in catalog                              637       22
TIMELINE, skipped                        36      405
_RESTORE_20260907, skipped               11        0
PUBLIC, skipped                          14        0
REVIEW, skipped                           2        1
total                                   700      428
```

The 22 "zero-row" tables are VIEWS. information_schema gives views a NULL row_count.
Confirmed live: all 22 are TABLE_TYPE = 'VIEW'. Real row counts unknown until counted.

## Wider warehouse, live

```
database          base tables   views   with a table comment
LIBRARY_RAW            2,354        2     678
LIBRARY_STAGING           34    3,491       0
LIBRARY_MARTS            700      428      44
LIBRARY_META              63       19      15
LIBRARY_TOOLS              0        0       —
THE_LIBRARY                0      252     252
```

The ~3,197 figure in the handoff does not match any live sum. Treat it as stale.

## Where key tags live — three places, not one

1. `catalog.json` regexes above. Unsaved, name-only, strong/medium/weak.
2. `portal_recon/tag_portal_index.py` — `TIER_ORDER = STEEL, STRONG, GEO, PROBABILISTIC`,
   token-based, with KEY_EXCLUDE and PAIR_RULES. `connect/keys.py` imports it
   and adds EXACT_TOKEN_KEYS. This is the platform's real tagger.
3. `LIBRARY_META.REGISTRY.COLUMN_CATALOG.DETECTED_KEY / KEY_TIER` — 751 columns, 25 tables.
   Tiers: STEEL 30, STRONG 2, GEO 13, PROBABILISTIC 80, none 626.

Also present: `LIBRARY_META.AUDIT.KEY_VALIDATION` 115 rows, `AUDIT.COLUMN_HEALTH` 8,613 rows,
`REGISTRY.COLUMN_TRUST` 174 rows. Not yet read for content.

## Existing plain-English text

```
place                                         covers                         status
dbt mart YAML description:                    679 mart .sql files            written, not pushed
  persist_docs                                not set in dbt_project.yml     → 0 of 20,868 mart column comments
LIBRARY_MARTS table COMMENT                   31 of 700 base tables          sparse
REGISTRY.FRIENDLY_LAYER.ONE_LINER             249 objects, 93 mart           table-level
REGISTRY.COLUMN_CATALOG.PLAIN_GLOSS           751 cols, 25 tables            673 heuristic, 78 curated
THE_LIBRARY view comments                     252 views, 918 of 10,104 cols  table-level mostly
LIBRARY_RAW table COMMENT                     678 of 2,356                   landing layer
```

ARCOS mart YAML: 3 `description:` lines. TRANSACTION_CODE has a not_null test, no description.

## Conflicts between the handoff and CLAUDE.md

- Handoff: "no tables unless he asks". CLAUDE.md: tables when comparable. CLAUDE.md wins.
- Handoff's gold plain.json says "Added by you"; its own style rule says
  "Added by your pipeline, not the source". Pick one before Phase 3.
- Handoff points at `reference/`. That folder does not exist in the repo.
  The three reference files exist only as chat attachments.
