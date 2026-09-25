-- Spain: full publisher and sector strings (glance truncated them), plus year issued / modified
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_ES_DATOSGOB)
select * from (
 select 'publisher' k, PUBLISHER v, count(*) n from t group by 2 order by 3 desc limit 12)
union all select * from (
 select 'sector', SECTOR, count(*) from t group by 2 order by 3 desc limit 8)
union all select * from (
 select 'issued_yr', right(trim(ISSUED),4), count(*) from t group by 2 order by 2)
union all select * from (
 select 'modified_yr', right(trim(MODIFIED),4), count(*) from t group by 2 order by 2)
union all select * from (
 select 'format', FORMAT, count(*) from t group by 2 order by 3 desc limit 8)
union all select * from (
 select 'dup_dist_url', DISTRIBUTION_URL, count(*) from t group by 2 having count(*)>1 order by 3 desc limit 5);
