"""Turning table and column names into English that reads like a person wrote it.

Split out of count_possibilities.py because this is where the whole thing lives
or dies: a count called "how many federal court case file -s are there" is
useless, and "how many case files are there" is not.
"""
from __future__ import annotations

import re

# Words that really are countable things, so a table ending in one can be named
# after it. Deliberately a whitelist -- table names also end in AGG, DATA, BULK,
# API and 2023, none of which name a thing.
THING_TAILS = {
    "ACCIDENTS": "accident", "ACTIONS": "action", "AGENCIES": "agency",
    "AIRCRAFT": "aircraft", "APPLICATIONS": "application", "APPROVALS": "approval",
    "AREAS": "area", "ARRESTS": "arrest", "AWARDS": "award", "BANKS": "bank",
    "BILLS": "bill", "BOUNDARIES": "boundary", "CANDIDATES": "candidate",
    "CASES": "case", "CITATIONS": "citation", "CLAIMS": "claim",
    "CLEARANCES": "clearance", "CLUSTERS": "opinion cluster", "COMMITTEES": "committee",
    "COMPANIES": "company", "COMPLAINTS": "complaint", "CONTRACTS": "contract",
    "CONTRIBUTION": "contribution", "CONTRIBUTIONS": "contribution",
    "CONVICTIONS": "conviction", "COURTS": "court", "DAMS": "dam",
    "DEATHS": "death", "DEBARMENTS": "debarment", "DEFICIENCIES": "deficiency",
    "DESIGNATIONS": "designation", "DEVICES": "device", "DIRECTORS": "director",
    "DISCLOSURES": "disclosure", "DOCKETS": "docket", "DOCUMENTS": "document",
    "DONATIONS": "donation", "DRUGS": "drug", "EARTHQUAKES": "earthquake",
    "EMPLOYERS": "employer", "ENFORCEMENT": "enforcement action",
    "ENROLLMENTS": "enrolment", "ENTITIES": "entity", "EVENTS": "event",
    "EXCLUSIONS": "exclusion", "FACILITIES": "facility", "FACILITY": "facility",
    "FAILURES": "failure", "FILINGS": "filing", "FINES": "fine",
    "GAUGES": "gauge", "GENERATORS": "generator", "GRANTS": "grant",
    "HOSPITALS": "hospital", "INCIDENTS": "incident", "INJURIES": "injury",
    "INSPECTIONS": "inspection", "INVESTIGATIONS": "investigation",
    "JUDGES": "judge", "LICENCES": "licence", "LICENSES": "licence",
    "LINKS": "link", "LOANS": "loan", "MEMBERS": "member", "MINES": "mine",
    "MONITORS": "monitor", "OFFICERS": "officer", "OPINIONS": "opinion",
    "ORDERS": "order", "ORGANIZATIONS": "organisation", "OWNERS": "owner",
    "PAPERS": "paper", "PATENTS": "patent", "PAYMENTS": "payment",
    "PENALTIES": "penalty", "PERMITS": "permit", "PLANS": "plan",
    "PLANTS": "plant", "POSITIONS": "position", "PRODUCTS": "product",
    "PROJECTS": "project", "PROVIDERS": "provider", "RECALLS": "recall",
    "RECORDS": "record", "REGISTRATIONS": "registration", "REPORTS": "report",
    "RETRACTIONS": "retraction", "RETURNS": "tax return", "REVOCATIONS": "revocation",
    "RULES": "rule", "SAMPLES": "sample", "SANCTIONS": "sanction",
    "SCHOOLS": "school", "SETTLEMENTS": "settlement", "SHIPMENTS": "shipment",
    "SHIPS": "ship", "SITES": "site", "SPECIES": "species", "STATIONS": "station",
    "SUBMISSIONS": "submission", "SYSTEMS": "system", "TESTS": "test",
    "TRANSACTIONS": "transaction", "TRIALS": "trial", "VEHICLES": "vehicle",
    "VESSELS": "vessel", "VIOLATIONS": "violation", "VISITS": "visit",
    "VOTES": "vote", "WELLS": "well", "TRADEMARKS": "trademark",
    "SUSPENSIONS": "suspension", "WARNINGS": "warning", "LETTERS": "letter",
    "SPILLS": "spill", "RELEASES": "release", "EMISSIONS": "emission",
    "OUTAGES": "outage", "CROSSINGS": "crossing", "STOPS": "stop",
    "SEIZURES": "seizure", "DETENTIONS": "detention", "REMOVALS": "removal",
    "PETITIONS": "petition", "APPEALS": "appeal", "MOTIONS": "motion",
    "BANKRUPTCIES": "bankruptcy", "FORECLOSURES": "foreclosure",
    "MORTGAGES": "mortgage", "POLICIES": "policy", "PRESCRIPTIONS": "prescription",
}

