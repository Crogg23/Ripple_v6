# CLOSE THE LOOP — Snowsight-hour checklist

**Purpose:** take `decisions.total` from **0 → ≥10** by proving the review→decide lane end to end.
Dependency-ordered. Do it top to bottom. **A00 (build lane) before A03 (revoke), with a smoke-test between** — that ordering is load-bearing; A03 is irreversible.

**Chris's decision (2026-07-14):** one build role — **`RIPPLE_TRANSFORM_RW`** — both runs dbt *and* owns the `CONNECT` spine. No new `RIPPLE_BUILD_RW`.

**Surfaces you'll use:** Snowsight worksheet (SQL) · Snowsight Admin UI (mint PATs) · your terminal (`.env` swap, smoke-test, dbt, A03).
**Golden rule:** where a step says "statement by statement," do **not** use Run All — some statements are *designed* to fail and Run All stops at the first error.

Legend: ☐ = do it · 🔒 = irreversible · 🟢 = read-only/safe · ↩ = reversible

---

## STEP 0 — pre-flight (🟢 read-only; run in Snowsight as ACCOUNTADMIN)

These two are the facts my reader lane could not see. Their output finalizes Step 4's grant block (which lines to keep, and the ETL warehouse name).

```sql
SHOW GRANTS TO ROLE RIPPLE_TRANSFORM_RW;
SHOW WAREHOUSES;
```

☐ Paste both back. **Then I fill in Step 4 and Step 5's `<ETL_WH>` and we resume.**
- From #1: which of Step 4's dbt-half grants `RIPPLE_TRANSFORM_RW` already has (so we don't re-grant), and whether it already has `USAGE` on the ETL warehouse.
- From #2: the real ETL/build warehouse name (`RIPPLE_WH` unless it's `DBT_WH` or similar) — the one that is **not** `SERVE_WH` and **not** `COMPUTE_WH`.

---

## STEP 1 — provision the review write lane (Snowsight worksheet, as ACCOUNTADMIN/SECURITYADMIN) ↩

