-- Slave voyages: time. Voyages that sailed from mainland North American ports (codes starting 2), by decade of arrival 1780-1869,
-- where they took the captives (broad landing region), captives embarked (editors' estimate); US-flag voyages; voyages landing in mainland North America
with t as (select floor(try_to_number(YEARAM)/10)*10 dec, left(PTDEPIMP,1)='2' us_dep, NATINIMP='9' us_flag, MJSELIMP1 land1,
             try_to_number(SLAXIMP) emb, try_to_number(SLAMIMP) lan
           from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC where try_to_number(YEARAM) >= 1780)
select dec, count(*) all_voy, count_if(us_dep) us_dep_voy, round(sum(iff(us_dep, emb, 0))) us_dep_emb,
  count_if(us_dep and land1='30000') us_to_carib, count_if(us_dep and land1='20000') us_to_na, count_if(us_dep and land1='50000') us_to_brazil,
  count_if(us_dep and land1='40000') us_to_spmain, count_if(us_dep and (land1 is null or land1 not in ('20000','30000','40000','50000'))) us_to_other,
  count_if(us_flag) usflag_voy, count_if(us_flag and not us_dep) usflag_not_usdep,
  count_if(land1='20000') land_na_voy, round(sum(iff(land1='20000', lan, 0))) land_na_captives
from t group by 1 order by 1;
