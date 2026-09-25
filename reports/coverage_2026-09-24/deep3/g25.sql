-- deep3 / g25: proper look at five glance-only tables, 2026-09-24
-- Tables: FINANCE__FED_FHFA_FHLB_MEMBERSHIP, FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS,
--         FINANCE__INTL_ISO_MIC_REGISTRY, FINANCE__FED_FEC_CANDIDATES, FINANCE__FED_SEC_INSIDER_SUBMISSION
-- Door: Python (connect/db.py) via g25/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g25/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- FHLB membership: profile by member type: rows, certs, dates, stand-in dates, blank IDs, first/last member date
select MEM_TYPE, count(*) n, count(distinct FHFA_ID) fhfa_ids, count(distinct nullif(trim(CERT),'')) certs,
  count_if(nullif(trim(CERT),'') is null) cert_blank, count_if(nullif(trim(NAIC_ID),'') is not null) naic,
  count_if(nullif(trim(NCUA_ID),'') is not null) ncua, count_if(APPR_DATE is null) appr_null,
  count_if(MEM_DATE = '1989-12-31') mem_19891231, count_if(MEM_DATE is null) mem_null,
  min(MEM_DATE) mem_min, max(MEM_DATE) mem_max,
  count_if(year(MEM_DATE) between 2000 and 2007) m00_07, count_if(year(MEM_DATE) between 2008 and 2015) m08_15,
  count_if(year(MEM_DATE) between 2016 and 2019) m16_19, count_if(year(MEM_DATE) >= 2020) m20on,
  count(distinct _SOURCE_RUN_ID) runs, max(_LOADED_AT) loaded
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP
group by rollup(MEM_TYPE) order by n desc;

-- [q02] statement 2
-- EPA informal actions: by program x statute x action type, and date sanity
select PGM_SYS_ACRNM, STATUTE, ENF_TYPE_DESC, count(*) n, count(distinct REGISTRY_ID) facs,
  min(ACHIEVED_DATE) dmin, max(ACHIEVED_DATE) dmax, count_if(ACHIEVED_DATE is null) dnull,
  count_if(year(ACHIEVED_DATE) < 1990) pre1990, count(distinct ENF_IDENTIFIER) ids, count_if(REGISTRY_ID is null or trim(REGISTRY_ID)='') reg_blank
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
group by 1,2,3 order by n desc limit 40;

-- [q03] statement 3
-- EPA informal actions: same months (Jan-Jul) across years, by program; plus full-year totals
select year(ACHIEVED_DATE) yr, count(*) n_all, count_if(month(ACHIEVED_DATE) <= 7) jan_jul,
  count_if(PGM_SYS_ACRNM='ICIS' and month(ACHIEVED_DATE) <= 7) icis_jj, count_if(PGM_SYS_ACRNM='RCRAINFO' and month(ACHIEVED_DATE) <= 7) rcra_jj,
  count_if(PGM_SYS_ACRNM not in ('ICIS','RCRAINFO') and month(ACHIEVED_DATE) <= 7) other_jj,
  count(distinct REGISTRY_ID) facs
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
where year(ACHIEVED_DATE) >= 2008 group by 1 order by 1;

-- [q04] statement 4
-- ISO MIC registry: confirm it's a lookup: status x category, expiry years, comments words
select 'status' k, STATUS a, OPRT_SGMT b, count(*) n, count(distinct ISO_COUNTRY_CODE_ISO_3166) c from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY group by 2,3
union all select 'cat', MARKET_CATEGORY_CODE, null, count(*), count_if(STATUS='EXPIRED') from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY group by 2
union all select 'expyr', year(EXPIRY_DATE)::text, null, count(*), count(distinct ISO_COUNTRY_CODE_ISO_3166) from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY where EXPIRY_DATE is not null group by 2
union all select 'crtyr', year(CREATION_DATE)::text, null, count(*), count_if(STATUS='EXPIRED') from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY group by 2
union all select 'rows', count(*)::text, count(distinct MIC)::text, count(distinct LEI), count(distinct _SOURCE_RUN_ID) from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY
order by 1, 4 desc;

-- [q05] statement 5
-- FEC candidates: per election year x office: rows, candidates, status mix, blank PCC, placeholder ZIP, exact dup rows
select CAND_ELECTION_YR yr, CAND_OFFICE off, count(*) n, count(distinct CAND_ID) cands,
  count_if(CAND_STATUS='C') st_c, count_if(CAND_STATUS='F') st_f, count_if(CAND_STATUS='N') st_n, count_if(CAND_STATUS='P') st_p,
  count_if(CAND_PCC is null or trim(CAND_PCC)='') pcc_blank, count_if(CAND_ZIP like '00000%') zip0,
  count_if(CAND_ST <> CAND_OFFICE_ST and CAND_OFFICE in ('H','S')) mail_out_of_state,
  count(*) - count(distinct hash(CAND_ID, CAND_NAME, CAND_PTY_AFFILIATION, CAND_ELECTION_YR, CAND_OFFICE_ST, CAND_OFFICE, CAND_OFFICE_DISTRICT, CAND_ICI, CAND_STATUS, CAND_PCC, CAND_ST1, CAND_ST2, CAND_CITY, CAND_ST, CAND_ZIP)) exact_dups
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES
group by rollup(1,2) order by 1,2;