IRREGULAR_PLURALS = {
    "aircraft": "aircraft", "species": "species", "series": "series",
    "person": "people", "child": "children", "man": "men", "woman": "women",
}

ACRONYMS = {"NPI", "EIN", "CIK", "UEI", "LEI", "SEC", "FDA", "EPA", "IRS", "FBI",
            "DEA", "CMS", "HHS", "DOT", "DOL", "FEC", "FCC", "FAA", "USDA", "VA",
            "US", "UK", "EU", "UN", "ID", "URL", "ZIP", "GDP", "CEO", "CFO",
            "MSHA", "OSHA", "NAICS", "SIC", "CBSA", "MSA", "FIPS", "NDC", "PWSID",
            "SIC", "PPP", "SBA", "ICE", "TSA", "ATF", "NIH", "CDC", "GAO"}

# Noise words a table name ends with that never name a thing.
NON_NOUN_TAILS = {"AGG", "DATA", "LIST", "FULL", "SUMMARY", "STATS", "API",
                  "BULK", "GEO", "CROSSWALK", "XREF", "MAP", "INDEX", "RAW",
                  "HISTORIC", "CURRENT", "ALL", "MASTER", "DETAIL", "MAIN",
                  "FILE", "FILES", "EXPORT", "DUMP", "SNAPSHOT", "V2", "V1"}


def article(word: str) -> str:
    """'a' or 'an', judged on the sound of the first letter."""
    w = word.strip().lower()
    if not w:
        return "a"
    first = w[0]
    if first in "aeiou":
        # 'a university', 'a one-off' are the exceptions people notice.
        if re.match(r"^(uni|use|user|usu|one|once|euro)", w):
            return "a"
        return "an"
    # An acronym read letter by letter: F, H, L, M, N, R, S, X start with a vowel sound.
    if word[:2].isupper() and len(word) > 1 and first.upper() in "FHLMNRSX":
        return "an"
    return "a"


def humanize(col: str) -> str:
    """FACILITY_TYPE -> 'facility type', keeping real acronyms uppercase."""
    parts = [p for p in re.split(r"[_\s]+", str(col)) if p]
    return " ".join(p if p.upper() in ACRONYMS else p.lower() for p in parts)


def singular(word: str) -> str:
    w = word.strip()
    low = w.lower()
    if low in IRREGULAR_PLURALS.values():
        return low
    if low.endswith("ies") and len(low) > 4:
        return low[:-3] + "y"
    if low.endswith(("ses", "xes", "zes", "ches", "shes")):
        return low[:-2]
    if low.endswith("s") and not low.endswith(("ss", "us", "is")):
        return low[:-1]
    return low


def plural(phrase: str) -> str:
    """Pluralise the LAST word of a phrase, and never emit '-s'."""
    p = re.sub(r"[\s\-]+$", "", str(phrase).strip())
    if not p:
        return "records"
    words = p.split()
    last = words[-1]
    low = last.lower()
    if low in IRREGULAR_PLURALS:
        words[-1] = IRREGULAR_PLURALS[low]
        return " ".join(words)
    if low in IRREGULAR_PLURALS.values():
        return " ".join(words)
    # Already plural ('judges', 'notices'): leave it alone rather than make
    # 'judgeses'. A word that is unchanged by singular() is genuinely singular.
    if low.endswith("s") and not low.endswith(("ss", "us", "is")) and singular(low) != low:
        return " ".join(words)
    if low.endswith(("s", "x", "z")) or low.endswith(("ch", "sh")):
        words[-1] = last + "es"
    elif low.endswith("y") and len(low) > 1 and low[-2] not in "aeiou":
        words[-1] = last[:-1] + "ies"
    else:
        words[-1] = last + "s"
    return " ".join(words)


def clean_phrase(s: str) -> str:
    """Strip the junk that makes a generated noun read like machine output."""
    s = str(s or "").strip()
    s = re.sub(r"\s*[\-–—]\s*$", "", s)      # trailing dash
    s = re.sub(r"[.,;:]+$", "", s)                       # trailing punctuation
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"^(the|a|an)\s+", "", s, flags=re.I)     # leading article
    return s.strip()


