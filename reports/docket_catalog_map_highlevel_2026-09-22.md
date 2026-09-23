# Docket mapped to THE_CATALOG, high level, 2026-09-22

150 questions. Catalog: 644 mart tables, 20,724 columns, 640 measured joins.

## Families, biggest first

| family | questions | hub tables | keys that carry it | measured joins |
|---|---|---|---|---|
| HEALTH | 43 | HEALTH__FED_CMS_OPEN_PAYMENTS, HEALTH__FED_CMS_FACILITY_AFFILIATION, HEALTH__FED_CMS_POS_OTHER | NPI, ASSOCIATE_ID, COVERED_RECIPIENT_PROFILE_ID | 8/43 |
| CROSS 3+ | 16 | HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY, PROCUREMENT__FED_SAM_EXCLUSIONS, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | LEI, IMO_NUMBER, STATE_FIPS | 3/16 |
| HEALTH+JUSTICE | 8 | JUSTICE__XC_VERA_INCARCERATION_TRENDS, HEALTH__FED_NURSINGHOME411, HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | none measured | 0/8 |
| HEALTH+RAW | 7 | FED_CMS_PARTD_PRESCRIBER_DRUG, HEALTH__FED_NURSINGHOME411, HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS | CHAIN_ID | 1/7 |
| HOUSING | 6 | HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS, HOUSING__FED_CFPB_HMDA_HISTORIC, HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS | none measured | 0/6 |
| ENVIRONMENT+HEALTH | 6 | HEALTH__FED_CMS_HCRIS, ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS, ENVIRONMENT__FED_EPA_TRI_FACILITY | none measured | 0/6 |
| ENVIRONMENT+HOUSING | 5 | ENVIRONMENT__FED_NOAA_STORM_EVENTS, ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT, HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF | none measured | 0/5 |
| FINANCE+POLITICS | 4 | POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP, FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES, FINANCE__FED_FEC_CAND_CMTE_LINKAGE | CAND_ID | 1/4 |
| PROCUREMENT+RAW | 3 | PROCUREMENT__FED_SAM_EXCLUSIONS, FED_USASPENDING_CONTRACTS_FULL_R2, FED_USASPENDING_ASSISTANCE_FULL | none measured | 0/3 |
| ECONOMICS+RAW | 3 | ECONOMICS__FED_FAC_SINGLE_AUDIT, FED_USASPENDING_ASSISTANCE_FULL, FED_USASPENDING_CONTRACTS_FULL_R2 | none measured | 0/3 |
| FINANCE+RAW | 3 | FINANCE__FED_FEC_INDIV_CONTRIBUTIONS, FED_FARA_BULK, FINANCE__FED_SENATE_STOCK_WATCHER | none measured | 0/3 |
| JUSTICE+RAW | 3 | JUSTICE__FED_CISA_KEV, FED_USASPENDING_CONTRACTS_FULL_R2, JUSTICE__FED_OFAC_SDN | none measured | 0/3 |
| ECONOMICS+HEALTH | 2 | HEALTH__FED_CMS_HCRIS, ECONOMICS__FED_BLS_QCEW, ECONOMICS__FED_SBA_PPP | none measured | 0/2 |
| JUSTICE | 2 | JUSTICE__FED_COURTLISTENER_INVESTMENTS, JUSTICE__FED_COURTLISTENER_POSITIONS, JUSTICE__FED_FJC_IDB_CIVIL | FINANCIAL_DISCLOSURE_ID | 1/2 |
| ECONOMICS+FINANCE | 2 | ECONOMICS__FED_FDIC_FAILED_BANKS, FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS, FINANCE__FED_PCAOB_FORM_AP_FILINGS | none measured | 0/2 |
| FINANCE+HEALTH | 2 | FINANCE__FED_FEC_COMMITTEES, HEALTH__FED_CMS_OPEN_PAYMENTS, FINANCE__FED_FEC_LEADERSHIP_PAC | none measured | 0/2 |
| ENVIRONMENT | 2 | ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS, ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS, ENVIRONMENT__FED_FRACFOCUS_REGISTRY | none measured | 0/2 |
| TRANSPORT | 2 | TRANSPORT__FED_NTSB_AVIATION_EVENTS, TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT, TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY | EV_ID, NTSB_NO, INCIDENT_NUMBER | 2/2 |
| ENVIRONMENT+RAW | 2 | FED_EPA_CAMPD_EMISSIONS_DAILY, ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY, ENVIRONMENT__FED_EPA_AQS_SITES | none measured | 0/2 |
| HEALTH+HOUSING | 2 | HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS, HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY, HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS | none measured | 0/2 |
| HEALTH+IMMIGRATION | 1 | HEALTH__FED_HHS_OIG_LEIE, HEALTH__FED_CMS_FACILITY_AFFILIATION, IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS | NPI | 1/1 |
| ENVIRONMENT+FINANCE | 1 | FINANCE__FED_FDIC_BANK_DATA, ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | none measured | 0/1 |
| FINANCE+LABOR | 1 | LABOR__FED_DOL_OLMS, FINANCE__FED_FEC_COMMITTEES | none measured | 0/1 |
| EDUCATION+REGULATORY | 1 | EDUCATION__FED_SENATE_LDA_FILINGS, REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS | none measured | 0/1 |
| EDUCATION+POLITICS | 1 | EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND, POLITICS__FED_FEC_PAC_SUMMARY, POLITICS__FED_MEDSL_HOUSE_RETURNS | none measured | 0/1 |
| GOVERNANCE+RAW | 1 | GOVERNANCE__FED_REVOLVINGDOOR_PROJECT, FED_USASPENDING_CONTRACTS_FULL_R2 | none measured | 0/1 |
| JUSTICE+POLITICS | 1 | POLITICS__FED_EAC_EAVS, JUSTICE__XC_VERA_INCARCERATION_TRENDS, POLITICS__FED_MEDSL_HOUSE_RETURNS | none measured | 0/1 |
| FINANCE+JUSTICE | 1 | JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS, JUSTICE__FED_FJC_IDB_CIVIL | none measured | 0/1 |
| ENVIRONMENT+LABOR | 1 | LABOR__FED_MSHA_MINES, ENVIRONMENT__FED_NID_DAMS, LABOR__FED_MSHA_VIOLATIONS | MINE_ID | 1/1 |
| HOUSING+RAW | 1 | FED_USASPENDING_CONTRACTS_FULL_R2, HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | none measured | 0/1 |
| LEGAL_ENFORCEMENT+RAW | 1 | FED_DEA_ARCOS_FULL, LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS | none measured | 0/1 |
| SCIENCE_RESEARCH | 1 | SCIENCE_RESEARCH__FED_NIH_REPORTER, SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS, SCIENCE_RESEARCH__FED_RETRACTION_WATCH | none measured | 0/1 |
| ECONOMICS+LABOR | 1 | LABOR__FED_OSHA_ITA_300A_SUMMARY_2024, ECONOMICS__FED_DOL_OSHA_INSPECTIONS, ECONOMICS__FED_BLS_QCEW | none measured | 0/1 |
| LABOR | 1 | LABOR__FED_MSHA_VIOLATIONS, LABOR__FED_MSHA_ACCIDENTS | CONTROLLER_ID, MINE_ID | 1/1 |
| IMMIGRATION+RAW | 1 | IMMIGRATION__FED_ICE_DETENTION_STINTS, IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES, FED_USASPENDING_CONTRACTS_FULL_R2 | none measured | 0/1 |
| IMMIGRATION+JUSTICE | 1 | IMMIGRATION__FED_ICE_DETAINERS, JUSTICE__XC_VERA_INCARCERATION_TRENDS | none measured | 0/1 |
| CORPORATE_REGISTRY+JUSTICE | 1 | CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC, JUSTICE__INTL_OPENSANCTIONS_DEFAULT, JUSTICE__FED_OFAC_SDN | none measured | 0/1 |
| ECONOMICS+POLITICS | 1 | POLITICS__IRS527_8871_ORGS, ECONOMICS__FED_IRS_AUTO_REVOCATIONS, POLITICS__IRS527_8872_REPORTS | FORM_ID_NUMBER | 1/1 |
| CONSUMER_PROTECTION+HOUSING | 1 | CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS, HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF | none measured | 0/1 |
| FINANCE+HOUSING | 1 | FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS, HOUSING__FED_MAPPING_INEQUALITY | none measured | 0/1 |
| CONSUMER_SAFETY | 1 | CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS, CONSUMER_SAFETY__FED_NHTSA_RECALLS | none measured | 0/1 |
| HOUSING+JUSTICE | 1 | JUSTICE__FED_FJC_IDB_BANKRUPTCY, HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | none measured | 0/1 |
| ENERGY+ENVIRONMENT | 1 | ENERGY__FED_EIA861_RELIABILITY, ENERGY__FED_EIA861_SERVICE_TERRITORY, ENVIRONMENT__FED_NOAA_STORM_EVENTS | none measured | 0/1 |
| IMMIGRATION | 1 | IMMIGRATION__FED_EOIR_CASES | none measured | 0/1 |
| POLITICS+RAW | 1 | FED_HOUSE_FD_PTR_INDEX, POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | none measured | 0/1 |
| ECONOMICS+ENVIRONMENT | 1 | ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY, ECONOMICS__FED_BLS_QCEW | none measured | 0/1 |
| HEALTH+PROCUREMENT | 1 | PROCUREMENT__FED_SAM_EXCLUSIONS, HEALTH__FED_CMS_NPPES | none measured | 0/1 |

