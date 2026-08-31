# The widened time census - 2026-08-20

The count sweep asked one question of every clocked table: how many rows
per period. These four ask what counting cannot answer.

| shape | tables pulled | scored | errors |
|---|---:|---:|---:|
| reporting lag | 83 | 70 | 0 |
| spans | 70 | 56 | 0 |
| category mix | 309 | 687 | 0 |
| entity cohorts | 329 | 142 | 0 |

## How the two censoring traps were handled

Raw lag and raw duration ALWAYS appear to shrink toward the present, in
every dataset, whether or not anything changed: an old record has had
years in which to be reported or to run long, and a recent one has not.
Nothing here is ranked on a raw median. Everything is ranked on a fixed
horizon -- share reported within a year, share closed within a year --
asked only of cohorts old enough to answer it. Birth curves drop their
first year and death curves drop their last, for the same reason.

## 1. Reporting lag -- the gap between happening and being told

**13 tables have the downstream clock landing BEFORE the event clock.**
Being told about something before it happens is impossible, so each of
these is one of two things: a parse fault, or -- more often -- two columns
that are not a report-of-an-event pair at all. The aircraft registry
compares year-of-manufacture against last-registry-action; the water
enforcement tables compare last-inspection against last-formal-action.
Neither is a reporting gap. Either way the clock labels need revisiting,
which is a finding about the index rather than about the world.

| table | happened clock | downstream clock | rows | share impossible |
|---|---|---|---|---|
| ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP | DATE_LAST_INSPECTION | DATE_LAST_FORMAL_ACTION | 52494 | 0.697 |
| TRANSPORT.TRANSPORT__FED_FAA_REGISTRY | YEAR_MFR | LAST_ACTION_DATE | 246006 | 0.681 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO | DATE_LAST_INSPECTION | DATE_LAST_FORMAL_ACTION | 565447 | 0.661 |
| SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS | AWARD_YEAR | SOLICITATION_YEAR | 219503 | 0.526 |
| HEALTH.HEALTH__FED_CMS_POS_OTHER | CHOW_DT | CRTFCTN_DT | 4757 | 0.5 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES | FACILITY_DEACTIVATION_DATE | FIRST_REPORTED_DATE | 570319 | 0.422 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | ACTION_DATE | SOLICITATION_DATE | 20000000 | 0.256 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_EVENTS_MILESTONES | EVENT_ACTUAL_DATE | FIRST_REPORTED_DATE | 394075 | 0.254 |
| JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL | PROCEEDING_DATE | FILE_DATE | 6299908 | 0.148 |
| POLITICS.POLITICS__CA_LOBBY_CHG_LOG | EFFECT_DT | LOG_DT | 74491 | 0.084 |
| FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE | CAND_ELECTION_YR | FEC_ELECTION_YR | 30530 | 0.054 |
| FINANCE.FINANCE__FED_FEC_LEADERSHIP_PAC | CAND_ELECTION_YR | FEC_ELECTION_YR | 8618 | 0.033 |
| SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | FISCAL_YEAR | DATE_ADDED | 2122611 | 0.024 |

**15 tables leave the downstream clock empty for most rows** -- the field
exists but is blank, so the gap is unmeasurable there.

| table | downstream clock | rows | share never reported |
|---|---|---|---|
| HEALTH.HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION | PUBLISHDATE | 2040 | 1.0 |
| JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS | DATE_NOMINATED | 1728 | 1.0 |
| HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | DATA_AS_OF | 113142 | 1.0 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | SUBMISSIONYEARQUARTER | 4164749 | 1.0 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | INITIAL_REPORT_DATE | 19902879 | 1.0 |
| JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS | DATE_FILED | 236171 | 0.95 |
| HEALTH.HEALTH__FED_FDA_FAERS_DEMO | FDA_DT | 4778271 | 0.848 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO | DATE_LAST_FORMAL_ACTION | 565447 | 0.805 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES | FIRST_REPORTED_DATE | 570319 | 0.755 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_SE_VIOLATIONS | RNC_DETECTION_DATE | 305478 | 0.746 |

**28 tables are retroactive archives** -- the oldest records were entered
long after the fact, so their early years describe when someone typed the
history in, not when anything happened.

| table | rows | earliest gap | recent gap | unit |
|---|---|---|---|---|
| JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL | 6299908 | 26228.0 | 0.0 | days |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS | 2495234 | 36166.0 | 105.945 | days |
| HEALTH.HEALTH__FED_FDA_MAUDE | 2379083 | 43751.5 | -1162.0 | days |
| SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | 2122611 | 10.0 | 0.0 | years |
| CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS | 2117711 | 38622.062 | 10.022 | days |
| FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION | 1772065 | 11694.0 | 2.0 | days |
| HEALTH.HEALTH__FED_HRSA_NPDB | 1640256 | 110.0 | 15.0 | years |
| JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL | 813782 | 23608.0 | -129.905 | days |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES | 570319 | 38340.0 | -3851.844 | days |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO | 565447 | 19269.0 | -2721.308 | days |

