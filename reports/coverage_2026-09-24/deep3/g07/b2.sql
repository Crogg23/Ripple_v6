-- # Pending physicians: the 7 LEIE hits in full, deactivated-NPI breakdown, entity types, and the 310 who billed Part B in 2024 (moved state?)
with p as (select distinct trim(NPI) npi, upper(trim(LAST_NAME)) ln, upper(trim(FIRST_NAME)) fn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
le as (select NPI, LAST_NAME, FIRST_NAME, GENERAL_CATEGORY, SPECIALTY, EXCLUSION_TYPE, EXCLUSION_DATE, REINSTATEMENT_DATE, WAS_REINSTATED, CITY, STATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL and NPI in (select npi from p)),
n as (select NPI, NPI_DEACTIVATION_REASON_CODE rc, NPI_DEACTIVATION_DATE dd, NPI_REACTIVATION_DATE rd, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, PROVIDER_ENUMERATION_DATE ed, ENTITY_TYPE_CODE et, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tx from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p)),
mp as (select NPI, RNDRNG_PRVDR_STATE_ABRVTN st, RNDRNG_PRVDR_TYPE ty, TOT_MDCR_PYMT_AMT pay, TOT_BENES b from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER where NPI in (select npi from p))
select 'leie' k, le.NPI a, p.ln||', '||p.fn b, le.LAST_NAME||', '||le.FIRST_NAME c, le.EXCLUSION_TYPE||' | '||coalesce(le.GENERAL_CATEGORY,'')||' | '||coalesce(le.SPECIALTY,'') d, le.EXCLUSION_DATE::varchar e, coalesce(le.REINSTATEMENT_DATE,'')||' reinst='||coalesce(le.WAS_REINSTATED::varchar,'') f, coalesce(le.CITY,'')||' '||coalesce(le.STATE,'')||' / nppes '||coalesce(n.st,'')||' / enum '||coalesce(n.ed::varchar,'')||' / deact '||coalesce(n.dd::varchar,'') g
from le join p on p.npi=le.NPI left join n on n.NPI=le.NPI
union all select 'deact', coalesce(rc,'(blank)'), year(dd)::varchar, count(*)::varchar, sum(iff(rd is not null,1,0))::varchar, min(dd)::varchar, max(dd)::varchar, null from n where dd is not null group by 2,3
union all select 'etype', coalesce(et,'(null)'), null, count(*)::varchar, null, null, null, null from n group by 2
union all select 'mover', null, null, count(*)::varchar, sum(iff(mp.st<>n.st,1,0))::varchar, sum(iff(n.st is null,1,0))::varchar, median(pay)::varchar, sum(pay)::varchar from mp left join n on n.NPI=mp.NPI
union all select * from (select 'topbill', mp.NPI, p.ln||', '||p.fn, mp.ty, mp.st||'->'||coalesce(n.st,'?'), round(mp.pay)::varchar, mp.b::varchar, n.ed::varchar from mp join p on p.npi=mp.NPI left join n on n.NPI=mp.NPI order by mp.pay desc limit 12)
-- # Pending physicians per state vs the state's 2024 Part B physician count (peer rate per 1,000)
with p as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
n as (select NPI, max(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME) st from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES where NPI in (select npi from p) group by 1),
pc as (select coalesce(st,'(none)') st, count(*) pend from p left join n on n.NPI=p.npi group by 1),
b as (select RNDRNG_PRVDR_STATE_ABRVTN st, count(*) docs from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PROVIDER
      where RNDRNG_PRVDR_ENT_CD='I' and not regexp_like(upper(RNDRNG_PRVDR_TYPE), '.*(NURSE|ASSISTANT|THERAP|PSYCHOLOG|SOCIAL WORK|AUDIOLOG|SPEECH|DIETITIAN|NUTRITION|MIDWIFE|ANESTHETIST|COUNSELOR|MARRIAGE|IMMUNIZ|AMBULANCE|PHARMAC|LABORATORY|SUPPLIER|CENTER|AGENCY).*')
      group by 1)
select pc.st, pc.pend, b.docs, round(1000*pc.pend/nullif(b.docs,0),2) per1k,
  median(round(1000*pc.pend/nullif(b.docs,0),2)) over () med_per1k, sum(pc.pend) over () tot_pend, sum(b.docs) over () tot_docs
from pc left join b on b.st=pc.st order by per1k desc nulls last
-- # Guttmacher: each state, same months across years (Q1 and Jul-Dec), per 100K residents (2020 census)
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
from g left join pop on pop.st=g.st group by 1,2 order by 1
-- # Guttmacher: month by month, do states add to US; ban-state aggregate vs the 11 late-added states; FL, TX, IL, IN, MO, ND
with g as (select STATE st, to_date(MONTH) m, MEDIAN v from LIBRARY_MARTS.HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION)
select m, max(iff(st='US',v,null)) us,
 sum(iff(st not in ('US','States with total bans','States without total bans'),v,0)) states_sum,
 max(iff(st='States with total bans',v,null)) ban_agg, max(iff(st='States without total bans',v,null)) noban_agg,
 sum(iff(st in ('AL','AR','ID','KY','LA','MS','OK','SD','TN','TX','WV'),v,0)) late11_sum,
 max(iff(st='TX',v,null)) tx, max(iff(st='FL',v,null)) fl, max(iff(st='IL',v,null)) il,
 max(iff(st='IN',v,null)) in_, max(iff(st='MO',v,null)) mo, max(iff(st='ND',v,null)) nd, max(iff(st='IA',v,null)) ia, max(iff(st='GA',v,null)) ga, max(iff(st='SC',v,null)) sc, max(iff(st='NC',v,null)) nc
from g group by 1 order by 1
-- # FAERS REAC: side-effect terms whose NEW cases in one quarter ran 3x+ their own prior-4-quarter average (case-level, first quarter a case shows the term)
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
 where sp.qi>=5 and sp.n>=300 and sp.n >= 3*sp.base order by sp.n - sp.base desc limit 40)
-- # FAERS OUTC deaths: primary-suspect drugs whose new death cases jumped most vs their own prior 2 years; lawyer-filed share
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
select * from (select drug, yr, n, lw, cn, round(prev2,1) from j where yr between '2005' and '2013' and n>=100 order by n - coalesce(prev2,0) desc limit 30)
