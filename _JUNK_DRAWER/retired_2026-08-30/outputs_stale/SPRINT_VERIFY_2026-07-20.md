# SPRINT VERIFY — 2026-07-20 (six-week-brief §3 battery, read-only)

**Session:** 2026-07-20, Claude Code (Fable), role `RIPPLE_READER` on `SERVE_WH` throughout for warehouse reads; zero warehouse mutations; repo writes this session: `CLOSE_THE_LOOP_checklist.md` (amended), `ROADMAP_2026-07-14.md` (changelog appended), this file.
**Method:** three parallel verification agents — repo state, live Snowflake state, adversarial audit of the checklist against the actual scripts. Every claim below carries a receipt.

---

## 1. THE §3 BATTERY, ANSWERED

| # | Brief question | Answer | Receipt |
|---|---|---|---|
| 1 | `SHOW GRANTS TO ROLE RIPPLE_TRANSFORM_RW` — covers the dbt half? | **Ran fine from the reader lane** (expected a denial): 1,832 rows. It has DB `USAGE` ×4, `SELECT` on 1,797 tables, `CREATE SCHEMA` on STAGING+MARTS, ownership of `CORE`/`EPSTEIN`/`SEEDS` schemas. It does **NOT** have: `DBT_CROGERS` schema access or object ownership, any `CONNECT` grants, `V_LEADS_PUBLISHED`, or **any warehouse USAGE at all**. Step 4 of the checklist is now finalized from this. | live `SHOW GRANTS TO ROLE RIPPLE_TRANSFORM_RW` |
| 2 | ETL warehouse name? | Still not knowable from the reader lane. Visible: `COMPUTE_WH`, `SERVE_WH`, `SYSTEM$STREAMLIT_NOTEBOOK_WH`. `RIPPLE_WH` remains the `profiles.yml:15` default and the expected answer; Chris's Step-0 `SHOW WAREHOUSES` (as ACCOUNTADMIN) settles it. | live `SHOW WAREHOUSES` |
| 3 | `V_STATE` — decisions/leads moved? | **Nothing moved.** All 25 metrics exactly at 07-14 values: `decisions.total=0`, leads sum 1,030 (773/236/11/2/2/6), `taps.landed=170`, `landing.rows=284,800,196`, `connect.entities=9,788,419`, `reading_room.views=252`. Platform fully idle. | live `SELECT * FROM LIBRARY_META.REGISTRY.V_STATE` (AS_OF 2026-07-20 12:25 PDT) |
| 4 | `REVIEW` schema / `LEAD_QUEUE` mart exist? | **Neither exists.** `LIBRARY_META` schemas: BUILD, CONNECT, INFORMATION_SCHEMA, INGEST_LOGS, PUBLIC, REGISTRY. Zero `LEAD_QUEUE` objects in `LIBRARY_MARTS` (tables or views). Loop still unprovisioned. | live INFORMATION_SCHEMA queries |
| 5 | SBA source tables landed + EVIDENCE_SQL clean? | **Reproduces cell-for-cell.** `FED_SBA_LOANS` = 2,174,502 rows (exact match). §3 master query ran clean; **every** ratio in the 4×8 grid identical to the finding ($2M FY24 = 26.5 on 291 observed; $500k FY23/24/25 = 1,615/2,885/4,008; $1M = 480/752/737; FY26 n=26,467). The finding is live-true as of today. | verbatim §3 SQL re-run 2026-07-20 |
| 6 | Three scripts present and unchanged? | **Yes, all three, committed and clean** at verification time. `provision_review_lane.sql` (PUBLISHED flip, LEAD_QUEUE grant last), `verify_review_lane.sql` (5-statement proof map verified), `revoke_straggler_pats.py` (preview-default, --apply-gated, 2-drop/6-keep allow-list). *(Line numbers shifted later the same day when the B1 two-step-gate edit landed — the flip now sits at :135, the final grant at :218.)* | file reads + `git status` clean |

**Bonus state:** acquisition still silent — last ingest run 2026-07-11 15:23 (2,364 runs), 9 days quiet. Commit `9744369` (today 12:23 PT, Chris) committed + pushed `ROADMAP_2026-07-14.md` and `CLOSE_THE_LOOP_checklist.md` — the docs-durability risk is closed; the generic commit message ("Refactor code structure…") is misleading but harmless.

---

## 2. THE CHECKLIST AUDIT — 5 REFUTED CLAIMS (all fixed in the file today)

An adversarial agent read the checklist against the actual scripts and code paths. Five claims failed; each would have cost real time inside the one scarce Snowsight hour:

