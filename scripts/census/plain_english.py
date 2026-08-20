"""Plain-English descriptions for every dataset and every date field.

WHO THIS IS FOR
---------------
Somebody who has never heard of any of these agencies. No acronyms left
unexplained, no "records" or "entities" or "instruments" -- what the thing IS,
who collects it, and what a date on it actually tells you.

TWO DICTIONARIES
----------------
TABLES  keyed by the source name (the part after the domain prefix): what the
        dataset is, in one sentence a stranger would understand.
FIELDS  keyed by column name: what that particular date marks.

Anything not in FIELDS falls through to `gloss()`, which turns a column name
into readable English by rule. That is deliberate: a column called
TERMINATION_DATE needs no hand-written note, while one called CYCLE does.

Accuracy rule followed throughout: where the dataset was not recognisable with
confidence, the description says what the name and the measured data support and
no more. Nothing here asserts a detail that was not either well known or visible
in the census.
"""
import re

# --------------------------------------------------------------------------
# WHAT EACH DATASET IS
# --------------------------------------------------------------------------

TABLES = {

# ---- Consumer complaints and product safety --------------------------------
"FED_CFPB_COMPLAINTS": "Complaints Americans filed against banks, credit card companies, debt collectors and mortgage servicers, to the federal consumer finance watchdog.",
"FED_CPSC_NEISS": "Emergency room visits caused by consumer products, sampled from a national panel of hospitals — the government's injury early-warning system.",
"FED_NHTSA_COMPLAINTS": "Complaints drivers filed with federal auto safety regulators about faults in their vehicles.",
"FED_NHTSA_RECALLS": "Every vehicle and car-part recall announced in the United States.",
"FED_NHTSA_INVESTIGATIONS": "Federal investigations into suspected vehicle defects — the step that sometimes leads to a recall.",

# ---- Company registries and offshore ---------------------------------------
"UK_COMPANIES_HOUSE_PSC": "The real human owners behind UK companies — who ultimately controls each one, as declared to the British companies register.",
"INTL_UK_COMPANIES_HOUSE": "Every company registered in the United Kingdom.",
"FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS": "Who is connected to whom in the leaked offshore files — the links between shell companies, their owners and the middlemen who set them up.",
"FED_IRS_EO_BMF": "Every organisation the US tax authority recognises as tax-exempt — charities, churches, foundations, trade groups.",
"INTL_IE_CRO": "Every company registered in Ireland.",
"FED_ICIJ_OFFSHORELEAKS_ENTITIES": "Shell companies and trusts named in the leaked offshore files — Panama Papers, Paradise Papers and the rest.",
"FED_ICIJ_OFFSHORELEAKS_OTHERS": "Other parties named in the leaked offshore files who don't fit the company or officer categories.",
"INTL_ES_BORME": "Spain's official companies gazette — legal notices of company formation and change. Nearly empty in this warehouse.",

# ---- Crime statistics -------------------------------------------------------
"FED_BJS_DATA": "A small sample from the federal statistics office that tracks crime, courts and prisons.",

# ---- Federal money in and out ----------------------------------------------
"FED_USASPENDING_CONTRACTS_FULL": "Every contract the US federal government signed — who got paid, how much, for what. The complete ledger.",
"FED_USASPENDING_ASSISTANCE_FULL": "Every federal grant, loan and aid payment — money the government gave out rather than bought with.",
"FED_USASPENDING_CONTRACTS": "Federal contract transactions, a second and smaller cut of the government's purchasing ledger.",
"FED_IRS_990_EFILE_INDEX": "An index of every annual tax return filed electronically by a US charity or nonprofit.",
"FED_BLS_QCEW": "Employment and wages by industry and county, counted from the payroll tax records nearly every US employer files.",
"FED_SBA_LOANS": "Small business loans backed by the federal government — who borrowed, how much, and whether it was paid back.",
"FED_IRS_BMF": "The tax authority's master list of registered businesses and organisations.",
"FED_IRS_AUTO_REVOCATIONS": "Charities that automatically lost their tax-exempt status for failing to file for three years running.",
"FED_IRS_REVOCATION": "Organisations whose tax-exempt status was revoked.",
"FED_SBA_PPP": "Pandemic relief loans to businesses — the Paycheck Protection Program, including who had the loan forgiven.",
"INTL_GLEIF_RELATIONSHIPS": "Which companies own which other companies, from the global registry of legal entity identifiers.",
"FED_TREASURY_DTS_DEPOSITS": "Money flowing into the US Treasury each day — the government's daily bank statement, deposits side.",
"FED_FAC_SINGLE_AUDIT": "Audits of organisations that spend federal grant money, including what the auditors found wrong.",
"INTL_FAO_FAOSTAT_FOOD_SECURITY": "United Nations statistics on hunger, food supply and undernourishment by country.",
"INTL_IT_ISTAT": "Official statistics published by Italy's national statistics agency.",
"FED_PBGC_DATA": "Figures from the federal agency that takes over company pension plans when the company can no longer pay them.",
"FED_FOREIGNASSISTANCE": "US foreign aid — which countries and programmes received American government money.",
"FED_US_SEC_EDGAR": "Filings companies are legally required to submit to the US securities regulator.",
"FED_DOL_FORM5500": "Annual reports from company retirement and health benefit plans — how big the plan is and who runs it.",
"FED_TREASURY_DEBT_TO_PENNY": "The exact size of the US national debt, published daily.",
"FED_TREASURY_MTS_RECEIPTS": "What the US government collected in taxes and fees each month.",
"FED_TREASURY_AVG_INTEREST_RATES": "The average interest rate the US government pays on its debt.",
"FED_FDIC_FAILED_BANKS": "Every US bank that has failed, and the date it was shut down.",
"FED_IRS_EO_PR": "Tax-exempt organisations registered in Puerto Rico.",
"FED_IRS_SOI_CHARITIES": "Financial summaries of charities, compiled by the tax authority's statistics division.",
"XC_OWID_GINI": "How unequally income is distributed in each country, tracked over time.",
"FED_US_USASPENDING_API": "A small sample of federal spending records pulled through an automated feed.",
"FED_TREASURY_DEBT_OUTSTANDING": "The total US national debt, reported at set points in time.",
"FED_IRS_990": "A small sample of charity tax returns.",
"FED_SEC_EDGAR": "A small sample of company filings to the US securities regulator.",
"FED_GRANTS_GOV": "A small sample of federal grant opportunities.",
"INTL_FAO_FAOSTAT": "A small sample of United Nations agriculture and food statistics.",

# ---- Political advertising and futures (filed under Education, wrongly) -----
"FED_GOOGLE_POLADS_CREATIVE_STATS": "Every political advert run on Google and YouTube — who paid, who saw it, and how much it cost.",
"FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND": "Weekly spending by each political advertiser on Google and YouTube.",
"FED_CFTC_COT_FUTURES": "Who holds bets on commodity prices — the weekly breakdown of futures positions by trader type.",
"FED_SENATE_LDA_FILINGS": "Lobbying disclosures filed with the US Senate — who is being paid to influence which issues.",
"FED_CFTC_COT_FINANCIAL": "Who holds bets on financial futures — the weekly breakdown by trader type.",

# ---- Energy -----------------------------------------------------------------
"INTL_EMBER_ELEC": "How each country generates its electricity, and how that mix has shifted, from an independent energy think tank.",
"FED_EIA860_3_1_GENERATOR": "Every electricity generating unit in the US — what fuel it burns, how big it is, and when it came online.",
"FED_EIA861_SERVICE_TERRITORY": "Which electric utility serves which counties.",
"FED_EIA860_3_3_SOLAR": "Every solar generating unit in the US and its technical details.",
"FED_EIA860_6_2_ENVIROEQUIP": "Pollution control equipment fitted to US power plants.",
"FED_EIA861_FRAME": "The master list of electric utilities that report to the federal energy agency.",
"FED_EIA860_3_5_MULTIFUEL": "Power plant units that can switch between fuels.",
"FED_EIA861_SALES_ULT_CUST": "How much electricity each utility sold, to whom, and for how much.",
"FED_EIA861_ADVANCED_METERS": "Smart meter rollout by utility.",
"FED_EIA861_SHORT_FORM": "The simplified annual return filed by smaller electric utilities.",
"FED_EIA861_OPERATIONAL_DATA": "Operating figures reported annually by electric utilities.",
"FED_EIA861_UTILITY_DATA": "Basic details of each electric utility that reports to the federal energy agency.",
"FED_EIA860_3_2_WIND": "Every wind generating unit in the US and its technical details.",
"FED_EIA861_DISTRIBUTION_SYSTEMS": "The physical distribution networks utilities operate — circuits, substations and their condition.",
"FED_EIA861_NET_METERING": "Customers who generate their own power and sell the surplus back to the grid.",
"FED_EIA861_RELIABILITY": "How often and how long each utility's customers lose power.",
"FED_EIA861_DYNAMIC_PRICING": "Utilities that charge different electricity prices at different times of day.",
"FED_EIA860_3_4_ENERGY_STORAGE": "Battery and other storage units attached to the US grid.",
"FED_EIA861_SALES_ULT_CUST_CS": "Electricity sales to customers, reported by a subset of utilities.",
"FED_EIA861_NON_NET_METERING_DISTRIBUTED": "Small-scale generation that is not on a net metering arrangement.",
"FED_EIA861_ENERGY_EFFICIENCY": "Utility energy-saving programmes and what they achieved.",
"FED_EIA861_DEMAND_RESPONSE": "Programmes that pay customers to cut electricity use at peak times.",
"FED_EIA861_DELIVERY_COMPANIES": "Companies that deliver electricity without selling it.",
"FED_EIA861_MERGERS": "Mergers and acquisitions among electric utilities.",
}

