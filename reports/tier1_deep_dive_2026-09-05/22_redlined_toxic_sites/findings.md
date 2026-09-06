# 22. Do redlined neighborhoods have more toxic sites today?

**One-sentence glossary.** HOLC = the 1930s Home Owners' Loan Corporation, which graded city neighborhoods A (best) to D (hazardous, drawn in red) for mortgage risk. TRI = the EPA's Toxic Release Inventory, the yearly list of plants that must report pounds of listed chemicals released.

## First pass said
D areas have 18x more toxic sites than A. No query survived, just the number.

## What was checked

**The mapping table is a slice.**
- `HOUSING__FED_MAPPING_INEQUALITY` (the mart) is 1,155 rows. `LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY` is 10,154.
- The mart holds exactly one polygon per (city, grade): 1,152 pairs, 1,155 rows. Every one of its 1,155 GEOMETRY strings appears verbatim in landing.
- So the mart is an 11% sample, one arbitrary neighborhood per grade per city. Every number below is on LANDING.
- The "814 blank HOLC_GRADE rows" are landing's: 814 exactly empty, 3 more are a lone space or a grade with a trailing space (`'A '`, `'C '`). Trim before grouping. The mart has 282 blanks for the same reason.
- HOLC_ID is one distinct value on both tables. Looks like an ID, isn't.

**Geometry exists and parses.**
- GEOMETRY is GeoJSON text: 9,586 MultiPolygon, 568 Polygon. `TRY_TO_GEOGRAPHY` parses 10,153 of 10,154.
- Total graded land: A 1,366 km², B 2,942, C 5,462, D 3,355; ungraded 2,782.

**Two coordinate formats, handled.**
- `TRI_FACILITY.FAC_LATITUDE` is DDMMSS packed into a number (343425 = 34°34'25"), 48,756 rows; 2,918 are zero; 15 sit in a decimal-looking band. `PREF_LATITUDE` is whole degrees only (0 fractional rows, 43 distinct values), useless at neighborhood scale.
- Converted DDMMSS, swapped the rows where lat and lon were stored backwards, kept 48,193 inside the US box.
- `TRI_BASIC_2023` has clean decimal lat/lon on all 78,647 rows, 21,870 facilities, every one matching a TRI_FACILITY_ID. 770 rows report in grams; converted.

**The join.** Point-in-polygon (`ST_CONTAINS`) of each facility against each HOLC polygon, then counts, land area, and 2023 release pounds by grade.

## The numbers (10,153 parsed polygons)

| grade | km² | 2023 sites inside | per km² | all-time TRI sites inside | per km² | % polygons with a site | 2023 lb / km² |
|---|---|---|---|---|---|---|---|
| A best | 1,366 | 1 | 0.0007 | 58 | 0.042 | 0.1% | 0 |
| B | 2,942 | 65 | 0.022 | 352 | 0.120 | 1.8% | 506 |
| C | 5,462 | 318 | 0.058 | 1,402 | 0.257 | 6.5% | 1,431 |
| **D redlined** | 3,355 | **448** | **0.134** | **1,501** | **0.447** | **13.6%** | **6,856** |
| no grade | 2,782 | 716 | 0.257 | 2,309 | 0.830 | 22.9% | 10,441 |

**D over A:**
- raw 2023 count: 448x (on one A site, so not a number to quote)
- per km², 2023 reporters: 182x (same caveat)
- per km², all-time facility list: **10.5x** (58 vs 1,501 sites, the stable one)
- 500 m buffer, 2023: 1,298 vs 69 = **18.8x** raw. This is almost certainly where the first pass's 18x came from; per km² that same buffer count is 7.7x.

**Pounds follow.** D released 23.0M lb in 2023 inside its polygons, C 7.8M, B 1.5M, A 0 (A's zero is one site; n=1, don't quote it). Widen to a 500 m ring and every grade has real counts: A 1,137, B 2,981, C 10,601, D 19,670 lb/km², D over A **17x**. Per-site medians do not grade (B 255 lb, C 507, D 305): it is more plants, not bigger plants. D's biggest site (a Cleveland steelworks, 7.6M lb) removed leaves D at 4,600 lb/km², still 3x C.

**Top 10 cities** (by 2023 sites inside graded polygons): Detroit 40, Chicago 34, Cleveland 28, Indianapolis 26, Los Angeles 25, St. Louis 24, Milwaukee 19, Akron 18, Memphis 15, Louisville 13. Grade A has zero sites in all ten. D beats A and B in all ten and is the densest grade in nine; Akron is the exception, where C edges D.

## What a hit means / what a miss means
- Hit: sites and pounds rise monotonically A→B→C→D on every method, per area and per polygon. That is what we see. Per-site pounds do not grade (C 507 > D 305), so this is a more-plants gradient, not a bigger-plants one.
- Miss would have been: gradient vanishes when you normalize by area (D polygons could just be bigger; they aren't, D is 3,355 km² to C's 5,462), or a per-site pounds gradient running the other way (it's flat).

## What a skeptic would attack
- **Grade A is one site.** Right. That's why the headline ratio uses the all-time facility list (58 A sites), and why the polygon-share chart exists. Every method agrees on direction; they disagree on magnitude by an order of magnitude.
- **Ungraded land beats D.** True and worth saying: HOLC didn't grade industrial, commercial and vacant land, and that's where plants sit. It doesn't dent the A-to-D ladder, but "redlined areas are the most toxic" is wrong; "redlined areas are the most toxic *residential* areas" is right. And it is an association: HOLC graded neighborhoods next to industry as D partly *because* they were next to industry, so the ungraded row is the confounder, not a side note.
- **Plants inside a 1930s boundary, not people.** The polygons are 1930s residential boundaries; who lives there now is not in these tables. The claim is about land, not residents.
- **Point-in-polygon at TRI precision.** TRI coordinates are facility-centroid, generally sub-100 m; the 500 m buffer check holds the direction (A 69, B 420, C 1,264, D 1,298).
- **One polygon failed to parse.** 1 of 10,154, not material.
- **HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY** was on the hunch's table list; it is county-level injury rates with no HOLC or facility key, so it adds nothing to this question and was not used.

## Traps found
- The MAPPING_INEQUALITY mart is a one-polygon-per-(city,grade) slice of landing, 1,155 of 10,154. Any spatial count off the mart is on 11% of the map.
- TRI_FACILITY.FAC_LATITUDE is packed DDMMSS in a NUMBER column, with ~40 rows lat/lon-swapped; PREF_LATITUDE is truncated to whole degrees.
- HOLC_GRADE carries trailing-space spellings (`'A '`, `'C '`, `' '`); the mart's HOLC_GRADE_RANK is null on those, so a rank-based filter drops them.

STATUS: confirmed but reframed
HEADLINE: Redlined (D) land is the most toxic residential land on the 1930s maps: 448 reporting toxic sites to grade A's 1, 10x the site density of A on the full facility list, and 17x the release pounds per km² within 500 m (19,670 vs 1,137 lb); an association, with ungraded industrial land as the confounder, not a cause.
