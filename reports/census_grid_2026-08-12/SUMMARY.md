# The Census Grid — every thing in the warehouse × every way to look at it

> **FILLED 2026-08-17:** measured row counts, date ranges, key reality and dup
> ratios now attached to every mart model — see `fill/FILL_SUMMARY.md`.

*Built 2026-08-12 from table metadata only (dbt manifest + model SQL + source
descriptions). Zero warehouse queries. Every number below is reproducible by
running `scripts/census/extract_models.py` then `scripts/census/build_grid.py`.*

## The one-screen picture

- **1765 modeled tables** described in one language: noun / event / link / code.
- **38 families** of things, **278 distinct things**, **52,235 grid cells** (thing × applicable display slot).
- **30,509 cells are ready to fill** (the columns exist); **21,726 are structural holes** (the column doesn't exist — visible, not dropped).
- **9 models remain unmapped** and **235 are shape-guessed only** — listed at the bottom, never silently dropped.
- **4,357 branches parked** across 10 branch types — the tally below is the build roadmap, by vote count.

## The parking-lot tally (the second deliverable — ranked by votes)

| votes | families touched | branch |
|---:|---:|---|
| 1,426 | 33 | per person served |
| 658 | 21 | was there an inspection first (real lineage) |
| 658 | 21 | did anyone get hurt (harm join) |
| 616 | 37 | any trend over time |
| 615 | 40 | join to the entity spine |
| 160 | 16 | assessed vs actually collected |
| 110 | 12 | events per noun via hard ID |
| 56 | 1 | row-level version of this aggregate |
| 46 | 12 | multi-year trending |
| 12 | 7 | full column inventory |

## Families (grid rows, one line each)

| family | class | models | cells ready | cells hole |
|---|---|---:|---:|---:|
| place | noun | 453 | 6,226 | 6,911 |
| unresolved | event | 235 | 4,374 | 2,644 |
| facility | noun | 142 | 2,710 | 1,408 |
| organization | noun | 131 | 2,274 | 1,525 |
| measurement | event | 82 | 1,276 | 1,184 |
| filing | event+noun | 73 | 1,618 | 791 |
| aggregate | aggregate | 56 | 847 | 609 |
| code | code | 47 | 711 | 699 |
| case | event+noun | 44 | 996 | 456 |
| provider | noun | 40 | 743 | 417 |
| action | event | 38 | 677 | 463 |
| role | link | 30 | 452 | 418 |
| contribution | event | 23 | 557 | 133 |
| registration | event+noun | 23 | 578 | 181 |
| person | noun | 22 | 330 | 308 |
| program | noun | 21 | 397 | 212 |
| award | event+noun | 20 | 534 | 126 |
| accident | event | 19 | 321 | 249 |
| enforcement | event | 18 | 418 | 122 |
| dataset | noun | 17 | 270 | 223 |
| trade | event | 17 | 414 | 96 |
| payment | event | 17 | 345 | 165 |
| product | noun | 16 | 297 | 167 |
| crosswalk | link | 16 | 232 | 232 |
| asset | noun | 15 | 271 | 164 |
| registry | noun | 15 | 253 | 182 |
| violation | event | 14 | 294 | 126 |
| document | noun | 14 | 193 | 213 |
| inspection | event | 13 | 287 | 103 |
| membership | link | 12 | 200 | 148 |
| loan | event+noun | 11 | 280 | 83 |
| ownership | link | 11 | 164 | 155 |
| change | event | 11 | 211 | 119 |
| recall | event+noun | 9 | 191 | 106 |
| vote | event | 9 | 130 | 140 |
| instrument | noun | 8 | 106 | 126 |
| complaint | event | 6 | 114 | 66 |
| post | event | 5 | 88 | 62 |
| natural_event | event | 3 | 53 | 37 |

## Source bookkeeping does not reconcile (a census finding in itself)

- Onboarding log: **774 sources attempted** — 88 complete, 684 failed, 2 waiting on API keys.
- Yet **1141 source directories are staged** and live in dbt, and **1329 raw landing tables** exist.
- These three numbers cannot currently be joined by any shared key. There is no
  single authoritative list of what the warehouse holds. PARKED: source-registry
  reconciliation (needs-crosswalk).

## The honest residue (visible holes, per the ratchet)

- 9 unmapped models: politics__xc_jcs_coa, stg_fed_eia861_balancing_authority__all, stg_portal_cka_houston_open_dat_09fd7e454a__records, stg_portal_cka_indiana_data_hub_7747efe139__records, stg_portal_cka_israel_national_44788840fc__records, stg_portal_cka_tampa_open_data_6c25ea91d4__records, stg_portal_cka_western_pennsylv_769bebae41__records, stg_portal_cka_wprdc_allegheny_4597fbdfe3__records, stg_tx_lobby__transportation
- 235 models classified by column shape only (family 'unresolved').
- 12 models whose column lists could not be fully recovered from SQL (flagged in table_map.csv).
- 674 models with no declared grain — their 'one row = one what' is unstated.

## What each file is

| file | what it holds |
|---|---|
| `things.csv` | the bottom-up thing-list (family > thing > model count) |
| `table_map.csv` | every model → family/class, with the evidence for the call |
| `grid_families.csv` | the one-page grid: family × slot × ready/hole counts |
| `grid_things.csv` | the full machine grid: model × slot × status |
| `slots.csv` | the display-slot vocabulary and what each requires |
| `parking_lot.csv` | every parked branch, one line each |
| `parking_tally.csv` | the ranked tally — the build roadmap |
| `sources_census.csv` | the onboarding log, every attempted source with status |