## Every question, by family

### HEALTH, 43 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 2 | found something | Which nursing home owners get fined the most per home, and does it repeat? | HEALTH__FED_NURSINGHOME411, HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES, HEALTH__FED_CMS_NURSING_HOME_PENALTIES | none |
| 6 | part done | Do dialysis chains that dominate a rural area have worse patient outcomes? | HEALTH__FED_CMS_DIALYSIS, HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES, HEALTH__FED_CMS_FACILITY_AFFILIATION, HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE, HEALTH__FED_CMS_OPEN_PAYMENTS | HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [34] ; HEALTH__FED_CMS_OPEN_PAYMENTS.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [500450] ; HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [326347] |
| 7 | found something | Are banned doctors working at clinics serving poor neighborhoods? | HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES, HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS, HEALTH__FED_HHS_OIG_LEIE | none |
| 10 | part done | Are the suppliers who bill the most also getting kickback-like payments? | HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER | none |
| 11 | part done | Do money-losing hospitals still have doctors taking big drug company payments? | HEALTH__FED_CMS_HCRIS, HEALTH__FED_CMS_FACILITY_AFFILIATION, HEALTH__FED_CMS_OPEN_PAYMENTS_2023 | HEALTH__FED_CMS_OPEN_PAYMENTS_2023.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [472757] |
| 12 | part done | Do hospitals with financial trouble also have padded ventilator equipment billing? | HEALTH__FED_CMS_LTCH, HEALTH__FED_CMS_POS_OTHER, HEALTH__FED_CMS_FACILITY_AFFILIATION, HEALTH__FED_CMS_OPEN_PAYMENTS | HEALTH__FED_CMS_OPEN_PAYMENTS.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [500450] |
| 13 | same as another | Do owners re-register the business right after getting fire-safety fines? | HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES, HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | none |
| 14 | nothing there | Are clinics claiming to be 'rural' actually sitting in cities? | HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS | none |
| 16 | nothing there | Are any of them on the federal fraud exclusion list? | HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM, HEALTH__FED_HHS_OIG_LEIE | none |
| 18 | part done | Do they order more of that device at the hospital they work for? | HEALTH__FED_CMS_OPEN_PAYMENTS, HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | none |
| 19 | nothing there | Do the ones taking industry payments still get top bonuses? | HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE, HEALTH__FED_CMS_PART_D_PRESCRIBERS | none |
| 20 | found a little | Are the same people running both, and is that a conflict? | HEALTH__FED_CMS_FACILITY_AFFILIATION | none |
| 23 | found something | How much money did banned suppliers still collect? | HEALTH__FED_HHS_OIG_LEIE, HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL | none |
| 24 | not started | Nothing to compare yet, program just started | HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS | none |
| 25 | found a little | Are centers whose local site shut down still collecting Medicare money as if open? | HEALTH__FED_CMS_POS_OTHER, HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS, HEALTH__FED_HRSA_SHORTAGE_AREAS | none |
| 27 | found something | Are any of them already banned for past fraud? | HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS, HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS, HEALTH__FED_HHS_OIG_LEIE, HEALTH__FED_CMS_FACILITY_AFFILIATION | HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [49] ; HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [103] ; HEALTH__FED_HHS_OIG_LEIE.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [15] |
| 28 | part done | Do homes exaggerate patient sickness to get paid more? | HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY, HEALTH__FED_NURSINGHOME411, HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | none |
| 30 | found something | Do new owners appear right after a home gets penalized, like a shell game? | HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS, HEALTH__FED_CMS_NURSING_HOME_PENALTIES | none |
| 31 | found a little | Do hospital-owned home health agencies perform worse but cost more? | HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS, HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS, HEALTH__FED_CMS_HOME_HEALTH | HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ASSOCIATE_ID = HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.ASSOCIATE_ID [475] ; HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.ASSOCIATE_ID = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ASSOCIATE_ID [475] ; HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.NPI = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.NPI [4] |
| 108 | not started | Were they still being paid after their device got recalled? | HEALTH__FED_FDA_DEVICE_ENFORCEMENT, HEALTH__FED_FDA_DEVICE_510K, HEALTH__FED_CMS_OPEN_PAYMENTS | none |
| 109 | not started | Do they have more reported deaths than devices reviewed the normal way? | HEALTH__FED_FDA_MAUDE, HEALTH__FED_FDA_DEVICE_510K | none |
| 111 | not started | Did their nearest full-service hospital shut down? | HEALTH__FED_IHS_FACILITIES, HEALTH__FED_IHS_SCB_FACILITY, HEALTH__FED_CMS_POS_OTHER | none |
| E37 | nothing there | Does a pay raise from a drug company lead to more prescriptions? | HEALTH__FED_CMS_OPEN_PAYMENTS_2023, HEALTH__FED_CMS_OPEN_PAYMENTS, HEALTH__FED_CMS_PART_D_PRESCRIBERS | HEALTH__FED_CMS_OPEN_PAYMENTS.COVERED_RECIPIENT_PROFILE_ID = HEALTH__FED_CMS_OPEN_PAYMENTS_2023.COVERED_RECIPIENT_PROFILE_ID [715581] ; HEALTH__FED_CMS_OPEN_PAYMENTS_2023.COVERED_RECIPIENT_PROFILE_ID = HEALTH__FED_CMS_OPEN_PAYMENTS.COVERED_RECIPIENT_PROFILE_ID [715581] |
| E38 | found something | Are drug and device companies still paying them anyway? | HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS, HEALTH__FED_CMS_OPEN_PAYMENTS | none |
| E39 | found something | Do the paid ones prescribe way more opioids than unpaid ones? | HEALTH__FED_CMS_OPEN_PAYMENTS, HEALTH__FED_CMS_PART_D_PRESCRIBERS | none |
| E40 | found something | Are brand-new doctors billing Medicare for millions in expensive wound-care products? | HEALTH__FED_CMS_NPPES, HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI | none |
| E41 | found something | Can hospitals still legally order tests and equipment through them? | HEALTH__FED_HHS_OIG_LEIE, HEALTH__FED_CMS_ORDER_AND_REFERRING | none |
| E42 | found something | Is drug industry money still being sent to them? | HEALTH__FED_CMS_NPPES, HEALTH__FED_CMS_OPEN_PAYMENTS | none |
| E43 | found something | Were they already losing money before the sale? | HEALTH__FED_CMS_HCRIS, HEALTH__FED_CMS_POS_OTHER | none |
| E44 | found something | Did its safety violations get worse right before the fines hit? | HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES, HEALTH__FED_CMS_NURSING_HOME_PENALTIES | none |
| E46 | nothing there | Are these 'triple owners' actually better or worse than others? | HEALTH__FED_CMS_FACILITY_AFFILIATION, HEALTH__FED_NURSINGHOME411 | none |
| E47 | found something | Were they already in financial trouble before converting? | HEALTH__FED_CMS_HCRIS, HEALTH__FED_CMS_POS_OTHER | none |
| E48 | found something | Were their financial reports already bad beforehand? | HEALTH__FED_CMS_HCRIS, HEALTH__FED_CMS_POS_OTHER | none |
| E51 | found a little | Does that label actually bring in more clinics? | HEALTH__FED_HRSA_HPSA_PRIMARY_CARE, HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES | HEALTH__FED_HRSA_HPSA_PRIMARY_CARE.BHCMIS_ORGANIZATION_ID = HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES.BHCMIS_ORGANIZATION_ID [1515] ; HEALTH__FED_HRSA_HPSA_PRIMARY_CARE.STATE_COUNTY_FIPS_CODE = HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES.STATE_COUNTY_FIPS_CODE [2271] ; HEALTH__FED_HRSA_HPSA_PRIMARY_CARE.STATE_FIPS_CODE = HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES.STATE_FIPS_CODE [59] ; HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES.BHCMIS_ORGANIZATION_ID = HEALTH__FED_HRSA_HPSA_PRIMARY_CARE.BHCMIS_ORGANIZATION_ID [1515] ; HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES.STATE_COUNTY_FIPS_CODE = HEALTH__FED_HRSA_HPSA_PRIMARY_CARE.STATE_COUNTY_FIPS_CODE [2271] ; HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES.STATE_FIPS_CODE = HEALTH__FED_HRSA_HPSA_PRIMARY_CARE.STATE_FIPS_CODE [59] |
| E56 | nothing there | Do bonus and non-bonus doctors get similar industry money? | HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE, HEALTH__FED_CMS_OPEN_PAYMENTS | none |
| E57 | found something | Are they also the ones industry pays the most? | HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER, HEALTH__FED_CMS_OPEN_PAYMENTS | none |
| E58 | nothing there | Do states with more malpractice payouts also get more industry money? | HEALTH__FED_HRSA_NPDB, HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE, HEALTH__FED_CMS_OPEN_PAYMENTS_2023 | none |
| E59 | nothing there | Do they have the worst quality ratings? | HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER, HEALTH__FED_CMS_HOSPITAL_GENERAL | none |
| E62 | found something | Are they still getting cited for missing sprinkler systems? | HEALTH__FED_NURSINGHOME411, HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | none |
| E63 | found a little | Does patient harm go up when leadership keeps turning over? | HEALTH__FED_NURSINGHOME411, HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | none |
| E68 | found something | Do they give very little free care to the poor despite huge profits? | HEALTH__FED_CMS_HCRIS | none |
| E71 | found a little | Does more payment per person mean more opioid prescribing? | HEALTH__FED_CMS_OPEN_PAYMENTS, HEALTH__FED_CMS_PART_D_PRESCRIBERS | none |
| E74 | part done | Is there a record of who the new owner is? | HEALTH__FED_CMS_HOME_HEALTH_OWNERS, HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS, HEALTH__FED_CMS_HOME_HEALTH | HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ASSOCIATE_ID = HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ASSOCIATE_ID [8933] ; HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ENROLLMENT_ID = HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ENROLLMENT_ID [11224] ; HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.NPI = HEALTH__FED_CMS_HOME_HEALTH_OWNERS.NPI [11184] ; HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ASSOCIATE_ID = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ASSOCIATE_ID [8933] ; HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ENROLLMENT_ID = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ENROLLMENT_ID [11224] ; HEALTH__FED_CMS_HOME_HEALTH_OWNERS.NPI = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.NPI [11184] |

