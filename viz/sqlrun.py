"""The guarded read lane: ONE chokepoint between any surface and Snowflake.

Every ad-hoc query — CLI, card, workbench, session loop — runs through run().
What stands between a typed query and the warehouse, in order:

  1. viz.guard.check()          — text guard (fast reject; comments/strings stripped)
  2. claim-table block          — raw LIBRARY_META."CONNECT" claim reads are refused
                                  and rerouted to V_LEADS_PUBLISHED (the libel firewall
                                  extends to ad-hoc SQL; --unsafe-claims force-bakes
                                  the LEAD badge instead)
  3. single-statement execution — plain cursor.execute(), never execute_string
  4. the session lane           — a serving PAT bound to a read-only role when
                                  provisioned (VERIFIED at connect, never assumed
                                  from env-var presence), else the default PAT with
                                  a loud banner
  5. row/cell caps + statement timeout (300s) applied at connect time

Warehouse: SERVE_WH when it exists, else COMPUTE_WH. NEVER RIPPLE_WH/DBT_WH —
those are the pour/dbt lanes.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
for _p in (str(_REPO), str(_LIB)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
try:  # anchor .env to the repo, not the CWD (connect/db.py pattern)
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

from viz import guard  # noqa: E402  (pure, stdlib-only)

DEFAULT_LIMIT_ROWS = 10_000
MAX_LIMIT_ROWS = 100_000
LIMIT_CELLS = 2_000_000
STATEMENT_TIMEOUT_S = 300
SERVE_WH = os.getenv("RIPPLE_SERVE_WH", "SERVE_WH")
FALLBACK_WH = "COMPUTE_WH"
READER_ROLE = os.getenv("RIPPLE_SERVE_ROLE", "RIPPLE_READER")
CACHE_PATH = _REPO / "outputs" / "_viz_cache.json"

_WRITE_PRIVS = ("CREATE", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "OPERATE",
                "MODIFY", "OWNERSHIP", "APPLYBUDGET", "WRITE")

_conn = None
_lane = None        # 'enforced' | 'client-guard'
_lane_notes: list[str] = []
_warehouse = None


class GuardError(Exception):
    """A query the read lane refuses to run (with the reason why)."""


# --------------------------------------------------------------------------- #
# Connection + lane
# --------------------------------------------------------------------------- #
def connect(refresh: bool = False):
    """The read-lane connection (module singleton). Verifies the lane honestly."""
    global _conn, _lane, _warehouse
    if _conn is not None and not refresh:
        return _conn
    import snow  # library-onboarding/snow.py

    _lane_notes.clear()
    serve_pat = (os.getenv("SNOWFLAKE_SERVE_PAT") or "").strip()
    params = {"STATEMENT_TIMEOUT_IN_SECONDS": STATEMENT_TIMEOUT_S,
              "ABORT_DETACHED_QUERY": True}
    # When riding the serve PAT, PIN the reader role (same rule as
    # reading_room/connections.py): the PAT is role-restricted, and without
    # an explicit role snow.connect falls back to SNOWFLAKE_ROLE from .env
    # (ACCOUNTADMIN on this box), which the restricted PAT refuses with
    # error 250001 (live, 2026-08-01).
    serve_role = os.getenv("RIPPLE_SERVE_ROLE", "RIPPLE_READER") \
        if serve_pat else None
    conn = snow.connect(pat=serve_pat or None, role=serve_role,
                        session_parameters=params)
    _conn = conn
    _lane = _verify_lane(conn, expected_reader=bool(serve_pat))
    _warehouse = _pick_warehouse(conn)
    # Default the session onto THE_LIBRARY (the friendly, browsable database) so
    # a Workbench query can name a table as SCHEMA.TABLE instead of always
    # needing the full DATABASE.SCHEMA.TABLE path -- without this, the session
    # has no default database/schema at all and even a real, granted object
    # fails with Snowflake's ambiguous "does not exist or not authorized"
    # (2026-07-30, reported live: THE_LIBRARY.GOVERNMENT.CONGRESS_ROLL_CALL_VOTES
    # unqualified). Queries against LIBRARY_MARTS/LIBRARY_RAW/etc. still need
    # their own database prefix -- a session can only default to one database.
    try:
        conn.cursor().execute("USE DATABASE THE_LIBRARY")
    except Exception as exc:
        # Best-effort convenience default; explicit qualification still works.
        # But swallowing this silently used to mean a lost grant/role change
        # showed up later as Snowflake's generic "does not exist or not
        # authorized" on an unqualified query, with no trace of the real
        # cause -- log it so lane_status() surfaces it instead.
        _lane_notes.append(f"[!!] default database THE_LIBRARY not set: {exc} "
                           "-- unqualified SCHEMA.TABLE queries will fail; "
                           "use the full DATABASE.SCHEMA.TABLE path")
    return conn


def _verify_lane(conn, expected_reader: bool) -> str:
    """'enforced' ONLY when positively proven: the session runs as the reader
    role, cannot switch roles, and the role holds zero write privileges.
    Env-var presence proves nothing — a PAT bound to a fat role would otherwise
    silently flip the banner while keeping the write surface."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT CURRENT_ROLE(), CURRENT_USER()")
        role, _user = cur.fetchone()
        if not expected_reader:
            _lane_notes.append(
                f"[!!] read-only NOT enforced server-side (role {role}) - client guard only. "
                "Provision SNOWFLAKE_SERVE_PAT (see scripts/instrument_snowflake_setup.sql).")
            return "client-guard"
        problems = []
        if role.upper() != READER_ROLE.upper():
            problems.append(f"session role is {role}, expected {READER_ROLE}")
        try:
            cur.execute("USE ROLE ACCOUNTADMIN")
            problems.append("session can switch to ACCOUNTADMIN")
            # the probe itself must never leave the session escalated
            cur.execute(f"USE ROLE {guard.validate_fqn(role)}")
        except Exception:
            pass  # good — role-restricted session
        try:
            cur.execute(f"SHOW GRANTS TO ROLE {guard.validate_fqn(role)}")
            grants = cur.fetchall()
            bad = sorted({r[1] for r in grants
                          if any(str(r[1]).upper().startswith(w) for w in _WRITE_PRIVS)})
            if bad:
                problems.append(f"role holds write privileges: {', '.join(bad)}")
            # a role granted INTO the reader inherits its privileges - direct
            # grants alone cannot prove read-only, so inheritance fails the check
            inherited = sorted({str(r[3]) for r in grants if str(r[2]).upper() == "ROLE"})
            if inherited:
                problems.append(f"role inherits other roles ({', '.join(inherited)}) - cannot prove read-only")
        except Exception as exc:
            problems.append(f"could not audit role grants ({exc})")
        if problems:
            for p in problems:
                _lane_notes.append(f"[!!] NOT enforced: {p}")
            return "client-guard"
        _lane_notes.append(f"[OK] read-only lane enforced (role {role})")
        return "enforced"
    finally:
        cur.close()


