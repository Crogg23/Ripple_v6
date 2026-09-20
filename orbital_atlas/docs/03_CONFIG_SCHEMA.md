# 03 — View and Theme Schemas

## The short version

- A **view** says what the map means. A **theme** says how it looks. A **version** of the map is one of each.
- The test for which side a setting belongs on: **"if I change this, does the reader learn a different fact?"** Yes means view. No means theme.
- The key trick that keeps them apart: the view names a **role**, the theme paints the role.
  - View: "these places are *highlighted*." Theme: "highlighted places get an amber fill," or "a hard outline."
  - View: "these places are *low-confidence*." Theme: "low-confidence places are desaturated," or "hatched."
  - View: "the scale is *diverging* around zero." Theme: "diverging scales run blue, dark, red."
- So **any theme works with any view.** That is the whole point.
- All nine illustration rows fit. **Three strains showed up.** They are listed at the bottom as findings.

This is a proposal to react to, not a decision.

---

## The view

```json
{
  "schema": "orbital.view/1",
  "id": "fines_per_bed",
  "title": "Nursing home fines per bed",
  "note": "One line of context for the margin.",

  "topology": "us_counties_2018",
  "layer": "cms_fines",
  "layer_b": null,
  "period": "latest",

  "measure": "ratio",
  "measure_locked": false,

  "scale": {
    "type": "quantile",
    "bins": 0,
    "ties": "share",
    "domain": null,
    "midpoint": null,
    "thresholds": null,
    "zero_class": false,
    "invert": false
  },

  "highlight":  { "rule": "none", "value": null },
  "confidence": { "field": "n", "low_below": null },
  "filter":     { "tier_in": null },

  "frame":    { "type": "national", "id": null },
  "on_click": "focus_parent",

  "readout": { "always": ["value", "rank"], "on_demand": ["denominator", "ratio", "n", "tier"] },
  "labels":  { "top": 0 },
  "empty_message": null
}
```

### View fields

| Field | Choices | Plain meaning |
|---|---|---|
| `topology` | a registered id | Which set of shapes. A tile cartogram is a different topology layout, so it lives here. |
| `layer` | a layer id, or `null` | Which table. `null` is the empty state. |
| `layer_b` | a layer id | Second table, for difference, ratio-of-two, or bivariate. |
| `period` | a period string, or `"latest"` | Which slice in time. |
| `measure` | `value`, `ratio`, `denominator`, `n`, `presence`, `difference`, `ratio_ab` | What number drives the colour. |
| `measure_locked` | true / false | If true, slicers cannot switch the map to another measure. The readout still shows everything. |
| `scale.type` | `linear`, `log`, `quantile`, `quantize`, `threshold`, `diverging`, `categorical`, `binary` | How numbers become positions on the palette. |
| `scale.bins` | `0` for smooth, or a count | Stepped or continuous. |
| `scale.ties` | `share`, `spread` | `share`: equal values get equal colour. Default. `spread` is what v1 did by accident. |
| `scale.midpoint` | a number | Centre of a diverging scale. |
| `scale.zero_class` | true / false | Zero gets its own class first, then the rest are scaled. "Binary-then-magnitude." |
| `scale.invert` | true / false | Flip the direction. |
| `highlight.rule` | `none`, `percentile_above`, `percentile_below`, `top_n`, `bottom_n`, `value_above`, `value_below`, `outlier_iqr`, `outlier_z` | Which places are called out. **The view picks who. The theme picks how.** |
| `confidence.field` | `n`, `denominator` | What makes a place shaky. Small sample, or small base. |
| `confidence.low_below` | a number | Below this, the place is low-confidence. |
| `filter.tier_in` | list of tier strings | Only draw rows with these tiers. |
| `frame.type` | `national`, `parent`, `places`, `neighbors`, `path` | What the camera fits to. |
| `on_click` | `focus_parent`, `select`, `none` | Default click behaviour. The event always fires as well. |
| `readout.always` | list | What the readout must show for every hovered place. |

### What the engine enforces, whatever the view says

- If the layer has a denominator, `value`, `denominator`, and `ratio` are **all reachable** from the readout. A view can promote them to `always`. It cannot remove them.
- **The legend is generated from `scale`.** There is no legend text field to get out of sync. A quantile scale prints "percentile" and shows real cut values. A smooth quantile legend is drawn with uneven tick spacing so it cannot be read as linear.
- If `confidence.low_below` is set, the legend gains a "low confidence" swatch automatically.
- If `highlight.rule` is set, the legend says what the rule is in words: "top 10%".

---

## The theme

