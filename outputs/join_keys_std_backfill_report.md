# JOIN_KEYS_STD backfill report

WRITE 82 | SKIP_MEASURED 58 | SKIP_NO_MEASURE 60 | NO_TABLE 0 | NO_REGISTRY_ROW 0

## WOULD WRITE (provisional -> measured)

| source_id | current | measured keys | tier | confirmed columns |
|---|---|---|---|---|
| fed_bia_tribal_geo | (empty) | GEOM,NAME | GEO | LAYER_NAME=NAME(100.0%/6d); NAME=NAME(48.0%/44d); GEOMETRY=GEOM(39.0%/29d) |
| fed_bls_qcew | (empty) | FIPS | GEO | AREA_FIPS=FIPS(100.0%/3773d) |
| fed_bop_statistics | (empty) | NAME | PROBABILISTIC | METRIC_NAME=NAME(100.0%/11d) |
| fed_cdc_drug_poisoning_county | (empty) | FIPS | GEO | FIPS=FIPS(100.0%/3149d); FIPS_STATE=FIPS(100.0%/51d) |
| fed_cdc_injury_violence_county | (empty) | FIPS,NAME | GEO | GEOID=FIPS(100.0%/3153d); NAME=NAME(100.0%/1837d); ST_GEOID=FIPS(100.0%/51d); ST_NAME=NAME(100.0%/51d) |
| fed_cdc_overdose | (empty) | NAME | PROBABILISTIC | STATE_NAME=NAME(100.0%/54d) |
| fed_cdc_suicide_rates | (empty) | NAME | PROBABILISTIC | STUB_NAME=NAME(100.0%/12d); STUB_NAME_NUM=NAME(100.0%/12d) |
| fed_cfpb_hmda | (empty) | LEI,NAME | STEEL | LEI=LEI(100.0%/531d); APPLICANT_CREDIT_SCORE_TYPE=NAME(100.0%/11d); CO_APPLICANT_CREDIT_SCORE_TYPE=NAME(100.0%/12d); APPLICANT_ETHNICITY_1=NAME(99.96%/8d); APPLICANT_ETHNICITY_2=NAME(2.94%/6d); CO_APPLICANT_ETHNICITY_1=NAME(100.0%/9d); CO_APPLICANT_ETHNICITY_2=NAME(0.98%/5d); APPLICANT_ETHNICITY_OBSERVED=NAME(100.0%/3d); CO_APPLICANT_ETHNICITY_OBSERVED=NAME(100.0%/4d); APPLICANT_RACE_1=NAME(99.99%/15d) |
| fed_cisa_kev | (empty) | NAME | PROBABILISTIC | VENDOR_PROJECT=NAME(100.0%/266d); VULNERABILITY_NAME=NAME(100.0%/1265d) |
| fed_cms_hospital_compare | (empty) | ZIP,ADDRESS,NAME | GEO | FACILITY_NAME=NAME(100.0%/5286d); ADDRESS=ADDRESS(100.0%/5441d); ZIP_CODE=ZIP(100.0%/4872d) |
| fed_cms_medicare_provider | (empty) | NPI,COUNTRY,FIPS,ZIP,NAME | STEEL | NPI=NPI(100.0%/49846d); RNDRNG_PRVDR_LAST_ORG_NAME=NAME(99.98%/27642d); RNDRNG_PRVDR_FIRST_NAME=NAME(95.24%/9938d); RNDRNG_PRVDR_STATE_FIPS=FIPS(100.0%/59d); RNDRNG_PRVDR_ZIP5=ZIP(100.0%/9572d); RNDRNG_PRVDR_CNTRY=COUNTRY(100.0%/6d) |
| fed_cms_open_payments | (empty) | NPI,COUNTRY,ZIP,NAME | STEEL | COVERED_RECIPIENT_TYPE=NAME(100.0%/3d); COVERED_RECIPIENT_PROFILE_ID=NAME(99.77%/43524d); NPI=NPI(99.69%/43884d); COVERED_RECIPIENT_FIRST_NAME=NAME(99.76%/9376d); COVERED_RECIPIENT_MIDDLE_NAME=NAME(39.85%/3324d); COVERED_RECIPIENT_LAST_NAME=NAME(99.73%/23890d); RECIPIENT_PRIMARY_BUSINESS_STREET_ADDRESS_LINE1=NAME(100.0%/34598d); RECIPIENT_PRIMARY_BUSINESS_STREET_ADDRESS_LINE2=NAME(19.49%/3098d); RECIPIENT_CITY=NAME(100.0%/4275d); RECIPIENT_STATE=NAME(91.0%/51d); RECIPIENT_ZIP_CODE=ZIP(100.0%/8470d); RECIPIENT_COUNTRY=COUNTRY(100.0%/2d) |
| fed_cms_open_payments_2023 | (empty) | NPI,ZIP,NAME | STEEL | COVERED_RECIPIENT_TYPE=NAME(100.0%/3d); COVERED_RECIPIENT_PROFILE_ID=NAME(99.82%/43789d); NPI=NPI(99.74%/43779d); COVERED_RECIPIENT_FIRST_NAME=NAME(99.82%/9279d); COVERED_RECIPIENT_MIDDLE_NAME=NAME(38.15%/3067d); COVERED_RECIPIENT_LAST_NAME=NAME(99.78%/24034d); RECIPIENT_PRIMARY_BUSINESS_STREET_ADDRESS_LINE1=NAME(100.0%/35418d); RECIPIENT_PRIMARY_BUSINESS_STREET_ADDRESS_LINE2=NAME(20.68%/3259d); RECIPIENT_CITY=NAME(100.0%/4206d); RECIPIENT_STATE=NAME(91.11%/51d); RECIPIENT_ZIP_CODE=ZIP(100.0%/8453d) |
| fed_cms_part_d_prescribers | (empty) | NPI,COUNTRY,FIPS,ZIP,NAME | STEEL | NPI=NPI(100.0%/50572d); PRSCRBR_LAST_ORG_NAME=NAME(99.95%/27657d); PRSCRBR_FIRST_NAME=NAME(100.0%/10804d); PRSCRBR_STATE_FIPS=FIPS(99.9%/55d); PRSCRBR_ZIP5=ZIP(100.0%/9815d); PRSCRBR_CNTRY=COUNTRY(100.0%/6d) |
| fed_congress_legislators | (empty) | BIOGUIDE,ICPSR,NAME | STEEL | BIOGUIDE=BIOGUIDE(99.9%/12853d); ICPSR=ICPSR(96.12%/12182d); NAME_FIRST=NAME(100.0%/1719d); NAME_LAST=NAME(100.0%/5932d); NAME_OFFICIAL_FULL=NAME(8.86%/1143d) |
| fed_dhs_ohss | (empty) | NAME | PROBABILISTIC | SOURCE_FILE_NAME=NAME(100.0%/13d); SOURCE_SHEET_NAME=NAME(100.0%/50d) |
| fed_dol_form5500 | (empty) | EIN,ZIP,NAME | STEEL | PLAN_NAME=NAME(100.0%/31033d); SPONSOR_DFE_NAME=NAME(99.99%/28568d); SPONS_DFE_DBA_NAME=NAME(5.83%/1576d); SPONS_DFE_CARE_OF_NAME=NAME(3.06%/825d); SPONS_DFE_MAIL_US_ZIP=ZIP(99.58%/10198d); SPONS_DFE_LOC_US_ZIP=ZIP(8.44%/1888d); SPONS_DFE_EIN=EIN(100.0%/29301d); ADMIN_NAME=NAME(3.49%/695d); ADMIN_US_ZIP=ZIP(3.49%/592d) |
| fed_dol_oflc | (empty) | NAICS,COUNTRY,ZIP,NAME | STRONG | CHANGE_EMPLOYER=NAME(100.0%/19d); EMPLOYER_NAME=NAME(100.0%/14579d); EMPLOYER_BUSINESS_DBA=NAME(7.83%/2050d); EMPLOYER_ADDRESS1=NAME(100.0%/14069d); EMPLOYER_ADDRESS2=NAME(46.38%/2257d); EMPLOYER_CITY=NAME(100.0%/2134d); EMPLOYER_STATE=NAME(92.33%/51d); EMPLOYER_POSTAL_CODE=NAME(100.0%/4637d); EMPLOYER_COUNTRY=COUNTRY(95.8%/4d); EMPLOYER_PROVINCE=NAME(0.76%/102d); EMPLOYER_PHONE=NAME(95.8%/14832d); EMPLOYER_PHONE_EXT=NAME(4.14%/349d); NAICS_CODE=NAICS(100.0%/1205d); AGENT_REPRESENTING_EMPLOYER=NAME(95.8%/2d); AGENT_ATTORNEY_LAW_FIRM_BUSINESS_NAME=NAME(67.38%/2448d); AGENT_ATTORNEY_POSTAL_CODE=ZIP(55.36%/1083d) |
| fed_dot_bts | (empty) | NAME | PROBABILISTIC | DATABASE_NAME=NAME(100.0%/21d) |
| fed_eac_eavs | (empty) | NAME | PROBABILISTIC | JURISDICTION_NAME=NAME(100.0%/5261d) |
| fed_ed_edfacts | (empty) | NAME | PROBABILISTIC | AGENCY_NAME=NAME(33.33%/10d) |
| fed_epa_echo | (empty) | NAICS,SIC,COUNTRY,FIPS,LATLON,ZIP,ADDRESS,NAME | STRONG | FAC_NAME=NAME(100.0%/46841d); FAC_STREET=ADDRESS(88.0%/42294d); FAC_ZIP=ZIP(88.14%/14871d); FAC_FIPS_CODE=FIPS(90.06%/2841d); FAC_INDIAN_CNTRY_FLG=COUNTRY(100.0%/2d); FAC_LAT=LATLON(98.16%/41894d); FAC_DERIVED_STCTY_FIPS=FIPS(80.41%/2694d); FAC_DERIVED_ZIP=ZIP(80.38%/13508d); CAA_NAICS=NAICS(8.5%/726d); CWA_NAICS=NAICS(8.23%/459d); RCRA_NAICS=NAICS(32.99%/2327d); FAC_SIC_CODES=SIC(26.77%/1586d); FAC_NAICS_CODES=NAICS(48.65%/3527d) |
| fed_faa_registry | (empty) | COUNTRY,ZIP,ADDRESS,NAME | GEO | NAME=NAME(98.55%/38512d); STREET=ADDRESS(98.54%/36705d); ZIP_CODE=ZIP(98.47%/14313d); COUNTRY=COUNTRY(98.55%/23d) |
| fed_fara | (empty) | NAME | PROBABILISTIC | REGISTRANT_NAME=NAME(100.0%/30d) |
| fed_fcc_licensing | (empty) | ZIP,ADDRESS,NAME | GEO | ENTITY_NAME=NAME(99.69%/49772d); ADDRESS_LINE1=ADDRESS(91.73%/45286d); ZIP_CODE=ZIP(98.72%/16341d); APPLICANT_TYPE_CODE=NAME(99.76%/5d) |
| fed_fec_bulk_candidates | ZIP | ZIP,NAME | GEO | CAND_NAME=NAME(99.99%/12251d); CAND_ZIP=ZIP(99.28%/7619d) |
| fed_fhfa_hpi | (empty) | NAME | PROBABILISTIC | PLACE_NAME=NAME(100.0%/479d) |
| fed_fhfa_nmdb | (empty) | NAME | PROBABILISTIC | GEO_NAME=NAME(100.0%/68d) |
| fed_ftc_datasets | (empty) | NAME | PROBABILISTIC | ACTION_NAME=NAME(100.0%/993d) |
| fed_hrsa_shortage_areas | (empty) | FIPS,LATLON,ZIP,ADDRESS,NAME | GEO | HPSA_NAME=NAME(100.0%/13339d); LONGITUDE=LATLON(13.59%/4937d); LATITUDE=LATLON(13.59%/4948d); BHCMIS_ORGANIZATION_IDENTIFICATION_NUMBER=NAME(3.1%/1111d); COMMON_COUNTY_NAME=NAME(100.0%/3113d); COMMON_POSTAL_CODE=ZIP(13.17%/3635d); COMMON_REGION_NAME=NAME(100.0%/11d); COMMON_STATE_COUNTY_FIPS_CODE=FIPS(100.0%/3129d); COMMON_STATE_FIPS_CODE=FIPS(100.0%/59d); COMMON_STATE_NAME=NAME(100.0%/60d); COUNTY_EQUIVALENT_NAME=NAME(100.0%/1911d); HPSA_ADDRESS=ADDRESS(13.06%/4453d); HPSA_COMPONENT_NAME=NAME(100.0%/28288d); HPSA_POSTAL_CODE=ZIP(13.17%/3635d); PRIMARY_STATE_FIPS_CODE=FIPS(100.0%/59d); PRIMARY_STATE_NAME=NAME(100.0%/60d) |
| fed_hud_data | (empty) | NAME | PROBABILISTIC | DATASET_NAME=NAME(100.0%/65d) |
| fed_ice_statistics | (empty) | COUNTRY | GEO | COUNTRY_OF_CITIZENSHIP=COUNTRY(89.14%/196d) |
| fed_irs_990 | (empty) | EIN | STEEL | EIN=EIN(100.0%/200d) |
| fed_irs_bmf | (empty) | EIN,ZIP,ADDRESS,NAME | STEEL | EIN=EIN(100.0%/49785d); NAME=NAME(100.0%/45121d); STREET=ADDRESS(100.0%/42617d); ZIP=ZIP(100.0%/16975d); C_ORGANIZATION=NAME(100.0%/7d); SORT_NAME=NAME(21.36%/10437d) |
| fed_irs_eo_bmf | (empty) | EIN,ZIP,ADDRESS,NAME | STEEL | EIN=EIN(100.0%/50114d); NAME=NAME(100.0%/43877d); STREET=ADDRESS(100.0%/42876d); ZIP=ZIP(100.0%/17465d); C_ORGANIZATION=NAME(100.0%/7d); SORT_NAME=NAME(21.3%/10618d) |
| fed_irs_revocation | (empty) | EIN,COUNTRY,ZIP,ADDRESS,NAME | STEEL | EIN=EIN(100.0%/50009d); LEGAL_NAME=NAME(100.0%/44051d); DBA_NAME=NAME(20.43%/9864d); ORG_ADDRESS=ADDRESS(99.83%/43531d); ZIP_CODE=ZIP(100.0%/17086d); COUNTRY=COUNTRY(100.0%/31d) |
| fed_irs_soi | (empty) | FIPS,ZIP | GEO | STATE_FIPS=FIPS(100.0%/51d); ZIP_CODE=ZIP(92.15%/26379d) |
| fed_medsl_house_returns | FIPS | FIPS | GEO | STATE_FIPS=FIPS(100.0%/50d) |
| fed_medsl_president_returns | FIPS | FIPS | GEO | STATE_FIPS=FIPS(100.0%/51d) |
| fed_medsl_senate_returns | FIPS | FIPS | GEO | STATE_FIPS=FIPS(100.0%/50d) |
| fed_nasa_open_data | (empty) | NAME | PROBABILISTIC | API_NAME=NAME(100.0%/2d) |
| fed_ncua_call_reports | (empty) | ZIP,NAME | GEO | CU_NAME=NAME(99.96%/5907d); ZIP_CODE=ZIP(99.96%/4477d); TABLE_NAME=NAME(100.0%/20d) |
| fed_noaa_storm_events | (empty) | FIPS,LATLON,NAME | GEO | STATE_FIPS=FIPS(100.0%/68d); MONTH_NAME=NAME(100.0%/12d); CZ_FIPS=FIPS(100.0%/576d); CZ_NAME=NAME(100.0%/3699d); BEGIN_LAT=LATLON(58.61%/10683d); BEGIN_LON=LATLON(58.61%/12592d); END_LAT=LATLON(58.61%/11681d); END_LON=LATLON(58.61%/13584d) |
| fed_noaa_weather_api | (empty) | GEOM,NAME | GEO | SENDER_NAME=NAME(100.0%/74d); GEOMETRY=GEOM(10.8%/31d) |
| fed_nsf_awards | (empty) | ZIP,NAME | GEO | AWARDEE_NAME=NAME(100.0%/98d); PI_NAME=NAME(100.0%/115d); PROGRAM_NAME=NAME(100.0%/38d); ZIP=ZIP(100.0%/93d) |
| fed_nursinghome411 | (empty) | CCN,LATLON,ADDRESS,NAME | STEEL | CMS_CERTIFICATION_NUMBER_CCN=CCN(100.0%/14345d); PROVIDER_NAME=NAME(100.0%/14453d); PROVIDER_ADDRESS=ADDRESS(100.0%/15085d); CHAIN_NAME=NAME(69.07%/624d); LATITUDE=LATLON(100.0%/13713d); LONGITUDE=LATLON(100.0%/10480d) |
| fed_ofac_sdn | IMO | IMO,NAME | STEEL | SDN_NAME=NAME(99.99%/18896d); IMO=IMO(10.63%/2039d) |
| fed_pbgc_data | (empty) | NAME | PROBABILISTIC | TABLE_NAME=NAME(100.0%/85d); METRIC_NAME=NAME(80.08%/576d) |
| fed_sba_loans | (empty) | ZIP,ADDRESS,NAME | GEO | CDC_NAME=NAME(10.3%/198d); CDC_STREET=ADDRESS(9.96%/192d); CDC_ZIP=ZIP(9.46%/173d); THIRDPARTYLENDER_NAME=NAME(5.44%/992d) |
| fed_sec_edgar | (empty) | CIK,EIN,SIC | STEEL | CIK=CIK(100.0%/20d); EIN=EIN(95.0%/19d); SIC=SIC(100.0%/13d) |
| fed_sec_edgar_financials | (empty) | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/8169d); NAME=NAME(100.0%/8345d); SIC=SIC(97.92%/404d); EIN=EIN(77.55%/5783d) |
| fed_us_sec_edgar | (empty) | CIK,EIN,SIC,ADDRESS,NAME | STEEL | CIK=CIK(100.0%/25d); ENTITY_NAME=NAME(100.0%/25d); SIC_CODE=SIC(100.0%/15d); BUSINESS_ADDRESS=ADDRESS(100.0%/25d); EIN=EIN(98.8%/24d) |
| fed_us_usaspending_api | (empty) | NAME | PROBABILISTIC | RECIPIENT_NAME=NAME(100.0%/146d); AWARDING_AGENCY_NAME=NAME(100.0%/13d); FUNDING_AGENCY_NAME=NAME(100.0%/13d) |
| fed_usaspending_contracts | DUNS,FIPS,NAICS,UEI | UEI,NAICS,COUNTRY,ZIP,NAME | STEEL | AWARDING_AGENCY_NAME=NAME(100.0%/52d); AWARDING_SUB_AGENCY_NAME=NAME(100.0%/134d); FUNDING_AGENCY_NAME=NAME(100.0%/58d); RECIPIENT_UEI=UEI(100.0%/7634d); RECIPIENT_NAME=NAME(100.0%/7294d); RECIPIENT_DOING_BUSINESS_AS_NAME=NAME(5.5%/637d); RECIPIENT_PARENT_UEI=UEI(99.99%/7116d); RECIPIENT_PARENT_NAME=NAME(99.99%/6991d); RECIPIENT_CITY_NAME=NAME(100.0%/2520d); RECIPIENT_STATE_CODE=NAME(82.98%/50d); RECIPIENT_ZIP_4_CODE=ZIP(98.79%/4313d); RECIPIENT_COUNTRY_NAME=COUNTRY(100.0%/75d); PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME=NAME(96.9%/2276d); NAICS_CODE=NAICS(99.98%/655d); NAICS_DESCRIPTION=NAICS(99.98%/643d) |
| fed_usgs_earthquakes | (empty) | LATLON | GEO | LATITUDE=LATLON(100.0%/45053d); LONGITUDE=LATLON(100.0%/47117d) |
| fed_usgs_minerals | (empty) | COUNTRY,LATLON,NAME | GEO | COUNTRY=COUNTRY(99.99%/140d); SITE_NAME=NAME(99.99%/36446d); LATITUDE=LATLON(99.99%/45958d); LONGITUDE=LATLON(99.99%/47040d) |
| fed_usgs_water | (empty) | LATLON,NAME | GEO | SITE_NAME=NAME(100.0%/3706d); PARAMETER_NAME=NAME(100.0%/4d); LATITUDE=LATLON(100.0%/3741d); LONGITUDE=LATLON(100.0%/3652d) |
| fed_voteview_members | (empty) | BIOGUIDE,ICPSR | STEEL | ICPSR=ICPSR(100.0%/12500d); BIOGUIDE_ID=BIOGUIDE(99.87%/12553d) |
| fed_voteview_rollcalls | (empty) | ICPSR | STEEL | ICPSR=ICPSR(100.0%/638d) |
| intl_adb_data | (empty) | NAME | PROBABILISTIC | PROJECT_NAME=NAME(34.15%/2d) |
| intl_ar_datosgob | (empty) | NAME | PROBABILISTIC | C_ORGANIZATION=NAME(93.7%/31d) |
| intl_eg_capmas | (empty) | NAME | PROBABILISTIC | INDICATOR_NAME=NAME(100.0%/3d) |
| intl_embl_ensembl | (empty) | NAME | PROBABILISTIC | SEQ_REGION_NAME=NAME(100.0%/11d); SOURCE_NAME=NAME(100.0%/4d) |
| intl_eu_sanctions | (empty) | COUNTRY,ZIP,ADDRESS,NAME | GEO | NAAL_LASTNAME=NAME(15.55%/4157d); NAAL_FIRSTNAME=NAME(15.52%/2047d); ADDR_LOGICAL_ID=ADDRESS(5.77%/2457d); ADDR_LEBA_NUMTITLE=ADDRESS(5.77%/377d); ADDR_LEBA_PUBLICATION_DATE=ADDRESS(5.77%/321d); ADDR_LEBA_URL=ADDRESS(5.77%/368d); ADDR_PROGRAMME=ADDRESS(5.77%/33d); ADDR_STREET=ADDRESS(4.15%/1702d); ADDR_ZIPCODE=ZIP(1.66%/486d); ADDR_CITY=ADDRESS(4.64%/652d); ADDR_COUNTRY=COUNTRY(5.57%/89d); ADDR_OTHER=ADDRESS(2.34%/862d); BIRT_COUNTRY=COUNTRY(6.17%/82d); IDEN_COUNTRY=COUNTRY(3.39%/70d); CITI_COUNTRY=COUNTRY(6.38%/85d) |
| intl_fatf_ratings | (empty) | COUNTRY | GEO | COUNTRY=COUNTRY(100.0%/151d) |
| intl_fr_data_gouv | (empty) | NAME | PROBABILISTIC | ORGANIZATION_ID=NAME(95.05%/354d); ORGANIZATION_NAME=NAME(95.05%/352d) |
| intl_freedomhouse | (empty) | COUNTRY | GEO | COUNTRY_TERRITORY=COUNTRY(100.0%/208d) |
| intl_gdelt | (empty) | COUNTRY,LATLON,NAME | GEO | ACTOR1NAME=NAME(89.26%/217d); ACTOR1COUNTRYCODE=COUNTRY(54.88%/40d); ACTOR2NAME=NAME(0.79%/3d); ACTOR1GEO_LAT=LATLON(88.57%/76d); ACTOR2GEO_FULLNAME=NAME(100.0%/4d); ACTOR2GEO_LAT=LATLON(100.0%/19d); ACTIONGEO_FULLNAME=NAME(100.0%/201d) |
| intl_gem_hazard | (empty) | COUNTRY | GEO | COUNTRY=COUNTRY(100.0%/12d) |
| intl_gleif | (empty) | LEI,COUNTRY,ADDRESS,NAME | STEEL | LEI=LEI(100.0%/19853d); ENTITY_LEGAL_NAME=NAME(98.42%/19822d); ENTITY_LEGAL_ADDRESS=ADDRESS(100.0%/13201d); ENTITY_HEADQUARTERS_ADDRESS=ADDRESS(100.0%/15908d); ENTITY_COUNTRY=COUNTRY(100.0%/167d) |
| intl_global_witness_defenders | (empty) | COUNTRY | GEO | COUNTRY=COUNTRY(21.55%/6d) |
| intl_ie_cro | (empty) | NAME | PROBABILISTIC | COMPANY_NUM=NAME(100.0%/50029d); COMPANY_NAME=NAME(100.0%/50172d); COMPANY_STATUS_CODE=NAME(100.0%/19d); COMPANY_STATUS=NAME(100.0%/13d); COMPANY_TYPE_CODE=NAME(100.0%/36d); COMPANY_TYPE=NAME(100.0%/33d); COMPANY_REG_DATE=NAME(97.94%/11722d); COMPANY_ADDRESS_1=NAME(100.0%/29800d); COMPANY_ADDRESS_2=NAME(92.82%/12413d); COMPANY_ADDRESS_3=NAME(69.52%/4799d); COMPANY_ADDRESS_4=NAME(96.85%/2795d); COMPANY_STATUS_DATE=NAME(60.48%/3883d); COMPANY_NAME_EFF_DATE=NAME(97.93%/11559d); COMPANY_TYPE_EFF_DATE=NAME(97.93%/10723d) |
| intl_ipc_food_insecurity_global | (empty) | COUNTRY | GEO | COUNTRY=COUNTRY(100.0%/50d) |
| intl_nti_cns_dprk_missile_tests | (empty) | LATLON,NAME | GEO | MISSILE_NAME=NAME(100.0%/37d); FACILITY_NAME=NAME(100.0%/48d); OTHER_NAME=NAME(28.71%/20d); FACILITY_LATITUDE=LATLON(94.72%/45d); FACILITY_LONGITUDE=LATLON(94.72%/47d) |
| intl_opensanctions | (empty) | NAME | PROBABILISTIC | NAME=NAME(76.9%/36096d) |
| intl_ucdp_ged | (empty) | COUNTRY,GEOM,LATLON,NAME | GEO | CONFLICT_NAME=NAME(100.0%/1128d); DYAD_NAME=NAME(100.0%/1317d); LATITUDE=LATLON(100.0%/14958d); LONGITUDE=LATLON(100.0%/14818d); GEOM_WKT=GEOM(100.0%/15355d); COUNTRY=COUNTRY(100.0%/103d) |
| intl_wb_ids | (empty) | COUNTRY,NAME | GEO | COUNTRY_NAME=COUNTRY(99.99%/133d); COUNTRY_CODE=COUNTRY(99.99%/136d); SERIES_NAME=NAME(99.99%/576d) |
| st_cannabis_policy_bundles | (empty) | FIPS | GEO | FIPS=FIPS(100.0%/50d) |
| xc_jcs_coa | (empty) | NAME | PROBABILISTIC | NAME=NAME(100.0%/701d) |
| xc_ransomwarelive_victims | (empty) | COUNTRY,NAME | GEO | GROUP_NAME=NAME(100.0%/332d); COUNTRY=COUNTRY(72.9%/190d) |
| xc_vera_incarceration_trends | (empty) | FIPS,NAME | GEO | COUNTY_FIPS=FIPS(100.0%/3069d); COUNTY_NAME=NAME(100.0%/1777d); STATE_FIPS=FIPS(100.0%/45d) |
| xc_wapo_fatal_force | (empty) | LATLON,NAME | GEO | LATITUDE=LATLON(89.07%/9285d); LONGITUDE=LATLON(89.06%/9273d); NAME=NAME(96.95%/10130d) |

