-- [q11_freshmen_pac_by_committee]
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

-- [q12_cmte_seat_concentration]
-- Who holds the most roster rows in the 119th, and how many of those rows are ex officio seats
select BIOGUIDE, max(MEMBER_NAME) nm, left(max(COMMITTEE_CODE),1) chamber, count(*) n_rows,
  sum(iff(TITLE ilike 'ex officio',1,0)) n_ex_officio, sum(iff(IS_SUBCOMMITTEE ilike 'false',1,0)) n_full,
  count(*) - sum(iff(TITLE ilike 'ex officio',1,0)) n_voting_seats
from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
where CONGRESS = '119'
group by 1 qualify row_number() over (order by count(*) desc) <= 8
   or row_number() over (order by count(*) - sum(iff(TITLE ilike 'ex officio',1,0)) desc) <= 5
order by n_rows desc;

-- [q13_house_turnout_gap]
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

-- [q14_judge_senior_timing]
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

-- [q15_ca_lobby_links]
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
