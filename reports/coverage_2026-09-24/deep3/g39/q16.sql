-- Envirofacts vs full TRI facility list: ZIP first digit mix (is the 5,000-row sample random or a slice?)
select 'envirofacts' src, left(POSTAL_CODE,1) z1, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ENVIROFACTS group by 1,2
union all
select 'tri_full', left(ZIP_CODE,1), count(*) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY group by 1,2
order by 1,2
