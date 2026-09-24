-- deep-6: coverage round 2, group 6. Python door, QUERY_TAG coverage-r2-2026-09-24. Read-only.
-- Tables: FEC independent expenditures, PCAOB Form AP, SEC 13F holdings, Senate eFD PTR, Senate trades.

-- [1] IE count + sample
select count(*) over () n_rows, * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES limit 5;

-- [2] PCAOB count + sample
select count(*) over () n_rows, * from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS limit 5;

-- [3] 13F count by source file and value unit, with over-1T rows
select SRC_FILE, VALUE_UNIT, count(*) n, count(distinct ACCESSION_NUMBER) filings, sum(VALUE_USD) sum_val, median(VALUE_USD) med_val, max(VALUE_USD) max_val, sum(iff(VALUE_USD >= 1e12,1,0)) over_1t, sum(iff(VALUE_USD >= 1e11,1,0)) over_100b from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS group by 1,2 order by 1,2;

-- [4] 13F sample
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS limit 5;

-- [5] EFD PTR count + sample
select count(*) over () n_rows, * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR limit 5;

-- [6] SENATE_TRADES count + sample
select count(*) over () n_rows, * from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES limit 5;

-- [7] join-partner tables that exist: FEC, election results, committees, SEC enforcement, tickers, 13F filer header
select table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where (table_name ilike '%FEC%' or table_name ilike '%ELECTION%' or table_name ilike '%COMMITTEE_MEMB%' or table_name ilike '%ENFORCE%' or table_name ilike '%AAER%' or table_name ilike '%RESTATE%' or table_name ilike '%LITIGATION%' or table_name ilike '%TICKER%' or table_name ilike '%13F%' or table_name ilike '%CANDIDATE%' or table_name ilike '%SIC%' or table_name ilike '%LEGISLATOR%' or table_name ilike '%PCAOB%') order by 1,2;

-- [8] IE profile per cycle: superseded, blank CAND_ID, bad amounts, raw vs deduped dollars
with b as (select *, try_to_double(EXP_AMO) amt, IS_SUPERSEDED::string ilike 'true' sup from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES),
r as (select CYCLE_FILE, count(*) n, sum(iff(sup,1,0)) n_sup, sum(iff(CAND_ID is null or trim(CAND_ID)='',1,0)) n_blank_cand, sum(iff(IS_SUSPECT_FILING::string ilike 'true',1,0)) n_suspect, sum(iff(amt is null,1,0)) n_bad_amt, sum(iff(amt<0,1,0)) n_neg, round(sum(amt)/1e6,1) all_m, round(sum(iff(not sup,amt,0))/1e6,1) live_m, max(amt) max_amt from b group by 1),
d as (select CYCLE_FILE, SPE_ID, CAND_ID, EXP_AMO, EXP_DATE, DISSEM_DT, PAY, SUP_OPP, max(amt) amt, count(*) copies from b where not sup group by all),
dd as (select CYCLE_FILE, count(*) n_dedup, sum(iff(copies>1,1,0)) keys_with_copies, round(sum(amt)/1e6,1) dedup_m from d group by 1)
select r.*, dd.n_dedup, dd.keys_with_copies, dd.dedup_m from r left join dd on dd.CYCLE_FILE = r.CYCLE_FILE order by 1;

-- [9] IE own-party primary attacks: group lean from all non-primary money, then primary oppose $ against candidates of the group's own lean party, 2020-2026
with b as (select *, try_to_double(EXP_AMO) amt, case when CAND_PTY_AFF ilike 'DEM%' then 'D' when CAND_PTY_AFF ilike 'REP%' then 'R' end pty from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where not (IS_SUPERSEDED::string ilike 'true') and CYCLE_FILE >= 2020 and CAN_OFFICE in ('H','S')),
d as (select CYCLE_FILE, SPE_ID, max(SPE_NAM) spe, CAND_ID, max(CAND_NAME) cand, max(pty) pty, ELE_TYPE, SUP_OPP, EXP_AMO, EXP_DATE, DISSEM_DT, PAY, max(amt) amt from b group by CYCLE_FILE, SPE_ID, CAND_ID, ELE_TYPE, SUP_OPP, EXP_AMO, EXP_DATE, DISSEM_DT, PAY),
lean as (select SPE_ID, sum(iff((pty='D' and SUP_OPP='S') or (pty='R' and SUP_OPP='O'), amt, 0)) pro_d, sum(iff((pty='R' and SUP_OPP='S') or (pty='D' and SUP_OPP='O'), amt, 0)) pro_r from d group by 1),
l2 as (select SPE_ID, case when pro_d > 3*pro_r then 'D' when pro_r > 3*pro_d then 'R' end lean_pty, pro_d, pro_r from lean)
select d.CYCLE_FILE, d.spe, l2.lean_pty, round(sum(d.amt)/1e6,2) own_party_primary_oppose_m, count(distinct d.CAND_ID) targets, listagg(distinct d.cand, '; ') within group (order by d.cand) target_names, round(max(l2.pro_d+l2.pro_r)/1e6,1) group_total_m
from d join l2 on l2.SPE_ID = d.SPE_ID
where d.ELE_TYPE like 'P%' and d.SUP_OPP = 'O' and d.pty = l2.lean_pty
group by 1,2,3 having sum(d.amt) > 1e6 order by own_party_primary_oppose_m desc limit 30;