## SKIP -- provisional but no key survived value-measurement

| source_id | name-detected but rejected |
|---|---|
| fed_cbp_encounters | (no key-named columns) |
| fed_cdc_anxiety_depression | (no key-named columns) |
| fed_cdc_data_portal | FIPS=FIPS(0.0%/0d); ZIP_CODE=ZIP(0.0%/0d) |
| fed_cdc_health_insurance | (no key-named columns) |
| fed_cdc_wonder | (no key-named columns) |
| fed_cms_hpt_mrf | HOSPITAL_NAME=NAME(0.0%/0d); HOSPITAL_ADDRESS=ADDRESS(0.0%/0d); NPI=NPI(0.0%/0d); ATTESTER_NAME=NAME(0.0%/0d); PAYER_NAME=NAME(0.0%/0d); PLAN_NAME=NAME(0.0%/0d) |
| fed_cms_main | NPI=NPI(0.0%/0d); FIPS=FIPS(0.0%/0d); ZIP=ZIP(0.0%/0d) |
| fed_cms_nadac | (no key-named columns) |
| fed_david_rumsey | (no key-named columns) |
| fed_densho_ddr | FIPS=FIPS(0.0%/0d) |
| fed_dhs_yearbook | COUNTRY_OF_BIRTH=COUNTRY(0.0%/0d); COUNTRY_OF_LAST_RESIDENCE=COUNTRY(0.0%/0d); TABLE_NAME=NAME(0.0%/0d) |
| fed_docsouth | (no key-named columns) |
| fed_eoir_case_data | (no key-named columns) |
| fed_faa_data_portal | DATASET_NAME=NAME(100.0%/3d); FIPS=FIPS(0.0%/0d); LAT=LATLON(0.0%/0d); LON=LATLON(0.0%/0d) |
| fed_fbi_cde | AGENCY_NAME=NAME(0.0%/0d); FIPS_STATE_CODE=FIPS(0.0%/0d); FIPS_COUNTY_CODE=FIPS(0.0%/0d); OFFENSE_NAME=NAME(0.0%/0d) |
| fed_fbi_nics_checks | (no key-named columns) |
| fed_fec_bulk_linkages | (no key-named columns) |
| fed_ffiec_call_reports | INSTITUTION_NAME=NAME(0.0%/0d) |
| fed_fincen_boi | REPORTING_COMPANY_NAME=NAME(100.0%/1d); EIN=EIN(0.0%/0d); BENEFICIAL_OWNER_FULL_NAME=NAME(0.0%/0d); BENEFICIAL_OWNER_ADDRESS=ADDRESS(0.0%/0d) |
| fed_foreignassistance | COUNTRY=COUNTRY(0.0%/0d); EIN=EIN(0.0%/0d) |
| fed_fra_safety | RAILROAD_NAME=NAME(100.0%/1d); STATE_FIPS=FIPS(100.0%/1d); COUNTY_FIPS=FIPS(100.0%/1d) |
| fed_grants_gov | AGENCY_NAME=NAME(0.0%/0d); GRANTOR_CONTACT_NAME=NAME(0.0%/0d) |
| fed_naag_multistate_settlements | (no key-named columns) |
| fed_sba_ppp | (no key-named columns) |
| fed_slavevoyages_intraamerican | (no key-named columns) |
| fed_slavevoyages_transatlantic | (no key-named columns) |
| fed_uscis_data | COUNTRY=COUNTRY(0.0%/0d) |
| fed_uscourts_stats | PUBLICATION_NAME=NAME(0.0%/0d); FIPS_CODE=FIPS(0.0%/0d) |
| fed_usgs_topoview | FIPS=FIPS(0.0%/0d) |
| fed_va_allcause_mortality | (no key-named columns) |
| fed_va_suicide_appendix | (no key-named columns) |
| fed_voteview_rollcall_meta | (no key-named columns) |
| intl_austlii | (no key-named columns) |
| intl_br_dados_gov | C_ORGANIZATION=NAME(0.0%/0d) |
| intl_eu_socta_europol | (no key-named columns) |
| intl_eurlex_cellar | COUNTRY=COUNTRY(0.0%/0d) |
| intl_eurostat | (no key-named columns) |
| intl_fao_faostat | (no key-named columns) |
| intl_fao_faostat_food_security | (no key-named columns) |
| intl_ge_datagov | COUNTRY=COUNTRY(100.0%/1d) |
| intl_gfi_trade | COUNTRY=COUNTRY(0.0%/0d) |
| intl_gh_datagovgh | (no key-named columns) |
| intl_leiden_russian_ops_europe | (no key-named columns) |
| intl_owid_milspend | (no key-named columns) |
| intl_voeten_unga_votes | (no key-named columns) |
| xc_guttmacher_monthly_abortion | (no key-named columns) |
| xc_jcs_medians | (no key-named columns) |
| xc_nagix_dprk_missile_tests | (no key-named columns) |
| xc_owid_ai_incidents_annual | (no key-named columns) |
| xc_owid_co2 | (no key-named columns) |
| xc_owid_cpi | (no key-named columns) |
| xc_owid_fertility | (no key-named columns) |
| xc_owid_fossil_share | (no key-named columns) |
| xc_owid_gini | (no key-named columns) |
| xc_owid_homicide | (no key-named columns) |
| xc_owid_life_expectancy | (no key-named columns) |
| xc_owid_nuclear_warheads | (no key-named columns) |
| xc_owid_refugees | REFUGEES_BY_COUNTRY_OF_ORIGIN=COUNTRY(0.0%/0d) |
| xc_owid_temp_anomaly | (no key-named columns) |
| xc_owid_terrorism_deaths | (no key-named columns) |

