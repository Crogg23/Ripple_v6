# Session Brief — The Political Domain ("The Stat Line") — 2026-06-29

**Branch:** `politics-domain` (cut from `main`; NOT merged — left for Chris to review/merge).
**Status:** Phases 0, 1, and **2** complete — additively, each independently verified PASS
on 4 adversarial dimensions. The vote↔money join is closed AND the first box-score stat
(money raised) is live and matches FEC.gov to the penny.

---

## PHASE 2 — THE MONEY SPINE (latest)

**The clean money spine is closed; the first box-score stat is live.** Verified PASS on
all 4 adversarial dimensions (additive safety, cycle-grain integrity, stat correctness +
FEC cross-check, vocab/registry).

### Two authorized precursor fixes
- **Fix A (append-only):** promoted `BIOGUIDE`, `ICPSR`, `FEC_CAND_ID`, `FEC_CMTE_ID` into
  `FACET_VOCAB` as STEEL (JOIN_KEY 21 → 25). Political keys are now governed first-class.
- **Fix B — the ONE authorized non-additive change (single one-row UPDATE):** `fed_fec_bulk`
  corrected `UNCLASSIFIED → money_in_politics`, `JOIN_KEYS_STD []→[FEC_CMTE_ID, FEC_CAND_ID]`,
  tier STEEL. Logged in the row's NOTES (`[Phase2 FixB 2026-06-29 …]`); `_LOADED_AT` unchanged
  (in-place edit, audit-verified). **No other existing row touched.**

### Landed (cycles 2024 + 2026, cycle grain preserved) + built
| Object | Rows |
|---|---|
| `LANDING.FED_FEC_BULK_CANDIDATES` (cn) | 17,900 |
| `LANDING.FED_FEC_BULK_LINKAGES` (ccl) | 16,327 |
| `LANDING.FED_FEC_BULK_SUMMARY` (weball — the only $ file) | 7,933 |
| `MARTS.POLITICS.POLITICS__FEC_CANDIDATE` (cand_id, cycle) | 17,900 |
| `MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK` (cand_id, cmte_id, cycle) | 16,229 |
| `MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY` (cand_id, cycle) | 7,933 |
| `MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED` (bioguide, cycle) | 1,050 |

+1 registry row (`fed_fec_bulk_summary`, append-only). dbt models + tests scaffolded.

### The stat — money raised per sitting member per cycle (533 members)
Computed **net of inter-committee transfers** (`TTL_RECEIPTS − TRANS_FROM_AUTH`), NOT a naive
`SUM(TTL_RECEIPTS)`. 741 member-figures are reduced by the netting (e.g. Scalise 2024 $14.7M
gross → $2.7M net). Identity graph closed: `bioguide → fec_cand_id → CAND_ID → linkage →
CMTE_ID → committee master (fed_fec_bulk)`. The join keys on (cand_id, cycle), so a member's
stale House ID never leaks into a Senate cycle.

### Smoke test — PASS, exact FEC match
Warren 2024: gross $9,039,537.78, **net $8,840,571.03**; OpenFEC published $9,039,537.78 —
match to the penny. Audit independently reproduced exact OpenFEC matches for Cruz ($68.9M net)
and Sanders ($8.2M, no transfers). 2024 spread: 519 members, min $64.7k / median $2.07M /
max $123.5M (Gallego AZ-Sen), 0 negative.

### Known scope notes
- Committee master `fed_fec_bulk` is a **2024 snapshot**, so 2026 linkage committee IDs
  resolve only ~57% (2024 resolves 98%). A 2026 committee-master load (`cm26`) closes that.
- Phase-1 member sources still carry their keys in free-text `JOIN_KEYS` (back-filling their
  `JOIN_KEYS_STD` with the now-governed keys is an existing-row UPDATE — deferred, additive-only).

---

## What got built

### Step 1 — current-state audit (verified, not assumed)
The handoff's infrastructure is all real: `LIBRARY_RAW/STAGING/MARTS/META/TOOLS`,
`SOURCE_REGISTRY` (1,610 rows pre-session), `INGEST_RUNS`, the **EIN/CIK STEEL-tier
spine** (EIN anchor `FED_CMS_NPPES` 9.6M; CIK anchor `FED_SEC_EDGAR_COMPANY_TICKERS`),
and the `FACET_VOCAB`-governed tiering. Two findings reshaped the plan:
- The catalog vocab already has political domains (`government_power`,
  `money_in_politics`, `elections_voting`, `spending_budget`) — used those, not UNCLASSIFIED.
- ~23 political sources were already scouted; **`fed_fec_bulk` already LANDED (20,938
  FEC committee-master rows)** — reused for the smoke test, not re-onboarded.

