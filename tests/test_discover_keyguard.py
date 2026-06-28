"""Offline tests for the Step-K key-config guard (connect/discover.validate_key_config).

The footgun it closes: adding a new join key takes coordinated edits across files.
Miss the KEY_DOMAIN entry and confidence() silently falls through to chance_free=0.9
(the spatial default), so the new key would pass random collisions as high-confidence
STEEL edges. The guard refuses to wire until every STEEL/STRONG value key has BOTH a
NORM_RULES entry (canonicalize) and a KEY_DOMAIN entry (collision math).
"""

import pytest

from connect import discover, keys


def test_real_config_is_complete():
    # The shipped config must pass — every current STEEL/STRONG value key is
    # fully wired. (If this fails, a key was added without finishing Step K.)
    discover.validate_key_config()


def test_missing_key_domain_is_caught(monkeypatch):
    # A new STEEL key with a NORM_RULES entry but NO KEY_DOMAIN entry: this is the
    # exact silent-0.9 footgun. The guard must raise and name the key.
    patched = dict(keys.KEY_TOKENS)
    patched["CUSIPX"] = ("STEEL", {"cusipx"})
    monkeypatch.setattr(keys, "KEY_TOKENS", patched)
    monkeypatch.setitem(keys.NORM_RULES, "CUSIPX", ("fixed", 9))   # NORM ok, DOMAIN missing
    with pytest.raises(ValueError) as exc:
        discover.validate_key_config()
    assert "CUSIPX" in str(exc.value) and "KEY_DOMAIN" in str(exc.value)


def test_missing_norm_rule_is_caught(monkeypatch):
    # A new STRONG key present in KEY_DOMAIN but with NO NORM_RULES entry would
    # raise mid-run inside normalize_sql; the guard catches it up front instead.
    patched = dict(keys.KEY_TOKENS)
    patched["FECX"] = ("STRONG", {"fecx"})
    monkeypatch.setattr(keys, "KEY_TOKENS", patched)
    monkeypatch.setitem(discover.KEY_DOMAIN, "FECX", 10**9)        # DOMAIN ok, NORM missing
    with pytest.raises(ValueError) as exc:
        discover.validate_key_config()
    assert "FECX" in str(exc.value) and "NORM_RULES" in str(exc.value)


def test_probabilistic_keys_are_exempt(monkeypatch):
    # NAME/ADDRESS (PROBABILISTIC) are scored separately and never use the value-
    # space collision model, so they're intentionally NOT required in KEY_DOMAIN.
    patched = dict(keys.KEY_TOKENS)
    patched["ALIASX"] = ("PROBABILISTIC", {"aliasx"})
    monkeypatch.setattr(keys, "KEY_TOKENS", patched)
    discover.validate_key_config()   # must not raise despite no KEY_DOMAIN entry