TABLES.update({

# ---- Pollution, water, land -------------------------------------------------
"FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT": "Every time a public drinking water system broke a safety rule, and what the regulator did about it.",
"FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS": "How much of each pollutant every reporting facility released into the air.",
"FED_EPA_NPDES_NPDES_QNCR_HISTORY": "Quarterly records of facilities in serious breach of their water pollution permits.",
"FED_USGS_WATER": "Readings from the national network of river and groundwater monitoring stations.",
"FED_EPA_ECHO": "The environmental regulator's compliance file — inspections, violations and penalties, facility by facility.",
"FED_EPA_RCRA_VIOSNC_HISTORY": "Hazardous waste handlers found in significant non-compliance, tracked over time.",
"FED_EPA_SDWA_SDWA_SITE_VISITS": "Visits inspectors made to public drinking water systems.",
"FED_EPA_NPDES_NPDES_INSPECTIONS": "Inspections of facilities that discharge pollution into water.",
"FED_NOAA_STORM_EVENTS": "Every recorded storm, flood, tornado and severe weather event in the US, including deaths and damage.",
"FED_EPA_SDWA_SDWA_FACILITIES": "The physical parts of public drinking water systems — wells, treatment plants, storage tanks.",
"FED_EPA_RCRA_EVALUATIONS": "Inspections and evaluations of hazardous waste handlers.",
"FED_USCG_NRC_INCIDENTS": "Reports to the national hotline for oil spills and chemical releases.",
"FED_EPA_SDWA_SDWA_LCR_SAMPLES": "Lead and copper test results from public drinking water systems.",
"FED_EPA_RCRA_VIOLATIONS": "Hazardous waste rules that facilities were found to have broken.",
"FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS": "Tests measuring what actually comes out of industrial smokestacks.",
"FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS": "Which places each public drinking water system serves.",
"FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS": "Annual statements from major air polluters certifying whether they complied with their permits.",
"FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS": "Warning letters and informal actions against water polluters — the step before formal enforcement.",
"FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS": "Which air pollution programmes each facility falls under.",
"FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS": "Every public drinking water system in the US and how many people it serves.",
"FED_EPA_NPDES_NPDES_PS_VIOLATIONS": "Water pollution permit breaches involving prohibited discharges and schedules.",
"FED_EPA_SDWA_SDWA_EVENTS_MILESTONES": "Milestones in getting a failing drinking water system back into compliance.",
"FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC": "Cases where a water system failed to tell the public about a problem.",
"FED_EPA_RCRA_ENFORCEMENTS": "Formal enforcement actions against hazardous waste handlers, including penalties.",
"FED_EPA_GHGRP_EMISSION": "Greenhouse gas emissions reported by large industrial facilities.",
"FED_EPA_NPDES_NPDES_SE_VIOLATIONS": "Water pollution breaches picked up from single-event reporting.",
"FED_USGS_MINERALS": "Production and consumption figures for mined minerals.",
"FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS": "Warning letters and informal actions against air polluters.",
"FED_EPA_GHGRP_FACILITY": "The large industrial facilities required to report their greenhouse gas emissions.",
"FED_USGS_ORPHANED_OIL_GAS_WELLS": "Abandoned oil and gas wells with no owner left to plug them.",
"FED_USCG_NRC_INCIDENT_REPORTS": "The detailed write-ups behind oil spill and chemical release reports.",
"FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS": "Formal legal actions against water polluters, including fines.",
"FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS": "Formal legal actions against air polluters, including fines.",
"EPA_PENALTY_GAP": "A Ripple-built comparison of penalties assessed against penalties actually collected.",
"FED_NID_DAMS": "Every significant dam in the US — how big, who owns it, and what happens if it fails.",
"FED_EPA_NPDES_NPDES_CS_VIOLATIONS": "Water polluters who missed deadlines in a compliance schedule.",
"FED_EPA_TRI_BASIC_2023": "Toxic chemicals released by industrial facilities in 2023, as self-reported.",
"XC_OWID_CO2": "Carbon dioxide emissions by country, going back to the 1750s.",
"FED_EPA_AQS_SITES": "The physical air quality monitoring stations across the US.",
"FED_EPA_EGRID_PLANT_2022": "Emissions and generation for every US power plant in 2022.",
"XC_OWID_FOSSIL_SHARE": "What share of each country's energy comes from fossil fuels.",
"FED_WQP_MONITORING_STATIONS": "Water quality monitoring stations run by federal, state and local bodies.",
"FED_EPA_SUPERFUND_SITE_BOUNDARIES": "The mapped boundaries of America's most contaminated cleanup sites.",
"FED_PHMSA_FLAGGED_INCIDENTS": "Pipeline incidents flagged by federal pipeline safety regulators.",
"XC_OWID_TEMP_ANOMALY": "How far global temperature has drifted from its historical average.",
"FED_NOAA_WEATHER_API": "A small sample of weather readings pulled from an automated feed.",
"INTL_GLOBAL_WITNESS_DEFENDERS": "Environmental and land defenders killed around the world, documented by an investigative NGO.",

# ---- Money, markets, banking ------------------------------------------------
"FED_FEC_INDIV_CONTRIBUTIONS": "Every reported donation an individual made to a federal political campaign — donor name, employer, amount and date.",
"FED_FDIC_SOD_BRANCH_DEPOSITS": "How much money is held at every single bank branch in America, year by year.",
"FED_SEC_INSIDER_NONDERIV_TRANS": "Company executives and directors buying and selling their own company's shares.",
"FED_SEC_INSIDER_SUBMISSION": "The filings themselves in which insiders disclose their share dealings.",
"FED_SEC_INSIDER_DERIV_TRANS": "Executives' dealings in share options and other derivatives of their own company's stock.",
"FED_FEC_COMMITTEE_TO_CANDIDATE": "Money moving from political committees to candidates.",
"FED_SEC_13F_FILERS": "Large investment managers required to disclose what they hold.",
"FED_SEC_13F_SUBMISSIONS": "The quarterly filings in which big investors reveal their holdings.",
"FED_FEC_INDEPENDENT_EXPENDITURES": "Money spent for or against a candidate by groups not coordinating with them — the core of super PAC spending.",
"FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS": "Federal environmental inspections logged in the enforcement case system.",
"FED_IRS_SOI": "Income and tax statistics compiled by the tax authority.",
"FED_PCAOB_FORM_AP_FILINGS": "Which audit partner signed off on which public company's accounts.",
"FED_SEC_EDGAR_INSIDERS": "Insider share dealing filings, a second cut of the same disclosures.",
"FED_SEC_EDGAR_FINANCIALS": "Financial statement figures pulled from company filings.",
"FED_FEC_CANDIDATES": "Everyone who has run for federal office in the US.",
"FED_FEC_CAND_CMTE_LINKAGE": "Which campaign committee belongs to which candidate.",
"FED_FDIC_BANK_DATA": "Every US bank — where it is, how big, and whether it is still open.",
"FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS": "Informal environmental enforcement actions logged in the case system.",
"FED_FEC_BULK_COMMITTEES": "The master list of federal political committees.",
"FED_FEC_LEADERSHIP_PAC": "Leadership PACs — the side funds politicians run to give money to other politicians.",
"FED_SEC_DERA_SUB_2024Q2": "Company financial filings submitted in spring 2024.",
"FED_SEC_DERA_SUB_2025Q2": "Company financial filings submitted in spring 2025.",
"FED_SEC_DERA_SUB_2024Q3": "Company financial filings submitted in summer 2024.",
"FED_SEC_DERA_SUB_2025Q3": "Company financial filings submitted in summer 2025.",
"FED_SEC_DERA_SUB_2024Q4": "Company financial filings submitted in autumn 2024.",
"FED_FHFA_FHLB_MEMBERSHIP": "Banks and insurers that belong to the Federal Home Loan Bank system.",
"FED_SEC_DERA_SUB_2025Q4": "Company financial filings submitted in autumn 2025.",
"FED_SEC_DERA_SUB_2025Q1": "Company financial filings submitted in winter 2025.",
"FED_SEC_DERA_SUB_2026Q1": "Company financial filings submitted in winter 2026.",
"FED_SEC_DERA_SUB_2024Q1": "Company financial filings submitted in winter 2024.",
"FED_NCUA_CALL_REPORTS_FOICU": "Basic details of every federally insured credit union.",
"FED_NCUA_CALL_REPORTS_FS220": "The financial accounts every credit union files with its regulator.",
"INTL_ISO_MIC_REGISTRY": "The official codes identifying stock exchanges and trading venues worldwide.",
"FED_SEC_MONEY_MARKET_FUND_INFORMATION": "Money market funds and what they hold.",

# ---- Foreign influence ------------------------------------------------------
"FED_FARA_BULK": "People and firms paid to represent foreign governments and interests inside the United States, as they are legally required to declare.",
})