-- [10] EFD PTR per senator: lines, paper, amendments, filed more than 45 days after the trade
with e as (select *, try_to_date(TRANSACTION_DATE::string) td, try_to_date(left(FILED_DATE::string,10)) fd from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR)
select coalesce(FILER_LAST_CLEAN,'(ALL)') filer, count(*) lines, count(distinct FILING_ID) filings, sum(iff(FILING_KIND='paper',1,0)) paper_lines, sum(iff(IS_AMENDMENT::string ilike 'true',1,0)) amend_lines, count(td) with_tdate, sum(iff(datediff(day, td, fd) > 45,1,0)) late45, sum(iff(datediff(day, td, fd) > 365,1,0)) late365, median(datediff(day, td, fd)) med_days, sum(iff(datediff(day, td, fd) < 0,1,0)) neg_days, min(td) first_t, max(td) last_t
from e group by rollup(FILER_LAST_CLEAN) order by lines desc limit 45;

-- [11] SENATE_TRADES: source, years, name-match pairs from 2021 on
select SOURCE_ID, year(try_to_date(TRANSACTION_DATE::string)) yr, count(*) n, count(distinct BIOGUIDE) senators, sum(iff(MATCH_NOTE ilike '%ambig%',1,0)) ambiguous, sum(iff(BIOGUIDE is null,1,0)) no_bioguide from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES group by 1,2 order by 1,2;

-- [12] SENATE_TRADES: raw name vs matched senator for 2021 on, to catch same-surname mixups
select SENATOR_RAW, SENATOR_NAME, BIOGUIDE, MATCH_NOTE, count(*) n, min(TRANSACTION_DATE) first_t, max(TRANSACTION_DATE) last_t from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES where try_to_date(TRANSACTION_DATE::string) >= '2021-01-01' group by 1,2,3,4 order by n desc;

-- [13] committee membership coverage by Congress
select CONGRESS, count(*) seats, count(distinct BIOGUIDE) members, sum(iff(COMMITTEE_CODE like 'SS%' and IS_SUBCOMMITTEE ilike 'false',1,0)) senate_full_seats, count(distinct iff(COMMITTEE_CODE like 'SS%', BIOGUIDE, null)) senators, min(SNAPSHOT_DATE) snap from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP group by 1 order by 1;

-- [14] IE junk amounts: per cycle, rows and dollars at $10M and $100M thresholds, and sane total after dropping rows of $100M+
with b as (select CYCLE_FILE, try_to_double(EXP_AMO) amt, try_to_double(AGG_AMO) agg from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where not (IS_SUPERSEDED::string ilike 'true'))
select CYCLE_FILE, count(*) n, count_if(amt >= 1e7) n_10m, round(sum(iff(amt>=1e7,amt,0))/1e6,1) m_10m, count_if(amt >= 1e8) n_100m, round(sum(iff(amt>=1e8,amt,0))/1e6,1) m_100m, count_if(amt >= 1e7 and agg < amt) n_10m_agg_below, round(sum(iff(amt<1e8,amt,0))/1e6,1) m_under_100m, round(sum(iff(amt<1e7,amt,0))/1e6,1) m_under_10m from b group by 1 order by 1;

-- [15] IE the 30 biggest single lines, to see what the junk looks like
select CYCLE_FILE, SPE_NAM, CAND_NAME, CAN_OFFICE, ELE_TYPE, SUP_OPP, PUR, EXP_AMO, AGG_AMO, EXP_DATE, FILE_NUM, AMNDT_IND from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where not (IS_SUPERSEDED::string ilike 'true') qualify row_number() over (order by try_to_double(EXP_AMO) desc nulls last) <= 30 order by try_to_double(EXP_AMO) desc;

-- [16] EFD original filings only (no amendments), ptr trades 2021 on: late over 45 days per senator, with lower-bound dollars
with e as (select *, try_to_date(TRANSACTION_DATE::string) td, try_to_date(left(FILED_DATE::string,10)) fd, try_to_number(regexp_replace(split_part(AMOUNT_RANGE,'-',1),'[^0-9]','')) lo from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILING_KIND='ptr' and not (IS_AMENDMENT::string ilike 'true'))
select coalesce(FILER_LAST_CLEAN,'(ALL)') filer, count(*) lines, count_if(datediff(day,td,fd) > 45) late45, round(100*count_if(datediff(day,td,fd) > 45)/count(*),1) pct_late, count_if(datediff(day,td,fd) > 365) late365, count(distinct iff(datediff(day,td,fd) > 45, FILING_ID, null)) late_filings, count(distinct FILING_ID) filings, sum(iff(datediff(day,td,fd) > 45, lo, 0)) late_lo_usd, max(datediff(day,td,fd)) max_days
from e where td >= '2021-01-01' group by rollup(FILER_LAST_CLEAN) having count(*) >= 5 order by late45 desc limit 30;

