-- g07 deep pass 3, 2026-09-24. Read-only. 22 queries, run over 6 Python connections (connect/db.py).
-- Each connection first ran these two setup statements (12 setup statements total):
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Results for query #N are in g07/out_NN.txt.

-- #1 FAERS REAC per quarter: rows, IDs filled, distinct reports, distinct report+term pairs (duplicate check)
select SRC_QUARTER q, count(*) n,
  count(nullif(trim(ISR),'')) isr_nn, count(distinct nullif(trim(ISR),'')) isr_d,
  count(nullif(trim(PRIMARYID),'')) pid_nn, count(distinct nullif(trim(PRIMARYID),'')) pid_d,
  count(distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),''))||'|'||upper(trim(PT))) pair_d
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_REAC group by 1 order by 1;

-- #2 FAERS INDI and OUTC per quarter: same duplicate check
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
order by 1,2;

-- #3 FAERS the glance's top report IDs: where do 19K / 10K / 3.7K rows for one report come from
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
order by 1,2,3;

-- #4 Pending physicians: well-formed NPIs, and one pass of semi-joins to NPPES, PECOS, opt-out, LEIE, 2024 Part B billing, order-and-refer, and the non-physician pending list
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
left join mp on mp.NPI=p.npi left join orf on orf.NPI=p.npi left join np on np.NPI=p.npi;

-- #5 Guttmacher: shape check (states, months, notes, constant columns)
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
order by 1,2;

-- #6 Pending physicians: the 7 LEIE hits in full, deactivated-NPI breakdown, entity types, and the 310 who billed Part B in 2024 (moved state?)
with p as (select distinct trim(NPI) npi, upper(trim(LAST_NAME)) ln, upper(trim(FIRST_NAME)) fn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
le as (select NPI, LAST_NAME, FIRST_NAME, GENERAL_CATEGORY, SPECIALTY, EXCLUSION_TYPE, EXCLUSION_DATE, REINSTATEMENT_DATE, WAS_REINSTATED, CITY, STATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL and NPI in (select npi from p)),
n as (select NPI, NPI_DEACTIVATION_REASON_CODE rc, NPI_DEACTIVATION_DATE dd, NPI_REACTIVATION_DATE rd, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, PROVIDER_ENUMERATION_DATE ed, ENTITY_TYPE_CODE et, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tx from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p)),
mp as (select NPI, RNDRNG_PRVDR_STATE_ABRVTN st, RNDRNG_PRVDR_TYPE ty, TOT_MDCR_PYMT_AMT pay, TOT_BENES b from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER where NPI in (select npi from p))
select 'leie' k, le.NPI a, p.ln||', '||p.fn b, le.LAST_NAME||', '||le.FIRST_NAME c, le.EXCLUSION_TYPE||' | '||coalesce(le.GENERAL_CATEGORY,'')||' | '||coalesce(le.SPECIALTY,'') d, le.EXCLUSION_DATE::varchar e, coalesce(le.REINSTATEMENT_DATE,'')||' reinst='||coalesce(le.WAS_REINSTATED::varchar,'') f, coalesce(le.CITY,'')||' '||coalesce(le.STATE,'')||' / nppes '||coalesce(n.st,'')||' / enum '||coalesce(n.ed::varchar,'')||' / deact '||coalesce(n.dd::varchar,'') g
from le join p on p.npi=le.NPI left join n on n.NPI=le.NPI
union all select 'deact', coalesce(rc,'(blank)'), year(dd)::varchar, count(*)::varchar, sum(iff(rd is not null,1,0))::varchar, min(dd)::varchar, max(dd)::varchar, null from n where dd is not null group by 2,3
union all select 'etype', coalesce(et,'(null)'), null, count(*)::varchar, null, null, null, null from n group by 2
union all select 'mover', null, null, count(*)::varchar, sum(iff(mp.st<>n.st,1,0))::varchar, sum(iff(n.st is null,1,0))::varchar, median(pay)::varchar, sum(pay)::varchar from mp left join n on n.NPI=mp.NPI
union all select * from (select 'topbill', mp.NPI, p.ln||', '||p.fn, mp.ty, mp.st||'->'||coalesce(n.st,'?'), round(mp.pay)::varchar, mp.b::varchar, n.ed::varchar from mp join p on p.npi=mp.NPI left join n on n.NPI=mp.NPI order by mp.pay desc limit 12);