TABLES.update({

# ---- Drugs, devices, doctors, care homes ------------------------------------
"FED_DEA_ARCOS": "Every shipment of prescription opioids in America from 2006 to 2012 - manufacturer to distributor to pharmacy, pill by pill. The dataset behind the opioid litigation.",
"FED_FDA_FAERS_DRUG": "The drugs named in reports of suspected side effects sent to US medicines regulators.",
"FED_FDA_FAERS_REAC": "What actually happened to patients in those side effect reports - the reactions themselves.",
"FED_CMS_OPEN_PAYMENTS": "Payments and gifts from drug and device companies to individual doctors and teaching hospitals.",
"FED_CMS_OPEN_PAYMENTS_2023": "Drug and device company payments to doctors in 2023.",
"FED_CMS_OPEN_PAYMENTS_2022": "Drug and device company payments to doctors in 2022.",
"FED_CMS_MEDICARE_DIALYSIS_FACILITIES": "Dialysis clinics and their reported quality and outcome measures.",
"FED_FDA_FAERS_INDI": "What each drug was being taken for in reports of suspected side effects.",
"FED_FDA_FAERS_DEMO": "Who the patient was in each suspected side effect report - age, sex, weight, outcome.",
"FED_FDA_GUDID": "Every medical device sold in the US and its identifying details.",
"FED_FDA_MAUDE": "Reports of medical devices injuring or killing patients, or malfunctioning.",
"FED_CDC_NNDSS_WEEKLY_2024": "Weekly counts of notifiable diseases reported by states in 2024.",
"FED_HRSA_NPDB": "The national database of malpractice payouts and disciplinary actions against health practitioners.",
"FED_FDA_FAERS_OUTC": "How each suspected side effect case ended - recovery, hospitalisation, death.",
"FED_CMS_NURSING_HOME_DEFICIENCIES": "Every problem inspectors found in a US nursing home, and how serious they judged it.",
"FED_CMS_NADAC": "What pharmacies actually pay to buy each drug - the government's national average.",
"FED_FDA_ESTABLISHMENT_REG": "Factories and facilities registered to make or handle medical products.",
"FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES": "Fire safety failures found during nursing home inspections.",
"FED_FDA_DEVICE_510K": "Medical devices cleared for sale on the grounds that they resemble something already on the market.",
"FED_HRSA_SHORTAGE_AREAS": "Places officially designated as short of medical care.",
"FED_NLM_DAILYMED_SPL_SETID_MAP": "The mapping between drug products and their official labelling documents.",
"FED_CDC_INJURY_VIOLENCE_COUNTY": "Injury and violence death rates by US county.",
"FED_FDA_CAERS": "Reports of people harmed by food, dietary supplements and cosmetics.",
"FED_CDC_OVERDOSE": "Drug overdose death counts.",
"FED_HHS_OIG_LEIE": "People and companies banned from billing Medicare and Medicaid - the healthcare exclusion list.",
"FED_HRSA_HPSA_PRIMARY_CARE": "Areas designated as short of primary care doctors.",
"FED_CMS_OPT_OUT_AFFIDAVITS": "Doctors who have formally opted out of Medicare entirely.",
"FED_FDA_DEVICE_PMA": "Medical devices that went through the full pre-market approval process, and every later change to them.",
"FED_CDC_DRUG_POISONING_COUNTY": "Drug poisoning death rates by US county.",
"FED_CMS_POS_OTHER": "Healthcare facilities certified to treat Medicare patients, and when they were certified.",
"FED_FDA_DRUG_MASTER_FILES": "Confidential files drug makers lodge with regulators about ingredients and processes.",
"FED_FDA_DEVICE_ENFORCEMENT": "Medical device recalls and enforcement actions.",
"XC_OWID_LIFE_EXPECTANCY": "Life expectancy by country over time.",
"FED_HRSA_UDS_SERVICE_DELIVERY_SITES": "The individual clinic locations run by federally funded community health centres.",
"FED_FDA_DRUG_ENFORCEMENT": "Drug recalls and enforcement actions.",
"FED_CDC_ANXIETY_DEPRESSION": "Survey estimates of anxiety and depression across the US population.",
"FED_CMS_NURSING_HOME_PENALTIES": "Fines and payment suspensions imposed on nursing homes.",
"FED_CDC_HEALTH_INSURANCE": "Survey estimates of how many people have health insurance.",
"FED_NURSINGHOME411": "Nursing home ownership and quality information compiled by an advocacy group.",
"FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS": "Which companies own and control each skilled nursing facility.",
"INTL_HEALTHCANADA_DPD_DRUG": "Every drug approved for sale in Canada.",
"FED_CMS_HOME_HEALTH": "Home health agencies and their reported quality measures.",
"FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS": "Which companies own and control each home health agency.",
"FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS": "Ownership of federally qualified health centres.",
"FED_CDC_LEADING_CAUSES_STATE": "The leading causes of death in each US state.",
"FED_CMS_HOSPITAL_ENROLLMENTS": "Which companies own and control each hospital.",
"FED_CMS_DIALYSIS": "Dialysis facilities and their details.",
"FED_CMS_HOSPICE": "Hospice providers and their details.",
"FED_CDC_SUICIDE_RATES": "Suicide rates broken down by group and place.",
"FED_CMS_HCRIS": "The detailed financial accounts hospitals file with Medicare.",
"FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS": "Ownership of rural health clinics.",
"FED_VA_ALLCAUSE_MORTALITY": "Death rates among US veterans.",
"PHARMA_MEAL_CAP_FINGERPRINT": "A Ripple-built check on drug company payments clustering suspiciously at reporting thresholds.",
"FED_FDA_PURPLE_BOOK": "Biologic medicines licensed in the US, including biosimilars.",
"XC_GUTTMACHER_MONTHLY_ABORTION": "Monthly abortion counts by state, from a reproductive health research institute.",
"FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS": "Clinics licensed to provide opioid addiction treatment.",
"FED_CDC_DATA_PORTAL": "The catalogue of datasets the US public health agency publishes.",
"FED_HRSA_UDS_HEALTH_CENTER_INFO": "Federally funded community health centres and who they serve.",
"FED_CMS_IRF": "Inpatient rehabilitation facilities and their details.",
"FED_VA_SUICIDE_STATE": "Veteran suicide figures by state.",
"ST_OEHHA_PROPOSITION_65_LIST": "Chemicals California officially lists as causing cancer or reproductive harm.",
"FED_CDC_WONDER": "Death and health statistics from the national public health query system.",
"FED_VA_SUICIDE_NATIONAL": "National veteran suicide figures.",
"FED_CLINICALTRIALS": "A sample of registered clinical trials.",
"FED_CMS_LTCH": "Long-term care hospitals and their details.",

# ---- History ----------------------------------------------------------------
"FED_SLAVEVOYAGES_INTRAAMERICAN": "Documented slave voyages within the Americas - ship, route, and the people carried.",
"FED_WPA_SLAVE_NARRATIVES": "First-person accounts recorded from formerly enslaved Americans in the 1930s.",

# ---- Housing and mortgages --------------------------------------------------
"FED_CFPB_HMDA_HISTORIC": "Every US mortgage application on record - who applied, for how much, and whether they were turned down. The core dataset for lending discrimination.",
"FED_FEMA_IA_HOUSING_REGISTRATIONS": "Households that applied for federal disaster housing assistance.",
"FED_FHFA_HPI": "House price indexes tracking how property values move.",
"FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT": "Government-insured single family mortgages currently outstanding.",
"FED_CFPB_HMDA": "Recent mortgage application records.",
"FED_CFPB_HMDA_DC_ONLY": "Mortgage application records for Washington DC.",
"FED_HUD_MF_FIRM_COMMITMENTS": "Government commitments to insure apartment building mortgages.",
"FED_HUD_MF_SECTION8_CONTRACTS": "Subsidised housing contracts - which buildings, how many units, and for how long.",
"FED_CFPB_HMDA_LAR": "Loan-level mortgage application records.",
"FED_FHFA_NMDB": "A statistical sample of US mortgages tracked over their lifetime.",
"FED_HUD_DATA": "A small sample from the federal housing department.",

# ---- Immigration and detention ----------------------------------------------
"FED_ICE_DETENTION_STINTS": "Individual stays in US immigration detention - when someone entered, where they were held, and when they left.",
"FED_DOL_OFLC": "Employer applications to hire foreign workers, including what wage they offered.",
"FED_ICE_DETAINERS": "Requests immigration enforcement sent to jails asking them to hold someone.",
"FED_EPA_SDWA_SDWA_SERVICE_AREAS": "The areas each public drinking water system covers. Filed under immigration by mistake.",
"FED_DHS_OHSS": "Immigration enforcement and benefits statistics from homeland security.",
"XC_OWID_REFUGEES": "Refugee numbers by country of origin and destination.",
"FED_CMS_HOSPICE_ENROLLMENTS": "Ownership of hospice providers. Filed under immigration by mistake.",
"FED_DHS_YEARBOOK": "Headline immigration statistics from the annual homeland security yearbook.",

# ---- Investigations ---------------------------------------------------------
"INTL_LEIDEN_RUSSIAN_OPS_EUROPE": "Documented Russian covert operations in Europe, compiled by academic researchers.",
"FED_OYEZ": "A small sample of Supreme Court case material.",
})

