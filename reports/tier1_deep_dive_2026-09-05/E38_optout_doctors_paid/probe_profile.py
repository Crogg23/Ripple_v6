from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid/queries.log")
H="LIBRARY_MARTS.HEALTH."
for t in ["HEALTH__FED_CMS_OPEN_PAYMENTS","HEALTH__FED_CMS_OPEN_PAYMENTS_2022","HEALTH__FED_CMS_OPEN_PAYMENTS_2023"]:
    for r in run(f"select PROGRAM_YEAR, count(*) n, count(distinct RECORD_ID) rid, count(distinct NPI) npis, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd, min(DATE_OF_PAYMENT) d0, max(DATE_OF_PAYMENT) d1 from {H}{t} group by 1 order by 1", f"py {t}"): print(t, r)
# overlap of record ids between the three
print(run(f"""select count(*) n from (select RECORD_ID from {H}HEALTH__FED_CMS_OPEN_PAYMENTS where PROGRAM_YEAR=2023) a join (select RECORD_ID from {H}HEALTH__FED_CMS_OPEN_PAYMENTS_2023) b using(RECORD_ID)""","overlap main vs 2023"))
print(run(f"""select count(*) n from (select RECORD_ID from {H}HEALTH__FED_CMS_OPEN_PAYMENTS where PROGRAM_YEAR=2022) a join (select RECORD_ID from {H}HEALTH__FED_CMS_OPEN_PAYMENTS_2022) b using(RECORD_ID)""","overlap main vs 2022"))
print(run(f"select COVERED_RECIPIENT_TYPE, count(*) n, count(distinct NPI) npis from {H}HEALTH__FED_CMS_OPEN_PAYMENTS group by 1 order by 2 desc","recipient types"))
# opt-out profile
print(run(f"select count(*) n, count(distinct NPI) npis, min(OPTOUT_EFFECTIVE_DATE) e0, max(OPTOUT_EFFECTIVE_DATE) e1, min(OPTOUT_END_DATE) x0, max(OPTOUT_END_DATE) x1, min(length(NPI)) l0, max(length(NPI)) l1, count(distinct LAST_UPDATED) lu from {H}HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS","optout profile"))
for r in run(f"select year(OPTOUT_EFFECTIVE_DATE) y, count(*) n, count(distinct NPI) npis from {H}HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS group by 1 order by 1","optout by year"): print(r)
print(run(f"select * from {H}HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS where NPI in (select NPI from {H}HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS group by 1 having count(*)>1) order by NPI limit 8","optout dupes sample"))
for r in run(f"select SPECIALTY, count(*) n from {H}HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS group by 1 order by 2 desc limit 15","optout specialties"): print(r)