-- [17] EFD late-filing detail for the heaviest late filers: one row per filing
with e as (select *, try_to_date(TRANSACTION_DATE::string) td, try_to_date(left(FILED_DATE::string,10)) fd, try_to_number(regexp_replace(split_part(AMOUNT_RANGE,'-',1),'[^0-9]','')) lo from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILING_KIND='ptr' and not (IS_AMENDMENT::string ilike 'true') and FILER_LAST_CLEAN in ('ARMSTRONG','BRITT','SHEEHY','MULLIN','FETTERMAN','TUBERVILLE','BOOZMAN'))
select FILER_LAST_CLEAN, FILING_ID, fd, count(*) lines, min(td) first_t, max(td) last_t, count_if(datediff(day,td,fd) > 45) late45, sum(lo) lo_usd, listagg(distinct ASSET_TYPE, ',') asset_types, listagg(distinct OWNER, ',') owners, count(distinct TICKER) tickers
from e group by 1,2,3 having count_if(datediff(day,td,fd) > 45) > 0 order by late45 desc limit 40;

-- [18] SENATE_TRADES 2020 double count: efd rows in 2020 that also appear in the stock-watcher feed
with s as (select BIOGUIDE, try_to_date(TRANSACTION_DATE::string) td, upper(trim(TICKER)) tk, AMOUNT_RANGE, TRANSACTION_TYPE, SOURCE_ID from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES where year(try_to_date(TRANSACTION_DATE::string)) = 2020)
select count_if(SOURCE_ID='fed_senate_efd_ptr') efd_2020, count_if(SOURCE_ID='fed_senate_stock_watcher') sw_2020,
 count_if(SOURCE_ID='fed_senate_efd_ptr' and exists (select 1 from s s2 where s2.SOURCE_ID='fed_senate_stock_watcher' and s2.BIOGUIDE=s.BIOGUIDE and s2.td=s.td and coalesce(s2.tk,'')=coalesce(s.tk,'') and s2.AMOUNT_RANGE=s.AMOUNT_RANGE)) efd_also_in_sw
from s;

-- [19] PCAOB profile by report type and audit-report year: rows, latest-version rows, partners, issuers, firms
select AUDIT_REPORT_TYPE, year(try_to_date(AUDIT_REPORT_DATE::string)) yr, count(*) n, count_if(LATEST_FORM_AP_FILING::string = '1') latest, count(distinct ENGAGEMENT_PARTNER_ID) partners, count(distinct ISSUER_ID) issuers, count(distinct FIRM_ID) firms, count_if(ENGAGEMENT_PARTNER_ID is null) no_partner from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS group by 1,2 order by 1,2;

-- [20] 13F thousands era: filings whose rows imply a share price over $20,000 (value typed in dollars, not thousands), top 25 by excess, named from the cover page
with h as (select ACCESSION_NUMBER, SRC_FILE, VALUE_USD v, SSHPRNAMT sh from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS where VALUE_UNIT = 'thousands' and SSHPRNAMTTYPE = 'SH' and SSHPRNAMT > 0 and left(CUSIP,6) <> '084670'),
a as (select ACCESSION_NUMBER, max(SRC_FILE) src, count(*) rows_all, count_if(v/sh > 20000) rows_bad, sum(v) val_all, sum(iff(v/sh > 20000, v, 0)) val_bad from h group by 1),
t as (select *, sum(val_bad) over () total_bad, sum(val_all) over () total_all, count_if(rows_bad > 0) over () filings_bad, count(*) over () filings_all from a)
select t.src, t.ACCESSION_NUMBER, f.FILINGMANAGER_NAME, t.rows_all, t.rows_bad, round(t.val_bad/1e12,2) bad_trillion, round(t.total_bad/1e12,1) all_bad_trillion, round(t.total_all/1e12,1) all_val_trillion, t.filings_bad, t.filings_all
from t left join (select ACCESSION_NUMBER, max(FILINGMANAGER_NAME) FILINGMANAGER_NAME from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS group by 1) f on f.ACCESSION_NUMBER = t.ACCESSION_NUMBER
order by t.val_bad desc limit 25;

