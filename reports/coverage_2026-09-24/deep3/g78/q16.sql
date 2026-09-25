-- Slave voyages: peer comparison inside the same era. Voyages arriving 1850-1866, by where they sailed from (broad region):
-- captives per voyage, share whose owners' goal was thwarted by people (FATE4=3, mostly captures), share delivered (FATE4=1), recorded death share
with t as (select case left(PTDEPIMP,1) when '2' then 'N America' when '3' then 'Caribbean' when '5' then 'Brazil' when '1' then 'Europe' else 'other/unknown' end dep,
             try_to_number(SLAXIMP) emb, try_to_number(SLAMIMP) lan, FATE4, try_to_double(VYMRTRAT) mort, MJSELIMP1 land1
           from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC where try_to_number(YEARAM) between 1850 and 1866)
select dep, count(*) voy, round(sum(emb)) emb, round(avg(emb)) emb_per_voy, round(median(emb)) med_emb, round(sum(lan)) landed,
  count_if(FATE4='1') delivered, count_if(FATE4='3') thwarted_people, count_if(FATE4='2') thwarted_nature, count_if(FATE4='4' or FATE4 is null) unknown,
  count_if(mort is not null) mort_n, round(avg(mort),3) mort_avg, count_if(land1='30000') to_carib, count_if(land1='50000') to_brazil
from t group by 1 order by voy desc;
