# Handbook evaluation — 2026-09-01

Target: `reports/viz/join_handbook.html` (3.2 MB, self-contained, built 2026-08-30 18:16).

## What was checked, and how

- Parsed `window.HANDBOOK_TABLES` / `HANDBOOK_META` / `HANDBOOK_CONTEXT` out of the HTML.
  - 573 tables listed, 3,718 reliable edges, 158 measured edges, snapshotDate 2026-08-30.
  - Key glossary: 53 IDs with plain-word descriptions. 6 corrections (was/now). 9 traps.
- Compared against `_build/handbook_pass2_edges_2026-08-29.csv`:
  - 96 rows: 95 MEASURED, 1 SUSPECT. Verdicts: 70 plain SOLID, ~13 qualified SOLID, 9 "level 2 only", 2 SUSPECT-noted.
  - measured_on: 40 rows @ 08-29, 3 @ 08-30, **53 @ 08-31** — after the page was built.
  - `grep -c "2026-08-31" join_handbook.html` → 0. Those 53 measurements are not in the page.
- Compared against warehouse loads since the snapshot (git log 2026-09-01):
  - FEC itoth (28.5M rows), House financial disclosures, Open States legislators, BIA tribal geo, FEC committee union dim — none reflected. `ITOTH` grep → 0 hits.
- Builder chain:
  - `build_join_handbook_md.py` docstring says it writes `reports/JOIN_HANDBOOK.md`. That file does not exist — the markdown twin was never produced (or was deleted).
  - Same script points its PAGE constant at `_build/legacy/join_handbook_rail.html` with a comment that "the real handbook is built by build_chain_handbook.py" — the build path is tangled across three scripts.
- Warehouse cross-check of the 573-table count: **not run**. The chat plug-in door is down (Snowflake MCP 401, invalid token). Scripts door untried — would cost a query.

## What a hit / miss means

- 2026-08-31 grep miss in the HTML = the freshest third of the measured edges lives only in the CSV.
- ITOTH grep miss = every table loaded since 08-30 is invisible to the handbook.
- Missing JOIN_HANDBOOK.md = anything (or anyone) reading the markdown twin gets nothing, while the docstring promises it exists.

## Quality notes (the good part)

- Traps walk their chains properly: NDC padding (raw join 0% → padded 82.1%), HMDA two-number-system split, DUNS zero-filter, float-text bank certs. Each states the check, the hit, the miss.
- Corrections carry was/now with re-measurement dates — e.g. the SAM UEI 92.5% → 33.1% correction on the full 93M-row file.
- Verdict language is honest: "level 2 only (name-free by construction)", "SOLID (site -> parent org)" with the two-hop confirmation noted inline.
- No spine language in live payload (the one "SPINE" hit is inside table-name strings, not the dead concept).

## Update pass — same day, later

- Rebuilt via `build_join_handbook.py --dump-data` + `build_chain_handbook.py`.
- First rebuild broke two things; both caught by skeptic passes and fixed:
  - payload dump dropped 146 zero-connection tables → restored from HEAD payload.
  - dump also emptied time/clock on 306 tables → restored; META.time back byte-identical to HEAD.
- Final page: 573 tables, 452 with clocks, snapshotDate 2026-09-01, measuredOn 2026-08-31.
- Skeptic verdict #2: loses nothing vs HEAD (SCHEMA deep-identical), gains the 08-31 verdict text and dates. No numeric rate changed — the numbers were already in.
- The 9 CSV pairs absent from the measured tier all exist as `solid` edges; verified rate-for-rate.
- Skeptic flags to keep: OSHA↔IRS_BMF shows 5.6% in the solid tier with n mismatched vs CSV (6857 vs 6414); SAM↔LEIE n off by one — solid tier and CSV are different runs.
- Still absent, knowingly: tables loaded 2026-09-01 (FEC itoth, House FD, Open States, BIA tribal geo). Needs a warehouse pull; price-gated.
- Builder hygiene fix worth making: `--dump-data` should carry time/clock through so the splice isn't needed next rebuild.

## Shape pass — option C shipped

