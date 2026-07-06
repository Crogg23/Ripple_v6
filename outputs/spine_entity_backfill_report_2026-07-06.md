# Spine-entity backfill proposal

NAME 96 | PLACE 1 | SUGGESTED 62 | UNKNOWN 190 | NO_TABLE 0

Sets ONLY spine_entity on grain-proven/entity-unknown sources. NAME + PLACE are auto-written by --apply; SUGGESTED needs --include-suggested; UNKNOWN stays NULL.

## TIER 1 -- NAME map (auto) (96)

| source_id | spine_entity | evidence |
|---|---|---|
| fed_congress_committee_membership | person | natural_key BIOGUIDE+COMMITTEE_CODE -> person |
| fed_dhs_yearbook | place | natural_key COUNTRY_OF_LAST_RESIDENCE+FISCAL_YEAR -> place |
| fed_fec_bulk_candidates | place | natural_key CAND_ZIP+CAND_ELECTION_YR+CYCLE+CAND_STATUS+CAND_ID -> place |
| fed_usaspending_bulk | organization | natural_key RECIPIENT_UEI+ACTION_DATE+ACTION_DATE_FISCAL_YEAR+PERIOD_OF_PERFORMANCE_START_DATE+AWARD_ID_PIID+PARENT_AWARD_AGENCY_ID+PARENT_AWARD_ID_PIID -> organization |
| fed_usaspending_contracts | organization | natural_key RECIPIENT_UEI+ACTION_DATE+PERIOD_OF_PERFORMANCE_START_DATE+PERIOD_OF_PERFORMANCE_CURRENT_END_DATE+AWARD_ID_PIID -> organization |
| intl_eu_sanctions | place | natural_key ADDR_ZIPCODE+DATE_FILE+LEBA_PUBLICATION_DATE+NAAL_LEBA_PUBLICATION_DATE+ENTITY_LOGICAL_ID+NAAL_LOGICAL_ID+ENTITY_LOGICAL_ID_1+ENTITY_LOGICAL_ID_2+BIRT_LOGICAL_ID+ENTITY_LOGICAL_ID_3+IDEN_LOGICAL_ID+ENTITY_LOGICAL_ID_4+CITI_LOGICAL_ID+ENTITY_LOGICAL_ID_5 -> place |
| intl_wb_ids | place | natural_key COUNTRY_CODE+COUNTERPART_AREA_CODE+SERIES_CODE -> place |
| portal_arc_atlanta_dataatla_51a606f539 | place | natural_key LONGITUDE+BUSINESS_LICENSE_YEAR+DATE_OF_OPENING_IN_ATLANTA+PREVIOUS_YEAR_REPORTED_REVENUE -> place |
| portal_arc_atlanta_dataatla_5d9b9c30a9 | place | natural_key ZIP+INDUSTRY_DESC -> place |
| portal_arc_atlanta_dataatla_ead25cbdc7 | place | natural_key LONGITUDE+BUSINESS_LICENSE_YEAR+DATE_OF_OPENING_IN_ATLANTA+PREVIOUS_YEAR_REPORTED_REVENUE -> place |
| portal_arc_atlanta_dataatla_fd3576897b | place | natural_key ZIP+INDUSTRY_DESC -> place |
| portal_arc_harris_county_op_1966ac023b | place | natural_key ZIP+VAL_DATE -> place |
| portal_arc_harris_county_op_6cdcf96ca7 | place | natural_key ZIP+VAL_DATE+IN_100_YR_FLOODPLAIN+IN_500_YR_FLOODPLAIN+ID+STATE_ID -> place |
| portal_arc_harris_county_op_e87e81379a | place | natural_key ZIP+VAL_DATE+IN_100_YR_FLOODPLAIN+IN_500_YR_FLOODPLAIN+ID+STATE_ID -> place |
| portal_arc_la_county_open_d_0a94db308e | provider | natural_key CCN+NPI+PARTICIPATION_DATE+APPROVAL_DATE+START_DATE -> provider |
| portal_arc_la_county_open_d_e034245e05 | provider | natural_key NPI+SCC_TYPE -> provider |
| portal_arc_open_baltimore_751d91c991 | facility | natural_key CCN+TYPE -> facility |
| portal_arc_open_data_dc_5b867c795c | facility | natural_key CCN_REV+DATE -> facility |
| portal_arc_open_data_dc_d8e55d5b7f | facility | natural_key CCN_REV+DATE -> facility |
| portal_arc_open_data_raleig_f18f09f22f | place | natural_key SHIPPING_ZIP_POSTAL_CODE+APPLICATION_DATE -> place |
| portal_arc_orange_county_op_644fb9535b | place | natural_key ZIP+INSPECTION_DATE+OPERATIONAL_STATUS+PROGRAM_ELEMENT -> place |
| portal_arc_tucson_open_data_14c7aa5ccf | place | natural_key ZIP+INDUSTRY_DESC -> place |
| portal_arc_tucson_open_data_32a72d9d1d | place | natural_key ZIP+INDUSTRY_DESC -> place |
| portal_arc_tucson_open_data_3a7e0821d1 | case | natural_key DOCKET+LAST_EDITED_DATE -> case |
| portal_arc_tucson_open_data_63c0193ff1 | case | natural_key DOCKET+LAST_EDITED_DATE -> case |
| portal_arc_tucson_open_data_7468cf46db | case | natural_key DOCKET+LAST_EDITED_DATE -> case |
| portal_arc_tucson_open_data_cdffe1002a | case | natural_key DOCKET+LAST_EDITED_DATE -> case |
| portal_arc_tucson_open_data_e0edea39be | place | natural_key ZIP+INDUSTRY_DESC -> place |
| portal_arc_tucson_open_data_f0203665dd | place | natural_key ZIP+INDUSTRY_DESC -> place |
| portal_arc_tucson_open_data_f919285f50 | case | natural_key DOCKET+LAST_EDITED_DATE -> case |
| portal_cka_analyze_boston_0012b002be | place | natural_key SHAPE_WKT+DATE_AND_TIME -> place |
| portal_cka_analyze_boston_1321cb60b5 | place | natural_key LAT+DATE_TIME -> place |
| portal_cka_analyze_boston_4eddc3919b | place | natural_key ZIP_CODE+APPLICATION_DATE -> place |
| portal_cka_analyze_boston_5288db6955 | place | natural_key SHAPE_WKT+DATE_DESIGNATED_1+CREATED_DATE+LAST_EDITED_DATE+UNIQUE_ID -> place |
| portal_cka_analyze_boston_9fe0838e9f | place | natural_key ZIPCODE+DATE_BUSINESS_ESTABLISHED+BUSINESS_TYPE+COB_CATEGORY_CODES1 -> place |
| portal_cka_analyze_boston_dd269d0a1d | place | natural_key ZIP_R+SEGMENT_ID -> place |
| portal_cka_analyze_boston_f1b3f76830 | place | natural_key CONTACT_ZIP+STATUS_DTTM -> place |
| portal_cka_california_open_6611464444 | place | natural_key LONGITUDE+SITE_CODE -> place |
| portal_cka_california_open_a5d78a8b63 | place | natural_key LATITUDE+LAST_MODIFIED_DATE+DATE_DATA_REFERS_TO+DWR_GW_SITE_CODE -> place |
| portal_cka_california_open_c19a7c8625 | place | natural_key COUNTRY+SUBMITTED_DATE -> place |
| portal_cka_houston_open_dat_a4490182ba | place | natural_key ZIPCODE+SR_CREATE_DATE+DUE_DATE+DATE_CLOSED+TAX_ID -> place |
| portal_cka_houston_open_dat_ab35bb6552 | place | natural_key ZIP+IN_DATE+DUE_DATE+OUT_DATE+ID -> place |
| portal_cka_indiana_data_hub_78f3e49d13 | place | natural_key COUNTY_FIPS+SCHOOL_YEAR+SUBMISSION_STATUS+SCHOOL_ID -> place |
| portal_cka_indiana_data_hub_d4dae8d984 | place | natural_key ZIPCODE+YEAR+AGE_GROUP -> place |
| portal_cka_indiana_data_hub_fe00d42acc | place | natural_key FIPS+DATE -> place |
| portal_cka_israel_national_03d9d0d534 | place | natural_key ZIPCODE+OPEN_DATE+CLOSE_DATE+BRANCH_CODE+ID -> place |
| portal_cka_israel_national_6272f09a75 | place | natural_key ZIP_CODE+CATEGORY+BANK_CODE -> place |
| portal_cka_israel_national_c05e5881a0 | place | natural_key ZIP_CODE+INSTITUTE_CODE -> place |
| portal_cka_israel_national_e3d369b05f | place | natural_key STN_LAT+DATE_OPEN+DATE_CLOSE -> place |
| portal_cka_open_data_sa_1c37ee3869 | place | natural_key SHAPE__LENGTH+FISCAL_YEAR -> place |
| portal_cka_open_data_sa_2fcd3aefd6 | place | natural_key SHAPE__LENGTH+CREATED_DATE -> place |
| portal_cka_open_data_sa_9dca88d285 | place | natural_key SHAPE__LENGTH+FISCAL_YEAR -> place |
| portal_cka_open_data_sa_a8ef161189 | place | natural_key SHAPE__LENGTH+CREATED_DATE -> place |
| portal_cka_san_jose_open_da_98849b65ee | place | natural_key LATITUDE+REPORTDATE -> place |
| portal_cka_virginia_open_da_3e67a117fb | place | natural_key FIPS+REPORT_DATE -> place |
| portal_cka_virginia_open_da_651c0c423a | place | natural_key ZIP_CODE+STARTING_DATE+EXPIRATION_DATE+INSERTED_DATE+BUFFER_ID -> place |
| portal_cka_virginia_open_da_cbc7fe8b75 | place | natural_key INCIDENT_FIPS+INCIDENT_YEAR+INCIDENT_MONTH -> place |
| portal_cka_western_pennsylv_070a16004d | place | natural_key ZIPCODE+LAST_EDIT_DATE -> place |
| portal_cka_western_pennsylv_23b8b5b7d2 | place | natural_key ZIP_CODE+CREATE_DATE+PROPERTY_TYPE+INSPECTION_STATUS+PARCEL_ID -> place |
| portal_cka_western_pennsylv_2dfc1addea | place | natural_key DECEDENT_ZIP+DEATH_DATE_AND_TIME -> place |
| portal_cka_western_pennsylv_4fc22c2c30 | place | natural_key ZIP_CODE+PERMIT_ISSUE_DATE+PERMIT_EXPIRE_DATE+PROJECT_TYPE+PARCEL_ID -> place |
| portal_cka_western_pennsylv_51b8dcf278 | place | natural_key LATITUDE+START_YEAR+APPROVED_DATE -> place |
| portal_cka_western_pennsylv_ed65b530a3 | place | natural_key GEOID+QUARTER -> place |
| portal_cka_wprdc_allegheny_12c9244c06 | place | natural_key ZIPCODE+LAST_EDIT_DATE -> place |
| portal_cka_wprdc_allegheny_1c103ee2cd | place | natural_key ZIP_CODE+CREATE_DATE+PROPERTY_TYPE+INSPECTION_STATUS+PARCEL_ID -> place |
| portal_cka_wprdc_allegheny_9ccbefbacc | place | natural_key GEOID+QUARTER -> place |
| portal_cka_wprdc_allegheny_a4e9ce945b | place | natural_key DECEDENT_ZIP+DEATH_DATE_AND_TIME -> place |
| portal_cka_wprdc_allegheny_bb0184f847 | place | natural_key ZIP_CODE+PERMIT_ISSUE_DATE+PERMIT_EXPIRE_DATE+PROJECT_TYPE+PARCEL_ID -> place |
| portal_cka_wprdc_allegheny_ce7a2694fc | place | natural_key LATITUDE+START_YEAR+APPROVED_DATE -> place |
| portal_soc_colorado_informa_1d5cfad830 | place | natural_key COUNTY_FIPS+FISCAL_YEAR+START_DATE+EXIT_DATE+STATE_ID+STATE_ID_COPY+APPRENTICE_ID+PROGRAM_ID -> place |
| portal_soc_colorado_informa_de6c8a6901 | place | natural_key COUNTY_FIPS+FISCAL_YEAR+START_DATE+EXIT_DATE+STATE_ID+STATE_ID_COPY+APPRENTICE_ID+PROGRAM_ID -> place |
| portal_soc_colorado_informa_e80ca7800e | place | natural_key COUNTY_FIPS+EXIT_DATE+FISCAL_YEAR+START_DATE+STATE_ID+STATE_ID_COPY+APPRENTICE_ID+PROGRAM_ID -> place |
| portal_soc_connecticut_open_aeb46f6c94 | place | natural_key C_9_ZIP+C_1_YEAR+C_18_INDUSTRY_SECTOR_CODE+C_19_INDUSTRY_SECTOR+C_3_FRS_ID+C_35_CAS_COMPOUND_ID+C_36_SRS_ID -> place |
| portal_soc_connecticut_open_ff2b86a533 | place | natural_key ZIP_CODE+FISCAL_YEAR+CONTRACT_EXECUTION_DATE -> place |
| portal_soc_datala_los_angel_361b8161b7 | place | natural_key MAILING_ZIP_CODE+LOCATION_START_DATE+LOCATION_END_DATE+ZIP_CODE -> place |
| portal_soc_datala_los_angel_dc3670afe1 | place | natural_key MAILING_ZIP_CODE+LOCATION_START_DATE+ZIP_CODE -> place |
| portal_soc_open_data_br_c110d5cf59 | place | natural_key ZIP+BUSINESS_NAICS_CODE+RESOURCE_TYPE+SUB_RESOURCE_TYPE+BUSINESS_ID+METADATA_ID -> place |
| portal_soc_seattle_open_dat_c8f2072189 | place | natural_key ZIP+LICENSE_START_DATE -> place |
| portal_soc_sf_opendata_data_79618299a6 | place | natural_key BUSINESS_ZIP+DBA_START_DATE+LOCATION_START_DATE -> place |
| portal_soc_sf_opendata_data_c19ee9eb44 | provider | natural_key NPI+PROGRAM_NAME -> provider |
| portal_soc_texas_open_data_28e2f49084 | organization | natural_key NPN_EIN+ACTIVE_DATE+APPOINTMENT_TYPE+NAIC_ID -> organization |
| portal_soc_texas_open_data_354e3abf4f | place | natural_key SITE_ZIP_CD+NOR_REGISTRATION_DATE -> place |
| portal_soc_texas_open_data_5410a1009f | place | natural_key OUTLET_ZIP_CODE+OUTLET_PERMIT_ISSUE_DATE -> place |
| portal_soc_texas_open_data_6f798a64fa | organization | natural_key EIN+ACTIVE_DATE+APPOINTMENT_TYPE+NAIC_ID -> organization |
| portal_soc_texas_open_data_a415622c5d | place | natural_key LOC_ZIP+PERMIT_DATE -> place |
| portal_soc_texas_open_data_d83872d208 | case | natural_key DISTRICT_COURT_DOCKET_NO+ORDER_DATE -> case |
| portal_soc_texas_open_data_da657010b1 | place | natural_key LOC_ZIP+RESP_BEGIN_DATE -> place |
| portal_soc_utah_open_data_p_103f7d641f | organization | natural_key RECIPIENT_DUNS+PERIOD_OF_PERFORMANCE_START+PERIOD_OF_PERFORMANCE_CURRENT+LAST_MODIFIED_DATE+AWARD_ID_FAIN+AWARD_ID_URI -> organization |
| portal_soc_utah_open_data_p_55ef6ef0c6 | provider | natural_key NPI+HCPCS_CODE -> provider |
| portal_soc_utah_open_data_p_5ef68422ff | organization | natural_key RECIPIENT_DUNS+PERIOD_OF_PERFORMANCE_START+PERIOD_OF_PERFORMANCE_CURRENT+PERIOD_OF_PERFORMANCE+AWARD_ID_PIID+PARENT_AWARD_AGENCY_ID+PARENT_AWARD_ID -> organization |
| portal_soc_utah_open_data_p_d5f7ca2621 | place | natural_key C_9_ZIP+C_1_YEAR+C_18_INDUSTRY_SECTOR_CODE+C_19_INDUSTRY_SECTOR+C_35_CAS_COMPOUND_ID+C_36_SRS_ID+C_3_FRS_ID -> place |
| portal_soc_utah_open_data_p_f1292b8d2f | organization | natural_key DUNS_NO+FISCAL_YEAR+EVALUATION_CLOSED_DATE -> organization |
| portal_soc_washington_state_1a95fb1665 | organization | natural_key UBI_EIN+AUDIT_CLOSED_DATE+RECIPIENT_TYPE+AUDIT_TYPE -> organization |
| st_cannabis_policy_bundles | place | natural_key FIPS+YEAR -> place |
| xc_owid_refugees | place | natural_key REFUGEES_BY_COUNTRY_OF_ORIGIN+YEAR+CODE -> place |
| xc_vera_incarceration_trends | place | natural_key STATE_FIPS+YEAR+STATE_CODE+COUNTY_CODE -> place |

