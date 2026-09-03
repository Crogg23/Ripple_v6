# Warehouse map — wow-factor audit, pass 2 (2026-09-02)

Driven with Playwright in dark mode, every state screenshotted.
Shots live in the session scratchpad: dark_open, s_far, s_close, s_roads,
s_finder, s_walk, s_walk_open. Template read line by line
(reports/viz/_build/atlas2_template.html, 595 lines).

## What was checked, what a hit means

Each finding: the check, what seeing it means, severity for a portfolio viewer.

### A. Atlas findings

**A1 — Uncharted owns the center. (blocker)**
Check: dark_open.png. The grey UNCHARTED cluster is the largest, most central
mass; the 8 colored regions are small satellites at the edges.
Means: the first frame says "mostly unknown grey stuff." The warehouse's
actual richness — FEC, CMS, EPA, IRS — reads as periphery.
Fix direction: invert the geography. Colored regions center-stage,
uncharted pushed to a dim outer rim, or shrunk + faded.

**A2 — Hover roads are invisible at far zoom. (bug)**
Check: hovered a node at fit zoom (s_roads.png) — no roads visible; shot is
pixel-identical to the resting state.
Mechanism: `.awire` is stroke-width 6, opacity .4. Fit scale is ~0.07, so
drawn width is ~0.4px. The feature exists but cannot be seen exactly where
users start.
Fix: scale-compensated stroke (divide by scale, or vector-effect).

**A3 — z-close is a raw starburst. (blocker)**
Check: s_close.png. At close zoom the mycelium threads render as dozens of
straight thin rays converging on the district hub, with mini-cards floating
on top. Reads as a wireframe debug view, not fungus.
Mechanism: `.mycl` curve offset is only 0.12 of the segment — visually
straight; `body.z-close .mycl` thins to 2px but stays full-length.
Fix: real organic curves (multi-segment, wandering), fade threads near
close zoom, or draw hyphae texture instead of hub-spokes.

**A4 — No title, no numbers, no story. (blocker for portfolio)**
Check: every atlas shot. Nothing on screen says what this is, how big it is,
or why it's impressive. Splash is the plain text "loading the atlas…".
A portfolio viewer gets a scatter of dots and a search box.
Fix: opening title card + count-up (567 tables · 4,215 proven joins ·
8 regions), region stat chips, maybe a "tour" affordance.

**A5 — Region labels whisper; hierarchy is flat.**
Check: dark_open.png. Region names are ~11px equivalent grey caps; district
labels only appear at mid zoom at 0.6 opacity. Nothing pulls the eye.
Fix: type scale with real display weight at far zoom, region color in the
label, size proportional to table count.

**A6 — Nothing moves.**
Check: template has zero animation beyond a 3-blink flash and .25s
crossfades. No ambient life, no transition between atlas and walk —
enterWalk() teleports (innerHTML swap + instant transform).
Fix: ambient shimmer on dots, slow thread pulse, and an animated camera
dive on click-to-walk. Respect prefers-reduced-motion.

### B. Walk-mode findings

**B1 — Walk mode is monochrome. (blocker)**
Check: s_walk.png. Every card is the same dark slab with a green top edge;
region colors vanish entirely. The wire-color legend (green/gold/grey)
is nearly imperceptible at 1px stroke on dark.
Fix: carry the region color into each card's edge/eyebrow; fatten and
glow the wires by class; group neighbors into labeled arcs by join type.

**B2 — Anchor card is a wall.**
Check: s_walk.png. FED_FAC_SINGLE_AUDIT shows ~25 column rows of 10px mono
at once. Dense block, violates the everything-collapses principle the
neighbors follow.
Fix: collapse the anchor's columns too — joinable hoisted + "show all".

**B3 — Entry is a teleport, exit is a teleport.**
Check: code path enterWalk/enterAtlas — instant swap. The handoff's
"cinematic fly-down" is entirely absent.

**B4 — Dead space and no orientation.**
Check: s_walk.png. Cards scatter to fill 1600×900 with huge gaps; nothing
says which direction the strong joins are, no ring/orbit reading. The
"+ N weaker connections not drawn" note is a floating whisper.

### C. Code-level notes

- Duplicate `focusin` handler pasted twice (template lines 559–570).
- `showRoads` ignores the relation type — all roads draw accent green,
  so the wire-color language doesn't exist in the atlas at all.
- LOD thresholds: far <0.07, mid 0.07–0.32, close ≥0.32. Fit lands at
  ~0.07 — right on the far/mid boundary; first wheel tick flips costumes,
  which reads as flicker.