-- [21] IE 2024 House+Senate: outside money per candidate vs the candidate's own spending (TTL_DISB), deduped, lines under $50M, with land rate, name check and whether the candidate is in Congress now
with b as (select *, try_to_double(EXP_AMO) amt from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where not (IS_SUPERSEDED::string ilike 'true') and CYCLE_FILE = 2024 and left(CAND_ID,1) in ('H','S')),
d as (select SPE_ID, CAND_ID, max(CAND_NAME) cand, SUP_OPP, EXP_AMO, EXP_DATE, DISSEM_DT, PAY, max(amt) amt from b where amt < 5e7 group by SPE_ID, CAND_ID, SUP_OPP, EXP_AMO, EXP_DATE, DISSEM_DT, PAY),
ie as (select CAND_ID, max(cand) cand, sum(amt) ie_amt, sum(iff(SUP_OPP='S',amt,0)) ie_sup, sum(iff(SUP_OPP='O',amt,0)) ie_opp, count(distinct SPE_ID) groups from d group by 1),
cs as (select CAND_ID, max(CAND_NAME) cs_name, max(TTL_DISB) disb, max(INCUMBENT_CHALLENGER) ici from LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY where CYCLE = 2024 group by 1),
leg as (select distinct f.value::string fec_id from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS l, lateral flatten(input => try_parse_json(l.FEC_IDS)) f where l.TERM_START <= '2025-01-03' and l.TERM_END > '2025-01-03'),
j as (select ie.*, cs.cs_name, cs.disb, cs.ici, iff(leg.fec_id is not null,'in Congress','not') now_status,
  upper(split_part(ie.cand, ',', 1)) = upper(split_part(cs.cs_name, ',', 1)) name_agree from ie left join cs on cs.CAND_ID = ie.CAND_ID left join leg on leg.fec_id = ie.CAND_ID)
select CAND_ID, cand, ici, now_status, round(ie_sup/1e6,2) sup_m, round(ie_opp/1e6,2) opp_m, round(disb/1e6,2) own_m, round(ie_amt/nullif(disb,0),1) ratio, groups,
 count(*) over () cands_with_ie, count(disb) over () landed, count_if(name_agree) over () names_agree, count_if(ie_amt > disb) over () ie_exceeds_own, count_if(ie_amt > disb and ie_amt > 1e6) over () exceeds_and_over_1m, count_if(now_status='in Congress') over () targets_in_congress, round(sum(ie_amt) over ()/1e6,1) total_ie_m
from j qualify disb is not null and row_number() over (partition by (disb is not null) order by ie_amt - disb desc) <= 25 order by ie_amt - disb desc;

-- [22] IE 2024 House+Senate losing bets per group: support for someone not in Congress now, or oppose someone who is; primary vs general
with b as (select *, try_to_double(EXP_AMO) amt from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where not (IS_SUPERSEDED::string ilike 'true') and CYCLE_FILE = 2024 and left(CAND_ID,1) in ('H','S')),
d as (select SPE_ID, max(SPE_NAM) spe, CAND_ID, ELE_TYPE, SUP_OPP, EXP_AMO, EXP_DATE, DISSEM_DT, PAY, max(amt) amt from b where amt < 5e7 group by SPE_ID, CAND_ID, ELE_TYPE, SUP_OPP, EXP_AMO, EXP_DATE, DISSEM_DT, PAY),
leg as (select distinct f.value::string fec_id from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS l, lateral flatten(input => try_parse_json(l.FEC_IDS)) f where l.TERM_START <= '2025-01-03' and l.TERM_END > '2025-01-03'),
x as (select d.*, leg.fec_id is not null won from d left join leg on leg.fec_id = d.CAND_ID)
select SPE_ID, max(spe) spe, round(sum(amt)/1e6,1) total_m,
 round(sum(iff((SUP_OPP='S' and not won) or (SUP_OPP='O' and won), amt, 0))/1e6,1) lost_m,
 round(100*sum(iff((SUP_OPP='S' and not won) or (SUP_OPP='O' and won), amt, 0))/nullif(sum(amt),0),0) pct_lost,
 round(sum(iff(ELE_TYPE like 'P%' and SUP_OPP='S' and not won, amt, 0))/1e6,1) primary_backed_not_in_congress_m,
 round(sum(iff(ELE_TYPE like 'G%' and SUP_OPP='S' and not won, amt, 0))/1e6,1) general_backed_loser_m,
 round(sum(iff(ELE_TYPE like 'G%' and SUP_OPP='O' and won, amt, 0))/1e6,1) general_opposed_winner_m,
 round(sum(sum(amt)) over ()/1e6,1) all_groups_m,
 round(sum(sum(iff((SUP_OPP='S' and not won) or (SUP_OPP='O' and won), amt, 0))) over ()/1e6,1) all_lost_m
from x group by SPE_ID qualify row_number() over (order by sum(iff((SUP_OPP='S' and not won) or (SUP_OPP='O' and won), amt, 0)) desc) <= 20 order by lost_m desc;