TABLES.update({

# ---- Courts, police, sanctions, crime ---------------------------------------
"FED_COURTLISTENER_DOCKETS": "Every federal court case file - who sued whom, in which court, and when.",
"FED_FJC_IDB_CIVIL": "Every civil lawsuit filed in US federal court, with how it was resolved.",
"FED_COURTLISTENER_FJC_IDB_CL_LINKED": "Federal court cases matched between two separate court record systems.",
"FED_COURTLISTENER_OPINION_CLUSTERS": "Written court rulings - the opinions judges actually publish.",
"FED_FJC_IDB_BANKRUPTCY": "Every bankruptcy filed in US federal court.",
"FED_FJC_IDB_CRIMINAL": "Every federal criminal defendant - the charge, the outcome, and the sentence.",
"FED_COURTLISTENER_INVESTMENTS": "Individual investments federal judges disclosed owning.",
"INTL_OPENSANCTIONS_DEFAULT": "People and companies under sanctions, on watchlists, or flagged as politically exposed, worldwide.",
"FED_FJC_IDB_APPELLATE": "Appeals filed in US federal appeals courts.",
"FED_COURTLISTENER_ORIGINATING_COURT_INFO": "Which lower court an appealed case came from.",
"INTL_UCDP_GED": "Every recorded event of organised violence worldwide - where, when, and how many died.",
"FED_FBI_CDE": "Crime figures reported by US police departments to the FBI.",
"RACIAL_JAIL_DISPARITY": "A Ripple-built measure of racial disparity in county jail populations.",
"XC_VERA_INCARCERATION_TRENDS": "Jail and prison populations by US county over decades, from a justice research institute.",
"FED_SCDB": "Every US Supreme Court decision, coded by issue, vote and outcome.",
"INTL_OPENSANCTIONS": "A second cut of the global sanctions and watchlist data.",
"FED_COURTLISTENER_FINANCIAL_DISCLOSURES": "The annual financial disclosures federal judges are required to file.",
"FED_COURTLISTENER_POSITIONS": "Every job a federal judge has held, including their time on the bench.",
"INTL_EU_SANCTIONS": "People and entities sanctioned by the European Union.",
"XC_UK_SANCTIONS_LIST": "People and entities sanctioned by the United Kingdom.",
"STATE_MO_SEX_OFFENDER_REGISTRY": "Missouri's public sex offender registry.",
"FED_CONSOLIDATED_SCREENING_LIST": "The combined US list of parties barred from trade and export dealings.",
"FED_FBI_NICS_CHECKS": "Monthly counts of background checks run for gun purchases.",
"FED_COURTLISTENER_JUDGES": "Every federal and state judge on record.",
"XC_MAPPING_POLICE_VIOLENCE": "People killed by US police, documented by an independent project.",
"FED_COURTLISTENER_JUDGE_EDUCATIONS": "Where each judge went to school.",
"XC_OWID_TERRORISM_DEATHS": "Deaths from terrorism by country over time.",
"XC_WAPO_FATAL_FORCE": "People shot and killed by US police, documented by the Washington Post.",
"FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS": "The political party each judge was affiliated with.",
"XC_OWID_HOMICIDE": "Homicide rates by country over time.",
"FED_COURTLISTENER_COURTS": "Every court in the United States.",
"COUNTY_DOUBLE_BURDEN": "A Ripple-built measure of counties carrying more than one kind of harm at once.",
"FED_CISA_KEV": "Software security holes that are known to be actively exploited by attackers.",
"FED_FTC_DATASETS": "A small set of consumer protection enforcement records.",
"XC_OWID_NUCLEAR_WARHEADS": "Nuclear warhead counts by country over time.",
"XC_NAGIX_DPRK_MISSILE_TESTS": "North Korean missile tests, from an independent tracker.",
"INTL_NTI_CNS_DPRK_MISSILE_TESTS": "North Korean missile tests, from a nuclear security institute.",
"FED_FHFA_SUSPENDED_COUNTERPARTIES": "Firms and individuals barred from doing business with US mortgage agencies.",
"INTL_EURLEX_CELLAR": "A small sample of European Union legal documents.",
"INTL_EU_SOCTA_EUROPOL": "A small set of European organised crime threat assessments.",
"FED_DOJ_FCA_SETTLEMENTS": "A small set of settlements where companies were accused of defrauding the government.",

# ---- Work, mines, pensions --------------------------------------------------
"FED_MSHA_VIOLATIONS": "Every safety violation a federal inspector wrote up at a US mine, and the fine that followed.",
"FED_OSHA_ITA_CASE_DETAIL_2023": "Individual workplace injuries and illnesses employers logged in 2023.",
"FED_OSHA_ITA_CASE_DETAIL_2024": "Individual workplace injuries and illnesses employers logged in 2024.",
"FED_DOL_OLMS": "The annual financial reports US labour unions must file - income, spending, membership and officer pay.",
"FED_OSHA_ITA_300A_SUMMARY_2024": "Each workplace's annual injury summary for 2024.",
"FED_OSHA_ITA_300A_SUMMARY_2023": "Each workplace's annual injury summary for 2023.",
"FED_OSHA_ITA_300A_SUMMARY_2025": "Each workplace's annual injury summary for 2025.",
"FED_OSHA_ITA_CASE_DETAIL_2025": "Individual workplace injuries and illnesses employers logged in 2025.",
"FED_MSHA_ACCIDENTS": "Every accident, injury and death at a US mine.",
"FED_MSHA_MINES": "Every mine in the United States, who operates it, and whether it is still active.",
"FED_DOL_EBSA_FORM5500_SCHEDULE_SB": "The actuary's report on whether a company pension plan has enough money to pay what it owes.",
"FED_PBGC_TRUSTEED_PLANS": "Company pension plans that failed and were taken over by the federal insurer.",

# ---- Multi-state settlements, shipping, open data ---------------------------
"FED_NAAG_MULTISTATE_SETTLEMENTS": "Settlements where groups of state attorneys general sued a company together.",
"FED_NOAA_AIS": "Ship movement tracking - where vessels have been, minute by minute, from their transponders.",
"MONEY__DEBT_REPAYMENT_CLIFF": "A Ripple-built view of debt repayments bunching up at particular dates.",
"INTL_FR_DATA_GOUV": "The catalogue of datasets the French government publishes.",
"INTL_CH_OPENDATASWISS": "The catalogue of datasets the Swiss government publishes.",
"INTL_DE_GOVDATA": "The catalogue of datasets the German government publishes.",
"INTL_GR_DATAGOV": "The catalogue of datasets the Greek government publishes.",
"INTL_CL_DATOSGOB": "The catalogue of datasets the Chilean government publishes.",
"INTL_CA_OPEN_CANADA": "The catalogue of datasets the Canadian government publishes.",
})

