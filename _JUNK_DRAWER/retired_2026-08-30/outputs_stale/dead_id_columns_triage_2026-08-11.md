# Dead ID Columns — Triage (2026-08-11)

Recomputed from `outputs/_mart_key_date_dup_scan_2026-08-11.jsonl` (filesystem only, no
warehouse). Rule: `(nonnull − sentinels) / n_rows <= 0.01`, `n_rows >= 100`, `_`-prefixed
metadata and `_RESTORE_*` tables excluded. **193 dead columns across 80 mart tables.**
(The verification report's "104 / 43" matches a stricter `rate = 0, n_rows >= 1000` cut,
which yields 94 cols / 43 tables — but that cut excludes biorxiv, which the report cites,
so the published pair was internally inconsistent; this file supersedes it.)

Counts: **(a) truly absent in source: 61 · (b) lost in ingest: 25 · (c) needs source-file
check: 107**

Repair status (2026-08-11 repair session): every category-(b) A1/A2/A3 item was fixed the
same day (cast fixes + model retirements + NCUA reload — see the repair session STATUS and
commits). A4 (Envirofacts re-pull) and all category-(c) A8 byte-checks are follow-up
backlog. The NYC CFB cluster (17 cols across 5 cycle tables, all-cycles-identical
blankness) is the first (c) worth promoting to (b) if the publisher CSV carries the
columns.

Path prefix `M/` = `library-onboarding/ripple_dbt/models/`. Action codes:

| code | action |
|---|---|
| A1 | Drop the `try_to_double`/`try_to_number` cast (use `try_to_date` for date fields); rebuild mart. |
| A2 | Drop stale July mart+staging; repoint to `FED_FAA_AIRCRAFT_REGISTRY` (N_NUMBER unique, 315,447). |
| A3 | Fix loader member selection (account-dictionary sheet landed, not call reports); full reload. |
| A4 | Re-pull Envirofacts API; 5,000-row husk with every id column NULL implies wrong payload shape. |
| A5 | Sparse repeating-slot column; document as expected and exclude from key tests. |
| A6 | Publisher does not populate this field (documented masked-ID trap); retire column / drop from `JOIN_KEYS_STD`. |
| A7 | Synthetic spine join-key the publisher never emits; retire the column. |
| A8 | Byte-check the publisher source file for this field before deciding. |

