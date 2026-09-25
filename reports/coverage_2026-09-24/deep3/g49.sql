-- deep3 / g49, 2026-09-24. Every statement this group ran, in order, as the runner (g49/run.py) sent it.
-- Door: Python (connect/db.py). Read-only: the runner refuses anything but SELECT / WITH.
-- 33 SELECT/WITH statements. Statement 6 (q06) failed to compile ("sample" is a reserved word) and was rerun as q06b.
-- Door overhead, not counted above: each of 8 connections opened with
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Raw results: g49/qNN.json.

-- [q01] statement 1
-- FJC appeals: shape by yearly snapshot (TAPE_YEAR). Is one appeal one row, or repeated across snapshots?
select TAPE_YEAR, count(*) n_rows,
  count(distinct CIRCUIT||'|'||DOCKET||'|'||REOPEN) n_appeals,
  count(distinct APPEAL_RECORD_ID) n_recid,
  count(JUDGMENT_DATE) n_judgment,
  min(try_to_date(DOCKET_DATE::string)) min_dd, max(try_to_date(DOCKET_DATE::string)) max_dd,
  max(try_to_date(JUDGMENT_DATE::string)) max_jd,
  sum(iff(FILING_FEE_STATUS='FP',1,0)) n_fp,
  count(distinct _SOURCE_RUN_ID) n_runs
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1 order by 1;

-- [q02] statement 2
-- FJC appeals: the dockets with the most rows (glance saw 1116673 at 1.6K rows). Duplicate load, or mass appeal?
select CIRCUIT, DOCKET, count(*) n, count(distinct REOPEN) n_reopen, count(distinct TAPE_YEAR) n_tape,
  count(distinct APPEAL_RECORD_ID) n_recid, count(distinct APPELLANT) n_appellant_names,
  min(APPELLANT) a_min, max(APPELLANT) a_max, max(APPELLEE) ee_max,
  min(DOCKET_DATE) dd_min, max(DOCKET_DATE) dd_max, mode(NATURE_OF_SUIT) nos, mode(APPEAL_TYPE) atype, mode(OUTCOME) outcome
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1,2 order by n desc limit 15;

-- [q03] statement 3
-- FJC appeals: decode APPEAL_TYPE from what rides with it (offense code, agency code, suit code, US side, fee waiver)
select APPEAL_TYPE, count(*) n,
  sum(iff(OFFENSE::string<>'-9',1,0)) has_offense, sum(iff(AGENCY::string<>'-9',1,0)) has_agency,
  sum(iff(NATURE_OF_SUIT::string<>'-9',1,0)) has_nos,
  sum(iff(US_APPELLANT::string='1',1,0)) us_appellant, sum(iff(US_APPELLEE::string='1',1,0)) us_appellee,
  sum(iff(FILING_FEE_STATUS='FP',1,0)) fp, sum(iff(PRO_SE_FILED::string<>'0' and PRO_SE_FILED::string<>'-8',1,0)) pro_se_any,
  mode(APPELLEE) top_appellee, mode(NATURE_OF_SUIT) top_nos, mode(AGENCY) top_agency, mode(ORIGINATING_PROCEEDING) top_orig
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
group by 1 order by n desc;

-- [q04] statement 4
-- FJC appeals: every coded outcome-type column, value counts in one pass
select 'OUTCOME' col, OUTCOME::string val, count(*) n from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'PROCEDURAL_TERMINATION', PROCEDURAL_TERMINATION::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'METHOD', METHOD::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'PUBLICATION_STATUS', PUBLICATION_STATUS::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'TERMINATION_TYPE', TERMINATION_TYPE::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'PRO_SE_FILED', PRO_SE_FILED::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'AGENCY', AGENCY::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
union all select 'DISPOSITION', DISPOSITION::string, count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE group by 1,2
order by 1, 3 desc;

-- [q05] statement 5
-- Warehouse: every CourtListener table and its row count. Is there an OPINIONS table to name a parenthetical's opinion?
select table_schema, table_name, row_count, last_altered
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where table_name ilike '%COURTLISTENER%' order by 2;

