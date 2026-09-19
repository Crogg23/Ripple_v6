# Idea cheat sheet, 2026-09-18

125 ideas from THE_WONDER_HANDBOOK.md, same order. Each one: the hunch, why care, the tables, the columns in plain words.
Columns listed are the ones the idea needs, not every column on the table.
Nothing here was run. Table and column names are copied from the handbook.
Grade is the handbook's: A clean shared id, B works with a stated limit, C proxy or partial, D cannot be answered as worded.

# PLACE

## 1) After a flood sends a county's households to FEMA for help, do banks there turn down more mortgages the next year?  `W1` grade B
   - It would mean a flood costs people twice: first the house, then the loan to fix or replace it. The data only reaches county level, not ZIP.

**LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS**
one row = one household's aid registration for one disaster
connects: FIPS, left-padded to 5 digits, matches STATE_CODE + COUNTY_CODE on the mortgage tables; DISASTER_NUMBER matches DISASTERNUMBER on FED_FEMA_DISASTER_DECLARATIONS
 - `DISASTER_NUMBER`  [join]
      - FEMA's number for the disaster this household registered under
 - `DECLARATION_DATE`  [date]
      - the day the disaster was officially declared
 - `FIPS`  [join]
      - five-digit state-plus-county number where the damaged home sits
      - WATCH: 74.21% filled; unpadded text for states 01-09 ('1097' and '01097' both exist, 636 distinct fall to 601 after padding); unpadded, nine states drop out
 - `DAMAGED_ZIP_CODE`  [label]
      - ZIP code of the damaged home
      - WATCH: no mortgage table carries a ZIP, so this cannot be the join
 - `CENSUS_GEOID`  [join]
      - Census id of the small neighborhood area around the damaged home
      - WATCH: 73.75% filled; tract-level join not yet tested
 - `FLOOD_DAMAGE`  [filter]
      - True if the home had flood damage, False if not
      - WATCH: fill not yet measured
 - `FLOOD_DAMAGE_AMOUNT`  [measure]
      - dollars of flood damage FEMA recorded for the home
      - WATCH: fill not yet measured
 - `IHP_AMOUNT`  [measure]
      - total dollars FEMA approved for the household under its Individuals and Households Program, the main aid pot
      - WATCH: fill not yet measured
 - `HA_AMOUNT`  [measure]
      - dollars FEMA approved for housing help: rent, repairs or replacement. A slice of the IHP total
      - WATCH: fill not yet measured

**LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS**
one row = one disaster in one designated area
connects: DISASTERNUMBER matches DISASTER_NUMBER on HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS; used to pick flood disasters by INCIDENTTYPE
 - `DISASTERNUMBER`  [join]
      - FEMA's number for the disaster, one per declared event
      - WATCH: fill not yet measured
 - `INCIDENTTYPE`  [filter]
      - the kind of disaster in words; used to keep only floods
      - WATCH: fill not yet measured
 - `DECLARATIONDATE`  [date]
      - the day the disaster was officially declared
      - WATCH: fill not yet measured
 - `FIPSSTATECODE`  [join]
      - number for the state of the designated area
      - WATCH: fill not yet measured
 - `FIPSCOUNTYCODE`  [join]
      - number for the county of the designated area
      - WATCH: fill not yet measured

**LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC**
one row = one mortgage application and what the lender did with it
connects: STATE_CODE + COUNTY_CODE, both left-padded, match FIPS on HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
 - `AS_OF_YEAR`  [date]
      - the year the application was reported, 2015 to 2017
      - WATCH: a year only, no date on this table
 - `STATE_CODE`  [join]
      - two-digit number for the state where the home sits
      - WATCH: 98.4% filled; unpadded in 2015-2017, left-pad before matching
 - `COUNTY_CODE`  [join]
      - three-digit number for the county where the home sits
      - WATCH: 98.17% filled; unpadded; null-county rows hold 19,331 denials, so require COUNTY_CODE is not null
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
      - WATCH: two file families in this table; group by ACTION_TAKEN first
 - `LOAN_PURPOSE`  [filter]
      - what the loan was for: 1 buy a home, 2 home improvement, 3 refinance. Source: public HMDA code list, not the handbook
 - `DENIAL_REASON_1`  [label]
      - main reason for a denial: 1 debt too high for income, 2 job history, 3 credit history, 4 collateral, 5 not enough cash, 6 info could not be verified, 7 application incomplete, 8 mortgage insurance denied, 9 other. Source: public HMDA code list, not the handbook
      - WATCH: empty on most rows in the profile sample

**LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 to 2024 (7 tables, same columns)**
one row = one mortgage application
connects: COUNTY_CODE matches FIPS on HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS; format and overlap not yet measured
 - `ACTIVITY_YEAR`  [date]
      - the year the application was reported
      - WATCH: fill not yet measured
 - `STATE_CODE`  [join]
      - code for the state where the home sits
      - WATCH: fill and format not yet measured
 - `COUNTY_CODE`  [join]
      - code for the county where the home sits
      - WATCH: fill and format not yet measured
 - `CENSUS_TRACT`  [join]
      - Census id of the small neighborhood area around the home
      - WATCH: fill not yet measured; tract join not yet tested
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
      - WATCH: placeholder rows with '-1': 1,961 in 2018 and 21 in 2019; filter them before any count
 - `LOAN_PURPOSE`  [filter]
      - what the loan was for: 1 buy a home, 2 home improvement, 31 refinance, 32 cash-out refinance, 4 other, 5 not applicable. Source: public HMDA code list, not the handbook
      - WATCH: layout changed at 2018, check codes by hand against 2015-2017
 - `DENIAL_REASON_1`  [label]
      - main reason for a denial: 1 debt too high for income, 2 job history, 3 credit history, 4 collateral, 5 not enough cash, 6 info could not be verified, 7 application incomplete, 8 mortgage insurance denied, 9 other. Source: public HMDA code list, not the handbook
      - WATCH: fill not yet measured

---

## 2) Do cities that got more red ink on the 1930s federal lending maps have dirtier drinking-water records today?  `W2` grade C
   - It would mean a ninety-year-old lending map still shows up at the tap. The data can only compare whole cities, never neighborhoods.

**LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY**
one row = one graded neighborhood shape on a 1930s city map
connects: CITY + STATE match CITY_SERVED + STATE_SERVED on ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS; or FIPS matches COUNTY_FIPS there, only if FIPS proves filled
 - `CITY`  [join]
      - name of the city the old map covers
      - WATCH: fill not yet measured
 - `STATE`  [join]
      - state of the city the old map covers
      - WATCH: fill not yet measured
 - `FIPS`  [join]
      - county number for the mapped city, if it was ever filled in
      - WATCH: unmeasured: may be filled, blank, or empty string; count before planning on it
 - `HOLC_GRADE`  [filter]
      - the map's letter grade for the neighborhood: A best through D, the red one
      - WATCH: 814 rows have a blank grade; 3 trailing-space spellings of the grades
 - `YEAR_MAPPED`  [date]
      - the year the city's map was drawn
      - WATCH: fill not yet measured
 - `GEOMETRY`  [measure]
      - the neighborhood's outline, stored as GeoJSON text
      - WATCH: parsed to a shape on 10,153 of 10,154 rows
 - `LAT`  [label]
      - latitude of a point for the neighborhood shape
      - WATCH: fill not yet measured
 - `LON`  [label]
      - longitude of a point for the neighborhood shape
      - WATCH: fill not yet measured
 - `HOLC_ID`  [label]
      - looks like a neighborhood id but holds a single value
      - WATCH: not a real id: one distinct value

**LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY**
one row = one merged shape per city and grade, a summary of the full map
connects: CITY + STATE match CITY_SERVED + STATE_SERVED on ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
 - `CITY`  [join]
      - name of the city the old map covers
 - `STATE`  [join]
      - state of the city the old map covers
 - `HOLC_GRADE`  [filter]
      - the map's letter grade: A best through D, the red one
      - WATCH: blank on some rows
 - `HOLC_GRADE_RANK`  [filter]
      - the letter grade as a number, 1 for A through 4 for D
 - `GEOMETRY`  [measure]
      - the merged outline of all same-grade areas in the city
      - WATCH: mart is 1,155 rows against 10,154, 11% of the shapes; use the landing table for any area count
 - `FIPS`  [join]
      - county number column that was never filled in
      - WATCH: blank on all 1,155 rows

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS**
one row = one area, a county, city or ZIP, served by one water system
connects: CITY_SERVED + STATE_SERVED match CITY + STATE on FED_MAPPING_INEQUALITY; PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
 - `PWSID`  [join]
      - the water system's id number, given by the drinking-water regulator
      - WATCH: 100% filled, 418,885 distinct; ids starting 04 to 10 are EPA regions and never match a place
 - `AREA_TYPE_CODE`  [filter]
      - what kind of area the row names; coded value, look at distinct values first (CN, CT, ZC, TR, IR seen)
 - `CITY_SERVED`  [join]
      - name of the city the water system serves
      - WATCH: name join; overlap not yet measured
 - `STATE_SERVED`  [join]
      - state of the area the water system serves
 - `COUNTY_FIPS`  [join]
      - five-digit state-plus-county number the water system serves
      - WATCH: filled on 404,823 of 405,396 named county rows

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT**
one row = one violation with its enforcement fields
connects: PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
 - `PWSID`  [join]
      - the water system's id number, given by the drinking-water regulator
      - WATCH: 100% filled, 265,738 distinct; ids starting 04 to 10 are EPA regions and never match a place
 - `VIOLATION_ID`  [measure]
      - id number of one violation; count these, not rows
      - WATCH: row grain not measured; one violation may repeat per enforcement action, so count distinct
 - `IS_HEALTH_BASED_IND`  [filter]
      - Y if the violation is about unsafe water, N if it is paperwork or testing
 - `VIOLATION_CODE`  [label]
      - which rule was broken; coded value, look at distinct values first (03, 23, 22, 3A seen)
 - `NON_COMPL_PER_BEGIN_DATE`  [date]
      - the day the water system started being out of compliance
      - WATCH: 93.5% filled; minimum 1900-01-01 is a placeholder, bound every date filter

---

## 3) Fold all the one-building companies back together and see which landlords really hold the most government-backed apartment buildings, and what the rent-subsidy contracts on them look like.  `W3` grade B
   - It would show whether a few big players sit behind thousands of separate company names. It would also show if their buildings get richer rents or all expire at once.

**LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS**
one row = one HUD-assisted or insured apartment property with its owner and manager
connects: PROPERTY_ID matches PROPERTY_ID on HOUSING__FED_HUD_MF_SECTION8_CONTRACTS; group by folded OWNER_ORGANIZATION_NAME + OWNER_ADDRESS_LINE1, or by MGMT_AGENT_PARTICIPANT_ID
 - `PROPERTY_ID`  [join]
      - the housing department's id number for the apartment property
      - WATCH: space-padded text; TRIM before any compare. Fill not yet measured
 - `PROPERTY_TOTAL_UNIT_COUNT`  [measure]
      - how many apartments are in the property
      - WATCH: fill not yet measured
 - `OWNER_PARTICIPANT_ID`  [label]
      - the housing department's id number for the owning company
      - WATCH: nearly one id per building: 22,352 ids on 23,612 properties, biggest id 21 buildings; finds no chains. 37 rows carry id 0 with a blank name
 - `OWNER_ORGANIZATION_NAME`  [join]
      - name of the company that owns the property
      - WATCH: space-padded; blanks are a single space, not NULL. 54 names sit on more than one owner id
 - `OWNER_ADDRESS_LINE1`  [join]
      - street line of the owner's mailing address
      - WATCH: space-padded; TRIM and fold by hand
 - `OWNER_ZIP_CODE`  [label]
      - ZIP code of the owner's mailing address
      - WATCH: space-padded; fill not yet measured
 - `OWNER_COMPANY_TYPE`  [filter]
      - what kind of company the owner is; coded value, look at distinct values first
      - WATCH: fill not yet measured
 - `OWNERSHIP_EFFECTIVE_DATE`  [date]
      - the day this owner took over the property
      - WATCH: fill not yet measured
 - `MGMT_AGENT_PARTICIPANT_ID`  [join]
      - id number of the company that manages the building day to day
      - WATCH: 5,209 manager ids; biggest block 136 buildings
 - `MGMT_AGENT_ORG_NAME`  [label]
      - name of the company that manages the building
      - WATCH: space-padded
 - `PRIMARY_FINANCING_TYPE`  [filter]
      - the main kind of government financing on the property; coded value, look at distinct values first
      - WATCH: fill not yet measured
 - `IS_INSURED_IND`  [filter]
      - flag for whether the property's loan is government insured; coded value, look at distinct values first
      - WATCH: fill not measured; count distinct values before using
 - `IS_HUD_HELD_IND`  [filter]
      - flag for whether the housing department itself holds the loan; coded value, look at distinct values first
      - WATCH: fill not measured; count distinct values before using
 - `COUNTY_CODE`  [label]
      - code for the county where the property sits
      - WATCH: fill not yet measured

**LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS**
one row = one rent-subsidy contract on one property
connects: PROPERTY_ID matches PROPERTY_ID on FED_HUD_MF_PROPERTIES_OWNERS
 - `PROPERTY_ID`  [join]
      - the housing department's id number for the apartment property
      - WATCH: fill not yet measured; TRIM the owner-file side before matching
 - `CONTRACT_NUMBER`  [label]
      - the id number of the rent-subsidy contract
 - `TRACS_STATUS_NAME`  [filter]
      - where the contract stands: Active, Expired, Pending, Suspended or Executed
 - `ASSISTED_UNITS_COUNT`  [measure]
      - how many apartments the contract subsidizes
 - `RENT_TO_FMR_RATIO`  [measure]
      - contract rent divided by the local fair-market rent
 - `RENT_TO_FMR_DESCRIPTION`  [filter]
      - the same ratio as a band in words, such as Below 80% FMR
 - `PROGRAM_TYPE_NAME`  [filter]
      - which subsidy program the contract falls under, such as Sec 8 NC or LMSA
 - `TRACS_EFFECTIVE_DATE`  [date]
      - the day the contract took effect
 - `TRACS_OVERALL_EXPIRATION_DATE`  [date]
      - the day the contract finally runs out
      - WATCH: sister column TRACS_CURRENT_EXPIRATION_DATE has a 1900-01-02 placeholder; bound the dates

---

## 4) After a county takes its first really expensive storm, do some banks quietly stop writing mortgages there?  `W5` grade B
   - It would mean storm damage drives lenders out, leaving homeowners with fewer places to borrow. That is a slow second hit after the storm itself.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS**
one row = one storm event in one county or forecast zone
connects: STATE_FIPS + CZ_FIPS, on rows where CZ_TYPE = 'C', match STATE_CODE + COUNTY_CODE on HOUSING__FED_CFPB_HMDA_HISTORIC and COUNTY_CODE on the 2018-2024 tables
 - `YEAR`  [date]
      - the calendar year the storm happened, 1996 to 2025
 - `STATE_FIPS`  [join]
      - number for the state the storm hit
 - `CZ_FIPS`  [join]
      - number for the county or forecast zone the storm hit
      - WATCH: only a county number when CZ_TYPE is 'C'
 - `CZ_TYPE`  [filter]
      - says what CZ_FIPS means: C is a county, Z is a forecast zone
      - WATCH: 'Z' rows are forecast zones, not counties, and drop out of the join
 - `EVENT_TYPE`  [filter]
      - the kind of storm in words, such as Hail or Flash Flood
 - `DAMAGE_PROPERTY`  [measure]
      - property damage in dollars, written as text like 10K or 2M
      - WATCH: text with K and M suffixes; must be parsed
 - `EPISODE_ID`  [label]
      - id that ties together the separate rows of one larger storm

**LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC**
one row = one mortgage application
connects: STATE_CODE + COUNTY_CODE match STATE_FIPS + CZ_FIPS on ENVIRONMENT__FED_NOAA_STORM_EVENTS; RESPONDENT_ID matches ARID_2017 on HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF
 - `RESPONDENT_ID`  [join]
      - the lender's id number under the old 2015-2017 system
      - WATCH: 100% filled, 7,391 distinct; may need its agency code attached before it matches ARID_2017; no lender name on this table
 - `AGENCY_CODE`  [join]
      - which regulator the lender reports to; coded value, look at distinct values first (7, 9, 3, 5, 1 seen)
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
      - WATCH: two file families in this table; group by ACTION_TAKEN first
 - `STATE_CODE`  [join]
      - two-digit number for the state where the home sits
      - WATCH: 98.4% filled; unpadded in 2015-2017, left-pad before matching
 - `COUNTY_CODE`  [join]
      - three-digit number for the county where the home sits
      - WATCH: 98.17% filled; unpadded; null-county rows hold 19,331 denials, so require COUNTY_CODE is not null

**LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 to 2024 (7 tables, same columns)**
one row = one mortgage application
connects: COUNTY_CODE matches the storm county key; LEI matches LEI_2018 on HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF
 - `LEI`  [join]
      - the lender's twenty-character global company id, used from 2018 on
      - WATCH: bridge to the sampled LAR table measured at 84%; fill not yet measured
 - `COUNTY_CODE`  [join]
      - code for the county where the home sits
      - WATCH: format and fill not yet measured
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
      - WATCH: placeholder rows with '-1': 1,961 in 2018 and 21 in 2019; filter them before any count
 - `ACTIVITY_YEAR`  [date]
      - the year the application was reported
      - WATCH: fill not yet measured

**LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF**
one row = one lender's 2017 id and its later company id
connects: ARID_2017 matches RESPONDENT_ID on HOUSING__FED_CFPB_HMDA_HISTORIC; LEI_2018 matches LEI on FED_CFPB_HMDA_LAR_2018
 - `ARID_2017`  [join]
      - the lender's old id as it stood in 2017
      - WATCH: format against RESPONDENT_ID unverified; 5,399 lenders here against 7,391 distinct RESPONDENT_IDs
 - `RESPONDENT_NAME`  [label]
      - the name of the bank or mortgage lender
 - `LEI_2018`  [join]
      - the lender's new global company id in 2018
 - `LEI_2019`  [join]
      - the lender's new global company id in 2019
      - WATCH: 93.91% filled
 - `LEI_2020`  [join]
      - the lender's new global company id in 2020
      - WATCH: 76.5% filled

---

## 5) Find the counties that lost their doctors, their bank branches and their factories all in the same ten years.  `W6` grade C
   - It would put a name on the places being hollowed out from three sides at once. The factory part only covers one year, so that leg is weak.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS**
one row = one bank branch in one survey year
connects: BRANCH_STATE_COUNTY_FIPS matches COUNTY_FIPS on XWALK_ZCTA_COUNTY
 - `SURVEY_YEAR`  [date]
      - the year of the bank regulator's yearly branch survey
 - `BRANCH_STATE_COUNTY_FIPS`  [join]
      - five-digit state-plus-county number where the branch sits
 - `BRANCH_UNINUM`  [measure]
      - the regulator's id number for one physical branch
      - WATCH: a branch missing next year can be a merger or renumbering
 - `FDIC_CERT`  [label]
      - the regulator's certificate number for the bank that owns the branch
 - `BRANCH_DEPOSITS_THOUSANDS`  [measure]
      - deposits held at the branch, in thousands of dollars

**LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 to DY2024 (12 tables, same columns)**
one row = one clinician who billed Medicare Part B in one year
connects: RNDRNG_PRVDR_ZIP5 matches ZCTA5 on XWALK_ZCTA_COUNTY; NPI matches NPI on FED_CMS_NPPES_DEACTIVATED
 - `NPI`  [join]
      - the ten-digit national id number of the doctor or clinician
 - `RNDRNG_PRVDR_ENT_CD`  [filter]
      - marks whether the biller is a person or an organization; coded value, look at distinct values first
      - WATCH: blank is an empty string, not NULL
 - `RNDRNG_PRVDR_TYPE`  [filter]
      - the clinician's specialty in words, such as the kind of doctor
      - WATCH: values not yet measured; must be read to keep physicians and drop nurse practitioners, labs, suppliers
 - `RNDRNG_PRVDR_ZIP5`  [join]
      - five-digit ZIP of the clinician's office
      - WATCH: blank is an empty string, not NULL; single-building hospital ZIPs have no ZIP-area and drop out
 - `RNDRNG_PRVDR_STATE_FIPS`  [label]
      - number for the state of the clinician's office
      - WATCH: fill not yet measured
 - `RNDRNG_PRVDR_RUCA`  [filter]
      - a rural-to-urban score for the office ZIP; coded value, look at distinct values first
      - WATCH: fill not yet measured
 - `TOT_BENES`  [measure]
      - how many Medicare patients the clinician saw that year
      - WATCH: fill not yet measured

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP-area and county pair
connects: ZCTA5 matches RNDRNG_PRVDR_ZIP5 on the Part B tables; COUNTY_FIPS matches BRANCH_STATE_COUNTY_FIPS and AREA_FIPS
 - `ZCTA5`  [join]
      - five-digit ZIP-area, the Census stand-in for a postal ZIP
      - WATCH: 10,186 of 33,791 ZIP-areas cross a county line; largest-area pick was right 47.1% of the time on those
 - `COUNTY_FIPS`  [join]
      - five-digit state-plus-county number the ZIP-area falls in

**LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED**
one row = one deactivated provider id and its date
connects: NPI matches NPI on the Part B tables; optional, tells a doctor who quit from one who moved
 - `NPI`  [join]
      - the ten-digit national id number of the provider who was switched off
 - `NPPES_DEACTIVATION_DATE`  [date]
      - the day the provider's id was switched off, stored as text MM/DD/YYYY
      - WATCH: text, not a date; parse it. Fill not yet measured

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_BLS_QCEW**
one row = one area, industry and ownership cell
connects: AREA_FIPS matches COUNTY_FIPS on XWALK_ZCTA_COUNTY
 - `AREA_FIPS`  [join]
      - five-digit number for the county or other area the cell covers
 - `INDUSTRY_CODE`  [filter]
      - code for the industry the cell covers; coded value, look at distinct values first
 - `ANNUAL_AVG_ESTABLISHMENTS`  [measure]
      - average number of workplaces in that industry and area over the year
      - WATCH: 2022 only; one year of movement, not a decade
 - `ANNUAL_AVG_EMPLOYMENT`  [measure]
      - average number of jobs in that industry and area over the year
      - WATCH: 2022 only; one year of movement, not a decade
 - `YEAR`  [date]
      - the calendar year the job and workplace numbers cover
      - WATCH: 2022 on every row

**LIBRARY_RAW.LANDING.FED_BLS_QCEW**
one row = the same cells, raw, with year-over-year change columns
connects: AREA_FIPS matches COUNTY_FIPS on XWALK_ZCTA_COUNTY
 - `AREA_FIPS`  [join]
      - five-digit number for the county or other area the cell covers
      - WATCH: fill not yet measured
 - `INDUSTRY_CODE`  [filter]
      - code for the industry the cell covers; coded value, look at distinct values first
      - WATCH: fill not yet measured
 - `OTY_ANNUAL_AVG_ESTABS_CHG`  [measure]
      - change in the number of workplaces against the year before
      - WATCH: one year of change only; fill not yet measured
 - `OTY_ANNUAL_AVG_EMPLVL_CHG`  [measure]
      - change in the number of jobs against the year before
      - WATCH: one year of change only; fill not yet measured

---

## 6) Find a single post office box that gets mail for a medical provider, a political committee and a federal contractor all at once.  `W7` grade B
   - It would mean three kinds of money that should be unrelated share one mail drop. That is the kind of overlap worth a closer look at who is behind it.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES**
one row = one provider id, a person or an organization
connects: cleaned PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS + first 5 of PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE match cleaned CMTE_ST1 + first 5 of CMTE_ZIP on FINANCE__FED_FEC_COMMITTEES
 - `NPI`  [measure]
      - the ten-digit national id number of the medical provider
 - `PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME`  [label]
      - the legal name of the provider when it is an organization
 - `PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS`  [join]
      - first line of the address where the provider gets mail
      - WATCH: no cleaned-address column exists; one hospital address is reused by thousands of its doctors, so keep to box or suite lines. Fill not yet measured
 - `PROVIDER_BUSINESS_MAILING_ADDRESS_CITY_NAME`  [label]
      - city of the provider's mailing address
      - WATCH: fill not yet measured
 - `PROVIDER_BUSINESS_MAILING_ADDRESS_STATE_NAME`  [label]
      - state of the provider's mailing address
      - WATCH: fill not yet measured
 - `PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE`  [join]
      - ZIP code of the provider's mailing address; use the first five digits
      - WATCH: fill not yet measured

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES**
one row = one committee in one election-cycle file
connects: cleaned CMTE_ST1 + first 5 of CMTE_ZIP match the cleaned mailing line and ZIP on HEALTH__FED_CMS_NPPES and on the contract tables
 - `CMTE_ID`  [measure]
      - the election regulator's id number for the political committee
      - WATCH: ids repeat across cycles with no cycle column: 60,031 rows, 38,693 ids; count committees, never rows
 - `CMTE_NM`  [label]
      - the name the political committee registered under
 - `CMTE_ST1`  [join]
      - first line of the committee's street or box address
      - WATCH: must be cleaned by hand
 - `CMTE_CITY`  [label]
      - city named in the political committee's mailing address
 - `CMTE_ST`  [label]
      - state named in the political committee's mailing address
 - `CMTE_ZIP`  [join]
      - ZIP code of the committee's address; use the first five digits
      - WATCH: 50 blank
 - `CMTE_TP`  [filter]
      - the kind of committee; coded value, look at distinct values first (H, N, Q, O, S seen)

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_BULK_COMMITTEES**
one row = one committee in one cycle
connects: cleaned CMTE_ST1 + first 5 of CMTE_ZIP match the same address key as the other tables
 - `FEC_CMTE_ID`  [measure]
      - the election regulator's id number for the political committee
 - `CMTE_ST1`  [join]
      - first line of the committee's street or box address
      - WATCH: must be cleaned by hand
 - `CMTE_ZIP`  [join]
      - ZIP code of the committee's address; use the first five digits
      - WATCH: 9 blank
 - `CYCLE`  [date]
      - the two-year election cycle the row belongs to
      - WATCH: range not yet measured

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: cleaned RECIPIENT_ADDRESS_LINE_1 + first 5 of RECIPIENT_ZIP_4_CODE match the same address key built from HEALTH__FED_CMS_NPPES and FINANCE__FED_FEC_COMMITTEES
 - `RECIPIENT_UEI`  [measure]
      - the government's id for the company that got the contract
      - WATCH: fill not yet measured
 - `RECIPIENT_NAME`  [label]
      - name of the company that got the contract
      - WATCH: fill not yet measured
 - `RECIPIENT_ADDRESS_LINE_1`  [join]
      - first line of the contractor's address
      - WATCH: must be cleaned by hand; fill not yet measured
 - `RECIPIENT_CITY_NAME`  [label]
      - city named in the federal contractor's address
      - WATCH: fill not yet measured
 - `RECIPIENT_ZIP_4_CODE`  [join]
      - the contractor's ZIP, nine-digit style; use the first five digits
      - WATCH: fill not yet measured

---

## 7) Find the counties that already had only about one doctor for every thousand people, and are still losing them.  `W8` grade C
   - These would be the places where seeing a doctor is turning into a long drive. The count only covers doctors who bill Medicare, and the population number stops at 2015.

**LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 to DY2024 (12 tables, same columns)**
one row = one clinician who billed Medicare Part B in one year
connects: RNDRNG_PRVDR_ZIP5 matches ZCTA5 on XWALK_ZCTA_COUNTY
 - `NPI`  [join]
      - the ten-digit national id number of the doctor or clinician
 - `RNDRNG_PRVDR_ENT_CD`  [filter]
      - marks whether the biller is a person or an organization; coded value, look at distinct values first
      - WATCH: blank is an empty string, not NULL
 - `RNDRNG_PRVDR_TYPE`  [filter]
      - the clinician's specialty in words, such as the kind of doctor
      - WATCH: values not yet measured; must be read to keep physicians and drop nurse practitioners, labs, suppliers
 - `RNDRNG_PRVDR_ZIP5`  [join]
      - five-digit ZIP of the clinician's office
      - WATCH: blank is an empty string, not NULL; single-building hospital ZIPs have no ZIP-area and drop out
 - `RNDRNG_PRVDR_RUCA`  [filter]
      - a rural-to-urban score for the office ZIP; coded value, look at distinct values first
      - WATCH: fill not yet measured
 - `TOT_BENES`  [measure]
      - how many Medicare patients the clinician saw that year
      - WATCH: fill not yet measured

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP-area and county pair
connects: ZCTA5 matches RNDRNG_PRVDR_ZIP5 on the Part B tables; COUNTY_FIPS matches FIPS on HEALTH__FED_CDC_DRUG_POISONING_COUNTY and COMMON_STATE_COUNTY_FIPS_CODE on HEALTH__FED_HRSA_HPSA_PRIMARY_CARE
 - `ZCTA5`  [join]
      - five-digit ZIP-area, the Census stand-in for a postal ZIP
      - WATCH: 10,186 of 33,791 ZIP-areas cross a county line; largest-area pick was right 47.1% of the time on those
 - `COUNTY_FIPS`  [join]
      - five-digit state-plus-county number the ZIP-area falls in

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY**
one row = one county in one year, with its population
connects: FIPS matches COUNTY_FIPS on XWALK_ZCTA_COUNTY, years 2013-2015
 - `FIPS`  [join]
      - five-digit state-plus-county number for the county the row covers
 - `YEAR`  [date]
      - the year of the population figure, 1999 to 2015
      - WATCH: ends at 2015; later years have no population to divide by
 - `POPULATION`  [measure]
      - how many people lived in the county that year
      - WATCH: ends at 2015

**LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE**
one row = one component of one primary-care shortage designation
connects: COMMON_STATE_COUNTY_FIPS_CODE matches COUNTY_FIPS on XWALK_ZCTA_COUNTY
 - `COMMON_STATE_COUNTY_FIPS_CODE`  [join]
      - five-digit state-plus-county number of the shortage area
 - `DESIGNATION_DATE`  [date]
      - the day the area was officially named short of doctors
 - `WITHDRAWN_DATE`  [date]
      - the day the shortage label was taken away, if it was
      - WATCH: 61.28% filled; empty means never withdrawn
 - `HPSA_STATUS`  [filter]
      - where the shortage label stands: Designated, Withdrawn or Proposed For Withdrawal
 - `HPSA_FTE`  [measure]
      - how many full-time doctors the area is judged to be missing
 - `DESIGNATION_POPULATION`  [measure]
      - how many people the shortage label covers
 - `FORMAL_RATIO`  [measure]
      - people per doctor in the area, as text like 3500:1
      - WATCH: text like '3500:1'; was wiped once by a numeric cast, read values before trusting
 - `RURAL_STATUS`  [filter]
      - Rural, Non-Rural, Partially Rural or Unknown for the shortage area

**LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED**
one row = one deactivated provider id and its date
connects: NPI matches NPI on the Part B tables
 - `NPI`  [join]
      - the ten-digit national id number of the provider who was switched off
 - `NPPES_DEACTIVATION_DATE`  [date]
      - the day the provider's id was switched off, stored as text MM/DD/YYYY
      - WATCH: text, not a date; parse it. Fill not yet measured

---

## 8) When a rural county loses its very last bank branch, does its clinic shut down soon after?  `W9` grade B
   - It would mean the basics of a small town fall like dominoes, money first and medicine next. That tells you where to look for the next closure.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER**
one row = one Medicare-certified non-hospital facility, latest record only
connects: FIPS_STATE_CD + FIPS_CNTY_CD, left-padded to 3, match BRANCH_STATE_COUNTY_FIPS on FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS
 - `CCN`  [label]
      - Medicare's certification number for the facility
      - WATCH: only the latest record per CCN is kept; a close-and-reopen shows one state
 - `PRVDR_CTGRY_CD`  [filter]
      - the kind of facility; coded value, look at distinct values first (21, 01, 12, 19, 06 seen)
      - WATCH: which value means rural health clinic is not yet measured
 - `PRVDR_CTGRY_SBTYP_CD`  [filter]
      - a finer kind of facility inside the main kind; coded value, look at distinct values first
 - `FAC_NAME`  [label]
      - the name on the door of the facility
 - `CBSA_URBN_RRL_IND`  [filter]
      - U if the facility is in an urban area, R if rural
      - WATCH: 323 blank
 - `TRMNTN_EXPRTN_DT`  [date]
      - the day the facility's Medicare participation ended or expired
      - WATCH: 40.92% filled; termination or expiration, not always a closed door
 - `PGM_TRMNTN_CD`  [filter]
      - why participation ended; coded value, look at distinct values first (00, 01, 07, 04, 05 seen)
      - WATCH: values not yet measured; needed to tell a closure from a merger or paperwork lapse
 - `FIPS_STATE_CD`  [join]
      - number for the state where the facility sits
      - WATCH: 316 blank
 - `FIPS_CNTY_CD`  [join]
      - number for the county where the facility sits
      - WATCH: 99.29% filled; a number, unpadded, left-pad to 3

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS**
one row = one bank branch in one survey year
connects: BRANCH_STATE_COUNTY_FIPS matches FIPS_STATE_CD + FIPS_CNTY_CD on HEALTH__FED_CMS_POS_OTHER
 - `SURVEY_YEAR`  [date]
      - the year of the bank regulator's yearly branch survey
 - `BRANCH_STATE_COUNTY_FIPS`  [join]
      - five-digit state-plus-county number where the branch sits
 - `BRANCH_UNINUM`  [measure]
      - the regulator's id number for one physical branch
      - WATCH: a branch missing next year can be a merger or renumbering
 - `FDIC_CERT`  [label]
      - the regulator's certificate number for the bank that owns the branch
 - `BRANCH_NAME`  [label]
      - the name the bank gives this branch

---

## 9) Do rural counties pay more in federal income tax than they get back in federal grants, loans and contracts?  `W10` grade B
   - It would flip the usual story about who carries whom. The data holds one tax year, 2016, so this is a snapshot and not a trend.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI**
one row = one ZIP in one income bracket
connects: ZIP_CODE matches ZCTA5 on XWALK_ZCTA_COUNTY
 - `ZIP_CODE`  [join]
      - five-digit ZIP the tax returns were filed from
      - WATCH: bridge is ZIP-area, not postal ZIP; a ZIP's tax must be split or assigned
 - `AGI_STUB`  [filter]
      - which income bracket the row covers, a number; values 1 to 6 seen
      - WATCH: sum across brackets to get the whole ZIP
 - `TOTAL_TAX`  [measure]
      - total federal income tax owed by returns in that ZIP and bracket
 - `AGI`  [measure]
      - total income reported by returns in that ZIP and bracket
      - WATCH: stored as text; cast it
 - `N_RETURNS`  [measure]
      - how many tax returns were filed in that ZIP and bracket
      - WATCH: stored as text; cast it
 - `TAX_YEAR`  [date]
      - the tax year of the numbers
      - WATCH: 2016 on every row

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP-area and county pair
connects: ZCTA5 matches ZIP_CODE on FINANCE__FED_IRS_SOI; COUNTY_FIPS matches PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on the spending tables and BRANCH_STATE_COUNTY_FIPS
 - `ZCTA5`  [join]
      - five-digit ZIP-area, the Census stand-in for a postal ZIP
      - WATCH: 10,186 of 33,791 ZIP-areas cross a county line; largest-area pick was right 47.1% of the time on those
 - `COUNTY_FIPS`  [join]
      - five-digit state-plus-county number the ZIP-area falls in
 - `XWALK_TYPE`  [label]
      - a label for how the pairing was built; every row says clean

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 to FY2026 (20 tables, same columns)**
one row = one grant, loan or direct-payment transaction
connects: PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on FED_USASPENDING_ASSISTANCE_FY2016 matches COUNTY_FIPS on XWALK_ZCTA_COUNTY
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed in this transaction; negative means money pulled back
      - WATCH: loans show $0.00 here on 11,788,945 rows; negative rows belong in the sum
 - `FACE_VALUE_OF_LOAN`  [measure]
      - the size of the loan in dollars, where the row is a loan
      - WATCH: this is where loan money lives; decide loans in or out before summing
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - the kind of aid: 07 and 08 are loans; others coded value, look at distinct values first. Source: public USAspending code list, not the handbook
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the government budget year the transaction happened in
      - WATCH: fill not yet measured
 - `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`  [join]
      - five-digit state-plus-county number where the funded work takes place
      - WATCH: 71% filled in FY2007 rising to 99% in FY2020; marks where work is done, not where the recipient lives

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on FED_USASPENDING_CONTRACTS_FY2016 matches COUNTY_FIPS on XWALK_ZCTA_COUNTY
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed in this transaction; negative means money pulled back
      - WATCH: negative rows belong in the sum
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the government budget year the transaction happened in
 - `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`  [join]
      - five-digit state-plus-county number where the contract work takes place
      - WATCH: 93% filled, 2,894 distinct counties, on FY2024

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS**
one row = one bank branch in one survey year
connects: BRANCH_STATE_COUNTY_FIPS matches COUNTY_FIPS on XWALK_ZCTA_COUNTY; borrowed only for its metro flag
 - `BRANCH_STATE_COUNTY_FIPS`  [join]
      - five-digit state-plus-county number where the branch sits
 - `BRANCH_METRO_FLAG`  [filter]
      - 1 if the branch sits in a big-city area, 0 if not
      - WATCH: a borrowed stand-in for rural; fill not yet measured
 - `BRANCH_MICRO_FLAG`  [filter]
      - 1 if the branch sits in a small-town area, 0 if not
      - WATCH: fill not yet measured

---

## 10) Do small country water systems break the drinking-water rules more often per person served than big city ones?  `W11` grade B
   - It would mean the fewer neighbors you share a pipe with, the less you can trust the tap. It might also just mean small systems skip paperwork.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS**
one row = one public water system
connects: PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT and on ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
 - `PWSID`  [join]
      - the water system's id number, given by the drinking-water regulator
      - WATCH: ids starting 04 to 10 are EPA regions and never match a state
 - `POPULATION_SERVED_COUNT`  [measure]
      - how many people drink from this system
      - WATCH: a size stand-in, not a rural measure; tiny systems make extreme rates. Fill not yet measured
 - `POP_CAT_5_CODE`  [filter]
      - the system's size band by people served, numbered 1 to 5
      - WATCH: fill not yet measured
 - `PWS_TYPE_CODE`  [filter]
      - the kind of system; coded value, look at distinct values first (TNCWS, CWS, NTNCWS, NP seen)
      - WATCH: fill not yet measured
 - `PWS_ACTIVITY_CODE`  [filter]
      - whether the system is still running; coded value, look at distinct values first (I, A, N seen)
      - WATCH: fill not yet measured
 - `OWNER_TYPE_CODE`  [filter]
      - who owns the system; coded value, look at distinct values first (P, L, M, S seen)
      - WATCH: about 49,268 rows empty
 - `SERVICE_CONNECTIONS_COUNT`  [measure]
      - how many homes and buildings are hooked up to the system
      - WATCH: fill not yet measured

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT**
one row = one violation with its enforcement fields
connects: PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
 - `PWSID`  [join]
      - the water system's id number, given by the drinking-water regulator
      - WATCH: 100% filled, 265,738 distinct; ids starting 04 to 10 are EPA regions and never match a place
 - `VIOLATION_ID`  [measure]
      - id number of one violation; count these, not rows
      - WATCH: row grain not measured; one violation may repeat per enforcement action, so count distinct
 - `IS_HEALTH_BASED_IND`  [filter]
      - Y if the violation is about unsafe water, N if it is paperwork or testing
 - `VIOLATION_CATEGORY_CODE`  [filter]
      - the broad kind of violation; coded value, look at distinct values first (MR, MCL, MON, Other seen)
 - `NON_COMPL_PER_BEGIN_DATE`  [date]
      - the day the water system started being out of compliance
      - WATCH: 93.5% filled; minimum 1900-01-01 is a placeholder, bound every date filter

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS**
one row = one area served by one water system
connects: PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS; COUNTY_FIPS used only if a county rural flag is borrowed
 - `PWSID`  [join]
      - the water system's id number, given by the drinking-water regulator
 - `AREA_TYPE_CODE`  [filter]
      - what kind of area the row names; coded value, look at distinct values first (CN, CT, ZC, TR, IR seen)
 - `COUNTY_SERVED`  [label]
      - name of the county the water system serves
      - WATCH: 6,255 county-type rows have a blank name, 4,262 in New Jersey and 581 in Florida
 - `COUNTY_FIPS`  [join]
      - five-digit state-plus-county number the water system serves
      - WATCH: filled on 404,823 of 405,396 named county rows

---

## 11) When a mine shuts down, do overdose deaths in that county climb over the next three years?  `W12` grade B
   - It would tie a lost paycheck to a body count, county by county. That is the human cost of a closure that never shows up in the jobs numbers.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES**
one row = one mine, with its current status only
connects: STATE matches STATE_ABBR on REF__DIM_STATE to get STATE_FIPS; STATE_FIPS + FIPS_CNTY_CD, left-padded to 3, match FIPS and GEOID on the two CDC tables
 - `MINE_ID`  [label]
      - the mine safety agency's id number for the mine
 - `CURRENT_MINE_STATUS`  [filter]
      - the mine's state now in words: Abandoned, Abandoned and Sealed, Active, Intermittent, Temporarily Idled
      - WATCH: current status only, no history; a mine that closed twice shows the last date
 - `CURRENT_STATUS_DT`  [date]
      - the day the mine entered its current status
      - WATCH: one date per mine
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for a metal or other mine
 - `NO_EMPLOYEES`  [measure]
      - how many people worked at the mine
      - WATCH: null on 39,735 of 91,906 mines
 - `STATE`  [join]
      - two-letter state where the mine sits
 - `FIPS_CNTY_CD`  [join]
      - three-digit number for the county where the mine sits
      - WATCH: county part only, 298 distinct; left-pad to 3 and add the state number

**LIBRARY_MARTS.REFERENCE.REF__DIM_STATE**
one row = one state or territory
connects: STATE_ABBR matches STATE on LABOR__FED_MSHA_MINES
 - `STATE_ABBR`  [join]
      - the state's two-letter postal abbreviation, such as UT
 - `STATE_FIPS`  [join]
      - the two-digit number the government assigns to the state

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY**
one row = one county in one year
connects: FIPS matches STATE_FIPS + FIPS_CNTY_CD built from the mines table
 - `FIPS`  [join]
      - five-digit state-plus-county number for the county the row covers
 - `YEAR`  [date]
      - the year of the death-rate estimate, 1999 to 2015
      - WATCH: no overdose data landed for 2016-2018
 - `POPULATION`  [measure]
      - how many people lived in the county that year
 - `ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES`  [measure]
      - the county's overdose death rate, given as one of eleven ranges
      - WATCH: a range, not a number; a rise inside one range is invisible

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY**
one row = one county, one cause of death, one period
connects: GEOID matches the same 5-digit key, STATE_FIPS + FIPS_CNTY_CD from the mines table
 - `GEOID`  [join]
      - five-digit state-plus-county number for the county the row covers
      - WATCH: 100% filled, 3,153 distinct
 - `INTENT`  [filter]
      - which cause of death the row covers, such as All_Suicide or FA_Deaths
      - WATCH: pick the overdose value; look at distinct values first
 - `PERIOD`  [date]
      - the year the row covers, or TTM for a rolling twelve months
 - `RATE`  [measure]
      - deaths per head of population for that cause, county and period
      - WATCH: -999 is a placeholder
 - `RATE_M`  [filter]
      - a text flag that sits beside the rate; coded value, look at distinct values first (1 and 0 seen)
      - WATCH: a text flag, not a rate
 - `COUNT_SUP`  [measure]
      - the death count, hidden when the number is small
      - WATCH: small counts are suppressed
 - `TTM_DATE_RANGE`  [date]
      - the start and end dates of the rolling twelve-month window

---

## 12) Do the counties that host the most power plants get the least federal grant and loan money?  `W13` grade B
   - It would mean some places carry the smokestacks for everyone else and get passed over when the checks go out.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022**
one row = one power plant
connects: PLANT_FIPS_STATE_CODE + PLANT_FIPS_COUNTY_CODE match PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on FED_USASPENDING_ASSISTANCE_FY2022
 - `DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE`  [label]
      - the energy department's id number for the power plant
 - `PLANT_FIPS_STATE_CODE`  [join]
      - number for the state where the plant stands
 - `PLANT_FIPS_COUNTY_CODE`  [join]
      - number for the county where the plant stands
      - WATCH: 99.71% filled
 - `PLANT_PRIMARY_FUEL_CATEGORY`  [filter]
      - what the plant mainly runs on: SOLAR, GAS, HYDRO, WIND, OIL and others
 - `PLANT_NAMEPLATE_CAPACITY_MW`  [measure]
      - the most power the plant is built to make, in megawatts
      - WATCH: stored as text; must be cast
 - `PLANT_ANNUAL_NOX_EMISSIONS_TONS`  [measure]
      - tons of nitrogen oxide smog gas the plant put out that year

**LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2019 to 2023, skipping 2022 (4 tables, same columns)**
one row = one power plant
connects: FIPSST + FIPSCNTY match PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on the matching fiscal-year assistance table
 - `ORISPL`  [label]
      - the energy department's id number for the power plant
      - WATCH: fill not yet measured
 - `FIPSST`  [join]
      - number for the state where the plant stands
      - WATCH: fill not yet measured
 - `FIPSCNTY`  [join]
      - number for the county where the plant stands
      - WATCH: fill not yet measured
 - `PLFUELCT`  [filter]
      - what the plant mainly runs on, short-code version of the 2022 fuel column
      - WATCH: short-code names; a five-year union needs a hand-written column map
 - `NAMEPCAP`  [measure]
      - the most power the plant is built to make, in megawatts
      - WATCH: fill not yet measured
 - `PLNOXAN`  [measure]
      - tons of nitrogen oxide smog gas the plant put out that year
      - WATCH: fill not yet measured

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 to FY2026 (20 tables, same columns)**
one row = one grant, loan or direct-payment transaction
connects: PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE matches the plant tables' state + county numbers, fiscal year to plant year
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed in this transaction; negative means money pulled back
      - WATCH: loans show $0.00 here on 11,788,945 rows; negative rows belong in the sum
 - `FACE_VALUE_OF_LOAN`  [measure]
      - the size of the loan in dollars, where the row is a loan
      - WATCH: this is where loan money lives; decide loans in or out before summing
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - the kind of aid: 07 and 08 are loans; others coded value, look at distinct values first. Source: public USAspending code list, not the handbook
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the government budget year the transaction happened in
      - WATCH: fill not yet measured
 - `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`  [join]
      - five-digit state-plus-county number where the funded work takes place
      - WATCH: 71% filled in FY2007 rising to 99% in FY2020

---

## 13) Find every dam that would likely kill people if it broke, and list the nursing homes sitting within ten miles of it.  `W15` grade B
   - Nursing home residents cannot leave fast. A list like this shows where a dam failure would be deadliest, and which of those dams nobody has rated.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS**
one row = one dam
connects: LATITUDE, LONGITUDE against LATITUDE, LONGITUDE on HEALTH__FED_CMS_NURSING_HOME, straight-line distance under 10 miles; no shared id
 - `NID_ID`  [label]
      - the national dam inventory's id for the dam
 - `DAM_NAME`  [label]
      - the name the dam goes by
 - `HAZARD_POTENTIAL`  [filter]
      - how bad a failure would be: High, Significant, Low or Undetermined
 - `CONDITION_ASSESSMENT`  [filter]
      - the inspector's rating: Satisfactory, Fair, Poor, Not Rated, or empty
      - WATCH: no rating means unknown, not safe
 - `CONDITION_ASSESSMENT_DATE`  [date]
      - the day the dam's condition was last rated
      - WATCH: 43.84% filled
 - `LAST_INSPECTION_DATE`  [date]
      - the day the dam was last inspected
      - WATCH: 62.71% filled; runs to the year 5023, bound dates
 - `HAS_EMERGENCY_ACTION_PLAN`  [filter]
      - true if the dam has a written plan for a failure, false if not
 - `NID_STORAGE_ACRE_FT`  [measure]
      - how much water the dam holds back, in acre-feet
 - `LATITUDE`  [join]
      - north-south map position of the dam
      - WATCH: fill not yet measured
 - `LONGITUDE`  [join]
      - east-west map position of the dam
      - WATCH: fill not yet measured
 - `STATE`  [label]
      - the state where the dam sits

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home
connects: LATITUDE, LONGITUDE against LATITUDE, LONGITUDE on ENVIRONMENT__FED_NID_DAMS, straight-line distance under 10 miles
 - `CMS_CERTIFICATION_NUMBER_CCN`  [label]
      - Medicare's certification number for the nursing home
 - `PROVIDER_NAME`  [label]
      - the name of the nursing home
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds the home is approved to fill
 - `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`  [measure]
      - how many people live in the home on a typical day
 - `LATITUDE`  [join]
      - north-south map position of the nursing home
      - WATCH: fill not yet measured; COUNTY_FIPS is blank on all 14,700 rows, so distance is the only way in
 - `LONGITUDE`  [join]
      - east-west map position of the nursing home
      - WATCH: fill not yet measured
 - `GEOCODING_FOOTNOTE`  [filter]
      - a note flag on how the map position was found; coded value, look at distinct values first
      - WATCH: 808 rows carry footnote 22

---

## 14) After the fracking wells show up in a county, do its public water systems start racking up more drinking-water violations?  `W16` grade B
   - It would tie a drilling boom to trouble at the tap. It only covers public water systems, not the private wells closest to the drilling.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST**
one row = one fracturing job disclosure at one well
connects: STATE_NAME matches STATE_NAME on REF__DIM_STATE; then STATE_FIPS + folded COUNTY_NAME match STATEFP + folded COUNTYNAME on FED_CENSUS_COUNTY_2020
 - `DISCLOSURE_ID`  [measure]
      - id of one fracking job report filed by the driller
      - WATCH: fill not yet measured
 - `API_NUMBER`  [label]
      - the oil industry's id number for the well
      - WATCH: fill not yet measured
 - `STATE_NAME`  [join]
      - full name of the state where the well is
      - WATCH: fill not yet measured
 - `COUNTY_NAME`  [join]
      - name of the county where the well is
      - WATCH: name join: strip suffixes, make St. and Saint equal, keep independent cities apart
 - `JOB_START_DATE`  [date]
      - the day the fracking job began
      - WATCH: range not yet measured; driller self-reporting, so early booms have no before
 - `TOTAL_BASE_WATER_VOLUME`  [measure]
      - how much water the fracking job used
      - WATCH: fill not yet measured
 - `LATITUDE`  [label]
      - north-south map position of the well
      - WATCH: fill not yet measured
 - `LONGITUDE`  [label]
      - east-west map position of the well
      - WATCH: fill not yet measured
 - `OPERATOR_NAME`  [label]
      - name of the company that ran the fracking job
      - WATCH: fill not yet measured

**LIBRARY_MARTS.REFERENCE.REF__DIM_STATE**
one row = one state or territory
connects: STATE_NAME matches STATE_NAME on ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST; STATE_FIPS matches STATEFP on FED_CENSUS_COUNTY_2020
 - `STATE_NAME`  [join]
      - the full spelled-out name of the state
 - `STATE_FIPS`  [join]
      - the two-digit number the government assigns to the state

**LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020**
one row = one county
connects: STATEFP + folded COUNTYNAME match STATE_FIPS + folded COUNTY_NAME; STATEFP + COUNTYFP match COUNTY_FIPS on ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
 - `STATEFP`  [join]
      - the two-digit number the government assigns to the state
      - WATCH: fill not yet measured
 - `COUNTYFP`  [join]
      - the county's three-digit number inside its state
      - WATCH: fill not yet measured; 3,235 unique FIPS verified
 - `COUNTYNAME`  [join]
      - the name of the county, spelled out
      - WATCH: bare names with no ' County' suffix slip past simple filters

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS**
one row = one area served by one water system
connects: COUNTY_FIPS matches STATEFP + COUNTYFP on FED_CENSUS_COUNTY_2020; PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
 - `PWSID`  [join]
      - the water system's id number, given by the drinking-water regulator
 - `COUNTY_FIPS`  [join]
      - five-digit state-plus-county number the water system serves
      - WATCH: filled on 404,823 of 405,396 named county rows; 6,255 county-type rows have a blank county name

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT**
one row = one violation with its enforcement fields
connects: PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
 - `PWSID`  [join]
      - the water system's id number, given by the drinking-water regulator
      - WATCH: 100% filled, 265,738 distinct; ids starting 04 to 10 are EPA regions and never match a place
 - `VIOLATION_ID`  [measure]
      - id number of one violation; count these, not rows
      - WATCH: row grain not measured; one violation may repeat per enforcement action, so count distinct
 - `IS_HEALTH_BASED_IND`  [filter]
      - Y if the violation is about unsafe water, N if it is paperwork or testing
 - `CONTAMINANT_CODE`  [label]
      - which substance the violation is about; coded value, look at distinct values first
 - `NON_COMPL_PER_BEGIN_DATE`  [date]
      - the day the water system started being out of compliance
      - WATCH: 93.5% filled; minimum 1900-01-01 is a placeholder, bound every date filter

---

## 15) Some water systems break the drinking water rules every single year and nobody ever comes after them.  `W18` grade A
   - It would mean the rulebook has no teeth for repeat offenders. People keep drinking from a system the regulator knows is failing.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT**
one row = one violation with its enforcement fields
connects: PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
 - `PWSID`  [join]
      - the federal id number of one public water system, 265,738 different ones here
 - `VIOLATION_ID`  [measure]
      - the id of one rule violation; repeats when a violation has several enforcement actions
      - WATCH: Row grain not measured. Count distinct VIOLATION_ID per year, never rows.
 - `IS_HEALTH_BASED_IND`  [filter]
      - whether the violation is a health risk kind: Y yes, N no
 - `VIOLATION_STATUS`  [filter]
      - where the violation stands: Resolved, Archived, Unaddressed, Addressed
 - `NON_COMPL_PER_BEGIN_DATE`  [date]
      - the day the system started being out of compliance
      - WATCH: Filled 93.5%; minimum 1900-01-01 is a placeholder. Blank rows cannot be placed in a year.
 - `ENFORCEMENT_ID`  [filter]
      - the id of an enforcement action taken against the violation; empty means none recorded
      - WATCH: Fill not measured. May hold empty strings, not NULLs; test both before counting.
 - `ENFORCEMENT_DATE`  [date]
      - the day the regulator took the enforcement action
      - WATCH: Fill not measured. Date columns carry 1900-01-01 placeholders.
 - `ENFORCEMENT_ACTION_TYPE_CODE`  [label]
      - short code for the kind of enforcement action, such as SOX or SIE; coded value, look at distinct values first
      - WATCH: Fill not measured.
 - `ENF_ACTION_CATEGORY`  [filter]
      - how serious the action was: Informal, Formal, or Resolving
      - WATCH: Fill not measured. Informal means a reminder letter counts as enforced unless you split it out.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS**
one row = one public water system
connects: PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
 - `PWSID`  [join]
      - the federal id number of one public water system
 - `PWS_NAME`  [label]
      - the name of the water system
 - `POPULATION_SERVED_COUNT`  [measure]
      - how many people drink from this system
 - `OWNER_TYPE_CODE`  [filter]
      - one-letter code for who owns the system; P, L, M, S seen; look at distinct values first
 - `PRIMACY_AGENCY_CODE`  [label]
      - the state or agency in charge of policing this system, such as MI or NY
 - `PWS_ACTIVITY_CODE`  [filter]
      - whether the system is still running; codes A, I, N seen; look at distinct values first
      - WATCH: 67.07% of systems carry a deactivation date. Filter to active or the list fills with dead systems.
 - `STATE_CODE`  [filter]
      - two-letter state of the water system
      - WATCH: Filled 96.67%.

---

## 16) When a coal power plant shuts down, the doctors nearby end up with fewer patients who have lung disease.  `W23` grade C
   - It would put a health payoff on closing coal plants. The measure is loose, so a yes is a hint, not proof.

**LIBRARY_RAW.LANDING.FED_EIA860_GENERATOR_Y2019 to Y2023 (5 tables, same columns)**
one row = one generator on one sheet: operable, proposed or retired
connects: PLANT_CODE matches PLANT_CODE on FED_EIA860_PLANT_Y* for the same year
 - `SHEET_NAME`  [filter]
      - which spreadsheet tab the row came from: operable, proposed or retired
      - WATCH: Footer rows land with every field NULL but SHEET_NAME on 12 of 15 sheet-years.
 - `PLANT_CODE`  [join]
      - the energy agency's id number for the power plant the generator sits in
      - WATCH: Repeats, not a row key. Filter PLANT_CODE is not null to drop footer rows.
 - `GENERATOR_ID`  [label]
      - the plant's own label for one generator unit
      - WATCH: Fill not measured.
 - `ENERGY_SOURCE_1`  [filter]
      - the main fuel the generator burns; coded value, look at distinct values first to find coal
      - WATCH: Fill not measured.
 - `STATUS`  [filter]
      - the generator's operating state; coded value, look at distinct values first
      - WATCH: Fill not measured.
 - `NAMEPLATE_CAPACITY_MW`  [measure]
      - the most power the generator is built to make, in megawatts
      - WATCH: Fill not measured.
 - `RETIREMENT_YEAR`  [date]
      - the year the generator was shut down for good
      - WATCH: Fill not measured. A plant retired before 2019 appears in none of these tables.
 - `RETIREMENT_MONTH`  [date]
      - the month the generator was shut down for good
      - WATCH: Fill not measured.

**LIBRARY_RAW.LANDING.FED_EIA860_PLANT_Y2019 to Y2023 (5 tables, same columns)**
one row = one power plant
connects: ZIP matches RNDRNG_PRVDR_ZIP5 on FED_CMS_PARTB_PROVIDER_DY2017 to DY2024; PLANT_CODE matches DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE on ENVIRONMENT__FED_EPA_EGRID_PLANT_2022
 - `PLANT_CODE`  [join]
      - the energy agency's id number for the power plant
      - WATCH: Fill not measured.
 - `ZIP`  [join]
      - the postal ZIP code where the plant stands
      - WATCH: Fill not measured. ZIP identifies nothing on its own.
 - `COUNTY`  [label]
      - the name of the county where the plant stands
      - WATCH: Fill not measured.
 - `STATE`  [filter]
      - the state where the plant stands
      - WATCH: Fill not measured.
 - `LATITUDE`  [label]
      - how far north the plant is, as a map coordinate
      - WATCH: Fill not measured.
 - `LONGITUDE`  [label]
      - how far east or west the plant is, as a map coordinate
      - WATCH: Fill not measured.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022**
one row = one power plant
connects: DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE matches PLANT_CODE on FED_EIA860_PLANT_Y*; gives the county code
 - `DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE`  [join]
      - the same power plant id number the energy agency uses
 - `PLANT_FIPS_STATE_CODE`  [join]
      - two-digit government number for the plant's state
 - `PLANT_FIPS_COUNTY_CODE`  [join]
      - three-digit government number for the plant's county inside the state
 - `PLANT_ANNUAL_COAL_NET_GENERATION_MWH`  [measure]
      - how much electricity the plant made from coal in 2022, in megawatt-hours

**LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2017 to DY2024 (8 tables, same columns)**
one row = one clinician's Medicare Part B year
connects: RNDRNG_PRVDR_ZIP5 matches ZIP on FED_EIA860_PLANT_Y*
 - `NPI`  [join]
      - the national id number of one doctor or other clinician
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_ZIP5`  [join]
      - the five-digit ZIP of the clinician's office
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, ''). It places the office, not where patients live.
 - `RNDRNG_PRVDR_STATE_FIPS`  [filter]
      - two-digit government number for the clinician's state
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_RUCA`  [filter]
      - a score for how rural or urban the office area is; coded value, look at distinct values first
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `TOT_BENES`  [measure]
      - how many Medicare patients the clinician saw that year
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `BENE_AVG_AGE`  [measure]
      - average age of the clinician's Medicare patients
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `BENE_AVG_RISK_SCRE`  [measure]
      - Medicare's score for how sick the clinician's patients are on average
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `BENE_CC_PH_COPD_V2_PCT`  [measure]
      - share of the clinician's Medicare patients flagged with chronic lung disease
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, ''). A chronic label, not claims; exists only from DY2017. CMS blanks small patient counts.
 - `BENE_CC_PH_ASTHMA_V2_PCT`  [measure]
      - share of the clinician's Medicare patients flagged with asthma
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, ''). Exists only from DY2017. CMS blanks small patient counts.

**LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 to DY2016 (4 tables, same columns)**
one row = one clinician's Medicare Part B year, older 59-column layout; not usable here, no lung-disease columns
connects: nothing. One table, no join
 - no columns named. The handbook marks this table not usable for this idea.

---

## 17) Polluting sites in neighborhoods with more people of color get fewer visits from government inspectors.  `P-081` grade B
   - Already measured: visits per site fall from 2.90 in the whitest tenth to 1.46 in the most-minority tenth. It means who lives next door may decide how hard a polluter gets watched.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP**
one row = one EPA-registered facility with its compliance, inspection and penalty counts
connects: nothing. One table, no join
 - `FRS_ID`  [label]
      - the environmental agency's id number for one regulated site
 - `PCT_MINORITY`  [filter]
      - share of the people living around the site who are not white; used to group sites into tenths
      - WATCH: Missing on 29,702 of 93,808 rows, 32%.
 - `TOTAL_INSPECTION_COUNT`  [measure]
      - how many times an inspector visited the site, as a snapshot total
      - WATCH: The period the total covers is not measured.
 - `QUARTERS_WITH_NONCOMPLIANCE`  [measure]
      - how many three-month periods the site was breaking the rules
      - WATCH: The period the total covers is not measured.
 - `FORMAL_ACTION_COUNT`  [measure]
      - how many formal enforcement actions were taken against the site
 - `TOTAL_PENALTIES`  [measure]
      - total fine dollars charged to the site
      - WATCH: 86,963 sites, 92.7%, have zero. Dollars run higher in high-minority groups, the opposite way.
 - `CHRONIC_NO_PENALTY`  [filter]
      - true if the site kept breaking rules and was never fined
 - `NEVER_INSPECTED_NONCOMPLIANT`  [filter]
      - true if the site was out of compliance and never inspected
      - WATCH: True on 53,587 rows, 57.1%.
 - `IN_MAJORITY_MINORITY_COMMUNITY`  [filter]
      - true if more than half the neighbors are people of color
      - WATCH: Empty on the same 29,702 rows that lack PCT_MINORITY.
 - `POPULATION_DENSITY`  [filter]
      - how tightly packed the people around the site live
 - `STATE`  [filter]
      - the state the site is in
 - `DATE_LAST_INSPECTION`  [date]
      - the day of the most recent inspector visit, 1978 to 2026
      - WATCH: Filled 55.96%; empty on 44% of rows. No trend can be drawn.
 - `HAS_AIR_PROGRAM`  [filter]
      - true if the site is regulated for air pollution
 - `HAS_WATER_PROGRAM`  [filter]
      - true if the site is regulated for water pollution
 - `HAS_HAZWASTE_PROGRAM`  [filter]
      - true if the site is regulated for hazardous waste

---

# BODY

## 18) The counties that got flooded with pain pills around 2010 are the same counties burying overdose victims in 2024, or maybe they are not.  `W26` grade B
   - A yes ties today's deaths to old pill shipments place by place. A no says the death wave moved somewhere the pills never went.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS**
one row = one shipment of one opioid product from a reporter to a buyer
connects: BUYER_COUNTY_FIPS matches FIPS on HEALTH__FED_CDC_DRUG_POISONING_COUNTY and GEOID on LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY
 - `BUYER_COUNTY_FIPS`  [join]
      - five-digit government number for the county of the pharmacy or buyer that got the pills
      - WATCH: Filled on 178,338,557 of 178,598,026 rows; a second source says 178,344,793. Virginia cities, Dona Ana, Juneau, Puerto Rico drop out.
 - `TRANSACTION_DATE`  [date]
      - the day the shipment was made, 2006 to 2012
 - `DOSAGE_UNITS`  [measure]
      - how many pills were in the shipment
 - `TOTAL_MME`  [measure]
      - the shipment's strength converted to a common morphine-equivalent scale
 - `DRUG_NAME`  [filter]
      - which opioid was shipped: HYDROCODONE or OXYCODONE
 - `BUYER_BUSINESS_ACTIVITY`  [filter]
      - what kind of buyer: CHAIN PHARMACY, RETAIL PHARMACY, PRACTITIONER
 - `BUYER_STATE`  [filter]
      - the state where the buyer that got the pills is located

**LIBRARY_RAW.LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY**
one row = one county, one intent such as overdose or suicide, one period
connects: GEOID matches BUYER_COUNTY_FIPS on HEALTH__FED_DEA_ARCOS
 - `GEOID`  [join]
      - five-digit government number for the county
      - WATCH: Fill not measured on this copy; the mart copy reads 100%, 3,153 distinct.
 - `INTENT`  [filter]
      - which kind of death the row counts; Drug_OD is overdose, others cover suicide, homicide, firearm
 - `PERIOD`  [date]
      - the year of the deaths, 2019 to 2024, or TTM for the trailing twelve months
 - `RATE`  [measure]
      - deaths per head of population as published by the CDC
      - WATCH: Holds -999 as a suppression marker on 822 overdose rows. Filter RATE >= 0.
 - `RATE_M`  [filter]
      - a 0 or 1 flag stored as long decimal text, marking the same rows as the 1-9 counts
      - WATCH: Filtering on it selects on the outcome.
 - `COUNT_SUP`  [measure]
      - number of deaths, as text; real counts plus the range strings 1-9 and 10-50 for small counties
      - WATCH: Text. Use this landing copy; the mart cast it to a number and nulled 61,400 of 132,000 rows.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY**
one row = the same file with COUNT_SUP cast to a number; used only for its profiled key
connects: GEOID matches FIPS on HEALTH__FED_CDC_DRUG_POISONING_COUNTY, measured 100%
 - `GEOID`  [join]
      - five-digit government number for the county, 3,153 different ones

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY**
one row = one county, one year, with population
connects: FIPS matches BUYER_COUNTY_FIPS on HEALTH__FED_DEA_ARCOS, same year 2006-2012
 - `FIPS`  [join]
      - five-digit government number for the county, 3,149 different ones
 - `YEAR`  [date]
      - the calendar year of the row, 1999 to 2015
 - `POPULATION`  [measure]
      - how many people lived in the county that year; the bottom half of pills per resident
      - WATCH: Fill not measured. No county population after 2015 is landed.

---

## 19) Right after a chain buys a nursing home, the paperwork starts describing the same residents as sicker, which makes Medicare pay more.  `W28` grade D
   - It would mean new owners are gaming the forms for money. With the data held, there is probably no before to compare.

**LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP**
one row = one enrollment, one owner, one role
connects: ENROLLMENT_ID matches ENROLLMENT_ID on HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS; 288,550 of 295,083 owner rows join
 - `ENROLLMENT_ID`  [join]
      - Medicare's id for one nursing home's sign-up record
      - WATCH: 6,533 owner rows name enrollments the enrollment snapshot does not carry.
 - `ASSOCIATE_ID_OWNER`  [label]
      - Medicare's id for the person or company listed as an owner
 - `ORGANIZATION_NAME_OWNER`  [label]
      - the name of the company that owns a piece of the home
 - `ROLE_TEXT_OWNER`  [filter]
      - what the owner's role is, such as director, officer or part owner
 - `ASSOCIATION_DATE_OWNER`  [date]
      - the day the owner record was tied to the home; a record date, not a sale date
      - WATCH: Free text in mixed formats with three 1800 placeholder values. Current owners only, no sale history.
 - `PERCENTAGE_OWNERSHIP`  [measure]
      - what percent of the home this owner holds
      - WATCH: Fill not measured.
 - `PRIVATE_EQUITY_COMPANY_OWNER`  [filter]
      - Y if the owner is flagged as a private equity firm
      - WATCH: Y on 196 of 295,083 rows, 0.67% of enrollments; blank on 67%. Blank means unknown.
 - `REIT_OWNER`  [filter]
      - Y if the owner is flagged as a real estate investment trust
      - WATCH: Y on 587 enrollments; blank on 198,546 rows, 67%. Blank means unknown.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS**
one row = one Medicare enrollment of a nursing home
connects: CCN matches CCN on HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY, measured 100%, and CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_NURSINGHOME411
 - `ENROLLMENT_ID`  [join]
      - Medicare's id for one nursing home's sign-up record; it encodes the record-creation date
      - WATCH: The date inside is O plus YYYYMMDD plus 6 digits; a record-creation date, not a purchase date.
 - `CCN`  [join]
      - Medicare's certification number for the nursing home building
 - `AFFILIATION_ENTITY_ID`  [label]
      - id of the chain or group the home belongs to
 - `AFFILIATION_ENTITY_NAME`  [label]
      - name of the chain or group the home belongs to
 - `PROPRIETARY_NONPROFIT`  [filter]
      - one-letter code for profit status; P, N, D seen; look at distinct values first

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY**
one row = one home, one report date, one assessment item, one answer
connects: CCN matches CCN on HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS, measured 100%
 - `CCN`  [join]
      - Medicare's certification number for the nursing home, one per building
 - `REPORT_DATE`  [date]
      - the date the batch of resident assessment answers was reported
      - WATCH: No date range known; one probed source says a single quarter, Q2 2026. Count distinct values first.
 - `MDS_ITEM_QUESTION_DESCRIPTION`  [filter]
      - the wording of the question on the resident assessment form, one of 551 items
      - WATCH: Which item is the one you want is unknown until distinct values are read.
 - `MDS_ITEM_RESPONSE`  [filter]
      - the answer option picked for that question on the assessment form
 - `OVERALL_PERCENT`  [measure]
      - share of all the home's residents who got this answer
      - WATCH: Fill not measured. 54,245 rows read 100 on all three percent columns; small homes make identical blocks.
 - `TOTAL_RESIDENTS`  [measure]
      - how many residents the home had on that report date
      - WATCH: Stored as text and repeated on every item row; cast it and take one value per home per date.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411**
one row = one nursing home, snapshot dated 2025-12-01
connects: CMS_CERTIFICATION_NUMBER_CCN matches CCN on HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS; overlap not measured
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's certification number for the nursing home building
 - `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS`  [filter]
      - Y if the home got a new owner in the year before 2025-12-01
      - WATCH: Y on only 55 rows. The same flag on the other nursing-home roster is N on all 14,700 rows.
 - `NURSING_CASE_MIX_INDEX`  [measure]
      - the federal score for how sick the home's residents are on paper
 - `CHAIN_ID`  [label]
      - id of the chain the home belongs to

---

## 20) When a big dialysis chain opens a clinic in a county, the local kidney doctors start disappearing.  `W29` grade B
   - It would mean chains push out independent kidney care. Patients end up with a clinic and fewer doctors to choose from.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS**
one row = one dialysis clinic, current directory
connects: ZIP_CODE matches ZCTA5 on XWALK_ZCTA_COUNTY; CCN matches CCN on HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES, measured 99%
 - `CCN`  [join]
      - Medicare's certification number for the dialysis clinic
 - `CHAIN_OWNED`  [filter]
      - whether a chain owns the clinic: Yes or No
 - `CHAIN_ORGANIZATION`  [label]
      - the name of the chain that owns the clinic today
      - WATCH: It is the chain today. A clinic bought in 2019 reads as a chain arrival at its older certification date.
 - `CERTIFICATION_DATE`  [date]
      - the day Medicare approved the clinic to operate, 1968 to 2026
 - `OF_DIALYSIS_STATIONS`  [measure]
      - how many dialysis chairs the clinic has
 - `ZIP_CODE`  [join]
      - the clinic's postal ZIP code, 5,361 different ones
 - `COUNTY_PARISH`  [label]
      - the name of the county the clinic is in
 - `STATE`  [filter]
      - the state the clinic is in

**LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 to DY2024 (12 tables, same columns)**
one row = one clinician, one year of Medicare Part B billing totals
connects: RNDRNG_PRVDR_ZIP5 matches ZCTA5 on XWALK_ZCTA_COUNTY; NPI matches NPI on FED_CMS_NPPES_DEACTIVATED
 - `NPI`  [join]
      - the national id number of one doctor or other clinician
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_TYPE`  [filter]
      - the clinician's specialty as text; find the kidney one by looking for Neph
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, ''). Exact kidney specialty text unknown; read distinct values first.
 - `RNDRNG_PRVDR_ZIP5`  [join]
      - the five-digit ZIP the clinician billed from that year
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_ENT_CD`  [filter]
      - whether the biller is a person or an organization; coded value, look at distinct values first
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `TOT_BENES`  [measure]
      - how many Medicare patients the clinician saw that year
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `TOT_SRVCS`  [measure]
      - how many services the clinician billed Medicare for that year
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES**
one row = one clinic, one quality measure, one year
connects: CCN matches CCN on HEALTH__FED_CMS_DIALYSIS, measured 99%
 - `CCN`  [join]
      - Medicare's certification number for the dialysis clinic, 8,235 different ones
 - `CHAIN`  [label]
      - the chain name as reported that year, such as DAVITA, FRESENIUS MEDICAL CARE or INDEPENDENT
      - WATCH: Only 2021-2024. Ownership before 2021 is not recorded anywhere landed.
 - `OWNERSHIP_TYPE`  [filter]
      - profit status of the clinic: For Profit, Non-profit or Unavailable
 - `YEAR_COL`  [date]
      - the year the row reports on, 2021 to 2024
      - WATCH: Filled 93.3%.

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP-area and county overlap
connects: ZCTA5 matches ZIP_CODE on HEALTH__FED_CMS_DIALYSIS and RNDRNG_PRVDR_ZIP5 on FED_CMS_PARTB_PROVIDER_DY*; hands back COUNTY_FIPS
 - `ZCTA5`  [join]
      - the five-digit census ZIP area, the map version of a ZIP code
      - WATCH: 10,186 of 33,791 ZIP areas cross a county line; hospital-campus ZIPs with no ZIP area drop out.
 - `COUNTY_FIPS`  [join]
      - five-digit government number for the county the ZIP area falls in

**LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED**
one row = one deactivated provider id with its deactivation date
connects: NPI matches NPI on FED_CMS_PARTB_PROVIDER_DY*; tells a retirement from a move
 - `NPI`  [join]
      - the national id number of a clinician whose id was shut off
      - WATCH: Not profiled.
 - `NPPES_DEACTIVATION_DATE`  [date]
      - the day the clinician's id was shut off
      - WATCH: Text in MM/DD/YYYY; parse before sorting. Not profiled.

---

## 21) Counties that lost their hospital are also the counties where the tap water keeps failing health rules.  `W30` grade B
   - It would mean the same places are losing both basics at once. It could also mean both just track poor or shrinking counties.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT**
one row = one violation and enforcement action pair for one water system
connects: PWSID matches PWSID on ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
 - `PWSID`  [join]
      - the federal id number of one public water system, 265,738 different ones
      - WATCH: Ids starting 04 to 10 are EPA regions, not states.
 - `VIOLATION_ID`  [measure]
      - the id of one rule violation; repeats once per enforcement action
      - WATCH: Repeats across enforcement actions. Count distinct violations, not rows.
 - `IS_HEALTH_BASED_IND`  [filter]
      - whether the violation is a health risk kind: Y yes, N no
 - `VIOLATION_CATEGORY_CODE`  [filter]
      - short code for the kind of violation, such as MR, MCL or MON; coded value, look at distinct values first
 - `NON_COMPL_PER_BEGIN_DATE`  [date]
      - the day the system started being out of compliance
      - WATCH: Filled 93.5%; 1900-01-01 is a placeholder. Bound the date range before charting.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS**
one row = one water system and one area it serves
connects: COUNTY_FIPS matches FIPS_STATE_CD joined to FIPS_CNTY_CD padded to 3 digits on HEALTH__FED_CMS_POS_OTHER
 - `PWSID`  [join]
      - the federal id number of one public water system, 418,885 different ones
 - `AREA_TYPE_CODE`  [filter]
      - what kind of area the row names; codes CN, CT, ZC, TR seen; look at distinct values first
 - `COUNTY_SERVED`  [label]
      - the name of the county the water system serves
      - WATCH: 6,255 county-type rows have a blank county name: New Jersey 4,262, Florida 581.
 - `STATE_SERVED`  [filter]
      - the state the water system serves
 - `COUNTY_FIPS`  [join]
      - five-digit government number for the county served
      - WATCH: Filled on 404,823 of 405,396 named county rows; blank-name rows got none.
 - `ZIP_CODE_SERVED`  [label]
      - a ZIP code the water system serves
      - WATCH: Filled 1.24%. Do not use.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER**
one row = one Medicare-certified provider, latest status
connects: FIPS_STATE_CD joined to FIPS_CNTY_CD padded to 3 digits matches COUNTY_FIPS on ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
 - `CCN`  [label]
      - Medicare's certification number for the provider
      - WATCH: Only the latest status per CCN is kept, so every closure count is a floor.
 - `PRVDR_CTGRY_CD`  [filter]
      - two-digit code for what kind of provider it is; coded value, look at distinct values first
      - WATCH: Which value means hospital is not known. No category here is a nursing home.
 - `PGM_TRMNTN_CD`  [filter]
      - two-digit code for why or whether the provider left Medicare; coded value, look at distinct values first
 - `TRMNTN_EXPRTN_DT`  [date]
      - the day the provider's Medicare certification ended, 1963 to 2026
      - WATCH: Filled 40.92%.
 - `FIPS_STATE_CD`  [join]
      - two-digit government number for the provider's state
      - WATCH: 316 blank strings.
 - `FIPS_CNTY_CD`  [join]
      - government number for the provider's county inside the state
      - WATCH: Filled 99.29%. Stored as a NUMBER, unpadded; pad to 3 digits.

---

## 22) New hospice agencies pop up in the counties where nursing homes are emptying out.  `W32` grade C
   - It would mean dying at home is replacing the nursing home bed, county by county. The data can only show empty beds today, not a fall.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE**
one row = one hospice agency, current directory
connects: STATE plus COUNTY_PARISH matches STATE plus COUNTYNAME on FED_CENSUS_COUNTY_2020, a name join
 - `CCN`  [label]
      - Medicare's certification number for the hospice agency
 - `CERTIFICATION_DATE`  [date]
      - the day Medicare approved the agency, 1983 to 2025; an opening day, not a patient count
      - WATCH: Current directory; whether closed agencies remain is not measured, so openings may be survivors only.
 - `OWNERSHIP_TYPE`  [filter]
      - profit status: For-Profit, Non-Profit, Government or Other
 - `COUNTY_PARISH`  [join]
      - the name of the county the agency is in
      - WATCH: Name join: strip the suffix, fold St. and Saint; Virginia independent cities miss without city.
 - `STATE`  [join]
      - the state the agency is in

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY**
one row = one home, one report date, one assessment item, one answer
connects: STATE plus FIPS_COUNTY_CODE matches STATE plus COUNTYFP on FED_CENSUS_COUNTY_2020; padding unknown
 - `CCN`  [join]
      - Medicare's certification number for the nursing home, one per building
 - `REPORT_DATE`  [date]
      - the date the batch of resident assessment answers was reported
      - WATCH: No date range known; one probed source says a single quarter, Q2 2026. Count distinct values first.
 - `TOTAL_RESIDENTS`  [measure]
      - how many residents the home had on that report date
      - WATCH: Stored as text and repeated on every item row; cast it and take one value per home per date.
 - `STATE`  [join]
      - two-letter state the nursing home sits in
 - `FIPS_COUNTY_CODE`  [join]
      - county number inside the state, not the full five-digit county code
      - WATCH: Only 298 distinct values, so it is a within-state code; padding unknown.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, snapshot
connects: STATE plus COUNTY_PARISH matches STATE plus COUNTYNAME on FED_CENSUS_COUNTY_2020, a name join
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds the home is approved to fill
 - `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`  [measure]
      - how many residents sleep in the home on a typical day
      - WATCH: Fill not measured.
 - `COUNTY_PARISH`  [join]
      - the name of the county the home is in
      - WATCH: COUNTY_FIPS on this table is blank on all 14,700 rows, so the county name is the only way in.
 - `STATE`  [join]
      - the state the home is in

**LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020**
one row = one county with its name and FIPS parts
connects: STATE plus COUNTYNAME matches STATE plus COUNTY_PARISH on the hospice and nursing home tables; STATEFP joined to COUNTYFP makes the five-digit county code
 - `STATE`  [join]
      - two-letter state abbreviation, used with the county name to match
 - `STATEFP`  [join]
      - two-digit government number for the state
 - `COUNTYFP`  [join]
      - three-digit government number for the county inside the state
 - `COUNTYNAME`  [join]
      - the county's name as the census writes it
      - WATCH: Not profiled; 3,235 rows with unique FIPS verified.

---

## 23) The nursing homes that say on paper their residents are the sickest are also the ones with the most fire safety write-ups.  `W33` grade B
   - It would mean the frailest people live in the least safe buildings. It could also hint that the sickness score is about money, not care.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, snapshot
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES, measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's certification number for the nursing home building
      - WATCH: 14,328 distinct ids on 14,700 rows; dedupe before joining.
 - `NURSING_CASE_MIX_INDEX`  [measure]
      - the federal score for how sick the home's residents are on paper
      - WATCH: Fill not measured. One snapshot; the score in past years is unknown.
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds the home is approved to fill
 - `TOTAL_NUMBER_OF_FIRE_SAFETY_DEFICIENCIES`  [measure]
      - the roster's own count of fire safety write-ups for the home
 - `AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS`  [filter]
      - whether sprinklers cover the building: Yes, Partial, or Data Not Available
 - `STATE`  [filter]
      - the state the home is in; compare homes inside the same state

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES**
one row = one fire-safety citation from one survey
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME, measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's certification number for the nursing home, 13,603 different ones here
 - `SURVEY_DATE`  [date]
      - the day inspectors walked the building, 2016 to 2026
      - WATCH: Citation counts track how often a home is surveyed, r = 0.84. Count per distinct SURVEY_DATE.
 - `DEFICIENCY_TAG_NUMBER`  [filter]
      - the rule number that was broken; K0351 is the only no-sprinkler tag
      - WATCH: A text search on sprinkler inflates the count 4x; use K0351.
 - `SCOPE_SEVERITY_CODE`  [filter]
      - letter grade for how bad and how widespread the problem was; B through F seen; look at distinct values first
 - `DEFICIENCY_CORRECTED`  [filter]
      - status of the fix as text, such as has date of correction or Waiver has been granted
      - WATCH: A status, not yes or no. Waiver has been granted means still open by permission.
 - `INSPECTION_CYCLE`  [filter]
      - which round of inspection the citation came from: 1, 2 or 3; keep the latest cycle

---

## 24) Some counties have piles of nursing home beds and almost no doctors around to look after the people in them.  `W34` grade B
   - It would point to places where old people are parked far from medical care. It is a map of now, not a trend.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, snapshot
connects: ZIP_CODE matches ZCTA5 on XWALK_ZCTA_COUNTY, which hands back COUNTY_FIPS
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds the home is approved to fill
 - `ZIP_CODE`  [join]
      - the home's postal ZIP code, 9,229 different ones
 - `COUNTY_PARISH`  [label]
      - the name of the county the home is in
 - `STATE`  [filter]
      - the state the home is in
 - `COUNTY_FIPS`  [join]
      - meant to be the five-digit county number, but it holds nothing
      - WATCH: Empty string on all 14,700 rows. Do not use it.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS**
one row = one prescriber, one year of Medicare Part D totals
connects: PRSCRBR_ZIP5 matches ZCTA5 on XWALK_ZCTA_COUNTY, which hands back COUNTY_FIPS
 - `NPI`  [measure]
      - the national id number of one person who wrote Medicare prescriptions
 - `PRSCRBR_TYPE`  [filter]
      - the prescriber's specialty as text; use it to keep doctors and drop dentists and nurse practitioners
      - WATCH: The file is anyone who wrote scripts in 2024, not just doctors.
 - `PRSCRBR_ZIP5`  [join]
      - the five-digit ZIP of the prescriber's billing or practice address
      - WATCH: 54 blank strings.
 - `PRSCRBR_STATE_FIPS`  [filter]
      - two-digit government number for the prescriber's state
      - WATCH: 1,234 blank strings.
 - `PRSCRBR_ENT_CD`  [filter]
      - whether the prescriber is a person or an organization; I on nearly every row, O on 2

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP-area and county overlap
connects: ZCTA5 matches ZIP_CODE on HEALTH__FED_CMS_NURSING_HOME and PRSCRBR_ZIP5 on HEALTH__FED_CMS_PART_D_PRESCRIBERS
 - `ZCTA5`  [join]
      - the five-digit census ZIP area, the map version of a ZIP code
      - WATCH: 10,186 of 33,791 ZIP areas cross a county line; single-building ZIPs like 44195 and 27710 drop out.
 - `COUNTY_FIPS`  [join]
      - five-digit government number for the county, 3,266 different ones
 - `COUNTY_NAME`  [label]
      - the plain name of the county, for reading the results

**LIBRARY_RAW.LANDING.FED_CENSUS_ZCTA_COUNTY_2020**
one row = one ZIP-area and county overlap, with land area of the overlap
connects: GEOID_ZCTA5_20 and GEOID_COUNTY_20 line up with ZCTA5 and COUNTY_FIPS on XWALK_ZCTA_COUNTY; largest AREALAND_PART wins a tie
 - `GEOID_ZCTA5_20`  [join]
      - the five-digit census ZIP area, the map version of a ZIP
      - WATCH: Not profiled.
 - `GEOID_COUNTY_20`  [join]
      - five-digit government number for the county
      - WATCH: Not profiled.
 - `AREALAND_PART`  [measure]
      - how much land the ZIP area and the county share; biggest share picks the county
      - WATCH: Largest-area pick is right 99.5% on single-county ZIP areas but only 47.1% on ones that cross a line.

---

## 25) When Medicare changed how it pays nursing homes in October 2019, homes suddenly started writing down a lot more dementia.  `W35` grade D
   - It would mean diagnoses follow the money, not the patients. The table probably holds one quarter of 2026, so the test may be impossible.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY**
one row = one home, one report date, one assessment item, one answer
connects: nothing. One table, no join
 - `CCN`  [label]
      - Medicare's certification number for the nursing home, 14,318 different ones
 - `REPORT_DATE`  [date]
      - the date the batch of resident assessment answers was reported
      - WATCH: No date range known; one probed source says a single quarter, Q2 2026. Count distinct values first.
 - `MDS_ITEM_QUESTION_DESCRIPTION`  [filter]
      - the wording of the question on the resident assessment form, one of 551 items
      - WATCH: Which item is the one you want is unknown until distinct values are read.
 - `MDS_ITEM_RESPONSE`  [filter]
      - the answer option picked for that question on the assessment form
 - `OVERALL_PERCENT`  [measure]
      - share of all the home's residents who got this answer
      - WATCH: Fill not measured. 54,245 rows read 100 on all three percent columns; small homes make identical blocks.
 - `LONG_STAY_PERCENT`  [measure]
      - share of the home's long-stay residents who got this answer
      - WATCH: Fill not measured. 54,245 rows read 100 on all three percent columns.
 - `SHORT_STAY_PERCENT`  [measure]
      - share of the home's short-stay residents who got this answer
      - WATCH: Fill not measured. 54,245 rows read 100 on all three percent columns.
 - `TOTAL_RESIDENTS`  [measure]
      - how many residents the home had on that report date
      - WATCH: Stored as text and repeated on every item row; cast it and take one value per home per date.
 - `STATE`  [filter]
      - two-letter state the nursing home sits in

---

## 26) Some tax-free hospitals sit on big yearly surpluses and give back only pennies of it as free care for poor patients, while paying their bosses more than the whole free-care bill.  `W36` grade B
   - Nonprofit hospitals skip taxes in exchange for helping the poor. This would name the ones taking the break and not paying it back.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS**
one row = one hospital cost report; the grain is RPT_REC_NUM
connects: PROVIDER_CCN matches CCN on XWALK_HOSPITAL_CCN_EIN; covers 3,891 of 6,703 nonprofit hospital ids, 58%
 - `PROVIDER_CCN`  [join]
      - Medicare's certification number for the hospital, 7,057 different ones
      - WATCH: PROVIDER_CCN plus SOURCE_FILE_YEAR is not unique: 1,186 hospital-years carry more than one report.
 - `RPT_REC_NUM`  [label]
      - the record number of one cost report; the true one-row id
 - `TYPE_OF_CONTROL`  [filter]
      - number code for who runs the hospital, nonprofit, for-profit or government; coded value, look at distinct values first
 - `COST_OF_CHARITY_CARE`  [measure]
      - dollars the hospital spent on free care for poor patients that fiscal year
      - WATCH: Fill not measured on the 13-year load.
 - `NET_INCOME`  [measure]
      - dollars the hospital had left over at year end, its surplus or loss
      - WATCH: Fill not measured. Text nan is stored as a floating NaN, not null; 89 rows counted. Rank only positive values.
 - `TOTAL_COSTS`  [measure]
      - all the dollars the hospital spent that fiscal year
 - `FISCAL_YEAR_END_DATE`  [date]
      - the last day of the hospital's financial year, 2011-04-30 to 2024-09-30; group on this
 - `FISCAL_YEAR_LENGTH_DAYS`  [filter]
      - how many days the report covers, 14 to 472
      - WATCH: Filter >= 300. Short reports are seller stubs and lose money 65% of the time against 34%.
 - `SOURCE_FILE_YEAR`  [label]
      - which yearly government file the report came in, 2011 to 2023
      - WATCH: A label, not the fiscal period.

**LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN**
one row = one hospital id matched to one tax id, with a match tier
connects: CCN matches PROVIDER_CCN on HEALTH__FED_CMS_HCRIS; EIN matches EIN on HEALTH__HOSPITAL_OFFICER_PAY
 - `CCN`  [join]
      - Medicare's certification number for the hospital
      - WATCH: Not profiled.
 - `EIN`  [join]
      - the federal tax id of the organization that files the hospital's tax return
      - WATCH: It is the system, not the building: 1,293 tax ids cover 3,222 rows; Kaiser's one id sits on 35 hospitals.
 - `MATCH_TIER`  [filter]
      - how the match was made: 1 and 2 name plus ZIP, 3 name plus state, 4 address
      - WATCH: Read it before trusting a row.
 - `MATCH_RULE`  [label]
      - the text name of the rule that made the match
 - `EIN_NTEE`  [label]
      - the tax agency's category code for what kind of charity the organization is
 - `PROPRIETARY_NONPROFIT`  [filter]
      - one-letter code for profit status; coded value, look at distinct values first

**LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY**
one row = one person on one hospital organization's Form 990, one tax year
connects: EIN matches EIN on XWALK_HOSPITAL_CCN_EIN, CORPORATE_REGISTRY__FED_IRS_EO_BMF with 3,914 shared values, and ECONOMICS__FED_IRS_990_EFILE_INDEX with 3,918
 - `EIN`  [join]
      - the federal tax id of the hospital organization, 3,962 different ones
 - `TAX_YEAR`  [date]
      - the tax year the return covers, 2016 to 2025
      - WATCH: Tax years before 2017 are absent from the underlying pay file.
 - `PERSON_NAME`  [label]
      - the name of the executive, officer or board member
 - `TITLE`  [label]
      - the person's job title on the return
 - `TOTAL_COMPENSATION`  [measure]
      - total dollars the person was paid that tax year
      - WATCH: One executive repeats on every affiliate's return. Take the max per person per tax year, never the sum.
 - `IS_SCHEDULE_J_POINTER`  [filter]
      - true if the line just restates a payout listed elsewhere; keep false only
      - WATCH: 239 person-returns carry a pointer line.
 - `IS_GROUP_RETURN`  [filter]
      - true if the return covers a group of organizations filed as one; drop these
      - WATCH: 61 rows.
 - `BMF_REVENUE_AMT`  [measure]
      - the organization's yearly revenue in dollars, copied from the tax agency's master file
 - `BMF_ASSET_AMT`  [measure]
      - the organization's total assets in dollars, copied from the tax agency's master file

**LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF**
one row = one tax-exempt organization, current master file
connects: EIN matches EIN on HEALTH__HOSPITAL_OFFICER_PAY, 3,914 shared values
 - `EIN`  [join]
      - the federal tax id of the tax-exempt organization
 - `NTEE_CODE`  [filter]
      - the tax agency's category code for what kind of charity it is
 - `REVENUE_AMT`  [measure]
      - the organization's yearly revenue in dollars
 - `ASSET_AMT`  [measure]
      - the organization's total assets in dollars
 - `INCOME_AMT`  [measure]
      - the organization's yearly income in dollars

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX**
one row = one e-filed return: who filed, which period, when
connects: EIN matches EIN on HEALTH__HOSPITAL_OFFICER_PAY, 3,918 shared values
 - `EIN`  [join]
      - the federal tax id of the organization that filed, 893,074 different ones
 - `TAX_PERIOD`  [date]
      - the tax period the return covers
 - `RETURN_TYPE`  [filter]
      - which form was filed: 990, 990EZ, 990PF and others
 - `OBJECT_ID`  [label]
      - the tax agency's id for the one filed return document
      - WATCH: No money columns here; it says a return exists, not what is in it.

---

## 27) When a hospital shuts, you can watch where the doctors around it turn up billing from the next year, or whether they vanish.  `W37` grade C
   - It shows whether a closure scatters a town's doctors or they stay put. The towns that gain them get named.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER**
one row = one Medicare-certified provider, latest status
connects: ZIP_CD matches RNDRNG_PRVDR_ZIP5 on FED_CMS_PARTB_PROVIDER_DY of the closure year; CCN matches CCN on HEALTH__FED_CMS_FACILITY_AFFILIATION, only 14%
 - `CCN`  [join]
      - Medicare's certification number for the provider, 43,797 different ones
      - WATCH: Only the latest status per CCN is kept, so closure counts are a floor.
 - `PRVDR_CTGRY_CD`  [filter]
      - two-digit code for what kind of provider it is; coded value, look at distinct values first
      - WATCH: Which value means hospital is not known.
 - `PGM_TRMNTN_CD`  [filter]
      - two-digit code for why or whether the provider left Medicare; coded value, look at distinct values first
 - `TRMNTN_EXPRTN_DT`  [date]
      - the day the provider's Medicare certification ended; the closure date
      - WATCH: Filled 40.92%. Only closures 2013-2023 have a before-and-after pair.
 - `ZIP_CD`  [join]
      - the postal ZIP code where the hospital or provider stands
      - WATCH: 270 blank strings.
 - `FAC_NAME`  [label]
      - the name of the hospital or facility
 - `ST_ADR`  [label]
      - the street address of the facility; can be matched to the doctor's street to narrow the group
      - WATCH: Match rate against RNDRNG_PRVDR_ST1 not measured.

**LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 to DY2024 (12 tables, same columns)**
one row = one clinician, one year of Medicare Part B billing totals
connects: RNDRNG_PRVDR_ZIP5 matches ZIP_CD on HEALTH__FED_CMS_POS_OTHER; NPI matches NPI on the next year's table and on FED_CMS_NPPES_DEACTIVATED
 - `NPI`  [join]
      - the national id number of one doctor or other clinician
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_ZIP5`  [join]
      - the five-digit ZIP the clinician filed claims from that year
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, ''). Often the health system's office, not the clinic.
 - `RNDRNG_PRVDR_ST1`  [label]
      - the street address the clinician filed claims from
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_CITY`  [label]
      - the town the clinician filed claims from
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_STATE_ABRVTN`  [filter]
      - two-letter state the clinician filed claims from
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_TYPE`  [filter]
      - the clinician's medical specialty written out as text
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `RNDRNG_PRVDR_ENT_CD`  [filter]
      - whether the biller is a person or an organization; coded value, look at distinct values first
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').
 - `TOT_BENES`  [measure]
      - how many Medicare patients the clinician saw that year
      - WATCH: Fill not measured. Blanks are empty strings, not NULL; use NULLIF(col, '').

**LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED**
one row = one deactivated provider id with its date
connects: NPI matches NPI on FED_CMS_PARTB_PROVIDER_DY* for doctors missing the next year; separates retired from not billing
 - `NPI`  [join]
      - the national id number of a clinician whose id was shut off
      - WATCH: Not profiled.
 - `NPPES_DEACTIVATION_DATE`  [date]
      - the day the clinician's id was shut off
      - WATCH: Text in MM/DD/YYYY; parse before sorting. Not profiled.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION**
one row = one clinician tied to one facility, current snapshot; used only to show it cannot answer this
connects: CCN matches CCN on HEALTH__FED_CMS_POS_OTHER; only 14% of provider-file ids appear here
 - `NPI`  [join]
      - the national id number of the clinician
 - `CCN`  [join]
      - Medicare's certification number for the facility the clinician is tied to
      - WATCH: Current snapshot; forgets closed hospitals and under-reports open ones, 35.5% of nursing homes list one clinician.
 - `FACILITY_TYPE`  [filter]
      - what kind of place it is: Hospital, Home health agency, Hospice, Nursing home, Dialysis facility

---

## 28) A lot of hospitals quietly own the home health agency they send you to after discharge, and we can count how many.  `W39` grade A
   - If the hospital owns the agency, the referral is also a sale. This counts ownership only, not who gets referred where.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS**
one row = one home health agency enrollment, one owner, one role
connects: ASSOCIATE_ID_OWNER matches ASSOCIATE_ID on HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS; ASSOCIATE_ID also matches ASSOCIATE_ID there, 411 shared values
 - `ENROLLMENT_ID`  [measure]
      - Medicare's id for one home health agency's sign-up record, 11,510 different ones
 - `ASSOCIATE_ID`  [join]
      - Medicare's id for the legal entity that runs the agency; links organizations only, never doctors
 - `ASSOCIATE_ID_OWNER`  [join]
      - Medicare's id for the person or company listed as an owner of the agency
 - `CCN`  [label]
      - Medicare's certification number for the home health agency
      - WATCH: Filled 98.12%. 95 rows carry a 7-character CCN with a letter suffix; a 6-character match drops them.
 - `ORGANIZATION_NAME`  [label]
      - the name of the home health agency's legal entity
 - `ORGANIZATION_NAME_OWNER`  [label]
      - the name of the company that owns a piece of the agency
 - `OWNER_KIND`  [filter]
      - whether the owner is an individual or an organization
 - `ROLE_TEXT_OWNER`  [filter]
      - the owner's role, such as CORPORATE DIRECTOR or 5% OR GREATER DIRECT OWNERSHIP INTEREST
 - `PERCENTAGE_OWNERSHIP`  [measure]
      - what percent of the agency this owner holds
      - WATCH: Fill not measured.
 - `AGENCY_STATE`  [filter]
      - the state the home health agency is in

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS**
one row = one Medicare enrollment of a hospital
connects: ASSOCIATE_ID matches ASSOCIATE_ID_OWNER and ASSOCIATE_ID on HEALTH__FED_CMS_HOME_HEALTH_OWNERS
 - `ASSOCIATE_ID`  [join]
      - Medicare's id for the hospital's legal entity, 5,162 different ones
      - WATCH: 9,175 rows for 5,162 entities; count distinct entities, not rows.
 - `CCN`  [label]
      - Medicare's certification number for the hospital, 9,201 different ones
 - `ORGANIZATION_NAME`  [label]
      - the name of the hospital's legal entity
 - `PROPRIETARY_NONPROFIT`  [filter]
      - one-letter code for profit status; N is nonprofit, P and D also seen; look at distinct values first
 - `ENROLLMENT_STATE`  [filter]
      - the state the hospital is enrolled in

---

## 29) Hospitals in counties where factories pump more chemicals into the air see a bigger share of patients with breathing trouble.  `W40` grade C
   - If true, factory air shows up in the local hospital's Medicare bills. It would point at which counties pay for dirty air with sick lungs.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023**
one row = one factory, one chemical, reporting year 2023
connects: first 5 digits of C_9_ZIP match XWALK_ZCTA_COUNTY.ZCTA5, which gives COUNTY_FIPS
 - `C_1_YEAR`  [date]
      - the reporting year of the release, 2023 on every row
 - `C_2_TRIFD`  [label]
      - the pollution program's id number for the factory
 - `C_9_ZIP`  [join]
      - the factory's ZIP code; take the first five digits
      - WATCH: ZIP identifies nothing on its own; it is shared by 129 tables
 - `C_7_COUNTY`  [label]
      - the county name the factory wrote on its report
 - `C_8_ST`  [filter]
      - two-letter state where the factory sits
 - `C_12_LATITUDE`  [label]
      - north-south map position of the factory
 - `C_13_LONGITUDE`  [label]
      - east-west map position of the factory
 - `C_37_CHEMICAL`  [label]
      - name of the chemical the factory released
 - `C_42_CLEAN_AIR_ACT_CHEMICAL`  [filter]
      - YES or NO: is the chemical on the Clean Air Act list
 - `C_50_UNIT_OF_MEASURE`  [filter]
      - unit the amounts are in: Pounds on most rows, Grams on 770
      - WATCH: releases mix units; check this before summing pounds
 - `C_51_5_1_FUGITIVE_AIR`  [measure]
      - amount that leaked into the air from leaks, vents and open tanks
 - `C_52_5_2_STACK_AIR`  [measure]
      - amount sent into the air through a stack or chimney

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE**
one row = one hospital, one diagnosis group, one year
connects: RNDRNG_PRVDR_ZIP5 matches XWALK_ZCTA_COUNTY.ZCTA5, which gives COUNTY_FIPS
 - `RNDRNG_PRVDR_CCN`  [join]
      - the federal certification number of the hospital, 2,855 different hospitals
 - `RNDRNG_PRVDR_ZIP5`  [join]
      - five-digit ZIP code of the hospital building
      - WATCH: single-building hospital ZIPs have no ZIP area and miss the county bridge entirely
 - `DRG_CD`  [filter]
      - code for the diagnosis group the stay was billed under
      - WATCH: which codes are respiratory is not in the sources; read DRG_DESC
 - `DRG_DESC`  [label]
      - plain description of the diagnosis group; read it to pick the breathing ones
 - `TOT_DSCHRGS`  [measure]
      - number of Medicare hospital stays in that diagnosis group
      - WATCH: Medicare fee-for-service only; the file's data year is not recorded anywhere
 - `AVG_MDCR_PYMT_AMT`  [measure]
      - average dollars Medicare paid per stay in that group

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP area and county overlap, 2020 vintage
connects: ZCTA5 is matched by C_9_ZIP and by RNDRNG_PRVDR_ZIP5; COUNTY_FIPS is the shared county on both sides
 - `ZCTA5`  [join]
      - the five-digit ZIP area drawn by the Census Bureau
      - WATCH: 10,186 of 33,791 ZIP areas cross a county line; single-building ZIPs have no ZIP area and miss
 - `COUNTY_FIPS`  [join]
      - the five-digit federal code for the county that ZIP area overlaps

**LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2013 to DY2024 (12 tables, same columns)**
one row = one clinician, one billing code, one place of service, one year
connects: optional: DY2023 RNDRNG_PRVDR_ZIP5 matches XWALK_ZCTA_COUNTY.ZCTA5, which gives COUNTY_FIPS
 - `NPI`  [label]
      - the national ten-digit id number of the clinician
      - WATCH: fill not yet measured
 - `RNDRNG_PRVDR_ZIP5`  [join]
      - the clinician's five-digit office ZIP code
      - WATCH: fill not yet measured
 - `RNDRNG_PRVDR_TYPE`  [filter]
      - the clinician's specialty, such as lung doctor
 - `HCPCS_CD`  [filter]
      - the billing code for the service done
      - WATCH: which codes count as respiratory is not in the sources; read HCPCS_DESC
 - `HCPCS_DESC`  [label]
      - plain description of the billing code; read it to pick breathing care
 - `TOT_BENES`  [measure]
      - number of different Medicare patients who got that service
      - WATCH: rows under 11 patients are deleted at the source; small rural practices lose most
 - `TOT_SRVCS`  [measure]
      - number of times the service was done

---

## 30) A handful of drugs drove Medicare's drug bill up over twelve years, and a few named prescribers wrote far more than their share of each.  `W44` grade B
   - If true, the cost growth has names on it, drug by drug. If not, the growth is just price and patient count spread over thousands of doctors.

**LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2013 to DY2024 (12 tables, same columns)**
one row = one prescriber, one drug, one year of claims
connects: stack the 12 tables with the year from the table name; NPI matches NPI on FED_CMS_PARTD_PRESCRIBER_DY of the same year
 - `NPI`  [join]
      - the national ten-digit id number of the prescriber
      - WATCH: fill not yet measured
 - `BRND_NAME`  [label]
      - the brand name of the drug as printed on the claim
 - `GNRC_NAME`  [label]
      - the generic name of the drug, free text
      - WATCH: a renamed or reformulated drug splits into two lines; check top names by eye
 - `TOT_DRUG_CST`  [measure]
      - total dollars paid for this prescriber's claims for this drug that year
      - WATCH: dollars of the year, not inflation adjusted; before or after rebates is not stated
 - `TOT_CLMS`  [measure]
      - number of prescriptions filled, refills included, for this prescriber and drug
 - `TOT_BENES`  [measure]
      - number of different Medicare patients who got this drug from this prescriber
 - `TOT_30DAY_FILLS`  [measure]
      - prescriptions restated as standard 30-day supplies
 - `PRSCRBR_TYPE`  [filter]
      - the prescriber's specialty, such as family practice or psychiatry
 - `PRSCRBR_STATE_ABRVTN`  [filter]
      - two-letter state of the prescriber's address
 - `PRSCRBR_CITY`  [label]
      - city of the prescriber's practice address
 - `GE65_SPRSN_FLAG`  [filter]
      - marker that the count for patients 65 and over was withheld; coded value, look at distinct values first
      - WATCH: by-drug tables store a blank as NULL, not an empty string

**LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2013 to DY2024 (12 tables, same columns)**
one row = one prescriber, one year of totals across all drugs
connects: NPI matches NPI on FED_CMS_PARTD_PRESCRIBER_DRUG_DY of the same year
 - `NPI`  [join]
      - the national ten-digit id number of the prescriber
      - WATCH: fill not yet measured
 - `PRSCRBR_TYPE`  [filter]
      - the prescriber's specialty; compare costly prescribers inside one specialty
 - `PRSCRBR_ZIP5`  [label]
      - five-digit ZIP of the prescriber's address
 - `TOT_DRUG_CST`  [measure]
      - total dollars for every drug this prescriber wrote that year
      - WATCH: blanks in this family are empty strings, not NULL
 - `TOT_BENES`  [measure]
      - number of different Medicare patients this prescriber wrote for
 - `BENE_AVG_RISK_SCRE`  [measure]
      - average sickness score of the prescriber's patients; higher means sicker

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS**
one row = one prescriber, one drug, data year 2022 only, with renamed columns
connects: cross-check only: its row count 25,869,521 equals FED_CMS_PARTD_PRESCRIBER_DRUG_DY2022
 - `NPI`  [join]
      - the national ten-digit id number of the prescriber, 1,038,177 different ones
 - `GENERIC_NAME`  [label]
      - the generic name of the drug, same thing as GNRC_NAME
 - `TOTAL_DRUG_COST`  [measure]
      - total dollars for this prescriber and drug, same thing as TOT_DRUG_CST

---

## 31) Nursing homes that share an owner dose their residents with antipsychotic drugs at about the same rate, high or low.  `W45` grade C
   - If true, how sedated grandma gets depends on who owns the building, not on her doctor. If not, prescribing follows the individual doctor.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS**
one row = one prescriber, one year of totals, data year 2024
connects: NPI matches HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI
 - `NPI`  [join]
      - the national ten-digit id number of the prescriber
 - `ANTPSYCT_GE65_TOT_CLMS`  [measure]
      - antipsychotic prescriptions filled for this prescriber's patients aged 65 and over
      - WATCH: text column; blank means a withheld count of 1 to 10, '0' is the real zero; spelled without the I
 - `ANTPSYCT_GE65_SPRSN_FLAG`  [filter]
      - marker that the antipsychotic count was withheld: '*' on 538,626 rows, blank on 878,257
 - `ANTPSYCT_GE65_TOT_BENES`  [measure]
      - number of patients 65 and over who got an antipsychotic from this prescriber
      - WATCH: fill not yet measured
 - `GE65_TOT_CLMS`  [measure]
      - all prescriptions of any drug filled for this prescriber's patients 65 and over
 - `PRSCRBR_TYPE`  [filter]
      - the prescriber's specialty, as Medicare lists it

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION**
one row = one clinician tied to one facility, current snapshot
connects: NPI matches HEALTH__FED_CMS_PART_D_PRESCRIBERS.NPI; CCN matches HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN
 - `NPI`  [join]
      - the national ten-digit id number of the clinician
 - `CCN`  [join]
      - the federal certification number of the facility the clinician is tied to
      - WATCH: 35.5% of nursing homes list exactly one clinician; the median is two
 - `FACILITY_TYPE`  [filter]
      - kind of facility: Hospital, Home health agency, Hospice, Nursing home, Dialysis facility

**LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411**
one row = one nursing home, snapshot of 2025-12-01
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_FACILITY_AFFILIATION.CCN and HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.CCN
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds the home is certified to fill
 - `CHAIN_ID`  [filter]
      - the id number of the chain the home belongs to
      - WATCH: blank on 4,551 homes; named chains include hospital systems
 - `CHAIN_NAME`  [label]
      - the name of the chain the home belongs to
 - `OWNERSHIP_TYPE`  [filter]
      - kind of owner, such as For profit - Corporation or Non profit - Corporation
 - `STATE`  [filter]
      - two-letter state where the home sits

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS**
one row = one Medicare enrollment of one nursing home
connects: CCN matches HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN; ENROLLMENT_ID matches FED_CMS_SNF_OWNERSHIP.ENROLLMENT_ID
 - `CCN`  [join]
      - the federal certification number of the nursing home
 - `ENROLLMENT_ID`  [join]
      - the id of this home's Medicare enrollment record
 - `AFFILIATION_ENTITY_ID`  [label]
      - id of a parent group the home says it belongs to; check distinct values before using

**LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP**
one row = one enrollment, one owner, one role
connects: ENROLLMENT_ID matches HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID
 - `ENROLLMENT_ID`  [join]
      - the id of the nursing home's Medicare enrollment record
      - WATCH: 288,550 of 295,083 owner rows join; 6,533 do not reach an enrollment; this file has no CCN
 - `ASSOCIATE_ID_OWNER`  [join]
      - the id number of the owner; group homes by this
      - WATCH: current owners only, one vintage
 - `ORGANIZATION_NAME_OWNER`  [label]
      - the company name of the owner
 - `ROLE_TEXT_OWNER`  [filter]
      - text saying what part this owner plays at the home
 - `PERCENTAGE_OWNERSHIP`  [filter]
      - what percent of the home this owner holds

---

## 32) Draw the line from opioid pills shipped to overdose deaths, then find the counties that sit far off that line.  `W46` grade B
   - A county with heavy pills and few deaths, or light pills and many, has something else going on. Those are the places worth a closer look.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS**
one row = one shipment of one opioid product from a reporter to a buyer, 2006-2012
connects: BUYER_COUNTY_FIPS matches HEALTH__FED_CDC_DRUG_POISONING_COUNTY.FIPS in the same year, and LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY.GEOID
 - `BUYER_COUNTY_FIPS`  [join]
      - the five-digit federal county code of the pharmacy or buyer
      - WATCH: filled on 178,338,557 of 178,598,026 rows
 - `TRANSACTION_DATE`  [date]
      - the day the pills were shipped
 - `DOSAGE_UNITS`  [measure]
      - number of pills in the shipment
 - `TOTAL_MME`  [measure]
      - strength of the shipment restated as morphine, so different opioids add up

**LIBRARY_RAW.LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY**
one row = one county, one kind of death, one period
connects: GEOID matches HEALTH__FED_DEA_ARCOS.BUYER_COUNTY_FIPS and HEALTH__FED_CDC_DRUG_POISONING_COUNTY.FIPS
 - `GEOID`  [join]
      - the five-digit federal county code, 3,153 different counties
 - `INTENT`  [filter]
      - which kind of death the row counts, such as All_Homicide, FA_Suicide; pick the overdose one
 - `PERIOD`  [date]
      - the year, 2019 to 2024, or TTM for the trailing twelve months
 - `RATE`  [measure]
      - deaths per population in that county and period
      - WATCH: -999 on 822 overdose rows; filter RATE >= 0 before fitting
 - `COUNT_SUP`  [measure]
      - number of deaths, or a range like '1-9' or '10-50' when withheld
      - WATCH: text column; the mart nulled 61,400 of 132,000 values, so use landing; a range is not a count

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY**
one row = one county, one year, with population, 1999-2015
connects: FIPS matches HEALTH__FED_DEA_ARCOS.BUYER_COUNTY_FIPS in the same year and LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY.GEOID
 - `FIPS`  [join]
      - the five-digit federal code for the county
 - `YEAR`  [date]
      - the calendar year of the population figure
      - WATCH: ends 2015; no county population after that is landed
 - `POPULATION`  [measure]
      - number of residents in the county that year; divides pills into pills per resident
      - WATCH: fill not yet measured

---

## 33) Once you allow for how old the patients are, some counties still write far more prescriptions per patient, year after year.  `W47` grade B
   - If true, heavy prescribing is a local habit, not just old patients. If not, the map of heavy prescribing is only a map of age.

**LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2013 to DY2024 (12 tables, same columns)**
one row = one prescriber, one year of totals
connects: PRSCRBR_ZIP5 matches XWALK_ZCTA_COUNTY.ZCTA5, which gives COUNTY_FIPS
 - `NPI`  [label]
      - the national ten-digit id number of the prescriber
      - WATCH: fill not yet measured
 - `PRSCRBR_ZIP5`  [join]
      - five-digit ZIP of the prescriber's address, not where the patient lives
      - WATCH: blanks are empty strings, not NULL; an is-null test finds nothing
 - `PRSCRBR_TYPE`  [filter]
      - the prescriber's specialty, as Medicare lists it
 - `TOT_CLMS`  [measure]
      - number of prescriptions filled, refills included, across all drugs
 - `TOT_BENES`  [measure]
      - number of different Medicare patients the prescriber wrote for
 - `TOT_30DAY_FILLS`  [measure]
      - prescriptions restated as standard 30-day supplies
 - `BENE_AVG_AGE`  [measure]
      - average age of this prescriber's Medicare drug patients
 - `BENE_AGE_LT_65_CNT`  [measure]
      - how many of the prescriber's patients are under 65
      - WATCH: may be withheld below 11, not yet measured; prefer BENE_AVG_AGE
 - `BENE_AGE_65_74_CNT`  [measure]
      - how many of the prescriber's patients are 65 to 74
      - WATCH: may be withheld below 11, not yet measured; prefer BENE_AVG_AGE
 - `BENE_AGE_75_84_CNT`  [measure]
      - how many of the prescriber's patients are 75 to 84
      - WATCH: may be withheld below 11, not yet measured; prefer BENE_AVG_AGE
 - `BENE_AGE_GT_84_CNT`  [measure]
      - how many of the prescriber's patients are over 84
      - WATCH: may be withheld below 11, not yet measured; prefer BENE_AVG_AGE
 - `BENE_AVG_RISK_SCRE`  [measure]
      - average sickness score of the prescriber's patients; higher means sicker

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS**
one row = one prescriber, data year 2024 only, the profiled copy
connects: PRSCRBR_ZIP5 matches XWALK_ZCTA_COUNTY.ZCTA5
 - `NPI`  [label]
      - the national ten-digit id number of the prescriber
 - `PRSCRBR_ZIP5`  [join]
      - five-digit ZIP of the prescriber's address, 21,041 different ZIPs
      - WATCH: 54 blank strings

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP area and county overlap, 2020 vintage
connects: ZCTA5 is matched by PRSCRBR_ZIP5; ZCTA5 and COUNTY_FIPS line up with GEOID_ZCTA5_20 and GEOID_COUNTY_20 on FED_CENSUS_ZCTA_COUNTY_2020
 - `ZCTA5`  [join]
      - the five-digit ZIP area drawn by the Census Bureau
      - WATCH: 10,186 of 33,791 ZIP areas cross a county line; single-building ZIPs get no ZIP area, 4.7% of doctor rows lost
 - `COUNTY_FIPS`  [join]
      - the five-digit federal county code, 3,266 different counties
 - `COUNTY_NAME`  [label]
      - the plain name of the county
 - `STATE_USPS`  [label]
      - two-letter postal abbreviation of the state

**LIBRARY_RAW.LANDING.FED_CENSUS_ZCTA_COUNTY_2020**
one row = one ZIP area and county overlap, with land area
connects: GEOID_ZCTA5_20 and GEOID_COUNTY_20 match XWALK_ZCTA_COUNTY.ZCTA5 and COUNTY_FIPS; used as a tie-break
 - `GEOID_ZCTA5_20`  [join]
      - the five-digit ZIP area, 2020 edition
 - `GEOID_COUNTY_20`  [join]
      - the five-digit federal county code, 2020 edition
 - `AREALAND_PART`  [measure]
      - land area of the piece of the ZIP area inside that county; largest wins
      - WATCH: the largest-land-area pick is right 47.1% of the time on ZIP areas that cross a county line

---

## 34) A drug company buys a doctor lunch or pays a speaking fee, and the next year that doctor writes more of the company's brand.  `W48` grade B
   - If true, the money comes before the prescribing, doctor by doctor. If not, the money just follows doctors who already wrote the drug.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022**
one row = one payment or gift from a drug or device maker to one recipient, year 2022
connects: NPI matches NPI on FED_CMS_PARTD_PRESCRIBER_DRUG_DY2021 and DY2022 for before, DY2023 for after; stack the three payment tables, never join them, zero RECORD_ID overlap
 - `NPI`  [join]
      - the national ten-digit id number of the doctor who got the payment
      - WATCH: blank is an empty string, not null, on 51,584 rows; a null filter misses them
 - `PROGRAM_YEAR`  [date]
      - the calendar year the payment was reported for
 - `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`  [measure]
      - dollars in this one payment or gift
      - WATCH: sum only this column; any sum over columns matching PAYMENT reads $1.5 quadrillion
 - `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`  [filter]
      - what the money was for, such as Food and Beverage, Travel and Lodging, speaker fees, royalties
      - WATCH: Debt forgiveness ($40.8M) and Acquisitions ($213M) are not cheques to a doctor
 - `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME`  [label]
      - name of the drug or device company that paid
      - WATCH: payer names split on case: 'ABBVIE INC.' and 'AbbVie Inc.'
 - `DATE_OF_PAYMENT`  [date]
      - the day the payment was made
      - WATCH: year-0002 dates seen on 73 rows of the 2024 table; count here not yet measured; use PROGRAM_YEAR
 - `COVERED_RECIPIENT_SPECIALTY_1`  [filter]
      - the first specialty listed for the doctor paid
 - `RECIPIENT_STATE`  [filter]
      - two-letter state of the doctor's address

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023**
one row = one payment or gift from a drug or device maker to one recipient, year 2023
connects: NPI matches NPI on FED_CMS_PARTD_PRESCRIBER_DRUG_DY2022 and DY2023 for before, DY2024 for after; stack the three payment tables, never join them, zero RECORD_ID overlap
 - `NPI`  [join]
      - the national ten-digit id number of the doctor who got the payment
      - WATCH: blank is an empty string, not null, on 44,233 rows; a null filter misses them
 - `PROGRAM_YEAR`  [date]
      - the calendar year the payment was reported for
 - `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`  [measure]
      - dollars in this one payment or gift
      - WATCH: sum only this column; any sum over columns matching PAYMENT reads $1.5 quadrillion
 - `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`  [filter]
      - what the money was for, such as Food and Beverage, Travel and Lodging, speaker fees, royalties
      - WATCH: Debt forgiveness ($40.8M) and Acquisitions ($213M) are not cheques to a doctor
 - `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME`  [label]
      - name of the drug or device company that paid
      - WATCH: payer names split on case: 'ABBVIE INC.' and 'AbbVie Inc.'
 - `DATE_OF_PAYMENT`  [date]
      - the day the payment was made
      - WATCH: year-0002 dates seen on 73 rows of the 2024 table; count here not yet measured; use PROGRAM_YEAR
 - `COVERED_RECIPIENT_SPECIALTY_1`  [filter]
      - the first specialty listed for the doctor paid
 - `RECIPIENT_STATE`  [filter]
      - two-letter state of the doctor's address

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS**
one row = one payment or gift from a drug or device maker to one recipient, year 2024
connects: NPI matches FED_CMS_PARTD_PRESCRIBER_DRUG_DY2024.NPI, same year only; no DY2025 is landed; stack the three payment tables, never join them, zero RECORD_ID overlap
 - `NPI`  [join]
      - the national ten-digit id number of the doctor who got the payment
      - WATCH: blank is an empty string, not null, on 48,059 rows; a null filter misses them
 - `PROGRAM_YEAR`  [date]
      - the calendar year the payment was reported for
 - `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`  [measure]
      - dollars in this one payment or gift
      - WATCH: sum only this column; any sum over columns matching PAYMENT reads $1.5 quadrillion
 - `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`  [filter]
      - what the money was for, such as Food and Beverage, Travel and Lodging, speaker fees, royalties
      - WATCH: Debt forgiveness ($40.8M) and Acquisitions ($213M) are not cheques to a doctor
 - `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME`  [label]
      - name of the drug or device company that paid
      - WATCH: payer names split on case: 'ABBVIE INC.' and 'AbbVie Inc.'
 - `DATE_OF_PAYMENT`  [date]
      - the day the payment was made
      - WATCH: 73 rows in the 2024 table carry year-0002 dates; use PROGRAM_YEAR for the year
 - `COVERED_RECIPIENT_SPECIALTY_1`  [filter]
      - the first specialty listed for the doctor paid
 - `RECIPIENT_STATE`  [filter]
      - two-letter state of the doctor's address

**LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2021 to DY2024 (4 tables, same columns)**
one row = one prescriber, one drug, one year of claims
connects: NPI matches NPI on the three payment tables; unpaid peers share PRSCRBR_TYPE and PRSCRBR_STATE_ABRVTN
 - `NPI`  [join]
      - the national ten-digit id number of the prescriber
      - WATCH: fill not yet measured
 - `BRND_NAME`  [label]
      - the brand name of the drug as printed on the claim
 - `GNRC_NAME`  [label]
      - the generic name of the drug, free text
      - WATCH: a renamed or reformulated drug splits into two lines; check top names by eye
 - `TOT_DRUG_CST`  [measure]
      - total dollars paid for this prescriber's claims for this drug that year
      - WATCH: dollars of the year, not inflation adjusted; before or after rebates is not stated
 - `TOT_CLMS`  [measure]
      - number of prescriptions filled, refills included, for this prescriber and drug
 - `TOT_BENES`  [measure]
      - number of different Medicare patients who got this drug from this prescriber
 - `PRSCRBR_TYPE`  [filter]
      - the prescriber's specialty, such as family practice or psychiatry
 - `PRSCRBR_STATE_ABRVTN`  [filter]
      - two-letter state of the prescriber's address
 - `GE65_SPRSN_FLAG`  [filter]
      - marker that the count for patients 65 and over was withheld; coded value, look at distinct values first
      - WATCH: by-drug tables store a blank as NULL, not an empty string

---

## 35) Some doctors banned from billing federal health programs are still getting paid by drug and device companies.  `W49` grade B
   - If true, it is a named list of barred doctors, the companies paying them and the amounts. It shows an overlap, not a crime.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE**
one row = one active ban of a person or business from federal health programs
connects: NPI, where NPI_IS_REAL is true, matches HEALTH__FED_CMS_OPEN_PAYMENTS.NPI
 - `NPI`  [join]
      - the national ten-digit id number of the banned person or business
      - WATCH: only 10.55% filled, 8,935 distinct; the '0000000000' placeholder is blanked to an empty string on 74,908 rows
 - `NPI_IS_REAL`  [filter]
      - true when the row carries a real id number: true 8,839 rows, false 74,908
 - `EXCLUSION_DATE`  [date]
      - the day the ban started, 1977-07-01 to 2026-08-20
 - `EXCLUSION_TYPE`  [filter]
      - the section of law the ban was made under, such as 1128b4 or 1128a1
 - `LAST_NAME`  [label]
      - last name of the banned person
 - `FIRST_NAME`  [label]
      - first name of the banned person
 - `SPECIALTY`  [label]
      - the banned person's line of work
 - `STATE`  [filter]
      - two-letter state of the banned person
 - `IS_ENTITY_NOT_INDIVIDUAL`  [filter]
      - true when the row is a business, not a person: true on 3,424 rows

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS**
one row = one payment or gift from a drug or device maker to one recipient, year 2024 only
connects: NPI matches HEALTH__FED_HHS_OIG_LEIE.NPI; keep rows where DATE_OF_PAYMENT is after EXCLUSION_DATE
 - `NPI`  [join]
      - the national ten-digit id number of the doctor who got the payment
      - WATCH: blank is an empty string, not null, on 48,059 rows; a null filter misses them
 - `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`  [measure]
      - dollars in this one payment or gift
      - WATCH: sum only this column; any sum over columns matching PAYMENT reads $1.5 quadrillion
 - `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`  [filter]
      - what the money was for, such as Food and Beverage, Travel and Lodging, speaker fees, royalties
      - WATCH: Debt forgiveness ($40.8M) and Acquisitions ($213M) are not cheques to a doctor
 - `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME`  [label]
      - name of the drug or device company that paid
      - WATCH: payer names split on case: 'ABBVIE INC.' and 'AbbVie Inc.'
 - `DATE_OF_PAYMENT`  [date]
      - the day the payment was made
      - WATCH: 73 payment rows carry year-0002 dates

---

## 36) Implants that pay royalties to surgeons get recalled more often than the same maker's other products.  `W50` grade C
   - If true, the devices surgeons have a money stake in are the ones that fail more. Patients would want to know that before surgery.

**LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS**
one row = one payment, with up to five product slots
connects: ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1 matches HEALTH__FED_FDA_GUDID.PRIMARY_DI, or FED_FDA_GUDID_FULL_IDENTIFIERS.DEVICEID for the wider net
 - `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`  [filter]
      - what the money was for; keep the royalty rows
 - `NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1`  [label]
      - name of the first product the payment was tied to
      - WATCH: product columns live only in this landing copy; the mart drops them
 - `ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1`  [join]
      - the device id number printed on the first product the payment was tied to
      - WATCH: fill rate not yet measured; may turn out empty
 - `INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1`  [filter]
      - says whether that first product is a drug, biological, device or medical supply
 - `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME`  [label]
      - name of the company that paid
 - `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`  [measure]
      - dollars paid in this one payment
      - WATCH: sum only this column; any sum over columns matching PAYMENT reads $1.5 quadrillion
 - `DATE_OF_PAYMENT`  [date]
      - the day the payment was made
 - `NPI`  [label]
      - the national ten-digit id number of the surgeon paid
      - WATCH: blank on rows holding 43% of all royalty dollars

**LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID**
one row = one device record in the federal device id database
connects: PRIMARY_DI is matched by ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1; COMPANY_NAME plus BRAND_NAME text-match DEVICE_ENFORCEMENT.RECALLING_FIRM plus PRODUCT_DESCRIPTION
 - `PRIMARY_DI`  [join]
      - the main id number printed on the device
      - WATCH: fill rate not yet measured
 - `BRAND_NAME`  [join]
      - the brand name the device is sold under
      - WATCH: text match only; single-word name matches were 8% real, multi-word 92%
 - `COMPANY_NAME`  [join]
      - the company that makes the device, 11,851 different companies
      - WATCH: text match only; use multi-word names
 - `PRIMARY_PRODUCT_CODE`  [label]
      - the federal code for the kind of device, 99.38% filled
      - WATCH: dead hop: the recall table's PRODUCT_CODE is 0.0% filled

**LIBRARY_RAW.LANDING.FED_FDA_GUDID_FULL_IDENTIFIERS**
one row = one id number, main or package level, for one device
connects: DEVICEID is matched by ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1; PRIMARYDI matches FED_FDA_GUDID_FULL_DEVICE.PRIMARYDI
 - `DEVICEID`  [join]
      - an id number printed on the device or on its box
      - WATCH: fill rate not yet measured
 - `DEVICEIDTYPE`  [filter]
      - whether the id is the main one or a package one; coded value, look at distinct values first
 - `PRIMARYDI`  [join]
      - the main id number of the device this id belongs to
      - WATCH: fill rate not yet measured

**LIBRARY_RAW.LANDING.FED_FDA_GUDID_FULL_DEVICE**
one row = one device record, the full 37-column file
connects: PRIMARYDI matches FED_FDA_GUDID_FULL_IDENTIFIERS.PRIMARYDI
 - `PRIMARYDI`  [join]
      - the main id number printed on the device
      - WATCH: fill rate not yet measured
 - `BRANDNAME`  [label]
      - the brand name the device is sold under
 - `COMPANYNAME`  [label]
      - the company that makes the device
 - `VERSIONMODELNUMBER`  [label]
      - the maker's version or model number
 - `CATALOGNUMBER`  [label]
      - the maker's catalog number for the device

**LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT**
one row = one device recall
connects: RECALLING_FIRM plus PRODUCT_DESCRIPTION text-match HEALTH__FED_FDA_GUDID.COMPANY_NAME plus BRAND_NAME; the PRODUCT_CODE hop is dead
 - `RECALL_NUMBER`  [label]
      - the federal number given to the recall
 - `RECALLING_FIRM`  [join]
      - name of the company pulling the device back
      - WATCH: text match, not an id
 - `PRODUCT_DESCRIPTION`  [join]
      - free-text description of the recalled device
      - WATCH: text match, not an id
 - `CLASSIFICATION`  [filter]
      - how serious the recall is: Class I, Class II or Class III
 - `RECALL_INITIATION_DATE`  [date]
      - the day the company started the recall
      - WATCH: runs back to 1930-12-11; payments are 2024 only, so only 2024 to 2026-07-07 recalls can follow
 - `PRODUCT_CODE`  [join]
      - meant to hold the federal code for the kind of device
      - WATCH: 0.0% filled, 0 distinct; empty column

---

## 37) The same nursing-home problem gets written up as serious harm in one state and as a minor slip in another.  `H-106` grade A
   - The federal rulebook is the same everywhere, so a 9.5x gap means the inspectors differ, not the homes. A home's record then depends on its state line.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation at one home on one inspection
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home that was cited
 - `STATE`  [filter]
      - the state whose inspectors wrote the citation
      - WATCH: citation volumes differ 25x across states; use rates and a 2,000+ citation floor
 - `SCOPE_SEVERITY_CODE`  [measure]
      - letter grade A to L for how bad and how widespread; G through L means harm
 - `DEFICIENCY_TAG_NUMBER`  [filter]
      - the number of the federal rule the home broke
 - `SURVEY_DATE`  [date]
      - the day the inspectors were in the building
      - WATCH: real coverage is 2023-2026 only: 273 rows in 2017 against 121,925 in 2024
 - `SURVEY_TYPE`  [filter]
      - kind of inspection; every row in the profile says Health

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, current snapshot
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
      - WATCH: 14,700 rows but 14,328 distinct numbers; dedupe before joining or rows double
 - `NUMBER_OF_CERTIFIED_BEDS`  [filter]
      - how many beds the home is certified to fill; use for size bands
      - WATCH: today's snapshot value, laid over older events
 - `OWNERSHIP_TYPE`  [filter]
      - kind of owner, such as For profit - Limited Liability company or Non profit - Corporation
 - `CHAIN_NAME`  [label]
      - the name of the chain the home belongs to
 - `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - nurse hours of all kinds per resident per day, as the home reported
      - WATCH: fill not yet measured

---

## 38) Nursing homes where nurses keep quitting, or where there are too few of them, get written up more at the next inspection.  `H-094` grade B
   - If true, staff churn is an early warning you can read before the inspector shows up. If not, the inspection record ignores staffing.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411**
one row = one nursing home, earlier snapshot, staffing as of 2025-12-01
connects: CMS_CERTIFICATION_NUMBER_CCN matches the same column on HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES and HEALTH__FED_CMS_NURSING_HOME
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
      - WATCH: 14,713 rows but 14,345 distinct numbers; dedupe before joining or rows double
 - `PROCESSING_DATE`  [date]
      - the day this snapshot was cut, 2025-12-01 on every row
 - `TOTAL_NURSING_STAFF_TURNOVER`  [measure]
      - share of all nursing staff who left within the year; test this first
      - WATCH: fill not yet measured; homes with blank staffing drop out
 - `REGISTERED_NURSE_TURNOVER`  [measure]
      - share of registered nurses who left within the year
      - WATCH: fill not yet measured
 - `NUMBER_OF_ADMINISTRATORS_WHO_HAVE_LEFT_THE_NURSING_HOME`  [measure]
      - how many administrators quit the home in the year
      - WATCH: fill not yet measured
 - `REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - registered-nurse hours per resident per day, as the home reported
      - WATCH: fill not yet measured
 - `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - nurse hours of all kinds per resident per day, as the home reported
      - WATCH: fill not yet measured
 - `DEVIATION_FROM_EXPECTED_TOTAL_NURSE_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - gap between the nurse hours reported and the nurse hours expected for the home
      - WATCH: fill not yet measured
 - `TOTAL_NUMBER_OF_NURSE_STAFF_HOURS_PER_RESIDENT_PER_DAY_ON_THE_WEEKEND`  [measure]
      - nurse hours per resident per day on weekends
      - WATCH: fill not yet measured
 - `NUMBER_OF_CERTIFIED_BEDS`  [filter]
      - how many beds the home is certified to fill; use for size bands
 - `OWNERSHIP_TYPE`  [filter]
      - kind of owner, such as For profit - Limited Liability company or Non profit - Corporation
 - `STATE`  [filter]
      - two-letter state of the home; compare inside one state

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation at one home on one inspection
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN; keep SURVEY_DATE after 2025-12-01
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home that was cited
 - `SURVEY_DATE`  [date]
      - the day the inspectors were in the building
      - WATCH: forward window is only 2025-12-01 to 2026-05-20; count citations per survey date, not per home
 - `SCOPE_SEVERITY_CODE`  [measure]
      - letter grade A to L for how bad and how widespread; G through L means harm
 - `DEFICIENCY_TAG_NUMBER`  [filter]
      - the number of the federal rule the home broke

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, later snapshot
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
 - `TOTAL_NURSING_STAFF_TURNOVER`  [measure]
      - share of nursing staff who left within the year
      - WATCH: fill not yet measured
 - `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - nurse hours of all kinds per resident per day, as the home reported
      - WATCH: fill not yet measured

---

## 39) Add up nursing-home fines by who owns the homes, and a few owners turn out to collect the same fine over and over.  `H-107` grade B
   - A fine per building looks small. A fine per owner across forty buildings shows who treats penalties as a cost of doing business.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES**
one row = one fine or payment denial against one home
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.CCN, and HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN on the side path
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home that was penalised
 - `PENALTY_DATE`  [date]
      - the day the fine or payment denial was issued, 2023-06-17 to 2026-05-13
 - `PENALTY_TYPE`  [filter]
      - what the penalty was: Fine, or Payment Denial
      - WATCH: only Fine rows carry a dollar amount; 2,470 of 16,180 rows are payment denials
 - `FINE_AMOUNT`  [measure]
      - dollars the home was fined on this row
      - WATCH: blank on the 2,470 payment-denial rows, 15% of the table
 - `FINE_ID`  [label]
      - the id number given to one fine
      - WATCH: blank on 2,470 payment-denial rows; count distinct drops them silently; not a full row id

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, current snapshot
connects: side path: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN, then group by CHAIN_ID
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
 - `CHAIN_NAME`  [label]
      - the name of the chain the home belongs to
      - WATCH: blank on 4,221 of 14,700 homes, 28.7%
 - `CHAIN_ID`  [filter]
      - the id number of the chain the home belongs to
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds the home is certified to fill; divides fines into dollars per bed
 - `STATE`  [filter]
      - two-letter state where the home sits
      - WATCH: Illinois fines $825 per bed against $261 for the rest of the US

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS**
one row = one Medicare enrollment of one nursing home
connects: CCN matches HEALTH__FED_CMS_NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN; ENROLLMENT_ID matches FED_CMS_SNF_OWNERSHIP.ENROLLMENT_ID
 - `ENROLLMENT_ID`  [join]
      - the id of this home's Medicare enrollment record
 - `CCN`  [join]
      - the federal certification number of the nursing home, 14,026 different ones
 - `ORGANIZATION_NAME`  [label]
      - the legal name the home enrolled under

**LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP**
one row = one enrollment, one owner, one role
connects: ENROLLMENT_ID matches HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID; then group by ASSOCIATE_ID_OWNER
 - `ENROLLMENT_ID`  [join]
      - the id of the nursing home's Medicare enrollment record
      - WATCH: 288,550 of 295,083 owner rows join; 6,533 name enrollments the snapshot does not carry
 - `ASSOCIATE_ID_OWNER`  [join]
      - the id number of the owner, 89,543 different ones; group fines by this
      - WATCH: current owners only; a home bought in 2025 hands its 2023 fines to the new owner
 - `ORGANIZATION_NAME_OWNER`  [label]
      - the company name of the owner
 - `ROLE_TEXT_OWNER`  [filter]
      - what the owner's role is; top value is ADP OF THE SNF at 93,015 rows
      - WATCH: pick roles first, or one fine is counted once per officer
 - `PERCENTAGE_OWNERSHIP`  [filter]
      - what percent of the home this owner holds; use as a floor
      - WATCH: filled on 96,823 of 295,083 rows
 - `TYPE_OWNER`  [filter]
      - kind of owner; coded value, look at distinct values first

---

## 40) When a nursing home gets fined and loses a star on the public rating site, which one happened first?  `H-105` grade C
   - If the fine comes first, stars are a late signal for families. If the star drops first, the rating is an early warning of fines to come.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES**
one row = one fine or payment denial against one home
connects: CMS_CERTIFICATION_NUMBER_CCN matches the same column on HEALTH__FED_NURSINGHOME411 and HEALTH__FED_CMS_NURSING_HOME
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home that was penalised
 - `PENALTY_DATE`  [date]
      - the day the fine or payment denial was issued, 2023-06-17 to 2026-05-13
 - `PENALTY_TYPE`  [filter]
      - what the penalty was: Fine, or Payment Denial
      - WATCH: only Fine rows carry a dollar amount; 2,470 of 16,180 rows are payment denials
 - `FINE_AMOUNT`  [measure]
      - dollars the home was fined on this row
      - WATCH: blank on the 2,470 payment-denial rows, 15% of the table

**LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411**
one row = one nursing home, earlier snapshot of 2025-12-01, with stars and two rating cycles
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN; star change is later OVERALL_RATING minus earlier
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
      - WATCH: 14,713 rows but 14,345 distinct numbers; dedupe before joining or rows double
 - `OVERALL_RATING`  [measure]
      - the home's overall star rating, one to five, as of 2025-12-01
      - WATCH: fill not yet measured
 - `HEALTH_INSPECTION_RATING`  [measure]
      - the star rating for inspections alone, one to five
      - WATCH: fill not yet measured
 - `RATING_CYCLE_1_STANDARD_SURVEY_HEALTH_DATE`  [date]
      - the day of the most recent regular inspection that feeds the stars
 - `RATING_CYCLE_2_STANDARD_HEALTH_SURVEY_DATE`  [date]
      - the day of the regular inspection before that one
 - `RATING_CYCLE_1_TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES`  [measure]
      - citations written at the most recent regular inspection
 - `RATING_CYCLE_2_3_TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES`  [measure]
      - citations written at the earlier regular inspections

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, later snapshot of 2026-05-01, with stars
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
      - WATCH: 14,700 rows but 14,328 distinct numbers; dedupe before joining or rows double
 - `OVERALL_RATING`  [measure]
      - the home's overall star rating, one to five, as of 2026-05-01
      - WATCH: only two star readings five months apart; penalties end 2026-05-13
 - `HEALTH_INSPECTION_RATING`  [measure]
      - the star rating for inspections alone, one to five
      - WATCH: a fine and a lost inspection star often come from the same inspection
 - `RATING_CYCLE_1_TOTAL_HEALTH_SCORE`  [measure]
      - the inspection points score from the most recent regular inspection
      - WATCH: fill not yet measured
 - `RATING_CYCLE_2_3_TOTAL_HEALTH_SCORE`  [measure]
      - the inspection points score from the earlier regular inspections
      - WATCH: fill not yet measured

---

## 41) Some big, thinly staffed, for-profit nursing homes in tough states have almost no citations, and that looks too good to be true.  `H-110` grade B
   - A record far cleaner than similar homes means either a very good home or a weak inspection. Either way it is a short list worth a visit.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, current snapshot
connects: CMS_CERTIFICATION_NUMBER_CCN left-joins to HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN so homes with no citations stay in
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
      - WATCH: 14,700 rows but 14,328 distinct numbers; dedupe before joining or rows double
 - `STATE`  [filter]
      - two-letter state of the home; peers must be in the same state
 - `NUMBER_OF_CERTIFIED_BEDS`  [filter]
      - how many beds the home is certified to fill; use for size bands
      - WATCH: fill not yet measured
 - `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`  [measure]
      - how many residents live in the home on a typical day
      - WATCH: fill not yet measured
 - `OWNERSHIP_TYPE`  [filter]
      - kind of owner, such as For profit - Limited Liability company or Non profit - Corporation
 - `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - nurse hours of all kinds per resident per day, as the home reported
      - WATCH: fill not yet measured
 - `TOTAL_NURSING_STAFF_TURNOVER`  [measure]
      - share of nursing staff who left within the year
      - WATCH: fill not yet measured
 - `DATE_OF_MOST_RECENT_HEALTH_INSPECTION`  [date]
      - the day inspectors last walked the home
 - `MOST_RECENT_HEALTH_INSPECTION_MORE_THAN_2_YEARS_AGO`  [filter]
      - Y when the last inspection is over two years old: Y 1,057 homes, N 13,643
      - WATCH: check this first; a skipped inspection looks the same as a clean record
 - `TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES`  [measure]
      - the home's citation count as the snapshot states it
      - WATCH: fill not yet measured
 - `DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES`  [date]
      - the day the home was first approved to take Medicare and Medicaid patients
      - WATCH: a home that opened in 2025 looks clean because it is new

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation at one home on one inspection
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the cited home, 14,275 different homes
      - WATCH: a home with zero citations has no rows here at all
 - `SURVEY_DATE`  [date]
      - the day the inspectors were in the building
      - WATCH: real coverage is 2023-2026 only: 273 rows in 2017 against 121,925 in 2024
 - `SCOPE_SEVERITY_CODE`  [measure]
      - letter grade A to L for how bad and how widespread; G through L means harm
 - `SURVEY_TYPE`  [filter]
      - kind of inspection; every row in the profile says Health

---

## 42) After a nursing home gets fined, does it actually clean up, compared with a similar home that was never fined?  `H-104` grade B
   - If citations drop after a fine, fines work. If not, the fine is just a bill the home pays and carries on.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES**
one row = one fine or payment denial against one home
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN; split citations at the first PENALTY_DATE
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home that was penalised
 - `PENALTY_DATE`  [date]
      - the day the fine or payment denial was issued, 2023-06-17 to 2026-05-13
      - WATCH: 3,722 homes have 2+ penalties; the first fine in this window may not be the first ever
 - `PENALTY_TYPE`  [filter]
      - what the penalty was: Fine, or Payment Denial
      - WATCH: 2,470 of 16,180 rows are payment denials; decide up front whether they count
 - `FINE_AMOUNT`  [measure]
      - dollars the home was fined on this row
      - WATCH: blank on the 2,470 payment-denial rows

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation at one home on one inspection
connects: CMS_CERTIFICATION_NUMBER_CCN matches HEALTH__FED_CMS_NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home that was cited
 - `SURVEY_DATE`  [date]
      - the day the inspectors were in the building
      - WATCH: fined homes get inspected more; count citations per survey date, real coverage 2023-2026
 - `SCOPE_SEVERITY_CODE`  [measure]
      - letter grade A to L for how bad and how widespread; G through L means harm
 - `DEFICIENCY_TAG_NUMBER`  [filter]
      - the number of the federal rule the home broke

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, current snapshot; the pool of unfined look-alike homes
connects: CMS_CERTIFICATION_NUMBER_CCN matches the same column on penalties and deficiencies; twin homes share STATE, bed band and OWNERSHIP_TYPE
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - the federal certification number of the nursing home
 - `STATE`  [filter]
      - two-letter state of the home; twins must share it
 - `NUMBER_OF_CERTIFIED_BEDS`  [filter]
      - how many beds the home is certified to fill; use for size bands
      - WATCH: today's snapshot, not the value at the time of the fine
 - `OWNERSHIP_TYPE`  [filter]
      - kind of owner, such as For profit - Limited Liability company or Non profit - Corporation
 - `LATITUDE`  [label]
      - north-south map position of the home
 - `LONGITUDE`  [label]
      - east-west map position of the home

---

## 43) Guess how many citations each nursing home should get from its size, staffing, owner type and state, then list the homes where the guess was way off.  `WN-147` grade B
   - A home far off the guess has something going on that size and staffing do not explain. If the misses share one state agency or one owner, that is the lead.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, current snapshot; the model inputs
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES, measured 100%, left join
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `STATE`  [filter]
      - two-letter state the home sits in
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds Medicare has approved at this home
 - `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`  [measure]
      - how many people actually live in the home on a typical day
 - `OWNERSHIP_TYPE`  [filter]
      - who owns it in words, such as For profit - Limited Liability company or Non profit - Corporation
 - `URBAN`  [filter]
      - Y if the home is in a city area, N if rural
 - `PROVIDER_RESIDES_IN_HOSPITAL`  [filter]
      - Y if the home sits inside a hospital, N if it stands alone
 - `REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - registered nurse hours worked per resident per day, as the home reported
 - `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - all nursing staff hours worked per resident per day, as the home reported
 - `NURSING_CASE_MIX_INDEX`  [measure]
      - score for how sick the residents are, so staffing can be compared fairly
 - `TOTAL_NURSING_STAFF_TURNOVER`  [measure]
      - share of all nursing staff who left during the year
 - `REGISTERED_NURSE_TURNOVER`  [measure]
      - share of registered nurses who left during the year

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation; the outcome
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME, measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `SURVEY_DATE`  [date]
      - the day inspectors visited and wrote this citation
      - WATCH: runs 2017-03-23 to 2026-05-20 but real coverage is 2023-2026; 273 rows in 2017 against 121,925 in 2024
 - `SCOPE_SEVERITY_CODE`  [measure]
      - letter grade for how bad and how widespread the problem was; D is most common, then E, F, G, J

---

## 44) Medicare puts the worst nursing homes on a named watch list, so check whether the homes that got picked improve faster than equally bad homes that did not.  `WN-149` grade C
   - If listed homes and the runner-up homes track each other, the watch list changes nothing the citation record can show. That matters because the list is Medicare's main tool for the worst homes.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, later snapshot dated 2026-05-01
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_NURSINGHOME411 and on HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES, both measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `SPECIAL_FOCUS_STATUS`  [filter]
      - watch list status: SFF means on the list, SFF Candidate means just as bad but not picked, blank means neither
      - WATCH: 88 listed and 440 candidates; there is no date saying when a home was listed
 - `STATE`  [filter]
      - two-letter state the home sits in
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds Medicare has approved at this home

**LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411**
one row = one nursing home, earlier snapshot dated 2025-12-01
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME, measured 100%; compare SPECIAL_FOCUS_STATUS across the two
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `SPECIAL_FOCUS_STATUS`  [filter]
      - watch list status in December 2025: SFF on the list, SFF Candidate not picked, blank neither
      - WATCH: fill not yet measured
 - `PROBLEM_FACILITIES_SFFS_CANDIDATES_ONE_STAR`  [filter]
      - Yes if the home is on the watch list, a candidate, or rated one star; otherwise No
      - WATCH: fill not yet measured
 - `PROCESSING_DATE`  [date]
      - the date Medicare cut this snapshot; every row says 2025-12-01

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation at one home on one survey
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME, measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `SURVEY_DATE`  [date]
      - the day inspectors visited and wrote this citation
      - WATCH: runs 2017-03-23 to 2026-05-20 but real coverage is 2023-2026; 273 rows in 2017 against 121,925 in 2024
 - `SCOPE_SEVERITY_CODE`  [measure]
      - letter grade for how bad and how widespread the problem was; D is most common, then E, F, G, J

---

## 45) Check whether nursing home inspectors mostly show up in the last weeks before the deadline, no matter how bad the home is.  `H-111` grade B
   - If visit gaps pile up at one fixed length for good and bad homes alike, the calendar sets the visit, not the risk. Bad homes would then wait as long as clean ones.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation at one home on one survey
connects: nothing. One table, no join
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `SURVEY_DATE`  [date]
      - the day inspectors visited and wrote this citation
      - WATCH: a clean survey leaves no row, so its date is missing and the gap across it reads double; real coverage 2023-2026
 - `INSPECTION_CYCLE`  [filter]
      - which of the home's last three standard inspections this was: 1, 2 or 3
      - WATCH: fill not yet measured
 - `SURVEY_TYPE`  [filter]
      - kind of survey; every row in this table says Health
      - WATCH: fill not yet measured; check values first
 - `STANDARD_DEFICIENCY`  [filter]
      - Y if the citation came from a scheduled standard inspection, N if not
      - WATCH: check its values first
 - `STATE`  [filter]
      - two-letter state the home sits in

---

## 46) Find the nursing homes that get the exact same two or three citations at the same letter grade on every single visit.  `WN-150` grade B
   - A record that never varies says more about the inspector's checklist than about the home. Clusters of these in one state or district point at the inspection office.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation at one home on one survey
connects: nothing. One table, no join
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `SURVEY_DATE`  [date]
      - the day inspectors visited and wrote this citation
      - WATCH: runs 2017-03-23 to 2026-05-20 but real coverage is 2023-2026; 273 rows in 2017 against 121,925 in 2024
 - `DEFICIENCY_TAG_NUMBER`  [measure]
      - the number of the specific rule the home broke
      - WATCH: fill not yet measured; a few tags are cited almost everywhere, so weight by how rare the tag is in that state
 - `SCOPE_SEVERITY_CODE`  [measure]
      - letter grade for how bad and how widespread the problem was; D is most common, then E, F, G, J
      - WATCH: fill not yet measured
 - `DEFICIENCY_CATEGORY`  [label]
      - broad family of the broken rule in words, such as Resident Rights Deficiencies
 - `STATE`  [filter]
      - two-letter state the home sits in

---

## 47) Some nursing homes with no chain name on file look exactly like one chain's homes on staffing, turnover and citations, so find them.  `WN-154` grade B
   - A lookalike is a lead on shared management that the official chain label does not show. It is a lead only, not proof of common ownership.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, current snapshot
connects: nothing. One table, no join
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `CHAIN_NAME`  [label]
      - name of the chain the home says it belongs to
      - WATCH: blank on 4,221 of 14,700 homes (28.7%); includes hospital systems; name matching gave 5 of 15 false positives
 - `CHAIN_ID`  [filter]
      - Medicare's number for the chain; use this, not the name, to group a chain
 - `NUMBER_OF_FACILITIES_IN_CHAIN`  [measure]
      - how many homes that chain runs in total
 - `STATE`  [filter]
      - two-letter state the home sits in; hold it fixed or clusters are just maps
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds Medicare has approved at this home
 - `REPORTED_NURSE_AIDE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - nurse aide hours worked per resident per day, as the home reported
      - WATCH: fill not yet measured
 - `REPORTED_LPN_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - licensed practical nurse hours worked per resident per day, as reported
      - WATCH: fill not yet measured
 - `REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - registered nurse hours worked per resident per day, as the home reported
      - WATCH: fill not yet measured
 - `REGISTERED_NURSE_HOURS_PER_RESIDENT_PER_DAY_ON_THE_WEEKEND`  [measure]
      - registered nurse hours per resident per day on Saturdays and Sundays
      - WATCH: fill not yet measured
 - `NURSING_CASE_MIX_INDEX`  [measure]
      - score for how sick the residents are, so staffing can be compared fairly
      - WATCH: fill not yet measured
 - `TOTAL_NURSING_STAFF_TURNOVER`  [measure]
      - share of all nursing staff who left during the year
      - WATCH: fill not yet measured
 - `REGISTERED_NURSE_TURNOVER`  [measure]
      - share of registered nurses who left during the year
      - WATCH: fill not yet measured
 - `TOTAL_WEIGHTED_HEALTH_SURVEY_SCORE`  [measure]
      - Medicare's points total for the home's recent inspections; higher means a worse record
      - WATCH: fill not yet measured
 - `TOTAL_AMOUNT_OF_FINES_IN_DOLLARS`  [measure]
      - dollars of federal fines against the home in the recent window
      - WATCH: fill not yet measured

---

## 48) Take the roughly 684 nursing homes that told Medicare a private-equity firm or a real-estate trust owns them, and compare them with similar homes that did not say so.  `N3` grade C
   - If flagged homes show fewer nurse hours, more turnover and more fines than matched neighbors, investor ownership shows up in care. A tie says little, because unflagged homes may be investor-owned too.

**LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP**
one row = one enrollment x one owner x one role
connects: ENROLLMENT_ID matches ENROLLMENT_ID on HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS; 288,550 of 295,083 rows join
 - `ENROLLMENT_ID`  [join]
      - Medicare's id for one home's sign-up to bill Medicare; the only link out of this file
      - WATCH: this file has no CCN of its own
 - `PRIVATE_EQUITY_COMPANY_OWNER`  [filter]
      - Y if the home reported this owner is a private-equity company
      - WATCH: Y on 196 rows, 97 enrollments (0.67%); blank on 198,546 rows (67%); blank is unknown, never no
 - `REIT_OWNER`  [filter]
      - Y if the home reported this owner is a real-estate investment trust
      - WATCH: Y on 587 enrollments; blank on 198,546 rows (67%); blank is unknown, never no
 - `ORGANIZATION_NAME_OWNER`  [label]
      - the owner's company name as written on the form
 - `ASSOCIATE_ID_OWNER`  [label]
      - Medicare's id number for the owner itself
 - `ROLE_TEXT_OWNER`  [filter]
      - what the owner does at the home in words, such as owner or managing party
 - `PERCENTAGE_OWNERSHIP`  [measure]
      - what percent of the home this owner holds
      - WATCH: filled on 96,823 of 295,083 rows
 - `ASSOCIATION_DATE_OWNER`  [date]
      - when this owner's tie to the home began
      - WATCH: free text in mixed formats with 1800 placeholder dates; current owners only, no purchase date

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS**
one row = one Medicare enrollment of one skilled nursing facility
connects: ENROLLMENT_ID matches ENROLLMENT_ID on FED_CMS_SNF_OWNERSHIP; CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME, measured 100%
 - `ENROLLMENT_ID`  [join]
      - Medicare's id for one home's sign-up to bill Medicare
 - `CCN`  [join]
      - Medicare's six-character id for the nursing home building
 - `PROPRIETARY_NONPROFIT`  [filter]
      - one-letter owner kind: P for profit, N nonprofit; D also appears, meaning not given here

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, current snapshot
connects: CMS_CERTIFICATION_NUMBER_CCN matches CCN on the enrollments table, and the same column on the deficiencies and penalties tables, measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `STATE`  [filter]
      - two-letter state the home sits in; used to pick matched peers
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - how many beds Medicare has approved; used to pick peers of the same size
 - `OWNERSHIP_TYPE`  [filter]
      - who owns it in words, such as For profit - Corporation; used to pick peers
 - `OVERALL_RATING`  [measure]
      - Medicare's overall star rating for the home, one to five stars
      - WATCH: fill not yet measured
 - `STAFFING_RATING`  [measure]
      - Medicare's star rating for staffing alone, one to five stars
      - WATCH: fill not yet measured
 - `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`  [measure]
      - all nursing staff hours worked per resident per day, as the home reported
      - WATCH: fill not yet measured
 - `TOTAL_NURSING_STAFF_TURNOVER`  [measure]
      - share of all nursing staff who left during the year
      - WATCH: fill not yet measured

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES**
one row = one health citation at one home on one survey
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME, measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `SURVEY_DATE`  [date]
      - the day inspectors visited and wrote this citation
      - WATCH: runs 2017-03-23 to 2026-05-20 but real coverage is 2023-2026; 273 rows in 2017 against 121,925 in 2024
 - `SCOPE_SEVERITY_CODE`  [measure]
      - letter grade for how bad and how widespread the problem was; D is most common, then E, F, G, J

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES**
one row = one fine or payment denial against one home
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME, measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's six-character id for the nursing home building, same on every home table
 - `PENALTY_DATE`  [date]
      - the day the fine or payment denial was imposed
      - WATCH: starts 2023-06-17; the record may belong to a prior owner
 - `PENALTY_TYPE`  [filter]
      - Fine, or Payment Denial meaning Medicare stopped paying for new residents
 - `FINE_AMOUNT`  [measure]
      - dollars of the fine charged to the home

---

# MONEY

## 49) Check whether big investment managers loaded up on a company's stock in the quarter right before that company won a federal contract.  `W51` grade B
   - If share counts rise before awards more than in ordinary quarters, someone saw the contract coming. If not, contract wins are not visible in advance in quarterly holdings.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS**
one row = one stock position on one manager's quarterly filing
connects: ACCESSION_NUMBER matches ACCESSION_NUMBER on FINANCE__FED_SEC_13F_SUBMISSIONS; CUSIP matches CUSIP on FED_SEC_13F_SECURITIES_LIST; NAMEOFISSUER matches RECIPIENT_PARENT_NAME on the contract tables by name, two or more words only
 - `ACCESSION_NUMBER`  [join]
      - the SEC's receipt number for one filing; ties each holding to its filing
      - WATCH: fill not yet measured, unprofiled view
 - `NAMEOFISSUER`  [join]
      - name of the company whose stock is held, as the manager typed it
      - WATCH: name match only; multi-word matches held up 92% of the time, single-word 8%
 - `CUSIP`  [join]
      - nine-character code for the stock itself, not for the company
      - WATCH: there is no table linking it to a company id
 - `VALUE_USD`  [measure]
      - dollar value of the position on the report date
 - `SSHPRNAMT`  [measure]
      - how many shares, or how much bond face value, the manager holds
 - `PUTCALL`  [filter]
      - Put or Call if the position is an option; blank for plain shares

**LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS**
one row = one 13F filing by one manager
connects: ACCESSION_NUMBER matches ACCESSION_NUMBER on FINANCE__FED_SEC_13F_HOLDINGS; gives the quarter
 - `ACCESSION_NUMBER`  [join]
      - the SEC's receipt number for one filing
 - `CIK`  [label]
      - the SEC's id number for the investment manager who filed; 16,205 managers
 - `PERIODOFREPORT`  [date]
      - the quarter-end date the holdings list describes
      - WATCH: the load missed 7 of 53 source zips; count filings per quarter before reading a change as real
 - `FILING_DATE`  [date]
      - the day the manager sent the filing to the SEC

**LIBRARY_RAW.LANDING.FED_SEC_13F_SECURITIES_LIST**
one row = one line of the SEC's official 13F securities list
connects: CUSIP matches CUSIP on FINANCE__FED_SEC_13F_HOLDINGS; dedupe the list on CUSIP first
 - `CUSIP`  [join]
      - nine-character code for the stock on the official list
      - WATCH: 25,333 lines but 23,277 distinct, about 2,000 exact repeats
 - `ISSUER_NAME`  [label]
      - the SEC's official spelling of the company name for that stock
 - `STATUS`  [filter]
      - coded value, look at distinct values first
      - WATCH: fill not yet measured

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK**
one row = one EPA facility matched to a corporate parent
connects: PARENT_LEGAL_NAME matches NAMEOFISSUER on FINANCE__FED_SEC_13F_HOLDINGS by name; PARENT_UEI matches RECIPIENT_PARENT_UEI on the contract tables
 - `PARENT_LEGAL_NAME`  [join]
      - legal name of the parent company that owns the facility
 - `PARENT_CIK`  [label]
      - the SEC's id number for the parent company
      - WATCH: 2.25% filled, 705 distinct
 - `PARENT_UEI`  [join]
      - the government's contractor id for the parent company
      - WATCH: 8.07% filled, 389,581 blank strings

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: RECIPIENT_PARENT_NAME matches NAMEOFISSUER on FINANCE__FED_SEC_13F_HOLDINGS by name; RECIPIENT_PARENT_UEI matches PARENT_UEI on ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK
 - `RECIPIENT_NAME`  [label]
      - name of the company that got the contract money
      - WATCH: fill not yet measured
 - `RECIPIENT_PARENT_NAME`  [join]
      - name of the parent company that owns the recipient
      - WATCH: fill not yet measured
 - `RECIPIENT_UEI`  [label]
      - the government's contractor id for the recipient
      - WATCH: fill not yet measured
 - `RECIPIENT_PARENT_UEI`  [join]
      - the government's contractor id for the recipient's parent company
      - WATCH: fill not yet measured
 - `ACTION_DATE`  [date]
      - the day this contract action was signed
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this action
      - WATCH: signed number; filter to values above zero or totals read wrong

---

## 50) See whether members of Congress buy and sell stock in the days right around their own recorded floor votes.  `W52` grade B
   - If trades bunch near votes more than chance would give, members may be trading on what they know is coming. Votes happen most weeks, so a miss is a real possibility.

**LIBRARY_RAW.LANDING.FED_HOUSE_PTR**
one row = one trade line parsed from a House periodic transaction report PDF
connects: FILER_LAST + FILER_FIRST + STATE_DISTRICT match NAME_LAST + NAME_FIRST + LAST_STATE + LAST_DISTRICT on POLITICS__MEMBER_CROSSWALK by name
 - `FILER_LAST`  [join]
      - last name of the House member who filed the report
      - WATCH: no member id on this table; name match only
 - `FILER_FIRST`  [join]
      - first name of the House member who filed the report
 - `STATE_DISTRICT`  [join]
      - the member's state and district number in one value
 - `TRANSACTION_DATE`  [date]
      - the day the stock was bought or sold
      - WATCH: fill not yet measured
 - `TRANSACTION_TYPE`  [filter]
      - coded value, look at distinct values first; says buy or sell
 - `TICKER`  [label]
      - stock symbol of what was traded
 - `AMOUNT_RANGE`  [measure]
      - dollar bracket for the trade; no exact figure is ever reported
      - WATCH: a range only, so any total is a bounded estimate
 - `IS_SCAN`  [filter]
      - marks a report filed as a scanned image instead of typed text
      - WATCH: scanned reports could not be read and carry no trade lines
 - `FILING_YEAR`  [date]
      - the year the report was filed, 2021 to 2026

**LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR**
one row = one trade line on a Senate periodic transaction report
connects: FILER_LAST_CLEAN matches NAME_LAST on POLITICS__MEMBER_CROSSWALK; of 62 filers, 26 land clean, 29 ambiguous, 7 missed
 - `FILER_LAST_CLEAN`  [join]
      - tidied last name of the senator who filed
      - WATCH: last name alone is ambiguous for 29 of 62 filers; Scott matches two sitting senators; do not use SENATOR, it holds the word Senator on 98 rows
 - `TRANSACTION_DATE`  [date]
      - the day the stock was bought or sold
      - WATCH: 98.54% filled
 - `TICKER`  [label]
      - stock symbol of what was traded
      - WATCH: 100 blank strings
 - `TRANSACTION_TYPE`  [filter]
      - what happened in words: Purchase, Sale (Full), Sale (Partial) or Exchange
 - `AMOUNT_RANGE`  [measure]
      - dollar bracket for the trade, such as $1,001 - $15,000
      - WATCH: a range only, so any total is a bounded estimate
 - `FILING_ID`  [label]
      - the Senate's id for the report this trade line came from

**LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK**
one row = one member of Congress, all of history, with every id
connects: NAME_LAST + NAME_FIRST + LAST_STATE + LAST_DISTRICT match the House filer columns; NAME_LAST matches FILER_LAST_CLEAN; ICPSR matches ICPSR on POLITICS__VOTEVIEW_VOTES
 - `NAME_LAST`  [join]
      - last name of the member of Congress
 - `NAME_FIRST`  [join]
      - first name of the member of Congress
 - `LAST_STATE`  [join]
      - state the member most recently represented
 - `LAST_DISTRICT`  [join]
      - House district number the member most recently held
 - `LAST_TERM_TYPE`  [filter]
      - most recent office: rep for House, sen for Senate
 - `ICPSR`  [join]
      - the id number political scientists give each member; it is how the vote tables name people
      - WATCH: 96.12% filled
 - `BIOGUIDE`  [label]
      - Congress's own official id for the member

**LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES**
one row = one member's vote on one roll call
connects: ICPSR matches ICPSR on POLITICS__MEMBER_CROSSWALK; CONGRESS + CHAMBER + ROLLNUMBER match the same three columns on POLITICS__VOTEVIEW_ROLLCALLS
 - `ICPSR`  [join]
      - the id number for the member who cast the vote; 639 distinct
 - `CONGRESS`  [join]
      - which two-year Congress the vote happened in, as a number
 - `CHAMBER`  [join]
      - which chamber held the vote: House or Senate
 - `ROLLNUMBER`  [join]
      - the vote's running number inside that Congress and chamber
 - `CAST_CODE`  [filter]
      - how the member voted as a number: 1 yea, 6 nay, 9 not voting, 7 present
 - `VOTE_POSITION`  [filter]
      - how the member voted in words: yea, nay, not_voting or present

**LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS**
one row = one roll-call vote
connects: CONGRESS + CHAMBER + ROLLNUMBER match the same three columns on POLITICS__VOTEVIEW_VOTES; gives VOTE_DATE
 - `CONGRESS`  [join]
      - which two-year Congress the vote happened in, as a number
 - `CHAMBER`  [join]
      - which chamber held the vote: House or Senate
 - `ROLLNUMBER`  [join]
      - the vote's running number inside that Congress and chamber
 - `VOTE_DATE`  [date]
      - the day the floor vote was held, 2023-01-03 to 2026-06-25
 - `BILL_NUMBER`  [label]
      - the bill the vote was about, such as a House or Senate bill number
      - WATCH: no subject code; tying a vote to an industry needs hand-coding
 - `VOTE_QUESTION`  [label]
      - what was being decided in words, such as passage or an amendment
 - `VOTE_DESC`  [label]
      - short written description of the vote

---

## 51) Find the ZIP codes whose residents write the most campaign checks per household while the fewest federal contract and grant dollars come back to that ZIP.  `W53` grade B
   - It shows which places fund politics without seeing federal money land locally. If giving and getting rise together, campaign money and contractor offices share an address, which is its own finding.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one itemized contribution from one person to one committee
connects: left 5 of ZIP_CODE matches left 5 of RECIPIENT_ZIP_4_CODE on contracts, RECIPIENT_ZIP_CODE on assistance, and ZIP_CODE on FINANCE__FED_IRS_SOI
 - `ZIP_CODE`  [join]
      - ZIP code of the donor's mailing address
      - WATCH: mixes 5 and 9 digit forms, take the left 5; 321,021 blank strings; a ZIP is a place, not a payer
 - `TRANSACTION_AMT`  [measure]
      - dollars the person gave in this one contribution
 - `TRANSACTION_DATE`  [date]
      - the day the contribution was made
      - WATCH: 99.98% filled; junk end dates run 0031-04-10 to 9206-07-02
 - `TRANSACTION_TYPE`  [filter]
      - code for the kind of money movement; 15 is a plain contribution, 15E is an earmarked pass-through
      - WATCH: leave 15E in and the same dollar can count twice
 - `STATE`  [filter]
      - two-letter state of the donor's mailing address

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: left 5 of RECIPIENT_ZIP_4_CODE matches left 5 of ZIP_CODE on FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
 - `RECIPIENT_ZIP_4_CODE`  [join]
      - ZIP plus four of the contractor's office address
      - WATCH: fill not yet measured; it is where the office sits, not where the work lands
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this action
      - WATCH: fill not yet measured
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the federal budget year the action fell in

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 to FY2026 (20 tables, same columns)**
one row = one grant, loan or direct-payment transaction
connects: RECIPIENT_ZIP_CODE matches left 5 of ZIP_CODE on FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
 - `RECIPIENT_ZIP_CODE`  [join]
      - ZIP code of the recipient's office address
      - WATCH: fill not yet measured; it is where the office sits, not where the benefit lands
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this action
      - WATCH: exactly $0.00 on 11,788,945 loan rows; a total on this column alone drops 47% of rows
 - `FACE_VALUE_OF_LOAN`  [measure]
      - the size of the loan in dollars; where loan money actually shows up
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - code for the kind of aid; 07 and 08 are loans. Source: public USAspending code list, not the handbook
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the federal budget year the action fell in

**LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI**
one row = one ZIP by income bracket, tax return totals
connects: ZIP_CODE matches left 5 of ZIP_CODE on FINANCE__FED_FEC_INDIV_CONTRIBUTIONS; the per-return denominator
 - `ZIP_CODE`  [join]
      - five-digit ZIP code the tax returns came from; 29,922 distinct
 - `N_RETURNS`  [measure]
      - how many tax returns were filed from this ZIP in this income bracket
 - `AGI`  [measure]
      - total income reported on those returns, after adjustments
 - `AGI_STUB`  [filter]
      - income bracket number, 1 to 6; sum across brackets to get the whole ZIP
 - `TAX_YEAR`  [date]
      - the tax year of the numbers
      - WATCH: 2016 only; a fixed denominator, not a matching year

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP-area to county pairing
connects: ZCTA5 matches the five-digit ZIP from the other tables; rolls up to COUNTY_FIPS
 - `ZCTA5`  [join]
      - the Census version of a five-digit ZIP code area
 - `COUNTY_FIPS`  [join]
      - five-digit federal county code; 3,266 distinct

---

## 52) Check whether the same few companies collect the federal contract work in the same county after every declared disaster.  `W55` grade B
   - One firm winning after most storms in a county, far above its quiet-year share, points to a standing lock on disaster money. Changing winners would say the work is open.

**LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS**
one row = one disaster by one designated area (county)
connects: FIPSSTATECODE || FIPSCOUNTYCODE matches PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on the contract tables
 - `DISASTERNUMBER`  [measure]
      - FEMA's number for one declared disaster
      - WATCH: 70,402 rows cover 5,264 disasters; count disasters with a distinct on this column
 - `DECLARATIONDATE`  [date]
      - the day the disaster was officially declared
      - WATCH: ISO text with a Z suffix, not a date type
 - `INCIDENTTYPE`  [filter]
      - kind of disaster in words, such as hurricane, flood or fire
 - `INCIDENTBEGINDATE`  [date]
      - the day the storm or event itself started
      - WATCH: ISO text with a Z suffix, not a date type
 - `FIPSSTATECODE`  [join]
      - two-digit federal code for the state
      - WATCH: fill not yet measured
 - `FIPSCOUNTYCODE`  [join]
      - three-digit federal code for the county inside the state
      - WATCH: fill not yet measured
 - `DESIGNATEDAREA`  [label]
      - name of the county or area covered, in words

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE matches FIPSSTATECODE || FIPSCOUNTYCODE on FED_FEMA_DISASTER_DECLARATIONS, with ACTION_DATE after DECLARATIONDATE
 - `RECIPIENT_UEI`  [label]
      - the government's contractor id for the company paid
      - WATCH: one firm can appear under several of these
 - `RECIPIENT_NAME`  [label]
      - name of the company that was paid on the contract
 - `RECIPIENT_PARENT_UEI`  [label]
      - the government's contractor id for the company's parent
      - WATCH: fill not yet measured
 - `ACTION_DATE`  [date]
      - the day this contract action was signed
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this action
      - WATCH: signed number; filter above zero
 - `AWARDING_SUB_AGENCY_NAME`  [filter]
      - the office that awarded the contract, such as FEMA; narrows to disaster work
      - WATCH: fill not yet measured
 - `NATIONAL_INTEREST_ACTION`  [filter]
      - tag naming the specific disaster or emergency the contract was for
      - WATCH: fill not yet measured
 - `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`  [join]
      - five-digit federal code of the county where the work was done
      - WATCH: measured on FY2024 only: filled on 93% of rows

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS**
one row = one storm event in one county or forecast zone
connects: STATE_FIPS || CZ_FIPS where CZ_TYPE = 'C' matches the same five-digit county code
 - `YEAR`  [date]
      - the year the storm happened, 1996 to 2025
 - `EVENT_TYPE`  [filter]
      - kind of storm in words, such as tornado, hail or flash flood
 - `CZ_TYPE`  [filter]
      - what the area code means: C county, Z forecast zone, M marine
      - WATCH: only C rows map to a county
 - `STATE_FIPS`  [join]
      - two-digit federal code for the state
 - `CZ_FIPS`  [join]
      - county code, or forecast-zone code when CZ_TYPE is not C
      - WATCH: not a county code unless CZ_TYPE is C
 - `DAMAGE_PROPERTY`  [measure]
      - estimated property damage from the storm; the optional severity measure

---

## 53) When the bank regulator slaps a formal order on a bank, check whether that bank keeps writing mortgages in the very same counties as before.  `W56` grade B
   - If the county footprint and loan volume do not move after an order, the order did not bite. If lending shrinks or moves, enforcement has real effect.

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS**
one row = one FDIC enforcement order
connects: CERT_NUMBER matches CERT on FINANCE__FED_FDIC_BANK_DATA and FDIC_CERT on FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS
 - `CERT_NUMBER`  [join]
      - the FDIC's certificate number for the bank; count banks by this, never by name
      - WATCH: 97.86% filled
 - `ORDER_DATE`  [date]
      - the day the order was issued
 - `ORDER_TYPE`  [filter]
      - kind of order in words, such as Cease and Desist / Consent Orders or Assessment of Civil Money Penalty
 - `TERMINATION_DATE`  [date]
      - the day the order was lifted
      - WATCH: 20.94% filled
 - `BANK_RSSD_ID`  [label]
      - the Federal Reserve's id number for the same bank
 - `INSTITUTION_NAME`  [label]
      - the bank's name as written on the order
      - WATCH: National Association names are one charter; count by CERT_NUMBER

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA**
one row = one FDIC-insured institution
connects: CERT matches CERT_NUMBER on the orders table; LEI matches LEI on the HMDA_LAR year tables; CERT matches RESPONDENT_ID on HOUSING__FED_CFPB_HMDA_HISTORIC, split by AGENCY_CODE, measured 70%
 - `CERT`  [join]
      - the FDIC's certificate number for the bank
 - `LEI`  [join]
      - the 20-character global company id that the newer mortgage files use for the lender
      - WATCH: 8.09% filled, 2,236 distinct
 - `NAME`  [label]
      - the bank's name as the FDIC records it
 - `RSSDID`  [label]
      - the Federal Reserve's id number for the bank

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS**
one row = one branch in one survey year
connects: FDIC_CERT matches CERT_NUMBER on JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS; gives the branch-county footprint
 - `FDIC_CERT`  [join]
      - the FDIC's certificate number for the bank that owns the branch
 - `SURVEY_YEAR`  [date]
      - the year of the annual branch deposit count, 1994 to 2025
 - `BRANCH_STATE_COUNTY_FIPS`  [filter]
      - five-digit federal code of the county where the branch stands
 - `BRANCH_DEPOSITS_THOUSANDS`  [measure]
      - deposits held at that branch, in thousands of dollars

**LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 to 2024 (7 tables, same columns)**
one row = one mortgage application
connects: LEI matches LEI on FINANCE__FED_FDIC_BANK_DATA
 - `LEI`  [join]
      - the 20-character global company id of the lender that took the application
      - WATCH: fill not yet measured
 - `STATE_CODE`  [filter]
      - state where the house being mortgaged sits
      - WATCH: fill not yet measured
 - `COUNTY_CODE`  [filter]
      - federal county code of the property; the finest place available along with tract, there is no ZIP
      - WATCH: fill not yet measured
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
      - WATCH: 2018 has 1,961 placeholder rows with '-1' and 2019 has 21; filter them first
 - `LOAN_AMOUNT`  [measure]
      - dollars the applicant asked to borrow
 - `ACTIVITY_YEAR`  [date]
      - the calendar year of the application

**LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC**
one row = one mortgage application, old layout
connects: RESPONDENT_ID, split by AGENCY_CODE, matches CERT on FINANCE__FED_FDIC_BANK_DATA, measured 70%
 - `RESPONDENT_ID`  [join]
      - the lender's id as its regulator assigned it; only unique together with AGENCY_CODE
      - WATCH: not a real id on its own; pair with AGENCY_CODE
 - `AGENCY_CODE`  [join]
      - number for which regulator the lender reports to; look at distinct values first
 - `STATE_CODE`  [filter]
      - federal state code of the property
      - WATCH: 98.4% filled; unpadded text
 - `COUNTY_CODE`  [filter]
      - three-digit county part of the property's federal code
      - WATCH: 98.17% filled; unpadded text; 19,331 denial rows have a null county
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
 - `AS_OF_YEAR`  [date]
      - the calendar year of the application; the only date on the table
      - WATCH: fact helper shows 2015-2017; a probe file says 2007-2017

---

## 54) When a county's local bank fails or gets swallowed by another bank, check whether government-backed small-business loans in that county dry up afterward.  `W58` grade B
   - If loan approvals fall and stay down where the vanished bank was big, losing a local bank costs small businesses their credit. Steady approvals would say other lenders filled the gap.

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_LOANS**
one row = one SBA-guaranteed loan approval
connects: PROJECT_COUNTY + PROJECT_STATE match COUNTYNAME + STATE on FED_CENSUS_COUNTY_2020 by name
 - `PROJECT_COUNTY`  [join]
      - name of the county where the business is, in words, not a code
      - WATCH: county names repeat across states and spellings vary; unmatched share not yet measured
 - `PROJECT_STATE`  [join]
      - two-letter state where the business is
 - `APPROVAL_DATE`  [date]
      - the day the loan was approved, 1990-10-01 to 2026-03-31
 - `APPROVAL_FISCAL_YEAR`  [date]
      - the federal budget year the loan was approved in
 - `GROSS_APPROVAL_AMOUNT`  [measure]
      - total dollars of the loan that was approved
 - `LENDER_NAME`  [label]
      - name of the bank that made the loan
 - `LENDER_STATE`  [filter]
      - two-letter state of the bank that made the loan

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA**
one row = one FDIC-insured institution, open or closed
connects: CERT matches FDIC_CERT on ECONOMICS__FED_FDIC_FAILED_BANKS and FDIC_CERT on FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS
 - `CERT`  [join]
      - the FDIC's certificate number for the bank
 - `FIPS`  [join]
      - five-digit federal code of the bank's home county; 2,980 distinct
 - `ENDEFYMD`  [date]
      - the day the bank stopped existing under its own charter
      - WATCH: 84.62% filled
 - `SUCCESSOR_CERT`  [filter]
      - certificate number of the bank that took this one over
      - WATCH: what it holds for a bank still open has not been checked; confirm before calling every filled row a merger
 - `ACTIVE`  [filter]
      - 1 if the bank is still open, 0 if it is gone
 - `NAME`  [label]
      - the bank's name as the FDIC records it

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS**
one row = one bank failure
connects: FDIC_CERT matches CERT on FINANCE__FED_FDIC_BANK_DATA; that is how a failure gets a county
 - `FDIC_CERT`  [join]
      - the FDIC's certificate number for the failed bank
 - `FAIL_DATE`  [date]
      - the day regulators closed the bank
 - `ACQUIRING_INSTITUTION`  [label]
      - name of the bank that took over the failed one
 - `CITY`  [label]
      - city where the failed bank was based
 - `STATE_ABBR`  [filter]
      - two-letter state where the failed bank was based
 - `FIPS`  [join]
      - meant to be the county code, but it holds nothing
      - WATCH: blank string on all 3,584 rows; do not use

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS**
one row = one branch in one survey year
connects: FDIC_CERT matches CERT on FINANCE__FED_FDIC_BANK_DATA; gives branch counties the year before the end date
 - `FDIC_CERT`  [join]
      - the FDIC's certificate number for the bank that owns the branch
 - `SURVEY_YEAR`  [date]
      - the year of the annual branch deposit count, 1994 to 2025
 - `BRANCH_STATE_COUNTY_FIPS`  [join]
      - five-digit federal code of the county where the branch stands
 - `SIMS_ACQUIRED_DATE`  [date]
      - the day the branch came to its current bank through a takeover
      - WATCH: 50.41% filled
 - `HOLDING_COMPANY_NAME`  [label]
      - name of the parent company that owns the bank
      - WATCH: 87.37% filled

**LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020**
one row = one county, name and FIPS
connects: COUNTYNAME + STATE match PROJECT_COUNTY + PROJECT_STATE on ECONOMICS__FED_SBA_LOANS; STATEFP || COUNTYFP gives the county code
 - `STATE`  [join]
      - two-letter postal abbreviation of the county's state
      - WATCH: fill not yet measured
 - `STATEFP`  [join]
      - two-digit federal code for the state
 - `COUNTYFP`  [join]
      - three-digit federal code for the county inside the state
 - `COUNTYNAME`  [join]
      - the county's name spelled out in words
      - WATCH: fill not yet measured

---

## 55) Find the pairs of next-door counties where mortgage applicants on one side of the line get turned down far more often than on the other.  `W59` grade B
   - A gap that survives matching on income and loan purpose points at place, not at who is applying. Without credit scores in the file it can still be credit mix.

**LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 to 2024 (7 tables, same columns)**
one row = one mortgage application
connects: COUNTY_CODE matches GEOID on REFERENCE__CENSUS_CB_COUNTY
 - `COUNTY_CODE`  [join]
      - five-digit federal county code of the property
      - WATCH: fill not yet measured
 - `STATE_CODE`  [filter]
      - state where the house being mortgaged sits
      - WATCH: fill not yet measured
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
      - WATCH: 2018 has 1,961 placeholder rows with '-1' and 2019 has 21; filter them
 - `INCOME`  [filter]
      - the applicant's yearly income as reported on the application
 - `LOAN_PURPOSE`  [filter]
      - what the loan was for: 1 buy a home, 2 home improvement, 31 refinance, 32 cash-out refinance, 4 other, 5 not applicable. Source: public HMDA code list, not the handbook
 - `LOAN_AMOUNT`  [measure]
      - dollars the applicant asked to borrow
 - `ACTIVITY_YEAR`  [date]
      - the calendar year of the application

**LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC**
one row = one mortgage application, old layout
connects: lpad(STATE_CODE,2) || lpad(COUNTY_CODE,3) matches GEOID on REFERENCE__CENSUS_CB_COUNTY
 - `STATE_CODE`  [join]
      - federal state code of the property
      - WATCH: 98.4% filled; unpadded text, pad to 2 before joining
 - `COUNTY_CODE`  [join]
      - three-digit county part of the property's federal code
      - WATCH: 98.17% filled; unpadded text, pad to 3; 19,331 denial rows have a null county and fall out
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
 - `APPLICANT_INCOME_000S`  [filter]
      - the applicant's yearly income in thousands of dollars
 - `LOAN_PURPOSE`  [filter]
      - what the loan was for: 1 buy a home, 2 home improvement, 3 refinance. Source: public HMDA code list, not the handbook
 - `AS_OF_YEAR`  [date]
      - the calendar year of the application
      - WATCH: verified span is 2015-2017 for this table

**LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY**
one row = one county with its boundary shape
connects: GEOMETRY touching GEOMETRY on the same table gives neighbor pairs; GEOID matches COUNTY_CODE on the mortgage tables
 - `GEOID`  [join]
      - five-digit federal code that names one county
 - `NAME`  [label]
      - the county's name spelled out in words
 - `STUSPS`  [label]
      - two-letter postal abbreviation of the county's state
 - `GEOMETRY`  [join]
      - the county's outline on the map; two counties that touch are neighbors
      - WATCH: no ready-made neighbor table exists; the pairs must be computed

---

## 56) For banks that failed after 2012, check whether customer complaints to the federal consumer watchdog climbed in the year before the bank went under.  `W60` grade B
   - If complaints rise first, the complaint file is an early warning for bank trouble. If failed banks are not in the file at all, it does not reach small failing banks and the question ends.

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS**
one row = one bank failure
connects: BANK_NAME matches COMPANY on CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS by name, multi-word names only; FDIC_CERT matches FDIC_CERT on FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS
 - `BANK_NAME`  [join]
      - name of the bank that failed, as written
      - WATCH: name match only; single-word matches were 8% real, use two or more words and check the state
 - `FDIC_CERT`  [join]
      - the FDIC's certificate number for the failed bank
 - `FAIL_DATE`  [date]
      - the day regulators closed the bank
      - WATCH: most failures cluster 2008-2012, before complaints start; count after 2012 not yet measured
 - `STATE_ABBR`  [filter]
      - two-letter state where the failed bank was based
 - `TOTAL_ASSETS_THOUSANDS`  [measure]
      - the bank's size at failure, in thousands of dollars
 - `ACQUIRING_INSTITUTION`  [label]
      - name of the bank that took over the failed one

**LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS**
one row = one consumer complaint
connects: COMPANY matches BANK_NAME on ECONOMICS__FED_FDIC_FAILED_BANKS, or HOLDING_COMPANY_NAME on FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS, by name
 - `COMPANY`  [join]
      - name of the company the customer complained about; 8,088 distinct
      - WATCH: 77% of the 17.17M complaints are three credit bureaus; banks are a minority
 - `DATE_RECEIVED`  [date]
      - the day the watchdog received the complaint
      - WATCH: starts 2011-12-01
 - `RECEIVED_MONTH`  [date]
      - the month the complaint was received; the bucket for counting
 - `PRODUCT`  [filter]
      - what the complaint was about in words, such as credit reporting or debt collection
 - `STATE`  [filter]
      - two-letter state of the customer who complained

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS**
one row = one branch in one survey year
connects: FDIC_CERT matches FDIC_CERT on ECONOMICS__FED_FDIC_FAILED_BANKS; HOLDING_COMPANY_NAME then matches COMPANY on the complaints table
 - `FDIC_CERT`  [join]
      - the FDIC's certificate number for the bank that owns the branch
 - `INSTITUTION_NAME`  [label]
      - the bank's name as written in the branch survey
 - `HOLDING_COMPANY_NAME`  [join]
      - name of the parent company that owns the bank; a second name to try
      - WATCH: 87.37% filled

---

## 57) An auditor warns that a grant recipient may not survive the year, and the government hands it a new grant anyway.  `W61` grade B
   - It would mean agencies are not reading the audits they require. Public money would be flowing to organizations already flagged as likely to fold.

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT**
one row = one federal single-audit report for one organization and one year
connects: AUDITEE_UEI matches RECIPIENT_UEI on the ASSISTANCE_FY tables; keep grants with ACTION_DATE after FAC_ACCEPTED_DATE
 - `AUDITEE_UEI`  [join]
      - the federal id number of the organization that was audited
 - `AUDITEE_EIN`  [label]
      - the tax id number of the organization that was audited
 - `AUDIT_YEAR`  [date]
      - the year the audit report covers
 - `IS_GOING_CONCERN_INCLUDED`  [filter]
      - whether the auditor doubted the organization would survive: Yes, No, or GSA_MIGRATION
      - WATCH: Handbook says fill not measured and count distinct values first. Profile shows No 407,344, Yes 3,978, GSA_MIGRATION 316.
 - `FAC_ACCEPTED_DATE`  [date]
      - the day the government accepted the audit report as filed
 - `TOTAL_AMOUNT_EXPENDED`  [measure]
      - total federal dollars the organization spent in the audited year
 - `ENTITY_TYPE`  [filter]
      - what kind of body it is: non-profit, local, higher-ed, state, tribal, unknown
 - `AUDITEE_NAME`  [label]
      - the name of the organization that was audited

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 to FY2026 (20 tables, same columns)**
one row = one grant, loan or direct-payment transaction
connects: RECIPIENT_UEI matches AUDITEE_UEI on FAC_SINGLE_AUDIT
 - `RECIPIENT_UEI`  [join]
      - the federal id number of whoever received the money
      - WATCH: Fill rate not yet measured.
 - `RECIPIENT_NAME`  [label]
      - the name of whoever received the money
      - WATCH: Fill rate not yet measured.
 - `ACTION_DATE`  [date]
      - the day this grant transaction was signed or changed
      - WATCH: Fill rate not yet measured.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this one transaction, can be negative
      - WATCH: Loans carry no obligation: assistance types 07 and 08 sum to exactly $0.00 on 11,788,945 rows. Use FACE_VALUE_OF_LOAN for those.
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - coded kind of aid; the entry names only 07 and 08 as loans. Source: public USAspending code list, not the handbook
      - WATCH: Fill rate not yet measured.
 - `ACTION_TYPE_CODE`  [filter]
      - coded value that separates a brand new award from a continuation or change
      - WATCH: A new row is not always a new award. Fill not yet measured.
 - `AWARDING_AGENCY_NAME`  [label]
      - the federal agency that gave out the money
      - WATCH: Fill rate not yet measured.

---

## 58) Big investment managers quietly sell a company's stock the quarter before its first large pollution or mine-safety fine lands.  `W62` grade B
   - It would mean the pros see trouble coming before the public does. If holdings stay flat, fines this size are not something managers trade on.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS**
one row = one stock position on one investment manager's quarterly filing
connects: NAMEOFISSUER is name-matched to CONTROLLER_NAME on MSHA_VIOLATIONS and to PARENT_LEGAL_NAME on XC_EPA_CORPORATE_CROSSWALK; ACCESSION_NUMBER matches ACCESSION_NUMBER on 13F_SUBMISSIONS
 - `ACCESSION_NUMBER`  [join]
      - the filing number that ties every position back to one quarterly report
      - WATCH: Fill not yet measured.
 - `NAMEOFISSUER`  [join]
      - the name of the company whose stock is held, as typed
      - WATCH: Name match only, multi-word names only. Overlap not yet measured.
 - `CUSIP`  [label]
      - the standard nine-character code that identifies one stock or bond
      - WATCH: Fill not yet measured.
 - `SSHPRNAMT`  [measure]
      - how many shares, or how much bond face value, the manager holds
      - WATCH: Fill not yet measured.
 - `VALUE_USD`  [measure]
      - the dollar value of that position on the report date
      - WATCH: Fill not yet measured.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS**
one row = one quarterly holdings filing by one manager
connects: ACCESSION_NUMBER matches ACCESSION_NUMBER on 13F_HOLDINGS and gives the quarter through PERIODOFREPORT
 - `ACCESSION_NUMBER`  [join]
      - the filing number for this one quarterly report
 - `CIK`  [label]
      - the securities regulator's id number for the manager who filed
 - `PERIODOFREPORT`  [date]
      - the quarter-end date the holdings are reported as of
      - WATCH: The 13F load missed 7 of 53 source zips. A missing quarter looks exactly like a sell-off.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one mine-safety violation with its penalty
connects: CONTROLLER_NAME is name-matched to NAMEOFISSUER on 13F_HOLDINGS
 - `CONTROLLER_ID`  [label]
      - the mine-safety agency's id for the company that controls the mine
      - WATCH: 93.24% filled.
 - `CONTROLLER_NAME`  [join]
      - the name of the company that controls the mine
      - WATCH: Name match, multi-word only. Most mine controllers are private and will match no 13F issuer.
 - `VIOLATION_ISSUE_DATE`  [date]
      - the day the inspector wrote up the violation
 - `PROPOSED_PENALTY`  [measure]
      - the dollar fine the agency proposed for this violation
      - WATCH: 500,990 of 3,087,265 violations carry the standard $100 minimum. Set a dollar floor.
 - `AMOUNT_DUE`  [measure]
      - dollars still owed on this fine
 - `AMOUNT_PAID`  [measure]
      - dollars actually paid on this fine

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS**
one row = one formal Clean Air Act enforcement action with its penalty
connects: PGM_SYS_ID matches PGM_SYS_ID on FRS_PROGRAM_LINKS
 - `PGM_SYS_ID`  [join]
      - the air program's own id number for the plant
      - WATCH: Fill rate not yet measured.
 - `ACTIVITY_ID`  [label]
      - the id number of this one enforcement action
 - `SETTLEMENT_ENTERED_DATE`  [date]
      - the day the settlement or order was entered
      - WATCH: 99.96% filled.
 - `PENALTY_AMOUNT`  [measure]
      - the dollar penalty attached to this action
 - `ENF_TYPE_DESC`  [filter]
      - the kind of action in words, such as Administrative Order or Civil Judicial Action
 - `STATE_EPA_FLAG`  [filter]
      - who brought the action; entry says it splits state from federal; values are S, L, E
      - WATCH: Decide once whether a state fine counts.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS**
one row = one EPA program id tied to one facility registry id
connects: PGM_SYS_ID matches PGM_SYS_ID on ICIS_AIR_FORMAL_ACTIONS; REGISTRY_ID matches EPA_REGISTRY_ID on XC_EPA_CORPORATE_CROSSWALK
 - `PGM_SYS_ACRNM`  [filter]
      - short name of the EPA program the id belongs to, such as AIR, NPDES, RCRAINFO
 - `PGM_SYS_ID`  [join]
      - the program's own id number for the plant
 - `REGISTRY_ID`  [join]
      - the single EPA master id for the physical facility

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK**
one row = one EPA facility matched to a corporate parent
connects: EPA_REGISTRY_ID matches REGISTRY_ID on FRS_PROGRAM_LINKS; PARENT_LEGAL_NAME is name-matched to NAMEOFISSUER on 13F_HOLDINGS
 - `EPA_REGISTRY_ID`  [join]
      - the single EPA master id for the physical facility
 - `PARENT_LEGAL_NAME`  [join]
      - the legal name of the company that ultimately owns the facility
      - WATCH: Last hop is a name match. Many plant parents are private and match no 13F issuer.
 - `PARENT_CIK`  [filter]
      - the securities regulator's id for the parent, present only for listed companies
      - WATCH: 2.25% filled, 705 distinct parents.

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP**
one row = one EPA-regulated facility with its penalty totals
connects: FRS_ID is the facility registry id; used only as a cross-check on totals, not joined in the chain
 - `FRS_ID`  [join]
      - the single EPA master id for the physical facility
 - `TOTAL_PENALTIES`  [measure]
      - all penalty dollars ever recorded against this facility, every program
 - `LAST_PENALTY_AMT`  [measure]
      - the dollar amount of the most recent penalty only
      - WATCH: One row per site with the last penalty only, so it cannot date a first fine.
 - `DATE_LAST_FORMAL_ACTION`  [date]
      - the day of the most recent formal enforcement action at the facility
      - WATCH: 39.47% filled.

---

## 59) List every company whose pension plan went broke and got taken over by the federal insurer, and count the workers left in it.  `W63` grade B
   - It shows which employers walked away from the most retirees. Repeat sponsors and a change of owner just before the collapse are the tells.

**LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS**
one row = one pension plan taken over by the federal pension insurer
connects: EIN matches SPONS_DFE_EIN on FED_DOL_FORM5500_FULL
 - `SPONSOR_NAME`  [label]
      - the name of the company that ran the pension plan
 - `PLAN_NAME`  [label]
      - the name of the pension plan itself
 - `EIN`  [join]
      - the tax id number of the company that sponsored the plan
      - WATCH: 4,447 distinct values in 5,176 rows, so one sponsor can repeat.
 - `DATE_OF_PLAN_TERMINATION`  [date]
      - the day the pension plan was officially ended
 - `DATE_OF_PBGC_TRUSTEESHIP`  [date]
      - the day the federal insurer took the plan over
 - `NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION`  [measure]
      - how many workers and retirees were in the plan when it ended
      - WATCH: The column name is misspelled in the table, PARICIPANTS without the T.
 - `STATE`  [filter]
      - the state listed for the plan sponsor

**LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL**
one row = one annual pension or benefit plan filing
connects: SPONS_DFE_EIN matches EIN on PBGC_TRUSTEED_PLANS; a LAST_RPT_SPONS_EIN that differs from SPONS_DFE_EIN hints at a new owner
 - `SPONS_DFE_EIN`  [join]
      - the tax id number of the plan sponsor on this year's filing
      - WATCH: Fill rate not yet measured.
 - `SPONSOR_DFE_NAME`  [label]
      - the name of the plan sponsor on this year's filing
      - WATCH: Fill rate not yet measured.
 - `LAST_RPT_SPONS_EIN`  [filter]
      - the sponsor tax id used on the previous filing, if it changed
      - WATCH: In the mart it is a blank string on 32,680 of 33,484 rows. Expect the same sparseness here.
 - `LAST_RPT_SPONS_NAME`  [label]
      - the sponsor name used on the previous filing, if it changed
      - WATCH: Fill rate not yet measured.
 - `TOT_PARTCP_BOY_CNT`  [measure]
      - how many people were in the plan at the start of the year
      - WATCH: Fill rate not yet measured.
 - `FORM_PLAN_YEAR_BEGIN_DATE`  [date]
      - the first day of the plan year the filing covers
      - WATCH: Fill rate not yet measured.
 - `BUSINESS_CODE`  [filter]
      - coded value for the sponsor's line of business, look at distinct values first
      - WATCH: Fill rate not yet measured.

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500**
one row = one annual plan filing, a small slice received in the first half of 2026
connects: SPONS_DFE_EIN matches EIN on PBGC_TRUSTEED_PLANS, but use the landing table for history
 - `SPONS_DFE_EIN`  [join]
      - the tax id number of the plan sponsor on the filing
      - WATCH: Slice of 33,484 rows only. Its EIN and SPONSOR_DFE_EIN columns are blank strings on all rows.

---

## 60) Some parent companies collect federal contracts through dozens of subsidiaries whose names give no hint of who owns them.  `W65` grade B
   - It would show which corporate families are much bigger government vendors than any one name suggests. The count of names is measured, the intent is not.

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: nothing. One table, no join
 - `RECIPIENT_PARENT_UEI`  [join]
      - the federal id number of the ultimate parent company, as the vendor declared it
      - WATCH: Fill not yet measured. Self-reported, so a parent that does not declare itself is invisible.
 - `RECIPIENT_PARENT_NAME`  [label]
      - the name of the ultimate parent company, as the vendor declared it
      - WATCH: Fill rate not yet measured.
 - `RECIPIENT_UEI`  [join]
      - the federal id number of the company that actually signed the contract
      - WATCH: Fill rate not yet measured.
 - `RECIPIENT_NAME`  [label]
      - the name of the company that actually signed the contract
      - WATCH: Fill rate not yet measured.
 - `AWARD_ID_PIID`  [measure]
      - the government's id number for the contract itself
      - WATCH: Fill rate not yet measured.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed on this one transaction, can be negative
      - WATCH: Sum only where above zero. Fill rate not yet measured.
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the government budget year the transaction falls in
      - WATCH: Fill rate not yet measured.

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS**
one row = one parent-child link between two global legal-entity ids
connects: Not joined. No table links the federal vendor id to the legal-entity id used here
 - `RELATIONSHIP_STARTNODE_NODEID`  [join]
      - the global legal-entity id of the child company in the link
      - WATCH: Uses a different id than the contracts. No bridge table exists, so it cannot be attached.
 - `RELATIONSHIP_ENDNODE_NODEID`  [join]
      - the global legal-entity id of the parent or manager in the link
 - `RELATIONSHIP_RELATIONSHIPTYPE`  [filter]
      - kind of link, such as IS_DIRECTLY_CONSOLIDATED_BY, IS_ULTIMATELY_CONSOLIDATED_BY, IS_FUND-MANAGED_BY
 - `RELATIONSHIP_PERIOD_1_STARTDATE`  [date]
      - the day the ownership link began
      - WATCH: 99.94% filled. Ended relationships are dropped each release, so current links only.

---

## 61) Some nonprofit hospitals pay their top boss a far bigger slice of every dollar coming in than others do.  `W66` grade C
   - It would point at tax-exempt hospitals where executive pay is out of line with the size of the place. Only hospitals can be ranked, not charities at large.

**LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY**
one row = one person listed on one nonprofit hospital's tax return
connects: EIN matches EIN on FED_IRS_BMF
 - `EIN`  [join]
      - the tax id number of the nonprofit hospital that filed the return
      - WATCH: 3,962 distinct hospitals only.
 - `TAX_YEAR`  [date]
      - the tax year the return covers
      - WATCH: Tax years before 2017 are absent from the source.
 - `PERSON_NAME`  [label]
      - the name of the officer, director or key employee listed
      - WATCH: The same executive repeats on every affiliate's return with the same dollars, up to five times.
 - `TITLE`  [label]
      - the person's job title as written on the return
 - `TOTAL_COMPENSATION`  [measure]
      - all pay reported for that person on that return, in dollars
      - WATCH: Group by person and tax year and take the max, or one person counts up to five times.
 - `REPORTABLE_COMP_FROM_RELATED_ORGS`  [measure]
      - pay the person got from sister organizations of the filer
 - `IS_SCHEDULE_J_POINTER`  [filter]
      - true when the line only restates a payout already listed elsewhere
      - WATCH: 239 person-returns carry a pointer line. Rank with this false.
 - `IS_GROUP_RETURN`  [filter]
      - true when one return lumps a whole hospital system's pay together
      - WATCH: 61 rows are group returns.
 - `BMF_REVENUE_AMT`  [measure]
      - the hospital's revenue from the IRS master file, one snapshot only
      - WATCH: One snapshot, not each tax year's revenue. Ratios for older years use the wrong year's revenue.
 - `HOSPITAL_NAME`  [label]
      - the name of the hospital that filed

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF**
one row = one tax-exempt organization on the IRS master file
connects: EIN matches EIN on HOSPITAL_OFFICER_PAY
 - `EIN`  [join]
      - the tax id number of the tax-exempt organization
      - WATCH: 3,914 shared values were measured against a sister table, not this one.
 - `NTEE_CODE`  [filter]
      - the IRS category code for what the charity does; E2 codes are hospitals
      - WATCH: Profile shows 581,028 blank strings of 1,974,830 rows.
 - `REVENUE_AMT`  [measure]
      - the organization's most recent reported revenue, one snapshot
      - WATCH: One snapshot, no history.
 - `ORGANIZATION_NAME`  [label]
      - the organization's name on the IRS master file

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990**
one row = one nonprofit tax return
connects: EIN matches EIN on the other two tables, but the table is too small to use
 - `EIN`  [join]
      - the tax id number of the nonprofit that filed
      - WATCH: 200 rows only. It cannot rank charities.
 - `OFFICER_COMPENSATION_AMT`  [measure]
      - total dollars paid to officers as one lump figure on the return
      - WATCH: 200 rows only.
 - `TOTAL_REVENUE_AMT`  [measure]
      - total revenue the nonprofit reported on the return
      - WATCH: 200 rows only.

---

## 62) When a county gets a federal disaster declaration, the charities based there see their revenue jump the next year.  `W67` grade D
   - It would show how much donation and relief money floods into local nonprofits after a disaster. It cannot be tested today because the nonprofit return table is too thin.

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990**
one row = one nonprofit tax return
connects: STATE matches STATE on FED_FEMA_DISASTER_DECLARATIONS, the only shared place field; no ZIP or county join is possible
 - `EIN`  [label]
      - the tax id number of the nonprofit that filed
      - WATCH: 200 distinct in 200 rows. Each organization appears once, so no before and after.
 - `TAX_YEAR`  [date]
      - the tax year the return covers
      - WATCH: Tax periods 202312 to 202512 only.
 - `TOTAL_REVENUE_AMT`  [measure]
      - total revenue the nonprofit reported on the return
      - WATCH: 200 rows only, no history.
 - `STATE`  [join]
      - the state where the nonprofit is based
      - WATCH: State grain only.
 - `ZIP_CODE`  [join]
      - meant to be the nonprofit's postal code, but nothing is in it
      - WATCH: Blank string on all 200 rows.

**LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS**
one row = one disaster for one designated area, usually a county
connects: STATE matches STATE on FED_IRS_990; FIPSSTATECODE plus FIPSCOUNTYCODE would make a county code if the returns had a place
 - `DISASTERNUMBER`  [label]
      - the federal number given to the disaster
      - WATCH: Fill rate not yet measured.
 - `DECLARATIONDATE`  [date]
      - the day the disaster was officially declared
      - WATCH: Fill rate not yet measured.
 - `STATE`  [join]
      - the two-letter state the declaration covers
      - WATCH: Fill rate not yet measured.
 - `FIPSSTATECODE`  [join]
      - the two-digit census code for the state, padded
      - WATCH: Fill rate not yet measured.
 - `FIPSCOUNTYCODE`  [join]
      - the three-digit census code for the county, padded
      - WATCH: Fill rate not yet measured.
 - `INCIDENTTYPE`  [filter]
      - the kind of disaster in words, such as flood or fire
      - WATCH: Fill rate not yet measured.

**LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS**
one row = one household's registration for disaster aid
connects: DISASTER_NUMBER is the same disaster number as DISASTERNUMBER on FED_FEMA_DISASTER_DECLARATIONS; not used in the join as written
 - `DISASTER_NUMBER`  [label]
      - the federal number given to the disaster
      - WATCH: 620 distinct disasters.
 - `DECLARATION_DATE`  [date]
      - the day the disaster was officially declared
 - `DAMAGED_ZIP_CODE`  [join]
      - the postal code of the damaged home
 - `FIPS`  [join]
      - the census county code of the damaged home
      - WATCH: 74.21% filled.

---

## 63) Some nonprofits take federal grant money and also pay lobbyists, and the grants grow after the lobbying starts.  `W68` grade B
   - It would mean public money is helping fund the push for more public money. If few match, nonprofit lobbying is mostly big institutions that were already funded.

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 to FY2026 (20 tables, same columns)**
one row = one grant, loan or direct-payment transaction
connects: RECIPIENT_NAME plus RECIPIENT_STATE_CODE is name-matched to CLIENT_NAME plus CLIENT_STATE on FED_SENATE_LDA_FILINGS
 - `RECIPIENT_NAME`  [join]
      - the name of whoever received the money
      - WATCH: Name match, multi-word names only. Campus names will miss system names.
 - `RECIPIENT_UEI`  [label]
      - the federal id number of whoever received the money
      - WATCH: Fill rate not yet measured.
 - `RECIPIENT_STATE_CODE`  [join]
      - the two-letter state of whoever received the money
      - WATCH: Fill rate not yet measured.
 - `BUSINESS_TYPES_DESCRIPTION`  [filter]
      - words describing what kind of body the recipient is, used to pick nonprofits
      - WATCH: Fill rate not yet measured.
 - `ACTION_DATE`  [date]
      - the day this grant transaction was signed or changed
      - WATCH: Fill rate not yet measured.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this one transaction, can be negative
      - WATCH: Fill rate not yet measured.
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - coded kind of aid, look at distinct values first. Source: public USAspending code list, not the handbook
      - WATCH: Fill rate not yet measured.
 - `AWARDING_AGENCY_NAME`  [label]
      - the federal agency that gave out the money
      - WATCH: Fill rate not yet measured.

**LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS**
one row = one lobbying registration or quarterly report filed with the Senate
connects: CLIENT_NAME plus CLIENT_STATE is name-matched to RECIPIENT_NAME plus RECIPIENT_STATE_CODE on the ASSISTANCE_FY tables
 - `CLIENT_ID`  [label]
      - the Senate's id number for the organization paying for the lobbying
      - WATCH: Fill rate not yet measured.
 - `CLIENT_NAME`  [join]
      - the name of the organization paying for the lobbying
      - WATCH: No tax id on either side. Name plus state is the only link.
 - `CLIENT_STATE`  [join]
      - the state of the organization paying for the lobbying
      - WATCH: Fill rate not yet measured.
 - `FILING_YEAR`  [date]
      - the year the lobbying report covers
      - WATCH: Fill rate not yet measured.
 - `FILING_PERIOD`  [date]
      - which part of the year the report covers, such as first_quarter or mid_year
      - WATCH: Fill rate not yet measured.
 - `REGISTRANT_NAME`  [label]
      - the name of the lobbying firm or in-house team that filed
      - WATCH: Fill rate not yet measured.
 - `INCOME`  [measure]
      - dollars a lobbying firm was paid by the client for the period
      - WATCH: Stored as text. A filing fills INCOME or EXPENSES, not both. Cast and combine before summing.
 - `EXPENSES`  [measure]
      - dollars an organization spent lobbying with its own staff for the period
      - WATCH: Stored as text. A filing fills INCOME or EXPENSES, not both. Cast and combine before summing.
 - `GOVERNMENT_ENTITIES`  [label]
      - the agencies and chambers the lobbyists say they contacted
      - WATCH: Fill rate not yet measured.
 - `LOBBYING_ISSUES`  [label]
      - the topics the lobbyists say they worked on
      - WATCH: Fill rate not yet measured.

**LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS**
one row = one lobbying filing, from an older partial build
connects: CLIENT_NAME would match the same way, but use the landing table instead
 - `CLIENT_NAME`  [join]
      - the name of the organization paying for the lobbying
      - WATCH: Stops at 2021. An earlier note measured only 1999 to 2010 and 2020 to 2021. Use the landing table.

---

## 64) Hospital political committees and hospital staff send their campaign money to the members of Congress who sit on the health and tax committees.  `W69` grade B
   - It would mean hospital money chases the people who write hospital rules. If it spreads like all other money, it follows geography or party instead.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one itemized contribution from one person to one political committee
connects: CMTE_ID matches CMTE_ID on FEC_COMMITTEES_DIM; EMPLOYER is text-matched to a hospital name list built from XWALK_HOSPITAL_CCN_EIN and FED_IRS_BMF
 - `CMTE_ID`  [join]
      - the election regulator's id for the committee that got the money
      - WATCH: 25,960 values shared with the committee table.
 - `EMPLOYER`  [join]
      - who the donor says they work for, typed free-hand
      - WATCH: Free text. Text match only, overlap not yet measured.
 - `OCCUPATION`  [filter]
      - what the donor says their job is, typed free-hand
 - `DONOR_NAME`  [label]
      - the name of the person who gave the money
 - `TRANSACTION_AMT`  [measure]
      - the dollar amount of this one contribution
 - `TRANSACTION_DATE`  [date]
      - the day the contribution was made
      - WATCH: 99.98% filled. The date range ends in junk values; window not re-measured.
 - `TRANSACTION_TYPE`  [filter]
      - coded kind of transaction such as 15, 15E, 24T; look at distinct values first

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM**
one row = one political committee, de-duplicated across election cycles
connects: CMTE_ID matches CMTE_ID on FEC_INDIV_CONTRIBUTIONS; CAND_ID matches FEC_ID on MEMBER_FEC_ID; CONNECTED_ORG_NM is text-matched to the hospital name list
 - `CMTE_ID`  [join]
      - the election regulator's id for the committee
      - WATCH: Fill not yet measured.
 - `CMTE_NM`  [label]
      - the name the political committee registered under
      - WATCH: Fill not yet measured.
 - `CONNECTED_ORG_NM`  [join]
      - the company or group that sponsors the committee, such as a hospital system
      - WATCH: Text match only.
 - `ORG_TP`  [filter]
      - one-letter code for the kind of sponsor; look at distinct values first
      - WATCH: Fill not yet measured.
 - `CAND_ID`  [join]
      - the candidate id, filled when the committee belongs to one candidate
      - WATCH: Overlap with member ids not yet measured.
 - `CYCLE`  [date]
      - the two-year election cycle the committee row belongs to
      - WATCH: Null on 55% of rows. Never filter on it.
 - `IS_AMBIGUOUS`  [filter]
      - true when the committee could not be pinned to one clean record
      - WATCH: True on 14.1% of real money rows, 270,519, measured on the older copy.

**LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID**
one row = one pairing of a member of Congress with a campaign candidate id
connects: FEC_ID matches CAND_ID on FEC_COMMITTEES_DIM; BIOGUIDE matches BIOGUIDE on CONGRESS_COMMITTEE_MEMBERSHIP
 - `FEC_ID`  [join]
      - the election regulator's candidate id for the member
 - `BIOGUIDE`  [join]
      - the official Congress id for the member
      - WATCH: 99.94% filled.
 - `FULL_NAME`  [label]
      - the full name of the member of Congress

**LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP**
one row = one member's seat on one committee in one congress
connects: BIOGUIDE matches BIOGUIDE on MEMBER_FEC_ID
 - `BIOGUIDE`  [join]
      - the official Congress id for the member
      - WATCH: Roster misses about 4% of members per congress. Dedupe before joining money or dollars multiply by seat count.
 - `CONGRESS`  [date]
      - the number of the two-year congress, not a calendar year
 - `COMMITTEE_CODE`  [filter]
      - the short code for the committee or subcommittee
 - `COMMITTEE_NAME`  [label]
      - the name of the congressional committee in words
 - `IS_SUBCOMMITTEE`  [filter]
      - True when the seat is on a subcommittee, False for a full committee

**LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN**
one row = one hospital matched to a tax-exempt filer
connects: CCN_NAME and EIN_NAME feed the hospital name list that EMPLOYER and CONNECTED_ORG_NM are text-matched against
 - `CCN_NAME`  [join]
      - the hospital's name as the federal health insurer lists it
      - WATCH: Fill rate not yet measured.
 - `EIN_NAME`  [join]
      - the hospital's name as the tax agency lists it
      - WATCH: Fill rate not yet measured.
 - `MATCH_TIER`  [filter]
      - coded value for how the two names were matched, look at distinct values first
      - WATCH: Fill rate not yet measured.

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF**
one row = one tax-exempt organization on the IRS master file
connects: ORGANIZATION_NAME where NTEE_CODE starts with E2 feeds the same hospital name list
 - `ORGANIZATION_NAME`  [join]
      - the organization's name on the IRS master file
      - WATCH: Text match only.
 - `NTEE_CODE`  [filter]
      - the IRS category code for what the charity does; codes starting E2 are hospitals
      - WATCH: Profile shows 581,028 blank strings of 1,974,830 rows.
 - `STATE`  [filter]
      - the state where the organization is based

---

## 65) Bigger counties get more federal contract money, so find the counties that get far more or far less than their head count predicts.  `W70` grade B
   - The leftovers point at places with an outsized pipeline to federal dollars, or places being passed over. Military bases and national labs explain some and need ruling out.

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE matches FIPS on CDC_DRUG_POISONING_COUNTY, with fiscal year matched to YEAR
 - `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`  [join]
      - the five-digit census code of the county where the work is done
      - WATCH: Measured on FY2024 only: 93% filled, 2,894 counties. Self-reported by the contracting office.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed on this one transaction, can be negative
      - WATCH: Signed value. Filter above zero or net it on purpose.
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the government budget year, which runs October to September
      - WATCH: Fiscal year against calendar-year population is a small mismatch.
 - `AWARDING_AGENCY_NAME`  [label]
      - the federal agency that signed the contract

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY**
one row = one county in one year, with its population
connects: FIPS matches PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on the CONTRACTS_FY tables, YEAR matched to fiscal year
 - `FIPS`  [join]
      - the five-digit census code for the county
 - `YEAR`  [date]
      - the calendar year of the population figure
      - WATCH: Ends in 2015. No county population after that.
 - `POPULATION`  [measure]
      - how many people lived in the county that year
      - WATCH: 1999 to 2015 only. Using 2015 population for later years is a stated approximation.
 - `STATE`  [label]
      - the state the county sits in
 - `COUNTY`  [label]
      - the name of the county in words

---

## 66) Poorer applicants get turned down for mortgages more everywhere, so find the lenders who say no more than their applicants' incomes explain.  `W71` grade B
   - It would flag lenders that are harsher than their peers on the same kind of borrower. With no credit score in the file, it is a lead and not proof.

**LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 to 2024 (7 tables, same columns)**
one row = one mortgage application
connects: LEI matches LEI_2018 on HMDA_ARID2017_LEI_XREF to get the lender's name
 - `LEI`  [join]
      - the global legal-entity id of the lender that took the application
      - WATCH: Null on the placeholder rows. Name match rate of 84% was measured on a small sample table only.
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
      - WATCH: 1,961 placeholder rows in 2018 and 21 in 2019 carry '-1'. Count people-facing actions only, not purchased or withdrawn.
 - `INCOME`  [measure]
      - the applicant's yearly income as written on the application
      - WATCH: Fill rate not yet measured.
 - `DEBT_TO_INCOME_RATIO`  [filter]
      - monthly debt as a share of income, stored as text bands like 20%-<30%
      - WATCH: Banded text value. Fill not measured; a sample table shows about 63% filled.
 - `LOAN_AMOUNT`  [measure]
      - the dollar size of the loan asked for
      - WATCH: Fill rate not yet measured.
 - `LOAN_PURPOSE`  [filter]
      - what the loan was for: 1 buy a home, 2 home improvement, 31 refinance, 32 cash-out refinance, 4 other, 5 not applicable. Source: public HMDA code list, not the handbook
      - WATCH: Fill rate not yet measured.
 - `LOAN_TYPE`  [filter]
      - coded kind of loan, values 1 to 4; look at distinct values first
      - WATCH: Fill rate not yet measured.
 - `STATE_CODE`  [filter]
      - the state where the property is
      - WATCH: Fill rate not yet measured.
 - `COUNTY_CODE`  [filter]
      - the census county code where the property is
      - WATCH: Fill rate not yet measured.
 - `DENIAL_REASON_1`  [filter]
      - main reason for a denial: 1 debt too high for income, 2 job history, 3 credit history, 4 collateral, 5 not enough cash, 6 info could not be verified, 7 application incomplete, 8 mortgage insurance denied, 9 other. Source: public HMDA code list, not the handbook
      - WATCH: Fill rate not yet measured.

**LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF**
one row = one lender with its 2017 id, its name and its newer global id
connects: LEI_2018 matches LEI on the HMDA_LAR tables; ARID_2017 matches RESPONDENT_ID on HMDA_HISTORIC
 - `ARID_2017`  [join]
      - the lender's old-style id from the 2017 filing year
      - WATCH: Format match to the old table is unverified.
 - `RESPONDENT_NAME`  [label]
      - the lender's name, from a 2017 list
      - WATCH: Lenders that started after 2017 have no name here.
 - `LEI_2018`  [join]
      - the lender's global legal-entity id as of 2018
 - `LEI_2019`  [join]
      - the lender's global legal-entity id as of 2019
      - WATCH: 93.91% filled.
 - `LEI_2020`  [join]
      - the lender's global legal-entity id as of 2020
      - WATCH: 76.5% filled.

**LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC**
one row = one mortgage application in the old file layout, 2015 to 2017
connects: RESPONDENT_ID matches ARID_2017 on HMDA_ARID2017_LEI_XREF, format match unverified
 - `RESPONDENT_ID`  [join]
      - the lender's old-style id, only unique together with AGENCY_CODE
      - WATCH: Not a lender id by itself; pair it with AGENCY_CODE. Format match to ARID_2017 unverified.
 - `AGENCY_CODE`  [join]
      - coded value for which regulator the lender reports to, look at distinct values first
 - `ACTION_TAKEN`  [filter]
      - what happened to the application: 1 loan made, 2 approved but not taken, 3 denied, 4 withdrawn, 5 file incomplete, 6 loan bought from another lender, 7 and 8 preapproval outcomes. Source: public HMDA code list, not the handbook
 - `APPLICANT_INCOME_000S`  [measure]
      - the applicant's yearly income in thousands of dollars
 - `LOAN_AMOUNT_000S`  [measure]
      - the loan size in thousands of dollars

---

## 67) A company gets barred from federal contracts, then a new company with a different name pops up at the same street address and wins work.  `W72` grade B
   - It would mean the ban is easy to dodge with fresh paperwork. A shared office building is not shared ownership, so every hit needs a second tell.

**LIBRARY_RAW.LANDING.FED_SAM_EXCLUSIONS_FULL_R2**
one row = one exclusion of one person or firm, full source layout with street address
connects: ADDRESS_1 plus left 5 of ZIP_CODE matches PHYSICAL_ADDRESS_LINE_1 plus PHYSICAL_ADDRESS_ZIP on FED_SAM_ENTITY_PUBLIC; SAM_NUMBER matches SAM_NUMBER on FED_SAM_EXCLUSIONS
 - `NAME`  [label]
      - the name of the barred person or firm
      - WATCH: Fill rate not yet measured.
 - `ADDRESS_1`  [join]
      - the street address of the barred person or firm, typed free-hand
      - WATCH: Free text. Unit numbers and spelling will break exact matches.
 - `CITY`  [label]
      - the city of the barred person or firm
      - WATCH: Fill rate not yet measured.
 - `STATE_PROVINCE`  [filter]
      - the state or province of the barred person or firm
      - WATCH: Fill rate not yet measured.
 - `ZIP_CODE`  [join]
      - the postal code of the barred party; use the first five digits
      - WATCH: Fill rate not yet measured.
 - `UNIQUE_ENTITY_ID`  [join]
      - the federal vendor id of the barred firm, when it has one
      - WATCH: Fill rate not yet measured.
 - `CAGE`  [label]
      - the defense supplier code of the barred firm, when it has one
      - WATCH: Fill rate not yet measured.
 - `SAM_NUMBER`  [join]
      - the registry's own number for this one exclusion record
      - WATCH: Fill rate not yet measured.
 - `ACTIVE_DATE`  [date]
      - the day the ban on federal business started
      - WATCH: Not profiled. The cleaned copy carries sentinel years 1908, 2084, 2099 and 11,016 nulls; expect the same junk.
 - `TERMINATION_DATE`  [date]
      - the day the ban ends or ended
      - WATCH: Whether ended exclusions are kept is not yet measured.
 - `EXCLUSION_TYPE`  [filter]
      - kind of ban in words, such as Prohibition/Restriction or Ineligible
      - WATCH: Fill rate not yet measured.
 - `CLASSIFICATION`  [filter]
      - what was barred: Individual, Firm, Special Entity Designation or Vessel
      - WATCH: Fill rate not yet measured.
 - `CROSS_REFERENCE`  [label]
      - other names or parties the registry ties to this exclusion
      - WATCH: Fill rate not yet measured.

**LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS**
one row = the same exclusions, cleaned, without the street address
connects: SAM_NUMBER matches SAM_NUMBER on FED_SAM_EXCLUSIONS_FULL_R2, to borrow clean dates and the firm-or-person flag
 - `SAM_NUMBER`  [join]
      - the registry's own number for this one exclusion record
 - `UEI`  [join]
      - the federal vendor id of the barred firm, when it has one
      - WATCH: 28.33% filled. 1,798 ids have three or more overlapping windows; use an exists test, not a join.
 - `ACTIVATION_DATE`  [date]
      - the day the ban started, cleaned
      - WATCH: 93.46% filled. Sentinel years 1908, 2084, 2099 and 11,016 nulls.
 - `IS_ENTITY_NOT_INDIVIDUAL`  [filter]
      - true when the barred party is a business and not a person
 - `ENTITY_NAME`  [label]
      - the name of the barred person or firm, cleaned

**LIBRARY_RAW.LANDING.FED_SAM_ENTITY_PUBLIC**
one row = one entity registered to do business with the government
connects: PHYSICAL_ADDRESS_LINE_1 plus PHYSICAL_ADDRESS_ZIP matches ADDRESS_1 plus left 5 of ZIP_CODE on FED_SAM_EXCLUSIONS_FULL_R2; UEI_SAM matches RECIPIENT_UEI on the CONTRACTS_FY tables
 - `UEI_SAM`  [join]
      - the federal vendor id of the registered business
      - WATCH: Fill rate not yet measured.
 - `CAGE_CODE`  [label]
      - the defense supplier code of the registered business
      - WATCH: Fill rate not yet measured.
 - `LEGAL_BUSINESS_NAME`  [label]
      - the registered legal name of the business
      - WATCH: Fill rate not yet measured.
 - `DBA_NAME`  [label]
      - the trading name the business goes by, if different
      - WATCH: Fill rate not yet measured.
 - `PHYSICAL_ADDRESS_LINE_1`  [join]
      - the street address where the business physically sits
      - WATCH: Free text. Unit numbers and spelling will break exact matches.
 - `PHYSICAL_ADDRESS_CITY`  [label]
      - the city where the business physically sits
      - WATCH: Fill rate not yet measured.
 - `PHYSICAL_ADDRESS_ZIP`  [join]
      - the postal code where the business physically sits
      - WATCH: Fill rate not yet measured.
 - `INITIAL_REGISTRATION_DATE`  [date]
      - the day the business first signed up to sell to the government
      - WATCH: Current extract only. Lapsed registrations may be missing.
 - `ENTITY_START_DATE`  [date]
      - the day the business says it was founded
      - WATCH: Fill rate not yet measured.
 - `ELEC_BUS_POC_FIRST_NAME`  [label]
      - first name of the business's listed contact person
      - WATCH: Fill rate not yet measured.
 - `ELEC_BUS_POC_LAST_NAME`  [join]
      - last name of the business's listed contact person, a second tell of same people
      - WATCH: Fill rate not yet measured.
 - `EXCLUSION_STATUS_FLAG`  [filter]
      - coded marker for whether the registry shows this business as barred, look at distinct values first
      - WATCH: Fill rate not yet measured.

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: RECIPIENT_UEI matches UEI_SAM on FED_SAM_ENTITY_PUBLIC, keeping ACTION_DATE after ACTIVE_DATE
 - `RECIPIENT_UEI`  [join]
      - the federal vendor id of the company that signed the contract
      - WATCH: Fill rate not yet measured.
 - `RECIPIENT_NAME`  [label]
      - the name of the company that signed the contract
      - WATCH: Fill rate not yet measured.
 - `ACTION_DATE`  [date]
      - the day this contract transaction was signed or changed
      - WATCH: Fill rate not yet measured.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed on this one transaction, can be negative
      - WATCH: Signed value. Filter above zero or totals during an exclusion window read negative.
 - `HIGHLY_COMPENSATED_OFFICER_1_NAME`  [join]
      - the name of the vendor's top-paid officer, a second tell of same people
      - WATCH: Fill rate not yet measured.

---

## 68) Businesses already on a federal do-not-pay list still got big pandemic payroll loans.  `W73` grade B
   - It would mean lenders skipped the most basic check before handing out public money. Near zero matches would say the screening worked, or barred firms borrowed under another name.

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS**
one row = one pandemic payroll loan
connects: BORROWERNAME plus left 5 of BORROWERZIP matches ENTITY_NAME plus left 5 of ZIP on FED_SAM_EXCLUSIONS, and BUSINESS_NAME plus ZIP on FED_HHS_OIG_LEIE
 - `BORROWERNAME`  [join]
      - the name of the business that got the loan
      - WATCH: No tax id on any side. Multi-word names held up 92% of the time, single-word names 8%.
 - `BORROWERADDRESS`  [label]
      - the street address of the business that got the loan
      - WATCH: Fill rate not yet measured.
 - `BORROWERCITY`  [label]
      - the city of the business that got the loan
      - WATCH: Fill rate not yet measured.
 - `BORROWERSTATE`  [filter]
      - the state of the business that got the loan
      - WATCH: Fill rate not yet measured.
 - `BORROWERZIP`  [join]
      - the postal code of the borrower; use the first five digits
      - WATCH: Fill rate not yet measured.
 - `DATEAPPROVED`  [date]
      - the day the loan was approved
      - WATCH: Approval dates not yet measured.
 - `INITIALAPPROVALAMOUNT`  [measure]
      - the dollar size of the loan when first approved
      - WATCH: Labeled 150K-plus but holds 4,092 loans under $150,000.
 - `FORGIVENESSAMOUNT`  [measure]
      - dollars of the loan the government later wrote off
      - WATCH: Fill rate not yet measured.
 - `PROCESSINGMETHOD`  [filter]
      - PPP for a first loan, PPS for a second-draw loan
      - WATCH: Second-draw loans are capped at exactly $2,000,000. Split by this column.

**LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS**
one row = one exclusion from federal contracting
connects: ENTITY_NAME plus left 5 of ZIP matches BORROWERNAME plus left 5 of BORROWERZIP on SBA_PPP_LOANS_150K_PLUS, keeping ACTIVATION_DATE before DATEAPPROVED
 - `ENTITY_NAME`  [join]
      - the name of the barred person or firm
      - WATCH: Name match, multi-word only.
 - `ZIP`  [join]
      - the postal code of the barred person or firm
      - WATCH: 81.9% filled.
 - `ACTIVATION_DATE`  [date]
      - the day the ban on federal contracting started
      - WATCH: 93.46% filled. Sentinel years 1908, 2084, 2099 and 11,016 nulls. Drop them before the date test.
 - `TERMINATION_DATE`  [date]
      - the day the ban ends or ended
      - WATCH: 5.5% filled.
 - `IS_ENTITY_NOT_INDIVIDUAL`  [filter]
      - true when the barred party is a business and not a person
 - `EXCLUSION_TYPE`  [filter]
      - kind of ban in words, such as Prohibition/Restriction or Ineligible

**LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE**
one row = one active exclusion from federal health programs
connects: BUSINESS_NAME plus ZIP matches BORROWERNAME plus left 5 of BORROWERZIP on SBA_PPP_LOANS_150K_PLUS, keeping EXCLUSION_DATE before DATEAPPROVED
 - `BUSINESS_NAME`  [join]
      - the name of the barred business, empty when the row is a person
      - WATCH: Active exclusions only. Reinstated firms are gone, so every count is a floor.
 - `ZIP`  [join]
      - the postal code of the barred party
 - `EXCLUSION_DATE`  [date]
      - the day the ban from federal health programs started
 - `ADDRESS`  [label]
      - the street address of the barred party
 - `IS_ENTITY_NOT_INDIVIDUAL`  [filter]
      - true when the barred party is a business and not a person

---

## 69) The same university doctors who lead federally funded research are also taking payments from drug and device makers.  `W74` grade C
   - It would show which campuses have the most scientists with a foot in both camps. Names are the only link, so every count is an estimate.

**LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER**
one row = one federal health research project in one fiscal year
connects: PI_NAMES split to first and last plus ORG_STATE is name-matched to COVERED_RECIPIENT_FIRST_NAME, COVERED_RECIPIENT_LAST_NAME and RECIPIENT_STATE on CMS_OPEN_PAYMENTS; ORG_NAME is name-matched to TEACHING_HOSPITAL_NAME
 - `ORG_NAME`  [join]
      - the name of the university or institution holding the grant
      - WATCH: Name match, overlap not yet measured.
 - `ORG_UEI`  [label]
      - the federal id number of the institution holding the grant
      - WATCH: 93.41% filled.
 - `ORG_CITY`  [filter]
      - the city of the institution, used to confirm a name match
 - `ORG_STATE`  [join]
      - the state where the grant-holding institution sits
 - `PI_NAMES`  [join]
      - the names of the lead scientists on the project, several in one cell
      - WATCH: Must be split into first and last. A common name in a large state matches the wrong person.
 - `PI_PROFILE_IDS`  [label]
      - the research agency's own id numbers for the lead scientists
      - WATCH: Not a doctor id. No doctor id exists on the grant side.
 - `FISCAL_YEAR`  [date]
      - the government budget year the project row belongs to
 - `AWARD_AMOUNT`  [measure]
      - dollars awarded to the project for that year
 - `ORG_ZIP`  [join]
      - meant to be the institution's postal code, but nothing is in it
      - WATCH: 0.0% filled.
 - `ORG_FIPS`  [join]
      - meant to be the institution's county code, but nothing is in it
      - WATCH: 0.0% filled.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS**
one row = one payment from a drug or device maker to a doctor or teaching hospital
connects: COVERED_RECIPIENT_FIRST_NAME plus COVERED_RECIPIENT_LAST_NAME plus RECIPIENT_STATE is name-matched to PI_NAMES plus ORG_STATE on NIH_REPORTER; NPI matches NPI on CMS_NPPES
 - `NPI`  [join]
      - the national id number of the doctor who was paid
      - WATCH: 48,059 blank strings.
 - `COVERED_RECIPIENT_FIRST_NAME`  [join]
      - first name of the doctor who was paid
      - WATCH: Name match only.
 - `COVERED_RECIPIENT_LAST_NAME`  [join]
      - last name of the doctor who was paid
      - WATCH: Name match only. Require an uncommon multi-word surname and same city.
 - `RECIPIENT_STATE`  [join]
      - the state of the doctor or hospital that was paid
 - `RECIPIENT_CITY`  [filter]
      - the city of the doctor or hospital that was paid
 - `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`  [measure]
      - the dollar value of this one payment or gift
      - WATCH: Program year 2024 only in this table.
 - `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`  [filter]
      - what the payment was for in words, such as food, consulting or debt forgiveness
      - WATCH: Debt forgiveness $40.8M and Acquisitions $213M put people on top with no check cut. Split by this first.
 - `TEACHING_HOSPITAL_NAME`  [join]
      - the name of the teaching hospital, when the hospital was paid
      - WATCH: Name match, overlap not yet measured.
 - `CCN`  [label]
      - the federal health insurer's hospital id, when the hospital was paid
      - WATCH: Blank string on 15,350,656 rows.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES**
one row = one provider id record from the national registry
connects: NPI matches NPI on CMS_OPEN_PAYMENTS; then compare practice city to ORG_CITY on NIH_REPORTER
 - `NPI`  [join]
      - the national id number of the doctor or provider
 - `PROVIDER_LAST_NAME_LEGAL_NAME`  [label]
      - the legal last name of the doctor or provider
 - `PROVIDER_FIRST_NAME`  [label]
      - the first name of the doctor or provider
 - `PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME`  [filter]
      - the city where the provider sees patients
 - `PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME`  [filter]
      - the state where the provider sees patients

---

## 70) The counties that pull in the most federal health research money are the same counties where drug makers buy doctors the most meals.  `W75` grade B
   - It would mean industry courts doctors hardest where the research happens. The likely answer is no, meals follow doctors and grants follow a few campuses, and that is still worth showing.

**LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER**
one row = one federal health research project in one fiscal year
connects: ORG_UEI matches UEI_SAM on FED_SAM_ENTITY_PUBLIC, measured at 80%
 - `ORG_UEI`  [join]
      - the federal id number of the institution holding the grant
      - WATCH: 93.41% filled; 6.59% of grant rows have none. Match to the registry is 80%.
 - `ORG_NAME`  [label]
      - the name of the university or institution holding the grant
 - `ORG_CITY`  [label]
      - the city of the institution, a fallback for placing unmatched rows
 - `ORG_STATE`  [label]
      - the state of the institution, a fallback for placing unmatched rows
 - `FISCAL_YEAR`  [date]
      - the government budget year the project row belongs to
 - `AWARD_AMOUNT`  [measure]
      - dollars awarded to the project for that year
 - `ORG_ZIP`  [join]
      - meant to be the institution's postal code, but nothing is in it
      - WATCH: 0.0% filled.
 - `ORG_FIPS`  [join]
      - meant to be the institution's county code, but nothing is in it
      - WATCH: 0.0% filled.

**LIBRARY_RAW.LANDING.FED_SAM_ENTITY_PUBLIC**
one row = one entity registered to do business with the government
connects: UEI_SAM matches ORG_UEI on NIH_REPORTER; left 5 of PHYSICAL_ADDRESS_ZIP matches ZCTA5 on XWALK_ZCTA_COUNTY
 - `UEI_SAM`  [join]
      - the federal id number of the registered institution
      - WATCH: Fill rate not yet measured.
 - `LEGAL_BUSINESS_NAME`  [label]
      - the registered legal name of the institution
      - WATCH: Fill rate not yet measured.
 - `PHYSICAL_ADDRESS_CITY`  [label]
      - the city of the institution's registered office
      - WATCH: Fill rate not yet measured.
 - `PHYSICAL_ADDRESS_STATE`  [label]
      - the state of the institution's registered office
      - WATCH: Fill rate not yet measured.
 - `PHYSICAL_ADDRESS_ZIP`  [join]
      - the postal code of the registered office; use the first five digits
      - WATCH: It is the registered office, so a multi-campus system's home county is overstated.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS**
one row = one payment from a drug or device maker to a doctor or teaching hospital
connects: left 5 of RECIPIENT_ZIP_CODE matches ZCTA5 on XWALK_ZCTA_COUNTY
 - `RECIPIENT_ZIP_CODE`  [join]
      - the postal code of the doctor who was paid; use the first five digits
      - WATCH: 464 blank strings.
 - `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`  [filter]
      - what the payment was for in words; keep the food and beverage rows
 - `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`  [measure]
      - the dollar value of this one payment or gift
 - `PROGRAM_YEAR`  [date]
      - the reporting year of the payment
      - WATCH: 2024 only in this table. One cross-section, no trend.

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one pairing of a census ZIP area with a county
connects: ZCTA5 matches left 5 of PHYSICAL_ADDRESS_ZIP on FED_SAM_ENTITY_PUBLIC and left 5 of RECIPIENT_ZIP_CODE on CMS_OPEN_PAYMENTS; COUNTY_FIPS is the shared county code
 - `ZCTA5`  [join]
      - the five-digit census ZIP area code
      - WATCH: 10,186 of 33,791 ZIP areas cross a county line. Single-building ZIPs like 44195, 94143, 27710 have no area and can miss.
 - `COUNTY_FIPS`  [join]
      - the five-digit census code for the county
      - WATCH: For ZIP areas that cross a line, picking the largest-land county was right 47.1% of the time.

---

## 71) Thousands of consumer complaints carry the exact same story, word for word, so somebody is filing from a template.  `M-239` grade A
   - It would mean a chunk of the complaint system is a filing mill, not upset individuals. The top text alone shows up 27,510 times.

**LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS**
one row = one consumer complaint
connects: nothing. One table, no join
 - `COMPLAINT_NARRATIVE`  [measure]
      - the story the consumer typed, word for word, with personal details blanked by the bureau
      - WATCH: Only 3.83M of 17.17M complaints have a story. Blanking makes exact-match counts a floor. Fill not yet measured.
 - `HAS_NARRATIVE`  [filter]
      - true or false: did the consumer agree to publish a written story
 - `COMPANY`  [label]
      - name of the company the complaint is against, 8,088 different names
      - WATCH: Three credit bureaus are 77% of all rows, and each can be spelled more than one way. List spellings first.
 - `DATE_RECEIVED`  [date]
      - the day the consumer bureau received the complaint
      - WATCH: It is the day received, not the day the problem happened. Batch uploads and weekends shape daily counts.
 - `PRODUCT`  [filter]
      - the kind of financial product complained about, such as credit report or mortgage
 - `ISSUE`  [label]
      - the type of problem the consumer picked from the bureau's list
 - `SUBMITTED_VIA`  [filter]
      - how the complaint arrived: Web, Referral, Phone, Postal mail or Fax
 - `ZIP_CODE`  [label]
      - the consumer's postal ZIP code as given on the complaint
 - `RECEIVED_MONTH`  [date]
      - the month the complaint was received, for counting by month

---

## 72) When complaints against one credit bureau jump on a given day, the other two bureaus jump on the same day.  `M-245` grade A
   - Shared spike days point to one outside sender or campaign hitting all three at once. Bureau-only spikes point to a company event like an outage or a breach.

**LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS**
one row = one consumer complaint
connects: nothing. One table, no join
 - `COMPANY`  [label]
      - name of the company the complaint is against, 8,088 different names
      - WATCH: Three credit bureaus are 77% of all rows, and each can be spelled more than one way. List spellings first.
 - `DATE_RECEIVED`  [date]
      - the day the consumer bureau received the complaint
      - WATCH: It is the day received, not the day the problem happened. Batch uploads and weekends shape daily counts.
 - `PRODUCT`  [filter]
      - the kind of financial product complained about, such as credit report or mortgage
 - `ISSUE`  [label]
      - the type of problem the consumer picked from the bureau's list
 - `SUBMITTED_VIA`  [filter]
      - how the complaint arrived: Web, Referral, Phone, Postal mail or Fax
 - `COMPLAINT_NARRATIVE`  [measure]
      - the story the consumer typed, word for word, with personal details blanked by the bureau
      - WATCH: Only 3.83M of 17.17M complaints have a story. Blanking makes exact-match counts a floor. Fill not yet measured.
 - `ZIP_CODE`  [label]
      - the consumer's postal ZIP code as given on the complaint

---

## 73) Some big companies close nearly every complaint with the same canned answer.  `M-240` grade A
   - It shows which companies treat complaints as paperwork to stamp and how rarely anyone gets relief. Experian uses one category on 79.2% of 4.12M complaints.

**LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS**
one row = one consumer complaint
connects: nothing. One table, no join
 - `COMPANY`  [label]
      - name of the company the complaint is against, 8,088 different names
      - WATCH: Three credit bureaus are 77% of all rows, and each can be spelled more than one way. List spellings first.
 - `COMPANY_RESPONSE`  [measure]
      - how the company closed it: Closed with explanation, with non-monetary relief, with monetary relief, In progress; 8 values
      - WATCH: 3.08% of rows have no value. The company picks the category, so it records what the company said it did.
 - `COMPANY_PUBLIC_RESPONSE`  [label]
      - the optional public statement the company chose to attach, picked from 11 canned lines
      - WATCH: Only 52.78% filled.
 - `IS_TIMELY`  [filter]
      - true or false: did the company answer within the deadline
 - `PRODUCT`  [filter]
      - the kind of financial product complained about, such as credit report or mortgage
 - `DATE_RECEIVED`  [date]
      - the day the consumer bureau received the complaint
      - WATCH: It is the day received, not the day the problem happened. Batch uploads and weekends shape daily counts.

---

## 74) Complaint stories used to be written by real people in their own words, and year by year more of them are copies.  `WN-143` grade B
   - A falling share of unique texts would show templates taking over the complaint system. A flat share would say templating was always there.

**LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS**
one row = one consumer complaint
connects: nothing. One table, no join
 - `COMPLAINT_NARRATIVE`  [measure]
      - the story the consumer typed, word for word, with personal details blanked by the bureau
      - WATCH: Only 3.83M of 17.17M complaints have a story. Blanking makes exact-match counts a floor. Fill not yet measured.
 - `HAS_NARRATIVE`  [filter]
      - true or false: did the consumer agree to publish a written story
 - `RECEIVED_YEAR`  [date]
      - the year the complaint was received, stored as the first of January of that year
      - WATCH: Stored as a date like 2011-01-01, not a number. 2026 is a partial year ending 2026-07-23.
 - `RECEIVED_MONTH`  [date]
      - the month the complaint was received, for counting by month
 - `COMPANY`  [label]
      - name of the company the complaint is against, 8,088 different names
      - WATCH: Three credit bureaus are 77% of all rows, and each can be spelled more than one way. List spellings first.
 - `PRODUCT`  [filter]
      - the kind of financial product complained about, such as credit report or mortgage

---

## 75) One person, by name and ZIP code, writes political checks to hundreds of different committees.  `WN-152` grade B
   - It finds the donors plugged into the most fundraising networks and shows whether they spread small gifts everywhere. The top name and ZIP pair reached 268 committees on an older copy.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one itemized contribution from one person to one committee
connects: nothing. One table, no join
 - `DONOR_NAME`  [join]
      - the donor's name as typed on the filing
      - WATCH: Name plus ZIP is not a real id. Common names in big ZIPs merge different people.
 - `ZIP_CODE`  [join]
      - the donor's postal ZIP code, sometimes 5 digits and sometimes 9
      - WATCH: 321,021 blank strings. Mixes 5 and 9 digit forms, 5,757,830 distinct values. Cut to the first 5 before grouping.
 - `CMTE_ID`  [measure]
      - the election commission's id for the committee that got the money, 40,294 different ones
 - `TRANSACTION_AMT`  [measure]
      - dollar amount of this one gift
 - `TRANSACTION_TYPE`  [filter]
      - coded kind of transaction: 15E is a gift passed through a conduit platform; check other codes first
      - WATCH: 15E earmark rows add the conduit as one more committee and can double the dollars. Decide once how to count them.
 - `TRANSACTION_DATE`  [date]
      - the day the gift was made
      - WATCH: 99.98% filled. Range runs 0031-04-10 to 9206-07-02, junk end dates. Real window on the 283,771,819-row table not re-measured.
 - `EMPLOYER`  [label]
      - the donor's employer as the donor typed it
 - `OCCUPATION`  [label]
      - the donor's job as the donor typed it
 - `CYCLE_FILE`  [filter]
      - which two-year election cycle file the row came from, such as 2020 or 2024

---

## 76) Some recipients of federal aid show up only in the two pandemic years and never before or after.  `N6` grade B
   - These are the outfits with no federal footprint that got money during the surge and then disappeared. The finding is in the big ones and in clusters at one address.

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2020**
one row = one grant, loan or direct-payment transaction
connects: RECIPIENT_UEI in FY2020 and FY2021 checked against RECIPIENT_UEI in the other 18 year tables; keep the ones found nowhere else
 - `RECIPIENT_UEI`  [join]
      - the government's current id number for the organization that got the money
      - WATCH: Fill never measured. Older rows may lack it, which makes a long-time recipient look new in 2020. Check fill by year.
 - `RECIPIENT_DUNS`  [join]
      - the older id number for the recipient, used before the current one
      - WATCH: Fill not yet measured. Fallback when RECIPIENT_UEI is blank.
 - `RECIPIENT_NAME`  [label]
      - name of whoever received the money
      - WATCH: County-level roll-up rows carry a generic recipient name, not a real organization.
 - `RECIPIENT_ADDRESS_LINE_1`  [label]
      - street address of the recipient, useful for spotting many recipients at one address
 - `RECIPIENT_ZIP_CODE`  [label]
      - postal ZIP code of the recipient
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the federal fiscal year the transaction falls in
      - WATCH: FY2026 is partial and some actions are dated ahead to 2026-09-30.
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - coded kind of aid; 07 and 08 are loans, for other codes look at distinct values first. Source: public USAspending code list, not the handbook
      - WATCH: Types 07 and 08 show exactly $0.00 obligation on 11,788,945 rows.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this transaction
      - WATCH: Zero for loans. Summing this alone drops the whole pandemic-loan story.
 - `FACE_VALUE_OF_LOAN`  [measure]
      - the dollar size of the loan, where loan money actually shows up
      - WATCH: $1.243T in FY2020 alone sits here, not in the obligation column.
 - `CFDA_NUMBER`  [filter]
      - the catalog number of the federal aid program
 - `CFDA_TITLE`  [label]
      - the plain name of the federal aid program the money came from
 - `BUSINESS_TYPES_DESCRIPTION`  [label]
      - text describing what kind of organization the recipient is
 - `DISASTER_EMERGENCY_FUND_CODES_FOR_OVERALL_AWARD`  [filter]
      - codes tagging the award to an emergency fund; coded value, look at distinct values first
 - `RECORD_TYPE_CODE`  [filter]
      - coded value the handbook says separates county-level roll-up rows; look at distinct values first
      - WATCH: Fill not yet measured. Needed to drop roll-up rows that hide individuals.

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2021**
one row = one grant, loan or direct-payment transaction
connects: RECIPIENT_UEI in FY2020 and FY2021 checked against RECIPIENT_UEI in the other 18 year tables; keep the ones found nowhere else
 - `RECIPIENT_UEI`  [join]
      - the government's current id number for the organization that got the money
      - WATCH: Fill never measured. Older rows may lack it, which makes a long-time recipient look new in 2020. Check fill by year.
 - `RECIPIENT_DUNS`  [join]
      - the older id number for the recipient, used before the current one
      - WATCH: Fill not yet measured. Fallback when RECIPIENT_UEI is blank.
 - `RECIPIENT_NAME`  [label]
      - name of whoever received the money
      - WATCH: County-level roll-up rows carry a generic recipient name, not a real organization.
 - `RECIPIENT_ADDRESS_LINE_1`  [label]
      - street address of the recipient, useful for spotting many recipients at one address
 - `RECIPIENT_ZIP_CODE`  [label]
      - postal ZIP code of the recipient
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the federal fiscal year the transaction falls in
      - WATCH: FY2026 is partial and some actions are dated ahead to 2026-09-30.
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - coded kind of aid; 07 and 08 are loans, for other codes look at distinct values first. Source: public USAspending code list, not the handbook
      - WATCH: Types 07 and 08 show exactly $0.00 obligation on 11,788,945 rows.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this transaction
      - WATCH: Zero for loans. Summing this alone drops the whole pandemic-loan story.
 - `FACE_VALUE_OF_LOAN`  [measure]
      - the dollar size of the loan, where loan money actually shows up
      - WATCH: $1.243T in FY2020 alone sits here, not in the obligation column.
 - `CFDA_NUMBER`  [filter]
      - the catalog number of the federal aid program
 - `CFDA_TITLE`  [label]
      - the plain name of the federal aid program the money came from
 - `BUSINESS_TYPES_DESCRIPTION`  [label]
      - text describing what kind of organization the recipient is
 - `DISASTER_EMERGENCY_FUND_CODES_FOR_OVERALL_AWARD`  [filter]
      - codes tagging the award to an emergency fund; coded value, look at distinct values first
 - `RECORD_TYPE_CODE`  [filter]
      - coded value the handbook says separates county-level roll-up rows; look at distinct values first
      - WATCH: Fill not yet measured. Needed to drop roll-up rows that hide individuals.

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 to FY2019 and FY2022 to FY2026 (18 tables, same columns)**
one row = one grant, loan or direct-payment transaction
connects: RECIPIENT_UEI in FY2020 and FY2021 checked against RECIPIENT_UEI in the other 18 year tables; keep the ones found nowhere else
 - `RECIPIENT_UEI`  [join]
      - the government's current id number for the organization that got the money
      - WATCH: Fill never measured. Older rows may lack it, which makes a long-time recipient look new in 2020. Check fill by year.
 - `RECIPIENT_DUNS`  [join]
      - the older id number for the recipient, used before the current one
      - WATCH: Fill not yet measured. Fallback when RECIPIENT_UEI is blank.
 - `RECIPIENT_NAME`  [label]
      - name of whoever received the money
      - WATCH: County-level roll-up rows carry a generic recipient name, not a real organization.
 - `RECIPIENT_ADDRESS_LINE_1`  [label]
      - street address of the recipient, useful for spotting many recipients at one address
 - `RECIPIENT_ZIP_CODE`  [label]
      - postal ZIP code of the recipient
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the federal fiscal year the transaction falls in
      - WATCH: FY2026 is partial and some actions are dated ahead to 2026-09-30.
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - coded kind of aid; 07 and 08 are loans, for other codes look at distinct values first. Source: public USAspending code list, not the handbook
      - WATCH: Types 07 and 08 show exactly $0.00 obligation on 11,788,945 rows.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars the government committed on this transaction
      - WATCH: Zero for loans. Summing this alone drops the whole pandemic-loan story.
 - `FACE_VALUE_OF_LOAN`  [measure]
      - the dollar size of the loan, where loan money actually shows up
      - WATCH: $1.243T in FY2020 alone sits here, not in the obligation column.
 - `CFDA_NUMBER`  [filter]
      - the catalog number of the federal aid program
 - `CFDA_TITLE`  [label]
      - the plain name of the federal aid program the money came from
 - `BUSINESS_TYPES_DESCRIPTION`  [label]
      - text describing what kind of organization the recipient is
 - `DISASTER_EMERGENCY_FUND_CODES_FOR_OVERALL_AWARD`  [filter]
      - codes tagging the award to an emergency fund; coded value, look at distinct values first
 - `RECORD_TYPE_CODE`  [filter]
      - coded value the handbook says separates county-level roll-up rows; look at distinct values first
      - WATCH: Fill not yet measured. Needed to drop roll-up rows that hide individuals.

---

# POWER

## 77) The same immigration judge grants relief more or less often depending on who is president.  `W76` grade B
   - It would mean the outcome of a deportation case depends on the calendar, not only the facts. If rates only move with the mix of nationalities, the judge is stable and the caseload changed.

**LIBRARY_RAW.LANDING.FED_EOIR_PROCEEDING**
one row = one proceeding in one immigration case
connects: IJ_CODE matches JUDGE_CODE on FED_EOIR_JUDGE; 33,135 rows carry a code missing from the judge table
 - `IJ_CODE`  [join]
      - short code for the immigration judge who handled the proceeding
      - WATCH: 33,135 rows carry a code absent from the judge table. Code AAA means All Judges, not a person.
 - `DEC_CODE`  [measure]
      - coded outcome of the case; coded value, look at distinct values first
      - WATCH: Blank three ways: NULL on 5.32M rows, a NUL byte on 1.45M, a single space on 729K. No code list landed, so which codes mean a grant is unknown.
 - `DEC_TYPE`  [filter]
      - coded kind of decision; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `COMP_DATE`  [date]
      - the day the proceeding was completed
      - WATCH: Fill and date range not yet measured.
 - `NAT`  [filter]
      - coded nationality of the person in the case; hold it constant when comparing
      - WATCH: Fill not yet measured.
 - `CASE_TYPE`  [filter]
      - coded kind of immigration case; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `CUSTODY`  [filter]
      - coded custody status of the person; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `BASE_CITY_CODE`  [label]
      - short code for the court city the case belongs to
      - WATCH: Fill not yet measured.

**LIBRARY_RAW.LANDING.FED_EOIR_JUDGE**
one row = one judge code in the immigration court lookup
connects: JUDGE_CODE matches IJ_CODE on FED_EOIR_PROCEEDING
 - `JUDGE_CODE`  [join]
      - short code that stands for one immigration judge
      - WATCH: Code AAA is the placeholder All Judges, not a person.
 - `JUDGE_NAME`  [label]
      - the name of the immigration judge behind the code
      - WATCH: Fill not yet measured.

---

## 78) Federal judges own stock in companies that show up as parties in cases assigned to them.  `W77` grade C
   - A judge with money riding on a party should step aside. A match of judge, company and year flags cases where that may not have happened.

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_INVESTMENTS**
one row = one line on one disclosure form
connects: FINANCIAL_DISCLOSURE_ID matches ID on FINANCIAL_DISCLOSURES; DESCRIPTION text-matches COMPANY_NAME on COMPANY_TICKERS_EXCHANGE
 - `DESCRIPTION`  [join]
      - free-text name of the asset the judge listed, such as a company's stock
      - WATCH: Scanned text with typos, AMCRICAN EXPRESS on 167 rows. Rows reading X Bank Accounts are cash, 93% of the wide match. Single-word matches were 8% real.
 - `GROSS_VALUE_CODE`  [measure]
      - letter code for the holding's value, J K L M most common; look at distinct values first
 - `FINANCIAL_DISCLOSURE_ID`  [join]
      - number pointing to the disclosure form this line belongs to
      - WATCH: Fill not yet measured.
 - `TRANSACTION_DATE`  [date]
      - the date on the line, 1969-12-31 to 2022-12-27
      - WATCH: Only 36.09% filled.

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES**
one row = one disclosure form
connects: ID matches FINANCIAL_DISCLOSURE_ID on INVESTMENTS; PERSON_ID matches ASSIGNED_TO_ID on DOCKETS
 - `ID`  [join]
      - the number of this one disclosure form
 - `PERSON_ID`  [join]
      - number for the judge who filed the form, 3,375 different judges
      - WATCH: Only 43.8% filled. More than half the forms cannot be tied to a judge.
 - `YEAR_COL`  [date]
      - meant to be the year the form covers
      - WATCH: 51.3% filled, values run 0 to 14423. Column-shifted text on 38,530 of 70,776 landing rows. Not usable as is.

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS**
one row = one court docket
connects: ASSIGNED_TO_ID matches PERSON_ID on FINANCIAL_DISCLOSURES; IDB_DATA_ID matches ID on FJC_IDB_CL_LINKED
 - `ASSIGNED_TO_ID`  [join]
      - number for the judge the case was assigned to
      - WATCH: Fill not yet measured. Assignment does not show whether the judge stepped aside.
 - `IDB_DATA_ID`  [join]
      - number pointing to the matching federal case record with party names
      - WATCH: Fill not yet measured.
 - `CASE_NAME`  [label]
      - the case caption, such as one party versus another
      - WATCH: Fill not yet measured.
 - `DATE_FILED`  [date]
      - the day the case was filed
      - WATCH: Fill not yet measured.
 - `COURT_ID`  [label]
      - short code for the court where the case sits
      - WATCH: Fill not yet measured.

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED**
one row = one federal case record with its named parties
connects: ID matches IDB_DATA_ID on DOCKETS; PLAINTIFF and DEFENDANT text-match COMPANY_NAME on COMPANY_TICKERS_EXCHANGE
 - `ID`  [join]
      - the number of this one case record
 - `PLAINTIFF`  [join]
      - name of the first party that sued
      - WATCH: First-named party only. Fill not yet measured.
 - `DEFENDANT`  [join]
      - name of the first party being sued
      - WATCH: First-named party only. Fill not yet measured.
 - `DATE_FILED`  [date]
      - the day the case was filed, 1901-01-01 to 2022-03-31
      - WATCH: File stops at 2022-03-31.
 - `NATURE_OF_SUIT`  [filter]
      - coded subject of the lawsuit; coded value, look at distinct values first

**LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE**
one row = one listed ticker
connects: COMPANY_NAME text-matches DESCRIPTION on INVESTMENTS and PLAINTIFF, DEFENDANT or CASE_NAME on the court tables; multi-word names only
 - `COMPANY_NAME`  [join]
      - the official name of a stock-market listed company, 7,920 different names
      - WATCH: Text match only. Single-word names were 8% real in a checked sample; multi-word cleared 92%.
 - `CIK`  [label]
      - the securities regulator's id number for the company
      - WATCH: No matching id exists on the investment side or the docket side.
 - `TICKER`  [label]
      - the stock symbol the company trades under

---

## 79) Lawsuits against a nursing-home chain pile up in federal court before Medicare gets around to fining it.  `W78` grade C
   - It would mean the courts see trouble before the regulator does. Lawsuit counts could then work as an early warning for bad chains.

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL**
one row = one federal civil case
connects: DEFENDANT name-matches CHAIN_NAME or LEGAL_BUSINESS_NAME on NURSING_HOME; multi-word names only, overlap not measured
 - `DEFENDANT`  [join]
      - name of the first party being sued
      - WATCH: First-named party only, so a suit naming the chain second is invisible. Fill not yet measured.
 - `NATURE_OF_SUIT`  [filter]
      - coded subject of the lawsuit; coded value, look at distinct values first
 - `FILE_DATE`  [date]
      - the day the case was filed, 1901-01-01 to 2026-03-31
      - WATCH: Filings stop at 2026-03-31.
 - `DISTRICT`  [label]
      - coded federal court district where the case was filed; look at distinct values first

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on NURSING_HOME_PENALTIES, measured 100%; CHAIN_NAME or LEGAL_BUSINESS_NAME name-matches DEFENDANT on FJC_IDB_CIVIL
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's id number for one nursing home, 14,328 different values on 14,700 rows
 - `CHAIN_ID`  [filter]
      - Medicare's number for the chain the home belongs to
      - WATCH: Blank on 4,551 homes in the sibling roster table. Count the blank share here before grouping.
 - `CHAIN_NAME`  [join]
      - name of the chain the home belongs to
      - WATCH: Chain names include hospital systems. Use multi-word names only.
 - `LEGAL_BUSINESS_NAME`  [join]
      - the legal business name on record for the home

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES**
one row = one penalty on one home
connects: CMS_CERTIFICATION_NUMBER_CCN matches CMS_CERTIFICATION_NUMBER_CCN on NURSING_HOME, measured 100%
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's id number for the penalized nursing home, 6,771 different homes
 - `PENALTY_DATE`  [date]
      - the day the penalty was imposed, 2023-06-17 to 2026-05-13
      - WATCH: Covers under three years, so the before window is short.
 - `PENALTY_TYPE`  [filter]
      - kind of penalty: Fine or Payment Denial
      - WATCH: 2,470 Payment Denial rows have a blank FINE_ID.
 - `FINE_AMOUNT`  [measure]
      - dollar size of the fine on this penalty
      - WATCH: Only rows where PENALTY_TYPE is Fine carry an amount.

---

## 80) Certain mine owners just do not pay their safety fines, and the debts sit open for years.  `W79` grade B
   - A fine nobody collects is not a penalty. $548M of $1.82B proposed was never collected, and the worst operators paid under 10%.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one mine safety citation
connects: MINE_ID matches MINE_ID on MSHA_MINES, measured 31,277 shared values
 - `VIOLATION_NO`  [join]
      - the number printed on this one safety citation
 - `MINE_ID`  [join]
      - the mine safety agency's id number for the mine, 32,133 different mines
 - `CONTROLLER_ID`  [join]
      - id number of the company that controlled the mine when it was cited
      - WATCH: 93.24% filled.
 - `CONTROLLER_NAME`  [label]
      - name of the company that controlled the mine when it was cited
 - `VIOLATION_ISSUE_DATE`  [date]
      - the day the citation was written, 1994-09-09 to 2026-07-18
      - WATCH: The last 24 months are inside the appeal window and were left out of the measured numbers.
 - `PROPOSED_PENALTY`  [measure]
      - dollars the agency proposed as the fine
      - WATCH: 500,990 rows carry the standard $100 minimum fine; that is the rulebook.
 - `AMOUNT_DUE`  [measure]
      - dollars due on the penalty for this citation
 - `AMOUNT_PAID`  [measure]
      - dollars actually paid so far on this citation
      - WATCH: Zero, not null, when unpaid. Use sums.
 - `SIG_SUB`  [filter]
      - Y or N flag on the citation; meaning not given, check before use
 - `NEGLIGENCE`  [filter]
      - how careless the operator was rated: NoNegligence, LowNegligence, ModNegligence, HighNegligence

**LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS**
one row = one citation, all 64 source columns
connects: used alone for timing; shares VIOLATION_NO, MINE_ID and CONTROLLER_ID with the mart copy
 - `VIOLATION_NO`  [join]
      - the number printed on this one safety citation
      - WATCH: Every value carries literal double quotes. Strip them before comparing.
 - `MINE_ID`  [join]
      - the mine safety agency's id number for the mine
      - WATCH: Every value carries literal double quotes.
 - `CONTROLLER_ID`  [join]
      - id number of the company that controlled the mine when cited
      - WATCH: Not profiled. Values carry literal double quotes.
 - `VIOLATION_ISSUE_DT`  [date]
      - the day the citation was written
      - WATCH: Not profiled. Strip quotes before casting to a date.
 - `FINAL_ORDER_ISSUE_DT`  [date]
      - the day the penalty became final and legally owed
      - WATCH: Not the day money arrived. Fill not yet measured. Strip quotes before casting.
 - `BILL_PRINT_DT`  [date]
      - the day the agency printed the bill
      - WATCH: Not a payment date. Fill not yet measured.
 - `LAST_ACTION_CD`  [filter]
      - coded kind of the last action on the penalty; coded value, look at distinct values first
      - WATCH: No code list landed, so whether any code means paid is unknown.
 - `LAST_ACTION_DT`  [date]
      - the day of the last action on the penalty
      - WATCH: Do not treat as a payment date.
 - `CONTESTED_IND`  [filter]
      - flag for whether the penalty was contested; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `CONTESTED_DT`  [date]
      - the day the penalty was contested
      - WATCH: Fill not yet measured.
 - `DOCKET_NO`  [label]
      - the docket number tied to the contested penalty
      - WATCH: Fill not yet measured.
 - `DOCKET_STATUS_CD`  [filter]
      - coded status of that docket; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `VACATE_DT`  [filter]
      - by its name, the day the citation was thrown out
      - WATCH: Thrown-out citations should leave the unpaid count. Fill not yet measured.
 - `PROPOSED_PENALTY`  [measure]
      - dollars the agency proposed as the fine
      - WATCH: Values carry literal double quotes; strip before casting to a number.
 - `AMOUNT_DUE`  [measure]
      - dollars due on the penalty for this citation
      - WATCH: Values carry literal double quotes.
 - `AMOUNT_PAID`  [measure]
      - dollars actually paid so far on this citation
      - WATCH: Zero, not null, when unpaid. Values carry literal double quotes.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES**
one row = one mine
connects: MINE_ID matches MINE_ID on MSHA_VIOLATIONS, measured 31,277 shared values
 - `MINE_ID`  [join]
      - the mine safety agency's id number for the mine
 - `CURRENT_OPERATOR_NAME`  [label]
      - name of the company running the mine today
      - WATCH: Current operator only, not who ran it when cited.
 - `CURRENT_CONTROLLER_ID`  [join]
      - id number of the company that controls the mine today
      - WATCH: 98.88% filled. Current only; use CONTROLLER_ID on the violation row for who ran it then.
 - `STATE`  [label]
      - the state where the mine sits
 - `FIPS_CNTY_CD`  [label]
      - the federal county code for where the mine sits

---

## 81) Employees of the companies paid to run immigration detention give political money to candidates in the states where they hold people.  `W80` grade C
   - It would show contractors buying goodwill exactly where their business depends on local politicians. If giving just follows headquarters or party lines, there is no such pull.

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: RECIPIENT_NAME name-matches EMPLOYER on FEC_INDIV_CONTRIBUTIONS by first 8 letters; PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE equals CAND_OFFICE_ST on FEC_CANDIDATES
 - `RECIPIENT_NAME`  [join]
      - name of the company that got the contract
      - WATCH: Name match only. A name-only join inflated counts 9x. Fill not yet measured.
 - `RECIPIENT_PARENT_NAME`  [label]
      - name of the parent company that owns the contractor
      - WATCH: Fill not yet measured.
 - `RECIPIENT_UEI`  [label]
      - the government's id number for the contractor
      - WATCH: Fill not yet measured.
 - `AWARDING_SUB_AGENCY_NAME`  [filter]
      - the agency office that awarded the contract, used to keep only immigration enforcement work
      - WATCH: Fill not yet measured.
 - `ACTION_DATE`  [date]
      - the day of the contract transaction
      - WATCH: Fill not yet measured.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed on this transaction, a signed number that can be negative
      - WATCH: Signed. Filter to positive amounts.
 - `PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE`  [join]
      - two-letter state where the contract work is done
      - WATCH: Fill not yet measured.

**LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES**
one row = one detention site code
connects: STATE lines up with STATE on ICE_DETENTION_STINTS; no key to a contractor
 - `DETENTION_FACILITY_NAME`  [label]
      - name of the detention site behind the code
 - `STATE`  [join]
      - the state where the detention site sits
 - `COUNTY`  [label]
      - the county where the detention site sits
 - `TYPE_DETAILED`  [filter]
      - kind of site: IGSA, Hospital, USMS IGA, Hold, Unknown and others
      - WATCH: Carries a facility type and no operator. It cannot say which company runs the site.

**LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS**
one row = one person's stay at one detention site
connects: grouped by STATE to count people held per state; no key to a contractor
 - `STINT_ID`  [label]
      - the number of this one stay
 - `DETENTION_FACILITY`  [label]
      - name of the site where the person was held
 - `DETENTION_FACILITY_CODE`  [join]
      - short code for the site where the person was held
      - WATCH: Fill not yet measured.
 - `STATE`  [join]
      - the state where the person was held
      - WATCH: Fill not yet measured.
 - `COUNTY`  [label]
      - the county where the person was held
      - WATCH: Fill not yet measured.
 - `BOOK_IN_AT`  [date]
      - the moment the person was booked in, 2004-12-05 to 2026-03-11
 - `DUPLICATE_DROP_ROW`  [filter]
      - True or False flag, by its name marking a repeated row to drop

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one contribution by one person
connects: EMPLOYER name-matches RECIPIENT_NAME on the contract tables; CMTE_ID matches CMTE_ID on CAND_CMTE_LINKAGE, measured 9,217 shared values
 - `EMPLOYER`  [join]
      - the donor's employer as the donor typed it
      - WATCH: Typed by the donor. First-8-letters match was 0 of 3 false in a small check; name-only join inflated counts 9x.
 - `DONOR_NAME`  [label]
      - the donor's name as typed on the filing
 - `CMTE_ID`  [join]
      - the election commission's id for the committee that got the money
 - `TRANSACTION_DATE`  [date]
      - the day the gift was made
      - WATCH: 99.98% filled. Range reads 0031-04-10 to 9206-07-02, typo dates. Real window not re-measured.
 - `TRANSACTION_AMT`  [measure]
      - dollar amount of this one gift
 - `TRANSACTION_TYPE`  [filter]
      - coded kind of transaction: 15E is a pass-through earmark row; check other codes first
      - WATCH: Exclude 15E earmark pass-through rows.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE**
one row = one candidate-committee link
connects: CMTE_ID matches CMTE_ID on FEC_INDIV_CONTRIBUTIONS, 9,217 shared; CAND_ID matches CAND_ID on FEC_CANDIDATES, 14,768 shared
 - `CMTE_ID`  [join]
      - the election commission's id for a committee
 - `CAND_ID`  [join]
      - the election commission's id for the candidate tied to that committee

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES**
one row = one candidate in one cycle
connects: CAND_ID matches CAND_ID on CAND_CMTE_LINKAGE, 14,768 shared; CAND_OFFICE_ST equals PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE on the contract tables
 - `CAND_ID`  [join]
      - the election commission's id for the candidate
 - `CAND_OFFICE_ST`  [join]
      - two-letter state the candidate is running in
 - `CAND_OFFICE`  [filter]
      - letter code for the office sought, values H, S and P; check meanings before use

---

## 82) Lobbyists pile onto a bill in the months right before it clears committee, and the filings say who paid them.  `W82` grade B
   - It shows which bills money cares about and when the pressure lands. The clients named are the ones trying to shape the bill before it moves.

**LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS**
one row = one lobbying filing
connects: bill number parsed out of SPECIFIC_ISSUES matches BILL_TYPE + BILL_NUMBER + CONGRESS on POLITICS__BILLS; FILING_YEAR pins the Congress
 - `FILING_UUID`  [label]
      - the unique id of this lobbying filing
      - WATCH: Table not profiled; fill not yet measured.
 - `FILING_YEAR`  [date]
      - the year the filing covers, 1999 to 2026
      - WATCH: Needed to pin which Congress a bill number like H.R. 1 belongs to.
 - `FILING_PERIOD`  [date]
      - which reporting period of the year the filing covers
      - WATCH: Filings are quarterly. Nothing finer than a quarter can be shown.
 - `CLIENT_NAME`  [label]
      - the client the lobbying was done for
      - WATCH: Fill not yet measured.
 - `REGISTRANT_NAME`  [label]
      - the lobbying firm or organization that filed the report
      - WATCH: Fill not yet measured.
 - `SPECIFIC_ISSUES`  [join]
      - free text describing what was lobbied on, where bill numbers get mentioned
      - WATCH: Bill number must be parsed from free text. Overlap with the bills table not yet measured.
 - `INCOME`  [measure]
      - lobbying income reported on the filing, in dollars, stored as text
      - WATCH: Text, and only one of INCOME or EXPENSES is filled per filer type. Cast both and add.
 - `EXPENSES`  [measure]
      - lobbying expenses reported on the filing, in dollars, stored as text
      - WATCH: Text, and only one of INCOME or EXPENSES is filled per filer type.

**LIBRARY_MARTS.POLITICS.POLITICS__BILLS**
one row = one bill
connects: CONGRESS + BILL_TYPE + BILL_NUMBER match the bill reference parsed from SPECIFIC_ISSUES; SPONSOR_BIOGUIDE matches BIOGUIDE on MEMBER_SPINE
 - `CONGRESS`  [join]
      - the number of the two-year Congress the bill belongs to
 - `BILL_TYPE`  [join]
      - kind of bill: HR, S, HRES, SRES, HJRES and others
 - `BILL_NUMBER`  [join]
      - the bill's number within its type and Congress
      - WATCH: The same number repeats every Congress, so CONGRESS must be part of the match.
 - `TITLE`  [label]
      - the title of the bill as written
 - `INTRODUCED_DATE`  [date]
      - the day the bill was introduced, 2023-01-03 to 2026-06-26
 - `ADVANCED_PAST_COMMITTEE`  [filter]
      - true or false: did the bill make it out of committee
      - WATCH: There is no markup date. This flag and LATEST_ACTION_DATE are the only signals.
 - `LATEST_ACTION_DATE`  [date]
      - the day of the most recent action on the bill
      - WATCH: Stands in for a markup date that does not exist.
 - `SPONSOR_BIOGUIDE`  [join]
      - Congress's id for the member who sponsored the bill, 634 different members

**LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE**
one row = one member of Congress
connects: BIOGUIDE matches SPONSOR_BIOGUIDE on POLITICS__BILLS
 - `BIOGUIDE`  [join]
      - Congress's id for one member, 99.9% filled
 - `STATE`  [label]
      - the state the member of Congress represents
 - `PARTY`  [label]
      - the member's party, such as Democrat or Republican

---

## 83) Political groups outside the parties pour far more money per registered voter into a few small states.  `W83` grade C
   - It shows where a voter is worth the most to outside money. It could also just show where the political vendors keep their offices.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES**
one row = one itemized expenditure by a 527 group
connects: RECIPIENT_STATE equals STATE_ABBR on FED_EAC_EAVS, after summing A1A per state
 - `ORG_NAME`  [label]
      - name of the political group that spent the money
 - `EIN`  [label]
      - the tax id number of the political group, 3,247 different groups
 - `EXPENDITURE_AMOUNT`  [measure]
      - dollars paid out on this one expenditure
 - `EXPENDITURE_DATE`  [date]
      - the day the money was spent, 2001-01-01 to 2026-08-27
      - WATCH: 99.79% filled.
 - `EXPENDITURE_PURPOSE`  [label]
      - what the group said the money was for
 - `RECIPIENT_STATE`  [join]
      - the state where the payee is located
      - WATCH: Where the payee is, not where the ad ran. A media buyer in Virginia counts as Virginia. Fill not yet measured.

**LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS**
one row = one election jurisdiction in one survey
connects: STATE_ABBR equals RECIPIENT_STATE on IRS527_SCHEDULE_B_EXPENDITURES
 - `STATE_ABBR`  [join]
      - two-letter state of the election jurisdiction
      - WATCH: Wisconsin reports by municipality, 1,851 rows, so state sums must add them all.
 - `FIPSCODE`  [label]
      - the federal place code of the election jurisdiction
      - WATCH: Fill not yet measured.
 - `JURISDICTION_NAME`  [label]
      - name of the election jurisdiction, a county or a municipality
 - `A1A`  [measure]
      - assumed to be total registered voters in the jurisdiction
      - WATCH: No codebook landed, meaning is assumed. Values -99 and -88 are placeholders on 231 rows. One survey vintage, no year.

---

## 84) American firms sign up as agents of a foreign government right before Congress votes on something that country cares about.  `W84` grade C
   - It would show foreign governments hiring help on a schedule set by the vote calendar. That is influence timed to the decision.

**LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK**
one row = one record from the foreign-agent filings
connects: FOREIGN_PRINCIPAL_COUNTRY text-matches the country named in VOTE_DESC on VOTEVIEW_ROLLCALLS; FOREIGN_PRINCIPAL_REGISTRATION_DATE falls within N days before VOTE_DATE
 - `REGISTRATION_NUMBER`  [label]
      - the registration number of one registered foreign agent
      - WATCH: Not one row per agent. One registration number carries 1,281 rows.
 - `REGISTRANT_NAME`  [label]
      - name of the firm registered as the agent
 - `FOREIGN_PRINCIPAL_NAME`  [label]
      - name of the foreign government or body the firm works for
 - `FOREIGN_PRINCIPAL_COUNTRY`  [join]
      - the country of the foreign client
      - WATCH: Text match against vote descriptions; overlap not yet measured.
 - `FOREIGN_PRINCIPAL_REGISTRATION_DATE`  [date]
      - the day the firm registered for that foreign client, 1942-07-03 to 2026-06-11
      - WATCH: Only 17.21% filled. Only dates from 2023 on have votes to meet.
 - `DATE_STAMPED`  [date]
      - the date stamped on the filed document
      - WATCH: Short-form rows keep their date only here.
 - `DOCUMENT_TYPE`  [filter]
      - kind of filing: Exhibit AB, Registration Statement, Supplemental Statement, Short-Form
      - WATCH: Blank on 20,581 of 48,103 rows.

**LIBRARY_RAW.LANDING.FED_FARA_BULK**
one row = one record from the foreign-agent filings, the fuller copy
connects: same match as the mart copy: FOREIGN_PRINCIPAL_COUNTRY to the country in VOTE_DESC, FOREIGN_PRINCIPAL_REGISTRATION_DATE before VOTE_DATE
 - `REGISTRATION_NUMBER`  [label]
      - the registration number of one registered foreign agent
      - WATCH: Not profiled. One registration number can carry many rows.
 - `REGISTRATION_DATE`  [date]
      - by its name, the day the agent itself registered
      - WATCH: Not profiled; fill not yet measured.
 - `REGISTRANT_NAME`  [label]
      - name of the firm registered as the agent
      - WATCH: Not profiled.
 - `FOREIGN_PRINCIPAL_COUNTRY`  [join]
      - the country of the foreign client
      - WATCH: Not profiled; fill not yet measured.
 - `FOREIGN_PRINCIPAL_REGISTRATION_DATE`  [date]
      - the day the firm registered for that foreign client
      - WATCH: Fill not yet measured here; 17.21% on the mart copy.
 - `DATE_STAMPED`  [date]
      - the date stamped on the filed document
      - WATCH: Not profiled.
 - `DOCUMENT_TYPE`  [filter]
      - kind of filing, such as Registration Statement or Short-Form; look at distinct values first
      - WATCH: Not profiled. 221,900 rows against the mart's 48,103; what the mart dropped is unknown.

**LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS**
one row = one roll-call vote
connects: VOTE_DESC keyword filter names the country, matched to FOREIGN_PRINCIPAL_COUNTRY on FARA_BULK; VOTE_DATE compared with FOREIGN_PRINCIPAL_REGISTRATION_DATE
 - `CONGRESS`  [label]
      - the number of the two-year Congress the vote was held in
 - `CHAMBER`  [filter]
      - which chamber voted: House or Senate
 - `ROLLNUMBER`  [label]
      - the number of the roll-call vote within its chamber and Congress
 - `VOTE_DATE`  [date]
      - the day the vote was held, 2023-01-03 to 2026-06-25
      - WATCH: Covers 2023-01-03 to 2026-06-25 only.
 - `BILL_NUMBER`  [label]
      - the bill or measure the vote was about
 - `VOTE_DESC`  [join]
      - free text describing what the vote was on
      - WATCH: No subject code exists. Trade or arms is a keyword list on this text, and the list decides the answer.
 - `VOTE_QUESTION`  [filter]
      - the question put to the chamber on this vote, as text

---

## 85) People who work for a power plant's owner write cheques to the members of Congress from that plant's state who sit on the energy committees.  `W85` grade C
   - If true, plant owners aim their money at the exact lawmakers who oversee them at home. The plant's location would predict who gets paid.

**LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER**
one row = one owner's share of one generator
connects: PLANT_CODE matches PLANT_CODE on EIA860_2_PLANT; OWNER_NAME is name-matched to EMPLOYER on FEC_INDIV_CONTRIBUTIONS
 - `PLANT_CODE`  [join]
      - the federal energy agency's number for one power plant
      - WATCH: Only 2,369 distinct plants here against 15,830 in the plant file; why the rest have no owner row is not measured.
 - `OWNER_NAME`  [join]
      - name of the company that owns a share of the generator
      - WATCH: Name match only, not an id; overlap with EMPLOYER not yet measured.
 - `OWNER_STATE`  [label]
      - state in the owner company's own address, not the plant's state
 - `PERCENT_OWNED`  [measure]
      - what share of the generator this owner holds

**LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT**
one row = one power plant
connects: PLANT_CODE matches PLANT_CODE on EIA860_4_OWNER; STATE equals STATE on MEMBER_FEC_ID
 - `PLANT_CODE`  [join]
      - the federal energy agency's number for one power plant
 - `STATE`  [join]
      - state where the power plant physically sits
 - `COUNTY`  [label]
      - county where the power plant physically sits

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one contribution by one person
connects: EMPLOYER is name-matched to OWNER_NAME on EIA860_4_OWNER; CMTE_ID matches CMTE_ID on CAND_CMTE_LINKAGE
 - `EMPLOYER`  [join]
      - the employer the donor wrote on the contribution form, free text
      - WATCH: Free text typed by donors; a name match, not an id.
 - `CMTE_ID`  [join]
      - election agency id of the campaign committee that got the money
 - `TRANSACTION_DATE`  [date]
      - the day the contribution was made
      - WATCH: Filled 99.98%. Date window on the current table not re-measured; an older 84.2M-row copy was 99.99% 2023-2026.
 - `TRANSACTION_AMT`  [measure]
      - dollar amount of the one contribution
 - `TRANSACTION_TYPE`  [filter]
      - election agency code for the kind of transaction: 15E marks an earmarked contribution, 15 is the other common one

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE**
one row = one candidate-committee link
connects: CMTE_ID matches CMTE_ID on FEC_INDIV_CONTRIBUTIONS; CAND_ID matches FEC_ID on MEMBER_FEC_ID
 - `CMTE_ID`  [join]
      - election agency id of a campaign committee
 - `CAND_ID`  [join]
      - election agency id of the candidate that committee raises money for

**LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID**
one row = one member and one FEC candidate id
connects: FEC_ID matches CAND_ID on CAND_CMTE_LINKAGE; BIOGUIDE matches BIOGUIDE on COMMITTEE_MEMBERSHIP; STATE equals STATE on EIA860_2_PLANT
 - `FEC_ID`  [join]
      - the member's candidate id at the election agency
 - `BIOGUIDE`  [join]
      - Congress's own id for one member, the same across every term
 - `STATE`  [join]
      - the state the member of Congress represents

**LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP**
one row = one committee seat in one Congress
connects: BIOGUIDE matches BIOGUIDE on MEMBER_FEC_ID; COMMITTEE_NAME filtered to energy committees
 - `BIOGUIDE`  [join]
      - Congress's own id for one member, the same across every term
      - WATCH: One row per Congress per seat; joining to money without select distinct multiplied dollars 5.7x. Roster misses 14 to 35 members per Congress, about 4%.
 - `COMMITTEE_NAME`  [filter]
      - name of the committee the member sits on; keep the energy ones
 - `CONGRESS`  [date]
      - number of the two-year Congress the seat belongs to, 113 to 119
 - `SNAPSHOT_DATE`  [date]
      - the day this copy of the committee roster was taken

---

## 86) When complaints about a bank pile up, count how many months pass before a federal regulator hits that bank with an order.  `W86` grade C
   - If true, complaint spikes are an early warning that regulators act on. If not, the two files cover different banks and complaints predict nothing here.

**LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS**
one row = one consumer complaint
connects: COMPANY is name-matched to BANK_NAME or INSTITUTION_NAME on FDIC_ENFORCEMENT_ORDERS, multi-word names only
 - `COMPLAINT_ID`  [label]
      - the consumer bureau's number for one complaint
 - `COMPANY`  [join]
      - name of the company the consumer complained about, as text
      - WATCH: Not a bank id; the table has no bank id of any kind. 8,088 distinct names.
 - `DATE_RECEIVED`  [date]
      - the day the bureau received the complaint, 2011-12-01 to 2026-07-23
 - `RECEIVED_MONTH`  [date]
      - the month the complaint came in, ready for monthly counts
 - `PRODUCT`  [filter]
      - kind of financial product complained about, such as credit reporting or a mortgage
      - WATCH: Three credit bureaus are 77% of complaints and are not banks; filter PRODUCT first.
 - `ISSUE`  [label]
      - what went wrong, in the bureau's own category words
 - `STATE`  [label]
      - state the complaining consumer lives in

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS**
one row = one FDIC enforcement order
connects: BANK_NAME or INSTITUTION_NAME is name-matched to COMPANY on CFPB_COMPLAINTS
 - `ORDER_ID`  [label]
      - the deposit insurer's number for one enforcement order
 - `ORDER_DATE`  [date]
      - the day the order was issued, 1975-06-11 to 2026-07-31
      - WATCH: Filled 99.79%. Orders before 2011-12-01 have no complaint side.
 - `ORDER_TYPE`  [filter]
      - kind of order: cease and desist, civil money penalty, removal of a person, and others
 - `INSTITUTION_NAME`  [join]
      - name of the institution the order is against, as text
      - WATCH: Name match only. Names ending National Association are one entity and must not be split.
 - `BANK_NAME`  [join]
      - name of the bank the order is against, as text
      - WATCH: Name match only. Generic bank names need BANK_STATE to tell apart.
 - `BANK_RSSD_ID`  [label]
      - the Federal Reserve's id number for the bank
      - WATCH: No partner on the complaint side, so it cannot be the join.
 - `CERT_NUMBER`  [label]
      - the deposit insurer's certificate number for the bank
      - WATCH: Filled 97.86%, 4,326 distinct. No partner on the complaint side.
 - `CMP_AMOUNT_TOTAL`  [measure]
      - total dollars of civil money penalty in the order
 - `BANK_STATE`  [filter]
      - state the bank is in; the tiebreak for banks with the same name

---

## 87) Lobbying reports that name an agency climb in the quarter or two before that agency publishes a big rule.  `W87` grade C
   - If true, lobbyists see rules coming and swarm the agency first. The data can only show quarters, never weeks.

**LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS**
one row = one lobbying filing
connects: agency names split out of GOVERNMENT_ENTITIES text are matched to AGENCY on FEDERAL_REGISTER_DOCUMENTS; FILING_YEAR plus FILING_PERIOD lines up with PUBLICATION_QUARTER
 - `FILING_YEAR`  [date]
      - the year the lobbying report covers, 1999 to 2026
      - WATCH: Use this LANDING table; the mart copy stops at FILING_YEAR 2021 and has zero overlap.
 - `FILING_PERIOD`  [date]
      - which quarter of the year the report covers
      - WATCH: Grain is a quarter; by how many weeks cannot be answered.
 - `CLIENT_NAME`  [label]
      - the company or group that paid for the lobbying
 - `GOVERNMENT_ENTITIES`  [join]
      - free-text list of the agencies and chambers the lobbyists contacted
      - WATCH: Free text; needs a hand-built alias list, and a filing naming ten agencies counts toward all ten. Fill not measured.
 - `LOBBYING_ISSUES`  [label]
      - broad topic areas the filing says were lobbied on
 - `SPECIFIC_ISSUES`  [label]
      - free-text description of the bills or rules discussed
      - WATCH: Does not say which rule was discussed; REGULATION_ID_NUMBERS has no partner here.

**LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS**
one row = one Federal Register document
connects: AGENCY is text-matched to agency names inside GOVERNMENT_ENTITIES on FED_SENATE_LDA_FILINGS; PUBLICATION_QUARTER lines up with FILING_YEAR plus FILING_PERIOD
 - `DOCUMENT_NUMBER`  [label]
      - the Federal Register's own number for one published document
 - `AGENCY`  [join]
      - the single agency name the mart built for the document
      - WATCH: Text match; the Federal Register uses its own agency names.
 - `AGENCIES`  [label]
      - the full list of agencies attached to the document
 - `TYPE`  [filter]
      - kind of document: Notice, Rule, Proposed Rule or Presidential Document
 - `PUBLICATION_DATE`  [date]
      - the day the document was printed, 2023-01-03 to 2026-06-16
      - WATCH: Only 2023-01-03 to 2026-06-16 on the mart, a short series for any lead-lag claim.
 - `PUBLICATION_QUARTER`  [join]
      - the calendar quarter the document was printed in, built by the mart
 - `IS_SIGNIFICANT`  [filter]
      - true when the rule was flagged significant; blank on about 90% of rows
 - `REGULATION_ID_NUMBERS`  [label]
      - the government's tracking numbers for the rule behind the document
      - WATCH: No partner on the lobbying side.

**LIBRARY_RAW.LANDING.FED_FEDERAL_REGISTER_DOCUMENTS**
one row = one Federal Register document, the fuller copy
connects: AGENCY_NAMES is text-matched to agency names inside GOVERNMENT_ENTITIES on FED_SENATE_LDA_FILINGS
 - `DOCUMENT_NUMBER`  [label]
      - the Federal Register's own number for one published document
 - `AGENCIES`  [label]
      - the full list of agencies attached to the document
 - `AGENCY_NAMES`  [join]
      - the agency names on the document as text; this copy has no AGENCY column
      - WATCH: Fill not measured. This table has no AGENCY, IS_SIGNIFICANT or PUBLICATION_QUARTER column.
 - `TYPE`  [filter]
      - kind of document, such as a rule or notice; coded value, look at distinct values first
 - `PUBLICATION_DATE`  [date]
      - the day the document was printed
      - WATCH: Date range not yet measured; 485,594 rows against the mart's 94,731. Measure min and max before choosing the table.
 - `SIGNIFICANT`  [filter]
      - raw flag for whether the rule was marked significant
 - `REGULATION_ID_NUMBERS`  [label]
      - the government's tracking numbers for the rule behind the document

---

## 88) The law firm a judge used to work at keeps showing up as counsel in that judge's own cases.  `W88` grade C
   - If true, old colleagues argue in front of their former partner more than chance allows. That is a lead on conflicts, not proof of one.

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS**
one row = one job held by one judge
connects: PERSON_ID matches ASSIGNED_TO_ID on DOCKETS; ORGANIZATION_NAME is text-matched inside ATTORNEYS on OPINION_CLUSTERS
 - `PERSON_ID`  [join]
      - the court database's id for one judge, 15,524 distinct
 - `POSITION_TYPE`  [filter]
      - coded kind of job, values like jud, prac, trial-jud; filled on about 59% of rows; check distinct values
 - `SECTOR`  [filter]
      - coded value, look at distinct values first; filled on only about 13% of rows
 - `ORGANIZATION_NAME`  [join]
      - name of the firm, school or office where the job was held
      - WATCH: Text match, multi-word firm names only. Firms rename and merge, so the old name misses later names.
 - `DATE_START`  [date]
      - the day the judge started that job
      - WATCH: Not profiled; fill not measured.
 - `DATE_TERMINATION`  [date]
      - the day the judge left that job; compare it with the case date
 - `LOCATION_STATE`  [label]
      - state where the job was located

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS**
one row = one court docket
connects: ASSIGNED_TO_ID matches PERSON_ID on POSITIONS; ID matches DOCKET_ID on OPINION_CLUSTERS
 - `ID`  [join]
      - the court database's id for one docket, meaning one case file
 - `ASSIGNED_TO_ID`  [join]
      - id of the judge the case was assigned to
      - WATCH: Fill not measured; an earlier note counts 3,350 judges on this column.
 - `DATE_FILED`  [date]
      - the day the case was filed
 - `COURT_ID`  [filter]
      - short code for the court hearing the case

**LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS**
one row = one decided opinion group
connects: DOCKET_ID matches ID on DOCKETS; ATTORNEYS text is searched for ORGANIZATION_NAME from POSITIONS
 - `DOCKET_ID`  [join]
      - id of the docket this opinion belongs to
 - `ATTORNEYS`  [join]
      - free-text block naming the lawyers and firms on the case
      - WATCH: Fill not measured; count it by year before anything else. Only cases with an opinion have it.
 - `DATE_FILED`  [date]
      - the day the opinion was filed
      - WATCH: Typo dates run 0019-01-31 to 2028-04-13; bound dates before use.

---

## 89) Count which government offices lobbyists most often write down as the job they used to hold.  `W89` grade B
   - It shows which agencies and congressional offices feed the lobbying trade. A clear top tier is a map of the revolving door.

**LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS**
one row = one lobbyist on one filing
connects: agency keywords found in COVERED_POSITION are loosely matched to AGENCY on REVOLVINGDOOR_PROJECT, as a label only
 - `LOBBYIST_ID`  [measure]
      - the Senate lobbying system's id for one lobbyist; count these, not rows
      - WATCH: The same lobbyist repeats across filings and quarters; count distinct.
 - `LOBBYIST_FIRST_NAME`  [label]
      - first name of the lobbyist on the filing
 - `LOBBYIST_LAST_NAME`  [label]
      - last name of the lobbyist on the filing
 - `COVERED_POSITION`  [filter]
      - free text where the lobbyist writes the government job they used to hold
      - WATCH: Fill not measured. In 1999, 205,142 of 213,881 rows hold the literal 'N/A'; null out 'N/A', 'n/a', 'NA', 'NONE' and 'See prior filing' first.
 - `HAS_COVERED_POSITION`  [filter]
      - true when the past-job box is not empty, junk text included
      - WATCH: A not-null test only; old years fill the blank with text like 'N/A', so true does not mean a real job.
 - `REGISTRANT_NAME`  [label]
      - the lobbying firm that filed the report
 - `CLIENT_NAME`  [label]
      - the company or group that paid for the lobbying
 - `FILING_YEAR`  [date]
      - the year the lobbying report covers
      - WATCH: Profile shows every row as 2011; a later note counts 213,881 rows for 1999 alone. Count rows per year first.

**LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT**
one row = one government job slot
connects: AGENCY is loosely matched to agency keywords in COVERED_POSITION on LDA_LOBBYIST_POSITIONS; job text to job slot, not person to person
 - `AGENCY`  [join]
      - the agency the job slot belongs to
      - WATCH: No person names and no year; it can label an agency, not confirm a person held a job.
 - `POSITION_NAME`  [label]
      - title of the government job slot
 - `POSITION_TYPE`  [label]
      - how the job is filled: Appointive or Senate-confirmed
 - `INDUSTRY_SECTOR`  [label]
      - the industry this job slot oversees or touches
 - `IS_SENATE_CONFIRMED`  [filter]
      - true when the job needs a Senate vote, 190 of 405 rows

---

## 90) Counties where immigration agents send more hold requests to local jails also see federal detention contract money grow.  `W90` grade B
   - If true, detention spending chases enforcement county by county. If not, the beds are bought where they already sit.

**LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETAINERS**
one row = one detainer request
connects: DETENTION_FACILITY_CODE matches DETENTION_FACILITY_CODE on ICE_DETENTION_FACILITY_CODES
 - `DETAINER_PREPARE_DATE`  [date]
      - the day the hold request was written, 2022-10-01 to 2026-08-25
      - WATCH: Only FY2023 to FY2026 overlap the contracts, and FY2026 is partial on both sides.
 - `DETENTION_FACILITY_CODE`  [join]
      - code of the immigration detention site tied to the request
      - WATCH: Fill not measured. It names the site tied to the request, not a contract.
 - `FACILITY_STATE`  [label]
      - state of the jail or facility the request was sent to
 - `DUPLICATE_LIKELY`  [filter]
      - True when the row is probably a repeat of another request; drop those

**LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES**
one row = one detention site code
connects: DETENTION_FACILITY_CODE matches DETENTION_FACILITY_CODE on ICE_DETAINERS; COUNTY plus STATE is name-matched to COUNTYNAME plus STATE on FED_CENSUS_COUNTY_2020
 - `DETENTION_FACILITY_CODE`  [join]
      - code of one immigration detention site
 - `COUNTY`  [join]
      - county name of the detention site, as text
      - WATCH: A name, not a code. Names repeat across states and spell Saint several ways; match on state plus name and expect dropped rows.
 - `STATE`  [join]
      - state where the detention site sits
 - `TYPE_DETAILED`  [filter]
      - kind of detention site: top values are IGSA, Hospital, USMS IGA, Hold and Unknown
      - WATCH: A type only; no operator or contract column ties a site to a contract.

**LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020**
one row = one county
connects: COUNTYNAME plus STATE is name-matched to COUNTY plus STATE on ICE_DETENTION_FACILITY_CODES; STATEFP joined to COUNTYFP equals PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on the contract tables
 - `STATE`  [join]
      - the state the county is in
      - WATCH: Table not profiled.
 - `STATEFP`  [join]
      - two-digit census number for the state
 - `COUNTYFP`  [join]
      - three-digit census number for the county inside its state
 - `COUNTYNAME`  [join]
      - name of the county as the census writes it

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE equals STATEFP joined to COUNTYFP on FED_CENSUS_COUNTY_2020
 - `AWARDING_SUB_AGENCY_NAME`  [filter]
      - the bureau inside the department that signed the contract; keep the immigration enforcement one
 - `PRODUCT_OR_SERVICE_CODE`  [filter]
      - federal code for what was bought; coded value, look at distinct values first
 - `ACTION_DATE`  [date]
      - the day this contract transaction was signed
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars this transaction added or took away; can be negative
 - `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`  [join]
      - five-digit census code of the county where the work is done
      - WATCH: Filled on 93% of FY2024 rows, 2,894 distinct counties; other years not measured. The 36-column contracts view has no county code.

---

## 91) Find the immigration judges who order people deported far more or far less often than the other judges in their own courthouse.  `W91` grade B
   - If true, the outcome of a case depends on which judge a person draws. If judges sit close together, the gap is between courts instead.

**LIBRARY_RAW.LANDING.FED_EOIR_PROCEEDING**
one row = one proceeding in one immigration case
connects: IJ_CODE matches JUDGE_CODE on FED_EOIR_JUDGE
 - `IJ_CODE`  [join]
      - short code for the immigration judge who heard the proceeding
      - WATCH: 33,135 rows carry a code absent from the judge table. Code AAA is the placeholder All Judges; exclude it.
 - `BASE_CITY_CODE`  [filter]
      - code for the court city the case was heard in
      - WATCH: No lookup table of city names is landed.
 - `DEC_CODE`  [measure]
      - code for what the judge decided; coded value, look at distinct values first
      - WATCH: Blank three ways: NULL 5.32M rows, NUL byte 1.45M, single space 729K. A plain not-null filter keeps 2.18M empty rows. No code lookup is landed.
 - `DEC_TYPE`  [filter]
      - coded value for the kind of decision, look at distinct values first
 - `COMP_DATE`  [date]
      - the day the proceeding was completed
 - `NAT`  [filter]
      - code for the person's nationality; hold it constant when comparing judges
 - `CASE_TYPE`  [filter]
      - coded value for the kind of case, look at distinct values first
 - `CUSTODY`  [filter]
      - coded value for whether the person was detained, look at distinct values first
 - `ABSENTIA`  [filter]
      - flag for a decision made when the person did not show up; look at distinct values first

**LIBRARY_RAW.LANDING.FED_EOIR_JUDGE**
one row = one judge code in the EOIR lookup
connects: JUDGE_CODE matches IJ_CODE on FED_EOIR_PROCEEDING
 - `JUDGE_CODE`  [join]
      - short code for one immigration judge
      - WATCH: Code AAA is the placeholder All Judges; exclude it.
 - `JUDGE_NAME`  [label]
      - the name of the immigration judge
 - `BLNACTIVE`  [filter]
      - flag for whether the judge is still active; look at distinct values first

---

## 92) Some federal agencies hand a much bigger slice of their contract dollars to foreign-owned companies than the government as a whole does.  `W92` grade B
   - If true, a few agencies lean on foreign firms far more than the rest. It shows share of dollars, never who lost the bid.

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: AWARDING_AGENCY_CODE matches TOPTIER_CODE on TOPTIER_AGENCIES, for the label only
 - `RECIPIENT_UEI`  [label]
      - the government's unique id for the company that got the contract
 - `RECIPIENT_NAME`  [label]
      - name of the company that got the contract
 - `RECIPIENT_PARENT_NAME`  [label]
      - name of the parent company that owns the recipient
 - `RECIPIENT_COUNTRY_NAME`  [label]
      - country in the recipient company's address
 - `FOREIGN_OWNED`  [filter]
      - flag saying the company is foreign-owned; look at distinct values first
      - WATCH: Fill not measured; two flags in this warehouse exist and are empty. Count distinct values per year first.
 - `DOMESTIC_OR_FOREIGN_ENTITY`  [filter]
      - text saying whether the company is a domestic or a foreign business
      - WATCH: Fill not measured; count distinct values per year, blanks included, before anything else.
 - `DOMESTIC_OR_FOREIGN_ENTITY_CODE`  [filter]
      - short code behind the domestic-or-foreign text; coded value, look at distinct values first
 - `AWARDING_AGENCY_CODE`  [join]
      - code of the department or agency that signed the contract
      - WATCH: Codes from 2007 may not all be in the fiscal 2026 agency lookup.
 - `AWARDING_AGENCY_NAME`  [label]
      - name of the department or agency that signed the contract
 - `NUMBER_OF_OFFERS_RECEIVED`  [measure]
      - how many bids came in for the award; losing bidders are not named
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars this transaction added or took away; can be negative
      - WATCH: Signed money. Sum this, never CURRENT_TOTAL_VALUE_OF_AWARD.
 - `ACTION_DATE`  [date]
      - the day this contract transaction was signed

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES**
one row = one top-tier agency
connects: TOPTIER_CODE matches AWARDING_AGENCY_CODE on the contract tables
 - `TOPTIER_CODE`  [join]
      - code for one top-level department or agency
      - WATCH: Fiscal 2026 list only, 111 agencies; overlap not measured.
 - `AGENCY_NAME`  [label]
      - plain name of the department or agency
 - `OBLIGATED_AMOUNT`  [measure]
      - total dollars the agency committed in fiscal 2026

---

## 93) Some political groups registered with the tax agency share the exact same street address and suite as a registered federal campaign money committee.  `W95` grade B
   - If true, two groups with different names may be run out of one office by the same people. Most shared addresses will just be the paperwork vendor.

**LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS**
one row = one 527 registration notice
connects: cleaned MAILING_ADDR1 plus first five digits of MAILING_ZIP equals cleaned CMTE_ST1 plus first five digits of CMTE_ZIP on FED_FEC_COMMITTEES
 - `FORM_ID_NUMBER`  [label]
      - the tax agency's number for one registration notice
 - `EIN`  [label]
      - the group's federal tax id number, 58,251 distinct
      - WATCH: Amended notices repeat an organization; dedupe on EIN.
 - `ORGANIZATION_NAME`  [label]
      - name of the political group on the notice
 - `MAILING_ADDR1`  [join]
      - street line of the group's mailing address, suite included
      - WATCH: A bare building address clusters unrelated tenants; keep the suite and treat many-tenant addresses as a vendor.
 - `MAILING_CITY`  [label]
      - city of the group's mailing address
 - `MAILING_STATE`  [label]
      - state of the group's mailing address
 - `MAILING_ZIP`  [join]
      - ZIP code of the mailing address; use the first five digits
 - `ESTABLISHED_DATE`  [date]
      - the day the group says it was set up
      - WATCH: Filled 91.21%. Typo dates start at 1808-01-01; bound before charting.
 - `CUSTODIAN_NAME`  [label]
      - the person who keeps the group's records

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES**
one row = one committee in one cycle file
connects: cleaned CMTE_ST1 plus first five digits of CMTE_ZIP equals cleaned MAILING_ADDR1 plus first five digits of MAILING_ZIP on IRS527_8871_ORGS; dedupe on CMTE_ID first
 - `CMTE_ID`  [join]
      - election agency id of one committee
      - WATCH: Repeats across cycles: 60,031 rows hold 37,886 distinct ids, 16,943 repeated, no cycle column. Dedupe first.
 - `CMTE_NM`  [label]
      - name of the campaign money committee
 - `CMTE_ST1`  [join]
      - street line of the committee's address, suite included
 - `CMTE_CITY`  [label]
      - city in the committee's registered address
 - `CMTE_ST`  [label]
      - state in the committee's registered address
 - `CMTE_ZIP`  [join]
      - ZIP code of the committee's address; use the first five digits
      - WATCH: Reads 100% filled but 50 rows are blank strings.
 - `CMTE_TP`  [filter]
      - one-letter committee type; top values H, N, Q, O, S; coded value, look at distinct values first
 - `TRES_NM`  [label]
      - name of the person serving as committee treasurer

---

## 94) Neighborhoods marked hazardous on 1930s federal lending maps got declared short of family doctors sooner than the neighborhoods graded best.  `W96` grade C
   - If true, a ninety-year-old lending map still predicts where doctors are scarce. Only the point-inside-the-shape test can say it is the same neighborhood.

**LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY**
one row = one graded polygon on one city's map; the full map
connects: FIPS matches STATE_COUNTY_FIPS_CODE on HPSA_PRIMARY_CARE if filled and county-level; finer: LATITUDE and LONGITUDE from HPSA_PRIMARY_CARE fall inside GEOMETRY; fallback: CITY plus STATE name-matched to HPSA_CITY plus STATE_ABBREVIATION
 - `CITY`  [join]
      - the city whose lending map the shape comes from
 - `STATE`  [join]
      - the state that mapped city is in
 - `FIPS`  [join]
      - a census place code for the mapped area; level not stated
      - WATCH: Fill not measured, and whether it is a county or place code is unstated. On the mart the same column is blank on every row. Count it first.
 - `HOLC_GRADE`  [filter]
      - the 1930s lending grade letter; D is the hazardous grade, A and B the good ones
      - WATCH: 814 grades are blank and there are 3 trailing-space spellings; trim first. HOLC_ID is one distinct value, not an id.
 - `YEAR_MAPPED`  [date]
      - the year the lending map was drawn
      - WATCH: Not profiled.
 - `GEOMETRY`  [join]
      - the outline of the graded neighborhood as map shape text
      - WATCH: Parsed on 10,153 of 10,154 rows.
 - `LAT`  [label]
      - latitude of a point for the graded shape
 - `LON`  [label]
      - longitude of a point for the graded shape

**LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY**
one row = one merged polygon per city and grade; not used for counts
connects: none usable
 - `FIPS`  [join]
      - meant to be a census place code, but empty here
      - WATCH: Blank string on all 1,155 rows. The mart covers 11% of the map; use the landing table for counts.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE**
one row = one component of one shortage-area designation
connects: STATE_COUNTY_FIPS_CODE matches FIPS on LANDING.FED_MAPPING_INEQUALITY; or LATITUDE and LONGITUDE point inside its GEOMETRY; or HPSA_CITY plus STATE_ABBREVIATION name-matched to CITY plus STATE
 - `HPSA_ID`  [label]
      - the health agency's id for one doctor-shortage designation
 - `HPSA_NAME`  [label]
      - name of the shortage area or facility
 - `DESIGNATION_TYPE`  [filter]
      - kind of shortage designation: a population group, a geographic area, a clinic or a facility
 - `DESIGNATION_DATE`  [date]
      - the day the place was declared short of primary-care doctors
      - WATCH: Minimum is 1970-01-01, which may be a default; count rows on that exact day first.
 - `WITHDRAWN_DATE`  [date]
      - the day the designation was taken away, if it was
      - WATCH: Filled 61.28%.
 - `STATE_COUNTY_FIPS_CODE`  [join]
      - five-digit census code for the county, 3,269 distinct
      - WATCH: A county match cannot say the designated area is the redlined area.
 - `HPSA_CITY`  [join]
      - city where the shortage area sits
 - `STATE_ABBREVIATION`  [join]
      - two-letter state of the shortage area
 - `LATITUDE`  [join]
      - latitude of the shortage area's point
      - WATCH: Fill not measured.
 - `LONGITUDE`  [join]
      - longitude of the shortage area's point
      - WATCH: Fill not measured.
 - `COMPONENT_TYPE_DESCRIPTION`  [filter]
      - what size of place the row covers: Census Tract, County Subdivision, Single County or Unknown

---

## 95) Find people who turn up as a licensed doctor, a political donor, a nursing home owner and a federal contractor all at the same ZIP code.  `W97` grade C
   - If true, one person holds several seats in the health money machine at once. Without a shared person id, every match is a lead to hand-check.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES**
one row = one provider id
connects: last name plus first name plus five-digit ZIP is name-matched to LAST_NAME_OWNER, FIRST_NAME_OWNER, ZIP_CODE_OWNER on FED_CMS_SNF_OWNERSHIP, to DONOR_NAME plus ZIP_CODE on FEC_INDIV_CONTRIBUTIONS, and to RECIPIENT_NAME plus RECIPIENT_ZIP_4_CODE on the contract tables
 - `NPI`  [label]
      - the national id number every licensed health provider gets
      - WATCH: The provider file's EIN column is '<UNAVAIL>' on every populated row; no id links a doctor to a company, donor or contractor.
 - `PROVIDER_LAST_NAME_LEGAL_NAME`  [join]
      - the provider's legal last name, as registered
      - WATCH: Single-word name matches were 8% real; use first plus last plus ZIP and hand-check.
 - `PROVIDER_FIRST_NAME`  [join]
      - the provider's first name, as registered
 - `PROVIDER_CREDENTIAL_TEXT`  [filter]
      - letters after the name, such as MD or DO, as typed
 - `PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE`  [join]
      - ZIP code of the office where the provider practices; use the first five digits
      - WATCH: A practice ZIP, a donor's home ZIP and an owner's business ZIP are often three different ZIPs for one person.
 - `ENTITY_TYPE_CODE`  [filter]
      - 1 is a single person, 2 is an organization; keep 1

**LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP**
one row = one owner in one role on one nursing-home enrollment
connects: LAST_NAME_OWNER plus FIRST_NAME_OWNER plus ZIP_CODE_OWNER is name-matched to NPPES name plus ZIP; ENROLLMENT_ID matches ENROLLMENT_ID on SNF_ENROLLMENTS
 - `ENROLLMENT_ID`  [join]
      - Medicare's id for one nursing home's enrollment
      - WATCH: 288,550 of 295,083 owner rows join; 6,533 name enrollments the snapshot does not carry.
 - `FIRST_NAME_OWNER`  [join]
      - first name of the owner, when the owner is a person
 - `LAST_NAME_OWNER`  [join]
      - last name of the owner, when the owner is a person
 - `ROLE_TEXT_OWNER`  [label]
      - the owner's role in words; coded text, look at distinct values first
 - `ZIP_CODE_OWNER`  [join]
      - ZIP code of the owner's address
      - WATCH: Not profiled; fill not measured.
 - `PERCENTAGE_OWNERSHIP`  [measure]
      - what share of the nursing home this owner holds
 - `TYPE_OWNER`  [filter]
      - marks the owner as an individual or an organization; count the values first

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS**
one row = one nursing-home Medicare enrollment
connects: ENROLLMENT_ID matches ENROLLMENT_ID on FED_CMS_SNF_OWNERSHIP, which leads to CCN
 - `ENROLLMENT_ID`  [join]
      - Medicare's id for one nursing home's enrollment
 - `CCN`  [label]
      - Medicare's certification number for the nursing home building, 14,026 distinct

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS**
one row = one owner in one role on one home health enrollment
connects: FIRST_NAME_OWNER plus LAST_NAME_OWNER plus ZIP_CODE_OWNER is name-matched to NPPES name plus ZIP
 - `FIRST_NAME_OWNER`  [join]
      - first name of the owner, when the owner is a person
 - `LAST_NAME_OWNER`  [join]
      - last name of the owner, when the owner is a person
 - `ZIP_CODE_OWNER`  [join]
      - ZIP code of the owner's address
      - WATCH: Filled on only 20.93% of rows.
 - `ROLE_TEXT_OWNER`  [label]
      - the owner's role in words: corporate director, corporate officer, 5% or greater owner, managing employee

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one contribution by one person
connects: DONOR_NAME plus ZIP_CODE is name-matched to NPPES name plus five-digit ZIP
 - `DONOR_NAME`  [join]
      - the donor's full name as one text string
      - WATCH: Name match only; a common surname in one ZIP is many people.
 - `OCCUPATION`  [filter]
      - the job the donor wrote on the form, free text
 - `ZIP_CODE`  [join]
      - the donor's ZIP code, usually home
      - WATCH: Reads 100% filled but 321,021 rows are blank strings.
 - `TRANSACTION_AMT`  [measure]
      - dollar amount of the one contribution

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: RECIPIENT_NAME plus RECIPIENT_ZIP_4_CODE is name-matched to NPPES name plus five-digit ZIP
 - `RECIPIENT_NAME`  [join]
      - name of whoever got the contract, almost always a company
      - WATCH: Fill not measured. Recipients are almost all companies; this leg mostly finds sole proprietors and named practices.
 - `RECIPIENT_ZIP_4_CODE`  [join]
      - the recipient's ZIP code with the four-digit add-on; use the first five digits
      - WATCH: Fill not measured.

---

## 96) Companies and people named in the big offshore tax haven leaks also turn up getting paid on US federal contracts.  `W98` grade C
   - If true, taxpayers are paying firms that keep shell companies offshore. Being in the leaks is not wrongdoing, so a match is a lead and nothing more.

**LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES**
one row = one offshore entity
connects: NAME is name-matched to RECIPIENT_NAME or RECIPIENT_PARENT_NAME on the contract tables, multi-word names only; filter COUNTRY_CODES to those containing USA
 - `NODE_ID`  [label]
      - the leak database's id for one offshore company
 - `NAME`  [join]
      - name of the offshore company in the leak
      - WATCH: Fill not measured. Single-word matches were 8% real; multi-word names cleared 92%.
 - `FORMER_NAME`  [label]
      - an earlier name the offshore company used
 - `JURISDICTION`  [label]
      - the tax haven where the company was registered
 - `INCORPORATION_DATE`  [date]
      - the day the offshore company was set up
      - WATCH: Filled 96.82%. Typo dates run 0199-04-25 to 2812-12-18; bound before any before-and-after test.
 - `COUNTRY_CODES`  [filter]
      - country codes tied to the company; keep rows containing USA
 - `SOURCE_LEAK`  [label]
      - which leak the record came from: Panama Papers, Bahamas Leaks, Offshore Leaks, Paradise Papers
      - WATCH: The eight copies in the warehouse were one snapshot; use this mart and do not count others as extra vintages.

**LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS**
one row = one officer or shareholder
connects: NAME is name-matched to HIGHLY_COMPENSATED_OFFICER_1_NAME on the contract tables; filter COUNTRY_CODES to those containing USA
 - `NODE_ID`  [label]
      - the leak database's id for one officer or shareholder
 - `NAME`  [join]
      - name of the officer or shareholder
      - WATCH: No year and no US place on officers; common names are many people.
 - `COUNTRY_CODES`  [filter]
      - country codes tied to the person; keep rows containing USA
 - `SOURCE_LEAK`  [label]
      - which leak the record came from

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: RECIPIENT_NAME or RECIPIENT_PARENT_NAME is name-matched to NAME on ICIJ ENTITIES; HIGHLY_COMPENSATED_OFFICER_1_NAME is name-matched to NAME on ICIJ OFFICERS
 - `RECIPIENT_NAME`  [join]
      - name of the company that got the contract
      - WATCH: Fill not measured.
 - `RECIPIENT_PARENT_NAME`  [join]
      - name of the parent company that owns the recipient
 - `RECIPIENT_UEI`  [label]
      - the government's unique id for the company that got the contract
 - `RECIPIENT_COUNTRY_NAME`  [filter]
      - country in the recipient company's address
 - `HIGHLY_COMPENSATED_OFFICER_1_NAME`  [join]
      - name of the recipient's top-paid executive, as reported
 - `ACTION_DATE`  [date]
      - the day this contract transaction was signed
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars this transaction added or took away; can be negative

---

## 97) Some people who run or sit on the board of a nonprofit hospital are also company insiders who file stock reports at a listed company.  `W99` grade C
   - If true, the same person sits on both sides of the table when a hospital buys from that company. The data shows both seats, not the purchase.

**LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY**
one row = one person on one hospital tax return
connects: PERSON_NAME is name-matched to OWNER_NAME on INSIDER_REPORTINGOWNER, with HOSPITAL_STATE equal to STATE
 - `EIN`  [label]
      - the hospital's federal tax id number, 3,962 distinct
 - `HOSPITAL_NAME`  [label]
      - name of the nonprofit hospital that filed the return
 - `HOSPITAL_STATE`  [join]
      - state of the hospital; the only tiebreak for the name match
 - `PERSON_NAME`  [join]
      - name of the officer, trustee or top-paid employee on the return
      - WATCH: Name formats on the two sides have not been compared; require first name, last name and state to agree.
 - `TITLE`  [label]
      - the person's job title at the hospital
 - `IS_OFFICER`  [filter]
      - true when the return lists the person as an officer
 - `IS_TRUSTEE_OR_DIRECTOR`  [filter]
      - true when the person sits on the hospital's board
 - `IS_SCHEDULE_J_POINTER`  [filter]
      - true on extra lines that only restate pay; keep false
      - WATCH: Pointer lines restate pay; filter to false.
 - `IS_GROUP_RETURN`  [filter]
      - true when the return covers a group of affiliates; keep false
      - WATCH: An executive repeats on every affiliate's return; filter to false and count each person once per TAX_YEAR.
 - `TAX_YEAR`  [date]
      - the tax year of the return, 2016 to 2025
      - WATCH: Tax years before 2017 are absent from the officer source.
 - `TOTAL_COMPENSATION`  [measure]
      - total dollars the hospital paid the person that year

**LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER**
one row = one reporting owner on one insider filing
connects: OWNER_NAME is name-matched to PERSON_NAME on HOSPITAL_OFFICER_PAY, with STATE equal to HOSPITAL_STATE; ACCESSION_NUMBER matches ACCESSION_NUMBER on INSIDER_SUBMISSION
 - `ACCESSION_NUMBER`  [join]
      - the securities regulator's number for one filing
 - `OWNER_CIK`  [label]
      - the securities regulator's id for the insider, 139,905 distinct
 - `OWNER_NAME`  [join]
      - name of the insider who filed the stock report
      - WATCH: Name match only; single-word or very common names are noise.
 - `RELATIONSHIP`  [filter]
      - the insider's tie to the company: Officer, Director, TenPercentOwner, or a mix
 - `TITLE`  [label]
      - the insider's job title at the listed company
 - `STATE`  [join]
      - state in the insider's address; the tiebreak for the name match

**LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION**
one row = one insider filing
connects: ACCESSION_NUMBER matches ACCESSION_NUMBER on INSIDER_REPORTINGOWNER, which leads to ISSUER_CIK and ISSUER_NAME
 - `ACCESSION_NUMBER`  [join]
      - the securities regulator's number for one filing
 - `FILING_DATE`  [date]
      - the day the insider report was filed, 2016-07-01 to 2025-03-31
 - `ISSUER_CIK`  [label]
      - the securities regulator's id for the listed company, 10,676 distinct
 - `ISSUER_NAME`  [label]
      - name of the listed company the insider belongs to
      - WATCH: Only listed companies appear; private companies file no insider reports.
 - `ISSUER_TICKER`  [label]
      - the listed company's stock ticker symbol

---

## 98) Campaign cheques to a sitting member of Congress bunch up in the seven days right before that member casts a vote.  `M-056` grade B
   - If true, donors time their money to the floor schedule, not the fundraising calendar. It says nothing about what the vote was on.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one contribution by one person
connects: CMTE_ID matches CMTE_ID on CAND_CMTE_LINKAGE
 - `CMTE_ID`  [join]
      - election agency id of the campaign committee that got the money, 40,294 distinct
 - `TRANSACTION_DATE`  [date]
      - the day the contribution was made
      - WATCH: Typo dates run 0031-04-10 to 9206-07-02 and 51,555 rows do not parse; bound the dates. Filled 99.98%.
 - `TRANSACTION_AMT`  [measure]
      - dollar amount of the one contribution
 - `TRANSACTION_TYPE`  [filter]
      - election agency code for the kind of transaction: 15E marks an earmarked contribution, 15 is the other common one
      - WATCH: Exclude earmark rows, TRANSACTION_TYPE 15E.
 - `EMPLOYER`  [label]
      - the employer the donor wrote on the contribution form, free text

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE**
one row = one candidate-committee link
connects: CMTE_ID matches CMTE_ID on FEC_INDIV_CONTRIBUTIONS; CAND_ID matches flattened FEC_IDS on MEMBER_CROSSWALK
 - `CMTE_ID`  [join]
      - election agency id of a campaign committee
 - `CAND_ID`  [join]
      - election agency id of the candidate that committee raises money for
 - `CMTE_TP`  [filter]
      - one-letter committee type; top values H, P, S, N, Q; coded value, look at distinct values first
 - `CMTE_DSGN`  [filter]
      - one-letter committee role; top values P, A, J, U, D; coded value, look at distinct values first

**LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK**
one row = one member of Congress, all id systems
connects: flattened FEC_IDS matches CAND_ID on CAND_CMTE_LINKAGE; ICPSR matches ICPSR on VOTEVIEW_VOTES
 - `FEC_IDS`  [join]
      - list of every election agency candidate id the member has used
      - WATCH: An array; must be flattened before joining. Fill not measured.
 - `ICPSR`  [join]
      - the vote-record project's id number for one member
      - WATCH: Filled 96.12%.
 - `BIOGUIDE`  [label]
      - Congress's own id for one member, the same across every term

**LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES**
one row = one member's vote on one roll call
connects: ICPSR matches ICPSR on MEMBER_CROSSWALK; CONGRESS plus CHAMBER plus ROLLNUMBER matches the same three on VOTEVIEW_ROLLCALLS
 - `ICPSR`  [join]
      - the vote-record project's id number for one member, 639 distinct
      - WATCH: The book counts 1.07M votes reaching 635 members; the table holds 945,523 rows and 639 ids. Recount before quoting.
 - `CONGRESS`  [join]
      - number of the two-year Congress, 118 or 119 here
      - WATCH: Two Congresses only, 118 and 119.
 - `CHAMBER`  [join]
      - which chamber held the vote: House or Senate
 - `ROLLNUMBER`  [join]
      - the number of the roll-call vote inside that chamber and Congress
 - `CAST_CODE`  [filter]
      - how the member voted, as a number: 1, 6, 7 and 9 appear; look up meanings first

**LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS**
one row = one roll-call vote
connects: CONGRESS plus CHAMBER plus ROLLNUMBER matches the same three on VOTEVIEW_VOTES, which gives VOTE_DATE
 - `CONGRESS`  [join]
      - number of the two-year Congress, 118 or 119 here
 - `CHAMBER`  [join]
      - which chamber held the vote: House or Senate
 - `ROLLNUMBER`  [join]
      - the number of the roll-call vote inside that chamber and Congress
 - `VOTE_DATE`  [date]
      - the day the roll-call vote was held, 2023-01-03 to 2026-06-25
      - WATCH: Several roll calls on one day collapse to one vote-day.
 - `BILL_NUMBER`  [label]
      - the bill the vote was about, when there was one
 - `VOTE_DESC`  [label]
      - short text describing what was voted on

---

## 99) Some small House and Senate races are paid for mostly by people who live in a different state.  `M-015` grade B
   - If true, outsiders are picking who represents places they do not live in. If it only shows up for famous names, it is just fame.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one contribution by one person
connects: CMTE_ID matches CMTE_ID on FINANCE__FED_FEC_CAND_CMTE_LINKAGE; 9,217 shared values measured
 - `CMTE_ID`  [join]
      - id of the campaign committee that received the money
 - `STATE`  [filter]
      - state in the donor's address, compared with the state the candidate runs in
      - WATCH: Fill not yet measured.
 - `ZIP_CODE`  [label]
      - ZIP code in the donor's address
      - WATCH: Reads 100% filled but 321,021 rows are blank strings.
 - `TRANSACTION_DATE`  [date]
      - day the committee says it received the money
      - WATCH: Fill 99.98%. Typo years run 0031 to 9206 and 51,555 rows do not parse. Bound the dates. Window on the current table not re-measured.
 - `TRANSACTION_AMT`  [measure]
      - dollar amount of this one contribution
 - `TRANSACTION_TYPE`  [filter]
      - code for the kind of transaction; 15E is an earmark memo row, 15 and 24T also common
      - WATCH: 15E rows are earmark memos that repeat a dollar already counted. Exclude them.
 - `CYCLE_FILE`  [filter]
      - which two-year election cycle file the row came from, such as 2024

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE**
one row = one link between a candidate and a committee
connects: CAND_ID matches CAND_ID on FINANCE__FED_FEC_CANDIDATES; 14,768 shared values measured
 - `CMTE_ID`  [join]
      - id of the committee, 15,853 distinct values
 - `CAND_ID`  [join]
      - id of the candidate the committee works for, 15,092 distinct values
 - `CMTE_TP`  [filter]
      - committee type code; values seen are H, P, S, N, Q; look at distinct values first
 - `CMTE_DSGN`  [filter]
      - committee designation code; values seen are P, A, J, U, D; look at distinct values first
 - `CAND_ELECTION_YR`  [filter]
      - election year the candidate-committee link belongs to

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES**
one row = one candidate in one election cycle
connects: CAND_ID matches CAND_ID on FINANCE__FED_FEC_CAND_CMTE_LINKAGE
 - `CAND_ID`  [join]
      - id of the candidate, 19,063 distinct across 27,095 rows
      - WATCH: Not unique: one row per cycle. Join on CAND_ID plus election year or every dollar repeats.
 - `CAND_NAME`  [label]
      - the candidate's name as filed with the election agency
 - `CAND_OFFICE`  [filter]
      - office sought, one letter; values seen are H, P, S, this idea uses House and Senate
 - `CAND_OFFICE_ST`  [filter]
      - state the candidate is running in
 - `CAND_OFFICE_DISTRICT`  [label]
      - House district number the candidate is running in
      - WATCH: No district geometry is landed; small race must be defined from dollars raised or office and state.
 - `CAND_ELECTION_YR`  [filter]
      - election year for this candidate row
      - WATCH: Not profiled.

---

## 100) Campaign donations pile up on the last few days before each quarterly reporting deadline.  `M-007` grade B
   - If true, the deadline rush is a known bump that has to be subtracted before reading any other daily pattern. Part of the bump may be committees typing in batches, not donors giving.

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS**
one row = one contribution by one person
connects: Optional: CMTE_ID matches CMTE_ID on FINANCE__FED_FEC_CAND_CMTE_LINKAGE; 9,217 shared values measured
 - `TRANSACTION_DATE`  [date]
      - day the committee says it received the money; flag day 29 or later in months 3, 6, 9, 12
      - WATCH: Fill 99.98%. Typo years 0031 to 9206, 51,555 rows do not parse, one parses to 2106-08-27. Bound dates; run the year count first.
 - `TRANSACTION_AMT`  [measure]
      - dollar amount of this one contribution
 - `TRANSACTION_TYPE`  [filter]
      - code for the kind of transaction; 15E is an earmark memo row
      - WATCH: 15E rows are earmark memos that repeat a dollar already counted. Exclude them.
 - `CMTE_ID`  [join]
      - id of the committee that received the money
 - `CYCLE_FILE`  [filter]
      - which two-year election cycle file the row came from

**LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE**
one row = one link between a candidate and a committee
connects: CMTE_ID matches CMTE_ID on FINANCE__FED_FEC_INDIV_CONTRIBUTIONS; used only to split candidate committees from the rest
 - `CMTE_ID`  [join]
      - id of the committee; a match here means it is a candidate's committee
 - `CMTE_TP`  [filter]
      - committee type code; values seen are H, P, S, N, Q; look at distinct values first
 - `CMTE_DSGN`  [filter]
      - committee designation code; values seen are P, A, J, U, D; look at distinct values first

---

## 101) Some immigration courts order far more people deported at hearings the person never showed up to than other courts do.  `N2` grade B
   - If true, whether you get deported without being heard depends on which courtroom your case landed in. The data cannot say why someone was absent or whether the notice reached them.

**LIBRARY_RAW.LANDING.FED_EOIR_PROCEEDING**
one row = one proceeding in one immigration case
connects: nothing. One table, no join
 - `ABSENTIA`  [filter]
      - flag for an order given with the person absent: Y yes, N no
      - WATCH: Measured: N 10.76M, Y 2.46M, NULL 3.58M, null byte 7,834, single space 6,126, digit 5 on one row. Clean all three blank kinds.
 - `BASE_CITY_CODE`  [label]
      - code for the court city that handled the proceeding
      - WATCH: Fill not yet measured. No lookup table names the court; read EOIR's own code list.
 - `COMP_DATE`  [date]
      - day the proceeding was completed; group by its year
      - WATCH: Fill not yet measured.
 - `DEC_CODE`  [filter]
      - code for the judge's decision; coded value, look at distinct values first
      - WATCH: Blank three ways: NULL 5.32M, null byte 1.45M, single space 729K rows. No lookup gives the code meanings.
 - `DEC_TYPE`  [filter]
      - code for the type of decision; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `CUSTODY`  [filter]
      - code for whether the person was detained; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `CASE_TYPE`  [filter]
      - code for the kind of immigration case; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `NAT`  [label]
      - code for the person's nationality; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `HEARING_LOC_CODE`  [label]
      - code for the place the hearing was held; coded value, look at distinct values first
      - WATCH: Fill not yet measured.
 - `IDNCASE`  [join]
      - case id; one person's case can hold several proceedings, use it to count cases
      - WATCH: Counting rows counts proceedings, not people.

---

# WORK

## 102) Employers asking the government for foreign workers are the same employers caught shorting their workers on pay.  `W102` grade C
   - If true, the visa office is approving sponsors another office of the same department already caught. The data shows wages owed, never whether they were paid.

**LIBRARY_RAW.LANDING.FED_DOL_WHD_ENFORCEMENT**
one row = one closed wage-and-hour case against one employer
connects: LEGAL_NAME plus first 5 of ZIP_CD matches EMPLOYER_NAME plus first 5 of EMPLOYER_POSTAL_CODE on IMMIGRATION__FED_DOL_OFLC; overlap not measured
 - `LEGAL_NAME`  [join]
      - the employer's legal name on the wage case
      - WATCH: Blank on 3,612 rows. Name match: multi-word names 92% real, single words 8%. Use multi-word only.
 - `TRADE_NM`  [label]
      - the name the employer trades under, the sign on the door
      - WATCH: Fill not yet measured; table unprofiled.
 - `ZIP_CD`  [join]
      - ZIP code of the employer on the wage case; use the first 5 characters
      - WATCH: Blank on 19 rows.
 - `ST_CD`  [filter]
      - state of the employer on the wage case
      - WATCH: Fill not yet measured; table unprofiled.
 - `H1B_VIOLTN_CNT`  [filter]
      - number of H-1B skilled-worker visa violations found in this case
      - WATCH: Confirmed by name only; two flags found this way were empty. Count non-zero rows first.
 - `H1B_BW_ATP_AMT`  [measure]
      - back wages the employer agreed to pay for H-1B visa violations, in dollars
      - WATCH: Fill not yet measured; table unprofiled.
 - `H1B_EE_ATP_CNT`  [measure]
      - number of employees owed back wages under the H-1B visa findings
      - WATCH: Fill not yet measured; table unprofiled.
 - `H1B_CMP_ASSD_AMT`  [measure]
      - civil money penalty assessed for H-1B visa violations, in dollars
      - WATCH: Fill not yet measured; table unprofiled.
 - `H2A_VIOLTN_CNT`  [filter]
      - number of H-2A farm-worker visa violations found in this case
      - WATCH: Confirmed by name only; count non-zero rows first.
 - `H2A_BW_ATP_AMT`  [measure]
      - back wages the employer agreed to pay for H-2A visa violations, in dollars
      - WATCH: Fill not yet measured; table unprofiled.
 - `H2B_VIOLTN_CNT`  [filter]
      - number of H-2B seasonal-worker visa violations found in this case
      - WATCH: Fill not yet measured; table unprofiled.
 - `BW_ATP_AMT`  [measure]
      - total back wages the employer agreed to pay in this case, in dollars
      - WATCH: Agreed to pay, not paid. No payment or collection column exists.
 - `CASE_VIOLTN_CNT`  [measure]
      - total number of violations found in this case
      - WATCH: Fill not yet measured; table unprofiled.
 - `FINDINGS_START_DATE`  [date]
      - first day of the period the findings cover
      - WATCH: Date columns carry typo years 0200 and 3021.
 - `FINDINGS_END_DATE`  [date]
      - last day of the period the findings cover
      - WATCH: Date columns carry typo years 0200 and 3021.

**LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_DOL_OFLC**
one row = one application by one employer to hire foreign workers
connects: EMPLOYER_NAME plus first 5 of EMPLOYER_POSTAL_CODE matches LEGAL_NAME plus first 5 of ZIP_CD on FED_DOL_WHD_ENFORCEMENT
 - `EMPLOYER_NAME`  [join]
      - name of the employer filing the visa application
      - WATCH: Fill not measured. Name match, not an id; use multi-word names only.
 - `EMPLOYER_POSTAL_CODE`  [join]
      - ZIP code of the employer on the application; use the first 5 characters
      - WATCH: Fill not measured. Head-office ZIP may differ from the cited worksite ZIP.
 - `EMPLOYER_STATE`  [filter]
      - state of the employer on the application
 - `VISA_CLASS`  [filter]
      - which visa program: mostly H-1B, also E-3 Australian, H-1B1 Singapore, H-1B1 Chile
 - `TOTAL_WORKER_POSITIONS`  [measure]
      - number of worker positions the employer asked for
 - `WILLFUL_VIOLATOR`  [filter]
      - flag for an employer previously found a willful violator; look at distinct values first
      - WATCH: Fill not yet measured.
 - `DECISION_DATE`  [date]
      - day the government decided the visa application
      - WATCH: One fiscal year only: 2018-10-01 to 2019-09-30.

---

## 103) Union locals lose members in the same counties where federal contract money is growing.  `W103` grade B
   - If true, federal dollars are flowing to places where organized labor is fading. If not, contracts and unions just run on separate clocks.

**LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS**
one row = one yearly financial report by one union body
connects: First 5 of ZIP matches ZCTA5 on XWALK_ZCTA_COUNTY; overlap not measured
 - `FILE_NUMBER`  [label]
      - the Labor Department's file number for the union body
 - `UNION_NAME`  [label]
      - name of the union as written on the report
      - WATCH: 78 column-shifted junk rows have a numeric UNION_NAME and null YEAR_COVERED; drop them.
 - `DESIGNATION_NUMBER`  [label]
      - the local's number within its parent union
 - `MEMBERS`  [measure]
      - number of members the union reported that year
      - WATCH: Fill not yet measured.
 - `YEAR_COVERED`  [date]
      - the year the report covers, 2000 to 2026
      - WATCH: 99.97% filled.
 - `ZIP`  [join]
      - ZIP code of the union's office, 56,870 distinct; use the first 5
      - WATCH: Office address, not where members work. A national headquarters puts all members in one county.
 - `STATE`  [filter]
      - state of the union's office address

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP-area and county pair
connects: COUNTY_FIPS matches PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on the contract year tables; overlap not measured
 - `ZCTA5`  [join]
      - five-digit Census ZIP area code for the place
 - `COUNTY_FIPS`  [join]
      - five-digit county code picked for that ZIP area by largest land share, 3,266 distinct
      - WATCH: Picks the right county 86.2% of the time; 47.1% on the 5,933 ZIP areas that cross a county line.
 - `XWALK_TYPE`  [filter]
      - label for how the pairing was made; only value seen is clean

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE matches COUNTY_FIPS on XWALK_ZCTA_COUNTY
 - `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`  [join]
      - five-digit code of the county where the contract work is performed
      - WATCH: On FY2024 filled on 93% of rows, 2,894 distinct counties. Other years not measured.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed by this transaction; negative rows are money taken back
      - WATCH: Signed. Sum as is for net dollars; never filter to positive for a county total.
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - federal fiscal year of the transaction

---

## 104) Mines that do not pay their safety fines hurt more workers the following year.  `W104` grade B
   - If true, an unpaid fine is an early warning that a mine is getting dangerous. If not, skipping fines is just a money habit.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one citation or order written at one mine
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_ACCIDENTS, 13,338 shared, and on LABOR__FED_MSHA_MINES, 31,277 shared
 - `MINE_ID`  [join]
      - the government's id for the mine, 32,133 distinct
 - `CONTROLLER_ID`  [label]
      - id of the company or person that controls the mine
      - WATCH: 93.24% filled.
 - `PROPOSED_PENALTY`  [measure]
      - the fine proposed for this citation, in dollars
      - WATCH: Fill not yet measured by the profile. 500,990 rows carry the standard $100 minimum; drags averages down.
 - `AMOUNT_DUE`  [measure]
      - dollars still owed on this fine today
      - WATCH: Fill not yet measured by the profile.
 - `AMOUNT_PAID`  [measure]
      - dollars paid on this fine as of today
      - WATCH: Fill not yet measured by the profile. Today's balance: a fine paid five years late looks like one paid on time.
 - `CAL_YR`  [date]
      - calendar year the citation was written in
 - `VIOLATION_ISSUE_DATE`  [date]
      - day the citation was written, 1994-09-09 to 2026-07-18

**LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS**
one row = one citation or order, full 64-column file
connects: MINE_ID matches MINE_ID on the marts; VIOLATION_NO matches VIOLATION_NO on LABOR__FED_MSHA_VIOLATIONS, strip quotes first
 - `VIOLATION_NO`  [join]
      - the citation number printed on the paper
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `MINE_ID`  [join]
      - the government's id for the mine
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `FINAL_ORDER_ISSUE_DT`  [date]
      - day the fine became final and owed
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `BILL_PRINT_DT`  [date]
      - day the bill for the fine was printed
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `LAST_ACTION_CD`  [filter]
      - code for the last thing that happened to the fine; coded value, look at distinct values first
      - WATCH: Code meanings are not in the warehouse. Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `LAST_ACTION_DT`  [date]
      - day of the last thing that happened to the fine
      - WATCH: Not labelled a payment date. Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `CONTESTED_IND`  [filter]
      - flag for whether the mine contested the fine
      - WATCH: Contested fines are not delinquent; set them aside. Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `CONTESTED_DT`  [date]
      - day the mine contested the fine
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `DOCKET_STATUS_CD`  [filter]
      - code for where the contested case stands; coded value, look at distinct values first
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `PROPOSED_PENALTY`  [measure]
      - the fine proposed for this citation, in dollars
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `AMOUNT_DUE`  [measure]
      - dollars still owed on this fine today
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `AMOUNT_PAID`  [measure]
      - dollars paid on this fine as of today
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS**
one row = one reported accident or injury
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_VIOLATIONS; 13,338 shared mine ids
 - `MINE_ID`  [join]
      - the government's id for the mine, 13,708 distinct
 - `CAL_YR`  [date]
      - calendar year of the accident; compare to fines from the year before
 - `NO_INJURIES`  [measure]
      - number of people injured in this accident
 - `DAYS_LOST`  [measure]
      - work days lost because of the injury
 - `DEGREE_INJURY`  [filter]
      - how bad the injury was, in words, such as DAYS AWAY FROM WORK ONLY or ACCIDENT ONLY
 - `IS_FATALITY`  [filter]
      - true if someone died in the accident, false if not
 - `ACCIDENT_DATE`  [date]
      - day of the accident, 2000-01-01 to 2026-07-14

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES**
one row = one mine, current state
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_VIOLATIONS; 31,277 shared mine ids
 - `MINE_ID`  [join]
      - the government's id for the mine
 - `NO_EMPLOYEES`  [measure]
      - number of workers at the mine right now
      - WATCH: Null on 39,735 of 91,906 mines, and a current value, not yearly.
 - `COAL_METAL_IND`  [filter]
      - one letter for the kind of mine; values seen are M and C, a coal or metal split
 - `CURRENT_MINE_STATUS`  [filter]
      - the mine's status today, such as Active, Abandoned, Intermittent, Temporarily Idled

---

## 105) Medical devices rushed through a fast or outsourced government review get recalled more often than devices reviewed the normal way.  `W107` grade D
   - If true, the shortcut lets worse devices reach patients. Today it cannot be answered: the recall table's two link columns are empty.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_510K**
one row = one 510(k) clearance decision
connects: Planned: K_NUMBER matches one element of K_NUMBER_LIST on HEALTH__FED_FDA_DEVICE_ENFORCEMENT; dead, right side 0.0% filled
 - `K_NUMBER`  [join]
      - the clearance number given to the device, 172,884 distinct
 - `EXPEDITED_REVIEW_FLAG`  [filter]
      - Y if the device got a fast-track review
      - WATCH: Fill not measured; profile sample shows Y on 28 rows and blank on 175,658.
 - `THIRD_PARTY_FLAG`  [filter]
      - Y if an outside reviewer did the review instead of the FDA, N if not
      - WATCH: Fill not yet measured.
 - `CLEARANCE_TYPE`  [filter]
      - kind of clearance: Traditional, Special, Abbreviated, Direct, Post-NSE
 - `PRODUCT_CODE`  [join]
      - the FDA's short code for the type of device
      - WATCH: 1,442 blank strings. The recall side is 0.0% filled, so this join is dead.
 - `APPLICANT`  [label]
      - name of the company that applied for clearance
      - WATCH: Name match to RECALLING_FIRM reaches a company, not a device.
 - `DECISION_DATE`  [date]
      - day the FDA decided, 1976-07-15 to 2026-07-26

**LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_PMA**
one row = one premarket approval or supplement
connects: None: the recall table has no approval-number column, so this route has no path
 - `PMA_NUMBER`  [join]
      - the premarket approval number given to the device
      - WATCH: No matching column exists on the recall table.
 - `EXPEDITED_REVIEW_FLAG`  [filter]
      - Y if the device got a fast-track review, N if not
 - `PRODUCT_CODE`  [join]
      - the FDA's short code for the type of device
      - WATCH: 768 blank strings. The recall side is 0.0% filled.
 - `APPLICANT`  [label]
      - name of the company that applied for approval
 - `DECISION_DATE`  [date]
      - day the FDA decided, 1960-10-14 to 2026-07-26

**LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT**
one row = one device recall
connects: K_NUMBER_LIST and PRODUCT_CODE were meant to match HEALTH__FED_FDA_DEVICE_510K; both are empty. Left over: RECALLING_FIRM to APPLICANT by name
 - `K_NUMBER_LIST`  [join]
      - list of clearance numbers for the recalled device
      - WATCH: Empty column: 0.0% filled, 0 distinct.
 - `PRODUCT_CODE`  [join]
      - the FDA's short code for the type of device
      - WATCH: Empty column: 0.0% filled, 0 distinct.
 - `CLASSIFICATION`  [filter]
      - the recall's class as filed: Class I, Class II, Class III
 - `RECALLING_FIRM`  [label]
      - name of the company doing the recall
      - WATCH: A name match mixes every device a firm makes.
 - `RECALL_INITIATION_DATE`  [date]
      - day the company started the recall
      - WATCH: Range starts 1930-12-11, while REPORT_DATE starts 2012-06-20.
 - `OPENFDA`  [join]
      - a bundle of extra FDA fields that may hold the clearance numbers inside
      - WATCH: Contents not yet measured. If no k_number inside, the fix is a reload.

---

## 106) A handful of recalled car models draw most of the owner complaints, and which states complain most differs by model.  `W111` grade B
   - If true, certain recalled cars are a bigger problem in certain states. With no sales data, a state with many complaints may simply have many of those cars.

**LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS**
one row = one recall campaign applied to one make, model and model year
connects: MAKE, MODEL, MODEL_YEAR match MAKE, MODEL, MODEL_YEAR on CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS; overlap not measured
 - `CAMPNO`  [label]
      - the recall campaign number given by the safety agency
 - `MAKE`  [join]
      - the car brand, written as text
      - WATCH: Text match, not an id.
 - `MODEL`  [join]
      - the car model, written as text
      - WATCH: Text match; overlap never counted.
 - `MODEL_YEAR`  [join]
      - the model year of the car, 1965 to 9999
      - WATCH: 9999 means unknown. Drop it before joining.
 - `COMPONENT`  [label]
      - the part of the car the recall is about
 - `POTENTIALLY_AFFECTED_UNITS`  [measure]
      - number of vehicles the recall might cover
 - `NOTIFICATION_DATE`  [date]
      - day owners were notified of the recall
      - WATCH: 98.36% filled. Placeholder dates at both ends: 1111-11-11 and 2027-08-16.

**LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS**
one row = one owner complaint
connects: MAKE, MODEL, MODEL_YEAR match the recalls table; STATE optionally matches STATE on FINANCE__FED_IRS_SOI
 - `CMPLID`  [label]
      - the id number of this one complaint
 - `MAKE`  [join]
      - the car brand, written as text
 - `MODEL`  [join]
      - the car model, free-typed by the public
      - WATCH: Spelling variants split one model into several; overlap never counted.
 - `MODEL_YEAR`  [join]
      - the model year of the car complained about
      - WATCH: 9999 means unknown. Drop it or every unknown matches every unknown.
 - `STATE`  [label]
      - the state of the owner who complained
      - WATCH: Fill not yet measured. Counts complainers, not cars on the road.
 - `COMPONENT`  [label]
      - the part of the car the complaint is about
 - `DATE_RECEIVED`  [date]
      - day the complaint was received, 1995-01-01 to 2026-07-22
 - `CRASH`  [filter]
      - Y if the complaint says there was a crash, N if not
 - `FIRE`  [filter]
      - Y if the complaint says there was a fire, N if not
 - `INJURED`  [measure]
      - number of people the complaint says were injured
 - `DEATHS`  [measure]
      - number of people the complaint says died

**LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI**
one row = one ZIP and income band of tax returns
connects: STATE matches STATE on CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS; optional income context
 - `STATE`  [join]
      - state the tax returns were filed from
 - `AGI`  [measure]
      - adjusted gross income reported on the returns in this row
 - `N_RETURNS`  [measure]
      - number of tax returns counted in this row
 - `TAX_YEAR`  [date]
      - the tax year the returns belong to
      - WATCH: Single value 2016. Can rank states once, not over time.

---

## 107) Some American nursing homes are owned by a company that also shows up on Britain's public list of who controls companies.  `W113` grade C
   - If true, the money and the decisions for a US care home sit offshore where US regulators cannot easily see. The match is a name only, so it gives a list to check by hand.

**LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC**
one row = one controller of one UK company
connects: NAME matches ORGANIZATION_NAME_OWNER on FED_CMS_SNF_OWNERSHIP; name only, overlap not measured
 - `COMPANY_NUMBER`  [label]
      - the UK register's number for the company being controlled, 10,679,125 distinct
      - WATCH: Table completeness is disputed: trap log says about 7M of 10M+ loaded, profile shows 15,804,611 rows. Counts are floors.
 - `NAME`  [join]
      - full name of the controller, a person or a company
      - WATCH: Name match, not an id: multi-word 92% real, single words 8%, tested inside the US only.
 - `KIND`  [filter]
      - what the controller is: individual person, corporate entity, a statement, or beneficial owner
 - `ADDRESS_COUNTRY`  [filter]
      - country written in the controller's address
 - `COUNTRY_REGISTERED`  [filter]
      - country where a corporate controller is registered
 - `REGISTRATION_NUMBER`  [label]
      - registration number of a corporate controller in its home register
 - `NATURES_OF_CONTROL`  [label]
      - text describing the kind of control this controller holds over the company
 - `NOTIFIED_ON`  [date]
      - day the register was told about this controller
      - WATCH: Placeholder dates: range runs 1083-01-01 to 2026-12-31.
 - `CEASED_ON`  [date]
      - day the control ended; empty means still in control
      - WATCH: 16.51% filled.

**LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP**
one row = one owner in one role on one nursing-home enrollment
connects: ENROLLMENT_ID matches ENROLLMENT_ID on HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS; 288,550 of 295,083 owner rows join
 - `ENROLLMENT_ID`  [join]
      - Medicare's id for the nursing home's enrollment
      - WATCH: 6,533 owner rows name enrollments the snapshot does not carry.
 - `ORGANIZATION_NAME`  [label]
      - name of the nursing home's enrolled organization
      - WATCH: Fill not yet measured; table unprofiled.
 - `ORGANIZATION_NAME_OWNER`  [join]
      - name of the owner when the owner is a company
      - WATCH: Name match only. One vintage, current owners only; a shell that sold last year is gone.
 - `TYPE_OWNER`  [filter]
      - the kind of owner; coded value, look at distinct values first
      - WATCH: Fill not yet measured; table unprofiled.
 - `ROLE_TEXT_OWNER`  [filter]
      - the owner's role on the home, written in words
      - WATCH: Fill not yet measured; table unprofiled.
 - `PERCENTAGE_OWNERSHIP`  [measure]
      - percent of the home this owner holds
      - WATCH: Fill not yet measured; table unprofiled.
 - `ADDRESS_LINE_1_OWNER`  [label]
      - street address of the owner, first line
      - WATCH: A UK address, if any, would sit in free text here.
 - `CITY_OWNER`  [label]
      - city in the address of the owner
      - WATCH: Fill not yet measured; table unprofiled.
 - `STATE_OWNER`  [filter]
      - state in the address of the owner
      - WATCH: US-style field; the file has no country column.
 - `ZIP_CODE_OWNER`  [label]
      - ZIP code of the owner's address
      - WATCH: US-style field; the file has no country column.
 - `HOLDING_COMPANY_OWNER`  [filter]
      - flag for whether the owner is a holding company; look at distinct values first
      - WATCH: Fill not yet measured; table unprofiled.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS**
one row = one nursing-home Medicare enrollment
connects: CCN matches CMS_CERTIFICATION_NUMBER_CCN on HEALTH__FED_CMS_NURSING_HOME; 100% on the landing pair
 - `ENROLLMENT_ID`  [join]
      - Medicare's id for the nursing home's enrollment
 - `CCN`  [join]
      - Medicare's certification number for the building, 14,026 distinct
 - `ORGANIZATION_NAME`  [label]
      - name of the organization enrolled with Medicare

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME**
one row = one nursing home, current state
connects: CMS_CERTIFICATION_NUMBER_CCN matches CCN on HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
 - `CMS_CERTIFICATION_NUMBER_CCN`  [join]
      - Medicare's certification number for the nursing home, 14,328 distinct
 - `PROVIDER_NAME`  [label]
      - the nursing home's name as Medicare lists it
 - `STATE`  [filter]
      - state the nursing home is in
 - `NUMBER_OF_CERTIFIED_BEDS`  [measure]
      - number of beds the home is certified for
 - `OVERALL_RATING`  [measure]
      - Medicare's overall rating number for the home, values 1 to 5

---

## 108) People and companies on Britain's list of company controllers also sit behind firms that win US government contracts.  `W115` grade C
   - If true, US taxpayer money is going to firms steered from abroad through a chain nobody has drawn. With no shared id the match is names only, so every hit is a lead and not proof.

**LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC**
one row = one controller of one UK company
connects: NAME for corporate kinds matches RECIPIENT_PARENT_NAME, and NAME for person kinds matches HIGHLY_COMPENSATED_OFFICER_n_NAME, on the contract year tables; name only
 - `NAME`  [join]
      - full name of the controller, a person or a company
      - WATCH: Name match only. Table completeness is disputed: trap log says about 7M of 10M+ loaded, profile shows 15,804,611 rows. Counts are floors.
 - `NAME_FORENAME`  [label]
      - first name of a controller who is a person
 - `NAME_SURNAME`  [label]
      - last name of a controller who is a person
 - `KIND`  [filter]
      - what the controller is: individual person, corporate entity, a statement, or beneficial owner
 - `COMPANY_NUMBER`  [label]
      - the UK register's number for the company being controlled
      - WATCH: No crosswalk from this number to a US contractor id exists.
 - `COUNTRY_OF_RESIDENCE`  [filter]
      - country where a person controller lives
 - `COUNTRY_REGISTERED`  [filter]
      - country where a corporate controller is registered
 - `NATURES_OF_CONTROL`  [label]
      - text describing the kind of control this controller holds over the company
 - `CEASED_ON`  [date]
      - day the control ended; empty means still in control
      - WATCH: 16.51% filled.

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: RECIPIENT_PARENT_NAME and HIGHLY_COMPENSATED_OFFICER_n_NAME match NAME on CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC; name only, overlap not measured
 - `RECIPIENT_UEI`  [label]
      - the government's unique id for the company that got the contract
      - WATCH: Fill not yet measured; tables unprofiled.
 - `RECIPIENT_NAME`  [label]
      - name of the company that got the contract
      - WATCH: Fill not yet measured; tables unprofiled.
 - `RECIPIENT_PARENT_NAME`  [join]
      - name of the parent company above the contractor
      - WATCH: Name match only. Column names may be case-sensitive lowercase on landing; confirm on one table.
 - `RECIPIENT_PARENT_UEI`  [label]
      - the government's unique id for the parent company
      - WATCH: Fill not yet measured; tables unprofiled.
 - `RECIPIENT_COUNTRY_CODE`  [filter]
      - country code of the contractor; narrow to the United Kingdom first
      - WATCH: Fill not yet measured; tables unprofiled.
 - `FOREIGN_OWNED`  [filter]
      - flag the contract file sets when the contractor is foreign owned
      - WATCH: Fill not yet measured; tables unprofiled.
 - `DOMESTIC_OR_FOREIGN_ENTITY_CODE`  [filter]
      - code for whether the contractor is a US or foreign entity; look at distinct values first
      - WATCH: Fill not yet measured; tables unprofiled.
 - `HIGHLY_COMPENSATED_OFFICER_1_NAME`  [join]
      - name of the contractor's number 1 highest-paid officer
      - WATCH: Person-name match is the weakest kind: single-word and common surnames 8% real. Needs a second fact.
 - `HIGHLY_COMPENSATED_OFFICER_2_NAME`  [join]
      - name of the contractor's number 2 highest-paid officer
      - WATCH: Person-name match is the weakest kind: single-word and common surnames 8% real. Needs a second fact.
 - `HIGHLY_COMPENSATED_OFFICER_3_NAME`  [join]
      - name of the contractor's number 3 highest-paid officer
      - WATCH: Person-name match is the weakest kind: single-word and common surnames 8% real. Needs a second fact.
 - `HIGHLY_COMPENSATED_OFFICER_4_NAME`  [join]
      - name of the contractor's number 4 highest-paid officer
      - WATCH: Person-name match is the weakest kind: single-word and common surnames 8% real. Needs a second fact.
 - `HIGHLY_COMPENSATED_OFFICER_5_NAME`  [join]
      - name of the contractor's number 5 highest-paid officer
      - WATCH: Person-name match is the weakest kind: single-word and common surnames 8% real. Needs a second fact.
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed by this transaction; negative rows are money taken back
      - WATCH: Fill not yet measured; tables unprofiled.
 - `ACTION_DATE`  [date]
      - day the contract transaction was signed off
      - WATCH: Fill not yet measured; tables unprofiled.

---

## 109) Some licensed American doctors are listed in Britain as the person who controls a UK company, and nobody has counted how many.  `W117` grade C
   - If true, it is a first look at US clinicians running businesses offshore. A first and last name across two countries proves nobody, so only rare names that hit exactly one doctor count.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES**
one row = one provider id, a person or an organization
connects: PROVIDER_FIRST_NAME plus PROVIDER_LAST_NAME_LEGAL_NAME matches NAME_FORENAME plus NAME_SURNAME on CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC; name only
 - `NPI`  [label]
      - the national id number given to each US health provider
 - `ENTITY_TYPE_CODE`  [filter]
      - values seen are 1, 2 and blank; the table mixes people and organizations, look at distinct values first
 - `PROVIDER_FIRST_NAME`  [join]
      - the first name of a provider who is a person
      - WATCH: 346,179 deactivated rows have empty name fields; a retired doctor cannot match.
 - `PROVIDER_MIDDLE_NAME`  [join]
      - the provider's middle name, used to make a match rarer
 - `PROVIDER_LAST_NAME_LEGAL_NAME`  [join]
      - the legal last name of a provider who is a person
      - WATCH: Common names hit many of 9,606,683 rows. Keep only names hitting exactly one NPI.
 - `PROVIDER_CREDENTIAL_TEXT`  [filter]
      - letters after the provider's name, typed in by the provider
 - `PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME`  [label]
      - state where the provider's practice is located
 - `HEALTHCARE_PROVIDER_TAXONOMY_CODE_1`  [filter]
      - code for the provider's first listed specialty; coded value, look at distinct values first
 - `PROVIDER_ENUMERATION_DATE`  [date]
      - day the provider id was issued, 2005-05-23 to 2026-06-06
      - WATCH: 96.4% filled.

**LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC**
one row = one controller of one UK company
connects: COMPANY_NUMBER matches COMPANY_NUMBER on CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE; 5,582,726 shared values
 - `NAME_FORENAME`  [join]
      - first name of a controller who is a person
      - WATCH: Name match, not an id. Table completeness is disputed: trap log says about 7M of 10M+ loaded, profile shows 15,804,611 rows. Counts are floors.
 - `NAME_MIDDLE`  [join]
      - middle name of the person controller, used to make a match rarer
 - `NAME_SURNAME`  [join]
      - last name of a controller who is a person
 - `NAME_TITLE`  [filter]
      - title in front of the name; Dr is a second sign
 - `DOB_YEAR`  [label]
      - year the person controller was born
      - WATCH: 87.26% filled. No birth year on the US side, so it cannot confirm a match.
 - `COUNTRY_OF_RESIDENCE`  [filter]
      - country where the controller lives; keep the United States
 - `NATIONALITY`  [label]
      - nationality the controller declared to the register
 - `COMPANY_NUMBER`  [join]
      - the UK register's number for the company being controlled
      - WATCH: Company table covers 5,582,726 of 10,679,125 distinct numbers here.
 - `CEASED_ON`  [date]
      - day the control ended; empty means still in control
      - WATCH: 16.51% filled.

**LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE**
one row = one UK company
connects: COMPANY_NUMBER matches COMPANY_NUMBER on CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC
 - `COMPANY_NUMBER`  [join]
      - the UK register's number for the company, 5,716,497 distinct
 - `COMPANY_NAME`  [label]
      - the company's name as registered in the UK
 - `COMPANY_CATEGORY`  [filter]
      - the legal form, such as Private Limited Company or Limited Partnership, 28 kinds
      - WATCH: A legal form, not an industry. Industry text sits only on the landing copy, fill not measured.
 - `COMPANY_STATUS`  [filter]
      - whether the company is alive: Active, Liquidation, In Administration and others, 14 kinds

---

## 110) Some mine operators get fined for the same safety rule, pay up, and get fined for it again, over and over.  `W120` grade B
   - If true, the fine is just a running cost of doing business and fixes nothing. If repeats only track how many mines an operator has, big operators repeat because they are big.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one citation or order written at one mine
connects: VIOLATION_NO matches VIOLATION_NO on LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS, strip quotes; overlap not measured
 - `CONTROLLER_ID`  [join]
      - id of the company or person that controls the mine, 19,855 distinct
      - WATCH: 93.24% filled; empty on 6.76% of rows, which fall out of every chain.
 - `CONTROLLER_NAME`  [label]
      - name of the company or person that controls the mine
 - `VIOLATOR_ID`  [label]
      - id of the party the citation was written against
 - `MINE_ID`  [label]
      - the government's id for the mine, 32,133 distinct
 - `SECTION_OF_ACT`  [join]
      - the section of the Mine Act cited, such as 316(b) or 103(k)
      - WATCH: 0.56% filled, 17,223 of 3,087,265 rows in the 2026-09-08 profile. This is the idea's group-by key, so count it first
 - `VIOLATION_NO`  [join]
      - the citation number printed on the paper
 - `VIOLATION_ISSUE_DATE`  [date]
      - day the citation was written, 1994-09-09 to 2026-07-18
 - `PROPOSED_PENALTY`  [measure]
      - the fine proposed for this citation, in dollars
      - WATCH: Fill not measured. 500,990 rows carry the standard $100 minimum; rank by repeats, not dollars.
 - `AMOUNT_DUE`  [measure]
      - dollars still owed on this fine today
      - WATCH: Fill not yet measured.
 - `AMOUNT_PAID`  [measure]
      - dollars paid on this fine as of today
      - WATCH: Fill not measured. Today's balance, with no payment date on the mart.
 - `SIG_SUB`  [filter]
      - a Y or N flag on the citation; meaning not given, look at distinct values first

**LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS**
one row = one citation or order, full 64-column file
connects: VIOLATION_NO matches VIOLATION_NO on LABOR__FED_MSHA_VIOLATIONS, strip quotes; 3,087,266 rows against 3,087,265
 - `VIOLATION_NO`  [join]
      - the citation number printed on the paper
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `CONTROLLER_ID`  [join]
      - id of the company or person that controls the mine
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `SECTION_OF_ACT`  [label]
      - the section of the Mine Act cited
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `SECTION_OF_ACT_1`  [label]
      - a further section-of-the-Act field; coded value, look at distinct values first
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `SECTION_OF_ACT_2`  [label]
      - a further section-of-the-Act field; coded value, look at distinct values first
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `PART_SECTION`  [join]
      - the specific regulation cited, sharper than the section of the Act
      - WATCH: No violation narrative exists; one regulation can still be different physical faults. Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `CIT_ORD_SAFE`  [filter]
      - coded value for the kind of paper written; look at distinct values first
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `INITIAL_VIOL_NO`  [label]
      - a citation number pointing back to an earlier citation; check a sample first
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `LAST_ACTION_CD`  [filter]
      - code for the last thing that happened to the fine; coded value, look at distinct values first
      - WATCH: A payment date only if this code says payment; code meanings are not in the warehouse. Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `LAST_ACTION_DT`  [date]
      - day of the last thing that happened to the fine
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `FINAL_ORDER_ISSUE_DT`  [date]
      - day the fine became final and owed
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `CONTESTED_IND`  [filter]
      - flag for whether the mine contested the citation
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `TERMINATION_DT`  [date]
      - day the citation was terminated, per the column name
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.
 - `VIOLATION_ISSUE_DT`  [date]
      - day the citation was written, landing copy
      - WATCH: Landing values are wrapped in literal double quotes; strip first. Empty is a pair of quotes, not NULL. Fill not measured.

---

## 111) In some neighborhoods, people file the same complaint about the same bank or lender every single year.  `W121` grade B
   - If true, a company has a standing problem in one place that never gets fixed. If it is only the biggest firms in the biggest ZIP codes, the pattern is just size.

**LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS**
one row = one consumer complaint
connects: nothing. One table, no join
 - `COMPLAINT_ID`  [label]
      - the id number of this one complaint
 - `ZIP_CODE`  [join]
      - ZIP code of the person complaining, 36,864 distinct
      - WATCH: 99.99% filled but part is masked as XXXXX or three digits plus XX. Masked share not measured. A place, not a person.
 - `COMPANY`  [join]
      - name of the financial company complained about, 8,088 distinct
      - WATCH: The three national credit bureaus dominate; run with and without them.
 - `PRODUCT`  [filter]
      - the kind of financial product the complaint is about
 - `ISSUE`  [join]
      - the kind of problem the complaint is about
      - WATCH: Templated bulk filings can fake a local repeat; one narrative appears 27,510 times.
 - `SUB_ISSUE`  [label]
      - a finer cut of what the complaint is about
 - `RECEIVED_YEAR`  [date]
      - the year the complaint came in; count distinct years per cell
      - WATCH: Stored as a date, first of January each year. 2011 holds one month, 2026 is partial.
 - `STATE`  [filter]
      - state of the person who filed the complaint
 - `COMPANY_RESPONSE`  [label]
      - how the company answered, such as Closed with explanation or Closed with monetary relief
      - WATCH: 96.92% filled.

---

## 112) The same counties flood, get federal money to rebuild, and then flood again a few years later.  `W122` grade B
   - If true, taxpayers keep paying to rebuild on the same wet ground. If aid shrinks each time or repeat counties are few, the money is not feeding the cycle.

**LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS**
one row = one disaster and one designated area
connects: FIPSSTATECODE joined to FIPSCOUNTYCODE matches FIPS on HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS, and DISASTERNUMBER matches DISASTER_NUMBER; overlap not measured
 - `DISASTERNUMBER`  [join]
      - the federal number for the disaster
      - WATCH: One row per disaster and area. Count distinct values, a plain row count overstates events.
 - `INCIDENTTYPE`  [filter]
      - kind of disaster in words; keep the flood ones
      - WATCH: Fill not yet measured; table unprofiled.
 - `DECLARATIONDATE`  [date]
      - day the federal disaster was declared
      - WATCH: Fill not yet measured; table unprofiled.
 - `INCIDENTBEGINDATE`  [date]
      - day the disaster itself began on the ground
      - WATCH: Fill not yet measured; table unprofiled.
 - `FIPSSTATECODE`  [join]
      - two-digit state code, padded with a leading zero
      - WATCH: Fill not yet measured; table unprofiled.
 - `FIPSCOUNTYCODE`  [join]
      - three-digit county code, padded; glue to the state code for a five-digit county
      - WATCH: Fill not yet measured; table unprofiled.
 - `DESIGNATEDAREA`  [label]
      - name of the county or area covered
      - WATCH: Fill not yet measured; table unprofiled.
 - `IHPROGRAMDECLARED`  [filter]
      - flag for one aid program being declared for this area; look at distinct values first
      - WATCH: Fill not yet measured; table unprofiled.
 - `IAPROGRAMDECLARED`  [filter]
      - flag for one aid program being declared for this area; look at distinct values first
      - WATCH: Fill not yet measured; table unprofiled.

**LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS**
one row = one household's aid registration
connects: FIPS left-padded to 5 matches PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE on the assistance year tables; overlap not measured
 - `DISASTER_NUMBER`  [join]
      - the federal number for the disaster, 620 distinct
 - `FIPS`  [join]
      - county code of the household that registered for aid
      - WATCH: 74.21% filled. Unpadded for states 01 to 09, '1097' and '01097' both exist; left-pad to 5.
 - `DECLARATION_DATE`  [date]
      - day the disaster was declared, 2002-10-24 to 2026-08-03
 - `INCIDENT_TYPE_CODE`  [filter]
      - one-letter disaster type; values seen are H, W, F, O, B; look at distinct values first
 - `FLOOD_DAMAGE`  [filter]
      - True if the home had flood damage, False if not
 - `FLOOD_DAMAGE_AMOUNT`  [measure]
      - dollar amount of flood damage recorded for the home
 - `FLOOD_INSURANCE`  [filter]
      - True if the household had flood insurance, False if not
      - WATCH: No flood-insurance claims table is landed; insured rebuilding is invisible.
 - `IHP_AMOUNT`  [measure]
      - total dollars FEMA approved for the household under its Individuals and Households Program, the main aid pot
 - `REPAIR_AMOUNT`  [measure]
      - aid dollars on this registration for repairing the home
 - `REPLACEMENT_AMOUNT`  [measure]
      - aid dollars on this registration for replacing the home

**LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 to FY2026 (20 tables, same columns)**
one row = one assistance transaction
connects: PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE matches the five-digit county code from the declarations and housing-aid tables; overlap not measured
 - `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`  [join]
      - five-digit code of the county where the aid is used
      - WATCH: Fill runs 71% in FY2007 to 99% in FY2020.
 - `CFDA_NUMBER`  [filter]
      - the catalog number of the federal aid program
 - `CFDA_TITLE`  [label]
      - the name of the federal aid program
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed by this one assistance transaction
      - WATCH: Loans carry no obligation: types 07 and 08 sum to exactly $0.00 on 11,788,945 rows.
 - `FACE_VALUE_OF_LOAN`  [measure]
      - the size of the loan in dollars; where disaster loan money actually sits
 - `ASSISTANCE_TYPE_CODE`  [filter]
      - code for the kind of aid; 07 and 08 are loans. Source: public USAspending code list, not the handbook
 - `AWARDING_AGENCY_NAME`  [label]
      - name of the federal agency that gave the aid
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - federal fiscal year of the transaction

---

## 113) When paychecks in a county shrink, does the local nonprofit hospital end up giving away more free care?  `W123` grade C
   - If yes, hospital charity follows local hardship. If no, it follows hospital policy or state rules, not how the neighbors are doing.

**LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS**
one row = one hospital cost report
connects: first 5 of ZIP_CODE matches ZCTA5 on XWALK_ZCTA_COUNTY; optional: PROVIDER_CCN matches CCN on XWALK_HOSPITAL_CCN_EIN
 - `RPT_REC_NUM`  [label]
      - the record number of one filed cost report; the only thing unique per row
      - WATCH: Hospital plus year is not unique: 1,186 hospital-years carry more than one report.
 - `PROVIDER_CCN`  [join]
      - the hospital's Medicare certification number, the federal id for the building
 - `FISCAL_YEAR_END_DATE`  [date]
      - the day the hospital's bookkeeping year ended for this report
 - `FISCAL_YEAR_LENGTH_DAYS`  [filter]
      - how many days the report covers; a short one is a stub, not a year
      - WATCH: Filter to 300 or more to drop sale-day stubs.
 - `COST_OF_CHARITY_CARE`  [measure]
      - dollars the hospital says it spent treating patients it did not bill
      - WATCH: Fill not measured. The text 'nan' became float NaN, not NULL, so is not null passes it. For-profits leave it mostly blank, 1,120 of 1,841 reports.
 - `COST_OF_UNCOMPENSATED_CARE`  [measure]
      - dollars of care the hospital was never paid for, charity plus unpaid bills
      - WATCH: Fill not measured; same NaN trap as the charity column.
 - `TOTAL_BAD_DEBT_EXPENSE`  [measure]
      - dollars of patient bills the hospital gave up collecting
 - `TOTAL_COSTS`  [measure]
      - the hospital's total spending for the year, the bottom of the share
 - `TYPE_OF_CONTROL`  [filter]
      - who owns the hospital, as a number code; coded value, look at distinct values first
 - `ZIP_CODE`  [join]
      - the hospital's mailing ZIP; use the first 5 characters
 - `COUNTY`  [label]
      - the county name as typed on the report, free text
 - `STATE_CODE`  [filter]
      - the two-letter state the hospital sits in

**LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY**
one row = one ZIP-area and county pair
connects: COUNTY_FIPS matches AREA_FIPS on ECONOMICS__FED_BLS_QCEW
 - `ZCTA5`  [join]
      - the five-digit ZIP area used by the Census, 2020 boundaries
 - `COUNTY_FIPS`  [join]
      - the five-digit federal county code that ZIP area falls in

**LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_BLS_QCEW**
one row = one area, ownership and industry cell of jobs and wages
connects: AREA_FIPS matches COUNTY_FIPS on XWALK_ZCTA_COUNTY
 - `AREA_FIPS`  [join]
      - the federal code for the area; for counties it is the five-digit county code
 - `OWNERSHIP_CODE`  [filter]
      - who the employer is, private or a level of government; coded value, look at distinct values first
 - `INDUSTRY_CODE`  [filter]
      - the industry the jobs are in, or the all-industries total code
 - `AGGREGATION_LEVEL_CODE`  [filter]
      - how rolled-up the row is, county total or industry detail; coded value, look at distinct values first
 - `ANNUAL_AVG_WEEKLY_WAGE`  [measure]
      - the average weekly paycheck in that area and industry for the year, in dollars
 - `AVG_ANNUAL_PAY`  [measure]
      - the average yearly pay per job in that cell, in dollars
 - `YOY_WAGES_PCT_CHANGE`  [measure]
      - percent change in total wages against the year before; negative means wages fell
      - WATCH: The only wage fall the table can show is this one column for 2022.
 - `YEAR`  [date]
      - the calendar year the wage numbers cover
      - WATCH: 2022 only. Thirteen years of cost reports have one wage year to pair with.

**LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN**
one row = one hospital certification number matched to one tax id
connects: CCN matches PROVIDER_CCN on HEALTH__FED_CMS_HCRIS
 - `CCN`  [join]
      - the hospital's Medicare certification number, the federal id for the building
      - WATCH: Covers 3,891 of 6,703 nonprofit hospitals, 58%.
 - `EIN`  [join]
      - the nine-digit tax id of the organization matched to that hospital
      - WATCH: Not a real id join: a name-and-address match. The tax id is the system that files, not the building: 1,293 tax ids cover 3,222 rows.
 - `MATCH_TIER`  [filter]
      - how strong the name-and-address match was; coded value, look at distinct values first
      - WATCH: Read it before trusting a row.
 - `MATCH_RULE`  [label]
      - which matching rule produced this pair; coded value, look at distinct values first
 - `EIN_NTEE`  [label]
      - the nonprofit category code the IRS gives that tax id
 - `PROPRIETARY_NONPROFIT`  [filter]
      - whether the hospital is for-profit or nonprofit; coded value, look at distinct values first

---

## 114) Once you account for how many plants a power company runs and what they burn, which companies still pump out more smoke than they should?  `W124` grade B
   - A company that stays above the line every year with the same fuel as cleaner peers is dirty by choice, not by fuel. If nothing is left over, dirtier just means burns more coal.

**LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2019, 2020, 2021, 2023 (4 tables, same columns)**
one row = one power plant, one year
connects: ORISPL equals DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE on the 2022 table; ORISPL matches PLANT_CODE on ENERGY__FED_EIA860_4_OWNER
 - `ORISPL`  [join]
      - the federal plant code, one number per power plant
 - `PNAME`  [label]
      - the name of the power plant as the agency lists it
 - `OPRNAME`  [label]
      - the name of the company that runs the plant, free text
      - WATCH: Free text. One company can appear under several spellings across years. The 2022 table has no column named operator.
 - `UTLSRVNM`  [label]
      - the name of the utility service territory the plant sits in
 - `PLPRMFL`  [filter]
      - the plant's main fuel as a short code, such as gas, coal or sun
 - `PLFUELCT`  [filter]
      - the plant's main fuel as a plain category, such as COAL, GAS or SOLAR
 - `NAMEPCAP`  [measure]
      - the plant's rated maximum output, in megawatts
 - `PLNGENAN`  [measure]
      - electricity the plant actually made that year, in megawatt-hours
 - `PLCO2AN`  [measure]
      - tons of carbon dioxide out of the stacks that year
      - WATCH: Files get revised: 2020 is the v2 file and 2023 is rev2. Note the revision with any published number.
 - `PLSO2AN`  [measure]
      - tons of sulfur dioxide out of the stacks that year
 - `PLNOXAN`  [measure]
      - tons of nitrogen oxides out of the stacks that year
 - `PSTATABB`  [filter]
      - the two-letter state the plant sits in

**LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022**
one row = one power plant, one year
connects: DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE equals ORISPL on the other four years and matches PLANT_CODE on ENERGY__FED_EIA860_4_OWNER
 - `DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE`  [join]
      - the federal plant code, same number the other years call ORISPL
 - `PLANT_NAME`  [label]
      - the name of the power plant as the agency lists it
 - `UTILITY_NAME`  [label]
      - the name of the utility tied to the plant
      - WATCH: Long-caption headers, unlike the other years. Whether PLANT_TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_NAME is the same field as OPRNAME is not checked.
 - `PLANT_PRIMARY_FUEL`  [filter]
      - the plant's main fuel as a short code: SUN solar, NG gas, WAT hydro, WND wind
 - `PLANT_NAMEPLATE_CAPACITY_MW`  [measure]
      - the plant's rated maximum output, in megawatts
 - `PLANT_ANNUAL_NET_GENERATION_MWH`  [measure]
      - electricity the plant actually made in 2022, in megawatt-hours
 - `PLANT_ANNUAL_CO2_EMISSIONS_TONS`  [measure]
      - tons of carbon dioxide out of the stacks in 2022
 - `PLANT_ANNUAL_SO2_EMISSIONS_TONS`  [measure]
      - tons of sulfur dioxide out of the stacks in 2022
 - `PLANT_ANNUAL_NOX_EMISSIONS_TONS`  [measure]
      - tons of nitrogen oxides out of the stacks in 2022
 - `DATA_YEAR`  [date]
      - the year the emissions numbers cover, 2022 on this table

**LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER**
one row = one owner's share of one generator
connects: PLANT_CODE, cast text to number, matches the plant code on the emissions tables
 - `PLANT_CODE`  [join]
      - the federal plant code, stored as text; cast to number before matching
      - WATCH: Only 2,369 distinct plants against 11,974 in the 2022 emissions table. Most plants have no owner row.
 - `GENERATOR_ID`  [label]
      - the id of one generating unit inside the plant
 - `OWNER_NAME`  [label]
      - the name of the company that owns a share of that generator
      - WATCH: One vintage, given as 2024, no year column. A plant sold since 2019 is credited to the wrong company.
 - `OWNERSHIP_ID`  [label]
      - the number the energy agency gives that owner
 - `PERCENT_OWNED`  [measure]
      - the owner's share of the generator; the profile shows only 0 and 1, so check it before weighting
 - `UTILITY_ID`  [label]
      - the number the energy agency gives the utility that reports the plant
 - `UTILITY_NAME`  [label]
      - the name of the utility that reports the plant

---

## 115) Which employers, counted by the tax number on the form, run work sites that hurt people far more than their industry does, three years in a row?  `W125` grade B
   - The same owner with the same bad rate at different buildings means the problem is the company, not one unlucky site. If high rates stay with single sites, the building is the right unit.

**LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 to 2025 (3 tables, same columns)**
one row = one establishment's yearly injury summary
connects: ESTABLISHMENT_ID matches ESTABLISHMENT_ID across the years; EIN, left-padded to 9, matches EIN on CORPORATE_REGISTRY__FED_IRS_EO_BMF and SPONS_DFE_EIN on FED_DOL_FORM5500_FULL
 - `ESTABLISHMENT_ID`  [join]
      - OSHA's id for one work site, the same number year to year
 - `EIN`  [join]
      - the employer's tax id as typed on the form; left-pad to 9 digits
      - WATCH: Filled 89.62% in 2023, 89.15% in 2024, 88.7% in 2025. Blank on 43,260 of 398,620 rows in 2024; leading zeros stripped on 14,083 rows. Pad before joining.
 - `ESTABLISHMENT_NAME`  [label]
      - the name of the work site as typed on the form
 - `COMPANY_NAME`  [label]
      - the company name as typed on the form, free text
      - WATCH: Not the company: reads 'Facility 982' on the Caltrans rows. Group on EIN, never the name.
 - `NAICS_CODE`  [filter]
      - the six-digit industry code the site picked for itself
 - `STATE`  [filter]
      - the two-letter state the work site is in
 - `ANNUAL_AVERAGE_EMPLOYEES`  [measure]
      - average number of workers at the site over the year
 - `TOTAL_HOURS_WORKED`  [measure]
      - hours all workers put in that year, the bottom of any injury rate
      - WATCH: Not per site for multi-site filers: Caltrans files 470 rows in 2024 with 14 distinct hour values. Keep 800 to 3,000 hours per employee, 88% of rows.
 - `TOTAL_INJURIES`  [measure]
      - count of work injuries the site wrote on the form that year
 - `TOTAL_DAFW_CASES`  [measure]
      - count of cases where the worker missed days of work
 - `TOTAL_DJTR_CASES`  [measure]
      - count of cases where the worker was moved or put on light duty
 - `TOTAL_DEATHS`  [measure]
      - count of workers who died on the job that year
 - `YEAR_FILING_FOR`  [date]
      - the calendar year the form covers; one value per table

**LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF**
one row = one tax-exempt organization
connects: EIN matches padded EIN on the OSHA tables
 - `EIN`  [join]
      - the nine-digit tax id of one tax-exempt organization
      - WATCH: Names nonprofits only: 6,930 shared tax ids in 2023, 6,414 in 2024, 6,455 in 2025.
 - `ORG_NAME`  [label]
      - the nonprofit's name on the IRS list
 - `STATE`  [filter]
      - the two-letter state of the nonprofit's mailing address
 - `NTEE_CODE`  [label]
      - the IRS category code for what kind of nonprofit it is

**LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL**
one row = one benefit-plan annual filing
connects: SPONS_DFE_EIN matches padded EIN on the OSHA tables
 - `SPONS_DFE_EIN`  [join]
      - the tax id of the employer that sponsors the benefit plan
      - WATCH: Matches 20,756 of 109,146 OSHA tax ids in 2024, 19.0%, because only plan sponsors file. Fill not measured.
 - `SPONSOR_DFE_NAME`  [label]
      - the name of the employer that sponsors the benefit plan
 - `SPONS_DFE_MAIL_US_STATE`  [filter]
      - the two-letter state of the sponsor's mailing address
 - `BUSINESS_CODE`  [label]
      - the industry code the plan sponsor put on the filing

---

## 116) Which mine companies had workers die on the job while the inspectors barely wrote them up beforehand?  `P-146` grade A
   - Deaths on file with no warnings before them means either nobody was inspecting or the citations miss the real danger. If deaths per citation is flat, citations track danger about as well as a count can.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS**
one row = one reported accident or injury
connects: CONTROLLER_ID matches CONTROLLER_ID on LABOR__FED_MSHA_VIOLATIONS; MINE_ID matches MINE_ID on LABOR__FED_MSHA_VIOLATIONS and LABOR__FED_MSHA_MINES
 - `MINE_ID`  [join]
      - the mine safety agency's id for one mine
 - `CONTROLLER_ID`  [join]
      - the id of the company that controlled the mine when the accident happened
 - `CONTROLLER_NAME`  [label]
      - the name of that controlling company
 - `IS_FATALITY`  [filter]
      - true when someone died; 1,208 rows are true
      - WATCH: 1,208 deaths over thousands of controllers. A ratio on one death is noise; set a floor such as two or more.
 - `DEGREE_INJURY`  [filter]
      - how bad it was, in words: days away from work, restricted duty, accident only, and so on
 - `NARRATIVE`  [label]
      - the written account of what happened, free text
 - `ACCIDENT_DATE`  [date]
      - the calendar day the accident happened at the mine
      - WATCH: Accidents start in 2000, citations in 1994. Use 2000 onward for both.
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one citation or order
connects: CONTROLLER_ID and MINE_ID match the same columns on LABOR__FED_MSHA_ACCIDENTS
 - `MINE_ID`  [join]
      - the mine safety agency's id for the mine that got cited
 - `CONTROLLER_ID`  [join]
      - the id of the company that controlled the mine on the day of the citation
 - `VIOLATION_NO`  [label]
      - the number printed on one citation or order
 - `SIG_SUB`  [filter]
      - Y when the inspector called the hazard serious, likely to hurt someone; N when not
 - `IS_SIGNIFICANT_AND_SUBSTANTIAL`  [filter]
      - the same serious-hazard mark as SIG_SUB, stored as true or false
 - `VIOLATION_OCCUR_DATE`  [date]
      - the calendar day the violation itself happened at the mine
 - `EVENT_NO`  [join]
      - the id of the inspection visit that produced the citation; count distinct for visits

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES**
one row = one mine, current state
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_ACCIDENTS
 - `MINE_ID`  [join]
      - the mine safety agency's id for one mine
 - `NO_EMPLOYEES`  [measure]
      - how many people work at the mine today
      - WATCH: Null on 39,735 of 91,906 mines. The per-worker rate covers only part of the field.
 - `CURRENT_MINE_TYPE`  [filter]
      - Surface, Underground or Facility, as of today
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal
 - `CURRENT_MINE_STATUS`  [filter]
      - whether the mine is Active, Abandoned, Intermittent or Temporarily Idled today

---

## 117) When a mine gets a new company name on its citations, do the serious write-ups suddenly drop?  `P-147` grade A
   - A hard drop right after a handover, bigger than at mines that never sold, suggests a new name buys a clean slate. If the rate is flat, it is a new name on the same mine with the same citations.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one citation or order
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_MINES; the handover is read inside this table, where CONTROLLER_ID changes within one MINE_ID ordered by VIOLATION_ISSUE_DATE
 - `MINE_ID`  [join]
      - the mine safety agency's id for the mine that got cited
      - WATCH: Landing copy wraps values in literal double quotes; whether the mart is stripped is not measured.
 - `CONTROLLER_ID`  [join]
      - the id of the company that controlled the mine on the day of the citation
      - WATCH: Empty on 6.76% of citations. An empty value between two real ones is not a change of hands.
 - `VIOLATION_NO`  [label]
      - the number printed on one citation or order
      - WATCH: Sources disagree on 500,990 rows: duplicates or the $100 minimum fine schedule. Count distinct against the row count before deleting.
 - `EVENT_NO`  [join]
      - the id of the inspection visit that produced the citation; count distinct for visits
 - `VIOLATION_ISSUE_DATE`  [date]
      - the day the inspector wrote the citation
      - WATCH: The handover date is the first citation under the new name, not the sale date. Leave out the last 24 months, still in the appeal window.
 - `SIG_SUB`  [filter]
      - Y when the inspector called the hazard serious, likely to hurt someone; N when not
 - `IS_SIGNIFICANT_AND_SUBSTANTIAL`  [filter]
      - the same serious-hazard mark as SIG_SUB, stored as true or false
 - `_LOADED_AT`  [date]
      - when the warehouse loaded the row; bookkeeping, not a mine fact

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES**
one row = one mine, current state
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_VIOLATIONS
 - `MINE_ID`  [join]
      - the mine safety agency's id for one mine
      - WATCH: Profile reports 92,336 distinct on a 91,906-row table. Recount before treating it as unique.
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal
 - `STATE`  [filter]
      - the two-letter state the mine is in
 - `NO_EMPLOYEES`  [measure]
      - how many people work at the mine today
 - `CURRENT_CONTROLLER_ID`  [label]
      - the id of the company controlling the mine today, not in the past
      - WATCH: Today's controller only. It cannot supply the history; the citations table has to.

---

## 118) After a worker dies at one mine, do the same company's other mines suddenly start getting written up more?  `P-148` grade A
   - A jump at the sister mines means either inspectors follow the owner or the owner's other sites were in the same bad shape. No jump means a death stays a one-site event in the record.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS**
one row = one reported accident or injury
connects: where IS_FATALITY is true, CONTROLLER_ID matches CONTROLLER_ID on LABOR__FED_MSHA_VIOLATIONS, keeping MINE_ID different from the death mine
 - `IS_FATALITY`  [filter]
      - true when someone died; 1,208 rows are true
      - WATCH: Only controllers with 2 or more mines count, 6,082 of them. How many of the 1,208 deaths survive that cut is not measured.
 - `ACCIDENT_DATE`  [date]
      - the calendar day the accident happened at the mine
 - `MINE_ID`  [join]
      - the mine safety agency's id for one mine
 - `CONTROLLER_ID`  [join]
      - the id of the company that controlled the mine when the accident happened

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one citation or order
connects: CONTROLLER_ID matches CONTROLLER_ID on LABOR__FED_MSHA_ACCIDENTS; MINE_ID matches MINE_ID on LABOR__FED_MSHA_MINES
 - `CONTROLLER_ID`  [join]
      - the id of the company that controlled the mine on the day of the citation
      - WATCH: Build the sister-mine list from this column as of the death date; the mine table only knows today's controller.
 - `MINE_ID`  [join]
      - the mine safety agency's id for the mine that got cited
      - WATCH: Landing copy carries literal double quotes; mart state not measured. Strip before joining.
 - `VIOLATION_ISSUE_DATE`  [date]
      - the day the inspector wrote the citation
 - `EVENT_NO`  [join]
      - the id of the inspection visit that produced the citation; count distinct for visits
      - WATCH: More citations can mean more inspecting, not more danger. Divide by distinct EVENT_NO and show both numbers.
 - `SIG_SUB`  [filter]
      - Y when the inspector called the hazard serious, likely to hurt someone; N when not
 - `VIOLATION_NO`  [label]
      - the number printed on one citation or order

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES**
one row = one mine, current state
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_VIOLATIONS, for state and mine type
 - `MINE_ID`  [join]
      - the mine safety agency's id for one mine
 - `STATE`  [filter]
      - the two-letter state the mine is in
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal
 - `NO_EMPLOYEES`  [measure]
      - how many people work at the mine today

---

## 119) Do employers guess their yearly injury total instead of counting it, so the numbers pile up on fives and tens?  `P-159` grade A
   - Too many totals ending in 0 or 5 means the federal injury numbers are estimates, and more so at big employers. It shows guessing, not hiding.

**LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 to 2025 (3 tables, same columns)**
one row = one establishment's yearly injury summary
connects: nothing. One table, no join
 - `TOTAL_INJURIES`  [measure]
      - count of work injuries the site wrote on the form that year
      - WATCH: Totals under 10 have no meaningful last digit. Multi-site filers stamp one number on many rows; collapse identical blocks first.
 - `TOTAL_DAFW_CASES`  [measure]
      - count of cases where the worker missed days of work
 - `TOTAL_DJTR_CASES`  [measure]
      - count of cases where the worker was moved or put on light duty
 - `TOTAL_OTHER_CASES`  [measure]
      - count of recordable cases with no days missed and no light duty
 - `TOTAL_DAFW_DAYS`  [measure]
      - total days workers stayed home because of injuries
      - WATCH: Day counts may bunch because of the form's own rules, which are not in the warehouse. Read them before flagging.
 - `TOTAL_HOURS_WORKED`  [measure]
      - hours all workers put in that year, the bottom of any injury rate
      - WATCH: Junk tail: 117 rows over 100M hours in 2024. Caltrans files 470 rows with 14 distinct hour values. Trim to 800 to 3,000 hours per employee.
 - `ANNUAL_AVERAGE_EMPLOYEES`  [measure]
      - average number of workers at the site over the year
 - `SIZE`  [filter]
      - the employer size band as a code; coded value, look at distinct values first
 - `NAICS_CODE`  [filter]
      - the six-digit industry code the site picked for itself
 - `ESTABLISHMENT_ID`  [join]
      - OSHA's id for one work site, the same number year to year
 - `YEAR_FILING_FOR`  [date]
      - the calendar year the form covers; one value per table

---

## 120) After a work site reports a death, what does it write down the next year for hours worked and injuries?  `P-160` grade B
   - Fewer injuries with steady hours looks like the site got safer. Hours collapsing or the site vanishing from the file looks like a shutdown or a reporting change instead.

**LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 to 2025 (3 tables, same columns)**
one row = one establishment's yearly injury summary
connects: ESTABLISHMENT_ID matches ESTABLISHMENT_ID between the 2023, 2024 and 2025 tables
 - `ESTABLISHMENT_ID`  [join]
      - OSHA's id for one work site, the same number year to year
      - WATCH: Not quite unique within a year: 388,245 distinct on 394,234 rows in 2023. Decide how to handle repeats before pairing years.
 - `TOTAL_DEATHS`  [measure]
      - count of workers who died on the job that year
      - WATCH: Small numbers: 859, 812 and 778 a year. A site that vanishes after a death is an outcome; count it, do not drop it.
 - `TOTAL_INJURIES`  [measure]
      - count of work injuries the site wrote on the form that year
 - `TOTAL_DAFW_CASES`  [measure]
      - count of cases where the worker missed days of work
 - `TOTAL_HOURS_WORKED`  [measure]
      - hours all workers put in that year, the bottom of any injury rate
      - WATCH: Wrong for multi-site filers and has a junk tail. A change in hours there is a change in the parent's number.
 - `ANNUAL_AVERAGE_EMPLOYEES`  [measure]
      - average number of workers at the site over the year
 - `NAICS_CODE`  [filter]
      - the six-digit industry code the site picked for itself
 - `STATE`  [filter]
      - the two-letter state the work site is in
 - `YEAR_FILING_FOR`  [date]
      - the calendar year the form covers; one value per table
 - `EIN`  [join]
      - the employer's tax id as typed on the form; left-pad to 9 digits
      - WATCH: Do not join on it: minimum length 1, blank on 43,260 rows in 2024.

---

## 121) When two mines with the same owner get slammed with citations in the same month, is that the owner, or just one inspectors' office working through its patch?  `WN-136` grade B
   - If same-owner pairs still spike together more than neighbors under different owners, trouble really travels with the company. If not, the earlier 34.3% finding was just the inspectors' route.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one citation or order
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_MINES and, after stripping quotes, MINE_ID on LIBRARY_RAW.LANDING.FED_MSHA_MINES
 - `MINE_ID`  [join]
      - the mine safety agency's id for the mine that got cited
 - `CONTROLLER_ID`  [join]
      - the id of the company that controlled the mine on the day of the citation
      - WATCH: Build owner pairs from this column as of the month in question; the mine table holds today's controller only.
 - `VIOLATION_ISSUE_DATE`  [date]
      - the day the inspector wrote the citation
 - `EVENT_NO`  [join]
      - the id of the inspection visit that produced the citation; count distinct for visits
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal

**LIBRARY_RAW.LANDING.FED_MSHA_MINES**
one row = one mine, current state, 62 columns
connects: MINE_ID, quotes stripped, matches MINE_ID on LABOR__FED_MSHA_VIOLATIONS
 - `MINE_ID`  [join]
      - the mine safety agency's id for one mine, wrapped in quote marks here
      - WATCH: Every landing value is wrapped in literal double quotes. Strip before joining. Unstripped, MINE_ID matches nothing.
 - `DISTRICT`  [filter]
      - the agency district office that covers the mine today
      - WATCH: Fill not measured; two columns found by name in this warehouse turned out empty. Count distinct values first. It is today's district, applied to all 32 years.
 - `OFFICE_CD`  [filter]
      - the code of the local field office that inspects the mine
      - WATCH: Fill not measured. Count distinct values first.
 - `OFFICE_NAME`  [label]
      - the name of that local field office
      - WATCH: Fill not measured. Count distinct values first.
 - `STATE`  [filter]
      - the two-letter state the mine is in
 - `FIPS_CNTY_CD`  [filter]
      - the county code for where the mine sits
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal
 - `CURRENT_CONTROLLER_BEGIN_DT`  [date]
      - the day today's controlling company took over the mine

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES**
one row = one mine, current state, 23 columns
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_VIOLATIONS
 - `MINE_ID`  [join]
      - the mine safety agency's id for one mine
      - WATCH: This copy drops DISTRICT, OFFICE_CD and OFFICE_NAME. Kept only for its measured join, 31,277 shared mine ids.
 - `STATE`  [filter]
      - the two-letter state the mine is in
 - `FIPS_CNTY_CD`  [filter]
      - the county code for where the mine sits; 298 distinct values
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal

---

## 122) Do mine inspectors go quiet in the same months every year, and do miners get hurt more in those quiet stretches?  `P-149` grade B
   - If accidents pile up when inspections thin out, the inspection calendar itself is a safety hole. If both calendars just follow how busy the mines are, the season is the work, not the oversight.

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS**
one row = one citation or order
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_ACCIDENTS; count distinct EVENT_NO by month of VIOLATION_ISSUE_DATE
 - `VIOLATION_ISSUE_DATE`  [date]
      - the day the inspector wrote the citation
      - WATCH: Use 2000 onward; the final months of 2026 are partial.
 - `EVENT_NO`  [join]
      - the id of the inspection visit that produced the citation; count distinct for visits
      - WATCH: Appears only when an inspection wrote at least one citation. Clean inspections leave no row, so a well-run mine looks uninspected.
 - `MINE_ID`  [join]
      - the mine safety agency's id for the mine that got cited
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal
 - `MINE_TYPE`  [filter]
      - what kind of mine it is: Surface, Underground or Facility

**LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS**
one row = one citation or order, full 64-column file
connects: one row per distinct EVENT_NO with its INSPECTION_BEGIN_DT and INSPECTION_END_DT; MINE_ID, quotes stripped, matches MINE_ID on LABOR__FED_MSHA_ACCIDENTS
 - `EVENT_NO`  [join]
      - the id of the inspection visit that produced the citation
      - WATCH: Citing inspections only. Inspections that found nothing are not here either.
 - `INSPECTION_BEGIN_DT`  [date]
      - the day that inspection visit started
      - WATCH: Fill not measured; two columns found by name here were empty. Strip quotes before casting; an empty value is a pair of quotes, not NULL.
 - `INSPECTION_END_DT`  [date]
      - the day that inspection visit ended
      - WATCH: Fill not measured. Strip quotes before casting; an empty value is a pair of quotes, not NULL.
 - `MINE_ID`  [join]
      - the mine safety agency's id for the cited mine, wrapped in quote marks here
      - WATCH: Every landing value is wrapped in literal double quotes. Strip before joining. This copy holds 3,087,266 rows against the mart's 3,087,265.
 - `VIOLATION_ISSUE_DT`  [date]
      - the day the inspector wrote the citation
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal

**LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS**
one row = one reported accident or injury
connects: MINE_ID matches MINE_ID on LABOR__FED_MSHA_VIOLATIONS
 - `ACCIDENT_DATE`  [date]
      - the calendar day the accident happened at the mine
      - WATCH: Starts in 2000. Surface mines shut for winter in many states, so a winter dip can be activity.
 - `MINE_ID`  [join]
      - the mine safety agency's id for one mine
      - WATCH: 13,708 mines have an accident row against 32,133 with a citation row. The gap test runs on the 13,338 shared mines.
 - `DEGREE_INJURY`  [filter]
      - how bad it was, in words: days away from work, restricted duty, accident only, and so on
 - `IS_FATALITY`  [filter]
      - true when someone died; 1,208 rows are true
 - `NO_INJURIES`  [measure]
      - how many people were hurt in that one event, usually 1
 - `COAL_METAL_IND`  [filter]
      - C for a coal mine, M for metal or non-metal

---

## 123) Do work sites in the same industry and the same state all report injury rates that run high or low together, beyond what their size explains?  `WN-144` grade B
   - If whole industry-and-state pockets sit far from the national rate, something local is moving everyone, like state rules, one dominant employer or how people report. If not, injury rates are just an industry fact.

**LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 to 2025 (3 tables, same columns)**
one row = one establishment's yearly injury summary
connects: nothing. One table, no join
 - `NAICS_CODE`  [filter]
      - the six-digit industry code the site picked for itself
      - WATCH: Fill not measured. Code editions are mixed; map to one edition or use the first 4 digits.
 - `NAICS_YEAR`  [filter]
      - which edition of the industry code list the site used, such as 2012, 2017 or 2022
      - WATCH: Runs from 0 to 180175 in the 2025 table. Mixed and partly junk.
 - `STATE`  [filter]
      - the two-letter state the work site is in
      - WATCH: Fill not measured. No flag for state-run OSHA programs, so a state effect cannot be split from a reporting-rule effect.
 - `SIZE`  [filter]
      - the employer size band as a code; coded value, look at distinct values first
 - `ANNUAL_AVERAGE_EMPLOYEES`  [measure]
      - average number of workers at the site over the year
 - `TOTAL_HOURS_WORKED`  [measure]
      - hours all workers put in that year, the bottom of any injury rate
      - WATCH: 1,065B hours against 138.8M employees, about 7,672 per employee. Keep rows between 800 and 3,000 hours per employee, 88% of rows.
 - `TOTAL_INJURIES`  [measure]
      - count of work injuries the site wrote on the form that year
      - WATCH: Multi-site filers report zero injuries 49 to 79% of the time against 6.7% for ordinary rows. One big public filer makes a state look safe.
 - `TOTAL_DAFW_CASES`  [measure]
      - count of cases where the worker missed days of work
 - `TOTAL_DJTR_CASES`  [measure]
      - count of cases where the worker was moved or put on light duty
 - `ESTABLISHMENT_ID`  [join]
      - OSHA's id for one work site, the same number year to year
 - `YEAR_FILING_FOR`  [date]
      - the calendar year the form covers; one value per table

---

## 124) Which employers got caught working kids illegally and still collect federal contract money afterward?  `N1` grade C
   - It would be a named list of companies the government fined with one hand and paid with the other. No matches can just mean the contract sits with a parent company at another address.

**LIBRARY_RAW.LANDING.FED_DOL_WHD_ENFORCEMENT**
one row = one closed wage-and-hour case against one employer
connects: LEGAL_NAME, multi-word, upper, trimmed, plus first 5 of ZIP_CD matches RECIPIENT_NAME plus first 5 of RECIPIENT_ZIP_4_CODE on the contract year tables
 - `CASE_ID`  [label]
      - the id of one closed wage investigation
 - `LEGAL_NAME`  [join]
      - the employer's legal name on the case; upper-case and trim before matching
      - WATCH: 3,612 rows have a blank LEGAL_NAME. Multi-word names only: single-word matches were 8% real, multi-word 92%.
 - `TRADE_NM`  [label]
      - the name the business trades under, the sign on the door
 - `ZIP_CD`  [join]
      - the employer's ZIP on the case; use the first 5 characters
      - WATCH: 19 rows have a blank ZIP_CD. Name plus ZIP misses a violation at a plant when the contract is with headquarters in another ZIP.
 - `ST_CD`  [filter]
      - the two-letter state of the employer
 - `NAIC_CD`  [filter]
      - the industry code on the case
 - `FLSA_CL_VIOLTN_CNT`  [measure]
      - count of child-labor violations found in the case
 - `FLSA_CL_MINOR_CNT`  [filter]
      - count of minors found working illegally in the case; 113 distinct values
      - WATCH: Filled on all 367,890 rows, 113 distinct values. How many rows are above zero is not measured.
 - `FLSA_CL_CMP_ASSD_AMT`  [measure]
      - dollars of fines assessed for the child-labor violations
 - `FINDINGS_START_DATE`  [date]
      - the first day of the period the investigator looked at
      - WATCH: Typo years 0200 and 3021; 954 rows have no parseable start date. Bound dates to 1990 to 2030.
 - `FINDINGS_END_DATE`  [date]
      - the last day of the period the investigator looked at
      - WATCH: Typo years 0200 and 3021. Bound dates to 1990 to 2030.

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: RECIPIENT_NAME plus first 5 of RECIPIENT_ZIP_4_CODE matches LEGAL_NAME plus first 5 of ZIP_CD on FED_DOL_WHD_ENFORCEMENT
 - `RECIPIENT_NAME`  [join]
      - the name of the company that got the contract money
      - WATCH: Not a real id: a name match. Landing columns here can be case-sensitive lowercase; confirm on one year table.
 - `RECIPIENT_UEI`  [label]
      - the government's id for the company that got the money
 - `RECIPIENT_PARENT_NAME`  [label]
      - the name of the recipient's parent company
 - `RECIPIENT_ZIP_4_CODE`  [join]
      - the recipient's ZIP plus four; use the first 5 characters
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed by this one contract action; negative means money taken back
      - WATCH: Signed: de-obligations are negative rows. Filter to positive.
 - `ACTION_DATE`  [date]
      - the day this contract action was signed
 - `AWARDING_AGENCY_NAME`  [label]
      - the federal agency that awarded the contract
 - `AWARD_ID_PIID`  [label]
      - the contract's id number; a new one first seen means a new award

---

## 125) Which employers flagged as repeat wage cheats keep getting new federal contract money year after year?  `N5` grade C
   - It would show the government keeps paying companies it has already caught shorting workers more than once. A miss means repeat violators are mostly small local shops, or the name match cannot see the real contracting company.

**LIBRARY_RAW.LANDING.FED_DOL_WHD_ENFORCEMENT**
one row = one closed wage-and-hour case against one employer
connects: LEGAL_NAME, multi-word, upper, trimmed, plus first 5 of ZIP_CD matches RECIPIENT_NAME plus first 5 of RECIPIENT_ZIP_4_CODE on the contract year tables
 - `CASE_ID`  [label]
      - the id of one closed wage investigation
 - `LEGAL_NAME`  [join]
      - the employer's legal name on the case; upper-case and trim before matching
      - WATCH: 3,612 rows have a blank LEGAL_NAME. Multi-word names only: single-word matches were 8% real, multi-word 92%.
 - `TRADE_NM`  [label]
      - the name the business trades under, the sign on the door
 - `ZIP_CD`  [join]
      - the employer's ZIP on the case; use the first 5 characters
      - WATCH: 19 rows have a blank ZIP_CD. Name plus ZIP misses parents, subsidiaries and worksites in other ZIPs.
 - `ST_CD`  [filter]
      - the two-letter state of the employer
 - `FLSA_REPEAT_VIOLATOR`  [filter]
      - repeat or willful mark: R repeat, W willful, RW both, N/A on 346,361 rows
      - WATCH: Measured 2026-09-18: R 15,146, W 4,381, RW 2,002, N/A 346,361. Marked cases are 21,529, 5.85% of the file.
 - `FLSA_VIOLTN_CNT`  [measure]
      - count of minimum-wage and overtime violations found in the case
 - `FLSA_BW_ATP_AMT`  [measure]
      - dollars of back wages the employer agreed to pay under the wage law
 - `FLSA_CMP_ASSD_AMT`  [measure]
      - dollars of fines assessed under the wage law
 - `SCA_VIOLTN_CNT`  [measure]
      - count of violations of the wage law for federal service contractors
 - `DBRA_VIOLTN_CNT`  [measure]
      - count of violations of the wage law for federal construction contractors
 - `FINDINGS_START_DATE`  [date]
      - the first day of the period the investigator looked at
      - WATCH: Typo years 0200 and 3021; 954 rows have no parseable start date. Bound dates to 1990 to 2030.
 - `FINDINGS_END_DATE`  [date]
      - the last day of the period the investigator looked at
      - WATCH: Typo years 0200 and 3021. Bound dates to 1990 to 2030.

**LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to FY2026 (20 tables, same columns)**
one row = one contract transaction
connects: RECIPIENT_NAME plus first 5 of RECIPIENT_ZIP_4_CODE matches LEGAL_NAME plus first 5 of ZIP_CD on FED_DOL_WHD_ENFORCEMENT
 - `RECIPIENT_NAME`  [join]
      - the name of the company that got the contract money
      - WATCH: Not a real id: a name match, multi-word names only.
 - `RECIPIENT_UEI`  [label]
      - the government's id for the company that got the money
 - `RECIPIENT_ZIP_4_CODE`  [join]
      - the recipient's ZIP plus four; use the first 5 characters
 - `FEDERAL_ACTION_OBLIGATION`  [measure]
      - dollars committed by this one contract action; negative means money taken back
      - WATCH: Signed: de-obligations are negative rows. Filter to positive. Dollars include add-ons to old awards, so winning is not visible here.
 - `ACTION_DATE`  [date]
      - the day this contract action was signed
 - `ACTION_DATE_FISCAL_YEAR`  [date]
      - the federal budget year the action falls in
 - `AWARDING_AGENCY_NAME`  [label]
      - the federal agency that awarded the contract
 - `AWARD_ID_PIID`  [label]
      - the contract's id number; a new one first seen means a new award
      - WATCH: Use values first seen after the case to mean a new award.

---