def noun_from_table_name(table: str) -> str | None:
    """VIOLATIONS at the end of a table name means the rows are violations."""
    src = table.split("__", 1)[-1].upper()
    tokens = [t for t in src.split("_") if t]
    for tok in reversed(tokens):
        if tok in NON_NOUN_TAILS or tok.isdigit():
            continue
        if tok in THING_TAILS:
            return THING_TAILS[tok]
        break
    return None


UNCOUNTABLE = {"money", "cash", "data", "information", "spending", "revenue",
               "funding", "traffic", "weather", "research", "evidence", "news",
               "software", "equipment", "staff", "content", "coverage", "activity",
               "electricity", "energy", "water", "air", "land", "health", "safety",
               "how", "what", "which", "who", "where", "when", "why"}

# A description that opens as a question ("How much electricity each plant made")
# describes a measure, not a countable row.
QUESTION_LEAD = re.compile(r"^(how|what|which|who|whose|where|when|why)", re.I)

# Phrases that describe the CONTAINER, not the thing. Strip them and look again.
META_LEAD = re.compile(
    r"^(?:a|an|the)?\s*(?:small\s+)?(?:sample|index|list|catalogue|catalog|register|"
    r"registry|directory|inventory|collection|set|table|file|extract|snapshot|"
    r"summary|summaries|figures|statistics|stats|records|details|information|data)"
    r"\s+(?:of|on|from|about|for)\s+(?:every|each|all|the|a|an)?\s*",
    re.I)

STOPWORDS = {"of", "in", "from", "to", "by", "for", "with", "on", "at", "about",
             "under", "over", "into", "across", "between", "against", "during",
             "that", "who", "whom", "which", "whose", "where", "when", "while",
             "is", "are", "was", "were", "has", "have", "had", "each", "every",
             "and", "or", "plus", "including", "the", "a", "an", "as", "per"}

PARTICIPLE = re.compile(r"^[a-z]+(?:ed|ing)$")


def _head_phrase(text: str) -> str | None:
    """The leading noun phrase of a sentence, cut at the first preposition or verb."""
    words = re.findall(r"[A-Za-z][A-Za-z\-']*", text)
    kept = []
    for w in words[:6]:
        low = w.lower()
        if kept and (low in STOPWORDS or PARTICIPLE.match(low)):
            break
        if not kept and low in ("a", "an", "the", "every", "each", "all"):
            continue
        if not kept and (low in STOPWORDS or PARTICIPLE.match(low)):
            return None
        kept.append(w)
        # A possessive is not a plural: "Spain's official companies gazette"
        # has to keep reading past "Spain's".
        if re.search(r"['’]s$", w):
            continue
        # A plural word ends the noun phrase: 'Filings companies are required'
        # is one thing (a filing) followed by a new clause, not two.
        if low.endswith("s") and not low.endswith(("ss", "us", "is")):
            break
        if len(kept) >= 4:
            break
    if not kept:
        return None
    return " ".join(kept)


def noun_from_description(desc: str) -> str | None:
    """Pull the countable noun out of a hand-written dataset sentence."""
    if not desc:
        return None
    text = desc.strip()
    if QUESTION_LEAD.match(text):
        return None
    for _ in range(2):                       # 'A small sample of federal grants'
        stripped = META_LEAD.sub("", text, count=1)
        if stripped == text:
            break
        text = stripped
    phrase = _head_phrase(text)
    if not phrase:
        return None
    phrase = clean_phrase(phrase)
    # "Spain's official companies gazette" -> drop the possessive owner.
    phrase = re.sub(r"^\S+['\u2019]s\s+", "", phrase).strip()
    # A bare possessive names an owner, not a countable thing.
    if not phrase or re.search(r"['\u2019]s$", phrase):
        return None
    words = phrase.split()
    head = singular(words[-1])
    if head in UNCOUNTABLE or len(head) < 3:
        return None
    words[-1] = head
    out = " ".join(w if w.upper() in ACRONYMS else w.lower() for w in words)
    return out if 2 < len(out) < 45 else None


# Adjectives and positions that describe a row without naming one.
NOT_A_THING = {"unique", "uniques", "last", "first", "prior", "next", "old", "new",
               "main", "other", "misc", "temp", "sub", "alt", "orig", "current",
               "total", "detail", "full", "raw", "final", "annual", "monthly"}


def row_noun(table: str, grain_phrase: str | None, description: str | None) -> str:
    """What one row of this table IS, as a singular noun phrase."""
    for candidate in (grain_phrase, noun_from_table_name(table), noun_from_description(description)):
        c = clean_phrase(candidate) if candidate else ""
        if not c or not (2 < len(c) < 45) or c.lower().startswith("one row"):
            continue
        if c.lower() in NOT_A_THING:
            continue
        return c
    return "record"
