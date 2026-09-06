"""E39 - paid opioid prescribers. Every query run for this hunch, in the order it ran.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E39_paid_opioid_prescribers/queries.py
Each block below was one script during the work; they are kept verbatim as functions. Results land in the scratchpad as JSON
and are logged to queries.log by _shared.q.run. SELECT only.
"""
from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/E39_paid_opioid_prescribers/queries.log")
# Brand list ONLY. An earlier version also carried bare generics (TRAMADOL|OXYCODONE|HYDROCODONE|MORPHINE|FENTANYL|
# HYDROMORPHONE|TAPENTADOL|OXYMORPHONE|BUPRENORPHINE). Bare BUPRENORPHINE would catch Suboxone/Sublocade/Brixadi generic
# strings (addiction treatment, not painkillers); in PY2024 it hit 1 NPI by luck. Tightened 2026-09-05; every headline number
# re-ran identical to the cent (38.71% / 6,477). The generics matched 1-8 NPIs each and never moved a number.
SCRATCH="/private/tmp/claude-501/-Users-chrisr--Desktop-The-Ripple-Portfolio-Ripple-v6/8b65fde3-6771-4850-89e5-068eb53d8a29/scratchpad"

def step1_probe():
    import json
    r = run("""select table_schema, table_name, row_count from LIBRARY_MARTS.information_schema.tables
     where table_name ilike '%OPEN_PAYMENTS%' or table_name ilike '%PART_D%' or table_name ilike '%PARTD%' order by 1,2""", "mart tables")
    for x in r: print(x)
    r = run("""select table_name, row_count from LIBRARY_RAW.information_schema.tables
     where table_schema='LANDING' and (table_name ilike '%OPEN_PAYMENTS%' or table_name ilike '%PARTD%' or table_name ilike '%PART_D%') order by 1""", "landing tables")
    for x in r: print(x)
    for t in ["HEALTH__FED_CMS_OPEN_PAYMENTS","HEALTH__FED_CMS_PART_D_PRESCRIBERS"]:
        r = run(f"select column_name, data_type from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='{t}' order by ordinal_position", f"cols {t}")
        print(t); print([ (x['COLUMN_NAME'],x['DATA_TYPE']) for x in r])

def step2_probe2():
    import json
    def show(r):
        for x in r: print(x)
    PD="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS"
    OP="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS"
    show(run(f"""select count(*) n, count(distinct NPI) npi_d, count(OPIOID_PRSCRBR_RATE) rate_nn,
     count(try_to_number(OPIOID_TOT_CLMS)) op_clm_nn, count(try_to_number(TOT_CLMS)) tot_nn,
     sum(case when OPIOID_TOT_CLMS='' then 1 end) op_blank, min(length(NPI)) l1, max(length(NPI)) l2 from {PD}""","pd sanity"))
    show(run(f"select PRSCRBR_ENT_CD, count(*) n from {PD} group by 1","pd ent cd"))
    show(run(f"select PRSCRBR_TYPE, count(*) n, avg(OPIOID_PRSCRBR_RATE) r from {PD} group by 1 order by 2 desc limit 15","pd top types"))
    show(run(f"select NPI, PRSCRBR_TYPE, TOT_CLMS, OPIOID_TOT_CLMS, OPIOID_PRSCRBR_RATE, OPIOID_TOT_BENES from {PD} limit 5","pd sample"))
    show(run(f"select PROGRAM_YEAR, count(*) n, count(NPI) npi_nn, count(distinct NPI) npi_d, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd from {OP} group by 1 order by 1","op undated years"))
    show(run(f"select PROGRAM_YEAR, count(*) n, count(distinct NPI) npi_d from {OP}_2022 group by 1","op 2022 years"))
    show(run(f"select PROGRAM_YEAR, count(*) n, count(distinct NPI) npi_d from {OP}_2023 group by 1","op 2023 years"))
    show(run(f"select COVERED_RECIPIENT_TYPE, count(*) n, count(NPI) npi_nn from {OP} group by 1 order by 2 desc","op recipient type"))
    show(run(f"select NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE, count(*) n, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd from {OP} group by 1 order by 2 desc limit 12","op nature"))
    show(run("""select SOURCE_ID, LANDING_FQN, * exclude(SOURCE_ID, LANDING_FQN) from LIBRARY_MARTS.PUBLIC.SOURCE_FRESHNESS where LANDING_FQN ilike '%PART_D_PRESCRIBERS%' or LANDING_FQN ilike '%OPEN_PAYMENTS%' limit 10""","freshness"))

