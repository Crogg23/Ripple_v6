-- France time: datasets created per year on the portal (native only; harvested rows carry the source's own date), and how many of each year are archived now
select year(CREATED_AT) yr, count(*) native_created, count_if(ARCHIVED='False') still_live, round(100*count_if(ARCHIVED<>'False')/count(*),1) pct_archived,
  count(distinct ORGANIZATION_ID) orgs, median(NB_RESOURCE_DOWNLOADS) med_dl, median(QUALITY_SCORE) med_quality
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV
where (HARVEST_REMOTE_URL is null or HARVEST_REMOTE_URL='') and year(CREATED_AT) between 2010 and 2026
group by 1 order by 1
