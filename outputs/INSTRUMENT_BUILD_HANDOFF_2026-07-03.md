# The Investigator Instrument — build handoff (2026-07-03)

Chris: this is your Power BI over the Library, except nothing is pre-decided.
Any table, any domain, live off the catalog. You drive; the tool keeps up.

**Try it right now (no setup needed):**
```
python ripple.py chart find shipping
python ripple.py chart "SELECT SPLIT_PART(CASE_TYPE, CHAR(9), 3) AS ST, COUNT(*) N FROM LIBRARY_RAW.LANDING.FED_EOIR_CASE_DATA GROUP BY 1 ORDER BY 2 DESC LIMIT 15"
```
A chart opens. A card (`investigations/.../qNN_*.py`) holds the real Plotly code.
Full manual: [viz/README.md](../viz/README.md).

---

## What shipped

| piece | what it is |
|---|---|
| `viz/` package | the core: `theme` (one validated dark template — ends the 4-palette drift) · `plugs` (10 chart components, real px/go code, `**px_kwargs` passthrough) · `guard` (read-lane SQL guard) · `sqlrun` (THE chokepoint: guard + claim-block + lane verify + row/cell caps + budget line) · `catalog` (live discovery, zero hardcoded lists) · `safety` (facts-vs-leads classifier + badges) · `card` (runnable .py per question + eject) |
| `ripple chart` | the CLI verb: `run / find / shelves / cols / profile / cast / last / eject / budget` |
| Workbench | 5th Reading Room view (`serve/app.py?view=workbench`): SQL box → grid → plug gallery → chart → Code tab with save-as-card. Thin shell — ALL logic in viz/, so CLI and Workbench can't drift |
| chart cards | `investigations/<slug>_<date>/qNN_<name>.py` — standalone, re-runnable from any CWD, utf-8/ASCII, one plotly.min.js per folder (KB-sized HTMLs). `.py` committed, `.html` gitignored |
| eject | `ripple chart eject <card>` inlines the plug's REAL source (`inspect.getsource` — zero template drift) so week-4 you hand-tunes raw Plotly |
| tests | 89 new offline tests (guard bypasses, fail-closed classifier, card subprocess round-trip from a foreign CWD, eject figure-equality, plotly-blocked import) — full suite 411 green |

## The proof (all live, 2026-07-03, budget 42.42 → 42.42/300 cr — charting is ~free)

| domain | table | what it proved |
|---|---|---|
| money-in-politics | `POLITICS__MEMBER_MONEY_RAISED` (typed mart, **no CATALOG row**) | the mart arm: discovery sees the 35-table POLITICS suite CATALOG structurally can't; party colors follow convention (D blue / R red) |
| intl conflict | `INTL_UCDP_GED` (386k rows, all-TEXT landing) | cast path; Rwanda '94 / Tigray '21 / Ukraine '22 read correctly off the chart |
| economy | `FED_FHFA_HPI` (landing) | **auto-suggest** picked `line` unprompted ("YEAR looks like time") |
| immigration (growth proof) | `FED_EOIR_CASE_DATA` — 12.6M rows, landed DURING the pour, named in no design doc | chartable with zero wiring — the built-to-grow claim, demonstrated |
| env/human rights (growth 2) | `INTL_GLOBAL_WITNESS_DEFENDERS` (landed 2026-07-02) | second zero-wiring proof, q02 auto-numbered into the same investigation |

Safety rails, live: name-only join → visible `[LEAD]` badge (baked into the card
code — survives re-run AND eject) · raw `"CONNECT".LEADS` read → **refused**, pointed
at `V_LEADS_PUBLISHED` · `DROP TABLE` → refused at the first keyword. Hot loop:
card re-run 0.12–0.16s warm; eject → still runs.

**Proof lane honesty:** everything above ran in the **client-guard lane as
ACCOUNTADMIN** (see action item 1 — the PAT session cannot `USE ROLE`, and
CLAUDE_MCP_READONLY holds CREATE TABLE, so today the text guard + single-statement
execution are the wall). The instrument SAYS this on every run; it never claims
"enforced" without proving it at connect time.

## What's live in Snowflake (created this session)

- `LIBRARY_META."CONNECT".V_LEADS_PUBLISHED` — published()-semantics as a view
  (STATUS='active' + DECISIONS latest-verdict anti-join + REVIEW_STATE/PUBLISHED
  columns). Verified: 1,030 leads, all pending, 0 published — matches the engine.
  Regenerable; the safe way to chart leads from ANY SQL surface, Snowsight included.

## 🔴 Found during the proof: FED_EOIR_CASE_DATA is a broken load

12.6M rows, **one column** (`CASE_TYPE`), each cell a full tab-separated record —
the loader parsed a TSV as single-column CSV. Every row distinct, so the density
gate passed it. Chartable via `SPLIT_PART(CASE_TYPE, CHAR(9), n)` (that's what the
proof did) but it needs a re-land with the right delimiter. Same failure class as
FED_FJC_IDB from the 2026-06-27 audit — consider a "1 column + >1M rows" tripwire
in the density gate.