Run **`scripts/provision_review_lane.sql`** top to bottom (it's idempotent/guarded; Run All is fine here).
Builds: `LIBRARY_META.REVIEW` schema + append-only `DECISIONS` table + `RIPPLE_REVIEW_WRITER` role, re-points `V_LEADS_PUBLISHED` at the living table, renames the empty `CONNECT.DECISIONS` stub.

☐ Expect: the two VERIFY queries at the bottom each return one row.
⚠ Its **last line** (Part 5 — `GRANT SELECT … LEAD_QUEUE …`) will error *"does not exist"* — that's expected; `LEAD_QUEUE` isn't built until Step 7. Everything above it has applied. Re-run that one line after Step 7.

---

## STEP 2 — mint the review PAT (Snowsight Admin UI) ↩

☐ Mint a PAT **restricted to role `RIPPLE_REVIEW_WRITER`**, with an expiry.
☐ Add it to `library-onboarding/.env` as **`RIPPLE_REVIEW_PAT`** (this is a *new* key; leave `SNOWFLAKE_PAT` alone for now).

---

## STEP 3 — prove the wall (Snowsight worksheet, **statement by statement**) 🟢

Run **`scripts/verify_review_lane.sql`** one statement at a time, as `RIPPLE_REVIEW_WRITER`.
The failures ARE the proof:
- [1] INSERT → **succeeds** (writes the permanent `SMOKE_TEST` proof row)
- [2] UPDATE, [3] DELETE → **PERMISSION DENIED** ← the point (append-only enforced by the DB)
- [4a] read `REGISTRY.SOURCE_REGISTRY` / `"CONNECT".LEADS`, [4b] read `LIBRARY_RAW…` → **not authorized** ← the writer sees only its one table
- [5] read the `SMOKE_TEST` row → **≥1 row**

☐ If [2]/[3]/[4] *succeed*, STOP — the lane is mis-provisioned; re-check grants in `provision_review_lane.sql`.

---

## STEP 4 — A00: the build lane grants (Snowsight worksheet, as ACCOUNTADMIN) ↩ (mostly)

> **DRAFT — finalized after Step 0.** `<BUILD_ROLE>` = `RIPPLE_TRANSFORM_RW`. Fill `<ETL_WH>` from Step 0.
> The **(b) spine ownership** block is the genuinely new capability. The **(a) dbt** lines are trimmed to only what Step 0 shows missing.

```sql
-- (b) SPINE — move CONNECT ownership onto the build role (Chris's call).
--     COPY CURRENT GRANTS preserves RIPPLE_READER's existing SELECTs on those tables.
GRANT USAGE, CREATE TABLE ON SCHEMA LIBRARY_META."CONNECT" TO ROLE RIPPLE_TRANSFORM_RW;
GRANT OWNERSHIP ON ALL TABLES    IN SCHEMA LIBRARY_META."CONNECT" TO ROLE RIPPLE_TRANSFORM_RW COPY CURRENT GRANTS;
GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA LIBRARY_META."CONNECT" TO ROLE RIPPLE_TRANSFORM_RW;

-- (a) dbt — keep ONLY the lines Step 0 proves RIPPLE_TRANSFORM_RW is missing:
GRANT USAGE ON DATABASE LIBRARY_STAGING, LIBRARY_MARTS, LIBRARY_RAW, LIBRARY_META TO ROLE RIPPLE_TRANSFORM_RW;
GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA LIBRARY_STAGING.DBT_CROGERS TO ROLE RIPPLE_TRANSFORM_RW;
GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA LIBRARY_MARTS.DBT_CROGERS   TO ROLE RIPPLE_TRANSFORM_RW;
GRANT SELECT ON ALL TABLES    IN SCHEMA LIBRARY_RAW.LANDING TO ROLE RIPPLE_TRANSFORM_RW;
GRANT SELECT ON FUTURE TABLES IN SCHEMA LIBRARY_RAW.LANDING TO ROLE RIPPLE_TRANSFORM_RW;
GRANT SELECT ON VIEW LIBRARY_META."CONNECT".V_LEADS_PUBLISHED TO ROLE RIPPLE_TRANSFORM_RW;

-- (c) ETL warehouse — fill from Step 0. NEVER SERVE_WH.
GRANT USAGE ON WAREHOUSE <ETL_WH> TO ROLE RIPPLE_TRANSFORM_RW;
```

☐ Then mint a PAT **restricted to `RIPPLE_TRANSFORM_RW`**, expiry set — this is the **build PAT** (Step 5 uses it).
Watch-item, deferred to Step 5 smoke-test: the spine runs `CREATE SCHEMA IF NOT EXISTS "LIBRARY_META"."CONNECT"`; if that trips as a non-owner, add `GRANT CREATE SCHEMA ON DATABASE LIBRARY_META TO ROLE RIPPLE_TRANSFORM_RW;` (or patch `connect/store.py`).

---

## STEP 5 — swap the lane + smoke-test (terminal) ↩

☐ In `library-onboarding/.env`, point the default lane at the build PAT (keep a copy of the old values to swap back after Step 7):
```
SNOWFLAKE_PAT=<the RIPPLE_TRANSFORM_RW build PAT>
SNOWFLAKE_ROLE=RIPPLE_TRANSFORM_RW
SNOWFLAKE_WAREHOUSE=<ETL_WH>
```
☐ Smoke-test — **dry-run, writes nothing** (writes only with `--run`):
```
python -m connect leads
```
Expect: it connects as `RIPPLE_TRANSFORM_RW` and prints lead previews. If it errors on schema/ownership, that's the watch-item above — fix the grant, re-run. **Do not proceed to Step 6 until this is clean.**

---

## STEP 6 — A03: revoke the straggler PATs (terminal) 🔒

Only now that the build lane is proven.
```
python scripts/revoke_straggler_pats.py        # preview first
python scripts/revoke_straggler_pats.py --apply # if the preview is right
```
☐ 🔒 Irreversible. This is why it comes after Step 5, not before.

---

## STEP 7 — build the queue mart (terminal, build lane) ↩

```
cd library-onboarding/ripple_dbt
dbt build --select marts.review
```
Materializes `LIBRARY_MARTS.DBT_CROGERS.LEAD_QUEUE`.
☐ If dbt errors replacing an existing `DBT_CROGERS` object it doesn't own, grant ownership of those the same way as Step 4(b) (`GRANT OWNERSHIP ON ALL TABLES/VIEWS IN SCHEMA … DBT_CROGERS … COPY CURRENT GRANTS`).
☐ Back in Snowsight, re-run `provision_review_lane.sql`'s **last line** (the `LEAD_QUEUE` grant that errored in Step 1).
☐ Swap `.env` back to the reader/serve lane (`RIPPLE_READER` / `SERVE_WH` / the reader PAT) so normal serving isn't left on the build lane.

---

## STEP 8 — let the Atlas see the budget (Snowsight worksheet, as ACCOUNTADMIN) ↩

```sql
GRANT MONITOR ON RESOURCE MONITOR SERVE_MON TO ROLE RIPPLE_READER;
```
☐ (Confirmed missing today — the reader can't see `SERVE_MON` yet. This is what lets the budget meter render.)

---

## AGENT (GREEN) — runs alongside, before the spine rerun

- ☐ Fix the NPPES column-rename break in `connect/entity_index_specs.py` (`PROVIDER_LAST_NAME__LEGAL_NAME` → single-underscore live name) — **must land before** the spine rerun or it crashes.
- ☐ Rerun spine + refresh leads **on the build lane** (preview-then-apply).
- ☐ Verify `LEAD_QUEUE` reconciles (`library-onboarding/ripple_dbt/tests/assert_lead_queue_reconciles.sql`).
- ☐ Export `REVIEW.DECISIONS` → git-committed CSV after each review session (first non-regenerable data).

---

## THE POINT — the top-10 review (Reading Room, ~1–2 hrs)

☐ Review **exactly the top 10 `LEAD_QUEUE` rows.** Every row gets a verdict: confirm / reject / needs-work.
**Ten rows in `REVIEW.DECISIONS` = success, whatever the verdicts.** All-rejects is a real finding about detector precision, not a failed phase.

**DONE (warehouse-checkable):** `V_STATE decisions.total ≥ 10`.
