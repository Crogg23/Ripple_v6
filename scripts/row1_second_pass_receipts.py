"""Row 1 second-pass receipts: re-runnable queries behind the 2026-08-31 claims.

Read-only. Dumps reports/row1/second_pass_receipts.json:
  - ASSISTANCE_FULL fiscal-year histogram (the member-slice truncation evidence)
  - MDS REPORT_DATE histogram incl. NULLs
  - dialysis COUNT(*) (publisher stats API said 12,456,456)
  - Part D ingest-log row (DY2022 receipt)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "reports", "row1")


def main():
    conn = connect()
    cur = conn.cursor()
    out = {}

    cur.execute('''select "action_date_fiscal_year", count(*)
        from LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FULL group by 1 order by 1''')
    out["assistance_full_by_fy"] = {str(r[0]): r[1] for r in cur.fetchall()}

    cur.execute('''select coalesce(REPORT_DATE, '<NULL>'), count(*)
        from LIBRARY_RAW.LANDING.FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY
        group by 1 order by 1''')
    out["mds_by_report_date"] = {str(r[0]): r[1] for r in cur.fetchall()}

    cur.execute("select count(*) from LIBRARY_RAW.LANDING.FED_CMS_MEDICARE_DIALYSIS_FACILITIES")
    out["dialysis_count_star"] = cur.fetchone()[0]

    cur.execute("""select SOURCE_ID, RUN_ID, ROW_COUNT, SOURCE_URL, MESSAGE
        from LIBRARY_META.INGEST_LOGS.INGEST_RUNS
        where RUN_ID = '431c13fc-5535-493a-9536-fe7c55070255'""")
    r = cur.fetchone()
    out["partd_ingest_run"] = dict(zip(
        ["source_id", "run_id", "row_count", "source_url", "message"], r)) if r else None

    zip_sources = [
        "FED_CFPB_COMPLAINTS", "INTL_GLEIF", "FED_NHTSA_COMPLAINTS", "FED_NHTSA_RECALLS",
        "FED_NHTSA_INVESTIGATIONS", "FED_OSHA_INSPECTIONS", "FED_OSHA_VIOLATIONS",
        "FED_DOL_WHD_WHISARD", "FED_MSHA_VIOLATIONS", "FED_MSHA_ACCIDENTS", "FED_MSHA_MINES",
        "FED_SEC_INSIDER", "FED_USASPENDING_CONTRACTS_FULL", "FED_USASPENDING_ASSISTANCE_FULL",
        "FED_FEC_COMMITTEES", "FED_FEC_CANDIDATES", "FED_FEC_CAND_CMTE_LINKAGE",
        "FED_FEC_PAC_SUMMARY",
    ]
    names = ",".join(f"'{s}'" for s in zip_sources)
    cur.execute(f"""select SOURCE_ID, STARTED_AT, STATUS, ROW_COUNT
        from LIBRARY_META.INGEST_LOGS.INGEST_RUNS
        where upper(SOURCE_ID) in ({names}) order by SOURCE_ID, STARTED_AT""")
    out["zip_spec_ingest_runs"] = [
        {"source_id": r[0], "started_at": str(r[1]), "status": r[2], "row_count": r[3]}
        for r in cur.fetchall()]
    cur.execute(f"""select table_name, row_count from LIBRARY_RAW.information_schema.tables
        where table_schema='LANDING' and table_name in ({names})""")
    out["zip_spec_landing_counts"] = {r[0]: r[1] for r in cur.fetchall()}

    out["shrunk_tables_count_star"] = {}
    for t in ["FED_FEC_CANDIDATES", "FED_FEC_COMMITTEES", "FED_NHTSA_RECALLS"]:
        cur.execute(f"select count(*) from LIBRARY_RAW.LANDING.{t}")
        out["shrunk_tables_count_star"][t] = cur.fetchone()[0]

    # row 16: checkpoint sums vs landing
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(repo, "logs", "sec13f_checkpoint.json")) as fh:
        tf = json.load(fh)
    out["sec13f"] = {
        "zips_in_checkpoint": sorted(tf.keys()),
        "infotable_sum": sum(v.get("INFOTABLE", 0) for v in tf.values()),
    }
    with open(os.path.join(repo, "logs", "faers_checkpoint.json")) as fh:
        fa = json.load(fh)
    out["faers_checkpoint_quarters"] = sorted(fa.keys()) if isinstance(fa, dict) else fa
    with open(os.path.join(repo, "outputs",
                           "nobrainer_load_checkpoint_2026-08-29.json")) as fh:
        nb = json.load(fh)
    out["campd"] = {
        k: {"rows": sum(v.get("rows", 0) for v in e.values() if isinstance(v, dict)),
            "chunks": len(e),
            "missing": sorted(kk for kk, v in e.items()
                              if isinstance(v, dict) and v.get("missing"))}
        for k, e in nb.items()}

    out["row16_landing"] = {}
    for t in ["FED_SEC_13F_HOLDINGS", "FED_EPA_CAMPD_EMISSIONS_DAILY",
              "FED_EPA_CAMPD_FACILITY", "FED_CPSC_NEISS", "FED_FDA_FAERS_DEMO",
              "FED_FDA_FAERS_DRUG", "FED_FDA_FAERS_REAC", "FED_FDA_FAERS_INDI",
              "FED_FDA_FAERS_OUTC"]:
        cur.execute(f"select count(*) from LIBRARY_RAW.LANDING.{t}")
        out["row16_landing"][t] = cur.fetchone()[0]
    conn.close()

    with open(os.path.join(OUT, "second_pass_receipts.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: (v if not isinstance(v, dict) or len(v) < 30 else "...")
                      for k, v in out.items()}, indent=1))


if __name__ == "__main__":
    main()