TABLES.update({

# ---- Politics, lobbying, elections ------------------------------------------
"INTL_ELECTIONS_CANADA_CONTRIBUTIONS": "Every political donation reported in Canada.",
"INTL_VOETEN_UNGA_VOTES": "How every country voted on every United Nations General Assembly resolution.",
"FED_FCC_LICENSING": "Licences to use the radio spectrum - broadcasters, mobile networks, and everyone else on the airwaves.",
"CA_LOBBY_COVER": "The cover pages of California lobbying reports - who filed, for whom, and for what period.",
"ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS": "Donations to New York City candidates in the 2021 election.",
"BILL_COSPONSORS": "Which members of Congress signed on to support which bills.",
"TX_LOBBY_COVER": "The cover pages of Texas lobbying reports.",
"ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS": "Donations to New York City candidates in the 2025 election.",
"TX_LOBBY_SUBJECT_MATTER": "What subjects Texas lobbyists were hired to work on.",
"ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION": "Donations to New York City candidates in the 2013 election.",
"ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION": "Donations to New York City candidates in the 2001 election.",
"ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION": "Donations to New York City candidates in the 2009 election.",
"FED_VOTEVIEW_ROLLCALL_META": "Every recorded vote taken in Congress, going back to 1789.",
"CA_LOBBY_CHG_LOG": "Changes filed to California lobbying registrations.",
"IRS527_8871_ORGS": "Political organisations that registered with the tax authority - the dark money vehicle.",
"IRS527_8872_REPORTS": "What those political organisations reported raising and spending.",
"FED_FEC_PAC_SUMMARY": "Summary totals for each political action committee.",
"TX_LOBBY_INDIVIDUAL_REPORTING": "What Texas lobbyists reported spending on individual officials.",
"BILLS": "Bills introduced in Congress.",
"FED_MEDSL_HOUSE_RETURNS": "US House election results, precinct by precinct.",
"CA_LOBBY_AMENDMENTS": "Amendments to California lobbying filings.",
"FEC_CANDIDATE": "Candidates for federal office.",
"FEC_CAND_CMTE_LINK": "Which campaign committee belongs to which candidate.",
"TX_LOBBY_FOOD_BEVERAGE": "Meals and drinks Texas lobbyists bought for officials.",
"FED_CONGRESS_LEGISLATORS": "Current and recent members of Congress and their biographical details.",
"MEMBER_CROSSWALK": "A Ripple-built map linking the same member of Congress across different ID systems.",
"MEMBER_SPINE": "A Ripple-built master list of members of Congress and their terms.",
"INTL_OWID_MILSPEND": "Military spending by country over time.",
"FEC_CANDIDATE_SUMMARY": "Summary fundraising totals per candidate.",
"CA_LOBBY_CONTRIBUTIONS": "Political donations reported by California lobbying interests.",
"FED_FJC_SERVICE": "Each federal judge's time on the bench - nominated, confirmed, sworn in, and how they left.",
"TX_LOBBY_GIFTS": "Gifts Texas lobbyists gave to officials.",
"FED_FJC_JUDGES": "Biographical records of every federal judge in US history.",
"FED_MEDSL_SENATE_RETURNS": "US Senate election results, precinct by precinct.",
"FED_MEDSL_PRESIDENT_RETURNS": "US presidential election results, precinct by precinct.",
"TX_LOBBY_TRANSPORTATION": "Travel Texas lobbyists paid for on behalf of officials.",
"VOTEVIEW_ROLLCALLS": "Recorded congressional votes, a second cut of the same data.",
"TX_LOBBY_EVENTS": "Events Texas lobbyists hosted for officials.",
"TX_LOBBY_ENTERTAINMENT": "Entertainment Texas lobbyists provided to officials.",
"XC_OWID_CPI": "Consumer price inflation by country over time.",
"CA_LOBBY_EMPLOYER": "The companies and groups that hire California lobbyists.",
"TX_LOBBY_AWARDS": "Awards and mementoes Texas lobbyists gave to officials.",
"ST_CANNABIS_POLICY_BUNDLES": "A compiled view of state cannabis policy over time.",
"TX_LOBBY_DOCKETS": "Specific regulatory dockets Texas lobbyists worked on.",
"MEMBER_MONEY_RAISED": "A Ripple-built summary of what each member of Congress raised.",
"XC_JCS_SCOTUS": "Academic estimates of where each Supreme Court justice sits ideologically.",
"FED_FEC_API": "A small sample of campaign finance records pulled through an automated feed.",
"CA_LOBBY_FIRM": "California lobbying firms.",
"CA_LOBBY_FIRM_EMPLOYER": "Which California lobbying firm works for which client, and for how long.",
"XC_JCS_MEDIANS": "Academic estimates of the ideological midpoint of the Supreme Court over time.",

# ---- Government purchasing --------------------------------------------------
"FED_SAM_EXCLUSIONS": "People and companies barred from receiving US government contracts or grants, and for how long.",
"INTL_EC_SERCOP": "Public procurement records from Ecuador's government purchasing system.",
"FED_USASPENDING_BULK": "Federal award records pulled in bulk.",
"FED_USASPENDING_SUBAWARDS": "Money passed down from a prime contractor to subcontractors.",

# ---- Reference lists --------------------------------------------------------
"FED_ITIS_REFERENCE_LINKS": "Links between species records and the scientific publications describing them.",
"FED_USGS_GNIS_ALL_NAMES": "Every named geographic feature in the US - every creek, ridge, town and school.",
"FED_ITIS_TAXONOMIC_UNITS": "The master scientific list of species and their classification.",
"FED_ITIS_GEOGRAPHIC_DIV": "Where each species is found.",
"FED_ITIS_SYNONYM_LINKS": "Alternative scientific names for the same species.",
"FED_ITIS_TAXON_AUTHORS_LKP": "The scientists credited with naming each species.",
"FED_ITIS_NODC_IDS": "Cross-references between species codes in different systems.",
"FED_ITIS_TU_COMMENTS_LINKS": "Links between species records and expert comments on them.",
"FED_ITIS_VERNACULARS": "Common everyday names for species, in multiple languages.",
"FED_ITIS_JURISDICTION": "Which countries and regions each species is native or introduced to.",
"XC_ROR_RESEARCH_ORGANIZATIONS": "The global registry of universities, institutes and research bodies.",
"FED_ITIS_VERN_REF_LINKS": "Sources backing up each common species name.",
"FED_ITIS_COMMENTS": "Expert notes attached to species records.",
"FED_ITIS_PUBLICATIONS": "The scientific publications underpinning species classifications.",
"XC_OWID_FERTILITY": "Birth rates by country over time.",
"FED_ITIS_OTHER_SOURCES": "Other sources feeding the species database.",
"INTL_GDELT": "A small sample from a global news event monitoring project.",
"FED_DHS_HIFLD": "A small sample of critical infrastructure location data.",
"FED_USGS_TOPOVIEW": "Historic US topographic maps and when they were published.",
"FED_ITIS_EXPERTS": "The taxonomists who vouch for species records.",
"FED_ITIS_TAXON_UNIT_TYPES": "The rank types used in scientific classification - genus, species and so on.",
"FED_ITIS_KINGDOMS": "The top-level kingdoms of life used to organise the species database.",

# ---- Rulemaking and internal ------------------------------------------------
"FED_FEDERAL_REGISTER_DOCUMENTS": "Every rule, proposed rule and notice the US government publishes in its official daily journal.",
"LEAD_QUEUE": "A Ripple-internal work list of leads to review. Not public data.",

# ---- Science and research ---------------------------------------------------
"FED_USGS_EARTHQUAKES": "Every recorded earthquake - where, when and how strong.",
"FED_NSF_AWARDS": "A small sample of national science research grants.",
"FED_NASA_OPEN_DATA": "A small sample of NASA's published datasets.",
"XC_OWID_AI_INCIDENTS_ANNUAL": "Annual counts of reported artificial intelligence incidents and harms.",
"FED_NIH_REPORTER": "Every federal medical research grant - who got it, how much, and for what.",
"FED_SBIR_STTR_AWARDS": "Federal research grants to small businesses.",
"FED_RETRACTION_WATCH": "Scientific papers that were retracted, and why.",
"XC_RETRACTION_WATCH_DATABASE": "The retracted scientific papers database, a second cut.",
"XC_BIORXIV_MEDRXIV": "Preprints - scientific papers posted publicly before peer review.",
"XC_OSF_REGISTRATIONS": "Research studies registered in advance, before results were known.",

# ---- Transport --------------------------------------------------------------
"FED_FRA_CASUALTIES": "Every person killed or injured on the US railroads.",
"FED_FAA_AIRCRAFT_REGISTRY": "Every civil aircraft registered in the US and who owns it.",
"FED_FAA_REGISTRY": "US aircraft registrations, a second cut of the same register.",
"FED_FRA_CROSSING_INCIDENTS": "Every collision at a railroad level crossing.",
"FED_FRA_EQUIPMENT_ACCIDENTS": "Train derailments, collisions and other equipment accidents.",
"FED_NTSB_AVIATION_AIRCRAFT": "The aircraft involved in investigated aviation accidents.",
"FED_NTSB_AVIATION_EVENTS": "Every aviation accident investigated by federal crash investigators.",
"FED_FRA_RAIL_DEATHS_BY_RAILROAD": "Rail deaths broken down by which railroad they happened on.",
})


