"""Push mart descriptions from dbt YAML into Snowflake comments, without a rebuild.

Why: the 2026-09-23 catalog audit found 292 mart models with a table description
and 212 columns with a column description in dbt YAML, but persist_docs was never
set, so Snowflake shows almost none of it. The capped 20M-row contracts table says
"CAPPED ... use r2" in YAML; in Snowflake it has no comment at all.

What it does:
  - reads every mart YAML under library-onboarding/ripple_dbt/models/marts
  - for each model whose table or view is live in LIBRARY_MARTS, writes
      COMMENT ON TABLE|VIEW <fqn> IS '<description>'         (table level)
      COMMENT ON COLUMN <fqn>.<col> IS '<description>'       (column level)
  - never overwrites an existing non-empty comment unless --overwrite is given
  - dry run by default: writes every statement to outputs/mart_comments_<date>.sql
    and prints counts; --apply executes them

dbt_project.yml gets `persist_docs` on marts the same day, so the next dbt build
writes the same text itself and a rebuild no longer wipes it.

Metadata only: COMMENT statements change no rows and use no warehouse compute.
Undo: COMMENT ON ... IS '' for any object, or re-run with the old text.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

MARTS = REPO / "library-onboarding" / "ripple_dbt" / "models" / "marts"


def lit(s: str) -> str:
    return "'" + " ".join(str(s).split()).replace("\\", "\\\\").replace("'", "''") + "'"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--overwrite", action="store_true", help="replace comments that already exist")
    ap.add_argument("--skip", nargs="*", default=[], help="mart names to leave out, e.g. one awaiting a rebuild")
    a = ap.parse_args()
    conn = db.connect()

    live = {r[1]: (r[0], r[2], r[3] or "") for r in db.rows(conn, """
        select table_schema, table_name, table_type, comment from LIBRARY_MARTS.information_schema.tables
        where table_schema not in ('INFORMATION_SCHEMA', 'TIMELINE')""")}
    colcm = {(r[0], r[1]): r[2] or "" for r in db.rows(conn, """
        select table_name, column_name, comment from LIBRARY_MARTS.information_schema.columns
        where table_schema not in ('INFORMATION_SCHEMA', 'TIMELINE')""")}

    stmts, kept, missing = [], 0, []
    for f in sorted(glob.glob(str(MARTS / "**" / "*.yml"), recursive=True)):
        for m in (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("models", []) or []:
            name = str(m.get("name", "")).upper()
            if name in {x.upper() for x in a.skip}:
                continue
            if name not in live:
                if m.get("description"):
                    missing.append(name)
                continue
            schema, ttype, cm = live[name]
            fqn = f'LIBRARY_MARTS."{schema}"."{name}"'
            kind = "VIEW" if ttype == "VIEW" else "TABLE"
            if m.get("description"):
                if cm and not a.overwrite:
                    kept += 1
                else:
                    stmts.append(f"COMMENT ON {kind} {fqn} IS {lit(m['description'])};")
            for c in m.get("columns", []) or []:
                col = str(c.get("name", "")).upper()
                if not c.get("description") or (name, col) not in colcm:
                    continue
                if colcm[(name, col)] and not a.overwrite:
                    kept += 1
                    continue
                if kind == "VIEW":  # Snowflake: a view column takes its comment through ALTER VIEW
                    stmts.append(f'ALTER VIEW {fqn} MODIFY COLUMN "{col}" COMMENT {lit(c["description"])};')
                else:
                    stmts.append(f'COMMENT ON COLUMN {fqn}."{col}" IS {lit(c["description"])};')

    out = REPO / "outputs" / f"mart_comments_{dt.date.today():%Y-%m-%d}.sql"
    out.write_text("\n".join(stmts) + "\n", encoding="utf-8")
    n_t = sum(1 for s in stmts if s.startswith(("COMMENT ON TABLE", "COMMENT ON VIEW")))
    print(f"statements: {len(stmts)}  ({n_t} tables or views, {len(stmts) - n_t} columns)")
    print(f"existing comments left alone: {kept}")
    print(f"described in YAML but not live in LIBRARY_MARTS: {len(missing)} {missing[:5]}")
    print("written:", out.relative_to(REPO))
    if not a.apply:
        print("DRY RUN -- nothing written to the warehouse.")
        return 0
    bad = 0
    for s in stmts:
        try:
            db.rows(conn, s)
        except Exception as e:  # noqa: BLE001  (one bad object must not stop the rest)
            bad += 1
            print("FAILED:", s[:120], "--", str(e)[:120])
    print(f"applied {len(stmts) - bad} of {len(stmts)}")
    conn.close()
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
