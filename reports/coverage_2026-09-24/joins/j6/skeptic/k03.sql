with c as (
 select FILER_IDENT, FILER_NAME, REPORT_INFO_IDENT, REPORT_TYPE_CD, FORM_TYPE_CD, PERIOD_START_DT::date ps, PERIOD_END_DT::date pe, FILED_DT, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media,
  row_number() over (partition by FILER_IDENT, PERIOD_START_DT, PERIOD_END_DT order by FILED_DT desc, REPORT_INFO_IDENT desc) rn
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER)
select iff(ltrim(FILER_IDENT,'0')='85404','SANDS','OTHER') who,
 case when ps between '2021-05-01' and '2026-06-30' then 'in_window_ps' when ps < '2021-05-01' and pe >= '2021-05-01' then 'straddles_start' when ps > '2026-06-30' then 'after' else 'before' end w,
 left(REPORT_TYPE_CD,12) rtype, datediff('day', ps, pe) > 40 multi_month,
 count(*) n, count_if(rn=1) n_dedup, sum(media) media_raw, sum(iff(rn=1,media,0)) media_dedup, count(distinct FILER_IDENT) filers, min(ps) ps0, max(ps) ps1
from c where pe >= '2020-01-01'
group by 1,2,3,4 having sum(media) > 0 or who='SANDS' order by 1,2,3,4