def step3_main():
    import json
    PD="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS"
    OP22="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022"
    OP23="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023"
    out={}
    # what do the null opioid rates hide?
    out['suppression']=run(f"""select case when OPIOID_TOT_CLMS='0' then 'zero' when OPIOID_TOT_CLMS='' then 'blank' else 'positive' end k,
     count(*) n, min(try_to_number(TOT_CLMS)) min_tot, median(try_to_number(TOT_CLMS)) med_tot, min(try_to_number(OPIOID_TOT_CLMS)) min_op
     from {PD} group by 1""","pd null meaning")
    # paid vs unpaid, three ways
    base=f"""with pay as (select NPI, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd, count(*) n_pay from {OP22} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' group by 1),
     j as (select p.NPI, p.PRSCRBR_TYPE, try_to_number(p.TOT_CLMS) tot, try_to_number(p.OPIOID_TOT_CLMS) opc, p.OPIOID_PRSCRBR_RATE rate,
            p.OPIOID_LA_PRSCRBR_RATE la_rate, coalesce(y.usd,0) usd, coalesce(y.n_pay,0) n_pay, y.NPI is not null paid
       from {PD} p left join pay y on y.NPI=p.NPI)"""
    out['paid_vs_unpaid']=run(base+"""
     select paid, count(*) n, count(rate) n_rate, avg(rate) mean_rate, median(rate) med_rate,
      sum(opc)/nullif(sum(tot),0)*100 agg_rate, avg(la_rate) mean_la,
      avg(case when rate>=10 then 1.0 else 0 end) share_ge10, avg(case when opc=0 then 1.0 else 0 end) share_zero,
      avg(case when rate is null then 1.0 else 0 end) share_null, median(tot) med_tot
     from j group by 1 order by 1""","paid vs unpaid 2022")
    out['deciles']=run(base+"""
     , d as (select *, case when not paid then 0 else ntile(10) over (partition by paid order by usd) end dec from j)
     select dec, count(*) n, min(usd) usd_lo, max(usd) usd_hi, median(usd) usd_med,
      avg(rate) mean_rate, median(rate) med_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate,
      avg(case when rate>=10 then 1.0 else 0 end) share_ge10, avg(case when rate is null then 1.0 else 0 end) share_null, median(tot) med_tot
     from d group by 1 order by 1""","deciles 2022")
    out['specialty']=run(base+"""
     select PRSCRBR_TYPE, paid, count(*) n, avg(rate) mean_rate, median(rate) med_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate,
      avg(case when rate>=10 then 1.0 else 0 end) share_ge10, avg(case when rate is null then 1.0 else 0 end) share_null, median(tot) med_tot
     from j where PRSCRBR_TYPE in (select PRSCRBR_TYPE from j group by 1 order by count(*) desc limit 12)
     group by 1,2 order by 1,2""","specialty x paid 2022")
    # specialty standardised: weight unpaid specialty rates by the paid specialty mix
    out['standardised']=run(base+"""
     , s as (select PRSCRBR_TYPE, sum(case when paid then 1 end) n_paid, sum(case when not paid then 1 end) n_unpaid,
       avg(case when paid then rate end) r_paid, avg(case when not paid then rate end) r_unpaid from j group by 1)
     select sum(n_paid*r_paid)/sum(case when r_paid is not null then n_paid end) paid_actual,
            sum(n_paid*r_unpaid)/sum(case when r_unpaid is not null then n_paid end) unpaid_at_paid_mix,
            sum(n_unpaid*r_unpaid)/sum(case when r_unpaid is not null then n_unpaid end) unpaid_actual
     from s""","direct standardisation 2022")
    json.dump(out, open(SCRATCH+"/e39_main.json","w"), default=str, indent=1)
    for k,v in out.items():
        print("==",k)
        for r in v: print(r)

