"""Hunch 78: senators trading tickers whose SIC falls in the sector their (current) Senate committee marks up.
Discovery is in discover.py / profile.py / profile2.py (same folder, same probe.log). SELECT only."""
import json
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/78_senators_trade_their_committee/probe.log")
R = {}
# Ticker -> CIK (EDGAR company tickers) -> SIC (DERA SUB, 2024Q1..2026Q1, latest filing per CIK)
SIC_MAP = """
dera as (
  select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2024Q1 union all select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2024Q2
  union all select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2024Q3 union all select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2024Q4
  union all select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2025Q1 union all select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2025Q2
  union all select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2025Q3 union all select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2025Q4
  union all select cik, sic, filed from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2026Q1),
cik_sic as (
  select try_to_number(cik) cik, try_to_number(sic) sic from dera where nullif(trim(sic),'') is not null
  qualify row_number() over (partition by try_to_number(cik) order by filed desc) = 1),
tick_sic as (
  select upper(e.ticker) ticker, min(s.sic) sic
  from LIBRARY_RAW.LANDING.FED_SEC_EDGAR_COMPANY_TICKERS e join cik_sic s on s.cik = try_to_number(e.cik_str)
  group by 1),
-- hand crosswalk: full Senate committee -> 4-digit SIC ranges it plainly marks up. Coarse on purpose; first number only.
cw as (
  select * from values
   ('SSBK', 6000, 6799, 'banks, insurance, real estate'),
   ('SSEG', 1000, 1499, 'mining, oil and gas'), ('SSEG', 2900, 2999, 'petroleum refining'), ('SSEG', 4900, 4999, 'utilities'),
   ('SSAS', 3720, 3729, 'aircraft'), ('SSAS', 3760, 3769, 'missiles, space'), ('SSAS', 3480, 3489, 'ordnance'), ('SSAS', 3812, 3812, 'defense electronics'),
   ('SSHR', 2830, 2836, 'pharma, biotech'), ('SSHR', 3840, 3851, 'medical devices'), ('SSHR', 8000, 8099, 'health services'),
   ('SSCM', 4800, 4899, 'telecom, broadcasting'), ('SSCM', 4500, 4599, 'airlines'), ('SSCM', 4000, 4299, 'rail, trucking'), ('SSCM', 3570, 3579, 'computers'), ('SSCM', 3670, 3679, 'semiconductors'), ('SSCM', 7370, 7379, 'software, internet'),
   ('SSAF', 100, 999, 'farming'), ('SSAF', 2000, 2099, 'food products'),
   ('SSEV', 1600, 1699, 'heavy construction'), ('SSEV', 3200, 3299, 'cement, glass'), ('SSEV', 4950, 4959, 'waste')
   as t(committee_code, sic_lo, sic_hi, sector)),
trades as (
  select bioguide, senator, upper(trim(ticker)) ticker, transaction_date, transaction_type, amount_band
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES
  where ticker is not null and trim(ticker) not in ('', '--', 'N/A') and transaction_type in ('Purchase','Sale (Full)','Sale (Partial)')),
seat as (
  select distinct bioguide, committee_code, committee_name from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
  where committee_code like 'S%' and is_subcommittee = 'False'),
hits as (
  select t.*, ts.sic, s.committee_code, s.committee_name, cw.sector
  from trades t join tick_sic ts on ts.ticker = t.ticker
  join seat s on s.bioguide = t.bioguide
  join cw on cw.committee_code = s.committee_code and ts.sic between cw.sic_lo and cw.sic_hi)
"""
R["coverage"] = run(f"""with {SIC_MAP}
  select (select count(*) from tick_sic) tickers_with_sic,
         (select count(distinct ticker) from trades) traded_tickers,
         (select count(distinct t.ticker) from trades t join tick_sic ts on ts.ticker=t.ticker) traded_tickers_with_sic,
         (select count(*) from trades) trade_rows,
         (select count(*) from trades t join tick_sic ts on ts.ticker=t.ticker) trade_rows_with_sic""", "coverage")
R["headline"] = run(f"""with {SIC_MAP}
  select count(distinct bioguide) senators, count(*) trades, count(distinct ticker) tickers,
         min(transaction_date) d0, max(transaction_date) d1 from hits""", "headline")
R["by_committee"] = run(f"""with {SIC_MAP}
  select committee_code, count(distinct bioguide) senators, count(*) trades, count(distinct ticker) tickers from hits group by 1 order by 3 desc""", "by_committee")
R["by_senator"] = run(f"""with {SIC_MAP}
  select senator, bioguide, committee_code, count(*) trades, count(distinct ticker) tickers, min(transaction_date) d0, max(transaction_date) d1,
         listagg(distinct ticker, ' ') within group (order by ticker) some_tickers
  from hits group by 1,2,3 order by 4 desc limit 12""", "by_senator")
R["eyeball"] = run(f"""with {SIC_MAP} select senator, ticker, sic, sector, committee_name, transaction_date, transaction_type from hits order by random() limit 5""", "eyeball_5")
json.dump(R, open("reports/politics_probe_2026-09-05/78_senators_trade_their_committee/results.json","w"), indent=1, default=str)
for k,v in R.items():
    print("==", k)
    for r in v: print("  ", r)
