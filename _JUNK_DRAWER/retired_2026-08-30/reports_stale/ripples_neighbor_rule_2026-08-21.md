# The generalized neighbor-spike rule — run across 3 domains, 2026-08-21

**What this is:** yesterday's nursing-home pilot, turned into one reusable rule
and pointed at every domain the 2026-08-21 survey found a real (noun, same-owner
neighbor key, bad-event) triple in. Script: `scripts/ripples/neighbor_spike_rule.py`,
configs: `scripts/ripples/domain_configs.py`, raw output:
`reports/ripples_neighbor_rule_2026-08-21.json`.

**The question, same in all three:** when one thing's bad-event count spikes in
a quarter, do its same-owner siblings also spike nearby in time — more than an
unrelated control group would by pure chance?

**What changed from yesterday's version, and why it matters:** yesterday
compared against ONE arbitrary control draw. This version redraws the control
group 20 times and reports the spread, not a single number — a real
random-world null check (docs/RIPPLES.md landmine 2 says this is
non-negotiable, not optional rigor). A gap that only shows up against one lucky
draw would not survive this; all three below do.

---

## Results

| Domain | Noun | Neighbor key | Same-owner co-spike | Control (20-draw avg) | Gap | Spikes tested |
|---|---|---|---:|---:|---:|---:|
| **Health** — nursing homes | facility (CCN) | ownership chain | 76.8% | 63.5% ± 0.6% | **+13.3%** | 2,524 |
| **Labor** — mine safety | mine | parent controller company | 52.1% | 17.7% ± 0.4% | **+34.3%** | 4,776 |
| **Environment** — toxic release sites | facility (FRS ID) | parent company | 17.9% | 6.2% ± 0.6% | **+11.8%** | 764 |

All three gaps are far larger than the 20-draw control spread itself (the
"z vs. redraw spread" column in the raw output, 18.7 to 95.8) — this isn't one
lucky comparison, the same-owner rate is consistently and repeatably higher
than chance in every domain tested.

**Mine safety is the strongest signal by a wide margin.** A same-owner mine is
nearly 3x as likely to also spike in violations as an unrelated mine would be
by chance (52.1% vs. 17.7%) — a much bigger gap than nursing homes or toxic
release sites. Worth noting this domain also had, by far, the strongest and
most independently cross-verified neighbor key of the three (see the survey
notes) — that may be part of why the signal reads cleaner here, not just that
the underlying behavior is stronger.

---

## The honest caveat, and it applies to all three, not just health

Yesterday's writeup flagged that nursing-home co-spikes might be a state
inspector's calendar, not the owner's management — sister facilities in the
same state get visited close together regardless of ownership. **The same
structural risk exists in mine safety (regional MSHA district offices covering
multiple mines) and toxic-release enforcement (EPA regional offices, and
multi-site settlements that are legitimately one enforcement action touching
several facilities of one company at once — which is a different kind of
"real" than what this rule is trying to measure).**

This rule cannot yet tell "the owner is doing something" apart from "the
inspector's/regulator's own schedule or process created the appearance of
togetherness." None of these three numbers should be read as a finding. They
are all evidence the *mechanism* works — real neighbor keys, real events, a
real and repeatable gap over a proper null check — not evidence of *what
causes* the gap.

**What would actually distinguish them:** a same-region control (compare
same-owner co-spikes against a control group matched on the SAME state/MSHA
district/EPA region, not just matched on size) — the same fix yesterday's
report proposed for health, now clearly needed for all three.

---

## What this proves about the rules layer itself

The mechanics generalize. Three different domains, three different kinds of
noun (a facility, a mine, a release site), three independently-verified
neighbor keys, one unmodified script — all three produced a real, repeatable,
above-chance gap. That is the piece 5 promise from docs/RIPPLES.md working as
described: a dumb question, asked the same way of different things, drawing
out a pattern nobody typed into any single table.

Justice was surveyed and dropped — court filings aren't a "bad event," they're
caseload, and no real substitute (a misconduct/reversal signal tied to a judge)
exists in the data today.
