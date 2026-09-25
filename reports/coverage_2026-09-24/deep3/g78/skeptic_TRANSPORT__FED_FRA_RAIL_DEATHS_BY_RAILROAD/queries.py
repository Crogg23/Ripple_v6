CAS = "LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES"
RB = "LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD"
TR = "FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%'"
Q = {}

# s1: re-derive headline from the roll-up; every UP-looking code; UP by year; gross ups vs downs
Q["s1"] = f"""
with t as (select * from {RB} where TYPE_OF_PERSON='Trespassers'),
r as (select RAILROAD_CODE code, sum(iff(INCIDENT_YEAR between 2015 and 2017,DEATHS,0))/3 a, sum(iff(INCIDENT_YEAR between 2023 and 2025,DEATHS,0))/3 b from t group by 1)
select 'nat' k, null code, null nm, null parent, round(sum(a),2) a, round(sum(b),2) b, count(*) n from r
union all select 'gross_up', null, null, null, round(sum(iff(b>a,b-a,0)),2), round(sum(iff(b<a,b-a,0)),2), count_if(b>a) from r
union all select 'up_like', RAILROAD_CODE, max(RAILROAD_NAME), max(PARENT_RAILROAD_CODE),
   round(sum(iff(INCIDENT_YEAR between 2015 and 2017,DEATHS,0))/3,2), round(sum(iff(INCIDENT_YEAR between 2023 and 2025,DEATHS,0))/3,2), count(*)
   from t where RAILROAD_NAME ilike '%union pac%' or PARENT_RAILROAD_CODE ilike 'UP%' or RAILROAD_CODE ilike 'UP%' group by RAILROAD_CODE
union all select 'up_yr', INCIDENT_YEAR::varchar, null, null, sum(DEATHS), null, count(*) from t where RAILROAD_CODE='UP' and INCIDENT_YEAR between 2012 and 2026 group by INCIDENT_YEAR
order by 1, 2"""

# s2: duplicates. Same person twice (same date+state+county+age), across railroads or inside UP; incident key repeats; report key repeats
Q["s2"] = f"""
with f as (select RAILROAD_CODE rr, DATE d, STATE_CODE s, COUNTY_CODE c, AGE_OF_PERSON age, INCIDENT_KEY ik, REPORT_KEY rk,
             iff(INCIDENT_YEAR<=2017,'A_2015_17','B_2023_25') p
           from {CAS} where {TR} and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025)),
g as (select p, d, s, c, age, count(*) n, count(distinct rr) nrr, count_if(rr='UP') nup, listagg(distinct rr, '+') within group (order by rr) rrs from f group by 1,2,3,4,5),
ik as (select p, ik, count(*) n, count(distinct rr) nrr, count_if(rr='UP') nup from f group by 1,2)
select 'person_key' k, p, count(*) grp, sum(n) rws, count_if(n>1) multi_grp, count_if(nrr>1) cross_rr_grp, count_if(nrr>1 and nup>0) cross_up_grp, count_if(nup>1) up_multi_grp, sum(iff(nup>1,nup-1,0)) up_excess, null rrs from g group by p
union all select 'incident_key', p, count(*), sum(n), count_if(n>1), count_if(nrr>1), count_if(nrr>1 and nup>0), count_if(nup>1), sum(iff(nup>1,nup-1,0)), null from ik group by p
union all select 'pair', p, count(*), null, null, null, null, null, null, rrs from g where nrr>1 and nup>0 group by p, rrs
union all select 'rk_dupe', p, count(*) - count(distinct rk), count_if(rk is null), count_if(d is null), count_if(c is null), count_if(age is null), null, null, null from f group by p
order by 1, 2"""

# s3: can the public file see suicides at all? covered-data and occurrence values on the whole file; fatal flag values; UP event mix; suicide words in non-blank narratives
Q["s3"] = f"""
select 'cov' k, COVERED_DATA_CODE a, COVERED_DATA_REASON b, count(*) n, count_if(FATALITY='Yes') m from {CAS} group by 2,3
union all select 'occ', CASUALTY_OCCURRENCE_CODE, null, count(*), count_if(FATALITY='Yes') from {CAS} group by 2
union all select 'fatality_vals', FATALITY, null, count(*), null from {CAS} group by 2
union all select 'up_event', EVENT, iff(INCIDENT_YEAR<=2017,'A','B'), count(*), null from {CAS}
   where {TR} and RAILROAD_CODE='UP' and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025) group by 2,3
union all select 'narr_suicide_word', iff(RAILROAD_CODE in ('UP','BNSF','CSX','NS','ATK'), RAILROAD_CODE, 'other'), null,
   count_if(NARRATIVE is not null), count_if(upper(NARRATIVE) like any ('%SUICID%','%INTENTIONAL%','%JUMPED IN FRONT%'))
   from {CAS} where FATALITY='Yes' and INCIDENT_YEAR between 2008 and 2025 group by 2
order by 1, 2, 3"""

