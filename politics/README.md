# The Political Domain — "The Stat Line"

A namespaced, **additive-only** expansion of the Ripple Library: every
ethically-sourced public dataset about US politics and politicians, wired into the
existing identifier spine, laying the foundation for a politician **stat card**.

> **Isolation contract.** All new work lives here (`politics/`) + a dedicated
> `POLITICS` schema in `LIBRARY_STAGING` / `LIBRARY_MARTS` + dbt models under
> `ripple_dbt/models/{staging,marts}/politics/`. Nothing existing is modified.
> Registry writes are **append-only**. Built on branch `politics-domain`.

> **`SESSION_BRIEF_2026-06-29.md` is stale — read this README, not that file,
> for current state.** The brief's "single next action" (build the itcont
> loader) was completed (`build_indiv_donations.py` / `smoke_itcont.py`), and
> an entire judiciary domain (FJC/SCOTUS/JCS) plus the `who_won` election-
> outcomes domain were built after the brief was written and are documented
> below, not in it. Kept for history, not as a runbook.

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
    build_bills_leg.py              # Phase 4: land GovInfo BILLSTATUS -> bill marts
    smoke_bills.py                  # Phase 4 must-pass proof (sponsored/enacted vs GovTrack)
    build_indiv_donations.py        # Task A: itemized individual donations per member (itcont)
    smoke_itcont.py                 # Task A referee -- reconciles itcont sum to FEC truth
    build_who_won.py                # Task B: MEDSL "who won" -- election outcomes joined to spine
    smoke_who_won.py                # Task B referee -- winners vs known facts
    build_fjc_judges.py             # Judiciary: FJC judges + SCOTUS crosswalk
    build_judicial_common_space.py  # Judiciary: JCS ideology scores for judges + justices
    build_scotus_justice.py         # Judiciary: POLITICS__SCOTUS_JUSTICE dimension + crosswalk
    build_cm26_refresh.py           # Maintenance: refresh FEC committee master to 2026 (cm26)
    verify_cm26.py                  # Maintenance: adversarial verification of the cm26 refresh
  registry/
    promote_keys_and_fix_domain.py  # Phase 2 Fix A (vocab) + Fix B (fed_fec_bulk one-row)
  SESSION_BRIEF_2026-06-29.md       # STALE as of 2026-07-30 -- see note below, don't treat as current state
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

# Phase 4 -- the bills leg (legislative output)
python politics/registry/register_political_sources.py --apply   # +2 rows (billstatus + cosponsors), append-only
python politics/loaders/build_bills_leg.py                       # land GovInfo BILLSTATUS 118+119 + build bill marts
python politics/loaders/build_bills_leg.py --skip-fetch          # rebuild marts only
python politics/loaders/smoke_bills.py                           # sponsored/enacted/cosponsored vs GovTrack 118th

# Task A -- individual donations (itcont)
python politics/loaders/build_indiv_donations.py                 # itemized donations per member
python politics/loaders/smoke_itcont.py                          # reconcile to FEC truth

# Task B -- "who won" (election outcomes)
python politics/loaders/build_who_won.py                         # land MEDSL + build who_won mart
python politics/loaders/smoke_who_won.py                         # verify winners vs known facts

# Judiciary -- FJC judges, SCOTUS crosswalk, judge ideology (JCS)
python politics/loaders/build_fjc_judges.py                      # FJC directory + SCOTUS crosswalk
python politics/loaders/build_scotus_justice.py                  # POLITICS__SCOTUS_JUSTICE
python politics/loaders/build_judicial_common_space.py           # JCS ideology scores

# Maintenance -- refresh the FEC committee master to the 2026 cycle
python politics/loaders/build_cm26_refresh.py
python politics/loaders/verify_cm26.py                           # read-only adversarial check
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

