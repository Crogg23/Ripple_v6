"""The OSHA cohort-outlier finding -> a reviewable LEADS artifact with a receipt.

connect.cohort scores every establishment against its own peer cohort and writes a
CSV for a human to read. That CSV is not yet a claim a hostile skeptic can verify or
a human can sign off on -- it has no frozen SQL, no content hash, no pinned data
snapshot, and no path through the two-step publish gate. This module closes that
gap WITHOUT inventing a parallel trust format: it reuses the same LIBRARY_META.
CONNECT.LEADS table and the same persistence helpers (leads._ensure_leads_table,
leads._merge_leads, leads._expire_rule) that every cross-domain lead job uses.

It does NOT go through leads.compile_sql / leads_specs.JOBS -- that machinery
assumes a hard-key LEFT-flag ⋈ RIGHT-active intersection, and this finding is a
single-source aggregation (one establishment scored against its own cohort), a
different shape. So COHORT_SPECS below is a minimal stand-in spec -- just enough
(`left`/`right` table names) for receipt.py's source_tables / resolve_snapshots /
source_urls to pin the one source table this finding reads. receipt.py's spec
lookup falls back to COHORT_SPECS when a RULE_NAME isn't a registered JobSpec, so
`connect receipt --id LEAD_xxx --check` works unmodified for this rule too.

    python -m connect.cohort_leads --year 2024              # dry-run preview
    python -m connect.cohort_leads --year 2024 --write       # persist to LEADS
"""

from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import date

import pandas as pd

from . import cohort, db, receipt, safety, store
from .leads import _ensure_leads_table, _expire_rule, _merge_leads

RULE_NAME = "osha_cohort_outlier_2024"

# Minimal stand-in "spec" -- just enough for receipt.source_tables/resolve_snapshots/
# source_urls, which only ever read spec["left"]["table"] / spec["right"]["table"].
# Both point at the same table because this finding has exactly one source: left ==
# right collapses to a single pinned snapshot (receipt.source_tables dedupes).
COHORT_SPECS: dict[str, dict] = {
    RULE_NAME: {
        "left": {"table": cohort.OSHA_TABLES[2024]},
        "right": {"table": cohort.OSHA_TABLES[2024]},
    }
}

# Same ranking floor cohort.run() prints/writes to CSV -- the LEADS rows must be the
# exact same set a human reviewing outputs/cohort_outliers_2024.csv is looking at.
MIN_DART_CASES = 5
MIN_FOLD = 2


def build_compiled_sql(year: int, naics_digits: int = 4,
                        min_hours: int = cohort.MIN_HOURS,
                        min_cohort: int = cohort.MIN_COHORT) -> str:
    """The exact, frozen, runnable query behind every lead this module writes.

    No CURRENT_DATE / wall-clock dependency (cohort.build_sql has none), so this is
    reproducible forever against the pinned source snapshot. LEFT_KEY_VALUE is the
    grain-identifying composite key (EIN + the establishment's dedup key) so
    receipt._verify's generic re-run check works unmodified for this rule too.
    """
    base = cohort.build_sql(year, naics_digits, min_hours, min_cohort)
    return f"""
WITH ranked_est AS ({base})
SELECT *, EIN || '|' || EST_KEY AS LEFT_KEY_VALUE
FROM ranked_est
WHERE dart_cases >= {MIN_DART_CASES} AND fold_vs_pooled >= {MIN_FOLD}
ORDER BY fold_vs_pooled DESC, dart_cases DESC
"""


def _lead_id(key_value: str) -> str:
    """Same scheme as leads._lead_id: stable across runs so MERGE tracks FIRST_SEEN."""
    return "LEAD_" + hashlib.md5(f"{RULE_NAME}|EIN_EST:{key_value}".encode()).hexdigest()[:16]


def _title(r: dict) -> str:
    """Neutral, peer-relative claim -- never negligence/wrongdoing language.
    That determination is Chris's call (RED lane, CLAUDE.md), not this finding's."""
    name = r["COMPANY"] or r["ESTABLISHMENT"] or r["EIN"]
    site = ", ".join(x for x in (r.get("CITY"), r.get("STATE")) if x)
    death_note = f"; {int(r['DEATHS'])} workplace death(s) reported" if (r.get("DEATHS") or 0) >= 1 else ""
    return (f"{name} ({site}) — DART injury rate {r['DART_RATE']} is {r['FOLD_VS_POOLED']}x its "
            f"NAICS-{r['NAICS']} {r['SIZE_BAND']}-employee peer cohort's pooled rate "
            f"({int(r['DART_CASES'])} DART cases in {int(r['HOURS']):,} hours worked){death_note}")


