"""Make the THE_LIBRARY view rollback files runnable as written.

get_ddl() returns `create or replace view NAME(` with no database or schema, so a rollback file
built from it cannot be run without hand edits. Each file carries a `-- THE_LIBRARY."SCHEMA"."NAME"`
line before each statement; this script uses it to qualify the name and add COPY GRANTS, then
test-compiles the SELECT body of every statement with EXPLAIN. Nothing is executed.

    python scripts/qualify_rollback_files.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

FILES = ["library_view_rollback_2026-09-20.sql", "library_view_rollback_catalog_types_2026-09-21.sql"]
HEAD = re.compile(r'^(-- THE_LIBRARY\."?(\w+)"?\."?(\w+)"?[^\n]*)\n(create or replace view )(\w+)\(', re.M | re.I)
SELECT_START = re.compile(r"\bas\s+(select)\b", re.I)
OLD_NOTE = "-- Names below are UNQUALIFIED as get_ddl returns them. Qualify with THE_LIBRARY.<schema> before running."
NEW_NOTE = "-- Names qualified and COPY GRANTS added 2026-09-21 by scripts/qualify_rollback_files.py; every SELECT body EXPLAIN-checked."


def main() -> int:
    conn = db.connect()
    for name in FILES:
        path = REPO / "outputs" / name
        text = path.read_text(encoding="utf-8")
        qualified = 0

        def fix(m: re.Match) -> str:
            nonlocal qualified
            qualified += 1
            return f"{m.group(1)}\n{m.group(4)}THE_LIBRARY.{m.group(2)}.{m.group(3)} copy grants("

        text = HEAD.sub(fix, text).replace(OLD_NOTE, NEW_NOTE)
        statements = [s for s in re.split(r";\s*\n", text) if re.search(r"^create or replace view", s, re.M)]
        failed = 0
        for stmt in statements:
            body = stmt[stmt.index("create or replace view"):]
            hits = list(SELECT_START.finditer(body))
            try:
                db.rows(conn, "explain " + body[hits[-1].start(1):])
            except Exception as exc:  # noqa: BLE001
                failed += 1
                print("   does not compile:", body[:70].replace("\n", " "), "|", str(exc).replace("\n", " ")[:90])
        path.write_text(text, encoding="utf-8")
        print(f"{name}: {qualified} statements qualified this run, {len(statements)} compile-checked, {failed} failed")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
