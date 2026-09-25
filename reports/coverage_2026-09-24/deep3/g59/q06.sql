-- FAO: pull the headline hunger series (point values only, not the confidence bounds) for local analysis
select AREA_CODE, AREA_CODE_M49, AREA, ITEM_CODE, YEAR_CODE, YEAR, VALUE, FLAG, NOTE
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT_FOOD_SECURITY
where ELEMENT = 'Value'
  and ITEM_CODE in ('210041','210011','210091','210401','210081','210071','210090','210400','210040','21025','210010')