def _pick_warehouse(conn) -> str:
    """SERVE_WH if it exists, else COMPUTE_WH. Never the pour/dbt lanes."""
    cur = conn.cursor()
    try:
        # SERVE_WH is env-controlled; sanitize it the same way the USE
        # WAREHOUSE call two lines below does, instead of raw f-string
        # interpolation into the LIKE literal (a stray quote in the env var
        # used to be able to break out of the string).
        cur.execute(f"SHOW WAREHOUSES LIKE '{guard.validate_fqn(SERVE_WH)}'")
        wh = SERVE_WH if cur.fetchall() else FALLBACK_WH
        if wh != SERVE_WH:
            _lane_notes.append(f"[!!] {SERVE_WH} missing - using {FALLBACK_WH} "
                               "(run serve/serve_wh.sql to create the capped serving lane)")
        cur.execute(f"USE WAREHOUSE {guard.validate_fqn(wh)}")
        return wh
    except Exception as exc:
        _lane_notes.append(f"[!!] warehouse pin failed: {exc}")
        return FALLBACK_WH
    finally:
        cur.close()


def lane_status() -> dict:
    """What the lane is running as — for banners and the card header."""
    connect()
    return {"lane": _lane, "warehouse": _warehouse, "notes": list(_lane_notes)}


# --------------------------------------------------------------------------- #
# run()
# --------------------------------------------------------------------------- #
def wrap_limit(sql: str, limit_rows: int) -> str:
    """Wrap a SELECT/WITH in a truncation-detecting LIMIT. Pure (testable).

    The NEWLINES around the inner SQL are load-bearing: a query ending in a
    trailing '-- comment' would otherwise swallow the closing paren and the
    LIMIT clause and fail with an unclosed-paren error."""
    kw = guard.first_keyword(guard.strip_comments_and_strings(sql))
    if kw not in ("SELECT", "WITH"):
        return sql  # SHOW/DESC/EXPLAIN run raw
    inner = sql.rstrip().rstrip(";")
    return f"SELECT * FROM (\n{inner}\n) LIMIT {limit_rows + 1}"