- DOM budget: 567 anodes × 3 costumes + panels + labels ≈ 2K positioned
  elements. Fine static; ambient animation should target transform/opacity
  only, or move dots to one canvas layer at z-far.
- Walk render is O(neighbors²) for cross-wires — MAXN 80 caps it; fine.

## Fix history from pass 1 (already done this session)

- Build files rescued from the dying scratchpad into reports/viz/_build/:
  build_atlas4.py, build_walk.py, atlas2_template.html, shot.py.
- reports/viz/atlas.html verified byte-identical to the published artifact
  (same 1,637,360 bytes, same timestamp).

## Wow-pass-1 build log (2026-09-02, later the same day)

Shipped steps 1-4 as build_atlas5.py + atlas3_template.html, published as
wow-pass-1 then wow-pass-1b. Skeptic verified all seven build claims in code;
its findings and my responses:

- Hash-skip was too narrow: any hash now skips the intro. Fixed.
- Flash pulse ignored reduced-motion. Fixed.
- Road stroke cap of 18 bound at the default fit scale 0.032, drawing
  1.7px roads. Raised to 34; verified by screenshot, roads read clearly.
- Dense-hover check by screenshot: 97-connection node at z-close was a
  grey wall from fuzzy halos. Fuzzy roads thinned to 1.6px base, halos
  removed for fuzzy class. Verified by second screenshot.
- Edge count: 3,927 post-twin-merge symmetric edges, not the pre-merge
  4,215. Skeptic confirmed adjacency is fully symmetric and the halving
  is honest.
- stats.regions = 7 excludes UNCHARTED on purpose; map draws 8 circles.
- Open question for Chris, not a bug: UNCHARTED holds 361 of 567 tables
  at radius 13,004 — double the largest colored region. The default frame
  crops it to a dim sliver on the right; 313 zero-edge frontier tables
  live mostly there. A viewer who never pans right never sees two thirds
  of the warehouse. Options: leave as designed, add a "frontier" affordance
  in the story layer, or split uncharted into arcs around the core.

## UX pass log (2026-09-02, after Chris's redirect)

Chris: "less performative and sales pitch and more focused on user
experience" then "entirely drop. And then ENHANCE." Saved as a feedback
memory. Shipped as ux-pass then ux-pass-2:

- Intro overlay deleted wholesale: markup, CSS, count-up JS. Stats moved
  to the always-on top badge.
- Eased camera: tweenTo with easeInOutCubic; zoom buttons 260ms,
  dblclick 320ms, fit 480ms; wheel stays direct; any pointer or wheel
  input cancels a running tween.
- Walk entry: clicking a table tweens the camera to it over 520ms, then
  walk mode crossfades in. Hash-restored walk entries skip the flight.
- Anchor card collapses to 10 columns with a show-all toggle.
- Mycelium at close zoom dimmed to .14 and stilled — the Esc-back ray
  web regression, caught by screenshot.

Skeptic round 2 disagreed on three, all confirmed real and fixed:

- Boot still tweened 480ms from the top-left corner because mode
  initialised to 'atlas', making wasAtlas true on first call. mode now
  starts empty; first paint verified at 150ms as the fitted frame.
- Walk-hash restore: the boot enterAtlas tween kept writing the camera
  for 480ms after the hash coords were applied, landing on atlas fit
  with the cards off-screen. doSwap now cancels tweens; verified stable
  at #w restore, transform identical at 900ms and 1600ms.
- show-all advertised n.c.length + n.x columns but the payload caps at
  40 per table, so 109 tables promised columns the page cannot show.
  Label now uses n.c.length; the truncation note lives inside the
  expansion. HMDA-class tables read honestly again.

## Walk pass log (2026-09-02, "keep going. Make this amzing")

walk-pass: jline on every neighbor card with join key, rate, and a
plain-words reason per class; region-colored dot on every card name;
"just visited" badge with dashed outline on the card you came from;
anchor footer join-mix summary. Verified by screenshot, zero JS errors.

Skeptic agreed on all seven claims and surfaced two data honesty gaps
the new jline exposed, both fixed in walk-pass-2:

- 466 of 7,854 edges carry rate > 100, peak 952.7 — fanout artifacts,
  not match rates. Jline now reads "fans out — one row matches many".
- 660 edges carry rate 0. Jline reads "no overlap in the sample", and
  the neighbor sort demotes both classes so they cannot lead the bloom.
- "just visited" now tracks the actual prior anchor via lastAnchor,
  correct through crumb navigation, cleared on atlas return.

