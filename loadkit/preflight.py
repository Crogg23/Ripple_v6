"""Pre-flight gates: refuse to START a load that would fail mid-stream.

The stress-test's #1 blocker: the Snowflake PAT expires (currently 2026-09-20, per
infra/keys_ledger.json), and a token
death mid-load can't even write the 'failed' marker (the except-block needs a live
connection), leaving a half-table the next run silently overwrites. The cure is to
never START a load whose worst-case runtime crosses the token's life -- fail FAST,
not half-way. Same idea for budget headroom and API-key expiry.

The DECISION logic here is pure (no I/O) so it is unit-tested. The thin live readers
(`live_pat_expiry` / `live_budget_credits`) wrap the real Snowflake/SHOW calls and
are kept out of the unit tests.
"""
from __future__ import annotations

import base64 as _b64
import datetime as _dt
import json as _json
import os as _os
from dataclasses import dataclass


class PreflightError(RuntimeError):
    """Raised by PreflightReport.raise_if_blocked when any gate fails."""


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    # WARN is advisory: the load still runs (ok=True) but the operator should act soon.
    # Optional with a default so every existing 3-arg Check(...) call keeps working.
    warn: bool = False


@dataclass
class PreflightReport:
    checks: list

    @property
    def ok(self) -> bool:
        return all(c.ok for c in self.checks)

    def raise_if_blocked(self) -> "PreflightReport":
        if not self.ok:
            fails = "\n".join(f"  [BLOCKED] {c.name}: {c.detail}" for c in self.checks if not c.ok)
            raise PreflightError("Pre-flight blocked the load:\n" + fails)
        return self

    def summary(self) -> str:
        # Tag widths match the original two-state format exactly ('OK ' / 'BLOCK')
        # so nothing parsing the old summary breaks; WARN is the only new tag.
        def _tag(c: Check) -> str:
            if not c.ok:
                return "BLOCK"
            return "WARN " if getattr(c, "warn", False) else "OK "
        return "\n".join(f"  [{_tag(c)}] {c.name}: {c.detail}" for c in self.checks)


def pat_check(expiry, now, est_hours, *, safety_factor: float = 2.0, min_buffer_hours: float = 24.0) -> Check:
    """Block unless the token (worst-case = est_hours * safety_factor) finishes with
    >= min_buffer_hours of token life to spare. Unknown expiry is a BLOCK, not a pass."""
    if expiry is None:
        return Check("pat", False, "token expiry unknown -- cannot guarantee it survives the load")
    finish = now + _dt.timedelta(hours=est_hours * safety_factor)
    deadline = expiry - _dt.timedelta(hours=min_buffer_hours)
    if finish >= deadline:
        return Check(
            "pat", False,
            f"token expires {expiry:%Y-%m-%d %H:%M}; worst-case finish {finish:%Y-%m-%d %H:%M} "
            f"(+{min_buffer_hours:.0f}h buffer) crosses it -- rotate the PAT first",
        )
    return Check("pat", True, f"token good to {expiry:%Y-%m-%d}; worst-case finish {finish:%Y-%m-%d %H:%M}")


def budget_check(quota_credits, used_credits, est_credits, *, suspend_pct: float = 0.90) -> Check:
    """Block if landing est_credits would cross the resource-monitor SUSPEND line
    (mid-write suspends abort the COPY across ALL warehouses)."""
    if quota_credits is None or used_credits is None:
        return Check("budget", False, "budget headroom unknown -- read SHOW RESOURCE MONITORS first")
    ceiling = quota_credits * suspend_pct
    projected = used_credits + est_credits
    if projected >= ceiling:
        return Check(
            "budget", False,
            f"projected {projected:.2f}cr >= suspend ceiling {ceiling:.2f}cr "
            f"({suspend_pct:.0%} of {quota_credits}cr) -- raise the quota or wait for reset",
        )
    return Check("budget", True, f"projected {projected:.2f}cr < ceiling {ceiling:.2f}cr (headroom {ceiling - projected:.2f})")


def key_check(name, expiry, now, *, min_buffer_hours: float = 48.0) -> Check:
    """Block if an API key (SAM_API_KEY, OpenFEC, data.gov) expires within the buffer."""
    if expiry is None:
        return Check(f"key:{name}", True, "no expiry tracked (assumed ok) -- set one to be safe")
    if now >= (expiry - _dt.timedelta(hours=min_buffer_hours)):
        return Check(f"key:{name}", False, f"{name} expires {expiry:%Y-%m-%d}; within {min_buffer_hours:.0f}h -- rotate")
    return Check(f"key:{name}", True, f"{name} good to {expiry:%Y-%m-%d}")


