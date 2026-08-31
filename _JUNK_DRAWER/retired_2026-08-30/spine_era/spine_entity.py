"""Key-type -> spine_entity mapping for the registry-driven staging generator.

DERIVES from entity_index_specs.ENTITY_TYPE_BY_KEY, which is the single source of
truth that connect/spine.py and connect/incremental.py also generate their
``CASE key_type ...`` expression from. So a source classified here always resolves
to the SAME entity type the spine writes into ``LIBRARY_META.CONNECT.ENTITY_MAP``,
by construction rather than by hand-syncing. Extended below with the grains
connect/ doesn't resolve to a hard ID yet (place, case, asset).

Chris's Step-1 taxonomy call (2026-07-05):
  - company collapses into organization (matches connect/'s catch-all; avoids a
    third taxonomy fork alongside connect/'s resolver and the registry's
    ENTITY_TYPES facet, which does keep company distinct for its own purposes).
  - place is included now as a label even though connect/ has no place resolver
    (FIPS/ZIP/GEOM are join-key tiers there, not ENTITY_MAP entries) -- makes the
    61-source gap visible instead of hiding it.
  - PATENT is classified 'asset' here. connect/spine.py's catch-all ELSE would
    call it 'organization' -- a deliberate, documented divergence, not a drift.

2026-07-30: before this date the mapping was hand-copied into FOUR files, each
carrying a comment asking the next reader to keep them in lockstep manually. A
drift across those sites silently re-types entities on an incremental MERGE. The
copies are gone; only the additive grains below are hand-written.

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

from entity_index_specs import ENTITY_TYPE_BY_KEY  # noqa: E402
from keys import ENTITY_KEYS, detect_key  # noqa: E402  (connect/keys.py)

# key_label -> spine_entity. DERIVED from entity_index_specs.ENTITY_TYPE_BY_KEY (the
# single source of truth that spine.py and incremental.py also generate their CASE
# expression from), then extended with the grains connect/ doesn't resolve to a hard
# ID yet (place, case, asset).
#
# 2026-07-30: this dict used to be a hand-maintained COPY of that mapping, with a
# docstring asking the reader to keep it in sync by hand. It's now computed, so the
# 'place'/'asset'/'case' additions below are the only hand-written part -- and adding
# a key axis in ENTITY_TYPE_BY_KEY automatically lands here too.
#
# A key absent here is not spine-eligible. NAICS/SIC/NCES are STRONG-tier in the
# tagger but are CLASSIFICATION codes, not entity IDs (many organizations share one
# NAICS code) -- deliberately excluded. So are NAME/ADDRESS: never a reliable unique
# natural key on their own.
SPINE_ENTITY_BY_KEY: dict[str, str] = {
    **ENTITY_TYPE_BY_KEY,
    # Grains connect/spine.py has no hard-ID resolver for. PATENT is 'asset' here
    # where spine.py's ELSE would call it 'organization' -- a deliberate divergence,
    # documented in this module's docstring.
    "PATENT": "asset",
    "DOCKET": "case",
    # place: included as a label even though connect/ has no place resolver
    # (FIPS/ZIP/GEOM are join-key tiers there, not ENTITY_MAP entries) -- makes the
    # 61-source gap visible instead of hiding it.
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
