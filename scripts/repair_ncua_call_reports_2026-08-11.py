"""Repair defect class 2 (2026-08-11 verification report): FED_NCUA_CALL_REPORTS
was loaded from the WRONG member of NCUA's quarterly call-report zip -- it holds
the AcctDesc account-description dictionary, not call-report data.

This loads the CORRECT members from the latest quarterly zip
(call-report-data-2026-03.zip) into NEW landing tables:

    FOICU.txt  -> LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS_FOICU
                  (credit union identity roster: charter number, name, city,
                   state, RSSD, peer group)
    FS220.txt  -> LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS_FS220
                  (main financial statement: ACCT_010 = total assets, etc.)

The bad table is NOT touched -- dropping it needs a human-run one-liner
(DROP is classifier-blocked by policy):

    DROP TABLE LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS;

Uses the shared bulk-load machinery (_load_bytes: dtype=str, no-silent-truncate
guard, post-write quality gate) and logs each load to INGEST_RUNS.
Members are matched by EXACT filename, never substring.
"""
from __future__ import annotations

import hashlib
import io
import sys
import uuid
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _bulk_load_utils import _load_bytes, bulk_log_run, new_conn  # noqa: E402

ZIP_URL = "https://ncua.gov/files/publications/analysis/call-report-data-2026-03.zip"

# Exact zip-member name -> landing table. Whole-name match only.
MEMBERS = {
    "FOICU.txt": "FED_NCUA_CALL_REPORTS_FOICU",
    "FS220.txt": "FED_NCUA_CALL_REPORTS_FS220",
}


def main() -> int:
    print(f"downloading {ZIP_URL}")
    resp = requests.get(ZIP_URL, timeout=600)
    resp.raise_for_status()
    zip_bytes = resp.content
    print(f"  {len(zip_bytes):,} bytes")

    conn = new_conn()
    failures = 0
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = set(zf.namelist())
        for member, table in MEMBERS.items():
            if member not in names:  # exact match, never substring
                print(f"  MISSING member {member!r} in zip -- aborting this table")
                failures += 1
                continue
            content = zf.read(member)
            sha = hashlib.sha256(content).hexdigest()
            run_id = str(uuid.uuid4())
            print(f"  loading {member} ({len(content):,} bytes) -> {table}")
            try:
                n = _load_bytes(conn, content, table)
                bulk_log_run(conn, table, run_id, sha256=sha, row_count=n,
                             status="success",
                             message=f"repair 2026-08-11: correct member {member}",
                             source_url=ZIP_URL, file_bytes=len(content))
                print(f"    OK {n:,} rows")
            except Exception as e:
                failures += 1
                bulk_log_run(conn, table, run_id, sha256=sha, status="failed",
                             message=str(e)[:2000], source_url=ZIP_URL,
                             file_bytes=len(content))
                print(f"    FAILED: {e}")
    conn.close()
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