def run(sql: str, limit_rows: int = DEFAULT_LIMIT_ROWS, unsafe_claims: bool = False):
    """Execute one read-only statement. Returns (DataFrame, meta dict).

    meta: rows, truncated, elapsed_s, warehouse, role, lane, as_of, budget,
    claim_refs (non-empty only with unsafe_claims=True — the caller MUST badge).
    """
    import pandas as pd

    ok, reason = guard.check(sql)
    if not ok:
        raise GuardError(reason)

    refs = guard.claim_refs(sql)
    if refs and not unsafe_claims:
        raise GuardError(
            f"raw read of LIBRARY_META.\"CONNECT\".{'/'.join(sorted(refs))} refused - "
            "unreviewed leads are not facts. Query LIBRARY_META.\"CONNECT\".V_LEADS_PUBLISHED "
            "instead (published-only semantics), or pass --unsafe-claims to proceed with a "
            "LEAD badge baked into the chart.")

    limit_rows = min(int(limit_rows or DEFAULT_LIMIT_ROWS), MAX_LIMIT_ROWS)
    conn = connect()
    wrapped = wrap_limit(sql, limit_rows)

    t0 = time.time()
    cur = conn.cursor()
    try:
        try:
            cur.execute(wrapped)
        except Exception as exc:
            if _is_conn_error(exc):  # 60s auto-suspend drops idle connections
                conn = connect(refresh=True)
                cur = conn.cursor()
                cur.execute(wrapped)
            elif _is_monitor_suspended(exc):
                raise GuardError(
                    "warehouse suspended by its resource monitor (budget cap hit). "
                    "No silent fallback - ask Chris to raise the monitor quota "
                    "(ALTER RESOURCE MONITOR ... SET CREDIT_QUOTA) or wait for monthly reset."
                ) from exc
            else:
                raise
        ncols = max(len(cur.description or []), 1)
        eff_rows = max(min(limit_rows, LIMIT_CELLS // ncols), 100)
        try:
            df = cur.fetch_pandas_all()
        except Exception:  # SHOW/DESC results aren't arrow-backed
            data = cur.fetchall()
            df = pd.DataFrame(data, columns=[c[0] for c in (cur.description or [])])
        truncated = len(df) > eff_rows or len(df) > limit_rows
        if truncated:
            df = df.iloc[:min(eff_rows, limit_rows)]
    finally:
        cur.close()

    meta = {
        "rows": len(df),
        "truncated": bool(truncated),
        "elapsed_s": round(time.time() - t0, 2),
        "warehouse": _warehouse,
        "lane": _lane,
        "as_of": _as_of(df),
        "budget": budget_line(),
        "claim_refs": sorted(refs),
    }
    return df, meta


def _as_of(df):
    """Best data-vintage stamp we can prove from the result itself."""
    for col in df.columns:
        if str(col).upper() == "_INGESTED_AT":
            try:
                return str(df[col].max())[:19]
            except Exception:
                return None
    return None


def _is_conn_error(exc) -> bool:
    text = str(exc).lower()
    return any(t in text for t in ("connection is closed", "connection was closed",
                                   "token is expired", "session no longer exists",
                                   "connection reset", "lost connection"))


def _is_monitor_suspended(exc) -> bool:
    text = str(exc).lower()
    # Two different messages, same cause: the warehouse gets SUSPENDED while
    # running, and refuses to RESUME once cold. The resume wording ("cannot be
    # resumed because resource monitor X has exceeded its quota") used to slip
    # past a bare "suspend" check and surface as a raw connector traceback
    # (2026-08-02, live: SERVE_WH / SERVE_MON).
    return "resource monitor" in text and (
        "suspend" in text or "exceeded its quota" in text or "cannot be resumed" in text)


# --------------------------------------------------------------------------- #
# Budget surfacing (cached 10 min — SHOW RESOURCE MONITORS costs a round trip)
# --------------------------------------------------------------------------- #
def budget_line(refresh: bool = False) -> str:
    cached = _cache_get("budget", ttl_s=600)
    if cached and not refresh:
        return cached
    try:
        from loadkit.preflight import live_budget_credits
        conn = connect()
        for monitor in ("SERVE_MON", "RIPPLE_BUDGET"):
            quota, used = live_budget_credits(conn, monitor)
            if quota is not None:
                line = f"{monitor}: {used:.2f}/{quota:.0f} cr used"
                _cache_put("budget", line)
                return line
        line = ("budget meter blind - no monitor visible to this role "
                "(grant MONITOR on SERVE_MON/RIPPLE_BUDGET to the reader role)")
        _cache_put("budget", line)
        return line
    except Exception as exc:
        return f"budget unknown ({exc})"


def _cache_load() -> dict:
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _cache_get(key: str, ttl_s: int):
    entry = _cache_load().get(key)
    if entry and (time.time() - entry.get("t", 0)) < ttl_s:
        return entry.get("v")
    return None


def _cache_put(key: str, value) -> None:
    data = _cache_load()
    data[key] = {"t": time.time(), "v": value}
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = CACHE_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=1), encoding="utf-8")
        os.replace(tmp, CACHE_PATH)
    except Exception:  # pragma: no cover — cache is best-effort
        pass
