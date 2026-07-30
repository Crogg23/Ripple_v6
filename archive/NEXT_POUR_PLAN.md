# Next Pour Plan — Ranked by Effort

Generated: 2026-07-27 | All public data, all free unless noted.

The order here is: **fastest to land first, highest connection-value first within each tier.** Each item notes what it connects to in the existing graph.

---

## TIER 1: One-command pours (direct download, loader pattern exists)

These are CSV/ZIP downloads with no auth. Build a loader, run it, done.

| # | Dataset | Size est. | Key type | Connects to (already landed) | Notes |
|---|---------|-----------|----------|------------------------------|-------|
| 1 | **FEC Leadership PAC sponsors** | ~5K rows | FEC_ID | FEC committees, legislators (BIOGUIDE) | Pre-built bridge: which member controls which PAC. fec.gov/files/bulk-data/ |
| 2 | **Housestockwatcher.com (STOCK Act trades)** | ~30K rows | BIOGUIDE | Legislators, SEC CIK (landed), Voteview | Free CSV maintained by civic tech. Completes insider-trading triangle. |
| 3 | **IRS 990 e-file index** | ~3M rows | EIN | IRS BMF (1.9M EINs landed), USASpending | Replaces your 200-row test load. CSV index → links to XML returns. s3.amazonaws.com/irs-form-990/ |
| 4 | **OpenSanctions bulk** | ~500K entities | Multi (IMO, name, address) | OFAC SDN (landed), GLEIF, legislators | 400+ sanctions/PEP lists unified. opensanctions.org CC-BY-NC. Daily refresh. |
| 5 | **FARA registrations (full bulk)** | ~222K (already landed but stale?) | FARA_REG_ID, name | OFAC, LDA lobbying (loading), legislators | Verify your FED_FARA_BULK is current. efile.fara.gov daily zips. |
| 6 | **EPA FRS uncapped** | ~4M facilities | FRS_ID, EIN | EPA ECHO (landed), USASpending, IRS BMF | Your current load is capped at 500K. Remove the cap → crosswalk jumps from 1.9% to ~60%. |
| 7 | **SEC Form 3/4/5 (insider transactions)** | ~5M rows | CIK | SEC 13F (just landed), EDGAR financials, GLEIF | Ownership backbone. sec.gov/files/dera/data/ quarterly TSV zips. |
| 8 | **FMCSA Motor Carrier Census** | ~1M carriers + 20M inspections | USDOT, EIN | USASpending, DOL OSHA (landed) | "Chameleon carriers" detector. ai.fmcsa.dot.gov bulk CSVs. |
| 9 | **FEC independent expenditures (full history)** | ~2M rows | FEC_ID | FEC contributions (84M landed), legislators | You have 261K. Full file goes back to 2008. fec.gov bulk. |
| 10 | **MEDSL election returns (House + President)** | ~500K rows | FIPS, BIOGUIDE | Voteview, legislators, Census | You have Senate. Add House + President. harvard.edu/doi:10.7910/DVN/VOQCHQ |
| 11 | **DOL OLMS (union finances)** | ~200K filings | EIN | IRS BMF, Form 5500 (landed) | Union self-dealing detector. olmsapps.dol.gov yearly pipe-delimited zips. |
| 12 | **PHMSA Pipeline Incidents** | ~50K incidents | OPID | EPA (landed), USASpending (operator→contractor) | phmsa.dot.gov CSV. Repeat-violator pattern. |
| 13 | **NHTSA Recalls + FARS (fatalities)** | ~30K recalls + 1M fatalities | VIN-prefix, make/model | CPSC NEISS (just landed) | static.nhtsa.gov flat files. Harm endpoint. |
| 14 | **ATF FFL Listings** | ~130K licensees | FFL_ID, name/address | ARCOS (just landed, DEA_NO) | data.gov mirror (atf.gov blocks scrapers). Geographic clustering detector. |
| 15 | **NIH ExPORTER** | ~1M grants | FAIN, PI name | USASpending (FAIN join), NPI (PI→provider) | reporter.nih.gov annual CSVs. Research-money lens. |
| 16 | **UK Companies House** | ~6M companies | Company number, LEI | GLEIF (3.4M LEIs landed), OpenSanctions | download.companieshouse.gov.uk monthly CSV. Offshore/shell detection. |
| 17 | **ROR (Research Organization Registry)** | ~110K orgs | ROR_ID, LEI, Wikidata | GLEIF, NIH grants, USASpending | doi.org/10.5281/zenodo — org-resolution glue for research money. |
| 18 | **FRA Safety Data (rail)** | ~300K crossings + incidents | Crossing ID, railroad name | DOT, OSHA (landed) | safetydata.fra.dot.gov CSV/DBF. Repeat-fatal-crossing pattern. |
| 19 | **FSIS Meat/Poultry Directory** | ~7K plants | Establishment #, name | OSHA (landed), EPA (landed) | fsis.usda.gov weekly CSV. Food-safety harm. |
| 20 | **FAA Releasable Airmen** | ~1M pilots/mechanics | Certificate #, name | (future: aircraft registry) | faa.gov monthly CSV. Revoked-airman pattern. |