-- [q06] statement 6
-- Parentheticals: the 20 most-described opinion IDs, tried against OPINION_CLUSTERS.ID. Do the names make sense?
with p as (select DESCRIBED_OPINION_ID::string id, count(*) n, count(distinct DESCRIBING_OPINION_ID) n_citing,
             any_value(left(TEXT,160)) sample
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_PARENTHETICALS group by 1 order by n desc limit 20)
select p.*, c.CASE_NAME, c.DATE_FILED, c.CITATION_COUNT
from p left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS c on c.ID::string = p.id
order by p.n desc;

-- [q07] statement 7
-- Parentheticals: whole-table shape. Duplicates, blank text, score spread, how many rows say overruled/abrogated
select count(*) n, count(distinct ID) n_id, count(distinct DESCRIBED_OPINION_ID) n_described,
  count(distinct DESCRIBING_OPINION_ID) n_describing, count(distinct GROUP_ID) n_groups,
  count(distinct DESCRIBED_OPINION_ID||'|'||DESCRIBING_OPINION_ID||'|'||TEXT) n_distinct_triples,
  sum(iff(TEXT is null or trim(TEXT)='',1,0)) blank_text, median(length(TEXT)) med_len,
  min(try_to_double(SCORE)) min_score, max(try_to_double(SCORE)) max_score, sum(iff(try_to_double(SCORE) is null,1,0)) score_not_num,
  sum(iff(TEXT ilike '%overrul%',1,0)) says_overrul, sum(iff(TEXT ilike '%abrogat%',1,0)) says_abrogat,
  min(ID) min_id, max(ID) max_id
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_PARENTHETICALS;

-- [q08] statement 8
-- Judge party ties: where the party label comes from (SOURCE a/o/b) by party; dates filled
select SOURCE, POLITICAL_PARTY, count(*) n, count(distinct PERSON_ID) people,
  count(DATE_START) has_start, count(DATE_END) has_end, min(DATE_CREATED) first_created, max(DATE_CREATED) last_created
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS
group by 1,2 order by n desc;

