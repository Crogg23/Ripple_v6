# Warehouse Map — UI/UX audit, 2026-09-02

Deep pass over the atlas+walk build. Each finding walks its chain:
what was looked at, what's wrong, what a fix looks like. Ranked by pain.

## P0 — breaks trust or comprehension

### 1. Wire soup at mid/close zoom in dense regions
- Looked at: HEALTH at scale 0.25 and 0.6 (screenshots ux_dense, ux_close).
- Wrong: hundreds of green identity wires cross the whole region; at close zoom
  the wires dominate and the four visible cards float in a thicket. The wires
  are also drawn *under* nothing — they cross chips and cards freely.
- Fix: atlas wires visible only at mid zoom, opacity scaled down with density;
  or draw wires only on hover/selection ("show me this table's roads").
  Simplicity rule: default map shows places; roads appear when asked.

### 2. Chips overlap and clip in dense grids
- Looked at: CMS grid at scale 0.25. Chip text truncates mid-word
  (FED_CMS_DIALYS…, …_HOS), neighbors butt against each other edge to edge.
- Wrong: chip width exceeds the 640px grid pitch; long names collide.
- Fix: shorten chip label (strip FED_/ST_ prefix, cap chars with ellipsis),
  smaller font (34px), max-width, and stagger overlap by z-index on hover.

### 3. Nodes placed outside the world slab
- Looked at: min gazetteer coords = (-4757, -1482); world div starts at 0,0.
- Wrong: newly-placed UNCHARTED tables spiral out past the canvas edge —
  the dot-grid slab ends but dots keep floating on the page ground.
- Fix: normalize gazetteer coords to positive space on build (one-time shift —
  a uniform translate keeps all relative addresses identical, so permanence survives).

## P1 — costs the user real effort

### 4. LOD switches are hard pops
- Costume swaps (dot→chip→mini card) happen at exact thresholds; the whole
  map re-dresses in one frame. Disorienting; feels like a glitch not a zoom.
- Fix: crossfade via opacity transition on the two costumes near thresholds;
  or overlap bands (chips fade in 0.09–0.13 while dots fade out).

### 5. No "where am I" affordance
- After panning into UNCHARTED there is no region label in view (labels sit
  at centroids), no minimap, no compass. Easy to get lost in 22k px.
- Fix: sticky region name in the top bar ("you're in: HEALTH"), from the
  nearest centroid. A minimap is heavier; the label is the simple 80%.

### 6. Zoom control is wheel-only
- No +/- buttons, no double-click zoom, no pinch on touch, no "fit" button.
- Fix: three buttons: + / − / ⌂ fit-to-world. Double-click = zoom in one step.

### 7. Walk mode loses the map metaphor
- Walking re-lays neighbors by join strength — the same table appears at a
  different screen position than its atlas address. The two views share no
  spatial memory; the user must re-orient every time.
- Fix (cheap): after "back to atlas", flash-highlight the anchor's dot so the
  eye reconnects. Fix (deeper): draw the walk *at* the anchor's map address.

### 8. Isolated tables read as broken
- Grey dots / grey chips ("iso") with "no proven connections yet". 313 tables.
- Wrong: grey = disabled in every UI language; users will avoid them.
- Fix: normal card look with an honest badge; or a distinct "frontier"
  treatment (dashed border) that invites rather than repels.

## P2 — polish that compounds

### 9. Jump box is exact-name-only
- No fuzzy match, no human-title search ("hospital costs" finds nothing).
- Fix: match against name + title + publisher, show top 8 in a dropdown.

### 10. Hint text never changes
- "click a table to walk its streets" shows even in walk mode.
- Fix: mode-aware hint; walk mode says "click a card to expand · walk to travel".

### 11. No loading state
- 1.5 MB inline JSON parses before first paint; blank ground for a beat.
- Fix: tiny "loading the atlas…" splash; or defer atlas wires until idle.

### 12. Region label collides with content
- MONEY & POLITICS label sits behind chips at mid zoom (screenshot at_mid).
- Fix: label above the region's bounding box, not centroid; lower opacity.

### 13. Dot size carries no meaning
- All far-zoom dots equal. Size could encode connection count (hubs = towns
  vs villages) for free information at altitude.

### 14. No link/share state
- Position, zoom, mode, anchor are not in the URL hash; refresh loses place.
- Fix: encode mode+anchor+xy+scale in location.hash on idle.

### 15. Accessibility
- No keyboard navigation, no focus states, hover-only wire highlighting,
  small mono fonts. At minimum: focusable cards, Enter = walk, Esc = atlas.

## Screenshots
- ux_dense.png, ux_close.png, at_far.png, at_mid.png — scratchpad, this session.

## Suggested order
1 wire discipline, 2 chip overlap, 3 coord normalize (one build), then
4 LOD crossfade + 5 region indicator + 6 zoom buttons in one pass,
then the rest opportunistically.
