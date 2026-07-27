# Plan: Data Quality Gate for Bulk Loaders

## Context

**The gap:** Bulk loaders (FAERS, NEISS, SEC 13F, CourtListener, ARCOS, EPA ECHO, DOL Enforce) operate outside the governance loop. The standard `ingest.py` path has density gating, INGEST_RUNS logging, and status tracking — none of which the bulk scripts use.

**What exists today:**
- `scripts/degenerate_load_detector.py` — read-only scanner that flags tables where 85%+ of columns have <=1 distinct value (dead-scrape signature). NOT automated.
- `scripts/build_freshness_ledger.py` — measures DATA_THROUGH (max date in data columns) per source. Runs on its own cadence, not triggered post-load.
- `LIBRARY_META.INGEST_LOGS.INGEST_RUNS` — the official load-log table. Bulk loaders never write to it.
- `scripts/heartbeat.py` ACQUIRE stage — checks recipe exit code only. No post-load validation.
- Each loader prints row counts to stdout but never asserts or persists them.

**Current per-loader behavior:**
```
Download -> SHA-256 -> write_pandas/COPY INTO -> print row count -> done
```

**Desired behavior:**
```
Download -> SHA-256 -> write_pandas/COPY INTO -> QUALITY GATE -> log INGEST_RUNS -> done (or FAIL)
```

---

## Implementation

### Step 1: Add `bulk_log_run()` and `assess_bulk_load()` to `_bulk_load_utils.py`

This is the centralized quality gate. Every bulk loader already imports `_bulk_load_utils`, so adding it here gives us one place to maintain.

```python
def assess_bulk_load(conn, table_fqn, run_id, expected_min_rows=0, prev_row_count=None):
    """Post-load quality gate. Returns (passed: bool, report: dict)."""
    report = {}
    
    # 1. Row count - did anything land?
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_fqn}")
    actual = cur.fetchone()[0]
    report["row_count"] = actual
    report["row_check"] = actual > expected_min_rows
    
    # 2. Row regression - did we lose rows? (only if prev known)
    if prev_row_count and actual < prev_row_count * 0.5:
        report["regression"] = True
        report["regression_detail"] = f"{actual} vs prev {prev_row_count} (>50% drop)"
    else:
        report["regression"] = False
    
    # 3. Density gate - sample 5000 rows, check for degenerate columns
    #    (reuses degenerate_load_detector logic inline)
    data_cols = [r[0] for r in cur.execute(
        f"SELECT COLUMN_NAME FROM {db}.INFORMATION_SCHEMA.COLUMNS WHERE ...").fetchall()
        if r[0] not in META_COLS]
    sample_query = f"SELECT {','.join(data_cols)} FROM {table_fqn} SAMPLE (5000 ROWS)"
    # count distinct per col, flag if <=1 distinct
    degenerate_frac = count_degenerate(cur, table_fqn, data_cols, sample=5000)
    report["degenerate_frac"] = degenerate_frac
    report["density_check"] = degenerate_frac < 0.85
    
    passed = report["row_check"] and not report["regression"] and report["density_check"]
    report["passed"] = passed
    cur.close()
    return passed, report


def bulk_log_run(conn, source_id, table_fqn, run_id, sha256, row_count, status, dq_report=None):
    """Write to INGEST_RUNS — same schema as ingest._log_run()."""
    conn.cursor().execute("""
        INSERT INTO LIBRARY_META.INGEST_LOGS.INGEST_RUNS 
        (SOURCE_ID, LANDING_TABLE, RUN_ID, SHA256, ROW_COUNT, STATUS, DQ_REPORT, RUN_AT)
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP())
    """, (source_id, table_fqn, run_id, sha256, row_count, status,
          json.dumps(dq_report) if dq_report else None))
```

Location: [scripts/_bulk_load_utils.py](scripts/_bulk_load_utils.py) — append after existing helpers (line ~260).

---

### Step 2: Wire into each active loader

Each loader gets 3 lines at the end, after the existing print statement:

```python
from _bulk_load_utils import assess_bulk_load, bulk_log_run

passed, report = assess_bulk_load(conn, TABLE_FQN, run_id)
bulk_log_run(conn, SOURCE_ID, TABLE_FQN, run_id, sha, report["row_count"],
             "success" if passed else "dq_failed", report)
if not passed:
    print(f"[DQ FAILED] {report}")
    sys.exit(1)
```

Files to modify:
- `scripts/fda_faers_load.py` — after line ~153 (per-quarter summary)
- `scripts/cpsc_neiss_load.py` — after line ~108 (per-year summary)
- `scripts/sec_13f_load.py` — after line ~122 (per-zip summary)
- `scripts/courtlistener_dockets_load.py` — after line ~117 (count print)
- `scripts/dea_arcos_full_load.py` — after line ~123 (count print)
- `scripts/epa_echo_bulk_load.py` — after load loop
- `scripts/dol_enforce_bulk_load.py` — after load loop

---

### Step 3: Add heartbeat post-ACQUIRE verify

In `scripts/heartbeat.py`, after the `run_guarded()` call succeeds (line ~870), add a lightweight verify:

```python
# After rc=0 from run_guarded:
if rc == 0 and recipe.get("verify_table"):
    verify_count = _quick_count(recipe["verify_table"])
    if verify_count == 0:
        log(f"[ACQUIRE] {sid} exited 0 but verify_table is EMPTY — marking failed")
        status = "dq_failed"
```

This requires adding a `verify_table` field to `acquire_recipes.json` for each recipe (the landing table name to spot-check).

---

### Step 4: DQ failure file (local fallback)

When `bulk_log_run` writes to INGEST_RUNS and the gate failed, also append to `outputs/_dq_failures.jsonl`:

```python
if not passed:
    with open(REPO / "outputs/_dq_failures.jsonl", "a") as f:
        f.write(json.dumps({"ts": utcnow, "source": source_id, **report}) + "\n")
```

This ensures failures are visible even when the Snowflake connection dies (the exact scenario the Jul 25 audit flagged at Area 4).

---

## Verification

1. **Dry run each loader** with `--dry-run` or on a small partition — confirm the gate runs and logs to INGEST_RUNS.
2. **Force a failure** — load a known-degenerate table (empty or 1-distinct-value) and confirm exit(1) + JSONL entry.
3. **Check INGEST_RUNS** — `SELECT * FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS WHERE RUN_AT > DATEADD('hour', -1, CURRENT_TIMESTAMP())` should show the new bulk-loader entries.
4. **Heartbeat integration** — run `python scripts/heartbeat.py --acquire-optin --dry-run` and confirm it respects the new `verify_table` field.

---

## Critical Files

- `scripts/_bulk_load_utils.py` — Where the gate logic lives (centralized for all loaders)
- `scripts/heartbeat.py` (~line 870) — Post-ACQUIRE verify hook
- `scripts/acquire_recipes.json` — Add `verify_table` field per recipe
- `scripts/degenerate_load_detector.py` — Logic to reuse for density check
- `infra/ddl/01_meta_base_tables.sql` — May need to add DQ_REPORT column to INGEST_RUNS
