#!/usr/bin/env python3
"""Land a dataframe into LIBRARY_RAW.LANDING with the usual guards.

Two loaders died on `from build_skeleton import land`. That module now lives only
in the junk drawer, and CLAUDE.md says nothing gets built from the drawer. This
is written fresh against the live modules it always called anyway: `ingest` for
the landing write, the density gate and the run log.

What it guards against, and why each guard exists:

  a truncated pull overwriting a healthy table
      A SAM load once landed 1,000 of ~167,000 rows and logged success. So a
      frame smaller than `shrink_floor` of the last good run is refused, the
      live table is left alone, and the run is logged 'partial'.

  a short pull passing as complete
      Pass `expect_rows` when the source declares its own count, e.g. an API
      envelope total. Falling short logs 'partial', never 'success'.

  a frame that parsed into nothing
      Columns can arrive full of blanks after a schema change. The density gate
      catches that and logs 'empty' instead of 'success'.

Everything lands as TEXT with three stamps, the same as every other loader, so
the freshness ledger and the coverage probe can read it without special cases.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import sys
import uuid
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

import ingest  # noqa: E402
import snow  # noqa: E402

META = [ingest.META_INGESTED_AT, ingest.META_SOURCE_RUN_ID, ingest.META_SRC_SHA256]


def _prior_success_rows(conn, source_id: str) -> int | None:
    """Rows the last good run landed. The house helper, so a database rename in
    config reaches here too."""
    n = ingest._latest_success_rows(conn, source_id)
    return int(n) if n else None


def land(df, source_id: str, url: str, message: str, *,
         table: str | None = None, expect_rows: int | None = None,
         min_rows: int | None = None, shrink_floor: float = 0.98,
         file_bytes: int | None = None, conn=None) -> dict:
    """Write `df` to LIBRARY_RAW.LANDING.<TABLE>, replacing what is there.

    Returns a dict with the status, the row count and the table name. Status is
    one of success, partial, empty or failed, and matches what INGEST_RUNS holds.
    """
    table = (table or source_id).upper()
    run_id = str(uuid.uuid4())
    started = ingest._utcnow()
    n = len(df)
    # Zero here leaves a cliff in the ledger for any size-drift check. The frame
    # as CSV is the honest fallback when the caller did not keep the payload.
    nbytes = int(file_bytes) if file_bytes is not None else len(
        df.to_csv(index=False).encode("utf-8", "replace"))

    own = conn is None
    conn = conn or snow.connect()
    try:
        prior = _prior_success_rows(conn, source_id)

        floor = min_rows if min_rows is not None else (
            int(expect_rows) if expect_rows else None)
        if floor and n < floor:
            msg = (f"REFUSED: pulled {n:,} rows against a declared floor of "
                   f"{floor:,}. Live table left alone. {message}")
            ingest._log_run(conn, source_id, run_id, "partial", n, nbytes, "", url,
                            started, ingest._utcnow(), msg)
            return {"status": "partial", "rows": n, "table": table, "message": msg}

        # expect_rows=0 is how a caller says a real shrink is expected.
        if prior and expect_rows != 0 and n < prior * shrink_floor:
            msg = (f"REFUSED: {n:,} rows against {prior:,} last time. "
                   f"Live table left alone. {message}")
            ingest._log_run(conn, source_id, run_id, "partial", n, nbytes, "", url,
                            started, ingest._utcnow(), msg)
            return {"status": "partial", "rows": n, "table": table, "message": msg}

        # The house stringifier, not astype(object): it also sanitises column
        # names, renders a nullable integer as 1 rather than 1.0, scrubs the
        # literal strings "nan" and "None", and de-duplicates columns.
        out = ingest._stringify(df)
        sha = hashlib.sha256(
            df.to_csv(index=False).encode("utf-8", "replace")).hexdigest()
        out[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
        out[ingest.META_SOURCE_RUN_ID] = run_id
        out[ingest.META_SRC_SHA256] = sha

        ingest._load_landing(conn, out, table, overwrite=True)

        density = ingest.assess_density(out.drop(columns=META, errors="ignore"))
        # Subscript, not .get. assess_density returns "empty", never "ok", and a
        # .get default turned the whole gate into a rubber stamp.
        status = "empty" if density["empty"] else "success"
        note = message if status == "success" else (
            f"EMPTY: {density['reason']}. {ingest._density_note(density)}. {message}")
        ingest._log_run(conn, source_id, run_id, status, n, nbytes, sha, url,
                        started, ingest._utcnow(), note)
        return {"status": status, "rows": n, "table": table, "message": note,
                "sha": sha}
    finally:
        if own:
            conn.close()
