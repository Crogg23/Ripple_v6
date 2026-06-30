# Session Brief — The Political Domain ("The Stat Line") — 2026-06-29

**Branch:** `politics-domain` (cut from `main`; NOT merged — left for Chris to review/merge).
**Status:** Phases 0–**4** complete — additively, each independently verified PASS on 4
adversarial dimensions. **The clean box score is now whole on one member: ideology + money
+ votes + bills**, all bioguide-keyed. Bills was the last leg with no fuzzy matching.

---

## PHASE 4 — THE BILLS LEG (latest)

**The last clean objective leg is live: bills sponsored / cosponsored / enacted per member
per congress, keyed bioguide → spine directly (sponsor AND cosponsor carry bioguide).**
This **completes the core box score (ideology + money + votes + bills).** Verified PASS on
all 4 adversarial dimensions. Fully additive — 0 existing rows/objects touched.

### Landed (GovInfo BILLSTATUS XML, 118th + 119th, all 8 bill types) + built
| Object | Rows |
|---|---|
| `LANDING.FED_GOVINFO_BILLSTATUS` (one row per bill) | 36,465 |
| `LANDING.FED_GOVINFO_BILL_COSPONSORS` (one row per bill × cosponsor, raw) | 367,742 |
| `MARTS.POLITICS.POLITICS__BILLS` (congress, bill_type, bill_number) | 36,465 |
| `MARTS.POLITICS.POLITICS__BILL_COSPONSORS` (…, cosponsor_bioguide) | 367,735 |
| `MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD` (bioguide, congress) | 1,104 |

**+2 registry rows** (`fed_govinfo_billstatus`, `fed_govinfo_bill_cosponsors`, append-only,
both `JOIN_KEYS_STD=[BIOGUIDE]` STEEL non-provisional). 635 members across the two congresses.
dbt staging + marts + tests scaffolded. **New parse pattern:** BILLSTATUS is **XML** (first XML
loader) — `lxml`/`xml.etree`, per-(congress, bill_type) bulk ZIP, one XML file per bill.

### The stat group — per (bioguide, congress) — headline-trap-proof by construction
- **bills_sponsored** — total; **never shown alone** (a raw count rewards spam — see Biggs below).
- **bills_sponsored_substantive vs resolutions_sponsored** — the mandatory type split
  (HR/S/HJRES/SJRES vs HRES/SRES/HCONRES/SCONRES).
- **bills_enacted** — sponsored bills with a `<laws>` element (became Public Law). 118th = 274 laws.
- **enacted_rate** = bills_enacted / **bills_sponsored_substantive** (law-eligible denominator —
  resolutions excluded; **NULL, not 0**, for the 12 resolution-only sponsors).
- **advanced_past_committee_count (+ advanced_rate)** — see the documented rule below.
- **cosponsored_count** — **separate** figure, withdrawn excluded; never summed into "bills".

### Definitional choices (the labels)
- **`became_law` = the `<laws>` element (public-law number)** — NOT a status-string match. The
  cleanest enacted signal; confirmed live before building.
- **Law-eligible = HR/S/HJRES/SJRES.** Resolutions (HRES/SRES/HCONRES/SCONRES) **cannot become
  law** → excluded from the enacted-rate denominator (the silent-bug guard). Verified: 0 enacted
  resolutions.
- **`advanced_past_committee` (DOCUMENTED RULE):** TRUE iff the bill's action history carries any
  GPO action type beyond introduce-and-refer — i.e. type ∈ {Committee, Calendars, Discharge,
  Floor, President, ResolvingDifferences, Veto, BecameLaw}. Counts a committee report/markup/
  **hearing** OR any later floor/calendar/presidential/enactment action (IntroReferral alone =
  died in committee). **Slightly generous** (includes hearings, not strictly reported-out) — stated
  plainly, computed off the action-`type` taxonomy (no fragile text matching).
- **Withdrawn cosponsorships EXCLUDED** from `cosponsored_count` (650 withdrawn rows; flagged
  `sponsorshipWithdrawnDate`) — matches GovTrack / the current congress.gov API. Including them
  would change 117 members (audit-confirmed material).
- **119th is PARTIAL** (`congress_partial=TRUE`) — mid-cycle, fewer enacted laws (101 vs 274);
  don't compare externally.

