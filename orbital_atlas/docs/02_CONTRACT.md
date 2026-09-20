# 02 — The Data Contract

## The short version

- A layer is **one flat table** plus **one small header**.
- The table is the seven columns from the brief. Unchanged.
- The header is new. **Finding: the seven columns cannot carry a unit or a label, and the engine cannot print "$4.2M per bed" without them.** The header is the smallest fix.
- The key of a row is `geo_id + geo_type + period`. One row per key.
- The engine never drops a row silently. Every load produces a **load report**.

---

## The table

| Column | Type | Required | Rule |
|---|---|---|---|
| `geo_id` | string | yes | Always a string. `"06037"`, never `6037`. Cleaned using the topology's `id_rule`. |
| `geo_type` | string | yes | Must match a registered topology's `geo_type`. |
| `period` | string | yes | `"latest"` is fine. Otherwise ISO-style so it sorts as text: `"2023"`, `"2023-Q2"`, `"2023-06"`. |
| `value` | number or empty | yes | The raw measurement. Empty means "no data", which is **not** zero. |
| `denominator` | number or empty | no | Raw. The engine divides. Zero is kept but never divided by. Negative is rejected. |
| `n` | number or empty | no | Count of records behind the value. Zero or more. |
| `tier` | string or empty | no | Free text from the source. The view decides what each tier means. |

**The source never sends a rate.** If it has a rate, it sends the numerator as `value` and the base as `denominator`.

### Why that rule pays off
One table gives four views with no new query:

| View | Shows |
|---|---|
| raw | `value` |
| normalized | `value / denominator × per` |
| base | `denominator` on its own |
| coverage | where rows exist, or where `n` is thin |

It also means **duplicates and roll-ups can be summed safely.** Two rates cannot be added. Two numerators and two denominators can.

---

## The header

Travels with the table. Plain data, no functions.

```json
{
  "schema": "orbital.layer/1",
  "id": "cms_fines",
  "label": "Nursing home fines",
  "source": "CMS penalties file",
  "value":       { "label": "Fines",  "unit": "$",    "format": "$,.3s" },
  "denominator": { "label": "Beds",   "unit": "beds", "format": ",.0f" },
  "ratio":       { "label": "Fines per bed", "per": 1, "unit": "$ per bed", "format": "$,.0f" },
  "n":           { "label": "Facilities" },
  "higher_is": "bad",
  "categories": null,
  "period_order": null
}
```

| Field | Why it exists |
|---|---|
| `format` | A format string, such as d3-format style. v1 used functions, and functions cannot be saved. |
| `per` | Multiplier for rates: `100000` for "per 100,000". |
| `higher_is` | `good`, `bad`, or `neutral`. Lets a theme pick a sensible palette direction. Optional. |
| `categories` | For categorical layers: a map from number code to label. See edge cases. |
| `period_order` | Only needed when periods do not sort as text, such as `"FY23"`. |

**When pasting with no header,** the engine makes a minimal one: label from the header row of the paste, no unit, default number format. Pasting must never require writing JSON.

---

