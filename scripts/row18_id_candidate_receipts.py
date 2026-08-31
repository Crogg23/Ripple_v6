"""Row 18 receipts: COUNT / COUNT(DISTINCT) / samples for the unregistered ID candidates.

Read-only. Dumps reports/row1/row18_id_candidate_receipts.json.
Re-runs the 2026-08-31 verification, including the UPIN blank-string resolution.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "reports", "row1", "row18_id_candidate_receipts.json")

CHECKS = [
    ("CONTRACT_AWARD_UNIQUE_KEY", "LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS", "CONTRACT_AWARD_UNIQUE_KEY"),
    ("TICKER", "LIBRARY_RAW.LANDING.FED_SENATE_STOCK_WATCHER", "TICKER"),
    ("UPIN", "LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE", "nullif(trim(UPIN),'')"),
    ("CLIENT_ID", "LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS", "CLIENT_ID"),
    ("REGISTRANT_ID", "LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS", "REGISTRANT_ID"),
    ("NID_judge", "LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE", "NID"),
    ("NID_appt", "LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT", "NID"),
    ("COMMITTEE_CODE", "LIBRARY_RAW.LANDING.FED_CONGRESS_COMMITTEE_MEMBERSHIP", "COMMITTEE_CODE"),
    ("BILL_NUMBER", "LIBRARY_MARTS.POLITICS.POLITICS__BILLS", "BILL_NUMBER"),
    ("JUSTICE_CODE", "LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_SCOTUS", "JUSTICE_CODE"),
    ("SUB_ID", "LIBRARY_RAW.LANDING.FED_FEC_INDIV_CONTRIBUTIONS", "SUB_ID"),
]


def main():
    conn = connect()
    cur = conn.cursor()
    out = {}
    for label, table, expr in CHECKS:
        cur.execute(f"select count(*), count({expr}), count(distinct {expr}) from {table}")
        tot, filled, dist = cur.fetchone()
        cur.execute(f"select distinct {expr} from {table} where {expr} is not null "
                    f"order by random() limit 5")
        out[label] = dict(table=table, rows=tot, filled=filled, distinct=dist,
                          samples=[str(r[0])[:40] for r in cur.fetchall()])
        print(f"{label}: rows {tot:,} filled {filled:,} distinct {dist:,}")
    conn.close()
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
