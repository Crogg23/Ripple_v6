"""Every spine key column must be visible to the connection map.

The spine (entity_index_specs.DISPLAY_SPECS) pins keys to explicit columns, so
it never needs name detection. The map (fingerprint/discover) DOES: it resolves
key columns via detect_key + TABLE_COLUMN_KEYS. When a spec column's name is
one detection can't read, the spine merges on it while the map draws no edge --
the failure that left the whole 2026-08 spine batch producing ZERO connections
until 2026-08-18, and left four older columns (leadership-PAC committee ID,
NCUA merging charter, SAM exclusions UEI, SEC insider CIK) edge-less for weeks.

This test pins the invariant: adding a spec whose key_col name detection can't
resolve now fails CI with the exact TABLE_COLUMN_KEYS one-liner to add.

Local-only (no warehouse): pure vocabulary against the spec dict.
"""
from connect.entity_index_specs import DISPLAY_SPECS, table_keys
from connect.keys import TABLE_COLUMN_KEYS, detect_key


def test_every_spine_key_col_is_map_visible():
    blind = []
    for tbl, spec in DISPLAY_SPECS.items():
        for key, col in table_keys(spec):
            scoped = TABLE_COLUMN_KEYS.get((tbl, col))
            got = scoped[0] if scoped else detect_key(col)[0]
            if got != key:
                blind.append(
                    f'("{tbl}", "{col}"): ("{key}", "STEEL"),  # map sees {got}')
    assert not blind, (
        "Spine key columns the map cannot see -- add these to "
        "connect/keys.py TABLE_COLUMN_KEYS (table-scoped, so nothing else "
        "can mis-tag):\n  " + "\n  ".join(blind))
