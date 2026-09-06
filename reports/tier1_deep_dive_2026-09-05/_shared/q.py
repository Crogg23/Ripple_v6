"""Query helper: run SQL through the Python door, log every statement + row count + elapsed."""
from __future__ import annotations
import sys, time, json
from pathlib import Path
_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO))
from connect import db  # noqa

LOG = None

def open_log(path):
    global LOG
    LOG = open(path, "a")

def run(sql: str, label: str = ""):
    conn = db.connect()
    t = time.time()
    try:
        out = db.dicts(conn, sql)
    finally:
        conn.close()
    el = round(time.time() - t, 1)
    if LOG:
        LOG.write(json.dumps({"label": label, "rows": len(out), "secs": el, "sql": sql.strip()}) + "\n"); LOG.flush()
    print(f"[{label}] {len(out)} rows, {el}s", file=sys.stderr)
    return out