1. **Step 1's role option was wrong.** "ACCOUNTADMIN/SECURITYADMIN" — but SECURITYADMIN holds no `CREATE SCHEMA` on `LIBRARY_META`, so Run All dies at the script's first statement (`provision_review_lane.sql:44`) with nothing applied. → ACCOUNTADMIN only.
2. **Step 1's verify instructions pointed at the wrong place.** The "two VERIFY queries at the bottom" are actually commented out in the file's **header** (:36–39 at audit time; :41–48 after the same-day B1 edit) — Run All never executes them — and the second (`SHOW GRANTS TO ROLE RIPPLE_REVIEW_WRITER`) returns ~5 rows, not one. → copy-out-and-run instructions with the real expectations.
3. **Step 4 contained invalid SQL.** `GRANT USAGE ON DATABASE LIBRARY_STAGING, LIBRARY_MARTS, …` — Snowflake takes one object per GRANT; comma-lists of objects are a compilation error. (Same defect in ROADMAP Appendix C :359.) Moot anyway: live grants show the role already has all four USAGEs. → line dropped.
4. **Step 7's lane story was broken.** dbt never reads `.env` — `profiles.yml` pulls from OS env vars, and its defaults are role **ACCOUNTADMIN** / warehouse `RIPPLE_WH`. As written, the "build lane" dbt run would silently execute as ACCOUNTADMIN, proving nothing. → `set -a; source library-onboarding/.env; set +a` added, footgun documented.
5. **Step 5's smoke test has a hidden dependency no step granted.** `python -m connect leads` (even dry-run) reads the suppression ledger at `LIBRARY_META.REVIEW.DECISIONS` (`connect/leads.py:507` → `connect/safety.py:58`), and on failure **falls back to CREATE DDL** (`safety.py:62-63`). Neither the old Step 4 nor Appendix C granted the build role anything on `REVIEW`. → two grants added as Step 4 (a′): `USAGE` on schema `REVIEW`, `SELECT` on `REVIEW.DECISIONS`.

**Upgraded from contingency to plan:** the `DBT_CROGERS` OWNERSHIP transfers (Appendix C had them; the checklist had demoted them to a Step-7 "if it errors" note). Live grants now **prove** `RIPPLE_TRANSFORM_RW` owns none of those objects, so dbt's `CREATE OR REPLACE` would have failed mid-hour. Moved into Step 4 proper.

**Verified-good (audit passes worth recording):** the 4→5→6→7 ordering exactly matches the roadmap's A00 → `.env` swap → smoke-test → A03 rule; `verify_review_lane.sql`'s 5-statement map is exact (and it self-clamps `USE SECONDARY ROLES NONE`); `provision_review_lane.sql` is genuinely idempotent statement-by-statement; the revoke script's allow-list fail-safe holds even with the two newly-minted PATs present (they show as "?? (left alone)"); `lead_queue.sql` sets `copy_grants=true` and the `marts.review` selector resolves; `SERVE_MON` is the real monitor name (`serve/serve_wh.sql:26`).

**Smaller flags folded into the checklist:** Snowflake's real denial wording (never the literal "PERMISSION DENIED"); A03 rides the build PAT and may lack `ALTER USER` — fails safe, Snowsight-as-ACCOUNTADMIN fallback documented; the revoke script's stale "all 5 stragglers/keeps" success strings (cosmetic — real counts 2/6); Step 0 gained a `CONNECT.DECISIONS` stub-empty count check (last verified 07-12); a possible future-OWNERSHIP grant collision on `CONNECT` (one outstanding future grant per schema).

---

## 3. STATE FINDINGS BEYOND THE BATTERY

- **NPPES spine fix: not landed.** `connect/entity_index_specs.py` untouched since 07-02; still references `PROVIDER_LAST_NAME__LEGAL_NAME` / `PROVIDER_ORGANIZATION_NAME__LEGAL_BUSINESS_NAME` (:22-23). Week-1 agent task, still open.
- **Possible second spine break:** the spec still lists `FED_CMS_FACILITY_AFFILIATION` (:29-33); Reading-Room build notes say that landing table was dropped. Check live before any spine rerun (added to the checklist's AGENT section).
- **Warehouse-lane leak: not fixed.** `connect/db.py:37` bare-connects and dbt both inherit `SNOWFLAKE_WAREHOUSE`; `.env` still says `SERVE_WH` / `RIPPLE_READER`. Week-1 agent task, still open. (`.env` also carries a second credential pair by key name: `SNOWFLAKE_SERVE_PAT` / `RIPPLE_SERVE_ROLE`.)
- **evidence.dev located:** `evidence/` — 252 pages, all git-tracked; `node_modules` AND a `build/` output dir already exist on disk (~88M `.evidence/`), so a build has at least partially run before despite the "hung twice" history. The Track-B clean-build probe remains the entry ticket; not attempted today (out of §3 scope).
- **Reader-lane visibility notes:** `SHOW GRANTS TO ROLE RIPPLE_TRANSFORM_RW` being readable from `RIPPLE_READER` most likely means the role is granted to user `CROGG23` (same user runs dbt) — worth a shrug, not an alarm; `COMPUTE_WH` is visible to the reader alongside `SERVE_WH`; `LIBRARY_MARTS.EPSTEIN` + `STG_EPSTEIN__*` are owned by `RIPPLE_TRANSFORM_RW` (consistent with roadmap Appendix A's mart census).
- **`provision_review_lane.sql:76`** hard-binds `RIPPLE_REVIEW_WRITER` to user `CROGG23` — fine for a one-person shop, just recorded.

---

## 4. TRACK STATUS AFTER TODAY

**Track A (close the loop):** the checklist is now live-data-finalized and audit-hardened; the only remaining pre-hour agent work is the NPPES fix + lane pinning + DR sizing (Week 1 list). The hour itself is Chris's.
**Track B (SBA public door):** the finding reproduces perfectly as of today, its only warehouse dependency is one committed table, and the evidence.dev scaffold exists with prior build artifacts. **Sole blocker: the confirm-vs-published ruling (roadmap §6.4)** — as provisioned, one ✅ Confirm click sets `PUBLISHED=TRUE` in the view the public surface would read. That ruling is the earliest RED decision of the sprint.
**Clock:** SBA FY26 fee schedule turns over ~Oct 1 — Track B's "still happening" claims need re-derivation after that. Ship before.
