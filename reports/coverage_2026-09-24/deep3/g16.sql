-- g16: deep pass 3, 2026-09-24. Python door, QUERY_TAG deep3-2026-09-24. Read-only: SELECT/WITH only.
-- Tables: POLITICS__CA_LOBBY_COVER, POLITICS__FED_MEDSL_SENATE_RETURNS, POLITICS__CA_LOBBY_COVER2,
--         POLITICS__TX_LOBBY_SUBJECT_MATTER, POLITICS__FED_FEC_PAC_SUMMARY.
-- Every statement run is below, in order, with its runtime.

-- ===== connection: b1.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q01_ca_cover_shape] (0.8s)
-- CA cover: rows vs filings vs versions by form and entity; junk dates; blank firm/activity
select FORM_TYPE, ENTITY_CD, count(*) n, count(distinct FILING_ID) n_filings,
  count(distinct FILING_ID||'-'||AMEND_ID) n_versions, sum(iff(AMEND_ID<>'0',1,0)) n_amend_rows,
  count(distinct FILER_ID) n_filers,
  sum(iff(RPT_DATE is null or year(RPT_DATE) not between 1999 and 2026,1,0)) bad_rpt,
  sum(iff(FROM_DATE is null or year(FROM_DATE) not between 1999 and 2026,1,0)) bad_from,
  min(iff(year(FROM_DATE) between 1999 and 2026, FROM_DATE, null)) min_from,
  max(iff(year(FROM_DATE) between 1999 and 2026, FROM_DATE, null)) max_from,
  sum(iff(nullif(trim(FIRM_NAME),'') is null,1,0)) blank_firm,
  sum(iff(nullif(trim(LOBBYING_ACTIVITY),'') is null,1,0)) blank_act,
  count(distinct _SOURCE_URL) n_urls
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER
group by 1,2 order by n desc;

-- [q02_ca_cover_by_year] (0.5s)
-- CA cover per filing (all versions folded): by period year and form, filings, filers, share amended, lag from period end to first report date
with f as (
  select FILING_ID, any_value(FORM_TYPE) ft, any_value(FILER_ID) filer, min(FROM_DATE) fd, max(THRU_DATE) td,
         max(try_to_number(AMEND_ID)) max_am, min(iff(AMEND_ID='0', RPT_DATE, null)) rpt0, count(*) nver
  from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER group by 1)
select year(fd) y, ft, count(*) filings, count(distinct filer) filers, sum(iff(max_am>0,1,0)) amended,
  round(avg(iff(max_am>0,1,0)),3) amend_rate, sum(nver) versions,
  median(datediff(day, td, rpt0)) med_lag, sum(iff(datediff(day, td, rpt0) > 60,1,0)) late60,
  sum(iff(rpt0 is null,1,0)) no_v0
from f where year(fd) between 1999 and 2026
group by 1,2 order by 2,1;

-- [q03_ca_cover2_shape] (1.5s)
-- CA cover2: listed people by entity code and form; ID fill; name variety; load runs
select ENTITY_CD, FORM_TYPE, count(*) n, count(distinct FILING_ID) n_filings,
  count(distinct FILING_ID||'-'||AMEND_ID) n_versions,
  count(distinct ENTITY_ID) n_ids, sum(iff(nullif(trim(ENTITY_ID),'') is null or trim(ENTITY_ID)='0',1,0)) blank_id,
  count(distinct upper(trim(ENTY_NAML))||','||upper(trim(ENTY_NAMF))) n_names,
  count(distinct _SOURCE_RUN_ID) n_runs,
  count(*) - count(distinct FILING_ID||'-'||AMEND_ID||'-'||coalesce(LINE_ITEM,'')||'-'||coalesce(ENTITY_CD,'')) dup_lines
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER2
group by 1,2 order by n desc;

-- [q04_ca_cover2_land_by_year] (0.7s)
-- CA cover2 -> cover on FILING_ID + AMEND_ID: land rate, and which period years the listed names cover
with c as (select FILING_ID, AMEND_ID, min(FROM_DATE) fd, any_value(FORM_TYPE) ft
           from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER group by 1,2)
select iff(c.FILING_ID is null, null, iff(year(c.fd) between 1999 and 2026, year(c.fd), -1)) y,
  count(*) n2, count(distinct c2.FILING_ID) filings2, sum(iff(c.FILING_ID is not null,1,0)) landed,
  listagg(distinct c.ft, ',') forms
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER2 c2
left join c on c2.FILING_ID = c.FILING_ID and c2.AMEND_ID = c.AMEND_ID
group by 1 order by 1;

