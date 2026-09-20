"""Repair the 12 THE_LIBRARY views that throw a SQL error on open (found 2026-09-20).

Two causes, both confirmed from GET_DDL:
  - 10 views are `CREATE VIEW v(col1, col2, ...) COMMENT='..' AS SELECT * FROM src`. The column
    list froze at creation; src has since gained or lost a column, so Snowflake refuses the view.
  - 2 views are typed projections over a landing table that was renamed (data exists under
    the new name; the view body still says the old one).

Fix, the same for all 12: recreate the view with its body and its catalog COMMENT intact, the
renamed table swapped in, and the frozen column list dropped -- so it can't drift again.
Every rewritten body is compiled against the warehouse BEFORE anything is changed. A view
whose declared names differ from what its body really outputs (a deliberate friendly rename)
is SKIPPED and reported, never guessed at.

    python scripts/repair_library_views.py            # dry run: shows exactly what would run
    python scripts/repair_library_views.py --apply    # Chris runs this; saves rollback DDL first
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

READ_ROLES = ("RIPPLE_READER", "CLAUDE_MCP_READONLY")

TARGETS = [
    ("CAMPAIGN_FINANCE", "INDIVIDUAL_DONATIONS"),
    ("CAMPAIGN_FINANCE", "OUTSIDE_SPENDING"),
    ("CRIME_SECURITY", "FBI_CRIME_INCIDENTS"),
    ("ENERGY_ENVIRONMENT", "POLLUTION_ENFORCEMENT"),
    ("GEOGRAPHY", "TRIBAL_LANDS_GEO"),
    ("GOVERNMENT", "REVOLVING_DOOR_APPOINTEES"),
    ("HEALTH", "CDC_MORTALITY_QUERIES"),
    ("HEALTH", "HOSPITAL_COST_REPORTS"),
    ("HEALTH", "NURSING_HOMES"),
    ("HEALTH", "VETERAN_MORTALITY_APPENDIX"),
    ("MONEY", "CREDIT_UNION_CALL_REPORTS"),
    ("TRANSPORT", "AIRCRAFT_REGISTRY"),
]

# landing tables renamed out from under their view: old name -> new name
RENAMED = {
    "LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS": "LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS_FS220",
    "LIBRARY_RAW.LANDING.FED_FAA_REGISTRY": "LIBRARY_RAW.LANDING.FED_FAA_AIRCRAFT_REGISTRY",
}


def split_ddl(ddl: str):
    """-> (declared column names, select body) from a GET_DDL view string, or None."""
    i = ddl.find("(")
    head_as = re.search(r"\bas\b", ddl[: i if i != -1 else len(ddl)], re.I)
    if i == -1 or head_as:                      # no column list at all
        m = re.search(r"\bas\s+", ddl, re.I)
        return ([], ddl[m.end():].rstrip().rstrip(";").rstrip()) if m else None
    j = ddl.find(")", i)                        # column names never contain parens
    declared = [c.strip().strip('"').upper() for c in ddl[i + 1: j].split(",") if c.strip()]
    rest = ddl[j + 1:].lstrip()
    if rest[:7].lower() == "comment":           # skip COMMENT='..' ('' is an escaped quote)
        n = rest.index("'") + 1
        while True:
            q = rest.index("'", n)
            if rest[q + 1: q + 2] == "'":
                n = q + 2
                continue
            break
        rest = rest[q + 1:].lstrip()
    m = re.match(r"as\s+", rest, re.I)
    if not m:
        return None
    return declared, rest[m.end():].rstrip().rstrip(";").rstrip()


def output_columns(conn, select_sql: str) -> list[str]:
    cur = conn.cursor()
    try:
        cur.execute(f"select * from ({select_sql}) limit 0")
        return [d[0].upper() for d in cur.description]
    finally:
        cur.close()


def plan(conn, schema: str, view: str) -> dict:
    fqn = f'THE_LIBRARY."{schema}"."{view}"'
    ddl = db.scalar(conn, f"select get_ddl('VIEW', '{fqn}')")
    parts = split_ddl(ddl)
    if not parts:
        return {"fqn": fqn, "ddl": ddl, "skip": "could not find the view's select body"}
    declared, body = parts

    swapped = []
    for old, new in RENAMED.items():            # longest-first isn't needed: old is never a prefix match with a trailing word char
        pat = re.compile(re.escape(old) + r"(?![A-Za-z0-9_])", re.I)
        if pat.search(body):
            body = pat.sub(new, body)
            swapped.append(f"{old} -> {new}")

    try:
        out_cols = output_columns(conn, body)
    except Exception as e:  # noqa: BLE001
        return {"fqn": fqn, "ddl": ddl, "skip": "rewritten body does not compile: " + str(e).replace("\n", " ")[:110]}

    gone = sorted(set(declared) - set(out_cols))
    if declared and len(gone) > max(2, len(declared) // 10):
        return {"fqn": fqn, "ddl": ddl,
                "skip": f"{len(gone)} declared names are not in the body's output (friendly renames?) e.g. {gone[:4]}"}

    comment = db.scalar(conn, "select comment from THE_LIBRARY.INFORMATION_SCHEMA.VIEWS "
                              f"where table_schema = '{schema}' and table_name = '{view}'")
    clause = " comment='" + comment.replace("'", "''") + "'" if comment else ""
    return {
        "fqn": fqn, "ddl": ddl, "swapped": swapped, "has_comment": bool(comment),
        "declared_n": len(declared), "output_n": len(out_cols),
        "gone": gone, "new": sorted(set(out_cols) - set(declared)) if declared else [],
        "new_ddl": f"create or replace view {fqn} copy grants{clause} as {body}",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="execute the DDL (default is a dry run)")
    args = ap.parse_args()

    conn = db.connect()
    plans = [plan(conn, s, v) for s, v in TARGETS]

    for p in plans:
        print("\n" + p["fqn"])
        if "skip" in p:
            print("   SKIP --", p["skip"])
            continue
        print(f"   columns: frozen list had {p['declared_n']}  |  body really outputs {p['output_n']}"
              f"  |  catalog comment kept: {'yes' if p['has_comment'] else 'none to keep'}")
        for s in p["swapped"]:
            print(f"   renamed table swapped in: {s}")
        if p["gone"]:
            print(f"   in the frozen list but no longer in the data: {p['gone']}")
        if p["new"]:
            print(f"   in the data but missing from the frozen list: {p['new'][:6]}")
        print("   rewritten body compiles against the warehouse: yes")

    todo = [p for p in plans if "skip" not in p]
    print(f"\n{len(todo)} of {len(plans)} views ready, {len(plans) - len(todo)} skipped.")
    if not args.apply:
        print("DRY RUN -- nothing was changed. Re-run with --apply to execute.")
        return 0

    out = REPO / "outputs" / f"library_view_rollback_{dt.date.today():%Y-%m-%d}.sql"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n\n".join(f"-- {p['fqn']}\n{p['ddl']}" for p in todo), encoding="utf-8")
    print(f"rollback DDL for all {len(todo)} views saved to {out}")

    fixed = 0
    for p in todo:
        try:
            db.rows(conn, p["new_ddl"])
            for role in READ_ROLES:
                try:
                    db.rows(conn, f"grant select on view {p['fqn']} to role {role}")
                except Exception:  # noqa: BLE001  (role may not exist in this account)
                    pass
            n = len(output_columns(conn, f"select * from {p['fqn']}"))
            print(f"   FIXED  {p['fqn']}  ({n} columns, opens clean)")
            fixed += 1
        except Exception as e:  # noqa: BLE001
            print(f"   FAILED {p['fqn']} -- " + str(e).replace("\n", " ")[:120])
    print(f"\n{fixed} of {len(todo)} views repaired.")
    return 0 if fixed == len(todo) else 1


if __name__ == "__main__":
    raise SystemExit(main())