**2 tables show a real change in how promptly things get reported**,
measured like-for-like. This is the collection signal the count sweep
could never separate out.

| table | rows | reported within a year (early) | (recent) | years compared | tail waited out |
|---|---|---|---|---|---|
| HEALTH.HEALTH__FED_FDA_FAERS_DEMO | 4778271 | 0.0 | 0.9 | 24 | 4 |
| JUSTICE.JUSTICE__INTL_UCDP_GED | 385918 | 0.604 | 0.965 | 34 | 2 |

## 2. Spans -- what was live at once, and for how long

**12 tables contain spans that END BEFORE THEY START.**

| table | start | end | rows | share backwards |
|---|---|---|---|---|
| ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | PERIOD_OF_PERFORMANCE_START_DATE | PERIOD_OF_PERFORMANCE_CURRENT_END_DATE | 19999869 | 0.015 |
| POLITICS.POLITICS__TX_LOBBY_COVER | APPLICABLE_YEAR | DUE_DT | 283803 | 0.007 |
| HEALTH.HEALTH__FED_CMS_POS_OTHER | ACRDTN_EFCTV_DT | TRMNTN_EXPRTN_DT | 7947 | 0.006 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | COMPL_PER_BEGIN_DATE | NON_COMPL_PER_END_DATE | 14430187 | 0.004 |
| ENVIRONMENT.ENVIRONMENT__FED_USGS_MINERALS | YR_FST_PRD | YR_LST_PRD | 15953 | 0.002 |
| CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS | BEGIN_MANUFACTURE_DATE | END_MANUFACTURE_DATE | 81500 | 0.002 |
| JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS | DATE_START | DATE_TERMINATION | 50420 | 0.001 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC | COMPL_PER_BEGIN_DATE | NON_COMPL_PER_END_DATE | 387627 | 0.001 |
| POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION | APPLICABLEYEAR | PERIODENDDT | 3697 | 0.001 |
| FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS | EXCERCISE_DATE | EXPIRATION_DATE | 229060 | 0.001 |

**28 tables are dominated by ONE exact duration** -- a standard term (a
30-day window, a 3-year permit), not a measured lifetime. An average
length computed on these measures the form, not the world.

| table | rows | the one duration | unit | share on it |
|---|---|---|---|---|
| JUSTICE.JUSTICE__INTL_UCDP_GED | 385918 | 0.0 | days | 1.0 |
| EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS | 174871 | 0.0 | years | 1.0 |
| POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE | 14452 | 30.0 | days | 1.0 |
| POLITICS.POLITICS__CA_LOBBY_EMPLOYER | 1730 | 1.0 | years | 1.0 |
| ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | 1780730 | 0.0 | days | 1.0 |
| POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION | 3697 | 0.0 | years | 0.999 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS | 983896 | 0.0 | days | 0.999 |
| POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING | 38661 | 30.0 | days | 0.997 |
| FINANCE.FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS | 260480 | 0.0 | days | 0.995 |
| IMMIGRATION.IMMIGRATION__FED_DOL_OFLC | 664616 | 1095.0 | days | 0.914 |
| POLITICS.POLITICS__TX_LOBBY_GIFTS | 4084 | 30.0 | days | 0.884 |
| POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS | 6505 | 91.0 | days | 0.867 |

**10 tables never record an end for most rows.** Their live-at-once curve
can only ever rise, so it is not a population trend.

| table | end clock | rows | share with no end |
|---|---|---|---|
| ECONOMICS.ECONOMICS__FED_DOL_FORM5500 | PLAN_YEAR_END_DATE | 33484 | 1.0 |
| REFERENCE.REFERENCE__FED_USGS_GNIS_ALL_NAMES | ENDING_DATE | 1122278 | 1.0 |
| JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS | DATE_END | 4117 | 0.985 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | REDUCED_MONITORING_END_DATE | 18734 | 0.963 |
| EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS | TERMINATION_DATE | 174871 | 0.955 |
| PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS | TERMINATION_DATE | 156912 | 0.943 |
| ENVIRONMENT.ENVIRONMENT__FED_USGS_MINERALS | YR_LST_PRD | 15953 | 0.726 |
| JUSTICE.JUSTICE__FED_CONSOLIDATED_SCREENING_LIST | END_DATE | 5094 | 0.696 |
| CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS | END_DATE | 703997 | 0.672 |
| HEALTH.HEALTH__FED_CMS_POS_OTHER | TRMNTN_EXPRTN_DT | 7947 | 0.602 |

**15 tables have a trustworthy live-at-once curve that MOVED.**

