"""Durable, resumable checkpoint for windowed loads.

An interrupted scrape (PAT death, SUSPEND, network) resumes per-window instead of
restarting -- and because the API pagination is decoupled from the Snowflake write,
an expired token blocks only the final landing, never the progress already banked.

Pure `CheckpointSet` state-machine (unit-tested) + the DDL for the Snowflake table
+ thin live read/write helpers (`# pragma: no cover`).
"""
from __future__ import annotations

from dataclasses import dataclass, field

CHECKPOINT_TABLE = "LIBRARY_META.INGEST_LOGS.LOAD_CHECKPOINT"

CHECKPOINT_DDL = f"""
CREATE TABLE IF NOT EXISTS {CHECKPOINT_TABLE} (
  SOURCE_ID       VARCHAR,
  WINDOW_KEY      VARCHAR,
  LAST_PAGE       NUMBER,
  ENVELOPE_COUNT  NUMBER,
  STATUS          VARCHAR,        -- pending | in_progress | done | overflow
  UPDATED_AT      TIMESTAMP_NTZ,
  PRIMARY KEY (SOURCE_ID, WINDOW_KEY)
)
""".strip()


@dataclass
class CheckpointSet:
    """In-memory view of one source's window progress -- mirrors the table. The
    pure logic (what's left, where to resume, is a window done) lives here and is
    unit-tested; the live helpers below just sync it to Snowflake."""

    source_id: str
    state: dict = field(default_factory=dict)   # window_key -> {last_page, status, envelope_count}

    def mark(self, window_key, *, last_page=0, status="in_progress", envelope_count=None):
        rec = self.state.setdefault(window_key, {"last_page": 0, "status": "pending", "envelope_count": None})
        rec["last_page"] = max(rec["last_page"], int(last_page))
        rec["status"] = status
        if envelope_count is not None:
            rec["envelope_count"] = envelope_count
        return self

    def is_done(self, window_key) -> bool:
        return self.state.get(window_key, {}).get("status") == "done"

    def resume_page(self, window_key) -> int:
        """Where to restart: the page AFTER the last fully-committed one (0 = fresh).
        Only an `in_progress` window resumes mid-way; `done` is skipped by `pending`."""
        rec = self.state.get(window_key)
        return (rec["last_page"] + 1) if rec and rec["status"] == "in_progress" else 0

    def pending(self, all_window_keys):
        """The windows still to do, in input order (done ones skipped)."""
        return [k for k in all_window_keys if not self.is_done(k)]


def load_checkpoints(conn, source_id):  # pragma: no cover - live I/O
    cur = conn.cursor()
    try:
        cur.execute(
            f"SELECT WINDOW_KEY, LAST_PAGE, STATUS, ENVELOPE_COUNT FROM {CHECKPOINT_TABLE} WHERE SOURCE_ID=%s",
            (source_id,),
        )
        cs = CheckpointSet(source_id)
        for wk, lp, st, ec in cur.fetchall():
            cs.state[wk] = {"last_page": int(lp or 0), "status": st, "envelope_count": ec}
        return cs
    finally:
        cur.close()


def save_checkpoint(conn, source_id, window_key, *, last_page, status, envelope_count=None):  # pragma: no cover
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            MERGE INTO {CHECKPOINT_TABLE} t
            USING (SELECT %s AS SOURCE_ID, %s AS WINDOW_KEY) s
              ON t.SOURCE_ID = s.SOURCE_ID AND t.WINDOW_KEY = s.WINDOW_KEY
            WHEN MATCHED THEN UPDATE SET
              LAST_PAGE = %s, STATUS = %s,
              ENVELOPE_COUNT = COALESCE(%s, t.ENVELOPE_COUNT), UPDATED_AT = CURRENT_TIMESTAMP()
            WHEN NOT MATCHED THEN INSERT (SOURCE_ID, WINDOW_KEY, LAST_PAGE, ENVELOPE_COUNT, STATUS, UPDATED_AT)
              VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP())
            """,
            (source_id, window_key, last_page, status, envelope_count,
             source_id, window_key, last_page, envelope_count, status),
        )
        conn.commit()
    finally:
        cur.close()