-- #7 Pending physicians per state vs the state's 2024 Part B physician count (peer rate per 1,000)
with p as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, max(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME) st from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p) group by 1),
pc as (select coalesce(st,'(none)') st, count(*) pend from p left join n on n.NPI=p.npi group by 1),
b as (select RNDRNG_PRVDR_STATE_ABRVTN st, count(*) docs from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER
      where RNDRNG_PRVDR_ENT_CD='I' and not regexp_like(upper(RNDRNG_PRVDR_TYPE), '.*(NURSE|ASSISTANT|THERAP|PSYCHOLOG|SOCIAL WORK|AUDIOLOG|SPEECH|DIETITIAN|NUTRITION|MIDWIFE|ANESTHETIST|COUNSELOR|MARRIAGE|IMMUNIZ|AMBULANCE|PHARMAC|LABORATORY|SUPPLIER|CENTER|AGENCY).*')
      group by 1)
select pc.st, pc.pend, b.docs, round(1000*pc.pend/nullif(b.docs,0),2) per1k,
  median(round(1000*pc.pend/nullif(b.docs,0),2)) over () med_per1k, sum(pc.pend) over () tot_pend, sum(b.docs) over () tot_docs
from pc left join b on b.st=pc.st order by per1k desc nulls last;

-- #8 Guttmacher: each state, same months across years (Q1 and Jul-Dec), per 100K residents (2020 census)
with g as (select STATE st, to_date(MONTH) m, MEDIAN v from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION),
pop as (select s.STATE_USPS st, sum(c.POPULATION_2020) pop from LIBRARY_MARTS.CORE.DIM_COUNTY c join LIBRARY_MARTS.CORE.DIM_STATE s on try_to_number(s.STATE_FIPS::varchar)=try_to_number(c.STATE_FIPS::varchar) group by 1)
select g.st, pop.pop, count(*) months,
 round(avg(iff(m between '2023-01-01' and '2023-03-31',v,null))) q1_23,
 round(avg(iff(m between '2024-01-01' and '2024-03-31',v,null))) q1_24,
 round(avg(iff(m between '2025-01-01' and '2025-03-31',v,null))) q1_25,
 round(avg(iff(m between '2026-01-01' and '2026-03-31',v,null))) q1_26,
 round(avg(iff(m between '2023-07-01' and '2023-12-31',v,null))) h2_23,
 round(avg(iff(m between '2024-07-01' and '2024-12-31',v,null))) h2_24,
 round(avg(iff(m between '2025-07-01' and '2025-12-31',v,null))) h2_25,
 round(100000*avg(iff(m between '2026-01-01' and '2026-03-31',v,null))/pop.pop,1) q1_26_per100k,
 round(100000*avg(iff(m between '2024-01-01' and '2024-03-31',v,null))/pop.pop,1) q1_24_per100k
from g left join pop on pop.st=g.st group by 1,2 order by 1;

-- #9 Guttmacher: month by month, do states add to US; ban-state aggregate vs the 11 late-added states; FL, TX, IL, IN, MO, ND
with g as (select STATE st, to_date(MONTH) m, MEDIAN v from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION)
select m, max(iff(st='US',v,null)) us,
 sum(iff(st not in ('US','States with total bans','States without total bans'),v,0)) states_sum,
 max(iff(st='States with total bans',v,null)) ban_agg, max(iff(st='States without total bans',v,null)) noban_agg,
 sum(iff(st in ('AL','AR','ID','KY','LA','MS','OK','SD','TN','TX','WV'),v,0)) late11_sum,
 max(iff(st='TX',v,null)) tx, max(iff(st='FL',v,null)) fl, max(iff(st='IL',v,null)) il,
 max(iff(st='IN',v,null)) in_, max(iff(st='MO',v,null)) mo, max(iff(st='ND',v,null)) nd, max(iff(st='IA',v,null)) ia, max(iff(st='GA',v,null)) ga, max(iff(st='SC',v,null)) sc, max(iff(st='NC',v,null)) nc
from g group by 1 order by 1;

