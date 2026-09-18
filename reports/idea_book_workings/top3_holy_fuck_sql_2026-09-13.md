# The Idea Book — top 3 "holy fuck" what-ifs, SQL mapped

Written 2026-09-13. Picked from all 752 idea rows across the three chapters
(MONEY, HEALTH, PLACE). Column names were checked live against
LIBRARY_MARTS.INFORMATION_SCHEMA through the Python door on 2026-09-13.
Nothing below has been run. Every query is a map, not a result.

How the three were picked: never run, chain already verified, jaw-drop if true,
national scale, and the table is healthy (not a 3-year window, not capped).

| pick | book id | wonder score | why it is the one |
|---|---|---|---|
| 1 | M-056 | 240, rank 29 | 54.2M contributions reach 695 sitting members; 1.07M votes reach 635; windows overlap exactly |
| 2 | P-147 | 500, rank 4 | 9,504 mines changed controller; controller stamped on every one of 3.09M violations across 26 years |
| 3 | P-062 | crossjoin rank 3 | PWSID is a steel key with 45 edges; 15.4M violations; 14,700 homes with a ZIP |

---

## 1. Does the money arrive right before the vote? (M-056)

**The physical thing:** a cheque dated three days before a roll call.

**Chain, one hop per line, every column real:**

```
FINANCE__FED_FEC_INDIV_CONTRIBUTIONS.CMTE_ID
  ➔ FINANCE__FED_FEC_CAND_CMTE_LINKAGE.CMTE_ID → CAND_ID
  ➔ POLITICS__MEMBER_CROSSWALK.FEC_IDS (VARIANT array, flatten) → ICPSR
  ➔ POLITICS__VOTEVIEW_VOTES.ICPSR (+ CONGRESS, ROLLNUMBER)
  ➔ POLITICS__VOTEVIEW_ROLLCALLS.VOTE_DATE
```

**What a hit means:** for the average member, dollars in the 7 days before a roll
call run well above that member's own daily baseline, after quarter-end
deadline days are dropped.
**What a miss means:** the pre-vote window looks like any other week. Money
follows the calendar, not the docket.

**Traps carried in:** FEC_INDIV is 99.99% 2023-2026, so this is two congresses
(118, 119) only. Earmarks are TRANSACTION_TYPE 15E, exclude. Filing-deadline
eves are the known artefact (M-007), so the baseline excludes the last 3 days
of each quarter. FEC_IDS is a VARIANT array, must be flattened. Same-day
multiple roll calls collapse to one vote-day per member.

```sql
-- Step 1: member ↔ committee bridge (one row per committee, member)
with member_cmte as (
  select distinct x.ICPSR, x.BIOGUIDE, l.CMTE_ID
  from LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK x,
       lateral flatten(input => x.FEC_IDS) f
  join LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE l
    on l.CAND_ID = f.value::string
  where x.ICPSR is not null
    and l.CMTE_TP in ('H','S')          -- the campaign committee, not a PAC
    and l.CMTE_DSGN in ('P','A')        -- principal or authorized
),
-- Step 2: daily dollars per member, earmarks out
daily as (
  select m.ICPSR, c.TRANSACTION_DATE as d, sum(c.TRANSACTION_AMT) as amt, count(*) as n
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS c
  join member_cmte m on m.CMTE_ID = c.CMTE_ID
  where c.TRANSACTION_DATE between '2023-01-03' and '2026-06-30'
    and c.TRANSACTION_TYPE <> '15E'
    and c.TRANSACTION_AMT > 0
  group by 1,2
),
-- Step 3: one vote-day per member (many roll calls a day collapse)
vote_days as (
  select distinct v.ICPSR, r.VOTE_DATE
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
  join LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS r
    on r.CONGRESS = v.CONGRESS and r.CHAMBER = v.CHAMBER and r.ROLLNUMBER = v.ROLLNUMBER
  where v.CONGRESS in (118, 119)
    and v.CAST_CODE in (1,2,3,4,5,6)    -- actually voted, not absent
),
-- Step 4: tag each member-day as pre-vote (7 days before) or not
tagged as (
  select d.ICPSR, d.d, d.amt, d.n,
         exists (select 1 from vote_days vd
                 where vd.ICPSR = d.ICPSR
                   and d.d between dateadd(day,-7,vd.VOTE_DATE) and dateadd(day,-1,vd.VOTE_DATE)) as pre_vote,
         (day(d.d) >= 29 and month(d.d) in (3,6,9,12)) as deadline_eve
  from daily d
)
-- Step 5: per member, pre-vote daily average vs the rest, deadline eves out
select ICPSR,
       avg(iff(pre_vote, amt, null))      as pre_vote_daily_avg,
       avg(iff(not pre_vote, amt, null))  as other_daily_avg,
       div0(avg(iff(pre_vote, amt, null)), avg(iff(not pre_vote, amt, null))) as lift,
       count_if(pre_vote) as pre_vote_days, count_if(not pre_vote) as other_days
from tagged
where not deadline_eve
group by 1
having other_days >= 60
order by lift desc;
```