## Chris's action items (in order; the tool works TODAY without them)

1. **Turn on enforced read-only**: run `scripts/instrument_snowflake_setup.sql`
   in Snowsight (creates a FRESH `RIPPLE_READER` role — provably clean, not a
   scrub of CLAUDE_MCP_READONLY which holds CREATE TABLE via FUTURE grants), then
   put the minted PAT in `.env` as `SNOWFLAKE_SERVE_PAT`. Verify:
   `python ripple.py chart budget` → "lane: enforced".
2. **Create the serving lane**: `serve/serve_wh.sql` (SERVE_WH + SERVE_MON 5 cr/mo;
   step 0 of the same script). Until then charting runs on COMPUTE_WH under
   RIPPLE_BUDGET only.
3. **Re-land `fed_eoir_case_data`** (delimiter bug above).
4. Optional: `pip install -r serve/requirements.txt` if the Workbench is wanted
   locally (streamlit 1.58 verified; installed in the current env already).
5. When you want the LEADS charts to show confirmed facts: review leads
   (`python -m connect review lead <LEAD_ID> confirmed --by chris`) — they flip to
   `PUBLISHED=TRUE` in `V_LEADS_PUBLISHED` automatically.

## The review pass (before commit)

A 52-agent review (8 finder angles → 1-vote verify) surfaced **42 verified findings**;
the correctness/safety ones were **fixed and regression-tested** in the same session:

- `IDENTIFIER('..."CONNECT".LEADS')` bypassed the claim-table scan → IDENTIFIER
  is now denied on the read lane.
- `JOIN (subquery) USING (name_col)` was invisible to the classifier and shipped
  as *clean* → standalone USING scan + a fail-closed net (any JOIN whose condition
  wasn't captured → UNVERIFIED). CROSS JOIN likewise.
- The lane-verify probe (`USE ROLE ACCOUNTADMIN`) could leave the session
  escalated on a misconfigured PAT → probe now reverts; grant audit also fails on
  role inheritance.
- Cards embedded SQL unescaped (a `'\t'` silently became a real TAB on re-run;
  `'\x'` corrupted the file) → escaped; round-trip tested.
- A trailing `-- comment` swallowed the LIMIT wrapper → newline-protected
  (`sqlrun.wrap_limit`, pure + tested).
- `line()/area()` sorted date TEXT lexicographically before converting → convert
  first. `cast_sql` drafted epoch-parsing `TRY_TO_DATE` on YYYYMMDD digit columns
  → format-explicit with a verify-me comment.
- PARTY colors could hijack any D/R-valued column → gated on the column being
  NAMED party; hexes now reference the theme palette.
- Card overwrite rule tightened: explicitly-named cards overwrite, auto-named
  always fork, **ejected (hand-tuned) cards are never overwritten**.
- Workbench Code-tab preview now built by the same `card.render_body()` as the
  save (a lead query's preview can't look cleaner than its card); the setup DDL
  gained server-side claim-table REVOKEs + a `V_LEADS_PUBLISHED` grant.

**Deferred with eyes open** (efficiency/consolidation, none load-bearing):
per-process lane verification costs ~4 round trips (~1s cold); the JSON discovery
cache has no eviction; `find()` caches per-term; four copies of the sys.path/.env
bootstrap and two `quote_ident`/`dicts()` twins exist across packages (dependency-
direction choices — a `ripple/common`-level consolidation is the v1.1 refactor);
`budget_line` runs SHOW twice on a cache miss; fetch transfers up to cap+1 rows
before client-side cell-cap truncation.

## Design notes (for future sessions)

- **Process**: 6 parallel readers → design spec → 8-lens adversarial stress-test
  (8/8 GO-WITH-FIXES; blockers folded: fail-closed classifier, two-arm find(),
  connect-time lane verification, card bootstrap, px-template-at-creation) →
  build → midpoint live proof → multi-agent diff review.
- **The classifier is downgrade-only** (badges LEAD/UNVERIFIED, never certifies
  "fact") — a regex parser must not make positive claims. The role lane is the wall.
- **Palette** is the dataviz-validated 8-slot dark set, re-validated against
  #0d1117; >8 categories fold to 'Other'; no dual-axis anywhere, by construction.
- **Cut from v1** (deliberate): `ripple chart nl` (the Claude Code session IS the
  NL layer; v1.1 candidate = `library-onboarding/llm.py` + `viz.catalog` context),
  `choropleth_county` (needs a vendored geojson — decide before building).
- Known limits, stated honestly: classify_query misses WHERE-clause join tiering
  (comma-FROM → UNVERIFIED, fail-closed, never silently "fact"); `sampled`
  lifecycle mislabels full loads whose run MESSAGE contains the word "sample"
  (upstream CATALOG bug, e.g. fed_fhfa_nmdb 19M rows — the instrument badges
  instead of hiding, so nothing is lost); SHOW/DESC results skip the row cap
  (harmless — metadata).
