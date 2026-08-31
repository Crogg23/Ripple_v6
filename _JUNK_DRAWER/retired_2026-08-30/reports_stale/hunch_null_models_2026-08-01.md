# Hunch Engine — What "Boring" Means (null-model design note, 2026-08-01)

One page. The rule from the census stands: ONE primitive (two things joined on a
shared key), ONE score (surprise). This note defines the *dull expectation* the
score measures distance from. There is no menu of hypothesis shapes — the null
is a property of the join axis, not a question we chose.

## The one score

**Surprise = how far the observed joint sits from the dullest possible null,
in log-likelihood terms, penalized by how many looks we took.**

For every pairing the feed shows `S = log10(observed / expected-under-null)`
(clipped, signed: excess is positive, absence is negative), plus the rank's
expected-fluke count (below). Nothing is ever labeled "overlap finding" or
"divergence finding" — those are just where the number happened to come from.

## The dull expectation, per join axis

**Hard entity key (STEEL/STRONG) — null = independence over the key's honest
value space.** Expected shared entities `E = (a_distinct × b_distinct) /
KEY_DOMAIN[key]` — exactly `connect/discover.py::confidence()`'s collision
math; the engine reuses it, never re-derives it. Boring is: overlap ≈ E
(chance), or overlap ≈ 100% of the smaller side *because one table is derived
from the other* (subset/mart lineage — flagged, not scored). Surprise runs in
three directions, all the same formula:
  - overlap far above E (they share far more entities than chance allows),
  - overlap far *below* what the two sides' coverage says it should be
    (entities that ought to appear in both but don't — the "banned but still
    operating" shape lives here, as a negative-S outlier, not as a category),
  - conditional composition: within the shared entities, an attribute's joint
    distribution vs the product of the two marginals (independence). Same
    log-ratio, applied cell-wise, largest deviation reported.

**Geo key (FIPS/ZIP/COUNTRY/spatial) — null = proportional-to-marginals.**
Predicted count in place p = A's share of p × B's total (independence of
place and measure); the flattest fallback when one side has no measure is
proportional-to-population. Boring is: both datasets just retrace where people
live. Surprise = places whose observed joint deviates most from the product of
marginals — again the same signed log-ratio. Two health datasets both peaking
in populous counties: boring. A permit dataset and a violation dataset that
co-deviate in the same handful of counties *after* population is divided out:
that's a number worth a human look.

**Time (annotation, not an axis) — null = each side's own marginal trend.**
Where both sides of a pairing carry a usable time axis (SOURCE_FRESHNESS
`RECENCY_KIND`), the joint is compared against "each series follows its own
trend independently". Co-movement or a stable lag beyond that is surprise;
flat-over-time and shared seasonality are boring. Time-only pairings (no join
key) stay out of the feed — the census counted that universe (3,321) as a
blind spot, and it stays a blind spot until a join axis exists.

**PROBABILISTIC (name-only) — scored last, shown last.** The null is the same
as hard keys but over an unknowable value space, so S is capped and every row
carries the LEAD badge discipline from `viz/safety.py` (downgrade-only). 78%
of the lattice is name-only; it never outranks a hard-ID row at equal S.

## Fluke control (the make-or-break)

Two layers, both reused from the platform's existing discipline:

1. **Per-pair gate** — `discover.confidence()`'s floors (MIN_MATCH, collision
   multiple) already killed 718 flukes; the sieve applies the same gate before
   any pair is scored deeper.
2. **Family-wide control** — the census fixed the family size: 7,174 pairs
   (and known sub-comparison counts per pair). At any surprise threshold t the
   feed states the expected number of chance survivors ("at this rank,
   ~N rows would clear the bar by luck alone") — a Benjamini-Hochberg-style
   expected-false-count, shown as a number next to the rank, never hidden.
   A hunch is only promotable to the Pattern Desk when its S clears the bar
   AND the expected-fluke count at its rank is < 1.

**Trap layer:** `honesty/traps.py` flags ride every scored row (the census
already carries them); a scored deviation on a trap-flagged column is shown
with the trap text and ranked down, and the future verdict click ("artifact")
writes the trap back — the feed learns the warehouse's scar tissue.

## What the calibration must show (step 3, running now)

On ~20 hard-ID-frontier pairings: verified-real pairs should score high-S,
chance-level pairs should sit near S≈0, and known-trap pairs should be caught
by the trap layer, not by luck. If the separation isn't clean, the null (not
the data) gets redesigned before any sieve is built.

**Result (same day, see hunch_calibration_2026-08-01.md):** positive
separation clean (verified ≥ +2.7, chance ≈ 0, NPPES-EIN trap fails safe).
One refinement required before the sieve: absence-surprise must condition on
observed value-range overlap — partitioned ID spaces (CCN facility-type
ranges, per-court dockets) otherwise read as fake dramatic absence. Built as
two layers: fmt-2 range/prefix data in the fingerprint scan, plus a
bucket-histogram verification at measure time (CCN's partition hides in the
middle digits — leading prefixes are just the state and overlap fully).
