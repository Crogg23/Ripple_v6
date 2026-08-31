# Session Brief: Data Warehouse Metrics → Visualization Options Map

**For a brand-new Claude Code session. Do not decide — map every viable option.**

**Recommended model: `claude-opus-5`, effort: `high` (use `max` if available in your client).**
Why: this is a creative/research synthesis task (breadth of options, novel chart concepts,
cross-library tradeoffs) — the constitution's staffing rule puts that in the "thinking" lane,
not the "building" lane. If Opus 5 is unavailable, fall back to Sonnet 5 at `high` effort, but
flag that the ceiling on novelty/creativity will be lower.

---

## 0. Read first

- `/Users/chrisr./Documents/GitHub/Ripple_v6/CLAUDE.md` — the operating constitution. Follow it.
- `/Users/chrisr./Documents/GitHub/Ripple_v6/reports/the_audit_2026-08-24/mechanics.md` — the
  source narrative for every metric below.
- The CSVs in that same folder: `tables.csv`, `columns.csv`, `key_columns_all.csv`,
  `key_columns_verified.csv`, `key_overlap_edges_new.csv`, `spine_connect_edges_live.csv`,
  `scale_summary_by_schema.csv`.

## 1. The ask, precisely

Chris wants these warehouse metrics visualized on his public **portfolio website**. He does
**not** want you to pick one library or one chart type per metric. He wants an **expansive,
creative, clever, novel map of every real option** — so he can choose the taste call himself
(RED lane, per the constitution). Your deliverable is a menu, not a decision.

This is explicitly NOT: a working prototype, a final recommendation, a narrowed shortlist, or
a single "best" answer per metric. If you catch yourself collapsing to one pick, stop — that's
the failure mode Chris is trying to avoid by asking for this document.

## 2. The metrics to map (pull exact numbers from mechanics.md, don't re-derive)

Group them yourself if a better taxonomy emerges, but at minimum cover:

- Warehouse scale: 7 databases, 5,436 objects, 3,350 tables, 2,086 views, 4.97B rows, 185.4GB
- Per-database breakdown (rows/tables/views × 7 databases, wildly different scales)
- Entity spine registration gap-and-correction story (847 → 178 → 267, the whole reconciliation
  narrative in §4a of mechanics.md — this has a "before/after correction" shape worth
  visualizing as its own thing, not just a bar)
- Entity graph scale: 33.3M golden entities, 84.4M keyset nodes, 181M match pairs, 4,910 edges,
  17,598 leads — six orders of magnitude in one pipeline
- Overlap coverage: 24,011 measured pairs (11,839 confirmed / 12,172 new), broken out by key
  type (DOCKET, EIN, NPI, CCN, CIK, etc.)
- The DOCKET trust breakdown: 45 trustworthy / 2,909 reclassified-as-noise / ~6,475 unverified
  — a three-tier confidence story, not a flat count
- Dead weight: THE_LIBRARY (254 views, 0 rows), PREDBT backup (318 tables), two spine backups
  (~272.6M rows each) — a "waste/inefficiency" story
- The four-verb pipeline itself (SCOUT → COLLECT → CONNECT → DETECT) as a system diagram, with
  live counts annotated at each stage
- Key trust tiers (STEEL / STRONG / GEO / PROBABILISTIC) and their real-world counts

## 3. Scope the library search wide — don't default to the obvious four

Explicitly research and score **at least these**, plus anything else you find in your own
research pass:

**Python-native, static-image output:**
matplotlib (+ custom stylesheets), seaborn, plotnine (ggplot2-style), Datashader (built for
billion-row scale — relevant given 181M/84M row counts), PyGraphviz/NetworkX for graph layouts.

**Python-native, interactive/web output:**
Plotly, Bokeh, Altair/Vega-Lite, HoloViews + hvPlot, pyecharts (wraps Apache ECharts — strong
for the "editorial/graphic-design" look Chris asked about), Panel/Dash for dashboards.

**Beyond standard chart libraries — for the "novel/clever" requirement:**
- Generative/creative-coding approaches: matplotlib or Python + Pillow driving a hand-built
  visual metaphor (e.g. render the warehouse as a physical structure, particle field sized by
  row count, isometric "data city")
- Graph/network visualization at scale: deck.gl (via pydeck) or Cosmos/Sigma.js for the 181M
  match-pairs / 84M-node entity graph — standard node-link plots will not render at that scale,
  so include aggregation/sampling strategies (hexbin, hierarchical edge bundling, hashed
  sampling) as their own option, not an afterthought