| table | rows | peak year | peak live | what moved |
|---|---|---|---|---|
| FINANCE.FINANCE__FED_NCUA_CALL_REPORTS_FOICU | 4336 | 2025 | 4336 | 55% share one exact duration (20175 days) -- a standard term, not a measured lifetime; how many were live at once grew from 87 to 4,335 |
| JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS | 50420 | 1942 | 2727 | 0.13% end before they start -- impossible; how many were live at once grew from 143 to 2,543 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES | 927415 | 2002 | 58888 | how many were live at once shrank from 43,516 to 8 |
| SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | 1993071 | 2010 | 191423 | 59% share one exact duration (364 days) -- a standard term, not a measured lifetime; how many were live at once grew from 12 to 575 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS | 6325621 | 2025 | 5175953 | share closing within a year rose from 3% to 99%; 63% share one exact duration (7 days) -- a standard term, not a measured lifetime; how many were live at once shrank from 671 to 10 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | 11189048 | 2013 | 3867573 | share closing within a year rose from 0% to 77%; how many were live at once grew from 8,964 to 347,317 |
| HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS | 24309 | 2026 | 24010 | share closing within a year rose from 0% to 38%; 60% share one exact duration (7304 days) -- a standard term, not a measured lifetime; how many were live at once shrank from 24 to 3 |
| POLITICS.POLITICS__CA_LOBBY_COVER | 524749 | 2024 | 28252 | how many were live at once grew from 19 to 155 |
| JUSTICE.JUSTICE__INTL_UCDP_GED | 385918 | 2024 | 28816 | how many were live at once grew from 3,363 to 25,359 |
| POLITICS.POLITICS__TX_LOBBY_AWARDS | 1589 | 2015 | 176 | 77% share one exact duration (30 days) -- a standard term, not a measured lifetime; how many were live at once shrank from 100 to 16 |
| POLITICS.POLITICS__TX_LOBBY_GIFTS | 4084 | 2011 | 816 | 88% share one exact duration (30 days) -- a standard term, not a measured lifetime; how many were live at once shrank from 208 to 37 |
| CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS | 81500 | 2013 | 23845 | 0.18% end before they start -- impossible; share closing within a year rose from 0% to 85%; how many were live at once shrank from 21,565 to 4,660 |

## 3. Category mix -- the make-up changing, not the amount

**687 table/column pairs measured; 476 shift on solid ground** (the field
existed throughout, it is not a lifecycle status that reads as of today,
and both ends carry real volume).

| table | column | rows | was mostly | share | now mostly | share | shift |
|---|---|---|---|---|---|---|---|
| ENVIRONMENT.ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS | STATE | 117672 | Missouri | 0.562 | Ohio | 0.189 | 1.0 |
| ENVIRONMENT.ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS | SOURCE | 117672 | Missouri Department of Natural Resources | 0.562 | Ohio Department of Natural Resources | 0.189 | 1.0 |
| ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT | DATA_SOURCE | 411638 | CENSUS | 1.0 | GSAFAC | 1.0 | 1.0 |
| ECONOMICS.ECONOMICS__FED_TREASURY_DTS_DEPOSITS | ACCOUNT_TYPE | 478149 | Federal Reserve Account | 0.945 | Treasury General Account (TGA) | 0.989 | 1.0 |
| ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS | SOURCE | 1029020 | UNAVAILABLE | 1.0 | TELEPHONE | 0.971 | 1.0 |
| ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | DATA_SOURCE | 1780730 | PDC | 1.0 | CSV | 1.0 | 1.0 |
| FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | INSURANCE_AGENCY | 2823000 | BIF | 0.84 | DIF | 1.0 | 1.0 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | ACTION_DATE_FISCAL_YEAR | 19902879 | 2007 | 0.5 | 2025 | 0.333 | 1.0 |
| JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS | SOURCE | 236171 | 20 | 0.947 | 3 | 0.571 | 1.0 |
| TRANSPORT.TRANSPORT__FED_FRA_CROSSING_INCIDENTS | RAILROAD_TYPE | 251139 | 1L | 0.943 | 1 | 0.479 | 0.99 |
| TRANSPORT.TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | CLASS | 224940 | 1L | 0.927 | 1 | 0.44 | 0.981 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS | AGENCY | 472507 | EPA | 0.991 | State | 0.99 | 0.981 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | TYPE_OF_IDC | 20000000 | NAN | 0.975 | INDEFINITE DELIVERY / INDEFINITE QUANTITY | 0.833 | 0.975 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS | STATE_EPA_FLAG | 983896 | E | 0.986 | S | 0.972 | 0.957 |
| HEALTH.HEALTH__FED_CDC_SUICIDE_RATES | FLAG | 6390 | ... | 0.948 | * | 1.0 | 0.948 |
| PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS | EXCLUSION_PROGRAM | 156912 | NonProcurement | 0.94 | Reciprocal | 1.0 | 0.94 |
| PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS | EXCLUDING_AGENCY | 156912 | HHS | 0.913 | OFAC | 0.542 | 0.935 |
| JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST | DESIGNATION_SOURCE | 33828 | UN | 1.0 | UK | 0.921 | 0.929 |
| JUSTICE.JUSTICE__FED_CISA_KEV | REQUIRED_ACTION | 1631 | Apply updates per vendor instructions. | 0.848 | Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable. | 0.555 | 0.927 |
| HEALTH.HEALTH__FED_FDA_DEVICE_510K | STATE | 175686 | IL | 0.899 | CA | 0.271 | 0.925 |
| HEALTH.HEALTH__FED_CMS_HOME_HEALTH | TYPE_OF_OWNERSHIP | 12391 | PROPRIETARY | 0.452 | - | 0.923 | 0.923 |
| JUSTICE.JUSTICE__XC_WAPO_FATAL_FORCE | RACE_SOURCE | 10430 | not_available | 0.985 | photo | 0.443 | 0.921 |
| HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 | PREVIOUS_52_WEEKS_MAX_FLAG | 1932840 | - | 0.887 | NC | 1.0 | 0.887 |
| IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS | CASE_THREAT_LEVEL | 2571974 | 1 | 0.809 | NA | 1.0 | 0.875 |
| HEALTH.HEALTH__FED_FDA_CAERS | REPORT_TYPE | 85511 | Direct | 0.787 | Expedited (15-Day) | 0.874 | 0.874 |

