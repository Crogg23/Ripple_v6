-- [q05b_house_returns_by_year]
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

-- [q06_pac_outliers]
-- Top PAC totals per cycle with names, to see what the $29.3M max is
select * from (
select p.CYCLE, p.BIOGUIDE, s.FULL_NAME, s.STATE, s.LAST_TERM_TYPE, p.PAC_DONATIONS, p.N_PAC_DONORS, p.OUTSIDE_FOR,
  row_number() over (partition by p.CYCLE order by p.PAC_DONATIONS desc nulls last) rk
from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_PAC_MONEY p left join LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE s on s.BIOGUIDE = p.BIOGUIDE)
where rk <= 8 order by CYCLE, rk;

-- [q07_cmte_titles]
-- Leadership titles by chamber and side, full committees vs subcommittees
select left(COMMITTEE_CODE,1) chamber, IS_SUBCOMMITTEE, PARTY, TITLE, count(*) n, count(distinct CONGRESS) n_congresses
from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
where nullif(trim(TITLE),'') is not null
group by 1,2,3,4 order by 1,2,3,5 desc;

-- [q08_cmte_roster_completeness]
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

-- [q09_judge_fjc_join]
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

-- [q10_cmte_new_chairs_pac]
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
