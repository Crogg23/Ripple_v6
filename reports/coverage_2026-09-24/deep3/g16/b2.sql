-- [q13_ca_amend_rate_peer]
-- CA firms (F625) and employers (F635), periods 2015-2025, filers with 20+ filings: amended share vs the peer median; top by count and by rate
with f as (
  select FILING_ID, any_value(FORM_TYPE) ft, any_value(FILER_ID) filer, max_by(FILER_NAML, try_to_number(AMEND_ID)) nm,
    min(FROM_DATE) fd, max(try_to_number(AMEND_ID)) max_am
  from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER where FORM_TYPE in ('F625','F635') group by 1),
g as (
  select ft, filer, max(nm) nm, count(*) n, sum(iff(max_am>0,1,0)) am, sum(max_am) am_versions
  from f where year(fd) between 2015 and 2025 group by 1,2),
s as (
  select g.*, round(am/n,3) rate, count(*) over (partition by ft) n_peers,
    median(am/n) over (partition by ft) med_rate, sum(am) over (partition by ft) am_all, sum(n) over (partition by ft) n_all
  from g where n >= 20)
select * from s
qualify row_number() over (partition by ft order by am desc) <= 15 or row_number() over (partition by ft order by rate desc, n desc) <= 10
order by ft, am desc;

-- [q14_ca_amend_waves_by_filed_year]
-- CA amendment versions by the year they were filed (RPT_DATE), per form: how many, how many filers, and how much the top filer carries
with a as (
  select year(RPT_DATE) y, FORM_TYPE ft, FILER_ID, any_value(FILER_NAML) nm, count(*) v
  from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER
  where AMEND_ID <> '0' and year(RPT_DATE) between 1999 and 2026 group by 1,2,3)
select y, ft, sum(v) versions, count(*) filers, max(v) top_v, max_by(nm, v) top_filer, round(max(v)/sum(v),3) top_share, median(v) med_v
from a group by 1,2 order by 2,1;

-- [q15_ca_2020_amend_spike_filers]
-- Who carries the 2020-period amendment spike: per filer, amended filings for 2019, 2020, 2021 periods, and when the 2020 ones were first amended
with f as (
  select FILING_ID, any_value(FORM_TYPE) ft, any_value(FILER_ID) filer, max_by(FILER_NAML, try_to_number(AMEND_ID)) nm,
    min(FROM_DATE) fd, max(try_to_number(AMEND_ID)) max_am, min(iff(AMEND_ID <> '0', RPT_DATE, null)) first_am_dt
  from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER where FORM_TYPE in ('F625','F635') group by 1)
select ft, filer, max(nm) nm,
  sum(iff(year(fd)=2019 and max_am>0,1,0)) am19, sum(iff(year(fd)=2020 and max_am>0,1,0)) am20, sum(iff(year(fd)=2021 and max_am>0,1,0)) am21,
  sum(iff(year(fd)=2020,1,0)) n20,
  min(iff(year(fd)=2020 and max_am>0, first_am_dt, null)) first_am20, max(iff(year(fd)=2020 and max_am>0, first_am_dt, null)) last_am20,
  sum(sum(iff(year(fd)=2020 and max_am>0,1,0))) over (partition by ft) am20_all
from f group by 1,2
qualify row_number() over (partition by ft order by am20 desc) <= 12
order by ft, am20 desc;

-- [q16_ca_topics_by_year]
-- CA employer reports (F635, latest version per filing): real activity text by year, and employers naming AI and other topics
with f as (
  select FILING_ID, max_by(LOBBYING_ACTIVITY, try_to_number(AMEND_ID)) act, any_value(FILER_ID) filer, min(FROM_DATE) fd
  from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER where FORM_TYPE = 'F635' group by 1)
select year(fd) y, count(*) filings, count(distinct filer) employers,
  sum(iff(len(trim(act)) > 30 and not (act ilike 'see att%' or act ilike '%see attach%'),1,0)) real_text,
  count(distinct iff(len(trim(act)) > 30 and not (act ilike 'see att%' or act ilike '%see attach%'), filer, null)) emp_real_text,
  count(distinct iff(act ilike '%artificial intelligence%' or regexp_instr(act, '(^|[^A-Za-z])AI([^A-Za-z]|$)') > 0
        or act ilike '%SB 1047%' or act ilike '%SB1047%' or act ilike '%automated decision%', filer, null)) emp_ai,
  count(distinct iff(act ilike '%artificial intelligence%', filer, null)) emp_ai_phrase,
  count(distinct iff(act ilike '%social media%', filer, null)) emp_social,
  count(distinct iff(act ilike '%cannabis%' or act ilike '%marijuana%', filer, null)) emp_cannabis,
  count(distinct iff(act ilike '%wildfire%', filer, null)) emp_wildfire,
  count(distinct iff(act ilike '%PFAS%' or act ilike '%perfluoro%', filer, null)) emp_pfas,
  count(distinct iff(act ilike '%privacy%', filer, null)) emp_privacy,
  round(avg(len(act)),0) avg_len, max(len(act)) max_len
