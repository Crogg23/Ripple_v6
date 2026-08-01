"""Curated per-column glosses - the hand-written layer that WINS over the
heuristics. Keyed by (fqn_or_'*', COLUMN): '*' means "this column name means
this everywhere" (TTL_RECEIPTS is TTL_RECEIPTS in every FEC table); a full
FQN pins a meaning to one table when the same name means different things.

Re-merged into LIBRARY_META.REGISTRY.COLUMN_CATALOG on every
scripts/build_column_catalog.py --apply run - git is the source of truth, the
warehouse table is the queryable copy. ASCII only, plain English, beer rule.
"""
from __future__ import annotations

STAR = "*"

COLUMN_GLOSS: dict[tuple[str, str], str] = {
    # ---- everywhere ----
    (STAR, "BIOGUIDE"): "Congress's permanent member ID - the cleanest key for a member",
    (STAR, "ICPSR"): "the vote-archive member ID (bridge to roll-call votes)",
    (STAR, "CAND_ID"): "FEC candidate ID (one person can hold several across cycles)",
    (STAR, "CMTE_ID"): "FEC committee ID - the entity that raises and spends",
    (STAR, "TTL_RECEIPTS"): "total money reported taken in (NOT net of transfers - see the trap)",
    (STAR, "TRANS_FROM_AUTH"): "money moved from the candidate's other committees - subtract to avoid double-counting",
    (STAR, "TTL_INDIV_CONTRIB"): "total from individual people",
    (STAR, "TTL_DISB"): "total money reported spent",
    (STAR, "COH_COP"): "cash on hand at close of the period",
    (STAR, "NPI"): "the provider's unique federal number",
    (STAR, "EIN"): "federal employer tax ID (9 digits; check for stripped leading zeros)",
    (STAR, "UEI"): "SAM.gov unique entity ID",
    (STAR, "CYCLE"): "the two-year election cycle the numbers belong to",
    (STAR, "STATE"): "two-letter state code",
    (STAR, "DISTRICT"): "congressional district number (00 = at-large or statewide)",
    (STAR, "PARTY"): "party affiliation as the source records it",
    (STAR, "CHAMBER"): "House or Senate",

    # ---- Senate stock trades (FED_SENATE_STOCK_WATCHER / POLITICS__SENATE_TRADES) ----
    (STAR, "TRANSACTION_DATE"): "the day the senator (or spouse/dependent) made the trade",
    (STAR, "ASSET_DESCRIPTION"): "the asset as written on the filing - free text, may name a company without a ticker",
    (STAR, "ASSET_TYPE"): "what kind of asset: stock, bond, option, fund...",
    (STAR, "OWNER"): "who held it: the senator, spouse, dependent, or joint",
    (STAR, "PTR_LINK"): "link to the original filing this row was parsed from - the receipt",
    (STAR, "SENATOR"): "the senator's name as the filing shows it - free text, not an ID",
    (STAR, "AMOUNT_BAND"): "the disclosure BAND (e.g. $15,001 - $50,000) - filings never give exact amounts; never average the band edges. 'Unknown' is the source's own value when the filing gave no band",
    (STAR, "MATCH_METHOD"): "HOW this row was linked to a member - 'unmatched' means the name match failed and no member claim should ride on it",
    (STAR, "TRANSACTION_TYPE"): "purchase, sale (full or partial), or exchange",
    ("LIBRARY_RAW.LANDING.FED_SENATE_STOCK_WATCHER", "TYPE"):
        "purchase, sale (full or partial), or exchange",
    ("LIBRARY_RAW.LANDING.FED_SENATE_STOCK_WATCHER", "AMOUNT"):
        "the disclosure BAND (e.g. $15,001 - $50,000) - filings never give exact amounts; never average the band edges",
    ("LIBRARY_RAW.LANDING.FED_SENATE_STOCK_WATCHER", "COMMENT"):
        "the filer's free-text note, verbatim",

    # ---- roll-call votes ----
    (STAR, "CAST_CODE"): "how the member voted: yea, nay, present, or not voting (numeric codes from the vote archive)",
    (STAR, "ROLLNUMBER"): "the roll-call vote's number within its congress",
    (STAR, "CONGRESS"): "which two-year Congress (118 = 2023-2024)",

    # ---- OSHA 300A ----
    (STAR, "TOTAL_HOURS_WORKED"): "all hours worked at the establishment that year - the denominator for injury rates",
    (STAR, "ANNUAL_AVERAGE_EMPLOYEES"): "average headcount that year, self-reported",
    (STAR, "TOTAL_DAFW_CASES"): "injuries causing Days Away From Work",
    (STAR, "TOTAL_DJTR_CASES"): "injuries causing Job Transfer or Restriction",

    # ---- LEIE ----
    (STAR, "EXCLTYPE"): "the legal authority for the exclusion (statute code - the app translates it)",
    (STAR, "EXCLDATE"): "the day the exclusion took effect (stored as YYYYMMDD text)",
    (STAR, "REINDATE"): "reinstatement date - all zeros means still excluded",
}
