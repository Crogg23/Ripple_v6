# 06 — Decisions Only You Can Make

Twelve questions, in the order to answer them. Earlier answers prune later ones. Each has the options, what it drives, and where the depth lives.

**Answer in one word or letter each. That is enough to start the build spec.**

---

## Group 1 — What the map must be able to do

These three decide the rendering technology.

### 1. Does print have to be vector-sharp?
> **ANSWERED 2026-09-19: b. No print. Screen only.** The SVG export path is dropped. A saved image is enough.
- **a.** Yes. It must survive being blown up to a poster.
- **b.** No. A high-resolution image is fine.
- *Drives:* whether an SVG export path gets built. Depth: `01` question 1 and 8.

### 2. What is the most shapes on one map in the first year?
> **ANSWERED 2026-09-19: c. Census tracts.** About 80,000 nationwide. Open follow-up: all tracts on one national map, or one state of tracts at a time. That follow-up decides whether the graphics-card method is forced.
> **FOLLOW-UP ANSWERED 2026-09-19: counties nationally, then tracts per state.** At most about 9,000 shapes on screen at once. Canvas stays comfortable; the graphics-card method is not forced by shape count.
> What this adds to the build spec:
> - **Drill-down:** focusing a state swaps the shape set from counties to that state's tracts.
> - **Topology registry** gains a `children` link: for parent `48`, load `us_tracts_48`. One tract file per state, fetched on demand.
> - **Contract:** one layer may carry both `county` and `tract` rows. The mixed `geo_type` rule in `02` already splits them. It becomes a feature, not an edge case.
> - **Scale honesty:** on drill-down the view must say whether colours are ranked against the state's tracts or all tracts nationally.
- **a.** About 3,000. Counties are the ceiling.
- **b.** About 10,000. Finer regions, such as ZIP areas for a few states.
- **c.** 50,000 and up. Census tracts nationwide.
- *Drives:* canvas is comfortable through b. Only c pushes toward WebGL. Depth: `01` question 1.

### 3. Does true 3D extrusion matter?
> **ANSWERED 2026-09-19: b. 3D someday, not now.**
> What this does to the build spec:
> - The first release draws flat, on canvas.
> - **The draw list stays**, even though print was dropped. It is now the seam for a future graphics-card painter: the engine decides what to draw as plain data, and a painter carries it out. Swap the painter later, keep everything else.
> - Hover hit-testing, scales, legend, contract, and configs must not touch canvas directly. Only the painter does.
> - A theme field for 3D is reserved but unused: `light.type: "extrude"`.
> - Known cost when 3D arrives: small multiples are capped by the browser, and a tilted camera needs motion rules of its own.
- **a.** No. Faked hillshade is enough.
- **b.** Yes, eventually.
- *Drives:* b is the only answer that forces WebGL. Depth: `04`, shape encodings.

---

## Group 2 — How you want to build and live with it

### 4. How do you feel about carrying a UI framework?
> **ANSWERED 2026-09-19: a. None.** Chosen because it is the reversible one: A to B later is easy, B to A is not. The typing cost lands on Claude, not Chris.
- **a.** None. I will take more hand-written code for zero churn.
- **b.** A small compiled one is fine for panels and slicers, if the engine stays clean of it.
- **c.** I would rather borrow a whole chart or map library and accept its ceiling.
- *Drives:* candidate A, B, or C/D in `05`.

### 5. TypeScript or plain JavaScript?
> **SETTLED BY CLAUDE 2026-09-19, follows from your answers. Flip it any time.** b. Plain JavaScript, with type notes in comments so editors still catch mistakes. Reason: answer 4 was chosen for "no build step", and TypeScript needs one.
- **a.** TypeScript. Types catch config mistakes while writing.
- **b.** Plain JavaScript. No build step.
- *Drives:* tooling, and whether config types can be generated from the schema.