def decode_jwt_exp(token):
    """Decode the `exp` claim from a JWT-shaped token, entirely offline.

    The Snowflake PAT is a JWT: header.payload.signature, each part base64url.
    We split, pad, and decode ONLY the payload — no network, no verification
    (we want the expiry date, not proof of authenticity). Returns an aware UTC
    datetime, or None when the token isn't a decodable JWT / has no exp.

    NEVER log or return the token itself — the caller may hand us a live
    credential and the whole point is that it stays out of logs."""
    if not token or not isinstance(token, str):
        return None
    parts = token.split(".")
    if len(parts) != 3:
        return None
    payload = parts[1]
    try:
        # base64url needs its padding restored — JWTs strip the trailing '='.
        padded = payload + "=" * (-len(payload) % 4)
        claims = _json.loads(_b64.urlsafe_b64decode(padded.encode("ascii")))
        exp = claims.get("exp")
        if exp is None:
            return None
        return _dt.datetime.fromtimestamp(float(exp), tz=_dt.timezone.utc)
    except Exception:
        return None


def pat_expiry_check(exp, now, *, block_days: float = 7.0, warn_days: float = 21.0) -> Check:
    """Calendar-distance gate on the PAT's decoded expiry: BLOCK under block_days,
    WARN under warn_days, OK otherwise. Unknown expiry (non-JWT token, opaque
    secret) is a WARN — not a BLOCK — pointing at the ledger, because plenty of
    valid credentials simply aren't JWTs and we can't decode what isn't there.

    This is deliberately SEPARATE from pat_check above: pat_check answers 'will
    the token survive THIS load' (runtime-relative); this answers 'is the token
    about to die on the calendar' (load-independent). Different questions,
    different semantics — do not merge them."""
    if now.tzinfo is None:
        now = now.replace(tzinfo=_dt.timezone.utc)
    if exp is None:
        return Check("pat_expiry", True,
                     "PAT expiry unknown (not a decodable JWT) — check infra/keys_ledger.json "
                     "and record it there", warn=True)
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=_dt.timezone.utc)
    days_left = (exp - now).total_seconds() / 86400.0
    if days_left < block_days:
        return Check("pat_expiry", False,
                     f"PAT expires {exp:%Y-%m-%d} ({days_left:.1f}d away, under the "
                     f"{block_days:.0f}d floor) — rotate NOW, then update infra/keys_ledger.json")
    if days_left < warn_days:
        return Check("pat_expiry", True,
                     f"PAT expires {exp:%Y-%m-%d} ({days_left:.1f}d away) — rotate soon "
                     f"and update infra/keys_ledger.json", warn=True)
    return Check("pat_expiry", True, f"PAT good to {exp:%Y-%m-%d} ({days_left:.0f}d of life left)")


def dep_check(name, present, *, detail: str = "") -> Check:
    """A required upstream object exists (e.g. the committee master for conduit
    resolution, the ccl linkage for itcont->candidate)."""
    return Check(f"dep:{name}", bool(present), detail or ("present" if present else "MISSING -- load it first"))


def preflight(*checks) -> PreflightReport:
    return PreflightReport(list(checks))


# --------------------------------------------------------------------------- #
# Thin live readers (not unit-tested -- they touch Snowflake). The build tasks
# call these to feed real values into the pure checks above.
# --------------------------------------------------------------------------- #
def live_pat_expiry():  # pragma: no cover
    """Decoded expiry of the live Snowflake PAT, or None. Zero-network: the PAT is
    a JWT, so its exp claim decodes locally. Reads SNOWFLAKE_PAT from the process
    env first (a loaded .env puts it there), then falls back to the onboarding
    settings object when importable. The token itself never leaves this frame."""
    token = _os.getenv("SNOWFLAKE_PAT", "").strip()
    if not token:
        try:
            import sys
            from pathlib import Path
            lib = Path(__file__).resolve().parents[1] / "library-onboarding"
            if str(lib) not in sys.path:
                sys.path.insert(0, str(lib))
            from config import settings
            token = (settings.snowflake_pat or "").strip()
        except Exception:
            return None
    return decode_jwt_exp(token)


def live_budget_credits(conn, monitor: str = "RIPPLE_BUDGET"):  # pragma: no cover
    """Return (quota_credits, used_credits) from SHOW RESOURCE MONITORS, or (None, None)."""
    cur = conn.cursor()
    try:
        cur.execute("SHOW RESOURCE MONITORS")
        cols = [c[0].lower() for c in cur.description]
        for row in cur.fetchall():
            r = dict(zip(cols, row))
            if str(r.get("name", "")).upper() == monitor.upper():
                quota = float(r.get("credit_quota") or 0) or None
                used = float(r.get("used_credits") or 0)
                return quota, used
        return None, None
    finally:
        cur.close()
