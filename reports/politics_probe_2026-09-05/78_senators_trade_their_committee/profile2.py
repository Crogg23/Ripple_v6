from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/78_senators_trade_their_committee/probe.log")
for r in run("""select table_schema, table_name, row_count from LIBRARY_RAW.information_schema.tables
  where table_name ilike '%BILL%' or table_name ilike '%STOCK%' or table_name ilike '%TRADE%' or table_name ilike '%PTR%' or table_name ilike '%COMMITTEE%' or table_name ilike '%LEGISLAT%' order by 2""", "other_bill_trade_tables"): print(r)
for r in run("""select column_name, data_type from LIBRARY_RAW.information_schema.columns where table_name='FED_SEC_DERA_SUB_2026Q1' order by ordinal_position""", "dera_cols"): print(r['COLUMN_NAME'], end=", ")
print()
# vintage: trading senators vs roster
for r in run("""select count(distinct t.bioguide) trading_senators, count(distinct c.bioguide) on_current_roster
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES t
  left join LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP c on c.bioguide=t.bioguide and c.committee_code like 'S%' and c.is_subcommittee='False'""", "vintage_overlap"): print(r)
for r in run("""select count(distinct t.bioguide) trading_senators_sponsoring_118_119, count(*) bills
  from LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES t join LIBRARY_RAW.LANDING.FED_GOVINFO_BILLSTATUS b on b.sponsor_bioguide=t.bioguide""", "trader_sponsor_overlap"): print(r)
