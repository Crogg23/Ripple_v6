# The Political Domain — "The Stat Line"

A namespaced, **additive-only** expansion of the Ripple Library: every
ethically-sourced public dataset about US politics and politicians, wired into the
existing identifier spine, laying the foundation for a politician **stat card**.

> **Isolation contract.** All new work lives here (`politics/`) + a dedicated
> `POLITICS` schema in `LIBRARY_STAGING` / `LIBRARY_MARTS` + dbt models under
> `ripple_dbt/models/{staging,marts}/politics/`. Nothing existing is modified.
> Registry writes are **append-only**. Built on branch `politics-domain`.

## What's here

```
politics/
  registry/
    political_sources.py            # the Phase 0 catalogue (data) + GAP buckets
    register_political_sources.py   # append-only loader (preview / --apply)
  loaders/
    build_skeleton.py               # Phase 1: fetch -> land -> staging -> marts
    smoke_test.py                   # the must-pass end-to-end join proof
  SESSION_BRIEF_2026-06-29.md       # session-end brief (start here next session)
```

Plus (additive) in the dbt project:
```
ripple_dbt/macros/generate_schema_name.sql               # safe schema routing (see note)
ripple_dbt/models/staging/politics/                      # 2 staging views + sources yml
ripple_dbt/models/marts/politics/                        # 3 marts + tests yml
```
And `outputs/politics_phase0_GAPS.md` (the state/local long-tail gap list).

## The build (run order)

```bash
# Phase 0 -- register the catalogue (append-only; preview first)
python politics/registry/register_political_sources.py            # preview
python politics/registry/register_political_sources.py --apply    # insert

# Phase 1 -- the skeleton (fetch + land + staging + marts)
python politics/loaders/build_skeleton.py
python politics/loaders/build_skeleton.py --skip-fetch            # rebuild marts only

# Prove the headline join end-to-end
python politics/loaders/smoke_test.py
```

dbt models mirror the Python-built marts (canonical tables are Python-built into
`LIBRARY_*.POLITICS`). To run them: `dbt build --select marts.politics+` from
`library-onboarding/ripple_dbt` (needs the env creds + `dbt deps`).

## What's built (Phase 1 skeleton)

| Object | Rows | What |
|---|---|---|
| `LIBRARY_RAW.LANDING.FED_CONGRESS_LEGISLATORS` | 12,847 | members + the ID crosswalk (CC0) |
| `LIBRARY_RAW.LANDING.FED_VOTEVIEW_MEMBERS` | 51,061 | member-by-congress DW-NOMINATE ideology |
| `LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK` | 12,794 | **keystone** — 1 row/member, keyed bioguide, every alt ID |
| `LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID` | 1,715 | **bridge** — 1 row/(bioguide, fec_id); 1:many preserved |
| `LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE` | 12,794 | bioguide-keyed member + DW-NOMINATE ideology |

## The join spine — clean vs fuzzy (be honest)

- **Clean (build freely):** `bioguide` (politician PK) ↔ `icpsr` (Voteview) ↔
  `fec_id` (FEC candidate ID). Proven: a member's votes (Voteview) and money
  (FEC committees) meet on one key.
- **Fuzzy (a chain, not a join):** `bioguide → fec_id → FEC contribution employer
  (dirty free-text) → EIN`. The org-name→EIN step is a separate, low-confidence
  module — never treat FEC employer/industry as a clean key.

## Key-vocab flag (open governance item)

The political join keys — `bioguide`, `icpsr`, `fec_id`, `govtrack` — are **not**
in `FACET_VOCAB`'s governed `JOIN_KEY` set (EIN/CIK/NPI/UEI/IMO/FIPS/…). Per
"flag, don't force" they are recorded in the free-text `JOIN_KEYS` column + a
`KEY-FLAG` note in `NOTES`; `JOIN_KEYS_STD` (the governed ARRAY) holds only
existing-vocab keys; `JOIN_KEY_TIER='STEEL'` is marked `PROVISIONAL=TRUE`.
**Recommended follow-up (append-only):** add `BIOGUIDE/ICPSR/FEC_ID` to
`FACET_VOCAB` (FACET='JOIN_KEY', TIER='STEEL') so the political keys become
first-class and `JOIN_KEYS_STD` can carry them.
