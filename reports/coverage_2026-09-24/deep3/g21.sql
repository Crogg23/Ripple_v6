-- g21 deep pass 3, 2026-09-24. Every statement run, in order, numbered.
-- Door: Python (connect/db.py). Read-only. Session setup on each connection (not counted):
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- ===== connection: b1.sql

-- [1] fjc_all
-- FJC SCOTUS crosswalk: whole table (40 rows). Is it a lookup? Do the two Jacksons get two FJC ids?
select * from LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK order by FIRST_TERM, JUSTICE_CODE;

-- [2] eain_by_state
-- IRS 527 election IDs per issuing state: forms, IDs, junk IDs, repeats, land rate on the 8871 org table
with e as (
  select trim(to_varchar(FORM_ID_NUMBER)) fid, trim(to_varchar(EAIN_ID)) eid, ELECTION_AUTHORITY_ID_NUMBER eaid, STATE_ISSUED st,
         _SOURCE_RUN_ID run, _INGESTED_AT ing,
         upper(regexp_replace(ELECTION_AUTHORITY_ID_NUMBER, '[^A-Za-z0-9]', '')) eaid_norm
  from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_EAIN),
o as (
  select trim(to_varchar(FORM_ID_NUMBER)) fid, max(EIN) ein, max(MAILING_STATE) mst, max(INSERT_DATETIME) ins
  from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS group by 1)
select coalesce(e.st, '(null)') st, count(*) n, count(distinct e.fid) forms, count(distinct e.fid || '|' || e.eid) form_line,
  count(distinct e.fid || '|' || coalesce(e.eaid_norm,'')) form_id_pairs,
  count(distinct e.eaid_norm) ids, count(distinct o.ein) eins,
  sum(iff(o.fid is null, 1, 0)) no_8871,
  sum(iff(e.eaid_norm is null or e.eaid_norm in ('', 'NA', 'NONE', 'N', '0', 'PENDING', 'APPLIEDFOR', 'TBD'), 1, 0)) junk_ids,
  sum(iff(o.mst = e.st, 1, 0)) mail_same_state,
  count(distinct e.run) runs, min(e.ing) ing_min, max(e.ing) ing_max, min(o.ins) ins_min, max(o.ins) ins_max
from e left join o on o.fid = e.fid
group by 1 order by 2 desc;

-- [3] eain_shared_ids
-- One state election ID listed by more than one 527 group (EIN): top 40, with names
with e as (
  select trim(to_varchar(FORM_ID_NUMBER)) fid, STATE_ISSUED st,
         upper(regexp_replace(ELECTION_AUTHORITY_ID_NUMBER, '[^A-Za-z0-9]', '')) eaid_norm
  from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_EAIN),
o as (
  select trim(to_varchar(FORM_ID_NUMBER)) fid, max(EIN) ein, max(ORGANIZATION_NAME) nm, max(MAILING_CITY) city, max(MAILING_STATE) mst
  from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS group by 1),
j as (
  select e.st, e.eaid_norm, o.ein, o.nm, o.city, o.mst from e join o on o.fid = e.fid
  where e.eaid_norm is not null and length(e.eaid_norm) >= 3 and e.eaid_norm not in ('NONE','PENDING','APPLIEDFOR','TBD')),
g as (
  select st, eaid_norm, count(distinct ein) eins, count(*) n,
         listagg(distinct left(nm, 60), ' || ') within group (order by left(nm, 60)) names
  from j group by 1, 2)
select (select count(*) from g) n_state_ids, (select count(*) from g where eins > 1) n_shared, g.*
from g where eins > 1 order by eins desc, n desc limit 40;

-- [4] medsl_all
-- MEDSL president returns: whole table (3,740 rows)
select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_PRESIDENT_RETURNS;

