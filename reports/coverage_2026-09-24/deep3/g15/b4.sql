-- [q16_judge_senior_timing_windows]
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

-- [q17_house_competitiveness_by_year]
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

-- [q18_ca_lobby_name_fields]
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