# --------------------------------------------------------------------------
# WHAT EACH DATE FIELD MARKS
# --------------------------------------------------------------------------

FIELDS = {
    "YEAR": "the year the figures cover",
    "DATA_YEAR": "the year the figures cover",
    "FY": "the government budget year the figures cover — it starts on 1 October, not 1 January",
    "FISCAL_YEAR": "the government budget year the figures cover — it starts on 1 October, not 1 January",
    "APPLICABLEYEAR": "the year the figures apply to",
    "PERIOD": "the stretch of time the figures cover",
    "CYCLE": "the two-year election cycle the figures belong to",
    "ELECTION_CYCLE": "the two-year election cycle the figures belong to",
    "SUBMISSIONYEARQUARTER": "the three-month window in which the report was handed in",
    "SRC_QUARTER": "the three-month window the source file covers",
    "DATE": "the date on the record",
    "FILED": "the day the paperwork was filed",
    "DATE_FILED": "the day the paperwork was filed",
    "DATE_RECEIVED": "the day it arrived with the agency",
    "RECORD_DATE": "the day the record was written",
    "UPDATE_DATE": "the last time anyone changed the record — not when the thing itself happened",
    "LAST_REPORTED_DATE": "the most recent time this was reported to the agency",
    "FIRST_REPORTED_DATE": "the first time this was reported to the agency",
    "INCORPORATION_DATE": "the day the company was legally created",
    "TERMINATION_DATE": "the day it ended",
    "START_DATE": "the day the period began",
    "END_DATE": "the day the period ended",
    "PERIODSTARTDT": "the day the reporting period began",
    "PERIODENDDT": "the day the reporting period ended",
    "ACTION_DATE": "the day the action was taken",
    "_LOADED_AT": "the day we downloaded the file - nothing about the real world",
    "INGESTED_AT": "the day we downloaded the file - nothing about the real world",

    # Agency shorthand that would otherwise stay shorthand.
    "RNC_DETECTION_DATE": "the day the regulator spotted the facility was in serious breach",
    "RNC_RESOLUTION_DATE": "the day that serious breach was cleared up",
    "COMPL_PER_BEGIN_DATE": "the day the compliance period began",
    "COMPL_PER_END_DATE": "the day the compliance period ended",
    "NON_COMPL_PER_BEGIN_DATE": "the day the facility fell out of compliance",
    "NON_COMPL_PER_END_DATE": "the day the facility came back into compliance",
    "PWS_DEACTIVATION_DATE": "the day the public water system was shut down",
    "MSC_CHARGE_DATE": "the day the person was charged",
    "MSC_CONVICTION_DATE": "the day the person was convicted",
    "CAL_YR": "the calendar year",
    "CAND_ELECTION_YR": "the election year the candidate was running in",
    "FEC_ELECTION_YR": "the election year the regulator assigned to the filing",
    "YEAR_MFR": "the year the aircraft was built",
    "STRUCK_OFF_DATE": "the day the company was struck off the register - dissolved",
    "THRU_DATE": "the day the period ran to",
    "FROM_DATE": "the day the period ran from",
    "ACTIVITYDATE": "the day the activity took place",
    "AS_OF_DATE_IN_FORM_YYMMDD": "the date the figures are accurate as of",
    "TERM": "the day it ended",
    "TERM_DATE": "the day it ended",
    "METADATA_MODIFIED": "the last time the dataset's description was edited - not the data itself",
    "METADATA_CREATED": "the day the dataset's listing was first created",
    "PERIOD_OF_PERFORMANCE_START_DATE": "the day work on the contract was due to start",
    "PERIOD_OF_PERFORMANCE_CURRENT_END_DATE": "the day work on the contract is currently due to finish",
    "PERIOD_OF_PERFORMANCE_POTENTIAL_END_DATE": "the latest the contract could run to if every option is taken up",
    "ORDERING_PERIOD_END_DATE": "the last day new orders could be placed under the contract",
    "SOLICITATION_DATE": "the day the government asked for bids",
    "AWARD_DATE": "the day the contract or grant was handed out",
    "SURVEY_DATE": "the day inspectors visited",
    "DATE_LAST_INSPECTION": "the day of the most recent inspection",
    "DATE_LAST_FORMAL_ACTION": "the day of the most recent formal enforcement action",
    "REVOCATION_DATE": "the day the status was taken away",
    "REVOCATION_POSTING_DATE": "the day the revocation was published",
    "REINSTATEMENT_DATE": "the day the status was given back",
    "STRUCK_OFF": "the day the company was struck off the register",
    "FAIL_DATE": "the day it failed",
    "ACHIEVED_DATE": "the day the required action was completed",
    "TAX_PERIOD": "the tax period the return covers",
    "PERIOD_OF_REPORT": "the period the report covers",
    "YEAR_FILING_FOR": "the year the filing is about",
    "YEAR_OF_FILING": "the year the filing was made",
    "PROGRAM_YEAR": "the programme year the figures cover",
    "RECORD_CALENDAR_YEAR": "the calendar year of the record",
    "RECORD_FISCAL_YEAR": "the government budget year of the record",
    "OPERATING_YEAR": "the year the equipment started operating",
    "INCIDENT_YEAR": "the year the incident happened",
    "BIRTH_YEAR": "the year the person was born",
    "BIRTH_DATE": "the day the person was born",
    "DATE_OF_INCIDENT": "the day the incident happened",
    "DATE_TIME_RECEIVED": "the moment the report arrived",
    "DATE_TIME_COMPLETE": "the moment it was completed",
    "CERT_ISSUE_DATE": "the day the certificate was issued",
    "CERTIFICATION_DATE": "the day it was certified",
    "ESTABLISHED_DATE": "the day it was set up",
    "SETTLEMENT_ENTERED_DATE": "the day the settlement was formally entered",
    "HEARING_DATE": "the day of the hearing",
    "RULING_DATE": "the day the ruling came down",
    "DECISION_DATE": "the day the decision was made",
    "CORRECTION_DATE": "the day the problem was fixed",
    "SCHEDULE_DATE": "the day it was scheduled for",
    "ACTUAL_DATE": "the day it actually happened",
    "ACTUAL_BEGIN_DATE": "the day it actually started",
    "ACTUAL_END_DATE": "the day it actually finished",
    "TRANSACTION_DATE": "the day the money moved",
    "CONTRIBUTION_DATE": "the day the donation was made",
    "REFUND_DATE": "the day the money was given back",
    "DATE_OF_PAYMENT": "the day the payment was made",
    "TRANSFER_DATE": "the day it was transferred",
    "ENTRY_DATE": "the day it was entered into the system",
    "PROCESSING_DATE": "the day it was processed",
    "PUBLICATION_DATE": "the day it was published",
    "PUBLISH_DATE": "the day it was published",
    "EXPIRATION_DATE": "the day it expires",
    "EFFECTIVE_DATE": "the day it takes effect",
    "APPROVAL_DATE": "the day it was approved",
    "WITHDRAWN_DATE": "the day it was withdrawn",
    "CLOSE_DATE": "the day it closed",
    "FILE_DATE": "the day it was filed",
    "FILING_DATE": "the day it was filed",
    "LAST_ACTION_DATE": "the most recent time anything happened on it",
    "REPORT_RECEIVED_DATE": "the day the report arrived",
    "SOURCE_DATE": "the date given by the original source",
    "TAX_YEAR": "the tax year the figures cover",
    "REPORT_YEAR": "the year the report covers",
    "REPORTING_YEAR": "the year being reported on",
    "ACTIVITY_YEAR": "the year the activity took place",
    "ELECTION_YEAR": "the year of the election",
    "CALCULATED_RTC_DATE": "the day the facility was calculated to have returned to compliance",
    "ACTUAL_RTC_DATE": "the day the facility actually returned to compliance",
    "DATE_FILED_NOA": "the day the notice of appeal was filed",
    "DATE_JUDGMENT_EOD": "the day the judgment was entered on the court docket",
    "DATE_RECEIVED_COA": "the day the appeals court received it",
    "FDA_DT": "the day the medicines regulator logged the report",
    "INIT_FDA_DT": "the day the medicines regulator first logged the case",
    "MFR_DT": "the day the manufacturer logged it",
    "REPT_DT": "the day it was reported",
    "RPT_DATE": "the day it was reported",
    "APP_DATE": "the day the application was made",
    "AS_OF_DATE": "the date the figures are accurate as of",
    "FY_END_DATE": "the day the government budget year ended",
    "PAID_IN_FULL_DATE": "the day it was paid off in full",
    "FUGITIVE_END_DATE": "the day the defendant stopped being a fugitive - blank for the overwhelming majority, who never were one",
    "STAY_BOOK_OUT_DATE": "the day the person was released from detention",
    "DATETIME": "the moment it was recorded",
    "TIME": "the moment it was recorded",
    "BASE_DATETIME": "the moment the position was recorded",
    "LAST_TERM_END": "the day the most recent term of office ended",
    "DORM_DATE": "a date the source labels only as DORM - meaning not established",
    "AS_OF_DATE_IN_FORM_YYYY_MM_DD": "the date the figures are accurate as of",
    "DATEUPDATE": "the last time the record was updated",
}

