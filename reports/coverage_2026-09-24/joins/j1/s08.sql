-- CMS penalties on CCN: Reliant MO homes vs other MO homes. fines, dollars, payment denials, per 100 beds; plus penalty date span and duplicate check on FINE_ID
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, iff(CHAIN_ID='446','reliant','other_mo') grp, NUMBER_OF_CERTIFIED_BEDS beds from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE='MO'),
p as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PENALTY_DATE, PENALTY_TYPE, FINE_ID, FINE_AMOUNT, PAYMENT_DENIAL_LENGTH_IN_DAYS pdd from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES where STATE='MO'),
pp as (select nh.grp, p.* from p join nh on nh.ccn=p.ccn)
select grp, (select count(*) from nh n2 where n2.grp=x.grp) homes, (select sum(beds) from nh n2 where n2.grp=x.grp) beds,
  count(*) penalties, count(distinct ccn) homes_penalized, count_if(PENALTY_TYPE ilike 'fine%') fines, sum(FINE_AMOUNT) fine_dollars, max(FINE_AMOUNT) max_fine,
  count_if(PENALTY_TYPE ilike 'payment%') pay_denials, sum(pdd) denial_days, min(PENALTY_DATE) p0, max(PENALTY_DATE) p1,
  count(FINE_ID) fine_ids, count(distinct FINE_ID) distinct_fine_ids,
  round(100*sum(FINE_AMOUNT)/(select sum(beds) from nh n2 where n2.grp=x.grp),0) fine_dollars_per_100_beds,
  round(100*count_if(PENALTY_TYPE ilike 'payment%')/(select sum(beds) from nh n2 where n2.grp=x.grp),3) denials_per_100_beds
from pp x group by grp order by grp
