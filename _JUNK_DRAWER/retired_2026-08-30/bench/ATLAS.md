# THE ATLAS

### Plotly 6.9.0, mapped by the question you walked in with

You never arrive at a chart library knowing you want a "parallel categories diagram." You arrive holding **a pile of columns and a question**. This document is filed that way: question first, data shape second, chart name last.

**Verified on this machine:** plotly 6.9.0 (bundling plotly.js 3.7.0), pandas 2.3.3, numpy 2.5.1, matplotlib 3.11.1, dash 4.4.1, Python 3.14.6, Windows. **Every number in this document came out of running code against this install** — either in the corpus sweeps this atlas was built from, or re-run while writing it. Nothing is remembered or estimated.

**Not installed here** (each confirmed by a failed import): `kaleido` (so no PNG/SVG/PDF export), `scipy`, `statsmodels`, `anywidget`, `scikit-image`, `plotly-geo`, `networkx`, `orjson`. What that blocks, and what to do instead, is in §6.

**Tiers used throughout:**

| Tier | Means |
|---|---|
| **DAILY** | You will use it most weeks. Learn it cold. |
| **REACH-FOR** | A few times a quarter, when the obvious chart isn't answering the question. Worth knowing it exists so you recognise the shape when your data looks like that. |
| **SPECIALIST** | Correct answer for one narrow data shape or one trade. Don't go hunting for an excuse to use it. |

---

# 1. THE WHOLE THING IN ONE PAGE

## 1.1 Six buckets, and only two of them change

A Plotly figure is a plain Python dictionary with two keys — `fig.to_dict().keys()` returns `['data', 'layout']` — plus an optional third, `frames`.

- **`data`** is a list of **traces**. A trace is one drawn thing: one set of bars, one line, one cloud of dots, one map layer. It carries your numbers *and* the styling of the marks that show them.
- **`layout`** is everything that is not a mark: the axes, the words, the legend, the colour rules, the panels, the buttons, and what happens when a human touches the chart.
- **`frames`** are snapshots, used for animation.

Every property in the library falls into one of six buckets:

| Bucket | What it decides | Lives on | Changes per chart type? |
|---|---|---|---|
| **DATA** | which columns become which channel — `x`, `y`, `z`, `labels`, `parents`, `lat`, `lon`, `values`, `dimensions`, `link` | the **trace** | **yes** |
| **MARK** | what the drawn thing looks like — `marker`, `line`, `fill`, `text`, `opacity`, `mode` | the **trace** | **yes** (but mostly shared, see §5) |
| **SCALE** | how numbers and categories map to space and colour — axes, ranges, tick formats, colour scales | **layout** | **no** |
| **FRAME** | everything around and behind the data — title, legend, margins, background, annotations, shapes, panel grid | **layout** | **no** |
| **INTERACTION** | what happens when a human hovers, clicks, drags, or presses a button | **layout** | **no** |
| **MOTION** | animation — how one state becomes the next | **layout** + `frames` | **no** |

**The whole point of this page:** SCALE, FRAME, INTERACTION and MOTION are **identical for every chart type in the library**. A bar chart and a sankey diagram and a 3D surface all share exactly the same title object, the same legend object, the same annotation object, the same hover machinery. You learn that once. Forever.

## 1.2 The counts that prove it

Measured this session (`go.Layout()._valid_props`, `go.<Trace>()._valid_props`, and a full walk of both trees):

| Thing | Count |
|---|---|
| Trace types registered (`go.Figure()._data_validator.class_strs_map`) | **49** |
| Trace types that are live (3 `*mapbox` ones are deprecated) | **46** |
| Distinct property names across all 46 live traces | **340** (280 once you drop the `*src` twins — see §5.3) |
| Total trace property slots across all 46 | **2,549** |
| Average top-level properties on one trace type | **55.4** (biggest: `box` 88 · smallest: `indicator` 24) |
| Property names that belong to exactly one trace type | **90** non-`src` (117 if you count the `*src` twins) |
| Trace types with **zero** properties of their own | **20 of 46** |
| Top-level properties on `layout` | **98** |
| Top-level properties on one axis (`layout.xaxis`) | **97** |
| Every setting under `layout`, all the way down | **2,488** |
| Every setting under all 46 traces, all the way down | **9,835** |

Read those last four together and the shape of the library is obvious: **the chart-type list is the small half.** One x-axis alone has more settings (97) than the average chart type has in total (55.4).

## 1.3 Where layout's 2,488 settings go

| Bucket | Nodes | Share |
|---|---|---|
| **FRAME** — everything around and behind the data | 1,012 | 40.7% |
| **SCALE** — how numbers and categories map to space | 884 | 35.5% |
| **INTERACTION** — what happens when a human touches it | 478 | 19.2% |
| *STATE* — bookkeeping that isn't visual (`template`, `uirevision`, `meta`) | 78 | 3.1% |
| *TRACE-MODE* — the handful of layout knobs that arrange traces (`barmode`, `boxgap`…) | 19 | 0.8% |
| **MOTION** — animation | 10 | 0.4% |
| *SUBPLOT* — the seven alternate-coordinate roots (`scene`, `polar`, `geo`…) | 7 | 0.3% |

At the top level, all **98** `layout` properties sort cleanly into the same buckets (hand-assigned name by name, verified to cover all 98 with no leftovers and no duplicates):

**FRAME 23 · INTERACTION 22 · SCALE 18 · TRACE-MODE 18 · STATE 9 · SUBPLOT 7 · MOTION 1**

Two facts fall straight out of that:

1. **Layout barely knows which chart you drew.** Exactly **18 of 98** top-level properties (`barmode`, `bargap`, `boxmode`, `violinmode`, `funnelmode`, `waterfallmode`, `scattermode`, and their `*gap` partners) are the only place layout acknowledges the chart type at all. Everything else applies to everything.
2. **Animation is almost nothing.** `layout.transition` is 1 property (3 settings inside it). The whole of motion is 10 of 2,488 nodes. The actual frames live on the figure in `go.Frame`, which has exactly **6** properties.

## 1.4 The arithmetic that makes the rest of this document small

- Learn the shared layout surface once: **195 names** — 98 on `layout` + 97 on an axis (§4).
- Of those, about **20** are what you touch on nearly every chart (§4.1).
- Then each new chart type costs you, on average: **55.4** top-level properties, of which only **14** are names you haven't already met if you know `scatter` and `bar`, and only **2** exist nowhere else in the library (90 one-offs ÷ 46 trace types = 1.96).
- Learn `scatter` + `bar` alone (88 names between them) and you already cover **74.0%** of the average chart type — worst case in the whole library is 50.9%. **Nothing is less than half-covered.**

*Averaging note:* the **74.0%** and the **14** are means across all **46** live trace types, which includes `scatter` and `bar` themselves (trivially 100% covered, 0 new names). Drop those two and average over the other 44 and the honest figures are **72.9%** covered and **14.7** new names — a slightly worse deal, same conclusion. Every other percentage in this document uses the 46 denominator too.

So: **one shared layout, plus about sixty new words per new chart type, of which two are genuinely new ideas.** That is the whole library.

## 1.5 Words this atlas uses

The reader is assumed to know SQL and basic pandas and to have made a bar chart. Everything else gets translated here, once.

| Word | Plain English |
|---|---|
| **trace** | One drawn series inside a figure — one set of bars, one line. A figure holds a list of them. |
| **layout** | The one object holding everything that isn't a mark: axes, titles, legend, colours, buttons. |
| **mark** | The physical thing on screen that stands for a row — a bar, a dot, a wedge, a ribbon. |
| **data shape** | Which columns you actually have and how many rows per thing. This, not the chart name, is what picks the chart. |
| **long-form / wide-form** | Long = one row per observation with a category column (`state, year, amount`). Wide = one column per series (`year, north, south`). Plotly Express takes both; the labels come out different (§2.3). |
| **domain trace** | A chart that owns a rectangle of the page instead of sitting on x/y axes — pie, sankey, table, treemap, indicator and five others. This is why "set the y-axis title on my pie" has no answer: a pie has no y-axis. |
| **ECDF** | "Empirical cumulative distribution function." A staircase line: at any value on the x-axis, its height tells you what share of your rows are at or below that value. No bins, no arguments about bin width. |
| **KDE** | "Kernel density estimate." A smoothed curve drawn through a pile of values to show its shape — a histogram with the steps sanded off. It's what makes a violin plot's outline. |
| **rug** | A thin strip of tick marks, one per row, drawn along an axis. Shows exactly where each individual value sits under a summary chart. |
| **jitter** | Nudging points sideways at random so ones with the same value stop landing on top of each other. |
| **quartiles / IQR** | Sort your values; Q1 is the value a quarter of the way up, the median is halfway, Q3 is three-quarters. The box of a box plot spans Q1→Q3; that span is the "interquartile range." |
| **power law** | A pattern where a few things are enormous and almost everything is tiny — money, contracts, donations. On a log-log chart a power law draws as a straight line, which is why a bend in that line is worth looking at. |
| **z-score** | How many standard deviations a value sits from the average. `abs(z) > 3` is a common "this is weird" rule. |
| **sparkline** | A tiny line chart with no axes, sat next to a number to show its recent trend. |
| **WebGL** | Drawing with the graphics card instead of with SVG shapes. Handles far more points; slightly fewer styling options; exports as pixels not vectors. |
| **d3 format string** | The mini-language for number and date formatting inside Plotly — `,.0f` = `1,234`, `$,.2f` = `$1,234.50`, `.1%` = `12.3%`, `%b %Y` = `Aug 2026`. |
| **Jaccard similarity** | A 0–1 score for how much two chart types' vocabularies overlap: shared property names ÷ combined property names. 1.0 = identical, 0 = nothing in common. Used in §5.5. |
| **`px` vs `go`** | `px` = `plotly.express`, one line per chart, does the dataframe work for you. `go` = `plotly.graph_objects`, one object per trace, total control. **They are not a fork in the road — `px` returns a `go.Figure` you can keep editing.** |

---

# 2. PICK BY QUESTION, NOT BY NAME

## 2.1 The ten questions

Every chart in the library answers one of these. Find yours, then find the row in §2.2 whose *data shape* matches the columns you actually have.

| Question | You're asking |
|---|---|
| **COMPARE** | which one is bigger? |
| **DISTRIBUTE** | how is it spread out? |
| **RELATE** | does X track Y? |
| **COMPOSE** | what is it made of? |
| **FLOW** | what moves where? |
| **RANK** | who's on top, and did it change? |
| **LOCATE** | where? |
| **CHANGE** | what happened over time? |
| **CONNECT** | what links to what? |
| **SINGLE VALUE** | one number that matters |

## 2.2 The lookup table

`px.*` = one line, hands it a dataframe. `go.*` = you build the trace. Where a cell says "build it," the recipe is in §3.2.

### COMPARE — which one is bigger?

| I have | I want to know | Start here (DAILY) | If that's not answering it (REACH-FOR) | Narrow cases (SPECIALIST) |
|---|---|---|---|---|
| one label column + one number, up to ~25 rows | which is biggest, and by how much? | `px.bar` + `.update_xaxes(categoryorder='total descending')` | `px.bar(orientation='h')` when labels are long words | `px.bar_polar` if the label is a compass direction or an hour |
| one label + one number, **hundreds or thousands of rows** | which is biggest — *and* how concentrated is the total? | `px.ecdf` (see DISTRIBUTE) **plus** `px.box` | `px.treemap` for the whole population at once | `px.strip` to name the outliers individually |
| one label + one number, **not yet aggregated** (many rows per label) | which label totals the most? | `px.histogram(x='label', y='num', histfunc='sum')` — a GROUP BY with no SQL | `df.groupby(...).sum()` then `px.bar` (a Series plots directly) | — |
| **two** label columns + one number | which combination runs hot? | `px.imshow` (grid you already pivoted) or `go.Heatmap` | `px.bar(barmode='group')` when one of the two has ≤4 levels | `px.parallel_categories` when there are 3+ label columns |
| one label + **two** numbers (before/after, budget/actual) | who moved the most? | dumbbell — 2 × `go.Scatter` + connecting shapes (build it) | slope chart — `px.line` across two dates | `go.Waterfall` when it's one entity's pieces, not many entities |
| one label + one number + a **target** | is it over the line? | `px.bar` + `fig.add_hline(y=target, annotation_text='cap')` | `go.Indicator(mode='number+gauge')` for one entity | `ff.create_bullet` for a target-vs-actual row |
| one category + one number with many rows each | which group runs higher, and who has wild outliers? | `px.box` | `px.violin` when you suspect two humps | `px.strip` under ~50 rows per group |

