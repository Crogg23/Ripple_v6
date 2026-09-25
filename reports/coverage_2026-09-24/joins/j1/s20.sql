-- [rerun, alias] USAspending miss check: MO rows, rows whose recipient name contains HEALTH CARE CENTER, and a sample, for CFDA 93.498 (Provider Relief) and 59.073 (PPP)
select RECIPIENT_STATE_CODE, count(*) n, count_if(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%') hcc, count_if(CFDA_NUMBER='93.498') prf_rows, count_if(CFDA_NUMBER='59.073') ppp_rows,
  listagg(distinct iff(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%' and CFDA_NUMBER in ('93.498','59.073'), RECIPIENT_NAME, null), '; ') within group (order by iff(upper(RECIPIENT_NAME) like '%HEALTH CARE CENTER%' and CFDA_NUMBER in ('93.498','59.073'), RECIPIENT_NAME, null)) name_sample
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL where RECIPIENT_STATE_CODE in ('MO') group by 1