-- [5] voeten_by_session
-- Voeten UNGA dyads per session: rows, countries, pairs, both-direction check, text-number junk, agree range
select try_to_number(SESSION_X) s, min(YEAR) y0, max(YEAR) y1, count(*) n,
  count(distinct CCODE1) c1, count(distinct CCODE2) c2, count(distinct CCODE1 || '-' || CCODE2) pairs,
  sum(iff(try_to_number(CCODE1) < try_to_number(CCODE2), 1, 0)) lo_hi, sum(iff(try_to_number(CCODE1) > try_to_number(CCODE2), 1, 0)) hi_lo,
  sum(iff(CCODE1 = CCODE2, 1, 0)) self_pairs,
  sum(iff(try_to_number(CCODE1) is null, 1, 0)) c1_bad,
  sum(iff(try_to_double(AGREE) is null, 1, 0)) agree_bad,
  sum(iff(try_to_double(IDEALPOINTFP_X) is null, 1, 0)) ipx_bad,
  sum(iff(try_to_double(IDEALPOINTDISTANCE) is null, 1, 0)) ipd_bad,
  min(try_to_double(AGREE)) amin, max(try_to_double(AGREE)) amax, round(avg(try_to_double(AGREE)), 4) aavg,
  sum(iff(try_to_double(AGREE) = 1, 1, 0)) a1, sum(iff(try_to_double(AGREE) = 0, 1, 0)) a0,
  max(try_to_double(NVOTESFP_X)) nv_max, count(distinct COL_0) col0
from LIBRARY_MARTS.POLITICS.POLITICS__INTL_VOETEN_UNGA_VOTES
group by 1 order by 1;

-- [6] vv_cast_profile
-- Voteview votes: cast code x position x Congress x chamber; PROB fill and range; duplicate key check
select CONGRESS, CHAMBER, CAST_CODE, VOTE_POSITION, count(*) n, count(PROB) prob_n,
  min(PROB) pmin, max(PROB) pmax, round(median(PROB), 1) pmed, sum(iff(PROB < 50, 1, 0)) p_lt50, sum(iff(PROB < 10, 1, 0)) p_lt10,
  count(distinct ICPSR) members,
  count(distinct ROLLNUMBER || '|' || ICPSR) keys
from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES
group by 1, 2, 3, 4 order by 1, 2, 3, 4;

-- ===== connection: b2.sql

-- [7] fjc_nid_check
-- Crosswalk FJC_NID against the FJC judge table: land rate, and is each id the right person (birth year vs first term)?
select x.JUSTICE_NAME, x.JUSTICE_CODE, x.FIRST_TERM, x.FJC_NID, x.MATCH_METHOD, x.CONFIDENCE,
       j.NID, j.FULL_NAME, j.SUFFIX, j.BIRTH_YEAR, j.DEATH_YEAR,
       (select count(*) from LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE jj where jj.LAST_NAME = x.FJC_LAST_NAME) same_surname_judges
from LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK x
left join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j on to_varchar(j.NID) = to_varchar(x.FJC_NID)
order by x.FIRST_TERM, x.JUSTICE_CODE;

-- [8] eain_fd_to_fec
-- IRS 527 "FD" (federal) election IDs: how many look like FEC committee ids, and how many land on the FEC committee table
with e as (
  select distinct upper(regexp_replace(ELECTION_AUTHORITY_ID_NUMBER, '[^A-Za-z0-9]', '')) id
  from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_EAIN where STATE_ISSUED = 'FD'),
f as (select distinct CMTE_ID from LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE)
select count(*) ids, sum(iff(regexp_like(e.id, 'C[0-9]{8}'), 1, 0)) fec_shaped,
  sum(iff(f.CMTE_ID is not null, 1, 0)) landed,
  sum(iff(regexp_like(e.id, '[0-9]{9}'), 1, 0)) ein_shaped
from e left join f on f.CMTE_ID = e.id;

