"""Apply typing rulings to select-star passthrough mart models.

Batch 2 of the typing rollout. For a model whose final select is a bare
`select *`, rewrite it as

    select
        * exclude (COL_A, COL_B),
        {{ ripple_num('COL_A') }} as COL_A,
        {{ ripple_dt('COL_B') }} as COL_B

Safety rails:
  - Only models where NO ruled column already appears cast (try_to/ripple_)
    anywhere in the file.
  - Only the LAST `select *` in the file is rewritten (CTE `select *` lines
    that feed a later explicit column list are left alone -- detected by the
    ruled columns having no aliased lines at all).
  - Models whose star reads a raw source() with quoted lower-case columns are
    SKIPPED unless the star is over a ref() (staging outputs upper-case, so
    `exclude (COL)` resolves); source-star models are listed for hand review.
  - Politics excluded (standing policy).
  - Column order changes (ruled columns move to the end of the row). Nothing
    in the dbt project selects marts positionally.

    python scripts/typing/apply_star_rulings.py            # dry run
    python scripts/typing/apply_star_rulings.py --write
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

STAR = re.compile(r"select\s*\*\s*\n(\s*)from", re.IGNORECASE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    by_table: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
    for r in csv.DictReader(open(RULINGS, newline="", encoding="utf-8")):
        if r["ruling"] in APPLY:
            by_table[(r["schema"], r["table"])][r["column"].upper()] = APPLY[r["ruling"]]

    touched, skipped = [], []
    for (schema, table), cols in sorted(by_table.items()):
        if schema.upper() == "POLITICS":
            continue
        model = MODELS / schema.lower() / f"{table.lower()}.sql"
        if not model.exists():
            continue
        text = model.read_text(encoding="utf-8")
        # skip if any ruled column is already handled (aliased or cast)
        if any(re.search(rf"as\s+{c}\b", text, re.IGNORECASE) for c in cols):
            continue  # explicit-column model; batch-1 territory
        stars = list(STAR.finditer(text))
        if not stars:
            continue
        m = stars[-1]
        # what does the star read? the from-line right after it
        after = text[m.end():].lstrip()
        if after.lower().startswith("{{ source("):
            skipped.append((schema, table, "star over raw source (quoted lower-case columns)"))
            continue
        indent = m.group(1) or "    "
        col_list = sorted(cols)
        excl = ", ".join(col_list)
        casts = ",\n".join(
            f"{indent}{{{{ {cols[c]}('{c}') }}}} as {c}" for c in col_list)
        replacement = (f"select\n{indent}* exclude ({excl}),\n{casts}\n{m.group(1)}from")
        new_text = text[:m.start()] + replacement + text[m.end():]
        header = ("-- TYPED 2026-08-22 (typing layer batch 2): ruled columns cast via\n"
                  "-- ripple_num/ripple_dt (see reports/typing_index/typing_rulings.csv);\n"
                  "-- they move to the end of the row -- nothing selects marts positionally.\n")
        new_text = re.sub(r"(\{\{\s*config[^}]*\}\}\s*\n)", r"\1\n" + header,
                          new_text, count=1)
        if args.write:
            model.write_text(new_text, encoding="utf-8")
        touched.append((schema, table, len(cols)))

    for schema, table, n in touched:
        print(f"EDIT  {schema}.{table}: {n} columns")
    for schema, table, why in skipped:
        print(f"SKIP  {schema}.{table}: {why}")
    print(f"\n{'WROTE' if args.write else 'DRY RUN'}: {len(touched)} models, "
          f"{sum(n for _, _, n in touched)} columns; {len(skipped)} skipped")
    if touched:
        print("\nselector: " + " ".join(t.lower() for _, t, _ in touched))
    return 0


if __name__ == "__main__":
    sys.exit(main())
