# HARDENED PLAN — Ripple Housekeeping (build spec, 2026-07-01)

> Product of a 50-agent adversarial stress-test (6 attack lenses → per-finding verify → synthesis)
> against `housekeeping_PLAN_2026-07-01.md`. 43 findings, 39 survived, 2 blockers.

## 1. VERDICT
**needs-rework — 2 blockers, same root cause.** C2 sourced mart FQNs from `CATALOG`, but
CATALOG has **no mart-name column** and only sees **25 of 73 physical marts**. Fix = drive the
Reading Room off the physical mart inventory via a new `FRIENDLY_LAYER` table (new step C1.5).
B and A are sound with doc fixes. C0/C1 hand-lists must be killed. Everything stays additive/reversible.

## 2. BLOCKERS (fix before any C build)
- **BLOCKER-1 — no mart FQN.** CATALOG exposes only `LANDING_FQN` + boolean `_REAL_MART`. Mart names
  (`PROCUREMENT__INTL_EC_SERCOP`) do NOT equal `<domain>__<source_id>` (1 of 25 match); schema
  (DBT_CROGERS vs POLITICS) isn't in CATALOG. **FQN is not reconstructable.**
- **BLOCKER-2 — 48 of 73 marts invisible to CATALOG.** All 24 POLITICS (incl. 945k-row voteview),
  5 CORE dims, 4 EPSTEIN facts, 4 cross-source DBT_CROGERS marts never appear. Verified: 73 physical vs 25.
- **FIX (step C1.5):** build `LIBRARY_META.REGISTRY.FRIENDLY_LAYER` (real table, keyed on physical
  `OBJECT_FQN`): `OBJECT_FQN, SOURCE_ID(nullable), LAYER('mart'|'landing'), FRIENDLY_NAME,
  FRIENDLY_DOMAIN, GENERATED_COMMENT, IS_SAMPLE, IS_STUB, GENERATED_AT`. Populate from a **physical
  walk of `LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES` (all 73)** + landed/modeled non-portal landing.
  A2 emits `COMMENT ON TABLE` per OBJECT_FQN; C2 emits `CREATE VIEW … AS SELECT * FROM OBJECT_FQN`.
  No FQN reconstruction, ever. Both A2 and C2 read this one table.

## 3. PER-WORKSTREAM CHANGES

### B — Cleanup
- **B1** fix reverse: `CREATE DATABASE SNOWFLAKE_SAMPLE_DATA FROM SHARE SFSALESSHARED.SFC_SAMPLES_PROD3.SAMPLE_DATA;`
- **B2** DEFAULT HOLD. "`DROP DATABASE` does NOT cancel billing — only unmounts." Gate: Chris cancels
  listing `GZTSZ290BUXPL` (provider `HFB60520`) in Snowsight → confirm cancelled → then agent drops.
  It's an **expired trial** (error 090693, tables already unreadable); 13 Snowflake-managed Trust
  Center/CIS functions reference it but don't hard-depend (scanner ran 2026-06-27). Reverse = re-subscribe.
- **B3** gated real-table copy: `CREATE TABLE …_BAK_20260701 AS SELECT * FROM SOURCE_REGISTRY` (expect
  1645) → verify counts equal → only then `DROP …_BAK_20260625`. Never a view.
- **B4** **do NOT drop, no action.** All three scratch tables are **already TRANSIENT** (born that way
  each rebuild). Dropping is undone within 7 days by heartbeat's weekly `connect all`, and interim
  `connect seed/incremental/validate` hard-error (002003). Delete the "convert to TRANSIENT / $0.02" line.
- **B5** two lanes, list built programmatically (`SHOW TABLES … WHERE rows<=1`):
  - **Lane 1 (10 dbt stubs):** fjc_idb, doj_crt_cases, naag_multistate_settlements, zefix, gemi, cro,
    hhs_taggs, fdic_enforcement, nara_wra_aad, slavevoyages_intraamerican. Recipe: `{{config(enabled=false)}}`
    in git → CTAS `_BAK_20260701` → `DROP TABLE`. Reverse = enable + dbt run.
  - **+ add `GOVERNMENT_RECORDS__FED_NARA_AAD` (9 rows, degenerate)** to Lane 1.
  - **BORME (3 rows):** separate decision — NOT a 1-row stub (see D3).
  - **Lane 2 EPSTEIN ledger (3 rows):** NOT dbt-managed (no model in repo). No disable step, no dbt
    reverse. Snapshot is the ONLY restore path. Default HOLD (see D2). Its 3 siblings (FCT_*) are real.

### A — Comments
- **Pre-A snapshot (new):** dump every existing non-null COMMENT → `outputs/_rollback_comments_20260701.sql`
  (DBs/schemas via `SHOW`; tables via INFORMATION_SCHEMA). A1 **must preserve** LIBRARY_TOOLS "do not drop".
- **A1** DB/schema comments (re-assert LIBRARY_TOOLS warning).
- **A2** iterate `FRIENDLY_LAYER` (all 73 marts + named landing), explicit allowlist, `COMMENT ON TABLE
  <OBJECT_FQN> IS %s`. Never schema-wide, never DB/schema/REGISTRY objects. Writes GENERATED_COMMENT once.
- **A3** portal templated comments (unchanged).

### C — Reading Room
- **Pre-req:** add `LAST_INGESTED_AT` to CATALOG (1-line projection of `ENDED_AT` from its existing
  latest-run CTE; fully populated 1060/1060). Needed by A2 + C3.
