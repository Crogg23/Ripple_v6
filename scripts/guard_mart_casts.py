"""Swap bare try_ casts in enabled mart files for the guarded staging macros.

Which shapes are bare was checked live 2026-09-21 through the Python door:
  try_to_double('nan')              -> NaN, poisons every sum       -> stg_float
  try_to_number('1.5')              -> 2, silent rounding           -> stg_int / stg_float
  try_to_date('2015')               -> a day in 1970                -> stg_date
  try_to_date('2015', 'MMDDYYYY')   -> 0005-02-01                   -> stg_date(.., 'MMDDYYYY')
  try_to_timestamp_tz('2015')       -> 1970-01-01 00:33:35          -> stg_ts
Shapes that came back NULL on a short digit string and are left alone: any
format with a separator, 'YYYYMMDD', the 14-digit wayback format, and an
explicit precision and scale on try_to_number / try_to_decimal.

A one-argument try_to_number is the only judgement call: a column that holds a
real fraction today gets stg_float, anything else gets stg_int. That is read
live, read-only, from the file's own source() table.

Dry run by default. --apply rewrites the files. Never runs dbt, never writes
to the warehouse.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MARTS = REPO / "library-onboarding" / "ripple_dbt" / "models" / "marts"
sys.path.insert(0, str(REPO))

CALL = re.compile(r"\btry_to_(number|double|date|timestamp_ntz|timestamp_tz|timestamp_ltz|timestamp)\s*\(", re.I)
SOURCE = re.compile(r"source\(\s*'([^']+)'\s*,\s*'([^']+)'\s*\)")
REF = re.compile(r"ref\(\s*'([^']+)'\s*\)")
EIGHT_DIGIT = {"MMDDYYYY"}


def close_paren(text: str, start: int) -> int:
    """Index of the ) that closes the ( at text[start - 1]."""
    depth, i, quote = 1, start, None
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def split_args(inner: str) -> list[str]:
    args, depth, quote, cur = [], 0, None, ""
    for ch in inner:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            args.append(cur.strip())
            cur = ""
            continue
        cur += ch
    args.append(cur.strip())
    return args


def jinja_str(expr: str) -> str | None:
    if "'" not in expr:
        return f"'{expr}'"
    if '"' not in expr:
        return f'"{expr}"'
    return None


def already_guarded(text: str, pos: int) -> bool:
    """True when the call sits inside an iff(regexp_like(...), <call>, null) guard on its line."""
    line_start = text.rfind("\n", 0, pos) + 1
    return "regexp_like(" in text[line_start:pos].lower()


def plan_file(path: Path):
    """Yield (start, end, kind, args) for every bare call, outermost first."""
    with path.open(encoding="utf-8", newline="") as fh:  # keep CRLF files CRLF
        text = fh.read()
    out = []
    for m in CALL.finditer(text):
        line_start = text.rfind("\n", 0, m.start()) + 1
        if text[line_start:m.start()].lstrip().startswith("--"):
            continue
        end = close_paren(text, m.end())
        if end < 0 or already_guarded(text, m.start()):
            continue
        fn = m.group(1).lower()
        args = split_args(text[m.end():end])
        fmt = args[1].strip("'") if len(args) == 2 else None
        if fn == "double" and len(args) == 1:
            kind = "float"
        elif fn == "number" and len(args) == 1:
            kind = "number"
        elif fn == "date" and len(args) == 1:
            kind = "date"
        elif fn == "date" and fmt in EIGHT_DIGIT:
            kind = "date_fmt"
        elif fn in ("timestamp_tz", "timestamp_ltz") and len(args) == 1:
            kind = "ts_tz"   # keeps its offset and its TIMESTAMP_TZ type
        elif fn.startswith("timestamp") and len(args) == 1:
            kind = "ts"
        else:
            continue
        out.append((m.start(), end + 1, kind, args))
    return text, out


def relation_for(conn, text: str) -> str | None:
    """The one relation a file reads: its landing table, or the live object behind its single ref()."""
    from connect import db

    tables = {t for _, t in SOURCE.findall(text)}
    refs = set(REF.findall(text))
    if len(tables) == 1 and not refs:
        return f"{db.RAW_DB}.{db.RAW_SCHEMA}.{tables.pop()}"
    if len(refs) == 1 and not tables:
        name = refs.pop().upper()
        for dbname in ("LIBRARY_STAGING", "LIBRARY_MARTS"):
            hit = db.rows(conn, f"""select table_schema from {dbname}.information_schema.tables
                where table_name = '{name}' and table_schema not in ('TIMELINE', 'DBT_CROGERS_RIPPLE')""")
            if len(hit) == 1:
                return f"{dbname}.{hit[0][0]}.{name}"
    return None


def has_fraction(conn, table: str, exprs: list[str]) -> dict[str, bool | None]:
    from connect import db

    cols = ", ".join(
        f"count_if(try_to_double(({e})::string) <> floor(try_to_double(({e})::string)))" for e in exprs
    )
    try:
        row = db.rows(conn, f"select {cols} from {table}")[0]
        return {e: n > 0 for e, n in zip(exprs, row)}
    except Exception as exc:  # noqa: BLE001
        print(f"    could not read {table}: {str(exc)[:110]}")
        return {e: None for e in exprs}


def leading_zeros(conn, table: str, exprs: list[str]) -> dict[str, int]:
    """Rows where the value is digits with a leading zero: an ID, and a number cast is already eating the zero."""
    from connect import db

    cols = ", ".join(f"count_if(regexp_like(trim(({e})::string), '0[0-9]+'))" for e in exprs)
    try:
        return dict(zip(exprs, db.rows(conn, f"select {cols} from {table}")[0]))
    except Exception:  # noqa: BLE001
        return {e: 0 for e in exprs}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--refs", action="store_true", help="work on marts that read ref() instead of source()")
    ap.add_argument("--staging", action="store_true", help="work on models/staging instead of models/marts")
    opts = ap.parse_args()

    from connect import db

    conn = db.connect()
    changed_files = changed_calls = 0
    leftovers: list[str] = []
    root = MARTS.parent / "staging" if opts.staging else MARTS
    for path in sorted(root.rglob("*.sql")):
        raw = path.read_text(encoding="utf-8")
        if re.search(r"enabled\s*=\s*false", raw, re.I) or (opts.refs == ("source(" in raw)):
            continue
        text, calls = plan_file(path)
        if not calls:
            continue
        rel = path.relative_to(root).as_posix()

        number_exprs = sorted({a[0] for _, _, k, a in calls if k == "number"})
        fractions: dict[str, bool | None] = {}
        if number_exprs:
            relation = relation_for(conn, text)
            fractions = has_fraction(conn, relation, number_exprs) if relation else {e: None for e in number_exprs}
            zeros = leading_zeros(conn, relation, number_exprs) if relation else {}
            for e, n in zeros.items():
                if n:
                    fractions[e] = None
                    leftovers.append(f"{rel}: {e[:50]} has {n:,} values with a leading zero -- an ID, not a number")

        # innermost-last so nested spans never overlap a rewritten outer span
        spans, done = [], 0
        for start, end, kind, args in sorted(calls, key=lambda c: -c[0]):
            if any(start < s and end > e for s, e, _ in spans):
                leftovers.append(f"{rel}: nested cast around {args[0][:50]}")
                continue
            arg = jinja_str(args[0])
            if arg is None:
                leftovers.append(f"{rel}: both quote kinds in {args[0][:50]}")
                continue
            if kind == "float":
                new = f"{{{{ stg_float({arg}) }}}}"
            elif kind == "date":
                new = f"{{{{ stg_date({arg}) }}}}"
            elif kind == "date_fmt":
                new = f"{{{{ stg_date({arg}, {args[1]}) }}}}"
            elif kind == "ts":
                new = f"{{{{ stg_ts({arg}) }}}}"
            elif kind == "ts_tz":
                new = f"{{{{ stg_ts_tz({arg}) }}}}"
            else:
                frac = fractions.get(args[0])
                if frac is None:
                    leftovers.append(f"{rel}: try_to_number({args[0][:50]}) needs a hand decision")
                    continue
                new = f"{{{{ stg_float({arg}) }}}}" if frac else f"{{{{ stg_int({arg}) }}}}"
                if frac:
                    print(f"    {rel}: {args[0]} holds real fractions -> stg_float")
            spans.append((start, end, new))
            done += 1
        for start, end, new in spans:  # already descending
            text = text[:start] + new + text[end:]
        if done:
            changed_files += 1
            changed_calls += done
            print(f"{done:4d}  {rel}")
            if opts.apply:
                with path.open("w", encoding="utf-8", newline="") as fh:
                    fh.write(text)
    conn.close()
    print(f"\n{'rewrote' if opts.apply else 'would rewrite'} {changed_calls} casts in {changed_files} files")
    for line in leftovers:
        print("  LEFT:", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
