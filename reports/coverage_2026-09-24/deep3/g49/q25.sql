-- Education peer comparison: federal judges by first appointing president (FJC), law school from CourtListener degrees (JID or NID key).
-- Share with a Harvard or Yale law degree, among judges whose law degree is on file.
with fjc as (select try_to_number(JID::string) jid, try_to_number(NID::string) nid, APPOINTING_PRESIDENT_1 pres,
               min(try_to_date(COMMISSION_DATE_1::string)) over (partition by APPOINTING_PRESIDENT_1) first_comm
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_ARTICLE_III_JUDGES),
cl as (select try_to_number(FJC_ID::string) fid, min(ID::string) pid from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES
       where try_to_number(FJC_ID::string) is not null group by 1),
law as (select e.PERSON_ID::string pid, max(iff(s.NAME ilike '%harvard%',1,0)) harvard, max(iff(s.NAME ilike '%yale%',1,0)) yale,
          max(iff(s.NAME ilike '%notre dame%' or s.NAME ilike '%georgetown%' or s.NAME ilike '%chicago%' or s.NAME ilike '%stanford%' or s.NAME ilike '%columbia%',1,0)) next5
        from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_EDUCATIONS e
        left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_SCHOOLS s on s.ID::string = e.SCHOOL_ID::string
        where e.DEGREE_LEVEL in ('jd','llb') group by 1)
select fjc.pres, min(fjc.first_comm) first_commission, count(*) judges, count(coalesce(c1.pid, c2.pid)) in_cl, count(law.pid) law_on_file,
  sum(law.harvard) harvard, sum(law.yale) yale, sum(iff(law.harvard=1 or law.yale=1,1,0)) harvard_or_yale, sum(law.next5) next5_schools
from fjc left join cl c1 on c1.fid = fjc.jid left join cl c2 on c2.fid = fjc.nid
left join law on law.pid = coalesce(c1.pid, c2.pid)
group by 1 order by 2