def step4_main2():
    import json
    PD="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS"
    OP22="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022"
    OP23="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023"
    def base(op): return f"""with pay as (select NPI, sum(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) usd, count(*) n_pay from {op} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' group by 1),
     j as (select p.NPI, p.PRSCRBR_TYPE, try_to_number(p.TOT_CLMS) tot, try_to_number(p.OPIOID_TOT_CLMS) opc, p.OPIOID_PRSCRBR_RATE rate,
            coalesce(y.usd,0) usd, y.NPI is not null paid, case when y.NPI is null then 'unpaid' when y.usd<2032.73 then 'paid_under_2k' else 'paid_top_decile' end band
       from {PD} p left join pay y on y.NPI=p.NPI)"""
    out={}
    out['top_decile_mix']=run(base(OP22)+"""
     select band, PRSCRBR_TYPE, count(*) n, avg(rate) mean_rate from j group by 1,2 qualify row_number() over (partition by band order by count(*) desc)<=8 order by 1,3 desc""","top decile specialty mix 2022")
    out['spec_band']=run(base(OP22)+"""
     select PRSCRBR_TYPE, band, count(*) n, avg(rate) mean_rate, median(rate) med_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate,
      avg(case when rate>=10 then 1.0 else 0 end) share_ge10, median(tot) med_tot
     from j where PRSCRBR_TYPE in ('Nurse Practitioner','Physician Assistant','Dentist','Internal Medicine','Family Practice')
     group by 1,2 order by 1,2""","top5 specialty x band 2022")
    out['paid_vs_unpaid_2023']=run(base(OP23)+"""
     select paid, count(*) n, avg(rate) mean_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate, avg(case when rate>=10 then 1.0 else 0 end) share_ge10 from j group by 1 order by 1""","paid vs unpaid 2023")
    out['bounded']=run(base(OP22)+"""
     select paid, count(*) n,
      sum(coalesce(opc, 1))/sum(tot)*100 agg_lo, sum(coalesce(opc,10))/sum(tot)*100 agg_hi, sum(opc)/sum(case when opc is not null then tot end)*100 agg_nonnull
     from j group by 1 order by 1""","suppression-bounded aggregate 2022")
    out['landing_cols']=run("""select column_name from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='FED_CMS_OPEN_PAYMENTS_2022' and (column_name ilike '%DRUG%' or column_name ilike '%PRODUCT%' or column_name ilike 'NPI%' or column_name ilike '%_NPI%') order by 1""","landing drug cols")
    json.dump(out, open(SCRATCH+"/e39_main2.json","w"), default=str, indent=1)
    for k,v in out.items():
        print("==",k)
        for r in v: print(r)