-- #10 FAERS REAC: side-effect terms whose NEW cases in one quarter ran 3x+ their own prior-4-quarter average (case-level, first quarter a case shows the term)
with d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
r as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, upper(trim(PT)) pt from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_REAC),
rd as (select r.pt, r.id, d.cs, d.q from r left join d on d.id=r.id),
f as (select cs, pt, min(q) q from rd where cs is not null group by 1,2),
pq as (select pt, q, (left(q,4)::int-2004)*4+right(q,1)::int qi, count(*) n from f group by 1,2),
tot as (select q, sum(n) tn from pq group by 1),
sp as (select a.pt, a.q, a.qi, a.n, coalesce(sum(b.n),0)/4 base from pq a left join pq b on b.pt=a.pt and b.qi between a.qi-4 and a.qi-1 group by 1,2,3,4)
select '__land' pt, null q, count(*) n, count(cs) base, count(distinct id) ratio, count(distinct iff(cs is null,id,null)) tn from rd
union all
select * from (select sp.pt, sp.q, sp.n, round(sp.base,1), round(sp.n/nullif(sp.base,0),1), tot.tn from sp join tot on tot.q=sp.q
 where sp.qi>=5 and sp.n>=300 and sp.n >= 3*sp.base order by sp.n - sp.base desc limit 40);

-- #11 FAERS OUTC deaths: primary-suspect drugs whose new death cases jumped most vs their own prior 2 years; lawyer-filed share
with o as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC where upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
d0 as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, left(SRC_QUARTER,4) yr, upper(trim(OCCP_COD)) occ from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
d as (select * from d0 where id in (select id from o)),
dr0 as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, upper(trim(DRUGNAME)) drug from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD))='PS'),
dr as (select distinct id, drug from dr0 where id in (select id from o)),
c as (select d.cs, dr.drug, min(d.yr) yr, max(iff(d.occ='LW',1,0)) lw, max(iff(d.occ='CN',1,0)) cn from o join d on d.id=o.id join dr on dr.id=o.id group by 1,2),
dy as (select drug, yr, count(*) n, sum(lw) lw, sum(cn) cn from c group by 1,2),
j as (select a.drug, a.yr, a.n, a.lw, a.cn, avg(b.n) prev2 from dy a left join dy b on b.drug=a.drug and b.yr::int between a.yr::int-2 and a.yr::int-1 group by 1,2,3,4,5)
select '__tot' drug, null yr, (select count(*) from o) n, (select count(distinct cs) from c) lw, (select count(*) from d) cn, null prev2
union all
select * from (select drug, yr, n, lw, cn, round(prev2,1) from j where yr between '2005' and '2013' and n>=100 order by n - coalesce(prev2,0) desc limit 30);

-- #12 Pending physicians by state: is Florida's excess new doctors or established Medicare billers? (2024 billers, old vs new NPIs, already in PECOS)
with p as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, max(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME) st, max(PROVIDER_ENUMERATION_DATE) ed from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p) group by 1),
mp as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER where NPI in (select npi from p)),
pe as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT where NPI in (select npi from p)),
orf as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING where NPI in (select npi from p))
select coalesce(n.st,'(none)') st, count(*) pend, count(mp.NPI) billed24, sum(iff(n.ed<'2016-01-01',1,0)) npi_pre2016, sum(iff(n.ed>='2025-01-01',1,0)) npi_2025plus,
  count(pe.NPI) in_pecos, count(orf.NPI) in_orderrefer, round(avg(year(n.ed)),1) avg_enum_year
from p left join n on n.NPI=p.npi left join mp on mp.NPI=p.npi left join pe on pe.NPI=p.npi left join orf on orf.NPI=p.npi
group by 1 having count(*)>=40 order by pend desc;

-- #13 Guttmacher: quarterly middle estimate with Guttmacher's own low-high range, ban states and Texas-border states
with g as (select STATE st, to_date(MONTH) m, MEDIAN v, try_to_double(LOWERBOUND) lo, try_to_double(UPPERBOUND) hi from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION
  where STATE in ('LA','MS','TX','AL','FL','NM','KS','CO','States with total bans'))
select st, year(m)||'q'||quarter(m) q, count(*) months, round(avg(v)) med, round(avg(lo)) lo, round(avg(hi)) hi
from g group by 1,2 order by 1,2;

