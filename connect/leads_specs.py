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
  date_mode        OPTIONAL 'gate' | 'annotate' + left_date_field and right_date_field
                   (or right_year_field). 'gate' keeps only activity dated on/after the
                   flag date; 'annotate' adds no predicate but carries both dates into
                   each evidence item under 'timeline'. Date fields are a bare column
                   name or {"col":..., "format":...} (TRY_TO_DATE format). A spec
                   WITHOUT these compiles byte-identically to the pre-feature SQL, so
                   existing SQL_SHA256 receipts never churn. No live rule uses it yet.
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

    # SANCTIONS × MARITIME on IMO — an OFAC-sanctioned hull appearing in the NOAA AIS
    # archive. The vessel can repaint its name (AIS name often differs from the OFAC
    # name); the IMO hull number can't change, so the hard-key join catches it anyway.
    # ARCHIVE-HONEST title on purpose: NOAA AIS is a US-coastal ARCHIVE, not a live
    # feed, so "broadcasting" would overclaim — the data shows the hull APPEARED, not
    # that it's transmitting today. Safe to rephrase in place: LEAD_ID is md5 of
    # rule + key value (title-independent), so the MERGE just updates titles next run.
    "sanctioned_vessel_broadcasting": {
        "rule_name": "sanctioned_vessel_broadcasting",
        "title_template": ("{l_name} — OFAC-sanctioned ({program}, flag {flag}); "
                           "appears in {count} AIS position reports (US-coastal "
                           "archive; not evidence of current broadcasting)"),
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

    # HEALTH × MONEY on NPI — an OIG-excluded provider still receiving pharma/device
    # payments (CMS Open Payments / Sunshine Act). NPI is a 10-char STEEL key, so a hit
    # is the SAME provider OIG excluded; require_surname corroborates against a fat-finger
    # NPI. breadth = number of Open Payments records that NPI pulled. NEUTRAL phrasing
    # ("appears in N records") on purpose: co-occurrence on NPI is FACT-grade, but
    # "paid WHILE excluded" only holds when EXCLDATE precedes the payment year — that
    # timeline lives in the evidence (excldate), not the title, so the title never
    # overclaims for the later-excluded cases (e.g. paid in 2024, excluded 2025).
    "banned_but_paid": {
        "rule_name": "banned_but_paid",
        "title_template": ("{l_first} {l_last} — OIG-excluded ({excltype}, {excldate}); "
                           "appears in {count} CMS Open Payments record(s)"),
        "left": {
            "table": "FED_HHS_OIG_LEIE",
            "key": "NPI", "key_col": "NPI",
            "name_cols": ["LASTNAME", "FIRSTNAME"],
            "carry": {"EXCLTYPE": "EXCLTYPE", "EXCLDATE": "EXCLDATE",
                      "CITY": "CITY", "STATE": "STATE"},
        },
        "right": {
            # All-years union (2023 + 2024), NOT the unsuffixed 2024-only landing table
            # (discovery sweep #23: the bare name is a half-the-data trap, and 338/353
            # leads ride this edge). The int view is a SELECT * passthrough so column
            # names are unchanged; the engine reads it via the fully-qualified name.
            "table": "LIBRARY_STAGING.DBT_CROGERS.INT_OPEN_PAYMENTS_ALL_YEARS",
            "key": "NPI", "key_col": "NPI",
            "name_cols": ["COVERED_RECIPIENT_LAST_NAME", "COVERED_RECIPIENT_FIRST_NAME"],
            "carry": {"PAYER": "APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME",
                      "NATURE": "NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE",
                      "YEAR": "PROGRAM_YEAR"},
        },
        "require_surname": True,
        "score": {"name_w": 0.4, "breadth_w": 0.6, "breadth_div": 50.0},
        "title_titlecase": ["l_first", "l_last"],
        "title_dates": ["excldate"],
        "no_fanout_guard": True,
    },

    # HEALTH × HEALTH on NPI — an OIG-excluded provider still billing Medicare Part D
    # (discovery sweep #27). 243 excluded providers carry a real NPI that appears in the
    # Part D prescriber file. NEUTRAL phrasing ("appears in N records") on purpose: the
    # engine can't date-gate, so "billed WHILE excluded" only holds where EXCLDATE precedes
    # the Part D program year — that timeline lives in the evidence (excldate), not the
    # title. WVRSTATE is carried so a reviewer sees the waiver (the one known survivor,
    # NPI 1285673012, has an OIG waiver -> human-review LEAD, never auto-FACT). All leads
    # default pending/unpublished via the safety gate, so this is review-only by design.
    "excluded_but_billing": {
        "rule_name": "excluded_but_billing",
        "title_template": ("{l_first} {l_last} — OIG-excluded ({excltype}, {excldate}); "
                           "appears in {count} Medicare Part D prescriber record(s)"),
        "left": {
            "table": "FED_HHS_OIG_LEIE",
            "key": "NPI", "key_col": "NPI",
            "name_cols": ["LASTNAME", "FIRSTNAME"],
            "carry": {"EXCLTYPE": "EXCLTYPE", "EXCLDATE": "EXCLDATE",
                      "WVRSTATE": "WVRSTATE", "STATE": "STATE"},
            "recency": {"col": "EXCLDATE", "format": "YYYYMMDD", "months": 24},
        },
        "right": {
            "table": "FED_CMS_PART_D_PRESCRIBERS",
            "key": "NPI", "key_col": "NPI",
            "name_cols": ["PRSCRBR_LAST_ORG_NAME", "PRSCRBR_FIRST_NAME"],
            "carry": {"DRUG_COST": "TOT_DRUG_CST", "OPIOID_COST": "OPIOID_TOT_DRUG_CST"},
        },
        "require_surname": True,
        "score": {"name_w": 0.5, "recency_w": 0.2, "breadth_w": 0.3, "breadth_div": 5.0},
        "title_titlecase": ["l_first", "l_last"],
        "title_dates": ["excldate"],
        "no_fanout_guard": True,
    },

    # SANCTIONS × MARITIME on IMO, v2 — left is now OFAC SDN ∪ OpenSanctions vessels
    # (int_sanctioned_vessels), NOT OFAC alone: OpenSanctions catches ~3x the broadcasting
    # hulls and only 1,486 of OFAC's 1,942 vessel IMOs overlap (#16/#17). 2,449 distinct
    # sanctioned IMOs now vs 1,942. The vessel can repaint its broadcast name, so AIS_NAME
    # (carried into evidence) vs the sanctions VESSEL_NAME (title) is a shadow-fleet-rename
    # tell — the IMO hull number can't change, so the hard-key join catches it regardless.
    # (An explicit name_mismatch score would need a small engine add; both names are already
    # surfaced in the lead for the human reviewer.) Title is archive-honest like v1: the
    # AIS data is a US-coastal archive, so "appears in" — never "broadcasting".
    "sanctioned_vessel_broadcasting_v2": {
        "rule_name": "sanctioned_vessel_broadcasting_v2",
        "title_template": ("{l_name} — sanctioned vessel ({sanction_source}, {program}); "
                           "appears in {count} AIS position report(s) (US-coastal "
                           "archive; not evidence of current broadcasting)"),
        "left": {
            "table": "LIBRARY_STAGING.DBT_CROGERS.INT_SANCTIONED_VESSELS",
            "key": "IMO", "key_col": "IMO",
            "name_col": "VESSEL_NAME",
            "carry": {"SANCTION_SOURCE": "SANCTION_SOURCE", "PROGRAM": "PROGRAM", "FLAG": "FLAG"},
        },
        "right": {
            "table": "FED_NOAA_AIS",
            "key": "IMO", "key_col": "IMO",
            "carry": {"AIS_NAME": "VESSELNAME"},
        },
        "score": {"breadth_w": 1.0, "breadth_div": 200.0},
        "no_fanout_guard": True,
    },

    # MONEY × MONEY on EIN — a company that files financials with the SEC whose EIN
    # ALSO appears in the IRS exempt-org (tax-exempt) master file. EIN is a 9-digit
    # STEEL key (keys.py 'pad' 9), so a hit is the SAME legal entity's tax ID on both
    # rosters — a hard, non-coincidental co-occurrence. This is the biggest lever
    # against the single-vertical concentration: it opens MONEY/finance as a second
    # world beyond the health-provider verticals that carry ~all leads today. Both
    # sides are ORG lists -> single-name display, NO surname gate (require_surname is
    # person-vs-person only; org-vs-org would never corroborate). LEFT is the SEC
    # financial-statement filer list (FED_SEC_EDGAR_FINANCIALS: 55,635 rows / 5,773
    # distinct EINs, carries NAME + CIK) — deliberately NOT FED_US_SEC_EDGAR, whose EIN
    # column is junk (48,990 rows collapse to 25 distinct EINs). RIGHT is the IRS BMF
    # (FED_IRS_BMF: 1.97M distinct EINs, the registered tax-exempt roster).
    #
    # NEUTRAL, co-occurrence phrasing on purpose: the title states the two rosters share
    # an EIN — it is NOT a violation claim. A commercial SEC filer legitimately sharing a
    # tax ID with an exempt entity (foundation, pension trust, related nonprofit) is a
    # thread to PULL, not a finding to assert; the human reviewer + evidence (SEC NAME/CIK
    # vs IRS NAME/STATE/NTEE) decides what it means.
    #
    # YIELD: ~3 leads today (measured 2026-07-02: 3 distinct EINs overlap both rosters,
    # normalized pad-9). The value is the CAPABILITY + the new vertical, not the count —
    # the overlap grows as more EIN-bearing SEC/IRS sources land.
    #
    # RECEIPT CAVEAT (documented, NOT fixed here): FED_IRS_BMF's provenance columns lack
    # the underscore prefix (it carries INGESTED_AT / SOURCE_RUN_ID / SRC_SHA256, not the
    # standard _-prefixed trio). receipt.resolve_snapshots SELECTs _SOURCE_RUN_ID, so the
    # IRS-BMF leg records 'unresolved' until BMF is re-landed with standard provenance —
    # honest-but-hollow on that one leg, acceptable for now.
    "sec_filer_in_irs_bmf": {
        "rule_name": "sec_filer_in_irs_bmf",
        "title_template": ("{l_name} — SEC filer (CIK {cik}) EIN also appears in the IRS "
                           "exempt-org roster ({count} record(s))"),
        "left": {
            "table": "FED_SEC_EDGAR_FINANCIALS",
            "key": "EIN", "key_col": "EIN",
            "name_col": "NAME",
            "carry": {"CIK": "CIK"},
        },
        "right": {
            "table": "FED_IRS_BMF",
            "key": "EIN", "key_col": "EIN",
            "carry": {"IRS_NAME": "NAME", "STATE": "STATE", "NTEE": "NTEE_CD"},
        },
        "score": {"breadth_w": 1.0, "breadth_div": 10.0},
        "no_fanout_guard": True,
    },
}