## Formal schema for a row

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "orbital.row/1",
  "type": "object",
  "required": ["geo_id", "geo_type", "period", "value"],
  "properties": {
    "geo_id":      { "type": "string", "minLength": 1 },
    "geo_type":    { "type": "string", "minLength": 1 },
    "period":      { "type": "string", "minLength": 1 },
    "value":       { "type": ["number", "null"] },
    "denominator": { "type": ["number", "null"], "minimum": 0 },
    "n":           { "type": ["number", "null"], "minimum": 0 },
    "tier":        { "type": ["string", "null"] }
  },
  "additionalProperties": true
}
```

Extra columns are allowed and ignored. A source can carry its own notes.

### Paste shorthand
To keep v1's friendliness, the paste adapter accepts fewer columns and fills the rest:

| Pasted columns | Filled in |
|---|---|
| `geo_id, value` | `geo_type` from the active topology; `period = "latest"` |
| `geo_id, value, denominator` | same |
| any named header row | columns matched by name, any order |

`fips` is accepted as another name for `geo_id`.

---

## Examples

**Minimal**
```
geo_id,geo_type,period,value
48201,county,latest,4731145
06037,county,latest,10014009
```

**With denominator and n**
```
geo_id,geo_type,period,value,denominator,n,tier
48201,county,2023,1250000,8400,61,exact
48201,county,2022,980000,8350,60,exact
01001,county,2023,0,210,2,fuzzy
```

**Political lean, using the same contract**
`value` = votes for party A minus votes for party B. `denominator` = total votes. The ratio is the margin, centred on zero.

---

## Edge cases and what the engine does

| Case | Engine behaviour | Shows in load report |
|---|---|---|
| **No `denominator` column** | Normalized view is unavailable. The slicer for it is hidden, not greyed with no reason. | "no denominator: raw only" |
| **Denominator empty on some rows** | Raw works everywhere. Normalized shows "no data" for those places. | count |
| **Denominator is zero** | Normalized is "no data". Never infinity, never zero. | count, with ids |
| **Denominator is negative** | Row is rejected. | count, with ids |
| **No `n` column** | Confidence marking is off. The legend does not mention it. | "no n: confidence off" |
| **`value` empty** | Place is drawn in the theme's "no data" style. **Distinct from zero.** | count |
| **`value` is text, `NaN`, or infinite** | Row is rejected. | count, first 20 shown |
| **Unknown `geo_id`** | Row kept aside, not drawn. | **count and the ids themselves** |
| **Unknown `geo_id` that matches a known alias** | Mapped if the topology has an alias table, and flagged. | "9 rows mapped via aliases" |
| **`geo_id` lost its leading zero** | Fixed by the topology's `id_rule`. | count of ids repaired |
| **Duplicate key** | Follows `on_duplicate`. Default is below. | count, with ids |
| **Mixed `geo_type` in one table** | Split into one layer slice per type. The view draws the one that matches its topology. | rows per type |
| **`geo_type` matches no topology** | Those rows are kept aside. | count per unknown type |
| **Places with no row at all** | Drawn as "no data". | "2,871 of 3,142 places covered" |
| **Many periods** | All are kept. The view picks one. `"latest"` as a view setting means the last in sort order. | list of periods found |
| **Places present in some periods only** | Each period stands alone. | coverage per period |
| **Negative `value`** | Allowed. Needed for margins and net flows. Log scales refuse it with a clear message. | — |
| **Categorical data** | `value` holds a whole-number code; `header.categories` maps code to label. | — |

### Duplicates: three policies

| `on_duplicate` | What happens | When it is right |
|---|---|---|
| `"reject"` | Every row for that key is set aside. The place shows "no data". | Proposed default, not yet chosen. A duplicate means the source has a problem. The map should not guess. |
| `"sum"` | `value`, `denominator`, and `n` are each added up. | The source sends one row per facility and the engine should roll up. Safe only because rates are never sent. |
| `"last"` | Last row wins. | Quick pastes. This is what v1 does silently. |

`on_duplicate` is a load option, passed to the adapter alongside the header. It is not a view or theme field, because it changes what data exists, not how it is shown.

The default is a decision for the person. See `06`.

---

## The load report

Returned on every load. Shown to the user, in words, not hidden in a console.

```json
{
  "rows_in": 3300,
  "rows_kept": 3120,
  "places_covered": 3098,
  "places_total": 3142,
  "periods": ["2022", "2023"],
  "unmatched":  { "count": 17, "sample": ["09110", "09120", "02063"] },
  "aliased":    { "count": 0 },
  "duplicates": { "count": 4,  "sample": ["48201|2023"] },
  "rejected":   { "count": 159, "reasons": { "value_not_number": 150, "denominator_negative": 9 } },
  "empty_values": 22,
  "zero_denominators": 3,
  "has_denominator": true,
  "has_n": true
}
```

**Why the unmatched sample matters here:** the reference topology is a 2018 county list. Connecticut's planning regions, `09110` to `09190`, and Alaska's `02063` and `02066` are not in it. Any recent federal dataset will trip this. v1 would have said nothing.

---

## Validation rules, in order

1. Parse. Match columns by name. Apply paste shorthand.
2. Clean `geo_id` with the topology's `id_rule`.
3. Reject rows with a bad `value`, negative `denominator`, or negative `n`.
4. Group by `geo_type`.
5. Match `geo_id` to the topology. Try aliases. Set unmatched aside.
6. Find duplicate keys. Apply `on_duplicate`.
7. Build the load report.
8. Hand the clean table to the engine. **The engine never sees a bad row.**

---

## Findings

| # | Finding | Effect |
|---|---|---|
| 1 | The seven columns cannot carry units, labels, or formats. | A header is needed. Decision in `06`. |
| 2 | `value` is a number, so categorical layers need a code-to-label map. | Lives in the header. |
| 3 | "Recency" of a value is not a column. | It can be derived when many periods are loaded: the newest period that has a value for that place. Not available with a single period. |
| 4 | Two-variable views, such as bivariate colour or a difference map, need two tables. | The contract stays one table per layer. The **view** names two layers. See `03`. |
| 5 | The 2018 vintage guarantees unmatched rows. | Alias table, or a newer topology alongside. Decision in `06`. |
