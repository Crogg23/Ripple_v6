"""The generalized Ripples neighbor-spike rule.

WHAT THIS IS
------------
The 2026-08-21 pilot (reports/ripples_functional_check_2026-08-21.md) proved out
one hand-built version of this on nursing homes: pick a NOUN with a real id, a
NEIGHBOR KEY that groups nouns under one real owner, and a countable BAD EVENT.
Ask: when one noun's bad-event rate spikes, do its same-owner neighbors also
spike nearby in time -- more than an unrelated control group would by chance?

This generalizes that into one script, parameterized per domain, so the same
rule runs against any (noun, neighbor key, bad event) triple without being
hand-rewritten each time. This is Ripple piece 5 (docs/RIPPLES.md) -- "a
question asked of every thing and its neighbors" -- taking its first repeatable
shape.

METHOD (a real change from the pilot, not just a copy)
--------------------------------------------------------
The pilot compared against ONE arbitrary control draw. Landmine 2 in
docs/RIPPLES.md is explicit that a boring-random-world null check is
non-negotiable, so this version draws the control group N_DRAWS times and
reports a distribution, not a single number -- the same discipline as a
permutation test. A gap that only shows up against one lucky/unlucky draw is
not a finding.

Ticks are calendar quarters per noun (not per-visit, which the pilot used but
which doesn't generalize across domains with different inspection cadences).
A spike is a quarter whose event count is in the top SPIKE_PCTILE of all
active noun-quarters in that domain AND at least SPIKE_MULTIPLE times the
noun's own median active-quarter count -- same two-part test the pilot
tightened to after its first "wash by construction" attempt, still applied
here so the same discipline carries over.

Reads Snowflake (read-only, small aggregate queries only -- no full-table
pulls, no writes). Prints a report; does not publish anything (CLAUDE.md
section 7: human sign-off on every finding, no exceptions -- this is a
measurement, not a claim).
"""
import argparse
import json
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _snowflake_conn import connect  # noqa: E402

SPIKE_PCTILE = 95       # a spike is a top-5% active-quarter count for that noun
SPIKE_MULTIPLE = 3.0    # AND at least 3x the noun's own median active quarter
WINDOW_QUARTERS = 1     # "nearby in time" = same quarter or one quarter either side
N_DRAWS = 20            # control-group redraws, for a real null distribution
MIN_ACTIVE_QUARTERS = 2  # a noun needs at least 2 active quarters to have a "spike"
SEED = 20260821


def load_events(conn, sql, label):
    """(noun_id, neighbor_key, event_date) -> aggregated (noun_id, neighbor_key,
    quarter) -> count. Aggregation happens in Snowflake; only the small
    per-noun-per-quarter result comes back to Python."""
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    print(f"  [{label}] {len(rows):,} noun-quarter rows pulled")
    return rows


def build_frame(rows):
    """rows: (noun_id, neighbor_key, quarter, n_events, state) -> dicts."""
    by_noun = defaultdict(dict)          # noun_id -> {quarter: count}
    neighbor_of = {}                     # noun_id -> neighbor_key
    state_of = {}                        # noun_id -> state
    for noun_id, neighbor_key, quarter, n, state in rows:
        by_noun[noun_id][quarter] = int(n)
        neighbor_of[noun_id] = neighbor_key
        state_of[noun_id] = state
    return by_noun, neighbor_of, state_of


def find_spikes(by_noun):
    """A spike: quarter count in this noun's own top-5th-percentile AND >= 3x
    the noun's median active-quarter count. Returns [(noun_id, quarter, count)]."""
    all_counts = [c for counts in by_noun.values() for c in counts.values()]
    if not all_counts:
        return [], 0
    global_p95 = np.percentile(all_counts, SPIKE_PCTILE)
    spikes = []
    for noun_id, counts in by_noun.items():
        if len(counts) < MIN_ACTIVE_QUARTERS:
            continue
        vals = list(counts.values())
        median = np.median(vals)
        if median <= 0:
            continue
        for q, c in counts.items():
            if c >= global_p95 and c >= SPIKE_MULTIPLE * median:
                spikes.append((noun_id, q, c))
    return spikes, global_p95


def quarter_index(q):
    """'2023Q1' -> 8093 (sortable integer: year*4 + quarter)."""
    y, qn = int(q[:4]), int(q[5])
    return y * 4 + qn


def has_nearby_spike(target_noun, target_q, candidate_nouns, spike_lookup):
    """Did ANY of candidate_nouns also spike within WINDOW_QUARTERS of target_q?"""
    tq = quarter_index(target_q)
    for cand in candidate_nouns:
        if cand == target_noun:
            continue
        for q in spike_lookup.get(cand, ()):
            if abs(quarter_index(q) - tq) <= WINDOW_QUARTERS:
                return True
    return False


