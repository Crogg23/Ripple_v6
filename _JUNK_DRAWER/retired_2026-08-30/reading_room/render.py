"""Case-file layout helpers — pure functions, no SQL, no streamlit, no
network. Everything here turns mart columns into plain English an analyst
can act on. Deterministic by construction (fixed dicts, no model anywhere).

Since 2026-08-01 the tier and verdict wording comes from the shared
top-level glossary package — one plain-English vocabulary across the
Reading Room and the Playground.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from glossary import GLOSSARY  # noqa: E402

TIER_DEFS = {k: GLOSSARY[k] for k in (
    "FACT_GRADE_3_SOURCE", "TWO_SOURCE", "NPPES_CONFLICT",
    "LEIE_ROW_MISSING", "HARD_ID_ONLY")}

VERDICT_TEXT = {k: GLOSSARY[k] for k in (
    "PAID_ON_OR_AFTER_EXCLUSION", "PAYMENTS_PREDATE_EXCLUSION",
    "TIMELINE_UNKNOWN", "NOT_EVALUATED")}


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


# ---------------------------------------------------------------------------
# Source-record elucidation — raw government fields, translated in place.
# Deterministic dicts only. Rules:
#   * every field is shown (nothing hidden),
#   * a translated value keeps the raw form beside it: "2023-09-20 (raw 20230920)",
#   * sentinels are decoded, never displayed bare (00000000, 0000000000, '-0- ').
# ---------------------------------------------------------------------------

# OIG 1128 exclusion codes -> plain English (same map lead_queue.sql ships).
EXCLTYPE_PLAIN = {
    "1128a1": "Conviction of a Medicare/Medicaid program-related crime",
    "1128a2": "Conviction relating to patient abuse or neglect",
    "1128a3": "Felony conviction relating to health-care fraud",
    "1128a4": "Felony conviction relating to controlled substances",
    "1128b1": "Misdemeanor conviction relating to health-care fraud",
    "1128b4": "License revoked, suspended, or surrendered",
    "1128b5": "Exclusion/suspension under a federal/state health program",
    "1128b7": "Fraud, kickbacks, or other prohibited activities",
    "1128b8": "Entities controlled by a sanctioned individual",
}

# raw column -> (plain label, optional note shown once per panel)
FIELD_LABELS = {
    "leie": {
        "lastname":  ("Last name", None),
        "firstname": ("First name", None),
        "midname":   ("Middle name", "OIG's file has no suffix column — "
                      "generational suffixes like 'II' get crammed in here "
                      "by their data entry, not by Ripple."),
        "busname":   ("Business name", None),
        "general":   ("Provider category (OIG shorthand)", None),
        "specialty": ("Specialty", None),
        "npi":       ("NPI (federal provider ID)", None),
        "upin":      ("UPIN (legacy pre-NPI provider ID)", None),
        "dob":       ("Date of birth", None),
        "address":   ("Address", None),
        "city":      ("City", None),
        "state":     ("State", None),
        "zip":       ("ZIP", None),
        "excltype":  ("Exclusion authority (statute code)", None),
        "excldate":  ("Excluded on", None),
        "reindate":  ("Reinstated on", None),
        "waiverdate": ("Waiver granted on", None),
        "wvrstate":  ("Waiver state", None),
    },
    "nppes": {
        "provider_last_name_legal_name": ("Legal last name", None),
        "provider_first_name":           ("First name", None),
        "provider_middle_name":          ("Middle name", None),
        "provider_name_suffix_text":     ("Suffix (Jr/II/...)", None),
        "provider_credential_text":      ("Credential (MD/DPM/...)", None),
        "npi":                           ("NPI (federal provider ID)", None),
    },
}


def _elucidate_value(source: str, field: str, raw: str) -> str:
    """Translate one raw value. Always returns display text; keeps the raw
    form visible whenever the translation changed it."""
    v = raw.strip()
    if v == "":
        return "—"
    f = field.lower()

    # OIG all-zero date sentinels: not a date, a state.
    if f == "reindate" and set(v) <= {"0"}:
        return "never — the exclusion is still active (raw 00000000)"
    if f in ("excldate", "reindate", "waiverdate", "dob"):
        if len(v) == 8 and v.isdigit():
            return f"{v[0:4]}-{v[4:6]}-{v[6:8]} (raw {v})"
        return v
    if f == "npi" and set(v) <= {"0"}:
        return "not recorded by OIG (raw 0000000000) — identity rests on name only"
    if f == "excltype":
        plain = EXCLTYPE_PLAIN.get(v.lower())
        return f"{plain} ({v})" if plain else v
    if v in ("-0-", "-0- "):
        return "— (source null token '-0-')"
    return v


def source_rows_to_panel(rows: list[dict], title: str) -> dict:
    """Normalize a source-record pull into a display panel: every field,
    plain-English labeled, sentinels decoded, NULLs shown as em-dashes
    (never hidden). `title` picks the label map ('leie' / 'nppes'); unknown
    sources fall back to raw field names."""
    labels = FIELD_LABELS.get(title, {})
    records, notes = [], []
    for row in rows:
        rec = {}
        for k, v in row.items():
            field = str(k)
            raw = "" if v is None else str(v)
            label_info = labels.get(field.lower())
            label = label_info[0] if label_info else field
            if label_info and label_info[1] and label_info[1] not in notes \
                    and raw.strip():
                notes.append(label_info[1])
            rec[label] = _elucidate_value(title, field, raw)
        records.append(rec)
    return {"title": title, "records": records, "notes": notes}


def name_conflict_message(leie_first: str | None,
                          nppes_first: str | None) -> str:
    """The audit-F4 warning for a hard first-name disagreement between the
    ban list and the registry. The tier corroborates on surname only, so
    this is surfaced loudly instead of oversold as fact-grade."""
    return (f"First names disagree across sources: OIG-LEIE says "
            f"“{leie_first or '—'}” but the NPPES registry says "
            f"“{nppes_first or '—'}” for this NPI. Often a "
            f"same-person alternate or anglicized name — verify the identity "
            f"before treating the corroboration as fact-grade.")


# ---------------------------------------------------------------------------
# Pattern Desk helpers — pure, deterministic, no SQL/streamlit/network.
# ---------------------------------------------------------------------------

def parse_receipts(raw) -> list[dict]:
    """The cohort mart's receipts_sample arrives as a VARIANT — usually a
    JSON string from the connector, occasionally already a list. Normalize
    to a list of dicts; anything unparseable becomes an empty list (the desk
    shows the member-list fallback instead of crashing)."""
    import json as _json
    if raw is None:
        return []
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    try:
        parsed = _json.loads(raw)
        return [r for r in parsed if isinstance(r, dict)] \
            if isinstance(parsed, list) else []
    except Exception:
        return []


def receipts_table(receipts: list[dict]) -> list[dict]:
    """Format the receipts sample for display: plain labels, em-dash for
    missing values, fold shown as '12.3x'. Every receipt keeps its lead_id
    so the desk can drill into the full case file."""
    out = []
    for r in receipts:
        def _v(key, suffix=""):
            v = r.get(key)
            return "—" if v is None else f"{v}{suffix}"
        out.append({
            "Lead": _v("lead_id"),
            "Establishment": _v("title"),
            "Where": (f"{r.get('city') or '—'}, {r.get('state') or '—'}"),
            "Employees": _v("employees"),
            "DART cases": _v("dart_cases"),
            "DART rate": _v("dart_rate"),
            "vs cohort": _v("fold", "x"),
            "Deaths": _v("deaths"),
        })
    return out


def cohort_features(row: dict) -> list[str]:
    """The 'what fired, in plain English' block for a cohort case file."""
    feats = [
        (f"Peer cohort = every 2024 OSHA Form 300A filer sharing "
         f"NAICS-{row.get('naics') or '—'} and the "
         f"{row.get('size_band') or '—'}-employee size band "
         f"({row.get('cohort_n') or '—'} establishments). Same industry, "
         f"same size — the fairest available comparison group."),
        (f"The cohort's pooled DART rate — DART means "
         f"{GLOSSARY['DART']} — is "
         f"{row.get('cohort_pooled_dart') or '—'}. Every establishment "
         f"flagged here reports at least 2x that, with at least 5 DART "
         f"cases — small-numbers noise is filtered before anything is "
         f"flagged."),
        ("A verdict on this cohort covers every member lead that has no "
         "individual decision; individual lead decisions always win "
         "(specific beats general). Nothing here can publish — publishing "
         "is a separate per-lead act with its own gate."),
    ]
    return feats


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
