-- (rerun of q25; "sample" is a reserved word) Read the words: enforcement / money / force keywords in titles across the four sampled catalogs. Hits and sample titles (source-scouting, not a story)
with u as (
  select 'AR' t, DATASET_TITLE title, C_ORGANIZATION pub from (select distinct DATASET_ID, DATASET_TITLE, C_ORGANIZATION from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_AR_DATOSGOB)
  union all select 'CL', TITLE, PUBLISHER_INSTITUTION from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB
  union all select 'DE', TITLE, PUBLISHER from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA
  union all select 'GR', TITLE, ORGANISATION_NAME from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV)
, k as (select column1 theme, column2 pat from values
  ('fines/sanctions', '(sanci|multa|bu(ss|ß)geld|sanktion|πρόστιμ|κυρώσ)'),
  ('contracts/purchasing', '(licitaci|contrataci|compras p|vergabe|auftr(a|ä)ge|συμβάσ|προμήθει)'),
  ('police/force/prisons', '(fuerza|armas|polic|penitenci|c(á|a)rcel|kriminal|gef(a|ä)ngnis|αστυνομ|φυλακ)'),
  ('grants/subsidies', '(subsidi|subvenci|zuwendung|f(ö|o)rder|επιχορήγ|ενίσχυσ)'),
  ('pollution/inspections', '(contamina|emision|emisi(ó|o)n|inspecci|fiscalizaci|kontrolle|schadstoff|ρύπαν|επιθεώρ)'))
select u.t, k.theme, count(*) hits, count(distinct u.pub) pubs, left(listagg(distinct left(u.title,55)||' ['||left(coalesce(u.pub,'?'),30)||']', ' || '),600) smp
from u join k on regexp_like(lower(u.title), '.*'||k.pat||'.*')
group by 1,2 order by 1,3 desc
