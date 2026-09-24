# Deep pass 10: FHA home loans, FHA apartment loans, Section 8 rents, redlining maps, USDA rural apartments

2026-09-24. Python door, tag `coverage-r2-2026-09-24`. **33 of 35 statements**, all logged in `deep-10.sql`. Each of the 6 connections also ran the two ALTER SESSION lines. Those 12 aren't counted.
Every person or company named here is a data match. None is checked against primary records.

## The menu

| Table | Verdict | The one number | Headline |
|---|---|---|---|
| HOUSING__FED_HUD_MF_SECTION8_CONTRACTS | **live** | White Birch Apartments, Milwaukee: HUD pays $2,574 per unit per month. The national median is $859. That's 3.0x, at 223% of local fair market rent | A second HUD file confirms the rent-to-FMR ratio. The owner join lands 766 of 766 contracts |
| HOUSING__FED_MAPPING_INEQUALITY | probed | Toxic-release plants (TRI 2023) per 100 km²: D areas 13.35, B areas 2.21, A areas 0.07. D is denser in 119 of 212 cities | The join works. The pattern is real but already published, and the plants probably came before the maps |
| HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT | probed | D.R. Horton's lender: median rate 3.99% vs 6.00% for everyone else. 59.3% of its loans sit at exactly 3.99% | The angle is backwards: builder borrowers pay about 1.7 points **less**. That's rate buydowns, already reported |
| HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS | probed | 56,159 units (13.5%) opened by 1980 and have no live affordability clause. 35,324 of them get rent help | The expiring-loan problem is known. The loan's due date isn't a column, so the 50-year term is a guess |
| HOUSING__FED_HUD_MF_FIRM_COMMITMENTS | probed | Top 10 lenders hold 59.7% of FY2020-26 insured dollars ($90.3B, 4,661 deals) | Known concentration. The SAM exclusion join lands 1 of 21,225 projects. The "$1.3B Williamsburg" figure counts one loan 3 times |

---

## 1. Section 8 contracts: **live**

**Checked**
- 24,309 contracts, 23,610 properties, 1,483,772 assisted units. RENT_TO_FMR_RATIO is 0 (meaning unknown) on 298 and null on 81.
- The denominator is Active contracts with a real ratio: 23,341 contracts, 1,458,275 units. Median ratio 94, 90th percentile 130.
- **Over 150% of FMR:** 766 contracts, 60,873 units, 3.3% of contracts.
- By program:
  - Sec. 202 elderly: 7.3% of contracts are over 150%.
  - Loan Management: 2.0%.
  - RAD conversions: 0%.
- What the 766 are:
  - 355 are elderly or disabled buildings (202/811) in cheap markets.
  - 207 are family or mixed buildings in cheap markets.
  - 124 are family buildings in pricey markets.
  - 64 are elderly buildings in pricey markets.
  - 16 are preservation deals.
  - Puerto Rico alone holds 119 contracts and 10,556 units.
  - "Cheap" means the one-bedroom FMR is under $1,300.
- **Owner join:** HUD's owners file (`LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS`) joined on PROPERTY_ID.
  - All 766 land, and the first six letters of the name agree on all 766.
  - It lands 99.9% of all Active contracts.
- **Second field:** HUD's Picture of Subsidized Households (Dec 2025). The first word of its CODE is the PROPERTY_ID.
  - Of the matched properties over 150%, 97% have unit counts that agree within 10%.
  - It gives real HUD spending per unit per month. The national median for project-based Section 8 is $859.
- **Real spending, same-market peers:**
  - Pricey markets: properties over 150% have a median of $1,922, against $1,200 for properties at 150% or under. 137 of 250 matched are over twice the national median.
  - Cheap markets outside Puerto Rico: $933 against $670. Only 18 of 326 are over twice the national median.
  - Properties with a contract over 150% have about 4.3% of the units. They take about 7.5% of matched spending, $1.30B a year.
- **White Birch Apartments Phase 1 & 2, Milwaukee** (property 800245270):
  - 339 units, Loan Management program, 223% of FMR. The one-bedroom FMR is $1,119.
  - HUD spends $2,574 a unit a month, and tenants pay $240. That's about $10.5M a year.
  - A new 240-month contract started 2023-12-01.
  - Owner: Aspen Crossing LIHTC LLC. Manager: Evergreen Real Estate Services, LLC.
- Other cheap-market buildings with checked spending:
  - Bicentennial Towers, Detroit: $1,726 (2.0x the median).
  - Harborview, St. Croix: $1,901.
  - Gateway Plaza, Cincinnati: $1,363.
  - Melville Towers, New Bedford: $1,521.
- Pricey-market leaders:
  - Lands End II, NYC: $5,294 (6.2x).
  - Manhattan Plaza: $3,638 on 1,520 units.
  - Marshall Field Garden, Chicago: $2,559.

**Hit means:** HUD pays two to six times the national per-unit median on named buildings. Two separate HUD files agree, and the owner is on record.

**Miss means:** if the ratio were a bedroom-mix or FMR-vintage artifact, the spending file would show normal dollars. For the buildings above, it doesn't.

