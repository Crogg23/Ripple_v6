# US Politics Load — Build Runbook

_2026-06-30 · the turnkey build plan a session can be "let loose" on without troubleshooting or cleanup._

This runbook is the authoritative, self-contained plan. It is the product of: the coverage audit
(`outputs/us_politics_coverage_audit_2026-06-30.md`), the three load scopes, and the adversarial
stress-test (`outputs/us_politics_load_stresstest_2026-06-30.md`). Every fix the stress-test demanded is
baked in here. The grabbable execution units are the GitHub issues `[P0]`–`[P6]`; this doc is the map.

**Tracker:** epic **#44**. Tasks: `#33` P0 human gate · `#34`–`#38` P1 (committees / FEC small files /
committee master / money marts / bolt-ons) · `#39` P2 assistance · `#40` P3 SAM · `#41` P4 LDA · `#42` P5
itcont · `#43` P6 deferred. Scaffolding `#32` (done). Each issue carries its own spec + acceptance + rollback.

---

## The contract — what "trouble-free" means here

A build session running this **cannot make a mess and cannot ship a wrong number**, because every load is:

1. **Pre-flight-gated** — `loadkit.preflight` refuses to *start* a load whose worst case crosses the PAT
   expiry, the budget suspend line, or a dead key. Fail fast, never fail half-way.
2. **Atomic + idempotent** — `loadkit.atomic_load` lands into `<TABLE>__STAGING` and only swaps it live on
   full success. A crash leaves the live table untouched and the staging table to be overwritten next run.
   **A failed load is a no-op you re-run, not a cleanup.**
3. **Referee-gated** — `loadkit.smoke` ties the load's numbers to an independent source (OpenFEC, the FEC
   site, USASpending) as a **precondition to the swap**. A load that doesn't reconcile never goes live.
4. **Resumable** — `loadkit.checkpoint` banks per-window progress; an interrupted scrape resumes, it doesn't
   restart.

What it *can't* do is make external sources never surprise us. When one does, the referee/quarantine catches
it and the load **stops clean and reports** — it doesn't ship and doesn't leave a half-table.

---

## The scaffolding (Phase 0 — DONE, tested offline)

`loadkit/` — 6 modules, 31 offline unit tests green (`tests/test_loadkit.py`), zero Snowflake/network.

| Module | Use it for | Key call |
|---|---|---|
| `fec_parse` | FEC pipe/CSV parsing that **quarantines** a shifted row instead of padding it | `parse_pipe(raw, COLS).require_clean()` / `parse_csv(raw, expected_columns=...)` |
| `preflight` | the start gate every load opens with | `preflight(pat_check(...), budget_check(...), dep_check(...)).raise_if_blocked()` |
| `windowed` | cursor-hostile APIs (LDA) — subdivide below the page ceiling | `plan_windows(roots, count_fn, subdivide)` + `assert_window_complete(...)` |
| `checkpoint` | durable per-window resume | `CheckpointSet` + `CHECKPOINT_DDL` + `load/save_checkpoint` |
| `atomic_load` | land-to-staging + atomic swap | `swap_plan(table,...)` / `execute_swap(conn, table,...)` |
| `smoke` | reconciliation referee (precondition to swap) | `penny_reconcile(measured, expected, label=...)` / `reconcile(..., tol_pct=...)` |

Every loader in this build imports loadkit; none reinvents these.

---

## ⛔ Phase 0 — the human gate (blocks everything) · `[P0]`

The agent **cannot** do these (classifier-blocked from `ALTER USER` / `ALTER RESOURCE MONITOR`). Chris does
them once, then the build runs unattended:

1. **Rotate the Snowflake PAT** to a fresh ≥90-day token. *(DONE 2026-07-02 — current PAT expires
   **2026-09-20**; expiries tracked in `infra/keys_ledger.json`.)* Update
   `library-onboarding/.env`. *Until this is done, `preflight.pat_check` blocks every load — by design.*
2. **Confirm month-to-date budget headroom** > the batch's estimated uptime-credits (`SHOW RESOURCE MONITORS`
   → `RIPPLE_BUDGET`). Loads are ~free per-row; the gate is leftover monthly headroom. If tight, raise the
   quota or flip 90/100 to NOTIFY for the window.
3. **Create the checkpoint table** once: run `loadkit.checkpoint.CHECKPOINT_DDL`.
4. *(while valid)* **Pre-flight the SAM key** against the data-services host (a 200 + ZIP), and register a
   **free OpenFEC key** (1000/hr) for the FEC referees — put it in `.env`.

Acceptance: `pat_check` and `budget_check` both return OK for an estimated-runtime probe. Then go.

---

## Phase 1 — bolt-ons + small FEC files (cheap, safe, no streaming) · `[P1]`

Order chosen so the parser/dedup/attribution machinery gets built and proven on **small** data before itcont.

