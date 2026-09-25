-- FRA casualties: UP vs BNSF inside the same states. States where both report trespasser deaths; yearly avg 2015-2017 vs 2023-2025
with f as (select RAILROAD_CODE rr, STATE_NAME st, INCIDENT_YEAR y from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF') and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025)),
s as (select st, count_if(rr='UP' and y<=2017)/3 up_a, count_if(rr='UP' and y>=2023)/3 up_b, count_if(rr='BNSF' and y<=2017)/3 bn_a, count_if(rr='BNSF' and y>=2023)/3 bn_b from f group by 1),
shared as (select * from s where up_a+up_b > 0 and bn_a+bn_b > 0)
select 'shared_total' k, count(*)::varchar st, round(sum(up_a),1) up_a, round(sum(up_b),1) up_b, round(sum(bn_a),1) bn_a, round(sum(bn_b),1) bn_b,
  count_if(up_b-up_a > bn_b-bn_a) up_rose_more, round(median(up_b-up_a),2) med_up_change, round(median(bn_b-bn_a),2) med_bn_change from shared
union all select * from (select 'state', st, round(up_a,1), round(up_b,1), round(bn_a,1), round(bn_b,1), null, null, null from shared order by up_b+bn_b desc limit 14);
