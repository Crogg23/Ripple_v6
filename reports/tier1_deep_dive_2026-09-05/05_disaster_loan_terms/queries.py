"""Hunch 5 - disaster loan terms. Every query, in run order. SELECT only.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/05_disaster_loan_terms/queries.py
Writes two aggregate CSVs beside this file; analysis.py does the math and the story."""
import csv, os
from _shared.q import run, open_log
HERE = os.path.dirname(os.path.abspath(__file__))
open_log(os.path.join(HERE, "queries.log"))
F = "LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS"
H = "LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC"

def dump(rows, name):
    with open(os.path.join(HERE, name), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# --- structure checks (LIMIT 5 first, per the brief) ---
run(f"select * from {F} limit 5", "fema_sample")
run(f"select * from {H} limit 5", "hmda_sample")
run(f"select column_name,data_type from LIBRARY_MARTS.information_schema.columns where table_schema='HOUSING' and table_name='HOUSING__FED_CFPB_HMDA_HISTORIC' and column_name ilike '%date%'", "hmda_date_cols")

# --- first-pass repro (47 / 6,090,110 / 636) ---
r = run(f"""select count(distinct DISASTER_NUMBER) dis, count(*) regs, count(distinct FIPS) fips,
 min(length(FIPS)) minlen, max(length(FIPS)) maxlen, sum(iff(FIPS is null,1,0)) nullfips,
 count(distinct lpad(FIPS,5,'0')) fips5
 from {F} where DECLARATION_DATE between '2015-01-01' and '2017-12-31'""", "fema_firstpass_repro")
print(r)

# --- FEMA: one row per disaster county (padded FIPS), 2015-2017 declarations ---
fema = run(f"""select lpad(FIPS,5,'0') fips5, DAMAGED_STATE_ABBREVIATION st, DISASTER_NUMBER dn,
 min(DECLARATION_DATE) decl, min(INCIDENT_TYPE_CODE) itype, count(*) regs
 from {F} where DECLARATION_DATE between '2015-01-01' and '2017-12-31' and FIPS is not null
 group by 1,2,3""", "fema_county_disaster")
dump(fema, "fema_county_disaster.csv")

# --- HMDA: county-year aggregates, 2015-2017, all states. ~9.6k rows out of 45M in. ---
hm = run(f"""select AS_OF_YEAR yr, STATE_ABBR st, lpad(STATE_CODE,2,'0')||lpad(COUNTY_CODE,3,'0') fips5,
 count(*) rows_all,
 sum(iff(ACTION_TAKEN in ('1','2','3'),1,0)) apps,
 sum(iff(ACTION_TAKEN in ('1','2','3','4','5'),1,0)) apps_wide,
 sum(iff(ACTION_TAKEN='3',1,0)) denied,
 sum(iff(ACTION_TAKEN='1',1,0)) orig,
 sum(iff(ACTION_TAKEN='1' and RATE_SPREAD is not null,1,0)) orig_rs,
 sum(iff(ACTION_TAKEN='1' and HOEPA_STATUS='1',1,0)) orig_hoepa,
 sum(iff(ACTION_TAKEN='1' and LIEN_STATUS='1',1,0)) orig_lien1,
 sum(iff(ACTION_TAKEN='1' and LIEN_STATUS='1' and RATE_SPREAD is not null,1,0)) orig_lien1_rs,
 avg(iff(ACTION_TAKEN='1',RATE_SPREAD,null)) avg_rs
 from {H} where AS_OF_YEAR in ('2015','2016','2017') and COUNTY_CODE is not null
 group by 1,2,3""", "hmda_county_year")
dump(hm, "hmda_county_year.csv")

# --- second-way rebuild of the first-pass HMDA year counts ---
print(run(f"select AS_OF_YEAR, count(*) n from {H} where AS_OF_YEAR in ('2015','2016','2017') group by 1 order by 1", "hmda_year_counts"))

# --- denial reasons by county-year, 13 states that had a 2016 declaration. Why did denials hold up? ---
dr = run(f"""select AS_OF_YEAR yr, STATE_ABBR st, lpad(STATE_CODE,2,'0')||lpad(COUNTY_CODE,3,'0') fips5,
 coalesce(DENIAL_REASON_1,'none') reason, count(*) n
 from {H} where AS_OF_YEAR in ('2015','2016','2017') and ACTION_TAKEN='3' and COUNTY_CODE is not null
 and STATE_ABBR in ('AR','FL','GA','LA','MN','MO','MS','NC','SC','TN','TX','VA','WV')
 group by 1,2,3,4""", "denial_reasons_county_year")
dump(dr, "denial_reasons_county_year.csv")
print(run(f"select DENIAL_REASON_1, DENIAL_REASON_NAME_1, count(*) n from {H} where AS_OF_YEAR='2016' and ACTION_TAKEN='3' group by 1,2 order by 1", "denial_reason_codes"))