### 6. Who writes view and theme configs?
> **SETTLED BY CLAUDE 2026-09-19, follows from your answers. Flip it any time.** a now, c later. Configs are plain JSON files, kept flat enough that each could become one warehouse row. Closes no door.
- **a.** Me, by hand, in an editor.
- **b.** A settings screen, eventually.
- **c.** They come out of the warehouse as rows.
- *Drives:* how much effort goes into editor autocomplete versus a config UI. With c, configs should stay flat enough to sit in a table. Depth: `01` question 3.

---

## Group 3 — Rules of the contract

### 7. Is the layer header accepted as part of the contract?
> **SETTLED BY CLAUDE 2026-09-19, follows from your answers. Flip it any time.** a. Yes. Without it the readout cannot print a unit, and row 3 of your nine cannot be expressed.
- **a.** Yes. Units, labels, and formats travel with the table.
- **b.** No. Keep the contract to the seven columns; put units in the view.
- *Why it is a question:* the seven columns cannot say "dollars" or "per bed". Depth: `02`, the header.

### 8. What is the default when two rows share a key?
> **SETTLED BY CLAUDE 2026-09-19, follows from your answers. Flip it any time.** a. Reject and report. Reason: your own "honesty by default" rule. It is a per-load option, so any load can choose sum or last.
- **a.** Reject both and say so. The map never guesses.
- **b.** Sum them. Lets the source send one row per facility.
- **c.** Last one wins. Forgiving for quick pastes.
- *Depth:* `02`, duplicates.

### 9. How should the 2018 county list be handled?
> **SETTLED BY CLAUDE 2026-09-19, follows from your answers. Flip it any time.** c. Both. Reason: tract ids begin with their county id, so tracts need a county list of the same year. A current county file ships as the default; 2018 stays as a second registered topology; a small alias table covers Connecticut and Alaska.
- **a.** Add an alias table for the known changes: Connecticut, Alaska.
- **b.** Ship a current-year topology alongside and let the view choose.
- **c.** Both.
- **d.** Neither yet. The unmatched report is enough.
- *Why it is a question:* recent federal data will have rows that match nothing. Depth: `00` and `02`.

### 10. Where does `encoding` live: fill, dots, hatch?
> **SETTLED BY CLAUDE 2026-09-19, follows from your answers. Flip it any time.** a. Stays in the theme as your brief says. The engine refuses size encodings on rates and says why.
- **a.** Theme, as the brief says, with the engine refusing size encodings on rates.
- **b.** Theme, and each view lists which encodings it allows.
- **c.** Move it to the view.
- *Why it is a question:* dots sized by a rate mislead, and a theme swap could cause it. Depth: `03` finding 1.

---

## Group 4 — Shape of the product

### 11. Where do slicers live?
> **SETTLED BY CLAUDE 2026-09-19, follows from your answers. Flip it any time.** c. Both. `setView` first, control component second. Reason: the host is undecided, so neither can be ruled out.
- **a.** The host draws them and calls the engine.
- **b.** A separate control component ships with the engine, placeable anywhere.
- **c.** Both: a first, b as an optional extra.
- *Depth:* `01` question 10.

### 12. Which whole-system candidate?
> **ANSWERED by answer 4: A. Plain core + web component.** The A + D hybrid for non-map views stays open; it costs nothing to decide later.
- **A.** Plain core + web component.
- **B.** Compiled-framework component.
- **C.** WebGL library.
- **D.** Spec compiler onto a chart library.
- **E.** Python-side, as a prototype only.
- **A + D hybrid.** Own the map, borrow the non-map views.
- *By this point answers 1 to 4 will have narrowed this to one or two.* Depth: `05`.

---

## Housekeeping, not a design decision

- **Where does this project live?** It is currently a folder inside the Ripple repo, uncommitted. It could be its own repo. Nothing in the design depends on it.

## Deliberately not asked

- **Which host.** The brief says decide late. Every candidate except E keeps that open.
- **Which render modes ship first.** That is a backlog question for the build phase. `04` is the menu.
- **The warehouse adapter.** Out of scope, and `01` question 7 shows it is a plug by construction.
