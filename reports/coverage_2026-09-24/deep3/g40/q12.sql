-- WBD HUC8: confirm it is a one-row-per-watershed lookup; check units (acres vs sq km vs map-software area) and cross-border rows
with h as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WBD_HUC8)
select 'profile' k, count(*)::text a, count(distinct HUC8)::text b, listagg(distinct length(HUC8)::text,',')::text c,
  count_if(STATES ilike '%CN%' or STATES ilike '%MX%')::text d, count(distinct _SOURCE_RUN_ID)::text e,
  count_if(SOURCE_FEATURE_ID=0)::text f,
  round(min(AREA_ACRES/nullif(AREA_SQ_KM,0)),3)::text||'..'||round(max(AREA_ACRES/nullif(AREA_SQ_KM,0)),3)::text g,
  round(min(SHAPE_AREA/nullif(AREA_SQ_KM*1e6,0)),2)::text||'..'||round(max(SHAPE_AREA/nullif(AREA_SQ_KM*1e6,0)),2)::text h
from h
union all select * from (select 'by_region', left(HUC8,2), count(*)::text, round(median(SHAPE_AREA/nullif(AREA_SQ_KM*1e6,0)),2)::text,
  count_if(STATES ilike '%CN%' or STATES ilike '%MX%')::text, left(any_value(STATES),20), null, round(sum(AREA_SQ_KM))::text, null from h group by 2 order by 2)