### CROSS 3+, 16 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 9 | part done | Do the biggest polluters also pay their workers the least? | ENVIRONMENT__FED_EPA_GHGRP_FACILITY, ECONOMICS__FED_BLS_QCEW, HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | none |
| 22 | found something | Do those same neighborhoods have more toxic factories today? | ENVIRONMENT__FED_EPA_TRI_FACILITY, ENVIRONMENT__FED_EPA_TRI_BASIC_2023, HOUSING__FED_MAPPING_INEQUALITY, HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | none |
| 76 | not started | Do they sell their company stock right before bad news like a fine hits? | FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS, ECONOMICS__FED_SEC_EDGAR_COMPANY_TICKERS, HEALTH__FED_NURSINGHOME411 | none |
| 78 | not started | Do they trade stock in industries their own committee oversees? | FINANCE__FED_SENATE_STOCK_WATCHER, POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP, FED_VOTEVIEW_ROLLCALLS | none |
| 81 | not started | Did executives sell their own stock right before the collapse? | LABOR__FED_PBGC_TRUSTEED_PLANS, FED_DOL_FORM5500_FULL, FINANCE__FED_SEC_DERA_SUB_2026Q1, FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS | none |
| 103 | not started | Do they still win federal contracts afterward? | ENVIRONMENT__FED_USCG_NRC_INCIDENTS, FED_USASPENDING_CONTRACTS_FULL_R2, PROCUREMENT__FED_SAM_EXCLUSIONS | none |
| 116 | not started | Do they pay the legal minimum wage and also rack up serious safety violations? | IMMIGRATION__FED_DOL_OFLC, ECONOMICS__FED_DOL_OSHA_INSPECTIONS, PROCUREMENT__FED_SAM_EXCLUSIONS | none |
| 118 | part done | Do the ones with the worst loan losses also have enforcement actions against them? | ECONOMICS__FED_SBA_LOANS, JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS, FINANCE__FED_FDIC_BANK_DATA | none |
| 121 | not started | Are any of them U.S. doctors or political donors? | CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS, HEALTH__FED_CMS_OPEN_PAYMENTS | none |
| 123 | not started | Who's the real parent company hiding behind them? | ECONOMICS__INTL_GLEIF_REPEX, ECONOMICS__INTL_GLEIF, HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF, ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | ECONOMICS__INTL_GLEIF.LEI = ECONOMICS__INTL_GLEIF_REPEX.LEI [3142422] ; ECONOMICS__INTL_GLEIF_REPEX.LEI = ECONOMICS__INTL_GLEIF.LEI [3142422] |
| 124 | found something | How much do they pay their top executives? | HEALTH__HOSPITAL_OFFICER_PAY, ECONOMICS__FED_IRS_BMF, FED_IRS_990_EFILE_INDEX | none |
| 140 | not started | Which investment funds and political donors are behind them? | ENVIRONMENT__FED_EPA_EGRID_PLANT_2022, ENERGY__FED_EIA860_4_OWNER, FED_SEC_13F_POSITIONS, POLITICS__FED_FEC_PAC_SUMMARY | none |
| A32 | not started | Do banned companies' owners also donate to political campaigns? | HEALTH__FED_HHS_OIG_LEIE, PROCUREMENT__FED_SAM_EXCLUSIONS, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | none |
| A34 | not started | Do polluted districts get less help from their representative? | FED_HOUSE_DISBURSEMENTS, ENVIRONMENT__FED_EPA_TRI_FACILITY, HOUSING__FED_MAPPING_INEQUALITY | none |
| A37 | not started | Do sanctioned individuals still show up as political donors? | JUSTICE__FED_OFAC_SDN, INTL_UN_CONSOLIDATED_SANCTIONS, JUSTICE__INTL_UK_SANCTIONS_LIST, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | JUSTICE__FED_OFAC_SDN.IMO_NUMBER = JUSTICE__INTL_UK_SANCTIONS_LIST.IMO_NUMBER [29] ; JUSTICE__INTL_UK_SANCTIONS_LIST.IMO_NUMBER = JUSTICE__FED_OFAC_SDN.IMO_NUMBER [29] |
| E52 | found a little | Do wages, suicide, and overdose rates all get worse there? | JUSTICE__XC_VERA_INCARCERATION_TRENDS, ECONOMICS__FED_BLS_QCEW, HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | JUSTICE__XC_VERA_INCARCERATION_TRENDS.STATE_FIPS = ECONOMICS__FED_BLS_QCEW.STATE_FIPS [45] |

