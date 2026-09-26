# Top 3 portfolio leads, flushed out, 2026-09-24

Leads #2 Reliant Care, #7 Texas hospice farms and #1 Las Vegas Sands from `LEADS.md`.
Ranked after a press check: Reliant first, hospices second, Sands third.
Every person or company named is a data match, not verified against primary records. Nothing here is published.
Warehouse numbers come from the saved dossiers and their skeptic passes. Nothing was re-queried today.
Press facts come from the web sources listed at the bottom of each section. They are not in the warehouse.

---

## 1. Reliant Care Management, Missouri

**Dossier:** `joins/j1.md`, skeptic `joins/j1_skeptic.md`. Related: LEADS #40, #121 (deep3 g00), #169 (deep3 g50).
**Grade:** B after the skeptic's fixes.

### The numbers, skeptic-corrected

| Measure | Reliant, 30 MO homes | Other MO for-profit | Gap |
|---|---|---|---|
| Nurse hours per resident per day | 2.16 | 3.35 | 35% fewer |
| RN hours per resident per day | 0.19 | 0.39 | about half |
| Harm citations per 100 beds, since 2023-06-17 | 4.67 | 1.23 | 3.8x |
| Fine dollars per 100 beds, 2023-06 to 2026-03 | $117,358 | $27,138 | 4.3x |
| Homes fined | 23 of 30 | 44% of others | |
| Harm per 100 beds, lowest staffing bin under 2.5 hrs | 5.10 | 2.07 | 2.5x pooled; median home 2.0x; per inspection 1.4x |
| Share of MO nursing-home residents with schizophrenia | 22% to 41% | | Reliant holds 7% of residents |
| MO registered sex offenders at a nursing-home address | 90 of 287, at five Reliant homes | | Reliant homes hold 2.2% of residents |
| Covid Provider Relief Fund, name match | $12.23M, 17 lines | | floor, no payment dates |
| PPP loans, any size | none | | real miss, both PPP sources checked |
| Owner's federal political gifts | $115K to $138K, both parties | | corrected for FEC duplicate rows |

- **Owner:** Richard J. DeStefane, on 31 of 32 chain-446 homes. Closed family chain. No private equity, no REIT.
- **Four homes carry half the harm:** Bridgewood, North Village Park, Heritage, Gregory Ridge. They hold 76 of 141 harm citations. Without them, harm and fines run 2.5x, not 3.8x and 4.3x.
- **The count is 30 MO homes, not 31.** Cassville has no Reliant owner row; NursingHome411 puts it with Prime Healthcare.
- **Dropped by the skeptic:** the before/after-takeover chart. Adding Holton KS flips it, 1.07 to 0.97.

### Chain

| Join | Checked | Hit means | Miss means |
|---|---|---|---|
| Roster to owner file, CCN to ENROLLMENT_ID to owner ID | 32 CCNs land; 31 carry a Reliant/DeStefane row | one family controls the chain | Cassville's chain label is likely wrong |
| Staffing, same row as the roster | resident-weighted means, 30 of 31 homes have hours | the gap is from CMS payroll data, not self-report | Portageville blank |
| Deficiencies and penalties, CCN | 418,479 distinct rows; FINE_IDs distinct | harm and fines are real rows | |
| Same-staffing bins | harm per 100 beds inside each staffing band | the operator adds harm beyond staffing | |
| Schizophrenia share, MDS frequency file, CCN | 9,560 homes hide 1-10 counts | Reliant share is a 22-41% range | |
| Sex-offender registry to nursing-home address | house number + first street word + ZIP | registrants live at these homes | no citation tied to a registrant |

### Already public

- **2017 DOJ settlement:** $8,368,878, for billing Medicare for unnecessary physical, speech and occupational therapy. Signed July 5, 2017.
- **Corporate integrity agreement,** OIG's five-year federal monitoring deal: July 5, 2017 to April 18, 2023. It covered Reliant Care Group, Reliant Care Management, the rehab arm, and 12 homes including Bernard, Bridgewood, Four Seasons, Heritage, Milan and North Village Park.
- **Tallgrass Economics, Dave Kingsley, Nov 10, 2024:** "the worst nursing home chain in America." Cost-report figures: $161.6M patient revenue, $28.8M paid to the home office and related companies, 90% Medicaid days. No mention of schizophrenia or sex offenders.
- **ProPublica Nursing Home Inspect, affiliate a-446:** 2.2 serious deficiencies vs 0.7 national, 2.5 nurse hours vs 3.9, 64.7% nurse turnover.
- **Reliant's own website:** it serves "the elderly and those 18 and older afflicted with mental illnesses in addition to a primary medical diagnosis."
- CMS already rates Reliant 2nd-worst of 301 chains.

