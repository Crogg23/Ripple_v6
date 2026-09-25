-- g15: deep pass 3, 2026-09-24. Python door, QUERY_TAG deep3-2026-09-24. Read-only: SELECT/WITH only.
-- Tables: POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP, POLITICS__CA_LOBBY_EMP_LOBBYIST, POLITICS__CA_LOBBY_FIRM_LOBBYIST, POLITICS__JUDGE_IDEOLOGY_COA, POLITICS__FED_MEDSL_HOUSE_RETURNS.
-- Every statement run is below, in order, with its runtime.

-- ===== connection: b1.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q01_cmte_by_congress] (0.8s)
-- Committee roster shape per Congress: snapshot, seats, members, subcommittee flag values, side values, titles
select CONGRESS, min(SNAPSHOT_DATE) snap_min, max(SNAPSHOT_DATE) snap_max, count(distinct SNAPSHOT_SHA) n_sha,
  count(*) n, count(distinct BIOGUIDE) n_members,
  sum(iff(IS_SUBCOMMITTEE ilike 'true',1,0)) n_sub, sum(iff(IS_SUBCOMMITTEE ilike 'false',1,0)) n_full,
  count(distinct iff(IS_SUBCOMMITTEE ilike 'false', COMMITTEE_CODE, null)) n_full_cmtes,
  count(distinct iff(COMMITTEE_CODE like 'H%', BIOGUIDE, null)) n_house_members,
  count(distinct iff(COMMITTEE_CODE like 'S%', BIOGUIDE, null)) n_senate_members,
  count(distinct iff(COMMITTEE_CODE like 'J%', COMMITTEE_CODE, null)) n_joint_codes,
  listagg(distinct PARTY, ',') party_vals,
  sum(iff(nullif(trim(TITLE),'') is not null,1,0)) n_title,
  sum(iff(try_to_number(RANK) is null,1,0)) n_rank_not_num,
  count(*) - count(distinct CONGRESS||COMMITTEE_CODE||BIOGUIDE) n_dup_seat
from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
group by 1 order by 1;

-- [q02_pac_money_coverage] (0.6s)
-- MEMBER_PAC_MONEY coverage by cycle, and how many 118th House full-committee members it reaches
with cm as (select distinct BIOGUIDE from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP where CONGRESS = '118' and COMMITTEE_CODE like 'H%' and IS_SUBCOMMITTEE ilike 'false')
select p.CYCLE, count(*) n, count(distinct p.BIOGUIDE) n_members, sum(p.PAC_DONATIONS) pac_sum, median(p.PAC_DONATIONS) pac_med,
  max(p.PAC_DONATIONS) pac_max, sum(iff(p.PAC_DONATIONS is null or p.PAC_DONATIONS = 0,1,0)) n_zero,
  count(distinct iff(cm.BIOGUIDE is not null, p.BIOGUIDE, null)) n_in_118_house_cmte,
  (select count(*) from cm) n_118_house_cmte_members
from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_PAC_MONEY p left join cm on cm.BIOGUIDE = p.BIOGUIDE
group by 1 order by 1;

-- [q03_ca_lobby_profile] (0.7s)
-- Both CA lobbyist link tables: sessions, rows, ids, names, ids carrying >1 name, overlap of ids across the two tables
with e as (select 'emp' src, SESSION_ID, LOBBYIST_ID, upper(trim(LOBBYIST_LAST_NAME))||'|'||upper(trim(LOBBYIST_FIRST_NAME)) nm, EMPLOYER_ID org_id, EMPLOYER_NAME org_name, _SOURCE_RUN_ID run from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMP_LOBBYIST
  union all select 'firm', SESSION_ID, LOBBYIST_ID, upper(trim(LOBBYIST_LAST_NAME))||'|'||upper(trim(LOBBYIST_FIRST_NAME)), FIRM_ID, FIRM_NAME, _SOURCE_RUN_ID from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM_LOBBYIST),
ids as (select LOBBYIST_ID, count(distinct nm) nn from e group by 1)
select src, SESSION_ID, count(*) n, count(distinct LOBBYIST_ID) n_ids, count(distinct nm) n_names, count(distinct org_id) n_orgs, count(distinct org_name) n_org_names,
  count(distinct run) n_runs, count(*) - count(distinct LOBBYIST_ID||'|'||org_id) n_dup_pairs,
  count(distinct iff(LOBBYIST_ID in (select LOBBYIST_ID from ids where nn > 1), LOBBYIST_ID, null)) n_ids_multi_name,
  count(distinct iff(src='emp' and LOBBYIST_ID in (select LOBBYIST_ID from e where src='firm'), LOBBYIST_ID,
                     iff(src='firm' and LOBBYIST_ID in (select LOBBYIST_ID from e where src='emp'), LOBBYIST_ID, null))) n_ids_in_both,
  max(cnt_per_id) max_orgs_per_id
from e join (select src s2, LOBBYIST_ID l2, count(distinct org_id) cnt_per_id from e group by 1,2) x on x.s2 = e.src and x.l2 = e.LOBBYIST_ID
group by 1,2 order by 1,2;

-- [q04_judge_jcs_profile] (0.5s)
-- Judge ideology table: circuits, distinct scores, how many judges share a score, duplicate names
with j as (select * from LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_COA),
v as (select JCS, count(*) n from j group by 1)
select 'circuit' k, CIRCUIT::string val, count(*) n, round(median(JCS),3) med, round(min(JCS),3) mn, round(max(JCS),3) mx, null extra from j group by 2
union all select 'score_top', JCS::string, n, null, null, null, null from (select * from v order by n desc limit 15)
union all select 'score_stats', 'distinct', (select count(*) from v), (select count(*) from v where n = 1), (select sum(n) from v where n >= 5), (select count(*) from j where JCS is null), null
union all select 'dup_name', JCS_JUDGE_NAME, count(*), null, null, null, listagg(CIRCUIT::string||':'||JCS::string, ' ') from j group by JCS_JUDGE_NAME having count(*) > 1
union all select 'sample', JCS_JUDGE_NAME, CIRCUIT, JCS, null, null, null from (select * from j order by random() limit 12)
order by 1, 3 desc;