def run_domain(cfg, conn):
    print(f"\n=== {cfg['name']} ===")
    rows = load_events(conn, cfg["sql"], cfg["name"])
    by_noun, neighbor_of, state_of = build_frame(rows)
    n_nouns = len(by_noun)
    n_groups = len(set(neighbor_of.values()))
    print(f"  {n_nouns:,} nouns, {n_groups:,} neighbor groups")

    spikes, threshold = find_spikes(by_noun)
    if not spikes:
        print("  No spikes found at this threshold -- domain has too little "
              "quarter-over-quarter variance to test. Skipping.")
        return None
    print(f"  spike threshold: count >= {threshold:.1f} (p95) AND >= "
          f"{SPIKE_MULTIPLE}x the noun's own median active quarter")
    print(f"  {len(spikes):,} spikes found across {n_nouns:,} nouns")

    spike_lookup = defaultdict(set)
    for noun_id, q, c in spikes:
        spike_lookup[noun_id].add(q)

    group_members = defaultdict(list)
    for noun_id, key in neighbor_of.items():
        group_members[key].append(noun_id)
    # only groups with >1 member can have a "sibling" at all
    multi_groups = {k: v for k, v in group_members.items() if len(v) > 1}
    testable_spikes = [(n, q, c) for n, q, c in spikes
                        if neighbor_of.get(n) in multi_groups]
    print(f"  {len(testable_spikes):,} of those spikes are at nouns with at "
          f"least one same-owner sibling (the only ones this rule can test)")
    if not testable_spikes:
        print("  No testable spikes -- every spiking noun is a singleton "
              "owner. Skipping.")
        return None

    same_owner_hits = 0
    for noun_id, q, c in testable_spikes:
        siblings = [m for m in multi_groups[neighbor_of[noun_id]] if m != noun_id]
        if has_nearby_spike(noun_id, q, siblings, spike_lookup):
            same_owner_hits += 1
    same_owner_rate = same_owner_hits / len(testable_spikes)

    rng = np.random.default_rng(SEED)
    all_noun_ids = list(by_noun.keys())
    by_state = defaultdict(list)
    for n in all_noun_ids:
        by_state[state_of.get(n)].append(n)

    def draw_rates(pool_for):
        rates = []
        for draw in range(N_DRAWS):
            hits = 0
            for noun_id, q, c in testable_spikes:
                group_size = len(multi_groups[neighbor_of[noun_id]])
                pool = [n for n in pool_for(noun_id) if n != noun_id]
                if not pool:
                    continue
                control = rng.choice(pool, size=min(group_size - 1, len(pool)),
                                      replace=False)
                if has_nearby_spike(noun_id, q, control, spike_lookup):
                    hits += 1
            rates.append(hits / len(testable_spikes))
        return np.array(rates)

    # control 1: strangers from anywhere (the original null)
    control_rates = draw_rates(lambda n: all_noun_ids)
    # control 2: strangers from the SAME STATE -- if the same-owner gap
    # survives this, the co-spiking is not the state inspector's shared
    # calendar (the honest caveat all three 2026-08-21 results carried)
    same_state_rates = draw_rates(lambda n: by_state.get(state_of.get(n), []))

    gap = same_owner_rate - control_rates.mean()
    gap_same_state = same_owner_rate - same_state_rates.mean()
    # a crude z-score against the draw-to-draw spread, not a formal test --
    # enough to say "is this bigger than the redraws' own noise"
    z = gap / control_rates.std() if control_rates.std() > 0 else float("inf")

    print(f"\n  SAME-OWNER co-spike rate:  {same_owner_rate:.1%} "
          f"({same_owner_hits}/{len(testable_spikes)})")
    print(f"  CONTROL co-spike rate:     {control_rates.mean():.1%} "
          f"+/- {control_rates.std():.1%}  ({N_DRAWS} redraws, "
          f"range {control_rates.min():.1%}-{control_rates.max():.1%})")
    print(f"  SAME-STATE control rate:   {same_state_rates.mean():.1%} "
          f"+/- {same_state_rates.std():.1%}")
    print(f"  GAP vs anywhere: {gap:+.1%}  (z vs. redraw spread: {z:.1f})")
    zs = (gap_same_state / same_state_rates.std()
          if same_state_rates.std() > 0 else float("inf"))
    print(f"  GAP vs same-state: {gap_same_state:+.1%}  (z: {zs:.1f})")

    return {
        "domain": cfg["name"], "n_nouns": n_nouns, "n_groups": n_groups,
        "n_spikes": len(spikes), "n_testable_spikes": len(testable_spikes),
        "same_owner_rate": same_owner_rate, "same_owner_hits": same_owner_hits,
        "control_rate_mean": float(control_rates.mean()),
        "control_rate_std": float(control_rates.std()),
        "control_rate_min": float(control_rates.min()),
        "control_rate_max": float(control_rates.max()),
        "gap": gap, "z_vs_redraw_spread": float(z),
        "same_state_control_mean": float(same_state_rates.mean()),
        "same_state_control_std": float(same_state_rates.std()),
        "gap_vs_same_state": gap_same_state,
        "z_vs_same_state_spread": float(zs),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="write JSON results here")
    args = ap.parse_args()

    from domain_configs import DOMAINS  # noqa: E402

    conn = connect(database="LIBRARY_MARTS")
    results = []
    for cfg in DOMAINS:
        r = run_domain(cfg, conn)
        if r:
            results.append(r)
    conn.close()

    print("\n=== SUMMARY ===")
    for r in results:
        print(f"  {r['domain']:20s} same-owner {r['same_owner_rate']:5.1%}  "
              f"vs control {r['control_rate_mean']:5.1%}  "
              f"gap {r['gap']:+5.1%}  z {r['z_vs_redraw_spread']:+.1f}")

    if args.out:
        with open(args.out, "w") as fh:
            json.dump(results, fh, indent=2, default=str)
        print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