| mart table | column | dead rate | n_rows | v | evidence | act |
|---|---|---|---|---|---|---|
| ECONOMICS__FED_DOL_FORM5500 | NUM_SCH_A_ATTACHED_CNT | 1.0000 | 33,484 | b | M/marts/economics/economics__fed_dol_form5500.sql:121 | A1 |
| ECONOMICS__FED_GRANTS_GOV | EXPECTED_NUMBER_OF_AWARDS | 1.0000 | 100 | b | M/marts/economics/economics__fed_grants_gov.sql:25 | A1 |
| ECONOMICS__INTL_GLEIF_RELATIONSHIPS | REGISTRATION_INITIALREGISTRATIONDATE | 1.0000 | 481,900 | b | M/marts/economics/economics__intl_gleif_relationships.sql:57 | A1 |
| ECONOMICS__INTL_GLEIF_RELATIONSHIPS | REGISTRATION_VALIDATIONREFERENCE | 0.9998 | 481,900 | b | M/marts/economics/economics__intl_gleif_relationships.sql:64 | A1 |
| ECONOMICS__INT_GLEIF_RR | REGISTRATION_INITIAL_REGISTRATION_DATE | 1.0000 | 481,933 | b | M/marts/economics/economics__int_gleif_rr.sql:57 | A1 |
| ECONOMICS__INT_GLEIF_RR | REGISTRATION_MANAGING_LOU | 1.0000 | 481,933 | b | M/marts/economics/economics__int_gleif_rr.sql:61 | A1 |
| ECONOMICS__INT_GLEIF_RR | REGISTRATION_NEXT_RENEWAL_DATE | 1.0000 | 481,933 | b | M/marts/economics/economics__int_gleif_rr.sql:60 | A1 |
| ECONOMICS__INT_GLEIF_RR | REGISTRATION_REGISTRATION_STATUS | 1.0000 | 481,933 | b | M/marts/economics/economics__int_gleif_rr.sql:59 | A1 |
| ECONOMICS__INT_GLEIF_RR | REGISTRATION_VALIDATION_DOCUMENTS | 1.0000 | 481,933 | b | M/marts/economics/economics__int_gleif_rr.sql:63 | A1 |
| ECONOMICS__INT_GLEIF_RR | REGISTRATION_VALIDATION_REFERENCE | 0.9998 | 481,933 | b | M/marts/economics/economics__int_gleif_rr.sql:64 | A1 |
| ECONOMICS__INT_GLEIF_RR | REGISTRATION_VALIDATION_SOURCES | 1.0000 | 481,933 | b | M/marts/economics/economics__int_gleif_rr.sql:62 | A1 |
| ENVIRONMENT__FED_EPA_ENVIROFACTS | FRS_ID | 1.0000 | 5,000 | b | M/marts/environment/environment__fed_epa_envirofacts.sql:1 | A4 |
| ENVIRONMENT__FED_EPA_ENVIROFACTS | HANDLER_ID | 1.0000 | 5,000 | b | M/marts/environment/environment__fed_epa_envirofacts.sql:1 | A4 |
| ENVIRONMENT__FED_EPA_ENVIROFACTS | SITE_ID | 1.0000 | 5,000 | b | M/marts/environment/environment__fed_epa_envirofacts.sql:1 | A4 |
| ENVIRONMENT__FED_EPA_ENVIROFACTS | STATE_CODE | 1.0000 | 5,000 | b | M/marts/environment/environment__fed_epa_envirofacts.sql:1 | A4 |
| FINANCE__FED_NCUA_CALL_REPORTS | ACCT_CODE | 1.0000 | 121,713 | b | reports/warehouse_verification_2026-08-11.md:35 | A3 |
| FINANCE__FED_NCUA_CALL_REPORTS | EIN | 1.0000 | 121,713 | b | reports/warehouse_verification_2026-08-11.md:35 | A3 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | COST_MEASURE_ID_10 | 1.0000 | 503,917 | b | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:185 | A1 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | COST_MEASURE_ID_21 | 1.0000 | 503,917 | b | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:207 | A1 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | COST_MEASURE_ID_22 | 1.0000 | 503,917 | b | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:209 | A1 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | COST_MEASURE_ID_24 | 1.0000 | 503,917 | b | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:213 | A1 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | COST_MEASURE_ID_4 | 1.0000 | 503,917 | b | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:173 | A1 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | COST_MEASURE_ID_5 | 1.0000 | 503,917 | b | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:175 | A1 |
| JUSTICE__FED_COURTLISTENER_POSITIONS | VOTES_NO_PERCENT | 0.9999 | 51,290 | b | M/marts/justice/justice__fed_courtlistener_positions.sql:40 | A1 |
| TRANSPORT__FED_FAA_REGISTRY | N_NUMBER | 1.0000 | 314,417 | b | M/staging/fed_faa_aircraft_registry/stg_fed_faa_aircraft_registry__aircraft.sql:5 | A2 |
| ECONOMICS__FED_DOL_FORM5500 | EIN | 1.0000 | 33,484 | a | scripts/build_registry_setup.py:574 | A6 |
| ECONOMICS__FED_FDIC_FAILED_BANKS | FIPS | 1.0000 | 3,584 | a | scripts/build_registry_setup.py:489 | A6 |
| ECONOMICS__FED_FOREIGNASSISTANCE | EIN | 1.0000 | 3,967,456 | a | scripts/build_registry_setup.py:574 | A6 |
| ECONOMICS__FED_IRS_990 | ZIP_CODE | 1.0000 | 200 | a | scripts/build_registry_setup.py:489 | A6 |
| ECONOMICS__FED_USASPENDING_CONTRACTS | RECIPIENT_DUNS | 1.0000 | 6,325,622 | a | M/marts/economics/economics__fed_usaspending_contracts.sql:22 | A7 |
| ECONOMICS__FED_US_SEC_EDGAR | ISIN | 1.0000 | 48,984 | a | M/marts/economics/economics__fed_us_sec_edgar.sql:20 | A7 |
| ECONOMICS__FED_US_USASPENDING_API | RECIPIENT_DUNS | 1.0000 | 300 | a | M/marts/economics/economics__fed_us_usaspending_api.sql:20 | A7 |
| ENERGY__FED_EIA860_3_4_ENERGY_STORAGE | DIRECT_SUPPORT_GEN_ID_3 | 0.9975 | 786 | a | M/marts/energy/energy__fed_eia860_3_4_energy_storage.sql | A5 |
| ENERGY__FED_EIA860_3_4_ENERGY_STORAGE | DIRECT_SUPPORT_PLANT_ID_3 | 0.9975 | 786 | a | M/marts/energy/energy__fed_eia860_3_4_energy_storage.sql | A5 |
| ENVIRONMENT__FED_NOAA_WEATHER_API | ZIP_CODE | 1.0000 | 287 | a | scripts/build_registry_setup.py:489 | A6 |
| ENVIRONMENT__FED_USGS_MINERALS | FIPS | 1.0000 | 304,632 | a | scripts/build_registry_setup.py:489 | A6 |
| HEALTH__FED_CDC_DATA_PORTAL | FIPS | 1.0000 | 15,000 | a | scripts/build_registry_setup.py:489 | A6 |
| HEALTH__FED_CDC_DATA_PORTAL | ZIP_CODE | 1.0000 | 15,000 | a | scripts/build_registry_setup.py:489 | A6 |
| HEALTH__FED_CLINICALTRIALS | NPI | 1.0000 | 500 | a | M/marts/health/health__fed_clinicaltrials.sql:36 | A7 |
| HEALTH__FED_CMS_MAIN | FIPS | 1.0000 | 158 | a | scripts/build_registry_setup.py:489 | A6 |
| HEALTH__FED_CMS_MAIN | NPI | 1.0000 | 158 | a | M/marts/health/health__fed_cms_main.sql:18 | A7 |
| HEALTH__FED_CMS_NPPES | HEALTHCARE_PROVIDER_TAXONOMY_CODE_13 | 0.9993 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | HEALTHCARE_PROVIDER_TAXONOMY_CODE_6 | 0.9946 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | OTHER_PROVIDER_IDENTIFIER_46 | 1.0000 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | OTHER_PROVIDER_IDENTIFIER_50 | 1.0000 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | OTHER_PROVIDER_IDENTIFIER_ISSUER_18 | 0.9999 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | OTHER_PROVIDER_IDENTIFIER_ISSUER_32 | 1.0000 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | OTHER_PROVIDER_IDENTIFIER_ISSUER_35 | 1.0000 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | OTHER_PROVIDER_IDENTIFIER_STATE_8 | 0.9973 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | PROVIDER_LICENSE_NUMBER_14 | 0.9999 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_NPPES | PROVIDER_LICENSE_NUMBER_6 | 0.9978 | 9,606,683 | a | M/marts/health/health__fed_cms_nppes.sql | A5 |
| HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT | ASSOCIATED_PROFILE_ID_2 | 1.0000 | 1,697,025 | a | M/marts/health/health__fed_cms_open_payments_profile_supplement.sql | A5 |
| HEALTH__FED_CMS_POS_OTHER | CLIA_ID_NUMBER_3 | 0.9909 | 44,429 | a | M/marts/health/health__fed_cms_pos_other.sql:96 | A5 |
| HEALTH__FED_CMS_POS_OTHER | CLIA_ID_NUMBER_4 | 0.9956 | 44,429 | a | M/marts/health/health__fed_cms_pos_other.sql:97 | A5 |
| HEALTH__FED_CMS_POS_OTHER | CLIA_ID_NUMBER_5 | 0.9975 | 44,429 | a | M/marts/health/health__fed_cms_pos_other.sql:98 | A5 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | PI_MEASURE_ID_20 | 0.9945 | 503,917 | a | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:145 | A5 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | PI_MEASURE_ID_21 | 1.0000 | 503,917 | a | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:148 | A5 |
| HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | QUALITY_MEASURE_ID_12 | 1.0000 | 503,917 | a | M/marts/health/health__fed_cms_quality_payment_program_experience.sql:79 | A5 |
| HOUSING__FED_MAPPING_INEQUALITY | FIPS | 1.0000 | 1,155 | a | scripts/build_registry_setup.py:489 | A6 |
| HOUSING__FED_MAPPING_INEQUALITY | HOLC_ID | 1.0000 | 1,155 | a | M/marts/housing/housing__fed_mapping_inequality.sql:15 | A7 |
| IMMIGRATION__FED_DOL_OFLC | PW_TRACKING_NUMBER_5 | 0.9999 | 664,616 | a | M/marts/immigration/immigration__fed_dol_oflc.sql:153 | A5 |
| IMMIGRATION__FED_DOL_OFLC | PW_TRACKING_NUMBER_7 | 1.0000 | 664,616 | a | M/marts/immigration/immigration__fed_dol_oflc.sql:195 | A5 |
| IMMIGRATION__FED_DOL_OFLC | PW_TRACKING_NUMBER_8 | 1.0000 | 664,616 | a | M/marts/immigration/immigration__fed_dol_oflc.sql:216 | A5 |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_10 | 0.9996 | 664,616 | a | M/marts/immigration/immigration__fed_dol_oflc.sql:252 | A5 |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_5 | 0.9969 | 664,616 | a | M/marts/immigration/immigration__fed_dol_oflc.sql:147 | A5 |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_7 | 0.9987 | 664,616 | a | M/marts/immigration/immigration__fed_dol_oflc.sql:189 | A5 |
| IMMIGRATION__FED_DOL_OFLC | WORKSITE_POSTAL_CODE_8 | 0.9991 | 664,616 | a | M/marts/immigration/immigration__fed_dol_oflc.sql:210 | A5 |
| JUSTICE__FED_FJC_IDB_APPELLATE | JUDGE_CODE_2 | 1.0000 | 988,183 | a | M/marts/justice/justice__fed_fjc_idb_appellate.sql | A5 |
| JUSTICE__FED_FJC_IDB_APPELLATE | JUDGE_CODE_3 | 1.0000 | 988,183 | a | M/marts/justice/justice__fed_fjc_idb_appellate.sql | A5 |
| JUSTICE__FED_FTC_DATASETS | CASE_TYPE | 1.0000 | 1,200 | a | M/marts/justice/justice__fed_ftc_datasets.sql:14 | A7 |
| JUSTICE__FED_FTC_DATASETS | EIN | 1.0000 | 1,200 | a | scripts/build_registry_setup.py:574 | A6 |
| JUSTICE__INTL_EU_SANCTIONS | ADDR_NUMBER | 1.0000 | 42,347 | a | M/marts/justice/justice__intl_eu_sanctions.sql:39 | A7 |
| JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST | SORT_KEY | 1.0000 | 1,011 | a | M/marts/justice/justice__xc_un_consolidated_sanctions_list.sql | A7 |
| JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST | SORT_KEY_LAST_MOD | 1.0000 | 1,011 | a | M/marts/justice/justice__xc_un_consolidated_sanctions_list.sql | A7 |
| OPEN_DATA__INTL_AR_DATOSGOB | SERIE_ID | 1.0000 | 3,556 | a | M/marts/open_data/open_data__intl_ar_datosgob.sql:20 | A7 |
| POLITICS__FED_FCC_LICENSING | EIN | 1.0000 | 1,689,338 | a | scripts/build_registry_setup.py:574 | A6 |
| POLITICS__FED_FJC_JUDGES | SEAT_ID_4 | 0.9970 | 4,067 | a | M/marts/politics/politics__fed_fjc_judges.sql:118 | A5 |
| POLITICS__FED_FJC_JUDGES | SEAT_ID_5 | 0.9998 | 4,067 | a | M/marts/politics/politics__fed_fjc_judges.sql:145 | A5 |
| POLITICS__FED_FJC_JUDGES | SEAT_ID_6 | 0.9998 | 4,067 | a | M/marts/politics/politics__fed_fjc_judges.sql:172 | A5 |
| PROCUREMENT__FED_SAM_EXCLUSIONS | NPI | 1.0000 | 2,940 | a | M/marts/procurement/procurement__fed_sam_exclusions.sql:6 | A7 |
| REFERENCE__FED_DHS_HIFLD | FIPS | 1.0000 | 500 | a | scripts/build_registry_setup.py:489 | A6 |
| REFERENCE__FED_USGS_TOPOVIEW | FIPS | 1.0000 | 250 | a | scripts/build_registry_setup.py:489 | A6 |
| SCIENCE__FED_NSF_AWARDS | EIN | 1.0000 | 125 | a | scripts/build_registry_setup.py:574 | A6 |
| TRANSPORT__FED_FRA_CROSSING_INCIDENTS | CROSSING_WARNING_EXPANDED_CODE_11 | 1.0000 | 251,149 | a | M/marts/transport/transport__fed_fra_crossing_incidents.sql | A5 |
| TRANSPORT__FED_FRA_CROSSING_INCIDENTS | CROSSING_WARNING_EXPANDED_CODE_9 | 1.0000 | 251,149 | a | M/marts/transport/transport__fed_fra_crossing_incidents.sql | A5 |
| UNCATEGORIZED__FED_FEC_LEADERSHIP_PAC | FEC_CANDIDATE_ID | 1.0000 | 8,619 | a | NO_MART_SQL | A7 |
| ECONOMICS__FED_DOL_FORM5500 | ADMIN_PHONE_NUM_FOREIGN | 0.9993 | 33,484 | c | M/marts/economics/economics__fed_dol_form5500.sql:128 | A8 |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_PHONE_NUM_FOREIGN | 1.0000 | 33,484 | c | M/marts/economics/economics__fed_dol_form5500.sql:146 | A8 |
| ECONOMICS__FED_DOL_FORM5500 | PREPARER_US_ZIP | 1.0000 | 33,484 | c | M/marts/economics/economics__fed_dol_form5500.sql:138 | A8 |
| ECONOMICS__FED_DOL_FORM5500 | SPONSOR_DFE_EIN | 1.0000 | 33,484 | c | M/marts/economics/economics__fed_dol_form5500.sql:19 | A8 |
| ECONOMICS__FED_DOL_FORM5500 | SPONS_DFE_PHONE_NUM_FOREIGN | 0.9945 | 33,484 | c | M/marts/economics/economics__fed_dol_form5500.sql:129 | A8 |
| ECONOMICS__FED_IRS_990 | EXEMPTION_CODE | 1.0000 | 200 | c | M/marts/economics/economics__fed_irs_990.sql:23 | A8 |
| ECONOMICS__FED_US_USASPENDING_API | DEF_CODE | 1.0000 | 300 | c | M/marts/economics/economics__fed_us_usaspending_api.sql:43 | A8 |
| ECONOMICS__FED_US_USASPENDING_API | GENERATED_UNIQUE_AWARD_ID | 1.0000 | 300 | c | M/marts/economics/economics__fed_us_usaspending_api.sql:18 | A8 |
| ECONOMICS__FED_US_USASPENDING_API | NAICS_CODE | 1.0000 | 300 | c | M/marts/economics/economics__fed_us_usaspending_api.sql:22 | A8 |
| ECONOMICS__FED_US_USASPENDING_API | PLACE_OF_PERFORMANCE_FIPS | 1.0000 | 300 | c | M/marts/economics/economics__fed_us_usaspending_api.sql:27 | A8 |
| ECONOMICS__FED_US_USASPENDING_API | RECIPIENT_EIN | 1.0000 | 300 | c | M/marts/economics/economics__fed_us_usaspending_api.sql:21 | A8 |
| ECONOMICS__FED_US_USASPENDING_API | RECIPIENT_LOCATION_FIPS | 1.0000 | 300 | c | M/marts/economics/economics__fed_us_usaspending_api.sql:28 | A8 |
| ECONOMICS__FED_US_USASPENDING_API | RECIPIENT_UEI | 1.0000 | 300 | c | M/marts/economics/economics__fed_us_usaspending_api.sql:19 | A8 |
| ECONOMICS__INTL_GLEIF | ENTITY_LEGALENTITYEVENTS_LEGALENTITYEVENT_1_GROUP_ID | 0.9981 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:230 | A8 |
| ECONOMICS__INTL_GLEIF | ENTITY_LEGALENTITYEVENTS_LEGALENTITYEVENT_2_GROUP_ID | 0.9981 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:249 | A8 |
| ECONOMICS__INTL_GLEIF | ENTITY_LEGALENTITYEVENTS_LEGALENTITYEVENT_2_GROUP_SEQUENCE_NO | 1.0000 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:250 | A8 |
| ECONOMICS__INTL_GLEIF | ENTITY_LEGALENTITYEVENTS_LEGALENTITYEVENT_3_GROUP_SEQUENCE_NO | 1.0000 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:269 | A8 |
| ECONOMICS__INTL_GLEIF | ENTITY_LEGALENTITYEVENTS_LEGALENTITYEVENT_4_GROUP_SEQUENCE_NO | 1.0000 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:288 | A8 |
| ECONOMICS__INTL_GLEIF | ENTITY_LEGALENTITYEVENTS_LEGALENTITYEVENT_5_GROUP_SEQUENCE_NO | 1.0000 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:307 | A8 |
| ECONOMICS__INTL_GLEIF | REGISTRATION_OTHERVALIDATIONAUTHORITIES_OTHERVALIDATIONAUTHORITY_2_VALIDATIONAUTHORITYID | 0.9935 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:335 | A8 |
| ECONOMICS__INTL_GLEIF | REGISTRATION_OTHERVALIDATIONAUTHORITIES_OTHERVALIDATIONAUTHORITY_3_OTHERVALIDATIONAUTHORITYID | 1.0000 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:339 | A8 |
| ECONOMICS__INTL_GLEIF | REGISTRATION_OTHERVALIDATIONAUTHORITIES_OTHERVALIDATIONAUTHORITY_5_OTHERVALIDATIONAUTHORITYID | 1.0000 | 3,382,301 | c | M/marts/economics/economics__intl_gleif.sql:345 | A8 |
| ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS | ACTIVITY_OUTCOME_CODE | 0.9994 | 1,900,067 | c | M/marts/environment/environment__fed_epa_npdes_npdes_inspections.sql:20 | A8 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | TRIBAL_CODE | 0.9976 | 578,198 | c | M/marts/environment/environment__fed_epa_sdwa_sdwa_geographic_areas.sql:15 | A8 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES | RECONCILIATION_ID | 0.9993 | 927,415 | c | M/marts/environment/environment__fed_epa_sdwa_sdwa_lcr_samples.sql:16 | A8 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES | RESULT_SIGN_CODE | 0.9916 | 927,415 | c | M/marts/environment/environment__fed_epa_sdwa_sdwa_lcr_samples.sql:21 | A8 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | ALT_PHONE_NUMBER | 0.9975 | 434,040 | c | M/marts/environment/environment__fed_epa_sdwa_sdwa_pub_water_systems.sql:45 | A8 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | CORRECTIVE_ACTION_ID | 0.9960 | 15,432,737 | c | M/marts/environment/environment__fed_epa_sdwa_sdwa_violations_enforcement.sql:36 | A8 |
| ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | SAMPLE_RESULT_ID | 0.9925 | 15,432,737 | c | M/marts/environment/environment__fed_epa_sdwa_sdwa_violations_enforcement.sql:35 | A8 |
| ENVIRONMENT__FED_EPA_TRI_FACILITY | BIA_CODE | 0.9978 | 64,990 | c | M/marts/environment/environment__fed_epa_tri_facility.sql | A8 |
| ENVIRONMENT__FED_EPA_TRI_FACILITY | FRS_ID | 1.0000 | 64,990 | c | M/marts/environment/environment__fed_epa_tri_facility.sql:3 | A8 |
| ENVIRONMENT__FED_NOAA_STORM_EVENTS | TOR_OTHER_CZ_FIPS | 0.9979 | 1,780,730 | c | M/marts/environment/environment__fed_noaa_storm_events.sql:47 | A8 |
| ENVIRONMENT__FED_NOAA_WEATHER_API | FIPS_CODE | 1.0000 | 287 | c | M/marts/environment/environment__fed_noaa_weather_api.sql:41 | A8 |
| ENVIRONMENT__FED_NOAA_WEATHER_API | STATION_ID | 1.0000 | 287 | c | M/marts/environment/environment__fed_noaa_weather_api.sql:31 | A8 |
| ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS | NUM_CONTRACTOR_FATALITIES | 0.9902 | 2,039 | c | M/marts/environment/environment__fed_phmsa_flagged_incidents.sql | A8 |
| ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS | NUM_EMPLOYEE_FATALITIES | 0.9902 | 2,039 | c | M/marts/environment/environment__fed_phmsa_flagged_incidents.sql | A8 |
| ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS | NUM_PUBLIC_FATALITIES | 0.9902 | 2,039 | c | M/marts/environment/environment__fed_phmsa_flagged_incidents.sql | A8 |
| ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS | NUM_WORKER_FATALITIES | 0.9902 | 2,039 | c | M/marts/environment/environment__fed_phmsa_flagged_incidents.sql | A8 |
| ENVIRONMENT__FED_USGS_WBD_HUC8 | SOURCE_FEATURE_ID | 1.0000 | 2,456 | c | M/marts/environment/environment__fed_usgs_wbd_huc8.sql | A8 |
| ENVIRONMENT__FED_WQP_MONITORING_STATIONS | CONTRIBUTING_DRAINAGE_AREA_MEASURE_UNIT_CODE | 0.9909 | 5,818 | c | M/marts/environment/environment__fed_wqp_monitoring_stations.sql | A8 |
| ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | PARENT_CIK | 0.9984 | 5,300,149 | a | M/marts/environment/environment__xc_epa_corporate_crosswalk.sql:19 | A5 |
| ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | PARENT_UEI | 0.9928 | 5,300,149 | a | M/marts/environment/environment__xc_epa_corporate_crosswalk.sql:20 | STALE |
| ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | ULTIMATE_PARENT_LEI | 0.9981 | 5,300,149 | a | M/marts/environment/environment__xc_epa_corporate_crosswalk.sql:17 | A5 |
| FINANCE__FED_PCAOB_FORM_AP_FILINGS | ISSUER_TICKER_NOT_AVAILABLE | 1.0000 | 155,384 | c | M/marts/finance/finance__fed_pcaob_form_ap_filings.sql | A8 |
| FOREIGN_INFLUENCE__FED_FARA_BULK | COMPANY_ID | 0.9954 | 48,104 | c | M/marts/foreign_influence/foreign_influence__fed_fara_bulk.sql:18 | A8 |
| HEALTH__FED_CMS_FACILITY_AFFILIATION | FACILITY_TYPE_CERTIFICATION_NUMBER | 0.9961 | 2,260,193 | c | M/marts/health/health__fed_cms_facility_affiliation.sql:21 | A8 |
| HEALTH__FED_CMS_MAIN | ZIP | 1.0000 | 158 | c | M/marts/health/health__fed_cms_main.sql:20 | A8 |
| HEALTH__FED_CMS_NURSING_HOME | PROVIDER_NUMBER | 1.0000 | 14,700 | c | M/marts/health/health__fed_cms_nursing_home.sql:15 | A8 |
| HEALTH__FED_CMS_NURSING_HOME | TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES | 1.0000 | 14,700 | c | M/marts/health/health__fed_cms_nursing_home.sql:133 | A8 |
| HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT | ASSOCIATED_PROFILE_ID_1 | 0.9949 | 1,697,025 | c | M/marts/health/health__fed_cms_open_payments_profile_supplement.sql | A8 |
| HEALTH__FED_CMS_POS_OTHER | ESRD_NTWRK_NUM | 1.0000 | 44,429 | c | M/marts/health/health__fed_cms_pos_other.sql:106 | A8 |
| HEALTH__FED_CMS_POS_OTHER | LTC_CROSS_REF_PROVIDER_NUMBER | 1.0000 | 44,429 | c | M/marts/health/health__fed_cms_pos_other.sql:118 | A8 |
| HEALTH__FED_CMS_POS_OTHER | MEDICARE_MEDICAID_PRVDR_NUMBER | 1.0000 | 44,429 | c | M/marts/health/health__fed_cms_pos_other.sql:122 | A8 |
| HEALTH__FED_CMS_POS_OTHER | TCHNCL_STF_NUM | 1.0000 | 44,429 | c | M/marts/health/health__fed_cms_pos_other.sql:458 | A8 |
| HEALTH__FED_FDA_CAERS | PRODUCT_INDUSTRY_CODE | 1.0000 | 85,511 | c | M/marts/health/health__fed_fda_caers.sql | A8 |
| HEALTH__FED_FDA_DEVICE_ENFORCEMENT | FEI_NUMBER_LIST | 1.0000 | 39,635 | c | M/marts/health/health__fed_fda_device_enforcement.sql:56 | A8 |
| HEALTH__FED_FDA_DEVICE_ENFORCEMENT | K_NUMBER_LIST | 1.0000 | 39,635 | c | M/marts/health/health__fed_fda_device_enforcement.sql:55 | A8 |
| HEALTH__FED_FDA_DEVICE_ENFORCEMENT | PRODUCT_CODE | 1.0000 | 39,635 | c | M/marts/health/health__fed_fda_device_enforcement.sql:6 | A8 |
| HEALTH__FED_FDA_DEVICE_ENFORCEMENT | REGISTRATION_NUMBER_LIST | 1.0000 | 39,635 | c | M/marts/health/health__fed_fda_device_enforcement.sql:54 | A8 |
| HEALTH__FED_FDA_DEVICE_PMA | ZIP_EXT | 1.0000 | 56,853 | c | M/marts/health/health__fed_fda_device_pma.sql | A8 |
| HEALTH__FED_FDA_DRUG_ENFORCEMENT | MORE_CODE_INFO | 0.9999 | 17,816 | c | M/marts/health/health__fed_fda_drug_enforcement.sql:43 | A8 |
| HEALTH__FED_FDA_ESTABLISHMENT_REG | PMA_NUMBER | 0.9907 | 263,374 | c | M/marts/health/health__fed_fda_establishment_reg.sql | A8 |
| HEALTH__FED_FDA_MAUDE | BASELINE_510K_NUMBER | 1.0000 | 2,743,561 | c | M/marts/health/health__fed_fda_maude.sql | A8 |
| HEALTH__FED_FDA_MAUDE | EVENT_KEY | 1.0000 | 2,743,561 | c | M/marts/health/health__fed_fda_maude.sql | A8 |
| HEALTH__FED_FDA_UNII_GSRS_SUBSTANCES | EC_NUMBER | 1.0000 | 168,046 | c | M/marts/health/health__fed_fda_unii_gsrs_substances.sql | A8 |
| HISTORY__FED_WPA_SLAVE_NARRATIVES | STATE_FIPS | 1.0000 | 100 | c | M/marts/history/history__fed_wpa_slave_narratives.sql:19 | A8 |
| HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | RENTAL_RESOURCE_ZIP_CODE | 0.9965 | 3,080,000 | c | M/marts/housing/housing__fed_fema_ia_housing_registrations.sql | A8 |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | DPV_RETURN_CODE | 1.0000 | 3,787 | c | M/marts/housing/housing__fed_hud_public_housing_authorities.sql | A8 |
| HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | PLACE_CLASS_CODE | 1.0000 | 3,787 | c | M/marts/housing/housing__fed_hud_public_housing_authorities.sql | A8 |
| JUSTICE__FED_COURTLISTENER_POSITIONS | PREDECESSOR_ID | 0.9971 | 51,290 | c | M/marts/justice/justice__fed_courtlistener_positions.sql:46 | A8 |
| JUSTICE__FED_COURTLISTENER_POSITIONS | SCHOOL_ID | 0.9955 | 51,290 | c | M/marts/justice/justice__fed_courtlistener_positions.sql:47 | A8 |
| JUSTICE__FED_COURTLISTENER_POSITIONS | SUPERVISOR_ID | 0.9969 | 51,290 | c | M/marts/justice/justice__fed_courtlistener_positions.sql:48 | A8 |
| JUSTICE__FED_FJC_IDB_APPELLATE | JUDGE_CODE_1 | 1.0000 | 988,183 | c | M/marts/justice/justice__fed_fjc_idb_appellate.sql | A8 |
| JUSTICE__FED_FJC_IDB_BANKRUPTCY | DESTINATION_CASE | 0.9989 | 6,965,441 | c | M/marts/justice/justice__fed_fjc_idb_bankruptcy.sql | A8 |
| LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | SB_ACTUARY_PHONE_NUM_FOREIGN | 0.9999 | 41,802 | c | M/marts/labor/labor__fed_dol_ebsa_form5500_schedule_sb.sql | A8 |
| LABOR__FED_DOL_OLMS | NUM_ATTACHMENTS | 1.0000 | 617,710 | c | M/marts/labor/labor__fed_dol_olms.sql | A8 |
| POLITICS__FED_FCC_LICENSING | EBF_TRANSACTION_ID | 1.0000 | 1,689,338 | c | M/marts/politics/politics__fed_fcc_licensing.sql:13 | A8 |
| POLITICS__FED_FCC_LICENSING | ELIGIBILITY_RULE_NUM | 1.0000 | 1,689,338 | c | M/marts/politics/politics__fed_fcc_licensing.sql:20 | A8 |
| POLITICS__FED_FCC_LICENSING | FCC_COUNTY_CODE | 1.0000 | 1,689,338 | c | M/marts/politics/politics__fed_fcc_licensing.sql:35 | A8 |
| POLITICS__FED_FEC_API | CANDIDATE_ID | 0.9980 | 500 | c | M/marts/politics_lobbying/politics__fed_fec_api.sql | A8 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION | EXEMPT_CODE | 0.9999 | 193,741 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2001_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION | SEQUENCE_NUMBER | 1.0000 | 193,741 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2001_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | EXEMPT_CODE | 0.9999 | 146,112 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2009_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | INTERMEDIARY_STREET_NUMBER | 1.0000 | 146,112 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2009_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | PAGE_NUMBER | 1.0000 | 146,112 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2009_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | PURPOSE_CODE | 0.9948 | 146,112 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2009_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION | SEQUENCE_NUMBER | 1.0000 | 146,112 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2009_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | EXEMPT_CODE | 0.9999 | 197,968 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2013_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | INTERMEDIARY_STREET_NUMBER | 1.0000 | 197,968 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2013_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION | STREET_NUMBER | 1.0000 | 197,968 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2013_contribution.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | EXEMPT_CODE | 1.0000 | 457,521 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2021_contributions.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | PAGE_NUMBER | 1.0000 | 457,521 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2021_contributions.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS | STREET_NUMBER | 1.0000 | 457,521 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2021_contributions.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | INTERMEDIARY_STREET_NUMBER | 1.0000 | 259,537 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2025_contributions.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | PAGE_NUMBER | 1.0000 | 259,537 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2025_contributions.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | PURPOSE_CODE | 0.9983 | 259,537 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2025_contributions.sql | A6 |
| POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | STREET_NUMBER | 1.0000 | 259,537 | a | M/marts/politics_lobbying/politics__st_nyc_cfb_campaign_2025_contributions.sql | A6 |
| PROCUREMENT__FED_USASPENDING_BULK | EVALUATED_PREFERENCE_CODE | 1.0000 | 49,613 | c | M/marts/procurement/procurement__fed_usaspending_bulk.sql | A8 |
| REFERENCE__FED_DHS_HIFLD | ZIP | 1.0000 | 500 | c | M/marts/reference/reference__fed_dhs_hifld.sql | A8 |
| SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV | FUNDER_ROR_ID | 1.0000 | 432 | a | M/marts/science_research/science_research__xc_biorxiv_medrxiv.sql:18 | A5 |
| SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV | FUNDING_ID_TYPE | 1.0000 | 432 | a | M/marts/science_research/science_research__xc_biorxiv_medrxiv.sql:39 | A5 |
| SCIENCE__INTL_EMBL_ENSEMBL | TAXON_ID | 1.0000 | 643 | c | M/marts/science/science__intl_embl_ensembl.sql:24 | A8 |
| TRANSPORT__FED_FRA_CASUALTIES | COVERED_DATA_CODE | 0.9984 | 1,150,788 | c | M/marts/transport/transport__fed_fra_casualties.sql | A8 |
| TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT | OPER_CERT | 1.0000 | 31,503 | a | M/marts/transport/transport__fed_ntsb_aviation_aircraft.sql | A6 |
| TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT | OPRTNG_CERT | 1.0000 | 31,503 | a | M/marts/transport/transport__fed_ntsb_aviation_aircraft.sql | A6 |
| TRANSPORT__FED_NTSB_AVIATION_EVENTS | FICHE_NUMBER | 1.0000 | 30,968 | a | M/marts/transport/transport__fed_ntsb_aviation_events.sql | A6 |
| TRANSPORT__FED_NTSB_AVIATION_EVENTS | NTSB_DOCKET | 1.0000 | 30,968 | a | M/marts/transport/transport__fed_ntsb_aviation_events.sql | A6 |