-- [q05_house_returns_by_year] (1.6s, ERROR)
-- House returns per year: rows, races, stages, flags, scattering/blank rows, null votes, fusion repeats, vote_mode
with h as (select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_HOUSE_RETURNS),
f as (select ELECTION_YEAR, STATE_ABBR, DISTRICT, STAGE, IS_SPECIAL_ELECTION, IS_RUNOFF, CANDIDATE_NAME, count(*) c from h group by 1,2,3,4,5,6,7)
select h.ELECTION_YEAR, count(*) n, count(distinct h.STATE_ABBR||h.DISTRICT||h.STAGE||h.IS_SPECIAL_ELECTION::string||h.IS_RUNOFF::string) n_races,
  listagg(distinct h.STAGE, ',') stages, listagg(distinct h.VOTE_MODE, ',') modes,
  sum(iff(h.IS_SPECIAL_ELECTION,1,0)) n_special, sum(iff(h.IS_RUNOFF,1,0)) n_runoff, sum(iff(h.IS_WRITEIN,1,0)) n_writein,
  sum(iff(h.CANDIDATE_NAME ilike '%scatter%' or h.CANDIDATE_NAME ilike '%blank%' or h.CANDIDATE_NAME ilike '%void%' or h.CANDIDATE_NAME ilike '%over vote%' or h.CANDIDATE_NAME ilike '%under vote%',1,0)) n_blank_rows,
  sum(iff(h.CANDIDATE_VOTES is null or h.CANDIDATE_VOTES < 0,1,0)) n_bad_votes,
  sum(iff(h.TOTAL_VOTES is null or h.TOTAL_VOTES <= 0,1,0)) n_bad_total,
  sum(iff(h.VOTE_SHARE >= 0.999,1,0)) n_share1,
  (select sum(c-1) from f where f.ELECTION_YEAR = h.ELECTION_YEAR and f.c > 1) n_fusion_extra,
  count(distinct h.STATE_ABBR) n_states
from h group by 1 order by 1;

-- ===== connection: b2.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q05b_house_returns_by_year] (0.6s)
-- (rerun of q05, which failed to compile) House returns per year: rows, races, stages, flags, scattering/blank rows, bad votes, fusion repeats
with h as (select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_HOUSE_RETURNS),
f as (select ELECTION_YEAR yr, sum(c-1) extra from (select ELECTION_YEAR, STATE_ABBR, DISTRICT, STAGE, IS_SPECIAL_ELECTION, IS_RUNOFF, CANDIDATE_NAME, count(*) c from h group by 1,2,3,4,5,6,7) where c > 1 group by 1)
select h.ELECTION_YEAR, count(*) n, count(distinct h.STATE_ABBR||'-'||h.DISTRICT||'-'||h.STAGE||h.IS_SPECIAL_ELECTION::string||h.IS_RUNOFF::string) n_races,
  listagg(distinct h.STAGE, ',') stages, listagg(distinct h.VOTE_MODE, ',') modes,
  sum(iff(h.IS_SPECIAL_ELECTION,1,0)) n_special, sum(iff(h.IS_RUNOFF,1,0)) n_runoff, sum(iff(h.IS_WRITEIN,1,0)) n_writein,
  sum(iff(h.CANDIDATE_NAME ilike '%scatter%' or h.CANDIDATE_NAME ilike '%blank%' or h.CANDIDATE_NAME ilike '%void%' or h.CANDIDATE_NAME ilike '%over vote%' or h.CANDIDATE_NAME ilike '%under vote%',1,0)) n_blank_rows,
  sum(iff(h.CANDIDATE_VOTES is null or h.CANDIDATE_VOTES < 0,1,0)) n_bad_votes,
  sum(iff(h.CANDIDATE_VOTES between 0 and 1,1,0)) n_votes_0_1,
  sum(iff(h.TOTAL_VOTES is null or h.TOTAL_VOTES <= 1,1,0)) n_bad_total,
  sum(iff(h.VOTE_SHARE >= 0.999,1,0)) n_share1,
  max(f.extra) n_fusion_extra,
  count(distinct h.STATE_ABBR) n_states
from h left join f on f.yr = h.ELECTION_YEAR group by 1 order by 1;

-- [q06_pac_outliers] (0.5s)
-- Top PAC totals per cycle with names, to see what the $29.3M max is
select * from (
select p.CYCLE, p.BIOGUIDE, s.FULL_NAME, s.STATE, s.LAST_TERM_TYPE, p.PAC_DONATIONS, p.N_PAC_DONORS, p.OUTSIDE_FOR,
  row_number() over (partition by p.CYCLE order by p.PAC_DONATIONS desc nulls last) rk
from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_PAC_MONEY p left join LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE s on s.BIOGUIDE = p.BIOGUIDE)
where rk <= 8 order by CYCLE, rk;

-- [q07_cmte_titles] (0.3s)
-- Leadership titles by chamber and side, full committees vs subcommittees
select left(COMMITTEE_CODE,1) chamber, IS_SUBCOMMITTEE, PARTY, TITLE, count(*) n, count(distinct CONGRESS) n_congresses
from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
where nullif(trim(TITLE),'') is not null
group by 1,2,3,4 order by 1,2,3,5 desc;

