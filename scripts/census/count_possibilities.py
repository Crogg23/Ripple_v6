"""Every 'number of X' you can pull out of the warehouse.

For every mart table, writes out every count that table can answer: a
plain-English question, a plain-English definition of what the number actually
means, the table it comes from, and a ready-to-paste SQL statement.

Nothing here runs a query. The SQL is written to be copied.

Inputs (all local):
  reports/_all_columns.csv                        every column of every mart table
  reports/time_index/live_tables.csv              row counts
  reports/time_index/clock_index.csv              which column is the table's clock
  reports/census_grid_2026-08-12/table_map.csv    'one row per ___' phrasing
  scripts/census/plain_english.py                 what each dataset is
  scripts/census/count_naming.py                  English naming rules
  glossary/column_gloss.py                        curated per-column meanings

Output:
  reports/count_possibilities.json
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "scripts", "census"))
sys.path.insert(0, REPO)

import plain_english as pe  # noqa: E402
from count_naming import article, humanize, plural, row_noun  # noqa: E402

try:
    from glossary.column_gloss import COLUMN_GLOSS
except Exception:  # pragma: no cover
    COLUMN_GLOSS = {}

DB = "LIBRARY_MARTS"
TEXT_TYPES = {"TEXT", "VARCHAR", "STRING", "CHAR"}

PLUMBING = re.compile(r"^(_|RIPPLE_)")
PLUMBING_EXACT = {"LOADED_AT", "INGESTED_AT", "SOURCE_RUN_ID", "SRC_FILE",
                  "SRC_SHA256", "FILE_NAME", "LOAD_TS", "ETL_TS"}

# Identifier columns whose thing has a real English name.
KNOWN_IDS = {
    "NPI": ("healthcare provider", "the federal provider number every US clinician and clinic has"),
    "EIN": ("organisation", "the federal employer tax number - a business, charity or pension plan"),
    "CIK": ("company", "the securities regulator's permanent company number"),
    "UEI": ("federal award recipient", "the government's unique entity ID, successor to DUNS"),
    "DUNS": ("business", "the old Dun & Bradstreet business number"),
    "LEI": ("legal entity", "the global identifier used across finance"),
    "CUSIP": ("security", "the identifier for one stock or bond"),
    "MMSI": ("ship", "the radio identifier a vessel broadcasts"),
    "IMO_NUMBER": ("ship", "the permanent hull number that follows a vessel for life"),
    "FRN": ("licence holder", "the communications regulator's registration number"),
    "BIOGUIDE": ("member of Congress", "Congress's permanent ID for a person"),
    "ICPSR": ("member of Congress", "the vote-archive ID for a legislator"),
    "CAND_ID": ("candidate", "the election commission's candidate ID"),
    "CMTE_ID": ("political committee", "the election commission's committee ID"),
    "MINE_ID": ("mine", "the federal ID for one mine site"),
    "CCN": ("certified facility", "the Medicare certification number for a hospital or care home"),
    "PWSID": ("public water system", "the identifier for one drinking water system"),
    "NDC": ("drug product", "the national drug code for one packaged medicine"),
    "COMPANY_NO": ("company", "the corporate register's company number"),
    "ACCESSION_NUMBER": ("filing", "the identifier for one submitted filing"),
    "REGISTRY_ID": ("registered site", "the environmental registry's site identifier"),
}

ID_SUFFIX = re.compile(r"_(ID|IDS|NO|NUM|NBR|NUMBER|KEY|UUID|GUID|PK)$")
GENERIC_IDS = {"ID", "RECORD_ID", "ROW_ID", "KEY", "UUID", "GUID", "PK", "INDEX"}
# Column stems that are adjectives or positions, never a thing you can count.
NOT_THINGS = {"unique", "last", "first", "prior", "next", "old", "new", "main",
              "other", "misc", "temp", "sub", "alt", "orig", "current", "rpt rec"}

NAME_TOKENS = ("NAME", "COMPANY", "ORGANIZATION", "ORGANISATION", "ENTITY", "FACILITY",
               "OPERATOR", "OWNER", "SPONSOR", "EMPLOYER", "MANUFACTURER", "AGENCY",
               "COURT", "JUDGE", "RECIPIENT", "DONOR", "APPLICANT", "REGISTRANT",
               "CONTRACTOR", "VENDOR", "SUPPLIER", "UTILITY", "INSTITUTION",
               "LAWYER", "ATTORNEY", "AUTHOR", "PUBLISHER", "FIRM", "BANK")

CATEGORY_TOKENS = ("TYPE", "STATUS", "CLASS", "CATEGORY", "KIND", "REASON", "RESULT",
                   "DISPOSITION", "SEVERITY", "PARTY", "GENDER", "SEX", "RACE",
                   "ETHNICITY", "LEVEL", "TIER", "GRADE", "SECTOR", "INDUSTRY",
                   "PRODUCT", "ISSUE", "ACTION", "OUTCOME", "DECISION", "METHOD",
                   "PURPOSE", "PROGRAM", "PROGRAMME", "SCOPE", "STAGE", "PHASE",
                   "ROLE", "RANK", "SEGMENT", "BRANCH", "DIVISION", "SUBTYPE",
                   "SUB_TYPE", "FORM_TYPE", "VIOLATION", "OFFENSE", "OFFENCE",
                   "CHARGE", "SANCTION", "REGIME", "JURISDICTION", "CURRENCY",
                   "FUEL", "SPECIES", "OCCUPATION", "DEGREE", "LANGUAGE", "SOURCE")

GEO_EXACT = {"STATE", "ST", "STATE_CODE", "STATE_NAME", "STATE_ABBR", "PROVINCE",
             "COUNTY", "COUNTY_NAME", "PARISH", "CITY", "TOWN", "MUNICIPALITY",
             "ZIP", "ZIPCODE", "ZIP_CODE", "POSTAL_CODE", "POSTCODE",
             "COUNTRY", "COUNTRY_NAME", "COUNTRY_CODE", "NATION", "REGION",
             "DISTRICT", "CONGRESSIONAL_DISTRICT", "FIPS", "FIPS_CODE",
             "CBSA", "MSA", "BOROUGH", "WARD"}

MONEY_TOKENS = ("AMOUNT", "AMT", "DOLLAR", "COST", "PRICE", "FEE", "FINE", "PENALTY",
                "SALARY", "WAGE", "REVENUE", "ASSET", "LIABILIT", "DEBT",
                "OBLIGATION", "DISBURSE", "RECEIPT", "CONTRIBUTION", "AWARD", "SPEND")

QUANTITY_TOKENS = ("NUMBER_OF", "NUM_", "N_", "COUNT", "QTY", "QUANTITY",
                   "EMPLOYEES", "BEDS", "UNITS", "HOURS", "DAYS", "POPULATION",
                   "ACRES", "TONS", "TONNES", "GALLONS", "POUNDS", "DOSES")

FLAG_PREFIX = ("IS_", "HAS_", "WAS_", "DID_", "CAN_")
FLAG_SUFFIX = ("_FLAG", "_IND", "_INDICATOR", "_YN", "_BOOL")

TEXT_TOKENS = ("DESCRIPTION", "DESC", "COMMENT", "NARRATIVE", "REMARK", "NOTE",
               "TEXT", "SUMMARY", "ABSTRACT", "BODY", "CONTENT", "ADDRESS",
               "STREET", "URL", "LINK", "EMAIL", "PHONE", "LATITUDE", "LONGITUDE",
               "GEOMETRY", "POLYGON", "SHAPE", "JSON", "XML", "RAW")

DATE_TYPES = {"DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ", "DATETIME"}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_") or "n"


def curated(fqn: str, col: str) -> str | None:
    for key in ((fqn, col.upper()), ("*", col.upper())):
        if key in COLUMN_GLOSS:
            return COLUMN_GLOSS[key]
    return None


def classify(col: str, dtype: str) -> str:
    up = col.upper()
    dt = dtype.upper()
    if PLUMBING.match(up) or up in PLUMBING_EXACT:
        return "skip"
    if any(t in up for t in TEXT_TOKENS):
        return "skip"
    if dt in DATE_TYPES:
        return "date"
    if dt == "BOOLEAN" or up.startswith(FLAG_PREFIX) or up.endswith(FLAG_SUFFIX):
        return "flag"
    if up in GEO_EXACT:
        return "geo"
    if up in KNOWN_IDS or up in GENERIC_IDS or ID_SUFFIX.search(up):
        return "id"
    if any(t in up for t in NAME_TOKENS):
        return "name"
    # A column with a time word in its name is a clock, never a category, even
    # when it also matches a category token (ACTION_DATE_FISCAL_YEAR).
    if any(t in up for t in ("YEAR", "DATE", "MONTH", "QUARTER", "_DAY", "TIME")):
        return "other"
    # COUNT / NUM / TOTAL beat category: BRANCH_COUNT is a number, not a kind.
    if any(t in up for t in QUANTITY_TOKENS):
        return "quantity"
    if any(t in up for t in CATEGORY_TOKENS):
        return "category"
    if any(t in up for t in MONEY_TOKENS):
        return "money"
    if up.endswith(("_CODE", "_CD")):
        return "category"
    if dt in ("NUMBER", "FLOAT"):
        return "quantity"
    return "other"


DANGLING = {"FROM", "TO", "BY", "OF", "IN", "AT", "WITH", "FOR", "ON", "VIA"}
# Short strings that ARE real words worth counting.
ACRONYMS_OK = {"NPI", "EIN", "CIK", "UEI", "LEI", "NDC", "FRN", "MINE", "SHIP",
               "BANK", "CASE", "FIRM", "PLAN", "SITE", "WELL", "DAM", "DRUG"}


def entity_noun(col: str, fallback: str) -> str | None:
    """The THING an identifier column identifies, or None if it does not name one."""
    up = col.upper()
    if up in KNOWN_IDS:
        return KNOWN_IDS[up][0]
    if up in GENERIC_IDS:
        return fallback           # a bare ID column identifies the table's own row
    base = ID_SUFFIX.sub("", up)
    base = re.sub(r"_(NAME|NAMES|FULL|FIRST|LAST)$", "", base)
    base = re.sub(r"^(PRIMARY|MAIN|SRC|SOURCE|TGT|TARGET)_", "", base)
    if not base:
        return fallback
    # APPEAL_FROM_ID, ASSIGNED_TO_ID: the tail is a preposition, so the name is a
    # relationship, not a noun. Pluralising it produces 'appeal froms'.
    if base.split("_")[-1] in DANGLING:
        return None
    out = humanize(base)
    # ASSISTANCE_TRANSACTION_UNIQUE_KEY -> 'assistance transaction', not
    # 'assistance transaction unique'. Trailing adjectives name nothing.
    words = out.split()
    while len(words) > 1 and words[-1].lower() in NOT_THINGS:
        words.pop()
    out = " ".join(words)
    # A one- or two-letter stub ('K', 'OBS') is not a word anyone would read.
    if len(out.replace(" ", "")) < 4 and out.upper() not in ACRONYMS_OK:
        return None
    # Some columns are a whole sentence ('HOW_MUCH_MEDICARE_SPENDS_ON_AN_EPISODE...').
    # That is a measure with a long label, not a thing to count.
    if len(out) > 40 or len(out.split()) > 5:
        return None
    if out.lower() in NOT_THINGS:
        return None
    return out


def blank_test(col: str, dtype: str) -> str:
    """A null/blank test that is valid for the column's actual type."""
    if dtype.upper() in TEXT_TYPES:
        return f"{col} is null or trim({col}) = ''"
    return f"{col} is null"


