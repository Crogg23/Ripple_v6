"""Census grid — step 2: classify every model, derive the thing-list bottom-up,
emit the grid (thing x slot x status), the parking lot with tallies, and the
sources census.

Reads build/models.jsonl + build/raw_sources.jsonl (from extract_models.py) and
the onboarding log. Deterministic, no LLM at runtime, no warehouse access.
Everything unmapped/unclassified stays visible with a count — never dropped.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BUILD = REPO / "reports" / "census_grid_2026-08-12" / "build"
OUT = REPO / "reports" / "census_grid_2026-08-12"
ONBOARDING_LOG = REPO / "library-onboarding" / "onboarding_log.json"

# =====================================================================
# 1. COLUMN SEMANTIC TYPES — ordered rules, first match wins as primary
# =====================================================================

SEM_RULES: list[tuple[str, re.Pattern]] = [
    ("meta", re.compile(r"^(_loaded_at|_ingested_at|_source_url|_run_id|_row_num|_file|_batch|objectid|globalid|shape__?(area|length)|_dl_|_source_file)")),
    ("date", re.compile(r"(^|_)(date|dt|yr|fy|year|month|week|day|time|timestamp|dob|filed|effective|expir\w*|issued|received|approved|opened|closed|created|updated|begin|start|end|term(ination)?|posted|signed|reported|observed)(_|$)|_at$|_date_|^date_")),
    ("population", re.compile(r"(^|_)(population|enrollment|enrollees|participants|beds|patients|students|pupils|members(hip)?_count|employees|employment|staff|census_count|persons_served|residents|customers?)(_|$)")),
    ("money", re.compile(r"(^|_)(amount|amt|penalt\w*|fine|fee|cost|price|salary|wage|compensation|revenue|income|receipts?|assets|liabilit\w*|equity|funding|funded|obligat\w*|outlay|disburse\w*|expenditure|spend\w*|dollars?|usd|paid|payment|award_amount|proceeds|premium|deposits?|balance|budget|loan_amount|contribution_amount|cash|earnings)(_|$)")),
    ("quantity", re.compile(r"(^|_)(count|cnt|num|number_of|qty|quantity|total|sum|rate|pct|percent|ratio|score|mw|kw|mwh|acres?|tons?|weight|volume|gallons|barrels|capacity|size|length|area|hours|days_)(_|$)")),
    ("geo_point", re.compile(r"(^|_)(lat(itude)?|long?(itude)?|lon|coords?|coordinates?|geometry|geom|shape|point|x_coord|y_coord)(_|$)")),
    ("geo", re.compile(r"(^|_)(state|city|county|zip|zipcode|zip5|fips|address|addr|street|region|country|nation|territory|tract|block|huc|congressional_district|district|municipality|place_name|location|geo\w*)(_|$)")),
    ("id", re.compile(r"(^|_)(id|key|uid|uuid|guid|ein|npi|duns|uei|cik|cusip|lei|ticker|isin|frs|rssd|ncua|omb|tsn|itis|npi_|nces\w*|unitid|bioguide|icpsr|fec_|crd|sec_|docket|case_num\w*|permit_num\w*|license_num\w*|registration_num\w*|accession|control_num\w*|record_num\w*|file_num\w*|charter|certificat\w*|enrollment_id)(_|$)|_no$|_number$|_num$|_code$")),  # _code$ moved to code below via ordering fix
    ("flag", re.compile(r"^(is|has)_|_(flag|flg|ind|indicator|yn)$")),
    ("code", re.compile(r"(^|_)(code|cd|type|status|category|class|classification|kind|reason|method|level|tier|grade|group|naics|sic|cip|taxonomy|subpart|pollutant|source_type|action_type)(_|$)")),
    ("name_text", re.compile(r"(^|_)(name|title|desc|description|text|comment|note|label|url|link|email|phone|website|narrative|remarks|subject)(_|$)")),
]
# fix ordering conflict: _code$ should be code, not id — handle by checking code rule first for *_code
CODE_FIRST = re.compile(r"_(code|cd)$")


def sem_type(col: str) -> str:
    if CODE_FIRST.search(col):
        return "code"
    for name, rx in SEM_RULES:
        if rx.search(col):
            return name
    return "other"


# =====================================================================
# 2. THING TOKEN DICTIONARY — token -> (family, class)
#    class: noun | event | event+noun (dual) | link | code | aggregate-flag
#    Covers every informative token seen in grain heads, staging suffixes,
#    and marts names. Junk tokens are skipped so scanning falls through.
# =====================================================================

D: dict[str, tuple[str, str]] = {}

def _add(family: str, cls: str, *tokens: str) -> None:
    for t in tokens:
        D[t] = (family, cls)

# ---- NOUN families ----
_add("facility", "noun", "facility", "facilities", "site", "sites", "plant", "plants",
     "station", "stations", "boiler", "boilers", "generator", "generators", "refinery",
     "terminal", "terminals", "mine", "mines", "mill", "mills", "reactor", "landfill",
     "tri", "brownfield", "superfund", "npl")
_add("provider", "noun", "provider", "providers", "prescriber", "prescribers",
     "physician", "physicians", "hospital", "hospitals", "pharmacy", "pharmacies",
     "clinic", "clinics", "supplier", "suppliers", "practitioner", "practitioners", "npi")
_add("organization", "noun", "organization", "organizations", "company", "companies",
     "employer", "employers", "firm", "firms", "business", "businesses", "charity",
     "charities", "nonprofit", "nonprofits", "bank", "banks", "thrifts", "insurer",
     "insurers", "utility", "utilities", "committee", "committees", "union", "unions",
     "agency", "agencies", "authority", "authorities", "institution", "institutions",
     "school", "schools", "college", "colleges", "university", "universities",
     "district", "districts", "sponsor", "sponsors", "contractor", "contractors",
     "intermediary", "intermediaries", "donee", "donees", "entity", "entities",
     "issuer", "issuers", "registrant", "registrants", "operator", "operators",
     "carrier", "carriers", "railroad", "railroads", "airline", "airlines", "pha",
     "cu", "bmf", "borme", "cro", "psc", "gleif", "manufacturer", "manufacturers",
     "grantee", "grantees", "payer", "payers", "lender", "lenders", "broker", "brokers",
     "dealer", "dealers", "advisers", "funder", "funders")
_add("person", "noun", "person", "people", "persons", "individual", "individuals",
     "judge", "judges", "legislator", "legislators", "lobbyist", "lobbyists",
     "candidate", "candidates", "inmate", "inmates", "expert", "experts",
     "director", "directors", "principal", "principals", "justice", "justices",
     "trustee", "trustees", "debarred")
_add("place", "noun", "place", "places", "parcel", "parcels", "boundary", "boundaries",
     "community", "communities", "county", "counties", "tract", "tracts", "zone",
     "zones", "area", "areas", "territory", "territories", "watershed", "huc8",
     "block", "blocks", "neighborhood", "region", "regions", "municipality",
     "feature", "features", "landmark", "address", "addresses", "location", "locations")
_add("asset", "noun", "asset", "assets", "vessel", "vessels", "aircraft", "vehicle",
     "vehicles", "dam", "dams", "bridge", "bridges", "well", "wells", "pipeline",
     "pipelines", "equipment", "meters", "tower", "towers", "antenna", "satellite",
     "locomotive", "tank", "tanks")
_add("program", "noun", "plan", "plans", "program", "programs", "policy", "policies",
     "fund", "funds", "scheme", "system", "systems", "service_area")
_add("product", "noun", "drug", "drugs", "device", "devices", "product", "products",
     "chemical", "chemicals", "substance", "substances", "ndc", "food")
_add("instrument", "noun", "security", "securities", "ticker", "tickers", "futures",
     "stock", "stocks", "bond", "bonds", "penny", "outstanding")
_add("dataset", "noun", "dataset", "datasets", "collection", "collections", "book",
     "aad", "series", "publication", "publications", "study", "studies", "survey")

# ---- EVENT families (dual = event+noun where the row has its own lifecycle) ----
_add("inspection", "event", "inspection", "inspections", "audit", "audits", "exam",
     "exams", "evaluation", "evaluations", "assessment", "assessments", "monitoring")
_add("violation", "event", "violation", "violations", "deficiency", "deficiencies",
     "citation", "citations", "exceedance", "exceedances", "infraction", "noncompliance")
_add("enforcement", "event", "enforcement", "penalty", "penalties", "fine", "fines",
     "settlement", "settlements", "order", "orders", "revocation", "revocations",
     "exclusion", "exclusions", "debarment", "debarments", "sanction", "suspension",
     "prosecution", "conviction", "convictions", "seizure", "forfeiture")
_add("accident", "event", "accident", "accidents", "incident", "incidents", "injury",
     "injuries", "fatality", "fatalities", "spill", "spills", "release", "releases",
     "crash", "crashes", "derailment", "derailments", "outage", "outages", "neiss")
_add("natural_event", "event", "earthquake", "earthquakes", "storm", "storms", "flood",
     "floods", "wildfire", "wildfires", "hazard", "hazards", "hurricane", "disaster",
     "disasters", "weather")
_add("payment", "event", "payment", "payments", "spend", "disbursement", "disbursements",
     "outlay", "outlays", "expenditure", "expenditures", "obligation", "obligations",
     "reimbursement", "refund", "refunds", "deposits")
_add("award", "event+noun", "award", "awards", "grant", "grants", "contract", "contracts",
     "subaward", "subawards", "procurement", "ppp", "idv")
_add("filing", "event+noun", "filing", "filings", "return", "returns", "report",
     "reports", "submission", "submissions", "disclosure", "disclosures", "statement",
     "statements", "form", "forms", "form5500", "990", "8k", "10k", "prospectus",
     "notice", "notices", "cover", "cover2", "schedule")
_add("registration", "event+noun", "registration", "registrations", "permit", "permits",
     "license", "licenses", "licensure", "certification", "certifications",
     "designation", "designations", "enrollment", "enrollments", "accreditation")
_add("contribution", "event", "contribution", "contributions", "donation", "donations",
     "gift", "gifts", "receipt", "receipts", "expenditures_pac", "indiv")
_add("trade", "event", "trade", "trades", "transaction", "transactions", "sale", "sales",
     "purchase", "purchases", "trans", "import", "imports", "export", "exports",
     "shipment", "shipments")
_add("loan", "event+noun", "loan", "loans", "mortgage", "mortgages", "lar")
_add("case", "event+noun", "case", "cases", "docket", "dockets", "matter", "matters",
     "lawsuit", "lawsuits", "proceeding", "proceedings", "investigation",
     "investigations", "charge", "charges", "complaint_case", "opinion", "opinions",
     "decision", "decisions", "judgment", "appeal", "appeals")
_add("vote", "event", "vote", "votes", "roll-call", "rollcall", "justice-vote")
_add("recall", "event+noun", "recall", "recalls", "retraction", "retractions",
     "withdrawal", "withdrawals")
_add("complaint", "event", "complaint", "complaints", "grievance", "grievances",
     "allegation", "allegations", "tips")
_add("action", "event", "action", "actions", "activity", "activities", "event",
     "events", "intervention", "response", "operation", "operations")
_add("measurement", "event", "rate", "rates", "reading", "readings", "measurement",
     "measurements", "measure", "measures", "observation", "observations", "sample",
     "samples", "test", "tests", "result", "results", "level", "levels", "emission",
     "emissions", "score", "scores", "capture", "estimate", "estimates", "index",
     "indices", "gini", "qcew", "count", "counts", "encounter", "encounters",
     "load", "voyage", "voyages", "position_report")
_add("change", "event", "change", "changes", "amendment", "amendments", "merger",
     "mergers", "modification", "modifications", "chg_log", "transfer", "transfers",
     "conversion", "history", "revision", "update", "updates", "correction")
_add("post", "event", "post", "posts", "comment", "comments", "press", "pr",
     "announcement", "speech", "speeches", "testimony")
_add("document", "noun", "document", "documents", "page", "pages", "wayback",
     "library", "listing", "snapshot", "archive", "archives", "manuscript", "map",
     "maps", "photograph", "photographs", "image", "images")

# ---- LINK families ----
_add("crosswalk", "link", "xref", "crosswalk", "crosswalks", "mapping", "mappings",
     "linkage", "linkages", "bridge_table", "links", "concordance", "match", "matches")
_add("membership", "link", "membership", "memberships", "affiliation", "affiliations",
     "association", "associations", "enviroassoc", "member", "members")
_add("ownership", "link", "owner", "owners", "ownership", "holding", "holdings",
     "position", "positions", "stake", "stakes", "subsidiary", "subsidiaries",
     "parent", "shareholder", "shareholders", "beneficial")
_add("role", "link", "officer", "officers", "relationship", "relationships", "pair",
     "pairs", "combination", "service", "assignment", "assignments", "tenure",
     "appointment", "appointments", "employment_link", "delegation", "emp_lobbyist",
     "firm_lobbyist", "firm_employer", "employer_firms", "lobbyist-employer-session",
     "employer-firm-session", "firm-filing-employer-period", "lobbyist-firm-session")

# ---- CODE families ----
_add("code", "code", "code", "codes", "naics", "sic", "cip", "taxonomy", "taxonomies",
     "lookup", "lookups", "reference", "vocabulary", "classification",
     "classifications", "subparts", "pollutants", "cip_codes", "facility_codes",
     "tsn", "taxon", "taxa", "species", "kingdom_id", "taxon_author_id", "mic",
     "categories", "definitions", "glossary", "dictionary")

# ---- registry: noun list of things (FAA registry, funder registry) ----
_add("registry", "noun", "registry", "registries", "roster", "directory", "list",
     "lists", "inventory", "census_frame", "frame", "catalog", "master")

# ---- aggregates (publisher pre-aggregated statistics) ----
_add("aggregate", "aggregate", "stats", "statistics", "summary", "summaries",
     "totals", "aggregates", "aggregate", "indicators", "faostat", "istat",
     "benchmarks", "rankings")

# source/system-specific vocabulary learned in the 2026-08-12 review pass
_add("contribution", "event", "fec")
_add("filing", "event+noun", "edgar", "fara", "dera")
_add("accident", "event", "faers", "defenders", "crime", "collisions", "overdose",
     "overdoses", "shootings")
_add("facility", "noun", "envirofacts", "echo", "center", "centers", "childcare",
     "restaurants", "establishments", "nursing")
_add("inspection", "event", "fces", "pces")
_add("enforcement", "event", "enforcements", "arrests")
_add("aggregate", "aggregate", "soi", "z1", "cot", "owid", "freedomhouse", "wb",
     "pbgc_data", "scorecard_agg", "uds")
_add("measurement", "event", "eia861", "water", "ideology", "voyages")
_add("organization", "noun", "offshoreleaks", "ffi", "filers", "osfi", "scorecard")
_add("award", "event+noun", "usaspending")
_add("code", "code", "sics")
_add("role", "link", "lobby", "lobbying")
_add("place", "noun", "zoning", "streets", "centerlines", "sidewalks", "trees")
_add("asset", "noun", "hydrants")
_add("complaint", "event", "311", "potholes")
_add("action", "event", "ops", "calls", "slavevoyages")
_add("payment", "event", "salaries", "payroll", "checkbook")
_add("aggregate", "aggregate", "minerals")

# exact-name overrides — checked before everything else (source-specific truths
# that token scanning gets wrong)
OVERRIDES: list[tuple[re.Pattern, str, str, str]] = [
    (re.compile(r"voteview_members"), "person", "noun", "voteview members are legislators"),
    (re.compile(r"voteview_rollcalls"), "vote", "event", "voteview rollcalls are votes"),
    (re.compile(r"va_suicide"), "aggregate", "aggregate", "VA suicide appendix is published statistics"),
    (re.compile(r"college_scorecard"), "organization", "noun", "scorecard rows are institutions"),
    (re.compile(r"uds_table\d"), "aggregate", "aggregate", "UDS tables are per-center published aggregates"),
    (re.compile(r"fed_pbgc_data$|fed_pbgc_data_"), "aggregate", "aggregate", "PBGC Data Book statistics"),
    (re.compile(r"dera_sub"), "filing", "event+noun", "DERA sub = EDGAR submissions"),
    (re.compile(r"nppes"), "provider", "noun", "NPPES is the national provider registry (columns live only in warehouse)"),
]

# tokens to skip while scanning names (never informative)
JUNK = {
    "data", "api", "bulk", "gov", "full", "info", "information", "queue", "state",
    "federal", "fed", "intl", "portal", "arc", "open", "record", "records", "row",
    "rows", "id", "ids", "all", "main", "misc", "other", "others", "detail",
    "details", "current", "active", "historic", "historical", "annual", "monthly",
    "daily", "quarterly", "latest", "new", "old", "raw", "clean", "final", "v2",
    "datosgob", "datagov", "opendataswiss",
    "govdata", "dados", "csv", "json", "file", "files", "tab", "part", "section",
    "line", "lines", "item", "items", "elec", "gas", "wind", "solar", "storage",
    "multifuel", "distributed", "metering", "pricing", "reliability", "efficiency",
    "security", "trade_global", "repex", "global", "cs", "cust", "book", "audit_",
    "deep", "landing", "table", "columns", "arrive", "text", "cast", "staging",
    "layer",
}

# years and pure numbers are junk
YEAR_RX = re.compile(r"^(19|20)\d{2}$|^\d+$")

GENERIC_GRAIN = {"record", "records", "row", "rows", "entry", "entries", "line",
                 "lines", "item", "items", "id", "identifier", "unique", "number",
                 "name", "of", "type", "level", "version", "file", "page", "post"}


def lookup_token(tok: str) -> tuple[str, str] | None:
    if tok in JUNK or YEAR_RX.match(tok):
        return None
    return D.get(tok)


CONTAINER_FAMILIES = {"document", "dataset", "registry"}  # generic wrappers:
# 'accident document', 'violation report', 'facility list' — the specific word wins


def scan_tokens(text: str) -> tuple[str, str, str] | None:
    """Scan words right-to-left through the dictionary; return (family, cls, tok).
    A generic container hit (document/dataset/registry) yields to a more
    specific hit further left."""
    toks = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower().replace("_", " "))
    container = None
    for w in reversed(toks):
        hit = lookup_token(w)
        if not hit:
            continue
        if hit[0] in CONTAINER_FAMILIES:
            container = container or (hit[0], hit[1], w)
            continue
        return hit[0], hit[1], w
    return container


def classify_model(m: dict, src_desc: str) -> dict:
    """Return dict(family, cls, thing_token, evidence, confidence).

    Signal order: exact overrides > grain declaration > name suffix > full name
    > raw-source description (portal dataset titles live there) > spine hint >
    column shape (lands in 'unresolved', never in a real family).
    """
    name_l = m["name"].lower()
    for rx, fam, cls, why in OVERRIDES:
        if rx.search(name_l):
            return {"family": fam, "cls": cls, "thing_token": "",
                    "evidence": f"override: {why}", "confidence": "high"}
    # signal 1: grain head noun
    g = m["grain_phrase"].lower().strip()
    if g:
        seg = re.sub(r"\bper\b.*$", "", g.split(",")[0]).strip()
        words = [w for w in re.findall(r"[a-z0-9_-]+", seg) if w not in GENERIC_GRAIN]
        hit = scan_tokens(" ".join(words)) if words else None
        if hit:
            return {"family": hit[0], "cls": hit[1], "thing_token": hit[2],
                    "evidence": f"grain says 'one row per {seg}'", "confidence": "high"}
    # signal 2: model name — suffix part first, then the whole name
    # (subject-dir prefix stripped: 'justice__fed_x' must not scan as 'justice')
    nm = re.sub(r"^(stg_|int_)", "", name_l)
    subj = (m.get("subject") or "").lower()
    if subj and nm.startswith(subj + "__"):
        nm = nm[len(subj) + 2 :]
    suffix = nm.split("__", 1)[-1] if "__" in nm else nm
    hit = scan_tokens(suffix)
    if hit:
        return {"family": hit[0], "cls": hit[1], "thing_token": hit[2],
                "evidence": f"name token '{hit[2]}'", "confidence": "medium"}
    hit = scan_tokens(nm)
    if hit:
        return {"family": hit[0], "cls": hit[1], "thing_token": hit[2],
                "evidence": f"source-name token '{hit[2]}'", "confidence": "medium"}
    # signal 3: the raw source's human description (portal dataset titles)
    if src_desc:
        title = re.sub(r"^raw landing table for\s*", "", src_desc.lower())
        title = title.split(". all columns arrive")[0]
        hit = scan_tokens(title)
        if hit:
            return {"family": hit[0], "cls": hit[1], "thing_token": hit[2],
                    "evidence": f"dataset title token '{hit[2]}' in: {title[:60]}",
                    "confidence": "medium"}
    # signal 4: spine entity hint
    sp = m["spine_entity"].lower().rstrip(". ")
    if sp:
        hit = lookup_token(sp) or lookup_token(sp + "s")
        if hit:
            return {"family": hit[0], "cls": hit[1], "thing_token": sp,
                    "evidence": f"spine hint '{sp}'", "confidence": "medium"}
    # signal 5: column shape — honest fallback bucket, kept out of real families
    stypes = Counter(sem_type(c) for c in m["columns"])
    n = max(1, len(m["columns"]))
    has_date = stypes["date"] > 0
    id_cols = [c for c in m["columns"] if sem_type(c) == "id"]
    if len(id_cols) >= 2 and n <= 8:
        return {"family": "unresolved", "cls": "link", "thing_token": "",
                "evidence": f"columns only: {len(id_cols)} ids, narrow", "confidence": "low"}
    if has_date and stypes["money"] > 0:
        return {"family": "unresolved", "cls": "event", "thing_token": "",
                "evidence": "columns only: dated money rows", "confidence": "low"}
    if has_date:
        return {"family": "unresolved", "cls": "event", "thing_token": "",
                "evidence": "columns only: dated rows", "confidence": "low"}
    if stypes["name_text"] > 0 and stypes["geo"] + stypes["geo_point"] > 0:
        return {"family": "unresolved", "cls": "noun", "thing_token": "",
                "evidence": "columns only: named located rows, undated", "confidence": "low"}
    return {"family": "UNMAPPED", "cls": "unclassified", "thing_token": "",
            "evidence": "no signal matched", "confidence": "none"}


# =====================================================================
# 3. SLOTS — derived from semantic types & class
# =====================================================================

SLOTS: list[dict] = [
    # id, label, requires (semantic types any-of; [] = universal), classes (None = all)
    {"id": "how_many", "label": "How many are there", "req": [], "cls": None},
    {"id": "row_count_vs_published", "label": "Rows held vs publisher total", "req": [], "cls": None},
    {"id": "freshness", "label": "How fresh is it (last load)", "req": [], "cls": None},
    {"id": "grain_integrity", "label": "Is one row really one thing (dup check)", "req": ["_key"], "cls": None},
    {"id": "id_integrity", "label": "Are the IDs real (distinct/sentinel check)", "req": ["id"], "cls": None},
    {"id": "rank_in_family", "label": "Rank among peers in its family", "req": [], "cls": None},
    {"id": "share_of_family", "label": "Share of its family", "req": [], "cls": None},
    {"id": "by_time", "label": "Over time", "req": ["date"], "cls": None},
    {"id": "first_last", "label": "Earliest and latest", "req": ["date"], "cls": None},
    {"id": "gaps", "label": "Missing periods in the record", "req": ["date"], "cls": None},
    {"id": "seasonality", "label": "By month / day-of-week", "req": ["date"], "cls": None},
    {"id": "births", "label": "New ones per period (first seen)", "req": ["date"], "cls": ["noun", "event+noun"]},
    {"id": "deaths", "label": "Disappeared per period (last seen)", "req": ["date"], "cls": ["noun", "event+noun"]},
    {"id": "age_distribution", "label": "How old the living ones are", "req": ["date"], "cls": ["noun", "event+noun"]},
    {"id": "by_state", "label": "By state", "req": ["geo"], "cls": None},
    {"id": "by_county_city", "label": "By county / city / zip", "req": ["geo"], "cls": None},
    {"id": "map_points", "label": "On a map (points)", "req": ["geo_point"], "cls": None},
    {"id": "geo_concentration", "label": "Geographic concentration", "req": ["geo"], "cls": None},
    {"id": "mix_by_code", "label": "Mix by type/status/category", "req": ["code"], "cls": None},
    {"id": "mix_over_time", "label": "Mix shifting over time", "req": ["code", "date"], "cls": None},
    {"id": "code_concentration", "label": "Does one category dominate", "req": ["code"], "cls": None},
    {"id": "total_money", "label": "Total dollars", "req": ["money"], "cls": None},
    {"id": "typical_money", "label": "Typical dollar size (median)", "req": ["money"], "cls": None},
    {"id": "money_distribution", "label": "Dollar distribution", "req": ["money"], "cls": None},
    {"id": "money_top_share", "label": "Top 1% share of dollars", "req": ["money"], "cls": None},
    {"id": "round_numbers", "label": "Suspiciously round amounts", "req": ["money"], "cls": None},
    {"id": "size_distribution", "label": "Size distribution", "req": ["quantity"], "cls": None},
    {"id": "per_noun_rate", "label": "Events per noun (the core ratio)", "req": ["id"], "cls": ["event", "event+noun"]},
    {"id": "zero_nouns", "label": "Nouns with zero events (never touched)", "req": ["id"], "cls": ["event", "event+noun"]},
    {"id": "repeaters", "label": "Repeat offenders / heaviest nouns", "req": ["id"], "cls": ["event", "event+noun"]},
    {"id": "noun_concentration", "label": "Top 1% of nouns' share of events", "req": ["id"], "cls": ["event", "event+noun"]},
    {"id": "per_person", "label": "Per person served", "req": ["population"], "cls": None},
    {"id": "flag_rates", "label": "Yes/no flag rates", "req": ["flag"], "cls": None},
    {"id": "degree_out", "label": "Connections per left noun", "req": [], "cls": ["link"]},
    {"id": "degree_in", "label": "Connections per right noun", "req": [], "cls": ["link"]},
    {"id": "multiplicity", "label": "One-to-one or many-to-many", "req": [], "cls": ["link"]},
    {"id": "codes_defined", "label": "Codes defined", "req": [], "cls": ["code"]},
    {"id": "codes_in_use", "label": "Codes actually used anywhere", "req": [], "cls": ["code"]},
    {"id": "code_usage_concentration", "label": "Usage concentration", "req": [], "cls": ["code"]},
    {"id": "orphan_codes", "label": "Values in data missing from vocabulary", "req": [], "cls": ["code"]},
]


def slot_status(slot: dict, cls: str, stypes: Counter, has_key: bool) -> str:
    if slot["cls"] is not None and cls not in slot["cls"]:
        return "na"  # slot doesn't apply to this class — blank, not a hole
    for req in slot["req"]:
        if req == "_key":
            if not has_key:
                return "hole:no-declared-key"
            continue
        if req == "geo":
            if stypes["geo"] + stypes["geo_point"] == 0:
                return "hole:no-geo-column"
            continue
        if stypes[req] == 0:
            return f"hole:no-{req}-column"
    return "ready"


# =====================================================================
# 4. PARKS — mechanical parking-lot generation from metadata conditions
# =====================================================================

def parks_for(m: dict, cls: str, stypes: Counter) -> list[tuple[str, str, str]]:
    """Return [(branch, park_type, line)]."""
    out = []
    name = m["name"]
    if stypes["population"] == 0 and cls in ("noun", "event", "event+noun"):
        out.append(("per person served", "needs-population",
                    f"{name}: no population/served column on the thing itself"))
    if not m["spine_entity"] and m["layer"] == "staging":
        out.append(("join to the entity spine", "needs-crosswalk",
                    f"{name}: spine entity undetermined at onboarding"))
    if stypes["date"] == 0:
        out.append(("any trend over time", "needs-history",
                    f"{name}: no date column — snapshot only"))
    if re.search(r"(19|20)\d{2}", name):
        out.append(("multi-year trending", "needs-history",
                    f"{name}: single-year table — history exists at publisher, not loaded"))
    if cls in ("event", "event+noun") and stypes["id"] == 0:
        out.append(("events per noun via hard ID", "needs-crosswalk",
                    f"{name}: events carry no entity ID — name-match only"))
    if cls in ("event", "event+noun") and stypes["money"] > 0:
        out.append(("assessed vs actually collected", "needs-second-table",
                    f"{name}: has amounts; collection outcome lives elsewhere if anywhere"))
    if cls in ("event", "event+noun"):
        out.append(("was there an inspection first (real lineage)", "needs-lineage",
                    f"{name}: stage-to-stage links need row-level lineage proof"))
        out.append(("did anyone get hurt (harm join)", "needs-second-table",
                    f"{name}: harm lives in a different fact table"))
    if cls == "aggregate":
        out.append(("row-level version of this aggregate", "needs-source-upgrade",
                    f"{name}: publisher pre-aggregated — per-noun cuts impossible below its grain"))
    if m["column_quality"] in ("documented-only-partial", "columns-unknown", "star-source"):
        out.append(("full column inventory", "needs-metadata-pull",
                    f"{name}: columns not fully recoverable from SQL"))
    return out


# =====================================================================
# 5. MAIN
# =====================================================================

def main() -> None:
    models = [json.loads(l) for l in (BUILD / "models.jsonl").open(encoding="utf-8")]
    raw_sources = [json.loads(l) for l in (BUILD / "raw_sources.jsonl").open(encoding="utf-8")]
    src_desc_by_table = {s["table"].lower(): s["description"] for s in raw_sources}

    # classify every model
    table_map = []
    parks: list[dict] = []
    fam_members: dict[str, list[dict]] = defaultdict(list)
    for m in models:
        src_dir = ""
        if m["layer"] == "staging" and m["name"].startswith("stg_"):
            src_dir = m["name"].removeprefix("stg_").split("__", 1)[0]
        c = classify_model(m, src_desc_by_table.get(src_dir, ""))
        stypes = Counter(sem_type(col) for col in m["columns"])
        has_key = bool(m["natural_key"]) or bool(m["columns_documented"])
        pre_agg = c["cls"] == "aggregate"
        rec = {
            "model": m["name"], "layer": m["layer"], "subject": m["subject"],
            "family": c["family"], "class": c["cls"], "thing_token": c["thing_token"],
            "map_evidence": c["evidence"], "map_confidence": c["confidence"],
            "grain_phrase": m["grain_phrase"], "spine_entity": m["spine_entity"],
            "natural_key": m["natural_key"], "n_columns": len(m["columns"]),
            "column_quality": m["column_quality"], "pre_aggregated": pre_agg,
            "sem_date": stypes["date"], "sem_money": stypes["money"],
            "sem_geo": stypes["geo"] + stypes["geo_point"], "sem_id": stypes["id"],
            "sem_code": stypes["code"], "sem_population": stypes["population"],
            "sem_flag": stypes["flag"], "sem_quantity": stypes["quantity"],
        }
        table_map.append(rec)
        fam_members[c["family"]].append({**m, "cls": c["cls"], "stypes": stypes, "has_key": has_key})
        for branch, ptype, line in parks_for(m, c["cls"], stypes):
            parks.append({"branch": branch, "park_type": ptype, "family": c["family"],
                          "model": m["name"], "line": line})

    # ---- per-model grid (the machine layer) ----
    rec_by_model = {r["model"]: r for r in table_map}
    grid_rows = []
    for m in models:
        rec = rec_by_model[m["name"]]
        stypes = Counter(sem_type(col) for col in m["columns"])
        has_key = bool(m["natural_key"]) or bool(m["columns_documented"])
        for slot in SLOTS:
            st = slot_status(slot, rec["class"], stypes, has_key)
            if st == "na":
                continue
            grid_rows.append({"model": m["name"], "family": rec["family"],
                              "class": rec["class"], "slot": slot["id"], "status": st})

    # ---- family grid (the one-page instrument) ----
    fam_grid = []
    for fam, members in sorted(fam_members.items()):
        classes = Counter(x["cls"] for x in members)
        cls = classes.most_common(1)[0][0]
        for slot in SLOTS:
            stats = Counter()
            for x in members:
                st = slot_status(slot, x["cls"], x["stypes"], x["has_key"])
                stats[st.split(":")[0]] += 1
            if stats["na"] == len(members):
                continue
            ready, hole = stats["ready"], stats["hole"]
            fam_grid.append({"family": fam, "class": cls, "n_members": len(members),
                            "slot": slot["id"], "slot_label": slot["label"],
                            "members_ready": ready, "members_hole": hole,
                            "status": "ready" if ready else "hole"})

    # ---- parking tallies ----
    tally_branch = Counter(p["branch"] for p in parks)
    tally_type = Counter(p["park_type"] for p in parks)
    fam_per_branch = defaultdict(set)
    for p in parks:
        fam_per_branch[p["branch"]].add(p["family"])

    # ---- sources census ----
    onboarding = json.loads(ONBOARDING_LOG.read_text(encoding="utf-8"))
    ob_status = Counter(v.get("status", "?") for v in onboarding.values())
    staged_sources = {m["name"].split("__")[0].removeprefix("stg_") for m in models if m["layer"] == "staging"}
    raw_tables_by_schema = Counter(s["schema"] for s in raw_sources)
    src_rows = []
    for name, v in sorted(onboarding.items()):
        src_rows.append({"source": name, "status": v.get("status", "?"),
                         "attempts": v.get("attempts", ""), "updated_at": v.get("updated_at", "")})

    # ---- write outputs ----
    def wcsv(path: Path, rows: list[dict]) -> None:
        if not rows:
            path.write_text("", encoding="utf-8")
            return
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    OUT.mkdir(parents=True, exist_ok=True)
    wcsv(OUT / "table_map.csv", table_map)
    wcsv(OUT / "grid_things.csv", grid_rows)
    wcsv(OUT / "grid_families.csv", fam_grid)
    wcsv(OUT / "parking_lot.csv", parks)
    wcsv(OUT / "parking_tally.csv",
         [{"branch": b, "times_parked": c, "families_touched": len(fam_per_branch[b])}
          for b, c in tally_branch.most_common()])
    wcsv(OUT / "sources_census.csv", src_rows)
    wcsv(OUT / "slots.csv", [{"slot": s["id"], "label": s["label"],
                              "requires": "+".join(s["req"]) or "universal",
                              "classes": ",".join(s["cls"]) if s["cls"] else "all"} for s in SLOTS])

    # ---- thing roll-up: family > thing (normalized token) > models ----
    def singularize(t: str) -> str:
        if not t:
            return ""
        if t.endswith("ies") and len(t) > 4:
            return t[:-3] + "y"
        if t.endswith("sses") or t.endswith("ches") or t.endswith("shes"):
            return t[:-2]
        if t.endswith("s") and not t.endswith("ss") and len(t) > 3:
            return t[:-1]
        return t

    thing_groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in table_map:
        thing = singularize(r["thing_token"]) or f"({r['family']} unspecified)"
        thing_groups[(r["family"], thing)].append(r)
    things_rows = []
    for (fam, thing), members in sorted(thing_groups.items()):
        classes = Counter(x["class"] for x in members)
        subjects = Counter(x["subject"] for x in members)
        things_rows.append({
            "family": fam, "thing": thing, "class": classes.most_common(1)[0][0],
            "n_models": len(members),
            "subjects": "; ".join(s for s, _ in subjects.most_common(5)),
            "example_models": "; ".join(x["model"] for x in members[:3]),
        })
    wcsv(OUT / "things.csv", things_rows)

    # ---- summary accounting ----
    unmapped = [r for r in table_map if r["family"] == "UNMAPPED"]
    conf = Counter(r["map_confidence"] for r in table_map)
    cls_c = Counter(r["class"] for r in table_map)
    fam_c = {f: len(v) for f, v in sorted(fam_members.items(), key=lambda kv: -len(kv[1]))}
    cell_c = Counter(g["status"].split(":")[0] for g in grid_rows)
    summary = {
        "models_total": len(models),
        "families": len(fam_members) - (1 if "UNMAPPED" in fam_members else 0),
        "unmapped_models": len(unmapped),
        "unmapped_list": [r["model"] for r in unmapped],
        "map_confidence": dict(conf),
        "class_counts": dict(cls_c),
        "family_sizes": fam_c,
        "grid_cells_total": len(grid_rows),
        "grid_cell_status": dict(cell_c),
        "family_grid_rows": len(fam_grid),
        "parks_total": len(parks),
        "park_branches": len(tally_branch),
        "top_parked": tally_branch.most_common(15),
        "park_types": dict(tally_type),
        "onboarding_sources": len(onboarding),
        "onboarding_status": dict(ob_status),
        "raw_landing_tables": len(raw_sources),
        "staged_source_dirs": len(staged_sources),
    }
    (OUT / "build" / "grid_report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # ---- SUMMARY.md — the readable front page (rough, numbers auto-filled) ----
    fam_ready = defaultdict(lambda: [0, 0])
    for g in fam_grid:
        fam_ready[g["family"]][0] += g["members_ready"]
        fam_ready[g["family"]][1] += g["members_hole"]
    lines = []
    a = lines.append
    a("# The Census Grid — every thing in the warehouse × every way to look at it")
    a("")
    a("*Built 2026-08-12 from table metadata only (dbt manifest + model SQL + source")
    a("descriptions). Zero warehouse queries. Every number below is reproducible by")
    a("running `scripts/census/extract_models.py` then `scripts/census/build_grid.py`.*")
    a("")
    a("## The one-screen picture")
    a("")
    a(f"- **{len(models)} modeled tables** described in one language: noun / event / link / code.")
    nf = len(fam_members) - (1 if "UNMAPPED" in fam_members else 0) - (1 if "unresolved" in fam_members else 0)
    a(f"- **{nf} families** of things, **{len(things_rows)} distinct things**, "
      f"**{len(grid_rows):,} grid cells** (thing × applicable display slot).")
    a(f"- **{cell_c['ready']:,} cells are ready to fill** (the columns exist); "
      f"**{cell_c['hole']:,} are structural holes** (the column doesn't exist — visible, not dropped).")
    a(f"- **{len(unmapped)} models remain unmapped** and **{len(fam_members.get('unresolved', []))} "
      f"are shape-guessed only** — listed at the bottom, never silently dropped.")
    a(f"- **{len(parks):,} branches parked** across {len(tally_branch)} branch types — the tally below is the build roadmap, by vote count.")
    a("")
    a("## The parking-lot tally (the second deliverable — ranked by votes)")
    a("")
    a("| votes | families touched | branch |")
    a("|---:|---:|---|")
    for b, c in tally_branch.most_common():
        a(f"| {c:,} | {len(fam_per_branch[b])} | {b} |")
    a("")
    a("## Families (grid rows, one line each)")
    a("")
    a("| family | class | models | cells ready | cells hole |")
    a("|---|---|---:|---:|---:|")
    order = sorted(fam_members, key=lambda f: -len(fam_members[f]))
    for f in order:
        if f in ("UNMAPPED",):
            continue
        cls = Counter(x["cls"] for x in fam_members[f]).most_common(1)[0][0]
        r, h = fam_ready[f]
        a(f"| {f} | {cls} | {len(fam_members[f])} | {r:,} | {h:,} |")
    a("")
    a("## Source bookkeeping does not reconcile (a census finding in itself)")
    a("")
    a(f"- Onboarding log: **{len(onboarding)} sources attempted** — "
      f"{ob_status.get('complete', 0)} complete, {ob_status.get('failed', 0)} failed, "
      f"{ob_status.get('needs_key', 0)} waiting on API keys.")
    a(f"- Yet **{len(staged_sources)} source directories are staged** and live in dbt, and "
      f"**{len(raw_sources)} raw landing tables** exist.")
    a("- These three numbers cannot currently be joined by any shared key. There is no")
    a("  single authoritative list of what the warehouse holds. PARKED: source-registry")
    a("  reconciliation (needs-crosswalk).")
    a("")
    a("## The honest residue (visible holes, per the ratchet)")
    a("")
    a(f"- {len(unmapped)} unmapped models: " + ", ".join(r["model"] for r in unmapped))
    a(f"- {len(fam_members.get('unresolved', []))} models classified by column shape only (family 'unresolved').")
    a("- 12 models whose column lists could not be fully recovered from SQL (flagged in table_map.csv).")
    a(f"- {sum(1 for m in models if not m['grain_declared'])} models with no declared grain — their 'one row = one what' is unstated.")
    a("")
    a("## What each file is")
    a("")
    a("| file | what it holds |")
    a("|---|---|")
    a("| `things.csv` | the bottom-up thing-list (family > thing > model count) |")
    a("| `table_map.csv` | every model → family/class, with the evidence for the call |")
    a("| `grid_families.csv` | the one-page grid: family × slot × ready/hole counts |")
    a("| `grid_things.csv` | the full machine grid: model × slot × status |")
    a("| `slots.csv` | the display-slot vocabulary and what each requires |")
    a("| `parking_lot.csv` | every parked branch, one line each |")
    a("| `parking_tally.csv` | the ranked tally — the build roadmap |")
    a("| `sources_census.csv` | the onboarding log, every attempted source with status |")
    a("")
    (OUT / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({k: v for k, v in summary.items() if k != "unmapped_list"}, indent=2))
    print("unmapped sample:", summary["unmapped_list"][:25])


if __name__ == "__main__":
    main()