-- [q08_cmte_roster_completeness] (0.8s)
-- Members whose last term ended early inside the 117th/118th/119th: are they on that Congress's roster snapshot?
with l as (select BIOGUIDE, NAME_OFFICIAL_FULL, TERM_TYPE, STATE, try_to_date(TERM_START) ts, try_to_date(TERM_END) te from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS),
early as (
  select '118' cg, l.* from l where te between '2023-01-04' and '2024-12-16' and ts < te
  union all select '117', l.* from l where te between '2021-01-04' and '2022-11-28' and ts < te
  union all select '119', l.* from l where te between '2025-01-04' and '2026-09-01' and ts < te
),
r as (select distinct CONGRESS, BIOGUIDE from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP)
select e.cg, count(*) n_left_early, sum(iff(r.BIOGUIDE is not null,1,0)) n_on_roster,
  listagg(e.NAME_OFFICIAL_FULL||' ('||e.TERM_TYPE||'-'||e.STATE||', ended '||e.te::string||')', '; ') within group (order by e.te) who
from early e left join r on r.CONGRESS = e.cg and r.BIOGUIDE = e.BIOGUIDE
group by 1 order by 1;

-- [q09_judge_fjc_join] (0.8s)
-- Name + circuit join from the JCS appeals-judge list to FJC appellate service; land rate, coverage by commission year
with j as (select JCS_JUDGE_NAME nm, CIRCUIT, JCS, upper(trim(split_part(JCS_JUDGE_NAME, ',', 1))) ln,
             upper(split_part(trim(split_part(JCS_JUDGE_NAME, ',', 2)), ' ', 1)) fn
           from LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_COA),
s as (select sv.NID, upper(trim(fj.LAST_NAME)) ln, upper(trim(fj.FIRST_NAME)) fn, sv.COURT_NAME, sv.COMMISSION_DATE, sv.SENIOR_STATUS_DATE, sv.TERMINATION_DATE, sv.APPOINTING_PRESIDENT,
        case when sv.COURT_NAME ilike '%District of Columbia Circuit%' then 12 when sv.COURT_NAME ilike '%Federal Circuit%' then 13
             when sv.COURT_NAME ilike '%First Circuit%' then 1 when sv.COURT_NAME ilike '%Second Circuit%' then 2 when sv.COURT_NAME ilike '%Third Circuit%' then 3
             when sv.COURT_NAME ilike '%Fourth Circuit%' then 4 when sv.COURT_NAME ilike '%Fifth Circuit%' then 5 when sv.COURT_NAME ilike '%Sixth Circuit%' then 6
             when sv.COURT_NAME ilike '%Seventh Circuit%' then 7 when sv.COURT_NAME ilike '%Eighth Circuit%' then 8 when sv.COURT_NAME ilike '%Ninth Circuit%' then 9
             when sv.COURT_NAME ilike '%Tenth Circuit%' then 10 when sv.COURT_NAME ilike '%Eleventh Circuit%' then 11 end circ
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE sv join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE fj on fj.NID = sv.NID
      where sv.COURT_TYPE ilike '%Appeals%'),
m as (select j.*, s.NID, s.fn fjc_fn, s.COMMISSION_DATE, s.APPOINTING_PRESIDENT,
        count(*) over (partition by j.nm, j.CIRCUIT) n_cand
      from j left join s on s.ln = j.ln and s.circ = j.CIRCUIT),
best as (select * from m where n_cand = 1 or left(fjc_fn,1) = left(fn,1)
         qualify row_number() over (partition by nm, CIRCUIT order by iff(fjc_fn = fn,0,1)) = 1)
select 'land' k, null yr, (select count(*) from j) n_jcs, count(*) n_rows, count(NID) n_landed, sum(iff(fn <> fjc_fn,1,0)) n_first_differs,
  (select count(distinct NID) from s where circ is not null) n_fjc_appellate, max(COMMISSION_DATE)::string mx
from best
union all
select 'by_commission_year', year(s.COMMISSION_DATE), count(*), count(b.NID), null, null, null, listagg(distinct iff(b.NID is null, s.ln, null), ',')
from s left join (select distinct NID, CIRCUIT from best) b on b.NID = s.NID and b.CIRCUIT = s.circ
where s.circ is not null and s.COMMISSION_DATE >= '2012-01-01'
group by 2
union all
select 'first_differs_sample', null, null, null, null, null, null, listagg(nm||'='||fjc_fn, '; ')
from (select * from best where fn <> fjc_fn limit 15)
order by 1, 2;

-- [q10_cmte_new_chairs_pac] (0.6s)
-- House full-committee chairs and ranking members: PAC money 2026 cycle vs 2024 cycle for members who GAINED or LOST a top seat between the 118th and 119th, against same-side members who never held one
with t as (select CONGRESS, BIOGUIDE, max(MEMBER_NAME) nm, max(PARTY) side,
             max(iff(TITLE ilike 'chair%' and TITLE not ilike '%vice%',1,0)) is_chair,
             max(iff(TITLE ilike 'ranking%',1,0)) is_rank
           from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
           where COMMITTEE_CODE like 'H%' and IS_SUBCOMMITTEE ilike 'false'
           group by 1,2),
a as (select c19.BIOGUIDE, c19.nm, c19.side side19, c18.side side18, c18.is_chair ch18, c19.is_chair ch19, c18.is_rank rk18, c19.is_rank rk19
      from t c19 join t c18 on c18.BIOGUIDE = c19.BIOGUIDE and c18.CONGRESS = '118' where c19.CONGRESS = '119'),