### HEALTH+JUSTICE, 8 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 8 | part done | When a county's jail population spikes, does drug overdose rise later? | JUSTICE__XC_VERA_INCARCERATION_TRENDS, HEALTH__FED_HRSA_SHORTAGE_AREAS, HEALTH__FED_CDC_DRUG_POISONING_COUNTY | none |
| 113 | not started | Are companies still paying doctors to promote them? | JUSTICE__FED_JPML_PENDING_MDLS, HEALTH__FED_CMS_OPEN_PAYMENTS | none |
| 133 | not started | Do the most-sued chains also get the most fines? | JUSTICE__FED_FJC_IDB_CIVIL, HEALTH__FED_NURSINGHOME411, HEALTH__FED_CMS_NURSING_HOME_PENALTIES | none |
| 134 | not started | Are they still allowed to work in health care because they were never formally banned? | JUSTICE__FED_FJC_IDB_CRIMINAL, HEALTH__FED_HHS_OIG_LEIE | none |
| 135 | not started | Does patient care quality drop afterward? | JUSTICE__XC_RANSOMWARELIVE_VICTIMS, HEALTH__FED_CMS_HOSPITAL_GENERAL, HEALTH__FED_NURSINGHOME411 | none |
| 139 | part done | Are more dealers in an area linked to more gun deaths? | JUSTICE__FED_ATF_FFL, JUSTICE__FED_FBI_NICS_CHECKS, HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | none |
| E35 | found a little | Did overdose deaths rise where jails emptied out? | JUSTICE__XC_VERA_INCARCERATION_TRENDS, HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | none |
| E67 | nothing there | Do they also have fewer doctors available? | JUSTICE__XC_VERA_INCARCERATION_TRENDS, HEALTH__FED_CMS_NPPES | none |