def step5_main3():
    import json
    PD="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS"
    L22="LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS_2022"
    # opioid analgesic brands marketed 2022 (MAT products and naloxone excluded on purpose)
    BRANDS="OXYCONTIN|XTAMPZA|NUCYNTA|BELBUCA|HYSINGLA|BUTRANS|SUBSYS|ROXYBOND|APADAZ|OXAYDO|ZOHYDRO|ARYMO|MORPHABOND|CONZIP|DSUVIA|PERCOCET|EMBEDA|EXALGO|DURAGESIC|ABSTRAL|FENTORA|LAZANDA|ACTIQ|OLINVYK|SEGLENTIS|ULTRAM|ROXICODONE|KADIAN|MS CONTIN|DILAUDID|OPANA|VICODIN|NORCO|LORTAB"
    names=" || '|' || ".join(f"coalesce(NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_{i},'')" for i in range(1,6))
    out={}
    out['registry']=run("""select table_catalog, table_schema, table_name from LIBRARY_MARTS.information_schema.tables where table_name ilike '%REGISTRY%' or table_name ilike '%FRESHNESS%' limit 20""","registry tables")
    out['opioid_names']=run(f"""select upper(trim(n)) name, count(*) n_pay, sum(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) usd, count(distinct NPI) npi_d
     from (select NPI, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS, NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1 n from {L22}
           union all select NPI, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS, NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_2 from {L22})
     where regexp_like(upper(n), '.*({BRANDS}).*') group by 1 order by 2 desc limit 40""","opioid brand names in OP 2022")
    out['targeting']=run(f"""with pay as (select NPI, sum(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) usd,
       sum(case when regexp_like(upper({names}), '.*({BRANDS}).*') then try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) else 0 end) usd_op,
       sum(case when regexp_like(upper({names}), '.*({BRANDS}).*') then 1 else 0 end) n_op
       from {L22} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' group by 1),
     j as (select p.PRSCRBR_TYPE, try_to_number(p.TOT_CLMS) tot, try_to_number(p.OPIOID_TOT_CLMS) opc, p.OPIOID_PRSCRBR_RATE rate, p.OPIOID_LA_PRSCRBR_RATE la_rate,
       case when y.NPI is null then '0 unpaid' when y.n_op=0 then '1 paid, no opioid brand' else '2 paid by opioid maker' end grp, y.usd_op
       from {PD} p left join pay y on y.NPI=p.NPI)
     select case when PRSCRBR_TYPE in ('Nurse Practitioner','Physician Assistant','Dentist','Internal Medicine','Family Practice') then PRSCRBR_TYPE else 'ALL' end spec,
       grp, count(*) n, avg(rate) mean_rate, median(rate) med_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate, avg(la_rate) mean_la,
       avg(case when rate>=10 then 1.0 else 0 end) share_ge10, median(tot) med_tot, median(usd_op) med_usd_op
     from j group by grouping sets ((spec, grp),(grp)) order by 1,2""","targeting: opioid-maker paid vs other paid vs unpaid 2022")
    json.dump(out, open(SCRATCH+"/e39_main3.json","w"), default=str, indent=1)
    for k,v in out.items():
        print("==",k)
        for r in v: print(r)

