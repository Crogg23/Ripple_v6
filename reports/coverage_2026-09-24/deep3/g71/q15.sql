-- Argentina: profile. Grain (dataset vs file), orgs, formats, LAST_MODIFIED text parse, empty columns, geo codes
select count(*) n, count(distinct DATASET_ID) ids, count(distinct RESOURCE_URL) urls, count(distinct DATASET_ID||'|'||RESOURCE_URL) id_url,
  count(distinct lower(trim(DATASET_TITLE))) titles, count(distinct C_ORGANIZATION) orgs,
  count_if(LAST_MODIFIED is null or trim(LAST_MODIFIED)='') lm_blank, count_if(try_to_timestamp(LAST_MODIFIED) is null and trim(LAST_MODIFIED)<>'') lm_unparsed,
  min(try_to_timestamp(LAST_MODIFIED)) lm_min, max(try_to_timestamp(LAST_MODIFIED)) lm_max,
  count_if(SERIE_ID is not null and SERIE_ID<>'') serie, count_if(PROVINCIA_ID is not null and PROVINCIA_ID<>'') prov, count_if(MUNICIPIO_ID is not null and MUNICIPIO_ID<>'') muni,
  count_if(C_ORGANIZATION is null or trim(C_ORGANIZATION)='') org_blank, count_if(DESCRIPTION is null or DESCRIPTION='') desc_blank,
  count_if(RESOURCE_URL ilike '%datos.gob.ar%') url_portal, count_if(RESOURCE_URL ilike '%infra.datos.gob.ar%') url_infra
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_AR_DATOSGOB
