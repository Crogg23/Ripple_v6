"""One-off: dump INFORMATION_SCHEMA.TABLES across all five Library databases
into a single markdown file, sorted alphabetically by table name.

Usage: python scripts/table_inventory.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from snow import connect  # noqa: E402

DATABASES = [
    "LIBRARY_RAW",
    "LIBRARY_STAGING",
    "LIBRARY_MARTS",
    "LIBRARY_META",
    "LIBRARY_TOOLS",
]

OUT_PATH = Path(__file__).resolve().parent.parent.parent / "reports" / "table_inventory.md"


def fmt_num(n) -> str:
    return f"{n:,}" if n is not None else ""


def main() -> None:
    conn = connect()
    rows = []
    missing_dbs = []
    try:
        cur = conn.cursor()
        for db in DATABASES:
            try:
                cur.execute(
                    f"""
                    SELECT
                        TABLE_CATALOG,
                        TABLE_SCHEMA,
                        TABLE_NAME,
                        ROW_COUNT,
                        BYTES,
                        CREATED,
                        LAST_ALTERED
                    FROM {db}.INFORMATION_SCHEMA.TABLES
                    ORDER BY TABLE_NAME
                    """
                )
                for r in cur.fetchall():
                    rows.append(r)
            except Exception as exc:
                missing_dbs.append((db, str(exc)))
        cur.close()
    finally:
        conn.close()

    rows.sort(key=lambda r: (r[2] or "", r[0] or "", r[1] or ""))

    lines = []
    lines.append("# Library Warehouse Table Inventory")
    lines.append("")
    lines.append(
        f"Full raw dump of `INFORMATION_SCHEMA.TABLES` across "
        f"{', '.join(DATABASES)}. {len(rows)} tables total. "
        "Sorted alphabetically by table name so duplicate/similar names sit together."
    )
    lines.append("")
    if missing_dbs:
        lines.append("**Databases that errored (not included above):**")
        for db, err in missing_dbs:
            lines.append(f"- `{db}`: {err.splitlines()[0]}")
        lines.append("")

    lines.append("| Table Name | Database | Schema | Row Count | Bytes | Created | Last Altered |")
    lines.append("|---|---|---|---|---|---|---|")
    for catalog, schema, name, row_count, num_bytes, created, last_altered in rows:
        lines.append(
            f"| {name} | {catalog} | {schema} | {fmt_num(row_count)} | {fmt_num(num_bytes)} "
            f"| {created} | {last_altered} |"
        )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {OUT_PATH}")
    if missing_dbs:
        print(f"WARNING: {len(missing_dbs)} database(s) errored: {[d for d, _ in missing_dbs]}")


if __name__ == "__main__":
    main()