def step6_main4():
    import json
    PD="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS"
    L22="LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS_2022"
    L23="LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS_2023"
    BRANDS="OXYCONTIN|XTAMPZA|NUCYNTA|BELBUCA|HYSINGLA|BUTRANS|SUBSYS|ROXYBOND|APADAZ|OXAYDO|ZOHYDRO|ARYMO|MORPHABOND|CONZIP|DSUVIA|PERCOCET|EMBEDA|EXALGO|DURAGESIC|ABSTRAL|FENTORA|LAZANDA|ACTIQ|OLINVYK|SEGLENTIS|ULTRAM|ROXICODONE|KADIAN|MS CONTIN|DILAUDID|OPANA|VICODIN|NORCO|LORTAB"
    names=" || '|' || ".join(f"coalesce(NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_{i},'')" for i in range(1,6))
    def base(L): return f"""with pay as (select NPI, sum(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) usd,
       sum(case when regexp_like(upper({names}), '.*({BRANDS}).*') then try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) else 0 end) usd_op,
       sum(case when regexp_like(upper({names}), '.*({BRANDS}).*') then 1 else 0 end) n_op
       from {L} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' group by 1),
     j as (select p.PRSCRBR_TYPE, try_to_number(p.TOT_CLMS) tot, try_to_number(p.OPIOID_TOT_CLMS) opc, p.OPIOID_PRSCRBR_RATE rate,
       case when y.NPI is null then '0 unpaid' when y.n_op=0 then '1 paid, no opioid brand' else '2 paid by opioid maker' end grp, y.usd_op, y.n_op, y.usd
       from {PD} p left join pay y on y.NPI=p.NPI)"""
    out={}
    out['targeting_2023']=run(base(L23)+"""
     select grp, count(*) n, avg(rate) mean_rate, median(rate) med_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate,
       avg(case when rate>=10 then 1.0 else 0 end) share_ge10, median(tot) med_tot from j group by 1 order by 1""","targeting replicated on OP 2023")
    out['claims_share']=run(base(L22)+"""
     select grp, count(*) n, sum(opc) opioid_clms, sum(tot) all_clms, sum(opc)/sum(sum(opc)) over () share_of_opioid_clms, count(*)/sum(count(*)) over () share_of_prescribers
     from j group by 1 order by 1""","share of all opioid claims by group 2022")
    out['dose']=run(base(L22)+"""
     , d as (select *, ntile(5) over (order by usd_op) q from j where grp like '2%')
     select q, count(*) n, min(usd_op) lo, max(usd_op) hi, median(usd_op) med_usd, median(n_op) med_npay, avg(rate) mean_rate, median(rate) med_rate,
       sum(opc)/nullif(sum(tot),0)*100 agg_rate, avg(case when rate>=10 then 1.0 else 0 end) share_ge10, median(tot) med_tot from d group by 1 order by 1""","dose response within opioid-paid 2022")
    out['payers']=run(f"""select APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME payer, count(*) n_pay, count(distinct NPI) npi_d,
       sum(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) usd, median(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) med_usd,
       sum(case when NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE='Food and Beverage' then 1 else 0 end)/count(*) food_share
     from {L22} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' and regexp_like(upper({names}), '.*({BRANDS}).*')
     group by 1 order by 2 desc limit 12""","who pays on opioid brands 2022")
    out['registry2']=run("""select table_catalog, table_schema, table_name from LIBRARY_RAW.information_schema.tables where table_name ilike '%SOURCE%' or table_name ilike '%WATERMARK%' limit 20""","raw registry tables")
    json.dump(out, open(SCRATCH+"/e39_main4.json","w"), default=str, indent=1)
    for k,v in out.items():
        print("==",k)
        for r in v: print(r)

def step7_main5():
    import json
    for r in run("""select column_name from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='FED_CMS_PART_D_PRESCRIBERS' and column_name like '\\\\_%' escape '\\\\' or (table_schema='LANDING' and table_name='FED_CMS_PART_D_PRESCRIBERS' and column_name ilike '%INGEST%')""","pd landing audit cols"): print(r)

def step8_main6():
    import json
    for t in ["FED_CMS_PART_D_PRESCRIBERS","FED_CMS_PARTD_PRESCRIBER_DRUG"]:
        for r in run(f"select '{t}' t, _SOURCE_RUN_ID, _SRC_SHA256, min(_INGESTED_AT) mn, max(_INGESTED_AT) mx, count(*) n from LIBRARY_RAW.LANDING.{t} group by 1,2,3", f"{t} run ids"): print(r)