-- [q05_tx_subject_shape] (0.8s)
-- TX subject lines by year: reports, filers, subjects, corrected, duplicates, typed descriptions, load runs
select APPLICABLEYEAR, count(*) n, count(distinct REPORT_ID) n_reports, count(distinct FILER_ID) n_filers,
  count(distinct SUBJECT_MATTER_ID) n_line_ids, count(distinct SUBJECTMATTERCODEVALUE) n_subjects,
  sum(iff(FORMTYPECD='CORLOBBYACT',1,0)) n_corr,
  count(*) - count(distinct REPORT_ID||'-'||SUBJECTMATTERCD) dup_report_subject,
  sum(iff(nullif(trim(SUBJECTMATTERDESCR),'') is not null,1,0)) n_descr,
  min(PERIODSTARTDT) min_ps, max(PERIODSTARTDT) max_ps, count(distinct _SOURCE_RUN_ID) n_runs,
  listagg(distinct LOBBYFORMTYPE, ',') forms
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER
group by 1 order by 1;

-- [q06_tx_cover_vs_subject_by_year] (0.6s)
-- TX: of all cover reports per year, how many carry any subject line (coverage check before any trend)
with s as (select REPORT_ID::string rid, count(*) nsub from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER group by 1),
cv as (select REPORT_INFO_IDENT::string rid, APPLICABLE_YEAR y, REPORT_TYPE_CD rt, FILER_IDENT fid from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER)
select cv.y, count(*) reports, count(distinct cv.fid) filers, sum(iff(s.rid is not null,1,0)) rep_with_subj,
  count(distinct iff(s.rid is not null, cv.fid, null)) filers_with_subj,
  sum(iff(cv.rt ilike '%ANNUAL%',1,0)) annual_reports, sum(iff(cv.rt ilike '%ANNUAL%' and s.rid is not null,1,0)) annual_with_subj
from cv left join s on cv.rid = s.rid
group by 1 order by 1;

-- [q07_tx_subject_list] (0.5s)
-- TX subject codes: rows, filers, years
select SUBJECTMATTERCD, SUBJECTMATTERCODEVALUE, count(*) n, count(distinct FILER_ID) filers, count(distinct REPORT_ID) reports,
  min(APPLICABLEYEAR) y0, max(APPLICABLEYEAR) y1
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER
group by 1,2 order by n desc;

-- [q08_medsl_shape_by_year] (0.5s)
-- Senate returns by year: races (state+stage), rows, stages, races where several TOTAL_VOTES values sit under one key, sum-vs-total mismatch, flags
with r as (
  select ELECTION_YEAR y, STATE_ABBR s, upper(STAGE) st, count(*) n, count(distinct TOTAL_VOTES) ntv, sum(CANDIDATE_VOTES) cv,
    max(TOTAL_VOTES) tv, sum(iff(IS_WRITEIN,1,0)) wi, sum(iff(IS_SPECIAL_ELECTION,1,0)) sp, max(VOTE_SHARE) top_share,
    sum(iff(CANDIDATE_NAME is null or upper(CANDIDATE_NAME) in ('NA','','BLANK VOTE','SCATTERING','OTHER','WRITEIN','WRITE-IN'),1,0)) junk_names,
    listagg(distinct upper(VOTE_MODE), ',') vm
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS group by 1,2,3)
select y, count(*) race_keys, count(distinct s) states, sum(n) rows_, listagg(distinct st, ',') stages,
  sum(iff(ntv>1,1,0)) multi_total_keys, sum(iff(abs(cv-tv) > greatest(10, 0.01*tv),1,0)) sum_mismatch,
  sum(sp) special_rows, sum(wi) writein_rows, sum(iff(top_share >= 0.99,1,0)) one_cand_races, sum(junk_names) junk_name_rows,
  listagg(distinct vm, '|') modes
from r group by 1 order by 1;

-- [q09_medsl_multi_race_keys] (0.4s)
-- State-years where one state+year+stage holds more than one TOTAL_VOTES value: two races under one key?
with k as (select ELECTION_YEAR y, STATE_ABBR s, upper(STAGE) st from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS
           group by 1,2,3 having count(distinct TOTAL_VOTES) > 1)
