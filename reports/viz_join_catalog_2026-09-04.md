# What the warehouse can visualize across a join — catalog, 2026-09-04

Source: `LIBRARY_META."CONNECT".CONNECT_EDGES` (4,512 proven table pairs, 30 key types)
and `KEYSET_LIVE` (290M key rows, 41 key types). Numbers are live as of today.
Shape of every item: **X per Y relative to Z**. Y is the join key. Z is the second table's attribute.

## Key families that carry joins

| Key | Tables | Edges | Matched rows | Quality |
|---|---|---|---|---|
| NPI | 34 | 364 | 117M | steel, ~100% |
| EIN | 34 | 366 | 10.4M | steel, 86–100% |
| FRS_ID | 17 | 136 | 54.6M | steel, ~100% |
| CCN | 25 | 78 | 0.5M | steel, ~100% |
| CIK | 19 | 128 | 0.4M | steel, 90–100% |
| FIPS | 15 | 78 | 0.2M | county, 73–100% |
| NPDES_ID | 10 | 45 | 4.7M | steel |
| PWSID | 10 | 45 | 8.5M | steel |
| FEC_CMTE_ID / CAND_ID | 10 / 9 | 81 | 0.5M | 72–100% |
| UEI / DUNS | 9 / 5 | 21 | 0.1M | 10–80%, sparse |
| LEI | 7 | 21 | 3.2M | steel |
| CL_PERSON_ID | 8 | 28 | 0.1M | steel |
| DOCKET | 17 | 2 | 8K | mostly unproven |
| EIA_PLANT_ID / UTILITY_ID | 10 / 12 | 0 | — | in keyset, no edges yet |
| PECOS_PAC_ID / ENRLMT_ID | 9 / 8 | 0 | — | in keyset, no edges yet |
| AWARD_KEY | 4 | 0 | — | 94.7M rows, no edges yet |
| NAICS / SIC | 16 / 17 | 0 | — | classifiers, join by code |
| CIK~EIN, EIN~UEI, DUNS~UEI | cross | 139 | — | 2–16% match, thin |
| NAME@ZIP | 122 | 2,512 | 38M | fuzzy, 8% single-word real |
| GEO_IN | 22 | 52 | — | TRAP: FR data.gouv matches everything |

## The catalog

### Health providers — NPI, CCN, PECOS
1. Open Payments dollars per prescriber relative to Part D claim volume
2. Opioid Part D claims per NPI relative to opioid-maker payments
3. Medicare Part B payments per provider relative to specialty peers by state
4. Order-and-referring volume per NPI relative to enrollment status
5. Home health NPIs per agency CCN relative to county population
6. Nursing home deficiencies per CCN relative to ownership type
7. Deficiencies per nursing home relative to MDS resident-days
8. SNF enrollments per PECOS PAC relative to facility affiliations count
9. Hospitals per physician affiliation relative to hospital enrollment size
10. Providers per zip relative to HPSA shortage designation

### Nonprofits and employers — EIN
11. 990 e-filings per EIN relative to BMF asset class
12. Revocations per state relative to active nonprofits
13. Pub78 eligibility per subsection code relative to BMF total
14. OSHA injuries per employer EIN relative to NAICS peer rate, 3 years
15. Federal assistance dollars per nonprofit relative to reported revenue
16. Single audits per auditee relative to award dollars received

### Federal money — UEI, DUNS, AWARD_KEY
17. Contract dollars per vendor relative to assistance dollars
18. Subawards per prime relative to prime contract value
19. NIH grants per org relative to SBIR awards
20. Exclusions per vendor relative to active contract dollars
21. Awards per agency relative to recipients per state

### Public companies — CIK
22. Auditor engagements per PCAOB firm relative to filer size
23. Insider filings per company relative to market cap
24. 13F holdings per manager relative to filer count
25. OSHA injury rate per public company relative to revenue, thin

### Environment — FRS_ID, NPDES_ID, PWSID, EIA
26. Violations per NPDES permit relative to inspections
27. Enforcement actions per facility relative to NAICS sector
28. Quarterly noncompliance per permit relative to SIC code
29. SDWA violations per water system relative to population served
30. Site visits per water system relative to violations
31. Lead sample exceedances per PWSID relative to service area
32. Air emissions per FRS facility relative to corporate parent
33. TRI releases per facility relative to county
34. Generators per plant relative to utility owner
35. eGRID emissions per plant relative to owner share
36. MSHA violations per mine relative to accidents

### Counties — FIPS
37. EPA facilities per county relative to QCEW employment
38. Drug poisoning deaths per county relative to HPSA shortage
39. Incarceration rate per county relative to injury deaths
40. FEMA housing registrations per county relative to population
41. Health shortage areas per county relative to provider count

### Politics — FEC, BIOGUIDE, ICPSR
42. Individual contributions per committee relative to candidate
43. PAC receipts per committee relative to individual contributions
44. Leadership PACs per candidate relative to committees linked
45. Committee-to-candidate transfers per PAC relative to PAC summary
46. Bills cosponsored per legislator relative to Voteview ideology
47. Committee memberships per legislator relative to bills sponsored

### Courts — CL_PERSON_ID, DOCKET, CL_COURT_ID
48. Positions per judge relative to political affiliation
49. Financial disclosures per judge relative to positions held
50. Judges per court relative to dockets filed
51. Opinions per docket relative to FJC case type
52. Oral arguments per case relative to opinion count

### Corporate registries — LEI, COMPANY_NO
53. Subsidiaries per GLEIF parent relative to EPA facilities
54. PSC owners per UK company relative to SIC code
55. HMDA loans per lender LEI relative to GLEIF entity

## Traps to respect
- GEO_IN edges to INTL_FR_DATA_GOUV_FULL are 100% match on 22 tables. Not real. Skip.
- NAME@ZIP is fuzzy. Multi-word names only.
- CIK~EIN and EIN~UEI match 2–16%. Show as a sample, never a rate.
- USAspending FULL tables are zip-truncated. Counts are floors.
- Portal tables cap at 10,000 rows.

## Added after the code sweep — keys the edge table has not built yet
Found in `connect/keys.py` TABLE_COLUMN_KEYS and `connect/bridge.py`. In the keyset or pinned by table, zero edges.

56. 13F positions per manager relative to CUSIP issuer — FED_SEC_13F_HOLDINGS × FTD_CUSIP_BRIDGE
57. Branch deposits per bank relative to FHLB membership — FDIC_CERT / RSSD
58. Mines per controller relative to violations per operator — MSHA_CONTROLLER_ID / OPERATOR_ID
59. Contract dollars per CAGE code relative to SAM exclusions — CAGE
60. Vessels per owner relative to port calls — IMO / MMSI, 2 tables
61. Any county metric relative to population — DIM_COUNTY.POPULATION_2020, 3,222 rows
62. Any zip metric rolled to county — XWALK_ZCTA_COUNTY, 46,960 rows

Bridge rule: only HARD×HARD crosswalks are materialized. NPI, EIN, CIK, DUNS, CCN, IMO, MMSI, UEI, LEI.
Code keys never bridge: NAICS, SIC, NCES, DOCKET, PATENT, FIPS, ZIP.