def step9_main7():
    import json
    PD="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS"
    L24="LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS"
    BRANDS="OXYCONTIN|XTAMPZA|NUCYNTA|BELBUCA|HYSINGLA|BUTRANS|SUBSYS|ROXYBOND|APADAZ|OXAYDO|ZOHYDRO|ARYMO|MORPHABOND|CONZIP|DSUVIA|PERCOCET|EMBEDA|EXALGO|DURAGESIC|ABSTRAL|FENTORA|LAZANDA|ACTIQ|OLINVYK|SEGLENTIS|ULTRAM|ROXICODONE|KADIAN|MS CONTIN|DILAUDID|OPANA|VICODIN|NORCO|LORTAB"
    names=" || '|' || ".join(f"coalesce(NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_{i},'')" for i in range(1,6))
    TOP5="('Nurse Practitioner','Physician Assistant','Dentist','Internal Medicine','Family Practice')"
    base=f"""with pay as (select NPI, sum(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) usd, count(*) n_pay,
       sum(case when regexp_like(upper({names}), '.*({BRANDS}).*') then try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) else 0 end) usd_op,
       sum(case when regexp_like(upper({names}), '.*({BRANDS}).*') then 1 else 0 end) n_op
       from {L24} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' group by 1),
     j as (select p.NPI, p.PRSCRBR_TYPE, try_to_number(p.TOT_CLMS) tot, try_to_number(p.OPIOID_TOT_CLMS) opc, p.OPIOID_PRSCRBR_RATE rate, p.OPIOID_LA_PRSCRBR_RATE la_rate,
       coalesce(y.usd,0) usd, y.NPI is not null paid,
       case when y.NPI is null then '0 unpaid' when y.n_op=0 then '1 paid, no opioid brand' else '2 paid by opioid maker' end grp, y.usd_op, y.n_op
       from {PD} p left join pay y on y.NPI=p.NPI)"""
    out={}
    out['ingest_run']=run("""select * from LIBRARY_META.INGEST_LOGS.INGEST_RUNS where RUN_ID='3c2495ce-6c28-437d-9c8c-5eae5dd9ebeb' or RUN_ID='431c13fc-5535-493a-9536-fe7c55070255'""","ingest runs for both Part D tables")
    out['paid_vs_unpaid']=run(base+"""
     select paid, count(*) n, count(rate) n_rate, avg(rate) mean_rate, median(rate) med_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate,
      avg(case when rate>=10 then 1.0 else 0 end) share_ge10, avg(case when rate is null then 1.0 else 0 end) share_null, median(tot) med_tot
     from j group by 1 order by 1""","PY2024 paid vs unpaid")
    out['deciles']=run(base+"""
     , d as (select *, case when not paid then 0 else ntile(10) over (partition by paid order by usd) end dec from j)
     select dec, count(*) n, min(usd) usd_lo, max(usd) usd_hi, median(usd) usd_med, avg(rate) mean_rate, median(rate) med_rate,
      sum(opc)/nullif(sum(tot),0)*100 agg_rate, avg(case when rate>=10 then 1.0 else 0 end) share_ge10, median(tot) med_tot
     from d group by 1 order by 1""","PY2024 deciles of all-industry money")
    out['standardised']=run(base+"""
     , s as (select PRSCRBR_TYPE, sum(case when paid then 1 end) n_paid, sum(case when not paid then 1 end) n_unpaid,
       avg(case when paid then rate end) r_paid, avg(case when not paid then rate end) r_unpaid from j group by 1)
     select sum(n_paid*r_paid)/sum(case when r_paid is not null then n_paid end) paid_actual,
            sum(n_paid*r_unpaid)/sum(case when r_unpaid is not null then n_paid end) unpaid_at_paid_mix,
            sum(n_unpaid*r_unpaid)/sum(case when r_unpaid is not null then n_unpaid end) unpaid_actual from s""","PY2024 direct standardisation")
    out['targeting']=run(base+f"""
     select case when PRSCRBR_TYPE in {TOP5} then PRSCRBR_TYPE else 'other specialties' end spec, grp, count(*) n,
       avg(rate) mean_rate, median(rate) med_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate, avg(la_rate) mean_la,
       avg(case when rate>=10 then 1.0 else 0 end) share_ge10, median(tot) med_tot, median(usd_op) med_usd_op,
       sum(opc) opioid_clms, sum(tot) all_clms
     from j group by grouping sets ((spec, grp),(grp)) order by 1,2""","PY2024 targeting by specialty")
    out['spec_band']=run(base+f"""
     select PRSCRBR_TYPE, case when not paid then 'unpaid' when usd<2000 then 'paid under $2k' else 'paid $2k+' end band, count(*) n,
      avg(rate) mean_rate, median(rate) med_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate, avg(case when rate>=10 then 1.0 else 0 end) share_ge10, median(tot) med_tot
     from j where PRSCRBR_TYPE in {TOP5} group by 1,2 order by 1,2""","PY2024 top5 specialty x all-money band")
    out['dose']=run(base+"""
     , d as (select *, ntile(5) over (order by usd_op) q from j where grp like '2%')
     select q, count(*) n, min(usd_op) lo, max(usd_op) hi, median(usd_op) med_usd, median(n_op) med_npay, avg(rate) mean_rate, median(rate) med_rate,
       sum(opc)/nullif(sum(tot),0)*100 agg_rate, avg(case when rate>=10 then 1.0 else 0 end) share_ge10, median(tot) med_tot from d group by 1 order by 1""","PY2024 dose response within opioid-paid")
    out['payers']=run(f"""select APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME payer, count(*) n_pay, count(distinct NPI) npi_d,
       sum(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) usd, median(try_to_number(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS)) med_usd,
       sum(case when NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE='Food and Beverage' then 1 else 0 end)/count(*) food_share
     from {L24} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' and regexp_like(upper({names}), '.*({BRANDS}).*')
     group by 1 order by 2 desc limit 12""","PY2024 who pays on opioid brands")
    out['names']=run(f"""select upper(trim(NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1)) name, count(*) n_pay, count(distinct NPI) npi_d
     from {L24} where regexp_like(upper(NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1), '.*({BRANDS}).*') group by 1 order by 2 desc limit 25""","PY2024 opioid brand names matched")
    json.dump(out, open(SCRATCH+"/e39_main7.json","w"), default=str, indent=1)
    for k,v in out.items():
        print("==",k)
        for r in v: print(r)

