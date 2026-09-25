with c as (
 select FILER_IDENT, FILER_NAME, REPORT_INFO_IDENT::string rid, PERIOD_START_DT::date ps, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
 where PERIOD_START_DT >= '2021-01-01' and ltrim(FILER_IDENT,'0') <> '85404'
 qualify row_number() over (partition by FILER_IDENT, PERIOD_START_DT, PERIOD_END_DT order by FILED_DT desc, REPORT_INFO_IDENT desc) = 1),
 cl as (select REPORT_ID::string rid, listagg(distinct upper(ONBEHALFNAME), ' | ') clients from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING group by 1)
select * from (
 select c.FILER_NAME, sum(media) m, count_if(media>0) months, min(iff(media>0,ps,null)) first_ps, max(iff(media>0,ps,null)) last_ps,
  left(listagg(distinct iff(media>0, cl.clients, null), ' || '), 300) clients_on_media_reports,
  sum(sum(media)) over () all_other
 from c left join cl on cl.rid = c.rid
 where ps between '2021-05-01' and '2026-06-30'
 group by 1)
where m > 0 order by m desc limit 12
