# CLOSE THE LOOP — Snowsight-hour checklist

**Purpose:** take `decisions.total` from **0 → ≥10** by proving the review→decide lane end to end.
Dependency-ordered. Do it top to bottom. **A00 (build lane) before A03 (revoke), with a smoke-test between** — that ordering is load-bearing; A03 is irreversible.

**Chris's decision (2026-07-14):** one build role — **`RIPPLE_TRANSFORM_RW`** — both runs dbt *and* owns the `CONNECT` spine. No new `RIPPLE_BUILD_RW`.

**Amended 2026-07-20** after a live re-verify + adversarial audit (receipts: `outputs/SPRINT_VERIFY_2026-07-20.md`). Five wrong claims corrected; Step 4 finalized from live grant data. Changelog at the bottom.

**Surfaces you'll use:** Snowsight worksheet (SQL, as **ACCOUNTADMIN**) · Snowsight Admin UI (mint PATs) · your terminal (`.env` swap, smoke-test, dbt, A03).
**Golden rule:** where a step says "statement by statement," do **not** use Run All — some statements are *designed* to fail and Run All stops at the first error.
**Error wording:** Snowflake never literally prints "PERMISSION DENIED." Denied writes read **"SQL access control error: Insufficient privileges to operate on table …"**; denied reads read **"… does not exist or not authorized."** The refusal is the proof, whatever the phrasing.

Legend: ☐ = do it · 🔒 = irreversible · 🟢 = read-only/safe · ↩ = reversible

---

## STEP 0 — pre-flight (🟢 read-only; Snowsight as ACCOUNTADMIN — 2 minutes)

*(2026-07-20: the old Step-0 grants question is answered — `SHOW GRANTS TO ROLE RIPPLE_TRANSFORM_RW` turned out to be readable from the reader lane (1,832 rows, dumped in the receipts file), and Step 4 below is finalized from it. Two small things remain.)*

```sql
SHOW WAREHOUSES;                                            -- ① the ETL warehouse name
SELECT COUNT(*) FROM LIBRARY_META."CONNECT".DECISIONS;      -- ② expect 0
```

☐ ① The build/ETL warehouse is the one that is **not** `SERVE_WH` / `COMPUTE_WH` / `SYSTEM$STREAMLIT_NOTEBOOK_WH` (those three are all the reader lane can see). Expected name: `RIPPLE_WH`. Write it into Step 4(c) and Step 5 as `<ETL_WH>`.
☐ ② Confirms the old `CONNECT.DECISIONS` stub is still empty (last verified 2026-07-12), so Step 1's rename is still zero-migration. If it's non-zero, STOP and flag — something wrote verdicts into the stub.

---

## STEP 1 — provision the review write lane (Snowsight worksheet, as **ACCOUNTADMIN**) ↩