-- [23] Senate trades 2021-26 (eFD originals): sector of stock vs senator's committee that oversees it, with base rate of trading senators on that committee
with tk as (select upper(TICKER) ticker, max(try_to_number(CIK)) cik from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
sic as (select try_to_number(CIK) cik, max(SIC) sic from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS group by 1),
t0 as (select BIOGUIDE, SENATOR_NAME, try_to_date(TRANSACTION_DATE::string) td, upper(trim(TICKER)) ticker from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES where SOURCE_ID = 'fed_senate_efd_ptr' and not (IS_AMENDMENT::string ilike 'true') and try_to_date(TRANSACTION_DATE::string) >= '2021-01-03'),
t1 as (select t0.*, case when td < '2023-01-03' then '117' when td < '2025-01-03' then '118' else '119' end congress from t0),
tr as (select t1.*, sic.sic,
  case when sic.sic between '3720' and '3769' or sic.sic in ('3812','3795','3480','3483') then 'defense'
       when sic.sic between '6000' and '6199' or sic.sic in ('6211','6282','6770') then 'banking'
       when sic.sic between '1300' and '1399' or sic.sic between '2900' and '2999' or sic.sic in ('4922','4923','4924','4911','4931','4932') then 'energy'
       when sic.sic in ('2834','2835','2836','8000','8011','8050','8051','8060','8062','8071','8082','8090','8093','6324','5122','5047','3841','3842','3845','3851') then 'health'
       when sic.sic between '4800' and '4899' or sic.sic in ('7370','7371','7372','7373','7374','7379','3674','3670','3672','3576','3577','3578','3661','3663') then 'tech_telecom'
       when sic.sic between '4000' and '4599' or sic.sic in ('3711','3713','3714','3716','3730','3743') then 'transport'
       when sic.sic between '0100' and '0999' or sic.sic in ('2000','2011','2013','2015','2020','2030','2033','2040','2050','2060','2070','2080','2086','2090','5140','5141','5150') then 'agriculture'
       else 'other' end sector
  from t1 left join tk on tk.ticker = t1.ticker left join sic on sic.cik = tk.cik where t1.ticker is not null and t1.ticker not in ('--','N/A','')),
map as (select column1 code, column2 sector from values ('SSAS','defense'),('SSBK','banking'),('SSEG','energy'),('SSEV','energy'),('SSHR','health'),('SSFI','health'),('SSCM','tech_telecom'),('SSCM','transport'),('SSAF','agriculture')),
cm as (select distinct m.BIOGUIDE, m.CONGRESS::string congress, map.sector from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP m join map on map.code = m.COMMITTEE_CODE where m.IS_SUBCOMMITTEE ilike 'false'),
traders as (select distinct BIOGUIDE, congress from t1),
base as (select s.sector, count(*) pairs, count(cm.BIOGUIDE) on_cmte from traders t cross join (select distinct sector from map) s left join cm on cm.BIOGUIDE = t.BIOGUIDE and cm.congress = t.congress and cm.sector = s.sector group by 1),
res as (select tr.sector, count(*) trades, count(cm.BIOGUIDE) by_member, count(distinct iff(cm.BIOGUIDE is not null, tr.BIOGUIDE, null)) member_traders, count(distinct tr.BIOGUIDE) traders_in_sector from tr left join cm on cm.BIOGUIDE = tr.BIOGUIDE and cm.congress = tr.congress and cm.sector = tr.sector where tr.sic is not null group by 1)
select res.sector, res.trades, res.by_member, round(100*res.by_member/res.trades,1) pct_by_member, round(100*base.on_cmte/base.pairs,1) pct_traders_on_cmte, res.member_traders, res.traders_in_sector,
 (select count(*) from tr) ticker_trades, (select count(sic) from tr) with_sic
from res left join base on base.sector = res.sector order by res.trades desc;

-- [24] Senate trades 2021-26: named senator x overseeing committee x sector, top 25
with tk as (select upper(TICKER) ticker, max(try_to_number(CIK)) cik from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
sic as (select try_to_number(CIK) cik, max(SIC) sic from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS group by 1),
t0 as (select BIOGUIDE, SENATOR_NAME, try_to_date(TRANSACTION_DATE::string) td, upper(trim(TICKER)) ticker, TRANSACTION_TYPE from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES where SOURCE_ID = 'fed_senate_efd_ptr' and not (IS_AMENDMENT::string ilike 'true') and try_to_date(TRANSACTION_DATE::string) >= '2021-01-03'),
t1 as (select t0.*, case when td < '2023-01-03' then '117' when td < '2025-01-03' then '118' else '119' end congress from t0),
tr as (select t1.*, sic.sic,
  case when sic.sic between '3720' and '3769' or sic.sic in ('3812','3795','3480','3483') then 'defense'
       when sic.sic between '6000' and '6199' or sic.sic in ('6211','6282','6770') then 'banking'
       when sic.sic between '1300' and '1399' or sic.sic between '2900' and '2999' or sic.sic in ('4922','4923','4924','4911','4931','4932') then 'energy'
       when sic.sic in ('2834','2835','2836','8000','8011','8050','8051','8060','8062','8071','8082','8090','8093','6324','5122','5047','3841','3842','3845','3851') then 'health'
       when sic.sic between '4800' and '4899' or sic.sic in ('7370','7371','7372','7373','7374','7379','3674','3670','3672','3576','3577','3578','3661','3663') then 'tech_telecom'
       when sic.sic between '4000' and '4599' or sic.sic in ('3711','3713','3714','3716','3730','3743') then 'transport'
       when sic.sic between '0100' and '0999' or sic.sic in ('2000','2011','2013','2015','2020','2030','2033','2040','2050','2060','2070','2080','2086','2090','5140','5141','5150') then 'agriculture'
       else 'other' end sector
  from t1 left join tk on tk.ticker = t1.ticker left join sic on sic.cik = tk.cik where t1.ticker is not null and t1.ticker not in ('--','N/A','')),
map as (select column1 code, column2 sector from values ('SSAS','defense'),('SSBK','banking'),('SSEG','energy'),('SSEV','energy'),('SSHR','health'),('SSFI','health'),('SSCM','tech_telecom'),('SSCM','transport'),('SSAF','agriculture')),
cm as (select distinct m.BIOGUIDE, m.CONGRESS::string congress, m.COMMITTEE_CODE, map.sector from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP m join map on map.code = m.COMMITTEE_CODE where m.IS_SUBCOMMITTEE ilike 'false')
select tr.SENATOR_NAME, listagg(distinct cm.COMMITTEE_CODE, ',') cmtes, tr.sector, count(distinct tr.BIOGUIDE||tr.td||tr.ticker||coalesce(tr.TRANSACTION_TYPE,'')) trades_approx, count_if(tr.TRANSACTION_TYPE ilike 'purchase%') buy_rows, min(tr.td) first_t, max(tr.td) last_t, listagg(distinct tr.ticker, ',') within group (order by tr.ticker) tickers
from tr join cm on cm.BIOGUIDE = tr.BIOGUIDE and cm.congress = tr.congress and cm.sector = tr.sector
group by 1,3 order by trades_approx desc limit 25;

-- [25] PCAOB operating-company audits (not funds, not benefit plans), newest version only: issuers per lead partner per year, top 20, with peer percentiles
with a as (select ENGAGEMENT_PARTNER_ID pid, max(ENGAGEMENT_PARTNER_FIRST_NAME||' '||ENGAGEMENT_PARTNER_LAST_NAME) partner, max(FIRM_NAME) firm, max(FIRM_COUNTRY) country, year(try_to_date(AUDIT_REPORT_DATE::string)) yr, count(distinct ISSUER_ID) issuers, count(distinct iff(ISSUER_CIK_NONE::string ilike 'true', ISSUER_ID, null)) no_cik
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where AUDIT_REPORT_TYPE ilike 'Issuer, other%' and LATEST_FORM_AP_FILING::string = '1' group by pid, yr)
select pid, partner, firm, country, yr, issuers, no_cik, percentile_cont(0.5) within group (order by issuers) over () p50, percentile_cont(0.99) within group (order by issuers) over () p99, count_if(issuers >= 20) over () partner_years_20plus, count(*) over () partner_years
from a where yr between 2017 and 2025 qualify row_number() over (order by issuers desc) <= 20 order by issuers desc;

-- [26] PCAOB partner rotation: same lead partner on the same operating company for 6+ consecutive fiscal years; firm size for the small-firm exemption
with a as (select distinct ENGAGEMENT_PARTNER_ID pid, ISSUER_ID iid, FIRM_ID fid, year(try_to_date(FISCAL_PERIOD_END_DATE::string)) fy from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where AUDIT_REPORT_TYPE ilike 'Issuer, other%' and LATEST_FORM_AP_FILING::string = '1' and FISCAL_PERIOD_END_DATE is not null),
firmsize as (select fid, fy, count(distinct iid) firm_issuers, count(distinct pid) firm_partners from a group by 1,2),
pairfirm as (select a.pid, a.iid, max(s.firm_issuers) max_firm_issuers, max(s.firm_partners) max_firm_partners from a join firmsize s on s.fid = a.fid and s.fy = a.fy group by 1,2),
isl as (select pid, iid, fy, fy - row_number() over (partition by pid, iid order by fy) grp from (select distinct pid, iid, fy from a)),
runs as (select pid, iid, min(fy) y1, max(fy) y2, count(*) run from isl group by pid, iid, grp),
big as (select r.*, p.max_firm_issuers, p.max_firm_partners from runs r join pairfirm p on p.pid = r.pid and p.iid = r.iid where r.run >= 6),
names as (select ENGAGEMENT_PARTNER_ID pid, ISSUER_ID iid, max(ENGAGEMENT_PARTNER_FIRST_NAME||' '||ENGAGEMENT_PARTNER_LAST_NAME) partner, max(ISSUER_NAME) issuer, max(FIRM_NAME) firm, max(FIRM_COUNTRY) country from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where AUDIT_REPORT_TYPE ilike 'Issuer, other%' group by 1,2)
select big.run, big.y1, big.y2, n.partner, n.issuer, n.firm, n.country, big.max_firm_issuers, big.max_firm_partners,
 count(*) over () pairs_6plus, count_if(big.max_firm_issuers >= 5 or big.max_firm_partners >= 10) over () pairs_6plus_not_small_firm, (select count(*) from runs where run >= 5) pairs_5plus, (select count(*) from runs) all_runs
from big join names n on n.pid = big.pid and n.iid = big.iid
order by (big.max_firm_issuers >= 5 or big.max_firm_partners >= 10) desc, big.run desc, big.max_firm_issuers desc limit 40;

-- [27] EFD Armstrong's single filing: buys vs sells, asset types, dollar bands, top positions
with e as (select *, try_to_date(TRANSACTION_DATE::string) td, try_to_number(regexp_replace(split_part(AMOUNT_RANGE,'-',1),'[^0-9]','')) lo, try_to_number(regexp_replace(split_part(AMOUNT_RANGE,'-',2),'[^0-9]','')) hi from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILER_LAST_CLEAN = 'ARMSTRONG')
select TRANSACTION_TYPE, OWNER, ASSET_TYPE, count(*) n, sum(lo) lo_usd, sum(hi) hi_usd, min(td) first_t, max(td) last_t, count_if(TICKER = 'WMB') wmb_lines, listagg(distinct iff(lo >= 250001, TICKER, null), ',') big_tickers, max(COMMENT) sample_comment
from e group by 1,2,3 order by n desc;

-- [28] PCAOB: where B F Borgers' operating-company clients (audited 2023-2024) went next, first new firm on a Form AP dated 2024 or later
with a as (select ISSUER_ID, max(FIRM_NAME) firm, year(try_to_date(AUDIT_REPORT_DATE::string)) yr from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where AUDIT_REPORT_TYPE ilike 'Issuer, other%' and LATEST_FORM_AP_FILING::string = '1' group by ISSUER_ID, FIRM_ID, yr),
bc as (select distinct ISSUER_ID from a where firm ilike 'B F Borgers%' and yr in (2023, 2024)),
nxt as (select a.ISSUER_ID, a.firm, a.yr from a join bc on bc.ISSUER_ID = a.ISSUER_ID where a.yr >= 2024 and a.firm not ilike 'B F Borgers%'),
fn as (select ISSUER_ID, firm from nxt qualify row_number() over (partition by ISSUER_ID order by yr, firm) = 1)
select coalesce(fn.firm, '(no later Form AP)') next_firm, count(*) issuers, sum(count(*)) over () borgers_clients_2023_24
from bc left join fn on fn.ISSUER_ID = bc.ISSUER_ID group by 1 order by 2 desc limit 25;

-- [29] PCAOB: 2024-2025 lead partners with 15+ operating-company audits in a year, with their firm's size that year
with a as (select ENGAGEMENT_PARTNER_ID pid, FIRM_ID fid, ISSUER_ID iid, year(try_to_date(AUDIT_REPORT_DATE::string)) yr from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where AUDIT_REPORT_TYPE ilike 'Issuer, other%' and LATEST_FORM_AP_FILING::string = '1'),
fs as (select fid, yr, count(distinct pid) firm_partners, count(distinct iid) firm_issuers from a group by 1,2),
py as (select pid, fid, yr, count(distinct iid) issuers from a where yr in (2024, 2025) group by 1,2,3),
nm as (select ENGAGEMENT_PARTNER_ID pid, FIRM_ID fid, max(ENGAGEMENT_PARTNER_FIRST_NAME||' '||ENGAGEMENT_PARTNER_LAST_NAME) partner, max(FIRM_NAME) firm, max(FIRM_COUNTRY) country, max(FIRM_ISSUING_CITY) city from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS group by 1,2)
select nm.partner, nm.firm, nm.country, nm.city, py.yr, py.issuers, fs.firm_partners, fs.firm_issuers, count(*) over () partner_years_2024_25, count_if(py.issuers >= 15) over () with_15plus
from py join fs on fs.fid = py.fid and fs.yr = py.yr join nm on nm.pid = py.pid and nm.fid = py.fid
qualify py.issuers >= 15 order by py.issuers desc limit 30;

-- [30] Senate 2021-26: per senator, share of sector-coded trades that are health stocks, split by whether they sat on HELP or Finance at the time
with tk as (select upper(TICKER) ticker, max(try_to_number(CIK)) cik from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
sic as (select try_to_number(CIK) cik, max(SIC) sic from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS group by 1),
t0 as (select BIOGUIDE, SENATOR_NAME, try_to_date(TRANSACTION_DATE::string) td, upper(trim(TICKER)) ticker from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES where SOURCE_ID = 'fed_senate_efd_ptr' and not (IS_AMENDMENT::string ilike 'true') and try_to_date(TRANSACTION_DATE::string) >= '2021-01-03' and TICKER is not null and TICKER not in ('--','N/A','')),
tr as (select t0.*, case when td < '2023-01-03' then '117' when td < '2025-01-03' then '118' else '119' end congress, sic.sic,
  sic.sic in ('2834','2835','2836','8000','8011','8050','8051','8060','8062','8071','8082','8090','8093','6324','5122','5047','3841','3842','3845','3851') is_health
  from t0 left join tk on tk.ticker = t0.ticker left join sic on sic.cik = tk.cik),
cm as (select distinct BIOGUIDE, CONGRESS::string congress from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP where COMMITTEE_CODE in ('SSHR','SSFI') and IS_SUBCOMMITTEE ilike 'false')
select tr.SENATOR_NAME, iff(cm.BIOGUIDE is not null, 'HELP/Finance', 'not') seat, count(*) coded_trades, count_if(tr.is_health) health_trades, round(100*count_if(tr.is_health)/count(*),1) pct_health
from tr left join cm on cm.BIOGUIDE = tr.BIOGUIDE and cm.congress = tr.congress where tr.sic is not null
group by 1,2 having count(*) >= 10 order by seat, coded_trades desc;

-- [31] IE second-field check on the losing-bets join: top targets of four groups, with candidate name, side and whether the target is in Congress now
with b as (select *, try_to_double(EXP_AMO) amt from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where not (IS_SUPERSEDED::string ilike 'true') and CYCLE_FILE = 2024 and left(CAND_ID,1) in ('H','S') and SPE_ID in ('C00870030','C00849729','C00865444','C00027466')),
d as (select SPE_ID, max(SPE_NAM) spe, CAND_ID, max(CAND_NAME) cand, max(CAN_OFFICE_STATE) st, SUP_OPP, EXP_AMO, EXP_DATE, DISSEM_DT, PAY, max(amt) amt from b where amt < 5e7 group by SPE_ID, CAND_ID, SUP_OPP, EXP_AMO, EXP_DATE, DISSEM_DT, PAY),
leg as (select distinct f.value::string fec_id from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS l, lateral flatten(input => try_parse_json(l.FEC_IDS)) f where l.TERM_START <= '2025-01-03' and l.TERM_END > '2025-01-03')
select max(d.spe) spe, d.CAND_ID, max(d.cand) cand, max(d.st) st, d.SUP_OPP, round(sum(d.amt)/1e6,2) m, max(iff(leg.fec_id is not null, 'in Congress', 'not')) now_status
from d left join leg on leg.fec_id = d.CAND_ID group by d.SPE_ID, d.CAND_ID, d.SUP_OPP qualify row_number() over (partition by d.SPE_ID order by sum(d.amt) desc) <= 5 order by 1, m desc;

-- [32] IE junk rows vs the suspect flag: rows of $10M+ by cycle and flag, with the filer names
select CYCLE_FILE, IS_SUSPECT_FILING::string suspect, count(*) rows_10m_plus, round(sum(try_to_double(EXP_AMO))/1e9,1) billions, count(distinct SPE_ID) filers, listagg(distinct left(SPE_NAM,30), ' | ') names
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES where try_to_double(EXP_AMO) >= 1e7 and not (IS_SUPERSEDED::string ilike 'true') group by 1,2 order by 1,2;

-- [33] EFD original ptr lines by year filed: lines, late over 45 days, late filings, and who
with e as (select *, try_to_date(TRANSACTION_DATE::string) td, try_to_date(left(FILED_DATE::string,10)) fd from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILING_KIND='ptr' and not (IS_AMENDMENT::string ilike 'true'))
select year(fd) filed_yr, count(*) lines, count_if(datediff(day,td,fd) > 45) late45, count_if(datediff(day,td,fd) > 45 and FILER_LAST_CLEAN <> 'ARMSTRONG') late45_ex_armstrong, count(distinct FILING_ID) filings, count(distinct iff(datediff(day,td,fd) > 45, FILING_ID, null)) late_filings, count(distinct FILER_LAST_CLEAN) filers, listagg(distinct iff(datediff(day,td,fd) > 45, FILER_LAST_CLEAN, null), ',') late_filers
from e group by 1 order by 1;

-- [34] PCAOB trend: partner-years with 20+ operating-company audits, and how many sit at firms with 1-2 lead partners, by audit-report year
with a as (select ENGAGEMENT_PARTNER_ID pid, FIRM_ID fid, FIRM_NAME firm, ISSUER_ID iid, year(try_to_date(AUDIT_REPORT_DATE::string)) yr from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where AUDIT_REPORT_TYPE ilike 'Issuer, other%' and LATEST_FORM_AP_FILING::string = '1'),
fs as (select fid, yr, count(distinct pid) firm_partners from a group by 1,2),
py as (select pid, fid, yr, max(firm) firm, count(distinct iid) issuers from a group by 1,2,3)
select py.yr, count(*) partner_years, count_if(py.issuers >= 20) py_20plus, count_if(py.issuers >= 20 and fs.firm_partners <= 2) py_20plus_tiny_firm, sum(iff(py.issuers >= 20 and fs.firm_partners <= 2, py.issuers, 0)) audits_by_tiny_heavy, listagg(distinct iff(py.issuers >= 20 and fs.firm_partners <= 2, left(py.firm,28), null), ' | ') tiny_heavy_firms
from py join fs on fs.fid = py.fid and fs.yr = py.yr where py.yr between 2017 and 2025 group by 1 order by 1;

-- [35] SENATE_TRADES stock-watcher era: rows where the raw filer name does not contain the matched senator's first name (same-surname mixup check)
select SENATOR_RAW, SENATOR_NAME, BIOGUIDE, MATCH_NOTE, count(*) n, min(TRANSACTION_DATE) first_t, max(TRANSACTION_DATE) last_t, sum(count(*)) over () mismatch_rows
from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES where SOURCE_ID = 'fed_senate_stock_watcher' and not (upper(SENATOR_RAW) like '%' || upper(split_part(SENATOR_NAME,' ',1)) || '%')
group by 1,2,3,4 order by n desc;
