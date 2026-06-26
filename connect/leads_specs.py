"""Declarative specs for the cross-domain LEAD jobs run by ``connect leads``.

A lead job is config, not code: each entry in ``JOBS`` describes a cross-domain
pattern that ``leads.compile_sql`` turns into one targeted SQL query, scores, and
persists. The general shape is a hard-key INTERSECTION — a LEFT "flag" list
(sanctions / exclusions / debarment) meeting a RIGHT "active" list (affiliations /
broadcasts / awards) on a shared ID. The SAME engine serves every domain; only the
spec changes. Adding a new smell across a new world = adding a dict here.

Column names below were confirmed live against LIBRARY_RAW.LANDING.

JobSpec shape:
  rule_name        unique id; also the stable LEAD_ID prefix
  title_template   str.format-ed per lead from the left display fields + {count}/{plural}
  left / right     {table, key, key_col, ...one name option..., carry{alias:col}}
                     name options: name_cols=[last,first] (person, enables surname
                     corroboration) | name_col="COL" (org/vessel, display only) | none
  left.recency     {col, format, months}            -> recency component of the score
  right.enrich_key / enrich_key_col                 -> secondary key counted for breadth
  enrich_name      {key, tables:[(table,name_col)], label?}  -> enrich key -> human name
  require_surname  drop pairs whose surnames disagree (person-vs-person only)
  score            {name_w?, recency_w?, breadth_w?, breadth_div?}  (absent weight = 0)
  title_titlecase / title_dates   field names to nice-case / date-format in the title
  no_fanout_guard  MUST be True: lead jobs run their own SQL, never connect.bridge
                   (its FANOUT_MAX / dedup would silently drop high-value leads).
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
    # HEALTH × HEALTH on NPI — an OIG-excluded provider still on CMS facility rosters.
    "banned_but_operating": {
        "rule_name": "banned_but_operating",
        "title_template": ("{l_first} {l_last} — OIG-excluded ({excltype}, {excldate}); "
                           "affiliated with {count} CMS facilit{plural}"),
        "left": {
            "table": "FED_HHS_OIG_LEIE",
            "key": "NPI", "key_col": "NPI",
            "name_cols": ["LASTNAME", "FIRSTNAME"],
            "carry": {"EXCLTYPE": "EXCLTYPE", "EXCLDATE": "EXCLDATE",
                      "CITY": "CITY", "STATE": "STATE"},
            "recency": {"col": "EXCLDATE", "format": "YYYYMMDD", "months": 12},
        },
        "right": {
            "table": "FED_CMS_FACILITY_AFFILIATION",
            "key": "NPI", "key_col": "NPI",
            "name_cols": ["PROVIDER_LAST_NAME", "PROVIDER_FIRST_NAME"],
            "enrich_key": "CCN", "enrich_key_col": "CCN",
            "carry": {"FACILITY_TYPE": "FACILITY_TYPE"},
        },
        "enrich_name": {"key": "CCN", "tables": _FACILITY_NAME_TABLES},
        "require_surname": True,
        "score": {"name_w": 0.5, "recency_w": 0.3, "breadth_w": 0.2, "breadth_div": 10.0},
        "title_titlecase": ["l_first", "l_last"],
        "title_dates": ["excldate"],
        "no_fanout_guard": True,
    },

    # SANCTIONS × MARITIME on IMO — an OFAC-sanctioned hull still broadcasting AIS.
    # The vessel can repaint its name (AIS name often differs from the OFAC name);
    # the IMO hull number can't change, so the hard-key join catches it anyway.
    "sanctioned_vessel_broadcasting": {
        "rule_name": "sanctioned_vessel_broadcasting",
        "title_template": ("{l_name} — OFAC-sanctioned ({program}, flag {flag}); "
                           "broadcasting AIS in {count} position reports"),
        "left": {
            "table": "FED_OFAC_SDN",
            "key": "IMO", "key_col": "IMO",
            "name_col": "SDN_NAME",
            "carry": {"PROGRAM": "PROGRAM", "FLAG": "VESS_FLAG"},
        },
        "right": {
            "table": "FED_NOAA_AIS",
            "key": "IMO", "key_col": "IMO",
            "carry": {"AIS_NAME": "VESSELNAME"},
        },
        "score": {"breadth_w": 1.0, "breadth_div": 200.0},
        "no_fanout_guard": True,
    },

    # SANCTIONS × SPENDING on UEI — a federally-debarred entity still holding federal
    # contract awards. UEI is a 12-char hard ID (keys.py 'fixed' mode), so a hit means
    # the SAME legal entity SAM excluded is the one USASpending paid — FACT-grade. SAM
    # carries UEI on the org exclusions only (individuals have a name, no UEI), so this
    # surfaces debarred FIRMS; breadth = how many award rows that UEI pulled. ENTITY_NAME
    # (left) vs RECIPIENT_NAME (right, in evidence) lets a human eyeball that the UEI
    # match is corroborated by name — a 12-char coincidence can't also match the name.
    # NB: SAM ACTIVATION_DATE is blank in the source, so there's no recency component and
    # no "awarded AFTER the debarment date" framing yet — that unlocks when SAM lands fully.
    "debarred_but_funded": {
        "rule_name": "debarred_but_funded",
        "title_template": ("{l_name} — federally debarred ({classification}, {exclusion_type}) "
                           "by {excluding_agency}; {count} federal contract awards"),
        "left": {
            "table": "FED_SAM_EXCLUSIONS",
            "key": "UEI", "key_col": "UEI",
            "name_col": "ENTITY_NAME",
            "carry": {"CLASSIFICATION": "CLASSIFICATION", "EXCLUSION_TYPE": "EXCLUSION_TYPE",
                      "EXCLUDING_AGENCY": "EXCLUDING_AGENCY"},
        },
        "right": {
            "table": "FED_USASPENDING_CONTRACTS",
            "key": "UEI", "key_col": "RECIPIENT_UEI",
            "carry": {"AWARDING_AGENCY": "AWARDING_AGENCY_NAME", "RECIPIENT_NAME": "RECIPIENT_NAME"},
        },
        "score": {"breadth_w": 1.0, "breadth_div": 100.0},
        "no_fanout_guard": True,
    },
}