-- [9] voeten_country_session
-- Voeten: per country per session, mean agreement with everyone, agreement with 8 anchor countries, ideal point
select try_to_number(SESSION_X) s, YEAR y, try_to_number(CCODE1) c, count(*) n_partners,
  round(avg(try_to_double(AGREE)), 4) avg_all,
  max(iff(try_to_number(CCODE2) = 2,   try_to_double(AGREE), null)) ag_us,
  max(iff(try_to_number(CCODE2) = 710, try_to_double(AGREE), null)) ag_chn,
  max(iff(try_to_number(CCODE2) = 365, try_to_double(AGREE), null)) ag_rus,
  max(iff(try_to_number(CCODE2) = 666, try_to_double(AGREE), null)) ag_isr,
  max(iff(try_to_number(CCODE2) = 200, try_to_double(AGREE), null)) ag_uk,
  max(iff(try_to_number(CCODE2) = 220, try_to_double(AGREE), null)) ag_fra,
  max(iff(try_to_number(CCODE2) = 255, try_to_double(AGREE), null)) ag_ger,
  max(iff(try_to_number(CCODE2) = 750, try_to_double(AGREE), null)) ag_ind,
  max(try_to_double(IDEALPOINTFP_X)) ip, count(distinct IDEALPOINTFP_X) ip_vals, max(try_to_double(NVOTESFP_X)) nv
from LIBRARY_MARTS.POLITICS.POLITICS__INTL_VOETEN_UNGA_VOTES
group by 1, 2, 3;

-- [10] vv_member_month_breaks
-- Voteview 118th-119th: per member per month, yea/nay votes cast, party votes, votes against own-party majority,
-- votes the NOMINATE model called the other way (PROB < 50). Party: 200 = R, 100 or 328 (independents who caucus D) = D.
with m as (
  select CONGRESS, CHAMBER, try_to_double(ICPSR)::number icpsr, any_value(PARTY_CODE) party_code,
         any_value(BIONAME) nm, any_value(STATE_ABBREV) st, any_value(BIOGUIDE_ID) bio, any_value(DISTRICT_CODE) dist
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
  where CONGRESS in (118, 119) and CHAMBER in ('House', 'Senate') group by 1, 2, 3),
v as (
  select v.CONGRESS, v.CHAMBER, v.ROLLNUMBER rn, v.ICPSR, v.CAST_CODE cc, v.PROB,
         m.party_code, m.nm, m.st, m.bio, m.dist,
         case when try_to_number(to_varchar(m.party_code)) = 200 then 'R'
              when try_to_number(to_varchar(m.party_code)) in (100, 328) then 'D' else 'O' end p
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
  left join m on m.CONGRESS = v.CONGRESS and m.CHAMBER = v.CHAMBER and m.icpsr = v.ICPSR),
rc as (
  select CONGRESS, CHAMBER, rn,
    sum(iff(p = 'D' and cc = 1, 1, 0)) dy, sum(iff(p = 'D' and cc = 6, 1, 0)) dn,
    sum(iff(p = 'R' and cc = 1, 1, 0)) ry, sum(iff(p = 'R' and cc = 6, 1, 0)) rnay
  from v group by 1, 2, 3),
rc2 as (
  select CONGRESS, CHAMBER, rn,
    iff(dy > dn, 1, iff(dn > dy, 6, null)) dpos, iff(ry > rnay, 1, iff(rnay > ry, 6, null)) rpos
  from rc),
r as (
  select CONGRESS, CHAMBER, try_to_number(to_varchar(ROLLNUMBER)) rn, try_to_date(left(to_varchar(VOTE_DATE), 10)) d
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS where CONGRESS in (118, 119))
select v.CONGRESS, v.CHAMBER, v.ICPSR, v.p, v.party_code, v.nm, v.st, v.bio, v.dist, date_trunc('month', r.d) mon,
  count(*) rolls,
  sum(iff(v.cc in (1, 6), 1, 0)) yn,
  sum(iff(v.cc = 9, 1, 0)) nv,
  sum(iff(v.cc in (1, 6) and rc2.dpos is not null and rc2.rpos is not null and rc2.dpos <> rc2.rpos, 1, 0)) pv_yn,
  sum(iff(v.cc in (1, 6) and rc2.dpos is not null and rc2.rpos is not null and rc2.dpos <> rc2.rpos
          and v.cc <> iff(v.p = 'R', rc2.rpos, rc2.dpos), 1, 0)) pv_break,
  sum(iff(v.cc in (1, 6) and iff(v.p = 'R', rc2.rpos, rc2.dpos) is not null and v.cc <> iff(v.p = 'R', rc2.rpos, rc2.dpos), 1, 0)) any_break,
  sum(iff(v.cc in (1, 6) and v.PROB is not null, 1, 0)) prob_n,
  sum(iff(v.cc in (1, 6) and v.PROB < 50, 1, 0)) prob_lt50,
  sum(iff(r.rn is null, 1, 0)) no_date
