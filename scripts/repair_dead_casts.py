"""Unwrap the try_to_* casts that were verified live to null out their column.

Driven by evidence, not by a heuristic: it only touches (model, column) pairs that
reports/mart_dead_columns_2026-08-10.csv proved are 100% NULL in the built mart
(verdict DEAD_CAST), plus the name-like columns that came back under 5% populated.
The heuristic that CREATED these casts is fixed separately in gen_mart_models.py
(HARD_TEXT / STRIP_WORDS); this script repairs what it already shipped.

    python scripts/repair_dead_casts.py            # dry run
    python scripts/repair_dead_casts.py --apply
"""
import argparse
import collections
import csv
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_mart_models import cast_is_suspicious  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARTS = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models", "marts")
EVIDENCE = os.path.join(REPO, "reports", "mart_dead_columns_2026-08-10.csv")

# A near-empty column whose surviving values are place names is the same bug as a
# fully empty one -- the few rows that parsed were numeric-looking place codes.
NAMEY = ("COUNTY", "COUNTRY", "PARISH")

_CAST_CALL = re.compile(
    r"\btry_to_(?:number|double|date|timestamp)\(\s*\"?([A-Za-z0-9_]+)\"?\s*[,)]")


def targets():
    """{model_name: {LANDING_COLUMN, ...}} to unwrap."""
    out = collections.defaultdict(set)
    with open(EVIDENCE, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            col, verdict = r["column"], r["verdict"]
            if verdict == "DEAD_CAST":
                out[r["mart_table"]].add(col)
            elif verdict == "MOSTLY_DEAD" and any(w in col.upper() for w in NAMEY):
                out[r["mart_table"]].add(col)
    return out


def repair_text(text, cols):
    """Strip try_to_*(COL) down to COL for each named column. Returns (text, hits)."""
    hits = []
    for col in sorted(cols):
        pat = re.compile(
            r"\btry_to_(?:number|double|date|timestamp)\(\s*(\"?%s\"?)\s*\)"
            % re.escape(col), re.IGNORECASE)
        text, n = pat.subn(r"\1", text)
        if n:
            hits.append(col)
    return text, hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--static", action="store_true",
                    help="also repair casts the static guard flags, not just the "
                         "columns the live scan proved dead")
    args = ap.parse_args()

    want = collections.defaultdict(set, targets())
    by_model = {os.path.splitext(os.path.basename(p))[0].upper(): p
                for p in glob.glob(os.path.join(MARTS, "*", "*.sql"))}
    if args.static:
        # Second pass: the same accident on columns the live scan did not reach
        # (marts it could not query, or aliases spelled differently). Only casts the
        # naive rules would have made and the guarded rules refuse -- see
        # gen_mart_models.cast_is_suspicious.
        for model, path in by_model.items():
            text = open(path, encoding="utf-8", errors="ignore").read()
            for col in set(_CAST_CALL.findall(text)):
                if cast_is_suspicious(col):
                    want[model].add(col)

    changed = fixed_cols = 0
    missing = []
    for model, cols in sorted(want.items()):
        path = by_model.get(model.upper())
        if not path:
            missing.append(model)
            continue
        text = open(path, encoding="utf-8").read()
        new, hits = repair_text(text, cols)
        if not hits:
            missing.append("%s (no cast found for %s)" % (model, ",".join(sorted(cols))))
            continue
        changed += 1
        fixed_cols += len(hits)
        print("  %-58s %d col(s): %s" % (
            os.path.relpath(path, MARTS).replace("\\", "/"), len(hits),
            ", ".join(hits[:4]) + ("..." if len(hits) > 4 else "")))
        if args.apply:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(new)

    print("\n%d model files, %d columns un-cast" % (changed, fixed_cols))
    if missing:
        print("\nNOT repaired here (cast lives elsewhere, or the model was "
              "hand-written) -- %d:" % len(missing))
        for m in missing:
            print("   %s" % m)
    if not args.apply:
        print("\nDRY RUN -- rerun with --apply to write files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