**Boring:**
- Rents over FMR can be legal. After an owner recapitalizes, HUD can reset rents to cover the owner's budget or to match comparable buildings. Neither method is tied to FMR. Elderly buildings with services cost more. Puerto Rico's FMRs are very low. Manhattan rents beat the metro-wide FMR.
- White Birch's new 20-year contract with a tax-credit (LIHTC) owner fits a recapitalization deal.
- **Not ruled out.** It's the hinge of the story.
- In cheap markets the typical over-150% building is only modestly expensive ($933). The lead is about 20 buildings, not 766.

**Traps**
- ⚠ The "$ over FMR" figures in the SQL are my estimates: (ratio/100 - 1) × units × FMR × 12. That gives $737M a year above FMR for the 766 contracts, and $2.68B for everything over 100%. Use the spending file's real dollars instead.
- FMR_xBR is 0 when a contract has no units of that size. It is not a real $0 rent.

---

## 2. Redlining maps (Mapping Inequality): probed

**Checked**
- 10,154 neighborhood shapes in 314 city-state pairs. GEOMETRY holds GeoJSON text on every row, and 1 row fails to parse.
- ⚠ FIPS is one blank value on every row. HOLC_ID and YEAR_MAPPED are empty. AREA_DESCRIPTION_DATA holds only `{}`, so the 1930s written reasons never loaded.
- The HOLC_GRADE text has stray spaces and some E and F grades. Use HOLC_GRADE_RANK.
- I did a point-in-shape join to TRI 2023 plants: one point per TRIFD, longitude forced negative, pounds only.
- **Land rate:** 1,549 of 21,856 TRI plants (7.1%) sit inside a graded or ungraded shape.

| Grade | Shapes | km² | Plants | Per 100 km² | M lbs released |
|---|---|---|---|---|---|
| A best | 1,094 | 1,365 | 1 | 0.07 | 0.0 |
| B | 2,480 | 2,942 | 65 | 2.21 | 1.49 |
| C | 3,559 | 5,460 | 318 | 5.82 | 7.82 |
| D redlined | 2,188 | 3,355 | 448 | 13.35 | 23.01 |
| Ungraded | 832 | 2,816 | 717 | 25.46 | 29.05 |

- **Same city:** 212 cities have both B and D areas. D is denser in 119 and B in 17. Both are zero in 76.
- The biggest releasers inside D shapes:
  - Cleveland-Cliffs Cleveland Works: 7.63M lbs.
  - Phillips 66 Bayway, Union Co. NJ: 2.84M lbs.
  - BP Whiting, Lake Co. IN: 1.95M lbs.
  - EQ Detroit (hazardous waste): 1.54M lbs.

**Hit means:** a D grade from the 1930s still predicts about 6x the plants and 13.6x the pounds per km² of a B grade in 2023, and it holds within cities.

**Miss means:** no gradient would kill the angle. There is a gradient.

**Boring:**
- The biggest D-area releasers are century-old refinery and steel sites. The graders likely marked the neighborhoods D because the industry was already next door.
- The ungraded shapes have the most plants of all, at 25 per 100 km². HOLC left industrial land ungraded.
- The written notes that would settle this are the column that didn't load.
- Redlining-to-pollution studies are already published.
- **Not ruled out.**

**Traps**
- ⚠ A grade join that drops the null grade loses 717 of the 1,549 plants. My first pass did exactly that.

---

## 3. FHA home loans, June 2026: probed

**Checked**
- 61,647 loans, one ID each. All are Purchase loans, endorsed in June 2026. 5,192 lenders. Rates run 2.75-8.75 with a median of 5.99, and none are blank.
- I tagged builder-owned lenders by name, 16 brands (DHI, Lennar, NVR, KBHS, Pulte, Inspire, M/I, Jet, K. Hovnanian, Taylor Morrison, Tri Pointe and others). They made 12.1% of FHA purchase loans.
- **D.R. Horton's lender (DHI Mortgage):**
  - 3,791 loans. Median rate 3.99% vs 6.00% for all other lenders.
  - 88.3% of its loans are under 5%. For all other lenders it's 5.7%.
  - 59.3% sit at exactly 3.99%.
  - Compared within the same county (348 counties with 10+ other-lender loans): the rate is 1.72 points lower and the loan is $26,156 bigger.
- **Lennar:** 1,973 loans, 1.58 points lower, $9,919 smaller.
- Every builder brand is cheaper than other lenders in the same county, by 0.30 to 1.72 points. Most carry bigger loans, $21K to $99K more. Shea's 3 loans are the outlier at +$162K.
- **County share**, 129 counties with 100+ FHA loans, against 12.1% nationally:
  - Manatee FL: 49.5% (103 of 208).
  - Denton TX: 47.3%.
  - Fort Bend TX: 46.7%.
  - Bexar TX: 44.3%, with Lennar on top.
  - Pasco FL: 40.2%.
  - Pinal AZ: 35.5%.

**Hit means:** in Sun Belt growth counties, close to half of FHA purchase loans come from the builder's own lender, at a bought-down 3.99%.