from v join rc2 on rc2.CONGRESS = v.CONGRESS and rc2.CHAMBER = v.CHAMBER and rc2.rn = v.rn
left join r on r.CONGRESS = v.CONGRESS and r.CHAMBER = v.CHAMBER and r.rn = v.rn
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10;

-- ===== connection: b3.sql

-- [11] vv_rollcall_party_split
-- Voteview 118th-119th: one row per roll call. Yea/nay by party, and three named members' votes, with the question and description
-- (from the small roll-call table, falling back to the long roll-call table), to test whether vote mix explains the party-break drop.
with m as (
  select CONGRESS, CHAMBER, try_to_double(ICPSR)::number icpsr, any_value(PARTY_CODE) party_code, any_value(BIONAME) nm
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
  where CONGRESS in (118, 119) and CHAMBER in ('House', 'Senate') group by 1, 2, 3),
v as (
  select v.CONGRESS, v.CHAMBER, v.ROLLNUMBER rn, v.CAST_CODE cc, m.nm,
         case when try_to_number(to_varchar(m.party_code)) = 200 then 'R'
              when try_to_number(to_varchar(m.party_code)) in (100, 328) then 'D' else 'O' end p
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
  left join m on m.CONGRESS = v.CONGRESS and m.CHAMBER = v.CHAMBER and m.icpsr = v.ICPSR),
rc as (
  select CONGRESS, CHAMBER, rn,
    sum(iff(p = 'D' and cc = 1, 1, 0)) dy, sum(iff(p = 'D' and cc = 6, 1, 0)) dn,
    sum(iff(p = 'R' and cc = 1, 1, 0)) ry, sum(iff(p = 'R' and cc = 6, 1, 0)) rnay,
    max(iff(nm ilike 'FETTERMAN%', cc, null)) fett,
    max(iff(nm ilike 'CUELLAR%', cc, null)) cuel,
    max(iff(nm ilike 'FITZPATRICK%', cc, null)) fitz
  from v group by 1, 2, 3),
r as (
  select CONGRESS, CHAMBER, try_to_number(to_varchar(ROLLNUMBER)) rn, VOTE_DATE, VOTE_QUESTION, VOTE_RESULT, BILL_NUMBER, left(VOTE_DESC, 90) descr
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS where CONGRESS in (118, 119)),
mt as (
  select try_to_number(to_varchar(CONGRESS)) cg,
         case when lower(CHAMBER) in ('house', 'rep', 'h') then 'House' when lower(CHAMBER) in ('senate', 'sen', 's') then 'Senate' end ch,
         try_to_number(to_varchar(ROLLNUMBER)) rn, VOTE_QUESTION q2, left(DTL_DESC, 90) dtl
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META where try_to_number(to_varchar(CONGRESS)) in (118, 119))
select rc.*, r.VOTE_DATE, r.VOTE_QUESTION, mt.q2, r.VOTE_RESULT, r.BILL_NUMBER, r.descr, mt.dtl
from rc
left join r on r.CONGRESS = rc.CONGRESS and r.CHAMBER = rc.CHAMBER and r.rn = rc.rn
left join mt on mt.cg = rc.CONGRESS and mt.ch = rc.CHAMBER and mt.rn = rc.rn
order by 1, 2, 3;

-- [12] fjc_harlan_ids
-- Which FJC ids hold a Harlan? Is Justice Harlan II (born 1899) in the FJC table under another id?
select NID, JID, FULL_NAME, SUFFIX, BIRTH_YEAR, DEATH_YEAR
from LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE where LAST_NAME ilike 'Harlan%';

