"""Hunch 91: a senator trades, then sponsors/cosponsors a bill in that sector inside 90 days. SELECT only."""
import json
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/91_trade_then_bill/probe.log")
R = {}
R["date_gap"] = run("""select (select max(transaction_date) from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES) last_trade,
  (select min(to_date(introduced_date)) from LIBRARY_RAW.LANDING.FED_GOVINFO_BILLSTATUS) first_bill,
  (select min(to_date(sponsorship_date)) from LIBRARY_RAW.LANDING.FED_GOVINFO_BILL_COSPONSORS) first_cosponsorship,
  (select count(*) from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES) trades,
  (select count(*) from LIBRARY_RAW.LANDING.FED_GOVINFO_BILLSTATUS) bills""", "date_gap")
R["window_90"] = run("""select count(*) trade_bill_pairs_within_90d, count(distinct t.bioguide) senators
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES t
  join LIBRARY_RAW.LANDING.FED_GOVINFO_BILLSTATUS b on b.sponsor_bioguide = t.bioguide
   and to_date(b.introduced_date) between t.transaction_date and dateadd(day, 90, t.transaction_date)""", "sponsor_within_90d")
R["window_90_cosp"] = run("""select count(*) trade_cosponsor_pairs_within_90d
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES t
  join LIBRARY_RAW.LANDING.FED_GOVINFO_BILL_COSPONSORS c on c.cosponsor_bioguide = t.bioguide
   and to_date(c.sponsorship_date) between t.transaction_date and dateadd(day, 90, t.transaction_date)""", "cosponsor_within_90d")
R["who_overlaps"] = run("""select count(distinct t.bioguide) trading_senators_who_sponsor_in_118_119,
  (select count(distinct bioguide) from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES) trading_senators
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES t join LIBRARY_RAW.LANDING.FED_GOVINFO_BILLSTATUS b on b.sponsor_bioguide=t.bioguide""", "who_overlaps")
R["subject_cols"] = run("""select column_name from LIBRARY_RAW.information_schema.columns
  where table_name in ('FED_GOVINFO_BILLSTATUS','FED_GOVINFO_BILL_COSPONSORS') and (column_name ilike '%SUBJ%' or column_name ilike '%POLICY%' or column_name ilike '%COMMITTEE%')""", "bill_subject_cols")
json.dump(R, open("reports/politics_probe_2026-09-05/91_trade_then_bill/results.json","w"), indent=1, default=str)
for k,v in R.items():
    print("==", k)
    for r in v: print("  ", r)