-- #14 FAERS REAC spike drill: in each spike quarter, which primary-suspect drugs, and how many cases came from lawyers (LW) or consumers (CN) vs the prior 4 quarters
with sp as (select column1 pt, column2 q from values ('MYOCARDIAL INFARCTION','2014q2'),('CEREBROVASCULAR ACCIDENT','2014q2'),('TYPE 2 DIABETES MELLITUS','2014q1'),('TARDIVE DYSKINESIA','2011q3'),('DEVICE EXPULSION','2011q3'),('BREAST CANCER FEMALE','2010q2'),('ABNORMAL DREAMS','2010q3'),('NAUSEA','2010q3'),('COMPLETED SUICIDE','2013q1'),('COMPLETED SUICIDE','2014q1'),('DRUG ABUSE','2013q1'),('PRODUCT QUALITY ISSUE','2008q4'),('INCORRECT DOSE ADMINISTERED','2009q3'),('CARDIOVASCULAR DISORDER','2005q4'),('INADEQUATE ANALGESIA','2013q4'),('GASTROINTESTINAL HAEMORRHAGE','2014q1'),('INJECTION SITE PAIN','2007q4'),('LOCAL SWELLING','2013q1')),
d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, (left(SRC_QUARTER,4)::int-2004)*4+right(SRC_QUARTER,1)::int qi, upper(trim(OCCP_COD)) occ from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
r as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, upper(trim(PT)) pt from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_REAC where upper(trim(PT)) in (select pt from sp)),
x as (select r.pt, sp.q spq, d.q, d.qi, (left(sp.q,4)::int-2004)*4+right(sp.q,1)::int sqi, d.cs, d.id, d.occ from r join d on d.id=r.id join sp on sp.pt=r.pt),
xs as (select * from x where qi=sqi),
dr as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, upper(trim(DRUGNAME)) drug from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD))='PS' and coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from xs)),
ag as (select xs.pt, xs.spq, dr.drug, count(distinct xs.cs) n, count(distinct iff(xs.occ='LW',xs.cs,null)) lw, count(distinct iff(xs.occ='CN',xs.cs,null)) cn from xs join dr on dr.id=xs.id group by 1,2,3),
rk as (select *, row_number() over (partition by pt, spq order by n desc) k from ag)
select 'pair' t, pt, spq, null drug,
  count(distinct iff(qi=sqi,cs,null)) n, count(distinct iff(qi=sqi and occ='LW',cs,null)) lw, count(distinct iff(qi=sqi and occ='CN',cs,null)) cn,
  count(distinct iff(qi between sqi-4 and sqi-1,cs,null)) prior4_n, count(distinct iff(qi between sqi-4 and sqi-1 and occ='LW',cs,null)) prior4_lw
from x group by 1,2,3,4
union all
select 'drug', pt, spq, drug, n, lw, cn, k, null from rk where k<=3
order by 2,3,1 desc,8;

-- #15 FAERS OUTC deaths drill: the 2012 oncology spike. Per drug and quarter: new death cases, sender, event-to-FDA lag, report type
with o as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC where upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
d0 as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(MFR_SNDR)) snd, EVENT_DT evt,
   coalesce(try_to_date(FDA_DT,'YYYYMMDD'), INIT_FDA_DT) fda, upper(trim(REPT_COD)) rept, upper(trim(OCCP_COD)) occ, upper(trim(coalesce(REPORTER_COUNTRY, OCCR_COUNTRY))) ctry from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
d as (select * from d0 where id in (select id from o)),
dr0 as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, upper(trim(DRUGNAME)) drug from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD))='PS'
   and upper(trim(DRUGNAME)) in ('TARCEVA','AVASTIN','XELODA','GLIVEC','GLEEVEC','ERLOTINIB TABLET','TRACLEER','HERCEPTIN','RITUXAN','PERJETA','ZELBORAF')),
dr as (select distinct id, drug from dr0 where id in (select id from o)),
c as (select dr.drug, d.cs, min(d.q) q, max(d.snd) snd, min(d.evt) evt, min(d.fda) fda, max(d.rept) rept, max(d.occ) occ, max(d.ctry) ctry from d join dr on dr.id=d.id group by 1,2)
select drug, q, count(*) new_death_cases, mode(snd) top_sender, count_if(snd like '%GENENTECH%' or snd like '%ROCHE%') roche_genentech, count_if(snd like '%NOVARTIS%') novartis, count_if(snd like '%ACTELION%') actelion,
  median(datediff(day, evt, fda)) med_lag_days, count_if(datediff(day,evt,fda) > 365) lag_over_1yr, count(evt) has_event_dt, mode(rept) top_rept, mode(occ) top_occ, mode(ctry) top_country
from c where q between '2010q1' and '2014q2' group by 1,2 order by 1,2;

