"""A1 -- plain-English COMMENTs on the 5 Ripple databases + their schemas.

Snapshots EVERY existing comment (DB/schema/table) to a reversible rollback file
FIRST, then applies the approved 'explain it so anyone gets it' voice to DB + schema
objects. Table comments are Workstream A2 (generated separately). Idempotent.

Usage: python scripts/thelibrary_a1_comments.py [--apply]
"""
from __future__ import annotations
import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
sys.path.insert(0, str(_LIB))
from snow import connect  # noqa: E402

APPLY = "--apply" in sys.argv
ROLLBACK = Path(__file__).resolve().parents[1] / "outputs" / "_rollback_comments_20260701.sql"
RIPPLE_DBS = ["LIBRARY_RAW", "LIBRARY_META", "LIBRARY_MARTS", "LIBRARY_STAGING", "LIBRARY_TOOLS"]

DB_COMMENTS = {
    "LIBRARY_RAW": "The loading dock. Every source arrives here first, exactly as it came -- every value stored as plain text, nothing cleaned or connected yet. The untouched original: if you ever wonder what a source really looked like at the door, it's here.",
    "LIBRARY_STAGING": "The prep kitchen. Raw data gets its columns renamed, its types fixed, and its duplicates removed here. Everything is a view -- a saved recipe that runs on demand, not a stored copy -- so it's cheap and always current.",
    "LIBRARY_MARTS": "The finished shelves. Clean, ready-to-use tables named for the question they answer -- health, politics, justice -- not the agency they came from. This is what you actually pull from.",
    "LIBRARY_META": "The card catalog and the wiring: what sources exist, when each last loaded, and how they link to each other through shared IDs (a doctor's NPI, a company's EIN). The map of the whole library.",
    "LIBRARY_TOOLS": "Not data -- an empty room that exists only to host the read-only robot Claude queries through. Holds nothing; safe to ignore. Do NOT delete it.",
}

SCHEMA_COMMENTS = {
    "LIBRARY_RAW.LANDING": "One table per data source, exactly as it arrived. About 129 are full sources; the ~655 named PORTAL_* are thin samples pulled from open-data portals because they share an ID we can join on.",
    "LIBRARY_META.REGISTRY": "The catalog itself: SOURCE_REGISTRY (every source we know about) plus the CATALOG view and helpers that classify and describe them. Start here to find what exists.",
    "LIBRARY_META.INGEST_LOGS": "The load history: one row per ingest run -- what loaded, when, how many rows, success or failure. How we know the data is real and current.",
    "LIBRARY_META.CONNECT": "The matchmaking engine. Takes every source's IDs and works out who links to whom -- the same person, company, or ship across datasets. Working tables here are large and rebuilt automatically; leave them be.",
    "LIBRARY_MARTS.CORE": "Shared reference tables -- calendars, state/county/tract lookups, ZIP crosswalks. The dimensions other tables join to for geography and dates.",
    "LIBRARY_MARTS.DBT_CROGERS": "The main set of finished tables (built by dbt). The schema name is a leftover developer default -- browse the friendly THE_LIBRARY database instead for plain-English names.",
    "LIBRARY_MARTS.EPSTEIN": "Tracking tables for the library's own history and the Epstein-document investigation -- snapshots of what data existed when, and how archived pages changed over time.",
    "LIBRARY_MARTS.POLITICS": "Finished tables for the politics investigation: who's in Congress, how they voted, who funds them, who won elections, and the judges on the bench.",
    "LIBRARY_STAGING.CORE": "Prep-kitchen views: raw reference data cleaned into shared dimensions. Nothing stored -- views only.",
    "LIBRARY_STAGING.DBT_CROGERS": "Prep-kitchen views feeding the finished tables: renamed, retyped, deduplicated. Nothing stored -- views only.",
    "LIBRARY_STAGING.POLITICS": "Prep-kitchen views for the politics tables: legislators and voting records cleaned before modeling.",
    "LIBRARY_STAGING.SEEDS": "Small hand-maintained lookup tables loaded from CSV (dimensions, nickname maps) -- the fixed reference data the pipeline leans on.",
}


def q(cur, sql):
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def esc(s):
    return s.replace("'", "''")


def main():
    conn = connect(); cur = conn.cursor()

    # ---- snapshot existing comments (reversible) -------------------------
    lines = ["-- Rollback of comments as they were before 2026-07-01 housekeeping.\n"]
    for d in q(cur, "SHOW DATABASES"):
        if d["name"] in RIPPLE_DBS and (d.get("comment") or ""):
            lines.append(f"COMMENT ON DATABASE {d['name']} IS '{esc(d['comment'])}';")
    for db in RIPPLE_DBS:
        for s in q(cur, f"SHOW SCHEMAS IN DATABASE {db}"):
            if (s.get("comment") or "") and s["name"] != "INFORMATION_SCHEMA":
                lines.append(f"COMMENT ON SCHEMA {db}.{s['name']} IS '{esc(s['comment'])}';")
        for t in q(cur, f"""SELECT TABLE_SCHEMA, TABLE_NAME, COMMENT FROM {db}.INFORMATION_SCHEMA.TABLES
                            WHERE COMMENT IS NOT NULL AND TABLE_SCHEMA<>'INFORMATION_SCHEMA'"""):
            kind = "VIEW" if False else "TABLE"
            lines.append(f"COMMENT ON TABLE {db}.{t['TABLE_SCHEMA']}.{t['TABLE_NAME']} IS '{esc(t['COMMENT'])}';")
    ROLLBACK.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"snapshot: {len(lines)-1} existing comments -> {ROLLBACK}")

    # ---- apply DB + schema comments -------------------------------------
    stmts = [(f"COMMENT ON DATABASE {db} IS '{esc(c)}'") for db, c in DB_COMMENTS.items()]
    stmts += [(f"COMMENT ON SCHEMA {fq} IS '{esc(c)}'") for fq, c in SCHEMA_COMMENTS.items()]
    print(f"\n{'APPLYING' if APPLY else 'PREVIEW'} {len(stmts)} DB/schema comments:")
    for s in stmts:
        obj = s.split(" IS '")[0].replace("COMMENT ON ", "")
        print(f"   {obj}")
        if APPLY:
            try:
                cur.execute(s)
            except Exception as e:
                print(f"      ERROR: {str(e)[:150]}")
    print("\nDONE." + ("" if APPLY else "  (preview -- re-run with --apply)"))
    cur.close(); conn.close()


if __name__ == "__main__":
    main()
