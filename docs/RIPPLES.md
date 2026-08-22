# RIPPLES — The Thinking Model

**Status: HOLY GRAIL. This is how Chris thinks about the entire warehouse from
2026-08-21 forward. Every session references this when reasoning about what to
build, measure, or hunt. It is a LENS, not a spec — no session is required to
execute it "to the letter," but every session is required to think through it.**

---

## GLOSSARY — the one vocabulary (chosen by Chris, 2026-08-21)

**Theme: WEATHER.** Ripple is a weather service for public data — we don't make
the weather, we run stations, take the same readings everywhere, and issue
warnings a human confirms. **Internal-brain language only** — for chat, docs,
and thinking. Never front-end/public-facing copy, and never code/table/file
renames (real names stay stable). "Ripple" now means exactly one thing: the
platform.

### The five pieces (the machine)

| New name | Replaces | Meaning |
|---|---|---|
| **Stations** | nouns, things | The real things we watch — facilities, owners, charities |
| **Readings** | measurements, census, counts | The same simple measurements, taken at every station |
| **Fronts** | neighbors (piece 3), wires | Connections — shared owner, address, officer |
| **Seasons** | ticks, the clock | The shared timeline; each data pull is one observation |
| **Instruments** | the rule, question, pass, sweep | A dumb question mounted once, then measuring everything automatically |

### The three lenses

| New name | Replaces | Question it answers |
|---|---|---|
| **Conditions** | Ripple 1 STATE | What is everything, right now? |
| **Systems** | Ripple 2 NEIGHBORS | What's connected — and what moves as one thing? |
| **Patterns** | Ripple 3 FLOW | What's moving, what leads what, where does it stall? |

### The actions