### DISTRIBUTE — how is it spread out?

| I have | I want to know | Start here (DAILY) | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| one number column, many rows | what's typical, how wide, how lopsided? | `px.histogram` (add `marginal='box'`) | `px.ecdf` — no bins to argue about | `px.violin` for the silhouette |
| one number, **thousands of entities, money-shaped** | what share sit above any threshold I pick? | **`px.ecdf(ecdfmode='complementary', log_x=True, log_y=True)`** — a power law draws as a straight line; a kink is an anomaly you see with your eyes | `px.box(points='suspectedoutliers')` | `px.histogram(log_y=True)` |
| one number + one category, ≤10 groups | whose spread is wider, and who has extremes? | `px.box` | `px.violin(box=True)` | `px.strip` when the individual rows are the point |
| one number + one category, 5–40 groups | how does the *shape* shift down the list? | ridgeline — stacked `go.Violin(side='positive')` with `violingap=0` (build it) | `px.box` with `categoryorder` | `px.imshow` of a binned grid |
| one number + one category, few rows per group | where is every single row? | `px.strip` (+ `customdata` so hovering names it) | `px.box(points='all')` | beeswarm — jittered strip (build it) |
| **two** numbers, 10k+ rows, the scatter is a black blob | where is the crowd actually piled up? | `px.density_heatmap` | `px.density_contour` for two overlapping groups | `go.Scattergl` when each point must stay hoverable |
| percentiles **already computed in SQL** | the same box plot, 400× smaller over the wire | `go.Box(q1=…, median=…, q3=…, lowerfence=…, upperfence=…)` | — | — |

### RELATE — does X track Y?

| I have | I want to know | Start here | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| two number columns, one row per thing | do they move together, and who are the weirdos? | `px.scatter` | `trendline='rolling'` / `'ewm'` / `'expanding'` (these work; `'ols'`/`'lowess'` need statsmodels, absent here) | `px.scatter(marginal_x=…, marginal_y=…)` for distributions on the edges |
| 3–8 number columns, no hypothesis yet | which *pairs* are related at all? | `px.scatter_matrix` | `px.imshow(df.corr(), text_auto=True)` — labels come free from the index | `showupperhalf=False` to kill the mirror half |
| 4–10 numbers describing the same entities | who is high on several at once? | `px.parallel_coordinates` — drag on any axis to filter live | `dimensions[i].constraintrange` to pre-set the filter | no hover tooltips on this one, ever |
| two numbers in wildly different units, same x | does the rate move with the count? | `make_subplots(specs=[[{'secondary_y': True}]])` | — | honest warning: two y-axes can manufacture a correlation by choice of range |
| three number columns | do all three move together? | `px.scatter` with `color=` and `size=` (easier to read) | `px.scatter_3d` only if the reader can rotate it | `go.Surface` / `go.Mesh3d` for a computed grid |
| 5–8 comparable scores, 1–3 entities | what shape is this entity, versus that one? | `go.Scatterpolar(fill='toself')` or `px.line_polar(line_close=True)` | — | radar exaggerates by axis order; 3 entities max |
| a value already computed over a grid of two inputs | where are the ridges and valleys? | `go.Contour` (**no `px` route** — `px.density_contour` bins raw points instead) | `contours.coloring='none'` for pure topographic lines | `contours.type='constraint'` to shade "where the rule holds" |

### COMPOSE — what is it made of?

| I have | I want to know | Start here | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| one category + one number that sums to a real whole, ≤6 slices | roughly what share is each? | `px.pie` (`hole=0.4` for a donut) | `px.bar` sorted — humans read length better than angle | `px.funnel_area` for ordered stages |
| category + subcategory + number | what's inside each bar? | `px.bar` + `barmode='stack'` | `barnorm='percent'` for share instead of level | `barmode='relative'` when there are negatives |
| date + category + number | how did the *mix* change? | `px.area(groupnorm='fraction')` | streamgraph — `go.Scatter(stackgroup='one', mode='none')` | — |
| parent/child columns + a number | where inside the hierarchy is the mass? | `px.treemap(path=[...])` — sizes are easiest to compare | `px.sunburst` when depth is the story | `px.icicle`, and `tiling.orientation='v', flip='y'` turns it into a flame graph |
| two categories of very unequal size + a number | who owns share *within* categories that aren't the same size? | marimekko — `go.Bar` with a `width` array + `barmode='stack'` (build it) | — | — |
| three numbers per row that sum to a fixed total, many rows | who's balanced, who's lopsided, do the lopsided cluster? | `px.scatter_ternary` | `px.line_ternary` for drift over time | — |

### FLOW — what moves where?

| I have | I want to know | Start here | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| a source column, a target column, an amount | where did it actually come from and go? | **`go.Sankey`** — any `GROUP BY a, b, SUM(x)` is already a sankey. **There is no `px.sankey`**, which is why most people never meet it | `arrangement='fixed'` + `node.x`/`node.y` to force your own story order | `link.colorscales` to colour ribbons by a value |
| 3–6 **category** columns on the same rows | which combinations actually co-occur? | `px.parallel_categories` — no reshaping needed | pass `counts=` a pre-aggregated row count | drops columns with >50 distinct values silently |
| ordered stages + a shrinking count | where do we lose them? | `px.funnel` (+ `textinfo` including `'percent previous'`) | `funnelmode='group'` to compare two pipelines | `px.funnel_area` |
| a start value, signed steps, an end value | what actually moved the number? | **`go.Waterfall`** (`measure=` tags each bar `relative`/`total`/`absolute`) | — | no `px.waterfall` exists |
| origin lat/lon + destination lat/lon | what connects to what geographically? | `go.Scattergeo(mode='lines')` with `None` between segments | `px.line_map` on a tile map | `go.Cone` / `go.Streamtube` for true 3D vector fields |

### RANK — who's on top, and did it change?

| I have | I want to know | Start here | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| label + number | who's on top right now? | `px.bar(orientation='h')` + `categoryorder='total descending'` | `visible='legendonly'` to ship top-5 with the rest one click away | — |
| label + number + date, several periods | who is climbing and who is falling? | bump chart — rank in SQL, then `px.line` + `.update_yaxes(autorange='reversed')` (build it) | `px.line` on raw values with `color=` | animation (below) |
| label + number at exactly two dates | who moved the most? | slope chart — `px.line` across the two dates | dumbbell (build it) | — |
| any of the above + a time column | how did the whole ranking move, year by year? | `animation_frame=` + `animation_group=` + **fixed `range_x`/`range_y`** | `sliders` / `updatemenus` hand-built | — |
| entity + 4–10 scores | who is top on everything vs. top on one thing? | `px.parallel_coordinates` | `px.scatter_matrix` | — |
| one number, thousands of rows | how rare is being this high? | `px.ecdf(ecdfmode='complementary')` — "1 in N are worse than this" | — | — |

### LOCATE — where?

Two families, and they do not mix. **`_geo`** draws country/state outlines itself: no tiles, no token, works offline, **and it can be faceted**. **`_map`** (MapLibre) gives a real pannable tile map with streets underneath.

| I have | I want to know | Start here | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| a region name or code column + a number | which regions run high? | `px.choropleth` — needs **no GeoJSON at all** (`locationmode` handles ISO-3, USA-states, country names) | `color_continuous_scale='RdBu', color_continuous_midpoint=0` for rates and changes | `fitbounds='locations'` to auto-zoom |
| lat + lon columns | where are these, and are they clustered? | `px.scatter_map` (tiles) or `px.scatter_geo` (outlines) | `size=` for magnitude, `color=` for type | `cluster=` on `scattermap` groups pins at low zoom |
| lat/lon, far too many points | where's the hotspot? | `px.density_map(radius=30)` | `ff.create_hexbin_map` — kills the "big areas look important" lie | — |
| your own boundaries (tracts, ZIPs, precincts) | which neighbourhoods are high? | `px.choropleth_map(geojson=…, featureidkey='properties.<key>')` | — | `ff.create_choropleth` (FIPS counties) needs `plotly-geo`, **absent here** |
| one map per year | did the pattern move? | `px.choropleth(facet_col='year')` — faceting exists only in the `_geo` family | `make_subplots(specs=[[{'type':'geo'},{'type':'geo'}]])` — verified, produces `geo` and `geo2` | — |

### CHANGE — what happened over time?

| I have | I want to know | Start here | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| a date column + a number | which way is it heading? | `px.line` (**sort first** — it draws rows in dataframe order) | `hovermode='x unified'` the moment there's more than one line | `line_shape='hv'` when values hold then jump |
| date + category + number | how did the total *and* the mix change? | `px.area` | `groupnorm='fraction'` for pure share | streamgraph for many categories |
| a period column + a number | how much in each period? | `px.bar` | `xperiodalignment` to centre a point on its month | — |
| one row per event with a **start and an end** | who overlapped with whom, and what ran long? | `px.timeline(x_start=…, x_end=…, y=…)` — contracts, licences, employment spells, suspensions | `ff.create_gantt` | it's secretly a `bar` with a `base` |
| entity × period + a number | who was on top when? | `go.Heatmap` / `px.imshow` (`zmid=0` if it can go both ways) | calendar heatmap — a 7×52 grid (build it) | — |
| a start total, named steps, an end total | what got us from A to B? | `go.Waterfall` | — | — |
| date + open/high/low/close | how wild was each period? | `go.Candlestick` | `go.Ohlc` when cramming hundreds of periods | kill the auto rangeslider: `xaxis_rangeslider_visible=False` |
| a long daily series | let the reader navigate it | `.update_xaxes(rangeslider_visible=True, rangeselector=dict(buttons=[…]))` | `rangebreaks` to delete weekends/overnights | `tickformatstops` to change label format by zoom level |

### CONNECT — what links to what?

| I have | I want to know | Start here | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| an edge list with amounts | where does the volume go? | `go.Sankey` | `arrangement='snap'` | `node.groups` to collapse nodes into one box |
| an edge list, arbitrary graph | who connects to whom? | **No network trace exists.** Build it: one `go.Scatter(mode='lines')` with `None` between each pair for all edges, plus one `go.Scatter(mode='markers+text')` for nodes | you compute the positions yourself (`networkx` is **not installed** here) | — |
| parent/child pairs (a tree, not a web) | what sits under what? | `px.treemap` / `px.sunburst` / `px.icicle` | `maxdepth=2` and let readers drill | — |
| an N × N overlap matrix | which two things can I actually join? | `px.imshow(text_auto=True)` — readable at 1,000×1,000, unlike a hairball network | `go.Heatmap` sorted by cluster | — |
| 3+ category columns on the same rows | which paths are common? | `px.parallel_categories` | — | — |
| "which of these columns relate at all" | — | `px.scatter_matrix` | — | — |

### SINGLE VALUE — one number that matters