## Notes on the (c) rows that need a named source URL

- NTSB (4 cols): `https://data.ntsb.gov/avdata/FileDirectory/DownloadFile` (avall.zip →
  avall.mdb), per `scripts/ntsb_aviation_load.py:48`. **Not a parse-position bug** — that
  loader reads named Access tables/columns via pandas (`scripts/ntsb_aviation_load.py:115-142`),
  so there is no positional-offset risk. Check the MDB fields directly.
- biorxiv (2 cols): biorxiv/medrxiv publisher API; `stg_xc_biorxiv_medrxiv__preprint_manuscript.sql:20`
  is a straight `funding_id as funder_ror_id` rename, so the landing column itself is empty.
- FAA: `https://registry.faa.gov/database/ReleasableAircraft.zip`, member `MASTER`
  (`scripts/sprint_rebuild_20260809_specs.py:44,46`).
- FCC ULS: `https://www.fcc.gov/uls/index.htm` (`stg_fed_fcc_licensing__records.sql:44`).
- NYC CFB (17 cols across 5 cycle tables): `STREET_NUMBER` / `PAGE_NUMBER` / `SEQUENCE_NUMBER` /
  `INTERMEDIARY_STREET_NUMBER` are 100% NULL in **every** cycle table — that consistency argues
  for a dropped-column-group ingest bug; promote to (b) if the publisher CSV carries them.

