# Session Brief — The Political Domain ("The Stat Line") — 2026-06-29

**Branch:** `politics-domain` (cut from `main`; NOT merged — left for Chris to review/merge).
**Status:** Definition-of-done met. Phase 0 + Phase 1 skeleton built, additively, and
independently verified PASS on all 4 adversarial dimensions.

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
**Phase 2, source #1 — land FEC candidate master + linkage bulk** (`fed_fec_bulk_candidates`
cn.zip + `fed_fec_bulk_linkages` ccl.zip, both registered, public-domain, no key). That
completes the clean money spine: member → fec_cand_id → (ccl) → committee → (already-landed
`fed_fec_bulk`) — turning the 1,715-row bridge into a full candidate→committee money graph,
and unlocking the first objective "money raised" box-score stat. Loader pattern is identical
to `build_skeleton.py` (`land()` helper reuses the shared `ingest` path).

*(Then: congress.gov votes via bioguide; Voteview full rollcall matrix; USAspending-by-district.)*

---

## How to resume / rebuild
```bash
python politics/registry/register_political_sources.py --apply   # idempotent, no-ops if present
python politics/loaders/build_skeleton.py                        # fetch + land + build
python politics/loaders/build_skeleton.py --skip-fetch           # rebuild marts only
python politics/loaders/smoke_test.py                            # prove the join
```
Verification workflow (read-only, re-runnable): `wf_6b3b65a4-53d`. See `politics/README.md`.