Known and accepted: on the 22 nodes with degree > 80, the arrival card
can fall outside the drawn slice — pre-existing, noted by the skeptic.

## Walk pass 3 log (2026-09-02, autonomous run)

- Ring labels: a small colored chip marks where each join-class band
  begins in the bloom, with its count. Placed at the first card of each
  class; verified visible in dark and light screenshots.
- Where-am-I chip now reads "region · N tables".
- Uncharted panel subtitle: "N sources · region not yet assigned" —
  honest about what uncharted means; some of those tables join fine.
- Light theme verified by screenshot for atlas and walk. Both hold.
- Published as walk-pass-3. Zero JS errors across all drives.

## Performance probe (2026-09-02)

Headless Chromium, 1600x900, dark, full animation load: 559 pulsing
mycelium paths + 567 breathing dots. Measured via rAF count over 2s.

- Idle at the default fit: 60.2 fps.
- Continuous wheel zooming: 47.3 fps.

Headless software rendering is the floor; real GPUs land higher. No
canvas rewrite needed at this node count. If effects grow, the far-view
dots are the first candidates for a single canvas layer.

## Session-wide skeptic + walk-pass-4 (2026-09-02, final)

Session skeptic verdict: all seven spot-checks agree, node --check clean,
no unmatched braces, no dead ids, audit report matches code. Four gaps
found; three fixed in walk-pass-4, one accepted:

- 1,024 of 7,854 edges carry no recorded join columns. Cards showed a
  key and rate but no "Joinable" group. Now they say "join columns not
  recorded for this pair".
- Footer read "KEY · 0% · CORROBORATED" beside a jline saying no
  overlap — a visual contradiction. Footer now uses the same honest
  words: "fans out" and "no overlap".
- The top-80 neighbor slice was picked by raw rate, letting fanout
  edges claim seats. The slice sort now demotes rate 0 and rate > 100,
  same as the display sort. 53 of 1,760 drawn cards were affected.
- Accepted, not fixed: whereami mislabels 1 node of 567 — nearest
  panel center ignores radius. FED_USGS_WATER reads as HEALTH.

Also fixed from the skeptic's declared blind spot: the fly-to-walk
flight ended at a different scale than walk mode opens at, causing a
zoom pop on arrival. The flight now lands at exactly walk scale 0.5.

Published as walk-pass-4. Full drive re-verified: zero JS errors.

Open for Chris: the badge counts 7 regions while 361 of 567 tables sit
in the uncharted rim outside that number. Flagged twice by skeptics.

## Web pass log (2026-09-02, "you are not able to grasp the size")

Chris's critique: the map hid the warehouse's size and interconnection.
He was right — roads drew on hover only, one table at a time, and the
default frame cropped the uncharted rim out entirely.

web-pass: all proven edges drawn at rest as an always-on web, colored
by join type, opacity by health, scale-compensated strokes. Region-pair
trunk arteries under the web, width by join count, 24 cross-region
pairs totaling 2,018 joins. Default open fits the whole world. The web
fades at mid and close zoom so reading stays clean. Payload 1.72MB.
FPS: 60 idle, 24 during continuous zoom, headless floor.

Skeptic on web-pass: dedupe clean, sets identical between Python and
JS, trunks reconcile exactly, layers ordered right. One real defect and
one honesty finding, both fixed in web-pass-2:

- The badge said 3,927 joins; the SVG draws 3,924. Six self-loops in
  the adjacency became three phantom edges under the divide-by-two
  count. Count now taken from the drawn edge list. Self-looped tables:
  CMS_POS_OTHER, FDIC_BANK_DATA, GLEIF, COURTLISTENER_COURTS,
  FMCSA_COMPANY_CENSUS, HUD_FHA_SF_PORTFOLIO_SNAPSHOT.
- 313 of 567 tables have zero proven joins; uncharted's 361 include
  just 72 connected. The badge now says "254 joined in" so the picture
  stops flattering the answer.
- Minor: stroke cap 34 vs 1/scale 40 at full fit thinned the web 15%.
  Cap raised to 42.

## Organism pass log (2026-09-02, the Erie Railroad references)

Chris shared two references: the 1855 New York & Erie Railroad org
diagram and a radial timeline poster. What they share: ONE structure
from ONE center, density as texture, engraved hairlines, everything
attached. The old map was eight separate blobs — that was the miss.

New layout engine build_atlas6.py, same template and interactions:

- Single root at world center. Every district is a limb radiating
  outward, angle sector proportional to region table count, limb
  length by district size with staggered depth.
