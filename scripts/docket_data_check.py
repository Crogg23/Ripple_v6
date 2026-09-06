#!/usr/bin/env python3
"""For every docket entry, check the data behind it is really there.

An entry names its warehouse tables. Nobody has checked whether those tables
exist, how much is in them, or how old they are. So the docket can say "run me"
about a question whose data was never loaded, and you find out after writing the
join. This asks the warehouse instead.

Per entry it records:
    tables_it_needs   how many tables the entry lists
    tables_we_have    how many of those actually exist
    rows_we_have      rows across the ones that exist
    years_known       the widest year span anyone has measured, if any
    oldest_of_them    how out of date the oldest one reads
    on_the_shelf      whether the tables are there, below

tables_state says ONE thing: are the tables on the shelf. It is not a
readiness score. Every probe that died last week would score "all tables here",
because none of them died on a missing table. They died on years that never
overlapped, on keys that matched strangers, and on a match that meant something
else. Those are three checks nobody has built yet.

    all tables here       every table exists, none reads stale
    here but going stale  every table exists, one is behind its schedule
    some tables missing   some exist, some do not
    no tables found       none of them exist
    no tables listed      the entry never named any

Read-only. Writes docket/docket_data.csv and updates the docket in place.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "library-onboarding"))
sys.path.insert(0, str(REPO / "scripts"))
try:
    from dotenv import load_dotenv
    load_dotenv(REPO / "library-onboarding" / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402

DOCKET = REPO / "docket" / "docket.csv"
OUT = REPO / "docket" / "docket_data.csv"


def table_names(row: dict) -> list[str]:
    """Exactly what the entry wrote, uppercased. Full names stay full.

    Matching on the bare name would call almost anything a hit: the warehouse
    holds 2,892 tables and many share a suffix. An entry that names
    LIBRARY_MARTS.HEALTH.X has to find that table, not a namesake in landing.
    """
    return [t.strip().upper() for t in (row.get("tables") or "").split("|") if t.strip()]


def live_tables(conn) -> dict[str, int]:
    """Every table and view in the warehouse, keyed by its full name."""
    cur = conn.cursor()
    found: dict[str, int] = {}
    for db in ("LIBRARY_RAW", "LIBRARY_MARTS", "LIBRARY_META"):
        try:
            cur.execute(f"""SELECT TABLE_SCHEMA, TABLE_NAME, ROW_COUNT
                            FROM {db}.INFORMATION_SCHEMA.TABLES""")
        except Exception as exc:
            print(f"  {db}: {str(exc).splitlines()[-1][:70]}")
            continue
        for sch, name, n in cur.fetchall():
            found[f"{db}.{sch}.{name}"] = int(n or 0)
    cur.close()
    return found


def coverage(conn) -> dict[str, tuple[int, int]]:
    """Measured year span per table, from the newest coverage run."""
    cur = conn.cursor()
    out: dict[str, tuple[int, int]] = {}
    try:
        cur.execute("""
            WITH runs AS (SELECT SOURCE_ID, MAX(MEASURED_AT) AT
                          FROM LIBRARY_META.REGISTRY.SOURCE_COVERAGE_YEARS GROUP BY 1),
            l AS (SELECT c.* FROM LIBRARY_META.REGISTRY.SOURCE_COVERAGE_YEARS c
                  JOIN runs r ON r.SOURCE_ID = c.SOURCE_ID AND r.AT = c.MEASURED_AT)
            SELECT UPPER(SPLIT_PART(LANDING_FQN, '.', 3)), MIN(DATA_YEAR), MAX(DATA_YEAR)
            FROM l GROUP BY 1""")
        for name, lo, hi in cur.fetchall():
            out[name] = (int(lo), int(hi))
    except Exception as exc:
        print("  coverage:", str(exc).splitlines()[-1][:70])
    cur.close()
    return out


def freshness(conn) -> dict[str, str]:
    """Freshness state per table, from the ledger."""
    cur = conn.cursor()
    out: dict[str, str] = {}
    try:
        cur.execute("""SELECT UPPER(SPLIT_PART(LANDING_FQN, '.', 3)), FRESHNESS_STATE
                       FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS""")
        for name, state in cur.fetchall():
            out[name] = state
    except Exception as exc:
        print("  freshness:", str(exc).splitlines()[-1][:70])
    cur.close()
    return out


WORST = ["dead", "stale", "overdue", "due", "unknown", "fresh"]


def main() -> int:
    rows = list(csv.DictReader(DOCKET.open()))
    conn = snow.connect()
    try:
        live = live_tables(conn)
        cov = coverage(conn)
        fresh = freshness(conn)
    finally:
        conn.close()
    print(f"warehouse: {len(live):,} tables, {len(cov)} with measured years, "
          f"{len(fresh)} with a freshness state")

    out_rows = []
    for r in rows:
        names = table_names(r)
        hit = [n for n in names if n in live]
        n_rows = sum(live[n] for n in hit)
        bare = [n.split(".")[-1] for n in hit]
        spans = [cov[n] for n in bare if n in cov]
        years = f"{min(s[0] for s in spans)}-{max(s[1] for s in spans)}" if spans else ""
        states = [fresh[n] for n in bare if n in fresh]
        worst = min(states, key=lambda s: WORST.index(s) if s in WORST else 9) if states else ""

        if not names:
            state = "no tables listed"
        elif not hit:
            state = "no tables found"
        elif len(hit) < len(names):
            state = "some tables missing"
        elif worst in ("dead", "stale", "overdue"):
            state = "here but going stale"
        else:
            state = "all tables here"

        out_rows.append({
            "id": r["id"], "where_it_stands": r["where_it_stands"], "question": r["question"],
            "tables_it_needs": len(names), "tables_we_have": len(hit),
            "rows_we_have": n_rows, "years_known": years, "oldest_of_them": worst,
            "on_the_shelf": state, "needs": r.get("needs", ""),
        })

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0]))
        w.writeheader()
        w.writerows(out_rows)

    import collections
    c = collections.Counter(r["on_the_shelf"] for r in out_rows)
    print("\nare the tables on the shelf:")
    for k, v in c.most_common():
        print(f"  {v:>4}  {k}")
    total = sum(r["rows_we_have"] for r in out_rows)
    print(f"\nrows reachable across every entry: {total:,}")
    known = sum(1 for r in out_rows if r["years_known"])
    print(f"\nyears measured on {known} of {len(out_rows)} entries")
    print("\nThis says the tables exist and what years they hold.")
    print("A working key and what a match means are still unchecked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