### What's new

- The psychiatric concentration: 22-41% of the state's nursing-home schizophrenia residents, and 90 of 287 nursing-home registrants, in one thin-staffed chain.
- The same-staffing test: the harm gap survives inside each staffing band.
- The timing: the warehouse's harm window opens 2023-06-17, two months after the federal monitoring deal ended. CMS's archived deficiency files could test before vs after.
- The owner map, the relief money, and the court list in one place.

### The other side, and the traps

- "We serve residents nobody else will take." True, and it's the stated business model. It explains acuity; it doesn't explain half the RN hours.
- Complaint-driven counts: Reliant homes get about twice the inspections. Per inspection, the gap is 1.4x to 2.0x.
- Schizophrenia coding: the New York Times reported in 2021 that nursing homes miscode schizophrenia, which removes residents from CMS's antipsychotic-drug measure. CMS began auditing that coding in 2023. Check whether Reliant homes carry the audit flag on Care Compare before leaning on the 22-41%.
- Staffing is one snapshot, not a time series.
- Political gifts are legal; present as context, never as a link.

### To publish

1. Read the harm citation texts (Form 2567) on Care Compare for the four worst homes; look for resident-on-resident abuse citations, F600 to F610.
2. Missouri Case.net for neglect and wrongful-death suits; federal court holds mostly job suits.
3. Missouri Department of Mental Health: how patients with serious mental illness get placed in these homes.
4. Care Compare schizophrenia-coding audit flag for each Reliant home.
5. Right of reply to Reliant Care Management.

### The chart

Paired bars, x = staffing band, y = harm citations per 100 beds, Reliant vs other MO homes, home counts on each bar. Rows in `joins/j1_skeptic.md`.

### Sources

- https://oig.hhs.gov/compliance/corporate-integrity-agreements/browse-cias/reliant-care-group-llc/
- https://tallgrasseconomics.org/2024/11/reliant-health-care-management-llc-the-worst-nursing-home-chain-in-america/
- https://projects.propublica.org/nursing-homes/affiliate/a-446
- https://www.reliantcaremgmt.com/bridgewood-health-care-center

---

## 2. Texas hospice farms

**Dossier:** `joins/j5.md`, skeptic `joins/j5_skeptic.md`, raw lists `joins/j5/farms.json`, `nodes.json`. Related: LEADS #23, #24, #120, #128.
**Grade:** B after fixes. Cannot reach A without hospice payment data.

### The numbers, skeptic-corrected

A farm = one authorized official, one street address, 4+ differently named hospice organizations in NPPES.

| Area | Hospice IDs in a farm | All hospice IDs | Share |
|---|---|---|---|
| San Antonio | 31 | 282 | 11.0% |
| Houston city | 37 | 535 | 6.9% |
| Houston 35-city metro | | | 3.9% |
| California | 182 | 5,563 | 3.3% |
| Everywhere else | 61 | 11,472 | 0.53% |

Say "hospice IDs," never "hospices": San Antonio has 282 IDs but 134 certified hospices.

### The four Texas clusters

| Building | Pattern | Dates | Certified |
|---|---|---|---|
| 7322 Southwest Fwy, Houston, Suite 610 | Rooms A to F, six hospice IDs, two signers; 14 hospice IDs under three signers in the building since 2008 | IDs Oct 4-11, 2022 | 5 certified Apr 13 to Jun 8, 2023 |
| 2922 Rosedale St, Houston | one signer on 10 hospice IDs, plus a consulting company on the same phone | 2014 to 2022 | 8 |
| 8746 Wurzbach Rd Suite 201, San Antonio | 18 tree-named LLCs under two signers; 14 hospice IDs on one phone, (210) 729-6922 | Feb 10 to Jul 6, 2021 | 5 |
| 2819 NW Loop 410, San Antonio | numbered corporations CFHC NO4 to NO23, a different signer on each, each certified under a new brand | Sep 27 to Oct 15, 2021 | 12 of 14 |

- Farm IDs certify at the Texas rate or better: CFHC 86%, core signers 45%, rest of Texas 39%.
- Brand swaps: New Dawn Hospice Inc certified as Compassion Hospice of Texas; the CFHC corps certified as Ariel, Bexar Hospice, Harmony, Nightingale, Willow Tree, Arms of Compassion, Genisa, Texas Heroes, Alta Vita, All Faith.

