# Design — The Confidence Ladder (v2)

*The unified model for how Ripple decides two records are related — from "certain, same
thing" down to "a whisper worth a look," on one scale, with nothing thrown away.*

Status: **design, hardened by adversarial review** · Date: 2026-06-25 · Scope: the
`connect/` engine (spine, resolve, leads, dossier).

> **v2 note.** v1 of this doc was put through a 6-lens adversarial review (FS math, eval
> integrity, SQL-at-scale, architecture fit, data reality, and a completeness critic). It
> found ~30 issues, a dozen of them blockers. The biggest: **the "FS scorer breaks the 0.77
> ceiling" premise was wrong** — on the one pair we can measure, the ceiling is a *data +
> blocking* problem, not a scoring-method problem, and the realistic lift is ~0.80–0.85, not
> 0.95. This version corrects the math, the SQL, the sequence, and adds the safety layer that
> v1 was missing entirely. Every §below marked **[fix]** addresses a specific finding.

---

## 0. The one-paragraph version

Every link between two records gets **one number: a match weight, measured in bits of
evidence** (Fellegi-Sunter — the math behind Splink/ICIJ/OCCRP linkage). Shared hard ID =
many bits = *certain*. A rare surname agreeing in the same place = a lot of bits =
*circumstantial but powerful*. Common name = ~nothing = *a hint*. We **keep every link at
every weight**, with its receipts, and **only ever fuse identity on a hard ID** — because a
wrong merge is the one mistake that silently poisons everything. The honest truth the review
forced into the open: **a better score alone won't break the precision ceiling on health-
provider matching — that ceiling is name-twins-in-the-same-ZIP, which only an orthogonal
feature (address, DOB) can split, and we have to confirm those features exist before we
promise any lift.** So the ladder is real and worth building across the whole Library; the
sequence is "clean the foundation and find the orthogonal signal *first*, score *second*."

---

## 1. The core principle: identity vs connection  *(survived review intact)*

| | **Identity** (a node) | **Connection** (an edge) |
|---|---|---|
| Claim | "these records *are* the same entity" | "these things are related / might be the same" |
| Built from | hard ID only (STEEL key agreement) | any evidence, at any weight |
| Cost if wrong | **poison** — every future query about the merged node lies, silently | **cheap** — a dead lead, 30 seconds lost |
| Policy | conservative; zero-false-merge by construction | keep everything, rank it, show receipts |

The architecture review **confirmed this split is airtight in the live code**: fuzzy matching
writes only `ENTITY_LINKS`; the spine's `ENTITY_ID = MD5(key_type|value)` is content-addressed
and rebuild-stable, so fuzzy literally cannot reach identity. We keep it that way.

---

## 2. The score: match weight in bits  **[fix: three-state, start term, calibration]**

For a candidate pair, compare it **field by field**. Each field votes in bits; the votes add.