```json
{
  "schema": "orbital.theme/1",
  "id": "ledger",
  "label": "Ledger",

  "ground": { "background": "#0b0f14", "land_empty": "#141b23", "texture": "none" },

  "palettes": {
    "sequential":  ["#10202c", "#1d4253", "#3f7f86", "#a9c9b8", "#eef3e6"],
    "diverging":   { "low": ["#4aa3ff", "#1c3f66"], "mid": "#0d1117", "high": ["#66231f", "#ff6b5e"] },
    "binary":      { "zero": "#151c24", "nonzero": ["#5a3a1e", "#e5a54a"] },
    "categorical": ["#4aa3ff", "#e5a54a", "#7bd389", "#ff6b5e", "#b49cff", "#9aa7b2"]
  },

  "encoding": "fill",

  "roles": {
    "highlight":      { "style": "accent_fill", "color": "#e5a54a" },
    "low_confidence": { "style": "desaturate", "amount": 0.75 },
    "no_data":        { "style": "fill", "color": "#141b23" },
    "hover":          { "style": "outline", "color": "#ffffff", "width": 1.2 },
    "focus_dim":      { "style": "veil", "color": "#02050a", "amount": 0.6 }
  },

  "light": { "type": "flat", "strength": 0, "source": null },
  "glow":  { "on": "none" },

  "lines": {
    "places":  { "color": "#bedcf0", "opacity": 0.12, "width": 0.55 },
    "parents": { "color": "#d7ecfa", "opacity": 0.55, "width": 0.9 },
    "outline": { "color": "#ebf6ff", "opacity": 0.75, "width": 0.7 }
  },

  "type": {
    "display":  "Instrument Serif, Georgia, serif",
    "data":     "IBM Plex Mono, ui-monospace, monospace",
    "numerals": "tabular"
  },

  "motion": { "zoom_ms": 250 }
}
```

### Theme fields

| Field | Choices | Plain meaning |
|---|---|---|
| `ground.texture` | `none`, `grain`, `paper`, `blueprint` | Static surface. Never animated. |
| `palettes` | one per scale family | The view's scale type picks the family. A theme must supply all four to be complete. |
| `encoding` | `fill`, `dots`, `hatch`, `stipple`, `bars` | How a value becomes ink. See finding 1. |
| `roles.*.style` | `accent_fill`, `outline`, `desaturate`, `hatch`, `dot`, `veil`, `fill` | How each role is painted. |
| `light.type` | `flat`, `radial`, `hillshade` | `hillshade` uses `light.source`, normally `"value"`, as the height. |
| `glow.on` | `none`, `highlight` | **Glow can only ever attach to highlighted places.** No free-floating glow. That is how "glow reserved for outliers" becomes impossible to break. |
| `motion.zoom_ms` | 0 to 400 | The only motion setting. Capped by the engine. `0` is a hard cut. No setting exists for idle or looping motion. |

---

## The nine illustration rows

Each is a view plus a theme. Only the fields that differ from the defaults are shown.

### 1. Money, with restraint
```json
{ "view":  { "layer": "payments", "measure": "value",
             "scale": { "type": "quantile", "bins": 0 },
             "highlight": { "rule": "percentile_above", "value": 0.9 } },
  "theme": { "glow": { "on": "none" }, "light": { "type": "flat" },
             "type": { "numerals": "tabular" },
             "palettes": { "sequential": ["#11161c", "#2a3440", "#566473", "#8e9aa6"] },
             "roles": { "highlight": { "style": "accent_fill", "color": "#e5a54a" } } } }
```
Muted ramp for ninety percent of places. One accent for the top decile. **Fits cleanly.**

### 2. Fatalities: zero versus non-zero first
```json
{ "view":  { "layer": "fatalities", "measure": "value",
             "scale": { "type": "quantile", "bins": 4, "zero_class": true },
             "readout": { "always": ["value", "n"] } },
  "theme": { "palettes": { "binary": { "zero": "#12181f", "nonzero": ["#5b2a2a", "#ff6b5e"] } } } }
```
`zero_class` pulls zero out first. The rest are binned. **Fits cleanly.**

### 3. Fines that only make sense per bed
```json
{ "view":  { "layer": "cms_fines", "measure": "ratio", "measure_locked": true,
             "readout": { "always": ["value", "denominator", "ratio", "rank"] } },
  "theme": {} }
```
The map is locked to the ratio. Both raw numbers are pinned in the readout. **Fits cleanly.**