## Byte-check resolutions (2026-08-11 follow-up session)

Four (c) clusters resolved against publisher source bytes. Verdict column updated above
(c→a); NOT promoted to (b) — none were loader bugs.

- **NYC CFB (17 cols, 5 cycle tables) → publisher-absent.** Downloaded CFB-Data.zip
  (102MB, the exact file the loader ingests) and scanned 50k raw rows of
  `2021_Contributions.csv`: `PAGENO`, `SEQUENCENO`, `STRNO`, `STRNAME`, `APARTMENT`,
  `INTSTRNO`, `INTSTRNM`, `INTAPTNO` are all 0 non-blank in the publisher's own file —
  CFB redacts filing page/sequence and street-number address detail from its public
  export. The all-cycles-identical pattern is redaction, not a dropped column group.
  `EXEMPTCD` (2/50k) and `PURPOSECD` (70/50k) are genuinely near-empty at source too.
  Documented in all five cycle staging schema.yml files. No reload needed.
- **NTSB aviation (4 cols) → publisher-absent.** Downloaded avall.zip (95.6MB) and
  queried avall.mdb directly via the Access ODBC driver: `ntsb_docket` and
  `fiche_number` are 0 non-null of 30,968 events rows; `oper_cert` and `oprtng_cert`
  are 0 non-null of 31,503 aircraft rows. NTSB ships them empty. Documented in the
  events/aircraft staging schema.yml files. No reload needed.
- **EPA corporate crosswalk (3 cols) → structural sparsity + one stale scan row.**
  Read-only funnel on the 5,300,149-row table: only 1.40% of facilities name-match a
  GLEIF LEI; 13.9% of those have an ACTIVE ultimate parent (`ULTIMATE_PARENT_LEI`
  0.19% overall); `PARENT_CIK` needs a further unique EDGAR name match (0.16%). Most
  facilities have no public-company/LEI parent — by design of the match ladder.
  **`PARENT_UEI` is NOT dead: 427,515 rows populated (8.07%) in both landing and mart
  today; the scan row above (0.9928 dead) is stale.** Documented in the crosswalk
  mart schema yml.
- **biorxiv funder IDs (2 cols) → publisher-sparse.** The bioRxiv details API DOES
  emit structured funder objects (name/id/id-type='ROR'/award) but only on ~6% of
  manuscripts (9 funder entries per 150 records sampled; id populated 8/9, id-type
  always 'ROR'). Our 432-row landing sample mixes details/pubs/stats shapes, so
  all-NULL is consistent with upstream sparsity at this size — not a mart bug. A
  fuller details-endpoint ingest would populate a minority of rows. Documented in the
  biorxiv staging schema.yml.
