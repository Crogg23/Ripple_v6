-- [q01_ca_cover_shape]
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

-- [q02_ca_cover_by_year]
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

-- [q03_ca_cover2_shape]
-- CA cover2: listed people by entity code and form; ID fill; name variety; load runs
select ENTITY_CD, FORM_TYPE, count(*) n, count(distinct FILING_ID) n_filings,
  count(distinct FILING_ID||'-'||AMEND_ID) n_versions,
  count(distinct ENTITY_ID) n_ids, sum(iff(nullif(trim(ENTITY_ID),'') is null or trim(ENTITY_ID)='0',1,0)) blank_id,
  count(distinct upper(trim(ENTY_NAML))||','||upper(trim(ENTY_NAMF))) n_names,
  count(distinct _SOURCE_RUN_ID) n_runs,
  count(*) - count(distinct FILING_ID||'-'||AMEND_ID||'-'||coalesce(LINE_ITEM,'')||'-'||coalesce(ENTITY_CD,'')) dup_lines
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER2
group by 1,2 order by n desc;

-- [q04_ca_cover2_land_by_year]
-- CA cover2 -> cover on FILING_ID + AMEND_ID: land rate, and which period years the listed names cover
with c as (select FILING_ID, AMEND_ID, min(FROM_DATE) fd, any_value(FORM_TYPE) ft
           from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER group by 1,2)
select iff(c.FILING_ID is null, null, iff(year(c.fd) between 1999 and 2026, year(c.fd), -1)) y,
  count(*) n2, count(distinct c2.FILING_ID) filings2, sum(iff(c.FILING_ID is not null,1,0)) landed,
  listagg(distinct c.ft, ',') forms
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER2 c2
left join c on c2.FILING_ID = c.FILING_ID and c2.AMEND_ID = c.AMEND_ID
group by 1 order by 1;

-- [q05_tx_subject_shape]
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

-- [q06_tx_cover_vs_subject_by_year]
-- TX: of all cover reports per year, how many carry any subject line (coverage check before any trend)
with s as (select REPORT_ID::string rid, count(*) nsub from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER group by 1),
cv as (select REPORT_INFO_IDENT::string rid, APPLICABLE_YEAR y, REPORT_TYPE_CD rt, FILER_IDENT fid from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER)
select cv.y, count(*) reports, count(distinct cv.fid) filers, sum(iff(s.rid is not null,1,0)) rep_with_subj,
  count(distinct iff(s.rid is not null, cv.fid, null)) filers_with_subj,
  sum(iff(cv.rt ilike '%ANNUAL%',1,0)) annual_reports, sum(iff(cv.rt ilike '%ANNUAL%' and s.rid is not null,1,0)) annual_with_subj
from cv left join s on cv.rid = s.rid
group by 1 order by 1;

-- [q07_tx_subject_list]
-- TX subject codes: rows, filers, years
select SUBJECTMATTERCD, SUBJECTMATTERCODEVALUE, count(*) n, count(distinct FILER_ID) filers, count(distinct REPORT_ID) reports,
  min(APPLICABLEYEAR) y0, max(APPLICABLEYEAR) y1
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER
group by 1,2 order by n desc;

-- [q08_medsl_shape_by_year]
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

-- [q09_medsl_multi_race_keys]
-- State-years where one state+year+stage holds more than one TOTAL_VOTES value: two races under one key?
with k as (select ELECTION_YEAR y, STATE_ABBR s, upper(STAGE) st from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS
           group by 1,2,3 having count(distinct TOTAL_VOTES) > 1)
select t.ELECTION_YEAR, t.STATE_ABBR, upper(t.STAGE) st, t.TOTAL_VOTES, count(*) n, sum(t.CANDIDATE_VOTES) cv,
  max_by(t.CANDIDATE_NAME, t.CANDIDATE_VOTES) top_cand, max(t.VOTE_SHARE) top_share, any_value(t.IS_SPECIAL_ELECTION) special
from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_SENATE_RETURNS t
join k on t.ELECTION_YEAR = k.y and t.STATE_ABBR = k.s and upper(t.STAGE) = k.st
group by 1,2,3,4 order by 1 desc, 2, 4 desc
limit 120;

-- [q10_pac_shape_by_cycle]
-- FEC PAC summary by cycle (from coverage end date): rows, committees, repeat rows, blank money, totals, load runs
with p as (select *, iff(COVERAGE_END_DATE is null, null, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2)) cyc
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY)
select cyc, count(*) n, count(distinct CMTE_ID) cmtes, count(*) - count(distinct CMTE_ID) repeat_rows,
  sum(iff(TOTAL_RECEIPTS is null,1,0)) null_rcpt, round(sum(TOTAL_RECEIPTS)/1e9,2) rcpt_b, round(sum(TOTAL_DISBURSEMENTS)/1e9,2) disb_b,
  min(COVERAGE_END_DATE) d0, max(COVERAGE_END_DATE) d1, count(distinct _SOURCE_RUN_ID) runs,
  listagg(distinct COMMITTEE_TYPE, ',') types,
  sum(iff(COMMITTEE_NAME is null,1,0)) null_name
from p group by 1 order by 1;

-- [q11_pac_cash_identity_by_cycle]
-- Does cash begin + receipts - disbursements = cash close? By cycle, how often and how far off
with p as (select *, iff(COVERAGE_END_DATE is null, null, year(COVERAGE_END_DATE) + mod(year(COVERAGE_END_DATE),2)) cyc,
             CASH_BEGINNING_OF_PERIOD + TOTAL_RECEIPTS - TOTAL_DISBURSEMENTS - CASH_CLOSE_OF_PERIOD gap
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY)
select cyc, count(*) n, count(gap) n_all4, sum(iff(abs(gap) < 1,1,0)) exact, sum(iff(abs(gap) >= 1 and abs(gap) < 1000,1,0)) under1k,
  sum(iff(abs(gap) >= 1000 and abs(gap) < 100000,1,0)) k1_100k, sum(iff(abs(gap) >= 100000,1,0)) over100k,
  sum(iff(gap >= 100000,1,0)) pos_over100k, sum(iff(gap <= -100000,1,0)) neg_over100k,
  round(sum(abs(gap))/1e6,1) abs_gap_m, round(sum(TOTAL_RECEIPTS)/1e6,1) rcpt_m
from p group by 1 order by 1;

-- [q12_pac_top_receipts]
-- Top 20 committee-cycles by receipts, with type and designation; conduits check
select CMTE_ID, COMMITTEE_NAME, COMMITTEE_TYPE, COMMITTEE_DESIGNATION, COVERAGE_END_DATE,
  round(TOTAL_RECEIPTS/1e6,1) rcpt_m, round(TOTAL_DISBURSEMENTS/1e6,1) disb_m, round(INDIVIDUAL_CONTRIBUTIONS/1e6,1) indiv_m,
  round(CONTRIBUTIONS_TO_OTHER_COMMITTEES/1e6,1) to_cmtes_m, round(TRANSFERS_TO_AFFILIATES/1e6,1) to_aff_m,
  round(CASH_BEGINNING_OF_PERIOD/1e6,1) cb_m, round(CASH_CLOSE_OF_PERIOD/1e6,1) cc_m
from LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY
order by TOTAL_RECEIPTS desc nulls last limit 20;
