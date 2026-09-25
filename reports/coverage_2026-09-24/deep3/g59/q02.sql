-- FAO food security: profile of measures, elements, years, flags, text values
with t as (select * from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT_FOOD_SECURITY)
select ITEM_CODE, ITEM, UNIT, count(*) n, count(distinct AREA_CODE) areas, count(distinct YEAR_CODE) years,
  min(YEAR_CODE) y0, max(YEAR_CODE) y1, listagg(distinct ELEMENT, '|') elems,
  count_if(VALUE like '<%') lt_vals, count_if(try_to_double(VALUE) is null and VALUE is not null and VALUE not like '<%') nonnum,
  count_if(VALUE is null or VALUE='') blank, listagg(distinct FLAG, '|') flags
from t group by 1,2,3 order by 1