**19 pairs are a field ARRIVING, not a mix changing** -- blank in the early
records because the column did not exist yet. Named so nobody mistakes
them for findings later.

| table | column | rows | blank early | blank now |
|---|---|---|---|---|
| ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | ORGANIZATIONAL_TYPE | 20000000 | 0.899 | 0.007 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | ASSISTANCE_TYPE_DESCRIPTION | 19902879 | 0.999 | 0 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | FUNDING_AGENCY_NAME | 19902879 | 1.0 | 0.002 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | ACTION_TYPE_DESCRIPTION | 19902879 | 1.0 | 0 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | RECORD_TYPE_DESCRIPTION | 19902879 | 1.0 | 0 |
| JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | JURISDICTION | 10323280 | 0.825 | 0 |
| JUSTICE.JUSTICE__FED_FJC_IDB_BANKRUPTCY | ORIGINAL_FEE_STATUS | 6965441 | 0.952 | 0.0 |
| HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | REGISTRATION_METHOD | 3079994 | 0.518 | 0.001 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS | AIR_STACK_TEST_STATUS_DESC | 620291 | 0.9 | 0.009 |
| LABOR.LABOR__FED_DOL_OLMS | AMENDED_FLAG | 617552 | 0.993 | 0.059 |
| LABOR.LABOR__FED_DOL_OLMS | HARDSHIP_FLAG | 617552 | 0.994 | 0.059 |
| TRANSPORT.TRANSPORT__FED_FRA_CROSSING_INCIDENTS | USER_SEX | 251139 | 1.0 | 0.091 |

**25 pairs are dated by when the thing came into existence.** Their early
years are a survivor list, not a census of what was built then.

| table | column | rows | was mostly | now mostly |
|---|---|---|---|---|
| CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO | COMPANY_TYPE | 805501 | External company | LTD - Private Company Limited by Shares |
| HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | ORGANIZATION_TYPE_STRUCTURE | 8989 | CORPORATION | LLC |
| CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO | COMPANY_STATUS | 805501 | Ceased | Normal |
| ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR | ENERGY_SOURCE_1 | 26854 | WAT | SUN |
| CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES | SOURCE_LEAK | 788448 | Paradise Papers - Bahamas corporate registry | Paradise Papers - Malta corporate registry |
| HEALTH.HEALTH__FED_CDC_DATA_PORTAL | DOMAIN_CATEGORY | 1471 | Motor Vehicle | National Institute for Occupational Safety and Health |
| HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | INCORPORATION_STATE | 8989 | ND | DE |
| HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS | INCORPORATION_STATE | 9211 | DE | CA |
| HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | STATE | 8989 | IN | FL |
| HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | ENROLLMENT_STATE | 8989 | IN | FL |

**19 pairs are lifecycle status columns that flipped.** Treat with
suspicion: a status normally reads as of today, so 'old ones are closed
and new ones are open' is a tautology rather than a change.

