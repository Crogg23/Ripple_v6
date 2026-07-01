"""Reconciliation referees: a load does not "succeed" until its numbers tie to an
independent source.

This is the precondition that keeps a plausible-but-WRONG follow-the-money figure
from ever landing -- the publish-safety cardinal sin. It mirrors the politics phases'
penny-exact smoke tests (FEC.gov, GovTrack), made reusable: the build calls a
referee as a PRECONDITION to the atomic swap, so a load that doesn't reconcile never
goes live.

Pure `reconcile` / `penny_reconcile` (unit-tested); `fetch_referee` is the thin HTTP
helper that ABORTS on a non-200 (never reconcile against an error page).
"""
from __future__ import annotations

from dataclasses import dataclass


class SmokeFailure(AssertionError):
    """Raised when measured data does not tie to the referee -- block the swap."""


@dataclass
class SmokeResult:
    label: str
    measured: float
    expected: float
    ok: bool
    detail: str


def reconcile(measured, expected, *, label, tol_abs: float = 0.0, tol_pct: float = 0.0) -> SmokeResult:
    """Tie `measured` to `expected` within max(tol_abs, |expected|*tol_pct). Raises
    SmokeFailure if it doesn't. Use tol for definition-bound stats (votes ~0.1pp);
    use penny_reconcile for money."""
    diff = abs(measured - expected)
    allowed = max(tol_abs, abs(expected) * tol_pct)
    ok = diff <= allowed
    res = SmokeResult(label, measured, expected, ok,
                      f"|{measured} - {expected}| = {diff} {'<=' if ok else '>'} {allowed}")
    if not ok:
        raise SmokeFailure(f"[{label}] reconciliation FAILED: {res.detail}")
    return res


def penny_reconcile(measured_dollars, expected_dollars, *, label) -> SmokeResult:
    """Exact-to-the-cent match (the strongest referee). Compares integer cents to
    dodge float drift."""
    m = round(float(measured_dollars) * 100)
    e = round(float(expected_dollars) * 100)
    if m != e:
        raise SmokeFailure(
            f"[{label}] penny reconcile FAILED: {measured_dollars} != {expected_dollars} (cents {m} != {e})"
        )
    return SmokeResult(label, float(measured_dollars), float(expected_dollars), True, "exact to the cent")


def fetch_referee(url, *, params=None, headers=None, timeout=60, expect_status=200):  # pragma: no cover - live I/O
    """GET an external referee and return its JSON -- but ABORT (raise) on any non-200
    so we never reconcile a load against an error/throttle page and call it a pass."""
    import requests  # noqa: E402

    r = requests.get(url, params=params, headers=headers, timeout=timeout)
    if r.status_code != expect_status:
        raise SmokeFailure(
            f"referee {url} returned HTTP {r.status_code} (expected {expect_status}) "
            f"-- ABORT, do not reconcile against an error page"
        )
    return r.json()