def build_rows(conn, run_id: str, dry_run: bool) -> pd.DataFrame:
    sql = build_compiled_sql(2024)
    sha = receipt.sql_sha256(sql)
    as_of = date.today().isoformat()
    spec = COHORT_SPECS[RULE_NAME]
    snapshots = json.dumps([] if dry_run else receipt.resolve_snapshots(conn, spec))
    rows = db.dicts(conn, sql)
    recs = []
    for r in rows:
        evidence = [{
            "naics": r["NAICS"], "industry": r["INDUSTRY"], "size_band": r["SIZE_BAND"],
            "city": r["CITY"], "state": r["STATE"],
            "employees": int(r["EMPLOYEES"] or 0), "hours": int(r["HOURS"] or 0),
            "dart_rate": float(r["DART_RATE"]), "cohort_pooled_dart": float(r["COHORT_POOLED_DART"]),
            "fold_vs_pooled": float(r["FOLD_VS_POOLED"]), "cohort_n": int(r["COHORT_N"]),
            "dart_cases": int(r["DART_CASES"]), "deaths": int(r["DEATHS"] or 0),
        }]
        recs.append({
            "LEAD_ID": _lead_id(r["LEFT_KEY_VALUE"]),
            "RULE_NAME": RULE_NAME,
            "LEFT_KEY_TYPE": "EIN|EST_KEY",
            "LEFT_KEY_VALUE": r["LEFT_KEY_VALUE"],
            "TITLE": _title(r),
            "SCORE": float(r["FOLD_VS_POOLED"]),
            "EVIDENCE": json.dumps(evidence),
            "EVIDENCE_COUNT": 1,
            "RUN_ID": run_id,
            "COMPILED_SQL": sql,
            "SQL_SHA256": sha,
            "AS_OF_DATE": as_of,
            "SOURCE_SNAPSHOTS": snapshots,
        })
    return pd.DataFrame(recs)


def run(write: bool = False, top: int = 20) -> dict:
    """Scoped to 2024 only, on purpose (CLAUDE.md scope law): this finish-line task
    is one finding, not a platform feature. Extending to other years is explicitly
    out of scope for this session."""
    run_id = uuid.uuid4().hex[:16]
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        if write:
            _ensure_leads_table(conn)
        sup = safety.suppressed(conn, "lead")  # rejected/retracted -> never shown as fact
        df = build_rows(conn, run_id, dry_run=not write)
        shown = df[~df["LEAD_ID"].isin(sup)] if len(df) else df
        hidden = len(df) - len(shown)
        print(f"[{RULE_NAME}] {len(shown)} leads  ({'writing' if write else 'DRY-RUN'})"
              + (f" — {hidden} hidden by review/retraction" if hidden else ""))
        for i, r in enumerate(shown.sort_values("SCORE", ascending=False).head(top).itertuples(index=False), 1):
            print(f"  {i:>2}. [{r.SCORE:.2f}x] {r.TITLE}")
        if write:
            if len(df):
                _merge_leads(conn, df)
            _expire_rule(conn, RULE_NAME, run_id)
            print(f"  merged {len(df)} into {store.cfqn('LEADS')}; staleness swept (run {run_id})")
            print("\n  ⚑ these leads are UNREVIEWED — none read as PUBLISHED fact. Two-step gate: "
                  "a human confirms first\n     `connect review lead <LEAD_ID> confirmed --by <you>`  "
                  "then publishes explicitly via `python scripts/publish_lead.py`\n     "
                  "(`connect safety` shows the ledger)")
        return {"rule": RULE_NAME, "leads": len(df)}
    finally:
        conn.close()


def main() -> int:
    ap = argparse.ArgumentParser(prog="connect.cohort_leads")
    ap.add_argument("--write", action="store_true", help="persist to LIBRARY_META.CONNECT.LEADS (default previews only)")
    ap.add_argument("--top", type=int, default=20)
    a = ap.parse_args()
    run(write=a.write, top=a.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