p as (select BIOGUIDE, max(iff(CYCLE='2024', PAC_DONATIONS, null)) p24, max(iff(CYCLE='2026', PAC_DONATIONS, null)) p26
      from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_PAC_MONEY group by 1),
g as (select a.*, p.p24, p.p26, p.p26 / nullif(p.p24,0) ratio,
        case when ch19 = 1 and ch18 = 0 then 'gained_chair'
             when ch18 = 1 and ch19 = 1 then 'kept_chair'
             when ch18 = 1 and ch19 = 0 then 'lost_chair'
             when rk19 = 1 and rk18 = 0 then 'gained_ranking'
             when rk18 = 1 and rk19 = 1 then 'kept_ranking'
             when rk18 = 1 and rk19 = 0 then 'lost_ranking'
             else 'none_'||side19 end grp
      from a join p on p.BIOGUIDE = a.BIOGUIDE where p.p24 > 0 and p.p26 is not null)
select 'grp' k, grp, count(*) n, round(median(ratio),3) med_ratio, round(avg(ratio),3) avg_ratio, round(median(p24)) med_p24, round(median(p26)) med_p26,
  sum(iff(ratio > 1,1,0)) n_up, null who
from g group by 2
union all
select 'member', grp, null, round(ratio,3), null, p24, p26, null, nm||' '||BIOGUIDE
from g where grp in ('gained_chair','lost_chair','gained_ranking','lost_ranking')
order by 1, 2, 4 desc;

-- ===== connection: b3.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q11_freshmen_pac_by_committee] (0.9s)
-- House freshmen (first roster appearance in the 118th or 119th) : PAC money in their first re-election cycle, by committee, split by side and by whether outside groups targeted the race ($1M+ for or against)
with r as (select CONGRESS, BIOGUIDE, COMMITTEE_CODE, PARTY, MEMBER_NAME from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP where IS_SUBCOMMITTEE ilike 'false'),
first_cg as (select BIOGUIDE, min(CONGRESS::int) fc from r group by 1),
fr as (select r.CONGRESS::int cg, r.BIOGUIDE, max(r.MEMBER_NAME) nm, max(r.PARTY) side,
         max(iff(COMMITTEE_CODE = 'HSBA',1,0)) on_fin, max(iff(COMMITTEE_CODE in ('HSWM','HSIF','HSAP'),1,0)) on_other_money,
         listagg(distinct COMMITTEE_CODE, ',') cmtes
       from r join first_cg f on f.BIOGUIDE = r.BIOGUIDE and f.fc = r.CONGRESS::int
       where r.CONGRESS in ('118','119') and r.COMMITTEE_CODE like 'H%'
       group by 1,2),
p as (select BIOGUIDE, CYCLE, PAC_DONATIONS, N_PAC_DONORS, coalesce(OUTSIDE_FOR,0) + coalesce(OUTSIDE_AGAINST,0) outside from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_PAC_MONEY),
x as (select fr.*, p.PAC_DONATIONS pac, p.N_PAC_DONORS donors, p.outside,
        iff(p.outside >= 1000000, 'targeted', 'not_targeted') tgt,
        case when on_fin = 1 then 'fin_services' when on_other_money = 1 then 'wm_ec_approps' else 'other' end grp
      from fr join p on p.BIOGUIDE = fr.BIOGUIDE and p.CYCLE = iff(fr.cg = 118, '2024', '2026'))
select 'grp' k, cg, side, tgt, grp, count(*) n, round(median(pac)) med_pac, round(median(donors)) med_donors, round(avg(pac)) avg_pac, null who
from x group by 2,3,4,5
union all
select 'grp_all', cg, side, 'all', grp, count(*), round(median(pac)), round(median(donors)), round(avg(pac)), null from x group by 2,3,5
union all
select 'top', cg, side, tgt, grp, null, pac, donors, outside, nm||' '||BIOGUIDE||' ['||cmtes||']'
from x qualify row_number() over (partition by cg order by pac desc) <= 8
union all
select 'fresh_count', cg, null, null, null, (select count(*) from fr f2 where f2.cg = x.cg), count(*), null, null, null from x group by 2
order by 1, 2, 3, 4, 5;

-- [q12_cmte_seat_concentration] (0.2s)
-- Who holds the most roster rows in the 119th, and how many of those rows are ex officio seats
select BIOGUIDE, max(MEMBER_NAME) nm, left(max(COMMITTEE_CODE),1) chamber, count(*) n_rows,
  sum(iff(TITLE ilike 'ex officio',1,0)) n_ex_officio, sum(iff(IS_SUBCOMMITTEE ilike 'false',1,0)) n_full,
  count(*) - sum(iff(TITLE ilike 'ex officio',1,0)) n_voting_seats
from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
where CONGRESS = '119'
group by 1 qualify row_number() over (order by count(*) desc) <= 8
   or row_number() over (order by count(*) - sum(iff(TITLE ilike 'ex officio',1,0)) desc) <= 5
order by n_rows desc;

-- [q13_house_turnout_gap] (0.9s)
-- Contested general-election House races (runner-up 25%+), total votes against the median contested district in the same state and year; fusion lines summed per candidate
with h as (select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_HOUSE_RETURNS
           where STAGE = 'gen' and not IS_SPECIAL_ELECTION and not IS_RUNOFF),
c as (select ELECTION_YEAR yr, STATE_ABBR st, DISTRICT dist, CANDIDATE_NAME cand, sum(CANDIDATE_VOTES) v, max(TOTAL_VOTES) tv
      from h where not (CANDIDATE_NAME ilike '%scatter%' or CANDIDATE_NAME ilike '%blank%' or CANDIDATE_NAME ilike '%void%' or CANDIDATE_NAME ilike '%over vote%' or CANDIDATE_NAME ilike '%under vote%')
      group by 1,2,3,4),