**Phase 4 — the bills leg** (GovInfo BILLSTATUS XML, 118th + 119th, all bill types)
| Object | Rows | What |
|---|---|---|
| `LANDING.FED_GOVINFO_BILLSTATUS` | 36,465 | one row per bill (sponsor bioguide, action types, `<laws>`, latest action) |
| `LANDING.FED_GOVINFO_BILL_COSPONSORS` | 367,742 | one row per (bill × cosponsor); withdrawn flagged |
| `MARTS.POLITICS.POLITICS__BILLS` | 36,465 | one row per (congress, bill_type, bill_number); became_law, advanced, stage |
| `MARTS.POLITICS.POLITICS__BILL_COSPONSORS` | 367,735 | one row per (bill, cosponsor_bioguide); is_original / is_withdrawn |
| `MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD` | 1,104 | **the stat** — sponsored / enacted / advanced / cosponsored, per (bioguide, congress) |

This **completes the clean box score: ideology + money + votes + bills**, all bioguide-keyed. The headline-trap stat (`bills_sponsored`) ships only with its qualifiers — the type split (substantive vs resolutions), `bills_enacted` + `enacted_rate` (**law-eligible denominator** — resolutions can't become law), `advanced_past_committee`, and a **separate** `cosponsored_count` (withdrawn excluded; authoring ≠ signing on). `became_law` comes from the `<laws>` element (public-law number), not a status-string match. Reconciled to GovTrack's 118th report card: **sponsored + cosponsored match to the integer** across 3 members (incl. Biggs's 612-bill spam outlier); `became_law` is ours (standalone `<laws>`) = GovTrack − {0,1} (GovTrack also counts text incorporated into other enacted bills).

**Task A — individual donations** (FEC itemized contributions, `itcont`)
| Object | What |
|---|---|
| `LANDING.FED_FEC_INDIV_CONTRIBUTIONS` | the raw 84M-row itcont firehose |
| `MARTS.POLITICS.POLITICS__MEMBER_INDIV_DONATIONS` | **the stat** — itemized individual donations per (bioguide, cycle) |

Reconciled by `smoke_itcont.py` against an independent FEC truth for clean committees — the module's own docstring notes a naive sum off the raw firehose gave a plausible-but-wrong answer three times before this referee existed.

**Task B — "who won"** (MEDSL/MIT Election Lab constituency returns)
| Object | What |
|---|---|
| `LANDING.FED_MEDSL_HOUSE_RETURNS` / `_SENATE_RETURNS` / `_PRESIDENT_RETURNS` | constituency-level election returns |
| `MARTS.POLITICS.POLITICS__WHO_WON` | election outcomes joined to the member spine |

**Honesty note (both docs and the module docstring agree on this):** the join here is **name + state (+ district)**, not a hard ID — MEDSL carries no FEC candidate ID or ICPSR, contradicting what `SESSION_BRIEF_2026-06-29.md` assumed going in. This is a fuzzy, LEAD-grade match, verified with `smoke_who_won.py` against known facts (seat counts, named winners), not a STEEL-tier join.

**Judiciary — federal judges, SCOTUS, and judge ideology**
| Object | What |
|---|---|
| `LANDING.FED_FJC_JUDGES` / `FED_FJC_SERVICE` | FJC Biographical Directory of Article III judges |
| `LANDING.FED_SCDB` | Spaeth SCOTUS database (already-landed, reused here) |
| `MARTS.POLITICS.POLITICS__FJC_JUDGE` / `POLITICS__FJC_APPOINTMENT` | the judiciary spine |
| `MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK` | links FJC judge records to SCOTUS justices |
| `MARTS.POLITICS.POLITICS__SCOTUS_JUSTICE` | one row per justice (~40 modern justices), keyed on the Spaeth/JCS naming convention |
| `MARTS.POLITICS.POLITICS__JCS_MEDIANS`, `POLITICS__JUDGE_IDEOLOGY_COA`, `POLITICS__JUDGE_IDEOLOGY_SCOTUS` | Judicial Common Space ideology scores — same scale as DW-NOMINATE, so judges and members of Congress are directly comparable |

**Maintenance — the cm26 refresh**
`build_cm26_refresh.py` re-lands the FEC committee master against the 2026 (119th-cycle) snapshot — the original Phase 2 landing was 2024-cycle-only, so 2026 candidate↔committee linkages were only resolving ~57% (vs ~98% for 2024). `verify_cm26.py` is the read-only adversarial check that the refresh actually closed that gap. This is a staleness fix, not a data-quality bug in the original Phase 2 work.

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