select t.ELECTION_YEAR, t.STATE_ABBR, upper(t.STAGE) st, t.TOTAL_VOTES, count(*) n, sum(t.CANDIDATE_VOTES) cv,
  max_by(t.CANDIDATE_NAME, t.CANDIDATE_VOTES) top_cand, max(t.VOTE_SHARE) top_share, any_value(t.IS_SPECIAL_ELECTION) special
from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS t
join k on t.ELECTION_YEAR = k.y and t.STATE_ABBR = k.s and upper(t.STAGE) = k.st
group by 1,2,3,4 order by 1 desc, 2, 4 desc
limit 120;

-- [q10_pac_shape_by_cycle] (0.4s)
-- FEC PAC summary by cycle (from coverage end date): rows, committees, repeat rows, blank money, totals, load runs
with p as (select *, iff(COVERAGE_END_DATE is null, null, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2)) cyc
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY)
select cyc, count(*) n, count(distinct CMTE_ID) cmtes, count(*) - count(distinct CMTE_ID) repeat_rows,
  sum(iff(TOTAL_RECEIPTS is null,1,0)) null_rcpt, round(sum(TOTAL_RECEIPTS)/1e9,2) rcpt_b, round(sum(TOTAL_DISBURSEMENTS)/1e9,2) disb_b,
  min(COVERAGE_END_DATE) d0, max(COVERAGE_END_DATE) d1, count(distinct _SOURCE_RUN_ID) runs,
  listagg(distinct COMMITTEE_TYPE, ',') types,
  sum(iff(COMMITTEE_NAME is null,1,0)) null_name
from p group by 1 order by 1;

-- [q11_pac_cash_identity_by_cycle] (0.2s)
-- Does cash begin + receipts - disbursements = cash close? By cycle, how often and how far off
with p as (select *, iff(COVERAGE_END_DATE is null, null, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2)) cyc,
             CASH_BEGINNING_OF_PERIOD + TOTAL_RECEIPTS - TOTAL_DISBURSEMENTS - CASH_CLOSE_OF_PERIOD gap
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY)
select cyc, count(*) n, count(gap) n_all4, sum(iff(abs(gap) < 1,1,0)) exact, sum(iff(abs(gap) >= 1 and abs(gap) < 1000,1,0)) under1k,
  sum(iff(abs(gap) >= 1000 and abs(gap) < 100000,1,0)) k1_100k, sum(iff(abs(gap) >= 100000,1,0)) over100k,
  sum(iff(gap >= 100000,1,0)) pos_over100k, sum(iff(gap <= -100000,1,0)) neg_over100k,
  round(sum(abs(gap))/1e6,1) abs_gap_m, round(sum(TOTAL_RECEIPTS)/1e6,1) rcpt_m
from p group by 1 order by 1;

-- [q12_pac_top_receipts] (0.3s)
-- Top 20 committee-cycles by receipts, with type and designation; conduits check
select CMTE_ID, COMMITTEE_NAME, COMMITTEE_TYPE, COMMITTEE_DESIGNATION, COVERAGE_END_DATE,
  round(TOTAL_RECEIPTS/1e6,1) rcpt_m, round(TOTAL_DISBURSEMENTS/1e6,1) disb_m, round(INDIVIDUAL_CONTRIBUTIONS/1e6,1) indiv_m,
  round(CONTRIBUTIONS_TO_OTHER_COMMITTEES/1e6,1) to_cmtes_m, round(TRANSFERS_TO_AFFILIATES/1e6,1) to_aff_m,
  round(CASH_BEGINNING_OF_PERIOD/1e6,1) cb_m, round(CASH_CLOSE_OF_PERIOD/1e6,1) cc_m
from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
order by TOTAL_RECEIPTS desc nulls last limit 20;

-- ===== connection: b2.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q13_ca_amend_rate_peer] (0.7s)
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

-- [q14_ca_amend_waves_by_filed_year] (0.7s)
-- CA amendment versions by the year they were filed (RPT_DATE), per form: how many, how many filers, and how much the top filer carries
with a as (
  select year(RPT_DATE) y, FORM_TYPE ft, FILER_ID, any_value(FILER_NAML) nm, count(*) v
  from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER
  where AMEND_ID <> '0' and year(RPT_DATE) between 1999 and 2026 group by 1,2,3)
