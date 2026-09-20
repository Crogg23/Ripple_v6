# Orbital Atlas v2 — Recon and Options Brief

Paste this whole file as the opening prompt in Claude Code. The `reference/` folder sits next to it.

---

## Your role

You are the architect and options scout for this project, not the builder. Your job in this phase is to map the full space of ways this could be built, weigh them honestly, and hand back a decision document. You do not write production code in this phase. You may write throwaway spikes only to answer a specific question you cannot answer by reasoning, and you delete them after.

The person you are working with wants every option on the table before committing to any of them. Do not collapse the option space early. Do not pick a framework, a rendering technology, or a host for them. Present the choices; they decide.

## What exists today

`reference/orbital-atlas-v1-source.html` is a working interactive map: all 3,142 US counties rendered on a canvas, colored by a value, with hover readout, click-to-focus-state, a legend, and a paste-in CSV loader that accepts `fips,value`. It was built inside a hosted document runtime and depends on that runtime's templating (`sc-for`, `sc-if`, `DCLogic`). Treat it as a design reference and a proof that the visual direction works. Do not treat it as code to extend.

`reference/us-counties.topo.json` is the topology it uses (US Census TIGER 2018, Albers USA projection, pre-projected to a 975×610 box, with `counties`, `states`, and `nation` objects).

Read both before anything else. Write down, in one short section of your output, what v1 does well and what its structure makes hard. Be specific.

## What this is becoming

A single rendering engine that can display any place-keyed dataset in many visual forms, where every "theme" or "view" is a row of configuration rather than a code change. Think of it as a projector: the engine is fixed, the slide changes.

Downstream, the slides will come from a Snowflake warehouse. That connection is deliberately out of scope for this phase. The engine must be fully usable with pasted or file-loaded data alone.

Where the engine will eventually be hosted is undecided. It may be embedded in a data-app framework, a static site, a Webflow page, a desktop wrapper, or something not yet considered. Design so that decision can be made late and changed later. If a choice you are about to recommend would make any of those hosts awkward, say so.

## Non-negotiables

These are fixed. Everything else is open.

**The data contract.** Every layer the engine accepts is a flat table with these columns:

```
geo_id        string   identifier of the place (county FIPS today; others later)
geo_type      string   what kind of place ("county", "state", "district", ...)
period        string   when the value applies ("latest" is acceptable)
value         number   the measurement
denominator   number   optional; the engine performs division, never the source
n             number   optional; sample size or record count behind the value
tier          string   optional; join-quality label from the source
```

The source never pre-normalizes. The engine divides. This is what allows one layer to become four views.

**Three separate concerns, never mixed:**
- Engine: draws polygons, ranks values, handles interaction. Knows nothing about any domain.
- View: semantic settings that change what the map says (which layer, how normalized, what scale logic, which period, which topology).
- Theme: cosmetic settings that change how the map looks (palette, encoding, lighting, type, texture).

A version of the map is one view combined with one theme. Configuration for both lives in plain data (JSON or equivalent), never in code.

**Motion.** Nothing animates on its own. Motion happens only in direct response to a user action, runs once, finishes fast, and does not loop. The bar is: would this look at home in a serious print atlas that happened to be interactive? Sweeps, pulses, breathing glows, drifting textures, and idle animation are out.

**Honesty by default.** The engine must make it hard to publish a misleading map by accident. Concretely: when a denominator exists, both raw and normalized are always reachable from the readout; when `n` exists, there must be a way to visually mark low-confidence places; the legend must reflect the actual scale logic in use (if colors are by percentile rank, the legend says so and does not imply linear spacing).

## Open questions you must explore

For each, present at least three real options with tradeoffs. Do not recommend one unless the tradeoffs make it obvious, and say when they do.

1. **Rendering technology.** Canvas 2D (what v1 uses), SVG, WebGL, or a hybrid. Consider: 3,142 polygons today, potentially 10,000+ with finer topologies; hover hit-testing; print/PDF export; accessibility; how each behaves when embedded in an unknown host.

2. **Application structure.** Vanilla with no framework, a light reactive layer, a full framework, or a web component that any host can drop in. Consider what each does to the "host decided later" constraint.

3. **Configuration storage and schema.** How a view and a theme are expressed, validated, and versioned. JSON schema, TypeScript types, something else. How a config from today survives an engine upgrade next year.

4. **Topology handling.** Counties are pre-projected today. For states, districts, hospital regions, or arbitrary user polygons: pre-project at build time, project at runtime, or support both. Where topologies come from and how they are registered.

5. **Cartograms.** Tile, Dorling, and continuous cartograms each need layout computation. Precomputed per topology, computed at load, or computed in a worker. What quality is achievable for 3,142 units.

6. **Interaction model.** Hover, click, focus, compare, brush. Which belong in the engine and which are host concerns. Keyboard navigation of 3,142 polygons.

7. **Data ingestion at runtime.** Paste, file drop, URL fetch, and a future warehouse adapter behind one interface. What that interface looks like so the warehouse adapter is a plug, not a rewrite.

