"""Offline unit tests for the PAT-expiry additions to loadkit/preflight.py.

Everything here is pure: synthetic JWTs built in-test, fixed clocks, zero network.
These pin the Wave-7 semantics:
  - decode_jwt_exp   : payload-only base64url decode, padding restored, None on
                       anything that isn't a decodable 3-part JWT with an exp
  - pat_expiry_check : calendar gate — BLOCK <7d, WARN <21d, OK beyond; unknown
                       expiry is a WARN pointing at infra/keys_ledger.json
  - Check.warn       : new advisory state that never blocks (back-compat with
                       every existing 3-arg Check)
The existing pat_check (runtime-relative, 'will the token survive THIS load')
keeps its own tests in test_loadkit.py — these two checks answer different
questions and must never be merged.
"""
import base64
import datetime as dt
import json

from loadkit.preflight import (
    Check,
    decode_jwt_exp,
    pat_expiry_check,
    preflight,
)

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 7, 2, 12, 0, 0, tzinfo=UTC)


def _b64url(obj: dict) -> str:
    """base64url WITHOUT padding — exactly how real JWTs ship their segments."""
    raw = json.dumps(obj).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def make_jwt(claims: dict) -> str:
    header = _b64url({"alg": "RS256", "typ": "JWT"})
    payload = _b64url(claims)
    return f"{header}.{payload}.fake-signature"


# =========================================================================== #
# decode_jwt_exp — the pure offline decoder
# =========================================================================== #
def test_decode_valid_jwt_returns_utc_datetime():
    exp = dt.datetime(2026, 9, 20, 14, 58, 55, tzinfo=UTC)
    tok = make_jwt({"sub": "CROGG23", "exp": int(exp.timestamp())})
    got = decode_jwt_exp(tok)
    assert got == exp
    assert got.tzinfo is not None   # always aware, never naive


def test_decode_handles_all_padding_lengths():
    # base64url padding depends on payload byte length mod 4 — sweep claim sizes
    # so every pad case (0, 1, 2 '=' chars) gets exercised.
    exp = int(dt.datetime(2027, 1, 1, tzinfo=UTC).timestamp())
    for filler in ("", "x", "xx", "xxx", "xxxx"):
        tok = make_jwt({"exp": exp, "f": filler})
        assert decode_jwt_exp(tok) is not None, f"pad case failed for filler={filler!r}"


def test_decode_jwt_without_exp_is_none():
    assert decode_jwt_exp(make_jwt({"sub": "nobody"})) is None


def test_decode_non_jwt_shapes_are_none():
    assert decode_jwt_exp(None) is None
    assert decode_jwt_exp("") is None
    assert decode_jwt_exp("just-an-opaque-api-key") is None
    assert decode_jwt_exp("two.parts") is None
    assert decode_jwt_exp("a.b.c.d") is None          # four parts is not a JWT
    assert decode_jwt_exp(12345) is None              # not even a string


def test_decode_garbage_payload_is_none_not_raise():
    # Structurally 3 parts but the middle is not base64/JSON — must swallow, not raise.
    assert decode_jwt_exp("aGVhZGVy.!!!not-base64!!!.c2ln") is None
    not_json = base64.urlsafe_b64encode(b"plain text").decode().rstrip("=")
    assert decode_jwt_exp(f"aGVhZGVy.{not_json}.c2ln") is None


# =========================================================================== #
# pat_expiry_check — the calendar gate (BLOCK <7d, WARN <21d, OK beyond)
# =========================================================================== #
def test_expiry_far_out_is_ok():
    c = pat_expiry_check(NOW + dt.timedelta(days=60), NOW)
    assert c.ok and not c.warn
    assert c.name == "pat_expiry"


def test_expiry_inside_warn_window_warns_but_runs():
    c = pat_expiry_check(NOW + dt.timedelta(days=10), NOW)
    assert c.ok and c.warn
    assert "keys_ledger" in c.detail   # the WARN must say where to act


def test_expiry_inside_block_window_blocks():
    c = pat_expiry_check(NOW + dt.timedelta(days=3), NOW)
    assert not c.ok
    assert "rotate" in c.detail.lower()


def test_expired_token_blocks():
    c = pat_expiry_check(NOW - dt.timedelta(days=1), NOW)
    assert not c.ok


def test_boundaries_just_inside_and_outside():
    # 7d floor: a minute PAST 7 days -> WARN (not block); a minute UNDER -> BLOCK.
    assert pat_expiry_check(NOW + dt.timedelta(days=7, minutes=1), NOW).ok
    assert not pat_expiry_check(NOW + dt.timedelta(days=7) - dt.timedelta(minutes=1), NOW).ok
    # 21d line: just past -> clean OK, just under -> WARN.
    assert not pat_expiry_check(NOW + dt.timedelta(days=21, minutes=1), NOW).warn
    assert pat_expiry_check(NOW + dt.timedelta(days=21) - dt.timedelta(minutes=1), NOW).warn


def test_unknown_expiry_is_warn_pointing_at_ledger_not_block():
    # Opaque (non-JWT) credentials are common and valid — unknown must not block,
    # but it must tell the operator where the truth is supposed to live.
    c = pat_expiry_check(None, NOW)
    assert c.ok and c.warn
    assert "keys_ledger" in c.detail


def test_naive_datetimes_are_tolerated():
    naive_now = dt.datetime(2026, 7, 2, 12, 0, 0)
    naive_exp = dt.datetime(2026, 9, 1, 0, 0, 0)
    c = pat_expiry_check(naive_exp, naive_now)
    assert c.ok and not c.warn


def test_custom_thresholds():
    c = pat_expiry_check(NOW + dt.timedelta(days=10), NOW, block_days=14, warn_days=30)
    assert not c.ok   # 10d < a 14d floor


# =========================================================================== #
# Check.warn — advisory state, backward compatible, never blocks
# =========================================================================== #
def test_check_three_arg_construction_still_works():
    c = Check("legacy", True, "old callers pass three positionals")
    assert c.warn is False


def test_warn_never_blocks_a_report():
    rep = preflight(
        Check("a", True, "fine"),
        pat_expiry_check(NOW + dt.timedelta(days=10), NOW),   # WARN
    )
    assert rep.ok
    rep.raise_if_blocked()   # must NOT raise on a warn


def test_summary_shows_warn_and_keeps_old_tags():
    rep = preflight(
        Check("clean", True, "d1"),
        Check("bad", False, "d2"),
        pat_expiry_check(NOW + dt.timedelta(days=10), NOW),
    )
    s = rep.summary()
    assert "[OK ] clean" in s        # exact legacy tag preserved
    assert "[BLOCK] bad" in s        # exact legacy tag preserved
    assert "[WARN ] pat_expiry" in s


# =========================================================================== #
# round trip: a synthetic "Snowflake PAT" through decode -> gate
# =========================================================================== #
def test_round_trip_synthetic_pat():
    exp = NOW + dt.timedelta(days=80)
    tok = make_jwt({"iss": "snowflake", "exp": int(exp.timestamp())})
    decoded = decode_jwt_exp(tok)
    c = pat_expiry_check(decoded, NOW)
    assert c.ok and not c.warn
    # and the check output never leaks anything token-shaped
    assert tok.split(".")[1] not in c.detail
