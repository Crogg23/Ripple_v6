-- # Pending physicians by state: is Florida's excess new doctors or established Medicare billers? (2024 billers, old vs new NPIs, already in PECOS)
with p as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, max(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME) st, max(PROVIDER_ENUMERATION_DATE) ed from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p) group by 1),
mp as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER where NPI in (select npi from p)),
pe as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT where NPI in (select npi from p)),
orf as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING where NPI in (select npi from p))
select coalesce(n.st,'(none)') st, count(*) pend, count(mp.NPI) billed24, sum(iff(n.ed<'2016-01-01',1,0)) npi_pre2016, sum(iff(n.ed>='2025-01-01',1,0)) npi_2025plus,
  count(pe.NPI) in_pecos, count(orf.NPI) in_orderrefer, round(avg(year(n.ed)),1) avg_enum_year
from p left join n on n.NPI=p.npi left join mp on mp.NPI=p.npi left join pe on pe.NPI=p.npi left join orf on orf.NPI=p.npi
group by 1 having count(*)>=40 order by pend desc
-- # Guttmacher: quarterly middle estimate with Guttmacher's own low-high range, ban states and Texas-border states
with g as (select STATE st, to_date(MONTH) m, MEDIAN v, try_to_double(LOWERBOUND) lo, try_to_double(UPPERBOUND) hi from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION
  where STATE in ('LA','MS','TX','AL','FL','NM','KS','CO','States with total bans'))
select st, year(m)||'q'||quarter(m) q, count(*) months, round(avg(v)) med, round(avg(lo)) lo, round(avg(hi)) hi
from g group by 1,2 order by 1,2
-- # FAERS REAC spike drill: in each spike quarter, which primary-suspect drugs, and how many cases came from lawyers (LW) or consumers (CN) vs the prior 4 quarters
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
order by 2,3,1 desc,8
-- # FAERS OUTC deaths drill: the 2012 oncology spike. Per drug and quarter: new death cases, sender, event-to-FDA lag, report type
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
from c where q between '2010q1' and '2014q2' group by 1,2 order by 1,2