- D3.js directly (not a Python library, but relevant since this ships to a website) — note
  where D3 beats every Python option for full custom control, and what the cost is (hand-coded,
  not "run a function")
- Observable Plot / Observable notebooks — lighter-weight D3 alternative, embeddable
- WebGL-backed options (regl, three.js via a thin Python data-prep step) for anything animated
  or 3D on the live site
- Icon-array / pictogram libraries or hand-rolled SVG grids for the "45 out of 6,560" trust
  story — this is a case where a boring bar chart undersells the finding

Do not stop at this list — if your research turns up something genuinely better suited
(a specific library built for treemaps-at-scale, a font-aware infographic toolkit, etc.),
include it. The instruction is "expansive," not "exhaustive-of-this-list-only."

## 4. For every metric group, produce multiple visualization CONCEPTS, not just chart types

For each metric group in §2, generate 3-6 genuinely different visual concepts (not just
"bar chart in library A vs library B" — that's one concept in two skins). Examples of what
"different concepts" looks like for the entity-graph-scale metric:
1. A funnel (33M → 84M → 181M → 4,910 → 17,598) — but note the funnel is non-monotonic
   (84M < 181M), so a naive funnel chart lies; propose how to handle that honestly
2. A Sankey diagram showing the reduction/expansion at each stage
3. A log-scale bar strip with annotated stage labels
4. A "zoom" visual metaphor — nested circles where each ring is 10x smaller, log-scaled
5. An animated counter/scrubber (interactive, web-only) that walks through the pipeline stages
6. A physical-object metaphor (e.g. sand through a funnel, sized to scale) rendered as static art

Do this same creative-options pass for every metric group. Favor variety of visual grammar
(hierarchy, flow, magnitude, part-to-whole, network, time, confidence/uncertainty) over variety
of libraries alone — a table that just swaps library names per row is not what was asked for.

## 5. Evaluation dimensions — score every concept×library combination against ALL of these

Do not pre-weight or rank these against each other — report all dimensions, let Chris weight them:

- **Load time / page weight** on a live website (static image vs. JS bundle size vs. lazy-load)
- **Interactivity** (hover/filter/zoom vs. static — and whether interactivity adds real value
  here or is just decoration)
- **Design/"graphic design" polish ceiling** — how good can this look with real design effort,
  not the library's default theme
- **Dev/build effort** — hours-to-first-draft vs. hours-to-portfolio-polish
- **Scalability to the actual row counts** (181M match pairs cannot be scatter-plotted directly
  — flag which options need aggregation/sampling and which handle scale natively)
- **Accessibility** (colorblind-safe palettes, screen-reader/alt-text feasibility for canvas/WebGL
  vs. SVG vs. static image)
- **Light/dark theme compatibility** on the website
- **Maintainability** — can this be regenerated automatically next time the audit re-runs, or
  is it hand-tuned one-off art
- **Novelty/"wow" factor** — how differentiated this looks vs. a generic dashboard chart

## 6. Deliverable format

Produce a single markdown report (plus any example images/code snippets as supporting files,
not required to be full builds) structured as:

1. One-paragraph plain-English intro (bar rule — no jargon without translation)
2. Per metric-group: the 3-6 concepts, each scored across every §5 dimension in a small table,
   with a 2-3 sentence description of what the concept actually looks like
3. A cross-cutting "library capability matrix" — every library from §3 as rows, key
   capabilities (interactive, scale-handling, static export, web-embeddable, license) as columns
4. An explicit "wildest ideas" section at the end — 3-5 options that are genuinely unconventional
   for a data-metrics page, kept in even if impractical, clearly labeled as high-risk/high-reward
5. NO final recommendation, NO "if I had to pick one" section, NO narrowed shortlist. End on
   the options themselves.

## 7. Constitution reminders for the new session

- This is a RED-lane taste question (what the portfolio *looks like*) — the new session's job
  is to hand Chris options, not make the call.
- Beer Rule: plain words, translate jargon, answer-first framing even in a long document —
  each section should open with what it's showing before the how.
- Never claim a library/tool capability you haven't verified this session (check current docs,
  don't rely on training-data assumptions about version-specific features).
- Report back to Chris in a hard-capped 3-5 bullet summary in chat; the full map lives in the
  file, not the conversation.