from f where year(fd) between 2000 and 2026 group by 1 order by 1;

-- [q17_ca_cover2_people]
-- CA cover2 names (original versions): who is listed under the most different filers, and the most filers in one quarter
with c as (select FILING_ID, AMEND_ID, any_value(FILER_ID) filer, min(FROM_DATE) fd
           from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER group by 1,2),
x as (select upper(trim(c2.ENTY_NAML))||', '||upper(trim(c2.ENTY_NAMF)) nm, c2.ENTITY_ID, c2.ENTITY_CD, c2.FORM_TYPE, c.filer, c.fd, c2.FILING_ID
      from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER2 c2
      join c on c2.FILING_ID = c.FILING_ID and c2.AMEND_ID = c.AMEND_ID
      where c2.AMEND_ID = '0'),
q as (select nm, max(nf) mx from (select nm, fd, count(distinct filer) nf from x group by 1,2) group by 1)
select x.nm, count(*) n, count(distinct x.FILING_ID) filings, count(distinct x.filer) filers, count(distinct x.ENTITY_ID) ids,
  listagg(distinct x.ENTITY_CD, ',') cds, listagg(distinct x.FORM_TYPE, ',') forms, min(year(x.fd)) y0, max(year(x.fd)) y1, any_value(q.mx) max_filers_one_qtr
from x join q on x.nm = q.nm
group by 1 order by filers desc limit 25;

-- [q18_tx_subject_filers_by_year]
-- TX: distinct lobbyists per subject per year, plus each year's total, for within-sample shares
select APPLICABLEYEAR y, SUBJECTMATTERCODEVALUE subj, count(distinct FILER_ID) filers, count(distinct REPORT_ID) reports
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER where APPLICABLEYEAR between '2002' and '2026' group by 1,2
union all
select APPLICABLEYEAR, '__ALL__', count(distinct FILER_ID), count(distinct REPORT_ID)
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER where APPLICABLEYEAR between '2002' and '2026' group by 1
order by 1, 3 desc;

-- [q19_tx_boxes_per_report]
-- TX: subjects ticked per report by year; reports that tick 40+ or 80+ boxes
with r as (select APPLICABLEYEAR y, REPORT_ID, any_value(REPORTTYPECD) rt, count(*) nsub
           from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER group by 1,2)
select y, count(*) reports, median(nsub) med, percentile_cont(0.9) within group (order by nsub) p90, max(nsub) mx,
  sum(iff(nsub >= 40,1,0)) r40, sum(iff(nsub >= 80,1,0)) r80, sum(iff(nsub >= 40, nsub, 0)) lines_in_40, sum(nsub) lines,
  sum(iff(rt = 'LOBBYACTANNUAL',1,0)) annual
from r group by 1 order by 1;

-- [q20_medsl_flags]
-- Senate returns: are the write-in and special flags ever true? Stage labels, party labels, FIPS shape
select IS_WRITEIN, IS_SPECIAL_ELECTION, upper(STAGE) st, count(*) n,
  sum(iff(CANDIDATE_NAME ilike '%write%' or CANDIDATE_NAME ilike '%scatter%',1,0)) writein_names,
  count(distinct ELECTION_YEAR) yrs, listagg(distinct PARTY_SIMPLIFIED, ',') parties,
  sum(iff(try_to_number(STATE_FIPS) is null,1,0)) bad_fips, min(len(STATE_FIPS)) min_fips_len,
  sum(iff(VOTE_SHARE is null,1,0)) null_share, sum(iff(abs(VOTE_SHARE - CANDIDATE_VOTES/nullif(TOTAL_VOTES,0)) > 0.001,1,0)) share_off
from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS
group by 1,2,3 order by n desc;

-- [q21_medsl_senate_vs_president]
-- Presidential years: Senate race total votes against the presidential total in the same state (roll-off). One Senate race per state: the larger one.
with p as (select ELECTION_YEAR y, STATE_ABBR s, max(TOTAL_VOTES) pt, count(*) prow
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_PRESIDENT_RETURNS group by 1,2),
se as (select ELECTION_YEAR y, STATE_ABBR s, TOTAL_VOTES tv, count(*) ncand,
         sum(iff(PARTY_SIMPLIFIED = 'DEMOCRAT',1,0)) nd, sum(iff(PARTY_SIMPLIFIED = 'REPUBLICAN',1,0)) nr,
         max_by(CANDIDATE_NAME, CANDIDATE_VOTES) winner, max_by(PARTY_SIMPLIFIED, CANDIDATE_VOTES) wparty, max(VOTE_SHARE) wshare
       from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS where upper(STAGE) = 'GEN' group by 1,2,3),
s1 as (select * from se qualify row_number() over (partition by y, s order by tv desc) = 1)
select s1.y, s1.s, p.pt, s1.tv, round(s1.tv / p.pt, 4) ratio, s1.ncand, s1.nd, s1.nr, s1.winner, s1.wparty, s1.wshare, p.prow
from s1 left join p on s1.y = p.y and s1.s = p.s
where mod(s1.y, 4) = 0
order by s1.y, ratio;