### HEALTH+RAW, 7 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 4 | found something | Do addiction doctors get paid more by drugmakers when they prescribe more? | HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS, FED_CMS_PARTD_PRESCRIBER_DRUG, HEALTH__FED_CMS_OPEN_PAYMENTS_2022 | none |
| 106 | not started | Are those same counties still struggling with opioids today? | FED_DEA_ARCOS_FULL, HEALTH__FED_CDC_DRUG_POISONING_COUNTY, HEALTH__FED_CMS_PART_D_PRESCRIBERS | none |
| 110 | not started | Do the same doctors' prescribing costs jump right along with it? | FED_CMS_NADAC, HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP, FED_CMS_PARTD_PRESCRIBER_DRUG | none |
| 143 | part done | Are they paying the same doctors running the trial to also promote the drug? | FED_CLINICALTRIALS_FULL, HEALTH__FED_CMS_OPEN_PAYMENTS | none |
| E69 | part done | How much grant money reaches each patient? | HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO, HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS, FED_USASPENDING_ASSISTANCE_FULL | none |
| E70 | nothing there | Are the worst-rated homes still getting VA contracts? | FED_USASPENDING_CONTRACTS_FULL_R2, HEALTH__FED_NURSINGHOME411 | none |
| E75 | found something | Did the worst chains get big pandemic bailout money? | FED_HRSA_PROVIDER_RELIEF_FUND, HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND, HEALTH__NURSING_HOME_RELIEF_BY_CHAIN, HEALTH__FED_NURSINGHOME411 | HEALTH__FED_NURSINGHOME411.CHAIN_ID = HEALTH__NURSING_HOME_RELIEF_BY_CHAIN.CHAIN_ID [617] ; HEALTH__NURSING_HOME_RELIEF_BY_CHAIN.CHAIN_ID = HEALTH__FED_NURSINGHOME411.CHAIN_ID [617] |

### HOUSING, 6 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 5 | part done | Do people get worse loan terms right after a hurricane or flood? | HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS, HOUSING__FED_CFPB_HMDA_HISTORIC | none |
| 96 | not started | Do they still get disaster payouts for flood damage? | HOUSING__FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK, HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | none |
| 97 | not started | Are they being rebuilt each time instead of relocated? | HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS, HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS, HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS | none |
| 130 | not started | Are their affordability contracts expiring in fast-gentrifying areas? | HOUSING__FED_HUD_MF_SECTION8_CONTRACTS, HOUSING__FED_FHFA_HPI | none |
| 131 | not started | Do they charge higher rates in historically redlined neighborhoods? | HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT, HOUSING__FED_MAPPING_INEQUALITY, HOUSING__FED_CFPB_HMDA_HISTORIC | none |
| E72 | nothing there | Is it sitting empty more than in safer counties? | HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS, HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | none |