### Phase 0 — registry (append-only)
**+18 rows** inserted into `SOURCE_REGISTRY` (`INSERT … WHERE NOT EXISTS`), tagged
`DOMAIN_SOURCE='politics_domain'`: **12 sources** (congress-legislators, Voteview
members + rollcalls, FEC candidate/linkage/contribution bulk, House PTR + disbursements,
OGE, LegiScan, Open States, C-SPAN) + **6 GAP buckets** (`gap_*`, INCLUDE='N'). 4 of my
intended ids already existed and were **left untouched**. Long-tail enumeration:
`outputs/politics_phase0_GAPS.md`. Loader: `politics/registry/`.

### Phase 1 — the skeleton (land → stage → mart, all in a new `POLITICS` schema)
| Object | Rows | Role |
|---|---|---|
| `LANDING.FED_CONGRESS_LEGISLATORS` | 12,847 | members + ID crosswalk (CC0) |
| `LANDING.FED_VOTEVIEW_MEMBERS` | 51,061 | DW-NOMINATE ideology |
| `MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK` | 12,794 | **keystone**: 1/member, keyed bioguide, every alt ID (0 dup) |
| `MARTS.POLITICS.POLITICS__MEMBER_FEC_ID` | 1,715 | **bridge**: 1/(bioguide,fec_id), 1:many preserved |
| `MARTS.POLITICS.POLITICS__MEMBER_SPINE` | 12,794 | bioguide-keyed member + ideology (12,121 with a usable score) |

Plus 2 staging views, dbt models (`ripple_dbt/models/{staging,marts}/politics/`), and a
behavior-neutral `generate_schema_name` macro for schema isolation.

### Smoke test — PASS
Sanders (S000033): bioguide→icpsr 29147→DW-NOMINATE **−0.545**; bioguide→fec
`[H8VT01016, S4VT00033]`→committee **C00411330 "Friends of Bernie Sanders"**.
Independently reproduced for Warren/McConnell/Cruz/Schumer. **The vote↔money join works.**

---

## Registry state
- `SOURCE_REGISTRY`: 1,610 → **1,628** (append-only; 0 existing rows mutated).
- New landing tables: 2. New schemas: `LIBRARY_STAGING.POLITICS`, `LIBRARY_MARTS.POLITICS`.
- Query everything this session added: `WHERE DOMAIN_SOURCE='politics_domain'`.

## GAPS list (logged, not yet researched — next sessions)
6 buckets in the registry (`gap_*`, INCLUDE='N') + `outputs/politics_phase0_GAPS.md`:
state campaign-finance, state lobbying, state financial disclosure, state exec/judiciary,
local officials, non-incumbent candidates. **No unified national person key below
Congress — name-match territory, deliberately deferred.**

## Open governance item (flagged, not forced)
Political join keys (`bioguide/icpsr/fec_id/govtrack`) are **not** in `FACET_VOCAB`'s
governed JOIN_KEY set. They're recorded in free-text `JOIN_KEYS` + a `KEY-FLAG` note;
`JOIN_KEYS_STD` holds only governed keys; tier=STEEL marked PROVISIONAL. **Recommended
append-only follow-up:** add `BIOGUIDE/ICPSR/FEC_ID` (TIER='STEEL') to `FACET_VOCAB` so
the political keys become first-class.

---

## THE SINGLE NEXT ACTION
**Land the Voteview full roll-call matrix** (`fed_voteview_rollcalls`, already registered,
public-domain, no key — `HSall_votes.csv` + `HSall_rollcalls.csv`). It keys to the spine via
`icpsr` (already in `MEMBER_SPINE`) and produces the **second objective box-score stat: votes
cast / missed votes / party-unity** — pairing the "votes" leg with the "money" leg now live.
Same loader pattern as `build_money_spine.py`, with the same grain discipline: key marts on
(icpsr, congress, rollnumber); the votes file is large, so chunk or filter to recent congresses
first (exactly like the FEC cycle scoping).

*(Then: congress.gov official votes via bioguide (free data.gov key); FEC contribution detail
`fed_fec_bulk_contributions` for money-IN-by-industry — the headline chain's first leg; the
2026 committee master `cm26` to close 2026 linkage resolution; USAspending-by-district.)*

---

## How to resume / rebuild
```bash
# Phase 0/1
python politics/registry/register_political_sources.py --apply   # idempotent, no-ops if present
python politics/loaders/build_skeleton.py                        # fetch + land + build
python politics/loaders/smoke_test.py                            # prove votes<->ideology+fec
# Phase 2 (money spine)
python politics/registry/promote_keys_and_fix_domain.py --apply  # Fix A (vocab) + Fix B (1 row)
python politics/loaders/build_money_spine.py                     # land FEC + build money marts
python politics/loaders/smoke_money.py                           # money raised vs FEC.gov
```
Verification workflows (read-only): Phase 1 `wf_6b3b65a4-53d`, Phase 2 `wf_4222b021-528`.
See `politics/README.md`.
