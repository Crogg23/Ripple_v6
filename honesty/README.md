# The Honesty Engine

**What it is, in bar words:** a machine that reads every mart's family tree and
stamps it `fact`, `lead`, or `unverified` — and a gate that refuses to average
a fact with a claim. No AI anywhere in the loop. No warehouse connection. It
reads one committed file (the dbt manifest) and writes two committed files
(the grades). ROADMAP_2026-07-14 §3.5, extracted from the Atlas per the
2026-07-20 sprint brief §5.2 (beta decision B9): the governance layer ships
standalone; UIs come and go on top of it.

## The three axes

**1. Provenance — machine-checked, never agent-asserted.**
`python -m honesty` walks each mart's full dbt lineage (the manifest DAG plus a
literal-FQN scan for reads that bypass `ref()`/`source()`), and grades:

| Grade | Meaning | What earns it |
|---|---|---|
| `fact` | a stranger can re-derive it from landing with hard IDs | every join in every ancestor is hard-ID-anchored (or join-free); lineage terminates in landing/seeds; no claims ancestry |
| `lead` | it carries review-gated claims | any ancestor reads the claims/review layer: `LEADS`, `V_LEADS_PUBLISHED`, `V_LATEST_DECISIONS`, `REVIEW.DECISIONS`, `LEAD_QUEUE`, or the spine claim tables (mirrors `viz/guard.py:36`) |
| `unverified` | the walker cannot vouch at all | a name-join anywhere upstream, an ON-clause it cannot read, or a model with no SQL — **all fail closed** |

The join taxonomy (the one documented judgment call, made once):
- **hard-anchored** — the clause contains ≥1 equality on a hard identifier
  (`NPI CCN UEI EIN CIK DUNS LEI IMO MMSI BIOGUIDE ICPSR` — the same key set
  the connect spine indexes). Extra name predicates on top of a hard ID only
  *restrict* the join (they can drop rows, never merge strangers), so
  `ON o.npi = l.npi AND o.lname = l.lname` stays fact-compatible.
- **name-join** — identity asserted by name-ish columns with no hard ID in the
  clause. This is how strangers get merged. → `unverified`.
- **neutral** — conformed-dimension equalities (state, year, county, codes):
  they group rows, they don't claim identity.
- **unparseable** — regex, not a SQL parser, on purpose (zero dependencies);
  anything it can't read **demotes**. Fail closed is what makes a cheap parser
  safe: the engine can under-grade, never over-grade.

Joins in disguise (added after the 2026-07-21 adversarial review, which
demonstrated each as a fail-open and is why they're now detected):
- **comma-style FROM lists** — `, LATERAL …`/`, TABLE(…)` is row expansion of
  the same row (neutral, recorded); any other bare comma-join **demotes**
  (its predicates live in WHERE and can't be bound to it).
- **WHERE-clause identity logic** — cross-alias equalities
  (`WHERE a.x = b.y` — comma-join predicates and semi-join correlations) and
  `col IN (SELECT …)` anchors are classified exactly like ON clauses: a
  name-based one merges strangers and demotes.
- **jinja inside a predicate** — an ON/USING clause assembled at parse time is
  unknowable and **demotes** (the placeholder no longer reads as a harmless
  column).
- **ID-prefixed name columns** — `NPI_NAME` is a *name* that mentions a
  register; it can never upgrade a join to hard.
- **ghost dependencies** — a `depends_on` entry the manifest can't resolve
  (disabled model, cross-project ref) is lineage the walker cannot see:
  **demotes**, never silently skipped.

**2. Weakest link + the refusal.** A measure inherits the weakest grade of
everything it touches (`honesty.effective_grade`). And the composer refuses,
at compose time, to blend fact-grade and lead-grade rows into one scalar:

```python
from honesty import MeasureInput, assert_composable, BlendRefusal

assert_composable([MeasureInput("op_payments", "fact"),
                   MeasureInput("banned_leads", "lead")])
# BlendRefusal: REFUSED: one scalar would blend fact-grade rows ... never
#               average a fact with a claim.
```

Side-by-side renders (`single_scalar=False`) pass — each input keeps its own
badge. Non-fact blends pass at the weakest grade; they never wore fact's face.

**3. Freshness/trap.** The standing POLICY data traps (`trap_ais_snapshot`,
`trap_leie_npi_and_dates`, `trap_ofac_sdn_type`, `trap_usaspending_grain`,
`trap_open_payments_split`) are mapped to their landing tables in
`honesty/traps.py` (mirrored verbatim from `scripts/build_registry_setup.py`;
a tripwire test fires if the mirror drifts). Traps do **not** change the grade
— "fact-grade but poisoned" is exactly the state they exist to name — they
attach as mandatory disclosures (`honesty.compose.disclosures`) that any
rendering surface must print with the number.

## Running it

```
cd library-onboarding/ripple_dbt && dbt parse --profiles-dir .   # refresh manifest (offline)
cd ../.. && python -m honesty                                    # grade + write artifacts
```

Outputs (commit both): `honesty/mart_grades.json` (every receipt: which
ancestor, which clause) and `honesty/MART_GRADES.md` (the human table).
Regenerate after any dbt model change — the artifacts are build-time control
files, the same doctrine as every control table in this repo.

## What it deliberately is NOT

- **Not a runtime dependency.** Nothing queries it live; surfaces read the
  committed JSON.
- **Not a badge engine.** `viz/safety.py` classifies SQL *text* today; the
  designed integration (post-sprint, when any UI work resumes) is: registry
  grade **wins** over text classification, failing closed — a text-classifier
  "clean" can never upgrade a `lead` mart, only downgrade further.
- **Not a certifier of truth.** `fact` means *mechanically re-derivable via
  hard IDs from landing* — the trust doctrine's bar for what a hostile skeptic
  can check. Whether the number MEANS anything still takes a human.

## Limitations, stated plainly

- Regex join-extraction can under-grade (e.g. an exotic clause reads as
  unparseable). By design that error direction is safe. If a mart you believe
  is fact-grade shows `unverified`, read its receipt in `mart_grades.json` —
  either the SQL deserves the demotion or the clause deserves a cleaner shape.
- **Out-of-dbt warehouse views are opaque.** The manifest DAG ends at a
  source; a source that is itself a VIEW (e.g. `V_LEADS_PUBLISHED`) hides its
  true upstreams. That one is caught because its *name* is on the claim list —
  a non-claim-named warehouse view would hide arbitrary lineage. Keep sources
  pointed at tables, or add such views to `CLAIM_SURFACES`/review by hand.
- **Macros are blanked before analysis.** Every project macro in use today is
  a pure column expression (audited 2026-07-21); a future macro containing its
  own FROM/JOIN would be invisible. Keep macros expression-only.
- Grades are as fresh as the manifest. `dbt parse` is offline and takes
  seconds; run it before regrading. The artifacts embed the manifest's own
  `generated_at` + invocation id — a diff always means models or rules
  changed, never the calendar.
- Seeds (committed CSVs) count as trusted reference data, like landing.
- `NATURAL JOIN` always demotes (implicit predicate — deliberate suspicion).
