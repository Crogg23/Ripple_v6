# Full Repo Audit — 2026-08-12

Context: Chris wants to pivot analysis to a top-down flow (high-level overview →
drill to granular), replacing the flat 2,873-row viz-idea CSV
(`reports/viz_brainstorm_2026-08-10.csv`) as the entry point. Three parallel
audit agents swept structure/pipeline, analysis/viz tooling, and data
coverage/trust. Filesystem + git only; no warehouse queries.

---

## 1. Structure & pipeline

**Core active dirs (commits within ~4 days):**
- `library-onboarding/` — onboarding agent + the dbt project (3,537 files; the heart).
- `library-onboarding/ripple_dbt/` — 1,808 model SQL + 1,681 yml. Layers:
  staging 1,172 (views, ~1,140 one-folder-per-source), marts 622 (tables,
  ~25 domains: health 191, environment 151, finance 124, justice 111, …),
  intermediate essentially unused (4). Only 15 macro/seed/test files for 1,800
  models. `dbt_project.yml` carries a long tail of per-model enable overrides.
- `scripts/` — 213 flat Python files: 76 per-source loaders, ~13 verifiers,
  dated one-off batch runners. 1.3 GB scratch dir inside it.
- `connect/` — entity spine / xref / cohort / dossier (35 modules). Active.
- `loadkit/` — shared load primitives (atomic load, checkpoint, windowed).
- `infra/` — numbered Snowflake DDL. `home/` — newest "one door" Streamlit app.
- `honesty/` — mart grading. `tests/` — 84 files.

**Loader logic is fragmented across four places:** `scripts/`, `loadkit/`,
`library-onboarding/`, `politics/loaders/` (+ a portal loader in `connect/`).

**Cooling/stale:** `viz/` (08-04), `bench/` (08-05), `playground/` (08-02),
`reading_room/` (08-01), `hunch/` (08-01), `ripple/` + `queues/` +
`mission_control/` (07-27), `portal_recon/`, `investigations/`, `.cortex/`.

**Cruft, ranked:**
1. `outputs/` = 5.1 GB — 4.1 GB bulk cache + 400 MB raw downloads commingled
   with 89 tracked report files.
2. `scripts/` — flat, dated one-offs never cleaned, 1.3 GB scratch inside.
3. Root-level: 2.19 GB PSC zip, 72 MB ICIJ zip, `.done` sentinel files.
4. Six Streamlit apps (`home/`, `serve/`, `playground/`, `reading_room/`,
   `mission_control/`, `bench/` + atlas app + panel server); `home/` is the
   intended consolidation, five predecessors linger.
5. Four overlapping root docs (CLAUDE/README/STATUS/build-state) + 65 KB
   CHRIS_DECISIONS.md; two venvs; three requirements files.
6. Genuinely dead (≥2 wks cold): `queues/`, `mission_control/`, `ripple/`,
   `portal_recon/`, `investigations/`, `.cortex/`. (Check imports before
   declaring `ripple/` dead — original CLI package.)

## 2. Data coverage & trust (from the repo's own audit artifacts)

**Scale:** 558–561 modeled sources, 24 domains, ~1.28B mart rows, ~607 mart
tables, 361 graded. 31.9M entities in the spine, 15.5M in 2+ sources.

**Trust headlines:**
- Completeness vs publisher (2026-08-11): 128 COMPLETE / 30 SHORT / 8 OVER /
  15 declared samples / **376 UNKNOWN (no publisher total — biggest blind
  spot)**. Of checkable sources: 71% complete.
- Value spot-checks: 16/18 tables matched publisher field-for-field.
- Same-day repair session closed all 14 defect classes from the verification
  sweep; first-ever full dbt test run 1,173/1,186 pass.
- Spine: every connection measured (847→829 after fixes), 99.6% name
  agreement, zero below the 50% floor. UEI join 97%, NPI join 96%+.
- Offline suite: 3,034 pass / 2 skip / 1 known fail (roll-call mart twin,
  113,512 vs 3,364 — standing three sessions).

**Top open data-trust issues (each one line):**
1. 376/558 sources have no publisher benchmark — completeness unverifiable.
2. Immigration court records: 12.6M rows, one real column, no loader exists.
3. USASpending contracts capped at exactly 20M rows; spine reads smaller copy.
4. Senate LDA lobbying ~9% of 1.98M filings (API-key blocked).
5. FDA MAUDE 2.7M of 25.7M; Federal Register 9% — priced go/no-go, unspent.
6. 21 new CourtListener court tables outside the entity map; judges have no
   national ID.
7. Roll-call mart twin disagreement (needs Python builder re-run).
8. 107 dead ID columns awaiting source-file byte checks.
9. 18 tables on exact loader page boundaries, never re-pulled.
10. Raw layer physically dirty: 22.9M junk dup rows, wrong-file NCUA, ~50
    orphans awaiting human DROP; failed citation-network load.
