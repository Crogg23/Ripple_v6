"""Discovery shared by hunches 35/78/91: columns + row counts of every table in the chain. SELECT only."""
import json, sys
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/78_senators_trade_their_committee/probe.log")
NAMES = "('SENATE_TRADES','FED_SENATE_STOCK_WATCHER','FED_HOUSE_FD_PTR_INDEX','FED_CONGRESS_COMMITTEE_MEMBERSHIP','FED_CONGRESS_LEGISLATORS','FED_GOVINFO_BILLSTATUS','FED_GOVINFO_BILL_COSPONSORS','FED_SEC_EDGAR_COMPANY_TICKERS','FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE','FED_VOTEVIEW_ROLLCALLS','FED_VOTEVIEW_ROLLCALL_META','FED_CONGRESS_COMMITTEES')"
out = {}
for db in ("LIBRARY_RAW", "LIBRARY_MARTS"):
    rows = run(f"""select table_schema, table_name, column_name, data_type, ordinal_position
        from {db}.information_schema.columns
        where regexp_replace(table_name, '^[A-Z]+__', '') in {NAMES} or table_name like '%SENATE_TRADES%' or table_name like '%FD_PTR%'
        order by 1,2,5""", f"cols_{db}")
    for r in rows:
        out.setdefault(f"{db}.{r['TABLE_SCHEMA']}.{r['TABLE_NAME']}", []).append(f"{r['COLUMN_NAME']}:{r['DATA_TYPE']}")
    rows = run(f"""select table_schema, table_name, row_count from {db}.information_schema.tables
        where regexp_replace(table_name, '^[A-Z]+__', '') in {NAMES} or table_name like '%SENATE_TRADES%' or table_name like '%FD_PTR%'""", f"rows_{db}")
    for r in rows:
        out[f"{db}.{r['TABLE_SCHEMA']}.{r['TABLE_NAME']}"].insert(0, f"ROWS={r['ROW_COUNT']}")
json.dump(out, open("reports/politics_probe_2026-09-05/_shared/discover_35_78_91.json","w"), indent=1)
for k,v in out.items(): print(k, v[0], len(v)-1, "cols"); print("   ", ", ".join(v[1:]))