### ENVIRONMENT+HEALTH, 6 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 29 | part done | Do hospitals near the most toxic sites fail financially more often? | ENVIRONMENT__FED_EPA_TRI_FACILITY, HEALTH__FED_CMS_HCRIS, HEALTH__FED_CMS_POS_OTHER | none |
| 98 | not started | Are any sitting downstream of a dam rated poor with no emergency plan? | ENVIRONMENT__FED_NID_DAMS, HEALTH__FED_CMS_NURSING_HOME | none |
| E34 | nothing there | Do they have more drug overdose deaths? | ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS, HEALTH__FED_CDC_DRUG_POISONING_COUNTY | none |
| E45 | nothing there | Do safety violations spike after a storm hits the area? | HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES, ENVIRONMENT__FED_NOAA_STORM_EVENTS | none |
| E60 | found a little | Do they die at a higher rate? | HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES, ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | none |
| E61 | found a little | Do they also have worse finances? | ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS, HEALTH__FED_CMS_HCRIS | none |

### ENVIRONMENT+HOUSING, 5 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 3 | nothing there | Do banks that lend money also own the polluting sites? | HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF, ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | none |
| 26 | part done | Does housing sit empty after a big storm instead of getting rebuilt? | ENVIRONMENT__FED_NOAA_STORM_EVENTS, HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS | none |
| 101 | not started | Are they still using outdated flood maps? | ENVIRONMENT__FED_NOAA_STORM_EVENTS, HOUSING__FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK | none |
| E32 | nothing there | Do drinking water violations spike after a flood? | ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT, HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | none |
| E55 | nothing there | Is poor housing placed disproportionately near hazards? | HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS, ENVIRONMENT__FED_EPA_ECHO, ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | none |

### FINANCE+POLITICS, 4 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 84 | lit — $586.0M against, $191.4M for, congress-matched | Who's spending money for or against them in elections? | FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES, FINANCE__FED_FEC_CAND_CMTE_LINKAGE, POLITICS__FED_CONGRESS_LEGISLATORS, POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES.CAND_ID = FINANCE__FED_FEC_CAND_CMTE_LINKAGE.CAND_ID [1925] |
| 88 | not started | Are the same people also treasurers of federal campaign committees? | POLITICS__IRS527_DIRECTORS_OFFICERS, FINANCE__FED_FEC_COMMITTEES | none |
| 89 | not started | Do the same people wine and dine state lawmakers and donate federally? | POLITICS__TX_LOBBY_COVER, POLITICS__CA_LOBBY_COVER, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | none |
| A36 | not started | Do the industries caught defrauding Medicare fund the committees that oversee Medicare? | FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE, POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | none |

### PROCUREMENT+RAW, 3 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 15 | found something | Are banned companies still getting paid on disaster relief contracts? | PROCUREMENT__FED_SAM_EXCLUSIONS, FED_USASPENDING_CONTRACTS_FULL_R2 | none |
| E49 | found something | Did they win government contracts specifically during their ban? | PROCUREMENT__FED_SAM_EXCLUSIONS, FED_USASPENDING_CONTRACTS_FULL_R2 | none |
| E66 | nothing there | Are they still getting health grants? | PROCUREMENT__FED_SAM_EXCLUSIONS, FED_USASPENDING_ASSISTANCE_FULL | none |

### ECONOMICS+RAW, 3 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 80 | not started | Do they still keep winning government contracts? | ECONOMICS__FED_FAC_SINGLE_AUDIT, FED_USASPENDING_CONTRACTS_FULL_R2 | none |
| E64 | found a little | Does the money keep flowing to them anyway? | ECONOMICS__FED_FAC_SINGLE_AUDIT, FED_USASPENDING_ASSISTANCE_FULL | none |
| E65 | nothing there | Were they still getting paid after losing it? | ECONOMICS__FED_IRS_REVOCATION, FED_USASPENDING_ASSISTANCE_FULL | none |

### FINANCE+RAW, 3 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 87 | not started | Do they also personally donate to U.S. political campaigns? | FED_FARA_BULK, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | none |
| 91 | not started | Do they buy a stock, then introduce a bill that helps it? | FINANCE__FED_SENATE_STOCK_WATCHER, FED_GOVINFO_BILLSTATUS, FED_GOVINFO_BILL_COSPONSORS | none |
| 92 | not started | Does office spending go to vendors who are also campaign donors? | FED_HOUSE_DISBURSEMENTS, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | none |

### JUSTICE+RAW, 3 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 136 | not started | Do the ones with the most known security flaws still win contracts? | JUSTICE__FED_CISA_KEV, FED_USASPENDING_CONTRACTS_FULL_R2 | none |
| 137 | not started | Are any of them showing up at U.S. ports anyway? | JUSTICE__FED_OFAC_SDN, FED_NOAA_AIS | none |
| 138 | not started | Do the ones involved in the most killings still get the most federal grant money? | JUSTICE__XC_MAPPING_POLICE_VIOLENCE, FED_USASPENDING_ASSISTANCE_FULL | none |

### ECONOMICS+HEALTH, 2 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 21 | part done | Do hospital employees get paid less than the local average wage? | HEALTH__FED_CMS_HCRIS, ECONOMICS__FED_BLS_QCEW | none |
| 117 | not started | Did the same ones get hit with health and safety fines? | ECONOMICS__FED_SBA_PPP, HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS, HEALTH__FED_CMS_NURSING_HOME_PENALTIES | none |