- **C0** live-driven + self-verifying: SELECT the actual UNCLASSIFIED landed/modeled set (=52); require a
  mapping for every one, **ABORT if any unmapped**. Add the 12 missing marquee sources (CMS×4→health;
  epa_echo→energy_environment; usgs→science_research; irs_bmf/revocation→corporate_entities;
  naag→justice_courts; sec_edgar_financials→money_finance; slavevoyages→history_culture;
  opensanctions→sanctions_enforcement). Close-out gate: UNCLASSIFIED landed/modeled must = 0 before C1.
- **C1** kill the hardcoded 16-schema list. Derive live: `SELECT DISTINCT domain_primary … lifecycle IN
  ('landed','modeled')`, map via ONE governed domain→schema function shared with C2 (all 23 FACET_VOCAB
  values). Adds CRIME_SECURITY, GEO_DEMOGRAPHICS, IMMIGRATION_MIGRATION, EDUCATION, PROCUREMENT_INTL +
  hand-mapped GEOGRAPHY (CORE), CAMPAIGN_FINANCE/GOVERNMENT/ELECTIONS/JUSTICE (POLITICS), INVESTIGATIONS.
- **C1.5 (NEW)** build FRIENDLY_LAYER (the blocker fix). Includes friendly_name generator:
  NAME primary → strip acronyms/tags, fix mojibake (U+FFFD), UPPER_SNAKE; **sub-entity-aware** before
  suffix (FEC_COMMITTEES/FEC_CANDIDATES/FEC_INDIVIDUAL_DONATIONS; HOSPITALS/NURSING_HOMES/…;
  HOUSE_RESULTS/SENATE_RESULTS/PRESIDENT_RESULTS). Fallback NAME→DESCRIPTION→hand-map (must cover 4 dirty
  rows). Per-domain collision pass; survivors→human review before apply (~40 known clusters).
- **C2** per-schema **reconcile** from FRIENDLY_LAYER: include LAYER='mart' (all 73) OR landed/modeled
  landing, IS_ORPHAN=FALSE, NOT LIKE '%.PORTAL_%'. **Do NOT gate on IS_SAMPLE** — keep the 3 modeled
  samples, add honesty badge. Stub guard (tiny mart + empty PK → point at LANDING, mark "raw-only").
  **Prune:** snapshot SHOW VIEWS → CREATE OR REPLACE target set → DROP generator-owned views not in
  target (allowlist-protect START_HERE) → emit added/kept/pruned diff for approval. **Post-dbt hook:**
  C2 re-runs after every `dbt run` (SELECT * views freeze columns). Success criterion → "one additive
  post-dbt regeneration step."
- **C3** START_HERE reads FRIENDLY_LAYER + CATALOG; freshness = LAST_INGESTED_AT; curated/portal tag on
  PORTAL_ name test + third value `curated-sample`.
- **C4** patch `grant_mcp_readonly_catalog.py` line 9 (hardcoded macOS path → `Path(__file__).resolve().
  parents[1]/"library-onboarding"`). Append THE_LIBRARY grants (USAGE db/all+future schemas, SELECT
  all+future views) TO ROLE CLAUDE_MCP_READONLY. Run only after C1/C2/C3 exist. Verify as the role.

## 4. REVISED ORDERING
```
0.  Pre-A COMMENT snapshot → outputs/_rollback_comments_20260701.sql
1.  B1 (drop sample mount) · B3 (backup→verify→drop old) · B5 Lane 1 (10+NARA_AAD)
    [GATED] B2 (Chris cancels billing) · B5 BORME · B5 EPSTEIN ledger · B4 = no-op
2.  Add CATALOG.LAST_INGESTED_AT · A1 (DB/schema comments)
3.  C0 (tag 52, abort-if-unmapped, gate UNCLASSIFIED=0)
4.  C1 (derive schemas live) → 5. C1.5 (FRIENDLY_LAYER + names + collision review)
6.  A2 (comments from FRIENDLY_LAYER, workflow) → 7. C2 (reconcile+prune diff→approve) · A3
8.  C3 (START_HERE) → 9. C4 (patch→grants→verify) → 10. ACCEPTANCE TESTS
Going forward: append C2/C3 regeneration to dbt orchestration.
```

## 5. DECISIONS FOR CHRIS
- **D1** paid mount → cancel sub in Snowsight then drop (expired trial, 370 noise views).
- **D2** EPSTEIN ledger → KEEP (no repo build path; snapshot-only reverse; likely intentional).
- **D3** BORME (3 rows) → KEEP, flag for re-ingest (not the 1-row stub signature).
- **D4** friendly names live in NEW `FRIENDLY_LAYER` table (covers the 48 source-less marts).

## 6. ACCEPTANCE TESTS (read-only)
- A. `SELECT COUNT(*) FROM CATALOG WHERE domain_primary='UNCLASSIFIED' AND lifecycle IN('landed','modeled')` = 0
- B. Every physical mart (73) has exactly one FRIENDLY_LAYER row (uncovered = 0)
- C. `THE_LIBRARY` view count == FRIENDLY_LAYER rows + START_HERE
- D. Every friendly view resolves (LIMIT 0, no invalid-identifier)
- E. Every landed/modeled non-portal domain has a THE_LIBRARY schema (0 unmapped)
- F. `SOURCE_REGISTRY` count == `_BAK_20260701` count
- G. `SHOW TABLES IN LIBRARY_META.CONNECT` → scratch tables present, kind=TRANSIENT
- H. `USE ROLE CLAUDE_MCP_READONLY; SELECT * FROM THE_LIBRARY.START_HERE LIMIT 1;` succeeds
- J. `python -m connect validate` → no 002003 · `dbt run` → success unchanged
