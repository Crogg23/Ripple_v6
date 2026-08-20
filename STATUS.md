# RIPPLE STATUS — 2026-08-19 — Front-door website thread opened: Webflow chosen, crash-course session queued; warehouse untouched today

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: one standing item only (unchanged).** The roll-call vote mart still
disagrees with its Python-built twin. Not touched. Warehouse state is exactly
as the 2026-08-18 evening close left it: suite 3,097 passed / 2 skipped / that
one standing failure.

---

## TODAY (2026-08-19) — planning session, zero warehouse work

New thread: the **front-door website** — a friends/family/hiring-manager-facing
intro site for Ripple. Decisions made (all Chris's calls, on researched facts):

- **Concept locked:** first-person "I had an idea..." scroll story, seven beats
  (dark screen → 178 source-dots rain in → hero numbers tick up → dots snap
  into the 4,899-connection web → one anonymous entity's footprints → mission
  + human-sign-off line → functional cards). ZERO analysis/findings shown.
- **Tool locked: Webflow, free tier first.** Won a 10-tool bake-off with live
  Aug-2026 pricing/review research. Why: $0 to learn, best-in-class scroll
  animation (GSAP-powered, free tier), and the only visual builder that
  exports real code (exit hatch to self-hosting later). Framer rejected (no
  export), Wix (buggy scroll), Squarespace/Shorthand (price), Canva/Flourish
  (can't do it), Figma Sites (messy output).
- **Division of labor:** Chris designs and owns everything in Webflow; the
  data-driven constellation pieces (beats 2/4/5) get built later as custom
  embeds by Claude Code sessions. "Living" numbers = a ~1-hour scheduled
  stats-export-to-static-file job, later; the public site never touches
  Snowflake directly.
- **First learning project:** beats 1 + 3 only, fake numbers, free tier.
- **Next session is queued:** a "Webflow for dummies" crash course. Handoff
  doc (audience, decisions, teaching arc, traps) is in the session scratchpad:
  `handoff-webflow-crash-course.md`. That session teaches; it does not build.
- Career context that shaped decisions: Chris targets analytics/insights
  engineer roles — tool choice is resume-irrelevant; the site's CONTENT (the
  warehouse story, dbt suite, data-quality war stories) is the resume asset.

## Live/open items (warehouse — all carried unchanged from 2026-08-18)

- **Nobody has read the map.** 4,899 connections, unexamined — incl. the new
  multi-cycle money→politics wiring. Still the cheapest next warehouse move.
- FEC-IDs flatten build (small; sniffer proved values live).
- FEC positional-header load-layer repair (parked; needs table-alter rights).
- 182 columns with literal 'nan' text; standing data-trap list (FAERS 76% dup,
  contracts epoch dates, NEISS future dates, SEC year-zero, 2 broken staging
  views).
- Two FDA device tables raw/unflattened (map-blind).
- ~900 gated portal tables incl. offshore-leaks (name-keyed; real decision).
- DEA numbers single-source, inert.
- Roll-call mart rebuild via Python builder (standing failure).
- Source-registry reconciliation; CourtListener citation-network retry.
- Six unparseable polygon tables; some invalid EPA/NTSB coordinates.
- Table-count discrepancy (2,216 claimed vs 1,871 live) unchased.

**YOUR MOVE:** start the Webflow crash-course session whenever ready (it boots
from the handoff doc). Separately, the warehouse open question stands: point a
session at reading the map, or at a repair.

**NEXT SESSION (website lane):** Webflow crash course per handoff doc — teach,
don't build; Chris drives.
**NEXT SESSION (warehouse lane):** read the map (politics history + enforcement
chains first) or FEC-IDs flatten / top data-trap repairs.

**Tests:** not run today (no code changed). Last known: 3,097 passed, 2
skipped, standing roll-call failure.

**COST today:** ~$1-2 (one web-research agent + chat). No warehouse compute.