def step10_main8():
    import json
    PD="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS"
    L24="LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS"
    BRANDS="OXYCONTIN|XTAMPZA|NUCYNTA|BELBUCA|HYSINGLA|BUTRANS|SUBSYS|ROXYBOND|APADAZ|OXAYDO|ZOHYDRO|ARYMO|MORPHABOND|CONZIP|DSUVIA|PERCOCET|EMBEDA|EXALGO|DURAGESIC|ABSTRAL|FENTORA|LAZANDA|ACTIQ|OLINVYK|SEGLENTIS|ULTRAM|ROXICODONE|KADIAN|MS CONTIN|DILAUDID|OPANA|VICODIN|NORCO|LORTAB"
    names=" || '|' || ".join(f"coalesce(NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_{i},'')" for i in range(1,6))
    base=f"""with pay as (select NPI, sum(case when regexp_like(upper({names}), '.*({BRANDS}).*') then 1 else 0 end) n_op
       from {L24} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' group by 1),
     j as (select p.PRSCRBR_TYPE, try_to_number(p.TOT_CLMS) tot, try_to_number(p.OPIOID_TOT_CLMS) opc, p.OPIOID_PRSCRBR_RATE rate,
       case when y.NPI is null then '0 unpaid' when y.n_op=0 then '1 paid, no opioid brand' else '2 paid by opioid maker' end grp
       from {PD} p left join pay y on y.NPI=p.NPI)"""
    out={}
    out['bounded']=run(base+"""
     select grp, count(*) n, avg(case when rate is null then 1.0 else 0 end) share_null, avg(case when opc=0 then 1.0 else 0 end) share_zero,
      sum(coalesce(opc,1))/sum(tot)*100 agg_lo, sum(coalesce(opc,10))/sum(tot)*100 agg_hi, sum(opc)/sum(case when opc is not null then tot end)*100 agg_nonnull
     from j group by 1 order by 1""","PY2024 suppression-bounded group rates")
    out['who']=run(base+"""
     select PRSCRBR_TYPE, count(*) n, avg(rate) mean_rate, sum(opc)/nullif(sum(tot),0)*100 agg_rate from j where grp like '2%' group by 1 order by 2 desc limit 12""","PY2024 opioid-paid group by specialty")
    json.dump(out, open(SCRATCH+"/e39_main8.json","w"), default=str, indent=1)
    for k,v in out.items():
        print("==",k)
        for r in v: print(r)