select y, ft, sum(v) versions, count(*) filers, max(v) top_v, max_by(nm, v) top_filer, round(max(v)/sum(v),3) top_share, median(v) med_v
from a group by 1,2 order by 2,1;

-- [q15_ca_2020_amend_spike_filers] (0.5s)
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

-- [q16_ca_topics_by_year] (0.8s)
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

-- [q17_ca_cover2_people] (1.3s)
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

-- [q18_tx_subject_filers_by_year] (0.8s)
-- TX: distinct lobbyists per subject per year, plus each year's total, for within-sample shares
select APPLICABLEYEAR y, SUBJECTMATTERCODEVALUE subj, count(distinct FILER_ID) filers, count(distinct REPORT_ID) reports
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER where APPLICABLEYEAR between '2002' and '2026' group by 1,2
union all
select APPLICABLEYEAR, '__ALL__', count(distinct FILER_ID), count(distinct REPORT_ID)
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER where APPLICABLEYEAR between '2002' and '2026' group by 1
order by 1, 3 desc;

-- [q19_tx_boxes_per_report] (0.3s)
-- TX: subjects ticked per report by year; reports that tick 40+ or 80+ boxes
with r as (select APPLICABLEYEAR y, REPORT_ID, any_value(REPORTTYPECD) rt, count(*) nsub
           from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER group by 1,2)
select y, count(*) reports, median(nsub) med, percentile_cont(0.9) within group (order by nsub) p90, max(nsub) mx,
  sum(iff(nsub >= 40,1,0)) r40, sum(iff(nsub >= 80,1,0)) r80, sum(iff(nsub >= 40, nsub, 0)) lines_in_40, sum(nsub) lines,
  sum(iff(rt = 'LOBBYACTANNUAL',1,0)) annual
from r group by 1 order by 1;

-- [q20_medsl_flags] (0.4s)
-- Senate returns: are the write-in and special flags ever true? Stage labels, party labels, FIPS shape
select IS_WRITEIN, IS_SPECIAL_ELECTION, upper(STAGE) st, count(*) n,
  sum(iff(CANDIDATE_NAME ilike '%write%' or CANDIDATE_NAME ilike '%scatter%',1,0)) writein_names,
  count(distinct ELECTION_YEAR) yrs, listagg(distinct PARTY_SIMPLIFIED, ',') parties,
  sum(iff(try_to_number(STATE_FIPS) is null,1,0)) bad_fips, min(len(STATE_FIPS)) min_fips_len,
  sum(iff(VOTE_SHARE is null,1,0)) null_share, sum(iff(abs(VOTE_SHARE - CANDIDATE_VOTES/nullif(TOTAL_VOTES,0)) > 0.001,1,0)) share_off
from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS
group by 1,2,3 order by n desc;

-- [q21_medsl_senate_vs_president] (0.7s)
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

-- [q22_pac_undated_rows] (0.5s)
-- FEC PAC summary: the rows with no coverage date. What types, do they carry any money, do the same IDs show up dated?
with d as (select distinct CMTE_ID from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY where COVERAGE_END_DATE is not null)
select t.COMMITTEE_TYPE, count(*) n, sum(iff(d.CMTE_ID is not null,1,0)) also_dated,
  sum(iff(t.TOTAL_DISBURSEMENTS is null and t.CASH_CLOSE_OF_PERIOD is null and t.DEBTS_OWED_BY is null and t.CASH_BEGINNING_OF_PERIOD is null,1,0)) all_null,
  min(t.COMMITTEE_NAME) ex1, max(t.COMMITTEE_NAME) ex2, listagg(distinct t.FILING_FREQUENCY, ',') freqs, listagg(distinct t.COMMITTEE_DESIGNATION, ',') desigs,
  min(t.CMTE_ID) id_lo, max(t.CMTE_ID) id_hi
from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY t left join d on t.CMTE_ID = d.CMTE_ID
where t.COVERAGE_END_DATE is null group by 1 order by n desc;

-- [q23_pac_repeat_rows] (0.3s)
-- FEC PAC summary: committees with two rows in one cycle. Duplicate load or two coverage periods?
with p as (select *, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2) cyc
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY where COVERAGE_END_DATE is not null)
select cyc, CMTE_ID, COMMITTEE_NAME, COMMITTEE_TYPE, COVERAGE_END_DATE, TOTAL_RECEIPTS, TOTAL_DISBURSEMENTS, CASH_BEGINNING_OF_PERIOD, CASH_CLOSE_OF_PERIOD
from p qualify count(*) over (partition by CMTE_ID, cyc) > 1
order by cyc, CMTE_ID, COVERAGE_END_DATE limit 60;

