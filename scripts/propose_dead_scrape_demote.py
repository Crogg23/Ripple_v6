#!/usr/bin/env python3
"""Preview (and optionally apply) STATUS='empty' demotions for the dead-scrape pile
surfaced by the 2026-06-27 discovery sweep -- sources that landed page chrome / nav /
cookie banners instead of data, so the '76 landed' headline is inflated by them.

Mechanism mirrors scripts/regrade_empty_loads.py: it UPDATEs existing INGEST_RUNS
rows (latest success per source) to STATUS='empty' and annotates MESSAGE. The
catalog LIFECYCLE is DERIVED from STATUS downstream, so this is enough -- no
SOURCE_REGISTRY / CATALOG write. SAFE BY DEFAULT: preview only; --apply gated.

  python3 scripts/propose_dead_scrape_demote.py                 # preview (READS only)
  python3 scripts/propose_dead_scrape_demote.py sid1 sid2 ...    # add extra source_ids
  python3 scripts/propose_dead_scrape_demote.py --apply          # Chris runs this

Per the triage decision (re-scrape the valuable, demote the rest), the RE-SCRAPE
candidates (doj_fca_settlements, doj_crt_cases, naag_multistate_settlements,
fdic_enforcement, slavevoyages_intraamerican) are NOT in the default list -- they
are demoted here ONLY IF their re-scrape loader fails (pass them as CLI args then).
wpa_slave_narratives is NOT demoted: its names live in TITLE/SUBJECTS and are
salvaged via a dbt rename, not a reload.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:  # pragma: no cover
    pass

import pandas as pd  # noqa: E402
import snow  # noqa: E402
from config import settings  # noqa: E402

# (source_id, finding, one-line reason) -- the confirmed low-value dead scrapes.
DEMOTE = [
    ("intl_ie_cro",                "#39",  "0 company records -- 3 rows are the opendata.cro.ie cookie-consent table"),
    ("intl_gr_gemi",               "#65",  "all 40 rows blank business fields; only 7 Greek UI/footer strings"),
    ("intl_ch_zefix",              "#103", "18 rows of scraped Zefix homepage nav/footer chrome, zero companies"),
    ("fed_nara_aad",               "#63",  "554 AAD series-description pages, not records; all record keys null + 4x HTTP 404"),
    ("fed_va_allcause_mortality",  "#101", "broken PDF list-of-figures scrape: 244 rows, 227 fully blank"),
    ("fed_oyez",                   "#83",  "25-row hollow stub; DECISION/DISPOSITION/AUTHOR/CITATION 100% blank"),
    ("intl_es_borme",             "#108", "company names/IDs mis-mapped into ACT_DESCRIPTION; 25 rows, low value -> demote"),
    ("fed_va_suicide_appendix",    "#87",  "flattened PDF, 2 stacked sub-tables, positional COL_n; low value -> demote"),
    # Re-scrape ATTEMPTED 2026-06-28 (phase1c-rescrape workflow) and confirmed un-scrapeable:
    ("fed_fdic_enforcement",       "#38",  "re-scrape failed: orders.fdic.gov is a Salesforce SPA, guest API blocked; ED&O is PDF-only"),
    ("fed_doj_fca_settlements",    "#84",  "re-scrape failed: no machine-readable FCA-settlements feed (press releases / PDF stats only)"),
    ("fed_doj_crt_cases",          "#93",  "re-scrape failed: no machine-readable CRT case feed (per-case HTML only)"),
]

# Re-scrape SUCCEEDED for these -- now carry real data, do NOT demote:
#   fed_slavevoyages_intraamerican (201 -> 11,521 voyages via api.slavevoyages.org I-Am1.0.csv)
#   fed_naag_multistate_settlements (26 -> 882 settlements via attorneysgeneral.org Ninja Tables AJAX)
RESCRAPE_SUCCEEDED = {"fed_slavevoyages_intraamerican", "fed_naag_multistate_settlements"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Demote dead-scrape loads to STATUS='empty'.")
    ap.add_argument("extra", nargs="*", help="extra source_ids to demote (e.g. a failed re-scrape)")
    ap.add_argument("--apply", action="store_true", help="WRITE: set STATUS='empty' (ACCOUNTADMIN)")
    args = ap.parse_args()

    targets = [(s, f, r) for s, f, r in DEMOTE]
    for sid in args.extra:
        if sid in RESCRAPE_SUCCEEDED:
            print(f"  skipping {sid}: re-scrape SUCCEEDED, carries real data -- not demoting.")
            continue
        targets.append((sid, "--", "explicitly demoted (manual)"))

    mode = "APPLY" if args.apply else "PREVIEW (reads only, no writes)"
    print("=" * 78)
    print(f"DEAD-SCRAPE DEMOTE  --  {mode}")
    print("=" * 78)

    fqn = (f'"{settings.meta_database}"."{settings.ingest_log_schema}".'
           f'"{settings.ingest_log_table}"')
    conn = snow.connect()
    try:
        cur = conn.cursor()
        # Current latest status per target, so the preview shows what actually changes.
        sids = [t[0] for t in targets]
        placeholders = ",".join(["%s"] * len(sids))
        cur.execute(
            f"SELECT source_id, status, row_count FROM {fqn} r "
            f"WHERE source_id IN ({placeholders}) AND started_at = "
            f"(SELECT MAX(started_at) FROM {fqn} s WHERE s.source_id=r.source_id)",
            tuple(sids))
        cur_state = {r[0]: (r[1], r[2]) for r in cur.fetchall()}
        cur.close()

        print(f"\n{'SOURCE_ID':<34} {'FINDING':>7} {'NOW':>9} {'ROWS':>8}  REASON")
        print(f"{'-'*34} {'-'*7} {'-'*9} {'-'*8}  {'-'*30}")
        to_apply = []
        for sid, finding, reason in targets:
            st, rc = cur_state.get(sid, ("(no run)", None))
            rcs = f"{rc:,}" if isinstance(rc, int) else "-"
            flag = "" if st == "success" else "  [already non-success / no run -- skip]"
            print(f"{sid:<34} {finding:>7} {str(st):>9} {rcs:>8}  {reason[:46]}{flag}")
            if st == "success":
                to_apply.append((sid, finding, reason))

        if not args.apply:
            print(f"\n{len(to_apply)} run(s) would be demoted success -> empty.")
            print("PREVIEW only -- re-run with --apply to write (Chris runs --apply).")
            return 0

        cur = conn.cursor()
        n = 0
        for sid, finding, reason in to_apply:
            note = (f"[dead-scrape demote {pd.Timestamp.utcnow():%Y-%m-%d}] {finding}: {reason} "
                    "-- demoted success->empty; catalog LIFECYCLE follows on next derive.")
            cur.execute(
                f"UPDATE {fqn} SET STATUS='empty', "
                "MESSAGE = LEFT(COALESCE(MESSAGE,'') || ' || ' || %s, 4000) "
                "WHERE source_id=%s AND STATUS='success' AND started_at = "
                f"(SELECT MAX(started_at) FROM {fqn} s WHERE s.source_id=%s AND s.status='success')",
                (note, sid, sid))
            n += cur.rowcount or 0
        conn.commit()
        cur.close()
        print(f"\nAPPLIED: demoted {n} run(s) to STATUS='empty'.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
