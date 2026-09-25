-- Slave voyages: after the US ban (voyage began 1808 or later by YEARDEP; also arrival 1809 or later), voyages that sailed from mainland North American ports:
-- count, captives embarked and landed (editors' estimates), how they ended (FATE4), and voyages that landed captives in mainland North America, split by FATE4
with t as (select try_to_number(YEARDEP) yd, try_to_number(YEARAM) ya, left(PTDEPIMP,1)='2' us_dep, MJSELIMP1 land1, FATE4,
             try_to_number(SLAXIMP) emb, try_to_number(SLAMIMP) lan
           from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC)
select 'usdep_yd1808' k, count(*) voy, round(sum(emb)) emb, round(sum(lan)) lan, count_if(FATE4='1') f1, count_if(FATE4='2') f2, count_if(FATE4='3') f3, count_if(FATE4='4') f4, min(yd) y0, max(yd) y1 from t where us_dep and yd >= 1808
union all select 'usdep_ya1809', count(*), round(sum(emb)), round(sum(lan)), count_if(FATE4='1'), count_if(FATE4='2'), count_if(FATE4='3'), count_if(FATE4='4'), min(ya), max(ya) from t where us_dep and ya >= 1809
union all select 'usdep_1700_1807', count(*), round(sum(emb)), round(sum(lan)), count_if(FATE4='1'), count_if(FATE4='2'), count_if(FATE4='3'), count_if(FATE4='4'), min(ya), max(ya) from t where us_dep and ya between 1700 and 1807
union all select 'landNA_ya1809', count(*), round(sum(emb)), round(sum(lan)), count_if(FATE4='1'), count_if(FATE4='2'), count_if(FATE4='3'), count_if(FATE4='4'), min(ya), max(ya) from t where land1='20000' and ya >= 1809
union all select 'yd_vs_ya', count_if(yd is null), count_if(yd > ya), count_if(ya - yd > 2), null, null, null, null, null, null from t;
