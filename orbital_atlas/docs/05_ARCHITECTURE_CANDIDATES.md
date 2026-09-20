# 05 — Whole-System Candidates

Five complete systems, each assembled from the options in `01`. Every one honours the contract and the view/theme split. They differ in **how much you own versus how much you borrow.**

Every library named here, its size, and its behaviour is from memory. None was checked in this session. Treat each as "might" and check before committing.

## At a glance

| | A. Plain core + web component | B. Compiled-framework component | C. WebGL library | D. Spec compiler onto a chart library | E. Python-side rendering |
|---|---|---|---|---|---|
| Rendering | Canvas, SVG export path | Canvas, SVG export path | WebGL | SVG | whatever the Python library does |
| Structure | plain library, custom tag shell | Svelte or Lit, compiled to a custom tag | library + thin wrapper | thin translator | a Python module |
| You own | nearly everything | the map; the framework owns the UI | config translation and styling | config translation | config translation |
| Borrowed weight | roughly 10 KB | roughly 15 to 40 KB | several hundred KB | roughly 100 to 250 KB | n/a, runs on a server |
| Host decided late? | **yes** | **yes** | mostly | yes | **no** |
| Sharp print | yes, via export path | yes, via export path | no | **yes, natively** | depends |
| 10,000+ shapes | yes | yes | **yes, easily** | strained | depends |
| Small multiples | yes | yes | capped by the browser | **free** | yes |
| Texture, light, grain | yes | yes | best | weak | weak |
| Extrusion | no | no | **yes** | no | no |
| Non-map views | hand-built | hand-built | hand-built | **free** | **free** |
| Time to first map | slowest | middle | middle | **fastest** | fastest |
| Biggest risk | volume of hand-written code | framework churn | fights the print-atlas brief | hits a ceiling on look and scale | locked to one host |

---

## A. Plain core + web component shell

**Recipe:** plain TypeScript library · Canvas 2D with a draw list · SVG writer for export · JSON configs checked by validators compiled at build time · `<orbital-atlas>` custom tag · optional `<atlas-controls>` · topologies pre-projected, runtime projection loadable on demand.

**Living with it.** You write a small engine that does exactly what the brief says and nothing else. The only outside code is the tiny topology decoder and perhaps a colour-interpolation helper. Every host is the same story: load one script, place one tag, hand it a view, a theme, and rows. A year from now nothing has broken, because there was nothing underneath to move. The cost is that every nicety is yours to write: the legend, the label collision pass, the keyboard walk, the table view, the slicer component. The first map takes longest of the five. The fiftieth render mode is no harder than the fifth, because nothing is in the way.

**Biggest risk:** sheer volume. A solo builder ends up writing a legend generator, a number formatter, a label placer, and an accessibility layer by hand. It is all known work, and there is a lot of it.

**Blunts the risk:** borrow small single-purpose pieces rather than a framework. A format-string library. A scale library. Each is a few KB and swappable.

---

## B. Compiled-framework component

**Recipe:** same canvas engine as A for the map itself · Svelte or Lit for everything around it: readout, legend, slicers, table, load report · compiled down to a custom tag so hosts still see one element.

**Living with it.** The map core is A's. The difference is the panel work. Instead of hand-writing "when the hovered place changes, update these six bits of text", you declare it and the framework keeps it in sync. The readout, legend, and slicers come together several times faster. Hosts cannot tell the difference, since the output is still a custom tag. You take on a build step and a framework's release cycle. Configs are untouched by any of that; they are still plain JSON.

**Biggest risk:** the UI half of the codebase is married to one framework. If that framework makes a breaking release, the engine survives and the panels need rework. Svelte has done this between major versions.

**Blunts the risk:** keep a hard wall. The engine package imports nothing from the framework. The UI package is replaceable.

---

## C. Stand on a WebGL map library

**Recipe:** a library such as deck.gl or MapLibre · shapes fed as flat x,y using the library's non-geographic mode, so Albers with insets still works · the library's built-in picking for hover · configs translated into layer settings.

**Living with it.** Hover picking, zoom, and 100,000 shapes are solved on day one. Extrusion is a checkbox. True shader hillshade is possible. But the library was built for slippy web maps, and the brief is a print atlas. You spend your time turning things off: inertia, easing, tile loading, default controls. Print is a screenshot. Small multiples hit the browser's cap on live WebGL contexts. Some embedded hosts throttle or drop WebGL contexts. The paper-and-ink themes fight the medium.

**Biggest risk:** the two things the brief cares most about, print quality and restraint, are the two things this stack is worst at.

**When it becomes right:** if decision 3 in `06` comes back "yes, extrusion matters" or decision 2 comes back "tract level, 80,000 shapes".

---

## D. Spec compiler onto a chart library

**Recipe:** a library such as Observable Plot or Vega-Lite · the engine is a translator: view + theme + rows in, chart spec out · the library draws SVG · wrapped in a custom tag.

**Living with it.** The first map is up in a day. Small multiples are one setting. The ranked strip, beeswarm, slope chart, and table-adjacent views come nearly free, from the same contract. Print is sharp with no extra work, because it is SVG all the way down. Then the ceiling arrives. 3,142 SVG shapes hover acceptably; 10,000 do not. Grain, soft light, hillshade, and blend modes are out of reach or slow. The legend is the library's legend, so the honesty rules must be forced through its options, or the legend rebuilt by hand anyway. The motion rule is easy, since these libraries barely animate.

**Biggest risk:** you hit the ceiling on look exactly when the project gets interesting, and the way out is a rewrite into A.

**A hybrid worth naming:** A or B for the map, D's library for the non-map views only. The map keeps its look. The strip and beeswarm come cheap. Cost: one more dependency, roughly 100 KB and up, loaded only when a non-map view is opened.

---

## E. Python-side rendering inside a data app

**Recipe:** Plotly, Altair, or similar · view and theme JSON read by Python · figure built server-side · shown in Streamlit or the like.

**Living with it.** If the host were already fixed as a Python data app, this is the least code of all. The warehouse connection is right there. Slicers are native widgets. But the brief says the host is undecided and must stay changeable. This candidate cannot run on a static site, a Webflow page, or a desktop wrapper without a Python server behind it. The motion rule and the custom look are also mostly out of your hands.

**Biggest risk:** it answers the host question by accident, permanently.

**Why it is listed:** every option on the table. It also makes a useful **throwaway prototype** for testing the config schema against real warehouse data before any engine exists.

---

## How the candidates map to the decisions

| If the answer in `06` is… | It points toward |
|---|---|
| Print must be vector-sharp | A, B, D |
| 10,000+ shapes in the first year | A, B, C |
| Extrusion matters | C |
| The look is the point: grain, light, ink | A, B |
| Fastest path to something on screen | D, then E |
| Least ongoing maintenance | A |
| Least code to write for panels and slicers | B |
| Non-map views early | D, or the A + D hybrid |

**An honest read, not a pick:** the brief's own non-negotiables — host late, print-atlas restraint, configs that outlive the engine — describe A or B. The real choice between those two is how you feel about hand-writing UI updates versus carrying a framework. C and D each win on one axis and lose on the brief's core. E is a prototype tool.
