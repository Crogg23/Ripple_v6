"""Wave-3 extractions: bank branches (Voronoi), money-shape (FEC amounts)."""
import json, os, sys
sys.path.insert(0, r"c:\Code\Ripple_v6")
from scripts._snowflake_conn import connect
OUT = os.path.dirname(os.path.abspath(__file__))
conn = connect(); cur = conn.cursor()
def q(sql):
    cur.execute(sql); return cur.fetchall()

print("fdic branches...", flush=True)
rows = q("""
select SIMS_LATITUDE, SIMS_LONGITUDE, BRANCH_DEPOSITS_THOUSANDS,
       upper(coalesce(BRANCH_STATE_NAME,'')), BRANCH_COUNTY_FIPS, INSTITUTION_NAME
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS
where SURVEY_YEAR = (select max(SURVEY_YEAR) from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS)
  and SIMS_LATITUDE is not null and SIMS_LONGITUDE is not null
  and SIMS_LATITUDE between 17 and 72 and SIMS_LONGITUDE between -180 and -60
""")
json.dump([[round(float(r[0]),4), round(float(r[1]),4),
            int(r[2]) if r[2] is not None else 0, r[3], r[4], (r[5] or "")[:40]] for r in rows],
          open(os.path.join(OUT, "branches.json"), "w"), separators=(",", ":"))
print(f"  {len(rows)} branches", flush=True)

print("fec amount shape...", flush=True)
# exact-amount counts for the 300 most common amounts + first-digit distribution + $ near limits
rows = q("""
select TRANSACTION_AMT, count(*)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
where TRANSACTION_AMT > 0 and TRANSACTION_AMT < 1000000
group by 1 order by 2 desc limit 300
""")
json.dump([[float(r[0]), int(r[1])] for r in rows],
          open(os.path.join(OUT, "fec_amounts.json"), "w"), separators=(",", ":"))
rows = q("""
select left(to_varchar(cast(TRANSACTION_AMT as integer)),1), count(*), sum(TRANSACTION_AMT)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
where TRANSACTION_AMT >= 1 and TRANSACTION_AMT < 1000000
group by 1 order by 1
""")
json.dump([[r[0], int(r[1]), float(r[2])] for r in rows],
          open(os.path.join(OUT, "fec_digits.json"), "w"), separators=(",", ":"))
# yearly totals for context
rows = q("""
select year(TRANSACTION_DATE), count(*), sum(TRANSACTION_AMT)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
where TRANSACTION_DATE between '2000-01-01' and '2026-12-31' and TRANSACTION_AMT > 0
group by 1 order by 1
""")
json.dump([[int(r[0]), int(r[1]), float(r[2])] for r in rows],
          open(os.path.join(OUT, "fec_years.json"), "w"), separators=(",", ":"))
print("DONE")
conn.close()
