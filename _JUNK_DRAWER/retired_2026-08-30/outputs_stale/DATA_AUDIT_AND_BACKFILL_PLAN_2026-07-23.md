# Ripple — Data Audit & Backfill Plan (2026-07-23)

Read-only audit of `LIBRARY_RAW.LANDING`. No writes. Row counts from
`INFORMATION_SCHEMA.TABLES`; failure modes confirmed against
`LIBRARY_META.INGEST_LOGS.INGEST_RUNS`.

---

## TL;DR

- The warehouse holds **1,785 landing tables**: ~196 curated federal/intl
  sources (the spine) + ~1,563 `PORTAL_*` open-data scrape mirrors.
- The problem is **not "some tables have 30 rows."** The small tables are broken
  in **four different ways**, and each needs a different fix. Lumping them into
  one "re-pour" job wastes money and re-lands blanks.
- The loader is **AI-driven per source** — the "grab only a sample" decision is
  baked into the *generated* download script, not a config toggle. Backfilling =
  re-onboarding with `--include-landed`.
- There is already a one-time-cost mechanism for exactly this: `budget_sprint.py`
  raises the credit ceiling for a sprint, then you restore steady-state after.
- **Blocked on Chris:** the pour needs (1) a **write-capable PAT** (current `.env`
  is read-only `RIPPLE_READER`), (2) a **live warehouse** (`.env` still points at
  `DBT_WH`, which no longer exists — use `COMPUTE_WH`), (3) **internet** (the
  agent's in-IDE Snowflake connection can't reach it). I can build the queue and
  plan; Chris runs the sprint.

---

## 1. Size tiers (all landing tables)

| Tier | Federal/Intl | Portal |
|---|---|---|
| stub (≤200 rows) | 54 | 581 |
| thin (201–2k) | 39 | 626 |
| partial (2k–50k) | 71 | 356 |
| substantial (50k–1M) | 33 | 0 |
| full (>1M) | 25 | 0 |

Every `PORTAL_*` table is ≤50k — the portal mirrors were *all* sampled. This plan
focuses on the **federal spine** (the sources that feed findings and cross-domain
bridges). The portal long tail is a separate, lower-priority decision.

**Caution on the row-count heuristic:** a round number is a *smell*, not proof.
`FED_CMS_HOSPITAL_GENERAL` = 5,432 rows is the real universe of US hospitals, not
a cap. `FED_USASPENDING_TOPTIER_AGENCIES` = 111 is all federal agencies. Every
small federal table gets a real-universe check before it's queued.

---

## 2. The four failure modes (confirmed from the ingest log)

### A. Capped samples — loaded clean, deliberately truncated → **re-pour full**
The generated script paginated an API and stopped early, or pointed at a sample
file. Data is real, just partial. `fed_sam_exclusions` even logged
*"1,000 rows landed; 5 pages skipped"* — it knows there's more.

| Table | Landed | Real universe (approx) | Note |
|---|---|---|---|
| `FED_IRS_990` | 200 | ~1.9M e-file returns | "chunked, streamed 200" — source URL was a sample, not the full corpus |
| `INTL_GLEIF` | 20,000 | ~2.9M LEIs | LEI spine; local-registry crosswalk column also didn't survive staging |
| `FED_SAM_EXCLUSIONS` | 1,000 | ~100k+ | explicitly skipped pages 1–5 |
| `FED_US_SEC_EDGAR` | 48,990 | ~900k filers | CIK↔EIN bridge; capped |
| `FED_FDIC_BANK_DATA` | 10,000 | ~75k+ inst/branches | round cap |
| `FED_EPA_ENVIROFACTS` | 5,000 | large | (ECHO at 3.2M already covers much of EPA — check overlap before re-pour) |
| `FED_USASPENDING_SUBAWARDS` | 5,000 | millions | logged "proof slice" |
| `FED_CLINICALTRIALS` | 500 | ~500k trials | NCT key; pairs with Open Payments |
| `FED_CFPB_COMPLAINTS` | 250 | millions | |
| `FED_NSF_AWARDS` | 125 | ~500k awards | |
| `FED_GRANTS_GOV` | 100 | large | |

### B. Empty / single-row loads — parser broke → **fix codegen, then re-pour**
The load "succeeded" but every column collapsed to blank, or only a wrapper
record landed. Re-pouring the same script just re-lands nothing. Needs the
recon/codegen step repaired (unnest the API envelope / fix the column mapping).

| Table | Landed | Status | Symptom |
|---|---|---|---|
| `FED_NIH_REPORTER` | 5,000 | empty | 5,000 rows, all blank (density 0%) — research-money source |
| `FED_DEA_ARCOS` | 409 | empty | density 0% |
| `FED_ED_FSA_DATACENTER` | 1 | empty | density 0% |
| `FED_FINCEN_BOI` | 1 | success(1 row) | beneficial ownership — envelope not unnested |
| `FED_FBI_CDE` | 1 | success(1 row) | |
| `FED_CDC_WONDER` | 1 | success(1 row) | |
| `FED_CMS_HPT_MRF` | 1 | success(1 row) | "streamed 1 rows" |