| table | column | rows | was mostly | now mostly |
|---|---|---|---|---|
| HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT | STATUS | 39635 | Terminated | Ongoing |
| POLITICS.POLITICS__FED_FCC_LICENSING | LICENSE_STATUS | 1667754 | E | A |
| HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES | STATUS | 41252 | Inactive | Active |
| ECONOMICS.ECONOMICS__FED_SBA_LOANS | LOAN_STATUS | 1869773 | P I F | CURR |
| CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO | COMPANY_STATUS | 805501 | Ceased | Normal |
| POLITICS.POLITICS__FEC_CANDIDATE | CAND_STATUS | 17891 | P | N |
| ENVIRONMENT.ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS | STATUS | 117672 | Abandoned | Orphan |
| HEALTH.HEALTH__FED_FDA_DRUG_ENFORCEMENT | STATUS | 17816 | Terminated | Ongoing |
| HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS | HPSA_STATUS | 165531 | Withdrawn | Designated |
| JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL | FUGITIVE_STATUS | 6299908 | Z | N |

## 4. Entity cohorts -- things arriving and leaving

**45 tables have entities appearing in one year only**, for more than 70%
of the population. Either the churn is real or the identifier is not
stable across years -- and from inside one table those look identical.

| table | entity column | rows | entities | one-year-only |
|---|---|---|---|---|
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | ENFORCEMENT_ID | 15432737 | 649479 | 0.836 |
| JUSTICE.JUSTICE__FED_FJC_IDB_BANKRUPTCY | DOCKET | 6965441 | 674677 | 0.945 |
| JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL | DOCKET | 6299908 | 264765 | 0.891 |
| HEALTH.HEALTH__FED_FDA_FAERS_DEMO | MFR_NUM | 5811086 | 679830 | 0.995 |
| CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS | NODE_ID_END | 3339267 | 237431 | 0.75 |
| HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | DISASTER_NUMBER | 3080000 | 625 | 0.744 |
| HEALTH.HEALTH__FED_FDA_MAUDE | LOT_NUMBER | 2743561 | 480894 | 0.847 |
| FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS | ACCESSION_NUMBER | 2672841 | 1354638 | 0.993 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS | VISIT_ID | 2495249 | 438855 | 0.958 |
| REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS | DOCUMENTATION_ID | 1970107 | 30982 | 0.878 |
| ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | EPISODE_ID | 1780730 | 394383 | 1.0 |
| JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE | DISTRICT_DOCKET | 988183 | 61950 | 0.703 |

**61 tables show a real change in arrivals or departures.**

| table | entity column | entities | median years alive | peak year | peak population | what moved |
|---|---|---|---|---|---|---|
| POLITICS.POLITICS__TX_LOBBY_GIFTS | FILER_ID | 434 | 0 | 2011 | 111 | fewer new arrivals lately: 48/yr -> 4/yr |
| LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS | PLAN_NUMBER | 104 | 8 | 1996 | 50 | fewer new arrivals lately: 6/yr -> 0/yr |
| JUSTICE.JUSTICE__XC_OWID_TERRORISM_DEATHS | ENTITY | 221 | 51 | 2006 | 216 | fewer new arrivals lately: 7/yr -> 1/yr; 87% of all entities are 'born' in the first year -- that is the data starting, not the world |
| REFERENCE.REFERENCE__XC_OWID_FERTILITY | ENTITY | 261 | 73 | 1950 | 259 | more new arrivals lately: 1/yr -> 82/yr |
| HEALTH.HEALTH__XC_OWID_LIFE_EXPECTANCY | ENTITY | 265 | 73 | 1950 | 261 | more new arrivals lately: 2/yr -> 57/yr |
| POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING | FILER_ID | 2079 | 2 | 2013 | 528 | more last-sightings lately: 7/yr -> 132/yr |
| HEALTH.HEALTH__FED_FDA_DEVICE_PMA | PMA_NUMBER | 1743 | 8 | 2021 | 695 | more new arrivals lately: 1/yr -> 21/yr; more last-sightings lately: 1/yr -> 119/yr |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_CS_VIOLATIONS | NPDES_ID | 8590 | 0 | 2020 | 1532 | more new arrivals lately: 2/yr -> 238/yr; more last-sightings lately: 1/yr -> 519/yr |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS | PGM_SYS_ID | 37365 | 0 | 2009 | 7495 | more new arrivals lately: 38/yr -> 612/yr; more last-sightings lately: 2/yr -> 1,545/yr |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS | NPDES_ID | 49312 | 0 | 2011 | 8684 | more new arrivals lately: 5/yr -> 1,206/yr |
| POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META | BILL_NUMBER | 16221 | 0 | 2003 | 3184 | more new arrivals lately: 11/yr -> 164/yr |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS | PGM_SYS_ID | 60544 | 0 | 2005 | 14406 | more new arrivals lately: 31/yr -> 208/yr; more last-sightings lately: 2/yr -> 1,836/yr |
| HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES | CMS_CERTIFICATION_NUMBER_CCN | 13914 | 2 | 2024 | 12091 | more last-sightings lately: 6/yr -> 3,643/yr |
| POLITICS.POLITICS__TX_LOBBY_SUBJECT_MATTER | FILER_ID | 2344 | 1 | 2015 | 607 | more last-sightings lately: 3/yr -> 145/yr |
| SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS | UEI | 17161 | 2 | 2020 | 5815 | more new arrivals lately: 48/yr -> 719/yr; more last-sightings lately: 2/yr -> 2,386/yr |
| TRANSPORT.TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | STATION | 23077 | 1 | 1980 | 8419 | fewer new arrivals lately: 2,331/yr -> 38/yr |
| POLITICS.POLITICS__TX_LOBBY_COVER | FILER_NAME | 12234 | 2 | 2015 | 2815 | more last-sightings lately: 1/yr -> 282/yr |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_SE_VIOLATIONS | NPDES_ID | 76438 | 0 | 2021 | 20363 | more new arrivals lately: 56/yr -> 3,441/yr; more last-sightings lately: 1/yr -> 7,908/yr |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS | ID_NUMBER | 136842 | 0 | 2004 | 25830 | more new arrivals lately: 2/yr -> 1,577/yr |
| JUSTICE.JUSTICE__INTL_UCDP_GED | COUNTRY_ID | 124 | 31 | 1999 | 92 | fewer new arrivals lately: 11/yr -> 0/yr; more last-sightings lately: 1/yr -> 9/yr |

