-- @fjc_nid_check
-- Crosswalk FJC_NID against the FJC judge table: land rate, and is each id the right person (birth year vs first term)?
select x.JUSTICE_NAME, x.JUSTICE_CODE, x.FIRST_TERM, x.FJC_NID, x.MATCH_METHOD, x.CONFIDENCE,
       j.NID, j.FULL_NAME, j.SUFFIX, j.BIRTH_YEAR, j.DEATH_YEAR,
       (select count(*) from LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE jj where jj.LAST_NAME = x.FJC_LAST_NAME) same_surname_judges
from LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK x
left join LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j on to_varchar(j.NID) = to_varchar(x.FJC_NID)
order by x.FIRST_TERM, x.JUSTICE_CODE;

-- @eain_fd_to_fec
-- IRS 527 "FD" (federal) election IDs: how many look like FEC committee ids, and how many land on the FEC committee table
with e as (
  select distinct upper(regexp_replace(ELECTION_AUTHORITY_ID_NUMBER, '[^A-Za-z0-9]', '')) id
  from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_EAIN where STATE_ISSUED = 'FD'),
f as (select distinct CMTE_ID from LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE)
select count(*) ids, sum(iff(regexp_like(e.id, 'C[0-9]{8}'), 1, 0)) fec_shaped,
  sum(iff(f.CMTE_ID is not null, 1, 0)) landed,
  sum(iff(regexp_like(e.id, '[0-9]{9}'), 1, 0)) ein_shaped
from e left join f on f.CMTE_ID = e.id;

-- @voeten_country_session
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

-- @vv_member_month_breaks
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