-- #16 Pending physicians, Florida: do a few addresses or cities carry the established-doctor excess? NPPES last-update year FL vs rest
with p as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, upper(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME) city,
   upper(PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS)||' '||left(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE,5) addr,
   PROVIDER_ENUMERATION_DATE ed, LAST_UPDATE_DATE lu, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tx
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p))
select * from (select 'city' k, city v, count(*) n, count_if(ed<'2016-01-01') old_npi, null x from n where st='FL' group by 2 order by 3 desc limit 10)
union all select * from (select 'addr', addr, count(*), count_if(ed<'2016-01-01'), null from n where st='FL' group by 2 order by 3 desc limit 8)
union all select * from (select 'addr_all', st||' '||addr, count(*), count_if(ed<'2016-01-01'), null from n group by 2 order by 3 desc limit 8)
union all select 'upd_year', iff(st='FL','FL',iff(st='PR','PR','rest'))||' '||year(lu), count(*), count_if(ed<'2016-01-01'), null from n where lu is not null group by 2
union all select * from (select 'tax_FL_old', tx, count(*), null, null from n where st='FL' and ed<'2016-01-01' group by 2 order by 3 desc limit 8);

-- #17 FAERS: the 2014q2 Avandia heart-attack/stroke wave and the 2014q1 Lipitor diabetes wave. Who sent them, event years, lag, deaths
with d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(MFR_SNDR)) snd, EVENT_DT evt,
   coalesce(try_to_date(FDA_DT,'YYYYMMDD'), INIT_FDA_DT) fda, upper(trim(REPT_COD)) rept, upper(trim(OCCP_COD)) occ from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO where SRC_QUARTER between '2012q4' and '2014q2'),
dr as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, iff(upper(DRUGNAME) like 'AVANDIA%' or upper(DRUGNAME) like 'ROSIGLITAZONE%','AVANDIA','LIPITOR') g
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where SRC_QUARTER between '2012q4' and '2014q2' and upper(trim(ROLE_COD))='PS' and (upper(DRUGNAME) like 'AVANDIA%' or upper(DRUGNAME) like 'ROSIGLITAZONE%' or upper(DRUGNAME) like 'LIPITOR%' or upper(DRUGNAME) like 'ATORVASTATIN%')),
r as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, upper(trim(PT)) pt from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_REAC where SRC_QUARTER between '2012q4' and '2014q2'
   and upper(trim(PT)) in ('MYOCARDIAL INFARCTION','CEREBROVASCULAR ACCIDENT','TYPE 2 DIABETES MELLITUS')),
de as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC where SRC_QUARTER between '2012q4' and '2014q2' and upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
c as (select dr.g, d.q, d.cs, max(d.snd) snd, max(d.rept) rept, max(d.occ) occ, min(d.evt) evt, min(d.fda) fda, max(iff(de.id is not null,1,0)) died
   from d join dr on dr.id=d.id join r on r.id=d.id and ((dr.g='AVANDIA' and r.pt<>'TYPE 2 DIABETES MELLITUS') or (dr.g='LIPITOR' and r.pt='TYPE 2 DIABETES MELLITUS')) left join de on de.id=d.id group by 1,2,3)
select g, q, count(*) cases, mode(snd) top_sender, count_if(snd like '%GLAXO%' or snd like '%GSK%') gsk_sent, count_if(snd like '%PFIZER%') pfizer_sent, mode(occ) top_occ, mode(rept) top_rept,
  count(evt) has_evt, count_if(year(evt)<2008) evt_pre2008, count_if(year(evt) between 2008 and 2010) evt_2008_10, count_if(year(evt)>=2011) evt_2011plus, median(datediff(day,evt,fda)) med_lag_days, sum(died) died
from c group by 1,2 order by 1,2;

-- #18 FAERS INDI: fentanyl mouth/nose sprays for cancer pain only (TIRF class). Why were they taken, by brand and year? Subsys (Insys) vs peers
with t as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, trim(DRUG_SEQ) seq,
   case when upper(DRUGNAME) like 'SUBSYS%' then 'SUBSYS' when upper(DRUGNAME) like 'FENTORA%' then 'FENTORA' when upper(DRUGNAME) like 'ACTIQ%' then 'ACTIQ'
        when upper(DRUGNAME) like 'ABSTRAL%' then 'ABSTRAL' when upper(DRUGNAME) like 'ONSOLIS%' then 'ONSOLIS' when upper(DRUGNAME) like 'LAZANDA%' then 'LAZANDA' end brand
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD)) in ('PS','SS')
   and (upper(DRUGNAME) like 'SUBSYS%' or upper(DRUGNAME) like 'FENTORA%' or upper(DRUGNAME) like 'ACTIQ%' or upper(DRUGNAME) like 'ABSTRAL%' or upper(DRUGNAME) like 'ONSOLIS%' or upper(DRUGNAME) like 'LAZANDA%')),