**Miss means:** the triage angle said builder borrowers pay higher rates. They don't. That premise is dead.

**Boring:**
- New homes cost more than resales, so the bigger loan is expected. The table has no new-vs-existing flag, so that's **not ruled out**.
- Builder buydowns and D.R. Horton's 3.99% FHA offers are already reported. This is one month.

**Traps**
- Builder lenders barely use down-payment help: DHI 0.1% and Lennar 0.0%, against 1.8% for everyone else. NVR (2.9%) and Jet (1.0%) are the exceptions. A down-payment-help angle is thin here.

---

## 4. USDA rural apartments (Section 515): probed

**Checked**
- 13,550 projects, one per borrower plus project. 417,524 units, 27,365 vacant (6.6%), 282,739 with rental help.
- **Restrictive-use date** (the rule that keeps rents affordable):
  - Already past: 6,400 projects, 184,580 units (44%).
  - None listed: 802 projects.
  - Now through 2030: 1,004 projects, 31,911 units, 23,900 with rental help.
  - 2031-2035: 1,260 projects, 40,978 units.
- The dates follow a formula: about 20 years after opening for the older deals, 50 for the newer ones. Anamosa Villa II: 1986 → 2006. Villa III: 1997 → 2047.
- **The loan's due date is not a column.** My stand-in: 50 years after opening. Projects opened by 1980 with no live clause: 56,159 units (13.5%), 35,324 of them with rental help.
- By state, against 13.5% nationally:
  - IA 36.1%, MO 31.9%, WI 30.7%, IL 30.6%, ME 27.9%.
  - Vacancy: MS 10.1%, IL 9.4%, IA 9.3%, against 6.6% nationally.

**Hit means:** tens of thousands of rural rent-help units can leave the program when their loan is paid off.

**Miss means:** without a real loan due date, the count is a proxy.

**Boring:**
- USDA and housing groups already track and publish the maturing-mortgage problem.
- A past restrictive date doesn't mean the project has left the program. The loan still binds it.
- **Not ruled out.**

**Traps**
- ⚠ 33 "active" projects list every unit vacant. Most are seasonal migrant farm-labor centers (Lodi 94 units, Patterson 92, Arvin 88, Shafter 88) or one-unit on-farm housing. The snapshot catches them off-season. It is not abandonment.
- 22 tax-credit dates are placeholders (before 1987 or after 2080).
- The newest opening is 2019-09-11. The source's own date isn't in the table. It was loaded 2026-08-07.

---

## 5. FHA apartment loan commitments: probed

**Checked**
- 25,557 rows but 24,819 FHA numbers. The raw sum is $307.85B. With one row per FHA number (the latest), it's **$298.32B**, so $9.5B is double-counted.
- FY2020-26, Finally Endorsed, one row per FHA number: 4,661 deals, $90.3B, 88 lenders.
  - The top 10 hold 59.7% of dollars.
  - Greystone $9.06B (10.0%), Dwight Capital $9.02B (10.0%), Berkadia $7.69B, Rockport $6.65B, Walker & Dunlop $5.97B.
- **NYCHA public-housing conversions (PACT):**
  - 5 FHA numbers across 3 NYCHA bundles, all through NYC HDC. They're HFA risk-sharing loans funded through the federal bank (FFB), for major rehab, endorsed in Dec 2021.
  - Latest amount per FHA number:
    - Linden-Penn Wortman: $377.3M.
    - Williamsburg: $298.7M + $150M.
    - Boulevard-Belmont-Sutter-Fiorentino: $331.1M + $200M.
  - Total: $1.36B on 5,205 units.
- **SAM exclusion join** on normalized exact names:
  - Lenders: 0 hits.
  - Project name plus state: 1 hit in 21,225. Lake Village of Auburn Hills, MI: FHA 04411138, a $36.7M refinance endorsed 2008-04-15, lender Greystone.
  - SAM has a HUD "Voluntary Exclusion" for that name and for "Lake Village of Auburn Hills, LLC", active since 2015-05-06. The loan came 7 years before the exclusion.

**Hit means:** a few MAP lenders run most FHA apartment insurance, and NYCHA's PACT conversions draw $1.36B of it.

**Miss means:** the barred-owner angle has almost nothing to land on. There are no owner names here, and 1 project hit.

**Boring:**
- The same few lenders are known to dominate. The PACT deals top the list because they are 1,600-1,900-unit campuses. PACT financing is already reported.

**Traps**
- ⚠ The fact line's "PACT Williamsburg Houses 1.3B" counts FHA 01298082 three times ($340.7M, $340.7M a day later, then $298.7M in 2025) and 01298113 twice. The real figure is $448.7M.
- Always dedupe on FHA_NUMBER before summing MORTGAGE_AMOUNT.

---

## Housekeeping
- I read one landing table, `LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS`, with a SELECT. It has no mart.
- For a few seconds I overwrote the shared scratchpad's `run.py`, which belongs to the deep-4 agent. It rewrote the file right away. No query ran through my copy: `deep-10.sql` didn't exist yet. My own runner lives in `scratchpad/d2_10/`.