# Word-level translations used by the fallback, so a derived line still reads
# like English rather than a column name with spaces in it.
WORDS = {
    "DT": "date", "DTE": "date", "TS": "time", "YR": "year", "MO": "month",
    "EFF": "effective", "EXP": "expiry", "TERM": "termination", "CERT": "certification",
    "APPT": "appointment", "RECV": "received", "SUB": "submission", "PUB": "published",
    "ISS": "issued", "REG": "registration", "INSP": "inspection", "VIOL": "violation",
    "ENF": "enforcement", "ACC": "accident", "OCCUR": "occurred", "CMPL": "completed",
    "ADJ": "adjudication", "DISP": "disposition", "SETTL": "settlement",
    "APPR": "approval", "REV": "revocation", "SVC": "service", "ANNL": "annual",
    "STMT": "statement", "TXN": "transaction", "AMT": "amount", "NUM": "number",
}

TRAILING = ("DATE", "DT", "DTE", "TIME", "TS", "YEAR", "YR", "ON", "AT",
            "DATETIME", "TIMESTAMP", "STAMP")
LEADING = ("DATE", "DT", "DATETIME", "TIMESTAMP")
FILLER = ("OF", "THE", "A", "COL", "COLUMN", "VAL", "VALUE", "FLD")


def gloss(col):
    """Turn an unlisted column name into a readable phrase.

    Deliberately conservative: it describes the field, it never invents a meaning
    for it. A name this cannot make sense of comes back as the plain words of the
    name itself, which is honest -- an invented explanation would not be.
    """
    if col in FIELDS:
        return FIELDS[col]
    parts = [p for p in re.split(r"[_\s]+", col) if p]

    # A trailing DATE / DT / YEAR is the word the sentence supplies itself.
    tail = ""
    while parts and parts[-1].upper() in TRAILING:
        tail = parts.pop().upper()
    # So is a leading one: DATE_OF_PAYMENT is "the payment date", not
    # "the date of payment date".
    while parts and parts[0].upper() in LEADING:
        if not tail:
            tail = parts[0].upper()
        parts.pop(0)
    parts = [p for p in parts if p.upper() not in FILLER]

    words = [WORDS.get(p.upper(), p.lower()) for p in parts]
    phrase = " ".join(words).strip()
    if not phrase:
        return "the date on the record"

    # Year first: RECEIVED_YEAR is a year, not a day, and the past-tense rule
    # below would otherwise turn it into "the day it was received".
    if tail in ("YEAR", "YR") and "year" not in phrase:
        if len(words) == 1 and words[0].endswith("ed") and len(words[0]) > 4:
            return "the year it was {}".format(words[0])
        return "the {} year".format(phrase)

    # One past-tense word reads far better as a clause than as a noun stack:
    # "the day it was terminated" beats "the terminated date".
    if len(words) == 1 and words[0].endswith("ed") and len(words[0]) > 4:
        return "the day it was {}".format(words[0])
    if phrase in ("start", "begin", "beginning"):
        return "the day it started"
    if phrase in ("end", "thru", "through", "finish"):
        return "the day it ended"

    # Never say "date" twice, and never call a year a date.
    if "year" in phrase or tail in ("YEAR", "YR"):
        return "the {}".format(phrase) if "year" in phrase else "the {} year".format(phrase)
    if any(w in phrase for w in ("date", "time", "day", "period", "quarter", "month")):
        return "the {}".format(phrase)
    return "the {} date".format(phrase)


