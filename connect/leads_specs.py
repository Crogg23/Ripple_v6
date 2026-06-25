"""Declarative specs for the cross-domain LEAD jobs run by ``connect leads``.

A lead job is config, not code: each entry in ``JOBS`` describes a cross-domain
pattern ("an OIG-excluded provider still affiliated with CMS facilities") that
``leads.run_job`` compiles to one targeted SQL query, scores, and persists.

Column names below were confirmed live against LIBRARY_RAW.LANDING on 2026-06-25
(see the Phase-1 pre-step). Adding a new job = adding a dict here, not touching
leads.py.

JobSpec shape:
  rule_name        unique id; also the stable LEAD_ID prefix
  title_template   str.format-ed per lead from {l_first,l_last,excltype,excldate,count}
  left/right       {table, key, key_col, last_col, first_col, carry{alias:col}}
  left.recency     {col, format, months}   -> recency component of the score
  right.enrich_key,enrich_key_col          -> the secondary key the enrich tables share
  enrich_name      {key, tables:[(table,name_col)]}  -> key -> a human facility name
  require_surname  drop pairs whose surnames disagree (the fluke guard)
  score            {name_w, recency_w, breadth_w, breadth_div}
  no_fanout_guard  MUST be True: lead jobs run their own SQL and never route through
                   connect.bridge (its FANOUT_MAX / dedup-vs-direct would silently
                   drop high-value leads — see build-state.md "ENGINE NUANCE").
"""

from __future__ import annotations

# The 7 CCN facility rosters: CCN -> a human facility name. All carry a `CCN`
# column (bridge_fuel aliased it); the name column differs per roster.
_FACILITY_NAME_TABLES = [
    ("FED_CMS_POS_OTHER", "FAC_NAME"),
    ("FED_CMS_HOSPITAL_GENERAL", "FACILITY_NAME"),
    ("FED_CMS_HOSPICE", "FACILITY_NAME"),
    ("FED_CMS_HOME_HEALTH", "PROVIDER_NAME"),
    ("FED_CMS_IRF", "PROVIDER_NAME"),
    ("FED_CMS_LTCH", "PROVIDER_NAME"),
    ("FED_CMS_DIALYSIS", "FACILITY_NAME"),
]

JOBS: dict[str, dict] = {
    "banned_but_operating": {
        "rule_name": "banned_but_operating",
        "title_template": ("{l_first} {l_last} — OIG-excluded ({excltype}, {excldate}); "
                           "affiliated with {count} CMS facilit{plural}"),
        "left": {
            "table": "FED_HHS_OIG_LEIE",
            "key": "NPI", "key_col": "NPI",
            "last_col": "LASTNAME", "first_col": "FIRSTNAME",
            "carry": {"EXCLTYPE": "EXCLTYPE", "EXCLDATE": "EXCLDATE",
                      "CITY": "CITY", "STATE": "STATE"},
            "recency": {"col": "EXCLDATE", "format": "YYYYMMDD", "months": 12},
        },
        "right": {
            "table": "FED_CMS_FACILITY_AFFILIATION",
            "key": "NPI", "key_col": "NPI",
            "last_col": "PROVIDER_LAST_NAME", "first_col": "PROVIDER_FIRST_NAME",
            "enrich_key": "CCN", "enrich_key_col": "CCN",
            "carry": {"FACILITY_TYPE": "FACILITY_TYPE"},
        },
        "enrich_name": {"key": "CCN", "tables": _FACILITY_NAME_TABLES},
        "require_surname": True,
        "score": {"name_w": 0.5, "recency_w": 0.3, "breadth_w": 0.2, "breadth_div": 10.0},
        "no_fanout_guard": True,
    },
}
