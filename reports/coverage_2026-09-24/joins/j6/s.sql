-- Julie Linn Minnehan (filer of the NY jet report): all her cover reports 2019-2026 with any spend, the clients named on each (REPORT_ID join), and subject lines
with cv as (select REPORT_INFO_IDENT::string rid, FORM_TYPE_CD, REPORT_TYPE_CD, APPLICABLE_YEAR, PERIOD_START_DT, FILED_DT,
   try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2) trans, try_to_number(TOTAL_EXPEND_FOOD,18,2) food, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media, try_to_number(TOTAL_EXPEND_EVENT,18,2) evt
  from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where FILER_NAME ilike 'Minnehan%'),
 cl as (select REPORT_ID::string rid, listagg(distinct upper(ONBEHALFNAME), ' | ') clients from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING group by 1),
 sm as (select REPORT_ID::string rid, listagg(distinct SUBJECTMATTERCODEVALUE, '; ') subj from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER group by 1)
select cv.*, cl.clients, left(sm.subj,150) subj, count(*) over () all_reports
from cv left join cl using (rid) left join sm using (rid)
where coalesce(trans,0)+coalesce(food,0)+coalesce(media,0)+coalesce(evt,0) > 0 or cl.clients is not null
order by PERIOD_START_DT
