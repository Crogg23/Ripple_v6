import os, sys
from _shared.q import run, open_log
from _shared.cols import cols
HERE = os.path.dirname(os.path.abspath(__file__)); open_log(os.path.join(HERE, "probe.log"))
STEP = int(os.environ.get("STEP", "1"))
if STEP == 1:
    cols("LIBRARY_MARTS", "GOVERNANCE", "GOVERNANCE__FED_REVOLVINGDOOR_PROJECT")
    cols("LIBRARY_RAW", "LANDING", "FED_USASPENDING_CONTRACTS_FULL_R2")
if STEP == 2:
    print(run("select count(*) n, count(distinct person_name) people, count(distinct agency) agencies, count(distinct industry_sector) sectors, sum(iff(is_political_appointee,1,0)) appointees, sum(iff(is_revolving_door,1,0)) rd from LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT", "rdp fill"))
    print(run("select agency, count(*) n from LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT group by 1 order by 2 desc limit 10", "rdp agencies"))
    print(run("select industry_sector, count(*) n from LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT group by 1 order by 2 desc limit 10", "rdp sectors"))
    print(run("select person_name, agency, industry_sector, position_name, sector1, sector1_interest, sector2, is_political_appointee from LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT limit 5", "rdp sample"))
    print(run("select min(_ingested_at) i0, max(_ingested_at) i1, count(distinct _source_run_id) runs from LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT", "rdp vintage"))
if STEP == 3:
    print(run("select person_name, count(*) n from LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT group by 1", "person_name values"))
if STEP == 4:
    print(run("select column_name from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='FED_REVOLVINGDOOR_PROJECT' order by ordinal_position", "landing cols"))
