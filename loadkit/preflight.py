"""Pre-flight gates: refuse to START a load that would fail mid-stream.

The stress-test's #1 blocker: the Snowflake PAT expires 2026-07-05, and a token
death mid-load can't even write the 'failed' marker (the except-block needs a live
connection), leaving a half-table the next run silently overwrites. The cure is to
never START a load whose worst-case runtime crosses the token's life -- fail FAST,
not half-way. Same idea for budget headroom and API-key expiry.

The DECISION logic here is pure (no I/O) so it is unit-tested. The thin live readers
(`live_pat_expiry` / `live_budget_credits`) wrap the real Snowflake/SHOW calls and
are kept out of the unit tests.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass


class PreflightError(RuntimeError):
    """Raised by PreflightReport.raise_if_blocked when any gate fails."""


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


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
        return "\n".join(f"  [{'OK ' if c.ok else 'BLOCK'}] {c.name}: {c.detail}" for c in self.checks)


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
