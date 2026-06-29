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
    smoke_test.py                   # Phase 1 must-pass join proof (votes<->ideology+fec)
    build_money_spine.py            # Phase 2: land FEC cn/ccl/weball -> money marts
    smoke_money.py                  # Phase 2 must-pass proof (money raised vs FEC.gov)
    build_votes_leg.py              # Phase 3: land Voteview votes+rollcalls -> voting marts
    smoke_votes.py                  # Phase 3 must-pass proof (missed-vote% vs GovTrack)
  registry/
    promote_keys_and_fix_domain.py  # Phase 2 Fix A (vocab) + Fix B (fed_fec_bulk one-row)
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
python politics/loaders/smoke_test.py                            # votes <-> ideology + fec

# Phase 2 -- the money spine
python politics/registry/promote_keys_and_fix_domain.py --apply  # Fix A (vocab) + Fix B (1 row)
python politics/loaders/build_money_spine.py                     # land FEC + build money marts
python politics/loaders/smoke_money.py                           # money raised vs FEC.gov

# Phase 3 -- the votes leg
python politics/loaders/build_votes_leg.py                       # land Voteview 118+119 + build voting marts
python politics/loaders/build_votes_leg.py --skip-fetch          # rebuild marts only
python politics/loaders/smoke_votes.py                           # missed-vote% vs GovTrack
```

dbt models mirror the Python-built marts (canonical tables are Python-built into
`LIBRARY_*.POLITICS`). To run them: `dbt build --select marts.politics+` from
`library-onboarding/ripple_dbt` (needs the env creds + `dbt deps`).

## What's built

**Phase 1 — the member skeleton**
| Object | Rows | What |
|---|---|---|
| `LANDING.FED_CONGRESS_LEGISLATORS` | 12,847 | members + the ID crosswalk (CC0) |
| `LANDING.FED_VOTEVIEW_MEMBERS` | 51,061 | member-by-congress DW-NOMINATE ideology |
| `MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK` | 12,794 | **keystone** — 1/member, keyed bioguide, every alt ID |
| `MARTS.POLITICS.POLITICS__MEMBER_FEC_ID` | 1,715 | **bridge** — 1/(bioguide, fec_id); 1:many preserved |
| `MARTS.POLITICS.POLITICS__MEMBER_SPINE` | 12,794 | bioguide-keyed member + ideology |

**Phase 2 — the money spine** (FEC bulk cn/ccl/weball, cycles 2024 + 2026)
| Object | Rows | What |
|---|---|---|
| `LANDING.FED_FEC_BULK_CANDIDATES` | 17,900 | candidate master (cn) |
| `LANDING.FED_FEC_BULK_LINKAGES` | 16,327 | candidate↔committee linkage (ccl) |
| `LANDING.FED_FEC_BULK_SUMMARY` | 7,933 | financial summary (weball) — the only $ file |
| `MARTS.POLITICS.POLITICS__FEC_CANDIDATE` | 17,900 | candidate identity, keyed (cand_id, cycle) |
| `MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK` | 16,229 | the linkage bridge, keyed (cand_id, cmte_id, cycle) |
| `MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY` | 7,933 | dollars, keyed (cand_id, cycle); net-of-transfers cols |
| `MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED` | 1,050 | **the stat** — money raised/sitting member/cycle (533 members) |

The identity graph is now closed: `bioguide → fec_cand_id → CAND_ID (candidate) → linkage → CMTE_ID → committee master (fed_fec_bulk)`. **Money raised is net of inter-committee transfers** (`TTL_RECEIPTS − TRANS_FROM_AUTH`).

**Phase 3 — the votes leg** (Voteview per-congress files, 118th + 119th)
| Object | Rows | What |
|---|---|---|
| `LANDING.FED_VOTEVIEW_ROLLCALLS` | 945,523 | the member×rollcall VOTES MATRIX (cast codes) |
| `LANDING.FED_VOTEVIEW_ROLLCALL_META` | 3,364 | roll-call metadata (date, counts, question, bill) |
| `MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES` | 945,523 | cast matrix, keyed (congress, chamber, rollnumber, icpsr) |
| `MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS` | 3,364 | roll-call metadata, keyed (congress, chamber, rollnumber) |
| `MARTS.POLITICS.POLITICS__MEMBER_VOTING_RECORD` | 1,105 | **the stat** — votes cast / missed-vote% / party unity, per (bioguide, congress) |

Voting stats are **definition-bound** (reconciled to GovTrack's 118th figures to ~0.1pp, not penny-exact). `missed_vote_pct` denominator = eligible roll-calls (`cast_code <> 0`); `party_unity` = CQ definition (member sides with own-party majority on votes where party majorities oppose). The 119th is **partial** (in progress).

## The join spine — clean vs fuzzy (be honest)

- **Clean (build freely):** `bioguide` (politician PK) ↔ `icpsr` (Voteview) ↔
  `fec_id` (FEC candidate ID). Proven: a member's votes (Voteview) and money
  (FEC committees) meet on one key.
- **Fuzzy (a chain, not a join):** `bioguide → fec_id → FEC contribution employer
  (dirty free-text) → EIN`. The org-name→EIN step is a separate, low-confidence
  module — never treat FEC employer/industry as a clean key.

## Key-vocab (resolved in Phase 2)

The political join keys are now **first-class governed vocab**: Phase 2 Fix A
appended `BIOGUIDE`, `ICPSR`, `FEC_CAND_ID`, `FEC_CMTE_ID` to `FACET_VOCAB`
(FACET='JOIN_KEY', TIER='STEEL', append-only). New money-spine sources register
their `JOIN_KEYS_STD` against these governed keys. (Phase 1 member sources still
carry their keys in free-text `JOIN_KEYS` + a `KEY-FLAG` note — back-filling their
`JOIN_KEYS_STD` is an existing-row UPDATE, deferred as out-of-scope/additive-only.)

**Phase 2 Fix B (the one authorized non-additive change):** `fed_fec_bulk` (the FEC
committee master) was registered `UNCLASSIFIED`; a single one-row UPDATE corrected
it to `money_in_politics` with `JOIN_KEYS_STD=[FEC_CMTE_ID, FEC_CAND_ID]`. Logged in
the row's NOTES (`[Phase2 FixB …]`) and in the session brief.
