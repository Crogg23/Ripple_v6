"""The shared plain-English glossary - one place where Ripple's jargon gets
translated, imported by BOTH the Reading Room and the Playground so the whole
product speaks one language (the beer rule, applied as code).

Pure data + pure functions: no SQL, no network, no streamlit. ASCII only.
Curated per-column glosses live in glossary/column_gloss.py and win over the
heuristics here.
"""
from __future__ import annotations

# --------------------------------------------------------------------------- #
# Jargon -> plain English. Keys are the EXACT vocabulary strings the platform
# uses (tier names, verdict names, column names, key names). Tests assert
# coverage, the Reading Room renders these verbatim, the Playground shows
# them beside raw column names.
# --------------------------------------------------------------------------- #
GLOSSARY: dict[str, str] = {

    # ---- connection-strength tiers (the graph vocabulary) ----
    "STEEL": "matched on the same government ID number - the strongest kind of match",
    "STRONG": "matched on an official identifier that is reliable but not a primary government ID",
    "PROBABILISTIC": "matched on name only - treat as a lead to verify, never a fact",
    "GEO": "matched by location only - same place, not necessarily the same thing",

    # ---- Reading Room confidence tiers ----
    "FACT_GRADE_3_SOURCE": (
        "All three federal files agree on this person: the ban list, the "
        "provider registry, and the activity records carry the same ID and "
        "the same name. The strongest corroboration this check can produce."),
    "TWO_SOURCE": (
        "The ban and the activity agree on ID and name, but the federal "
        "provider registry entry is blank or deactivated - the third "
        "confirmation is not available. Check by hand before relying on it."),
    "NPPES_CONFLICT": (
        "The federal provider registry shows a DIFFERENT last name for this "
        "ID. Often a paperwork artifact (a business suffix crammed into the "
        "name), sometimes a genuine identity problem - verify before using."),
    "LEIE_ROW_MISSING": (
        "The exclusion row has vanished from the current ban list since this "
        "lead was found (the monthly refresh removes reinstated providers). "
        "The ban may have been lifted - check the OIG site first."),
    "HARD_ID_ONLY": (
        "The match is on a hard government ID (company, vessel, or employer "
        "number) and no third registry exists to double-check the name. "
        "Names from both sides are shown for the eyeball check."),

    # ---- Reading Room timeline verdicts ----
    "PAID_ON_OR_AFTER_EXCLUSION": (
        "The latest recorded payment is ON or AFTER the exclusion date - "
        "activity while banned."),
    "PAYMENTS_PREDATE_EXCLUSION": (
        "All recorded payments happened BEFORE the exclusion - the person "
        "was banned later. Weaker as a story."),
    "TIMELINE_UNKNOWN": (
        "A date needed for the before/after comparison is missing from the "
        "current source rows - no timing claim can be made."),
    "NOT_EVALUATED": (
        "This check's records carry no usable dates - the timing comparison "
        "was not attempted, by design."),

    # ---- decision vocabulary ----
    "confirmed": "a human looked at this and nominated it as real (nothing publishes from this alone)",
    "rejected": "a human looked at this and ruled it out - it never shows again",
    "needs_work": "flagged for another look - stays visible, marked",
    "retracted": "was confirmed once, then withdrawn - it never shows again",
    "stale": "the records that supported it have vanished from the source - retired",
    "published": "went through the separate, explicit publish step - the only state that is public-facing",

    # ---- workplace-injury (OSHA) vocabulary ----
    "DART": ("injuries serious enough to cause Days Away from work, "
             "Restricted duty, or a job Transfer - the standard severity "
             "measure on OSHA Form 300A"),
    "DART_RATE": ("serious injuries per 100 full-time workers per year "
                  "(cases x 200,000 / hours worked)"),
    "POOLED_RATE": ("the peer group's combined rate: all its injuries "
                    "divided by all its hours - steadier than averaging "
                    "each company's own rate"),
    "FOLD": "how many times the typical rate - 3x means triple the peers",
    "NAICS": "the federal industry classification code - which line of business",
    "SIZE_BAND": "employer size bucket by employee count, so companies are compared with similar-sized peers",

    # ---- FEC / campaign-money columns ----
    "TTL_RECEIPTS": "total money the committee reported taking in",
    "TRANS_FROM_AUTH": ("money moved over from the candidate's other "
                        "committees - subtract it or you double-count"),
    "TTL_INDIV_CONTRIB": "total from individual people (as opposed to PACs and committees)",
    "TTL_DISB": "total money the committee reported spending",
    "COH_COP": "cash on hand at the close of the reporting period",
    "CAND_ID": "the FEC's ID for a candidate (one person can hold several across cycles)",
    "CMTE_ID": "the FEC's ID for a committee (the entity that actually raises and spends)",
    "TRANSACTION_PGI": "which race the money was for: P = primary, G = general, plus a year",

    # ---- hard ID keys ----
    "BIOGUIDE": ("Congress's permanent member ID (from the Biographical "
                 "Directory) - the cleanest key for a member of Congress"),
    "ICPSR": "the political-science member ID used by the roll-call vote archive",
    "FEC_CAND_ID": "the FEC candidate ID - bridges a member to their campaign money",
    "FEC_CMTE_ID": "the FEC committee ID - the entity that raises and spends",
    "NPI": "national provider ID - a doctor or facility's unique federal number, never reused",
    "EIN": "federal employer tax ID, 9 digits",
    "UEI": "SAM.gov unique entity ID - who the government does business with",
    "CIK": "the SEC's company filer ID",
    "IMO": "a ship's permanent hull number - a vessel can repaint its name, not its hull number",
    "CCN": "CMS certification number - a healthcare facility's Medicare ID",
    "TICKER": "the stock-exchange symbol for a traded company",
}


def gloss(term: str, default: str | None = None) -> str | None:
    """Exact-match lookup, case-sensitive first, then upper-cased."""
    if term in GLOSSARY:
        return GLOSSARY[term]
    return GLOSSARY.get(str(term).upper(), default)


def heuristic_gloss(column: str, detected_key: str | None = None,
                    chart_role: str | None = None) -> str:
    """A best-effort plain reading of a column when no curated gloss exists.
    Deterministic, word-level, honest about being a guess ('looks like')."""
    if detected_key and detected_key in GLOSSARY:
        return GLOSSARY[detected_key]
    name = str(column).upper()
    if name in GLOSSARY:
        return GLOSSARY[name]
    words = name.replace("_", " ").strip().lower()
    hints = []
    if chart_role == "date" or any(t in name for t in ("DATE", "_DT")):
        hints.append("a date")
    elif chart_role == "numeric" or any(
            t in name for t in ("AMOUNT", "TOTAL", "_USD", "COST", "COUNT",
                                "RATE", "PCT", "NUM_")):
        hints.append("a number")
    elif chart_role == "category":
        hints.append("a category with a small set of values")
    if hints:
        return f"{words} (looks like {hints[0]})"
    return words