-- [13] who_won_president_years
-- Does another table carry 2020 and 2024 presidential results by state?
select OFFICE, YEAR, count(*) n, count(distinct STATE) states
from LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON
where OFFICE ilike '%pres%' group by 1, 2 order by 1, 2;

-- ===== connection: b4.sql

-- [14] vv_senate119_close_and_warpowers
-- 119th Senate: every war-powers roll call ("Armed Forces from hostilities") and every party vote decided by 3 or fewer,
-- with the tally by party, who crossed their party's majority, and who did not vote.
with m as (
  select try_to_double(ICPSR)::number icpsr, any_value(PARTY_CODE) party_code, any_value(BIONAME) nm, any_value(STATE_ABBREV) st
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
  where CONGRESS = 119 and CHAMBER = 'Senate' group by 1),
v as (
  select v.ROLLNUMBER rn, v.CAST_CODE cc, m.nm, m.st,
         case when try_to_number(to_varchar(m.party_code)) = 200 then 'R'
              when try_to_number(to_varchar(m.party_code)) in (100, 328) then 'D' else 'O' end p
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v
  left join m on m.icpsr = v.ICPSR
  where v.CONGRESS = 119 and v.CHAMBER = 'Senate'),
rc as (
  select rn,
    sum(iff(p = 'D' and cc = 1, 1, 0)) dy, sum(iff(p = 'D' and cc = 6, 1, 0)) dn,
    sum(iff(p = 'R' and cc = 1, 1, 0)) ry, sum(iff(p = 'R' and cc = 6, 1, 0)) rnay
  from v group by 1),
rc2 as (
  select rc.*, iff(dy > dn, 1, iff(dn > dy, 6, null)) dpos, iff(ry > rnay, 1, iff(rnay > ry, 6, null)) rpos from rc),
r as (
  select try_to_number(to_varchar(ROLLNUMBER)) rn, VOTE_DATE, VOTE_QUESTION, VOTE_RESULT, BILL_NUMBER, left(VOTE_DESC, 200) descr
  from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS where CONGRESS = 119 and CHAMBER = 'Senate'),
sel as (
  select rc2.*, r.VOTE_DATE, r.VOTE_QUESTION, r.VOTE_RESULT, r.BILL_NUMBER, r.descr
  from rc2 join r on r.rn = rc2.rn
  where r.descr ilike '%Armed Forces from hostilities%'
     or (dpos is not null and rpos is not null and dpos <> rpos and abs((dy + ry) - (dn + rnay)) <= 3))
select sel.rn, sel.VOTE_DATE, sel.VOTE_QUESTION, sel.VOTE_RESULT, sel.BILL_NUMBER, sel.descr, sel.dy, sel.dn, sel.ry, sel.rnay, sel.dpos, sel.rpos,
  listagg(case when v.cc in (1, 6) and v.cc <> iff(v.p = 'R', sel.rpos, sel.dpos) then v.nm || ' (' || v.p || '-' || v.st || ')' end, '; ') crossers,
  listagg(case when v.cc = 9 then v.nm || ' (' || v.p || ')' end, '; ') not_voting
from sel join v on v.rn = sel.rn
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
order by 1;

-- ===== connection: b5.sql

-- [15] voeten_eyeball_argentina
-- Eyeball the raw dyad rows behind the Argentina finding, both directions, sessions 76-79: Argentina-US, Argentina-Israel, UK-US
select SESSION_X, YEAR, CCODE1, CCODE2, AGREE, IDEALPOINTFP_X, NVOTESFP_X, IDEALPOINTFP_Y, NVOTESFP_Y, IDEALPOINTDISTANCE, COL_0
from LIBRARY_MARTS.POLITICS.POLITICS__INTL_VOETEN_UNGA_VOTES
where try_to_number(SESSION_X) between 76 and 79
  and ((CCODE1 = '160' and CCODE2 in ('2', '666')) or (CCODE1 = '2' and CCODE2 in ('160', '200')))
order by CCODE1, CCODE2, SESSION_X;
