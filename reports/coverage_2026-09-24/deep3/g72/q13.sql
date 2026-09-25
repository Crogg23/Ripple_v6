-- Dull-explanation test: do the two over-1 tracts soak up geocoder fallbacks? Registrations by 12-digit block group and ZIP,
-- for the two outliers and their burn-zone peers (Lahaina 314.02, 314.05; Fort Myers Beach 601.02).
select DISASTER_NUMBER::text dn, left(CENSUS_GEOID,11) tr, left(CENSUS_GEOID,12) bg, count(distinct REGISTRATION_ID) regs,
  count(distinct DAMAGED_ZIP_CODE) zips, mode(DAMAGED_ZIP_CODE) top_zip, mode(DAMAGED_CITY) top_city,
  round(100*count_if(VERIFIED_OCCUPANCY::text in ('True','true','1'))/count(*),1) pct_ver_occ,
  round(100*count_if(PRIMARY_RESIDENCE::text in ('True','true','1'))/count(*),1) pct_primary,
  round(100*count_if(OWN_RENT='R')/count(*),1) pct_rent, listagg(distinct RESIDENCE_TYPE, '|') res_types,
  mode(RESIDENCE_TYPE) top_res
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
where DISASTER_NUMBER::text in ('4673','4724')
  and left(CENSUS_GEOID,11) in ('15009031404','15009031402','15009031405','12071001910','12071060102')
group by 1,2,3 order by 1,2,3;