-- [q22_pac_undated_rows]
-- FEC PAC summary: the rows with no coverage date. What types, do they carry any money, do the same IDs show up dated?
with d as (select distinct CMTE_ID from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY where COVERAGE_END_DATE is not null)
select t.COMMITTEE_TYPE, count(*) n, sum(iff(d.CMTE_ID is not null,1,0)) also_dated,
  sum(iff(t.TOTAL_DISBURSEMENTS is null and t.CASH_CLOSE_OF_PERIOD is null and t.DEBTS_OWED_BY is null and t.CASH_BEGINNING_OF_PERIOD is null,1,0)) all_null,
  min(t.COMMITTEE_NAME) ex1, max(t.COMMITTEE_NAME) ex2, listagg(distinct t.FILING_FREQUENCY, ',') freqs, listagg(distinct t.COMMITTEE_DESIGNATION, ',') desigs,
  min(t.CMTE_ID) id_lo, max(t.CMTE_ID) id_hi
from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY t left join d on t.CMTE_ID = d.CMTE_ID
where t.COVERAGE_END_DATE is null group by 1 order by n desc;

-- [q23_pac_repeat_rows]
-- FEC PAC summary: committees with two rows in one cycle. Duplicate load or two coverage periods?
with p as (select *, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2) cyc
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY where COVERAGE_END_DATE is not null)
select cyc, CMTE_ID, COMMITTEE_NAME, COMMITTEE_TYPE, COVERAGE_END_DATE, TOTAL_RECEIPTS, TOTAL_DISBURSEMENTS, CASH_BEGINNING_OF_PERIOD, CASH_CLOSE_OF_PERIOD
from p qualify count(*) over (partition by CMTE_ID, cyc) > 1
order by cyc, CMTE_ID, COVERAGE_END_DATE limit 60;

-- [q24_pac_gap_by_type]
-- FEC PAC summary peer check: how often the cash math balances, by committee type and cycle
with p as (select *, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2) cyc,
             CASH_BEGINNING_OF_PERIOD + TOTAL_RECEIPTS - TOTAL_DISBURSEMENTS - CASH_CLOSE_OF_PERIOD gap
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY where COVERAGE_END_DATE is not null)
select cyc, COMMITTEE_TYPE, count(*) n, sum(iff(abs(gap) < 1,1,0)) exact, round(avg(iff(abs(gap) < 1,1,0)),3) exact_rate,
  sum(iff(abs(gap) >= 100000,1,0)) over100k, round(sum(abs(gap))/1e6,1) abs_gap_m, round(sum(TOTAL_RECEIPTS)/1e6,1) rcpt_m,
  sum(iff(month(COVERAGE_END_DATE) <> 12 or day(COVERAGE_END_DATE) <> 31,1,0)) not_yearend,
  sum(iff(abs(gap) >= 1 and (month(COVERAGE_END_DATE) <> 12 or day(COVERAGE_END_DATE) <> 31),1,0)) gap_and_not_yearend
from p where cyc between 2018 and 2024 group by 1,2 order by 1,2;

-- [q25_pac_chain_and_top_gaps]
-- Cycle to cycle: does one cycle's closing cash equal the next cycle's opening cash? Plus the 25 biggest in-cycle gaps with their chain gap
with p as (
  select CMTE_ID, COMMITTEE_NAME, COMMITTEE_TYPE, COVERAGE_END_DATE ce, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2) cyc,
    TOTAL_RECEIPTS r, TOTAL_DISBURSEMENTS d, CASH_BEGINNING_OF_PERIOD cb, CASH_CLOSE_OF_PERIOD cc,
    CASH_BEGINNING_OF_PERIOD + TOTAL_RECEIPTS - TOTAL_DISBURSEMENTS - CASH_CLOSE_OF_PERIOD gap
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY where COVERAGE_END_DATE is not null
  qualify row_number() over (partition by CMTE_ID, cyc order by COVERAGE_END_DATE desc) = 1),
j as (select a.*, b.cb next_cb, a.cc - b.cb chain_gap from p a left join p b on a.CMTE_ID = b.CMTE_ID and b.cyc = a.cyc + 2)
select 'chain' k, cyc, count(*) n, count(next_cb) n_next, sum(iff(abs(chain_gap) < 1,1,0)) chain_exact,
  sum(iff(abs(chain_gap) >= 100000,1,0)) chain_over100k, round(sum(abs(chain_gap))/1e6,1) chain_abs_m,
  null::string nm, null::string tp, null::float cb_m, null::float r_m, null::float d_m, null::float cc_m, null::float gap_m, null::float chain_m, null::date ce
from j where cyc < 2024 group by cyc
union all
select * from (
  select 'top', cyc, null, null, null, null, null, COMMITTEE_NAME || ' [' || CMTE_ID || ']', COMMITTEE_TYPE,
    round(cb/1e6,2), round(r/1e6,2), round(d/1e6,2), round(cc/1e6,2), round(gap/1e6,2), round(chain_gap/1e6,2), ce
  from j order by abs(gap) desc limit 25)
order by k, cyc;