**63 tables carry a population that persists across years** -- these are the
ones where 'events per living entity' is computable inside a single table,
with no second source needed.

| table | entity column | rows | entities | rows each | median years alive |
|---|---|---|---|---|---|
| ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX | EIN | 5544626 | 899097 | 6.17 | 5 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | RECIPIENT_UEI | 20000000 | 420990 | 47.51 | 2 |
| ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | RECIPIENT_UEI | 19902879 | 223721 | 88.96 | 2 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS | REGISTRY_ID | 10411826 | 162513 | 64.07 | 8 |
| HEALTH.HEALTH__FED_DEA_ARCOS | BUYER_DEA_NO | 178598026 | 148587 | 1201.98 | 4 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_VIOSNC_HISTORY | ID_NUMBER | 2675581 | 146181 | 18.3 | 1 |
| ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT | AUDITEE_EIN | 411638 | 68128 | 6.04 | 7 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS | PGM_SYS_ID | 620302 | 34839 | 17.8 | 3 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS | NPDES_ID | 397615 | 33842 | 11.75 | 1 |
| LABOR.LABOR__FED_MSHA_VIOLATIONS | MINE_ID | 3087265 | 31277 | 98.71 | 7 |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS | PGM_SYS_ID | 499113 | 24075 | 20.73 | 13 |
| TRANSPORT.TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | STATION | 224941 | 23077 | 9.75 | 1 |
| SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS | UEI | 219503 | 17161 | 12.79 | 2 |
| FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS | CIK | 336124 | 16310 | 20.61 | 4 |
| FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | RSSD_ID | 2823000 | 15544 | 181.61 | 13 |
| HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | CMS_CERTIFICATION_NUMBER_CCN | 418479 | 14632 | 28.6 | 3 |
| HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES | CMS_CERTIFICATION_NUMBER_CCN | 200030 | 13914 | 14.38 | 2 |
| LABOR.LABOR__FED_MSHA_ACCIDENTS | MINE_ID | 273623 | 13489 | 20.28 | 4 |
| POLITICS.POLITICS__CA_LOBBY_COVER | FIRM_ID | 524828 | 13205 | 39.74 | 3 |
| FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | CMTE_ID | 84172112 | 12277 | 6856.08 | 1 |


---

## 5. Events per living entity -- the denominator, for free

The count sweep's closing line was that no trend here is safe without a
denominator, and that getting one meant a second table per series. For
**75 tables that turned out to be wrong**: where the same entity recurs
across years, the population is measurable inside the SAME table. An entity
is present in year Y if it was first seen on or before Y and last seen on
or after Y. Divide the events by that and the question answers itself.

This denominator counts entities VISIBLE IN THIS DATASET, which is a proxy
for the real population, not the population. An entity that never appears
is invisible, so the true count is higher. It answers 'per entity we can
see' -- the honest version, and far better than no denominator.

30 tables were skipped because the count sweep and the cohort sweep picked
different clocks, so numerator and denominator would count different years.

### The rise was really MORE ENTITIES, not more per entity

The raw count climbed, and the per-entity rate did not. These are the cases where a headline number would have been wrong.

