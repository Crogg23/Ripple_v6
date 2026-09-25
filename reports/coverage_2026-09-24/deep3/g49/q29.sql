-- Education bias test: CourtListener's degree rows vs the FJC Article III table's own SCHOOL_1..5 / DEGREE_1..5, same judges (JID key).
-- Does CL cover a random slice, or skew to Harvard/Yale? Presidents from Reagan on; Trump split into 2017-21 and 2025-26.
with f as (select try_to_number(JID::string) jid, year(try_to_date(COMMISSION_DATE_1::string)) cy,
             APPOINTING_PRESIDENT_1 || iff(APPOINTING_PRESIDENT_1 ilike '%Trump%' and year(try_to_date(COMMISSION_DATE_1::string)) >= 2025, ' (2nd term)', '') pres,
             iff(concat_ws('|', coalesce(DEGREE_1,''), coalesce(DEGREE_2,''), coalesce(DEGREE_3,''), coalesce(DEGREE_4,''), coalesce(DEGREE_5,'')) ilike any ('%J.D.%','%LL.B.%'),1,0) f_law,
             iff(concat_ws('|', coalesce(SCHOOL_1,''), coalesce(SCHOOL_2,''), coalesce(SCHOOL_3,''), coalesce(SCHOOL_4,''), coalesce(SCHOOL_5,'')) ilike any ('%Harvard Law%','%Yale Law%'),1,0) f_hy
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_ARTICLE_III_JUDGES),
cl as (select try_to_number(FJC_ID::string) fid, min(ID::string) pid from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES
       where try_to_number(FJC_ID::string) is not null group by 1),
law as (select e.PERSON_ID::string pid, max(iff(s.NAME ilike '%harvard%' or s.NAME ilike '%yale%',1,0)) cl_hy
        from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_EDUCATIONS e
        left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_SCHOOLS s on s.ID::string = e.SCHOOL_ID::string
        where e.DEGREE_LEVEL in ('jd','llb') group by 1)
select f.pres, min(f.cy) first_year, count(*) judges, sum(f.f_law) fjc_law_on_file, sum(f.f_hy) fjc_harvard_yale,
  count(law.pid) cl_law_on_file, sum(law.cl_hy) cl_harvard_yale,
  sum(iff(law.pid is not null, f.f_hy, 0)) fjc_hy_among_cl_covered
from f left join cl on cl.fid = f.jid left join law on law.pid = cl.pid
where f.cy >= 1981
group by 1 order by 2