-- [q24_pac_gap_by_type] (0.2s)
-- FEC PAC summary peer check: how often the cash math balances, by committee type and cycle
with p as (select *, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2) cyc,
             CASH_BEGINNING_OF_PERIOD + TOTAL_RECEIPTS - TOTAL_DISBURSEMENTS - CASH_CLOSE_OF_PERIOD gap
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY where COVERAGE_END_DATE is not null)
select cyc, COMMITTEE_TYPE, count(*) n, sum(iff(abs(gap) < 1,1,0)) exact, round(avg(iff(abs(gap) < 1,1,0)),3) exact_rate,
  sum(iff(abs(gap) >= 100000,1,0)) over100k, round(sum(abs(gap))/1e6,1) abs_gap_m, round(sum(TOTAL_RECEIPTS)/1e6,1) rcpt_m,
  sum(iff(month(COVERAGE_END_DATE) <> 12 or day(COVERAGE_END_DATE) <> 31,1,0)) not_yearend,
  sum(iff(abs(gap) >= 1 and (month(COVERAGE_END_DATE) <> 12 or day(COVERAGE_END_DATE) <> 31),1,0)) gap_and_not_yearend
from p where cyc between 2018 and 2024 group by 1,2 order by 1,2;

-- [q25_pac_chain_and_top_gaps] (0.3s)
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

-- ===== connection: b3.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q26_ca_ai_employers_eyeball] (0.1s, ERROR)
-- CA employer reports naming AI, 2019-2026, one row per employer: quarters per year, how it matched, and a text sample to eyeball
with f as (
  select FILING_ID, max_by(LOBBYING_ACTIVITY, try_to_number(AMEND_ID)) act, any_value(FILER_ID) filer,
         max_by(FILER_NAML, try_to_number(AMEND_ID)) nm, min(FROM_DATE) fd
  from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER where FORM_TYPE = 'F635' group by 1),
m as (
  select f.*, iff(act ilike '%artificial intelligence%',1,0) phrase,
    iff(regexp_instr(act, '(^|[^A-Za-z])AI([^A-Za-z]|$)') > 0,1,0) rx,
    iff(act ilike '%SB 1047%' or act ilike '%SB1047%',1,0) sb1047,
    iff(act ilike '%automated decision%',1,0) adt
  from f where year(fd) between 2019 and 2026),
h as (select * from m where phrase + rx + sb1047 + adt > 0)
select filer, max(nm) nm,
  sum(iff(year(fd)=2019,1,0)) q19, sum(iff(year(fd)=2020,1,0)) q20, sum(iff(year(fd)=2021,1,0)) q21, sum(iff(year(fd)=2022,1,0)) q22,
  sum(iff(year(fd)=2023,1,0)) q23, sum(iff(year(fd)=2024,1,0)) q24, sum(iff(year(fd)=2025,1,0)) q25, sum(iff(year(fd)=2026,1,0)) q26,
  sum(phrase) n_phrase, sum(iff(rx=1 and phrase=0 and sb1047=0 and adt=0,1,0)) n_rx_only, sum(sb1047) n_sb1047, sum(adt) n_adt,
  min(fd) first_q,
  max_by(coalesce(regexp_substr(act, '.{0,70}[Aa]rtificial [Ii]ntelligence.{0,40}'), regexp_substr(act, '.{0,70}SB ?1047.{0,40}'),
                  regexp_substr(act, '.{0,70}(^|[^A-Za-z])AI([^A-Za-z]|$).{0,40}'), regexp_substr(act, '.{0,70}[Aa]utomated [Dd]ecision.{0,40}')), fd) sample
from h group by 1 order by q24 + q25 + q26 desc, first_q limit 250;

