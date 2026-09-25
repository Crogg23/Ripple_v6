-- [q26_ca_ai_employers_eyeball]
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

-- [q27_pac_party_and_big_gaps]
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

-- [q28_medsl_pres_years_and_odd_rows]
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

-- [q29_tx_util_energy_no_boxtickers]
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