| I have | I want to know | Start here | REACH-FOR | SPECIALIST |
|---|---|---|---|---|
| one number, and a prior value | what is it, and is it up or down? | **`go.Indicator(mode='number+delta')`** — no `px` route exists | `mode='number+delta+gauge'`, `gauge.threshold` for a target line | `gauge.shape='bullet'` for a compact bar |
| one number + a target + good/ok/bad bands | am I on track? | `ff.create_bullet` | `gauge.steps` coloured bands | — |
| a handful of numbers that must be exact | the receipt | `go.Table` (`cells.values` is **column-major**) | `ff.create_table` | — |
| a KPI row | four tiles side by side | `make_subplots(rows=1, cols=4, specs=[[{'type':'indicator'}]*4])` | — | — |

## 2.3 Before you plot: is your data the shape you think it is?

Five things about your columns decide whether the chart works. All five verified by running them.

| Your situation | What Plotly does | The fix |
|---|---|---|
| **Wide table** (`year, north, south`) | `px.line(df, x='year', y=['north','south'])` works and gives 2 traces — but names the legend **`variable`** and the y-axis **`value`** | `labels={'variable':'Region','value':'Sales'}` |
| **A pandas Series** (what `df.groupby('state')['amt'].sum()` hands you) | `px.bar(series)` just works — index becomes x, values become y. No `.reset_index()` needed | — |
| **A category coded as an integer** (`team_id`, FIPS, NAICS) | `color='team_id'` on an int column produces **one trace and a continuous colour bar**, not a legend | `color=df.team_id.astype(str)` → 2 traces and a legend |
| **NULLs in a line** | the line **breaks** at the gap; `connectgaps` defaults to off | `fig.update_traces(connectgaps=True)` if bridging is honest |
| **Dates arriving as strings** | rows are drawn in dataframe order and the axis stays text; `fig.layout.xaxis.type` reads `None` either way, so it is not a diagnostic | `df['d'] = pd.to_datetime(df.d); df = df.sort_values('d')` |

## 2.4 The chart drew, but it looks wrong

The most common failures, each verified, each with the one-line fix.

| Symptom | Cause | Fix |
|---|---|---|
| Bars are in alphabetical order | Plotly does not sort for you | `.update_xaxes(categoryorder='total descending')` |
| …and that did nothing | **`categoryorder` only fires on a category axis.** With int years/FIPS on x it is stored and silently ignored | cast x to `str`, or `.update_xaxes(type='category')` |
| Horizontal bar chart reads upside down | on `orientation='h'`, y runs bottom-to-top, so an *ascending* sort puts the biggest at the top | sort ascending for horizontal, descending for vertical |
| Axis says `total_bill`; legend says `sex` | raw column names | `labels={'total_bill':'Bill ($)','sex':'Gender'}` — renames axis, legend **and** hover in one dict |
| Long category names cut off | default left margin | `fig.update_layout(margin_l=200)` |
| Value labels print `1234.5` | `text_auto=True` becomes `texttemplate='%{y}'` — raw | `text_auto=',.0f'` → `'%{y:,.0f}'` |
| Bar labels clipped at the top | default `textposition` | `fig.update_traces(textposition='outside', cliponaxis=False)`. Note `bar` takes `inside/outside/auto/none`; `scatter` takes a 9-way compass — same name, incompatible values |
| A legend appeared out of nowhere | one px trace sets `showlegend=False` on itself; adding a second trace switches it on | `fig.add_trace(go.Scatter(..., showlegend=False))` for reference lines |
| Facet titles read `day=Sun` | px writes them that way | `fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))` |
| Treemap numbers double-count | `branchvalues`. Via `px.treemap(path=…)` it is set to `'total'` for you; via `go.Treemap(labels=, parents=, values=)` the JS default `'remainder'` applies (the Python attribute reads `None`) and parents get added to their children | on the `go` route, set `branchvalues='total'` when parent rows already include their children |
| Pie slices repeat colours | more slices than the 10-colour palette | `extendpiecolors` is on by default; better, roll up to top-N + "Other" |
| Tooltip says `(29543, 78.2)` | default hover | `hover_name=` + `hover_data=` (px) or `hovertemplate` (go) — §6.5 |
| Chart never appeared at all | `pio.renderers.default` is **`'browser'`** here — `fig.show()` opens a browser tab; in a plain script nothing prints | `fig.write_html('out.html')` and open it, or set the renderer |
| Nothing renders in a notebook | `nbformat` missing | `pip install nbformat` |
| Error: `Value of 'x' is not the name of a column in 'data_frame'. Expected one of ['total_bill', 'tip', …] but received: stat` | typo in a column name — Plotly prints the valid list | read the list in the error |

---

# 3. THE FULL MENU

All **46 live trace types**, grouped by the question they answer, one line each. `props` = top-level properties on that trace (`obj._valid_props`) — it tells you how much chart there is to learn. Nothing is hidden: every one of the 46 appears exactly once here, and the 3 deprecated ones are listed at the end.

**"px or go"**: `px.name` means Plotly Express builds it for you from a dataframe. **go only** means there is no Express shortcut and you must write `go.Thing(...)` — **17 of the 46 live traces are like this**, verified by building every px function and reading back the trace types that came out. Seven of those 17 are things a working analyst actually wants: `sankey`, `waterfall`, `indicator`, `table`, `contour`, `candlestick`, `ohlc`.

## 3.1 The 46

### COMPARE — which one is bigger?

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `bar` | `px.bar`, `px.timeline` | 77 | one label column + one number | the question is which is biggest and by how much; flip `orientation='h'` when labels are words | DAILY |
| `heatmap` | `px.imshow` | 74 | a number for every combination of two category columns (a pivot table) | you want to see which row/column pairs run hot without reading 500 numbers | DAILY |
| `contour` | **go only** | 76 | a value **already computed** across a grid of two inputs | you want ridges and valleys, not cell-by-cell readout. `px.density_contour` is not this — that one bins raw points | REACH-FOR |
| `barpolar` | `px.bar_polar` | 49 | a wrap-around category (compass, hour, month) + a number | December and January are neighbours in reality but opposite ends of a normal bar axis | SPECIALIST |

### DISTRIBUTE — how is it spread out?

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `histogram` | `px.histogram` | 69 | one raw number column, one row per event | you want where the bulk sits and how long the tail runs — Plotly does the counting. Also a GROUP BY machine: `x='cat', y='num', histfunc='sum'` | DAILY |
| `box` | `px.box`, `px.strip` | **88 (most in the library)** | one number, optionally split by a category | comparing averages would lie. Also accepts **pre-computed** `q1/median/q3/lowerfence/upperfence` — five numbers instead of ten million rows | DAILY |
| `violin` | `px.violin` | 63 | one number split by a category, and you suspect the shape is lumpy | a box hides two humps, a hard floor at zero, or a pile-up at a cap; this shows all three | REACH-FOR |
| `histogram2d` | `px.density_heatmap` | 66 | two raw number columns, far too many rows to draw as dots | the scatter has gone to a solid blob and you need to know where points pile up | REACH-FOR |
| `histogram2dcontour` | `px.density_contour` | 67 | same as above | you want smooth density rings instead of blocky cells, or two groups overlaid | REACH-FOR |

### RELATE — does X track Y?

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `scatter` | `px.scatter`, `px.line`, `px.area`, `px.ecdf` | 77 | two numbers, or a date + a number | **one trace, four charts** — `mode='lines'` is a line chart, `mode='markers'` a scatter, `+fill` an area, `+stackgroup` a stacked area | DAILY |
| `scattergl` | `px.scatter(render_mode='webgl')` | 66 | identical to `scatter` | tens of thousands of rows and the page has gone sticky. Same question, different renderer. Slightly fewer styling options (66 vs 77) | REACH-FOR |
| `splom` | `px.scatter_matrix` | 42 | 3–8 number columns, no hypothesis yet | the first exploratory move — every column against every other, in one grid | REACH-FOR |
| `parcoords` | `px.parallel_coordinates` | 26 | 4+ number columns describing the same rows | the question is "which rows are high on A *and* low on B", which no scatter can answer past two columns. **No hover tooltips — ever** | REACH-FOR |
| `scatter3d` | `px.scatter_3d`, `px.line_3d` | 58 | three number columns | the third dimension is genuinely spatial and the reader can rotate it. `projection` drops shadows on the walls, which is what makes it readable | SPECIALIST |
| `surface` | **go only** | 60 | a value over a grid of two inputs | you want the landscape's shape — where's the peak | SPECIALIST |
| `mesh3d` | **go only** | 72 | vertices `x,y,z` plus triangle indices `i,j,k` (or `alphahull` to auto-wrap a point cloud) | 3D modelling, not data analysis | SPECIALIST |
| `carpet` | **go only** | 38 | grid coordinates `a`,`b` and where each node lands | **it is the graph paper, not the data** — for two variables that aren't perpendicular (engineering charts) | SPECIALIST |
| `scattercarpet` | **go only** | 53 | `a`, `b` + `carpet='<id>'` | points on that warped grid; needs a `carpet` trace already in the figure | SPECIALIST |
| `contourcarpet` | **go only** | 55 | `a`, `b`, `z` + `carpet='<id>'` | contour lines on that warped grid | SPECIALIST |
| `scattersmith` | **go only** | 51 | `real` + `imag` | radio-frequency impedance. Outside RF this has no use — and it **cannot be placed in a `make_subplots` grid** (verified: `ValueError: Unsupported subplot type: 'smith'`) | SPECIALIST |

### COMPOSE — what is it made of?

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `pie` | `px.pie` | 59 | one category + one number that sums to a real whole, ≤6 slices | the question is genuinely "what share", not "which is biggest". `labels` alone works — Plotly counts for you | DAILY |
| `treemap` | `px.treemap` | 51 | `path=[level1, level2, …]`, or `labels` + `parents` | comparing sizes inside a hierarchy — nested rectangles, area = value | REACH-FOR |
| `sunburst` | `px.sunburst` | 51 | same | depth of nesting is the story — concentric rings out from a centre | REACH-FOR |
| `icicle` | `px.icicle` | 52 | same | labels are long words needing horizontal room, or you want a flame graph (`tiling.orientation='v', flip='y'`) | REACH-FOR |
| `funnelarea` | `px.funnel_area` | 49 | ordered stages + shrinking counts | you want a cone sitting in a page rectangle next to pies, not on axes | SPECIALIST |
| `scatterternary` | `px.scatter_ternary`, `px.line_ternary` | 54 | three numbers per row that are parts of one total | the only chart that shows three-way composition for **many entities at once** — a stacked bar manages a handful | SPECIALIST |

### FLOW — what moves where?

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `sankey` | **go only** | 27 | `node.label` + `link.source/target/value` | a from/to/amount table and you want to see where the volume splits and pools. **`source`/`target` must be integer positions into the label list — passing names validates cleanly and renders nothing** | REACH-FOR |
| `parcats` | `px.parallel_categories` | 25 | 3+ category columns on the same rows | which combinations co-occur. Ribbon thickness = row count; pass `counts=` to feed it pre-aggregated rows | REACH-FOR |
| `funnel` | `px.funnel` | 69 | one ordered stage column + one count | where the pipeline leaks. `textinfo` including `'percent previous'` prints the drop-off on the chart | REACH-FOR |
| `cone` | **go only** | 63 | six arrays: `x,y,z` positions + `u,v,w` vector components | which way the field is pushing at each point, and how hard | SPECIALIST |
| `streamtube` | **go only** | 61 | the same six arrays | where a weightless particle released here would end up | SPECIALIST |