### JUSTICE, 2 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 77 | not started | Do they own stock in companies whose cases they're deciding? | JUSTICE__FED_COURTLISTENER_INVESTMENTS, JUSTICE__FED_COURTLISTENER_POSITIONS, JUSTICE__FED_FJC_IDB_CIVIL | none |
| 95 | not started | Do gifts or debts they report ever involve parties in their own courtroom? | JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS, JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS, JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS | JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS.FINANCIAL_DISCLOSURE_ID = JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS.FINANCIAL_DISCLOSURE_ID [520] ; JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS.FINANCIAL_DISCLOSURE_ID = JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS.FINANCIAL_DISCLOSURE_ID [520] ; JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS.FINANCIAL_DISCLOSURE_ID = JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS.FINANCIAL_DISCLOSURE_ID [3247] ; JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS.FINANCIAL_DISCLOSURE_ID = JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS.FINANCIAL_DISCLOSURE_ID [770] |

### ECONOMICS+FINANCE, 2 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 79 | not started | Did they quietly switch auditors right before collapsing? | ECONOMICS__FED_FDIC_FAILED_BANKS, FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS, FINANCE__FED_PCAOB_FORM_AP_FILINGS | none |
| 128 | part done | Were failed banks still active members right up until they collapsed? | FINANCE__FED_FHFA_FHLB_MEMBERSHIP, ECONOMICS__FED_FDIC_FAILED_BANKS | none |

### FINANCE+HEALTH, 2 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 85 | not started | Does it flow from their corporate PAC into top leaders' campaign funds? | HEALTH__FED_CMS_OPEN_PAYMENTS, FINANCE__FED_FEC_COMMITTEES, FINANCE__FED_FEC_LEADERSHIP_PAC | none |
| A33 | not started | Do the worst-fined chains also run a political action committee? | HEALTH__FED_NURSINGHOME411, FINANCE__FED_FEC_COMMITTEES | none |

### ENVIRONMENT, 2 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 102 | not started | Do they also have the worst drinking water problems? | ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS, ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS, ENVIRONMENT__FED_FRACFOCUS_REGISTRY, ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | none |
| E33 | found a little | Do they violate pollution rules more right after a storm? | ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY, ENVIRONMENT__FED_NOAA_STORM_EVENTS | none |

### TRANSPORT, 2 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 104 | not started | Do the same addresses show up behind multiple fatal crashes? | TRANSPORT__FED_NTSB_AVIATION_EVENTS, TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT, TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY | TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT.EV_ID = TRANSPORT__FED_NTSB_AVIATION_EVENTS.EV_ID [30968] ; TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT.NTSB_NO = TRANSPORT__FED_NTSB_AVIATION_EVENTS.NTSB_NO [30438] ; TRANSPORT__FED_NTSB_AVIATION_EVENTS.EV_ID = TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT.EV_ID [30968] ; TRANSPORT__FED_NTSB_AVIATION_EVENTS.NTSB_NO = TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT.NTSB_NO [30438] |
| 105 | not started | Do the same crossings get hit by trains again and again? | TRANSPORT__FED_FRA_CROSSING_INCIDENTS, TRANSPORT__FED_FRA_CASUALTIES | TRANSPORT__FED_FRA_CASUALTIES.INCIDENT_NUMBER = TRANSPORT__FED_FRA_CROSSING_INCIDENTS.INCIDENT_NUMBER [98233] ; TRANSPORT__FED_FRA_CROSSING_INCIDENTS.INCIDENT_NUMBER = TRANSPORT__FED_FRA_CASUALTIES.INCIDENT_NUMBER [98233] |

### ENVIRONMENT+RAW, 2 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 142 | not started | Do some have pollution spikes that never trigger a violation? | FED_EPA_CAMPD_EMISSIONS_DAILY, ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY, ENVIRONMENT__FED_EPA_AQS_SITES | none |
| E53 | nothing there | Do they get penalized less often than other neighborhoods? | ENVIRONMENT__FED_EPA_ECHO, DIM_TRACT | none |

### HEALTH+HOUSING, 2 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| E36 | nothing there | Does overdose death rise after a disaster? | HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS, HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | none |
| E50 | nothing there | Do new health care businesses pop up right after, chasing relief money? | HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS, HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | none |

### HEALTH+IMMIGRATION, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 1 | part done | Are doctors banned from Medicare still showing up on hospice paperwork? | HEALTH__FED_HHS_OIG_LEIE, HEALTH__FED_CMS_FACILITY_AFFILIATION, IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS, HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | HEALTH__FED_HHS_OIG_LEIE.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [15] |

### ENVIRONMENT+FINANCE, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 17 | missing a piece | Same as #3 but through a different bank record | FINANCE__FED_FDIC_BANK_DATA, ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | none |

### FINANCE+LABOR, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 82 | not started | Do unions reporting missing money also have an active political fund? | LABOR__FED_DOL_OLMS, FINANCE__FED_FEC_COMMITTEES | none |

### EDUCATION+REGULATORY, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 83 | not started | Does lobbying spending spike right before a new safety rule is finalized? | EDUCATION__FED_SENATE_LDA_FILINGS, REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS | none |

### EDUCATION+POLITICS, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 86 | not started | Are big-spending political advertisers avoiding official campaign finance reporting? | EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND, POLITICS__FED_FEC_PAC_SUMMARY, POLITICS__FED_MEDSL_HOUSE_RETURNS | none |

### GOVERNANCE+RAW, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 90 | not started | Do agency contracts shift toward an official's old industry after they arrive? | GOVERNANCE__FED_REVOLVINGDOOR_PROJECT, FED_USASPENDING_CONTRACTS_FULL_R2 | none |

### JUSTICE+POLITICS, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 93 | not started | Do places with more rejected mail ballots overlap with high-incarceration areas? | POLITICS__FED_EAC_EAVS, JUSTICE__XC_VERA_INCARCERATION_TRENDS, POLITICS__FED_MEDSL_HOUSE_RETURNS | none |

