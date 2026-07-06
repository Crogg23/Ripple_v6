"""Key-type -> spine_entity mapping for the registry-driven staging generator.

Mirrors connect/spine.py's ``_ENTITY_TYPE_SQL`` (NPI->provider, CCN->facility,
IMO/MMSI->vessel, BIOGUIDE/ICPSR->person, everything else->organization) so a
source classified here resolves to the SAME entity type connect/'s spine already
writes into ``LIBRARY_META.CONNECT.ENTITY_MAP`` -- extended with grains connect/
doesn't resolve to a hard ID yet (place, case, asset). Chris's Step-1 taxonomy
call (2026-07-05):
  - company collapses into organization (matches connect/'s catch-all; avoids a
    third taxonomy fork alongside connect/'s resolver and the registry's
    ENTITY_TYPES facet, which does keep company distinct for its own purposes).
  - place is included now as a label even though connect/ has no place resolver
    (FIPS/ZIP/GEOM are join-key tiers there, not ENTITY_MAP entries) -- makes the
    61-source gap visible instead of hiding it.
  - PATENT is classified 'asset' here. connect/spine.py's catch-all ELSE would
    call it 'organization' -- that's not fixed there (out of scope: live
    production code), only diverged from here.

NOT importing connect/spine.py's _ENTITY_TYPE_SQL directly -- it's an inline SQL
string, not a mapping. Keep SPINE_ENTITY_BY_KEY in sync by hand if that CASE
expression ever changes.

Only keys that identify a THING are natural-key candidates. NAICS/SIC/NCES are
STRONG-tier in connect/keys.py's tagger but are classification codes, not entity
IDs (many organizations share one NAICS code) -- deliberately excluded here.
"""

from __future__ import annotations

import sys
from pathlib import Path

_CONNECT = Path(__file__).resolve().parent
if str(_CONNECT) not in sys.path:
    sys.path.insert(0, str(_CONNECT))

from keys import ENTITY_KEYS, detect_key  # noqa: E402  (connect/keys.py)

# key_label -> spine_entity. Ordered by connect/spine.py's classifier first, then
# the additive grains. A key absent here is not spine-eligible (e.g. NAICS/SIC/NCES,
# NAME/ADDRESS -- never a reliable unique natural key on their own).
SPINE_ENTITY_BY_KEY: dict[str, str] = {
    "NPI": "provider",
    "CCN": "facility",
    "IMO": "vessel",
    "MMSI": "vessel",
    "BIOGUIDE": "person",
    "ICPSR": "person",
    "EIN": "organization",
    "CIK": "organization",
    "UEI": "organization",
    "DUNS": "organization",
    "LEI": "organization",
    "PATENT": "asset",
    "DOCKET": "case",
    "FIPS": "place",
    "ZIP": "place",
    "LATLON": "place",
    "GEOM": "place",
    "COUNTRY": "place",
}

# Governed vocabulary for the new SPINE_ENTITY registry column (FACET_VOCAB facet
# 'SPINE_ENTITY'). Superset of SPINE_ENTITY_BY_KEY's values plus grains that have no
# single hard-ID column (payment/filing/event/aircraft) -- those are assigned from
# the registry's existing ENTITY_TYPES facet when no key-based candidate is found.
# 'company' is deliberately absent (Chris's call: collapses into 'organization').
SPINE_ENTITY_VOCAB = sorted(
    set(SPINE_ENTITY_BY_KEY.values()) | {"payment", "filing", "event", "aircraft"}
)

# STRONG-tier codes explicitly NOT eligible as spine keys (classification codes,
# not entity identifiers) -- documented here so the exclusion is visible, not just
# an absence from SPINE_ENTITY_BY_KEY.
_CLASSIFICATION_CODES = {"NAICS", "SIC", "NCES"}


def candidate_keys_for_columns(column_names: list[str]) -> list[tuple[str, str, str]]:
    """For a table's column names, return (column_name, key_label, spine_entity)
    for every column that carries a spine-eligible identifier.

    Order-preserving; a column can match at most one key (detect_key already
    picks the strongest tier per column).
    """
    hits = []
    for col in column_names:
        key, _tier = detect_key(col)
        if key and key in SPINE_ENTITY_BY_KEY:
            hits.append((col, key, SPINE_ENTITY_BY_KEY[key]))
    return hits
