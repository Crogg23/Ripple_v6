# Mart defects — VERIFIED verdicts, 2026-08-10 (late)

This file supersedes `mart_defects_from_viz_sweep_2026-08-10.md`. That one was a
read of model code with nothing checked against live data. Everything below was
checked against the warehouse this session. Where the two disagree, this file wins.

Evidence written down (per CLAUDE.md section 7, so nothing has to be re-derived):

- `mart_defect_verification_2026-08-10.csv` — all 610 mart models: columns in the
  mart vs columns in the landing table behind it, live row count vs the catalog vs
  the model's own header comment, page-cap signature, and every cast the generator
  applied to a text column.
- `mart_dead_columns_2026-08-10.csv` — the column-level scan: `COUNT(*)`,
  `COUNT(col)`, `COUNT(DISTINCT col)` and a value sample for each flagged column.
  Bare null checks were never used alone.

Checker: `scripts/verify_mart_defects.py` (phase A metadata-only, phase B scans).

---

## 1. Text cast to number — CONFIRMED, and bigger than reported

**133 columns across 82 marts were 100% NULL in the built table.** Not sampled,
not estimated — counted.

Root cause found and fixed: `scripts/gen_mart_models.py`'s `infer_cast()` matched
its rules as bare substrings.

| the rule | what it was meant to catch | what it also caught |
|---|---|---|
| `"COUNT"` | `TOTAL_COUNT`, `NUM_COUNT` | **COUNTRY**, **COUNTY**, `COUNTERPART`, `ACCOUNT_TYPE` |
| `"RATIO"` | a real ratio | `INCORPORATION`, `REGISTRATION`, `FILTRATION` |
| `"AMT"` | `TRANSACTION_AMT` | `SSHPRNAMTTYPE` (a 13F share-type label) |
| `"UPDATED"`/`"DATE_"` | a real date | `UPDATE_FREQUENCY` |
| `"_RATE"` | a rate | `FOOTNOTE_FOR_..._RATE` (free text) |

`TRY_TO_NUMBER` does not fail on bad input — it returns NULL. So every one of
those models built green, `dbt test` stayed green, and the catalog kept advertising
the source as fully modeled while the column was gone.

Casualties included every country field in the SEC DERA quarterly submissions
(2024Q1–2026Q1), both Senate lobbying country fields, the EPA county fields, the
FDA adverse-event reporter country, ten DOL worksite-county fields, and the EU/UN
sanctions country fields.

**Fixed:**
- `gen_mart_models.py` — `HARD_TEXT` (free text never casts) and `STRIP_WORDS`
  (the accidental word is removed before the rules run, so `INCORPORATION_DATE`
  still casts as a date while `COUNTY_FIPS` is left alone). Verified against all
  133 known victims and against the columns that must keep their cast.
- `scripts/repair_dead_casts.py` — un-wrapped **173 columns across 101 model
  files**: 136 driven by the live evidence, 37 more the static guard caught.
- All 101 models rebuilt. **143 of 150 checked columns now carry data.**
- `tests/test_mart_cast_guard.py` — 44 offline tests. One fails the build if
  `infer_cast` ever hands a numeric cast to a textual name; another scans every
  mart `.sql` on disk for the same accident, so a hand edit or an old copy of the
  generator cannot slip it back in.

**The 7 that are still empty are genuinely empty upstream, not cast damage:**
FinCEN BOI (1-row stub), the USAspending API mart, the 30-row FARA stub, a Texas
lobbying column, ADB (41 rows), DHS HIFLD (500-row sample), NIH RePORTER org
country. Blank in the source.

**Side effect worth knowing:** county/state FIPS columns are now text, not numbers.
That is the fix, not a regression — casting a FIPS to a number strips the leading
zero (`01001` → `1001`) and breaks every join keyed on it.

## 2. Shell marts — MOSTLY WRONG. One real case.

The sweep flagged a class of marts exposing almost none of their source. Checked
live, **only one is real**:

- **Immigration court case data — CONFIRMED, and worse than described.**
  12,631,225 rows. The *landing* table `FED_EOIR_CASE_DATA` has exactly one real
  column, `CASE_TYPE`. Every judge, court, hearing-date, charge and outcome field
  was dropped **at ingest**, not by the mart. So this cannot be remodeled — the
  data is not in the warehouse. It needs a re-ingest, and no loader for it exists
  in the repo. Not fixed this session; the model now carries a header saying
  exactly this so nothing gets built on it by mistake. The generated test that
  asserted `case_type` is *unique* across 12.6M rows was also removed.
- **FDIC enforcement — CONFIRMED but small.** Landing has only `RAW_TEXT` and
  `ORDER_URL`; the scrape never parsed bank, date or penalty. Its mart is not
  built at all.
- **The eleven openFDA / Wayback / USAspending "shells" — FALSE ALARM.** Their
  landing tables hold one VARIANT column because they are JSON, and the marts
  already flatten them properly through staging: FDA GUDID exposes 17 columns,
  MAUDE 25, drug enforcement 30, device enforcement 29. Nothing to fix.

## 3. Positional column names — CONFIRMED for FEC, false alarm elsewhere

- **Four FEC marts — CONFIRMED and FIXED.** Candidates, committees,
  candidate-committee linkage and PAC summary all shipped `c1..c27`. The loader
  wrote headerless FEC bulk files. Real names restored from the official FEC bulk
  layout and verified field-by-field against the landing values (candidate master
  `H0AL02087 / ROBY, MARTHA / REP / 2018 / AL / H` lines up exactly). Rebuilt and
  confirmed live. Their `schema_*.yml` tests, which asserted on `c1`/`c7`, were
  rewritten to the real key columns.
- **Freedom House — FALSE ALARM.** `C1`, `C2`, `C3` are Freedom House's own
  indicator codes (Category C questions). The source really names them that.
- **NHTSA — duplicates, removed.** The `transport/` copies were positional; the
  `consumer_safety/` copies have real names and are the live ones (2.23M
  complaints, 154k investigations, 243k recalls). The transport tables were
  already moved out of the live schema on 2026-07-31; the three stale model files
  and their schema files are now deleted from the project. **No table was dropped
  — that stays Chris's call.**
- **EAC EAVS — FALSE ALARM.** It has real column names.

## 4. Suspected page caps — 18 confirmed as round numbers, NOT re-pulled

Confirmed sitting on an exact loader-page boundary (this is a strong signal, not
proof, and none of these were re-pulled this session):

500,000 — IRS auto-revocations, IRS Pub 78 eligible donees, three Google political
ads tables, CourtListener investments, OSHA ITA case detail 2023 and 2024.
10,000 — Treasury daily deposits, FDIC BankFind.
5,000 — EPA Envirofacts, USAspending subawards, two international open-data portals.
2,000 — HUDOC. 1,000 — BJS, two more portals.

## 5. Row counts that disagree with themselves — 49 confirmed

49 marts where the live row count disagrees with `CATALOG.MART_ROW_COUNT` and/or
the model's own header comment by more than 1%. Listed per-model in the
verification CSV. Not reconciled this session.

## 6. Not touched this session

Steps 3 and 4 of the plan — re-pulling the short tables and labelling the
sample-only sources in the catalog — were out of scope for this session and remain
open. The FEMA individual-assistance reload and the UK Companies House PSC wipe
also remain as they were.
