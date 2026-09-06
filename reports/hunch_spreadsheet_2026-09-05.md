# Hunch spreadsheet, 2026-09-05

One row per hunch. A = appendix 1 in the matrix file, E = expansion report 32-75, bare numbers = matrix 1-31 and appendix 2 76-144. CSV beside this file.

| id | who | what | where_tables | when | why_it_matters | status |
|---|---|---|---|---|---|---|
| 1 | excluded doctors, hospices, SNF owners | excluded NPIs still listed at hospices whose owner also runs a SNF | LEIE, FACILITY_AFFILIATION, HOSPICE/SNF_ENROLLMENTS | affiliation snapshot 2026-07 | banned people still inside the Frank shape | tier 1, 4 NPIs at 8 hospices |
| 2 | PE nursing-home chains | fines per bed and repeat tags by chain | NH411, NH_DEFICIENCIES, NH_PENALTIES | deficiencies 2017-26, penalties 2023-06 on | which chains pay to keep failing | tier 1, Bria 5.4 fines/home |
| 3 | banks, EPA sites | lender LEI vs EPA sites | HMDA LEI xref, EPA corporate crosswalk | 2017 HMDA | finance-to-pollution edge | dead, finds banks' own sites; merged into 22 |
| 4 | opioid prescribers, drug makers | buprenorphine share vs maker payments | PART_D drug DY2022, OPEN_PAYMENTS 2022, OTP | one year | paid prescribers push the maker's drug | dead as written, OTP rows are orgs |
| 5 | disaster homeowners, lenders | rate spread and HOEPA flags after a declaration | FEMA IA, HMDA_HISTORIC | 2015-2017 | predatory lending follows disasters | tier 1, 47 disasters, 636 counties |
| 6 | dialysis chains, rural clinicians | chain-owned dialysis outcomes in HPSA areas | DIALYSIS, AFFILIATION, QPP, OPEN_PAYMENTS | one vintage | rural monopoly kills | tier 2 |
| 7 | FQHC doctors | excluded or opted-out doctors at FQHCs | UDS sites, OPT_OUT, LEIE | n/a | ghost clinics in deserts | dead, no org-to-person bridge |
| 8 | jails, counties | jail jumps then HPSA designation then poisoning deaths | VERA, HPSA, CDC poisoning | 2010-2024 | incarceration hollows out care | tier 2 |
| 9 | big emitters, county workers | GHGRP tonnage vs county wage vs injury | GHGRP, QCEW 2022, CDC injury | cross-section | polluters pay less, hurt more | tier 2 |
| 10 | DME referrers | referral volume vs supplier payments | DME by referrer | DY2024 | equipment kickback loop | tier 2, three column traps |
| 11 | losing hospitals, their doctors | negative net income vs pharma money to affiliated doctors | HCRIS FY2023, AFFILIATION, OPEN_PAYMENTS_2023 | 2023 | cost-report hypocrisy | tier 2 |
| 12 | LTCHs | margin vs ventilator beds vs device royalties | HCRIS, POS, AFFILIATION, OPEN_PAYMENTS | 2023 | ventilator churn | tier 2, 340 LTCHs |
| 13 | nursing homes | fire tags then reincorporation | NH_FIRE_DEFICIENCIES, SNF_ENROLLMENTS | 2016-2026 | shell game after fire tag | merged into 30 |
| 14 | rural health clinics | RHC at urban ZIPs | RHC_ENROLLMENTS, RUCA | snapshot | subsidy harvesters | dead as written, ZIP-only version lives |
| 15 | SAM-excluded contractors, FEMA | excluded firms holding FEMA contracts | SAM, USASPENDING contracts R2 | untimed | disaster grifters | tier 1, 26 UEIs $169M, needs dates |
| 16 | MDPP suppliers | MDPP NPIs on LEIE | MDPP, LEIE | snapshot | diabetes billing mills | parked, 0 of 1,037 |
| 17 | banks, polluters | FDIC LEI to EPA sites | FDIC_BANK_DATA, EPA crosswalk | n/a | polluter bank | dead, FDIC LEI 0% filled |
| 18 | surgeons with royalties | royalty income vs outpatient joint/spine volume | OPEN_PAYMENTS, outpatient by service | 2024 one year | hardware funnel | tier 2, $847M royalties |
| 19 | MIPS clinicians | bonus vs top-decile opioid rate | QPP PY2024, PART_D DY2024 | 2024 | quality bonus laundering | tier 2 |
| 20 | nursing-home and dialysis NPIs | NPIs at both | AFFILIATION | snapshot | nursing-to-dialysis churn | tier 2, 120 NPIs |
| 21 | hospital workers | HCRIS salaries vs county hospital wage | HCRIS, QCEW NAICS 622 | 2022 vs 2023 | wage starvation | tier 2 |
| 22 | redlined neighborhoods | TRI density by HOLC grade | TRI_FACILITY, MAPPING_INEQUALITY, CDC injury | current | redlined toxicity | tier 1, D over A 18x |
| 23 | debarred DME suppliers | excluded suppliers' share of DME dollars | LEIE, DME by supplier | ingested 2026-07 | catheter ring $1.425B | tier 1 |
| 24 | specialty model doctors | baseline for CY2027 model | ASM participants | 2027 start | extraction later | baseline only |
| 25 | FQHC sites in HPSA counties | terminated sites, still-enrolled orgs | POS_OTHER, FQHC_ENROLLMENTS, HPSA | since 2020 | FQHC evaporation | tier 2, 20 sites |
| 26 | storm counties, USDA housing | vacancy after $10M+ storm | NOAA_STORM_EVENTS, USDA MFH | 1996-2025, one MFH snapshot | storm housing arbitrage | tier 2 |
| 27 | pending Medicare applicants | excluded people applying | PENDING tables, LEIE, AFFILIATION | 2026-07 snapshot | pending workforce | tier 1, 9 NPIs |
| 28 | nursing homes | MDS acuity vs tags vs staffing | MDS Q2 2026, NH411, deficiencies | one quarter | assessment padding | tier 2 |
| 29 | hospitals in TRI counties | TRI vs net income vs terminations | TRI, HCRIS, POS | 2015-2024 | pollution hospital failure | tier 2, 2023 spike suspect |
| 30 | nursing-home owners | incorporated after first penalty | SNF_ENROLLMENTS, NH_PENALTIES | penalties 2023-06 on | PECOS shell carousel | tier 1, 39 homes |
| 31 | hospital-owned HHAs | stars, DTC, spend vs independents | HOSPITAL/HHA enrollments, HOME_HEALTH | snapshot | post-acute funnel | tier 1, 519 HHAs, mixed |
| A32 | excluded orgs, FEC donors | excluded names as contributors or treasurers | LEIE, SAM, FEC | untimed | banned providers fund campaigns | unprobed |
| A33 | PE nursing chains | chains that run a PAC | NH411, FEC committees | untimed | worst chains buy influence | unprobed |
| A34 | House districts | member spending vs TRI-by-HOLC | HOUSE_DISBURSEMENTS, TRI, HOLC | untimed | polluted districts starved | unprobed |
| A35 | House members | trades vs committee | HOUSE_FD_PTR_INDEX, committee membership | untimed | trading what you regulate | unprobed |
| A36 | DME and PE chains | industry money to CMS oversight committees | FEC, committee membership | untimed | funding your own overseer | unprobed |
| A37 | sanctioned persons | sanctions names in FEC | OFAC/UN/UK, FEC | untimed | sanctioned money in politics | unprobed |
| E32 | declared counties | drinking-water violations after floods | SDWA, FEMA declarations | 2015-2024 | floods break water | killed, OK+TX rule 220 |
| E33 | sewage plants | SNC after storms | NPDES QNCR, storms | quarterly | storms break sewage | live on wastewater permits only |
| E34 | counties | hazardous waste vs poisoning | RCRA, CDC poisoning | 2003-2015 | waste kills | killed r=0.007 |
| E35 | decriminalization states | jails down, overdoses up | VERA, CDC injury | 2019-2024 | policy backfire | lead, Washington 12/12 up |
| E36 | disaster counties | overdose after disasters | FEMA, CDC injury | 2019-2024 | disasters drive overdose | killed |
| E37 | paid prescribers | money jump vs Part D jump | OPEN_PAYMENTS, PART_D | PY2023-24 | industry buys volume | null, money is buyouts |
| E38 | opted-out doctors | still paid by industry | OPT_OUT, OPEN_PAYMENTS | PY2023 | opt-out is not exit | lead, $70.8M |
| E39 | NPs paid by opioid makers | opioid rate paid vs unpaid | OPEN_PAYMENTS, PART_D | two years | reps follow volume | lead, 45% vs 0% |
| E40 | new NPIs | skin-substitute billing by 2022+ NPIs | NPPES, PART_B | DY2024 | newborn NPIs bill millions | lead, $1.35B |
| E41 | excluded NPIs | still cleared to order | LEIE, ORDER_AND_REFERRING | snapshot | exclusion not enforced | lead, 7 NPIs |
| E42 | dead NPIs | industry pays deactivated NPIs | NPPES, OPEN_PAYMENTS | PY2024 | payments to nobody | lead, $4.19M |
| E43 | sold hospitals | negative income before sale | HCRIS, POS CHOW | FY2022-24 | bleeding then sold | lead, 60.5% |
| E44 | Bria and chains | G-tags rising then fined | NH deficiencies, penalties | 2023-2025 | hunch 2 with time | lead |
| E45 | nursing homes | E-tags after storms | NH deficiencies, storms | event windows | storms ignored | null |
| E46 | triple owners | SNF+HHA+hospice owners' stars | enrollments, NH411 | snapshot | integrated owners are better | reversed to composition |
| E47 | REH converters | negative before conversion | HCRIS, POS | last full year | rural hospitals convert broke | lead, 84% |
| E48 | terminated hospitals | negative income before termination | HCRIS, POS | 2024-26 | cost reports foreshadow closure | lead, 67.6% |
| E49 | excluded firms | awards inside exclusion window | SAM, USASPENDING | timed | hunch 15 timed | lead, $800k |
| E50 | post-disaster providers | provider startups after disasters | enrollments, FEMA | DiD | disaster startups | killed |
| E51 | HPSA counties | clinics after designation | HPSA, UDS sites | DiD | designation pulls clinics | undetermined |
| E52 | jail-heavy counties | wage, suicide, overdose by jail quintile | VERA, QCEW, CDC | one year wage | jails and violent death | weak |
| E53 | majority-minority tracts | SNC facilities unpenalized | ECHO, DIM_TRACT | snapshot | penalty deserts | reversed |
| E54 | air violators | factory wages | ICIS_AIR, QCEW | one year | violators pay less | killed, refineries |
| E55 | HUD housing | near noncompliant facilities | HUD, ECHO, SDWA | snapshot | subsidized beside pollution | killed |
| E56 | MIPS clinicians | bonus vs lunches | QPP, OPEN_PAYMENTS | PY2024 | bonus and money | null |
| E57 | top billers | top payees | PART_B, OPEN_PAYMENTS | DY2024 | billers get paid | lead, 2.0x |
| E58 | states | NPDB malpractice vs industry money | NPDB, QPP, OPEN_PAYMENTS | 2022-24 | state backdrop | killed, denominator |
| E59 | top-paid hospitals | pay vs stars | inpatient by provider, HOSPITAL_GENERAL | one year | paid badly rated | null |
| E60 | dialysis in bad-water counties | mortality vs SDWA | DIALYSIS, SDWA | yearly file landed | water kills patients | weak lead |
| E61 | hospitals as RCRA violators | violations vs income | RCRA, HCRIS | one year | waste and margins | weak |
| E62 | sprinkler-flag homes | flag yes, cited K0351 | NH data, deficiencies | snapshot | flag lies | weak |
| E63 | administrator churn | churn vs G-tags | NH411, deficiencies | 2024-25 | churn harms | weak lead |
| E64 | material-weakness grantees | money keeps flowing | FAC, USASPENDING assistance | capped table | audit ignored | weak, capped |
| E65 | revoked nonprofits | still funded | IRS revocations, assistance | dated | funded after revocation | refuted, reinstated |
| E66 | excluded entities | HHS grants | SAM, assistance | capped | excluded get grants | null floor |
| E67 | jail counties | clinician deserts | VERA, NPPES | snapshot | jails and deserts | killed |
| E68 | fat-margin nonprofits | charity under 1% | HCRIS | FY2023 | thin charity | lead, 37 hospitals |
| E69 | health centers | dollars per patient | UDS, assistance | 6 of 24 months | bridge found | money capped |
| E70 | VA-contracted homes | one-star share | USASPENDING, NH411 | snapshot | VA pays bad homes | null |
| E71 | counties | pharma dollars per head vs opioid share | OPEN_PAYMENTS, PART_D | one year | pharma per capita | weak |
| E72 | HUD housing | repeat-disaster counties | HUD, FEMA | snapshot | housing in harm's way | null, Puerto Rico |
| E73 | SAM clinicians | SAM adds clinicians | SAM, NPPES | snapshot | SAM leg | dead |
| E74 | HHA ownership change | no leg | POS_OTHER | n/a | HHA CHOW | dead, wish 5 |
| E75 | nursing chains | PRF money | PRF stub | n/a | relief funds to chains | dead |
| 76 | public nursing/hospital chain insiders | insider sales before fines | SEC insider trans, tickers, NH411 | 2025Q1+, check quarters | insiders knew | unprobed |
| 77 | federal judges | judge stock in defendants | CL investments, positions, FJC IDB civil | disclosure years | recusal failures | unprobed |
| 78 | senators | trades vs committee vote | SENATE_TRADES, committee membership, Voteview | 30-day windows | trading what you regulate | unprobed, cols unconfirmed |
| 79 | failed banks, auditors | auditor swap before failure | FDIC failed banks, SOD, PCAOB AP | 2017+ | auditor churn signal | unprobed |
| 80 | going-concern auditees | contracts after doubt | FAC, contracts R2 | after FY end | paid while dying | unprobed |
| 81 | pension sponsors | PBGC dump vs insider sales | PBGC, FORM5500_FULL, DERA, insider | termination year | execs cashed out | unprobed |
| 82 | union locals | shortage plus PAC | OLMS, FEC committees DIM | same fiscal year | missing money, active PAC | unprobed |
| 83 | health trade groups | lobby surge around CMS rules | LDA filings, Federal Register | comment windows | lobbying the fine | unprobed, cols unconfirmed |
| 84 | CMS oversight members | independent expenditures for/against | FEC IE, linkage, legislators, committees | by cycle | who buys the overseers | unprobed |
| 85 | device/pharma PACs | corporate PAC to leadership PAC | OPEN_PAYMENTS payers, FEC DIM, leadership PAC | by cycle | makers fund leaders | unprobed |
| 86 | Google political advertisers | ad spend with no FEC committee | POLADS, PAC_SUMMARY, MEDSL | by cycle | ad money FEC never saw | unprobed |
| 87 | FARA agents | donations inside registration window | FARA_BULK landing, FEC indiv | registration window | foreign agents giving | unprobed |
| 88 | 527 directors | same person as FEC treasurer | IRS527 directors, FEC DIM | untimed | dark money and PAC, one person | unprobed |
| 89 | state lobbyists | state dinners, federal checks | TX/CA lobby, FEC indiv | by year | two-level influence | unprobed |
| 90 | political appointees | agency awards tilt to prior sector | REVOLVINGDOOR, contracts R2 | no dates landed | revolving door in dollars | unprobed |
| 91 | members of Congress | trade then sponsor bill | SENATE_TRADES, bills, cosponsors | 90-day window | trades then bills | unprobed |
| 92 | House offices | allowance paid to donors | HOUSE_DISBURSEMENTS, FEC indiv | by quarter | office money to donors | unprobed |
| 93 | election jurisdictions | rejected ballots vs jail rate | EAVS, VERA, MEDSL | survey cycles | ballot rejection geography | unprobed, no codebook |
| 94 | judges | party and donations vs dispositions | CL affiliations, FEC, FJC IDB civil | by judge | politics on the bench | unprobed |
| 95 | judges | gifts and creditors as parties | CL gifts/debts/reimbursements, dockets | disclosure years | conflicts in disclosures | unprobed |
| 96 | NFIP opt-out communities | IA flood dollars there | NFIP status book, FEMA IA | per disaster | flood money, no insurance | unprobed |
| 97 | repeat-disaster ZIPs | destroyed 3+ times | FEMA IA, HUD, USDA MFH | 2015+ | rebuilt three times | unprobed |
| 98 | nursing homes below dams | high-hazard poor dams, no EAP | NID, NH, hospitals, HUD | last inspection | dam risk over the frail | unprobed |
| 99 | mine controllers | tailings dams plus unpaid penalties | MSHA mines/violations, NID | current | tailings and delinquency | unprobed |
| 100 | disaster vendors | first award right after declaration | contracts R2, FEMA IA | 60-day window | pop-up contractors | unprobed |
| 101 | flood counties | damage under old maps | NOAA storms, NFIP map dates | 2015+ | stale flood maps | unprobed |
| 102 | fossil counties | pipeline+orphan wells+fracking vs water | PHMSA, orphan wells, FracFocus, SDWA | current | three burdens one water | unprobed |
| 103 | spill reporters | spillers with contracts | NRC incidents, contracts R2, SAM | same years | spillers on the payroll | unprobed |
| 104 | aircraft LLC registrants | shared address, repeat fatal events | NTSB, FAA registry | by event | serial LLC fleets | unprobed |
| 105 | rail crossings | hit 5+ times | FRA crossings, casualties | 2010+ | never upgraded | unprobed, no inventory |
| 106 | pill-mill counties, pharmacies | ARCOS MME per capita then vs prescriber rate now | ARCOS, CDC poisoning, PART_D DY2024 | 2006-14 vs 2024 | then and now | unprobed, biggest table |
| 107 | opioid distributors, state AGs | distributor share vs settlement signers | ARCOS, NAAG settlements | 2006-14 vs settlement year | who signed, who got hit | unprobed |
| 108 | royalty surgeons | royalties on a recalled device | FDA recalls, 510k mart, OPEN_PAYMENTS, outpatient | around recall date | paid on a bad device | unprobed |
| 109 | device makers | death reports by clearance path | MAUDE mart, 510k mart | 2020+ | third-party review deaths | unprobed |
| 110 | generic drug spikes, prescribers | NADAC 3x jump vs Part D spend | NADAC landing, DailyMed, PART_D drug | effective dates | who rode the spike | unprobed |
| 111 | tribal areas | nearest hospital terminated | IHS facilities, POS | 2015+ | tribal access loss | unprobed |
| 112 | research institutions, SBIR firms | retractions per grant dollar | NIH, SBIR, Retraction Watch | by year | misconduct per dollar | unprobed, NIH capped |
| 113 | MDL products | still promoted with payments | JPML, OPEN_PAYMENTS, PART_D/B | after MDL date | litigated, still pushed | unprobed |
| 114 | establishments | injury rate up, no inspection | OSHA 300A 2023-25, inspections, QCEW | three years | injuries ignored | unprobed |
| 115 | mine controllers | unpaid penalties then accident | MSHA violations, accidents, mines | before/after | delinquent then deadly | unprobed |
| 116 | visa employers | wage floor plus willful OSHA | OFLC, OSHA inspections, SAM | by year | cheap labor, unsafe | unprobed |
| 117 | nursing-home operators | PPP forgiven, fines paid | PPP, SNF enrollments, penalties | 2020-21 vs fines | forgiven and fined | unprobed |
| 118 | SBA lenders | charge-offs vs enforcement | SBA loans, failed banks | by year | bad lenders | dead leg, FDIC enforcement 14 rows |
| 119 | ICE contractors, facilities | cost per detainee-day | ICE stints, facility codes, contracts R2 | by year | detention economics | unprobed, aggregate only |
| 120 | detainer counties | detainers per jail admission | ICE detainers, VERA | by year | enforcement geography | unprobed, thin mart |
| 121 | offshore officers | doctors and donors offshore | ICIJ officers, FEC, OPEN_PAYMENTS | untimed | offshore doctors | unprobed, cols unconfirmed |
| 122 | UK company controllers | sanctioned PSCs | UK PSC, OpenSanctions, OFAC | notified/ceased dates | sanctioned owners | unprobed |
| 123 | undisclosed parents | US lenders and polluters with REPEX parents | GLEIF REPEX, GLEIF, HMDA xref, EPA crosswalk | current | parents nobody names | unprobed |
| 124 | thin-charity hospitals | officer pay | IRS BMF, 990 index | n/a | fat officers | dead, 990 amounts not landed |
| 125 | 527 orgs | revoked, still filing | IRS527, revocations, 8872 | after revocation | revoked 527s | unprobed |
| 126 | mortgage lenders | complaints climb vs denial gap | CFPB complaints, HMDA xref | monthly | complaints foretell | unprobed, enforcement leg dead |
| 127 | HOLC D-zone branches | branch and deposit loss by grade | FDIC SOD, HOLC | survey years | branches leaving | unprobed |
| 128 | FHLB members | failed banks that were members | FHLB membership, failed banks | at failure | system kept lending | half dead, half live |
| 129 | vehicle make-models | complaints years before recall | NHTSA complaints, recalls | lag years | late recalls | unprobed |
| 130 | Section 8 properties | expiring in hot markets | HUD Section 8, FHFA HPI | 2026-28 | assisted units at risk | unprobed |
| 131 | FHA lenders | rates in D-zone ZIPs | FHA snapshot, HOLC, HMDA | one month | redlined FHA pricing | unprobed |
| 132 | disaster ZIPs | Ch 7 filings after declaration | FJC bankruptcy, FEMA IA | 12 months after | disasters bankrupt | unprobed |
| 133 | nursing chains | suits per bed vs fines | FJC civil, NH411, penalties | by year | sued and fined | unprobed |
| 134 | health-fraud defendants | convicted, not excluded | FJC criminal, LEIE | judgment to exclusion | exclusion lag | unprobed |
| 135 | ransomed hospitals | ratings after attack | ransomware victims, HOSPITAL_GENERAL, NH411 | attack date on | ransomware fallout | unprobed |
| 136 | exploited vendors | KEV count vs federal IT dollars | CISA KEV, contracts R2 | by year | paid to be hacked | unprobed |
| 137 | sanctioned vessels | AIS pings in US ports | OFAC SDN, NOAA AIS | after designation | sanctions busting | unprobed, AIS cols unconfirmed |
| 138 | police departments | killings vs federal grants | MPV, assistance | by year | grants to deadliest | unprobed, assistance capped |
| 139 | gun dealers | density vs firearm deaths | ATF FFL, NICS, CDC injury | state level | dealers and deaths | tier 2 |
| 140 | plant owners, funds, PACs | who owns the dirtiest plants | eGRID, EIA860 owner, 13F, PAC summary | 2022 | ownership of pollution | unprobed |
| 141 | utilities | worst outages, most storms, rates | EIA861 reliability, territory, storms, sales | by year | outages and rates | unprobed |
| 142 | power units | emission spikes, no violation | CAMPD daily, ICIS_AIR, AQS | daily | unpunished spikes | unprobed, cols unconfirmed |
| 143 | trial sponsors | paying own PIs | clinicaltrials stub | n/a | trial conflicts | dead, AACT not landed |
| 144 | immigration judges | outcomes by judge and facility | EOIR | n/a | court outcomes | dead, column unparsed |
