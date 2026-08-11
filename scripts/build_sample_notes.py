"""Lift every mart model's own SAMPLE-ONLY declaration into a control table.

THE GAP THIS CLOSES (2026-08-11). Seventeen mart models carry a hand-written
header saying, in plain words, that the table is a slice and not the full source
-- e.g. HMDA is one state-year of a fifty-state corpus, FDIC BankFind is a
10,000-row API slice of the whole institution universe. That warning was only
ever visible to someone opening the .sql file. Anyone browsing the catalog or
building a chart saw a source carrying the FULL source's name and a 'modeled'
lifecycle, with nothing to say it was a slice.

Parsing at build time and writing the result to a plain table keeps the platform
AI-free and file-free at runtime (constitution section 7): the catalog view just
joins this table.

Idempotent -- full replace on every run.

  python scripts/build_sample_notes.py --dry-run   # print what it found
  python scripts/build_sample_notes.py             # write the control table
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARTS = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models", "marts")
TABLE = "LIBRARY_META.REGISTRY.MART_SAMPLE_NOTES"

# Only an explicit, deliberate declaration counts. Deliberately NOT matching a
# bare "sample" -- that word shows up in ordinary prose ("sampled at source",
# "sample rate") and a false positive here is worse than a miss: it would brand
# a complete dataset as partial.
DECLARATION_RE = re.compile(r"(SAMPLE ONLY|PROOF SLICE)\b", re.IGNORECASE)


def header_of(path):
    """The leading comment block only. A declaration further down is not a header.

    Models open with a `{{ config(...) }}` call before the comments, so leading
    jinja and blank lines are skipped rather than treated as the end of the
    header -- reading them as a terminator is why the first version of this
    parser found zero declarations in files that plainly contain them.
    """
    lines = []
    started = False
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            s = line.strip()
            if s.startswith("--"):
                started = True
                lines.append(s.lstrip("-").strip())
            elif not s or (not started and s.startswith("{{")):
                continue
            else:
                break
    return " ".join(lines)


def scan():
    out = []
    for path in sorted(glob.glob(os.path.join(MARTS, "*", "*.sql"))):
        header = header_of(path)
        if not DECLARATION_RE.search(header):
            continue
        model = os.path.basename(path)[:-4]
        if "__" not in model:
            continue
        source_id = model.split("__", 1)[1]
        # Keep the author's own sentence -- it explains WHICH slice, which is the
        # part a chart builder actually needs. Trim to something a UI can show.
        note = header
        m = DECLARATION_RE.search(header)
        note = header[m.start():]
        if len(note) > 900:
            note = note[:897] + "..."
        out.append({
            "source_id": source_id.upper(),
            "model": model,
            "folder": os.path.basename(os.path.dirname(path)),
            "note": note,
        })
    return out


def write(rows):
    sys.path.insert(0, os.path.join(REPO, "library-onboarding"))
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(REPO, "library-onboarding", ".env"), override=True)
    except Exception:
        pass
    import snow
    conn = snow.connect()
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            SOURCE_ID   VARCHAR,
            MODEL       VARCHAR,
            FOLDER      VARCHAR,
            SAMPLE_NOTE VARCHAR,
            DETECTED_AT TIMESTAMP_NTZ
        )
    """)
    cur.execute(f"DELETE FROM {TABLE}")
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    cur.executemany(
        f"INSERT INTO {TABLE} (SOURCE_ID, MODEL, FOLDER, SAMPLE_NOTE, DETECTED_AT)"
        f" VALUES (%s, %s, %s, %s, %s)",
        [(r["source_id"], r["model"], r["folder"], r["note"], now) for r in rows],
    )
    cur.execute(f"SELECT COUNT(*) FROM {TABLE}")
    print(f"{TABLE}: {cur.fetchone()[0]} row(s)")
    cur.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    rows = scan()
    print(f"{len(rows)} mart model(s) declare themselves a sample\n")
    for r in rows:
        print(f"  {r['source_id'][:44]:44s} {r['note'][:88]}")
    if args.dry_run:
        return
    print()
    write(rows)


if __name__ == "__main__":
    main()