Run **`scripts/provision_review_lane.sql`** top to bottom (it's idempotent/guarded; Run All is fine here).
Builds: `LIBRARY_META.REVIEW` schema + append-only `DECISIONS` table + `RIPPLE_REVIEW_WRITER` role, re-points `V_LEADS_PUBLISHED` at the living table, renames the empty `CONNECT.DECISIONS` stub.
**Two-step publish gate (beta ruling B1, 2026-07-20):** in the re-pointed view, ✅ Confirm = nomination only. `PUBLISHED=TRUE` needs a separate explicit publish verdict via `scripts/publish_lead.py` (preview by default, `--apply` to write, refuses anything not confirmed first). One click can no longer publish.

⚠ **ACCOUNTADMIN only** — the script's own header offers SECURITYADMIN, but SECURITYADMIN can't `CREATE SCHEMA`, so under it Run All dies on the first statement with nothing applied.
⚠ Its **last line** (Part 5 — `GRANT SELECT … LEAD_QUEUE …`) will error *"does not exist"* — that's expected; `LEAD_QUEUE` isn't built until Step 7. Everything above it has applied. Re-run that one line after Step 7.
☐ Verify: the two VERIFY queries are **commented out in the file's header (~lines 41–48)** — they do NOT run under Run All. Copy them into the worksheet and run them by hand:
- the first returns **one row**;
- the second (`SHOW GRANTS TO ROLE RIPPLE_REVIEW_WRITER;`) returns **~5 rows** — check the only *table* privileges are **INSERT + SELECT on `REVIEW.DECISIONS`**, nothing else. (The old "each return one row" claim was wrong.)

---

## STEP 2 — mint the review PAT (Snowsight Admin UI) ↩

☐ Mint a PAT **restricted to role `RIPPLE_REVIEW_WRITER`**, with an expiry.
☐ Add it to `library-onboarding/.env` as **`RIPPLE_REVIEW_PAT`** (this is a *new* key; leave `SNOWFLAKE_PAT` alone for now).

---

## STEP 3 — prove the wall (Snowsight worksheet, **statement by statement**) 🟢

Run **`scripts/verify_review_lane.sql`** one statement at a time, as `RIPPLE_REVIEW_WRITER`.
The failures ARE the proof:
- [1] INSERT → **succeeds** (writes the permanent `SMOKE_TEST` proof row)
- [2] UPDATE, [3] DELETE → **denied** ("Insufficient privileges to operate on table…") ← the point (append-only enforced by the DB)
- [4a] read `REGISTRY.SOURCE_REGISTRY` / `"CONNECT".LEADS`, [4b] read `LIBRARY_RAW…` → **denied** ("does not exist or not authorized") ← the writer sees only its one table
- [5] read the `SMOKE_TEST` row → **≥1 row**

☐ If [2]/[3]/[4] *succeed*, STOP — the lane is mis-provisioned; re-check grants in `provision_review_lane.sql`.

---

## STEP 4 — A00: the build lane grants (Snowsight worksheet, as ACCOUNTADMIN) ↩ (mostly)

> **FINALIZED 2026-07-20** from a live read of `SHOW GRANTS TO ROLE RIPPLE_TRANSFORM_RW` (1,832 grants).
> **Already has:** `USAGE` on all four databases · `SELECT` on ~1,800 landing/meta tables · `CREATE SCHEMA` on `LIBRARY_MARTS`/`LIBRARY_STAGING` · ownership of the `CORE`/`EPSTEIN`/`SEEDS` schemas it built.
> **Missing (everything below):** the two `DBT_CROGERS` schemas, ownership of their objects, `V_LEADS_PUBLISHED`, the `REVIEW` read, all of `CONNECT`, and **any warehouse at all** (it currently has USAGE on none).

```sql
-- (b) SPINE — move CONNECT ownership onto the build role (Chris's call, decided 07-14).
--     COPY CURRENT GRANTS preserves RIPPLE_READER's existing SELECTs on those tables.
GRANT USAGE, CREATE TABLE ON SCHEMA LIBRARY_META."CONNECT" TO ROLE RIPPLE_TRANSFORM_RW;
GRANT OWNERSHIP ON ALL TABLES    IN SCHEMA LIBRARY_META."CONNECT" TO ROLE RIPPLE_TRANSFORM_RW COPY CURRENT GRANTS;
GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA LIBRARY_META."CONNECT" TO ROLE RIPPLE_TRANSFORM_RW;

-- (a) dbt — the DBT_CROGERS build surface. The two OWNERSHIP transfers are NOT optional:
--     live grants prove RIPPLE_TRANSFORM_RW owns none of these objects today, and dbt does
--     CREATE OR REPLACE — without ownership, Step 7 fails mid-hour.
GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA LIBRARY_STAGING.DBT_CROGERS TO ROLE RIPPLE_TRANSFORM_RW;
GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA LIBRARY_MARTS.DBT_CROGERS   TO ROLE RIPPLE_TRANSFORM_RW;
GRANT OWNERSHIP ON ALL TABLES IN SCHEMA LIBRARY_MARTS.DBT_CROGERS   TO ROLE RIPPLE_TRANSFORM_RW COPY CURRENT GRANTS;
GRANT OWNERSHIP ON ALL VIEWS  IN SCHEMA LIBRARY_STAGING.DBT_CROGERS TO ROLE RIPPLE_TRANSFORM_RW COPY CURRENT GRANTS;
GRANT SELECT ON FUTURE TABLES IN SCHEMA LIBRARY_RAW.LANDING TO ROLE RIPPLE_TRANSFORM_RW;
GRANT SELECT ON VIEW LIBRARY_META."CONNECT".V_LEADS_PUBLISHED TO ROLE RIPPLE_TRANSFORM_RW;

-- (a′) NEW 2026-07-20 — the smoke test's hidden dependency: `python -m connect leads`
--      checks the suppression ledger in REVIEW.DECISIONS even in dry-run, and if it can't
--      READ it, it tries to CREATE it. These two grants keep the dry-run read-only:
GRANT USAGE  ON SCHEMA LIBRARY_META.REVIEW TO ROLE RIPPLE_TRANSFORM_RW;
GRANT SELECT ON TABLE  LIBRARY_META.REVIEW.DECISIONS TO ROLE RIPPLE_TRANSFORM_RW;

-- (c) the ETL warehouse — MANDATORY (the role has no warehouse USAGE at all today). NEVER SERVE_WH.
GRANT USAGE ON WAREHOUSE <ETL_WH> TO ROLE RIPPLE_TRANSFORM_RW;
```

Dropped vs. the 07-14 draft: the four-database `USAGE` line (already granted — and its comma-separated-objects form was invalid Snowflake syntax anyway; one object per GRANT) and `SELECT ON ALL TABLES IN LANDING` (already granted, ~1,800 tables).

☐ Then mint a PAT **restricted to `RIPPLE_TRANSFORM_RW`**, expiry set — this is the **build PAT** (Step 5 uses it).
Watch-items, deferred to the Step 5 smoke-test:
- the spine runs `CREATE SCHEMA IF NOT EXISTS "LIBRARY_META"."CONNECT"` on every start; if that trips as a non-owner, add `GRANT CREATE SCHEMA ON DATABASE LIBRARY_META TO ROLE RIPPLE_TRANSFORM_RW;` (or patch `connect/store.py`).
- if the `FUTURE TABLES` OWNERSHIP grant errors about an existing future grant: Snowflake allows only one outstanding future-ownership grant per schema — `SHOW FUTURE GRANTS IN SCHEMA LIBRARY_META."CONNECT";`, revoke the old one, re-run.

---

## STEP 5 — swap the lane + smoke-test (terminal) ↩

☐ In `library-onboarding/.env`, point the default lane at the build PAT (keep a copy of the old values to swap back after Step 7):
```
SNOWFLAKE_PAT=<the RIPPLE_TRANSFORM_RW build PAT>
SNOWFLAKE_ROLE=RIPPLE_TRANSFORM_RW
SNOWFLAKE_WAREHOUSE=<ETL_WH>
```
☐ Smoke-test — dry-run, writes leads only with `--run` (not literally write-free: it attempts the `CREATE SCHEMA IF NOT EXISTS` above, harmless once the role owns `CONNECT`'s tables):
```
python -m connect leads
```
Expect: it connects as `RIPPLE_TRANSFORM_RW` and prints lead previews.
- Error naming `REVIEW.DECISIONS` → the Step 4 (a′) grants were missed.
- Error on `CREATE SCHEMA` / `CONNECT` ownership → Step 4's first watch-item.
**Do not proceed to Step 6 until this is clean.**

🟢 **The Reading Room is immune to this swap** (proof run 2026-07-21, appendix in `BETA_DECISIONS_2026-07-20.md`): verdict writes hard-pin `RIPPLE_REVIEW_PAT` + role `RIPPLE_REVIEW_WRITER` and **raise instead of falling back** when that PAT is absent; its read lane rides `SNOWFLAKE_SERVE_PAT` with the role pinned to `RIPPLE_READER`. Nothing about reviewing depends on what `SNOWFLAKE_PAT` holds.

---

## STEP 6 — A03: revoke the straggler PATs (preview in terminal, **drop in Snowsight as ACCOUNTADMIN**) 🔒

Only now that the build lane is proven.
**Verified 2026-07-21:** `RIPPLE_TRANSFORM_RW`'s 1,832 grants are all object-level — no user-management privilege — but token *viewing* is self-service (`SHOW USER PROGRAMMATIC ACCESS TOKENS` succeeded live as `RIPPLE_READER`; all 8 tokens listed, both drop-targets present). Self-service `ALTER USER` from a scoped lane is **unproven**, so the drop runs in Snowsight by default — don't bet the hour on it.

☐ **Preview** from the terminal (read-only, works on any lane):
```
python scripts/revoke_straggler_pats.py
```
Expect exactly **2 to drop** (`ripple_loader`, `RIPPLE_LOADER_PAT2`) and **6 keeps** (`RIPPLE_LOADER_PAT`, `CLAUDE_MCP_RO`, `PORTAL_RECON`, `WAVE3_LOAD`, `LIBRARY_PAT`, `READER`). The new Step-2/Step-4 PATs show as "?? (left alone)" — expected. Ignore the stale "all 5 …" wording.
☐ 🔒 **Drop in Snowsight, as ACCOUNTADMIN** (irreversible — keep the worksheet as the record, since the script's `outputs/` snapshot only writes under `--apply`):
```sql
SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER CROGG23;
ALTER USER CROGG23 REMOVE PROGRAMMATIC ACCESS TOKEN ripple_loader;
ALTER USER CROGG23 REMOVE PROGRAMMATIC ACCESS TOKEN RIPPLE_LOADER_PAT2;
```
☐ Re-run the terminal preview: both stragglers should now be gone from the inventory. (`infra/keys_ledger.json` only updates under the script's `--apply` — note the Snowsight drop there by hand if you want the ledger exact.)

---

## STEP 7 — build the queue mart (terminal, build lane) ↩

⚠ **dbt does not read `.env`** — it takes credentials from shell environment variables via `env_var()`. Export first, in the same shell:
```
set -a; source library-onboarding/.env; set +a
cd library-onboarding/ripple_dbt
dbt build --select marts.review
```
(The export is still required — dbt only reads shell env vars. Since 2026-07-20 the un-exported failure is at least LOUD: `profiles.yml` now defaults to role `RIPPLE_TRANSFORM_RW`, so a bare shell fails on grants instead of silently escalating to ACCOUNTADMIN.)
Materializes `LIBRARY_MARTS.DBT_CROGERS.LEAD_QUEUE`.
☐ Ownership errors on existing `DBT_CROGERS` objects shouldn't happen anymore (Step 4 transfers ownership up front); if one appears anyway, that object class is missing from Step 4's transfer — grant it the same way.
☐ Back in Snowsight (as ACCOUNTADMIN), re-run `provision_review_lane.sql`'s **last line** (the `LEAD_QUEUE` grant that errored in Step 1).
☐ Swap `.env` back to the reader/serve lane (`RIPPLE_READER` / `SERVE_WH` / the reader PAT) so normal serving isn't left on the build lane.

---

## STEP 8 — **OPTIONAL, fine to skip** — budget-meter grant (Snowsight worksheet, as ACCOUNTADMIN) ↩

*This grant exists only to feed the Atlas budget meter, and the Atlas is post-sprint under ruling B3 (the freeze). Nothing in Steps 0–7 or the review depends on it — skip without a second thought, or run it now so it's done when the Atlas wakes.*

```sql
GRANT MONITOR ON RESOURCE MONITOR SERVE_MON TO ROLE RIPPLE_READER;
```
☐ (Reader-side visibility of `SERVE_MON` was confirmed missing 2026-07-14, not re-checked since; harmless to re-run if it's been granted meanwhile.)

---

## AGENT (GREEN) — runs alongside, before the spine rerun

- ☑ ~~Fix the NPPES column-rename break~~ **DONE 2026-07-20**: spec now carries the live single-underscore names (verified against all 333 live columns).
- ☑ ~~Check `FED_CMS_FACILITY_AFFILIATION`~~ **DONE 2026-07-20**: table confirmed gone from landing; its spine-spec entry removed (its NPIs stay on the spine via NPPES/LEIE; the frozen detector evidence is unaffected).
- ☐ Rerun spine + refresh leads **on the build lane** (preview-then-apply).
- ☐ Verify `LEAD_QUEUE` reconciles (`library-onboarding/ripple_dbt/tests/assert_lead_queue_reconciles.sql`).
- ☐ Export `REVIEW.DECISIONS` → git-committed CSV after each review session (`scripts/export_review_decisions.py`, shipped 2026-07-20).

---

## THE POINT — the top-10 review (Reading Room, ~1–2 hrs)

☐ Review **exactly the top 10 `LEAD_QUEUE` rows.** Every row gets a verdict: confirm / reject / needs-work.
**Ten rows in `REVIEW.DECISIONS` = success, whatever the verdicts.** All-rejects is a real finding about detector precision, not a failed phase.
☐ Pin #1, when you pick it: confirm it in the Reading Room, then publish it explicitly — `python scripts/publish_lead.py <LEAD_ID> --by chris --reason "…" --apply`. (Two-step gate: confirm nominates, publish is its own recorded act.)

**DONE (warehouse-checkable):** `V_STATE decisions.total ≥ 10`.

---

## CHANGELOG

**2026-07-20** — amended after a live re-verify + adversarial audit (full receipts: `outputs/SPRINT_VERIFY_2026-07-20.md`). Five corrected claims:
1. Step 1 is **ACCOUNTADMIN only** — SECURITYADMIN can't `CREATE SCHEMA`; Run All would die at statement 1 with nothing applied.
2. Step 1's VERIFY queries live in the script's *header comment*, not "at the bottom", and the second returns ~5 rows, not 1.
3. Step 4 finalized from live grant data (the old Step-0 `SHOW GRANTS` is answered): dropped two already-granted lines (one was invalid comma-list SQL), moved the `DBT_CROGERS` OWNERSHIP transfers up from a Step-7 contingency (live grants prove they WILL be needed), added the `REVIEW.DECISIONS` read grants the smoke test silently requires, marked the warehouse grant mandatory (the role has none today).
4. Step 7: dbt ignores `.env` — added the `set -a; source …` export and flagged the ACCOUNTADMIN default-role footgun in `profiles.yml`.
5. Error-wording note added (Snowflake says "Insufficient privileges" / "not authorized", never "PERMISSION DENIED"); Step 6 credential + stale-count notes; Step 0 gained the stub-empty count check.

**2026-07-20 (later, beta session — `BETA_DECISIONS_2026-07-20.md`):**
6. **Two-step publish gate (ruling B1)** landed across the stack *before* the provision script's first run — Confirm = nomination; `scripts/publish_lead.py` is the only publish path. Step 1, THE POINT, and the provision script itself updated to match.
7. Spine spec fixes landed (NPPES single-underscore names verified live; dead facility-affiliation entry removed) — the two agent pre-tasks above are done.
8. Lane pinning shipped behind `SNOWFLAKE_ETL_WAREHOUSE` (commented in `.env` until Step 0 names the warehouse); dbt's default role is now `RIPPLE_TRANSFORM_RW`, not ACCOUNTADMIN.