def load():
    cols = defaultdict(list)
    with open(os.path.join(REPO, "reports", "_all_columns.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            cols[(r["schema"], r["table"])].append((r["column"], r["dtype"], int(r["ordinal"])))

    rows = {}
    with open(os.path.join(REPO, "reports", "time_index", "live_tables.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[(r["schema_name"], r["table_name"])] = (
                int(r["row_count"]) if r["row_count"] else None)

    grain = {}
    p = os.path.join(REPO, "reports", "census_grid_2026-08-12", "table_map.csv")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r.get("grain_phrase"):
                    grain[r["model"].upper()] = r["grain_phrase"].strip()

    clock = {}
    p = os.path.join(REPO, "reports", "time_index", "clock_index.csv")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if str(r.get("is_primary")).lower() == "true":
                    clock[r["model"].upper()] = (r["column"].upper(), r["clock"], r["grain"])
    return cols, rows, grain, clock


def load_timeline():
    """The tables that have a parsed, clamped timestamp waiting in the clock layer."""
    p = os.path.join(REPO, "reports", "_timeline_aliases.json")
    if not os.path.exists(p):
        return set()
    return set(json.load(open(p, encoding="utf-8")))


def build():
    cols, rowcounts, grain, clock = load()
    timeline = load_timeline()
    entries, tables = [], []
    # Which strong keys show up in more than one table -> the joinable counts.
    key_homes = defaultdict(set)
    for (schema, table), collist in cols.items():
        for name, dtype, _ in collist:
            if name.upper() in KNOWN_IDS:
                key_homes[name.upper()].add(f"{schema}.{table}")

    for (schema, table), collist in sorted(cols.items()):
        if (schema, table) not in rowcounts:
            continue
        fqn = f"{DB}.{schema}.{table}"
        n_rows = rowcounts[(schema, table)]
        src = table.split("__", 1)[-1]
        desc = pe.TABLES.get(src.upper())
        what_it_is = desc or "No plain-English description has been written for this dataset yet."
        noun = row_noun(table, grain.get(table.upper()), desc)
        noun_known = noun != "record"
        nouns = plural(noun)

        collist_pairs = [(name, dtype) for name, dtype, _ in collist]
        roles = defaultdict(list)
        for name, dtype, ordinal in collist:
            roles[classify(name, dtype)].append((name, dtype))

        ids = (roles["id"] + roles["name"])[:6]
        cats = roles["category"][:6]
        geos = roles["geo"][:3]
        flags = roles["flag"][:3]
        money = roles["money"][:2]
        qty = roles["quantity"][:2]
        ck = clock.get(table.upper())
        date_col = ck[0] if ck and ck[1] not in ("not_a_date", "unclear") else None
        if not date_col and roles["date"]:
            date_col = roles["date"][0][0]

        out = []

        def add(kind, question, means, sql, needs="one table", rank=50):
            out.append({"kind": kind, "question": question, "means": means,
                        "sql": sql.strip(), "table": f"{schema}.{table}", "fqn": fqn,
                        "dataset": what_it_is, "subject": schema.replace("_", " ").title(),
                        "rows": n_rows, "noun": noun, "noun_known": noun_known,
                        "needs": needs, "rank": rank})

        size = (f"The dataset holds {n_rows:,} rows today."
                if n_rows is not None else
                "The row count for this table has never been recorded, so the size is unknown.")
        unknown = ("" if noun_known else
                   " No noun is on record for this table, so 'record' is a placeholder.")
        add("How many in total",
            f"How many {nouns} are there?",
            f"One row is one {noun}. {size} The whole dataset, unfiltered.{unknown}",
            f"select count(*) as n_{slug(nouns)}\nfrom {fqn};", rank=0)

        for name, dtype in ids:
            e_noun = entity_noun(name, noun)
            if e_noun is None:
                # No English noun for this key -- ask about the column instead.
                lab = humanize(name)
                add("How many different things",
                    f"How many different values does {lab} take?",
                    f"{lab} points at another record, not a named thing. Compare to the row "
                    f"count to see how much repeats.",
                    f"select count(distinct {name}) as n_values\nfrom {fqn}\n"
                    f"where {name} is not null;", rank=12)
                add("How many are missing it",
                    f"How many {nouns} have no {lab} recorded?",
                    f"The blank count on {lab}.",
                    f"select count(*) as n_missing\nfrom {fqn}\n"
                    f"where {blank_test(name, dtype)};", rank=70)
                continue
            e_nouns = plural(e_noun)
            gloss = curated(fqn, name) or (KNOWN_IDS[name.upper()][1]
                                           if name.upper() in KNOWN_IDS else None)
            tail = f" {humanize(name)} is {gloss}." if gloss else ""
            add("How many different things",
                f"How many different {e_nouns} appear?",
                f"Distinct values of {humanize(name)} - a repeated {e_noun} counts once. "
                f"Close to the row count means one row per {e_noun}; far apart means "
                f"repeats.{tail}",
                f"select count(distinct {name}) as n_{slug(e_nouns)}\n"
                f"from {fqn}\nwhere {name} is not null;", rank=10)

            if e_noun != noun:
                add("How many each one has",
                    f"How many {nouns} does each {e_noun} have?",
                    f"Ranks {e_nouns} by {nouns} count. The top may just be bigger, not more "
                    f"active - get a denominator before calling it a finding.",
                    f"select {name}, count(*) as n_{slug(nouns)}\nfrom {fqn}\n"
                    f"where {name} is not null\ngroup by 1\norder by 2 desc\nlimit 100;", rank=20)

            add("How many are missing it",
                f"How many {nouns} have no {humanize(name)} recorded?",
                f"The blank count. Large here means totals broken down by {e_noun} "
                f"quietly drop records.",
                f"select count(*) as n_missing\nfrom {fqn}\n"
                f"where {blank_test(name, dtype)};", rank=70)

            # Worth asking even when the key names the row itself -- that case is
            # the duplicate check, and it is the most useful one.
            if True:
                add("How many show up more than once",
                    f"How many {plural(e_noun)} appear more than once?",
                    f"Splits {plural(e_noun)} into once vs. repeats. Almost none repeating means "
                    f"{humanize(name)} is a real one-per-row key; almost all repeating means it's "
                    f"a grouping column, and any 'top ten' is really who appears most.",
                    f"with per_{slug(e_noun)} as (\n  select {name}, count(*) as n\n"
                    f"  from {fqn}\n  where {name} is not null\n  group by 1\n)\n"
                    f"select count(case when n = 1 then 1 end) as appears_once,\n"
                    f"       count(case when n > 1 then 1 end) as appears_more_than_once,\n"
                    f"       max(n)                            as most_for_one\n"
                    f"from per_{slug(e_noun)};", rank=72)

            if e_noun != noun:
                add("How many pass a threshold",
                    f"How many {plural(e_noun)} have at least ten {nouns}?",
                    f"The concentrated end - swap ten for your own line. Backs any claim that a "
                    f"few {plural(e_noun)} account for most {nouns}.",
                    f"with per_{slug(e_noun)} as (\n  select {name}, count(*) as n\n"
                    f"  from {fqn}\n  where {name} is not null\n  group by 1\n)\n"
                    f"select count(*) as n_{slug(plural(e_noun))}_with_10_or_more\n"
                    f"from per_{slug(e_noun)}\nwhere n >= 10;", rank=74)

            others = sorted(key_homes.get(name.upper(), set()) - {f"{schema}.{table}"})
            if others:
                other = others[0]
                add("How many across two tables",
                    f"How many {nouns} per {e_noun}, matched against another dataset?",
                    f"{humanize(name)} also appears in {len(others)} other "
                    f"{'table' if len(others) == 1 else 'tables'} - the same {e_noun} can be "
                    f"matched across both. Check both sides use the identifier the same way; "
                    f"padding and blanks have faked matches before.",
                    f"select a.{name},\n       count(*) as n_{slug(nouns)}\n"
                    f"from {fqn} as a\njoin {DB}.{other} as b\n  on a.{name} = b.{name}\n"
                    f"where a.{name} is not null\ngroup by 1\norder by 2 desc\nlimit 100;",
                    needs=f"two tables ({schema}.{table} + {other})", rank=80)

        for name, dtype in cats:
            label = humanize(name)
            add("How many of each kind",
                f"How many {nouns} of each {label}?",
                f"Splits {nouns} by {label} - the mix. A shifting mix usually says more than "
                f"the total does.",
                f"select {name}, count(*) as n\nfrom {fqn}\ngroup by 1\norder by 2 desc;", rank=30)
            add("How many kinds exist",
                f"How many different {plural(label)} are used?",
                f"Distinct values {label} takes. A handful is a real category you can chart; "
                f"thousands is closer to free text.",
                f"select count(distinct {name}) as n_{slug(label)}\nfrom {fqn};", rank=60)

        for name, dtype in geos:
            label = humanize(name)
            add("How many in each place",
                f"How many {nouns} in each {label}?",
                f"The map view. Raw counts follow population - the biggest {label} tops the "
                f"list regardless.",
                f"select {name}, count(*) as n\nfrom {fqn}\nwhere {name} is not null\n"
                f"group by 1\norder by 2 desc;", rank=40)
            if ids:
                idn, idt = ids[0]
                e_noun = entity_noun(idn, noun)
            if ids and e_noun:
                add("How many different things per place",
                    f"How many different {plural(e_noun)} in each {label}?",
                    f"Distinct {plural(e_noun)} per {label}, not rows - the denominator before "
                    f"comparing one {label} to another.",
                    f"select {name}, count(distinct {idn}) as n_{slug(plural(e_noun))}\n"
                    f"from {fqn}\nwhere {name} is not null\ngroup by 1\norder by 2 desc;", rank=45)

        for name, dtype in flags:
            label = humanize(name)
            add("How many are flagged",
                f"How many {nouns} are marked '{label}'?",
                f"Yes/no split on {label}. Check the blank count too - empty isn't the same "
                f"as false.",
                f"select {name}, count(*) as n\nfrom {fqn}\ngroup by 1\norder by 2 desc;", rank=55)

        # WHERE the time queries read from. Only 242 of the primary clock columns
        # are actually DATE-typed; the rest are text or plain numbers, and
        # year(text) is a compilation error. The timeline layer already holds a
        # parsed, clamped timestamp for 403 tables, so read that when it exists.
        tl_view = f"{DB}.TIMELINE.{table}" if f"{schema}.{table}" in timeline else None
        raw_date_ok = date_col and any(
            dt.upper() in DATE_TYPES for nm, dt in collist_pairs if nm.upper() == date_col)
        if tl_view:
            t_from, t_expr, t_src = tl_view, "ripple_ts", "clean"
        elif raw_date_ok:
            t_from, t_expr, t_src = fqn, date_col, "raw"
        else:
            t_from = t_expr = t_src = None

        if t_from:
            clock_word = {"happened": "when the thing itself happened",
                          "reported": "when it was reported, which can be long after",
                          "decided": "when an authority ruled on it",
                          "span_start": "the opening edge of a period",
                          "span_end": "the closing edge of a period"}.get(
                              ck[1] if ck else "", "the date on the record")
            add("How many per year",
                f"How many {nouns} per year?",
                f"The trend by year. The date means {clock_word}. Counts records, not events "
                f"- a rise can mean more happening or more being logged.",
                f"select year({t_expr}) as yr, count(*) as n\nfrom {t_from}\n"
                f"where {t_expr} is not null\ngroup by 1\norder by 1;", rank=5)
            if cats:
                k = cats[0][0]
                add("How the mix moved",
                    f"How many {nouns} of each {humanize(k)}, per year?",
                    f"The mix over time - a flat total with a flipping mix is the story.",
                    f"select year({t_expr}) as yr, {k}, count(*) as n\nfrom {t_from}\n"
                    f"where {t_expr} is not null\ngroup by 1, 2\norder by 1, 3 desc;", rank=35)
            if ids:
                idn, idt = ids[0]
                e_noun = entity_noun(idn, noun)
            if ids and e_noun:
                add("How many different things per year",
                    f"How many different {plural(e_noun)} appear each year?",
                    f"Distinct {plural(e_noun)} covered each year. Climbing alongside the "
                    f"totals means coverage growing, not the world changing.",
                    f"select year({t_expr}) as yr, count(distinct {idn}) as n\nfrom {t_from}\n"
                    f"where {t_expr} is not null\ngroup by 1\norder by 1;", rank=15)
                add("How many arrived and left",
                    f"How many {plural(e_noun)} show up for the first time each year?",
                    f"New arrivals - first year each {e_noun} is seen. Swap min for max for "
                    f"last seen, the closest thing here to a death date.",
                    f"with first_seen as (\n  select {idn}, min(year({t_expr})) as yr\n"
                    f"  from {t_from}\n  where {t_expr} is not null and {idn} is not null\n"
                    f"  group by 1\n)\nselect yr, count(*) as n_new\nfrom first_seen\n"
                    f"group by 1\norder by 1;", rank=25)

        for name, dtype in money:
            label = humanize(name)
            add("How many have a value",
                f"How many {nouns} carry {article(label)} {label} at all?",
                f"Rows where {label} is filled, and how many are zero. Run before totalling - "
                f"a mostly-blank column makes a made-up total.",
                f"select count(*) as n_rows,\n       count({name}) as n_with_value,\n"
                f"       count(case when {name} = 0 then 1 end) as n_zero\nfrom {fqn};", rank=65)

        for name, dtype in qty:
            label = humanize(name)
            add("How many have a value",
                f"How many {nouns} have {article(label)} {label} recorded?",
                f"Fill check on {label}. Averaging a half-empty column only describes the "
                f"filled half.",
                f"select count(*) as n_rows, count({name}) as n_filled\nfrom {fqn};", rank=66)

        # Two columns can produce the same question ('how many different dockets'
        # from both ID and DOCKET_NUMBER). Name the column so they are telling apart.
        seen = defaultdict(int)
        for e in out:
            seen[e["question"]] += 1
        used = defaultdict(int)
        for e in out:
            if seen[e["question"]] > 1:
                used[e["question"]] += 1
                m = re.search(r"count\(distinct\s+([A-Z_0-9]+)\)", e["sql"])
                if not m:
                    m = re.search(r"select\s+([A-Z_0-9]+),", e["sql"])
                if m:
                    e["question"] = e["question"].rstrip("?") + f" (going by {humanize(m.group(1))})?"

        out.sort(key=lambda e: e["rank"])
        entries.extend(out)
        tables.append({"table": f"{schema}.{table}", "subject": schema.replace("_", " ").title(),
                       "dataset": what_it_is, "noun": noun, "noun_known": noun_known,
                       "rows": n_rows, "n_counts": len(out), "n_columns": len(collist),
                       "has_clock": bool(t_from)})
    return entries, tables


if __name__ == "__main__":
    entries, tables = build()
    out = os.path.join(REPO, "reports", "count_possibilities.json")
    json.dump({"entries": entries, "tables": tables},
              open(out, "w", encoding="utf-8"), indent=1)
    from collections import Counter
    print(f"{len(entries):,} counts across {len(tables):,} tables -> {out}")
    for k, n in Counter(e["kind"] for e in entries).most_common():
        print(f"  {n:>6,}  {k}")
    print(f"  tables with no written description: "
          f"{sum(1 for t in tables if not t['noun_known']):,}")