-- [q27_pac_party_and_big_gaps] (0.4s)
-- FEC PAC summary: big party committees in every cycle, plus any PAC or party row whose cash math is off by $1M+; prior-row close for the chain
with p as (
  select CMTE_ID, COMMITTEE_NAME, COMMITTEE_TYPE, COMMITTEE_DESIGNATION, COVERAGE_END_DATE,
    round(CASH_BEGINNING_OF_PERIOD/1e6,2) cb_m, round(TOTAL_RECEIPTS/1e6,2) r_m, round(TOTAL_DISBURSEMENTS/1e6,2) d_m, round(CASH_CLOSE_OF_PERIOD/1e6,2) cc_m,
    round((CASH_BEGINNING_OF_PERIOD + TOTAL_RECEIPTS - TOTAL_DISBURSEMENTS - CASH_CLOSE_OF_PERIOD)/1e6,2) gap_m,
    round(lag(CASH_CLOSE_OF_PERIOD) over (partition by CMTE_ID order by COVERAGE_END_DATE)/1e6,2) prev_cc_m,
    round(TRANSFERS_FROM_AFFILIATES/1e6,2) tfa_m, round(TRANSFERS_TO_AFFILIATES/1e6,2) tta_m, round(NONFEDERAL_TRANSFERS_RECEIVED/1e6,2) nonfed_m,
    round(DEBTS_OWED_BY/1e6,2) debt_m
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
  where COVERAGE_END_DATE is not null and COMMITTEE_TYPE in ('Y','N','O','Q','V','W'))
select * from p
where abs(gap_m) >= 1
   or CMTE_ID in (select CMTE_ID from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY where COMMITTEE_TYPE = 'Y' group by 1 having max(TOTAL_RECEIPTS) > 100e6)
order by CMTE_ID, COVERAGE_END_DATE;

-- [q28_medsl_pres_years_and_odd_rows] (0.4s)
-- MEDSL: which years the president table holds and how states are coded; plus the odd Senate rows behind the roll-off outliers
select 'pres' k, ELECTION_YEAR::string y, count(*)::string a, count(distinct STATE_ABBR)::string b,
  min(STATE_ABBR) || '..' || max(STATE_ABBR) c, sum(CANDIDATE_VOTES)::string d, max(TOTAL_VOTES)::string e, null::string f
from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_PRESIDENT_RETURNS group by ELECTION_YEAR
union all
select 'sen', ELECTION_YEAR::string, STATE_ABBR || ' ' || STAGE, CANDIDATE_NAME, PARTY_SIMPLIFIED, CANDIDATE_VOTES::string, TOTAL_VOTES::string, VOTE_SHARE::string
from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS
where (ELECTION_YEAR = 2000 and STATE_ABBR = 'NE') or (ELECTION_YEAR in (1984, 1992, 1980) and STATE_ABBR = 'LA')
   or (ELECTION_YEAR in (1992, 2008) and STATE_ABBR = 'GA') or (ELECTION_YEAR = 2004 and STATE_ABBR = 'CT')
order by 1, 2, 3, 6 desc;

-- [q29_tx_util_energy_no_boxtickers] (0.4s)
-- TX: lobbyists listing Utilities / Energy / Disaster by year, with reports that tick 40+ subjects removed from both counts
with r as (select REPORT_ID, count(*) nsub from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER group by 1),
x as (select t.APPLICABLEYEAR y, t.FILER_ID, t.SUBJECTMATTERCODEVALUE s
      from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER t join r on t.REPORT_ID = r.REPORT_ID
      where r.nsub < 40 and t.APPLICABLEYEAR between '2011' and '2026')
select y, count(distinct FILER_ID) filers,
  count(distinct iff(s = 'Utilities', FILER_ID, null)) util, count(distinct iff(s = 'Energy', FILER_ID, null)) energy,
  count(distinct iff(s in ('Utilities','Energy'), FILER_ID, null)) util_or_energy,
  count(distinct iff(s = 'Disaster Preparedness And Relief', FILER_ID, null)) disaster,
  count(distinct iff(s = 'Law Enforcement', FILER_ID, null)) law_enf, count(distinct iff(s = 'Gambling', FILER_ID, null)) gambling
from x group by 1 order by 1;

-- ===== totals: 29 SELECT/WITH statements (q26 failed to compile: SAMPLE is a reserved word) + 6 session-setup = 35 of 35.
-- q26's eyeball was redone OFF the warehouse, on the local raw CAL-ACCESS download
--   library-onboarding/raw_downloads/ca_lobby/CVR_LOBBY_DISCLOSURE_CD.TSV (2026-08-05), by g16/ai_eyeball.py.
--   Same rules as q16. It reproduced q16's AI employer counts (2024: 94 both; 2025: 58 raw vs 59 warehouse).