- Chris picked C: surface the buried traps and corrections.
- My earlier "no search" finding was wrong: the picker has a finder box; grep missed its "find a table" placeholder.
- Template gained two legend-grid sections: "Traps — columns that lie" (red, 2-col) and "Corrections — what an earlier pass got wrong" (amber, was struck through, now beside it).
- Data wired from META.traps / META.corrections, which previously shipped in every copy and never rendered.
- Verified three ways: headless DOM probes (9/9 traps, 6/6 corrections, full strings, no duplicates), skeptic pass (AGREE; flagged that the earlier date-stamp change wasn't restated), full-page screenshot (panel paints below the footnotes, legible).
- Files: _build/chain/chain_template.html (+18 lines markup, +2 data fields), join_handbook.html rebuilt (3,206,308 bytes).

## UI/UX pass — thorough loop

What changed in _build/chain/chain_template.html, page rebuilt each time:

1. Near-empty place columns collapse. Any table with >3 non-trap place columns under 1% filled folds them into one grey "N more place columns hidden" row; full list survives in the row's tooltip. Fires on 3 tables: NPPES (57 hidden), DOL OFLC (37), DOL Form 5500 (6). Trap rows can never be swallowed — the filter excludes traps by construction.
2. Source-panel Columns section collapsed by default behind a show/hide toggle. NPPES start panel drops from ~7,100px to ~4,800px rendered.
3. Badge under the intro: "⚠ 9 traps and 6 corrections live at the bottom — read them before you join", anchor-links to the traps panel.
4. Measured-tier legend date now reads META.measuredOn instead of hardcoded "08-29/30". The "60 matched pairs" fact, briefly dropped, was restored after skeptic flagged the omission.
5. Canvas fit: replaced trust in the hand-tuned height estimator with a measure-and-grow pass after each render (_fitCanvas). This also fixed a pre-existing bug — HEAD's page clipped ~2,200px of the source panel in its only state; skeptic found the new toggle clipped 4 of 6 columns when opened; now zero clipped containers in all tested states.

Verified by real clicks in Chrome via Playwright: closed / open / closed-again / one hop / card open — clipped-container count 0 in every state. Toggle expands and collapses, caret flips, previously clipped columns (REPLACEMENT_NPI, NPI_DEACTIVATION_REASON_CODE, deactivation/reactivation dates) render.

Skeptic pass #3 verdict: collapse, badge, wiring, card math all confirmed; blocker was the open-state clip, fixed above. Also noted my page-height numbers are viewport-dependent (his 1440px measurements differed) — treat all px figures as ~1560px-viewport numbers.

Not done, still parked: 09-01 warehouse loads absent from the page (needs a priced warehouse pull); builder hygiene fix for --dump-data time/clock passthrough.

## Explorer build — Map / Routes / Trails / Pivot tabs

Full send on the three exploration modes, one self-contained page, no new measurement.

- New file _build/chain/explorer.js, injected by build_chain_handbook.py. Tab bar sticky at top; the pivot is untouched inside #view-pivot with pickTable exposed as window.__openPivot.
- Map: canvas force layout, 573 nodes sized by ID-join count, colored by domain, 1,832 deduped undirected ID edges, place edges toggleable. 355 tables with no ID join sit faded on a fixed outer ring. Hover highlights a node's edges; click opens it in the pivot. First physics pass pinned everything to the walls; rewritten with autoscale-to-fit.
- Routes: two table pickers, three routes ranked strongest-weakest-link first. Skeptic caught BFS ranking a 0%-link route first; added a widest-path pass — OPEN_PAYMENTS→ECHO now leads with a 46.4% weakest-link route. Cross-island pairs get an honest "different islands" message.
- Trails: three curated chains, every hop verified against the payload at render time, all seven steps carry the exact measured % — Open Payments→NPPES→Part D (NPI 100/100), TRI→FRS→ECHO (FRS_ID 99.9/98), donor→committee→candidate→summary (89/100/100).
- Structural find the map surfaced: the ID graph is 370 components — one 162-table health/finance mainland, an 11-table FEC island, 355 isolates. FEC genuinely cannot reach health on IDs today.
- Fixes from skeptic pass #4: route ranking (above); isolate-count contradiction (pivot said 333, map said 355 — 333 counted tables with no edges at all, 355 counts no ID edge; both now derive as 355 to match the sentence they sit in); 6 self-loop edges dropped from the dedupe.
- Honesty notes from skeptic: 5 console errors on load are pre-existing (template placeholders + a self-CORS fetch), identical at HEAD; "pivot unchanged" means unchanged by the explorer layer — it does carry this session's earlier UX changes.
- Verified by Playwright clicks at 1560px: all four tabs, no new JS errors, route search both islands, trail click-through into the pivot, pivot chain-walk still works.

## Things tab — the new front door

The atom: a thing in the world and the identity language it speaks. Everything else derives.

- 17 entity cards: doctor, hospital, company, bank, politician, committee, factory, utility, water, mine, ship/plane/railroad, judge/court, detention, drug, device, award, place. Default tab.
- Card → dossier: language chips with glossary tooltips, "also appears as" bridges, tables grouped by domain sorted by rows, every row click-through to the pivot.
- Bridges are exactly symmetric by construction; skeptic named FED_CMS_NPPES as the doctor↔hospital bridge, 33 tables wide.
- Skeptic pass #5 fixes applied: BHCMIS moved bank→clinic, OFAC + SEC series keys added to company, RR_CODE rail added, HMDA_ARID unreliability now on the card, dead single-table keys dropped.
- Things exposed an upstream data trap: 12 tables carry domain "immigration" wrongly in the marts registry. Logged in .claude/traps.md.
- Verified: card counts equal independent recomputation, all five tabs click clean, zero new JS errors.

## Map redo + humanize pass

- Skeptic pass #6 rejected the first anchored map with the math to prove it: spiral spacing shrank as 1/sqrt of n so every cluster got the same radius, and the label offset formula cancelled itself so labels sat a constant height and collided with other clusters.
- Fixes: constant spiral spacing so radius grows with cluster size; row-packing layout where each cluster claims a box sized by its real radius plus its label width; scale-to-fit capped by both height and width; labels derive from actual cluster extent.
- Result at 1560px: 17 labeled neighborhoods, no overlaps, no clipping, bridge arcs legible between company / doctor / factory / hospital.
- Humanize: 120 curated names first pass, skeptic counted 98 joined tables still raw — all 98 now named. Coverage: 218 of 218 joined tables carry a plain-English name in Things, map hover, routes, trails. Raw name and id survive in tooltips. Pivot keeps original labels.
- Two names softened after skeptic pushback: FED_IRS_BMF is now "IRS business master file" — its row count is within 0.4% of the nonprofit master file, so "every business" was a claim the data doesn't back; parked for a warehouse check. FED_SAM_ENTITY_PUBLIC shows 0 rows in the payload — renamed neutrally.
- Legend cap removed — all domains listed, counts now sum to the drawn total.

## Enhancement pass — planned, approved, shipped

All 7 plan items live, verified by Playwright clicks and a fresh-eyes skeptic pass:

1. HUMAN names extracted to _build/chain/human_names.js, emitted in head, shared page-wide.
2. Cross-tab wiring: "route →" chip on every dossier row prefills Routes without opening the pivot; route inputs accept plain-English names — exact match wins, then unique substring.
3. URL hash state: #tab / #thing / #route=A..B / #pivot all restore on refresh; back button walks states; no hashchange loops in a 30-click hammer test.
4. Dossier briefings: grain/desc line under each table, clock + place + red trap badges, trap text in tooltips.
5. Copy-the-SQL on routes and trails: fqn JOINs with real lc/rc columns, correct sides both directions, warning comments where the payload carries note/norm. Skeptic caught the big one — 512 translation edges would have emitted fake tilde columns like CCN~NPI; those hops now emit an honest commented-out JOIN naming the crosswalk problem instead. Verified: 0 tilde columns in live JOIN lines, warning text present.
6. Pivot plain-names toggle next to reset; cards, source panel and chain survive toggling both ways. Two bugs found and fixed on the way: a replace that made cardLabel recurse into itself, and a toggle that dropped state keys.
7. Map cluster labels brighten on hover and click through to the Things dossier.

Also fixed during verification: const reassignment crash in the routes resolver.
Skeptic honesty notes kept: warnings exist on only 158 of 4,156 edges — say "where the payload has one"; 4 tables lack an fqn and emit bare ids; the route-from-here chip writes #tab=routes, so a refresh keeps the tab but loses the prefill.