## SKIP -- already measured (provisional=FALSE, untouched)

- fed_cfpb_complaints (NAME,ZIP / GEO)
- fed_clinicaltrials (NAME,NPI / STEEL)
- fed_cms_dialysis (ADDRESS,CCN,NAME,ZIP / STEEL)
- fed_cms_facility_affiliation (CCN,NAME,NPI / STEEL)
- fed_cms_hcris (ADDRESS,CCN,NAME,NPI,ZIP / STEEL)
- fed_cms_home_health (ADDRESS,CCN,NAME,ZIP / STEEL)
- fed_cms_hospice (ADDRESS,CCN,NAME,ZIP / STEEL)
- fed_cms_hospital_general (ADDRESS,CCN,NAME,ZIP / STEEL)
- fed_cms_irf (ADDRESS,CCN,NAME,ZIP / STEEL)
- fed_cms_ltch (ADDRESS,CCN,NAME,ZIP / STEEL)
- fed_cms_nppes (EIN,NAME,NPI,ZIP / STEEL)
- fed_cms_nursing_home (ADDRESS,CCN,FIPS,LATLON,NAME,NPI,ZIP / STEEL)
- fed_cms_pos_other (CCN,FIPS,NAME,ZIP / STEEL)
- fed_congress_committee_membership (BIOGUIDE / STEEL)
- fed_doj_crt_cases (none / NONE)
- fed_doj_epstein_library (none / NONE)
- fed_doj_fca_settlements (none / NONE)
- fed_fara_bulk (ADDRESS,COUNTRY,NAME,ZIP / GEO)
- fed_fda_drug_enforcement (ADDRESS,COUNTRY,ZIP / GEO)
- fed_fdic_enforcement (none / NONE)
- fed_fdic_failed_banks (FIPS,NAME / GEO)
- fed_fec_bulk (FEC_CMTE_ID,FEC_CAND_ID / STEEL)
- fed_fec_bulk_committees (FEC_CMTE_ID,FEC_CAND_ID / STEEL)
- fed_fec_bulk_summary (FEC_CAND_ID / STEEL)
- fed_fec_committee_to_candidate (FEC_CMTE_ID,FEC_CAND_ID / STEEL)
- fed_fec_independent_expenditures (FEC_CMTE_ID,FEC_CAND_ID / STEEL)
- fed_fec_indiv_contributions (FEC_CMTE_ID,ZIP / STEEL)
- fed_federal_register_documents (none / NONE)
- fed_fjc_judges (none / STRONG)
- fed_fjc_service (none / STRONG)
- fed_govinfo_bill_cosponsors (BIOGUIDE / STEEL)
- fed_govinfo_billstatus (BIOGUIDE / STEEL)
- fed_hhs_oig_leie (ADDRESS,EIN,NAME,NPI,ZIP / STEEL)
- fed_mapping_inequality (FIPS,GEOM,LATLON / GEO)
- fed_nara_aad (FIPS / GEO)
- fed_nara_wra_aad (FIPS / GEO)
- fed_noaa_ais (IMO,LATLON,MMSI / STEEL)
- fed_oyez (DOCKET,NAME / STRONG)
- fed_revolvingdoor_project (NAME / PROBABILISTIC)
- fed_scdb (DOCKET / STRONG)
- fed_sec_edgar_company_tickers (CIK / STEEL)
- fed_treasury_avg_interest_rates (none / NONE)
- fed_treasury_debt_to_penny (none / NONE)
- fed_usaspending_toptier_agencies (NAME / PROBABILISTIC)
- fed_wpa_slave_narratives (FIPS / GEO)
- intl_ch_zefix (ADDRESS,COUNTRY,NAME / GEO)
- intl_ec_sercop (NAME / PROBABILISTIC)
- intl_ember_elec (COUNTRY / GEO)
- intl_es_borme (COUNTRY / GEO)
- intl_gr_gemi (NAME / PROBABILISTIC)
- intl_hudoc (COUNTRY,NAME / GEO)
- intl_it_istat (COUNTRY / GEO)
- xc_biorxiv_medrxiv (none / NONE)
- xc_jcs_scotus (none / STEEL)
- xc_wayback_doj_epstein (none / NONE)
- xc_wayback_replay_doj_deep_pages (none / NONE)
- xc_wayback_replay_doj_listing (none / NONE)
- xc_wikipedia_largest_us_companies (NAME / PROBABILISTIC)

## No physical LANDING table (0)


## No SOURCE_REGISTRY row (0)
