-- [q01_cmte_by_congress]
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

-- [q02_pac_money_coverage]
-- MEMBER_PAC_MONEY coverage by cycle, and how many 118th House full-committee members it reaches
with cm as (select distinct BIOGUIDE from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP where CONGRESS = '118' and COMMITTEE_CODE like 'H%' and IS_SUBCOMMITTEE ilike 'false')
select p.CYCLE, count(*) n, count(distinct p.BIOGUIDE) n_members, sum(p.PAC_DONATIONS) pac_sum, median(p.PAC_DONATIONS) pac_med,
  max(p.PAC_DONATIONS) pac_max, sum(iff(p.PAC_DONATIONS is null or p.PAC_DONATIONS = 0,1,0)) n_zero,
  count(distinct iff(cm.BIOGUIDE is not null, p.BIOGUIDE, null)) n_in_118_house_cmte,
  (select count(*) from cm) n_118_house_cmte_members
from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_PAC_MONEY p left join cm on cm.BIOGUIDE = p.BIOGUIDE
group by 1 order by 1;

-- [q03_ca_lobby_profile]
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

-- [q04_judge_jcs_profile]
-- Judge ideology table: circuits, distinct scores, how many judges share a score, duplicate names
with j as (select * from LIBRARY_MARTS.POLITICS.POLITICS__JUDGE_IDEOLOGY_COA),
v as (select JCS, count(*) n from j group by 1)
select 'circuit' k, CIRCUIT::string val, count(*) n, round(median(JCS),3) med, round(min(JCS),3) mn, round(max(JCS),3) mx, null extra from j group by 2
union all select 'score_top', JCS::string, n, null, null, null, null from (select * from v order by n desc limit 15)
union all select 'score_stats', 'distinct', (select count(*) from v), (select count(*) from v where n = 1), (select sum(n) from v where n >= 5), (select count(*) from j where JCS is null), null
union all select 'dup_name', JCS_JUDGE_NAME, count(*), null, null, null, listagg(CIRCUIT::string||':'||JCS::string, ' ') from j group by JCS_JUDGE_NAME having count(*) > 1
union all select 'sample', JCS_JUDGE_NAME, CIRCUIT, JCS, null, null, null from (select * from j order by random() limit 12)
order by 1, 3 desc;

-- [q05_house_returns_by_year]
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