### Validation against the public record, checked today

Texas Senate Health and Human Services committee, April 10, 2026, testimony by Lisa McNair of Hospice Brazos Valley, reported by The Texan:
- "15 hospices located in one building on the Northwest Loop 410 in San Antonio. Two were established in 2019, 13 were established in 2021."
  - The dossier's 2819 NW Loop 410 holds two 2019 hospice IDs, Community First Hospice Care of San Antonio 2019-08-30 and Yellow Rose Hospice Care 2019-09-03, plus the 2021 CFHC/HFCH/JP2D series. Testimony gave no street number, so the match is by road, year pattern and suite count.
  - The one-signer farm rule does **not** flag this building, because each CFHC corp has its own signer. The dossier caught it by the numbered-name series. That is a known blind spot of the rule.
- "At 9896 Bissonnet in Houston, there were six hospices ... all with the same owner."
  - `farms.json` flags 9896 Bissonnet St independently: one official, 4 hospice IDs.
- Check: grep of `joins/j5/farms.json`, `nodes.json`, `s02`, `s03`, `s05`, `s06`. Not re-queried.

### Already public

- ProPublica, 2022: for-profit hospices in four states sharing addresses and owners, licenses bought and sold.
- CMS, July 2023: enhanced oversight, pre-payment review, for new hospices in Arizona, California, Nevada and Texas.
- Texas hospice count nearly doubled, 688 to 1,366, January 2020 to March 2026; 308 newest co-located with 1 to 15 others. At least 7 Texas hospices had 100% live discharge; 25 more above 90%.
- Since April 15, 2026, CMS contractor Qlarant has suspended Medicare payments to Texas hospices with 90%+ live discharge over a 15-month lookback. National norm is about 19%.
- CMS Administrator Oz, April 28, 2026: fraud shifts to new states as enforcement tightens.
- DOJ Southern District of Texas: a $110M Houston hospice scheme, seven charged; a $150M scheme, CEO sentenced.
- Hospice News, June 3, 2026: "'Wild West' of hospice fraud intensifies in Texas."

### What's new

- A national base rate: 0.5% elsewhere vs 11% in San Antonio. The testimony gave counts, not a comparison.
- Clusters not named in anything found: Suite 610 Rooms A to F, the Wurzbach tree LLCs, the 2922 Rosedale signer, the CFHC brand swaps.
- The migration thread: LEADS #120 shows 83 new Arizona hospices with Los Angeles phone numbers, 43 registered in 2022 Q1. Texas farm IDs cluster in 2021-22. That fits Oz's shifting-fraud line, as a hypothesis.

### The other side, and the traps

- **No money.** No hospice claims, payments or live-discharge data in the warehouse. Nothing shows any of these IDs billed Medicare a dollar.
- The signer is who filed the ID application, not necessarily the owner. The 2922 Rosedale signer runs a consulting company on the same phone, which fits a licensing consultant.
- A formation shop selling ready-to-license corporations can be legal. Flipping a new hospice for its Medicare number is what CMS rules now target.
- 12 of 33 certified ties are exact name + same city + same street, not an ID.
- Private individuals, name-matched. Name addresses and corporate series, not people, until reported.

### To publish

1. Load CMS hospice spending by provider and the hospice quality file with live discharge; join on CCN to every farm ID. This is the one load that makes it an A.
2. Texas HHSC license search, and the HHSC agency closures list: it shows Treasured Moments Hospice LLC, 7322 Southwest Fwy Suite 645 Room C, closed 2026-07-20.
3. Texas Secretary of State officers and registered agents for CFHC NO4 to NO23, the tree LLCs, and the Suite 610 five.
4. PACER party search for the signers.
5. Right of reply to each company.

### The chart

Dot timeline, one lane per signer, each dot one hospice ID by issue date, filled if certified. Side panel: farm share by area, 11.0 / 6.9 / 3.3 / 0.5.

### Sources