- **An observation** — one run of a question across everything (was: a pass, a sweep).
- **The forecast desk** — the unbuilt always-on layer: instruments reading automatically every season (piece 5's frontier).

### The outputs

| New name | Replaces | Meaning |
|---|---|---|
| **Blip** | statistical hit, queue item | Passed the luck-check but unconfirmed — a queue, never a finding |
| **Warning** | lead (queue sense) | Answered loudly, worth a human's time — a human decides if it's real |
| **Leading indicator** | "A leads B" (timing sense) | A stream that consistently moves before another |
| **Finding** | (unchanged) | A warning that survived resemblance + fronts + Chris's sign-off |
| **Dead air** | where the wave breaks, silence | The hand-off that should happen but doesn't (complaints in, enforcement never follows) |

**"Lead" is retired from the timing sense.** In chat and docs, "lead" only ever
means the old queue sense, and even that is now preferably "warning."

### The traps

- **False readings** (was: landmines) — wrong *explanations*, never forbidden
  data. Instruments should OUTPUT their confounds as readings, not silently
  control them away.
- **The climate** — the shared background rhythm (federal fiscal calendar, macro
  tide) that every instrument must subtract before a blip counts.

### Untouched older strata (load-bearing, fine as-is)

The entity spine, connection tiers, clock lanes, detectors, the 52-lens
catalogue, queue-vs-finding law. Their names stand.

---

## The core idea: through simplicity comes complexity

Conway's Game of Life: a grid of squares, alive or dead, one dumb rule
("count your neighbors"). Run it and spirals, gliders, and machines emerge that
nobody designed. The complexity was never in the pieces — **it was in what the
pieces do when they touch.**

That is the whole bet of Ripple:

> **Simple pieces. Honestly measured. Allowed to touch.
> Then the patterns draw themselves.**

This is why the nouns-first approach was right. A count is a cell. Uniform
measurement is what makes cells comparable. The elephant is eaten one bite at a
time — and **every bite is the same bite.** The sameness is the superpower:
ten thousand identical measurements don't add up, they *compound*, because each
one is comparable to every other one.

Complicated pieces can't do this. The moment a piece gets clever, it gets
incompatible, and incompatible pieces can't make spirals.

---

## The five pieces (Game of Life → Ripple translation)

| Game of Life | Ripple | Status 2026-08-21 |
|---|---|---|
| Squares | The nouns — real things (facilities, owners, permits, charities...) | Built |
| State (alive/dead) | The simple counts/measurements, taken uniformly | Built (measurement grid filled) |
| Neighbors | Connections — shared owner, address, officer, zip, inspector | Built (entity spine; coverage uneven) |
| Time (ticks) | The shared timeline; each data pull is one tick | Built (canonical clock, 2026-08) |
| **The rule** | **A question asked of every thing AND its neighbors, every tick, automatically** | **NOT built — this is the missing layer** |

A "rule" is one dumb question, asked of everything at once, every time the
clock ticks. Most squares return nothing. The squares that answer loudly are
the leads — found without knowing what you were looking for.

### The worked example (keep this — it's the whole machine in one story)

A nursing home's violations jump 3 → 9 in one tick. Alone: noise. But the rule
fires: *"when a square gets worse, what happened to its neighbors?"* Seven of
its eleven same-owner siblings also spiked, timed to the owner buying a 13th
home, while the geographically-nearby homes under other owners stayed flat.
**That pattern exists in no single row anywhere.** It only becomes visible when
simple facts + connections + time + one dumb question all touch. Nobody typed
"this owner strips staff chain-wide" into any database — it emerged.

---

## The Ripples (the lenses — each one starts simple and checks boxes)

Every Ripple is "a disturbance somewhere, spreading outward through the
record." Three are named so far. More can be added — this list is not a ceiling.

### Ripple 1 — STATE (what things are)
The census instinct. Number of X, size of X, age of X — every noun, the same
~30 questions, identically. This one is largely DONE (the measurement grid).
It is the prerequisite for everything below.

### Ripple 2 — NEIGHBORS (who touches whom)
Two distinct meanings, both real, different trust levels:

- **Touching by WIRE (literal — follow the joins).** Shared hard facts: same
  owner ID, same address, same officer. Provable, court-ready. Answers "who is
  connected to whom." Finding shape: "these 12 homes are secretly one chain."
- **Touching by RESEMBLANCE (conceptual — same shape, no join).** Zero shared
  keys, but the same behavioral signature (e.g., violations spike ~18 months
  post-acquisition, staffing goes suspiciously smooth). Neighbors in behavior
  space. Answers "who is playing the same game." Finding shape: "this isn't a
  bad company, it's a playbook — 40 unrelated companies are running it."

Resemblance is only visible because of Ripple 1's uniformity — things can only
rhyme if they were asked the same questions. **The loop: resemblance finds the
suspects, wires confirm the connections, a pattern that survives both is a
finding.** Resemblance alone is NEVER a finding — only a queue.

### Ripple 3 — FLOW (when things move, and who moves first)
The ocean picture: every stream has a rhythm; findings live where two rhythms
are offset — one stream is the other's early warning. The check-the-boxes
ladder, in order, breadth-first across all streams before deepening any:

- **Box 0 — How stale is this stream?** Reporting delay per source, measured
  FIRST. (See landmine 1 — this box is load-bearing, not hygiene.)
- **Box 1 — Does it flow at all?** Rising / falling / flat / seasonal. One word
  per stream.
- **Box 2 — What's its heartbeat?** Steady drip vs. bursts; annual dump vs.
  daily trickle.
- **Box 3 — Do two streams move together?** Co-movement only, no lead-lag yet.
- **Box 4 — Who moves FIRST?** A stream that consistently leads another is a
  free crystal ball.
- **Box 5 — Where does the wave BREAK?** Waves should flow through
  (complaints → violations → closures). Where the hand-off fails
  ("complaints spiked, enforcement never followed") is itself a finding.

The ~950 trendable columns are already inventoried in plain English
(reports/ area); the shared clock shipped 2026-08 — Box 1 is startable.

---

## The landmines (stress-tested 2026-08-21 — these are load-bearing walls, not garnish)

1. **The clock ticks ragged.** Sources land daily / annually / years late. A
   reporting lag will impersonate a real-world lead constantly. "A leads B" may
   only mean "A's paperwork gets filed faster." Box 0 (staleness per stream)
   comes before any lead-lag claim. Related: raw lags always look like they
   shrink near the present because recent events haven't finished happening —
   wait out the tail (see the time-censoring memory, 2026-08-20).
2. **Resemblance mining is a false-positive firehose.** ~950 streams means
   hundreds of thousands of pairs; thousands will dance together by pure luck.
   The boring-random-world null check is non-negotiable. Resemblance = queue,
   never finding.
3. **The neighbor web has real holes.** Only 14 connection families are
   rock-solid; the next tier is name+zip matching. Politics has zero verified
   hard links to the rest; courts / sanctions / ARCOS / ICIJ are graph dark
   matter. Ripples will dazzle where wiring is thick and go blind where it's
   thin. Never mistake well-lit for clean, or dark for fine. The method needs
   a "where can this even see" coverage overlay.
4. **A pattern is not a mechanism.** The machine's ceiling is "this pattern
   exists and here's how strong it is." Intent/mechanism is a human story on
   top, which is exactly where the human sign-off gate sits. Auto-publish
   stays blocked; the pattern is evidence, never a verdict.

---

## How sessions use this

- **It's a lens, not a checklist.** When facing any warehouse question, ask:
  which Ripple is this? What's the simplest cell/state version? Who are the
  neighbors (wire AND resemblance)? What does it look like over ticks?
- **Start simple, check boxes, breadth-first.** Same discipline as the nouns
  pass, applied to every new Ripple. Never skip to the fancy rule.
- **The rules layer (piece 5) is the standing unbuilt frontier.** Anything that
  moves toward "dumb questions asked of everything automatically, every tick"
  moves the project forward.
- **New Ripples are welcome.** State, Neighbors, Flow are the first three, not
  the last. When a new lens earns a name, it gets added here.

*Origin: Chris + Claude riff session, 2026-08-21. Chris named them Ripples.
This document changes only when Chris's thinking changes.*
