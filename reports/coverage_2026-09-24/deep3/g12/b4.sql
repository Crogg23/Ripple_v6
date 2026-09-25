-- [q23_absence_streaks_118_119]
-- Longest unbroken run of missed roll calls per member (cast code 9), with dates, and whether it runs to the member's last roll; peer = median over all members, same chamber and Congress
with v as (
  select v.CONGRESS, v.CHAMBER, v.ICPSR, v.ROLLNUMBER, r.VOTE_DATE, iff(v.CAST_CODE = 9,1,0) m
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
  join LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS r on r.CONGRESS = v.CONGRESS and r.CHAMBER = v.CHAMBER and r.ROLLNUMBER = v.ROLLNUMBER),
g as (
  select *, row_number() over (partition by CONGRESS, CHAMBER, ICPSR order by ROLLNUMBER)
          - row_number() over (partition by CONGRESS, CHAMBER, ICPSR, m order by ROLLNUMBER) grp
  from v),
runs as (
  select CONGRESS, CHAMBER, ICPSR, grp, count(*) len, min(VOTE_DATE) d0, max(VOTE_DATE) d1, max(ROLLNUMBER) end_roll
  from g where m = 1 group by 1,2,3,4),
best as (select * from runs qualify row_number() over (partition by CONGRESS, CHAMBER, ICPSR order by len desc, end_roll desc) = 1),
mem as (
  select CONGRESS, CHAMBER, ICPSR, max(ROLLNUMBER) last_row_roll, count(*) rolls, sum(m) missed, max(iff(m = 0, VOTE_DATE, null)) last_cast_date
  from v group by 1,2,3),
mm as (
  select CONGRESS, CHAMBER, try_to_double(ICPSR)::number icpsr, BIONAME, BIOGUIDE_ID, STATE_ABBREV, PARTY_CODE
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS where CONGRESS in (118,119) and CHAMBER in ('House','Senate')),
x as (
  select mem.*, coalesce(b.len,0) max_streak, b.d0, b.d1, (b.end_roll = mem.last_row_roll) trailing,
    mm.BIONAME, mm.BIOGUIDE_ID, mm.STATE_ABBREV, mm.PARTY_CODE
  from mem left join best b on b.CONGRESS = mem.CONGRESS and b.CHAMBER = mem.CHAMBER and b.ICPSR = mem.ICPSR
  left join mm on mm.CONGRESS = mem.CONGRESS and mm.CHAMBER = mem.CHAMBER and mm.icpsr = mem.ICPSR
  where coalesce(mm.STATE_ABBREV,'') not in ('AS','GU','PR','MP','VI','DC')),
y as (
  select x.*, median(max_streak) over (partition by CONGRESS, CHAMBER) med_streak,
    percentile_cont(0.9) within group (order by max_streak) over (partition by CONGRESS, CHAMBER) p90_streak,
    count(*) over (partition by CONGRESS, CHAMBER) n_members,
    rank() over (partition by CONGRESS, CHAMBER order by max_streak desc) rk
  from x)
select CONGRESS, CHAMBER, rk, BIONAME, BIOGUIDE_ID, STATE_ABBREV, PARTY_CODE, max_streak, d0, d1, trailing, rolls, missed, last_cast_date, med_streak, p90_streak, n_members
from y where rk <= 10 order by CONGRESS, CHAMBER, rk;

-- [q24_bills_118_floor_peer]
-- 118th, law-eligible: real advancement = LATEST_STAGE reached_floor or later; flag vs stage; peer = chamber + party
with m as (
  select SPONSOR_BIOGUIDE bio, iff(upper(BILL_TYPE) in ('HR','HJRES'),'House','Senate') ch, max(SPONSOR_NAME) nm,
    mode(regexp_substr(SPONSOR_NAME, '\\[([A-Z]+)-', 1, 1, 'e', 1)) party, count(*) bills,
    sum(iff(LATEST_STAGE in ('reached_floor','passed_both_to_president','became_law'),1,0)) floor,
    sum(iff(ADVANCED_PAST_COMMITTEE,1,0)) adv_flag, sum(iff(BECAME_LAW,1,0)) laws
  from LIBRARY_MARTS.POLITICS.POLITICS__BILLS where CONGRESS = 118 and IS_LAW_ELIGIBLE group by 1,2),
p as (
  select ch, party, count(*) members, median(bills) med_bills, median(floor) med_floor, round(sum(floor)/sum(bills),4) pooled_floor_rate,
    median(adv_flag) med_adv_flag, round(sum(adv_flag)/sum(bills),4) pooled_adv_flag_rate, sum(iff(floor = 0,1,0)) zero_floor,
    sum(iff(floor = 0 and bills >= 40,1,0)) zero_floor_40plus
  from m group by 1,2),
r as (select m.*, rank() over (partition by ch order by bills desc) rk from m where floor = 0)
select 'a_peer' kind, ch, party, null bio, null nm, members, med_bills bills, med_floor floor, pooled_floor_rate, med_adv_flag adv_flag, pooled_adv_flag_rate, zero_floor, zero_floor_40plus, null laws, null rk
from p where members >= 3
union all
select 'b_zero_floor', ch, party, bio, nm, null, bills, floor, null, adv_flag, null, null, null, laws, rk from r where rk <= 8
order by kind, ch, rk, party;