Runner-up: dbt uniqueness suite has no scheduled cadence — can silently stale.

**Assessment for the pivot (given to Chris in chat):** none of this blocks
starting top-down analysis. The unknown-completeness majority is a per-finding
verification chore, not a gate. Known-incomplete sources need a trust label on
every chart. Top-down analysis will surface which gaps are worth paying for.

## 3. Analysis & viz tooling — tool by tool

- **Bench** (`bench/`, Dash 8051, ~15.6k lines): 145 chart types with typed
  slots, six-bucket knob tree, two-way code sync, snapshot-backed catalog
  drawer. Serious and tested; last commit 08-05. **Bottom-up by design** — you
  arrive knowing SQL + chart type; no overview path in.
- **Playground** (`playground/`, Streamlit 8502): ~10 hardcoded question packs
  → dictionary panel → one read-only SQL → Plotly → saved card. Strong honesty
  rails. Semi-abandoned (08-02) with a detailed unactioned fix list; its own
  verdict: "the lab can't see the map."
- **Reading Room** (`reading_room/`, 8890): case desk (entity) + pattern desk
  (cohort → member receipts), append-only sign-off, AI-free enforced by test.
  Dormant (08-01) but **the only tool with a real two-level hierarchy** — the
  right drill-down shape.
- **Library Atlas chain** (`viz/compile_library.py` → `library_app.py` →
  `export_html.py`): compiles all 1,043 tables to `outputs/library.json` with
  presence states (lit/dark/keyless/uncharted) and three morphing lenses
  (subject treemap / connection / DAG journey), zero-Snowflake. **Strongest
  existing overview layer, but stale**: library.json is 08-02, its inputs were
  rebuilt 08-09/08-11. Deprecated predecessors (anatomy/atlas compilers,
  atlas_app) still sitting alongside.
- **CLI charting core** (`viz/catalog.py` etc.): live domain rollup
  (`shelves()` = domains by data volume), find/columns/profile/cast helpers,
  cards to `investigations/`, hard rails. Maintained. **`shelves()` is the
  best candidate top-of-funnel — it just has no UI.**
- **Hunch engine** (`hunch/`): pure-function lattice census + surprise score
  S = log10((obs+1)/(exp+1)) with absence clamping and fluke control +
  two-stage hypothesis sieve. Complete, calibrated, tested, **parked since
  08-01 with no UI** — already a ranked idea generator, i.e. what the CSV
  tries to be by hand.
- **Home / one door** (`home/`, 8500, newest 08-11): Findings (rule → leads →
  receipts) / Look up (entity dossier) / Explore (bookmark links only). The
  only end-to-end drill (pattern → lead → dossier) but starts mid-altitude;
  nothing above pattern level; no state handoff to other tools.
- **The idea CSV** (`reports/viz_brainstorm_2026-08-10.csv`): 2,873 rows —
  single 2,192 / cross 575 / catalog 106; strength high 1,816 / medium 840 /
  wild 217. **Defects:** `rigor` is a constant (all "plausible-from-metadata"
  — no maturity ladder); `chart_shape` = 315 free-text values not mapped to
  bench registry keys; `domain` = 203 uncontrolled values with near-dupes
  (politics vs money_in_politics, finance vs money_finance); **orphaned** — no
  script generates or consumes it.

## 4. Gap list for a top-down (overview → drill) analysis flow

1. No top-altitude screen anywhere — every tool starts mid-altitude.
2. Idea CSV disconnected at both ends (no generator, no consumer, no FK to
   chart registry or catalog domains).
3. `domain` is not a controlled vocabulary (203 values, near-dupes).
4. No maturity ladder for ideas (rigor constant) — nothing to rank/filter by.
5. Overview map on disk is stale vs the 08-11 warehouse; no recompile check.
6. No state handoff between surfaces (every boundary retyped by hand).
7. Hunch engine output has no human-facing surface.
8. Findings drill has one level (no domain rollup above, no chart below).
9. Deprecated compilers/HTML still live → "which map is real" is ambiguous.
10. Three chart-artifact formats, no shared index ("what have I already
    charted for this domain?" is unanswerable).

## 5. Synthesis — what this means for the pivot

The parts of a top-down funnel already exist, disconnected:
- **Top:** domain rollup (`shelves()`), presence-state map (library.json,
  needs recompile), completeness/trust grades (honesty + audit CSVs).
- **Middle:** the 2,873 ideas (need domain normalization + maturity ladder),
  hunch-engine scoring (parked), connection map (current).
- **Bottom:** Bench for chart building, Findings/Look up for entity receipts,
  Reading Room for sign-off.

The missing piece is not another tool — it's the spine connecting altitudes:
a controlled domain vocabulary, a maturity ladder for ideas, a fresh overview
compile, and click-through handoffs. The CSV is ore, not the map.
