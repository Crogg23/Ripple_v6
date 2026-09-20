# 04 — Render-Mode Feasibility

A map of the territory, not a backlog. Nothing here has been built.

## How to read the ratings

| Rating | Means |
|---|---|
| **trivial** | A few lines once the engine exists. Mostly config. |
| **moderate** | Real work, known technique, no research. |
| **hard** | Needs an algorithm, tuning, or a second rendering path. |
| **later** | Out of scope for a first release. The reason is given. |

**If SVG becomes the live renderer instead,** as in candidate D of `05`, these ratings change: film grain, paper texture, radial sun, stipple, glow, and hillshade all move to hard or out of reach. Small multiples and print get easier.

Ratings assume the leaning in `01`: a canvas map, a draw list, and a registered topology with adjacency. Where a different rendering choice would change the rating, it says so.

## The count

```
              trivial   moderate   hard   later
shape            1         5        2       2
colour           6         3        0       0
light            2         2        1       0
comparison       1         5        0       0
framing          3         2        1       0
annotation       2         2        1       0
non-map          2         3        0       0
surface          4         0        0       0
              ──────    ──────    ────    ─────
                21        22        5       2      = 50 modes
```

Two rows carry a split rating. Each is counted once, at its harder rating.

---

## Shape encodings

| Mode | Rating | Why |
|---|---|---|
| Fill choropleth | trivial | v1 already does it. |
| Centroid dots sized by value | moderate | Drawing is easy. Overlap in the dense East and a size legend are the work. Honest only for counts. |
| Contour bands | hard | Needs a smooth surface built from place centres, then contour tracing. The result ignores borders, which can mislead. |
| Hillshade or extrusion | moderate / later | Fake hillshade from value differences between neighbours: moderate. True 3D extrusion needs WebGL: later. |
| Hatching density | moderate | Canvas patterns clipped per shape. Must scale with zoom. Works in SVG export too. |
| Stipple | moderate | Random dots inside each shape, seeded so they never shimmer. Thousands of dots; needs the offscreen cache. |
| Inset bars per polygon | moderate | Easy to draw. Unreadable for small counties; needs a size cutoff or state level only. |
| Tile cartogram | moderate for states, hard for counties | States have well-known grids. 3,142 counties need an offline assignment solve, and the East scrambles. |
| Dorling cartogram | moderate | Force simulation in a worker, 1 to 3 seconds. Best cartogram for counties. |
| Continuous cartogram | later | Slow, fiddly, and ugly at county level. Better imported as a precomputed topology. |

## Colour logic

| Mode | Rating | Why |
|---|---|---|
| Sequential | trivial | Default. |
| Diverging, dark midpoint | trivial | A scale type plus a palette family. |
| Binary-then-magnitude | trivial | `zero_class` in the scale. |
| Bivariate 3×3 | moderate | Needs two layers, a 3×3 palette, and a square legend. The legend is most of the work. |
| Value plus confidence, by saturation | moderate | Colour maths is easy. Doing it in a perceptual colour space so it looks even is the care. |
| Value plus recency, by brightness | moderate | Same maths. Recency must be derived from multiple periods; see `02` finding 3. |
| Categorical | trivial | Code-to-label map in the layer header. |
| Top-N only | trivial | A highlight rule, with the rest muted. |
| Hard threshold | trivial | `scale.type: "threshold"`. |

## Light and atmosphere

| Mode | Rating | Why |
|---|---|---|
| Flat | trivial | Do nothing. |
| Radial sun | trivial | v1 has it: one gradient in soft-light blend. |
| Directional hillshade | moderate | Per-place shade from the slope toward its neighbours. Needs adjacency, which is already there. |
| Glow for statistical outliers only | moderate | The blur is v1's. The new part is the outlier rule, and the Safari blur check. |
| Edge vignette by data density | hard | "Density" needs defining, then a smooth field built from it. Risk of reading as data when it is mood. |

## Comparison layouts

| Mode | Rating | Why |
|---|---|---|
| Side-by-side | moderate | Two engine instances, a shared topology cache, linked hover, **one shared scale**. |
| Swipe | moderate | Two canvases stacked, one clipped by a draggable divider. Drag is direct manipulation, so it passes the motion rule. |
| Difference map | moderate | One map. `layer_b`, subtraction, a diverging scale. Both layers must share units. |
| Ratio map | moderate | As above, with division and a log-style diverging scale centred on 1. |
| Small multiples | moderate | Many instances. Cheap on canvas. **WebGL's context cap would make this hard.** |
| Ghost outline overlay | trivial | Stroke the highlighted set from view B over map A. |

## Framing

| Mode | Rating | Why |
|---|---|---|
| National | trivial | Fit to the topology's real box. |
| State, or any parent | trivial | v1 does it. Generalise the parent lookup. |
| Region | trivial | A named list of parents. Fit to their joint box. |
| Neighbour ring | moderate | Walk adjacency out N steps, dim the rest, fit. Alaska and Hawaii insets have no true neighbours. |
| Corridor along a path | hard | Needs a path, a buffer around it, and a test of which places it crosses. With pre-projected shapes, distances are in map units, not miles. |
| Cursor spotlight | moderate | A soft mask that follows the pointer. It is a direct response to the user, so it is legal. It must vanish when the pointer leaves. |

## Annotation

| Mode | Rating | Why |
|---|---|---|
| Auto-labels for top places | moderate | Picking the places is trivial. Stopping labels colliding is the work. |
| Margin callouts with leaders | hard | Label layout in the margins with non-crossing leader lines is a real algorithm. |
| Rank badges | moderate | Small numbered markers at place centres. Same collision problem, smaller. |
| Legend marker for the hovered place | trivial | One tick on the legend at the hovered value. High value for the effort. |
| Margin summary stats | trivial | Count, median, min, max, coverage. All already computed for the scale. |

## Non-map views of the same contract

| Mode | Rating | Why |
|---|---|---|
| Ranked strip | trivial | One thin bar per place, sorted. Same colours as the map. |
| Beeswarm | moderate | Dot layout that avoids overlap. 3,142 dots needs a fast packing pass. |
| Slope chart between two periods | moderate | Two periods, one line per place. 3,142 lines is mud; needs highlight-and-mute. |
| Sortable table | trivial | Also the accessibility equivalent of the map. **Arguably not optional.** |
| Sparkline grid | moderate | One tiny line per place across periods. Needs many periods loaded and windowed scrolling. |

**A shortcut worth knowing:** an existing chart library could draw every row in this table from the same contract. See candidate D in `05`.

## Surface

| Mode | Rating | Why |
|---|---|---|
| Film grain | trivial | One static noise tile, seeded, overlaid. Never animated. |
| Paper texture | trivial | Same, different tile, multiply blend. |
| Blueprint | trivial | A palette, a grid line pattern, a type choice. It is a theme. |
| Print-safe grayscale | trivial | A theme whose palettes are single-hue by lightness. Add hatch for roles so nothing depends on colour. |

---

## Three things the matrix shows

- **The honesty features are all cheap.** Generated legend, tie sharing, confidence marking, legend marker, summary stats: every one is trivial or moderate.
- **Everything rated hard is a layout algorithm,** not a rendering problem: contours, county tiles, corridors, callouts, density vignette. None of them change the architecture. All can wait.
- **Only one item forces a technology:** true extrusion needs WebGL. Everything else works on canvas.