rc as (select yr, st, dist, max(tv) tv, sum(v) sumv, max_by(cand, v) winner, max(v) wv,
         max(iff(rk = 2, v, 0)) / nullif(max(tv),0) ru_share
       from (select c.*, row_number() over (partition by yr, st, dist order by v desc) rk from c) group by 1,2,3),
con as (select rc.*, median(tv) over (partition by yr, st) st_med, count(*) over (partition by yr, st) st_n, tv / median(tv) over (partition by yr, st) ratio
        from rc where ru_share >= 0.25),
nat as (select yr, median(tv) nat_med from con group by 1)
select 'year' k, con.yr, null st, null dist, count(*) n_contested, round(max(nat.nat_med)) nat_med,
  sum(iff(st_n >= 5 and ratio < 0.5,1,0)) n_under_half_state_med, sum(iff(st_n >= 5,1,0)) n_in_big_states,
  round(min(iff(st_n >= 5, ratio, null)),3) min_ratio, null winner
from con join nat on nat.yr = con.yr group by 2
union all
select 'low_2018', yr, st, dist, tv, st_med, st_n, null, round(ratio,3), winner||' '||round(wv/tv,3)
from con where yr = 2018 and st_n >= 5 qualify row_number() over (order by ratio) <= 12
union all
select 'low_1996', yr, st, dist, tv, st_med, st_n, null, round(ratio,3), winner
from con where yr = 1996 and st_n >= 5 qualify row_number() over (order by ratio) <= 6
union all
select 'mismatch', null, null, null, count(*), sum(iff(abs(sumv - tv) > 0.01 * tv,1,0)), sum(iff(sumv > tv * 1.01,1,0)), null, null, null from rc
order by 1, 2, 9;

-- [q14_judge_senior_timing] (0.9s)
-- Appeals judges taking senior status: rate per presidency by whether the sitting president shares the appointing president's party, among judges eligible (age 65+, age+service 80+ by term end); JCS medians for goers vs stayers
with pres as (select column1 pname, column2 pparty, column3::date s, column4::date e from values
   ('Carter','Democratic','1977-01-20','1981-01-20'), ('Reagan','Republican','1981-01-20','1989-01-20'), ('Bush41','Republican','1989-01-20','1993-01-20'),
   ('Clinton','Democratic','1993-01-20','2001-01-20'), ('Bush43','Republican','2001-01-20','2009-01-20'), ('Obama','Democratic','2009-01-20','2017-01-20'),
   ('Trump1','Republican','2017-01-20','2021-01-20'), ('Biden','Democratic','2021-01-20','2025-01-20'), ('Trump2','Republican','2025-01-20','2026-09-01')),
s as (select sv.NID, sv.COURT_NAME, sv.PARTY_OF_APPOINTING_PRESIDENT pa, sv.COMMISSION_DATE cd, sv.SENIOR_STATUS_DATE sd, sv.TERMINATION_DATE td, fj.BIRTH_YEAR by_,
        upper(trim(fj.LAST_NAME)) ln, upper(trim(fj.FIRST_NAME)) fn,
        case when sv.COURT_NAME ilike '%District of Columbia Circuit%' then 12 when sv.COURT_NAME ilike '%Federal Circuit%' then 13
             when sv.COURT_NAME ilike '%First Circuit%' then 1 when sv.COURT_NAME ilike '%Second Circuit%' then 2 when sv.COURT_NAME ilike '%Third Circuit%' then 3
             when sv.COURT_NAME ilike '%Fourth Circuit%' then 4 when sv.COURT_NAME ilike '%Fifth Circuit%' then 5 when sv.COURT_NAME ilike '%Sixth Circuit%' then 6
             when sv.COURT_NAME ilike '%Seventh Circuit%' then 7 when sv.COURT_NAME ilike '%Eighth Circuit%' then 8 when sv.COURT_NAME ilike '%Ninth Circuit%' then 9
             when sv.COURT_NAME ilike '%Tenth Circuit%' then 10 when sv.COURT_NAME ilike '%Eleventh Circuit%' then 11 end circ
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE sv join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE fj on fj.NID = sv.NID
      where sv.COURT_TYPE ilike '%Appeals%'),
j as (select JCS_JUDGE_NAME nm, CIRCUIT, JCS, upper(trim(split_part(JCS_JUDGE_NAME, ',', 1))) ln,
             upper(split_part(trim(split_part(JCS_JUDGE_NAME, ',', 2)), ' ', 1)) fn
      from LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_COA),
jm as (select s.NID, s.circ, j.JCS from j join s on s.ln = j.ln and s.circ = j.CIRCUIT
       qualify count(*) over (partition by j.nm, j.CIRCUIT) = 1 or left(s.fn,1) = left(j.fn,1)),
pool as (select p.pname, p.pparty, p.s, p.e, s.*, iff(s.pa = p.pparty, 'same', 'other') rel,
           iff((year(p.e) - s.by_) >= 65 and (year(p.e) - s.by_) + datediff(year, s.cd, p.e) >= 80, 1, 0) elig,
           iff(s.sd >= p.s and s.sd < p.e, 1, 0) went,
           jm.JCS
         from pres p join s on s.cd < p.s and coalesce(s.sd, '9999-12-31'::date) >= p.s and coalesce(s.td, '9999-12-31'::date) >= p.s
         left join jm on jm.NID = s.NID and jm.circ = s.circ
         where s.pa in ('Republican','Democratic'))
