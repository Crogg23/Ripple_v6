"""Date/time cast inventory — every LANDING column that looks like a date or a
timestamp, classified into a bucket with a ready-to-use Snowflake cast expression.

Read-only. Runs entirely against the gen-1 content recon's local JSON profiles
(reports/recon/content/json/*.json) — no warehouse query, no cost. Each profile
already carries a content-derived `date_fmt` per column (content_recon.py's
`classify()`) plus sample values in `top`, which is enough to pick a cast without
touching Snowflake.

Buckets:
  native     already TIMESTAMP_NTZ/DATE — nothing to do
  content_date  TEXT column, format detected from content (iso/us/ymd8/mdy8/dmon/
             epochms/epochs) — auto cast expression below
  audit_num  NUMBER column matching the audit-column name pattern (_INGESTED_AT,
             CREATED_AT, ...) — epoch unit inferred from the digit-width of a
             real sample value, auto cast expression below
  unclassified_needs_eyeball    column name carries a real DATE/DT/TIME token
             but content recon could not fit its sample values to any known
             format — needs a human look, no auto cast offered
  unclassified_blank_or_sentinel  same, but the sample is empty or a null
             placeholder ('nan', '-', ',,') — nothing to classify, not a format gap

Output: reports/recon/date_cast_inventory_<DATE>.csv, one row per flagged column.
        reports/recon/date_cast_inventory_<DATE>.md,  the summary counts.

Usage:
  python scripts/date_cast_inventory.py
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
JSON_DIR = REPO / "reports" / "recon" / "content" / "json"
OUT_CSV = REPO / "reports" / "recon" / "date_cast_inventory_2026-09-03.csv"
OUT_MD = REPO / "reports" / "recon" / "date_cast_inventory_2026-09-03.md"

AUDIT_RX = re.compile(r"INGEST|LOADED|_LOADED|LOAD_TS|CREATED_AT|UPDATED_AT|_AT$|SNAPSHOT|RUN_ID|FILE_NAME", re.I)


def name_tokens(col: str) -> list[str]:
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", col)
    return re.split(r"[_\W]+", s.upper())


def has_date_token(col: str) -> bool:
    # a standalone DATE/DT/TIME/TIMESTAMP token, not a substring of a bigger word
    # (UPDATE, LIQUIDATED, OVERTIME, TIMELY all contain the letters but aren't dates)
    return any(t in ("DATE", "DT", "TIME", "TIMESTAMP") for t in name_tokens(col))


def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def content_date_expr(col: str, fmt: str, typ: str) -> str:
    c = q(col)
    numeric = typ in ("NUMBER", "FLOAT")
    if fmt == "iso":
        return f"TRY_TO_TIMESTAMP_NTZ(TO_VARCHAR({c}))" if numeric else f"TRY_TO_TIMESTAMP_NTZ({c})"
    if fmt == "us":
        v = f"TO_VARCHAR({c})" if numeric else c
        # date-only "us" samples have no time tokens to match against the HH12 format,
        # so TRY_TO_TIMESTAMP_NTZ silently returns NULL without this fallback -- verified live.
        return f"COALESCE(TRY_TO_TIMESTAMP_NTZ({v}, 'MM/DD/YYYY HH12:MI:SS AM'), TRY_TO_TIMESTAMP_NTZ({v}, 'MM/DD/YYYY'))"
    if fmt == "ymd8":
        return f"TRY_TO_DATE(TO_VARCHAR({c}), 'YYYYMMDD')" if numeric else f"TRY_TO_DATE({c}, 'YYYYMMDD')"
    if fmt == "mdy8":
        return f"TRY_TO_DATE(TO_VARCHAR({c}), 'MMDDYYYY')" if numeric else f"TRY_TO_DATE({c}, 'MMDDYYYY')"
    if fmt == "dmon":
        v = f"TO_VARCHAR({c})" if numeric else c
        return f"COALESCE(TRY_TO_DATE({v}, 'DD-MON-YY'), TRY_TO_DATE({v}, 'DD-MON-YYYY'))"
    if fmt == "epochms":
        # numeric columns hold a clean millisecond integer; text columns carry a trailing '.0' to strip.
        n = f"FLOOR({c})" if numeric else f"TRY_TO_NUMBER(SPLIT_PART({c}, '.', 1))"
        return f"DATEADD('millisecond', {n}, '1970-01-01'::timestamp_ntz)"
    if fmt == "epochs":
        n = f"FLOOR({c})" if numeric else f"TRY_TO_NUMBER({c})"
        return f"DATEADD('second', {n}, '1970-01-01'::timestamp_ntz)"
    return None


def epoch_unit(sample: str) -> str | None:
    try:
        n = abs(int(float(sample)))
    except (ValueError, TypeError):
        return None
    digits = len(str(n))
    if digits == 0:
        return None
    if digits <= 10:
        return "second"
    if digits <= 13:
        return "millisecond"
    if digits <= 16:
        return "microsecond"
    if digits <= 19:
        return "nanosecond"
    return None


def audit_num_expr(col: str, unit: str) -> str:
    return f"DATEADD('{unit}', {q(col)}, '1970-01-01'::timestamp_ntz)"


def classify_table(table: str, doc: dict) -> list[dict]:
    profile = doc.get("profile", {})
    roles = doc.get("roles", {})
    rows = []
    for col, prof in profile.items():
        col_roles = roles.get(col, [])
        typ = prof.get("type")
        fmt = prof.get("date_fmt")
        top = prof.get("top") or []
        sample = top[0][0] if top else None

        if typ in ("TIMESTAMP_NTZ", "DATE") or fmt == "native":
            rows.append(dict(table=table, column=col, bucket="native", type=typ,
                              pattern=fmt, sample=sample, cast_expr=""))
            continue

        if fmt and typ in ("TEXT", "NUMBER", "FLOAT"):
            expr = content_date_expr(col, fmt, typ)
            rows.append(dict(table=table, column=col, bucket="content_date", type=typ,
                              pattern=fmt, sample=sample, cast_expr=expr or ""))
            continue

        if typ == "NUMBER" and AUDIT_RX.search(col):
            unit = epoch_unit(sample) if sample is not None else None
            if unit:
                rows.append(dict(table=table, column=col, bucket="audit_num", type=typ,
                                  pattern=f"epoch_{unit}", sample=sample,
                                  cast_expr=audit_num_expr(col, unit)))
            else:
                rows.append(dict(table=table, column=col, bucket="audit_num_unreadable",
                                  type=typ, pattern="", sample=sample, cast_expr=""))
            continue

        if typ == "TEXT" and has_date_token(col) and "date" not in col_roles:
            blank = sample is None or str(sample).strip().lower() in ("", "nan", "-", ",,", "none", "null", "n/a")
            bucket = "unclassified_blank_or_sentinel" if blank else "unclassified_needs_eyeball"
            rows.append(dict(table=table, column=col, bucket=bucket,
                              type=typ, pattern="", sample=sample, cast_expr=""))
            continue
    return rows


def main():
    all_rows = []
    tables_seen = 0
    for path in sorted(JSON_DIR.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        tables_seen += 1
        all_rows.extend(classify_table(doc.get("table", path.stem), doc))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["table", "column", "bucket", "type", "pattern", "sample", "cast_expr"])
        w.writeheader()
        w.writerows(all_rows)

    by_bucket = Counter(r["bucket"] for r in all_rows)
    tables_by_bucket = {b: len({r["table"] for r in all_rows if r["bucket"] == b}) for b in by_bucket}
    by_pattern = Counter((r["bucket"], r["pattern"]) for r in all_rows if r["bucket"] in ("content_date", "audit_num"))

    lines = [
        "# Date/time cast inventory",
        "",
        f"Tables scanned: {tables_seen}",
        f"Flagged columns: {len(all_rows)}",
        "",
        "## By bucket",
        "",
        "| bucket | columns | tables |",
        "|---|---|---|",
    ]
    for b, n in by_bucket.most_common():
        lines.append(f"| {b} | {n} | {tables_by_bucket[b]} |")
    lines += ["", "## By pattern (auto-fixable buckets only)", "", "| bucket | pattern | columns |", "|---|---|---|"]
    for (b, p), n in sorted(by_pattern.items(), key=lambda x: -x[1]):
        lines.append(f"| {b} | {p} | {n} |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"tables_scanned={tables_seen}")
    print(f"flagged_columns={len(all_rows)}")
    for b, n in by_bucket.most_common():
        print(f"  {b}: {n} columns across {tables_by_bucket[b]} tables")
    print(f"csv={OUT_CSV}")
    print(f"md={OUT_MD}")


if __name__ == "__main__":
    main()
