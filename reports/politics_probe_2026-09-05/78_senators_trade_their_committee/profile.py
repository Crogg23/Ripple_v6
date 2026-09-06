"""Profile phase shared by 35/78/91. SELECT only."""
import json
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/78_senators_trade_their_committee/probe.log")
R = {}
R["sic_cols"] = run("""select table_schema, table_name, column_name from LIBRARY_RAW.information_schema.columns
  where (column_name ilike '%SIC%' and column_name not ilike '%CLASSIC%' and column_name not ilike '%PHYSIC%' and column_name not ilike '%MUSIC%' and column_name not ilike '%BASIC%')
     or table_name ilike '%DERA%' or (column_name ilike '%SUBJECT%' or column_name ilike '%POLICY_AREA%') and (table_name ilike '%BILL%' or table_name ilike '%CONGRESS%' or table_name ilike '%GOVINFO%')
  order by 1,2,3""", "sic_subject_cols")
R["dera_tables"] = run("""select table_schema, table_name, row_count from LIBRARY_RAW.information_schema.tables where table_name ilike '%DERA%' or table_name ilike '%SEC_%SUB%' or table_name ilike '%EDGAR%' or table_name ilike '%CONGRESS%' or table_name ilike '%GOVINFO%' order by 2""", "sec_congress_tables")
R["st_profile"] = run("""select count(*) n, count(distinct bioguide) n_bio, count(distinct senator) n_sen, count(distinct nullif(trim(ticker),'')) n_tick,
  sum(iff(ticker is null or trim(ticker) in ('','--','N/A'),1,0)) tick_blank, min(transaction_date) d0, max(transaction_date) d1,
  sum(iff(bioguide is null,1,0)) bio_null from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES""", "st_profile")
R["st_match"] = run("select match_method, transaction_type, count(*) n, count(distinct senator) sen from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES group by 1,2 order by 3 desc", "st_match")
R["st_sample"] = run("select * from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES where ticker is not null and trim(ticker) not in ('','--') limit 5", "st_sample")
R["cm_profile"] = run("""select left(committee_code,1) chamber, is_subcommittee, count(*) n, count(distinct committee_code) n_cmte, count(distinct bioguide) n_bio
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP group by 1,2 order by 1,2""", "cm_profile")
R["cm_senate_cmtes"] = run("""select committee_code, committee_name, count(*) n from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
  where is_subcommittee in ('false','False','0','N','FALSE') or is_subcommittee is null group by 1,2 order by 1""", "cm_committees")
R["cm_sample"] = run("select * from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP limit 5", "cm_sample")
R["fd_profile"] = run("""select count(*) n, count(distinct docid) n_doc, count(distinct hash(*)) n_hash, min(year) y0, max(year) y1, min(filingdate) f0, max(filingdate) f1,
  count(distinct last||'|'||first) n_names from LIBRARY_RAW.LANDING.FED_HOUSE_FD_PTR_INDEX""", "fd_profile")
R["fd_types"] = run("select filingtype, count(*) n, count(distinct hash(*)) n_hash from LIBRARY_RAW.LANDING.FED_HOUSE_FD_PTR_INDEX group by 1 order by 2 desc", "fd_types")
R["fd_sample"] = run("select * from LIBRARY_RAW.LANDING.FED_HOUSE_FD_PTR_INDEX where filingtype='P' limit 5", "fd_sample")
R["bill_profile"] = run("""select count(*) n, min(congress) c0, max(congress) c1, count(distinct sponsor_bioguide) n_spon, min(introduced_date) d0, max(introduced_date) d1,
  sum(iff(sponsor_bioguide is null or sponsor_bioguide='',1,0)) spon_null, count(distinct congress||bill_type||bill_number) n_key from LIBRARY_RAW.LANDING.FED_GOVINFO_BILLSTATUS""", "bill_profile")
R["bill_sample"] = run("select congress,bill_type,bill_number,introduced_date,sponsor_bioguide,sponsor_name,left(title,120) title,n_cosponsors from LIBRARY_RAW.LANDING.FED_GOVINFO_BILLSTATUS limit 5", "bill_sample")
R["cosp_profile"] = run("select count(*) n, min(congress) c0, max(congress) c1, count(distinct cosponsor_bioguide) n_bio, min(sponsorship_date) d0, max(sponsorship_date) d1 from LIBRARY_RAW.LANDING.FED_GOVINFO_BILL_COSPONSORS", "cosp_profile")
R["tick_overlap"] = run("""select count(distinct t.ticker) st_tickers, count(distinct e.ticker) matched
  from (select distinct upper(trim(ticker)) ticker from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES where ticker is not null and trim(ticker) not in ('','--')) t
  left join (select distinct upper(ticker) ticker from LIBRARY_RAW.LANDING.FED_SEC_EDGAR_COMPANY_TICKERS) e on e.ticker=t.ticker""", "ticker_overlap")
R["vv"] = run("""select min(congress) c0, max(congress) c1, count(*) n from LIBRARY_RAW.LANDING.FED_VOTEVIEW_ROLLCALLS""", "vv_range")
R["vvm"] = run("""select chamber, min(date) d0, max(date) d1, count(*) n from LIBRARY_RAW.LANDING.FED_VOTEVIEW_ROLLCALL_META group by 1""", "vvm_range")
R["leg"] = run("""select count(*) n, count(distinct bioguide) n_bio, count(distinct icpsr) n_icpsr, sum(iff(term_type='sen',1,0)) sen_rows, max(term_end) max_end from LIBRARY_RAW.LANDING.FED_CONGRESS_LEGISLATORS""", "leg_profile")
json.dump(R, open("reports/politics_probe_2026-09-05/_shared/profile_35_78_91.json","w"), indent=1, default=str)
for k,v in R.items():
    print("==", k)
    for r in v[:40]: print("  ", r)