select pname, min(s) term_start, rel, count(*) n_active, sum(elig) n_eligible, sum(iff(elig = 1, went, 0)) n_went_eligible, sum(went) n_went_all,
  round(sum(iff(elig = 1, went, 0)) / nullif(sum(elig),0), 3) rate_eligible,
  round(median(iff(elig = 1 and went = 1, JCS, null)),3) jcs_med_goers, round(median(iff(elig = 1 and went = 0, JCS, null)),3) jcs_med_stayers,
  count(JCS) n_with_jcs, max(sd)::string max_senior_date
from pool group by 1, 3 order by 2, 3 desc;

-- [q15_ca_lobby_links] (1.3s)
-- CA lobbyist link tables: spend per in-house lobbyist (employer table join), spend per firm lobbyist (firm table join), in-house-to-firm movers, employer ids with several names
with e as (select * from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMP_LOBBYIST),
f as (select * from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM_LOBBYIST),
emp as (select EMPLOYER_ID, SESSION_ID, max(EMPLOYER_NAME) nm, max(SESSION_TOTAL_AMT) amt, max(YR_1_YTD_AMT) y1, max(YR_2_YTD_AMT) y2 from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER group by 1,2),
firm as (select FIRM_ID, SESSION_ID, max(FIRM_NAME) nm, max(SESSION_TOTAL_AMT) amt from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM group by 1,2),
el as (select e.SESSION_ID, e.EMPLOYER_ID, count(*) n_lob from e group by 1,2),
fl as (select f.SESSION_ID, f.FIRM_ID, count(*) n_lob from f group by 1,2)
select 'emp_land' k, el.SESSION_ID sess, count(*) n_orgs, count(emp.EMPLOYER_ID) n_landed, sum(iff(emp.amt > 0,1,0)) n_amt_pos, sum(emp.amt) amt_sum, null n_lob, null per_lob, null nm
from el left join emp on emp.EMPLOYER_ID = el.EMPLOYER_ID and emp.SESSION_ID = el.SESSION_ID group by 2
union all
select 'emp_emp_sessions', SESSION_ID, count(*), null, sum(iff(amt > 0,1,0)), sum(amt), null, null, null from emp group by 2
union all
select 'firm_land', fl.SESSION_ID, count(*), count(firm.FIRM_ID), sum(iff(firm.amt > 0,1,0)), sum(firm.amt), null, null, null
from fl left join firm on firm.FIRM_ID = fl.FIRM_ID and firm.SESSION_ID = fl.SESSION_ID group by 2
union all
select 'firm_firm_sessions', SESSION_ID, count(*), null, sum(iff(amt > 0,1,0)), sum(amt), null, null, null from firm group by 2
union all
select * from (select 'emp_top_per_lob', el.SESSION_ID, null, null, null, emp.amt, el.n_lob, round(emp.amt / el.n_lob), emp.nm
  from el join emp on emp.EMPLOYER_ID = el.EMPLOYER_ID and emp.SESSION_ID = el.SESSION_ID where emp.amt > 0 order by emp.amt / el.n_lob desc limit 6)
union all
select * from (select 'emp_top_n_lob', el.SESSION_ID, null, null, null, emp.amt, el.n_lob, round(emp.amt / nullif(el.n_lob,0)), coalesce(emp.nm, (select max(EMPLOYER_NAME) from e where e.EMPLOYER_ID = el.EMPLOYER_ID))
  from el left join emp on emp.EMPLOYER_ID = el.EMPLOYER_ID and emp.SESSION_ID = el.SESSION_ID order by el.n_lob desc limit 6)
union all
select * from (select 'firm_top_per_lob', fl.SESSION_ID, null, null, null, firm.amt, fl.n_lob, round(firm.amt / fl.n_lob), firm.nm
  from fl join firm on firm.FIRM_ID = fl.FIRM_ID and firm.SESSION_ID = fl.SESSION_ID where firm.amt > 0 order by firm.amt / fl.n_lob desc limit 6)
union all
select 'mover', f.SESSION_ID, null, null, null, null, null, null,
  f.LOBBYIST_FIRST_NAME||' '||f.LOBBYIST_LAST_NAME||': in-house '||listagg(distinct e.SESSION_ID||' '||e.EMPLOYER_NAME, ' / ')||' -> firm '||f.FIRM_NAME
from f join e on e.LOBBYIST_ID = f.LOBBYIST_ID group by f.SESSION_ID, f.LOBBYIST_ID, f.LOBBYIST_FIRST_NAME, f.LOBBYIST_LAST_NAME, f.FIRM_NAME
union all
select 'emp_id_many_names', SESSION_ID, count(distinct EMPLOYER_NAME), null, null, null, null, null, EMPLOYER_ID||': '||listagg(distinct EMPLOYER_NAME, ' | ')
from e group by SESSION_ID, EMPLOYER_ID having count(distinct EMPLOYER_NAME) > 1 qualify row_number() over (order by count(distinct EMPLOYER_NAME) desc) <= 5
order by 1, 2;

-- ===== connection: b4.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q16_judge_senior_timing_windows] (0.7s)
-- Same test as q14, tightened: eligible on inauguration day (age 65+, age+service 80+), first 17 months of each presidency (Trump2 has only ~17 months of data) and full term; circuit spread of the goers; other exits counted separately
with pres as (select column1 pname, column2 pparty, column3::date s, column4::date e from values
   ('Carter','Democratic','1977-01-20','1981-01-20'), ('Reagan','Republican','1981-01-20','1989-01-20'), ('Bush41','Republican','1989-01-20','1993-01-20'),
   ('Clinton','Democratic','1993-01-20','2001-01-20'), ('Bush43','Republican','2001-01-20','2009-01-20'), ('Obama','Democratic','2009-01-20','2017-01-20'),
   ('Trump1','Republican','2017-01-20','2021-01-20'), ('Biden','Democratic','2021-01-20','2025-01-20'), ('Trump2','Republican','2025-01-20','2026-09-01')),
