"""Case-file layout helpers — pure functions, no SQL, no streamlit, no
network. Everything here turns mart columns into plain English an analyst
can act on. Deterministic by construction (fixed dicts, no model anywhere).
"""
from __future__ import annotations

TIER_DEFS = {
    "FACT_GRADE_3_SOURCE": (
        "Name agrees across all three federal sources (NPPES registry + "
        "OIG-LEIE + the activity source) on the same hard ID. The strongest "
        "corroboration this detector can produce."),
    "TWO_SOURCE": (
        "The ban and the activity agree on ID and name, but the NPPES "
        "registry record is blank/deactivated — the third confirmation "
        "isn't available. Manual check before publishing."),
    "NPPES_CONFLICT": (
        "The NPPES registry shows a DIFFERENT surname on this ID. Often a "
        "credential-suffix artifact ('Smith Md Pc'), sometimes a genuine "
        "identity problem — verify before using."),
    "LEIE_ROW_MISSING": (
        "The exclusion row has vanished from the current LEIE file since "
        "this lead was detected (OIG's monthly refresh removes reinstated "
        "providers). No comparison is possible; the ban may have been "
        "lifted — check the OIG site before anything else."),
    "HARD_ID_ONLY": (
        "A hard-ID detector (UEI / IMO / EIN): the key match IS the "
        "identity, and no third registry exists to corroborate against. "
        "Names from both sides are shown for the eyeball check."),
}

VERDICT_TEXT = {
    "PAID_ON_OR_AFTER_EXCLUSION": (
        "The latest recorded payment is ON or AFTER the exclusion date — "
        "activity while banned."),
    "PAYMENTS_PREDATE_EXCLUSION": (
        "All recorded payments predate the exclusion (later-excluded; "
        "weaker as a story)."),
    "TIMELINE_UNKNOWN": (
        "A date needed for the timeline is missing from the current source "
        "rows — no on/after claim can be made."),
    "NOT_EVALUATED": (
        "This detector's activity side carries no usable dates — the "
        "timeline was not evaluated, by design."),
}


def linkage_features(detector: str, key_type: str, key_value: str,
                     tier: str) -> list[str]:
    """The 'what fired, in plain English' block. Detector leads join on hard
    federal IDs — there are no probabilistic weights to show (the fuzzy
    matcher's calibration applies to entity resolution, not these leads)."""
    key_names = {
        "NPI": "NPI (national provider ID — unique, never reused)",
        "UEI": "UEI (SAM.gov unique entity ID, 12-char)",
        "IMO": "IMO hull number (permanent — a vessel can repaint its name, "
               "not its hull number)",
        "EIN": "EIN (federal tax ID, 9-digit)",
    }
    feats = [f"Exact match on {key_names.get(key_type, key_type)}: "
             f"{key_value} appears on BOTH lists — the match is the identity "
             f"(fact_vs_lead: hard ID across two sources = FACT)."]
    if key_type == "NPI":
        if tier == "FACT_GRADE_3_SOURCE":
            feats.append("Surname agreement across all 3 sources — the "
                         "corroboration that a fat-fingered ID can't fake.")
        elif tier in TIER_DEFS:
            feats.append(f"Corroboration state: {tier} — "
                         f"{TIER_DEFS[tier]}")
    else:
        feats.append("Name fields from both sides are displayed for the "
                     "eyeball check (no automatic name matching was used).")
    return feats


def source_rows_to_panel(rows: list[dict], title: str) -> dict:
    """Normalize a source-record pull into a display panel: every field,
    labeled, NULLs shown as em-dashes (never hidden)."""
    return {
        "title": title,
        "records": [
            {str(k): ("—" if v is None or str(v).strip() == "" else str(v))
             for k, v in row.items()}
            for row in rows
        ],
    }


def three_sources(row: dict) -> list[str]:
    """The receipt's source list for the verdict section."""
    out = []
    if row.get("entity_a_source"):
        out.append(f"[flag]      {row['entity_a_source']}")
    if (row.get("entity_a_key_type") or "") == "NPI":
        out.append("[registry]  LIBRARY_RAW.LANDING.FED_CMS_NPPES")
    if row.get("entity_b_source"):
        out.append(f"[activity]  {row['entity_b_source']}")
    return out
