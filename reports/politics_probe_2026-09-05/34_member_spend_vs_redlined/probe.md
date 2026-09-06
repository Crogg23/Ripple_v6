# 34 Member spend vs redlined zone

- Checked: no congressional-district geometry is landed (information_schema, both catalogs, DISTRICT/CONGRESS/TIGER/CD/XC_ names: only XC_CENSUS_CB_STATE/COUNTY/ZCTA). So hunch 22's city-level D-grade TRI density was rolled to STATE and set against member-office MRA spend (detail rows, try_to_number, 2016-2025) per office-year; office → state via legislators on last name + first initial, 769 of 1,030 offices unique-matched.
- First number: across 37 states with HOLC cities, Spearman = 0.004 (Pearson 0.12) between D-grade sites/km² and median spend per office-year. Top-quartile pollution states' median spend $1,447,980 vs bottom-quartile $1,418,445 — a 2% gap.
- A hit would have meant the most-polluted places get systematically more (or less) member office money. A miss means office spend is the formula-driven allowance (spread is $1.28M–$1.75M by state) and says nothing about pollution.
- Trap hit: 371K inline subtotal rows and TEXT AMOUNT (filtered, try_to_number); and the missing leg — state is the finest cut possible, and state-level is not the question the hunch asks.
- Nearest substitute for a real test: a district shapefile (Census TIGER CD) to place HOLC polygons in districts. Not landed; not built.

STATUS: dim
HEADLINE: At state level (the only level possible), redlined-zone toxic density and member office spend are unrelated: Spearman 0.004 across 37 states, top vs bottom quartile $1.45M vs $1.42M.
