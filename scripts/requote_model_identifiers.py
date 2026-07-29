"""Repair mart models that reference case-sensitive landing columns without quotes.

Several landing tables were created with quoted, non-upper-case column names --
"Prscrbr_NPI", "contract_transaction_unique_key", "1862_land_grant_college". A bare
reference to one of those gets upper-cased by Snowflake and fails with
"invalid identifier". gen_mart_models.py emitted bare references, so every affected
model died at build time.

This rebuilds a model's select list from the real column list, keeping whatever cast
the original chose (try_to_double / try_to_number / try_to_date / none) and keeping
output names unquoted lower-case so Snowflake stores them upper-case, which is what
every other mart in LIBRARY_MARTS does.

Usage:
    python scripts/requote_model_identifiers.py --check            # scan all marts
    python scripts/requote_model_identifiers.py <model.sql> --apply
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _snowflake_conn as sc  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARTS = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models", "marts")

SOURCE_RE = re.compile(r"source\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)")
CAST_RE = re.compile(
    r"^\s*(?:(?P<cast>try_to_double|try_to_number|try_to_date|try_to_timestamp)"
    r"\(\s*(?P<inner>\"?[A-Za-z0-9_\-]+\"?)\s*\)|(?P<bare>\"?[A-Za-z0-9_\-]+\"?))"
    r"(?:\s+as\s+(?P<alias>\"?[A-Za-z0-9_]+\"?))?\s*,?\s*$",
    re.IGNORECASE,
)
RESERVED = {"select", "from", "source", "with", "as", "where", "and", "or", "final",
            "cleaned", "base", "qualify", "case", "when", "then", "end", "null"}


def parse_select_list(text):
    """Yield (cast, source_column, alias) for each simple select-list line."""
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        m = CAST_RE.match(line)
        if not m:
            continue
        src = (m.group("inner") or m.group("bare") or "").strip('"')
        if not src or src.lower() in RESERVED:
            continue
        alias = (m.group("alias") or "").strip('"') or None
        out.append((m.group("cast"), src, alias))
    return out


def safe_output_name(name):
    out = name.lower().replace("-", "_")
    if out[0].isdigit():
        m = re.match(r"^(\d+)_?(.*)$", out)
        out = f"{m.group(2)}_{m.group(1)}" if m.group(2) else f"col_{out}"
    return out


def rebuild(text, columns):
    """Return the model text with a requoted select list, or None if not applicable."""
    by_upper = {c.upper(): c for c in columns}
    entries = [e for e in parse_select_list(text) if e[1].upper() in by_upper]
    if not entries or "\nselect" not in text.lower():
        return None

    def expr_of(cast, src):
        exact = by_upper[src.upper()]
        return f'{cast}("{exact}")' if cast else f'"{exact}"'

    width = max(len(expr_of(c, s)) for c, s, _a in entries)
    lines = []
    for cast, src, alias in entries:
        out = alias or safe_output_name(by_upper[src.upper()])
        lines.append(f"    {expr_of(cast, src):<{width}} as {out},")
    lines[-1] = lines[-1].rstrip(",")

    head = text[:text.lower().rindex("\nselect")]
    return head + "\nselect\n" + "\n".join(lines) + "\nfrom source\n"


def needs_fix(text, conn):
    m = SOURCE_RE.search(text)
    if not m:
        return None, None
    table = m.group(2)
    try:
        cols = sc.columns_of(table, conn=conn)
    except Exception:
        return table, None
    risky = {c.upper() for c in cols if c != c.upper()}
    if not risky:
        return table, None
    body = text.lower().split("from source")[0]
    for _cast, src, _alias in parse_select_list(text):
        if src.upper() in risky and f'"{src.lower()}"' not in body:
            return table, cols
    return table, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", help="path to a model .sql file")
    ap.add_argument("--check", action="store_true", help="scan all mart models")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    conn = sc.connect()
    try:
        targets = ([args.model] if args.model
                   else sorted(glob.glob(os.path.join(MARTS, "**", "*.sql"),
                                         recursive=True)))
        hits = 0
        for path in targets:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            table, cols = needs_fix(text, conn)
            if not cols:
                continue
            hits += 1
            rel = os.path.relpath(path, MARTS)
            new = rebuild(text, cols)
            if new is None:
                print(f"SKIP  {rel} (could not rebuild select list)")
                continue
            print(f"FIX   {rel}  (source {table})")
            if args.apply:
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(new)
        print(f"\n{hits} model(s) reference case-sensitive columns without quotes")
        if hits and not args.apply:
            print("DRY RUN -- rerun with --apply to write changes")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
