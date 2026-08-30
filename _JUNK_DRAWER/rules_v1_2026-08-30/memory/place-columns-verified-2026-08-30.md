---
name: place-columns-verified-2026-08-30
description: "2026-08-30 value scan of all 2,244 place columns — 72% are what their name says; the trap list (LONG/LAT false hits, lost leading zeros, 0,0 coords, numeric \"state\" codes) + the Snowflake REGEXP_LIKE whole-string gotcha"
metadata: 
  node_type: memory
  type: project
  originSessionId: b3eeac94-389f-4ecc-be3a-a1812c354077
  modified: 2026-08-30T13:29:22.522Z
---

The 08-29 name-scanned place index (2,244 columns / 386 marts) was value-verified on 2026-08-30 in one
~9-minute read-only pass (one query per mart; ~$1–2). Results: reports/location_index/LOCATION_VALUES.md,
location_columns_verified.csv, location_values_2026-08-30.json; script scripts/location_value_scan_2026_08_30.py.

- 1,615 / 2,238 columns (72%) are usable as named; 306 of 386 marts have ≥1 usable place column
  (230 clean 2-letter state, 125 clean ZIP, 80 county name, 52 clean lat/lon, 53 FIPS).
- Traps: 166 empty, 39 constant, 36 "coordinates" that are counts/money (name scan matched LONG/LAT —
  CFTC positions, NICS LONG_GUN, HCRIS liabilities), 27 FIPS + 10 ZIP with leading zeros lost, 19 lat/lon
  with 0,0 rows, 21 "state" columns that are numeric FIPS/ICPSR codes, 42 "ZIP" that aren't (foreign
  postcodes), 171 place columns that are codes not names. 3 index rows stale (2 marts gone, 1 lost columns).
- Gotcha hit while building it: **Snowflake REGEXP_LIKE matches the WHOLE string** — a '[A-Z]' "has
  letters" test only matches 1-char values. Anchor-free tests need REGEXP_INSTR/RLIKE with '.*' or
  REGEXP_COUNT.

**How to apply:** use location_columns_verified.csv (not the name-scan CSV) when picking place join
columns; it's the input for the handbook's "same location" tier ([[time-and-place-are-joins]]).