def step11_fix():
    import json
    PD="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS"
    L24="LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS"
    # brand list only: no bare generic names (BUPRENORPHINE would catch Suboxone/Sublocade/Brixadi generics)
    BRANDS="OXYCONTIN|XTAMPZA|NUCYNTA|BELBUCA|HYSINGLA|BUTRANS|SUBSYS|ROXYBOND|APADAZ|OXAYDO|ZOHYDRO|ARYMO|MORPHABOND|CONZIP|DSUVIA|PERCOCET|EMBEDA|EXALGO|DURAGESIC|ABSTRAL|FENTORA|LAZANDA|ACTIQ|OLINVYK|SEGLENTIS|ULTRAM|ROXICODONE|KADIAN|MS CONTIN|DILAUDID|OPANA|VICODIN|NORCO|LORTAB"
    names=" || '|' || ".join(f"coalesce(NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_{i},'')" for i in range(1,6))
    base=f"""with pay as (select NPI, sum(case when regexp_like(upper({names}), '.*({BRANDS}).*') then 1 else 0 end) n_op
       from {L24} where COVERED_RECIPIENT_TYPE<>'Covered Recipient Teaching Hospital' group by 1),
     j as (select p.PRSCRBR_TYPE, try_to_number(p.TOT_CLMS) tot, try_to_number(p.OPIOID_TOT_CLMS) opc, p.OPIOID_PRSCRBR_RATE rate,
       case when y.NPI is null then '0 unpaid' when y.n_op=0 then '1 paid, no opioid brand' else '2 paid by opioid maker' end grp
       from {PD} p left join pay y on y.NPI=p.NPI)"""
    out={}
    out['std']=run(base+"""
     , s as (select PRSCRBR_TYPE, grp, sum(opc) opc, sum(tot) tot, count(*) n from j group by 1,2),
     w as (select PRSCRBR_TYPE, tot w from s where grp like '2%')
     select s.grp, sum(w.w * s.opc/nullif(s.tot,0))/sum(case when s.tot>0 then w.w end)*100 agg_at_opioid_mix, count(*) n_spec
     from s join w using (PRSCRBR_TYPE) group by 1 order by 1""","PY2024 groups standardised to opioid-maker specialty mix (claim-weighted), brand-only regex")
    out['matched']=run(base+"""
     select PRSCRBR_TYPE, grp, count(*) n, sum(opc)/nullif(sum(tot),0)*100 agg_rate from j
     where PRSCRBR_TYPE in ('Nurse Practitioner','Physician Assistant','Pain Management','Interventional Pain Management','Anesthesiology','Physical Medicine and Rehabilitation','Family Practice','Internal Medicine')
     group by 1,2 order by 1,2""","PY2024 matched specialties, brand-only regex")
    out['bound']=run(base+"""
     select sum(case when grp like '2%' then opc end) op_clms, sum(opc) op_all_nonnull, sum(coalesce(opc,10)) op_all_hi, sum(case when grp like '2%' then 1 end) n,
      sum(case when grp like '2%' then opc end)/sum(opc)*100 share_hi, sum(case when grp like '2%' then coalesce(opc,1) end)/sum(coalesce(opc,10))*100 share_lo from j""","PY2024 opioid-claims share bounds")
    json.dump(out, open(SCRATCH+"/e39_fix.json","w"), default=str, indent=1)
    for k,v in out.items():
        print("==",k)
        for r in v: print(r)

if __name__=='__main__':
    step1_probe()
    step2_probe2()
    step3_main()
    step4_main2()
    step5_main3()
    step6_main4()
    step7_main5()
    step8_main6()
    step9_main7()
    step10_main8()
    step11_fix()