# s4: same-county difference-in-differences. UP counties = counties where UP had a trespasser death in 2010-2014, picked before both windows
Q["s4"] = f"""
with f as (select RAILROAD_CODE rr, STATE_NAME st, STATE_CODE||'-'||COUNTY_CODE cty, INCIDENT_YEAR y from {CAS}
           where {TR} and INCIDENT_YEAR between 2010 and 2025),
upc as (select distinct cty from f where rr='UP' and y between 2010 and 2014 and cty is not null),
ups as (select distinct st from f where rr='UP' and y between 2010 and 2014),
tag as (select f.*, case when upc.cty is not null then '1_up_county' when ups.st is not null then '2_up_state_other_cty' else '3_non_up_state' end zone
        from f left join upc on f.cty=upc.cty left join ups on f.st=ups.st),
c as (select zone, cty, iff(max(st)='CALIFORNIA','CA','nonCA') part,
  count_if(rr='UP' and y between 2015 and 2017)/3 up_a, count_if(rr='UP' and y between 2023 and 2025)/3 up_b,
  count_if(rr='BNSF' and y between 2015 and 2017)/3 bn_a, count_if(rr='BNSF' and y between 2023 and 2025)/3 bn_b,
  count_if(rr!='UP' and y between 2015 and 2017)/3 ot_a, count_if(rr!='UP' and y between 2023 and 2025)/3 ot_b
  from tag group by 1,2),
agg as (
  select zone, 'ALL' part, count(*) n_cty, sum(up_a) up_a, sum(up_b) up_b, sum(bn_a) bn_a, sum(bn_b) bn_b, sum(ot_a) ot_a, sum(ot_b) ot_b,
    median(up_b-up_a) med_up, median(ot_b-ot_a) med_ot, count_if(up_b-up_a > ot_b-ot_a) up_more, count_if(up_b-up_a < ot_b-ot_a) ot_more from c group by zone
  union all
  select zone, part, count(*), sum(up_a), sum(up_b), sum(bn_a), sum(bn_b), sum(ot_a), sum(ot_b),
    median(up_b-up_a), median(ot_b-ot_a), count_if(up_b-up_a > ot_b-ot_a), count_if(up_b-up_a < ot_b-ot_a) from c group by zone, part)
select zone, part, n_cty, round(up_a,1) up_a, round(up_b,1) up_b, round(bn_a,1) bn_a, round(bn_b,1) bn_b, round(ot_a,1) ot_a, round(ot_b,1) ot_b,
  round(med_up,2) med_up, round(med_ot,2) med_ot, up_more, ot_more from agg order by 1,2"""

# s5: state peer. UP vs every other railroad in the same state, only states where UP reports; plus West Coast passenger lines
Q["s5"] = f"""
with f as (select RAILROAD_CODE rr, STATE_NAME st, INCIDENT_YEAR y from {CAS}
           where {TR} and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025)),
s as (select st, count_if(rr='UP' and y<=2017)/3 up_a, count_if(rr='UP' and y>=2023)/3 up_b,
        count_if(rr!='UP' and y<=2017)/3 ot_a, count_if(rr!='UP' and y>=2023)/3 ot_b,
        count_if(rr in ('ATK','SCAX','PCJX','PCMZ','NCTC','SDNX') and y<=2017)/3 ps_a, count_if(rr in ('ATK','SCAX','PCJX','PCMZ','NCTC','SDNX') and y>=2023)/3 ps_b from f group by 1),
u as (select * from s where up_a+up_b>0)
select 'tot' k, count(*)::varchar st, round(sum(up_a),1) up_a, round(sum(up_b),1) up_b, round(sum(ot_a),1) ot_a, round(sum(ot_b),1) ot_b,
  round(sum(ps_a),1) ps_a, round(sum(ps_b),1) ps_b, round(median(up_b-up_a),2) med_up, round(median(ot_b-ot_a),2) med_ot, count_if(up_b-up_a > ot_b-ot_a) up_more, count_if(up_b-up_a < ot_b-ot_a) ot_more from u
union all select 'tot_exCA', count(*)::varchar, round(sum(up_a),1), round(sum(up_b),1), round(sum(ot_a),1), round(sum(ot_b),1), round(sum(ps_a),1), round(sum(ps_b),1),
  round(median(up_b-up_a),2), round(median(ot_b-ot_a),2), count_if(up_b-up_a > ot_b-ot_a), count_if(up_b-up_a < ot_b-ot_a) from u where st!='CALIFORNIA'
union all select * from (select 'st', st, round(up_a,1), round(up_b,1), round(ot_a,1), round(ot_b,1), round(ps_a,1), round(ps_b,1), null, null, null, null from u order by up_b desc)
order by 1, 4 desc"""