## TIER 2 -- PLACE, FIPS values (auto) (1)

| source_id | spine_entity | evidence |
|---|---|---|
| portal_cka_indiana_data_hub_83ba6435c2 | place | LOCATION_ID (geo-named) FIPS-valid 100% (n=1000); e.g. 18025, 18007, 18017, 18019, 18015 |

## TIER 2 -- SUGGESTED org/person (review, --include-suggested to write) (62)

| source_id | spine_entity | evidence |
|---|---|---|
| fed_cfpb_complaints | organization | COMPANY org-token 98% (n=500); e.g. EQUIFAX, INC., TRANSUNION INTERMEDIATE HOLDINGS, INC., Experian Information Solutions Inc. |
| fed_clinicaltrials | organization | LEAD_SPONSOR_NAME org-token 72% (n=500); e.g. Wake Forest University Health Sciences, TG Therapeutics, Inc., University Medical Center Groningen |
| fed_cms_open_payments | person | structured COVERED_RECIPIENT_FIRST_NAME+COVERED_RECIPIENT_LAST_NAME populated (n=997) |
| fed_cms_open_payments_2023 | person | structured COVERED_RECIPIENT_FIRST_NAME+COVERED_RECIPIENT_LAST_NAME populated (n=994) |
| fed_dol_form5500 | organization | SPONSOR_DFE_NAME org-token 88% (n=1000); e.g. MCCOY GROUP INC., BONE ROOFING SUPPLY, INC., BBHB TOTAL GAS SERVICES, INC. |
| fed_faa_registry | organization | NAME org-token 48% (n=980); e.g. MERTESDORF JOHN P                       , WINGS OVER TEXAS HOLDINGS LLC           , SALE REPORTED                            |
| fed_fdic_failed_banks | organization | NAME org-token 76% (n=1000); e.g. FON DU LAC STATE BANK, WINDOM FS&LA, ROCKY MOUNTAIN S & L ASSOC. |
| fed_fec_bulk | organization | CMTE_NM org-token 46% (n=1000); e.g. FAMILIES FOR JAMES LANKFORD, AMERICAN MEDICAL ASSOCIATION POLITICAL A, GARNOTT HALL |
| fed_fec_bulk_committees | organization | CMTE_NM org-token 48% (n=1000); e.g. PUMP THE VOTE, RACHEL FOR US SENATE, BOARDWALK GP LLC PUBLIC AFFAIRS COMMITTE |
| fed_us_usaspending_api | organization | RECIPIENT_NAME org-token 95% (n=300); e.g. HUMANA GOVERNMENT BUSINESS INC, LOCKHEED MARTIN CORP, NATIONAL TECHNOLOGY & ENGINEERING SOLUTI |
| fed_usaspending_toptier_agencies | organization | AGENCY_NAME org-token 93% (n=111); e.g. 400 Years of African-American History Co, Access Board, Administrative Conference of the U.S. |
| portal_arc_harris_county_op_12691a85a0 | organization | NAME org-token 100% (n=38); e.g. LEAGUE CITY POLICE DEPARTMENT, WEBSTER POLICE DEPARTMENT, CLEAR LAKE SHORES POLICE DEPARTMENT |
| portal_arc_harris_county_op_87f4853c1a | organization | NAME org-token 90% (n=30); e.g. HOUSTON PHYSICIANS HOSPITAL, VIBRA HOSPITAL OF CLEAR LAKE, HCA HOUSTON HEALTHCARE CLEAR LAKE |
| portal_arc_harris_county_op_a2dae85c30 | organization | NAME org-token 100% (n=38); e.g. LEAGUE CITY POLICE DEPARTMENT, WEBSTER POLICE DEPARTMENT, CLEAR LAKE SHORES POLICE DEPARTMENT |
| portal_arc_la_county_open_d_75836d970c | organization | FAC_NAME org-token 52% (n=1000); e.g. C E G CONSTRUCTION, VALLEY COLLISION INC, CEDARS-SINAI MARINA DEL REY HOSPITAL |
| portal_arc_new_mexico_open_1b6c7f7fbd | organization | NAME org-token 78% (n=32); e.g. KIT CARSON ELECTRIC COOP, INC, CITY OF AZTEC - (NM), LEA COUNTY ELECTRIC COOP, INC |
| portal_arc_open_data_dc_d359158bc8 | organization | COUNTY_NAME org-token 100% (n=733); e.g. DISTRICT OF CO, DISTRICT OF CO, DISTRICT OF CO |
| portal_arc_open_data_raleig_5e5b26dc88 | person | structured FIRST_NAME+LAST_NAME populated (n=252) |
| portal_arc_open_data_raleig_8ee851c810 | person | structured FIRST_NAME+LAST_NAME populated (n=1000) |
| portal_arc_open_data_raleig_df19dcbb03 | person | structured FIRST_NAME+LAST_NAME populated (n=1000) |
| portal_arc_open_data_raleig_efbb617010 | person | structured FIRST_NAME+LAST_NAME populated (n=1000) |
| portal_arc_tucson_open_data_55d5164315 | organization | SCHOOLS_DISTRICT_NAME org-token 93% (n=60); e.g. Tucson Unified District, Basis Charter Schools INC. (6361), Tucson Unified District |
| portal_arc_wisconsin_open_d_4ebc995c5d | organization | NAME org-token 88% (n=56); e.g. WESTFIELDS HOSPITAL AND CLINIC, CUMBERLAND HEALTHCARE HOSPITAL, MAYO CLINIC HEALTH SYSTEM - CHIPPEWA VAL |
| portal_arc_wisconsin_open_d_5206358bdd | organization | FACILITY_NAME org-token 85% (n=604); e.g. ESSENTIA HEALTH ST MARYS, HEALTHEAST BETHESDA HOSPITAL, FAIRVIEW LAKES MEDICAL CENTER |
| portal_arc_wisconsin_open_d_cb1509f410 | organization | NAME org-token 90% (n=42); e.g. HSHS ST. JOSEPH'S HOSPITAL, SACRED HEART HOSPITAL, ASPIRUS MEDFORD HOSPITAL |
| portal_cka_analyze_boston_7f82f529e8 | organization | NAME org-token 75% (n=60); e.g. Massachusetts General Hospital Dietetic , Suffolk University, Benjamin Franklin Institute of Technolog |
| portal_cka_analyze_boston_9a0fe05b1b | organization | VENDOR_NAME1 org-token 82% (n=1000); e.g. Barbizon Light of New England, C Quinn Masonry Inc, Symetrica Inc. |
| portal_cka_california_open_35e42b9770 | organization | SUPPLIER_NAME org-token 58% (n=1000); e.g. City of Calexico, City of Arroyo Grande, California American Water Company - Sacr |
| portal_cka_california_open_f8f7b5716b | organization | SUPPLIER_NAME org-token 49% (n=808); e.g. Adelanto  City Of, Adelanto  City Of, Alameda County Water District |
| portal_cka_houston_open_dat_092dc52bc1 | organization | NAME org-token 100% (n=1000); e.g. Block Group 1; Census Tract 6701.01; For, Block Group 2; Census Tract 3433.01; Har, Block Group 3; Census Tract 6701.01; For |
| portal_cka_houston_open_dat_09fd7e454a | organization | DEPARTMENT_NAME org-token 76% (n=25); e.g. Houston Police Department, Department of Neighborhoods, Houston Fire Department |
| portal_cka_houston_open_dat_0a6665137f | organization | NAME org-token 100% (n=1000); e.g. Block Group 1; Census Tract 6920.04; Mon, Block Group 1; Census Tract 3409; Harris, Block Group 1; Census Tract 3129.01; Har |
| portal_cka_houston_open_dat_405fbdb44a | organization | NAME org-token 100% (n=1000); e.g. Block Group 1; Census Tract 5202; Harris, Block Group 2; Census Tract 4110.01; Har, Block Group 3; Census Tract 3311; Harris |
| portal_cka_houston_open_dat_442a765041 | organization | NAME org-token 100% (n=1000); e.g. Block Group 1; Census Tract 6701.01; For, Block Group 1; Census Tract 6942.04; Mon, Block Group 3; Census Tract 6701.01; For |
| portal_cka_houston_open_dat_48b03033d3 | organization | BUSINESS_AREA_TYPE org-token 65% (n=31); e.g. Public Safety, Human & Cultural Services, Public Safety |
| portal_cka_houston_open_dat_4df426d97d | organization | NAME org-token 100% (n=1000); e.g. Block Group 1; Census Tract 6701.01; For, Block Group 1; Census Tract 5325.03; Har, Block Group 3; Census Tract 6701.01; For |
| portal_cka_houston_open_dat_501ee45dc7 | organization | NAME org-token 100% (n=1000); e.g. Block Group 3; Census Tract 5410.04; Har, Block Group 1; Census Tract 4223.04; Har, Block Group 2; Census Tract 5518; Harris |
| portal_cka_houston_open_dat_583918009f | organization | NAME org-token 100% (n=1000); e.g. Block Group 1; Census Tract 5549.04; Har, Block Group 2; Census Tract 6701.01; For, Block Group 1; Census Tract 4518; Harris |
| portal_cka_houston_open_dat_5848c85560 | organization | COMPANY_OWNER org-token 72% (n=487); e.g. YELLOW CAB/UNITED TRANSPORTATION SERVICE, YELLOW CAB/UNITED TRANSPORTATION SERVICE, SUNSET CAB COMPANY |
| portal_cka_houston_open_dat_6082321c0c | organization | NAME org-token 100% (n=1000); e.g. Block Group 2; Census Tract 5548.09; Har, Block Group 1; Census Tract 5526.03; Har, Block Group 1; Census Tract 3430; Harris |
| portal_cka_houston_open_dat_76e445329f | organization | COMPANY_OWNER org-token 68% (n=439); e.g. SUNSET CAB COMPANY, FARLEY SCHOOL BUS SERVICE, YELLOW CAB/UNITED TRANSPORTATION SERVICE |
| portal_cka_houston_open_dat_95cc6891bd | organization | NAME org-token 100% (n=1000); e.g. Block Group 2; Census Tract 4203; Harris, Block Group 1; Census Tract 4329.04; Har, Block Group 3; Census Tract 6925.02; Mon |
| portal_cka_houston_open_dat_aefb1b6a56 | organization | NAME org-token 100% (n=1000); e.g. Block Group 1; Census Tract 6701.01; For, Block Group 2; Census Tract 6701.01; For, Block Group 3; Census Tract 6701.01; For |
| portal_cka_houston_open_dat_ebcdf36b9e | organization | NAME org-token 100% (n=1000); e.g. Block Group 3; Census Tract 4517; Harris, Block Group 2; Census Tract 6701.01; For, Block Group 3; Census Tract 6701.01; For |
| portal_cka_tampa_open_data_33f54db74c | organization | C_ORGANIZATION org-token 100% (n=1000); e.g. Solid Waste Department, Solid Waste Department, Solid Waste Department |
| portal_cka_tampa_open_data_39c5b89d70 | organization | C_ORGANIZATION org-token 90% (n=29); e.g. City of Tampa, City of Tampa, City of Tampa |
| portal_cka_tampa_open_data_6a2b19fd67 | organization | C_ORGANIZATION org-token 100% (n=477); e.g. Wastewater Department, Wastewater Department, Wastewater Department |
| portal_cka_tampa_open_data_8b7716d270 | organization | C_ORGANIZATION org-token 100% (n=316); e.g. Convention Center & Tourism, Convention Center & Tourism, Convention Center & Tourism |
| portal_cka_tampa_open_data_9909aa9ed8 | organization | C_ORGANIZATION org-token 100% (n=1000); e.g. Logistics & Asset Management (Logistics , Logistics & Asset Management, Logistics & Asset Management |
| portal_cka_tampa_open_data_a61789d619 | organization | C_ORGANIZATION org-token 100% (n=106); e.g. Police Department, Police Department, Police Department |
| portal_cka_tampa_open_data_ddbaf3b966 | organization | C_ORGANIZATION org-token 65% (n=88); e.g. Planning & Development (Development and , Development & Growth Mgmt, Development & Growth Mgmt |
| portal_cka_virginia_open_da_11b79485f6 | organization | APPLICANT org-token 59% (n=509); e.g. Giles County Industrial Development Auth, Joseph Colao, Fairfax County Park Authority |
| portal_cka_virginia_open_da_77706d86da | organization | SWC_OPE_NAME org-token 82% (n=1000); e.g. Barton Malow Co, Hourigan Construction Corporation, JE Liesfeld Contractor Inc |
| portal_cka_virginia_open_da_97ad4bc66c | organization | COUNTY_NAME org-token 100% (n=999); e.g. Augusta (CO), Chesterfield (CO), Spotsylvania (CO) |
| portal_cka_western_pennsylv_20e1a330ce | organization | LEGAL_NAME org-token 94% (n=526); e.g. Avalon Fuel Company, Neelkanth Ansh Enterprises Inc, 7 Eleven Inc |
| portal_cka_western_pennsylv_ef682f7e59 | organization | OWNER_NAME org-token 74% (n=413); e.g. MAO REALTY 2 LLC, PEMBROKE PROPERTIES LLC, 1 MARSHALL ROAD LLC |
| portal_cka_wprdc_allegheny_16a0bb67b4 | organization | LEGAL_NAME org-token 94% (n=526); e.g. Avalon Fuel Company, Neelkanth Ansh Enterprises Inc, 7 Eleven Inc |
| portal_cka_wprdc_allegheny_5b37a5568e | organization | OWNER_NAME org-token 74% (n=461); e.g. DAG REAL ESTATE LLC, RP2ALL LLC, HRLP FOURTH AVENUE LLC |
| portal_soc_connecticut_open_88b075d7af | organization | NAME org-token 90% (n=1000); e.g. SHPS, PLLC, 1690 NBA LLC, Barbs Beachside, LLC |
| portal_soc_new_york_state_o_0c94dd2b8a | organization | PERMIT_ISSUED_TO_NAME org-token 83% (n=1000); e.g. UNITED PARCEL SERVICE GENERAL SERVICES C, EXPRESSWAY RECYCLING INC., JOINTA GALUSHA, LLC |
| portal_soc_new_york_state_o_c08efa40c8 | organization | FACILITY_NAME org-token 46% (n=1000); e.g. SOUTHOLD GT FACILITY, FREEPORT POWER PLANT #1, FREEPORT POWER PLANT #1 |
| portal_soc_texas_open_data_0f8f4663c8 | organization | BUSINESS_TYPE org-token 100% (n=1000); e.g. TEXAS LIMITED LIABILITY COMPANY, FOREIGN PROFIT CORPORATION, FRGN LIMITED PRTNSHP |

## still UNKNOWN -- left NULL (190)

| source_id | reason |
|---|---|
| fed_cdc_wonder | no-strong-value-signal |
| fed_cisa_kev | no-strong-value-signal |
| fed_cms_main | no-strong-value-signal |
| fed_david_rumsey | no-strong-value-signal |
| fed_densho_ddr | no-strong-value-signal |
| fed_epa_echo | no-strong-value-signal |
| fed_fec_api | no-strong-value-signal |
| fed_fec_bulk_linkages | no-strong-value-signal |
| fed_fec_bulk_summary | no-strong-value-signal |
| fed_fec_committee_to_candidate | no-strong-value-signal |
| fed_fec_indiv_contributions | no-strong-value-signal |
| fed_grants_gov | no-strong-value-signal |
| fed_naag_multistate_settlements | no-strong-value-signal |
| fed_noaa_weather_api | no-strong-value-signal |
| fed_usgs_earthquakes | no-strong-value-signal |
| fed_usgs_minerals | no-strong-value-signal |
| fed_wpa_slave_narratives | no-strong-value-signal |
| intl_br_dados_gov | no-strong-value-signal |
| intl_ca_open_canada | no-strong-value-signal |
| intl_ch_opendataswiss | no-strong-value-signal |
| intl_cl_datosgob | no-strong-value-signal |
| intl_de_govdata | no-strong-value-signal |
| intl_ec_sercop | no-strong-value-signal |
| intl_embl_ensembl | no-strong-value-signal |
| intl_fr_data_gouv | no-strong-value-signal |
| intl_gem_hazard | no-strong-value-signal |
| intl_gr_datagov | no-strong-value-signal |
| intl_opensanctions | no-strong-value-signal |
| intl_ucdp_ged | no-strong-value-signal |
| portal_arc_atlanta_dataatla_1a7f4adc21 | no-strong-value-signal |
| portal_arc_atlanta_dataatla_4ab9f9e31e | no-strong-value-signal |
| portal_arc_atlanta_dataatla_79e3c7bd36 | no-strong-value-signal |
| portal_arc_atlanta_dataatla_a59db2e766 | no-strong-value-signal |
| portal_arc_atlanta_dataatla_de1e9d4350 | no-strong-value-signal |
| portal_arc_harris_county_op_1a53499962 | no-strong-value-signal |
| portal_arc_harris_county_op_2d6f9d0da7 | no-strong-value-signal |
| portal_arc_harris_county_op_3cfe4113ed | no-strong-value-signal |
| portal_arc_harris_county_op_3e1426df10 | no-strong-value-signal |
| portal_arc_harris_county_op_8549ec1226 | no-strong-value-signal |
| portal_arc_harris_county_op_d354d2d6e2 | no-strong-value-signal |
| portal_arc_harris_county_op_d9a3089ed0 | no-strong-value-signal |
| portal_arc_harris_county_op_ede1e11f9d | no-strong-value-signal |
| portal_arc_harris_county_op_f3d3a3ab57 | no-strong-value-signal |
| portal_arc_open_data_dc_582a28d212 | no-strong-value-signal |
| portal_arc_open_data_dc_59913164d2 | no-strong-value-signal |
| portal_arc_open_data_dc_74d9616143 | no-strong-value-signal |
| portal_arc_open_data_dc_e1dd5d3551 | no-strong-value-signal |
| portal_arc_open_data_dc_f37f5ddc3d | no-strong-value-signal |
| portal_arc_open_data_raleig_bbf9abca0d | no-strong-value-signal |
| portal_arc_orange_county_op_05390f8d55 | no-strong-value-signal |
| portal_arc_orange_county_op_0dea033879 | no-strong-value-signal |
| portal_arc_orange_county_op_41e4e2185f | no-strong-value-signal |
| portal_arc_orange_county_op_43a1fe3fbe | no-strong-value-signal |
| portal_arc_tn_data_tennesse_655f6bcc6d | no-strong-value-signal |
| portal_arc_wisconsin_open_d_022efd1ae5 | no-strong-value-signal |
| portal_arc_wisconsin_open_d_717f8037eb | no-strong-value-signal |
| portal_arc_wisconsin_open_d_b2efa24715 | no-strong-value-signal |
| portal_arc_wisconsin_open_d_d05399642c | no-strong-value-signal |
| portal_cka_analyze_boston_0f7b6b1f80 | no-strong-value-signal |
| portal_cka_analyze_boston_5ccb249b71 | no-strong-value-signal |
| portal_cka_analyze_boston_5fc2a4d010 | no-strong-value-signal |
| portal_cka_analyze_boston_7d75fd803f | no-strong-value-signal |
| portal_cka_analyze_boston_824b1b659e | no-strong-value-signal |
| portal_cka_analyze_boston_a6c2b4684a | no-strong-value-signal |
| portal_cka_analyze_boston_acca0df381 | no-strong-value-signal |
| portal_cka_analyze_boston_b6c7223760 | no-strong-value-signal |
| portal_cka_analyze_boston_bbe6f0fd04 | no-strong-value-signal |
| portal_cka_analyze_boston_db1aefd5b6 | no-strong-value-signal |
| portal_cka_analyze_boston_db29ec5366 | no-strong-value-signal |
| portal_cka_california_open_0ad648012f | no-strong-value-signal |
| portal_cka_california_open_3b70ad4f80 | no-strong-value-signal |
| portal_cka_california_open_490b55c81b | no-strong-value-signal |
| portal_cka_california_open_7f65d27db7 | no-strong-value-signal |
| portal_cka_california_open_ac6c9e2b47 | no-strong-value-signal |
| portal_cka_california_open_c65b641866 | no-strong-value-signal |
| portal_cka_houston_open_dat_1629ef6392 | no-strong-value-signal |
| portal_cka_houston_open_dat_19cbd263cc | no-strong-value-signal |
| portal_cka_houston_open_dat_2e1926ecb2 | no-strong-value-signal |
| portal_cka_houston_open_dat_399393985d | no-strong-value-signal |
| portal_cka_houston_open_dat_702315b033 | no-strong-value-signal |
| portal_cka_houston_open_dat_7a8148751c | no-strong-value-signal |
| portal_cka_houston_open_dat_aa67e5b416 | no-strong-value-signal |
| portal_cka_houston_open_dat_aeb065e230 | no-strong-value-signal |
| portal_cka_houston_open_dat_bdf3a70a86 | no-strong-value-signal |
| portal_cka_houston_open_dat_cfdcdf13fd | no-strong-value-signal |
| portal_cka_houston_open_dat_f572136326 | no-strong-value-signal |
| portal_cka_houston_open_dat_fb1f968c19 | no-strong-value-signal |
| portal_cka_indiana_data_hub_7747efe139 | no-strong-value-signal |
| portal_cka_ireland_national_f2efde1a8c | no-strong-value-signal |
| portal_cka_israel_national_05cd5564c6 | no-strong-value-signal |
| portal_cka_israel_national_07ec1af377 | no-strong-value-signal |
| portal_cka_israel_national_23ec89fe35 | no-strong-value-signal |
| portal_cka_israel_national_32cf786f4c | no-strong-value-signal |
| portal_cka_israel_national_338ef2b642 | no-strong-value-signal |
| portal_cka_israel_national_44788840fc | no-strong-value-signal |
| portal_cka_israel_national_50096ddb0e | no-strong-value-signal |
| portal_cka_israel_national_511b70eb2b | no-strong-value-signal |
| portal_cka_israel_national_6c5e40114c | no-strong-value-signal |
| portal_cka_israel_national_7362ebc06f | no-strong-value-signal |
| portal_cka_israel_national_964780e58d | no-strong-value-signal |
| portal_cka_israel_national_b37ba647d0 | no-strong-value-signal |
| portal_cka_israel_national_d59087e169 | no-strong-value-signal |
| portal_cka_israel_national_da3ca6db5d | no-strong-value-signal |
| portal_cka_israel_national_ee52e94997 | no-strong-value-signal |
| portal_cka_open_data_sa_5b3ce659e5 | no-strong-value-signal |
| portal_cka_open_data_sa_e846782f2c | no-strong-value-signal |
| portal_cka_san_jose_open_da_00b8041d47 | no-strong-value-signal |
| portal_cka_tampa_open_data_044202d137 | no-strong-value-signal |
| portal_cka_tampa_open_data_06c9cc7276 | no-strong-value-signal |
| portal_cka_tampa_open_data_18b980d54d | no-strong-value-signal |
| portal_cka_tampa_open_data_2ff7ba4861 | no-strong-value-signal |
| portal_cka_tampa_open_data_31262c6d5a | no-strong-value-signal |
| portal_cka_tampa_open_data_35b3415bb7 | no-strong-value-signal |
| portal_cka_tampa_open_data_3aa5c05b7d | no-strong-value-signal |
| portal_cka_tampa_open_data_456ec0addb | no-strong-value-signal |
| portal_cka_tampa_open_data_485b900d71 | no-strong-value-signal |
| portal_cka_tampa_open_data_662d0d6bcb | no-strong-value-signal |
| portal_cka_tampa_open_data_6c25ea91d4 | no-strong-value-signal |
| portal_cka_tampa_open_data_7b31b708c9 | no-strong-value-signal |
| portal_cka_tampa_open_data_c8043a5df9 | no-strong-value-signal |
| portal_cka_tampa_open_data_e00e42a7e9 | no-strong-value-signal |
| portal_cka_tampa_open_data_e290dd0b04 | no-strong-value-signal |
| portal_cka_tampa_open_data_e589c6750a | no-strong-value-signal |
| portal_cka_tampa_open_data_eaee1e870c | no-strong-value-signal |
| portal_cka_virginia_open_da_039aacd655 | no-strong-value-signal |
| portal_cka_virginia_open_da_1d39bdec50 | no-strong-value-signal |
| portal_cka_virginia_open_da_ac3869ee0e | no-strong-value-signal |
| portal_cka_virginia_open_da_ace8ac0352 | no-strong-value-signal |
| portal_cka_virginia_open_da_ae7dccb05b | no-strong-value-signal |
| portal_cka_virginia_open_da_e4498c978c | no-strong-value-signal |
| portal_cka_western_pennsylv_09335a764b | no-strong-value-signal |
| portal_cka_western_pennsylv_152133d5ed | no-strong-value-signal |
| portal_cka_western_pennsylv_20c6fc6029 | no-strong-value-signal |
| portal_cka_western_pennsylv_6a4c3e0e78 | no-strong-value-signal |
| portal_cka_western_pennsylv_769bebae41 | no-strong-value-signal |
| portal_cka_western_pennsylv_7bfb1a4c7d | no-strong-value-signal |
| portal_cka_western_pennsylv_7d8c19b074 | no-strong-value-signal |
| portal_cka_western_pennsylv_90a0a8b740 | no-strong-value-signal |
| portal_cka_western_pennsylv_9ef4c60f58 | no-strong-value-signal |
| portal_cka_western_pennsylv_a3b7349811 | no-strong-value-signal |
| portal_cka_western_pennsylv_aad84a1f6e | no-strong-value-signal |
| portal_cka_western_pennsylv_c7339fba3b | no-strong-value-signal |
| portal_cka_western_pennsylv_d7da51769c | no-strong-value-signal |
| portal_cka_western_pennsylv_ddb61776d0 | no-strong-value-signal |
| portal_cka_western_pennsylv_f6a018a1cb | no-strong-value-signal |
| portal_cka_western_pennsylv_f810addeec | no-strong-value-signal |
| portal_cka_western_pennsylv_f82e02e6b2 | no-strong-value-signal |
| portal_cka_western_pennsylv_fbecf42e16 | no-strong-value-signal |
| portal_cka_western_pennsylv_fd81b4fb82 | no-strong-value-signal |
| portal_cka_wprdc_allegheny_0cd6a9957c | no-strong-value-signal |
| portal_cka_wprdc_allegheny_1b2d51749e | no-strong-value-signal |
| portal_cka_wprdc_allegheny_1ba8209338 | no-strong-value-signal |
| portal_cka_wprdc_allegheny_415f1fe712 | no-strong-value-signal |
| portal_cka_wprdc_allegheny_4597fbdfe3 | no-strong-value-signal |
| portal_cka_wprdc_allegheny_49ed6437bf | no-strong-value-signal |
| portal_cka_wprdc_allegheny_508c030bd9 | no-strong-value-signal |
| portal_cka_wprdc_allegheny_692c217fc7 | no-strong-value-signal |
| portal_cka_wprdc_allegheny_7af23acd2f | no-strong-value-signal |
| portal_cka_wprdc_allegheny_7b65ae0cff | no-strong-value-signal |
| portal_cka_wprdc_allegheny_822e5dba4c | no-strong-value-signal |
| portal_cka_wprdc_allegheny_ae7030c35b | no-strong-value-signal |
| portal_cka_wprdc_allegheny_b20a13551f | no-strong-value-signal |
| portal_cka_wprdc_allegheny_b78655de4f | no-strong-value-signal |
| portal_cka_wprdc_allegheny_c96164a13d | no-strong-value-signal |
| portal_cka_wprdc_allegheny_cda9e537dc | no-strong-value-signal |
| portal_cka_wprdc_allegheny_da448e7083 | no-strong-value-signal |
| portal_cka_wprdc_allegheny_eef5b53bc5 | no-strong-value-signal |
| portal_cka_wprdc_allegheny_fa3191e7a1 | no-strong-value-signal |
| portal_soc_austin_open_data_0b4c639a1c | no-strong-value-signal |
| portal_soc_cambridge_open_d_8a1152140c | no-strong-value-signal |
| portal_soc_chicago_data_por_26de83baf4 | no-strong-value-signal |
| portal_soc_colorado_informa_239fba8b76 | no-strong-value-signal |
| portal_soc_colorado_informa_46101be391 | no-strong-value-signal |
| portal_soc_colorado_informa_6367a44c92 | no-strong-value-signal |
| portal_soc_colorado_informa_a50da9b699 | no-strong-value-signal |
| portal_soc_colorado_informa_b4dd509314 | no-strong-value-signal |
| portal_soc_colorado_informa_d017cfcf7f | no-strong-value-signal |
| portal_soc_colorado_informa_f0e162d7a8 | no-strong-value-signal |
| portal_soc_colorado_informa_f78543c045 | no-strong-value-signal |
| portal_soc_colorado_informa_f9498d9b7f | no-strong-value-signal |
| portal_soc_new_york_state_o_eff72c4402 | no-strong-value-signal |
| portal_soc_open_data_br_6083bc2934 | no-strong-value-signal |
| portal_soc_texas_open_data_24c81c0c8a | no-strong-value-signal |
| portal_soc_utah_open_data_p_1614522f52 | no-strong-value-signal |
| portal_soc_utah_open_data_p_589cc47a29 | no-strong-value-signal |
| portal_soc_utah_open_data_p_81a81b1650 | no-strong-value-signal |
| portal_soc_utah_open_data_p_8de28da9d9 | no-strong-value-signal |
| portal_soc_washington_state_11cd1995b7 | no-strong-value-signal |
| portal_soc_washington_state_48eeef5dfc | no-strong-value-signal |
| xc_wapo_fatal_force | no-strong-value-signal |