**The readout:** median `lift` across members. Above about 1.15 with the deadline
eves gone is the story. Then the follow-up is the same query with `vd.VOTE_DATE`
restricted to roll calls whose VOTE_DESC or BILL_NUMBER names a sector, and the
donor EMPLOYER matched to that sector. That second cut is where the name lands.

**Cost:** no prior run of this shape on the 283.8M-row table. No real number.
The 2023-2026 filter cuts it to roughly 84M rows; expect minutes, not hours.

---

## 2. Rename, and the record resets: does a mine's violation rate change when it changes hands? (P-147, wonder E10)

**The physical thing:** the same hole in the ground, a new company name on the
citation. The nursing-home version is dead (CHOW flag 'N' on all 14,700 rows).
Mines can do it because CONTROLLER_ID rides on every violation for 26 years.

**Chain:**

```
LABOR__FED_MSHA_VIOLATIONS (MINE_ID, CONTROLLER_ID, VIOLATION_ISSUE_DATE, EVENT_NO, SIG_SUB)
  ➔ handover = first VIOLATION_ISSUE_DATE where CONTROLLER_ID differs from the prior one, same MINE_ID
  ➔ LABOR__FED_MSHA_MINES (MINE_ID) for COAL_METAL_IND, STATE, NO_EMPLOYEES
```

**What a hit means:** significant-and-substantial (S&S) violations per inspection
day drop hard in the 24 months after the handover versus the 24 before, and
the drop is bigger than at matched mines that did not change hands.
**What a miss means:** the rate is flat across the handover. New name, same
mine, same citations.

**Traps carried in:** every MSHA value carries literal double quotes, strip them.
500,990 copy-paste rows exist, dedupe on VIOLATION_NO. EVENT_NO is the
inspection event, the honest denominator. MSHA_MINES holds the current
controller only, so the handover date comes from the violations table, not
the mines table. The trailing 24 months are inside the appeal window, exclude.

```sql
with v as (
  select replace(VIOLATION_NO,'"','') as violation_no,
         replace(MINE_ID,'"','')      as mine_id,
         replace(CONTROLLER_ID,'"','') as controller_id,
         replace(EVENT_NO,'"','')     as event_no,
         VIOLATION_ISSUE_DATE as issued,
         iff(replace(SIG_SUB,'"','') = 'Y' or IS_SIGNIFICANT_AND_SUBSTANTIAL, 1, 0) as ss
  from LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS
  where VIOLATION_ISSUE_DATE between '1996-01-01' and dateadd(month,-24,current_date)
  qualify row_number() over (partition by violation_no order by _LOADED_AT desc) = 1
),
-- the ordered controller sequence per mine
seq as (
  select mine_id, controller_id, issued,
         lag(controller_id) over (partition by mine_id order by issued, violation_no) as prev_controller
  from v
),
-- handover = first citation under a new controller
handovers as (
  select mine_id, controller_id as new_controller, prev_controller as old_controller,
         min(issued) as handover_date
  from seq
  where prev_controller is not null and controller_id <> prev_controller
  group by 1,2,3
),
-- before / after windows, 24 months each, per handover
windows as (
  select h.mine_id, h.old_controller, h.new_controller, h.handover_date,
         iff(v.issued < h.handover_date, 'before', 'after') as side,
         count(distinct v.event_no) as inspection_events,
         count(*) as violations,
         sum(v.ss) as ss_violations
  from handovers h
  join v on v.mine_id = h.mine_id
        and v.issued between dateadd(month,-24,h.handover_date) and dateadd(month,24,h.handover_date)
  group by 1,2,3,4,5
),
paired as (
  select mine_id, old_controller, new_controller, handover_date,
         max(iff(side='before', ss_violations, null)) as ss_before,
         max(iff(side='after',  ss_violations, null)) as ss_after,
         max(iff(side='before', inspection_events, null)) as ev_before,
         max(iff(side='after',  inspection_events, null)) as ev_after
  from windows group by 1,2,3,4
)
select m.COAL_METAL_IND, m.STATE,
       count(*) as handovers,
       median(div0(ss_before, ev_before)) as ss_per_event_before,
       median(div0(ss_after,  ev_after))  as ss_per_event_after,
       median(div0(div0(ss_after, ev_after), div0(ss_before, ev_before))) as median_ratio,
       count_if(div0(ss_after, ev_after) < 0.5 * div0(ss_before, ev_before)) as halved,
       count_if(div0(ss_after, ev_after) > 2.0 * div0(ss_before, ev_before)) as doubled
from paired p
join LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES m on replace(m.MINE_ID,'"','') = p.mine_id
where ev_before >= 5 and ev_after >= 5         -- enough inspections on both sides
group by 1,2
order by handovers desc;
```

