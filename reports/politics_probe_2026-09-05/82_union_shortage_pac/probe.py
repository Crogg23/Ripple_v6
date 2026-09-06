import os, sys
from _shared.q import run, open_log
from _shared.cols import cols
HERE = os.path.dirname(os.path.abspath(__file__)); open_log(os.path.join(HERE, "probe.log"))
STEP = int(os.environ.get("STEP", "1"))
if STEP == 1:
    cols("LIBRARY_MARTS", "LABOR", "LABOR__FED_DOL_OLMS")
    cols("LIBRARY_MARTS", "FINANCE", "FINANCE__FED_FEC_COMMITTEES_DIM")
    cols("LIBRARY_MARTS", "FINANCE", "FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE")
if STEP == 2:
    print(run("""select count(*) n, count(shortage_amount) sh_nonnull, sum(iff(shortage_amount>0,1,0)) sh_pos, sum(iff(shortage_amount>0,shortage_amount,0)) sh_dollars,
      min(year_covered) y0, max(year_covered) y1, count(distinct file_number) files, count(distinct union_name) unions
      from LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS""", "olms fill"))
    print(run("select pac_funds, count(*) n from LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS group by 1 order by 2 desc", "pac_funds values"))
    print(run("select union_name, affiliation_abbr, unit_name, designation_name, year_covered, shortage_amount, pac_funds, total_receipts from LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS where shortage_amount>0 order by shortage_amount desc limit 5", "shortage sample"))
    print(run("select connected_org_nm, count(*) n, count(distinct cmte_id) cmtes from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM where org_tp='L' group by 1 order by 2 desc limit 8", "fec labor connected orgs"))
if STEP == 3:
    # are all 78 shortage rows column-shifted junk? (numeric union_name, null year, shortage value that reads like a year)
    print(run("""select count(*) n, sum(iff(regexp_like(union_name,'^[0-9]+$'),1,0)) numeric_name, sum(iff(year_covered is null,1,0)) null_year,
      sum(iff(shortage_amount between 1990 and 2030,1,0)) looks_like_year, sum(iff(total_receipts is null,1,0)) null_receipts
      from LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS where shortage_amount>0""", "shortage rows junk check"))
if STEP == 4:
    print(run("select column_name from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='FED_DOL_OLMS' and column_name ilike '%SHORT%'", "landing shortage col"))
if STEP == 5:
    print(run("select count(*) n, count(nullif(trim(SHORTAGE),'')) sh, sum(iff(try_to_number(SHORTAGE)>0,1,0)) pos from LIBRARY_RAW.LANDING.FED_DOL_OLMS", "landing shortage fill"))