s as (select sv.NID, sv.COURT_NAME, sv.PARTY_OF_APPOINTING_PRESIDENT pa, sv.COMMISSION_DATE cd, sv.SENIOR_STATUS_DATE sd, sv.TERMINATION_DATE td, fj.BIRTH_YEAR by_
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE sv join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE fj on fj.NID = sv.NID
      where sv.COURT_TYPE ilike '%Appeals%'),
hz as (select max(greatest(coalesce(cd,'1900-01-01'::date), coalesce(sd,'1900-01-01'::date), coalesce(td,'1900-01-01'::date))) horizon from s),
pool as (select p.pname, p.pparty, p.s, p.e, dateadd(month, 17, p.s) e17, s.*, iff(s.pa = p.pparty, 'same', 'other') rel,
           iff(s.sd >= p.s and s.sd < dateadd(month, 17, p.s), 1, 0) went17,
           iff(s.sd >= p.s and s.sd < p.e, 1, 0) went_full,
           iff(s.sd is null and s.td >= p.s and s.td < p.e, 1, 0) other_exit_full
         from pres p join s on s.cd < p.s and coalesce(s.sd, '9999-12-31'::date) >= p.s and coalesce(s.td, '9999-12-31'::date) >= p.s
         where s.pa in ('Republican','Democratic')
           and (year(p.s) - s.by_) >= 65 and (year(p.s) - s.by_) + datediff(year, s.cd, p.s) >= 80),
circ as (select pname, rel, COURT_NAME, sum(went_full) g from pool group by 1,2,3)
select pool.pname, min(pool.s) term_start, pool.rel, count(*) n_eligible_day1,
  sum(went17) went_17m, round(sum(went17) / count(*), 3) rate_17m,
  sum(went_full) went_full, round(sum(went_full) / count(*), 3) rate_full, sum(other_exit_full) other_exits_full,
  (select count(*) from circ where circ.pname = pool.pname and circ.rel = pool.rel and circ.g > 0) n_circuits_with_goers,
  (select max(g) from circ where circ.pname = pool.pname and circ.rel = pool.rel) max_goers_one_circuit,
  max(hz.horizon)::string data_horizon
from pool cross join hz group by pool.pname, pool.rel order by 2, 3 desc;

-- [q17_house_competitiveness_by_year] (0.5s)
-- House general elections per year: no real opponent (runner-up under 5%), 40-point landslides, races under 5 points; fusion lines summed per candidate, blank/scattering lines dropped
with h as (select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_HOUSE_RETURNS
           where STAGE = 'gen' and not IS_SPECIAL_ELECTION and not IS_RUNOFF
             and not (CANDIDATE_NAME ilike '%scatter%' or CANDIDATE_NAME ilike '%blank%' or CANDIDATE_NAME ilike '%void%' or CANDIDATE_NAME ilike '%over vote%' or CANDIDATE_NAME ilike '%under vote%')),
c as (select ELECTION_YEAR yr, STATE_ABBR st, DISTRICT dist, CANDIDATE_NAME cand, sum(CANDIDATE_VOTES) v, max(TOTAL_VOTES) tv from h group by 1,2,3,4),
rc as (select yr, st, dist, max(tv) tv, max(iff(rk = 1, v, 0)) / nullif(max(tv),0) w, max(iff(rk = 2, v, 0)) / nullif(max(tv),0) ru
       from (select c.*, row_number() over (partition by yr, st, dist order by v desc) rk from c) group by 1,2,3)
select yr, count(*) n_races,
  sum(iff(ru < 0.05 or ru is null,1,0)) n_no_opponent,
  sum(iff(w - ru >= 0.40,1,0)) n_margin_40plus,
  sum(iff(w - ru < 0.05,1,0)) n_margin_under5,
  sum(iff(tv <= 1,1,0)) n_filler_total,
  round(median(w - ru),3) med_margin
from rc group by 1 order by 1;

-- [q18_ca_lobby_name_fields] (0.5s)
-- CA lobbyist tables: how often the employer/firm name field holds the lobbyist's own surname
select 'emp' src, SESSION_ID, count(*) n,
  sum(iff(upper(trim(EMPLOYER_NAME)) = upper(trim(LOBBYIST_LAST_NAME)),1,0)) n_name_is_lobbyist_surname,
  sum(iff(upper(EMPLOYER_NAME) like upper(trim(LOBBYIST_LAST_NAME))||',%',1,0)) n_name_starts_surname_comma,
  count(distinct EMPLOYER_ID) n_ids, count(distinct EMPLOYER_NAME) n_names
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMP_LOBBYIST group by 1,2
union all
select 'firm', SESSION_ID, count(*),
  sum(iff(upper(trim(FIRM_NAME)) = upper(trim(LOBBYIST_LAST_NAME)),1,0)),
  sum(iff(upper(FIRM_NAME) like upper(trim(LOBBYIST_LAST_NAME))||',%',1,0)),
  count(distinct FIRM_ID), count(distinct FIRM_NAME)
from LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM_LOBBYIST group by 1,2
order by 1,2;