-- [q06] statement 6
-- SEC insider submission: filings per quarter by document type; filing lag vs period of report
select date_trunc('quarter', FILING_DATE)::date q, count(*) n,
  count_if(DOCUMENT_TYPE='4') f4, count_if(DOCUMENT_TYPE='3') f3, count_if(DOCUMENT_TYPE='5') f5, count_if(DOCUMENT_TYPE like '%/A') amend,
  count_if(DOCUMENT_TYPE='4' and datediff('day', PERIOD_OF_REPORT, FILING_DATE) > 5) f4_gt5d,
  count_if(DOCUMENT_TYPE='4' and datediff('day', PERIOD_OF_REPORT, FILING_DATE) > 30) f4_gt30d,
  count_if(DOCUMENT_TYPE='4' and datediff('day', PERIOD_OF_REPORT, FILING_DATE) < 0) f4_neg,
  count_if(NO_SECURITIES_OWNED) no_sec, count_if(NOT_SUBJECT_TO_SECTION16) not16, count_if(PERIOD_OF_REPORT is null) por_null,
  count(distinct ISSUER_CIK) issuers
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION
group by 1 order by 1;

-- [q07] statement 7
-- SEC insider: nonderivative transaction codes, and how many Form 4 accessions land in the transaction table
with t as (select ACCESSION_NUMBER, count(*) n, count_if(TRANSACTION_CODE in ('P','S')) nps from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS group by 1)
select 'code' k, TRANSACTION_CODE a, FORM_TYPE b, count(*) n, count(distinct ACCESSION_NUMBER) m,
  count_if(TRANSACTION_DATE is null) x, count_if(year(TRANSACTION_DATE) < 2000 or year(TRANSACTION_DATE) > 2026) y
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS group by 2,3
union all
select 'land', s.DOCUMENT_TYPE, null, count(*), count(t.ACCESSION_NUMBER), count_if(t.nps > 0), count_if(t.nps = t.n)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s left join t on t.ACCESSION_NUMBER = s.ACCESSION_NUMBER
group by 2
order by 1, 4 desc;

-- [q08] statement 8
-- SEC insider: Form 4s holding an open-market buy (P) or sale (S): days from the earliest P/S trade to filing, by filing year
with t as (
  select ACCESSION_NUMBER, min(case when TRANSACTION_CODE in ('P','S') then TRANSACTION_DATE end) ps_min,
    count_if(TRANSACTION_CODE in ('P','S')) nps, count_if(TRANSACTION_CODE = 'S') ns, count_if(TRANSACTION_CODE = 'P') np,
    sum(case when TRANSACTION_CODE in ('P','S') then TRANSACTION_VALUE end) ps_val
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS group by 1 having count_if(TRANSACTION_CODE in ('P','S')) > 0),
j as (select year(s.FILING_DATE) yr, datediff('day', t.ps_min, s.FILING_DATE) lag, t.*
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s join t on t.ACCESSION_NUMBER = s.ACCESSION_NUMBER
  where s.DOCUMENT_TYPE = '4')
select yr, count(*) ps_filings, count_if(np > 0) with_buy, count_if(ns > 0) with_sale,
  count_if(lag < 0) neg, count_if(lag between 0 and 5) ontime_0_5, count_if(lag between 6 and 10) d6_10,
  count_if(lag between 11 and 30) d11_30, count_if(lag between 31 and 365) d31_365, count_if(lag > 365) gt365,
  round(100 * count_if(lag between 11 and 365) / count(*), 2) pct_late_11_365,
  round(100 * count_if(np > 0 and lag between 11 and 365) / nullif(count_if(np > 0), 0), 2) pct_late_buy,
  round(100 * count_if(ns > 0 and lag between 11 and 365) / nullif(count_if(ns > 0), 0), 2) pct_late_sale,
  round(sum(case when lag between 11 and 365 then ps_val end) / 1e9, 2) late_val_bn, round(sum(ps_val) / 1e9, 1) all_val_bn
from j group by 1 order by 1;

-- [q09] statement 9
-- FHLB: future and stand-in member dates, and CERT join to FDIC bank data (active flag) and FDIC failed-bank list
with m as (select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP where nullif(trim(CERT),'') is not null),
b as (select try_to_number(CERT) c, max(ACTIVE) active, max(ENDEFYMD) endd, max(NAME) bname, max(ASSET) asset from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA group by 1),
f as (select try_to_number(FDIC_CERT) c, max(FAIL_DATE) fail_date, max(BANK_NAME) fname, max(TOTAL_ASSETS_THOUSANDS) fassets from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS group by 1)
select 'sum' k, count(*)::text a, count(b.c)::text b_, count_if(b.active='1')::text c_, count_if(b.active='0')::text d_,
  count(f.c)::text e_, count_if(m.MEM_DATE > current_date())::text f_, count_if(m.APPR_DATE > current_date())::text g_, null h_
from m left join b on b.c = try_to_number(m.CERT) left join f on f.c = try_to_number(m.CERT)
union all
select 'failed', m.MEMBER_NAME, m.CERT, m.DISTRICT, m.MEM_DATE::text, f.fail_date::text, f.fname, b.active, round(f.fassets/1e3)::text
from m join f on f.c = try_to_number(m.CERT)
union all
select 'future', m.MEMBER_NAME, m.CERT, m.MEM_TYPE, m.MEM_DATE::text, m.APPR_DATE::text, b.bname, b.active, b.endd::text
from m left join b on b.c = try_to_number(m.CERT) where m.MEM_DATE > current_date()
order by 1, 6;

-- [q10] statement 10
-- EPA informal: Jan-Jul 2022-2026 by statute, program, EPA region (first 2 chars of case number) and action type
select left(ENF_IDENTIFIER, 2) reg, STATUTE, PGM_SYS_ACRNM, ENF_TYPE_DESC,
  count_if(year(ACHIEVED_DATE)=2022 and month(ACHIEVED_DATE)<=7) y22, count_if(year(ACHIEVED_DATE)=2023 and month(ACHIEVED_DATE)<=7) y23,
  count_if(year(ACHIEVED_DATE)=2024 and month(ACHIEVED_DATE)<=7) y24, count_if(year(ACHIEVED_DATE)=2025 and month(ACHIEVED_DATE)<=7) y25,
  count_if(year(ACHIEVED_DATE)=2026 and month(ACHIEVED_DATE)<=7) y26, count(*) n_all
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
where year(ACHIEVED_DATE) between 2022 and 2026
group by 1,2,3,4 having count(*) >= 8 order by y26 desc, n_all desc limit 45;

