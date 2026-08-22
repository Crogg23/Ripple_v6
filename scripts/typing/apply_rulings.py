"""Apply typing rulings to the dbt mart models.

Phase 3 of the canonical typing layer. Reads reports/typing_index/
typing_rulings.csv and rewrites `<expr> as <ALIAS>` lines in the matching
mart model to wrap the source expression in the ripple_num / ripple_dt
macros (macros/ripple_typing.sql).

Safety rules (the ones that keep this from being a regex chainsaw):
  - Only cast_double / cast_date / ambiguous_* rulings are applied.
  - Only SIMPLE source expressions are rewritten: a bare identifier
    (COL_NAME) or a double-quoted identifier ("col name"). Anything else
    (already-cast lines, functions, concatenations) is SKIPPED and listed
    for hand review — never auto-mangled.
  - A line already containing `try_to` or `ripple_` is left alone.
  - The politics marts are excluded entirely (Python-built canonical tables,
    guard_politics_mirror standing policy).
  - Every touched model is listed on stdout; nothing is rebuilt here — run
    dbt on the printed selector afterwards.

    python scripts/typing/apply_rulings.py            # dry run (default)
    python scripts/typing/apply_rulings.py --write    # edit the model files
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
RULINGS = _REPO / "reports" / "typing_index" / "typing_rulings.csv"
MODELS = _REPO / "library-onboarding" / "ripple_dbt" / "models" / "marts"

APPLY = {"cast_double": "ripple_num", "ambiguous_number": "ripple_num",
         "cast_date": "ripple_dt", "ambiguous_date": "ripple_dt"}

# expr must be a bare identifier or one double-quoted identifier
SIMPLE = re.compile(r'^\s*(("[^"]+")|([A-Za-z_][A-Za-z0-9_$]*))\s*$')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    by_table: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
    for r in csv.DictReader(open(RULINGS, newline="", encoding="utf-8")):
        if r["ruling"] in APPLY:
            by_table[(r["schema"], r["table"])][r["column"].upper()] = APPLY[r["ruling"]]

    touched, skipped, missing_models = [], [], []
    for (schema, table), cols in sorted(by_table.items()):
        if schema.upper() == "POLITICS":
            skipped.append((schema, table, "*", "politics guard"))
            continue
        model = MODELS / schema.lower() / f"{table.lower()}.sql"
        if not model.exists():
            missing_models.append(f"{schema}.{table}")
            continue
        text = model.read_text(encoding="utf-8")
        lines = text.splitlines()
        n_hit = 0
        for i, line in enumerate(lines):
            m = re.match(r'^(\s*)(.*?)\s+as\s+([A-Za-z_][A-Za-z0-9_$]*)\s*(,?)\s*$',
                         line, flags=re.IGNORECASE)
            if not m:
                # bare-identifier select-list line: `    ACTION_DATE,`
                b = re.match(r'^(\s+)([A-Za-z_][A-Za-z0-9_$]*)\s*(,?)\s*$', line)
                if b and b.group(2).upper() in cols:
                    indent, col, comma = b.groups()
                    macro = cols[col.upper()]
                    lines[i] = f"{indent}{{{{ {macro}('{col}') }}}} as {col}{comma}"
                    n_hit += 1
                continue
            indent, expr, alias, comma = m.groups()
            macro = cols.get(alias.upper())
            if not macro:
                continue
            if "try_to" in expr.lower() or "ripple_" in expr.lower():
                skipped.append((schema, table, alias, "already cast"))
                continue
            if not SIMPLE.match(expr):
                skipped.append((schema, table, alias, f"complex expr: {expr[:60]}"))
                continue
            src = expr.strip()
            arg = src.replace("'", "\\'")
            lines[i] = f"{indent}{{{{ {macro}('{arg}') }}}} as {alias}{comma}"
            n_hit += 1
        if n_hit:
            if args.write:
                model.write_text("\n".join(lines) + "\n", encoding="utf-8")
            touched.append((schema, table, n_hit))

    for schema, table, n in touched:
        print(f"EDIT  {schema}.{table}: {n} columns")
    for schema, table, col, why in skipped:
        print(f"SKIP  {schema}.{table}.{col}: {why}")
    for t in missing_models:
        print(f"NO-MODEL  {t}")
    print(f"\n{'WROTE' if args.write else 'DRY RUN'}: {len(touched)} models, "
          f"{sum(n for _, _, n in touched)} columns; "
          f"{len(skipped)} skipped, {len(missing_models)} without model files")
    if touched and args.write:
        sel = " ".join(t.lower() for _, t, _ in touched)
        print(f"\nrebuild with:\n  dbt run --select {sel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