# s6: sentinels and lag. UP vs BNSF top ages; 2025 vs 2026 by month; load date
Q["s6"] = f"""
select * from (
select 'age_top' k, RAILROAD_CODE a, AGE_OF_PERSON::varchar b, count(*) n from {CAS}
  where {TR} and RAILROAD_CODE in ('UP','BNSF') and INCIDENT_YEAR between 2015 and 2025 group by 2,3
  qualify row_number() over (partition by RAILROAD_CODE order by count(*) desc) <= 4)
union all select 'age_edge', RAILROAD_CODE, iff(AGE_OF_PERSON is null, 'null', iff(AGE_OF_PERSON<=1,'le1', iff(AGE_OF_PERSON>=99,'ge99','ok'))), count(*) from {CAS}
  where {TR} and RAILROAD_CODE in ('UP','BNSF') and INCIDENT_YEAR between 2015 and 2025 group by 2,3
union all select 'month', INCIDENT_YEAR::varchar, month(DATE)::varchar, count(*) from {CAS} where {TR} and INCIDENT_YEAR in (2025,2026) group by 2,3
union all select 'load', max(_INGESTED_AT)::varchar, min(_INGESTED_AT)::varchar, count(distinct _INGESTED_AT) from {CAS}
order by 1,2,3"""

TRAIN = "EVENT ilike any ('%on-track equipment%','%on track equipment%','Highway-rail%','Caught Between Equipment%')"

# s7: were they killed by trains? event mix train vs not-train per railroad and window; national; top non-train events; UP age-40 share
Q["s7"] = f"""
with f as (select iff(RAILROAD_CODE in ('UP','BNSF','CSX','NS','ATK'), RAILROAD_CODE, 'other') rr, INCIDENT_YEAR y,
             iff({TRAIN}, 'train', 'nontrain') ev, EVENT, AGE_OF_PERSON age
           from {CAS} where {TR} and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025))
select 'mix' k, rr, ev, round(count_if(y<=2017)/3,1) a, round(count_if(y>=2023)/3,1) b from f group by rr, ev
union all select 'nat', 'ALL', ev, round(count_if(y<=2017)/3,1), round(count_if(y>=2023)/3,1) from f group by ev
union all select 'nontrain_ev', rr, EVENT, round(count_if(y<=2017)/3,1), round(count_if(y>=2023)/3,1) from f
   where ev='nontrain' and rr in ('UP','BNSF','CSX','NS') group by rr, EVENT having count(*) >= 6
union all select 'age40', rr, iff(y<=2017,'A','B'), count_if(age=40), count(*) from f where rr in ('UP','BNSF','CSX','NS') group by 2,3
order by 1, 2, 3"""

# s8: same-county DiD on train strikes only; UP year by year train vs not-train and two new-looking event codes
Q["s8"] = f"""
with f as (select RAILROAD_CODE rr, STATE_NAME st, STATE_CODE||'-'||COUNTY_CODE cty, INCIDENT_YEAR y, EVENT ev0, {TRAIN} tr
           from {CAS} where {TR} and INCIDENT_YEAR between 2010 and 2025),
upc as (select distinct cty from f where rr='UP' and y between 2010 and 2014 and cty is not null),
c as (select f.cty, iff(max(f.st)='CALIFORNIA','CA','nonCA') part,
  count_if(tr and rr='UP' and y between 2015 and 2017)/3 up_a, count_if(tr and rr='UP' and y between 2023 and 2025)/3 up_b,
  count_if(tr and rr!='UP' and y between 2015 and 2017)/3 ot_a, count_if(tr and rr!='UP' and y between 2023 and 2025)/3 ot_b
  from f join upc on f.cty=upc.cty group by 1)
select 'did_train' k, 'ALL' part, count(*) n, round(sum(up_a),1) up_a, round(sum(up_b),1) up_b, round(sum(ot_a),1) ot_a, round(sum(ot_b),1) ot_b,
  round(median(up_b-up_a),2) med_up, round(median(ot_b-ot_a),2) med_ot, count_if(up_b-up_a > ot_b-ot_a) up_more, count_if(up_b-up_a < ot_b-ot_a) ot_more from c
union all select 'did_train', part, count(*), round(sum(up_a),1), round(sum(up_b),1), round(sum(ot_a),1), round(sum(ot_b),1),
  round(median(up_b-up_a),2), round(median(ot_b-ot_a),2), count_if(up_b-up_a > ot_b-ot_a), count_if(up_b-up_a < ot_b-ot_a) from c group by part
union all select 'up_yr', y::varchar, count_if(rr='UP'), count_if(rr='UP' and tr), count_if(rr='UP' and not tr),
  count_if(rr='UP' and ev0='On track equipment, other incidents'), count_if(rr='UP' and ev0='Aggravated pre-existing condition'),
  count_if(rr='BNSF' and not tr), count_if(rr='CSX' and not tr), null, null from f group by y
order by 1, 2"""
