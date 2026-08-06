"""Shared boilerplate for tiny flat-file (CSV/JSON/XML) snapshot-replace loaders.

Reused by: jpml_pending_mdl_load.py (custom, PDF), oehha_prop65_load.py,
fhfa_suspended_counterparty_load.py, un_consolidated_sanctions_load.py,
uk_sanctions_list_load.py, consolidated_screening_list_load.py,
ice_facility_codes_load.py. Mirrors scripts/cisa_kev_load.py's pattern.
"""
from __future__ import annotations

import hashlib
import sys
import uuid
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest        # noqa: E402
import register      # noqa: E402
import snow          # noqa: E402
from config import settings  # noqa: E402


def load_and_register(df, sid: str, table: str, url: str, register_cfg: dict, run: bool) -> str:
    """Returns a status string: 'preview', 'skipped', 'success', 'empty', or 'partial'.

    Callers should exit non-zero when the returned status is 'empty' or 'partial'.
    """
    print(f"{len(df):,} rows, {len(df.columns)} cols", flush=True)
    dens = ingest.assess_density(df)
    if not run:
        print("\nSAMPLE (first 3):")
        for _, row in df.head(3).iterrows():
            print(" ", dict(list(row.items())[:5]))
        print(f"\ndensity: {dens}")
        print("\nPREVIEW only -- add --run to land.")
        return "preview"

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    sha = hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()
    conn = snow.connect()
    try:
        if settings.skip_if_unchanged:
            last_sha = ingest._latest_success_sha(conn, sid)
            if last_sha == sha:
                print(f"\nskip (sha unchanged) -- sha {sha[:12]} matches last successful run.", flush=True)
                return "skipped"

        # DENSITY GATE: an all-blank frame never overwrites the landing table.
        if dens.get("populated_fraction", 0) < 0.01:
            ended = ingest._utcnow()
            ingest._log_run(conn, sid, run_id, "empty", len(df), None, sha, url, started, ended,
                            f"EMPTY -- {sid}; {len(df):,} rows; density "
                            f"{dens.get('populated_fraction')}. Write SKIPPED, existing table "
                            "LEFT INTACT (not overwritten).")
            print(f"\nEMPTY -- density {dens.get('populated_fraction')}; write skipped, "
                  f"existing table left intact (status=empty)", flush=True)
            return "empty"

        # NEVER-SHRINK: refuse to overwrite a healthy table with a truncated pull.
        # (Same guard as politics/loaders/build_skeleton.py::land().)
        prior = ingest._latest_success_rows(conn, sid)
        if prior and len(df) < prior * 0.98:
            ended = ingest._utcnow()
            guard = int(prior * 0.98)
            ingest._log_run(
                conn, sid, run_id, "partial", len(df), None, sha, url, started, ended,
                f"PARTIAL -- {len(df):,} rows is below the never-shrink floor "
                f"({prior:,} last success x 0.98 = {guard:,}). Existing table "
                f"LEFT INTACT (not overwritten).")
            print(f"\nREFUSED -- {len(df):,} rows < floor {guard:,} (prior {prior:,}) "
                  "-- table kept, status=partial", flush=True)
            return "partial"

        from snowflake.connector.pandas_tools import write_pandas
        snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{settings.raw_database}"."{settings.raw_schema}"')
        out = ingest._stringify(df)
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha
        out.columns = [ingest._sf_col(c) for c in out.columns]
        ok, _c, nrows, _ = write_pandas(conn, out, table_name=table,
                                        database=settings.raw_database, schema=settings.raw_schema,
                                        auto_create_table=True, overwrite=True, quote_identifiers=False)
        if not ok:
            raise RuntimeError("write_pandas failed")
        ended = ingest._utcnow()
        status = "success"
        ingest._log_run(conn, sid, run_id, status, len(df), None, sha, url, started, ended,
                        f"{sid}; {len(df):,} rows; density {dens.get('populated_fraction')}")
        snow.execute(conn, *register._merge_sql(register._build_row(register_cfg, {})))
        print(f"\nLOADED {len(df):,} rows -> {settings.raw_database}.{settings.raw_schema}.{table} "
              f"(status={status}); registered INCLUDE=Y", flush=True)
        n = snow.fetch_scalar(conn, f'SELECT COUNT(*) FROM "{settings.raw_database}"."{settings.raw_schema}"."{table}"')
        print(f"verify: {n:,} rows in landing", flush=True)
        return status
    finally:
        conn.close()