### LOCATE — where?

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `choropleth` | `px.choropleth` | 50 | `locations` (names or codes) + a number | **start here** — the built-in country/state outlines mean no GeoJSON file at all, and this family is the only one that facets | DAILY |
| `scattergeo` | `px.scatter_geo`, `px.line_geo` | 54 | `lat`+`lon`, or `locations`+`locationmode` | points or routes on a projected outline, offline, no token | REACH-FOR |
| `scattermap` | `px.scatter_map`, `px.line_map` | 50 | `lat` + `lon` | you want real streets under the dots. `cluster` groups pins at low zoom | REACH-FOR |
| `densitymap` | `px.density_map` | 49 | `lat` + `lon` (+ optional weight `z`) | so many points that dots become mush — a blurred heat cloud. `radius` is array-able, so each blob can be sized by importance | REACH-FOR |
| `choroplethmap` | `px.choropleth_map` | 50 | `geojson` + `locations` + `z` | the regions aren't countries or states — tracts, ZIPs, precincts, districts | REACH-FOR |
| `isosurface` | **go only** | 62 | `x,y,z,value` covering a 3D grid + `isomin`/`isomax` | the boundary shell where a value crosses a threshold inside a volume | SPECIALIST |
| `volume` | **go only** | 63 | the same four arrays | you want the whole gradient, not one shell. Tune `opacityscale` or you get fog | SPECIALIST |

### CHANGE — what happened over time?

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `waterfall` | **go only** | 76 | step labels + signed changes + a `measure` column | the number went from A to B and the question is *what were the pieces*. Two bars hide churn; this shows it | REACH-FOR |
| `candlestick` | **go only** | 53 | date + `open/high/low/close` | did it close above where it opened, and how wild was the swing | SPECIALIST |
| `ohlc` | **go only** | 53 | the same four price columns | same question, lower ink — reads better when cramming hundreds of periods | SPECIALIST |
| `scatterpolar` | `px.scatter_polar`, `px.line_polar` | 56 | a cyclical category (`theta`) + a number (`r`) | does this repeat around a cycle. `fill='toself'` closes it into a radar chart | SPECIALIST |
| `scatterpolargl` | `px.scatter_polar(render_mode='webgl')` | 54 | identical | the polar chart has tens of thousands of points | SPECIALIST |

### SINGLE VALUE

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `indicator` | **go only** | **24 (fewest in the library)** | one scalar `value`, optionally `delta.reference` | the KPI tile: big number, up/down arrow, optional dial or bullet bar. `mode` combines `number+delta+gauge` | DAILY |

### Not really charts

| Trace | px or go | props | Data shape | Use when | Tier |
|---|---|---|---|---|---|
| `table` | **go only** | 26 | `header.values` + `cells.values` | the receipt matters — the reader needs the real rows next to the chart. **`cells.values` is column-major: a list per column, not per row** | DAILY |
| `image` | `px.imshow` (RGB input) | 41 | an H×W×3/4 pixel array, or a `data:` URI in `source` | you have actual pixels — a scan, a floor plan, a screenshot — and want to plot marks on top | REACH-FOR |

### Deprecated — do not use in new code

`scattermapbox` (50 props), `densitymapbox` (49), `choroplethmapbox` (50). Prop-for-prop twins of `scattermap` / `densitymap` / `choroplethmap`; constructing one raises `DeprecationWarning: *scattermapbox* is deprecated! Use *scattermap* instead.` The only signature difference in px is `mapbox_style=` instead of `map_style=`. They still work, which is exactly why old code sits on them silently.

## 3.2 Charts that have a name but no trace type

People ask for these by name. Plotly has none of them as a trace — every one is assembled from the traces above. All were built and run; these are the load-bearing lines, not full scripts.