- Tables are berries on their district's frond; berry stems and limbs
  are the mycelium skeleton, now scale-compensated and 3x brighter.
- Concentric hairline rings and a root disc, echoing both references.
- The join web stays as a faint under-glow: opacity .09/.025.
- Frontier fix mid-pass: 289 zero-edge tables drew as hollow rings,
  10px world borders — invisible at far zoom. Now filled berries at
  half opacity; base berry size raised 110 to 170 world px.
- Uncharted label placed by limb centroid angle, not sector mid.
- Region colors kept for now; the references are monochrome ivory —
  open question for Chris below.
- Gazetteer regenerated: every table has a NEW permanent address.
  Old spatial memory is reset — the price of the re-lay.
- Published as organism-pass. Full drive: zero JS errors.

Open for Chris: keep the region color language, or commit to the
references' engraved monochrome — one ink on charcoal, region told by
sector labels alone.

## Gravity settle log (2026-09-02, option A of the CA five)

Chris riffed cellular automata; five options proposed and saved to
memory as project-map-emergence-options. He picked A: gravity settle.

build_atlas7.py, numpy force simulation over the 254 connected tables:

- Springs on all 3,924 edges, weight 1.0 for healthy rates and 0.25
  for fanout or zero-rate edges, so weak evidence pulls weakly.
- Repulsion between every pair, gentle center gravity, 900 ticks with
  linear cooling, clipped steps, fixed seed 42 — deterministic, so
  permanence survives reruns as long as the edge list is unchanged.
- Scale set by the 92nd percentile radius; outliers reined to 16,500.
- The 313 unjoined tables ring the settled core in three staggered
  rows, ordered by region — a visible halo of what awaits joining.
- Tuning round: first run overpacked the nucleus. REP 9 to 30,
  GRAV .015 to .010, percentile scaling added. Second frame verified.
- Districts, mycelium skeleton, rings all empty in this layout; the
  join web itself is the structure, opacity restored to .20/.05.
- What emerged, unprompted: CMS pink cluster, SEC blue block, FEC
  green nucleus, gold geography arteries, one grey PCAOB islet.
- Published as gravity-settle. Payload 1.70MB.

Tradeoff for Chris: the settle discards the curated region geography.
Regions now interleave where the joins actually interleave — truer,
less tidy. Old organism-pass survives in git and build_atlas6.py.

## Gravity tuning + genesis replay (2026-09-02, continued)

Chris: still crowded in the center. Two tuning rounds:

- Rest-length springs with degree-normalized pull: FAILED, collapsed
  tighter — the halo gap grew and the core shrank. Reverted approach.
- ForceAtlas-style mass repulsion: repulsion weighted by the degree
  product of both endpoints to the 0.75, hub spring pull damped by
  min-degree to the 0.35. WORKED — CMS sheet, SEC lattice, and EPA
  bridges spread into readable neighborhoods. gravity-settle-2.

Option B shipped as genesis-replay:

- Breadth-first generations from the highest-degree hub; disconnected
  components seed at their own top hub; isolates get the final
  generation. 23 generations, computed at boot, baked into styles.
- The zoomer's new replay button plays birth as staggered pop-ins,
  edges lighting one beat after their later endpoint. ~11 seconds.
- Guarded by prefers-reduced-motion no-preference; user-triggered
  only, honoring the no-performative-intro rule.
- Web edge generations matched to nodes by rounded coordinate key —
  gaz stores tenths, aweb stores ints; both sides now Math.round.
- Verified by staged screenshots at 0.7s, 2.1s, 5.6s: seed
  neighborhood first, core assembled, halo last. Zero JS errors.

## Heartbeat pass log (2026-09-02, "take more initiative")

Option D plus resting-state visual differentiation, shipped as
heartbeat:

- Hover pulse: BFS three hops from the hovered table computed live,
  edges classed hp1/hp2/hp3 with staggered transition delays, all
  unrelated edges dimmed to .015. Web paths gained data-a/data-b
  endpoint names, matched by rounded coordinates.
- Hubs as suns: dot diameter and glow now scale with degree at double
  the old rate, so FEC and EPA hubs visibly anchor their clusters.
- Organic edges: every web curve gets a deterministic bow of 0.10 to
  0.24 with random sign, replacing near-straight lines.
- Tried and cut: ambient opacity shimmer on the 1,734 strong edges.
  Idle fps fell 60 to 20, zooming to 3.8. Removed; verified restored
  at 60.3 idle, 31.3 zooming.