-- [q11] statement 11
-- EPA informal: facilities with the most informal actions: name, state, span, statutes; ECHO formal actions and penalties; EPA formal case count
with i as (select REGISTRY_ID, count(*) n, count(distinct ENF_IDENTIFIER) ids, min(ACHIEVED_DATE) d0, max(ACHIEVED_DATE) d1,
  listagg(distinct STATUTE, ',') sts, listagg(distinct PGM_SYS_ACRNM, ',') pgms, count_if(ACHIEVED_DATE >= '2021-01-01') n_since21,
  max(left(ENF_IDENTIFIER,2)) reg
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS group by 1 order by n desc limit 30),
e as (select FRS_ID, max(FACILITY_NAME) nm, max(CITY) city, max(STATE) st, max(FORMAL_ACTION_COUNT) formal, max(TOTAL_PENALTIES) pen,
  max(INFORMAL_ACTION_COUNT) echo_inf, max(IS_ON_TRIBAL_LAND::int) tribal, max(HAS_DRINKING_WATER_PROGRAM::int) dw, count(*) echo_rows
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where FRS_ID in (select REGISTRY_ID from i) group by 1),
c as (select REGISTRY_ID, count(distinct CASE_NUMBER) cases, max(FACILITY_NAME) cnm, max(STATE_CODE) cst
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES where REGISTRY_ID in (select REGISTRY_ID from i) group by 1)
select i.*, e.nm, e.city, e.st, e.formal, e.pen, e.echo_inf, e.tribal, e.dw, e.echo_rows, c.cases, c.cnm, c.cst
from i left join e on e.FRS_ID = i.REGISTRY_ID left join c on c.REGISTRY_ID = i.REGISTRY_ID order by i.n desc;

-- [q12] statement 12
-- FHLB (rerun of q09 with the join fixed): CERT join to FDIC bank data (active flag) and FDIC failed-bank list; future member dates
with m as (select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP where nullif(trim(CERT),'') is not null),
b as (select try_to_number(CERT) c, max(ACTIVE) active, max(ENDEFYMD) endd, max(NAME) bname, max(ASSET) asset from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA group by 1),
f as (select try_to_number(FDIC_CERT) c, max(FAIL_DATE) fail_date, max(BANK_NAME) fname, max(TOTAL_ASSETS_THOUSANDS) fassets from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS group by 1)
select 'sum' k, count(*)::text a, count(b.c)::text b_, count_if(b.active='1')::text c_, count_if(b.active='0')::text d_,
  count(f.c)::text e_, count_if(m.MEM_DATE > current_date())::text f_, count_if(m.APPR_DATE > current_date())::text g_, listagg(distinct b.active, '|') h_
from m left join b on b.c = try_to_number(m.CERT) left join f on f.c = try_to_number(m.CERT)
union all
select 'failed', m.MEMBER_NAME, m.CERT, m.DISTRICT, m.MEM_DATE::text, f.fail_date::text, f.fname, b.active, round(f.fassets/1e3)::text
from m join f on f.c = try_to_number(m.CERT) left join b on b.c = try_to_number(m.CERT)
union all
select 'inactive', m.MEMBER_NAME, m.CERT, m.MEM_TYPE, m.MEM_DATE::text, b.endd::text, b.bname, b.active, round(b.asset/1e3)::text
from m join b on b.c = try_to_number(m.CERT) where b.active <> '1'
union all
select 'future', m.MEMBER_NAME, m.CERT, m.MEM_TYPE, m.MEM_DATE::text, m.APPR_DATE::text, b.bname, b.active, b.endd::text
from m left join b on b.c = try_to_number(m.CERT) where m.MEM_DATE > current_date()
order by 1, 6;

-- [q13] statement 13
-- FHLB: peer test. FDIC-supervised active banks (BKCLASS NM), FHLB member or not, by asset band: share with any FDIC order dated 2020 on
with b as (select try_to_number(CERT) c, max(ASSET) asset, max(BKCLASS) cls from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA where ACTIVE = '1' group by 1),
m as (select distinct try_to_number(CERT) c from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP where nullif(trim(CERT),'') is not null),
o as (select CERT_NUMBER c, count(*) n_orders, count_if(ORDER_TYPE ilike '%consent%' or ORDER_TYPE ilike '%cease%') n_cd, max(ORDER_DATE) last_order
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS where ORDER_DATE >= '2020-01-01' group by 1),
j as (select b.*, (m.c is not null) member, o.n_orders, o.n_cd,
  case when b.asset < 100000 then 'a <100M' when b.asset < 500000 then 'b 100-500M' when b.asset < 2000000 then 'c 500M-2B' else 'd 2B+' end band
  from b left join m on m.c = b.c left join o on o.c = b.c)
select 'rate' k, band, member::text mem, count(*) banks, count_if(n_orders > 0) any_order, count_if(n_cd > 0) cd_order,
  round(100 * count_if(n_orders > 0) / count(*), 1) pct_any, round(100 * count_if(n_cd > 0) / count(*), 1) pct_cd
from j where cls = 'NM' group by 2, 3
union all
select 'otype', ORDER_TYPE, ORDER_CATEGORY, count(*), count(distinct CERT_NUMBER), null, null, null
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS where ORDER_DATE >= '2020-01-01' group by 2, 3
order by 1, 2, 3;

