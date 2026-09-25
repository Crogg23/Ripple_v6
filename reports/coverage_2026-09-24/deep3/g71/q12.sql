-- Greece: padding check. Per top org: datasets, distinct titles, share whose files are only map-service links (WMS/WFS), median files
select ORGANISATION_NAME org, count(*) n, count(distinct lower(trim(TITLE))) titles,
  count_if(RESOURCE_FORMATS ilike '%WMS%' or RESOURCE_FORMATS ilike '%WFS%') map_svc, count_if(RESOURCE_FORMATS ilike '%CSV%' or RESOURCE_FORMATS ilike '%XLS%' or RESOURCE_FORMATS ilike '%JSON%') tabular,
  median(NUM_RESOURCES) med_files, min(DATE_CREATED)::date first_c, max(DATE_CREATED)::date last_c, count(distinct DATE_CREATED::date) days,
  count_if(DESCRIPTION like 'Δεν παρέχεται%') no_desc, left(any_value(TITLE),60) sample_title
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV group by 1 order by 2 desc limit 10