- Verified by hover screenshot: three-hop reach lights bright green
  against a dimmed field. Zero JS errors.

## Heartbeat skeptic round (2026-09-02) — one blocker, fixed

Skeptic DISAGREED, rightly. The chain of the blocker:

- Build emitted edge endpoints as Python round() ints — half-to-even.
- Template matched them against JS Math.round() keys — half-up.
- Gazetteer stores tenths, so exact .5 coords are common: 105 nodes.
- 52 nodes never matched; 889 of 3,924 edges — 22.7% — could not
  pulse, and fell to generation 0 in the genesis replay.
- Worst case user-visible: FED_EPA_FRS_FRS_PROGRAM_LINKS, degree 112,
  went fully dark on hover while dimming everything else.
- My screenshots missed it: I verified a healthy node. A good-node
  screenshot proves nothing about the broken 52. Lesson logged.

Fix shipped as heartbeat-3: aweb now carries table names, the
coordinate round-trip is deleted. Verified in the browser: zero
unresolvable endpoints, the once-dark hub lights 2,521 neighborhood
edges, walk round-trips clear the dim, hop-3-to-hop-3 edges excluded.
Payload 1.96MB. Also fixed from the same round: enterWalk and
enterAtlas now clear any active pulse.

## Cosmos engine swap (2026-09-02, "engine")

Chris asked about tools; verdict was keep our map, borrow the MIT
engine. He said "engine". Shipped as cosmos-engine:

- New template atlas4_template.html; the DOM version stays intact in
  atlas3_template.html. build_atlas7.py takes the template as an arg.
- Engine: @cosmos.gl/graph 3.4.1, the WebGL engine behind Cosmograph,
  MIT licensed. The jsdelivr ESM route died on a luma.gl duplicate
  version clash; the fix was the package's self-contained UMD bundle,
  dist/index.min.js, global Cosmos, one classic script tag — inside
  the artifact CSP allowlist.
- Atlas renders as GPU points and links: settled positions normalized
  to cosmos space, region colors read live from CSS vars so the canvas
  matches the theme, degree-scaled sizes, engine hover ring.
- Heartbeat pulse is now a GPU recolor: three-hop BFS writes new
  point and link alpha arrays, restored on mouse-out or walk entry.
- Genesis replay is a GPU alpha animation over the same generations.
- Hub and region labels float as DOM chips repositioned on every
  zoom via spaceToScreenPosition.
- Tooltip on hover: table name, human title, join count, walk cue.
- Walk mode is byte-for-byte the DOM card system; wheel and pointer
  handlers gate on mode so the canvas owns atlas gestures.
- Verified: pulse recolor, walk entry, Esc return, genesis run, all
  by driven screenshot, zero page errors. Exploration CSVs for the
  Cosmograph app also live at reports/viz/cosmograph_edges.csv and
  cosmograph_nodes.csv, 3,924 edges and 567 nodes.

## Cosmos skeptic round (2026-09-02) — two real, both fixed

- Tooltip pinned to viewport 0,0: the engine's mouse-over event
  carries no clientX in this build, so the position branch never
  fired. Fix: a passive mousemove listener tracks the cursor; the
  tooltip uses it as fallback. Verified: tooltip at 839,447 beside a
  mouse at 823,433.
- CDN as single point of failure: a blocked jsdelivr killed the whole
  script at the Cosmos global. Fix: HASGL guard, a Proxy stub graph,
  a one-line notice in the atlas, finder routes straight to walk.
  Verified with the CDN deliberately blocked: search into walk mode
  works fully, zero errors.
- Accepted minors from the same round: theme flips after load do not
  recolor the canvas; region labels can overlap at far zoom; hover
  during a genesis replay is invisible until it ends; atlas camera
  no longer survives reload since the atlas hash was dropped.
- Published as cosmos-engine-2.

## The swing plan, refined by this pass

Order matters — A2/A3 fixes make the canvas worth animating first.

1. **Recenter the world** — colored regions in, uncharted to the rim (A1).
2. **Fix the broken beauty** — scale-aware roads, organic threads,
   LOD threshold nudge, road colors by join type (A2, A3, C).
3. **Opening cinematic** — title card, count-up numbers, staged region
   light-up, fly-in (A4, A6).
4. **Living fungus** — shimmer, pulse, hover ripple (A6).
5. **Cinematic walk** — camera dive in/out, colored + grouped neighbor
   blooms, collapsed anchor (B1–B4).
6. **Story layer** — region stat chips, hero numbers, guided tour (A4).