---

## TIER 2: Needs a free key or minor setup

| # | Dataset | Key signup | Connects to | Notes |
|---|---------|-----------|-------------|-------|
| 21 | **BIS Consolidated Screening List** | developer.trade.gov (free) | USASpending, EDGAR, GLEIF | "Denied party still a subawardee?" Export-restricted entities. |
| 22 | **GovInfo Bill Text + Status** | api.govinfo.gov (free key) | LDA lobbying (bill numbers), Voteview (roll calls) | Closes the "lobbied bill → vote" triangle. Large XML corpus. |
| 23 | **OSHA inspections full bulk** | enforcedata.dol.gov or Login.gov DOL key | DOL MSHA (landed), USASpending, EPA | You have MSHA. OSHA ITA is partially landed. Full inspection data needs the Login.gov key. |
| 24 | **Census API (ACS demographics)** | api.census.gov/data/key_signup.html | FIPS joins to everything geographic | Context data: income/race/health by geography. Enriches detector output. |
| 25 | **CourtListener API** | courtlistener.com (free token) | Dockets (71M rows landed) | Adds party names to your landed dockets. Slow crawl but high-value entity resolution. |

---

## TIER 3: Parsing/joining projects (data exists, needs engineering)

| # | Dataset | What's needed | Payoff |
|---|---------|--------------|--------|
| 26 | **LDA → Voteview bill-number join** | Parse bill numbers from LDA SPECIFIC_ISSUES text, match to Voteview roll calls | "This bill was lobbied by X, voted yes by Y who received $Z from X's PAC" — the full influence loop |
| 27 | **IRS 990 XML Schedule I/R parsing** | Bulk download (~TB of XML), extract grants-out + related-org tables | Dark-money graph: who funds whom. Multi-sprint project. |
| 28 | **Congressional financial disclosures (Senate XML)** | efdsearch.senate.gov structured data | Member assets + positions. Senate is XML; House is mostly PDF. |
| 29 | **EPA FRS Program Linkages** | echo.epa.gov crosswalk file → multi-key bridge table | Connects all EPA programs (RCRA, SDWA, TRI, NPDES) via FRS_ID. |
| 30 | **Congressional hearing witnesses** | govinfo.gov/bulkdata/CHRG/ (XML hearing transcripts) | Who testifies + which companies/orgs they represent → lobbying correlation. |

---

## TIER 4: Hard / Needs a decision from you

| # | Dataset | The catch | Worth it? |
|---|---------|-----------|-----------|
| 31 | **OpenCorporates** | ODbL license = disclose project publicly | Solves 50-state SoS problem. RED-lane call. |
| 32 | **State campaign finance (all 50)** | 50 different portals, no unified bulk | followthemoney.org aggregates but commercial. |
| 33 | **State bar directories** | No bulk APIs, per-state scraping | "Disbarred but still filing" — dockets already landed. |
| 34 | **NMLS (mortgage originators)** | No bulk file exists; lookup-only | Low priority — HMDA LEI (landed) covers the institution level. |
| 35 | **White House visitor logs** | Administration-dependent publication | When available: easy CSV. Currently: unclear status. |

---

## Suggested attack order

**Sprint A (this week — direct downloads, high graph value):**
1. FEC Leadership PAC sponsors (#1)
2. Housestockwatcher STOCK Act (#2)
3. IRS 990 e-file index (#3)
4. EPA FRS uncap (#6)
5. SEC insider transactions (#7)

**Sprint B (next — broadens the network):**
6. OpenSanctions (#4)
7. FMCSA Motor Carrier (#8)
8. MEDSL full election returns (#10)
9. BIS Screening List (#21)
10. GovInfo bills (#22)

**Sprint C (depth — harm endpoints + money-out):**
11. NIH ExPORTER (#15)
12. UK Companies House (#16)
13. DOL OLMS unions (#11)
14. PHMSA pipelines (#12)
15. NHTSA/FARS (#13)

**Sprint D (engineering projects):**
16. LDA → bill-number → Voteview join (#26)
17. 990 XML Schedule I/R (#27)
18. Congressional disclosures (#28)
19. EPA program linkages (#29)

---

*This is a living plan. Cross items off as they land. The connection engine will wire new tables automatically once they have recognized key columns (NPI, EIN, CIK, UEI, LEI, IMO, BIOGUIDE, ICPSR, DEA_NO).*