d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(MFR_SNDR)) snd from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
i as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(DRUG_SEQ),''),trim(INDI_DRUG_SEQ)) seq, upper(trim(INDI_PT)) ip from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI
   where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
ic as (select *, case when ip is null or ip like '%UNKNOWN%' then 'unknown'
     when regexp_like(ip,'.*(CANCER|CARCINOMA|NEOPLASM|TUMOU?R|LYMPHOMA|LEUK|MYELOMA|METASTA|MALIGNAN|SARCOMA|MELANOMA|BLASTOMA|MESOTHELIOMA|ONCO).*') then 'cancer'
     when ip in ('PAIN','BREAKTHROUGH PAIN','ANALGESIC THERAPY','PAIN MANAGEMENT','ANALGESIA','DRUG USE FOR UNKNOWN INDICATION') then 'generic_pain'
     else 'named_noncancer' end cls from i),
j as (select t.brand, d.cs, min(left(d.q,4)) yr, max(d.snd) snd, max(iff(ic.cls='cancer',1,0)) ca, max(iff(ic.cls='named_noncancer',1,0)) nc, max(iff(ic.cls='generic_pain',1,0)) gp, max(iff(ic.cls='unknown',1,0)) uk, count(ic.ip) nind
   from t join d on d.id=t.id left join ic on ic.id=t.id and ic.seq=t.seq group by 1,2)
select 'yr' k, brand, yr v, count(*) cases, count_if(nind>0) with_ind, sum(ca) cancer, sum(nc) named_noncancer, sum(gp) generic_pain, sum(uk) unknown from j group by 2,3
union all select 'all', brand, mode(snd), count(*), count_if(nind>0), sum(ca), sum(nc), sum(gp), sum(uk) from j group by 2
union all select * from (select 'top', t.brand, ic.ip, count(distinct d.cs), null, null, null, null, null from t join d on d.id=t.id join ic on ic.id=t.id and ic.seq=t.seq
   where t.brand in ('SUBSYS','FENTORA','ACTIQ') group by 2,3 qualify row_number() over (partition by t.brand order by count(distinct d.cs) desc) <= 10)
order by 1,2,3;

-- #19 FAERS late-filing test: days from company awareness (MFR_DT) to FDA receipt (FDA_DT), spike quarters vs normal quarters, same drugs. Expedited reports are due in 15 days
with d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q,
   MFR_DT mfr, coalesce(try_to_date(FDA_DT,'YYYYMMDD'), INIT_FDA_DT) fda, upper(trim(REPT_COD)) rept from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO
   where SRC_QUARTER in ('2010q2','2010q4','2011q2','2011q3','2012q1','2012q4','2013q3','2014q2')),
dr as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id,
   case when upper(DRUGNAME) like 'AVANDIA%' then 'AVANDIA' when upper(DRUGNAME) in ('TARCEVA','ERLOTINIB TABLET') then 'TARCEVA' else upper(trim(DRUGNAME)) end drug
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where SRC_QUARTER in ('2010q2','2010q4','2011q2','2011q3','2012q1','2012q4','2013q3','2014q2') and upper(trim(ROLE_COD))='PS'
   and (upper(DRUGNAME) like 'AVANDIA%' or upper(trim(DRUGNAME)) in ('TARCEVA','ERLOTINIB TABLET','AVASTIN','HERCEPTIN','RITUXAN','XELODA','TRACLEER','GLIVEC','GLEEVEC'))),
