"""One UPDATE: replace the stale fed_nih_reporter CAPPED note in SOURCE_REGISTRY.

Old note preserved in reports/row1/registry_note_fix_2026-08-31.md.
Run by hand: python3 scripts/fix_nih_registry_note_2026_08_31.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connect import db

NEW = (
    "FULLY LOADED (verified 2026-08-31 audit): FY2000-2026 contiguous, 2,122,611 rows, "
    "zero duplicate APPL_IDs; FY2024 = 83,519 vs API published 83,516. "
    "The earlier 'CAPPED at FY2000-2002' note was overtaken - the resume ran to completion. "
    "Old note preserved in reports/row1/registry_note_fix_2026-08-31.md."
)


def main():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(
        "select NOTES from LIBRARY_META.REGISTRY.SOURCE_REGISTRY where SOURCE_ID='fed_nih_reporter'"
    )
    old = cur.fetchone()[0]
    if "CAPPED at FY2000-2002" not in old:
        print("note already updated, nothing to do:")
        print(old[:200])
        return
    cur.execute(
        "update LIBRARY_META.REGISTRY.SOURCE_REGISTRY set NOTES=%s "
        "where SOURCE_ID='fed_nih_reporter'",
        (NEW,),
    )
    print("updated rows:", cur.rowcount)
    conn.commit()


if __name__ == "__main__":
    main()
