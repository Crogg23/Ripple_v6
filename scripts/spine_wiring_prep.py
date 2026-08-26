"""Read-only prep tool for the spine wiring backlog (reports/SPINE_WIRING_PLAN_2026-08-24.md).

For every candidate table (from the audit's key_columns_verified.csv, entity-grade,
unwired, deduped against junk/backup/mirror schemas): pull live INFORMATION_SCHEMA
columns, pull 5 live sample rows, run the platform's own trap check (COUNT vs
COUNT DISTINCT normalized, per connect/keys.py:normalize_sql) on the key column, and
propose candidate name/address columns by pattern.

Writes ONE draft packet per table to reports/spine_wiring_drafts/<db>.<schema>.<table>.json.
This is a DRAFT, not a DISPLAY_SPECS entry -- every packet still needs the human
person/org/authority call (plan step 3-6) before anything is wired. Read-only against
Snowflake: SELECT / DESCRIBE only, never DDL/DML.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from connect import db  # noqa: E402
from connect.keys import normalize_sql  # noqa: E402

AUDIT_CSV = _REPO / "reports/the_audit_2026-08-24/key_columns_verified.csv"
OUT_DIR = _REPO / "reports/spine_wiring_drafts"
ENTITY_GRAINS = {"person", "organization", "facility", "provider", "case", "asset"}

NAME_HINTS = ("NAME", "LEGAL_", "ORGANIZATION", "PROVIDER", "BUSINESS", "COMPANY",
              "FACILITY", "LAST_", "FIRST_", "ENTITY")
ADDR_HINTS = {"city": ("CITY",), "state": ("STATE",), "zip": ("ZIP", "POSTAL")}


def is_junk(db_name: str, schema: str, table: str) -> bool:
    if db_name == "THE_LIBRARY":
        return True
    if "PREDBT" in db_name:
        return True
    if "RESTORE" in schema or "RESTORE" in table:
        return True
    if schema == "TIMELINE":
        return True
    if "BAK_" in schema or "PRESPINE" in schema:
        return True
    return False


def load_worklist() -> dict[tuple[str, str, str], list[dict]]:
    tables: dict[tuple[str, str, str], list[dict]] = {}
    with open(AUDIT_CSV, newline="") as f:
        for r in csv.DictReader(f):
            if r["spine_entity_grain"] not in ENTITY_GRAINS:
                continue
            if r["spine_wired"] != "False":
                continue
            key = (r["database"], r["schema"], r["table"])
            if is_junk(*key):
                continue
            tables.setdefault(key, []).append(r)
    return tables


def guess_name_addr_cols(all_cols: list[str]) -> dict:
    upper = {c: c.upper() for c in all_cols}
    name_candidates = [c for c, u in upper.items() if any(h in u for h in NAME_HINTS)]
    addr = {}
    for field, hints in ADDR_HINTS.items():
        matches = [c for c, u in upper.items() if any(h in u for h in hints)]
        addr[field] = matches
    return {"name_candidates": name_candidates, "address_candidates": addr}


def process_table(conn, db_name: str, schema: str, table: str, key_rows: list[dict]) -> dict:
    fqtn = f"{db_name}.{schema}.{table}"

    # Snowflake's INFORMATION_SCHEMA is scoped to the database you query it from --
    # a bare `information_schema.columns` only ever sees the CURRENT database, even
    # with a table_catalog filter in the WHERE clause. Must qualify per-database.
    cols = db.dicts(
        conn,
        f"""
        select column_name, data_type, ordinal_position
        from {db_name}.information_schema.columns
        where table_schema = %s and table_name = %s
        order by ordinal_position
        """,
        (schema, table),
    )
    if not cols:
        return {"fqtn": fqtn, "status": "SCHEMA_NOT_FOUND", "checked": True}

    col_names = [c["COLUMN_NAME"] for c in cols]
    guesses = guess_name_addr_cols(col_names)

    try:
        sample = db.dicts(conn, f'select * from {fqtn} sample (5 rows)')
    except Exception as e:
        sample = []
        sample_error = str(e)
    else:
        sample_error = None

    key_checks = []
    for kr in key_rows:
        key_label = kr["key_label"]
        col = kr["column"]
        check = {"key_label": key_label, "column": col}
        try:
            norm = normalize_sql(key_label, f'"{col}"')
            row = db.rows(
                conn,
                f"""
                select count(*), count({norm}), count(distinct {norm})
                from {fqtn}
                """,
            )[0]
            check.update(
                total_rows=row[0],
                nonnull_after_norm=row[1],
                distinct_after_norm=row[2],
                trap_verdict=(
                    "REAL" if row[2] and row[2] > max(10, 0.01 * row[0]) else "SUSPECT_MASKED_OR_SPARSE"
                ),
            )
        except Exception as e:
            check.update(error=str(e), trap_verdict="CHECK_FAILED")
        key_checks.append(check)

    return {
        "fqtn": fqtn,
        "status": "DRAFTED",
        "checked": True,
        "live_columns": col_names,
        "name_addr_guesses": guesses,
        "key_checks": key_checks,
        "sample_rows": sample,
        "sample_error": sample_error,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    worklist = load_worklist()
    print(f"Worklist: {len(worklist)} candidate tables")

    conn = db.connect()
    done = 0
    failed = []
    try:
        for (db_name, schema, table), key_rows in sorted(worklist.items()):
            out_path = OUT_DIR / f"{db_name}.{schema}.{table}.json"
            if out_path.exists():
                continue
            try:
                packet = process_table(conn, db_name, schema, table, key_rows)
            except Exception as e:
                packet = {"fqtn": f"{db_name}.{schema}.{table}", "status": "ERROR", "error": str(e)}
                failed.append((db_name, schema, table, str(e)))
            out_path.write_text(json.dumps(packet, indent=2, default=str))
            done += 1
            if done % 25 == 0:
                print(f"  ...{done}/{len(worklist)}")
    finally:
        conn.close()

    print(f"Done: {done} packets written to {OUT_DIR}")
    if failed:
        print(f"Failed: {len(failed)}")
        for f in failed[:20]:
            print("  ", f)


if __name__ == "__main__":
    main()