### 1a · committee-membership (re-scoped — NOT one trivial file)
- **Source:** `@unitedstates/congress-legislators` → `committee-membership-current.yaml` **+** `committees-current.yaml` (flatten nested subcommittees). 119th-current only.
- **Key:** `bioguide` + `thomas_id` → `POLITICS__MEMBER_CROSSWALK`. **Mart:** `POLITICS__COMMITTEE_MEMBERSHIP`.
- **Referee:** a known committee's roster size matches the site (e.g. Senate Finance). bioguide join-rate = 100%.
- **Rollback:** atomic swap (nothing) + append-only registry.

### 1b · GovInfo BILLSUM (bill summaries)  ·  1c · Demand Progress earmarks  ·  1d · EveryCRSReport  ·  1e · GovInfo BILLS + PLAW (text)
- Each lands all-TEXT via `land()` (small) or chunked if a corpus; keys: `bill_id` / `bioguide` / `crs_product_id` / `law_number`.
- **Referees:** BILLSUM — every bill_id joins `POLITICS__BILLS`, spot a non-empty summary. earmarks — a member's count vs a known figure, bioguide join ~100%. CRS — ~23k products, a product_id resolves. BILLS/PLAW — enacted-law count cross-checks `POLITICS__BILLS.became_law`.

### 1f · FEC small transaction files — pas2 / independent_expenditure / oth / oppexp
- **Parser:** `fec_parse.parse_pipe(...).require_clean(0.001)` for pas2/oth/oppexp (pipe); `fec_parse.parse_csv(..., expected_columns=IE_COLS)` for independent_expenditure (comma+header). **Branch by file** — never feed the IE CSV to `parse_pipe`.
- **Landing:** `atomic_load` to `FED_FEC_*__STAGING` → swap. SOURCE_IDs: `fed_fec_committee_to_candidate`, `fed_fec_independent_expenditures`, `fed_fec_committee_transfers`, `fed_fec_operating_expenditures`. **Reconcile the SOURCE_ID scheme against the existing `fed_fec_bulk_contributions` row first** (append-only won't catch a colliding id).
- **Dedup:** per-file on `(CMTE_ID, TRAN_ID, TRANSACTION_TP)` keep latest `FILE_NUM` (so a 24A/24E pair survives). **Cross-file assertion:** no `SUB_ID` appears in both the pas2-derived and oth-derived marts (pas2 ⊂ oth).
- **IE:** carry `support_amount` / `oppose_amount` **separately** (never sum 24A+24E). The IE CSV (`SUP_OPP`) is the source of truth; pas2/oth 24A/24E are coverage cross-check only.
- **Referee (`smoke`):** one PAC's contributions to a candidate (pas2) and one committee's operating disbursements (oppexp) penny-reconcile to OpenFEC `/committee/{id}/totals`. abort-on-non-200.

### 1g · cumulative committee master + conduit resolution (prereq for money marts)
- Build `POLITICS__FEC_COMMITTEE_ALL` = union of all `cm` snapshots; add an `OTHER_ID → cn` candidate fallback for H/S/P-prefixed ids. **Measure the unresolved `CMTE_ID`/`OTHER_ID` rate** before trusting any money mart.
- **Conduit rule (split by purpose):** exclude `MEMO_CD='X'` from **dollar sums**, but **keep** the `X`/`15E` memo lines for **attribution** (follow `OTHER_ID` to the true recipient). **Assert** ActBlue `C00401224` / WinRed `C00694323` never appear as a *member's* recipient.

---

## Phase 2 — USASpending assistance + sub-awards · `[P2]`

- **The verified bug to fix:** the contract loader's `COLUMNS` list is contract-only; reusing it for assistance silently drops CFDA/FAIN/URI (`usaspending_load.py:52-66,133`). Write a **separate assistance COLUMNS projection** (`recipient_uei, assistance_listing/CFDA, fain, uri, action_date, federal_action_obligation, place FIPS`).
- **Award types:** `prime_award_types` = grants `02-05`, direct payments `06,10`, loans `07,08`, other `09,11` (its **own** job → `fed_usaspending_assistance`). Sub-awards: `sub_award_types=["grant","procurement"]` → `fed_usaspending_subawards` (split, schema differs). Loan **face value** vs **subsidy cost** land as distinct columns.
- **Backfill:** the **Award Data Archive** pre-generated FY ZIPs (no fragile on-demand job near any clock).
- **Referee:** assert `FAIN`+`CFDA` non-blank before registering; a CFDA program's quarter obligation total ties to USASpending. UEI rollups `COUNT DISTINCT award_id` (never SUM breadths).
- **Bridge:** assistance `UEI` → `debarred_but_funded` (screen contracts **and** assistance).

---

## Phase 3 — SAM exclusions via WINDOWED v4 API (NOT the CSV) · `[P3]`

- **Correction baked in:** do **not** swap to the active-only Extracts CSV — the existing v4 loader already yields `UEI` + activation + termination (`sam_exclusions_load.py:70,84,85`); the CSV drops UEI and **silently disarms `debarred_but_funded`**.
- **Fix:** keep the v4 Entity API; beat the 10k ceiling by **windowing** (by `exclusionType`/agency) — same `loadkit.windowed` pattern as LDA. Preserve `TERMINATION_DATE`.
- **Referee:** total active exclusions ties to SAM's published count; `UEI` populated above a floor; **assert `debarred_but_funded` still returns > 0 join keys** after the reload (the guard against the regression). License string stays the loader's D&B-Open-Data note (not CC0).

---

## Phase 4 — LDA lobbying, 2021–2026 first pass · `[P4]`

- **Base URL** `https://lda.gov/api/v1/` (not the dying hostname). Two tables: `/filings/` → `fed_senate_lda`, `/contributions/` (LD-203) → `fed_senate_lda_contributions` (new). Land LDA under a **new source_id** OR an explicit authorized one-row UPDATE — append-only can't refresh `fed_senate_lda`'s stale facets, and "retire `fed_senate_lda_bulk`" is a no-op under INSERT-only.
- **Windowing (fix):** `loadkit.windowed.plan_windows` by `filing_year`+`filing_type`, **recursively sub-split** any window whose `count` > ~2500; **`assert_window_complete`** (`pages*25 >= count`) before marking a window done. The `<10k/slice` target is dropped — it's above the ceiling.
- **Resume:** `loadkit.checkpoint` per `(year, quarter, type)`; decouple paging from the Snowflake write so a dead PAT blocks only the final land.
- **Landing:** one row per `filing_uuid`, nested arrays as JSON-text; explode in staging via `LATERAL FLATTEN`. **Post-FLATTEN assertion:** exploded activities > 0 for > X% of non-"No Activity" filings (density gate only proves the blob landed).
- **The libel guard:** publish lobbying-on-a-bill as a **co-occurrence COUNT of filings**, never a summed per-bill dollar (one LD-2 carries one lump across all its bills; the bill regex is fuzzy). Any $ context reads ESTIMATED with the match-rate attached, never next to a named member as fact.
- **Scope:** 2021–2026 only this pass (fits inside a fresh PAT). 1999 backfill → Phase 6.

---

## Phase 5 — itcont (the firehose) LAST, behind its referee · `[P5]`

Do **not** start until 5a + 5b exist and Phase 0 gates are green for the estimate.

- **5a · `smoke_itcont.py`** — penny-reconcile ONE clean committee's itemized individual contributions (memo-`X` excluded, conduit-resolved, refunds netted) to OpenFEC `/committee/{id}/totals`, registered key, **abort on non-200**. **Passing it is a PRECONDITION to landing.**
- **5b · streaming generator** — onboard via `onboard.py` `load_mode='chunked'` with a `fetch_data` that `z.open(name)` → `io.TextIOWrapper(latin-1)` and yields a DataFrame every `chunk_rows` lines (parsed with `fec_parse.parse_pipe`). **Never** `zf.read()` / `splitlines()` the whole member — `build_money_spine`/`land()` OOM on 30–40GB. Land to a **staging table**, `atomic_load.execute_swap` on success; resume via a monotonic source row number or full staging rebuild (the `COUNT(*)`-offset resume is dup-unsafe under a re-published file).
- **Pre-flight:** a capped `ONBOARD_CHUNK_MAX_ROWS=1_000_000` smoke load first to measure the real credit delta; confirm `(estimated runtime × 2)` fits inside the fresh PAT and budget headroom; then run in bounded capped passes. itcont stays the **last** thing, never within the PAT's final 24h.

---

## Phase 6 — deferred (after the above, low-priority) · `[P6]`

- LDA **1999 backfill** in many short capped runs (never one 11hr straddle).
- **Freshness-ledger entries** for every new source: add to `scripts/freshness_mapping.json` + a `MMDDYYYY` parser branch in `build_freshness_ledger.py` (FEC `TRANSACTION_DT` is MMDDYYYY; assistance → `action_date`; LDA → `dt_posted`). Treat "ledger entry + `--apply` re-run" as a **load-completion gate** for each source as it lands.

---

## The build order, one line

```
[P0] human gate (PAT + budget + checkpoint DDL + keys)
  → [P1] bolt-ons + small FEC files (+ committee master/conduit)   ← builds the machinery on cheap data
  → [P2] USASpending assistance + sub-awards
  → [P3] SAM windowed v4 (keep UEI — not the CSV)
  → [P4] LDA 2021–2026 (windowed + checkpoint + count referee)
  → [P5] itcont LAST (smoke_itcont + streaming generator + capped passes)
  → [P6] LDA 1999 backfill + freshness-ledger entries
```

## What this build does NOT cover (by design — out of frame)
- The fuzzy **money → EIN/industry** bridge (employer free-text; a downstream `int_` module, separate gated step).
- Everything **below federal** (state/local) — the all-levels layer from the coverage audit.
- Other federal gaps (PTRs, nominations, ad spend, scorecards, surveys, lower judiciary).

After this build, **federal money + influence is complete on hard keys.** The rest is the next conversation.