de as (select distinct coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC where upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
c as (select dr.drug, d.q, d.cs, min(d.mfr) mfr, min(d.fda) fda, max(iff(de.id is not null,1,0)) died from d join dr on dr.id=d.id left join de on de.id=d.id group by 1,2,3)
select drug, q, count(*) cases, sum(died) death_cases, count(mfr) has_mfr_dt, median(datediff(day,mfr,fda)) med_days_mfr_to_fda,
  count_if(datediff(day,mfr,fda)>15) over_15d, count_if(datediff(day,mfr,fda)>365) over_1yr, min(mfr) earliest_mfr, max(fda) latest_fda
from c group by 1,2 order by 1,2;

-- #20 FAERS INDI trap check: across the 2012q4 format switch, how is 'unknown reason' spelled, and what share of lines is it
select SRC_QUARTER q, count(*) n,
  count_if(upper(INDI_PT) like '%UNKNOWN%') unknown_any, count_if(INDI_PT like '%UNKNOWN%') unknown_upper, count_if(INDI_PT like '%nknown%') unknown_mixed,
  count(distinct INDI_PT) dist_raw, count(distinct upper(INDI_PT)) dist_upper, count(nullif(trim(DRUG_SEQ),'')) has_drug_seq, count(nullif(trim(INDI_DRUG_SEQ),'')) has_indi_drug_seq
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI where SRC_QUARTER between '2011q3' and '2014q2' group by 1 order by 1;

-- #21 FAERS INDI robustness: Actiq + Fentora reasons split by who reported (health professional vs consumer vs lawyer) and by period (pre-REMS legacy, post-REMS legacy, post-REMS new format)
with t as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, trim(DRUG_SEQ) seq
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD)) in ('PS','SS') and (upper(DRUGNAME) like 'ACTIQ%' or upper(DRUGNAME) like 'FENTORA%')),
d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(OCCP_COD)) occ
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
i as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(DRUG_SEQ),''),trim(INDI_DRUG_SEQ)) seq, upper(trim(INDI_PT)) ip from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI
   where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
ic as (select *, case when ip is null or ip like '%UNKNOWN%' then 'unknown'
     when regexp_like(ip,'.*(CANCER|CARCINOMA|NEOPLASM|TUMOU?R|LYMPHOMA|LEUK|MYELOMA|METASTA|MALIGNAN|SARCOMA|MELANOMA|BLASTOMA|MESOTHELIOMA|ONCO).*') then 'cancer'
     when ip in ('PAIN','BREAKTHROUGH PAIN','ANALGESIC THERAPY','PAIN MANAGEMENT','ANALGESIA') then 'generic_pain'
     else 'named_noncancer' end cls from i),
j as (select d.cs, min(d.q) q, max(d.occ) occ, max(iff(ic.cls='cancer',1,0)) ca, max(iff(ic.cls='named_noncancer',1,0)) nc, max(iff(ic.cls='generic_pain',1,0)) gp
   from t join d on d.id=t.id join ic on ic.id=t.id and ic.seq=t.seq group by 1)
select case when q<='2011q4' then '1 2004-2011 pre-REMS' when q<='2012q3' then '2 2012q1-q3 REMS legacy' else '3 2012q4-2014q2 new format' end period,
  case when occ in ('MD','PH','OT','HP') then 'health pro' when occ='CN' then 'consumer' when occ='LW' then 'lawyer' else coalesce(occ,'blank') end who,
  count(*) cases_with_reason, sum(ca) cancer, sum(nc) named_noncancer, sum(gp) generic_pain, round(100*sum(nc)/count(*)) pct_noncancer
from j group by 1,2 order by 1,2;

-- #22 Pending physicians eyeball: 5 organization NPIs on the physician list, and 6 Florida rows with pre-2016 NPIs and NPPES untouched since before 2017
with p as (select distinct trim(NPI) npi, LAST_NAME ln, FIRST_NAME fn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, ENTITY_TYPE_CODE et, PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME org, PROVIDER_LAST_NAME_LEGAL_NAME nl, PROVIDER_FIRST_NAME nf, PROVIDER_CREDENTIAL_TEXT cred,
   PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, upper(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME) city, PROVIDER_ENUMERATION_DATE ed, LAST_UPDATE_DATE lu, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tx
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p))
select * from (select 'org' k, p.npi, p.ln||', '||p.fn pending_name, coalesce(n.org,'')||' / '||coalesce(n.nl,'') nppes_name, n.st||' '||n.city place, n.ed::varchar enum_dt, n.lu::varchar last_upd, n.tx from p join n on n.NPI=p.npi where n.et='2' order by p.npi limit 5)
union all
select * from (select 'fl_stale', p.npi, p.ln||', '||p.fn, coalesce(n.nl,'')||', '||coalesce(n.nf,'')||' '||coalesce(n.cred,''), n.st||' '||n.city, n.ed::varchar, n.lu::varchar, n.tx from p join n on n.NPI=p.npi
  where n.st='FL' and n.ed<'2016-01-01' and n.lu<'2017-01-01' order by hash(p.npi) limit 6);