**The readout:** `median_ratio` well under 1 says the record resets. Then run the
same thing with handovers replaced by a random date per never-sold mine, 20
draws, the same control the 2026-08-21 co-spike rule used. If the sold mines
drop and the controls do not, that is the finding. The named version: which
`old_controller` shows up as `new_controller` somewhere else within a year
(the shell shuffle).

**Cost:** the wonder-rankings verification pass counted controllers per mine
on this table in seconds. No prior run of the windowed version. Expect
well under a minute on 3.09M rows.

---

## 3. Who drinks from the failing pipe? (P-062, crossjoin build 3)

**The physical thing:** a nursing home whose tap water has failed health
standards for years, with the residents' count next to it.

**Chain:**

```
ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT (PWSID, IS_HEALTH_BASED_IND, NON_COMPL_PER_BEGIN_DATE)
  ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS (PWSID → ZIP_CODE_SERVED, AREA_TYPE_CODE = 'ZC')
  ➔ HEALTH__FED_CMS_NURSING_HOME (ZIP_CODE, PROVIDER_NAME, NUMBER_OF_RESIDENTS_IN_CERTIFIED_BEDS)
  ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS (PWSID → PWS_NAME, POPULATION_SERVED_COUNT)
```

**What a hit means:** a named home, its resident count, inside a system with
health-based violations in five or more distinct years, and no enforcement
row on most of them.
**What a miss means:** the chronic violators serve empty land or the ZIP hop
lands the homes in systems with paper violations only (monitoring, not
health).

**Traps carried in:** ZIP identifies nothing on its own, a ZIP can sit in more
than one PWSID and one PWSID serves many ZIPs. This query is a candidate list,
each row then needs the address checked against the system boundary. Health
violations are IS_HEALTH_BASED_IND = 'Y'; everything else is monitoring and
reporting. ENFORCEMENT_ID null means no action ever recorded. COUNTY_SERVED is
a bare name and leaks, do not use it here; the ZIP hop is the clean one.

```sql
with chronic as (
  select PWSID,
         count(distinct year(NON_COMPL_PER_BEGIN_DATE)) as viol_years,
         count(*) as health_viols,
         count_if(ENFORCEMENT_ID is null) as never_enforced,
         min(NON_COMPL_PER_BEGIN_DATE) as first_viol,
         max(coalesce(NON_COMPL_PER_END_DATE, current_date)) as last_viol,
         count_if(VIOLATION_STATUS in ('Unaddressed','Addressed')) as still_open
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  where IS_HEALTH_BASED_IND = 'Y'
    and NON_COMPL_PER_BEGIN_DATE >= '2010-01-01'
  group by 1
  having viol_years >= 5
),
zips as (
  select distinct PWSID, left(ZIP_CODE_SERVED,5) as zip5
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
  where AREA_TYPE_CODE = 'ZC' and ZIP_CODE_SERVED is not null
)
select nh.PROVIDER_NAME, nh.CITY, nh.STATE, nh.ZIP_CODE,
       nh.NUMBER_OF_RESIDENTS_IN_CERTIFIED_BEDS as residents,
       nh.OVERALL_RATING,
       pws.PWS_NAME, pws.POPULATION_SERVED_COUNT, pws.OWNER_TYPE_CODE,
       c.PWSID, c.viol_years, c.health_viols, c.never_enforced, c.still_open,
       c.first_viol, c.last_viol
from chronic c
join zips z   on z.PWSID = c.PWSID
join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME nh on left(nh.ZIP_CODE,5) = z.zip5
join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS pws
  on pws.PWSID = c.PWSID and pws.PWS_ACTIVITY_CODE = 'A'
qualify row_number() over (partition by nh.CMS_CERTIFICATION_NUMBER_CCN order by c.viol_years desc, c.health_viols desc) = 1
order by c.viol_years desc, residents desc
limit 200;
```

**The readout:** count of homes and residents on the list, then the top ten by
`viol_years` with `never_enforced` beside them. The map version shades every
PWSID by `viol_years` and drops the homes as dots. Clinics and subsidised
buildings are the same query with HRSA_UDS_SERVICE_DELIVERY_SITES and
HUD_ASSISTED_HOUSING_PROJECTS swapped in for the nursing-home table.

**Cost:** no prior run of this join. The violations scan is 15.4M rows filtered
to health-based; the other two tables are small. Expect under a minute.

---

## What is not in these three, and why

| left out | why |
|---|---|
| P-145 mine fines $548M never collected | already measured, rank 1; it is a result, not a what-if |
| H-106 state inspector 9.5x spread | already measured, rank 2 |
| P-079 2.93M EPA facilities never inspected | probed 2026-09-08, "strongest thing found", a wow pick already |
| H-165 new doctors billing $1.35B wound care | found, tier 1 lead |
| P-146 deaths without a paper trail | close fourth; approach written, needs the same 20-draw control as pick 2 |

Skeptic pass not yet run on this file. Status: looks mapped, not run.