-- [q14] statement 14
-- EPA informal: Region 6 SDWA notices via ICIS (the Osage-county injection wells), by year: rows vs distinct actions vs wells;
-- EPA inspections of the same wells by year (ICIS-FE&C inspections), and all EPA Region 6 SDWA inspections as control
with w as (select distinct REGISTRY_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS'),
inf as (select year(ACHIEVED_DATE) yr, count(*) rows_, count(distinct ENF_IDENTIFIER) actions, count(distinct REGISTRY_ID) wells
        from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
        where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS' group by 1),
ins as (select year(i.ACTUAL_BEGIN_DATE) yr, count(distinct iff(w.REGISTRY_ID is not null, i.ACTIVITY_ID, null)) insp_wells,
          count(distinct iff(w.REGISTRY_ID is not null, i.REGISTRY_ID, null)) wells_inspected,
          count(distinct iff(i.EPA_REGION_CODE = '06' and i.STATUTE_CODE ilike '%SDWA%', i.ACTIVITY_ID, null)) r6_sdwa_insp,
          count(distinct i.ACTIVITY_ID) all_insp
        from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS i left join w on w.REGISTRY_ID = i.REGISTRY_ID group by 1)
select coalesce(inf.yr, ins.yr) yr, inf.rows_, inf.actions, inf.wells, ins.insp_wells, ins.wells_inspected, ins.r6_sdwa_insp, ins.all_insp,
  (select count(*) from w) wells_total
from inf full outer join ins on ins.yr = inf.yr where coalesce(inf.yr, ins.yr) >= 2000 order by 1;

-- [q15] statement 15
-- EPA informal: the 2025-2026 jumps. Region 6 SFDW drinking-water notices and Region 5 FIFRA warning letters: who, where, on how many days
with x as (select i.*, case when left(ENF_IDENTIFIER,2)='06' and PGM_SYS_ACRNM='SFDW' then 'R6 SFDW' else 'R5 FIFRA' end grp
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS i
  where year(ACHIEVED_DATE) >= 2025 and ((left(ENF_IDENTIFIER,2)='06' and PGM_SYS_ACRNM='SFDW') or (left(ENF_IDENTIFIER,2)='05' and STATUTE='FIFRA'))),
e as (select FRS_ID, max(FACILITY_NAME) nm, max(STATE) st, max(IS_ON_TRIBAL_LAND::int) tribal from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
  where FRS_ID in (select REGISTRY_ID from x) group by 1)
select 'grp' k, grp a, null b, count(*) n, count(distinct ENF_IDENTIFIER) ids, count(distinct REGISTRY_ID) facs, count(distinct ACHIEVED_DATE) days,
  count(e.FRS_ID) echo_hit, sum(e.tribal) tribal, max(ACHIEVED_DATE)::text dmax
from x left join e on e.FRS_ID = x.REGISTRY_ID group by 2
union all
select 'st', grp, e.st, count(*), count(distinct ENF_IDENTIFIER), count(distinct REGISTRY_ID), count(distinct ACHIEVED_DATE), null, sum(e.tribal), null
from x left join e on e.FRS_ID = x.REGISTRY_ID group by 2, 3
union all
select 'day', grp, ACHIEVED_DATE::text, count(*), count(distinct ENF_IDENTIFIER), count(distinct REGISTRY_ID), null, null, null, null
from x group by 2, 3 qualify row_number() over (partition by grp order by count(*) desc) <= 5
union all
select 'name', grp, e.nm, count(*), count(distinct ENF_IDENTIFIER), count(distinct REGISTRY_ID), null, null, max(e.tribal), max(x.PGM_SYS_ID)
from x left join e on e.FRS_ID = x.REGISTRY_ID group by 2, 3 qualify row_number() over (partition by grp order by count(*) desc) <= 8
order by 1, 2, 4 desc;

-- [q16] statement 16
-- SEC insider: open-market SALES (code S) reported on Form 4 more than 10 days after the sale, by issuer. Peer = all issuers with 30+ sale filings.
-- Plus: late small buys (<= $10K, the Rule 16a-6 deferral) and a summary by exchange
with t as (select ACCESSION_NUMBER, min(case when TRANSACTION_CODE='S' then TRANSACTION_DATE end) s_min,
             min(case when TRANSACTION_CODE='P' then TRANSACTION_DATE end) p_min,
             sum(case when TRANSACTION_CODE='P' and PRICE_PER_SHARE between 0.01 and 5000 then SHARES*PRICE_PER_SHARE end) p_val,
             sum(case when TRANSACTION_CODE='S' and PRICE_PER_SHARE between 0.01 and 5000 then SHARES*PRICE_PER_SHARE end) s_val
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE in ('P','S') group by 1),
o as (select ACCESSION_NUMBER, min(OWNER_CIK) owner from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER group by 1),
s as (select sub.ISSUER_CIK, sub.ISSUER_NAME, sub.FILING_DATE, t.*, o.owner,
        datediff('day', t.s_min, sub.FILING_DATE) slag, datediff('day', t.p_min, sub.FILING_DATE) plag
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
      left join o on o.ACCESSION_NUMBER = sub.ACCESSION_NUMBER where sub.DOCUMENT_TYPE = '4'),
iss as (select ISSUER_CIK, max(ISSUER_NAME) nm, count_if(s_min is not null) sale_f, count_if(slag between 11 and 365) late_s,
          count(distinct iff(slag between 11 and 365, owner, null)) late_owners, count(distinct iff(s_min is not null, owner, null)) sale_owners,
          median(iff(slag between 11 and 365, slag, null)) med_late_days, round(sum(iff(slag between 11 and 365, s_val, 0))/1e6, 1) late_s_musd,
          count_if(slag between 11 and 365 and FILING_DATE >= '2023-10-01') late_s_post_sweep, count_if(s_min is not null and FILING_DATE >= '2023-10-01') sale_f_post,
          min(iff(slag between 11 and 365, FILING_DATE, null)) first_late, max(iff(slag between 11 and 365, FILING_DATE, null)) last_late
        from s group by 1),
pe as (select *, round(100*late_s/sale_f, 1) pct from iss where sale_f >= 30),
x as (select try_to_number(CIK) c, max(EXCHANGE) ex from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1)
select 'top' k, ISSUER_CIK a, nm b, sale_f n1, late_s n2, pct n3, late_owners n4, sale_owners n5, med_late_days n6, late_s_musd n7, late_s_post_sweep n8, sale_f_post n9, first_late::text c, last_late::text d
from pe qualify row_number() over (order by late_s desc) <= 25
union all
select 'toppct', ISSUER_CIK, nm, sale_f, late_s, pct, late_owners, sale_owners, med_late_days, late_s_musd, late_s_post_sweep, sale_f_post, first_late::text, last_late::text
from pe where sale_f >= 60 qualify row_number() over (order by pct desc) <= 15
union all
select 'peer', 'issuers 30+ sale filings', null, count(*), sum(late_s), round(100*sum(late_s)/sum(sale_f),2), median(pct), percentile_cont(0.9) within group (order by pct),
  count_if(pct = 0), count_if(pct >= 10), null, null, null, null from pe
union all
select 'exch', coalesce(x.ex, 'no ticker match'), null, sum(sale_f), sum(late_s), round(100*sum(late_s)/nullif(sum(sale_f),0),2), count(*), null, null, null, null, null, null, null
from iss left join x on x.c = try_to_number(iss.ISSUER_CIK) group by 2
union all
select 'buys', 'late buys 11-365d', null, count_if(p_min is not null), count_if(plag between 11 and 365), count_if(plag between 11 and 365 and p_val <= 10000),
  count_if(p_min is not null and p_val <= 10000), median(iff(plag between 11 and 365, p_val, null)), median(iff(p_min is not null, p_val, null)), null, null, null, null, null from s
order by 1, 5 desc;

-- [q17] statement 17
-- FEC candidates: one principal campaign committee named by several different candidates; one mailing address used by many candidates
with c as (select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES),
p as (select CAND_PCC, count(distinct CAND_ID) ids, count(distinct CAND_NAME) names, listagg(distinct CAND_NAME, ' / ') within group (order by CAND_NAME) nm,
        listagg(distinct CAND_OFFICE_ST || '-' || CAND_OFFICE, ',') off, min(CAND_ELECTION_YR) y0, max(CAND_ELECTION_YR) y1
      from c where nullif(trim(CAND_PCC),'') is not null group by 1 having count(distinct CAND_ID) > 1),
a as (select upper(trim(CAND_ST1)) || ' | ' || upper(trim(CAND_CITY)) || ' ' || CAND_ST || ' ' || left(CAND_ZIP,5) addr, count(distinct CAND_ID) ids, count(distinct CAND_NAME) names,
        listagg(distinct CAND_OFFICE, ',') offs, count(distinct CAND_OFFICE_ST) sts, min(CAND_ELECTION_YR) y0, max(CAND_ELECTION_YR) y1,
        left(listagg(distinct CAND_NAME, ' / '), 200) nm
      from c where nullif(trim(CAND_ST1),'') is not null group by 1 having count(distinct CAND_NAME) >= 4)
select 'pcc_sum' k, null a, count(*) n1, count_if(names > 1) n2, count_if(ids >= 3) n3, null n4, null n5, null n6, null t from p
union all select 'pcc', CAND_PCC, ids, names, y0, y1, null, null, left(nm || ' || ' || off, 300) from p where names > 1 qualify row_number() over (order by ids desc, names desc) <= 15
union all select 'addr', addr, ids, names, sts, y0, y1, null, offs || ' || ' || nm from a qualify row_number() over (order by names desc) <= 15
order by 1, 3 desc;

-- [q18] statement 18
-- SEC insider: eyeball the late open-market sale filings (11-365 days) at six high-ranked issuers: who, when sold, when filed, how much
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min, max(TRANSACTION_DATE) s_max, count(*) n_s, sum(SHARES) sh,
             sum(iff(PRICE_PER_SHARE between 0.01 and 5000, SHARES*PRICE_PER_SHARE, null)) val, min(PRICE_PER_SHARE) pmin, max(PRICE_PER_SHARE) pmax
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
o as (select ACCESSION_NUMBER, listagg(distinct OWNER_NAME, ' + ') nm, listagg(distinct coalesce(nullif(TITLE,''), RELATIONSHIP), ' + ') ttl
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER group by 1)
select sub.ISSUER_NAME, o.nm, left(o.ttl, 60) ttl, t.s_min, t.s_max, sub.FILING_DATE, datediff('day', t.s_min, sub.FILING_DATE) lag,
  t.n_s, round(t.sh) shares, round(t.val) usd, t.pmin, t.pmax, sub.ACCESSION_NUMBER, left(sub.REMARKS, 80) remarks
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
left join o on o.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
where sub.DOCUMENT_TYPE = '4' and datediff('day', t.s_min, sub.FILING_DATE) between 11 and 365
  and sub.ISSUER_CIK in ('0001341766','0001476840','0001624512','0001436208','0000834365','0001562088')
order by sub.ISSUER_NAME, t.val desc nulls last;

-- [q19] statement 19
-- SEC insider: sale-only late rate by year and by exchange group (time x peer), and insiders with the most late sale filings across all issuers
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min,
             sum(iff(PRICE_PER_SHARE between 0.01 and 5000, SHARES*PRICE_PER_SHARE, null)) val
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
x as (select try_to_number(CIK) c, max(EXCHANGE) ex from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
s as (select sub.ACCESSION_NUMBER, sub.ISSUER_NAME, year(sub.FILING_DATE) yr, datediff('day', t.s_min, sub.FILING_DATE) lag, t.val,
        case when x.ex in ('NYSE','Nasdaq') then 'NYSE/Nasdaq' when x.ex = 'OTC' then 'OTC' else 'other/none' end grp
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
      left join x on x.c = try_to_number(sub.ISSUER_CIK) where sub.DOCUMENT_TYPE = '4'),
o as (select r.ACCESSION_NUMBER, r.OWNER_CIK, r.OWNER_NAME from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER r
      where r.ACCESSION_NUMBER in (select ACCESSION_NUMBER from s where lag between 11 and 365))
select 'yr' k, yr::text a, grp b, count(*) n, count_if(lag between 11 and 365) late, round(100*count_if(lag between 11 and 365)/count(*), 2) pct,
  round(sum(iff(lag between 11 and 365, val, 0))/1e6) late_musd, null c
from s group by 2, 3
union all
select 'owner', o.OWNER_CIK, max(o.OWNER_NAME), count(distinct s.ACCESSION_NUMBER), count(distinct s.ISSUER_NAME), median(s.lag),
  round(sum(s.val)/1e6, 1), left(listagg(distinct s.ISSUER_NAME, ' / '), 120)
from o join s on s.ACCESSION_NUMBER = o.ACCESSION_NUMBER group by 2 qualify row_number() over (order by count(distinct s.ACCESSION_NUMBER) desc) <= 15
order by 1, 2, 3;

-- [q20] statement 20
-- EPA informal: Osage-county wells (Region 6 SDWA via ICIS) vs every other informal action, by year; formal EPA cases naming those wells by case-number year;
-- and how many of the wells carry the OS (Osage) well-name prefix in ECHO
with w as (select distinct REGISTRY_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS'),
inf as (select year(ACHIEVED_DATE) yr, count(distinct iff(w.REGISTRY_ID is null, ENF_IDENTIFIER, null)) other_actions,
          count(distinct iff(w.REGISTRY_ID is null and i.PGM_SYS_ACRNM = 'ICIS', ENF_IDENTIFIER, null)) other_icis_actions,
          count(distinct iff(w.REGISTRY_ID is not null, ENF_IDENTIFIER, null)) osage_actions
        from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS i left join w on w.REGISTRY_ID = i.REGISTRY_ID
        where year(ACHIEVED_DATE) >= 2015 group by 1),
cs as (select try_to_number(split_part(CASE_NUMBER, '-', 2)) yr, count(distinct CASE_NUMBER) osage_cases, count(distinct cf.REGISTRY_ID) osage_case_wells
       from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES cf join w on w.REGISTRY_ID = cf.REGISTRY_ID group by 1),
nm as (select count(*) wells_in_echo, count_if(FACILITY_NAME like 'OS%') os_prefix, count_if(STATE = 'OK') in_ok, count_if(IS_ON_TRIBAL_LAND) tribal
       from (select FRS_ID, max(FACILITY_NAME) FACILITY_NAME, max(STATE) STATE, max(IS_ON_TRIBAL_LAND::int)::boolean IS_ON_TRIBAL_LAND
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where FRS_ID in (select REGISTRY_ID from w) group by 1))
select coalesce(inf.yr, cs.yr) yr, inf.osage_actions, inf.other_actions, inf.other_icis_actions, cs.osage_cases, cs.osage_case_wells,
  nm.wells_in_echo, nm.os_prefix, nm.in_ok, nm.tribal
from inf full outer join cs on cs.yr = inf.yr cross join nm where coalesce(inf.yr, cs.yr) >= 2015 order by 1;

-- [q21] statement 21
-- EPA informal: what the 2025-2026 Region 6 drinking-water notices (SFDW) are about. PWSID join to SDWIS violations with a federal enforcement action dated 2024 on
with p as (select distinct PGM_SYS_ID pwsid from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where year(ACHIEVED_DATE) >= 2025 and left(ENF_IDENTIFIER,2) = '06' and PGM_SYS_ACRNM = 'SFDW'),
v as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
      where PWSID in (select pwsid from p) and ENFORCEMENT_DATE >= '2024-01-01')
select 'sum' k, null a, null b, null c, (select count(*) from p) n1, count(distinct PWSID) n2, count(*) n3, count_if(ENF_ORIGINATOR_CODE = 'F') n4
from v
union all
select 'rule_viol', RULE_CODE, VIOLATION_CODE, ENF_ORIGINATOR_CODE, count(distinct PWSID), count(distinct VIOLATION_ID), count(*), count_if(IS_HEALTH_BASED_IND = 'Y')
from v where ENF_ORIGINATOR_CODE = 'F' group by 2, 3, 4 qualify row_number() over (order by count(distinct PWSID) desc) <= 12
union all
select 'enf_type', ENFORCEMENT_ACTION_TYPE_CODE, year(ENFORCEMENT_DATE)::text, ENF_ORIGINATOR_CODE, count(distinct PWSID), count(distinct ENFORCEMENT_ID), count(*), null
from v group by 2, 3, 4 qualify row_number() over (order by count(distinct PWSID) desc) <= 12
order by 1, 5 desc;

-- [q22] statement 22
-- FHLB: insurers by district and join era (peer = the district's other members); insurer names hinting at captives; the newest insurers
with m as (select *, case when year(MEM_DATE) > year(current_date()) then year(MEM_DATE) - 100 else year(MEM_DATE) end yr
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP)
select 'district' k, DISTRICT a, null b, count(*) n_all, count_if(MEM_TYPE = 'Insurance Company') ins, round(100*count_if(MEM_TYPE = 'Insurance Company')/count(*), 1) ins_pct,
  count_if(yr >= 2016) new16, count_if(yr >= 2016 and MEM_TYPE = 'Insurance Company') ins16, round(100*count_if(yr >= 2016 and MEM_TYPE = 'Insurance Company')/nullif(count_if(yr >= 2016), 0), 1) ins16_pct
from m group by 2
union all
select 'year', yr::text, null, count(*), count_if(MEM_TYPE = 'Insurance Company'), round(100*count_if(MEM_TYPE = 'Insurance Company')/count(*), 1),
  count_if(MEM_TYPE = 'Credit Union'), count_if(MEM_TYPE = 'Commercial Bank'), count_if(MEM_TYPE like 'Community Development%')
from m where yr >= 2005 group by 2
union all
select 'captive?', MEMBER_NAME, DISTRICT || ' ' || STATE || ' ' || MEM_DATE::text, null, null, null, null, null, null
from m where MEM_TYPE = 'Insurance Company' and (MEMBER_NAME ilike '%captive%' or MEMBER_NAME ilike '%reinsur%' or MEMBER_NAME ilike '% re %' or MEMBER_NAME ilike '% re' or MEMBER_NAME ilike '%mortgage%' or MEMBER_NAME ilike '%funding%')
order by 1, 2;

-- [q23] statement 23
-- EPA informal: Osage-county well set, month by month 2024-01 to 2026-07: notices vs EPA inspections; plus null-dated notices that could hide 2025 actions
with w as (select distinct REGISTRY_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS'),
n as (select date_trunc('month', ACHIEVED_DATE)::date mo, count(distinct ENF_IDENTIFIER) notices
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS where REGISTRY_ID in (select REGISTRY_ID from w) group by 1),
i as (select date_trunc('month', ACTUAL_BEGIN_DATE)::date mo, count(distinct ACTIVITY_ID) insp, count(distinct REGISTRY_ID) wells
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS where REGISTRY_ID in (select REGISTRY_ID from w) group by 1)
select 'month' k, coalesce(n.mo, i.mo)::text mo, n.notices, i.insp, i.wells
from n full outer join i on i.mo = n.mo where coalesce(n.mo, i.mo) >= '2024-01-01'
union all
select 'nulldate', ENF_TYPE_DESC, count(*), count(distinct ENF_IDENTIFIER), count(distinct REGISTRY_ID)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS where REGISTRY_ID in (select REGISTRY_ID from w) and ACHIEVED_DATE is null group by 2
union all
select 'idyear', split_part(ENF_IDENTIFIER, '-', 2), count(*), count(distinct ENF_IDENTIFIER), count_if(ACHIEVED_DATE is null)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS where REGISTRY_ID in (select REGISTRY_ID from w) and split_part(ENF_IDENTIFIER, '-', 2) >= '2022' group by 2
order by 1, 2;

-- [q24] statement 24
-- FEC candidates: 2024 filers by office joined to the FEC candidate summary (cycle 2024): how many raised anything, how many reached $5,000;
-- the one Claremont CA address; and what the 2020 House out-of-state mailing addresses are
with c as (select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES),
s as (select CAND_ID, max(TTL_RECEIPTS) rcpt from LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY where CYCLE = '2024' group by 1),
c24 as (select distinct CAND_ID, CAND_OFFICE, CAND_STATUS from c where CAND_ELECTION_YR = 2024)
select 'y2024' k, CAND_OFFICE a, null b, count(distinct c24.CAND_ID) n1, count(distinct s.CAND_ID) n2, count(distinct iff(s.rcpt > 0, s.CAND_ID, null)) n3,
  count(distinct iff(s.rcpt >= 5000, s.CAND_ID, null)) n4, count(distinct iff(CAND_STATUS = 'N', c24.CAND_ID, null)) n5
from c24 left join s on s.CAND_ID = c24.CAND_ID group by 2
union all
select 'claremont', upper(trim(CAND_ST1)), null, count(distinct c.CAND_ID), count(distinct s.CAND_ID), count(distinct iff(s.rcpt > 0, s.CAND_ID, null)), min(CAND_ELECTION_YR), max(CAND_ELECTION_YR)
from c left join s on s.CAND_ID = c.CAND_ID where upper(CAND_ST1) like '1742 WOODBEND%' group by 2
union all
select 'oos2020', CAND_ST, CAND_OFFICE_ST, count(*), count(distinct CAND_ID), count_if(nullif(trim(CAND_ST),'') is null), null, null
from c where CAND_ELECTION_YR = 2020 and CAND_OFFICE = 'H' and CAND_ST <> CAND_OFFICE_ST group by 2, 3 qualify row_number() over (order by count(*) desc) <= 12
order by 1, 4 desc;

-- [q25] statement 25
-- SEC insider hostile check: were the same sales also reported ON TIME by another filer? Every Form 4/4-A with a sale in the three windows, all filers
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min, max(TRANSACTION_DATE) s_max, count(*) n_s, round(sum(SHARES)) sh
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
o as (select ACCESSION_NUMBER, left(listagg(distinct OWNER_NAME, ' + '), 90) nm from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER group by 1)
select sub.ISSUER_NAME, sub.DOCUMENT_TYPE, o.nm, t.s_min, t.s_max, sub.FILING_DATE, datediff('day', t.s_min, sub.FILING_DATE) lag, t.n_s, t.sh, sub.ACCESSION_NUMBER
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
left join o on o.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
where (sub.ISSUER_CIK = '0001341766' and t.s_max >= '2024-04-25' and t.s_min <= '2024-05-10')
   or (sub.ISSUER_CIK = '0001562088' and t.s_max >= '2021-11-10' and t.s_min <= '2021-12-05')
   or (sub.ISSUER_CIK = '0000834365' and t.s_max >= '2019-10-01' and t.s_min <= '2020-06-05' and o.nm ilike any ('%WAVI%', '%VILLIGER%', '%GIRSCHWEILER%', '%TAURUS%'))
order by 1, 4, 6;

-- [q26] statement 26
-- SEC insider dedupe: drop late sale filings that mirror an ON-TIME filing (same issuer, same first sale date, same total shares, filed within 5 days).
-- Re-rank issuers (30+ sale filings) on the late filings that remain; peer median and 90th percentile after the dedupe
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min, round(sum(SHARES)) sh,
             sum(iff(PRICE_PER_SHARE between 0.01 and 5000, SHARES*PRICE_PER_SHARE, null)) val
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
f as (select sub.ISSUER_CIK, sub.ISSUER_NAME, sub.ACCESSION_NUMBER, sub.FILING_DATE, t.s_min, t.sh, t.val, datediff('day', t.s_min, sub.FILING_DATE) lag
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER where sub.DOCUMENT_TYPE = '4'),
late as (select f.*, exists (select 1 from f f2 where f2.ISSUER_CIK = f.ISSUER_CIK and f2.s_min = f.s_min and f2.sh = f.sh
                                and f2.lag between 0 and 5 and f2.ACCESSION_NUMBER <> f.ACCESSION_NUMBER) mirrored
         from f where lag between 11 and 365),
iss as (select f.ISSUER_CIK, max(f.ISSUER_NAME) nm, count(*) sale_f,
          count(l.ACCESSION_NUMBER) late_all, count_if(l.mirrored) late_mirrored, count_if(not l.mirrored) late_real,
          round(sum(iff(not l.mirrored, l.val, 0))/1e6, 1) late_real_musd, count_if(not l.mirrored and l.FILING_DATE >= '2023-10-01') late_real_post
        from f left join late l on l.ACCESSION_NUMBER = f.ACCESSION_NUMBER group by 1),
pe as (select *, round(100*late_real/sale_f, 1) pct from iss where sale_f >= 30)
select 'all' k, null a, null b, (select count(*) from f) n1, (select count(*) from late) n2, (select count_if(mirrored) from late) n3,
  (select count_if(not mirrored) from late) n4, null n5, null n6, null n7
union all
select 'peer', null, null, count(*), sum(late_real), median(pct), percentile_cont(0.9) within group (order by pct), count_if(pct >= 10), count_if(pct = 0), null from pe
union all
select 'top', ISSUER_CIK, nm, sale_f, late_all, late_mirrored, late_real, pct, late_real_musd, late_real_post
from pe qualify row_number() over (order by late_real desc) <= 20
union all
select 'topmirror', ISSUER_CIK, nm, sale_f, late_all, late_mirrored, late_real, pct, late_real_musd, late_real_post
from iss qualify row_number() over (order by late_mirrored desc) <= 8
order by 1, 7 desc;

-- [q27] statement 27
-- (rerun of q26 with the topmirror pct fixed) SEC insider dedupe: drop late sale filings that mirror an ON-TIME filing (same issuer, same first sale date, same total shares, filed within 5 days).
-- Re-rank issuers (30+ sale filings) on the late filings that remain; peer median and 90th percentile after the dedupe
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min, round(sum(SHARES)) sh,
             sum(iff(PRICE_PER_SHARE between 0.01 and 5000, SHARES*PRICE_PER_SHARE, null)) val
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
f as (select sub.ISSUER_CIK, sub.ISSUER_NAME, sub.ACCESSION_NUMBER, sub.FILING_DATE, t.s_min, t.sh, t.val, datediff('day', t.s_min, sub.FILING_DATE) lag
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER where sub.DOCUMENT_TYPE = '4'),
late as (select f.*, exists (select 1 from f f2 where f2.ISSUER_CIK = f.ISSUER_CIK and f2.s_min = f.s_min and f2.sh = f.sh
                                and f2.lag between 0 and 5 and f2.ACCESSION_NUMBER <> f.ACCESSION_NUMBER) mirrored
         from f where lag between 11 and 365),
iss as (select f.ISSUER_CIK, max(f.ISSUER_NAME) nm, count(*) sale_f,
          count(l.ACCESSION_NUMBER) late_all, count_if(l.mirrored) late_mirrored, count_if(not l.mirrored) late_real,
          round(sum(iff(not l.mirrored, l.val, 0))/1e6, 1) late_real_musd, count_if(not l.mirrored and l.FILING_DATE >= '2023-10-01') late_real_post
        from f left join late l on l.ACCESSION_NUMBER = f.ACCESSION_NUMBER group by 1),
pe as (select *, round(100*late_real/sale_f, 1) pct from iss where sale_f >= 30)
select 'all' k, null a, null b, (select count(*) from f) n1, (select count(*) from late) n2, (select count_if(mirrored) from late) n3,
  (select count_if(not mirrored) from late) n4, null n5, null n6, null n7
union all
select 'peer', null, null, count(*), sum(late_real), median(pct), percentile_cont(0.9) within group (order by pct), count_if(pct >= 10), count_if(pct = 0), null from pe
union all
select 'top', ISSUER_CIK, nm, sale_f, late_all, late_mirrored, late_real, pct, late_real_musd, late_real_post
from pe qualify row_number() over (order by late_real desc) <= 20
union all
select 'topmirror', ISSUER_CIK, nm, sale_f, late_all, late_mirrored, late_real, round(100*late_real/sale_f, 1), late_real_musd, late_real_post
from iss qualify row_number() over (order by late_mirrored desc) <= 8
order by 1, 7 desc;

-- [q28] statement 28
-- EPA informal: where the Region 6 SDWA/ICIS well set sits (FRS program links: state + county), and what its case numbers look like
with w as (select distinct REGISTRY_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS'),
g as (select REGISTRY_ID, max(STATE_CODE) st, max(upper(COUNTY_NAME)) cty from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS
      where REGISTRY_ID in (select REGISTRY_ID from w) group by 1)
select 'county' k, coalesce(g.st, '(no FRS row)') a, g.cty b, count(*) n, null c
from w left join g on g.REGISTRY_ID = w.REGISTRY_ID group by 2, 3 qualify row_number() over (order by count(*) desc) <= 10
union all
select 'idfmt', regexp_replace(ENF_IDENTIFIER, '[0-9]', '9'), max(ENF_IDENTIFIER), count(*), max(PGM_SYS_ID)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS where REGISTRY_ID in (select REGISTRY_ID from w) group by 2
qualify row_number() over (order by count(*) desc) <= 6
order by 1, 4 desc;