### Smoke test — PASS, reconciled to GovTrack's 118th report card
GovTrack's `/report-card/2024` page summarizes the whole 118th. **Sponsored + cosponsored match
to the integer** across all 3 members:
| Member | introduced | enacted | cosponsored |
|---|---|---|---|
| **Biggs** (high-vol / spam) | 612 = 612 ✓ | 0 vs 1 | 409 = 409 ✓ |
| **Graves** (high-enact / low-vol) | 21 = 21 ✓ | 4 vs 5 | 127 = 127 ✓ |
| **AOC** (mid control) | 11 = 11 ✓ | 0 = 0 ✓ | 378 = 378 ✓ |

The named divergence: `became_law` is ours (standalone `<laws>`) = GovTrack − {0,1}; GovTrack also
counts text **incorporated into other enacted bills**, ours counts only a bill's own public-law
element (cleaner, more conservative; ours never exceeds GovTrack). **Biggs is the headline-trap
case validated by real data:** 612 sponsored (many identical "limitation on availability of funds"
messaging bills), 0 enacted, 0.00% rate — exactly why bills_sponsored is never headlined alone.

### Audit (4 adversarial dimensions, read-only workflow `wf_16535469-3f9`) — PASS
- **Additive safety — PASS:** Phase 1-3 marts byte-for-byte unchanged (12,794 / 1,050 / 1,105 /
  12,794); registry +2 (politics_domain 20→22); no existing politics row re-stamped; clean ingest runs.
- **Grain integrity — PASS (after one fix):** 0 dup keys in all 3 marts; cosponsor list does NOT
  inflate bills. The auditor caught that `n_cosponsors` was a **raw pre-dedup count** (the source
  double-lists a member as cosponsor on 7 bills, e.g. 118 HR 6116 = 30 items / 27 distinct).
  **Fixed:** `n_cosponsors` now = DISTINCT cosponsors, so SUM over bills = cosponsor-mart rows
  EXACTLY (367,735; reconciliation closes to 0).
- **Stat correctness + GovTrack — PASS:** enacted only on law-eligible; enacted_rate denominator =
  substantive (NULL when 0); withdrawn excluded (material); GovTrack reconciliation holds.
- **Vocab/registry — PASS:** both rows `government_power` + `BIOGUIDE` (governed STEEL); landing
  table = UPPER(source_id); catalog lifecycle='landed'.

### How to resume / rebuild (Phase 4)
```bash
python politics/registry/register_political_sources.py --apply  # +2 rows, append-only, idempotent
python politics/loaders/build_bills_leg.py                      # land BILLSTATUS 118+119 + build marts
python politics/loaders/build_bills_leg.py --skip-fetch         # rebuild marts only
python politics/loaders/smoke_bills.py                          # sponsored/enacted/cosponsored vs GovTrack
```

---

## PHASE 3 — THE VOTES LEG

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
**The clean box score is DONE (ideology + money + votes + bills).** The next legs step up in
difficulty and editorial care — they are no longer pure bioguide joins. Recommended first:
the **2026 committee-master `cm26` refresh** (one bulk file, no fuzzy matching) to close the
2026 FEC linkage resolution gap from Phase 2 (2026 committee IDs resolve only ~57% vs 98% for
2024) — a quick, clean win that strengthens the existing money leg before the hard stuff.

*(Then the harder legs, in rising order of fuzziness / editorial weight:*
- ***FEC contribution detail** `fed_fec_bulk_contributions` (itcont) — money-IN-by-industry,
  ties money↔votes, but employer→EIN is fuzzy + the file is huge (chunked load).*
- ***STOCK Act PTRs** (member stock trades) — PDF parsing, high public interest, name-match to bioguide.*
- ***Senate LDA lobbying** — org→EIN fuzzy.*
- *USAspending-by-district.)*

### Still-open / parked items
- **`cm26`** 2026 committee-master refresh (above) — parked since Phase 2.
- **"Money raised" card-labeling decision** — how to present gross vs net on the stat card (parked).
- **Voting-stat definitions** — party-unity / missed-vote labels for the card (parked from Phase 3).
- **Phase-1 member sources' `JOIN_KEYS_STD` back-fill** — existing-row UPDATE, deferred (additive-only).
- **`fed_voteview_rollcalls` one-row tidy-up** (set `['ICPSR']`) — deferred (additive-only).

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
# Phase 4 (bills leg)
python politics/loaders/build_bills_leg.py                       # land GovInfo BILLSTATUS 118+119 + bill marts
python politics/loaders/smoke_bills.py                           # sponsored/enacted/cosponsored vs GovTrack 118th
```
Verification workflows (read-only): Phase 1 `wf_6b3b65a4-53d`, Phase 2 `wf_4222b021-528`,
Phase 3 `wf_1d283e03-750`, Phase 4 `wf_16535469-3f9`. See `politics/README.md`.