-- [q09] statement 9
-- Oral arguments: court x year, via DOCKET_ID -> DOCKETS.COURT_ID. Count, median length, transcript fill
with oa as (select DOCKET_ID::string did, DURATION, try_to_date(DATE_CREATED::string) dc, STT_STATUS,
              iff(STT_TRANSCRIPT is not null and length(STT_TRANSCRIPT) > 50, 1, 0) has_tx
            from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da
      from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select coalesce(d.COURT_ID,'(no docket)') court, year(coalesce(d.da, oa.dc)) yr, count(*) n,
  median(oa.DURATION) med_sec, sum(oa.has_tx) n_tx, sum(iff(d.da is null,1,0)) no_argued_date
from oa left join d on d.id = oa.did
group by 1,2 order by 1,2;

-- [q06b] statement 10
-- Parentheticals (rerun of q06; "sample" is a reserved word): top 20 described opinion IDs vs OPINION_CLUSTERS.ID
with p as (select DESCRIBED_OPINION_ID::string id, count(*) n, count(distinct DESCRIBING_OPINION_ID) n_citing,
             any_value(left(TEXT,160)) sample_text
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_PARENTHETICALS group by 1 order by n desc limit 20)
select p.*, c.CASE_NAME, c.DATE_FILED, c.CITATION_COUNT
from p left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS c on c.ID::string = p.id
order by p.n desc;

-- [q10] statement 11
-- FJC appeals: decode OUTCOME by appeal type, with DISPOSITION / METHOD / procedural-termination alongside (terminated tapes only)
select APPEAL_TYPE::string t, OUTCOME::string o, count(*) n,
  sum(iff(DISPOSITION::string='1',1,0)) d1, sum(iff(DISPOSITION::string='2',1,0)) d2,
  sum(iff(DISPOSITION::string='4',1,0)) d4, sum(iff(DISPOSITION::string='5',1,0)) d5,
  sum(iff(METHOD::string='1',1,0)) m1, sum(iff(METHOD::string='3',1,0)) m3, sum(iff(METHOD::string='4',1,0)) m4,
  sum(iff(PROCEDURAL_TERMINATION::string<>'-8',1,0)) proc_term, sum(iff(US_APPELLANT::string='1',1,0)) us_appellant
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
where TAPE_YEAR::string <> '2099' and APPEAL_TYPE::string in ('1','3','4','6','19','21','17')
group by 1,2 order by 1,3 desc;

-- [q11] statement 12
-- FJC appeals: appeals docketed per month, Oct 2022 - Mar 2026, by stream. One appeal = circuit+docket+reopen, counted once.
with a as (select distinct CIRCUIT, DOCKET, REOPEN,
             date_trunc('month', try_to_date(DOCKET_DATE::string)) m, NATURE_OF_SUIT::string nos, AGENCY::string ag,
             APPEAL_TYPE::string t, US_APPELLANT::string usa, US_APPELLEE::string use
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
           where try_to_date(DOCKET_DATE::string) >= '2022-10-01')
select m, count(*) all_appeals,
  sum(iff(nos='463',1,0)) alien_habeas, sum(iff(nos='463' and usa='1',1,0)) alien_habeas_us_appeals,
  sum(iff(ag='6',1,0)) agency6, sum(iff(t='3' and usa='1',1,0)) us_civil_appeals_by_us,
  sum(iff(t='3',1,0)) us_civil_all, sum(iff(t in ('14','15','16','17','18','19','20','21'),1,0)) criminal
from a group by 1 order by 1;

-- [q12] statement 13
-- Oral arguments: length distribution by year for the D.C. Circuit, the Supreme Court, and the other 12 federal appeals courts pooled
with oa as (select DOCKET_ID::string did, DURATION from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select case when d.COURT_ID in ('cadc','scotus') then d.COURT_ID when d.COURT_ID like 'ca%' then 'other_fed_circuits' else 'illinois' end grp,
  year(d.da) yr, count(*) n, percentile_cont(0.25) within group (order by DURATION) p25, median(DURATION) med,
  percentile_cont(0.75) within group (order by DURATION) p75, sum(iff(DURATION > 3600,1,0)) over_60m,
  sum(iff(DURATION > 5400,1,0)) over_90m, max(DURATION) mx, sum(iff(DURATION is null or DURATION <= 0,1,0)) bad_dur
from oa join d on d.id = oa.did
where year(d.da) >= 2012
group by 1,2 order by 1,2;

-- [q13] statement 14
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
group by 1 order by 1;

-- [q14] statement 15
-- FJC appeals, immigration-detention habeas (NATURE_OF_SUIT 463): by circuit, three periods, with the circuit's all-appeals denominator
with a as (select distinct CIRCUIT, DOCKET, REOPEN, try_to_date(DOCKET_DATE::string) dd, NATURE_OF_SUIT::string nos,
             US_APPELLANT::string usa, PRO_SE_FILED::string ps, DISTRICT_COURT::string dc
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
           where try_to_date(DOCKET_DATE::string) >= '2023-10-01')
select CIRCUIT,
  sum(iff(nos='463' and dd < '2024-10-01',1,0)) hab_fy24,
  sum(iff(nos='463' and dd >= '2024-10-01' and dd < '2025-10-01',1,0)) hab_fy25,
  sum(iff(nos='463' and dd >= '2025-10-01',1,0)) hab_oct25_mar26,
  sum(iff(nos='463' and dd >= '2025-10-01' and usa='1',1,0)) hab_oct25_mar26_us_appeals,
  sum(iff(nos='463' and dd >= '2025-10-01' and ps not in ('0','-8'),1,0)) hab_oct25_mar26_pro_se,
  count(distinct iff(nos='463' and dd >= '2025-10-01', dc, null)) hab_n_districts,
  sum(iff(dd >= '2025-10-01',1,0)) all_oct25_mar26,
  sum(iff(dd >= '2024-10-01' and dd < '2025-04-01',1,0)) all_oct24_mar25
from a group by 1 order by hab_oct25_mar26 desc;

-- [q15] statement 16
-- FJC appeals, 463 appeals docketed Oct 2025 - Mar 2026: which trial courts they came from, by month. Do 3-4 courts carry it?
with a as (select distinct CIRCUIT, DOCKET, REOPEN, try_to_date(DOCKET_DATE::string) dd, US_APPELLANT::string usa,
             DISTRICT_COURT::string dc, APPELLANT, APPELLEE, PRO_SE_FILED::string ps
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
           where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01')
select CIRCUIT, dc, count(*) n,
  sum(iff(month(dd)=10,1,0)) oct, sum(iff(month(dd)=11,1,0)) nov, sum(iff(month(dd)=12,1,0)) dec_,
  sum(iff(month(dd)=1,1,0)) jan, sum(iff(month(dd)=2,1,0)) feb, sum(iff(month(dd)=3,1,0)) mar,
  sum(iff(usa='1',1,0)) us_appellant, sum(iff(ps not in ('0','-8'),1,0)) pro_se,
  count(distinct APPELLANT) n_appellant_names, mode(APPELLANT) top_appellant, mode(APPELLEE) top_appellee
from a group by 1,2 order by n desc limit 25;

-- [q16] statement 17
-- FJC appeals: eyeball 16 detention-habeas appeals docketed January 2026, spread across circuits
select CIRCUIT, DOCKET, REOPEN, DOCKET_DATE, APPEAL_TYPE, US_APPELLANT, US_APPELLEE, APPELLANT, APPELLEE,
  DISTRICT_COURT, DISTRICT_OFFICE, DISTRICT_DOCKET, DISTRICT_DOCKET_DATE, APPEAL_DATE, PRO_SE_FILED, FILING_FEE_STATUS,
  TAPE_YEAR, OUTCOME, DISPOSITION, JUDGMENT_DATE
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) between '2026-01-01' and '2026-01-31'
qualify row_number() over (partition by CIRCUIT order by DOCKET) <= 2
order by CIRCUIT, DOCKET;

-- [q17] statement 18
-- JOIN: 463 appeals (Oct 2025 - Mar 2026) -> FJC civil trial-court case (district + office + docket). Land rate, and who won below, by who appealed.
-- Plus: 463 filings per month in the trial courts (the pipeline feeding the appeals). Civil cases repeat across tapes: keep one row per case.
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               try_to_date(FILE_DATE::string) fd, try_to_date(TERM_DATE::string) td, JUDGMENT::string j, DISPOSITION::string disp
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2023-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
ap as (select distinct CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, US_APPELLANT::string usa
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01')
select 'join' section, ap.usa k1, coalesce(civ.j,'(no match)') k2, coalesce(civ.disp,'') k3, count(*) n
from ap left join civ on civ.d = ap.d and civ.o = ap.o and civ.k = ap.k
group by 1,2,3,4
union all
select 'filings_by_month', to_char(date_trunc('month', fd),'YYYY-MM'), '', '', count(*) from civ group by 1,2,3,4
union all
select 'terminations_by_month_judgment', to_char(date_trunc('month', td),'YYYY-MM'), j, '', count(*) from civ where td is not null and td >= '2025-06-01' group by 1,2,3,4
order by 1,2,3,4;

-- [q18] statement 19
-- JOIN, peer view by trial court: detention-habeas (463) filings and who won (Oct 2025 - Mar 2026), vs appeals docketed and which side appealed.
-- Side = appellant name matched to the trial case's DEFENDANT (government) or PLAINTIFF (detainee), first 5 letters; appellee checked the other way.
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k, CIRCUIT::string cir,
               try_to_date(FILE_DATE::string) fd, try_to_date(TERM_DATE::string) td, JUDGMENT::string j,
               upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
ap as (select distinct CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01'),
js as (select ap.d, civ.j,
         case when civ.k is null then 'nomatch'
              when left(ap.a,5) = left(civ.df,5) or left(ap.e,5) = left(civ.p,5) then 'gov'
              when left(ap.a,5) = left(civ.p,5) or left(ap.e,5) = left(civ.df,5) then 'detainee' else 'unclear' end side
       from ap left join civ on civ.d = ap.d and civ.o = ap.o and civ.k = ap.k),
dist as (select d, max(cir) cir, sum(iff(fd >= '2025-10-01',1,0)) filed,
           sum(iff(td >= '2025-10-01' and j='1',1,0)) pet_won, sum(iff(td >= '2025-10-01' and j='2',1,0)) gov_won
         from civ group by 1),
apps as (select d, count(*) appeals, sum(iff(side='gov',1,0)) gov_app, sum(iff(side='detainee',1,0)) det_app,
           sum(iff(side='unclear',1,0)) unclear, sum(iff(side='nomatch',1,0)) nomatch,
           sum(iff(side='gov' and j='1',1,0)) gov_app_after_pet_won, sum(iff(side='detainee' and j='2',1,0)) det_app_after_gov_won
         from js group by 1)
select coalesce(dist.d, apps.d) district, dist.cir, dist.filed, dist.pet_won, dist.gov_won, coalesce(apps.appeals,0) appeals,
  apps.gov_app, apps.det_app, apps.unclear, apps.nomatch, apps.gov_app_after_pet_won, apps.det_app_after_gov_won
from dist full outer join apps on apps.d = dist.d
order by appeals desc, filed desc limit 40;

-- [q19] statement 20
-- JOIN eyeball: 12 detention-habeas appeals with the trial case they came from (names, dates, judgment code)
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               FILE_DATE, TERM_DATE, JUDGMENT::string j, DISPOSITION::string disp, PLAINTIFF, DEFENDANT, TAPE_YEAR
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2025-01-01'
             qualify row_number() over (partition by d, o, k order by try_to_date(TERM_DATE::string) desc nulls last, TAPE_YEAR desc) = 1)
select ap.CIRCUIT, ap.DOCKET, ap.DOCKET_DATE, ap.APPELLANT, ap.APPELLEE, ap.US_APPELLANT, ap.DISTRICT_COURT, ap.DISTRICT_DOCKET,
  civ.PLAINTIFF, civ.DEFENDANT, civ.FILE_DATE, civ.TERM_DATE, civ.j judgment, civ.disp disposition
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE ap
left join civ on civ.d = upper(trim(ap.DISTRICT_COURT::string)) and civ.o = try_to_number(ap.DISTRICT_OFFICE::string) and civ.k = try_to_number(ap.DISTRICT_DOCKET::string)
where ap.NATURE_OF_SUIT::string='463' and try_to_date(ap.DOCKET_DATE::string) >= '2025-10-01'
  and upper(trim(ap.DISTRICT_COURT::string)) in ('22','52','46','12','70','81')
qualify row_number() over (partition by ap.DISTRICT_COURT order by ap.DOCKET) <= 2
order by ap.DISTRICT_COURT, ap.DOCKET;

-- [q20] statement 21
-- Dull-explanation test: new federal civil cases per month, detention habeas (463) vs general habeas (530) vs everything. Reclassification, or new volume?
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               try_to_date(FILE_DATE::string) fd, NATURE_OF_SUIT::string nos
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by TAPE_YEAR desc) = 1)
select to_char(date_trunc('month', fd),'YYYY-MM') m, count(*) all_civil, sum(iff(nos='463',1,0)) n463, sum(iff(nos='530',1,0)) n530,
  sum(iff(nos in ('510','520','540','550','555','560'),1,0)) other_prisoner, count(distinct iff(nos='463', d, null)) districts_with_463
from civ group by 1 order by 1;

-- [q18b] statement 22
-- q18 again with no row limit, for complete totals and the median district. JOIN, peer view by trial court: detention-habeas (463) filings and who won (Oct 2025 - Mar 2026), vs appeals docketed and which side appealed.
-- Side = appellant name matched to the trial case's DEFENDANT (government) or PLAINTIFF (detainee), first 5 letters; appellee checked the other way.
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k, CIRCUIT::string cir,
               try_to_date(FILE_DATE::string) fd, try_to_date(TERM_DATE::string) td, JUDGMENT::string j,
               upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
ap as (select distinct CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01'),
js as (select ap.d, civ.j,
         case when civ.k is null then 'nomatch'
              when left(ap.a,5) = left(civ.df,5) or left(ap.e,5) = left(civ.p,5) then 'gov'
              when left(ap.a,5) = left(civ.p,5) or left(ap.e,5) = left(civ.df,5) then 'detainee' else 'unclear' end side
       from ap left join civ on civ.d = ap.d and civ.o = ap.o and civ.k = ap.k),
dist as (select d, max(cir) cir, sum(iff(fd >= '2025-10-01',1,0)) filed,
           sum(iff(td >= '2025-10-01' and j='1',1,0)) pet_won, sum(iff(td >= '2025-10-01' and j='2',1,0)) gov_won
         from civ group by 1),
apps as (select d, count(*) appeals, sum(iff(side='gov',1,0)) gov_app, sum(iff(side='detainee',1,0)) det_app,
           sum(iff(side='unclear',1,0)) unclear, sum(iff(side='nomatch',1,0)) nomatch,
           sum(iff(side='gov' and j='1',1,0)) gov_app_after_pet_won, sum(iff(side='detainee' and j='2',1,0)) det_app_after_gov_won
         from js group by 1)
select coalesce(dist.d, apps.d) district, dist.cir, dist.filed, dist.pet_won, dist.gov_won, coalesce(apps.appeals,0) appeals,
  apps.gov_app, apps.det_app, apps.unclear, apps.nomatch, apps.gov_app_after_pet_won, apps.det_app_after_gov_won
from dist full outer join apps on apps.d = dist.d
order by appeals desc, filed desc;

-- [q21] statement 23
-- Oral arguments, test inside the group: in each court, are cases with "Trump" in the name the long ones, or did everything get longer?
with oa as (select DOCKET_ID::string did, DURATION, CASE_NAME from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select case when d.COURT_ID in ('cadc','scotus') then d.COURT_ID else 'other_fed_circuits' end grp,
  case when year(d.da) between 2021 and 2024 then '2021-24' when year(d.da) >= 2025 then '2025-26' end period,
  iff(oa.CASE_NAME ilike '%trump%', 'trump_named', 'other') kind,
  count(*) n, median(DURATION) med, percentile_cont(0.75) within group (order by DURATION) p75,
  sum(iff(DURATION > 3600,1,0)) over_60m
from oa join d on d.id = oa.did
where d.COURT_ID like 'ca%' or d.COURT_ID = 'scotus'
group by 1,2,3 having period is not null order by 1,2,3;

-- [q22] statement 24
-- Oral arguments eyeball: the 15 longest D.C. Circuit arguments argued 2025-26, with case name and panel
with oa as (select DOCKET_ID::string did, DURATION, CASE_NAME, JUDGES from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da, DOCKET_NUMBER from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select d.da, d.DOCKET_NUMBER, round(oa.DURATION/60) minutes, left(oa.CASE_NAME,90) case_name, left(oa.JUDGES,80) judges
from oa join d on d.id = oa.did
where d.COURT_ID = 'cadc' and year(d.da) >= 2025
order by oa.DURATION desc limit 15;

-- [q23] statement 25
-- Parentheticals: how much of the table sits in the new opinion-ID range (>= 9M) where the cluster join names the wrong case;
-- and, in the old range, the opinions most often described with "overruled", named via OPINION_CLUSTERS
with p as (select try_to_number(DESCRIBED_OPINION_ID::string) did, TEXT from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_PARENTHETICALS),
band as (select 'band' section, iff(did >= 9000000, 'described id >= 9M', 'described id < 9M') k, count(*) n, count(distinct did) n2,
           null::string case_name, null::string date_filed, null::string sample_text from p group by 2),
ov as (select did, count(*) n, any_value(left(TEXT,140)) sample_text from p where TEXT ilike '%overrul%' and did < 9000000 group by 1 order by n desc limit 15)
select * from band
union all
select 'overruled_top', ov.did::string, ov.n, null, c.CASE_NAME, c.DATE_FILED::string, ov.sample_text
from ov left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS c on try_to_number(c.ID::string) = ov.did
order by 1, 3 desc;

-- [q24] statement 26
-- Judge tables completeness, redone on the right key: FJC JID = CourtListener FJC_ID (q13 used NID and landed only 2017-19).
-- By first commission year: in CL? has degrees? law degree? party row? party agrees with FJC's appointing-president party? Also how many land on NID instead.
with fjc as (select try_to_number(JID::string) jid, try_to_number(NID::string) nid, year(try_to_date(COMMISSION_DATE_1::string)) cy,
               PARTY_OF_APPOINTING_PRESIDENT_1 p from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_ARTICLE_III_JUDGES),
cl as (select try_to_number(FJC_ID::string) fid, min(ID::string) pid from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES
       where try_to_number(FJC_ID::string) is not null group by 1),
ed as (select PERSON_ID::string pid, max(iff(DEGREE_LEVEL in ('jd','llb'),1,0)) has_law
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_EDUCATIONS group by 1),
af as (select PERSON_ID::string pid, max(iff(SOURCE='a', POLITICAL_PARTY, null)) a_party
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS group by 1)
select case when fjc.cy is null then 'no date' when fjc.cy < 1990 then 'before 1990' when fjc.cy < 2017 then '1990-2016' else fjc.cy::string end yb,
  count(*) fjc_judges, count(cl.fid) in_cl_by_jid, count(cl2.fid) in_cl_by_nid, count(ed.pid) has_edu, sum(ed.has_law) has_law_degree,
  count(af.pid) has_party_row, sum(iff(af.a_party is not null,1,0)) has_appointer_party,
  sum(iff((af.a_party='d' and fjc.p ilike 'Democrat%') or (af.a_party='r' and fjc.p ilike 'Republican%'),1,0)) party_agree,
  sum(iff(af.a_party in ('d','r') and not ((af.a_party='d' and fjc.p ilike 'Democrat%') or (af.a_party='r' and fjc.p ilike 'Republican%')),1,0)) party_disagree
from fjc left join cl on cl.fid = fjc.jid left join cl cl2 on cl2.fid = fjc.nid
left join ed on ed.pid = coalesce(cl.pid, cl2.pid) left join af on af.pid = coalesce(cl.pid, cl2.pid)
group by 1 order by 1;

-- [q25] statement 27
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
group by 1 order by 2;

-- [q26] statement 28
-- Oral arguments, dull-explanation test for the D.C. Circuit: is the rise just more en banc (full-court) sittings? Split by panel size.
with oa as (select DOCKET_ID::string did, DURATION, JUDGES from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select iff(d.COURT_ID='cadc','cadc','other_fed_circuits') grp, year(d.da) yr,
  sum(iff(regexp_count(oa.JUDGES, ';') + 1 <= 3,1,0)) n_panel, median(iff(regexp_count(oa.JUDGES, ';') + 1 <= 3, DURATION, null)) med_panel,
  sum(iff(regexp_count(oa.JUDGES, ';') + 1 > 3,1,0)) n_big_bench, median(iff(regexp_count(oa.JUDGES, ';') + 1 > 3, DURATION, null)) med_big,
  sum(iff(oa.JUDGES is null or trim(oa.JUDGES)='',1,0)) no_judges
from oa join d on d.id = oa.did
where (d.COURT_ID = 'cadc' or d.COURT_ID in ('ca1','ca2','ca3','ca4','ca5','ca6','ca7','ca8','ca9','ca10','ca11','cafc')) and year(d.da) >= 2019
group by 1,2 order by 1,2;

-- [q27] statement 29
-- JOIN, cleaner rate: detainee wins (JUDGMENT 1) closed Oct-Dec 2025 -- 90+ days before the data ends -- and how many drew a government appeal, by district
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               try_to_date(TERM_DATE::string) td, JUDGMENT::string j, upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
wins as (select * from civ where j='1' and td between '2025-10-01' and '2025-12-31'),
ap as (select distinct CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01'),
w as (select wins.d, wins.k, wins.o,
        max(iff(ap.k is not null and (left(ap.a,5) = left(wins.df,5) or left(ap.e,5) = left(wins.p,5)),1,0)) gov_appealed,
        max(iff(ap.k is not null,1,0)) any_appeal
      from wins left join ap on ap.d = wins.d and ap.o = wins.o and ap.k = wins.k group by 1,2,3)
select coalesce(d,'ALL') district, count(*) wins_oct_dec, sum(gov_appealed) gov_appealed, sum(any_appeal) any_appeal,
  round(sum(gov_appealed)/count(*),3) gov_rate
from w group by rollup(d) having count(*) >= 40 order by wins_oct_dec desc;

-- [q28] statement 30
-- Dull-explanation test for the appeal-rate gap: were the low-appeal districts' wins a different kind (consent, other)? Disposition mix of Oct-Dec 2025 detainee wins
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               try_to_date(TERM_DATE::string) td, try_to_date(FILE_DATE::string) fd, JUDGMENT::string j, DISPOSITION::string disp,
               upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by td desc nulls last, TAPE_YEAR desc) = 1),
wins as (select * from civ where j='1' and td between '2025-10-01' and '2025-12-31' and d in ('22','52','46','70','74','01','81','3G','12')),
ap as (select distinct upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01')
select wins.d, wins.disp, count(distinct wins.k||'|'||wins.o) wins, median(datediff('day', wins.fd, wins.td)) med_days_to_win,
  count(distinct iff(left(ap.a,5) = left(wins.df,5) or left(ap.e,5) = left(wins.p,5), wins.k||'|'||wins.o, null)) gov_appealed
from wins left join ap on ap.d = wins.d and ap.o = wins.o and ap.k = wins.k
group by 1,2 order by 1, 3 desc;

-- [q29] statement 31
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
group by 1 order by 2;

-- [q30] statement 32
-- Hostile-editor test: are the government's detention-habeas appeals real fights, or notices filed and then dropped?
-- 463 appeals docketed Oct 2025 - Mar 2026: closed by 31 Mar 2026? on the merits (DISPOSITION 1/2, OUTCOME filled) or without a ruling (4/5)? By side, top-3 trial courts vs rest.
with civ as (select upper(trim(DISTRICT::string)) d, try_to_number(OFFICE::string) o, try_to_number(DOCKET::string) k,
               upper(trim(PLAINTIFF)) p, upper(trim(DEFENDANT)) df
             from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
             where NATURE_OF_SUIT::string='463' and try_to_date(FILE_DATE::string) >= '2024-10-01'
             qualify row_number() over (partition by d, o, k order by try_to_date(TERM_DATE::string) desc nulls last, TAPE_YEAR desc) = 1),
ap as (select CIRCUIT, DOCKET, REOPEN, upper(trim(DISTRICT_COURT::string)) d, try_to_number(DISTRICT_OFFICE::string) o,
         try_to_number(DISTRICT_DOCKET::string) k, upper(trim(APPELLANT)) a, upper(trim(APPELLEE)) e, TAPE_YEAR::string tape,
         DISPOSITION::string disp, OUTCOME::string outc, PROCEDURAL_TERMINATION::string pt,
         datediff('day', try_to_date(DOCKET_DATE::string), try_to_date(JUDGMENT_DATE::string)) days
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
       where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01'
       qualify row_number() over (partition by CIRCUIT, DOCKET, REOPEN order by TAPE_YEAR) = 1)
select iff(ap.d in ('22','52','46'), ap.d, 'rest') trial_court,
  case when civ.k is null then 'nomatch' when left(ap.a,5) = left(civ.df,5) or left(ap.e,5) = left(civ.p,5) then 'gov'
       when left(ap.a,5) = left(civ.p,5) or left(ap.e,5) = left(civ.df,5) then 'detainee' else 'unclear' end side,
  count(*) appeals, sum(iff(tape <> '2099',1,0)) closed, sum(iff(disp in ('1','2'),1,0)) closed_merits,
  sum(iff(disp in ('1','2') and outc='1',1,0)) merits_outcome1, sum(iff(disp in ('1','2') and outc<>'1',1,0)) merits_other,
  sum(iff(disp in ('4','5'),1,0)) closed_no_ruling, mode(iff(disp='4', pt, null)) top_proc_code, median(iff(tape <> '2099', days, null)) med_days_open
from ap left join civ on civ.d = ap.d and civ.o = ap.o and civ.k = ap.k
group by 1,2 order by 1,2;

-- [q31] statement 33
-- Peer/base rate for "dropped fast": share of appeals closed without a merits ruling within 90 days of docketing.
-- Detention habeas docketed Oct-Dec 2025 (90+ days before data ends) vs other U.S.-party civil appeals docketed FY2023-24. Split by the US-appellant flag.
with a as (select CIRCUIT, DOCKET, REOPEN, try_to_date(DOCKET_DATE::string) dd, try_to_date(JUDGMENT_DATE::string) jd,
             NATURE_OF_SUIT::string nos, APPEAL_TYPE::string t, US_APPELLANT::string usa, DISPOSITION::string disp
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
           where try_to_date(DOCKET_DATE::string) >= '2022-10-01'
           qualify row_number() over (partition by CIRCUIT, DOCKET, REOPEN order by TAPE_YEAR) = 1)
select case when nos='463' and dd between '2025-10-01' and '2025-12-31' then 'detention habeas, docketed Oct-Dec 2025'
            when t='3' and nos<>'463' and dd between '2022-10-01' and '2024-09-30' then 'other US-party civil, docketed FY2023-24' end grp,
  usa us_appellant_flag, count(*) appeals,
  sum(iff(disp in ('4','5') and datediff('day', dd, jd) <= 90,1,0)) closed_no_ruling_90d,
  sum(iff(disp in ('1','2') and datediff('day', dd, jd) <= 90,1,0)) closed_merits_90d,
  round(sum(iff(disp in ('4','5') and datediff('day', dd, jd) <= 90,1,0)) / count(*), 3) share_no_ruling_90d
from a group by 1,2 having grp is not null order by 1,2;
