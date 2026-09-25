-- Judge tables completeness: FJC Article III judges by first commission year -> in CourtListener JUDGES (FJC_ID = NID)?
-- has any education row? a law degree? a party row? Does CL's appointer-party agree with FJC's appointing-president party?
with fjc as (select try_to_number(NID::string) nid, year(try_to_date(COMMISSION_DATE_1::string)) cy,
               PARTY_OF_APPOINTING_PRESIDENT_1 p from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_ARTICLE_III_JUDGES),
cl as (select try_to_number(FJC_ID::string) fid, min(ID::string) pid from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES
       where try_to_number(FJC_ID::string) is not null group by 1),
ed as (select PERSON_ID::string pid, count(*) n_deg, max(iff(DEGREE_LEVEL in ('jd','llb','llm','jsd'),1,0)) has_law
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_EDUCATIONS group by 1),
af as (select PERSON_ID::string pid, max(iff(SOURCE='a', POLITICAL_PARTY, null)) a_party
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS group by 1)
select case when fjc.cy is null then 'no date' when fjc.cy < 1990 then 'before 1990' when fjc.cy < 2015 then '1990-2014' else fjc.cy::string end yb,
  count(*) fjc_judges, count(cl.fid) in_cl, count(ed.pid) has_edu, sum(ed.has_law) has_law_degree, count(af.pid) has_party_row,
  sum(iff(af.a_party is not null,1,0)) has_appointer_party,
  sum(iff((af.a_party='d' and fjc.p ilike 'Democrat%') or (af.a_party='r' and fjc.p ilike 'Republican%'),1,0)) party_agree,
  sum(iff(af.a_party in ('d','r') and not ((af.a_party='d' and fjc.p ilike 'Democrat%') or (af.a_party='r' and fjc.p ilike 'Republican%')),1,0)) party_disagree
from fjc left join cl on cl.fid = fjc.nid left join ed on ed.pid = cl.pid left join af on af.pid = cl.pid
group by 1 order by 1
