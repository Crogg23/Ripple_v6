"""Land the whole HUDOC (European Court of Human Rights) document index.

WHAT STOPPED THE OLD TABLE
  INTL_HUDOC is 2,000 rows: the onboarding fetch_data called the HUDOC search
  API once at length=2000 (or looped to its own cap). Probed 2026-09-07: the
  same query reports resultcount 211,778 and honours length=2000 with a
  start= offset.

THE SECOND CAP, found on the first --run
  The search window is 10,000 rows per query: start >= 10000 returns zero
  results with resultcount still 211,778, and start+length past 10,000 also
  returns zero. So one query can never page the set. The loader partitions
  the query by kpdate year (Lucene range syntax kpdate:[a TO b]; the field
  syntax kpdate>="..." silently returns 0) and splits any year that reaches
  10,000 into months. Rows with no kpdate are fetched as one extra partition.
  The first --run on 2026-09-07 landed 10,000 rows (run 9901da93) before this
  was known.

THE THIRD CAP, found on the second --run
  With sort blank the API pages a relevance order that is not stable, so
  start=2000 repeats rows start=0 already gave and drops others. Run 40e14cd3
  came back 211,778 rows, 187,418 distinct itemids. Paging 2010 alone: no sort
  6,703 distinct of 7,656; sort=itemid Ascending 7,656 of 7,656; kpdate
  Ascending 7,633 (ties). SORT is now itemid Ascending. The complete pull is
  the newest run id; runs 9901da93 and 40e14cd3 stay in the table until a
  gated DELETE by run id removes them.

WHAT THE ROWS ARE
  One row per HUDOC document (judgment, decision, report, resolution...) in the
  ECHR collection, press releases and old Commission documents excluded, the
  same filter the site's own default search uses. The same case appears once
  per language version (HEJUD English, HFJUD French), so APPNO repeats; the
  per-row key is CASE_ID (HUDOC itemid).

WHAT THIS DOES
  Pages /app/query/results with start=/length= into
  LIBRARY_RAW.LANDING.INTL_HUDOC_FULL, same 18 columns as the old table plus
  _INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256. Derived columns follow the old
  table's shape: COUNTRY = respondent, PERSON_NAME = the applicant side of the
  title (text before ' v. ' / ' c. '), URL = hudoc.echr.coe.int/eng?i=itemid.
  The old table is not touched.

    python scripts/hudoc_full_load.py          # dry run
    python scripts/hudoc_full_load.py --run    # land it
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _repage_land as rp  # noqa: E402

SOURCE_ID = "intl_hudoc_full"
TABLE = "INTL_HUDOC_FULL"
URL = "https://hudoc.echr.coe.int/app/query/results"
QUERY = "contentsitename:ECHR AND (NOT (doctype=PR OR doctype=HFCOMOLD OR doctype=HECOMOLD))"
SELECT = ("itemid,appno,docname,judgementdate,kpdate,doctype,importance,article,violation,"
          "nonviolation,originatingbody,respondent,ecli,kpthesaurus,conclusion,languageisocode")
PAGE = 2000
SORT = "itemid Ascending"  # unsorted paging repeats rows: 2010 gave 6,703 distinct of 7,656
COLUMNS = ["CASE_ID", "APPNO", "CASE_TITLE", "DATE", "COUNTRY", "PERSON_NAME", "DOC_TYPE",
           "IMPORTANCE", "ARTICLES", "VIOLATION", "NONVIOLATION", "ORIGINATING_BODY",
           "RESPONDENT", "ECLI", "KEYWORDS", "CONCLUSION", "LANGUAGE", "URL"]
_VS = re.compile(r"\s+(v\.|c\.|v|c)\s+", re.I)


def _person(title: str) -> str:
    if not title:
        return ""
    return _VS.split(title, maxsplit=1)[0].strip()


def total() -> int:
    return int(fetch_q(QUERY, 0, 1)["resultcount"])


WINDOW = 10_000
FIRST_YEAR, LAST_YEAR = 1950, 2027


def partitions(start_year: int = FIRST_YEAR):
    """Yield (label, query) pieces each under the 10,000-row window."""
    def rng(a, b):
        return f"{QUERY} AND kpdate:[{a}T00:00:00 TO {b}T23:59:59]"
    for y in range(start_year, LAST_YEAR + 1):
        q = rng(f"{y}-01-01", f"{y}-12-31")
        n = int(fetch_q(q, 0, 1)["resultcount"])
        if n == 0:
            continue
        if n < WINDOW:
            yield f"{y} ({n:,})", q
            continue
        for m in range(1, 13):
            last = 31 if m in (1, 3, 5, 7, 8, 10, 12) else (30 if m != 2 else 29)
            qm = rng(f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last}")
            nm = int(fetch_q(qm, 0, 1)["resultcount"])
            if nm >= WINDOW:
                raise RuntimeError(f"{y}-{m:02d} holds {nm:,} rows, over the window; split finer")
            if nm:
                yield f"{y}-{m:02d} ({nm:,})", qm
    q = f"{QUERY} AND NOT kpdate:[{FIRST_YEAR}-01-01T00:00:00 TO {LAST_YEAR}-12-31T23:59:59]"
    n = int(fetch_q(q, 0, 1)["resultcount"])
    if n >= WINDOW:
        raise RuntimeError(f"undated partition holds {n:,} rows, over the window")
    if n:
        yield f"undated ({n:,})", q


def fetch_q(query: str, start: int, length: int, tries: int = 6) -> dict:
    """HUDOC resets connections mid-run (seen 2026-09-07 after ~50K rows);
    retry with backoff rather than lose the run."""
    for i in range(tries):
        try:
            r = requests.get(URL, params={"query": query, "select": SELECT, "sort": SORT,
                                          "start": start, "length": length},
                             headers=rp.UA, timeout=300)
            r.raise_for_status()
            return r.json()
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError, ValueError) as e:
            if i == tries - 1:
                raise
            wait = 5 * 2 ** i
            print(f"  fetch failed ({e.__class__.__name__}); retry {i + 1}/{tries - 1} in {wait}s")
            time.sleep(wait)


def pages(start_year: int = FIRST_YEAR):
    for label, q in partitions(start_year):
        print(f"  partition {label}")
        start = 0
        while True:
            data = fetch_q(q, start, PAGE)
            results = data.get("results", [])
            if not results:
                break
            yield _frame(results)
            start += len(results)
            if len(results) < PAGE:
                break


def _frame(results) -> pd.DataFrame:
        rows = []
        for res in results:
            c = res.get("columns", {})
            item = c.get("itemid", "")
            rows.append({
                "CASE_ID": item,
                "APPNO": c.get("appno", ""),
                "CASE_TITLE": c.get("docname", ""),
                "DATE": c.get("judgementdate") or c.get("kpdate", ""),
                "COUNTRY": c.get("respondent", ""),
                "PERSON_NAME": _person(c.get("docname", "")),
                "DOC_TYPE": c.get("doctype", ""),
                "IMPORTANCE": c.get("importance", ""),
                "ARTICLES": c.get("article", ""),
                "VIOLATION": c.get("violation", ""),
                "NONVIOLATION": c.get("nonviolation", ""),
                "ORIGINATING_BODY": c.get("originatingbody", ""),
                "RESPONDENT": c.get("respondent", ""),
                "ECLI": c.get("ecli", ""),
                "KEYWORDS": c.get("kpthesaurus", ""),
                "CONCLUSION": c.get("conclusion", ""),
                "LANGUAGE": c.get("languageisocode", ""),
                "URL": f"https://hudoc.echr.coe.int/eng?i={item}" if item else "",
            })
        return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="land it; default is dry run")
    ap.add_argument("--append", action="store_true", help="allow landing on top of existing rows")
    ap.add_argument("--resume-run-id", help="continue an interrupted run under its run id, "
                    "skipping CASE_IDs it already landed")
    ap.add_argument("--start-year", type=int, default=FIRST_YEAR,
                    help="first kpdate year partition to fetch (use with --resume-run-id)")
    args = ap.parse_args()
    n = total()
    print(f"source {URL}\nserver says {n:,} documents; page size {PAGE:,}")
    rp.land_pages(source_id=SOURCE_ID, table=TABLE, source_url=URL, columns=COLUMNS,
                  pages=lambda: pages(args.start_year), run=args.run, append=args.append,
                  expected_total=n, resume_run_id=args.resume_run_id, key_col="CASE_ID")


if __name__ == "__main__":
    main()
