"""Live table/column discovery — driven off the catalog, never a hardcoded list.

The reach of the instrument is a QUERY against the current state of the
warehouse, so a source that lands next month is chartable with zero wiring:

  find(term)     two live arms, merged:
                   arm 1  LIBRARY_META.REGISTRY.CATALOG (sources; lifecycle-gated,
                          sampled sources BADGED not hidden)
                   arm 2  LIBRARY_MARTS INFORMATION_SCHEMA base tables — the typed
                          marts CATALOG structurally can't see (multi-source marts
                          like the POLITICS suite have no catalog row at all)
                 FRIENDLY_LAYER decorates names when it has them (LEFT-join
                 semantics — a stale snapshot can not hide a live table).
  shelves()      the browse menu: live CATALOG grouped by domain + the mart arm.
  columns(fqn)   DESCRIBE TABLE — metadata-only, no warehouse, works on ANY fqn
                 (portal tables included; discovery visibility never gates access).
  profile(fqn)   one single-pass probe over (SELECT * FROM fqn LIMIT n) — never
                 SAMPLE (n ROWS), which scans the whole table. Classifies each
                 column's chart role; all-digit strings are numeric, never dates.
  cast_sql(fqn)  drafts the casted SELECT that makes an all-TEXT landing table
                 chartable — the starting point Chris edits, not a black box.
  snapshot_write / snapshot_read
                 the bench's browse surface: find('') + shelves() written to
                 one disk file, read back with zero warehouse contact. Refresh
                 is an explicit button, never a background job.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from viz import guard, sqlrun

FIND_TTL_S = 30 * 60
PROFILE_TTL_S = 7 * 24 * 3600
PROFILE_MAX_TEXT_COLS = 80


def _rows(sql: str, params: tuple = ()):  # small helper on the shared lane
    cur = sqlrun.connect().cursor()
    try:
        cur.execute(sql, params or ())
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


# --------------------------------------------------------------------------- #
# find + shelves
# --------------------------------------------------------------------------- #
def find(term: str = "", include_portals: bool = False, refresh: bool = False) -> list[dict]:
    """Chartable objects matching `term`. Every row carries the BEST fqn to
    chart (typed mart when one exists, else the raw landing table)."""
    key = f"find::{term.lower()}::{include_portals}"
    cached = sqlrun._cache_get(key, FIND_TTL_S)
    if cached and not refresh:
        return cached

    like = f"%{term}%"
    src_sql = """
        SELECT SOURCE_ID, NAME, DOMAIN_PRIMARY, LIFECYCLE, IS_SAMPLE,
               LANDED_ROW_COUNT, LANDING_FQN, JOIN_KEYS_STD
        FROM LIBRARY_META.REGISTRY.CATALOG
        WHERE LIFECYCLE IN ('landed','modeled','sampled')
          AND LANDED_ROW_COUNT > 0
          AND (%s = '' OR SOURCE_ID ILIKE %s OR NAME ILIKE %s OR DOMAIN_PRIMARY ILIKE %s)
    """
    if not include_portals:
        src_sql += " AND SOURCE_ID NOT ILIKE 'portal_%%'"
    src_sql += " ORDER BY LANDED_ROW_COUNT DESC"
    sources = _rows(src_sql, (term, like, like, like))

    mart_sql = """
        SELECT TABLE_SCHEMA, TABLE_NAME, ROW_COUNT
        FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
          AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
          AND NOT STARTSWITH(TABLE_SCHEMA, '_')
          AND (%s = '' OR TABLE_SCHEMA ILIKE %s OR TABLE_NAME ILIKE %s)
        ORDER BY ROW_COUNT DESC NULLS LAST
    """
    marts = _rows(mart_sql, (term, like, like))
    friendly = _friendly_names()

    out: list[dict] = []
    mart_source_ids = set()
    for m in marts:
        fqn = f"LIBRARY_MARTS.{m['TABLE_SCHEMA']}.{m['TABLE_NAME']}"
        parsed = (m["TABLE_NAME"].split("__", 1)[1].lower()
                  if "__" in m["TABLE_NAME"] else None)
        if parsed:
            mart_source_ids.add(parsed)
        f = friendly.get(fqn, {})
        out.append({
            "kind": "mart", "fqn": fqn,
            "name": f.get("FRIENDLY_NAME") or m["TABLE_NAME"],
            "one_liner": f.get("ONE_LINER") or "",
            "domain": f.get("FRIENDLY_DOMAIN") or m["TABLE_SCHEMA"].lower(),
            "lifecycle": "modeled", "is_sample": False,
            "rows": m.get("ROW_COUNT"), "source_id": parsed,
        })
    for s in sources:
        sid = (s["SOURCE_ID"] or "").lower()
        if sid in mart_source_ids:
            continue  # the typed mart row already covers this source better
        f = friendly.get(s.get("LANDING_FQN") or "", {})
        out.append({
            "kind": "source", "fqn": s["LANDING_FQN"],
            "name": f.get("FRIENDLY_NAME") or s["NAME"] or sid,
            "one_liner": f.get("ONE_LINER") or "",
            "domain": s["DOMAIN_PRIMARY"], "lifecycle": s["LIFECYCLE"],
            "is_sample": bool(s.get("IS_SAMPLE")),
            "rows": s.get("LANDED_ROW_COUNT"), "source_id": sid,
            "join_keys": s.get("JOIN_KEYS_STD"),
        })
    sqlrun._cache_put(key, out)
    return out


_FRIENDLY_MEMO: dict = {"t": 0.0, "v": None}


def _friendly_names() -> dict:
    """FRIENDLY_LAYER decoration keyed on OBJECT_FQN. Decoration ONLY — it is a
    hand-refreshed snapshot (thelibrary_refresh.py) and may lag the live catalog.
    Memoized in-process (30 min) so per-term find() cache misses don't re-read
    the whole table."""
    import time
    if _FRIENDLY_MEMO["v"] is not None and time.time() - _FRIENDLY_MEMO["t"] < FIND_TTL_S:
        return _FRIENDLY_MEMO["v"]
    try:
        rows = _rows("""SELECT OBJECT_FQN, FRIENDLY_NAME, ONE_LINER, FRIENDLY_DOMAIN
                        FROM LIBRARY_META.REGISTRY.FRIENDLY_LAYER""")
        out = {r["OBJECT_FQN"]: r for r in rows}
    except Exception:
        out = {}
    _FRIENDLY_MEMO.update(t=time.time(), v=out)
    return out


def shelves() -> list[dict]:
    """The browse menu, live: domains by real data volume + the mart arm."""
    dom = _rows("""
        SELECT DOMAIN_PRIMARY AS DOMAIN, COUNT(*) AS SOURCES,
               SUM(COALESCE(MART_ROW_COUNT, LANDED_ROW_COUNT, 0)) AS TOTAL_ROWS
        FROM LIBRARY_META.REGISTRY.CATALOG
        WHERE LIFECYCLE IN ('landed','modeled','sampled') AND LANDED_ROW_COUNT > 0
          AND SOURCE_ID NOT ILIKE 'portal_%'
        GROUP BY 1 ORDER BY 3 DESC""")
    marts = _rows("""
        SELECT TABLE_SCHEMA AS DOMAIN, COUNT(*) AS SOURCES, SUM(ROW_COUNT) AS TOTAL_ROWS
        FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
          AND NOT STARTSWITH(TABLE_SCHEMA, '_')
        GROUP BY 1 ORDER BY 3 DESC NULLS LAST""")
    return [{"arm": "catalog", **d} for d in dom] + [{"arm": "marts", **m} for m in marts]


# --------------------------------------------------------------------------- #
# snapshot — the bench's browse surface, served entirely from disk
# --------------------------------------------------------------------------- #
SNAPSHOT_PATH = sqlrun.CACHE_PATH.parent / "bench_catalog.json"


def snapshot_write(path: Path | None = None) -> dict:
    """Rebuild the on-disk catalog snapshot. This is the ONLY discovery call
    that is allowed to cost warehouse time on purpose: one find('') pass and
    one shelves() pass (two live queries when the 30-min find cache is cold).

    Everything the bench browses afterwards comes from this file — so browsing
    never wakes the warehouse and never costs anything Chris didn't press a
    button for."""
    path = Path(path) if path else SNAPSHOT_PATH
    snap = {
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "tables": find("", refresh=True),
        "shelves": shelves(),
        "budget": sqlrun.budget_line(refresh=True),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(snap, indent=1, default=str), encoding="utf-8")
    os.replace(tmp, path)
    return snap


def snapshot_read(path: Path | None = None) -> dict | None:
    """The snapshot as written, or None when there isn't one yet. Pure disk —
    this function must NEVER open a warehouse connection."""
    path = Path(path) if path else SNAPSHOT_PATH
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# --------------------------------------------------------------------------- #
# columns + profile + cast_sql
# --------------------------------------------------------------------------- #
def columns(fqn: str) -> list[dict]:
    """DESCRIBE TABLE — metadata-only (no warehouse), any 2-3 part identifier."""
    safe = guard.validate_fqn(fqn)
    rows = _rows(f"DESCRIBE TABLE {safe}")
    return [{"column": r.get("name"), "sf_type": r.get("type")} for r in rows]


def profile(fqn: str, n: int = 10_000, refresh: bool = False) -> list[dict]:
    """Per-column chart roles for any table, cheap: one pass over LIMIT n rows.

    Typed columns classify straight off DESCRIBE; TEXT columns get TRY_TO_NUMBER /
    TRY_TO_DATE probes. Date rule (live-proven trap): a value only counts as a
    date when TRY_TO_DATE succeeds AND TRY_TO_NUMBER fails — otherwise FEC image
    numbers, NPIs and ZIPs land on time axes as epoch dates."""
    safe = guard.validate_fqn(fqn)
    key = f"profile::{safe}::{n}"
    cached = sqlrun._cache_get(key, PROFILE_TTL_S)
    if cached and not refresh:
        return cached

    cols = columns(safe)
    typed, text_cols = [], []
    for c in cols:
        name, sf = c["column"], (c["sf_type"] or "").upper()
        if name.upper() in ("_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"):
            continue
        if sf.startswith(("NUMBER", "FLOAT", "INT", "DECIMAL")):
            typed.append({"column": name, "role": "numeric", "how": "typed"})
        elif sf.startswith(("DATE", "TIMESTAMP")):
            typed.append({"column": name, "role": "date", "how": "typed"})
        else:
            text_cols.append(name)

    probed: list[dict] = []
    capped = text_cols[:PROFILE_MAX_TEXT_COLS]
    if capped:
        exprs = ["COUNT(*) AS _N"]
        for i, name in enumerate(capped):
            q = guard.quote_ident(name)
            v = f"TO_VARCHAR({q})"
            exprs += [
                f"COUNT({q}) AS NN_{i}",
                f"COUNT(TRY_TO_NUMBER({v})) AS NUM_{i}",
                f"COUNT(CASE WHEN TRY_TO_DATE({v}) IS NOT NULL AND TRY_TO_NUMBER({v}) IS NULL THEN 1 END) AS DT_{i}",
                f"APPROX_COUNT_DISTINCT({q}) AS CARD_{i}",
            ]
        row = _rows(f"SELECT {', '.join(exprs)} FROM (SELECT * FROM {safe} LIMIT {int(n)})")[0]
        total = max(int(row["_N"]), 1)
        for i, name in enumerate(capped):
            nonnull = int(row[f"NN_{i}"] or 0)
            num_r = (row[f"NUM_{i}"] or 0) / max(nonnull, 1)
            dt_r = (row[f"DT_{i}"] or 0) / max(nonnull, 1)
            card = int(row[f"CARD_{i}"] or 0)
            hint = any(t in name.upper() for t in ("DATE", "_DT", "YEAR", "MONTH", "TIME"))
            digit_date = False
            if nonnull == 0:
                role = "empty"
            elif dt_r > 0.9:
                role = "date"          # real date strings
            elif hint and num_r > 0.9:
                role = "date"          # YYYYMMDD-style all-digit column with a date name
                digit_date = True      # -> must NEVER be cast with bare TRY_TO_DATE
                                       #    (Snowflake parses digits as epoch seconds)
            elif num_r > 0.9:
                role = "numeric"
            elif card <= 100:
                role = "category"
            else:
                role = "text"
            probed.append({"column": name, "role": role, "how": "probed",
                           "digit_date": digit_date,
                           "nonnull_pct": round(100 * nonnull / total, 1),
                           "distinct_sampled": card})
    skipped = [{"column": c, "role": "text", "how": "skipped (col cap)"}
               for c in text_cols[PROFILE_MAX_TEXT_COLS:]]
    out = typed + probed + skipped
    sqlrun._cache_put(key, out)
    return out


def cast_sql(fqn: str, n: int = 10_000) -> str:
    """Draft the casted SELECT that makes an all-TEXT landing table chartable.
    This is a STARTING POINT to edit, not a hidden layer — it goes in the card."""
    safe = guard.validate_fqn(fqn)
    lines = []
    for p in profile(fqn, n=n):
        q = guard.quote_ident(p["column"])
        if p["how"] == "typed":
            lines.append(f"    {q}")
        elif p["role"] == "numeric":
            lines.append(f"    TRY_TO_NUMBER({q}) AS {q}")
        elif p["role"] == "date" and p.get("digit_date"):
            # bare TRY_TO_DATE on digits parses EPOCH SECONDS -> year 2445 dates
            lines.append(f"    TRY_TO_DATE(TO_VARCHAR({q}), 'YYYYMMDD') AS {q}  -- all-digit date: verify the format")
        elif p["role"] == "date":
            lines.append(f"    TRY_TO_DATE({q}) AS {q}")
        elif p["role"] in ("category", "text"):
            lines.append(f"    {q}")
        # 'empty' columns are dropped from the draft on purpose
    body = ",\n".join(lines) if lines else "    *"
    return f"SELECT\n{body}\nFROM {safe}"
