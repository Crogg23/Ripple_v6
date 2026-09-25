-- # FAERS REAC per quarter: rows, IDs filled, distinct reports, distinct report+term pairs (duplicate check)
select SRC_QUARTER q, count(*) n,
  count(nullif(trim(ISR),'')) isr_nn, count(distinct nullif(trim(ISR),'')) isr_d,
  count(nullif(trim(PRIMARYID),'')) pid_nn, count(distinct nullif(trim(PRIMARYID),'')) pid_d,
  count(distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),''))||'|'||upper(trim(PT))) pair_d
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_REAC group by 1 order by 1
-- # FAERS INDI and OUTC per quarter: same duplicate check
select 'INDI' t, SRC_QUARTER q, count(*) n,
  count(nullif(trim(ISR),'')) isr_nn, count(distinct nullif(trim(ISR),'')) isr_d,
  count(nullif(trim(PRIMARYID),'')) pid_nn, count(distinct nullif(trim(PRIMARYID),'')) pid_d,
  count(distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),''))||'|'||coalesce(DRUG_SEQ,'')||'|'||coalesce(INDI_DRUG_SEQ,'')||'|'||upper(trim(INDI_PT))) pair_d
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI group by 1,2
union all
select 'OUTC', SRC_QUARTER, count(*),
  count(nullif(trim(ISR),'')), count(distinct nullif(trim(ISR),'')),
  count(nullif(trim(PRIMARYID),'')), count(distinct nullif(trim(PRIMARYID),'')),
  count(distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),''))||'|'||upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE))))
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC group by 1,2
order by 1,2
-- # FAERS the glance's top report IDs: where do 19K / 10K / 3.7K rows for one report come from
select 'REAC' t, ISR, SRC_QUARTER q, count(*) n, count(distinct upper(PT)) dist_val, min(PT) mn, max(PT) mx
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_REAC where ISR in ('8390205','8390097') group by 1,2,3
union all
select 'INDI', ISR, SRC_QUARTER, count(*), count(distinct DRUG_SEQ||'|'||upper(INDI_PT)), min(INDI_PT), max(INDI_PT)
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI where ISR in ('6661292') group by 1,2,3
union all
select 'OUTC', ISR, SRC_QUARTER, count(*), count(distinct OUTC_COD), min(OUTC_COD), max(OUTC_COD)
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC where ISR in ('6572320','7429646') group by 1,2,3
union all
select 'DEMO', ISR, SRC_QUARTER, count(*), count(distinct C_CASE), min(C_CASE), max(MFR_SNDR)
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO where ISR in ('8390205','8390097','6661292','6572320','7429646') group by 1,2,3
order by 1,2,3
-- # Pending physicians: well-formed NPIs, and one pass of semi-joins to NPPES, PECOS, opt-out, LEIE, 2024 Part B billing, order-and-refer, and the non-physician pending list
with p as (select distinct trim(NPI) npi, upper(trim(LAST_NAME)) ln, upper(trim(FIRST_NAME)) fn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, max(ENTITY_TYPE_CODE) et, max(upper(PROVIDER_LAST_NAME_LEGAL_NAME)) ln, max(PROVIDER_ENUMERATION_DATE) enum_dt, max(NPI_DEACTIVATION_DATE) deact, max(NPI_REACTIVATION_DATE) react
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p) group by 1),
pe as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT where NPI in (select npi from p)),
oo as (select NPI, max(OPTOUT_EFFECTIVE_DATE) eff, max(OPTOUT_END_DATE) en from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS where NPI in (select npi from p) group by 1),
le as (select NPI, max(upper(LAST_NAME)) ln, max(EXCLUSION_DATE) ex, max(REINSTATEMENT_DATE) rs from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL and NPI in (select npi from p) group by 1),
mp as (select NPI, sum(TOT_MDCR_PYMT_AMT) pay from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER where NPI in (select npi from p) group by 1),
orf as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING where NPI in (select npi from p)),
np as (select distinct trim(NPI) NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS)
select count(*) rows_d, count(distinct p.npi) npi_d,
  sum(iff(regexp_like(p.npi,'^[12][0-9]{9}$'),1,0)) well_formed,
  sum(iff(p.ln is null or p.ln='',1,0)) blank_last,
  count(n.NPI) in_nppes, sum(iff(n.ln=p.ln,1,0)) nppes_last_agrees, sum(iff(n.et='1',1,0)) nppes_person,
  sum(iff(n.deact is not null and (n.react is null or n.react<n.deact),1,0)) npi_deactivated,
  min(n.enum_dt) enum_min, median(datediff(day,'1970-01-01',n.enum_dt)) enum_med_days, max(n.enum_dt) enum_max,
  sum(iff(n.enum_dt < '2020-01-01',1,0)) enum_pre2020, sum(iff(n.enum_dt >= '2025-01-01',1,0)) enum_2025plus,
  count(pe.NPI) in_pecos, count(oo.NPI) in_optout, sum(iff(oo.en >= '2026-01-01',1,0)) optout_active,
  count(le.NPI) in_leie, sum(iff(le.ln=p.ln,1,0)) leie_last_agrees,
  count(mp.NPI) billed_partb_2024, sum(mp.pay) partb_pay, count(orf.NPI) in_order_refer, count(np.NPI) also_nonphys_list
from p left join n on n.NPI=p.npi left join pe on pe.NPI=p.npi left join oo on oo.NPI=p.npi left join le on le.NPI=p.npi
left join mp on mp.NPI=p.npi left join orf on orf.NPI=p.npi left join np on np.NPI=p.npi
-- # Guttmacher: shape check (states, months, notes, constant columns)
select 'state' k, STATE v, count(*) n, min(MONTH) mn, max(MONTH) mx, sum(MEDIAN) s, count(distinct NOTES) nd
from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION group by 2
union all
select 'month', MONTH, count(*), min(STATE), max(STATE), sum(MEDIAN), count(distinct NOTES)
from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION group by 2
union all
select 'note', left(NOTES,300), count(*), min(STATE), max(STATE), sum(MEDIAN), count(distinct MONTH)
from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION group by 2
union all
select 'const', 'src='||count(distinct SOURCE)||' pub='||count(distinct PUBLISHDATE)||' lbnum='||count(try_to_double(LOWERBOUND))||' ubnum='||count(try_to_double(UPPERBOUND))||' mednull='||count_if(MEDIAN is null), count(*), min(PUBLISHDATE), max(PUBLISHDATE), sum(MEDIAN), count(distinct LOWERBOUND)
from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION
order by 1,2
