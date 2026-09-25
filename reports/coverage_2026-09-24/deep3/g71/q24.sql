-- France dull test on the vanished headline datasets: any LIVE dataset (any publisher) whose title carries the same key words?
with k as (select column1 topic, column2 pat from values
  ('Alim confiance (restaurant hygiene inspections)', '%alim%confiance%'), ('Alim confiance', '%contr_les officiels sanitaires%'),
  ('Musees de France list', '%mus_es de france%'), ('Foundations of public utility', '%utilit_ publique%'),
  ('Sitadel building permits', '%sitadel%'), ('Social housing RPLS', '%locatifs des bailleurs%'), ('Social housing RPLS', '%rpls%'),
  ('Pegase energy stats', '%p_gase%'), ('Meteo-France station obs', '%observation%stations m_t_orologiques%'), ('Meteo-France station obs', '%synop%'))
, t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
select k.topic, k.pat, count_if(t.ARCHIVED='False') live_hits, count_if(t.ARCHIVED<>'False') archived_hits,
  left(listagg(distinct iff(t.ARCHIVED='False', left(t.TITLE,60)||' ['||coalesce(t.ORGANIZATION_NAME,t.OWNER,'?')||', '||t.CREATED_AT::date||', dl '||coalesce(t.NB_RESOURCE_DOWNLOADS,0)||']', null), ' || '),700) live_titles
from k left join t on lower(t.TITLE) like k.pat
group by 1,2 order by 1