### C. Hard failure — never landed → **fix the generated SQL, re-pour**
| Table | Status | Cause |
|---|---|---|
| `FED_HHS_TAGGS` | failed | SQL compile error (invalid identifier) in generated load — HHS grants EIN source |

### D. Redundant API-stub siblings — a full sibling already exists → **do NOT re-pour; drop/rewire**
Re-pouring these wastes money; a fuller table already covers them.

| Stub | Landed | Full sibling already loaded |
|---|---|---|
| `FED_FARA` | 30 | `FED_FARA_BULK` (221,900) |
| `FED_SEC_EDGAR` | 200 | EDGAR family (`FED_US_SEC_EDGAR` 48,990 + `FED_SEC_EDGAR_FINANCIALS` 55,635) — though the family itself needs uncapping (see A) |
| `FED_FEC_API` | 500 | FEC bulk family (`FED_FEC_INDIV_CONTRIBUTIONS` 84M, etc.) |
| `FED_US_USASPENDING_API` | 300 | `FED_USASPENDING_CONTRACTS` (6.3M) |
| `FED_CMS_MAIN` | 158 | CMS provider/facility tables (full) |

---

## 3. Backfill mechanism (how a re-pour actually runs)

Per source, from `library-onboarding/`:
```
python onboard.py --name FED_IRS_990 --include-landed --skip-dbt --yes
```
- `--include-landed` — collision-gate escape; re-onboards a source that already
  has a successful ingest run (a deliberate re-land).
- `--skip-dbt` — land-only; skip model generation during the sprint, build models
  after. Much faster/cheaper per source.
- `--yes` — unattended auto-approve (only safe for category A; see below).

Batch form (preferred for the sprint): build one curated queue JSON and run
```
python onboard.py --queue backfill_queue.json --batch --include-landed --skip-dbt --yes
```

**Category A** (capped samples) is safe to run unattended `--yes` — codegen just
needs to paginate to completion / target the bulk file.
**Categories B and C** must be **attended** — the fix is in recon/codegen, and an
unattended run will burn auto-repair retries and likely re-land blanks. Watch
these one at a time.

---

## 4. Most-efficient one-time backfill (the sprint)

1. **Preflight (Chris):** put a write-capable PAT in `.env`, set
   `SNOWFLAKE_WAREHOUSE=COMPUTE_WH`, confirm internet. Rotate the leaked
   Anthropic key + PAT while you're in there.
2. **Raise the ceiling for the sprint:** `python scripts/budget_sprint.py`
   (restore steady-state after — this is the "expensive one-time cost, not the
   routine norm" you asked for, and the tool is built for it).
3. **Wave 1 — Category A, unattended, land-only.** One `--queue` batch of the
   capped samples, priority-ordered (Tier 1 first, below). Land raw; skip dbt.
4. **Wave 2 — Categories B + C, attended.** Fix codegen per source, re-pour,
   eyeball density > 0 before moving on.
5. **Wave 3 — drop/rewire Category D** redundant stubs (cheap SQL, no pour).
6. **Then** build dbt models on the newly-full tables (the part skipped in step 3).

### Priority order (connective value, not row count)
**Tier 1 — feeds findings + cross-domain bridges now:**
`FED_IRS_990`, `FED_SAM_EXCLUSIONS`, `INTL_GLEIF`, `FED_NIH_REPORTER` (fix empty),
`FED_CLINICALTRIALS`, `FED_US_SEC_EDGAR`.
**Tier 2 — strong accountability sources:**
`FED_HHS_TAGGS` (fix), `FED_CFPB_COMPLAINTS`, `FED_FDIC_BANK_DATA`,
`FED_NSF_AWARDS`, `FED_GRANTS_GOV`, `FED_USASPENDING_SUBAWARDS`, `FED_EPA_ENVIROFACTS`.
**Tier 3 — triage single-row/empty:**
`FED_FINCEN_BOI`, `FED_FBI_CDE`, `FED_CDC_WONDER`, `FED_CMS_HPT_MRF`,
`FED_DEA_ARCOS`, `FED_ED_FSA_DATACENTER`.

---

## 5. Adjacent (not backfill — new "hook up"): the cross-domain keystones

Separate from re-pouring existing stubs, three sources that are **absent** and
would connect the money-world ↔ health-world (the bridge that died last session):
**Federal Audit Clearinghouse** (EIN + UEI in one row), **Transparency-in-Coverage**
(NPI + tax-ID), **PECOS Enrollment** (NPI + CCN). These are new onboards, best
folded into the same budget sprint. FAC first — one ingest, two keys already held.

---

## 6. Blockers (Chris)

1. **Write PAT** — current `.env` token is read-only `RIPPLE_READER`; no pour can write.
2. **Warehouse** — `.env` `SNOWFLAKE_WAREHOUSE=DBT_WH` no longer exists for the
   reader role → set `COMPUTE_WH`.
3. **Leaked secrets** — `.env` still holds a live Anthropic key + live PAT in
   plaintext (re-shared into chat again this session). Rotate.

---

*Audit is read-only and grounded: every failure-mode classification is backed by
the source's latest `INGEST_RUNS` record. Nothing was poured or written.*