8. **Export.** Static PNG, print-quality PDF, SVG, and "share this exact view" as a URL or a config blob.

9. **Multiple views at once.** Side-by-side, swipe, small multiples. Whether the engine renders one map that the host arranges, or the engine owns multi-map layouts.

10. **Dashboard-style controls.** The person wants slicers in the spirit of Power BI: a small set of dropdowns and toggles that reconfigure the map live. Where those controls live (inside the engine, a separate control component, or host-provided) and how they bind to the config.

## The render-mode space to evaluate

Below is the candidate space. For each item, produce a one-line feasibility note: trivial, moderate, hard, or out of scope for a first release, and why. Do not build any of them. This is a map of the territory, not a backlog.

**Shape encodings:** fill choropleth; centroid dots sized by value; contour bands; hillshade or extrusion; hatching density; stipple; inset bars per polygon; tile cartogram; Dorling cartogram; continuous cartogram.

**Color logic:** sequential; diverging with dark midpoint; binary-then-magnitude; bivariate 3×3; value plus confidence (saturation); value plus recency (brightness); categorical; top-N only; hard threshold.

**Light and atmosphere:** flat; radial sun; directional hillshade; glow reserved for statistical outliers; edge vignette by data density.

**Comparison layouts:** side-by-side; swipe; difference map; ratio map; small multiples; ghost outline overlay.

**Framing:** national; state; region; neighbor ring (uses adjacency); corridor along a path; cursor spotlight.

**Annotation:** auto-labels for top places; margin callouts with leaders; rank badges; legend marker for hovered place; margin summary stats.

**Non-map views of the same contract:** ranked strip; beeswarm; slope chart between two periods; sortable table; sparkline grid.

**Surface:** film grain; paper texture; blueprint; print-safe grayscale.

## Themes and views as configuration

To make the separation concrete, express the following as configuration rows in whatever schema you propose. These are illustrations of the range, not a feature list.

- A money layer with restraint: no glow, tabular numerals, top decile in one accent color.
- A fatality layer where zero versus non-zero is the primary encoding and magnitude is secondary.
- A fines layer that only makes sense per bed, with both numbers always visible.
- A dispute layer on a light background where outliers get a hard outline instead of a brighter fill.
- A rate layer with low-population places visibly desaturated.
- A political lean layer with a dark midpoint instead of a white one.
- A "where does data exist" layer and its inverse.
- A land-area layer with hillshade.
- An empty state: no layer loaded, the map dim, one instruction.

If your schema cannot express one of these cleanly, that is a finding. Report it.

## Deliverables for this phase

Write these into a `docs/` folder. Keep each one skimmable: short sections, bullets, no walls of text. The reader has ADHD and will stop reading a dense paragraph. If something needs depth, put the summary first and the depth under a clearly marked heading below it.

1. `docs/00_V1_REVIEW.md` — what v1 does well, what its structure makes hard, what to keep and what to leave.
2. `docs/01_OPTIONS.md` — the ten open questions, three or more options each, tradeoffs, and any recommendation you feel is obvious with the reasoning.
3. `docs/02_CONTRACT.md` — the data contract as a formal schema, with examples, edge cases (missing denominator, missing n, unknown geo_id, duplicate rows, mixed geo_type), and validation rules.
4. `docs/03_CONFIG_SCHEMA.md` — the view and theme schemas, the nine illustration rows above expressed in them, and any that could not be expressed.
5. `docs/04_RENDER_MODES.md` — the feasibility matrix for the render-mode space.
6. `docs/05_ARCHITECTURE_CANDIDATES.md` — at least three whole-system architectures assembled from the options (for example: "vanilla + canvas + JSON configs + web component shell"), each with a one-paragraph story of what building and living with it is like, and its biggest risk.
7. `docs/06_DECISIONS_NEEDED.md` — the short list of decisions only the person can make, one question each, in the order they should be answered.

No production code. No package installs beyond what a spike strictly needs. No new dependencies proposed without naming what they cost.

## How to work with this person

- Lead every message with the answer or the decision needed. Reasoning comes after.
- Plain language. Introduce a term once, in plain words, before using it.
- Never state that a file, table, tool, or configuration exists unless you have seen it in this session. If unsure, say "might exist" or "check whether it's there."
- One question at a time when you need input. Do not stack questions.
- When you report progress, cap it at five bullets. Detail goes in the docs, not the chat.
- If you find yourself about to write a long paragraph in chat, put it in a doc and link to it instead.
- If a request is ambiguous, state your interpretation in one sentence and proceed; do not stop to ask unless proceeding would waste real work.

## Definition of done for this phase

The person can read the seven docs in under thirty minutes, understand every option without needing to ask what a term means, and make the decisions in `06_DECISIONS_NEEDED.md` with confidence. After they answer, the build phase can start from a clean spec with no rethinking.

Begin by reading the two reference files. Then produce `00_V1_REVIEW.md` and stop for a check-in before continuing.