# Where the same column name means something different depending on the dataset.
# ARCOS transactions are pills moving, not money; a court's "cert" is the Supreme
# Court agreeing to hear a case, not a certificate.
TABLE_FIELDS = {
    ("FED_DEA_ARCOS", "TRANSACTION_DATE"): "the day the pills were shipped",
    ("FED_COURTLISTENER_DOCKETS", "DATE_CERT_GRANTED"): "the day the Supreme Court agreed to hear the case",
    ("FED_COURTLISTENER_DOCKETS", "DATE_CERT_DENIED"): "the day the Supreme Court refused to hear the case",
    ("FED_COURTLISTENER_DOCKETS", "DATE_REARGUMENT_DENIED"): "the day a request to argue the case again was refused",
    ("FED_COURTLISTENER_DOCKETS", "DATE_LAST_FILING"): "the day of the most recent filing in the case",
    ("FED_COURTLISTENER_DOCKETS", "DATE_TERMINATED"): "the day the case was closed",
    ("FED_COURTLISTENER_DOCKETS", "DATE_FILED"): "the day the case was opened",
    ("FED_NOAA_AIS", "BASE_DATETIME_HOUR"): "the hour the ship's position was recorded",
    ("FED_CFPB_COMPLAINTS", "DATE_SENT_TO_COMPANY"): "the day the complaint was passed on to the company",
    ("FED_CFPB_COMPLAINTS", "RECEIVED_MONTH"): "the month the complaint arrived",
    ("FED_CFPB_HMDA_HISTORIC", "AS_OF_YEAR"): "the year the lending figures are as of",
    ("FED_USASPENDING_ASSISTANCE_FULL", "INITIAL_REPORT_DATE"): "the day the award was first reported",
    ("FED_USASPENDING_ASSISTANCE_FULL", "LAST_MODIFIED_DATE"): "the last time the award record was changed",
    ("FED_USASPENDING_CONTRACTS_FULL", "ACTION_DATE"): "the day the contract action took effect",
    ("FED_USASPENDING_ASSISTANCE_FULL", "ACTION_DATE"): "the day the award action took effect",
    ("FED_MSHA_VIOLATIONS", "VIOLATION_OCCUR_DATE"): "the day the mine safety violation happened",
    ("FED_MSHA_ACCIDENTS", "ACCIDENT_DATE"): "the day of the accident at the mine",
    ("FED_CMS_NURSING_HOME_DEFICIENCIES", "SURVEY_DATE"): "the day inspectors visited the nursing home",
    ("FED_FDA_FAERS_DRUG", "EXP_DT"): "the drug's expiry date",
    ("FED_SLAVEVOYAGES_INTRAAMERICAN", "YEAR"): "the year of the voyage",
}


def field_gloss(source, column):
    """What this date means, in this particular dataset."""
    hit = TABLE_FIELDS.get((source.upper(), column.upper()))
    return hit if hit else gloss(column.upper())


def describe(source, column, means, grain):
    """One line a stranger could read: what the data is, and what the date marks."""
    what = TABLES.get(source.upper())
    if not what:
        what = readable_source(source)
    when = field_gloss(source, column)
    frame = {
        "happened": "This date is {} — when the thing itself took place.",
        "reported": "This date is {} — when it was reported, which can be long after it happened.",
        "decided": "This date is {} — when an authority ruled on it.",
        "span_start": "This date is {} — the opening edge of a period, not a one-off event.",
        "span_end": "This date is {} — the closing edge of a period, not a one-off event.",
    }[means]
    precision = {
        "day": "Precise to the day.",
        "month": "Only precise to the month.",
        "quarter": "Only precise to the three-month quarter.",
        "year": "Only precise to the year — there is no finer detail underneath it.",
    }[grain]
    return what, frame.format(when), precision


def readable_source(source):
    """Fallback label for a dataset with no hand-written description yet."""
    return "A public dataset: {}. No plain-English description written yet.".format(
        source.replace("_", " ").title())