### 4. Disputes on a light ground, outliers outlined
```json
{ "view":  { "layer": "disputes", "measure": "ratio",
             "highlight": { "rule": "outlier_iqr", "value": 1.5 } },
  "theme": { "ground": { "background": "#f4f1ea", "land_empty": "#e6e1d6", "texture": "paper" },
             "palettes": { "sequential": ["#e9e4d8", "#c9c0ab", "#8f866f", "#4f4a3c"] },
             "roles": { "highlight": { "style": "outline", "color": "#111111", "width": 1.6 },
                        "hover":     { "style": "outline", "color": "#b3261e" } },
             "lines": { "places": { "color": "#3a3528", "opacity": 0.15 } } } }
```
Same `highlight` idea as row 1. A different theme paints it as an outline. **This is the separation working.**

### 5. A rate, with low-population places desaturated
```json
{ "view":  { "layer": "overdose_deaths", "measure": "ratio",
             "confidence": { "field": "denominator", "low_below": 5000 } },
  "theme": { "roles": { "low_confidence": { "style": "desaturate", "amount": 0.8 } } } }
```
**Small strain.** "Low population" is the denominator, not `n`. So `confidence.field` has to allow either. It does.

### 6. Political lean, dark midpoint
```json
{ "view":  { "layer": "pres_2024", "measure": "ratio",
             "scale": { "type": "diverging", "midpoint": 0 } },
  "theme": { "palettes": { "diverging": { "low": ["#4aa3ff", "#17314f"], "mid": "#0b0e13", "high": ["#4f1b18", "#ff5a4d"] } } } }
```
`value` is the vote margin, `denominator` is total votes. Close races go dark. Landslides go bright. **Fits cleanly.**

### 7. Where data exists, and the inverse
```json
{ "view":  { "layer": "any_layer", "measure": "presence", "scale": { "type": "binary" } } }
```
And the inverse:
```json
{ "view":  { "layer": "any_layer", "measure": "presence", "scale": { "type": "binary", "invert": true } } }
```
**Fits cleanly.** One open detail: "exists" could mean "a row exists" or "the value is not empty". Proposed: not empty.

### 8. Land area with hillshade
```json
{ "view":  { "layer": "land_area", "measure": "value", "scale": { "type": "quantile" } },
  "theme": { "light": { "type": "hillshade", "strength": 0.6, "source": "value" } } }
```
**Strain, see finding 2.** Hillshade driven by the value is a second encoding of the data, sitting in the theme.

### 9. Empty state
```json
{ "view":  { "layer": null, "empty_message": "Paste a table: geo_id, value" },
  "theme": {} }
```
With no layer, every place takes the `no_data` role, and the message shows. The words are content, so they live in the view. **Fits cleanly.**

---

## Findings

| # | Finding | Why it matters | Options |
|---|---|---|---|
| 1 | **`encoding` straddles the line.** The brief puts it in the theme. But dots sized by value say "magnitude", and only make sense for counts, not rates. | A theme swap could quietly turn an honest rate map into a misleading one. | a. Keep it in the theme, and let a view list `allowed_encodings`. b. Move it to the view. c. Keep in theme, engine refuses size encodings on ratio measures. |
| 2 | **Hillshade from value is data, not decoration.** | Same shape as finding 1. Low stakes, since it doubles the colour rather than contradicting it. | Accept it as theme. Or restrict `light.source` to `"value"` only, so it can never encode something else. |
| 3 | **Two-layer views are needed** for difference, ratio-of-two, and bivariate. | None of the nine rows need it. Half the comparison list in `04` does. | `layer_b` as above. Bivariate would also need a fifth palette family, a 3×3 grid. |
| 4 | **Rows 1 and 4 prove the role idea.** | Same view setting, two looks. | Keep. |
| 5 | **The contract needs a header.** Row 3 cannot print "per bed" without one. | Carried from `02`. | Decision in `06`. |

---

## Validation and versioning

- Both schemas are published as JSON Schema files. A config that starts with `"$schema": ".../orbital.view.1.json"` gets autocomplete and red squiggles in most editors, with no tooling to install.
- **Defaults are in the schema.** A view can be three lines long.
- **Partial themes are allowed.** A theme can name a `"base"` theme and override a few fields. That is how the snippets above stay short.
- Version rules are in `01_OPTIONS`, question 3: add freely, rename only with a major bump and an upgrade function, never drop unknown fields.
- **Cross-checks a schema alone cannot do**, done by the engine on load:
  - `measure: "ratio"` on a layer with no denominator → refuse, say why.
  - `scale.type: "log"` with zero or negative values → refuse, say why.
  - `scale.type: "diverging"` with no `midpoint` → refuse.
  - `layer.geo_type` does not match `topology.geo_type` → refuse.