| table | entity | events | population x | events x | PER ENTITY x | verdict |
|---|---|---|---|---|---|---|
| REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS | DOCUMENTATION_ID | 1902469 | 7.06 | 5.99 | 0.99 | the rise is MORE ENTITIES, not more per entity |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS | PGM_SYS_ID | 483619 | 9.7 | 8.59 | 0.89 | the rise is MORE ENTITIES, not more per entity |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS | REGISTRY_ID | 472413 | 18.52 | 11.78 | 0.65 | the rise is MORE ENTITIES, not more per entity |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS | ID_NUMBER | 380212 | 5.05 | 3.27 | 0.74 | the rise is MORE ENTITIES, not more per entity |
| FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS | CIK | 302781 | 1.67 | 1.56 | 0.92 | the rise is MORE ENTITIES, not more per entity |
| EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND | ADVERTISER_ID | 260305 | 1.99 | 1.86 | 0.9 | the rise is MORE ENTITIES, not more per entity |
| POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META | BILL_NUMBER | 111688 | 5.94 | 6.82 | 1.18 | the rise is MORE ENTITIES, not more per entity |
| LABOR.LABOR__FED_MSHA_MINES | CURRENT_CONTROLLER_ID | 89813 | 3.8 | 3.65 | 0.95 | the rise is MORE ENTITIES, not more per entity |
| FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE | CAND_ID | 30045 | 4.79 | 3.77 | 0.61 | the rise is MORE ENTITIES, not more per entity |
| ENVIRONMENT.ENVIRONMENT__XC_OWID_CO2 | ENTITY | 7512 | 2.43 | 2.45 | 1.01 | the rise is MORE ENTITIES, not more per entity |
| ENERGY.ENERGY__FED_EIA860_3_3_SOLAR | UTILITY_ID | 6266 | 2.55 | 2.42 | 0.95 | the rise is MORE ENTITIES, not more per entity |

### The fall was really FEWER ENTITIES

The raw count dropped because the population shrank, not because each one is doing less.

| table | entity | events | population x | events x | PER ENTITY x | verdict |
|---|---|---|---|---|---|---|
| TRANSPORT.TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | STATION | 214607 | 0.23 | 0.2 | 0.87 | the fall is FEWER ENTITIES, not fewer per entity |

### A flat total hiding a moving rate

Nothing looked like it was happening. Per entity, it was.

| table | entity | events | population x | events x | PER ENTITY x | verdict |
|---|---|---|---|---|---|---|
| ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | RECIPIENT_UEI | 18000000 | 0.52 | 1.0 | 1.92 | flat total hides a RISING per-entity rate |
| FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | RSSD_ID | 2665583 | 0.4 | 0.96 | 2.4 | flat total hides a RISING per-entity rate |

### A flat total hiding a falling rate

| table | entity | events | population x | events x | PER ENTITY x | verdict |
|---|---|---|---|---|---|---|
| HEALTH.HEALTH__FED_FDA_GUDID | LABELER_DUNS_NUMBER | 4995317 | 3.13 | 0.95 | 0.27 | flat total hides a FALLING per-entity rate |

### The rise SURVIVES the denominator

Both the total and the per-entity rate moved the same way. These are the strongest candidates in the warehouse.

| table | entity | events | population x | events x | PER ENTITY x | verdict |
|---|---|---|---|---|---|---|
| CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | COMPANY | 12680402 | 3.23 | 28.4 | 6.94 | rise survives the denominator |
| EDUCATION.EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS | NUM_OF_DAYS | 1464495 | 1.0 | 1.51 | 1.55 | rise survives the denominator |
| IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS | BOOK_IN_SITE | 1247703 | 0.93 | 5.57 | 6.02 | rise survives the denominator |
| CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF | GROUP_EXEMPTION_NUM | 1237526 | 0.85 | 5.77 | 10.8 | rise survives the denominator |
| CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS | NODE_ID_END | 703517 | 3.55 | 11.83 | 3.08 | rise survives the denominator |
| POLITICS.POLITICS__CA_LOBBY_COVER | FIRM_ID | 524663 | 1.32 | 2.47 | 1.97 | rise survives the denominator |
| HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | CMS_CERTIFICATION_NUMBER_CCN | 384445 | 7.38 | 14.6 | 1.62 | rise survives the denominator |
| POLITICS.POLITICS__TX_LOBBY_COVER | FILER_NAME | 276666 | 1.59 | 3.45 | 1.77 | rise survives the denominator |
| CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS | MFG_RECALL_NUMBER | 238910 | 2.24 | 5.74 | 2.42 | rise survives the denominator |
| REFERENCE.REFERENCE__FED_ITIS_TU_COMMENTS_LINKS | COMMENT_ID | 181636 | 2.77 | 9.67 | 4.08 | rise survives the denominator |
| JUSTICE.JUSTICE__FED_COURTLISTENER_INVESTMENTS | PAGE_NUMBER | 178589 | 2.04 | 21.12 | 10.3 | rise survives the denominator |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS | PGM_SYS_ID | 175398 | 13.4 | 17.24 | 1.43 | rise survives the denominator |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS | NPDES_ID | 107791 | 16.79 | 23.02 | 1.53 | rise survives the denominator |
| CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS | RECALL_NUMBER | 87901 | 0.82 | 8.41 | 7.21 | rise survives the denominator |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_CS_VIOLATIONS | NPDES_ID | 73317 | 3.85 | 5.65 | 1.51 | rise survives the denominator |