### FINANCE+JUSTICE, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 94 | not started | Does a judge's political leaning or donations predict how they rule? | JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS, FINANCE__FED_FEC_INDIV_CONTRIBUTIONS, JUSTICE__FED_FJC_IDB_CIVIL | none |

### ENVIRONMENT+LABOR, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 99 | not started | Do the ones with unsafe dams also have a pile of unpaid safety fines? | LABOR__FED_MSHA_MINES, ENVIRONMENT__FED_NID_DAMS, LABOR__FED_MSHA_VIOLATIONS | LABOR__FED_MSHA_MINES.MINE_ID = LABOR__FED_MSHA_VIOLATIONS.MINE_ID [31277] ; LABOR__FED_MSHA_VIOLATIONS.MINE_ID = LABOR__FED_MSHA_MINES.MINE_ID [31277] |

### HOUSING+RAW, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 100 | not started | Did they spring up right after the disaster was declared? | FED_USASPENDING_CONTRACTS_FULL_R2, HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | none |

### LEGAL_ENFORCEMENT+RAW, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 107 | not started | Did the biggest distributors in a state match who actually got sued? | FED_DEA_ARCOS_FULL, LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS | none |

### SCIENCE_RESEARCH, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 112 | not started | Do the ones with more retracted (fake or flawed) studies keep getting funded? | SCIENCE_RESEARCH__FED_NIH_REPORTER, SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS, SCIENCE_RESEARCH__FED_RETRACTION_WATCH | none |

### ECONOMICS+LABOR, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 114 | not started | Are they going uninspected for years at a time? | LABOR__FED_OSHA_ITA_300A_SUMMARY_2024, ECONOMICS__FED_DOL_OSHA_INSPECTIONS, ECONOMICS__FED_BLS_QCEW | none |

### LABOR, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 115 | not started | Do accidents happen at their mines afterward? | LABOR__FED_MSHA_VIOLATIONS, LABOR__FED_MSHA_ACCIDENTS | LABOR__FED_MSHA_ACCIDENTS.CONTROLLER_ID = LABOR__FED_MSHA_VIOLATIONS.CONTROLLER_ID [6565] ; LABOR__FED_MSHA_ACCIDENTS.MINE_ID = LABOR__FED_MSHA_VIOLATIONS.MINE_ID [13338] ; LABOR__FED_MSHA_VIOLATIONS.CONTROLLER_ID = LABOR__FED_MSHA_ACCIDENTS.CONTROLLER_ID [6565] ; LABOR__FED_MSHA_VIOLATIONS.MINE_ID = LABOR__FED_MSHA_ACCIDENTS.MINE_ID [13338] |

### IMMIGRATION+RAW, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 119 | not started | How much do they get paid per day, per detained person? | IMMIGRATION__FED_ICE_DETENTION_STINTS, IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES, FED_USASPENDING_CONTRACTS_FULL_R2 | none |

### IMMIGRATION+JUSTICE, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 120 | not started | Do they also have high jail populations generally? | IMMIGRATION__FED_ICE_DETAINERS, JUSTICE__XC_VERA_INCARCERATION_TRENDS | none |

### CORPORATE_REGISTRY+JUSTICE, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 122 | not started | Are any of them under U.S. or international sanctions? | CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC, JUSTICE__INTL_OPENSANCTIONS_DEFAULT, JUSTICE__FED_OFAC_SDN | none |

### ECONOMICS+POLITICS, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 125 | not started | Are they still operating and filing paperwork as if nothing happened? | POLITICS__IRS527_8871_ORGS, ECONOMICS__FED_IRS_AUTO_REVOCATIONS, POLITICS__IRS527_8872_REPORTS | POLITICS__IRS527_8871_ORGS.FORM_ID_NUMBER = POLITICS__IRS527_8872_REPORTS.FORM_ID_NUMBER [243] ; POLITICS__IRS527_8872_REPORTS.FORM_ID_NUMBER = POLITICS__IRS527_8871_ORGS.FORM_ID_NUMBER [243] |

### CONSUMER_PROTECTION+HOUSING, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 126 | not started | Do consumer complaints about them pile up before regulators catch on? | CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS, HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF | none |

### FINANCE+HOUSING, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 127 | not started | Are banks pulling branches out of those neighborhoods over time? | FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS, HOUSING__FED_MAPPING_INEQUALITY | none |

### CONSUMER_SAFETY, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 129 | not started | Do complaints pile up for years before an official recall happens? | CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS, CONSUMER_SAFETY__FED_NHTSA_RECALLS | none |

### HOUSING+JUSTICE, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 132 | not started | Do bankruptcy filings spike in the year after? | JUSTICE__FED_FJC_IDB_BANKRUPTCY, HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | none |

### ENERGY+ENVIRONMENT, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 141 | not started | Do the ones with the worst storm outages also charge the highest rates? | ENERGY__FED_EIA861_RELIABILITY, ENERGY__FED_EIA861_SERVICE_TERRITORY, ENVIRONMENT__FED_NOAA_STORM_EVENTS, ENERGY__FED_EIA861_SALES_ULT_CUST | none |

### IMMIGRATION, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| 144 | part done | Do outcomes vary a lot by judge and detention facility? | IMMIGRATION__FED_EOIR_CASES | none |

### POLITICS+RAW, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| A35 | not started | Do members trade stock in industries their committee oversees? | FED_HOUSE_FD_PTR_INDEX, POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | none |

### ECONOMICS+ENVIRONMENT, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| E54 | nothing there | Do they pay workers less than clean factories? | ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY, ECONOMICS__FED_BLS_QCEW | none |

### HEALTH+PROCUREMENT, 1 questions

| id | status | question | tables | measured join |
|---|---|---|---|---|
| E73 | found something | Do banned contractors turn out to also be doctors? | PROCUREMENT__FED_SAM_EXCLUSIONS, HEALTH__FED_CMS_NPPES | none |