**Every comparison is THREE-valued, not two** — this is the #1 FS implementation bug and v1
had it. A field is `AGREE`, `DISAGREE`, or **`NULL` (can't compare — missing on a side)**. A
NULL field contributes **exactly 0 bits**, never the disagreement weight. (LEIE often lacks a
clean street address; punishing a true pair for data we never had would silently tank recall.)

```
weight(field) =
    0                              if either side is NULL        ← can't-compare, neutral
    log2( m / u )                  if the field AGREES           ← evidence FOR
    log2( (1-m) / (1-u) )          if the field DISAGREES        ← evidence AGAINST
```

- **m** = P(agree | truly same entity) — how often this field matches for real pairs (typos
  drag it below 1).
- **u** = P(agree | NOT the same) — the **coincidence rate**. This is the whole game.

**The total**, with the prior term **always included** (v1 dropped it from every example,
which biases M upward by ~20 bits and shoves everything toward "merge"):

```
M  =  start  +  Σ_i  weight_i           start = log2( λ / (1-λ) )
```

`λ` = prior that a candidate pair matches. **Critical subtlety the review surfaced:** because
we *block* (only compare records sharing a cheap key), λ is the **within-block** match prior,
not the global one — and it's pinned in the model table, re-estimated if blocking changes. We
estimate it straight from the eval harness (`positives / candidate-pairs-within-blocks`).

**Reading M as a probability — do NOT trust the raw sigmoid. [fix: calibration]** Hand-set
m/u + correlated fields make `2^M/(1+2^M)` *decorative*: it'll print 0.99994 when the real
match rate is 0.85. The displayed confidence is the **empirical precision of the M-bin against
ground truth** (isotonic/Platt fit in `evaluate.py`), not the theoretical sigmoid. Receipts
say "observed match rate in this band," never a spuriously precise probability.

**Why weak features stack:** weights are log-likelihood ratios, so adding them multiplies the
odds. Three independent +2-bit agreements = +6 bits = 64× the odds. *No single field has to be
a smoking gun.* — **but only if the fields are independent** (next section's trap).

---

## 3. Rarity weighting — done the *right* way  **[fix: Splink additive form, don't score the blocker]**

The move that makes "a rare name match is strong evidence" rigorous. v1 did it wrong (swapped
`u → TF`, leaving the disagree branch's `u` undefined and un-implementable). The correct form
(Splink) is **additive** around a base weight:

```
base_weight   = log2( m / u_base )                      u_base = the field's AVERAGE coincidence rate (a real number in the model table)
tf_adjustment = log2( u_base / GREATEST(TF(value), floor) )
agree_weight  = base_weight + tf_adjustment             ← only on the AGREE branch
disagree_weight = log2( (1-m) / (1-u_base) )            ← uses u_base, well-defined
```

*Plain English: start from how informative this field is on average, then nudge up for a rare
value (Kowalczyk) or down for a common one (Smith). The base-u stays a real number so the
disagree branch still works.*

**Two hard rules the review demands:**

1. **Never score the blocking key. [blocker]** We block on `SOUNDEX(surname)+ZIP`. Inside a
   block, ZIP is ~constant — so "ZIP agrees" is *guaranteed for every candidate pair* and
   carries **zero** discriminating information. v1 listed ZIP as a +2-bit feature; that's
   self-fulfilling double-counting that inflates every score. **ZIP (and the surname stem) are
   blockers, not features.** The only geographic signal that *adds* information is finer than
   the block: **address-line agreement within the shared ZIP.**
2. **No single field can promote a merge. [blocker]** A capped-rare surname alone is ~13 bits —
   enough to clear a naive bar with zero corroboration. Hard policy, independent of M:
   **CONFIRMED / merge-eligible requires agreement on ≥2 independent comparison fields** (name
   AND a non-name corroborator). The TF floor is tied to corpus size (`1/N`-ish, documented),
   capping the max bits any one name can contribute *below* the merge bar by construction.

**Independence is enforced, not asserted. [fix]** Pick ONE geography term (address-within-ZIP),
not address+ZIP+place. Treat correlated fields as a single composite with a jointly-measured
`u`. Discount the name pair (surname↔first-name correlate through ethnicity). Validate the
discounts against the eval harness rather than assuming independence.

---

## 4. The ladder: rungs by *measured* precision  **[fix: empirical bands, not sigmoid]**

Rungs are cut points on M — but **labeled by observed precision against ground truth**, not by
the theoretical probability.

| Rung | Meaning | Gate |
|---|---|---|
| **CERTAIN** | same entity | shared STEEL hard ID → **merge** (the spine) |
| **CONFIRMED** | ≈ same | M high **AND ≥2 independent fields agree** AND the M-bin's measured precision ≥ target → eligible for *reviewable, reversible* promotion (never silent) |
| **STRONG** | several features corroborate | top of the leads list |
| **CIRCUMSTANTIAL** | a real lead | name + an orthogonal feature; "worth a look" |
| **HINT** | a whisper | common-name + geography; stored, shown on request |
| **(negative M)** | disagreement | used to *disprove* / disambiguate; never deleted |

Nothing below CERTAIN changes identity. The bottom rung is stored, not shown. *We avoid
"diving into shit" by never presenting a maybe as a fact — not by deleting the maybes.*

---

## 5. Reconciling with the engine you already have  **[fix: don't mutate confidence(), LADDER_RANK, normalizer, MATCH_MODEL as seed]**

- **Don't mutate `discover.confidence()` in place. [blocker]** Its `(score, keep)` sets every
  edge's confidence, the keep/drop gate, the sort order, and the `by_tier` counts that
  `build-state.md` treats as a regression baseline. Add a **parallel** `match_weight()` writing
  a **new** `match_weight`/`rung` field alongside the legacy `confidence`, behind a flag
  (`scorer='fs_v1'`). Snapshot-diff edge counts vs `connect_graph.json` before any cutover.
- **Tier vocabulary. [major]** `CORROBORATED` and `BRIDGE` have no `TIER_RANK` entry; any
  `TIER_RANK[edge_tier]` KeyErrors on ~600 edges. Define a **separate `LADDER_RANK`** covering
  all 6 legacy tiers + the rungs; never reuse the 4-tier tagger `TIER_RANK` for edges. Add an
  assertion that every emitted tier string has a rank.
- **One normalizer. [major]** The engine canonicalizes names via `keys.normalize_sql` (token-
  sorted, suffix-stripped); `resolve.py` uses a *different* raw `UPPER(TRIM)` + SOUNDEX path.
  The TF table and the comparison **must key on the same SQL expression**, or rarity attaches
  to the wrong string. Reuse `keys.normalize_sql` everywhere; add a test that the TF-key
  expression and the compare expression are byte-identical.
- **`MATCH_MODEL` is SEED data. [minor]** Load it `CREATE TABLE IF NOT EXISTS` + `MERGE` (like
  `LEADS`), **never** `CREATE OR REPLACE` — a rebuild must not wipe hand-calibrated m/u. Give
  the ladder its own versioned table (`MATCH_LINKS`), don't overload the existing
  `ENTITY_LINKS` schema.

The existing collision guard (`expected = a_distinct·b_distinct / domain`) stays as a **set-
level keep/drop pre-filter** — but it is **not** the per-pair `u` (v1 claimed it was; that's
wrong). The FS scorer computes `u` independently (`1/D` for flat IDs, per-value TF for names).

---

## 6. Receipts — auditable AND reproducible  **[fix: three-state + versioning]**

Every link carries its derivation. v1 stored the bits but not what produced them.

```json
{
  "match_weight": 11.4, "rung": "STRONG",
  "observed_precision_band": 0.83,            // measured, not a sigmoid
  "model_version": "fs_v1.2", "tf_snapshot": "nppes@sha256:e502…", "lambda": -19.8,
  "features": [
    {"field":"surname", "state":"agree",   "value":"KOWALCZYK", "tf":1.2e-5, "bits": 11.3},
    {"field":"address", "state":"agree",   "value":"…", "bits": 2.1},
    {"field":"npi",     "state":"null",    "comparable": false, "bits": 0},     // couldn't compare ≠ disagreed
    {"field":"first",   "state":"disagree","bits": -2.0}
  ]
}
```

`model_version` + `tf_snapshot` + `lambda` make a published claim **replayable** — recompute
the identical bits later, or see exactly why they changed. Without them a routine NPPES reload
silently rewrites every number you printed.

---

## 7. Implementation guardrails (the SQL traps)  **[all blocker/major from the SQL lens]**

A builder must clear every one of these or the scorer returns wrong numbers / melts the warehouse:

- **Units.** Snowflake `JAROWINKLER_SIMILARITY` returns **0–100**, not 0–1. Define `agrees :=
  JAROWINKLER(a,b)/100.0 >= AGREE_THRESHOLD` (named constant) and store the **scaled** value in
  receipts (the current code stores raw 0–100 in evidence — a bug to fix).
- **LOG / divide-by-zero.** `LOG(2, x)` errors on `x<=0`. Guard every term:
  `LOG(2, m / GREATEST(NULLIF(tf,0), floor))`, `LOG(2, GREATEST(1-m,1e-6) / GREATEST(1-u,1e-6))`.
  Constrain `MATCH_MODEL` to `0<m<1 AND 0<u<1`. (TF=0 is the *common* case — a left value absent
  from the right corpus.)
- **NULL propagation.** `M = start + w1 + w2 + …` with `+` propagates NULL → one NULL term nulls
  the whole score → the row silently fails `M >= threshold` and a real lead vanishes. Wrap every
  term: `COALESCE(w_i, 0)`. A missing field is 0 bits, never a veto.
- **Probability overflow.** `2^M/(1+2^M)` overflows for CERTAIN (~30+ bits). Use
  `1/(1+POWER(2,-M))`, and classify rungs on **M**, not on the probability.
- **Block-size cap. [blocker]** `SOUNDEX(last)+ZIP` self-joins **quadratically** — a common
  SOUNDEX in a dense ZIP = a mega-block of millions of pairs (this is already the known
  false-positive hotspot). Before the self-join, drop/flag blocks where `left_size*right_size`
  exceeds a pair budget; use a finer block key (`+first-initial` / double-metaphone). The
  `EDITDISTANCE<=3` prune runs *after* the join and does **not** bound it.
- **Scratch hygiene.** `RESOLVE_SCRATCH` is a fixed global name never dropped — two concurrent
  runs clobber each other. Use `TEMPORARY` (session-scoped, auto-drop) + a run-id suffix.
- **All-in-SQL.** Build `ENTITY_LINKS` via `INSERT … SELECT` with `OBJECT_CONSTRUCT`/`TO_JSON`
  receipts — never round-trip millions of candidate rows through pandas (`write_pandas` is for
  the tiny nickname seed only).

---

## 8. What's real on the data — the honest ceiling  **[the headline correction]**

Measured on `leie_nppes` (the one pair with ground truth), the review found the 0.77 ceiling is
**not** a weak-scorer problem:

- **ZIP is the blocker → 0 net info from geography** (§3). The only geographic lever that adds
  anything is address-line-within-ZIP.
- **The residual false positives at the tight threshold are name-twins.** At M's top end, 501 of
  ~2,130 selected pairs are *different real people with the same name in the same ZIP*
  (`BERNHARD,LAWRENCE ~ BERNHARD,LAWRENCE @ 21012`). Name/TF features are, by definition,
  powerless to split them. **Only an orthogonal feature (address, DOB, phone) can.**
- **The one named orthogonal lever — address — isn't even confirmed clean on the NPPES side**
  (the fingerprint tags zero ADDRESS/ZIP keys for NPPES; the resolver reaches a postal column by
  raw name). DOB/phone/gender are absent across all 646 tables in the fingerprint.
- **A blank-surname blocking bug is faking part of the problem.** 23.8% of NPPES rows are orgs
  with no last name; `''` passes the `IS NOT NULL` filter, `SOUNDEX('')` collapses them into one
  giant block, `JAROWINKLER('','')=100` → in the frozen fixture **1,301 of 1,500 negatives are
  blank-org-vs-blank-org garbage**. Part of "0.77" is this defect, not scoring weakness.
- **TF rarity barely bites here:** the false-positive head is common surnames (NGUYEN, SMITH,
  WILLIAMS…) where TF correctly says "worthless" — but name-JW already separated those. On the
  rare names, TF *boosts* the name-twin false pair. Net: a small mid-band gain, not a top-end
  break.

**Honest expectation:** after the blocking clean-up + an address feature (if it proves out),
precision on `leie_nppes` plausibly moves **~0.77 → ~0.80–0.85 at ~0.82 recall** — **not 0.95**.
The name-twins-in-ZIP class structurally bounds it. And **recall is capped at ~0.84 by single-
pass blocking** regardless of scorer — fixable only by *multi-pass blocking*, not by the score.

This doesn't kill the ladder — it **reframes the win.** The beast isn't "0.77→0.95 on banned
doctors." It's a **calibrated, receipt-bearing confidence ladder over the *whole* Library** —
millions of cross-domain links a human can rank and defend. The leie_nppes precision was a red
herring goal; the real value is breadth done rigorously.

**Measurement integrity rules [blockers from the eval lens]:**
- **NPI is label-only.** The scorer must **not** read NPI (or any hard ID used as ground truth)
  during eval — using "known ID disagrees" as a *feature* while NPI is the *answer key* is pure
  leakage that fakes precision toward 1.0. Hold it out; if you want a known-ID-disagree feature,
  label on one ID (NPI) and feature on a *different* one (CCN/EIN).
- **Fix the fixture.** The frozen test is 50/50 prevalence vs ~0.3% real → it reports ~0.999
  "precision" that's fiction. Freeze a **prevalence-preserving, seeded-random** sample; relabel
  the test a *rank-separation* check, not a precision check.
- **Report precision at fixed recall (or PR-AUC), with a Wilson CI lower bound**, and recommend
  an auto-merge bar only if `precision_lower_95 ≥ target AND n_in_bin ≥ ~300`. 1,983 positives
  can't certify 0.99 by a point estimate.
- **Both-NPI precision is a PROXY** for the no-NPI leads we'd actually publish — hand-label a
  sample of real leads to measure the product population.
- **Decide the grain:** the merge decision is per-*entity*, not per-pair. Report entity-grain,
  not just pair-grain, precision.

---

## 9. The safety layer — required before any publication  **[the completeness critic]**

v1 was a scoring engine with no publishing safety. This is journalism about **named real
people**; the following are blockers before a single circumstantial claim ships (and several
shape the engine even pre-publish, so the hooks go in now):

- **Suppression / retraction that survives rebuilds. [blocker]** A `SUPPRESSIONS` table keyed on
  the stable id (LEAD_ID / link-hash / entity-pair), with reason + reviewer + timestamp. Every
  publish path LEFT-ANTI-JOINs it, so a human-rejected claim can **never** be resurrected by the
  next `CREATE OR REPLACE` rebuild. Plus `STATUS` (active/retracted/corrected) and an immutable
  publish-audit log.
- **Source-trust gate on the TF corpus AND the spine. [blocker]** `u = TF(value)` and the spine
  GROUP-BY both currently read *every* source — so one junk/adversarial source poisons rarity
  weights (inject one-off fake-rare names → ~13 bits each → fake CONFIRMED links) or widens a
  real person's entity via a mistyped ID. TF + spine read only `INCLUDE='Y' AND TRUST_TIER ≥ T`;
  thin/auto-harvested sources are quarantined until reviewed; log the exact corpus snapshot.
- **Model + TF versioning** (§6) — a parameter change must not silently rewrite published
  confidences; stamp `model_version` + `tf_snapshot`, keep `MATCH_MODEL` append-versioned.
- **Fuzzy links are NOT transitive. [major]** A~B + B~C does **not** imply A~C (B may be a name-
  twin hub). Any future clustering must be a **clique** (every internal pair clears the bar),
  not connected-components, with cannot-link constraints from disagreeing hard IDs and a size
  cap. Never merge a cluster on one bridging edge.
- **Lead staleness / expiry. [major]** After each run, expire leads absent from the current
  staging set (`STATUS='stale'`, `disappeared_at`) so a person cleared by the source drops off.
  Stamp each lead with its source-snapshot date; render "as of <date>"; never publish a lead
  older than the current load without a re-verify flag.
- **Review queue as a first-class object. [major]** `review_state`/`reviewer`/`reviewed_at` on
  every publishable link; a bounded priority order (top-N by weight, novelty since LAST_SEEN);
  an explicit capacity assumption; **unreviewed = suppressed from publication, not shown as
  fact.** "Confirmed" is a recorded human act, not a score band.
- **Eval as a CI gate, not a report. [minor]** Fail the build if precision-at-fixed-recall /
  PR-AUC / the rung histogram move beyond tolerance vs the accepted baseline, after any
  `MATCH_MODEL` change or TF-touching reload.
- **Privacy note. [minor]** The inferred "who-is-secretly-whom" table is more sensitive than any
  source row (NPPES masks EIN precisely to prevent this join). Write a minimal governance note:
  retention, access tier (raw vs inferred), minimization, sensitive-category flags.

---

## 10. Build roadmap — re-sequenced  **[fix: foundation & features BEFORE the scorer]**

The review's clearest verdict: building the scorer first produces a disappointing ~0.82 and a
(correct) "can't auto-merge," risking the wrong conclusion that "FS doesn't work" when the real
gap is missing orthogonal data. So:

1. **Foundation clean-up + honest baseline.** Fix blocking (`last_n <> ''`, individual/type-1
   NPIs only for the person matcher; route orgs to an org+EIN matcher). Fix the eval harness
   (NPI held out, prevalence-correct seeded fixture, Wilson-CI + precision-at-fixed-recall,
   blocking-recall reported separately, entity-grain). **Re-baseline:** what's the *true*
   name-only precision once the blank-org garbage is gone? (Likely already > 0.77.) *Cheap,
   safe, and it sets the real starting line.*
2. **Full-column schema scan + multi-pass blocking.** Prove whether NPPES carries a clean,
   populated street address (and any DOB/phone); measure its m/u on labeled pairs. UNION several
   blocking passes to lift the ~0.84 recall ceiling.
3. **The FS scorer** — a new `match_weight()` module with the `MATCH_MODEL` seed table, TF
   tables (trust-gated, snapshot-stamped), the three-state weight SQL with all §7 guards, and
   `OBJECT_CONSTRUCT` receipts. Built only on features step 2 proved exist.
4. **Calibrate & gate** — fit M→empirical-precision, set the rung cuts, answer the auto-merge
   question with a CI, wire the eval CI gate.
5. **The safety layer** (§9) — suppression, versioning, trust-gating, review-state, staleness.
6. **Auto-spine** — widen the hard-ID spine from 10 → ~96 tables (config from fingerprint);
   ships + companies into dossiers. *Identity, widened.* Independent of 1–5; can run anytime.
7. **Land the anchors** — IRS EO BMF (EIN), SEC company facts (CIK+EIN crosswalk), SAM.gov.
8. **More lead jobs** — config on the above; each a candidate story (with §9 safety on).

---

## Appendix — starter parameters

`LIBRARY_META.CONNECT.MATCH_MODEL (field, m, u_base, tf_adjust BOOLEAN, model_version)`, seeded
from domain knowledge, **`MERGE`-loaded never replaced**, append-versioned, graduating to
EM-estimated values once labeled volume exists. `u_base` is always a real number (so the
disagree branch is defined even for TF-adjusted fields). Illustrative seeds (to be calibrated,
with `0<m<1`, `0<u_base<1` enforced):

| field | m | u_base | tf_adjust | note |
|---|---|---|---|---|
| surname (exact, normalized) | 0.92 | 0.002 | yes | base + log2(u_base/TF); ≥2-field rule caps solo merges |
| first name (nickname-aware) | 0.88 | 0.01 | yes | discount vs surname (correlated) |
| address-within-ZIP | 0.75 | 0.002 | no | **the** orthogonal lever — only if schema scan confirms it |
| ~~ZIP / place~~ | — | — | — | **blocker, not a feature — never scored** |
| known hard ID disagrees | — | — | — | hard negative; **only when BOTH sides carry the ID; held out during eval** |

Sources: Fellegi & Sunter (1969); Robin Linacre — *The mathematics of the Fellegi-Sunter model*,
*Term frequency adjustments*, *Understanding match weights* (Splink docs, UK MoJ); dedupe.io;
OCCRP Aleph. Full adversarial-review findings: workflow `harden-confidence-ladder`, 2026-06-25.

---

## Implementation notes — code vs this doc (Builds 3–6, reconciled after the commit audit)

Where the shipped code differs from the conceptual text above, the code is authoritative:

- **Rungs (§4).** `connect/calibrate.py` implements three persisted rungs — **CONFIRMED / STRONG /
  LEAD** — defined by *held-out Wilson-lower precision* bars **0.85 / 0.50 / 0.10**. These are a
  concrete, measured subset of the conceptual ladder (CERTAIN is the hard-ID spine; CIRCUMSTANTIAL/
  HINT fold into LEAD/below). The numeric bars live in code, not in the §4 table.
- **Seed vs operating model.** `match.py` carries a hand-set SEED model (illustrative, standalone
  `match`); the OPERATING model is the empirical, held-out-calibrated one `calibrate` persists to
  `MATCH_MODEL`/`MATCH_RUNGS` (content-addressed version, append-versioned). Their M-scales differ —
  don't compare match.py's M to calibrate's rung cuts.
- **Surname normalization (§5).** The surname is normalized as raw `UPPER(TRIM(...))` (NOT
  `keys.normalize_sql`) in both the TF-key (`match._build_tf`) and the compare-key (the `resolve`
  scratch `LAST_N`); they are kept byte-identical by convention so TF rarity attaches to the right
  string. The other engine paths (spine/discover/dossier) use `keys.normalize_sql`; unifying the
  surname path onto one shared helper + a byte-identical regression test is a deferred follow-up.
- **Candidate-recall ceiling.** `evaluate.py`'s reported ceiling counts true matches that survive
  the whole candidate pipeline (blocking + size-cap + EDITDISTANCE prune), not blocking alone.
