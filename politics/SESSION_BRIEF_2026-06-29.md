# Session Brief — The Political Domain ("The Stat Line") — 2026-06-29

**Branch:** `politics-domain` (cut from `main`; NOT merged — left for Chris to review/merge).
**Status:** Phases 0–**3** complete — additively, each independently verified PASS on 4
adversarial dimensions. Both halves of the thesis are now live on one member: **money**
(raised per cycle, FEC-verified) AND **votes** (cast / missed / party unity, GovTrack-verified).

---

## PHASE 3 — THE VOTES LEG (latest)

**The "what they did" leg is live: votes cast / missed votes / party unity per member per
congress, keyed to the spine via icpsr.** Verified PASS on all 4 adversarial dimensions;
reconciled to GovTrack's 118th figures to ~0.1pp. **Fully additive — no Fix-B-style
exception this phase.**

### Landed (118th + 119th per-congress files — NOT the 700MB full history) + built
| Object | Rows |
|---|---|
| `LANDING.FED_VOTEVIEW_ROLLCALLS` (the votes MATRIX) | 945,523 |
| `LANDING.FED_VOTEVIEW_ROLLCALL_META` (roll-call metadata) | 3,364 |
| `MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES` (congress, chamber, rollnumber, icpsr) | 945,523 |
| `MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS` (congress, chamber, rollnumber) | 3,364 |
| `MARTS.POLITICS.POLITICS__MEMBER_VOTING_RECORD` (bioguide, congress) | 1,105 |

+1 registry row (`fed_voteview_rollcall_meta`, append-only). **Zero existing rows or vocab
touched.** dbt models + tests scaffolded. 635 members across the two congresses.

### The stat group — per (bioguide, congress)
- **votes_cast / missed_votes / missed_vote_pct** — objective. Denominator = eligible
  roll-calls (`cast_code <> 0`). 118th avg 4.14% missed.
- **party_unity_pct** — judgment-tier (CQ definition: member sides with own-party majority
  on roll-calls where the party majorities oppose). Major parties only (D/R). 118th avg 94.78%.

### Definitional choices (the labels)
- **Missed-vote denominator = eligible roll-calls** (`cast_code <> 0`). **Delegates**
  (AS/GU/PR/VI/MP/DC) carry ~538 eligible vs ~1235 for full members (they can't vote on final
  passage) — correct, not a bug.
- **President excluded** — Biden/Trump have recorded positions in the raw matrix (icpsr
  99913/99912) but aren't voting members → excluded from the record (478 votes, accounted for).
- **Party switchers collapsed** — a member with 2 icpsr in one congress (e.g. Manchin) = one row.
- **119th is PARTIAL** (`congress_partial=TRUE`) — mid-cycle counts; don't compare externally.

### Smoke test — PASS, reconciled to GovTrack
Missed-vote% vs GovTrack's 118th: Grijalva 39.19 vs 39.08, Jackson Lee 38.12 vs 38.0, Guthrie
0.08 vs 0.08. Audit independently confirmed AOC (3.08 vs 3.06) and MTG (5.75 vs 5.72) — missed
**counts match exactly**; the ~0.1pp residual is a named ~6-vote difference between Voteview's
roll-call set and the House Clerk's (GovTrack's source). Reconciled by definition, not decimals.

### Known scope notes
- `fed_voteview_rollcalls` registry row keeps its Phase-0 metadata (still says "Deferred",
  `JOIN_KEYS_STD=[]`) because additive-only forbids updating it; the matrix DID land into its
  table (lifecycle now 'landed'). A future authorized one-row tidy-up could set `['ICPSR']`.
- Party unity excludes independents from the stat by design (they still get votes/missed).

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
**Bills sponsored & cosponsored (legislative output) — the last clean objective box-score
stat.** From `unitedstates/congress` bulk or the congress.gov API (free data.gov key),
keyed on `bioguide` (no fuzzy matching, joins straight to the spine). Produces
`POLITICS__MEMBER_BILLS` (bioguide, congress): bills sponsored, cosponsored, enacted —
completing the core box score (ideology + money + votes + **bills**) before the fuzzy/heavy
legs. Same loader + grain pattern; scope to the 118th + 119th like the votes leg.

*(Then, the harder legs of the headline chain: FEC contribution detail
`fed_fec_bulk_contributions` (itcont) for money-IN-by-industry — ties the money leg to the
votes leg, but employer→industry is fuzzy + the file is huge (chunked load); STOCK Act PTRs
(member stock trades — PDF hell, high public interest); Senate LDA lobbying; the 2026
committee-master `cm26` refresh to close 2026 FEC linkage resolution; USAspending-by-district.)*

---

## How to resume / rebuild
```bash
# Phase 0/1 (skeleton: members + ideology)
python politics/registry/register_political_sources.py --apply   # idempotent, no-ops if present
python politics/loaders/build_skeleton.py                        # fetch + land + build
python politics/loaders/smoke_test.py                            # prove votes<->ideology+fec
# Phase 2 (money spine)
python politics/registry/promote_keys_and_fix_domain.py --apply  # Fix A (vocab) + Fix B (1 row)
python politics/loaders/build_money_spine.py                     # land FEC + build money marts
python politics/loaders/smoke_money.py                           # money raised vs FEC.gov
# Phase 3 (votes leg)
python politics/loaders/build_votes_leg.py                       # land Voteview 118+119 + voting marts
python politics/loaders/smoke_votes.py                           # missed-vote% vs GovTrack
```
Verification workflows (read-only): Phase 1 `wf_6b3b65a4-53d`, Phase 2 `wf_4222b021-528`,
Phase 3 `wf_1d283e03-750`. See `politics/README.md`.