### The fall SURVIVES the denominator

| table | entity | events | population x | events x | PER ENTITY x | verdict |
|---|---|---|---|---|---|---|
| ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS | REGISTRY_ID | 8528799 | 0.3 | 0.08 | 0.27 | fall survives the denominator |
| LABOR.LABOR__FED_MSHA_ACCIDENTS | MINE_ID | 252343 | 0.54 | 0.37 | 0.68 | fall survives the denominator |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | ANSI_ENTITY_CODE | 83355 | 0.99 | 0.41 | 0.42 | fall survives the denominator |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_AQS_SITES | SITE_NUMBER | 20328 | 1.1 | 0.13 | 0.12 | fall survives the denominator |
| JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST | DESIGNATION_ID | 18908 | 1.51 | 0.49 | 0.27 | fall survives the denominator |
| HEALTH.HEALTH__FED_FDA_DRUG_ENFORCEMENT | EVENT_ID | 17399 | 1.03 | 0.63 | 0.66 | fall survives the denominator |
| HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS | ASSOCIATE_ID | 7667 | 1.07 | 0.16 | 0.15 | fall survives the denominator |

### Not interpretable: the denominator is itself a coverage ramp

The visible population multiplies by more than twenty, which is a dataset filling in rather than a world of new entities.

| table | entity | events | population x | events x | PER ENTITY x | verdict |
|---|---|---|---|---|---|---|
| JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS | CASE_NAME_SHORT | 9987014 | 469.49 | 8204.28 | 18.25 | denominator is a coverage ramp -- not interpretable |
| JUSTICE.JUSTICE__FED_FJC_IDB_BANKRUPTCY | DOCKET | 6809347 | 214.69 | 421.65 | 1.98 | denominator is a coverage ramp -- not interpretable |
| HEALTH.HEALTH__FED_FDA_FAERS_DEMO | MFR_NUM | 4579779 | 1185.31 | 1202.53 | 0.99 | denominator is a coverage ramp -- not interpretable |
| FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS | ACCESSION_NUMBER | 2672551 | 682.65 | 923.65 | 1.43 | denominator is a coverage ramp -- not interpretable |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS | VISIT_ID | 2472409 | 51.74 | 5.78 | 0.1 | denominator is a coverage ramp -- not interpretable |
| HEALTH.HEALTH__FED_FDA_MAUDE | LOT_NUMBER | 2377323 | 1507.55 | 1313.67 | 0.77 | denominator is a coverage ramp -- not interpretable |
| FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION | ISSUER_CIK | 1713116 | 53.63 | 1753.22 | 34.49 | denominator is a coverage ramp -- not interpretable |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS | ID_NUMBER | 1156576 | 20.16 | 17.49 | 0.92 | denominator is a coverage ramp -- not interpretable |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS | REGISTRY_ID | 953458 | 256.53 | 229.09 | 0.94 | denominator is a coverage ramp -- not interpretable |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS | PGM_SYS_ID | 613065 | 43.26 | 188.83 | 4.25 | denominator is a coverage ramp -- not interpretable |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS | NPDES_ID | 322598 | 40.86 | 77.84 | 1.97 | denominator is a coverage ramp -- not interpretable |
| ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_SE_VIOLATIONS | NPDES_ID | 293913 | 58.55 | 67.7 | 1.21 | denominator is a coverage ramp -- not interpretable |


## What these four sweeps still cannot do

1. **No cross-table comparison.** Every measurement uses one table and its
   own columns. Nothing is joined to anything.
2. **A category is whatever the publisher called it.** A mix flip can be a
   coding change with nothing underneath, and that is not visible from
   inside the column.
3. **Last seen is not dead; no end recorded is not still running.** Both are
   reported as measured, with the censoring stated.
4. **Strangeness is not importance.** A small registry with a clean flip
   outranks a huge table that changed slowly. Row counts are on every line
   so it can be re-sorted by hand.

## Files

| file | what it holds |
|---|---|
| `lag.jsonl` / `lag_ranked.csv` | per-year reporting gap, every table with two clocks |
| `spans.jsonl` / `spans_ranked.csv` | start-year x end-year grid and the ranked read of it |
| `mix.jsonl` / `mix_ranked.csv` | year x category counts and the ranked shifts |
| `cohorts.jsonl` / `cohorts_ranked.csv` | births, deaths and lifespans per table |