| What they asked for | Data shape / question | How you build it |
|---|---|---|
| **Bump chart** | entity + value + date over many periods; who's climbing? | rank in SQL or pandas, then `px.line(df, x='date', y='rank', color='entity', markers=True).update_yaxes(autorange='reversed', dtick=1)` |
| **Slope chart** | entity + value at exactly two dates | `px.line` on just those two dates, one line per entity |
| **Dumbbell** | entity + two values; who moved most? | two `go.Scatter(mode='markers')` + a `go.Scatter`/shape connecting each pair. The bar's *length* is the change |
| **Ridgeline** | one number across 5–40 groups | stacked `go.Violin(side='positive', orientation='h', points=False)` + `violingap=0, violingroupgap=0` |
| **Beeswarm** | one number, few rows per group, show every row | `px.strip` (it is a `box` trace with `boxpoints='all'` and an invisible box) |
| **Raincloud** | shape + summary + every row, together | half-violin + `go.Box` + `px.strip`, stacked in one axis slot |
| **Marimekko / mosaic** | two categories of unequal size + a number | `go.Bar` with a **`width` array** + `barmode='stack'`: height = share, width = how big that category is |
| **Lollipop / Cleveland dot** | entity + one or two numbers, many entities | `go.Scatter(mode='markers')` + thin line shapes. Less ink than bars at 40+ rows |
| **Band / confidence interval** | x + a low and high bound | `go.Scatter(x=x+x[::-1], y=hi+lo[::-1], fill='toself', line_color='rgba(0,0,0,0)')` under a normal line trace — verified, 2 `scatter` traces |
| **Pareto** | category + count, sorted, with a cumulative % line | `make_subplots(specs=[[{'secondary_y': True}]])` + sorted `go.Bar` + `go.Scatter` of the running share on the second axis — verified |
| **Population pyramid** | two groups + a shared category axis | two `go.Bar(orientation='h')`, one side's values negated, `barmode='relative'` — verified |
| **Waffle / unit chart** | one share, shown as counted squares | `go.Heatmap(z=grid, xgap=3, ygap=3, showscale=False)` — verified |
| **Calendar heatmap** | date + count; is there a weekly rhythm? | reshape to a 7 × 52 grid, `go.Heatmap(xgap=2, ygap=2)` |
| **Network / node-link** | an edge list | one `go.Scatter(mode='lines')` holding **all** edges with `None` between each pair (so it's one trace, not 400), plus one `go.Scatter(mode='markers+text')` for nodes. You compute positions yourself — `networkx` is not installed here |
| **Benford's law check** | any pile of naturally-occurring numbers | `go.Bar` of observed first-digit frequency + `go.Scatter` of the expected curve |
| **Gantt** | task + start + end | `px.timeline(x_start=, x_end=, y=)`, or `ff.create_gantt` |
| **Hexbin map** | far too many lat/lon points | `ff.create_hexbin_map(...)` — returns a `choroplethmap` |
| **Annotated heatmap** | a grid where the numbers must be readable | `ff.create_annotated_heatmap`, or `px.imshow(..., text_auto=True)` |

**Genuinely absent, with no clean recipe:** Venn diagram, UpSet plot, chord diagram, arc diagram, word cloud. For "entity appears in 2 of 5 datasets," build a bar chart of set-combination counts, or a pairwise-overlap heatmap.

---

# 4. THE SHARED 200

This is the part that pays off forever. **195 property names — 98 on `layout` plus 97 on one axis** — are the same for every chart type in the library. Verified: `len(go.Layout()._valid_props) == 98`, `len(go.layout.XAxis()._valid_props) == 97`.

`layout.yaxis` also has 97, and **95 of them are identical to `xaxis`**. The entire difference is four names: `xaxis` alone has `rangeselector` and `rangeslider` (the time-navigator pair); `yaxis` alone has `shift` and `autoshift` (nudging stacked axes sideways in pixels).

Depth-tiered below: **Tier 0** is what you touch constantly, **Tier 1** is the rest of the 98 top-level names by bucket, **Tier 2** opens the big container objects, **Tier 3** is the specialist coordinate systems you may never open.

## 4.1 Tier 0 — the 20 you touch on almost every chart

| # | Property | What it does, in half a sentence |
|---|---|---|
| 1 | `title.text` | Says what the reader is looking at, before they read a single axis. |
| 2 | `xaxis.title.text` / `yaxis.title.text` | "Which is biggest?" is unanswerable if you never said biggest *what*. |
| 3 | `xaxis.categoryorder` | Sorts a category axis — **18 values**, and `'total descending'` turns an alphabetical bar chart into an actual answer. |
| 4 | `barmode` | `'group'` to compare side by side, `'stack'` to add up, `'relative'` when there are negatives, `'overlay'` for two histograms. |
| 5 | `yaxis.tickformat` | A d3 format string; stops `1.2e+06` appearing on a chart a human has to read. |
| 6 | `yaxis.range` | Forces the window — the only way two charts side by side are honestly comparable. |
| 7 | `xaxis.type` | `'log'` when values span orders of magnitude; `'date'` / `'category'` when Plotly guessed wrong. Six values. |
| 8 | `hovermode` | `'x unified'` gives one tooltip listing every series at that x. **The single biggest usability win in Plotly, and it is off by default.** |
| 9 | `showlegend` | One series → off, it's noise. Twelve → on. |
| 10 | `legend.orientation` | `'h'` across the top of a wide chart hands ~15% of the width back to the data. |
| 11 | `legend.x` / `legend.y` | `x=1.02` parks the legend outside the plot instead of on top of your data. |
| 12 | `margin.l/.r/.t/.b` | The fix for clipped category labels, and for a 200px KPI tile losing 40% of itself to default padding. |
| 13 | `width` / `height` | Both default to `None`, which means "fill the container" — only set them when exporting at a fixed size. |
| 14 | `template` | First line of any styling work; 11 built-ins, `'plotly_white'` or `'simple_white'` instantly stops a chart looking like a demo. |
| 15 | `paper_bgcolor` / `plot_bgcolor` | Two backgrounds and everyone forgets there are two: `paper` is the whole image, `plot` is just the data rectangle. |
| 16 | `font.family` / `.size` / `.color` | One place to set the typeface, instead of the 37 separate font objects underneath. |
| 17 | `colorway` | The ordered list of colours handed to series one by one — where your brand palette goes. |
| 18 | `yaxis.showgrid` / `.gridcolor` | Grid on and faint when reading exact values matters; off when the shape is the point. |
| 19 | `annotations` | "This spike is the March outage." A labelled chart needs no caption. **The most under-used property in Plotly.** |
| 20 | `shapes` | Target lines, thresholds, shaded bands — `add_hline` / `add_vrect` are the easy front doors. |

**Honourable mentions**, the moment a chart is more than a one-off: `uirevision` (any constant — the user's zoom survives a data refresh, essential in Dash) · `xaxis.rangeslider.visible` · `title.x` with `title.xref='paper'` (centres over the *data*, not the image) · `xaxis.fixedrange=True` (lock one axis so only the other zooms) · `yaxis.tickprefix='$'` / `.ticksuffix='%'` · `uniformtext.mode='hide'` + `minsize` (kills unreadable 4px labels) · `dragmode='pan'` (kinder than zoom-by-default on a dashboard) · `legend.traceorder='reversed'` (makes a stacked-area legend match the picture).

## 4.2 Tier 1 — all 98 top-level layout names, by bucket

Every name below is real and was read off `go.Layout()._valid_props`. The seven groups sum to exactly 98.

**SCALE (18)** — how numbers and categories become position and colour
`xaxis` · `yaxis` · `coloraxis` · `colorscale` · `colorway` · `piecolorway` · `sunburstcolorway` · `treemapcolorway` · `iciclecolorway` · `funnelareacolorway` · `extendpiecolors` · `extendsunburstcolors` · `extendtreemapcolors` · `extendiciclecolors` · `extendfunnelareacolors` · `autotypenumbers` · `separators` · `calendar`
> The five `*colorway` twins let each part-of-whole chart family carry its own palette; the five `extend*colors` switches decide whether the palette repeats when there are more slices than colours (which is how three different pie slices end up the same colour). `separators` is the decimal/thousands pair for non-American readers. `calendar` accepts **16** calendar systems.

**FRAME (23)** — everything around and behind the data
`title` · `legend` · `annotations` · `annotationdefaults` · `shapes` · `shapedefaults` · `images` · `imagedefaults` · `margin` · `font` · `width` · `height` · `autosize` · `minreducedwidth` · `minreducedheight` · `paper_bgcolor` · `plot_bgcolor` · `showlegend` · `grid` · `uniformtext` · `hiddenlabels` · `hiddenlabelssrc` · `barcornerradius`
> The `*defaults` names are template mirrors: set the default look of every annotation once instead of per call. `hiddenlabels` starts named pie/funnel slices switched off but still clickable back on.

**INTERACTION (22)** — what happens when a human touches it
`hovermode` · `hoverdistance` · `hoverlabel` · `hoversort` · `hoversubplots` · `hoveranywhere` · `clickmode` · `clickanywhere` · `dragmode` · `selectdirection` · `selections` · `selectiondefaults` · `newselection` · `activeselection` · `newshape` · `activeshape` · `modebar` · `updatemenus` · `updatemenudefaults` · `sliders` · `sliderdefaults` · `spikedistance`
> `dragmode` has **12** values including five drawing tools; `hovermode` has 6; `hoversort` can turn a unified tooltip into a live leaderboard (`'value descending'`).

**TRACE-MODE (18)** — the only place layout acknowledges which chart you drew
`barmode` · `barnorm` · `bargap` · `bargroupgap` · `boxmode` · `boxgap` · `boxgroupgap` · `violinmode` · `violingap` · `violingroupgap` · `funnelmode` · `funnelgap` · `funnelgroupgap` · `waterfallmode` · `waterfallgap` · `waterfallgroupgap` · `scattermode` · `scattergap`
> Each `*mode` is "side by side" vs "on top of each other"; each `*gap` pair is spacing between groups and within them. Learn the pattern once, it repeats six times. `scattermode='group'` is how you jitter points that share an x.

**STATE (9)** — bookkeeping that isn't visual
`template` · `uirevision` · `datarevision` · `editrevision` · `selectionrevision` · `meta` · `metasrc` · `computed` · `hidesources`
> `meta` is a free slot for your own values (source, pull date) that rides along with the figure and can be printed in a tooltip as `%{meta.source}`.

**SUBPLOT (7)** — the alternate coordinate systems
`scene` · `polar` · `ternary` · `geo` · `map` · `mapbox` · `smith` — see Tier 3.

**MOTION (1)**
`transition` — 3 settings: `duration`, `easing` (**36** named curves), `ordering`.

## 4.3 Tier 2 — opening the containers

These are the objects the 98 names point at. Sizes verified this session; this is the second layer you actually type.

| Object | Direct props | What it holds |
|---|---|---|
| `layout.xaxis` / `layout.yaxis` | **97** each | the whole axis: type, range, ticks, grid, line, spikes, and (x only) the time navigators |
| `layout.coloraxis.colorbar` | **49** | the colour legend strip — the biggest non-axis object in layout; the same 49 appear on every trace's `marker.colorbar` too |
| `layout.annotations` (each) | **43** | text, arrow, box, position, font, click behaviour |
| `layout.shapes` (each) | **34** | line/rect/circle/path, position, layer, fill, and its own label |
| `layout.legend` | **29** | position, orientation, ordering, click behaviour, grouping |
| `layout.sliders` (each) | **24** | the step list plus everything about the bar itself |
| `layout.updatemenus` (each) | **18** | dropdown or button row, with `buttons` inside |
| `layout.newshape` | **15** | how a shape looks *while the reader is drawing it* |
| `layout.images` (each) | **15** | logo, watermark, base map, floor plan |
| `layout.xaxis.minor` | **14** | a complete second, finer tick system under the main one |
| `layout.selections` (each) | **12** | a persistent highlighted region |
| `layout.grid` | **12** | rows, columns, coupling, spacing — panels without `make_subplots` |
| `layout.xaxis.rangeselector` | **12** | the 1M / 6M / YTD / 1Y button row |
| `layout.title` | **11** | text, subtitle, font, position, and the `xref` that trips everyone up |
| `layout.coloraxis` | **9** | one shared colour scale across several traces; `cmid` keeps a diverging scale honest |
| `layout.font` | **9** | `color, family, lineposition, shadow, size, style, textcase, variant, weight` — **this exact object appears 37 times across layout** |
| `layout.modebar` | **9** | the floating toolbar: add, remove, recolour |
| `layout.xaxis.rangeslider` | **8** | the mini overview strip under a long time series |
| `layout.hoverlabel` | **7** | tooltip styling; `namelength=-1` fixes "Depart…" truncation |
| `layout.margin` | **6** | `l, r, t, b, pad, autoexpand` |
| `layout.xaxis.title` | **3** | `text, font, standoff` |
| `layout.transition` | **3** | `duration, easing, ordering` |
| `layout.uniformtext` | **2** | `minsize`, `mode` — the fix for 4px labels |
| `go.Frame` | **6** | `baseframe, data, group, layout, name, traces` — the whole of animation's data side |

## 4.4 Tier 3 — the seven alternate coordinate systems

Nearly half of layout (1,161 of 2,488 nodes, 47%) is coordinate systems you will never open unless you are doing that exact kind of work. Sizes verified.

| Root | Direct props | What it opens |
|---|---|---|
| `scene` | 13 | a 3D box with x/y/z axes and a camera (each axis has 60 props — *lighter* than the 97 of a Cartesian axis) |
| `geo` | 32 | the built-in world map: **22** projections, 7 scopes, coastlines/countries/land/ocean/lakes/rivers toggles, `fitbounds` |
| `polar` | 10 | radius + angle; `gridshape='linear'` gives the polygonal radar grid |
| `ternary` | 7 | a triangle where three parts sum to a whole — the only family where that constraint is enforced by the geometry |
| `map` | 10 | the current MapLibre tile canvas: style, centre, zoom, bearing, pitch, custom layers |
| `mapbox` | 11 | the legacy canvas — identical plus `accesstoken`. Recognise it in old code; don't write it |
| `smith` | 4 | the RF impedance chart |

## 4.5 Two structural facts worth carrying

1. **`xaxis` and `yaxis` are counted once but are not limited to one each.** `layout.update(xaxis99=...)` is accepted with no error, as are `scene2`, `polar2`, `geo2`. So 2,488 is the number of distinct *kinds* of setting, not a ceiling on how many you can set.
2. **21% of layout (520 of 2,488 nodes) sits inside a `*defaults` mirror** — `annotationdefaults`, `shapedefaults`, `sliderdefaults` and ten more, each an exact duplicate of its list sibling. They exist so a template can set the default once. You don't touch them by hand.
---

# 5. WHAT CHANGES PER CHART

Section 4 was the half you learn once. This is the half that changes — and it is much smaller than it looks.

## 5.1 The 11 blocks that are 80.5% of every trace

Across the 46 live trace types there are 2,549 property slots. **95 distinct names, grouped into 11 reusable blocks, account for 2,051 of them — 80.5%.** Learn these and four fifths of any new chart type is already familiar.

| Block | Names | Traces carrying ≥1 | What it is |
|---|---|---|---|
| **IDENTITY** — `type, name, uid, visible, meta(+src), uirevision, ids(+src), customdata(+src)` | 11 | 46/46 | who this series is and whether it's shown |
| **STREAM** — `stream` | 1 | 46/46 | legacy live-streaming config; nobody uses it |
| **LEGEND** — `legend, legendgroup, legendgrouptitle, legendrank, legendwidth, showlegend` | 6 | 46/46 | how it appears in the key |
| **MARK STYLE** — `marker, line, fill, fillcolor, opacity, mode, width, offset, base` | 9 | 44/46 | what the drawn thing looks like |
| **HOVER** — `hoverinfo(+src), hoverlabel, hovertemplate(+src/+fallback), hovertext(+src), hoveron, hoverongaps` | 10 | 43/46 | the tooltip |
| **TEXT** — `text(+src), textfont, textposition(+src), texttemplate(+src/+fallback), textangle, textinfo, insidetextfont, outsidetextfont, constraintext, insidetextanchor` | 14 | 41/46 | labels drawn on the chart itself |
| **DATA X/Y/Z** — `x(+src), x0, dx, y(+src), y0, dy, z(+src)` | 10 | 27/46 | the ordinary coordinate channels |
| **CARTESIAN BIND** — `xaxis, yaxis, xcalendar, ycalendar, zorder, cliponaxis, alignmentgroup, offsetgroup` | 8 | 24/46 | which axes this trace attaches to, and its draw order |
| **SELECTION** — `selected, unselected, selectedpoints` | 3 | 23/46 | how points look when box-selected |
| **PERIOD / TICK-FORMAT** — `xperiod, xperiod0, xperiodalignment, yperiod, yperiod0, yperiodalignment, xhoverformat, yhoverformat, zhoverformat` | 9 | 22/46 | period alignment for monthly data, and per-axis hover formats |
| **COLOR AXIS** — `coloraxis, colorscale, colorbar, autocolorscale, reversescale, showscale, zauto/zmin/zmax/zmid, cauto/cmin/cmax/cmid` | 14 | 15/46 | mapping a number to colour |

Block coverage runs from **97.1%** (`funnel` — only 2 properties fall outside the blocks) down to **60.0%** (`parcats`). Median trace has about 11 properties outside the 11 blocks.

## 5.2 The 10 names on literally every trace

`type` · `name` · `visible` · `uid` · `uirevision` · `meta` · `metasrc` · `stream` · `legendgrouptitle` · `legendwidth`

Three of those earn their keep daily:

- **`visible`** takes `True`, `False`, or the string **`'legendonly'`** — hidden but with a clickable legend entry still there. That is the right default for "show the top 5, let the reader un-hide the rest."
- **`uirevision`** — set it to any constant and the reader's zoom and pan survive a redraw. The fix for the single loudest Dash complaint.
- **`meta`** — your own values riding along with the trace, printable in a tooltip as `%{meta.source}`. Provenance that travels with the chart.

Add the next tier and you have the practical core: `customdata`, `ids`, `legend`, `legendrank` (45/46 — all missing only from `parcats`), `hoverinfo` (42), `hoverlabel` (41), `hovertemplate` (40), `opacity` (39), `text` / `hovertext` (38), `legendgroup` / `showlegend` (36), `marker` (26).

**The rule behind every exception:** `indicator`, `parcats`, `parcoords`, `carpet`, `table` and `sankey` are not point-and-series charts, so the point-and-series vocabulary doesn't apply to them. Everything else obeys the core.

## 5.3 The `*src` twins — 18% of the library you can delete from your head

**60 of the 340 names end in `src`** — `xsrc`, `textsrc`, `marker.colorsrc`. Across the 46 traces that is **466 of 2,549 slots, 18.3%.** Each one lets a chart definition say "the x values live in the column named `revenue` in the dataset with this id" instead of embedding the array. **They only do anything in Chart Studio's grid workflow. In Python you never set one.** Mentally delete them and the library shrinks by a fifth on the spot.

## 5.4 What is actually unique to each chart

**Only 90 non-`src` property names in the entire library belong to exactly one trace type. Twenty of the 46 trace types have none at all** — they are assembled entirely from parts shared with other charts (verified list: `bar`, `barpolar`, `candlestick`, `choropleth`, `choroplethmap`, `contour`, `funnel`, `heatmap`, `histogram2d`, `histogram2dcontour`, `icicle`, `isosurface`, `scattercarpet`, `scattergeo`, `scattergl`, `scatterpolar`, `scatterpolargl`, `sunburst`, `treemap`, `volume`).

A bar chart has no settings that some other chart lacks. Neither does a heatmap, a treemap, or a choropleth map.

The 26 that do have one-offs, in full:

| Trace | # | Its own words |
|---|---|---|
| `box` | 14 | `boxmean, boxpoints, lowerfence, mean, median, notched, notchspan, notchwidth, q1, q3, sd, sdmultiple, showwhiskers, upperfence` |
| `mesh3d` | 9 | `alphahull, delaunayaxis, facecolor, i, intensity, intensitymode, j, k, vertexcolor` |
| `violin` | 8 | `bandwidth, box, meanline, points, scalemode, side, span, spanmode` |
| `scatter` | 5 | `fillgradient, fillpattern, groupnorm, stackgaps, stackgroup` |
| `splom` | 5 | `diagonal, showlowerhalf, showupperhalf, xaxes, yaxes` |
| `carpet` | 4 | `aaxis, baxis, cheaterslope, font` |
| `indicator` | 4 | `align, delta, gauge, number` |
| `pie` | 4 | `automargin, direction, hole, pull` |
| `sankey` | 4 | `link, node, valueformat, valuesuffix` |
| `table` | 4 | `cells, columnorder, columnwidth, header` |
| `parcats` | 3 | `bundlecolors, counts, sortpaths` |
| `parcoords` | 3 | `labelangle, labelside, rangefont` |
| `scatter3d` | 3 | `error_z, projection, surfaceaxis` |
| `contourcarpet` | 2 | `atype, btype` |
| `funnelarea` | 2 | `aspectratio, baseratio` |
| `image` | 2 | `colormodel, source` |
| `scattersmith` | 2 | `imag, real` |
| `scatterternary` | 2 | `c, sum` |
| `streamtube` | 2 | `maxdisplayed, starts` |
| `waterfall` | 2 | `measure, totals` |
| `cone` | 1 | `anchor` |
| `densitymap` | 1 | `radius` |
| `histogram` | 1 | `cumulative` |
| `ohlc` | 1 | `tickwidth` |
| `scattermap` | 1 | `cluster` |
| `surface` | 1 | `hidesurface` |

**Average across all 46: 1.96 genuinely new ideas per chart type.** `box` is the outlier at 14 — and it is the biggest trace in the library (88 props) precisely because it accepts both raw rows *and* pre-summarised statistics, which is the single most useful property in the library for anyone working off a warehouse.

## 5.5 The cost of learning a new chart

Measured: if you know `scatter` and `bar` (88 names between them), then across all 46 live trace types —

- mean coverage **74.0%**, median **73.4%**, **worst case 50.9%** (`contourcarpet`)
- mean **14.1 property names you haven't seen**, maximum 35 (`mesh3d`)
- of those, mean 2 exist nowhere else

(Excluding `scatter` and `bar` from the average — see the note in §1.4 — those become 72.9% and 14.7. The worst case, `contourcarpet` at 50.9%, is unaffected either way.)

Which charts are secretly the same chart (Jaccard similarity — shared names ÷ combined names; mean across all 1,035 pairs is **0.395**, so any two random Plotly charts already share ~40% of their vocabulary):

| Similarity | Pair | Meaning |
|---|---|---|
| **0.984** | `isosurface` ↔ `volume` | one shell vs the whole cloud |
| **0.981** | `icicle` ↔ `treemap` | the hierarchy trio is one chart with three skins |
| **0.964** | `scatterpolar` ↔ `scatterpolargl` | SVG vs graphics card |
| **0.963** | `candlestick` ↔ `ohlc` | two renderings of the same four price columns |
| **0.923** | `choropleth` ↔ `choroplethmap` | outlines vs tiles |
| **0.900** | `histogram2d` ↔ `histogram2dcontour` | blocks vs rings |
| **0.899** | `contour` ↔ `heatmap` | same trace with `contours` bolted on |
| **0.883** | `funnel` ↔ `waterfall` | both are bars with connectors |
| **0.857** | `scatter` ↔ `scattergl` | — |
| **0.750** | **`bar` ↔ `scatter`** | the two charts that look least alike to a beginner share three quarters of their words |

The odd one out is `parcats`: its highest similarity to anything is 0.457 (`parcoords`), and it is the only trace missing `customdata`, `ids`, `legend` and `legendrank`.

## 5.6 `marker` — the biggest single lever

**26 of 46 traces have a `marker`.** Across them there are 37 distinct `marker.*` names but only **14 distinct marker shapes**, and they nest:

| Size | Traces | Relationship to `scatter.marker` |
|---|---|---|
| **29** | `scatter, scattercarpet, scatterpolar, scattersmith, scatterternary` | the full set |
| 28 | `scattergeo` | minus `maxdisplayed` |
| 24 | `scattergl, scatterpolargl, splom` | minus `angleref, gradient, maxdisplayed, standoff*` |
| 24 | `scattermap` | GPU set minus `line`, plus `allowoverlap` |
| 21 | `scatter3d` | minus the angle/gradient/standoff family |
| 17 | `bar, histogram` | colour block + `line, opacity, cornerradius, pattern` |
| 17 | `treemap` | + `colors, depthfade, pad` |
| 16 / 15 / 14 | `barpolar` / `funnel` / `icicle, sunburst` | trimmed versions of the bar set |
| 7 | `box, violin` | `angle, color, line, opacity, outliercolor, size, symbol` |
| 4 | `pie, funnelarea` | `colors, colorssrc, line, pattern` |
| 3 | `choropleth, choroplethmap` | `line, opacity, opacitysrc` |
| 2 | `histogram2d, histogram2dcontour` | `color, colorsrc` |

**Six of the 14 are strict subsets of `scatter.marker`; the other eight add at most six names.** Learn `scatter.marker` (29 properties) and you have the marker vocabulary of the whole library minus about ten words. Inside it, `marker.size` as an array is a bubble chart, `marker.symbol` offers **324 named shapes**, `marker.colorscale` offers **94 named ramps**, and `marker.pattern` (8 hatch shapes) is your only non-colour channel when colour won't do.

## 5.7 The cheapest order to learn them in

Two answers, and they disagree — take the human one.

**Maximum-vocabulary order** (greedy set cover over all 340 names): `box` (+88 names, 25.9% of the library) → `mesh3d` (+35) → `pie` (+29) → `contourcarpet` (+19) → `histogram` (+16). After three traces you cover **81.7%** of any trace you'll meet; after five, 86.6%; after eight, 91.8%.

**The order that actually helps a human:** `scatter` → `bar` → `histogram` → `box` → `heatmap` → `pie`. Lands in the same coverage territory and every one of those answers a question you already have.

---

# 6. NOT A CHART TYPE

Nothing here answers a data question. Everything here decides whether the answer is legible, shareable, and honest.

## 6.1 Subplots — several panels in one figure

```python
from plotly.subplots import make_subplots
make_subplots(rows=1, cols=1, shared_xaxes=False, shared_yaxes=False,
              start_cell='top-left', print_grid=False,
              horizontal_spacing=None, vertical_spacing=None,
              subplot_titles=None, column_widths=None, row_heights=None,
              specs=None, insets=None, column_titles=None, row_titles=None,
              x_title=None, y_title=None, figure=None)
```

**The trap that makes mixed dashboards come out blank:** ten trace types position themselves by fraction-of-page rather than by axes — `pie, sunburst, treemap, icicle, funnelarea, parcoords, parcats, sankey, table, indicator`. In a grid you **must** declare the cell type or the trace silently doesn't land:

```python
make_subplots(rows=2, cols=2,
    specs=[[{'type': 'xy'},    {'type': 'domain'}],
           [{'type': 'geo', 'colspan': 2}, None]])
```

Verified accepted `type` values: `'xy'`, `'scene'`, `'polar'`, `'ternary'`, `'map'`, `'mapbox'`, `'domain'`, **`'geo'`**, or a trace name like `'choropleth'`. **`'smith'` is not supported** — `ValueError: Unsupported subplot type: 'smith'`. A geo grid genuinely works: two `{'type':'geo'}` cells produced `layout.geo` and `layout.geo2`, so small-multiple maps are available in `go` even though the tile-map px functions can't facet.

Also: `secondary_y=True` in `specs` for two units on one x (`fig.add_trace(..., secondary_y=True)` adds `yaxis2`) · `insets=[dict(cell=(1,1), l=.6, b=.6, w=.35, h=.35)]` for an overview-plus-detail box · `shared_xaxes=True` so zooming one panel zooms all (it sets `matches` and hides duplicate tick labels) · `fig.print_grid()` to see the layout as text · `fig.get_subplot(1,1)` and `fig.update_xaxes(..., row=2, col=1)` to reach back in.

**More than two y-axes needs no subplots at all:** add traces with `yaxis='y2'` / `'y3'`, then `yaxis2=dict(overlaying='y', side='right')`, `yaxis3=dict(overlaying='y', side='right', anchor='free', position=0.9)`, and shrink `xaxis.domain` to make room.

## 6.2 Faceting — small multiples with no assembly

`facet_row` / `facet_col` / `facet_col_wrap` / `facet_row_spacing` / `facet_col_spacing` exist on **18 px functions**: `scatter, scatter_geo, density_contour, density_heatmap, line, line_geo, area, bar, timeline, violin, box, strip, histogram, ecdf, choropleth, pie, funnel, imshow`.

```python
px.scatter(tips, x='total_bill', y='tip', facet_row='sex', facet_col='day')
# verified: 8 traces, 8 x-axes, 6 annotations; fig.layout.xaxis2.matches == 'x'
```

- **Facets share scales by default** (`matches='x'`). Shared = an honest comparison of magnitude. `fig.update_yaxes(matches=None, showticklabels=True)` gives each panel its own height, good for comparing *shape*. **Choose deliberately — unshared panels sitting side by side look comparable and are not.**
- Facet titles arrive as `day=Sun`. Fix: `fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))`.
- **`px.pie` is the only part-of-whole chart that facets.** `sunburst`/`treemap`/`icicle`/`funnel_area` have no facet parameters. Tile maps can't facet either — only the `_geo` family can.
- Colour must be pinned across panels or the same shade means different numbers in different panels: `fig.update_layout(coloraxis=dict(cmin=0, cmax=3))` and `coloraxis='coloraxis'` on each trace.

## 6.3 Animation

`animation_frame` is on **32 of the 40** px figure functions (everything except `scatter_matrix`, `parallel_coordinates`, `parallel_categories`, `pie`, `sunburst`, `treemap`, `icicle`, `funnel_area`); `animation_group` on 31.

```python
px.scatter(gapminder, x='gdpPercap', y='lifeExp', animation_frame='year',
           animation_group='country', size='pop', color='continent',
           log_x=True, range_x=[100,100000], range_y=[25,90])
# verified: 12 frames, 1 updatemenu with 2 buttons (play/pause), 1 slider with 12 steps
```

**Two non-negotiable rules.** Always set `range_x` / `range_y` by hand — otherwise the axes rescale every frame and everything appears to stand still while the ruler moves. Always set `animation_group` — it tells Plotly that "Kenya" in 1952 and 1957 are the same object, so it glides instead of teleporting.

Hand-built frames give you more: `go.Frame` has 6 properties, and **`layout` is one of them** — a frame can change the title, the axis range, the annotations, not just the data. `layout.transition` sets `duration` and `easing` (36 named curves: `linear, quad, cubic, sin, exp, circle, elastic, back, bounce`, each with `-in`, `-out`, `-in-out`). Only **5 traces** transition smoothly rather than jumping: `bar`, `icicle`, `indicator`, `sunburst`, `treemap`.

**Export trap:** `fig.write_html(..., auto_play=True, animation_opts=dict(...))` works; with `auto_play=False` the `animation_opts` are **silently ignored** and no animate call is written at all.

## 6.4 Annotations, shapes and reference lines

Ten of `go.Figure`'s 59 `add_*` methods are not traces — they are how you write on a chart: `add_annotation`, `add_shape`, `add_hline`, `add_vline`, `add_hrect`, `add_vrect`, `add_layout_image`, `add_selection`, `add_trace`, `add_traces`.

```python
fig.add_hline(y=40, line_dash='dot', line_color='red',
              annotation_text='statutory cap', annotation_position='top right')
fig.add_vrect(x0='2020-03-01', x1='2020-06-01', fillcolor='orange',
              opacity=.15, line_width=0, annotation_text='lockdown')
fig.add_annotation(text='Source: FEC bulk filings, pulled 2026-08-04',
                   xref='paper', yref='paper', x=0, y=-0.15,
                   showarrow=False, xanchor='left', font=dict(size=11, color='grey'))
```

- `add_hline`/`add_vline`/`add_hrect`/`add_vrect` all take `row='all', col='all'` and **`exclude_empty_subplots=True`** by default. Verified: on an empty 2×2 grid `add_hline(y=1)` produced **0 shapes**; with one trace per panel, **4 shapes**; with `exclude_empty_subplots=False` on the empty grid, **4**. If your reference line vanished, that's why.
- `xref`: `'x'` = data coordinates · `'paper'` = 0–1 across the plot box regardless of data · `'x domain'` = 0–1 across one subplot. The paper-anchored note above is how every published chart gets its source line.
- `add_shape(type=...)` takes exactly four values: `'circle'`, `'rect'`, `'path'`, `'line'`. `layer='below'` puts a band **behind** the data instead of washing it out. Circles are defined by a bounding box (`x0,x1,y0,y1`), not centre+radius.
- On an annotation, `ax`/`ay` are the **tail** offset, not the point — negative `ay` moves the text up. This confuses everyone exactly once.

## 6.5 Hover — the biggest gap between amateur and professional

The fast path, in px:

```python
px.scatter(df, x='gdpPercap', y='lifeExp', hover_name='country',
           hover_data={'pop': ':,.0f', 'gdpPercap': False, 'continent': True})
```
Verified, that generates `<b>%{hovertext}</b><br><br>lifeExp=%{y}<br>pop=%{customdata[0]:,.0f}<br>continent=%{customdata[1]}<extra></extra>` and packs the extra columns into `customdata` for you.

The controlled path, in `go`:

```python
go.Scatter(x=…, y=…, customdata=np.stack([df['pop'], df.npi], axis=-1),
    hovertemplate='<b>%{text}</b><br>Paid $%{y:,.0f}<br>NPI %{customdata[1]}<extra></extra>')
```

**Three rules.** `%{field}` inserts a value — available fields include `x, y, z, text, hovertext, customdata[i], marker.size, label, value, parent, id, location`. A colon adds a **d3 number format** (`%{y:,.0f}`), a pipe adds a **date format** (`%{x|%b %Y}`). **`<extra></extra>` deletes the grey trace-name box** on the right; leave it out and you get an unwanted second box.

Layout-side: `hovermode='x unified'` (one box listing every series at that x — turn it on for any multi-line time series), `hoversort='value descending'` (makes that box a live leaderboard), `hoverlabel.namelength=-1` (stops "Depart…" truncation), `hoversubplots='axis'` (hovering the top panel lights up every panel below), and `hoverinfo='skip'` on a reference trace so your dashed target line stops stealing tooltips.

**For investigative work this is not decoration.** `customdata` carrying the NPI, the EIN, the filing ID is what makes a chart traceable back to a row. A chart you can't trace back is a dead end.

## 6.6 Colour

Four kinds, and picking the wrong one is a factual error, not a taste one:

| Kind | Your data | Example scales |
|---|---|---|
| **Sequential** | one number, low→high, no natural middle | `Viridis`, `Blues`, `Cividis` |
| **Diverging** | one number with a real midpoint (change %, surplus/deficit) | `RdBu`, `PuOr`, `BrBG` — **always pair with `color_continuous_midpoint=0` or `zmid=0`**, or the neutral colour lands at the data mean and silently lies |
| **Qualitative** | an unordered category | `Plotly`, `Safe`, `Set2`, `Dark2` |
| **Cyclical** | a number that wraps — hour, month, compass bearing | `Phase`, `Twilight` |

Counted this session by listing the actual colour lists in each module: **qualitative 38 · sequential 132 · diverging 44 · cyclical 14**, plus `carto` 68, `colorbrewer` 70, `cmocean` 36, `plotlyjs` 36. `px.colors.named_colorscales()` returns **94**. Every palette has a reversed `_r` twin.

- Browse them: `px.colors.sequential.swatches()`, `.qualitative.swatches()`, `.diverging.swatches_continuous()`, and **`.cyclical.swatches_cyclical()`** — which returns a figure of 7 `barpolar` wheels, because a cyclical palette only makes sense drawn round.
- Build one: `pc.sample_colorscale('Viridis', 5)` pulls N evenly-spaced colours out of a continuous ramp — the way to make a custom discrete palette from a scale you like. Also `n_colors`, `make_colorscale`, `hex_to_rgb`, `get_colorscale`, and 16 more.
- Share one scale across traces or panels with `layout.coloraxis` (9 props) and set the trace's `coloraxis='coloraxis'`. Its `colorbar` is 49 properties — the same 49 everywhere in the library.
- **Never use a rainbow (`Jet`, `Rainbow`) for a sequential number.** It invents boundaries that aren't in the data and is unreadable to colour-blind readers.

## 6.7 Templates — your house style, set once

**11 built-ins**, verified via `list(pio.templates)`: `ggplot2, seaborn, simple_white, plotly, plotly_white, plotly_dark, presentation, xgridoff, ygridoff, gridon, none`. Default here is `plotly`. The last four are modifiers, not full themes.

```python
pio.templates.default = 'plotly_white+presentation+xgridoff'   # later entries win

pio.templates['ripple'] = go.layout.Template(
    layout=dict(paper_bgcolor='#0b0f14', plot_bgcolor='#0b0f14',
                font=dict(family='Inter', color='#e6edf3', size=13),
                colorway=['#58a6ff', '#f778ba', '#3fb950', '#d29922'],
                title=dict(x=0.02, xanchor='left')),
    data=dict(bar=[go.Bar(marker_line_width=0)]))
pio.templates.default = 'ripple'
```

A template has two keys: `data` (per-trace-type defaults — `plotly_dark` sets them for 25 trace types) and `layout` (which includes `annotationdefaults`, `shapedefaults`, `sliderdefaults`, `updatemenudefaults`, so you can style every annotation and shape without touching them per call). `pio.templates.merge_templates(...)` composes `Template` objects programmatically. `pio.to_templated(fig, skip=('title','text'))` **extracts** the style out of a figure you already made into a reusable template. On the px side, `px.defaults.template = 'plotly_white'` makes every chart in the session inherit it.

## 6.8 Export

Measured this session on the same two-bar chart:

| `include_plotlyjs=` | File size | Needs the internet? | Use when |
|---|---|---|---|
| `True` (default) | **4,862,985 bytes** | for cartesian charts, no — **but see the topojson trap** | emailing one self-contained file |
| `'cdn'` | **8,090 bytes** | yes, at open time | the normal choice for anything published |
| `'directory'` | ~8 KB + writes `plotly.min.js` beside it (the bundle is 4,851,117 characters / 4,855,045 bytes on disk) | no | a folder of 50 charts sharing one library copy |
| `False` | **7,837 bytes** | you supply the script tag | many figures on one page |
| **any URL or path string** | **7,992 bytes** | your server | verified: `include_plotlyjs='https://example.com/plotly.js'` writes exactly that `src` — this is the self-hosting route |
| `'require'` | inline | no | AMD/RequireJS pages |

That is a **601×** difference between the default and `'cdn'` on the same chart. The small numbers shift by a few hundred bytes with the figure you measure (a bare `go.Figure(go.Bar(x=['a','b'], y=[1,2]))` comes out ~465 bytes under every row above); the ratio is the point, not the exact byte.

**The offline trap nobody documents:** `config['topojsonURL']` defaults to `https://cdn.plot.ly/un/`, and the bundled plotly.js does **not** ship the world topojson (verified: the string `cdn.plot.ly/un` is in the bundle, `world_110m` is not). So a `choropleth` or `scattergeo` written with `include_plotlyjs=True` is **still not offline** — it renders blank on an air-gapped machine unless you copy the topojson files locally and set `config={'topojsonURL': './topojson/'}`.

Other facts worth having: the bundled plotly.js version is **3.7.0** (`plotly.offline.get_plotlyjs_version()`), which is what you pin a self-hosted copy to. `fig.to_json()` / `pio.from_json()` round-trip exactly, so a figure can live in a database column or cross an API. `pio.renderers.default` is `'browser'` here, and each of the 25 renderers is a tunable object (`pio.renderers['png'].scale = 2`).

**A three-chart dashboard as one static file, no server:** emit each figure with `to_html(full_html=False, include_plotlyjs='cdn' if i==0 else False, div_id=f'fig{i}')`, wrap them in your own HTML. Corpus-measured at 37,429 bytes, fully interactive, emailable, no install on the other end.

**Static images are blocked here.** `fig.write_image()` raises: `ValueError: Image export using the "kaleido" engine requires the Kaleido package`. Note that `pip install kaleido` alone is not sufficient under Kaleido v1 — it also needs a Chrome binary, and plotly ships the command that fetches one (`pio.get_chrome()`, or the console script `plotly_get_chrome`). Missing kaleido also blocks `fig.full_figure_for_development()`, the tool that asks Plotly "after all your defaults and auto-ranging, what did you actually decide?" — worth installing for that alone. `pio.defaults` has 8 settings, not 4: `default_format, default_width, default_height, default_scale`, plus **`topojson`, `plotlyjs`, `mathjax`, `headers`** — the offline controls for static export.

**But your readers can still export.** `config['toImageButtonOptions'] = dict(format='svg', scale=2, width=900, height=600)` puts a working SVG/PNG download behind the camera icon in the toolbar, and that path runs in the reader's browser with no kaleido anywhere.

## 6.9 Interactivity with no server

The `config` dict is not part of the figure — it's a separate argument to `write_html`, `to_html`, `show`, or `dcc.Graph`. There are **39 keys**; the ones that matter:

```python
config = dict(displayModeBar=True, displaylogo=False, responsive=True,
              scrollZoom='cartesian',            # flaglist, default 'gl3d+geo+map'
              doubleClick='reset+autosize',       # or False / 'reset' / 'autosize'
              plotGlPixelRatio=2,                 # 1–4: WebGL render resolution
              modeBarButtonsToRemove=['lasso2d','select2d'],
              modeBarButtonsToAdd=['drawline','drawrect','eraseshape'],
              edits=dict(annotationPosition=True, axisTitleText=True),
              setBackground='transparent',
              toImageButtonOptions=dict(format='svg', filename='chart', scale=2))
```

- **`scrollZoom` is not a boolean.** Default `'gl3d+geo+map'` means wheel-zoom is already on for 3D, geo and map subplots and off only for cartesian. `scrollZoom='cartesian'` is the targeted enable.
- **`edits`** is ten independent booleans (`annotationPosition, annotationTail, annotationText, axisTitleText, colorbarPosition, colorbarTitleText, legendPosition, legendText, shapePosition, titleText`) — far better than the all-or-nothing `editable=True` when you're handing a chart to an editor.
- **`plotGlPixelRatio`** (default 2, range 1–4) is the dial that makes a heavy WebGL page usable on a weak machine.
- There are **36 built-in modebar button names**; `modeBarButtons` replaces the toolbar wholesale.

**Buttons, dropdowns and sliders** live in layout, work in a static file, and can only swap between data already in the file:

```python
fig.update_layout(updatemenus=[dict(type='dropdown', x=0, y=1.15, buttons=[
    dict(label='2023', method='update', args=[{'visible':[True,False]}, {'title':'2023'}]),
    dict(label='log / linear', method='relayout',
         args=[{'yaxis.type':'log'}], args2=[{'yaxis.type':'linear'}])])])
```
`method` ∈ `restyle` (traces) / `relayout` (layout) / `update` (both) / `animate` / `skip`. **`args2` fires on the second click** — one button, two states, no state tracking.

**Drawing and selection:** `dragmode` has 12 values including `drawline`, `drawrect`, `drawopenpath`, `drawcircle` — hand a chart to a subject-matter expert and let them circle what matters. `newshape` styles what they're drawing; `selected` / `unselected` on a trace make box-select feel right (chosen points bold, the rest faded rather than gone).

**Custom JavaScript with no server:** `post_script=` injects raw JS that runs after the plot draws. The full client API is available there — `Plotly.react` (diffed redraw), `Plotly.extendTraces` / `prependTraces` (append points without resending the trace), `Plotly.animate`, `Plotly.downloadImage`, `Snapshot.toSVG`, plus `plotly_click`, `plotly_hover`, `plotly_selected` events for cross-filtering between figures in one HTML file.

**When Dash instead?** Dash 4.4.1 is installed and works. The dividing line in one sentence: **a static HTML file ships all the data inside it; Dash keeps the data on the server and recomputes on demand.** Use Dash only when the data is too big to ship, must not leave the server, the reader's choice can't be enumerated in advance, it must refresh live, or it needs writes. Otherwise you've bought a server, a deploy and an uptime problem for the life of the report. Note: **`Dash.run_server` no longer exists in 4.4.1** — every tutorial older than ~2023 says `app.run_server(debug=True)` and it now raises `AttributeError`. Use `app.run()`. `dcc.Graph`'s four output props (`clickData`, `hoverData`, `selectedData`, `relayoutData`) are what let a chart be an *input* to Python; `relayoutData` in particular carries the new axis range, so you can fetch high-resolution data only for the window someone zoomed into. `go.FigureWidget` (Python callbacks on chart events in a notebook) needs `anywidget`, **absent here**.

## 6.10 Large data — the levers before you reach for Dash

Measured this session:

| Same chart, two ways | Bytes in `fig.to_json()` |
|---|---|
| Box plot from 200,000 raw values | **2,728,215** |
| Box plot from 5 pre-computed numbers (`q1/median/q3/lowerfence/upperfence`) | **6,760** |
| 200,000-point scattergl, x/y as **numpy float32** | **2,668,931** |
| The same, x/y as **Python lists** | **7,714,369** |

Two separate wins there. **Aggregate in the warehouse and ship shapes, not rows** — over 400× on that box plot. And **hand Plotly numpy arrays, not lists** — plotly.py 6 serialises numpy as base64 binary, which was 2.89× smaller here for float32 with zero visual difference (the win is dtype-dependent; for `int32` binary is actually slightly larger).

Every chart here has a pre-aggregated form: box → five percentile columns; heatmap → a pre-binned grid; `parcats` → the `counts` array; sankey → aggregated by definition; histogram2d → bin in SQL and use `go.Heatmap` instead (`histogram2d` bins *in the browser*, so it ships every raw row first).

Also: `px.scatter` and `px.ecdf` **switch from `scatter` to `scattergl` at exactly n > 1000** (verified: 1000 → `scatter`, 1001 → `scattergl`) — which matters because WebGL output is rasterised, so force `render_mode='svg'` if you need a clean vector export. `px.imshow(..., binary_format='jpg')` cut a 600×800 RGB image from 2,074,798 to 410,887 bytes. And there is no downsampler in the library at all — `marker.maxdisplayed` is a hard cap, not a resample, and `plotly-resampler` is not installed.

## 6.11 `figure_factory` — 19 pre-built recipes

Things people look for as chart types that are actually assemblies. Status on this machine:

**Working (14):** `create_annotated_heatmap` (a heatmap with the number printed in every cell — the single most useful one), `create_2d_density`, `create_bullet`, `create_candlestick`, `create_ohlc`, `create_facet_grid`, `create_gantt`, `create_hexbin_map`, `create_hexbin_mapbox`, `create_quiver`, `create_streamline`, `create_scatterplotmatrix`, `create_table`, `create_trisurf`.

**Blocked here (5):** `create_distplot`, `create_dendrogram`, `create_violin` (need `scipy`) · `create_ternary_contour` (needs `scikit-image`) · `create_choropleth` (US county FIPS map; needs `plotly-geo`).

## 6.12 The bridge from matplotlib

**matplotlib 3.11.1 is installed here**, and `plotly.tools.mpl_to_plotly(fig)` converts a matplotlib figure into a `go.Figure` — verified on a real `plt.subplots()` line chart, which came back as a `scatter` trace with the title preserved. Also `plotly.offline.plot_mpl` / `iplot_mpl`. Useful when there's existing matplotlib code you want interactive without rewriting it.

## 6.13 Accessibility and internationalisation — know the hole

This is the one area where the honest answer is "Plotly does not do this for you."

- **A Plotly chart is an unlabelled SVG to a screen reader.** Counted in the shipped bundle: `role="img"` appears **0** times, `aria-live` **0**, and of 21 `aria-label` occurrences exactly one belongs to Plotly (a modebar button) — the other 20 are inside the bundled map libraries. Data points are not keyboard reachable. **Every published chart needs a text alternative you write yourself** — a caption, a summary sentence, or a `go.Table` twin of the same numbers.
- **Locale switching effectively doesn't work out of the box.** `config['locale']` defaults to `'en-US'` and only two locale modules are bundled (`en`, `en-US`). Setting `locale='fr'` silently does nothing unless you load and register a locale bundle.
- **Non-colour channels are narrower than they look.** `marker.pattern.shape` has 8 values (`'' / \ x - | + .`) and exists on only 8 traces. `line.dash` has 6 named values plus a custom dash-array string (`'5px,10px'`). In px: `pattern_shape` exists on `bar, area, histogram, timeline, bar_polar` only; `symbol` on `scatter, line, area`; **`line_dash` on `px.line` only**. So for a colour-blind-safe `px.bar`, pattern is your single alternative channel — and for `px.scatter` there is no dash option at all. Plan around that before you pick the chart.

---

# 7. THE NESTING MAP

## 7.1 How to read a dotted path

`layout.xaxis.tickfont.size` reads left to right as **"in the figure's layout → on the x-axis → the font used for the tick labels → its size."** Every path in Plotly reads the same way: each dot walks one step further into a nested dictionary, and the last word is the thing you actually set.

You get there by asking three questions in order:

1. **Is this thing a mark, or is it furniture?** A mark (the bar, the dot, the wedge, the ribbon) lives on a **trace** — `fig.data[0]...`. Everything else — the axis, the title, the legend, the tooltip box, the colour bar — lives on **`fig.layout`**.
2. **Which object owns it?** The bit of the chart it belongs to: the axis, the legend, the colour bar, the annotation.
3. **Is it text, a line, or a colour?** Text nearly always sits in a `font` sub-object (9 properties, always the same nine). Lines sit in `line` (`color`, `width`, `dash`). Colours are usually a plain `*color` property one level up.

Worked: *"the numbers along the bottom are too big."* → furniture → owned by the x-axis → they're text → `layout.xaxis.tickfont.size`.

## 7.2 From the thing on screen to the property

| What you can see | The path |
|---|---|
| the words along the bottom | `layout.xaxis.tickfont.size` / `.color` / `.family` |
| how those numbers are written (`1,234` vs `1.2e+3`) | `layout.xaxis.tickformat` |
| the label under the axis | `layout.xaxis.title.text`, and its size at `layout.xaxis.title.font.size` |
| the faint lines across the plot | `layout.yaxis.gridcolor` / `.gridwidth` / `.griddash` / `.showgrid` |
| the line along the edge of the plot | `layout.xaxis.linecolor` / `.linewidth` / `.showline` |
| the order the bars sit in | `layout.xaxis.categoryorder` |
| the white space around everything | `layout.margin.l` / `.r` / `.t` / `.b` |
| the background behind the bars | `layout.plot_bgcolor` (the whole image is `layout.paper_bgcolor`) |
| the key at the side | `layout.legend.x`, `.orientation`, `.font.size`, `.title.text` |
| the big headline | `layout.title.text`, `layout.title.font.size`, `layout.title.x` |
| the grey box that pops up on hover | `layout.hoverlabel.bgcolor`, `layout.hoverlabel.font.size` |
| what that box actually says | `fig.data[0].hovertemplate` (a **trace** property, not layout) |
| the coloured strip down the right | `layout.coloraxis.colorbar.thickness`, `.len`, `.title.text` |
| the numbers on that strip | `layout.coloraxis.colorbar.tickfont.size` |
| the colour of the bars themselves | `fig.data[0].marker.color` |
| the outline around each bar | `fig.data[0].marker.line.color` / `.width` |
| the numbers printed on the bars | `fig.data[0].texttemplate` and `fig.data[0].textfont.size` |
| the dot shape / size | `fig.data[0].marker.symbol` / `.size` |
| the dashes in a line | `fig.data[0].line.dash` |

## 7.3 Four shortcuts that save the typing

```python
fig.update_layout(title_text='hi', title_font_size=22, legend_title_text='Sex')
```
**Magic underscores** walk the dots for you, so you never write `title=dict(font=dict(size=22))`.

```python
fig.update_traces(marker_size=12, selector=dict(name='Male'))
fig.update_traces(marker_symbol='square', selector=lambda t: t.name == 'Female')
fig.for_each_trace(lambda t: t.update(name=t.name.title()))
```
**`selector=`** reaches into a figure px already built and changes one trace out of thirty, by property or by function. The same pattern exists for `update_annotations`, `update_shapes`, `update_xaxes`, `update_yaxes`, `update_coloraxes`, `update_layout_images`, `update_selections`, `update_legends`, each with `for_each_*` and `select_*` versions. `go.Figure` has 133 public methods; these are the ones you'll actually use.

```python
fig.update_xaxes(title='t', row=2, col=1)   # one cell
fig.update_yaxes(type='log')                # every cell
```
**`row`/`col`** targets a panel; leaving them off hits all panels.

```python
go.Bar()._valid_props                       # every settable name on a bar
go.Layout()._get_validator('hovermode').values   # the real list of allowed values
go.Scatter().marker._valid_props            # one level deeper
```
**Introspection beats the docs.** Over a fifth of all layout settings (511 of 2,253 leaves) are "pick one of N words", and `_get_validator(...).values` prints the words. Every enum quoted in this document came from exactly that call.

## 7.4 How deep it actually goes

- **Maximum nesting depth is 5**, in both trees. The longest path in a scatter trace is `scatter.marker.colorbar.title.font.color`. **There is no level 6.**
- Layout by depth: 98 nodes at depth 1, 695 at depth 2, 1,123 at depth 3, 462 at depth 4, 110 at depth 5.
- **The bottom of the tree is always fonts.** Of the 110 deepest layout nodes, 92 are frame-or-text; the depth-5 containers are ten `Font` objects and four cut-down `Textfont` objects, and that is the end.
- **Depth 4 is repetition, not new ideas.** The class census explains why: `Font` appears **37 times** in layout — and across the 46 trace trees there are another 87 instances of that same 9-property font plus 47 of its src-doubled 18-property twin. Then `Tickformatstop` 22, `Tickfont` 13, `Title` 12, `Line` 10, `Domain` 8. Learn each shape once.
- `marker` alone is 122 of a scatter trace's 325 nodes (37.5%), and `colorbar` is 75 of those 122 (61%). **Learning `marker.colorbar` once buys you the colour legend of 34 chart types** — there is exactly one shape of colorbar in the whole library, verified by collecting all 35 instances.
- Only one branch of layout was ever cut during the walk: `layout.template` contains a `Layout`, which contains a `template`, forever. Everything else is enumerated to its true bottom.

## 7.5 Reproduce any number in this atlas

```python
import plotly.graph_objects as go

f = go.Figure()
f._data_validator.class_strs_map          # the authoritative 49 trace types
f._data_validator.get_trace_class('bar')  # -> go.Bar
len(go.Bar()._valid_props)                # 77
len(go.Box()._valid_props)                # 88  (most)
len(go.Indicator()._valid_props)          # 24  (fewest)
len(go.Layout()._valid_props)             # 98
len(go.layout.XAxis()._valid_props)       # 97
go.layout.XAxis()._get_validator('categoryorder').values   # the 18 sort orders
go.Indicator()._get_validator('mode').flags                # number / delta / gauge
```

Nothing in this document is remembered. Every count above came back from one of those calls.
