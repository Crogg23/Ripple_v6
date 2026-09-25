-- Germany: per publisher. Rows, rows touched on 2025-08-12 exactly, created span, HVD flags, temporal sentinels, grant-data titles
select PUBLISHER pub, count(*) n, count_if(METADATA_MODIFIED::date='2025-08-12') mod_0812, min(METADATA_CREATED)::date c_min, max(METADATA_CREATED)::date c_max,
  count_if(IS_HVD is not null and IS_HVD not in ('','[]','null')) hvd, count_if(year(TEMPORAL_END)>=9000 or year(TEMPORAL_START)<1000) t_sentinel,
  count_if(TITLE ilike '%zuwendung%') zuwendung, count_if(TAGS ilike '%lebensmittel%') food_tag, count_if(TAGS ilike '%kriminalstat%') pks_tag,
  count(distinct lower(trim(TITLE))) titles, left(any_value(TITLE),70) sample_title
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA group by 1 order by 2 desc limit 15