-- ===== connection: b5.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q19_judge_timing_robustness] (0.5s)
-- Robustness for the senior-status gap: per-circuit spread, age and service of the eligible pools, and what the "waiters" did once the White House changed party
with pres as (select column1 pname, column2 pparty, column3::date s, column4::date e from values
   ('Obama','Democratic','2009-01-20','2017-01-20'), ('Trump1','Republican','2017-01-20','2021-01-20'), ('Biden','Democratic','2021-01-20','2025-01-20'), ('Trump2','Republican','2025-01-20','2026-09-01')),
s as (select sv.NID, sv.COURT_NAME, sv.PARTY_OF_APPOINTING_PRESIDENT pa, sv.COMMISSION_DATE cd, sv.SENIOR_STATUS_DATE sd, sv.TERMINATION_DATE td, sv.TERMINATION term, fj.BIRTH_YEAR by_, fj.FULL_NAME fname
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE sv join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE fj on fj.NID = sv.NID
      where sv.COURT_TYPE ilike '%Appeals%'),
pool as (select p.pname, p.pparty, p.s, p.e, s.*, iff(s.pa = p.pparty, 'same', 'other') rel,
           iff(s.sd >= p.s and s.sd < p.e, 1, 0) went, year(p.s) - s.by_ age0, datediff(year, s.cd, p.s) svc0
         from pres p join s on s.cd < p.s and coalesce(s.sd, '9999-12-31'::date) >= p.s and coalesce(s.td, '9999-12-31'::date) >= p.s
         where s.pa in ('Republican','Democratic')
           and (year(p.s) - s.by_) >= 65 and (year(p.s) - s.by_) + datediff(year, s.cd, p.s) >= 80)
select 'circuit' k, pname, rel, regexp_replace(COURT_NAME, 'U.S. Court of Appeals for the ', '') c1, count(*)::string c2, sum(went)::string c3, null c4
from pool where pname in ('Trump1','Biden') group by 2,3,4
union all
select 'age', pname, rel, 'median age / service yrs / n', median(age0)::string, median(svc0)::string, count(*)::string from pool group by 2,3
union all
select 'waiters', pname, rel, 'stayed through term, still active at next inauguration',
  count(*)::string,
  sum(iff(sd >= e and sd < dateadd(month, 17, e),1,0))::string,
  sum(iff(sd >= e,1,0))::string || ' went senior after; ' || sum(iff(sd is null and td >= e,1,0))::string || ' left another way; ' || sum(iff(sd is null and td is null,1,0))::string || ' still active'
from pool where went = 0 and rel = 'other' and pname in ('Obama','Trump1','Biden')
  and coalesce(sd, '9999-12-31'::date) >= e and coalesce(td, '9999-12-31'::date) >= e
group by 2,3
union all
select 'waiter_names_biden', pname, rel, fname, regexp_replace(COURT_NAME, 'U.S. Court of Appeals for the ', ''), by_::string,
  coalesce('senior ' || sd::string, 'left ' || td::string || ' ' || term, 'active')
from pool where pname = 'Biden' and rel = 'other' and went = 0
order by 1, 2, 3, 5 desc;

-- ===== connection: b6.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q20_judge_timing_age_bands] (0.9s)
-- Dull-explanation test: the same-party pool is 1.5-2 years older. Senior-status rate inside age bands (age on inauguration day), eligible judges only
with pres as (select column1 pname, column2 pparty, column3::date s, column4::date e from values
   ('Bush43','Republican','2001-01-20','2009-01-20'), ('Obama','Democratic','2009-01-20','2017-01-20'), ('Trump1','Republican','2017-01-20','2021-01-20'), ('Biden','Democratic','2021-01-20','2025-01-20')),
s as (select sv.NID, sv.PARTY_OF_APPOINTING_PRESIDENT pa, sv.COMMISSION_DATE cd, sv.SENIOR_STATUS_DATE sd, sv.TERMINATION_DATE td, fj.BIRTH_YEAR by_
      from LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE sv join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE fj on fj.NID = sv.NID
      where sv.COURT_TYPE ilike '%Appeals%'),
pool as (select p.pname, p.s, iff(s.pa = p.pparty, 'same', 'other') rel, iff(s.sd >= p.s and s.sd < p.e, 1, 0) went, year(p.s) - s.by_ age0
         from pres p join s on s.cd < p.s and coalesce(s.sd, '9999-12-31'::date) >= p.s and coalesce(s.td, '9999-12-31'::date) >= p.s
         where s.pa in ('Republican','Democratic')
           and (year(p.s) - s.by_) >= 65 and (year(p.s) - s.by_) + datediff(year, s.cd, p.s) >= 80)
select pname, min(s) term_start, case when age0 < 70 then 'a 65-69' when age0 < 75 then 'b 70-74' else 'c 75+' end band,
  sum(iff(rel = 'same', 1, 0)) n_same, sum(iff(rel = 'same', went, 0)) went_same,
  sum(iff(rel = 'other', 1, 0)) n_other, sum(iff(rel = 'other', went, 0)) went_other
from pool group by 1, 3 order by 2, 3;

-- ===== totals
-- 33 of 35 statements: 21 SELECTs (q05 failed to compile and was rerun as q05b) + 12 session-setup lines over 6 connections.
-- Offline, no warehouse: two-sided Fisher exact tests on q16 counts, computed in Python with math.comb.
--   Biden 28/38 vs 6/28 p=4.6e-05 | Trump1 16/40 vs 4/31 p=0.016 | Obama 12/25 vs 10/30 p=0.29
--   Biden without the Ninth Circuit 21/28 vs 6/25 p=0.0003 | Trump1 without the Sixth 12/35 vs 4/28 p=0.087
--   Waiters, first 17 months: Biden-era 8/26 vs Trump2-era 1/21 p=0.03 (Benton went senior 2026-06-21, one day past 17 months; counting him, 2/21 gives p=0.15)
