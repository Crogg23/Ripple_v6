-- @fjc_all
-- FJC SCOTUS crosswalk: whole table (40 rows). Is it a lookup? Do the two Jacksons get two FJC ids?
select * from LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK order by FIRST_TERM, JUSTICE_CODE;

-- @eain_by_state
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

-- @eain_shared_ids
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

-- @medsl_all
-- MEDSL president returns: whole table (3,740 rows)
select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_MEDSL_PRESIDENT_RETURNS;

-- @voeten_by_session
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

-- @vv_cast_profile
-- Voteview votes: cast code x position x Congress x chamber; PROB fill and range; duplicate key check
select CONGRESS, CHAMBER, CAST_CODE, VOTE_POSITION, count(*) n, count(PROB) prob_n,
  min(PROB) pmin, max(PROB) pmax, round(median(PROB), 1) pmed, sum(iff(PROB < 50, 1, 0)) p_lt50, sum(iff(PROB < 10, 1, 0)) p_lt10,
  count(distinct ICPSR) members,
  count(distinct ROLLNUMBER || '|' || ICPSR) keys
from LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES
group by 1, 2, 3, 4 order by 1, 2, 3, 4;
