-- @irs8872_all
select FORM_TYPE, FORM_ID_NUMBER, EIN, ORGANIZATION_NAME, INITIAL_REPORT_IND, AMENDED_REPORT_IND, FINAL_REPORT_IND,
  PERIOD_BEGIN_DATE, PERIOD_END_DATE, ORG_FORMATION_DATE, TOTAL_SCHED_A, TOTAL_SCHED_B, INSERT_DATETIME
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS
-- @irs527_copy_check
with p as (select EIN, ORGANIZATION_NAME from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS),
e as (select EIN, ORG_NAME, FILED_DATE from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_527_ORGS),
ed as (select distinct EIN, ORG_NAME from e)
select (select count(*) from p) p_rows, (select count(*) from e) e_rows,
  (select count(distinct EIN) from p) p_eins, (select count(distinct EIN) from e) e_eins,
  (select count(*) from p left join ed on p.EIN = ed.EIN and p.ORGANIZATION_NAME = ed.ORG_NAME where ed.EIN is null) p_rows_no_match_in_e,
  (select min(FILED_DATE)::string from e) e_min_filed, (select max(FILED_DATE)::string from e) e_max_filed
-- @jcs_copy_check
with x as (select JUSTICENAME, try_to_number(TERM::string) term, try_to_double(JCS::string) jcs from LIBRARY_MARTS.POLITICS.POLITICS__XC_JCS_SCOTUS),
j as (select JUSTICE_NAME, try_to_number(TERM::string) term, try_to_double(JCS::string) jcs from LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_SCOTUS)
select (select count(*) from x) x_rows, (select min(term) from x) x_min_term, (select max(term) from x) x_max_term,
  (select count(*) from j) j_rows,
  (select count(*) from x join j on x.JUSTICENAME = j.JUSTICE_NAME and x.term = j.term and abs(x.jcs - j.jcs) < 1e-6) exact_matches
-- @fec_cmte_zombies
select * from LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE
where CMTE_ID in ('C00306860','C00347591','C00222455','C00410118','C00229377','C00410829','C00308387','C00440115',
  'C00196915','C00384016','C00153684','C00382457','C00238444','C00002592','C00703975')
   or CAND_ID = 'P40010415'
-- @fec_link_zombies
select * from LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK
where CMTE_ID in ('C00306860','C00347591','C00222455','C00410118','C00229377','C00410829','C00308387','C00440115',
  'C00196915','C00384016','C00153684','C00382457','C00238444','C00002592')
-- @ca_employer_names_for_ours
select e.EMPLOYER_ID, e.SESSION_ID, e.EMPLOYER_NAME, e.SESSION_TOTAL_AMT, e.INTEREST_NAME
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER e
where e.EMPLOYER_ID in (select EMPLOYER_ID from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER_FIRMS)
-- @ca_employer_session_coverage
select e.SESSION_ID::string session_id, count(distinct e.EMPLOYER_ID) employers_all,
  count(distinct case when f.EMPLOYER_ID is not null then e.EMPLOYER_ID end) employers_in_emp_firms
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER e
left join (select distinct EMPLOYER_ID, SESSION_ID from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER_FIRMS) f
  on e.EMPLOYER_ID = f.EMPLOYER_ID and e.SESSION_ID = f.SESSION_ID
group by 1 order by 1
-- @ca_firm_names_for_ours
select FIRM_ID, SESSION_ID, FIRM_NAME, SESSION_TOTAL_AMT
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM
where FIRM_ID in (select FIRM_ID from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER_FIRMS)
-- @ca_cover_q2_2001
select FORM_TYPE, ENTITY_CD, count(*) n_rows, count(distinct FILING_ID) filings, count(distinct FILER_ID) filers,
  count(distinct case when FILING_ID in (select FILING_ID from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM_EMPLOYER) then FILING_ID end) in_firm_emp
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER
where FROM_DATE::string like '2001-04-01%'
group by 1, 2 order by 3 desc