- https://thetexan.news/issues/healthcare/texas-senators-hear-testimony-on-potential-fraud-in-state-s-health-welfare-programs/article_8aaa8b25-1cec-4301-bf93-18a987f8618a.html
- https://www.propublica.org/article/hospices-arizona-california-nevada-texas-cms-medicaid-medicare
- https://www.hchlawyers.com/blog/2026/may/texas-hospice-agencies-qlarant-audits-and-medica/
- https://www.morganlewis.com/pubs/2026/05/cms-trains-its-program-integrity-sights-on-texas-hospices
- https://hospicenews.com/2026/06/03/wild-west-of-hospice-fraud-intensifies-in-texas/
- https://www.justice.gov/usao-sdtx/pr/four-more-charged-110-million-hospice-fraud-scheme
- https://apps.hhs.texas.gov/providers/directories/Closures/hcssa_closures.pdf

---

## 3. Las Vegas Sands, Texas lobby "media"

**Dossier:** `joins/j6.md`, skeptic `joins/j6_skeptic.md`. Related: LEADS #18, #28.
**Grade:** A. Headline numbers reproduce to the cent.

### The numbers, skeptic-corrected

| Measure | Value |
|---|---|
| Sands media spend on Texas lobby reports, May 2021 to Jun 2026 | $20,575,810.66, 62 monthly reports, one filer, Andy Abboud |
| Every other Texas lobby filer, same months | $8,259,680.94 |
| Sands share | 70-71%; about 2.5 to 1 over everyone else combined |
| Spent in Jan-May of session years | $15,192,584, 74% |
| Spent Jan-Apr 2025 | $9,369,224: Jan $2.40M, Feb $2.79M, Mar $2.27M, Apr $1.91M, May $19.6K |
| Off-session months | flat $15.6K to $31K |
| Federal lobby fees, matched months | about $5.1M, so ads run about 4x the fees |
| Miriam Adelson to Truth and Courage PAC, 2024 | $2M, about 5% of its receipts; the PAC spent $21.95M against Colin Allred |

- Chart by the month money was **spent**, `PERIOD_START_DT`, not the report name. Each report covers the prior month.

### Already public

- Texas Tribune, April 2021: Sands spent $10M to $20M in recent months on ads, and hired a 51-member lobby team.
- 2025 session: 100+ lobbyists, "destination resort" ads that never said casino; died in the Senate, where Lt. Gov. Dan Patrick is the gatekeeper.
- Texas Sands PAC: over $9.3M cash for 2026; gave Republicans $2,646,000 and Democrats $1,245,500 the prior year.
- Abboud is Sands' senior vice president of government relations.

### What's new

- The five-year ledger total and the 70% share of all Texas lobby media. Not found in any coverage searched.
- The session-calendar shape, month by month.
- **The 2021 gap:** the press put 2021 ads at $10M to $20M by mid-April. The lobby ledger holds $1.5M for May-June 2021 and nothing earlier. The early money likely ran through the Texas Destination Resort Alliance PAC, registered with the IRS March 11, 2021. That's campaign finance, which the warehouse doesn't hold. Same campaign, two ledgers: a hypothesis to test.

### The traps

- It's Sands' own ad money, filed by its in-house executive. Never write "a lobbyist spent."
- "Media" isn't defined in the table. Get the Texas Ethics Commission rule.
- Subject and docket joins hit 0 of 62; that's normal for TEC, and it means no month can be tied to a bill from the data.
- Ads vs federal lobby fees is scale, not like for like.
- RAGA to Paxton and RSLC to Phelan are second hops through pooled funds at about 1%. No arrows.
- MAGA Inc.'s two $5M lines on 2026-09-04 may be one buy. Never sum them.

### To publish

1. Load the Texas Ethics Commission campaign-finance bulk files. Texas Sands PAC and the Alliance PAC live there.
2. Get TEC's lobby-report instructions for the media category.
3. Match the April 2025 spending stop to the joint resolution's last legislative action.
4. Right of reply to Sands.

### The chart

Quarterly columns, Sands vs a thin line for everyone else, session months shaded, election days marked. Rows in `joins/j6.md`.

### Sources

- https://www.texastribune.org/2021/04/14/las-vegas-sands-texas-gambling
- https://www.keranews.org/news/2021-04-18/las-vegas-sands-launches-multimillion-dollar-ad-campaign-to-push-for-casinos-in-texas
- https://www.texasmonthly.com/news-politics/texas-legislature-sands-casinos-gambling-bust/
- https://fortworthbusiness.com/business/las-vegas-sands-went-all-in-on-legalizing-casinos-in-texas-heres-why-the-multimillion-dollar-effort-did-not-make-it-far-this-session/
- https://casinobeats.com/2025/08/13/las-vegas-sands-2026-texas-casino-pac/
