select COURT_ID, DATE_FILED::varchar df, DATE_TERMINATED::varchar dt, DOCKET_NUMBER, left(CASE_NAME,110) cn, NATURE_OF_SUIT, left(CAUSE,50) cause
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
where DATE_FILED >= '2018-01-01' and (
 upper(CASE_NAME) like '%KAPADIA%' or upper(CASE_NAME) like '%JENG%' or upper(CASE_NAME) like '%REYES CHOUZA%' or upper(CASE_NAME) like '%YUKEE%'
 or upper(CASE_NAME) like '%CASTILLO MADRIGAL%' or upper(CASE_NAME) like '%TULSYAN%' or upper(CASE_NAME) like '%BAHARLOO%' or upper(CASE_NAME) like '%KOHANZADEH%'
 or upper(CASE_NAME) like '%HAJHOSSEINI%' or upper(CASE_NAME) like '%LIMPEROS%' or upper(CASE_NAME) like '%YALAMURI%' or (upper(CASE_NAME) like '%DENNY%' and COURT_ID in ('azd','azb','ca9'))
 or (upper(CASE_NAME) like '%PALACIOS%' and COURT_ID in ('azd','azb','ca9')) or (upper(CASE_NAME) like '%KINDS%' and COURT_ID in ('azd','azb','ca9'))
 or upper(CASE_NAME) like '%GUTSTEIN%' or upper(CASE_NAME) like '%PIASECKI%' or upper(CASE_NAME) like '%OKORO%' or upper(CASE_NAME) like '%AMNIO%'
 or upper(CASE_NAME) like '%SKIN SUBSTITUTE%' or upper(CASE_NAME) like '%ORGANOGENESIS%' or upper(CASE_NAME) like '%ENCOLL%' or upper(CASE_NAME) like '%BIOLAB%' or upper(CASE_NAME) like '%LEGACY MEDICAL%' or upper(CASE_NAME) like '%APEX MEDICAL%')
order by df desc limit 200
