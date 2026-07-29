"""Pre-flight check for dbt source declarations.

Catches the two YAML mistakes that make `dbt parse` fail outright, both of which
have already broken this project:

1. Duplicate (source, table) pairs. dbt requires a landing table to be declared
   exactly once across the whole project. Redeclaring one in a mart-level
   _<domain>__sources.yml when staging/<source>/schema.yml already has it is a
   fatal Compilation Error, not a warning.
2. A source whose `tables:` key is present but empty, which crashes dbt's yaml
   reader with `TypeError: 'NoneType' object is not iterable`.

Exit code 0 = clean, 1 = problems found. Safe to wire into CI or a pre-commit hook.

Usage: python scripts/audit_dbt_sources.py [--quiet]
"""
import argparse
import collections
import glob
import os
import sys

import yaml

MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "library-onboarding", "ripple_dbt", "models")


def scan(root=MODELS):
    """Return (occurrences, empty_table_lists, unreadable_files)."""
    occ = collections.defaultdict(list)
    empty, broken = [], []
    for path in glob.glob(os.path.join(root, "**", "*.yml"), recursive=True):
        rel = os.path.relpath(path, root)
        try:
            with open(path, encoding="utf-8") as fh:
                doc = yaml.safe_load(fh)
        except Exception as exc:
            broken.append((rel, str(exc)[:200]))
            continue
        if not isinstance(doc, dict):
            continue
        for src in doc.get("sources") or []:
            name = src.get("name")
            if "tables" in src and not src.get("tables"):
                empty.append((rel, name))
                continue
            for tbl in src.get("tables") or []:
                occ[(name, tbl.get("name"))].append(rel)
    return occ, empty, broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true",
                    help="only print problems and the summary line")
    args = ap.parse_args()

    occ, empty, broken = scan()
    dups = {k: v for k, v in occ.items() if len(v) > 1}

    for rel, msg in broken:
        print(f"UNREADABLE {rel}: {msg}")
    for rel, name in empty:
        print(f"EMPTY-TABLES {rel}: source '{name}' has an empty tables list "
              f"-- delete the source block or give it a table")
    for (src, tbl), files in sorted(dups.items()):
        print(f"DUPLICATE {src}.{tbl} declared in {len(files)} files:")
        for f in sorted(set(files)):
            print(f"    {f}")

    problems = len(dups) + len(empty) + len(broken)
    if not args.quiet or problems:
        print(f"\n{len(occ)} source tables declared across the project | "
              f"{len(dups)} duplicates, {len(empty)} empty table lists, "
              f"{len(broken)} unreadable files")
    if problems:
        print("FAIL -- `dbt parse` will not succeed until these are resolved")
    else:
        print("PASS -- source declarations are clean")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
