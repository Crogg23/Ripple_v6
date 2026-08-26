# JOIN_KEYS_STD backfill report

WRITE 32 | SKIP_MEASURED 272 | SKIP_NO_MEASURE 130 | NO_TABLE 4 | NO_REGISTRY_ROW 197

## WOULD WRITE (provisional -> measured)

| source_id | current | measured keys | tier | confirmed columns |
|---|---|---|---|---|
| FED_PHMSA_FLAGGED_INCIDENTS | (empty) | LATLON,ZIP,ADDRESS,NAME | GEO | NAME=NAME(100.0%/303d); OPERATOR_STREET_ADDRESS=ADDRESS(100.0%/189d); OPERATOR_CITY_NAME=NAME(100.0%/89d); OPERATOR_POSTAL_CODE=ZIP(99.85%/126d); LOCATION_LATITUDE=LATLON(100.0%/1959d); LOCATION_LONGITUDE=LATLON(100.0%/1977d); ONSHORE_POSTAL_CODE=ZIP(88.72%/1295d); ONSHORE_CITY_NAME=NAME(88.33%/968d); ONSHORE_COUNTY_NAME=NAME(88.52%/771d); DESIGNATED_NAME=NAME(65.28%/1210d); PIPE_FAC_NAME=NAME(90.63%/1535d); SEGMENT_NAME=NAME(85.68%/1601d); WATER_NAME=NAME(2.84%/47d); OFFSHORE_COUNTY_NAME=NAME(1.32%/17d); ONE_CALL_CENTER_NAME=NAME(3.38%/43d) |
| fed_cdc_leading_causes_state | (empty) | NAME | PROBABILISTIC | C_113_CAUSE_NAME=NAME(100.0%/11d); CAUSE_NAME=NAME(100.0%/11d) |
| fed_courtlistener_financial_disclosures | (empty) | CL_PERSON_ID | STEEL | PERSON_ID=CL_PERSON_ID(41.31%/3256d) |
| fed_dol_osha_inspections | EIN,FIPS,ZIP | NAICS,SIC,ZIP,ADDRESS,NAME | STRONG | ESTAB_NAME=NAME(99.99%/43920d); SITE_ADDRESS=ADDRESS(99.83%/47181d); SITE_ZIP=ZIP(99.97%/15145d); SIC_CODE=SIC(83.93%/1032d); NAICS_CODE=NAICS(99.96%/1023d); MAIL_STREET=ADDRESS(62.32%/27465d); MAIL_ZIP=ZIP(99.97%/12322d) |
| fed_epa_envirofacts | (empty) | ZIP,NAME | GEO | CITY_NAME=NAME(100.0%/819d); POSTAL_CODE=ZIP(100.0%/1129d); COUNTY_NAME=NAME(100.0%/136d); FACILITY_NAME=NAME(100.0%/4461d) |
| fed_epa_npdes_npdes_cs_violations | NPDES_ID | NPDES_ID | STEEL | NPDES_ID=NPDES_ID(100.0%/9145d) |
| fed_epa_npdes_npdes_formal_enforcement_actions | ACTIVITY_ID,NPDES_ID | NPDES_ID | STEEL | NPDES_ID=NPDES_ID(100.0%/29357d) |
| fed_epa_npdes_npdes_ps_violations | NPDES_ID | NPDES_ID | STEEL | NPDES_ID=NPDES_ID(100.0%/22994d) |
| fed_epa_npdes_npdes_qncr_history | NPDES_ID | NPDES_ID | STEEL | NPDES_ID=NPDES_ID(100.0%/44147d) |
| fed_epa_npdes_npdes_se_violations | NPDES_ID | NPDES_ID | STEEL | NPDES_ID=NPDES_ID(100.0%/27839d) |
| fed_epa_superfund_site_boundaries | (empty) | GEOM,ZIP,ADDRESS,NAME | GEO | SITE_NAME=NAME(100.0%/1924d); SITE_FEATURE_NAME=NAME(98.58%/1507d); STREET_ADDR_TXT=ADDRESS(100.0%/1906d); ADDR_COMMENT=ADDRESS(43.66%/544d); CITY_NAME=NAME(100.0%/1351d); ZIP_CODE=ZIP(99.91%/1611d); SITE_CONTACT_NAME=NAME(97.97%/488d); SHAPE__AREA=GEOM(100.0%/2073d); SHAPE__LENGTH=GEOM(100.0%/2092d) |
| fed_faa_aircraft_registry | (empty) | COUNTRY,ZIP,ADDRESS,NAME | GEO | NAME=NAME(98.52%/37457d); STREET=ADDRESS(98.52%/36788d); ZIP_CODE=ZIP(98.42%/14781d); COUNTRY=COUNTRY(98.53%/27d) |
| fed_fdic_bank_data | (empty) | DOCKET,LATLON,ZIP,ADDRESS,NAME | STRONG | ADDRESS=ADDRESS(100.0%/22638d); CBSA_METRO_NAME=NAME(68.5%/391d); DOCKET=DOCKET(100.0%/11593d); LATITUDE=LATLON(100.0%/23456d); LONGITUDE=LATLON(100.0%/23494d); NAME=NAME(100.0%/21678d); ZIP=ZIP(100.0%/12700d) |
| fed_fec_api | (empty) | ZIP,NAME | GEO | CONTRIBUTOR_NAME=NAME(100.0%/334d); CONTRIBUTOR_EMPLOYER=NAME(90.8%/57d); CONTRIBUTOR_ZIP=ZIP(94.2%/308d) |
| fed_fra_casualties | (empty) | LATLON,NAME | GEO | RAILROAD_NAME=NAME(100.0%/720d); COUNTY_NAME=NAME(25.4%/1156d); STATE_NAME=NAME(100.0%/50d); LATITUDE=LATLON(19.18%/2789d); LONGITUDE=LATLON(19.18%/2766d); REPORTING_PARENT_RAILROAD_NAME=NAME(100.0%/585d); REPORTING_RAILROAD_HOLDING_COMPANY=NAME(100.0%/40d) |
| fed_fra_crossing_incidents | (empty) | NAME | PROBABILISTIC | RAILROAD_NAME=NAME(100.0%/730d); OTHER_RAILROAD_NAME=NAME(1.87%/51d); MAINTENANCE_RAILROAD_NAME=NAME(91.78%/946d); COUNTY_NAME=NAME(99.89%/1724d); STATE_NAME=NAME(100.0%/50d); CITY_NAME=NAME(83.46%/8612d); HIGHWAY_NAME=NAME(98.97%/29166d); TRACK_NAME=NAME(99.78%/7683d); REPORTING_PARENT_RAILROAD_NAME=NAME(100.0%/589d); REPORTING_RAILROAD_HOLDING_COMPANY=NAME(100.0%/38d) |
| fed_fra_equipment_accidents | (empty) | LATLON,NAME | GEO | REPORTING_RAILROAD_NAME=NAME(100.0%/716d); OTHER_RAILROAD_NAME=NAME(8.56%/367d); MAINTENANCE_RAILROAD_NAME=NAME(99.97%/1436d); STATE_NAME=NAME(100.0%/50d); COUNTY_NAME=NAME(98.39%/1514d); TRACK_NAME=NAME(98.8%/17656d); ADJUNCT_NAME_1=NAME(11.4%/18d); ADJUNCT_NAME_2=NAME(1.28%/17d); LATITUDE=LATLON(31.55%/7416d); LONGITUDE=LATLON(31.56%/7588d); REPORTING_PARENT_RAILROAD_NAME=NAME(100.0%/581d); REPORTING_RAILROAD_HOLDING_COMPANY=NAME(100.0%/42d) |
| fed_ice_detainers | (empty) | ICE_FACILITY,COUNTRY,ADDRESS | STEEL | DEPARTURE_COUNTRY=COUNTRY(30.33%/118d); DETENTION_FACILITY_CODE=ICE_FACILITY(99.99%/3417d); CITIZENSHIP_COUNTRY=COUNTRY(100.0%/179d); BIRTH_COUNTRY=COUNTRY(100.0%/186d); CRIMINAL_STREET_GANG_YES_NO=ADDRESS(30.94%/2d) |
| fed_ice_detention_stints | (empty) | ICE_FACILITY,COUNTRY | STEEL | BIRTH_COUNTRY=COUNTRY(100.0%/174d); CITIZENSHIP_COUNTRY=COUNTRY(100.0%/166d); DEPARTURE_COUNTRY=COUNTRY(71.04%/159d); DETENTION_FACILITY_CODE=ICE_FACILITY(100.0%/481d) |
| fed_irs_eo_bmf | (empty) | EIN,ZIP,ADDRESS,NAME | STEEL | EIN=EIN(100.0%/49287d); NAME=NAME(100.0%/44096d); STREET=ADDRESS(100.0%/42170d); ZIP=ZIP(100.0%/17030d); C_ORGANIZATION=NAME(100.0%/7d); SORT_NAME=NAME(20.87%/10047d) |
| fed_pbgc_trusteed_plans | (empty) | EIN,NAME | STEEL | SPONSOR_NAME=NAME(99.98%/4369d); PLAN_NAME=NAME(99.98%/5247d); EIN=EIN(100.0%/4414d) |
| fed_sec_edgar_company_tickers_exchange | (empty) | CIK,NAME | STEEL | CIK=CIK(100.0%/7911d); NAME=NAME(100.0%/7995d) |
| fed_usace_nid_dams | (empty) | LATLON,NAME | GEO | DAM_NAME=NAME(95.27%/43406d); LATITUDE=LATLON(99.82%/47382d); LONGITUDE=LATLON(99.82%/47970d); RIVER_OR_STREAM_NAME=NAME(90.1%/20093d) |
| fed_usaspending_bulk | AWARD_ID_PIID,CAGE_CODE,CONTRACT_AWARD_UNIQUE_KEY,RECIPIENT_DUNS,RECIPIENT_UEI | UEI,NAME | STEEL | PARENT_AWARD_AGENCY_NAME=NAME(67.95%/101d); AWARDING_AGENCY_NAME=NAME(100.0%/58d); AWARDING_SUB_AGENCY_NAME=NAME(100.0%/126d); AWARDING_OFFICE_NAME=NAME(100.0%/998d); FUNDING_AGENCY_NAME=NAME(100.0%/72d); FUNDING_SUB_AGENCY_NAME=NAME(100.0%/217d); FUNDING_OFFICE_NAME=NAME(100.0%/1844d); RECIPIENT_UEI=UEI(100.0%/10147d); RECIPIENT_NAME=NAME(100.0%/10090d); RECIPIENT_NAME_RAW=NAME(100.0%/10136d); RECIPIENT_DOING_BUSINESS_AS_NAME=NAME(6.26%/1468d); RECIPIENT_PARENT_UEI=UEI(99.99%/9828d); RECIPIENT_PARENT_NAME=NAME(99.99%/9871d); RECIPIENT_PARENT_NAME_RAW=NAME(100.0%/10034d) |
| fed_usaspending_contracts_full_r2 | (empty) | DUNS,UEI,NAICS,COUNTRY,ZIP,NAME | STEEL | AWARDING_AGENCY_NAME=NAME(100.0%/59d); AWARDING_SUB_AGENCY_NAME=NAME(100.0%/153d); FUNDING_AGENCY_NAME=NAME(93.66%/69d); RECIPIENT_UEI=UEI(100.0%/13658d); RECIPIENT_DUNS=DUNS(63.04%/10629d); RECIPIENT_NAME=NAME(100.0%/12889d); RECIPIENT_DOING_BUSINESS_AS_NAME=NAME(4.54%/973d); RECIPIENT_PARENT_UEI=UEI(99.93%/12460d); RECIPIENT_PARENT_NAME=NAME(99.95%/12129d); RECIPIENT_CITY_NAME=NAME(99.99%/3564d); RECIPIENT_STATE_CODE=NAME(83.34%/51d); RECIPIENT_ZIP_4_CODE=ZIP(98.02%/6415d); RECIPIENT_COUNTRY_NAME=COUNTRY(99.53%/83d); PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME=NAME(95.31%/3059d); NAICS_CODE=NAICS(97.86%/928d); NAICS_DESCRIPTION=NAICS(97.54%/921d) |
| intl_ca_open_canada | (empty) | NAME | PROBABILISTIC | C_ORGANIZATION=NAME(100.0%/15d) |
| intl_ch_opendataswiss | (empty) | NAME | PROBABILISTIC | NAME=NAME(99.98%/4963d); C_ORGANIZATION=NAME(100.0%/85d) |
| intl_cl_datosgob | (empty) | NAME | PROBABILISTIC | NAME=NAME(100.0%/1021d) |
| intl_de_govdata | (empty) | NAME | PROBABILISTIC | NAME=NAME(100.0%/4951d) |
| intl_opensanctions_default | (empty) | NAME | PROBABILISTIC | NAME=NAME(92.9%/46263d) |
| intl_uk_sanctions_list | (empty) | ADDRESS,NAME | PROBABILISTIC | NAME_6=NAME(99.8%/9775d); NAME_1=NAME(41.73%/2212d); NAME_2=NAME(21.31%/1504d); NAME_3=NAME(4.42%/308d); NAME_4=NAME(0.88%/69d); NAME_TYPE=NAME(99.89%/3d); NAME_NON_LATIN_SCRIPT=NAME(1.65%/198d); REGIME_NAME=NAME(100.0%/31d); ADDRESS_LINE_1=ADDRESS(56.36%/1598d); ADDRESS_LINE_2=ADDRESS(36.18%/908d); ADDRESS_LINE_3=ADDRESS(22.14%/487d); ADDRESS_LINE_4=ADDRESS(9.04%/232d); ADDRESS_LINE_5=ADDRESS(13.19%/299d); ADDRESS_LINE_6=ADDRESS(66.12%/540d); ADDRESS_POSTAL_CODE=ADDRESS(19.72%/637d) |
| state_mo_sex_offender_registry | (empty) | ZIP,ADDRESS,NAME | GEO | NAME=NAME(100.0%/21188d); ADDRESS=ADDRESS(98.52%/16018d); ZIP=ZIP(84.09%/1051d) |

## SKIP -- provisional but no key survived value-measurement

| source_id | name-detected but rejected |
|---|---|
| FED_FDA_CAERS | (no key-named columns) |
| FED_FDA_DEVICE_510K | (no key-named columns) |
| FED_FDA_DEVICE_CLASSIFICATION | (no key-named columns) |
| FED_FDA_DEVICE_ENFORCEMENT | (no key-named columns) |
| FED_FDA_DEVICE_PMA | (no key-named columns) |
| FED_FDA_DRUG_ENFORCEMENT | (no key-named columns) |
| FED_FDA_ESTABLISHMENT_REG | (no key-named columns) |
| FED_FDA_GUDID | (no key-named columns) |
| FED_FDA_MAUDE | (no key-named columns) |
| FED_FEC_CANDIDATES | (no key-named columns) |
| FED_FEC_CAND_CMTE_LINKAGE | (no key-named columns) |
| FED_FEC_COMMITTEES | (no key-named columns) |
| FED_FEC_LEADERSHIP_PAC | (no key-named columns) |
| FED_FEC_PAC_SUMMARY | (no key-named columns) |
| FED_NHTSA_COMPLAINTS | (no key-named columns) |
| FED_NHTSA_INVESTIGATIONS | (no key-named columns) |
| FED_NHTSA_RECALLS | (no key-named columns) |
| FED_SEC_13F_POSITIONS | (no key-named columns) |
| FED_SEC_13F_SUBMISSION | (no key-named columns) |
| FED_SEC_INSIDER_DERIV_TRANS | (no key-named columns) |
| FED_SEC_INSIDER_NONDERIV_TRANS | (no key-named columns) |
| FED_SEC_INSIDER_SUBMISSION | (no key-named columns) |
| ca_lobby_cover2 | (no key-named columns) |
| fed_bjs_data | (no key-named columns) |
| fed_cbp_encounters | (no key-named columns) |
| fed_cdc_anxiety_depression | (no key-named columns) |
| fed_cdc_data_portal | FIPS=FIPS(0.0%/0d); ZIP_CODE=ZIP(0.0%/0d) |
| fed_cdc_health_insurance | (no key-named columns) |
| fed_cdc_nndss_weekly_2024 | (no key-named columns) |
| fed_cdc_wonder | (no key-named columns) |
| fed_cftc_cot_financial | (no key-named columns) |
| fed_cftc_cot_futures | (no key-named columns) |
| fed_cms_hpt_mrf | HOSPITAL_NAME=NAME(0.0%/0d); HOSPITAL_ADDRESS=ADDRESS(0.0%/0d); NPI=NPI(0.0%/0d); ATTESTER_NAME=NAME(0.0%/0d); PAYER_NAME=NAME(0.0%/0d); PLAN_NAME=NAME(0.0%/0d) |
| fed_cms_main | NPI=NPI(0.0%/0d); FIPS=FIPS(0.0%/0d); ZIP=ZIP(0.0%/0d) |
| fed_cms_nadac | (no key-named columns) |
| fed_courtlistener_investments | (no key-named columns) |
| fed_cpsc_neiss | (no key-named columns) |
| fed_david_rumsey | (no key-named columns) |
| fed_densho_ddr | FIPS=FIPS(0.0%/0d) |
| fed_dhs_hifld | NAME=NAME(0.0%/0d); ADDRESS=ADDRESS(0.0%/0d); ZIP=ZIP(0.0%/0d); FIPS=FIPS(0.0%/0d); LATITUDE=LATLON(0.0%/0d); LONGITUDE=LATLON(0.0%/0d); NAICS_CODE=NAICS(100.0%/1d); LAYER_NAME=NAME(100.0%/1d) |
| fed_dhs_yearbook | COUNTRY_OF_BIRTH=COUNTRY(0.0%/0d); COUNTRY_OF_LAST_RESIDENCE=COUNTRY(0.0%/0d); TABLE_NAME=NAME(0.0%/0d) |
| fed_docsouth | (no key-named columns) |
| fed_doj_fca_settlements | DEFENDANT_COMPANY=NAME(0.0%/0d); RELATOR_NAME=NAME(0.0%/0d) |
| fed_eoir_case_data | (no key-named columns) |
| fed_epa_icis_air_icis_air_fces_pces | (no key-named columns) |
| fed_epa_icis_air_icis_air_formal_actions | (no key-named columns) |
| fed_epa_icis_air_icis_air_informal_actions | (no key-named columns) |
| fed_epa_icis_air_icis_air_pollutants | (no key-named columns) |
| fed_epa_icis_air_icis_air_program_subparts | (no key-named columns) |
| fed_epa_icis_air_icis_air_programs | (no key-named columns) |
| fed_epa_icis_air_icis_air_stack_tests | (no key-named columns) |
| fed_epa_icis_air_icis_air_titlev_certs | (no key-named columns) |
| fed_epa_icis_air_icis_air_violation_history | (no key-named columns) |
| fed_faa_data_portal | DATASET_NAME=NAME(100.0%/3d); FIPS=FIPS(0.0%/0d); LAT=LATLON(0.0%/0d); LON=LATLON(0.0%/0d) |
| fed_fbi_cde | (no key-named columns) |
| fed_fbi_nics_checks | (no key-named columns) |
| fed_fda_faers_drug | (no key-named columns) |
| fed_fda_faers_indi | (no key-named columns) |
| fed_fda_faers_outc | (no key-named columns) |
| fed_fda_faers_reac | (no key-named columns) |
| fed_ffiec_call_reports | INSTITUTION_NAME=NAME(0.0%/0d) |
| fed_fincen_boi | REPORTING_COMPANY_NAME=NAME(100.0%/1d); EIN=EIN(0.0%/0d); BENEFICIAL_OWNER_FULL_NAME=NAME(0.0%/0d); BENEFICIAL_OWNER_ADDRESS=ADDRESS(0.0%/0d) |
| fed_foreignassistance | COUNTRY=COUNTRY(0.0%/0d); EIN=EIN(0.0%/0d) |
| fed_frb_h15_selected_rates | (no key-named columns) |
| fed_frb_z1_csv | (no key-named columns) |
| fed_google_polads_advertiser_id_mapping | (no key-named columns) |
| fed_google_polads_creative_id_mapping | (no key-named columns) |
| fed_grants_gov | AGENCY_NAME=NAME(0.0%/0d); GRANTOR_CONTACT_NAME=NAME(0.0%/0d) |
| fed_hrsa_uds_health_center_info | (no key-named columns) |
| fed_hrsa_uds_table3a_patients | (no key-named columns) |
| fed_icij_offshoreleaks_relationships | (no key-named columns) |
| fed_jpml_pending_mdls | (no key-named columns) |
| fed_naag_multistate_settlements | (no key-named columns) |
| fed_sba_ppp | (no key-named columns) |
| fed_sec_13f_holdings | (no key-named columns) |
| fed_slavevoyages_intraamerican | (no key-named columns) |
| fed_slavevoyages_transatlantic | (no key-named columns) |
| fed_treasury_debt_outstanding | (no key-named columns) |
| fed_treasury_dts_deposits | (no key-named columns) |
| fed_treasury_mts_receipts | (no key-named columns) |
| fed_uscis_data | COUNTRY=COUNTRY(0.0%/0d) |
| fed_uscourts_stats | PUBLICATION_NAME=NAME(0.0%/0d); FIPS_CODE=FIPS(0.0%/0d) |
| fed_usgs_topoview | FIPS=FIPS(0.0%/0d) |
| fed_va_allcause_mortality | (no key-named columns) |
| fed_va_suicide_appendix | (no key-named columns) |
| fed_va_suicide_national | (no key-named columns) |
| fed_va_suicide_state | (no key-named columns) |
| fed_voteview_rollcall_meta | (no key-named columns) |
| intl_br_dados_gov | C_ORGANIZATION=NAME(0.0%/0d) |
| intl_es_datosgob | (no key-named columns) |
| intl_eu_socta_europol | (no key-named columns) |
| intl_eurlex_cellar | COUNTRY=COUNTRY(0.0%/0d) |
| intl_eurostat | (no key-named columns) |
| intl_fao_faostat | (no key-named columns) |
| intl_fao_faostat_food_security | (no key-named columns) |
| intl_gfi_trade | COUNTRY=COUNTRY(0.0%/0d) |
| intl_gh_datagovgh | (no key-named columns) |
| intl_gleif_relationships | (no key-named columns) |
| intl_gr_datagov | ORGANISATION_NAME=NAME(0.24%/2d) |
| intl_leiden_russian_ops_europe | (no key-named columns) |
| intl_owid_milspend | (no key-named columns) |
| intl_voeten_unga_votes | (no key-named columns) |
| irs527_eain | (no key-named columns) |
| st_oehha_proposition_65_list | (no key-named columns) |
| tx_lobby_awards | (no key-named columns) |
| tx_lobby_cover | (no key-named columns) |
| tx_lobby_dockets | (no key-named columns) |
| tx_lobby_entertainment | (no key-named columns) |
| tx_lobby_events | (no key-named columns) |
| tx_lobby_food_beverage | (no key-named columns) |
| tx_lobby_gifts | (no key-named columns) |
| tx_lobby_individual_reporting | (no key-named columns) |
| tx_lobby_subject_matter | (no key-named columns) |
| tx_lobby_transportation | (no key-named columns) |
| xc_biorxiv_medrxiv | FUNDING_NAME=NAME(0.0%/0d) |
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

- FED_CFPB_COMPLAINTS (STATE,ZIP / GEO)
- FED_CMS_PARTD_PRESCRIBER_DRUG (NPI,FIPS,NAME / STEEL)
- FED_EPA_FRS_FULL (FRS_ID,COUNTRY,FIPS,ZIP,ADDRESS,NAME / STEEL)
- FED_FAC_SINGLE_AUDIT (EIN,UEI,ZIP,ADDRESS,NAME / STEEL)
- FED_FEC_INDEPENDENT_EXPENDITURES (FEC_CAND_ID,NAME / STEEL)
- FED_IRS_990_EFILE_INDEX (EIN,NAME / STEEL)
- FED_IRS_EO_PR (EIN,ZIP,ADDRESS,NAME / STEEL)
- FED_MSHA_ACCIDENTS (MINE_ID,FIPS,NAME / STEEL)
- FED_MSHA_MINES (MINE_ID,SIC,FIPS,NAME / STEEL)
- FED_MSHA_VIOLATIONS (MINE_ID,DOCKET,NAME / STEEL)
- FED_SEC_INSIDER_REPORTINGOWNER (ZIP / GEO)
- FED_USASPENDING_ASSISTANCE_FULL (DUNS,UEI,COUNTRY,NAME / STEEL)
- FED_USASPENDING_CONTRACTS_FULL (DUNS,UEI,NAME / STEEL)
- INTL_GLEIF (LEI,NAME / STEEL)
- INT_UK_COMPANIES_HOUSE (COMPANY_NO,SIC,COUNTRY,ADDRESS,NAME / STEEL)
- ca_lobby_amendments (NAME / PROBABILISTIC)
- ca_lobby_chg_log (ZIP,NAME / GEO)
- ca_lobby_contributions (NAME / PROBABILISTIC)
- ca_lobby_cover (NAME / PROBABILISTIC)
- ca_lobby_emp_lobbyist (NAME / PROBABILISTIC)
- ca_lobby_employer (NAME / PROBABILISTIC)
- ca_lobby_employer_firms (NAME / PROBABILISTIC)
- ca_lobby_firm (NAME / PROBABILISTIC)
- ca_lobby_firm_employer (NAME / PROBABILISTIC)
- ca_lobby_firm_lobbyist (NAME / PROBABILISTIC)
- fed_bia_tribal_geo (GEOM,NAME / GEO)
- fed_bls_qcew (FIPS / GEO)
- fed_bop_statistics (NAME / PROBABILISTIC)
- fed_cdc_drug_poisoning_county (FIPS,STATE / GEO)
- fed_cdc_injury_violence_county (FIPS / GEO)
- fed_cdc_overdose (STATE / GEO)
- fed_cdc_suicide_rates (NAME / PROBABILISTIC)
- fed_cfpb_hmda (CENSUS_TRACT,LEI / STEEL)
- fed_cisa_kev (NAME / PROBABILISTIC)
- fed_clinicaltrials (NAME,NPI / STEEL)
- fed_cms_ambulatory_specialty_model_participants (NPI,NAME / STEEL)
- fed_cms_dialysis (CCN,STATE,ZIP / STEEL)
- fed_cms_facility_affiliation (CCN,NPI / STEEL)
- fed_cms_facility_level_minimum_data_set_frequency (CCN,FIPS,ZIP,NAME / STEEL)
- fed_cms_federally_qualified_health_center_enrollments (CCN,NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_fiscal_intermediary_shared_system_attending_and_rendering (NPI,NAME / STEEL)
- fed_cms_hcris (CCN,COUNTY,STATE,ZIP / STEEL)
- fed_cms_home_health (CCN,STATE,ZIP / STEEL)
- fed_cms_home_health_agency_enrollments (CCN,NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_hospice (CCN,STATE,ZIP / STEEL)
- fed_cms_hospice_enrollments (CCN,NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_hospital_compare (STATE,ZIP / GEO)
- fed_cms_hospital_enrollments (CCN,NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_hospital_general (CCN,STATE,ZIP / STEEL)
- fed_cms_irf (CCN,STATE,ZIP / STEEL)
- fed_cms_ltch (CCN,STATE,ZIP / STEEL)
- fed_cms_medicare_diabetes_prevention_program (NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_medicare_dialysis_facilities (CCN,NPI,NAME / STEEL)
- fed_cms_medicare_durable_medical_equipment_devices_supplies_by_refer (NPI,COUNTRY,FIPS,ZIP,NAME / STEEL)
- fed_cms_medicare_durable_medical_equipment_devices_supplies_by_suppl (NPI,FIPS,ZIP,NAME / STEEL)
- fed_cms_medicare_fee_for_service_public_provider_enrollment (NPI,NAME / STEEL)
- fed_cms_medicare_inpatient_hospitals_by_provider (CCN,FIPS,ZIP,NAME / STEEL)
- fed_cms_medicare_inpatient_hospitals_by_provider_and_service (CCN,FIPS,ZIP,NAME / STEEL)
- fed_cms_medicare_outpatient_hospitals_by_provider_and_service (CCN,FIPS,ZIP,NAME / STEEL)
- fed_cms_medicare_physician_other_practitioners_by_provider (NPI,COUNTRY,FIPS,ZIP,NAME / STEEL)
- fed_cms_medicare_physician_other_practitioners_by_provider_and_servi (NPI,FIPS,ZIP,NAME / STEEL)
- fed_cms_medicare_provider (NPI / STEEL)
- fed_cms_nppes (NPI / STEEL)
- fed_cms_nursing_home (ADDRESS,CCN,FIPS,LATLON,NAME,NPI,ZIP / STEEL)
- fed_cms_nursing_home_deficiencies (CCN,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_nursing_home_fire_deficiencies (CCN,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_nursing_home_penalties (CCN,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_open_payments (CCN,NPI / STEEL)
- fed_cms_open_payments_2022 (NPI,CCN,RECORD_ID,NDC / STEEL)
- fed_cms_open_payments_2023 (CCN,NPI / STEEL)
- fed_cms_opioid_treatment_program_providers (NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_opt_out_affidavits (NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_order_and_referring (NPI,NAME / STEEL)
- fed_cms_part_d_prescribers (NPI,STATE / STEEL)
- fed_cms_pending_initial_logging_and_tracking_non_physicians (NPI,NAME / STEEL)
- fed_cms_pending_initial_logging_and_tracking_physicians (NPI,NAME / STEEL)
- fed_cms_pos_other (CCN / STEEL)
- fed_cms_quality_payment_program_experience (NPI / STEEL)
- fed_cms_rural_health_clinic_enrollments (CCN,NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_cms_skilled_nursing_facility_enrollments (CCN,NPI,ZIP,ADDRESS,NAME / STEEL)
- fed_congress_committee_membership (BIOGUIDE / STEEL)
- fed_congress_legislators (BIOGUIDE,ICPSR,STATE / STEEL)
- fed_consolidated_screening_list (NAME / PROBABILISTIC)
- fed_courtlistener_dockets (DOCKET,NAME / STRONG)
- fed_courtlistener_judges (COUNTRY,NAME / GEO)
- fed_courtlistener_positions (NAME / PROBABILISTIC)
- fed_cpsc_neiss_codes (NAME / PROBABILISTIC)
- fed_dea_arcos_full (DEA_NO,ZIP,NAME / STEEL)
- fed_dhs_ohss (NAME / PROBABILISTIC)
- fed_doj_epstein_library (none / NONE)
- fed_dol_form5500 (EIN,ZIP,NAME / STEEL)
- fed_dol_oflc (NAICS,COUNTRY,ZIP,NAME / STRONG)
- fed_dot_bts (NAME / PROBABILISTIC)
- fed_eac_eavs (STATE / GEO)
- fed_ed_edfacts (NAME / PROBABILISTIC)
- fed_epa_air_emissions_poll_rpt_combined_emissions (FRS_ID,NAME / STEEL)
- fed_epa_echo (COUNTY,FIPS,FRS_ID,STATE,ZIP / STEEL)
- fed_epa_egrid_plant_2022 (FIPS,LATLON,NAME / GEO)
- fed_epa_frs_frs_naics_codes (FRS_ID,NAICS / STEEL)
- fed_epa_frs_frs_program_links (FRS_ID,COUNTRY,FIPS,ZIP,ADDRESS,NAME / STEEL)
- fed_epa_frs_frs_sic_codes (FRS_ID,SIC / STEEL)
- fed_epa_icis_air_icis_air_facilities (FRS_ID,NAICS,SIC,ZIP,ADDRESS,NAME / STEEL)
- fed_epa_icis_fec_case_enforcement_conclusion_facilities (ZIP,NAME / GEO)
- fed_epa_icis_fec_case_facilities (FRS_ID,NAICS,SIC,ZIP,ADDRESS,NAME / STEEL)
- fed_epa_icis_fec_epa_informal_enforcement_actions (FRS_ID / STEEL)
- fed_epa_icis_fec_icis_fec_epa_inspections (FRS_ID,NAME / STEEL)
- fed_epa_npdes_icis_facilities (LATLON,ZIP,ADDRESS,NAME / GEO)
- fed_epa_npdes_npdes_informal_enforcement_actions (FRS_ID / STEEL)
- fed_epa_npdes_npdes_inspections (FRS_ID / STEEL)
- fed_epa_npdes_npdes_naics (NAICS / STRONG)
- fed_epa_npdes_npdes_sics (SIC / STRONG)
- fed_epa_sdwa_sdwa_events_milestones (PWSID / STEEL)
- fed_epa_sdwa_sdwa_facilities (PWSID,NAME / STEEL)
- fed_epa_sdwa_sdwa_geographic_areas (PWSID,ZIP / STEEL)
- fed_epa_sdwa_sdwa_lcr_samples (PWSID / STEEL)
- fed_epa_sdwa_sdwa_pn_violation_assoc (PWSID / STEEL)
- fed_epa_sdwa_sdwa_pub_water_systems (PWSID,COUNTRY,ZIP,ADDRESS,NAME / STEEL)
- fed_epa_sdwa_sdwa_service_areas (PWSID / STEEL)
- fed_epa_sdwa_sdwa_site_visits (PWSID / STEEL)
- fed_epa_sdwa_sdwa_violations_enforcement (PWSID / STEEL)
- fed_epa_tri_basic_2023 (FRS_ID,LATLON,ZIP,ADDRESS,NAME / STEEL)
- fed_fara (NAME / PROBABILISTIC)
- fed_fara_bulk (STATE,ZIP / GEO)
- fed_fatca_ffi (COUNTRY,NAME / GEO)
- fed_fcc_licensing (STATE,ZIP / GEO)
- fed_fda_faers_demo (COUNTRY / GEO)
- fed_fdic_enforcement (none / NONE)
- fed_fdic_failed_banks (FIPS,NAME / GEO)
- fed_fec_bulk (FEC_CMTE_ID,FEC_CAND_ID / STEEL)
- fed_fec_bulk_candidates (FEC_ID / STEEL)
- fed_fec_bulk_committees (FEC_CMTE_ID,FEC_CAND_ID / STEEL)
- fed_fec_bulk_linkages (FEC_CAND_ID,FEC_CMTE_ID / STEEL)
- fed_fec_bulk_summary (FEC_ID / STEEL)
- fed_fec_committee_to_candidate (FEC_ID,STATE,ZIP / STEEL)
- fed_fec_indiv_contributions (FEC_ID,STATE,ZIP / STEEL)
- fed_federal_register_documents (DOCKET / STRONG)
- fed_fhfa_hpi (NAME / PROBABILISTIC)
- fed_fhfa_nmdb (NAME / PROBABILISTIC)
- fed_fhfa_suspended_counterparty_program (NAME / PROBABILISTIC)
- fed_fjc_judges (none / STRONG)
- fed_fjc_service (none / STRONG)
- fed_ftc_datasets (NAME / PROBABILISTIC)
- fed_google_polads_advertiser_declared_stats (ADDRESS,NAME / PROBABILISTIC)
- fed_google_polads_advertiser_geo_spend (COUNTRY,NAME / GEO)
- fed_google_polads_advertiser_stats (NAME / PROBABILISTIC)
- fed_google_polads_advertiser_weekly_spend (NAME / PROBABILISTIC)
- fed_google_polads_creative_stats (NAME / PROBABILISTIC)
- fed_google_polads_geo_spend (COUNTRY / GEO)
- fed_govinfo_bill_cosponsors (BIOGUIDE / STEEL)
- fed_govinfo_billstatus (BIOGUIDE / STEEL)
- fed_hhs_oig_leie (NPI,STATE,ZIP / STEEL)
- fed_hrsa_shortage_areas (STATE / GEO)
- fed_hud_assisted_housing_projects (LATLON,ZIP,ADDRESS,NAME / GEO)
- fed_hud_data (NAME / PROBABILISTIC)
- fed_ice_detention_facility_list (NAME / PROBABILISTIC)
- fed_ice_statistics (COUNTRY / GEO)
- fed_icij_offshoreleaks_addresses (COUNTRY,ADDRESS,NAME / GEO)
- fed_icij_offshoreleaks_entities (COUNTRY,ADDRESS,NAME / GEO)
- fed_icij_offshoreleaks_intermediaries (COUNTRY,ADDRESS,NAME / GEO)
- fed_icij_offshoreleaks_officers (COUNTRY,NAME / GEO)
- fed_icij_offshoreleaks_others (COUNTRY,NAME / GEO)
- fed_irs_990 (EIN / STEEL)
- fed_irs_auto_revocations (EIN,COUNTRY,ZIP,NAME / STEEL)
- fed_irs_bmf (EIN,STATE,ZIP / STEEL)
- fed_irs_pub78_eligible_donees (EIN,COUNTRY,NAME / STEEL)
- fed_irs_revocation (COUNTRY,EIN,STATE,ZIP / STEEL)
- fed_irs_soi (FIPS,STATE,ZIP / GEO)
- fed_irs_soi_charities (EIN,ZIP,ADDRESS,NAME / STEEL)
- fed_mapping_inequality (STATE / GEO)
- fed_medsl_house_returns (FIPS,STATE / GEO)
- fed_medsl_president_returns (FIPS,STATE / GEO)
- fed_medsl_senate_returns (FIPS,STATE / GEO)
- fed_nara_aad (FIPS / GEO)
- fed_nara_wra_aad (FIPS / GEO)
- fed_nasa_open_data (NAME / PROBABILISTIC)
- fed_nid_dams (LATLON,NAME / GEO)
- fed_nih_reporter (DUNS,UEI,NAME / STEEL)
- fed_noaa_ais (IMO / STEEL)
- fed_noaa_storm_events (FIPS,STATE / GEO)
- fed_noaa_weather_api (GEOM,NAME / GEO)
- fed_nsf_awards (STATE,ZIP / GEO)
- fed_ntsb_aviation_aircraft (COUNTRY,ZIP,ADDRESS,NAME / GEO)
- fed_ntsb_aviation_events (COUNTRY,GEOM,LATLON,ZIP,NAME / GEO)
- fed_nursinghome411 (CCN,LATLON,ADDRESS,NAME / STEEL)
- fed_ofac_sdn (IMO / STEEL)
- fed_osha_ita_300a_summary_2023 (EIN,NAICS,ZIP,ADDRESS,NAME / STEEL)
- fed_osha_ita_300a_summary_2024 (EIN,NAICS,ZIP,ADDRESS,NAME / STEEL)
- fed_osha_ita_300a_summary_2025 (EIN,NAICS,ZIP,ADDRESS,NAME / STEEL)
- fed_osha_ita_case_detail_2023 (EIN,NAICS,ZIP,ADDRESS,NAME / STEEL)
- fed_osha_ita_case_detail_2024 (EIN,NAICS,ZIP,ADDRESS,NAME / STEEL)
- fed_osha_ita_case_detail_2025 (EIN,NAICS,ZIP,ADDRESS,NAME / STEEL)
- fed_oyez (DOCKET,NAME / STRONG)
- fed_pbgc_data (STATE / GEO)
- fed_retraction_watch (COUNTRY / GEO)
- fed_revolvingdoor_project (NAME / PROBABILISTIC)
- fed_sam_exclusions (UEI,COUNTRY,ZIP,NAME / STEEL)
- fed_sba_loans (ZIP,ADDRESS,NAME / GEO)
- fed_scdb (DOCKET_ID / STEEL)
- fed_sec_13f_filers (ZIP,NAME / GEO)
- fed_sec_13f_submissions (CIK / STEEL)
- fed_sec_business_development_company_report (CIK,ZIP,ADDRESS,NAME / STEEL)
- fed_sec_closed_end_fund_information (CIK,ZIP,ADDRESS,NAME / STEEL)
- fed_sec_dera_sub_2024q1 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_dera_sub_2024q2 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_dera_sub_2024q3 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_dera_sub_2024q4 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_dera_sub_2025q1 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_dera_sub_2025q2 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_dera_sub_2025q3 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_dera_sub_2025q4 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_dera_sub_2026q1 (CIK,EIN,SIC,NAME / STEEL)
- fed_sec_edgar (CIK,EIN / STEEL)
- fed_sec_edgar_company_tickers (CIK / STEEL)
- fed_sec_edgar_financials (CIK,EIN / STEEL)
- fed_sec_edgar_insiders (CIK / STEEL)
- fed_sec_money_market_fund_information (CIK,NAME / STEEL)
- fed_senate_lda_filings (COUNTRY,NAME / GEO)
- fed_senate_stock_watcher (none / PROBABILISTIC)
- fed_treasury_avg_interest_rates (none / NONE)
- fed_treasury_debt_to_penny (none / NONE)
- fed_us_sec_edgar (ACCESSION_NUMBER,CIK,EIN / STEEL)
- fed_us_usaspending_api (NAME / PROBABILISTIC)
- fed_usaspending_contracts (STATE,UEI / STEEL)
- fed_usaspending_subawards (EIN,FIPS / STEEL)
- fed_usaspending_toptier_agencies (NAME / PROBABILISTIC)
- fed_usgs_earthquakes (LATLON / GEO)
- fed_usgs_minerals (STATE / GEO)
- fed_usgs_water (LATLON,NAME / GEO)
- fed_voteview_members (BIOGUIDE,ICPSR / STEEL)
- fed_voteview_rollcalls (ICPSR / STEEL)
- fed_wpa_slave_narratives (STATE / GEO)
- intl_adb_data (NAME / PROBABILISTIC)
- intl_ar_datosgob (NAME / PROBABILISTIC)
- intl_ec_sercop (NAME / PROBABILISTIC)
- intl_eg_capmas (NAME / PROBABILISTIC)
- intl_ember_elec (COUNTRY / GEO)
- intl_embl_ensembl (NAME / PROBABILISTIC)
- intl_es_borme (COUNTRY / GEO)
- intl_eu_sanctions (COUNTRY,ZIP,ADDRESS,NAME / GEO)
- intl_fatf_ratings (COUNTRY / GEO)
- intl_fr_data_gouv (NAME / PROBABILISTIC)
- intl_freedomhouse (COUNTRY / GEO)
- intl_gdelt (COUNTRY,LATLON,NAME / GEO)
- intl_gem_hazard (COUNTRY / GEO)
- intl_gleif_repex (LEI / STEEL)
- intl_global_witness_defenders (COUNTRY / GEO)
- intl_hudoc (COUNTRY / GEO)
- intl_ie_cro (NAME / PROBABILISTIC)
- intl_ipc_food_insecurity_global (COUNTRY / GEO)
- intl_it_istat (COUNTRY / GEO)
- intl_nti_cns_dprk_missile_tests (LATLON,NAME / GEO)
- intl_opensanctions (NAME / PROBABILISTIC)
- intl_ucdp_ged (COUNTRY,GEOM,LATLON,NAME / GEO)
- intl_wb_ids (COUNTRY,NAME / GEO)
- irs527_8871_orgs (EIN,ZIP,ADDRESS,NAME / STEEL)
- irs527_8872_reports (EIN,ZIP,ADDRESS,NAME / STEEL)
- irs527_directors_officers (EIN,ZIP,NAME / STEEL)
- irs527_related_entities (EIN,ZIP,NAME / STEEL)
- st_cannabis_policy_bundles (FIPS,STATE / GEO)
- xc_epa_corporate_crosswalk (FRS_ID,LEI,UEI,NAME / STEEL)
- xc_jcs_coa (NAME / PROBABILISTIC)
- xc_jcs_scotus (none / STEEL)
- xc_mapping_police_violence (LATLON,ZIP,ADDRESS,NAME / GEO)
- xc_ransomwarelive_victims (COUNTRY,NAME / GEO)
- xc_uk_sanctions_list (ADDRESS,NAME / PROBABILISTIC)
- xc_un_consolidated_sanctions_list (ADDRESS,NAME / PROBABILISTIC)
- xc_vera_incarceration_trends (COUNTY,FIPS,STATE / GEO)
- xc_wapo_fatal_force (COUNTY,STATE / GEO)
- xc_wayback_doj_epstein (none / NONE)
- xc_wayback_replay_doj_deep_pages (none / NONE)
- xc_wayback_replay_doj_listing (none / NONE)
- xc_wikipedia_largest_us_companies (NAME / PROBABILISTIC)

## No physical LANDING table (4)

- INT_GLEIF_RR (modeled)
- fed_dea_arcos (modeled)
- fed_fjc_idb (modeled)
- intl_uk_companies_house (modeled)

## No SOURCE_REGISTRY row (197)

- fed_atf_ffl (modeled)
- fed_cdc_data_portal_full (landed)
- fed_cfpb_hmda_arid2017_lei_xref (modeled)
- fed_cfpb_hmda_historic (modeled)
- fed_cfpb_hmda_lar (modeled)
- fed_cftc_cot_financial_hist (landed)
- fed_cms_marketplace_plan_attributes_puf (landed)
- fed_cms_open_payments_profile_supplement (modeled)
- fed_cms_pecos_provider_enrollment (landed)
- fed_courtlistener_citation_map (landed)
- fed_courtlistener_citations (modeled)
- fed_courtlistener_court_appeals_to (modeled)
- fed_courtlistener_courthouses (modeled)
- fed_courtlistener_courts (modeled)
- fed_courtlistener_disclosure_agreements (modeled)
- fed_courtlistener_disclosure_debts (modeled)
- fed_courtlistener_disclosure_gifts (modeled)
- fed_courtlistener_disclosure_non_investment_income (modeled)
- fed_courtlistener_disclosure_positions (modeled)
- fed_courtlistener_disclosure_reimbursements (modeled)
- fed_courtlistener_disclosure_spousal_income (modeled)
- fed_courtlistener_fjc_idb_cl_linked (modeled)
- fed_courtlistener_judge_educations (modeled)
- fed_courtlistener_judge_political_affiliations (modeled)
- fed_courtlistener_judge_races (modeled)
- fed_courtlistener_opinion_clusters (modeled)
- fed_courtlistener_oral_arguments (modeled)
- fed_courtlistener_originating_court_info (modeled)
- fed_courtlistener_parentheticals (modeled)
- fed_courtlistener_race_codes (modeled)
- fed_courtlistener_schools (modeled)
- fed_dol_ebsa_form5500_schedule_sb (modeled)
- fed_dol_olms (modeled)
- fed_dtcc_dtc_participants (landed)
- fed_ed_college_scorecard_institution (modeled)
- fed_ed_nces_cip_codes (modeled)
- fed_eia860_1_utility (modeled)
- fed_eia860_2_plant (modeled)
- fed_eia860_3_1_generator (modeled)
- fed_eia860_3_2_wind (modeled)
- fed_eia860_3_3_solar (modeled)
- fed_eia860_3_4_energy_storage (modeled)
- fed_eia860_3_5_multifuel (modeled)
- fed_eia860_4_owner (modeled)
- fed_eia860_6_1_enviroassoc (modeled)
- fed_eia860_6_2_enviroequip (modeled)
- fed_eia861_advanced_meters (modeled)
- fed_eia861_balancing_authority (landed)
- fed_eia861_delivery_companies (modeled)
- fed_eia861_demand_response (modeled)
- fed_eia861_distribution_systems (modeled)
- fed_eia861_dynamic_pricing (modeled)
- fed_eia861_energy_efficiency (modeled)
- fed_eia861_frame (modeled)
- fed_eia861_mergers (modeled)
- fed_eia861_net_metering (modeled)
- fed_eia861_non_net_metering_distributed (modeled)
- fed_eia861_operational_data (modeled)
- fed_eia861_reliability (modeled)
- fed_eia861_sales_ult_cust (modeled)
- fed_eia861_sales_ult_cust_cs (modeled)
- fed_eia861_service_territory (modeled)
- fed_eia861_short_form (modeled)
- fed_eia861_utility_data (modeled)
- fed_eia_860_generator (landed)
- fed_eia_860_plant (landed)
- fed_eia_860_utility (landed)
- fed_eia_861_balancing_authority (modeled)
- fed_epa_aqs_sites (modeled)
- fed_epa_frs_frs_facilities (modeled)
- fed_epa_ghgrp_emission (modeled)
- fed_epa_ghgrp_facility (modeled)
- fed_epa_rcra_enforcements (modeled)
- fed_epa_rcra_evaluations (modeled)
- fed_epa_rcra_facilities (modeled)
- fed_epa_rcra_rcra_enforcements (landed)
- fed_epa_rcra_rcra_evaluations (landed)
- fed_epa_rcra_rcra_facilities (landed)
- fed_epa_rcra_rcra_naics (modeled)
- fed_epa_rcra_rcra_violations (landed)
- fed_epa_rcra_rcra_viosnc_history (landed)
- fed_epa_rcra_violations (modeled)
- fed_epa_rcra_viosnc_history (modeled)
- fed_epa_tri_facility (modeled)
- fed_faa_adip_private_airports (landed)
- fed_fda_device_enforcement__staging (landed)
- fed_fda_drug_master_files (modeled)
- fed_fda_gudid__staging (landed)
- fed_fda_purple_book (modeled)
- fed_fda_unii_gsrs_substances (modeled)
- fed_fdic_sod_branch_deposits (modeled)
- fed_fema_ia_housing_registrations (modeled)
- fed_fema_nfip_community_status_book (modeled)
- fed_fema_nfip_community_status_book_full_r2 (landed)
- fed_fhfa_fhlb_membership (modeled)
- fed_fhfa_suspended_counterparties (modeled)
- fed_fhfa_suspended_counterparty (landed)
- fed_finra_mpid_list (modeled)
- fed_fjc_article_iii_judges (landed)
- fed_fjc_idb_appellate (modeled)
- fed_fjc_idb_bankruptcy (modeled)
- fed_fjc_idb_civil (modeled)
- fed_fjc_idb_criminal (modeled)
- fed_fracfocus_disclosure_list (modeled)
- fed_fracfocus_registry (modeled)
- fed_fracfocus_water_source (modeled)
- fed_hrsa_hpsa_primary_care (modeled)
- fed_hrsa_npdb (modeled)
- fed_hrsa_uds_service_delivery_sites (modeled)
- fed_hud_fha_sf_portfolio_snapshot (modeled)
- fed_hud_mf_firm_commitments (modeled)
- fed_hud_mf_section8_contracts (modeled)
- fed_hud_public_housing_authorities (modeled)
- fed_ice_detention_facility_codes (modeled)
- fed_ihs_facilities (modeled)
- fed_ihs_scb_facility (modeled)
- fed_irs_527_orgs (landed)
- fed_irs_fatca_ffi_list (landed)
- fed_itis_comments (modeled)
- fed_itis_experts (modeled)
- fed_itis_geographic_div (modeled)
- fed_itis_hierarchy (modeled)
- fed_itis_jurisdiction (modeled)
- fed_itis_kingdoms (modeled)
- fed_itis_longnames (modeled)
- fed_itis_nodc_ids (modeled)
- fed_itis_other_sources (modeled)
- fed_itis_publications (modeled)
- fed_itis_reference_links (modeled)
- fed_itis_strippedauthor (modeled)
- fed_itis_synonym_links (modeled)
- fed_itis_taxon_authors_lkp (modeled)
- fed_itis_taxon_unit_types (modeled)
- fed_itis_taxonomic_units (modeled)
- fed_itis_tu_comments_links (modeled)
- fed_itis_vern_ref_links (modeled)
- fed_itis_vernaculars (modeled)
- fed_jpml_pending_mdl (landed)
- fed_msrb_registrants (modeled)
- fed_ncua_call_reports_foicu (modeled)
- fed_ncua_call_reports_fs220 (modeled)
- fed_ncua_charter_merger_events (modeled)
- fed_ncua_federally_insured_cu_list (modeled)
- fed_nlm_dailymed_spl_setid_map (modeled)
- fed_ntsb_aviation_injury (modeled)
- fed_occ_national_banks (modeled)
- fed_occ_national_banks_by_name (landed)
- fed_occ_thrifts (modeled)
- fed_pbgc_trusteed_pension_plans (landed)
- fed_pcaob_form_ap_filings (modeled)
- fed_sam_exclusions_full_r2 (landed)
- fed_sba_ppp_loans_150k_plus (landed)
- fed_sbir_sttr_awards (modeled)
- fed_sec_investment_company_series_class (modeled)
- fed_trade_consolidated_screening_list (landed)
- fed_usaspending_tas_filter_tree (modeled)
- fed_uscg_nrc_incident_reports (modeled)
- fed_uscg_nrc_incidents (modeled)
- fed_usda_rd_mfh_active_projects (modeled)
- fed_usgs_gnis_all_names (modeled)
- fed_usgs_orphaned_oil_gas_wells (modeled)
- fed_usgs_wbd_huc8 (modeled)
- fed_voteview_rollcall_meta_full (landed)
- fed_wqp_monitoring_stations (modeled)
- icij_offshore_leaks_addresses (landed)
- icij_offshore_leaks_entities (landed)
- icij_offshore_leaks_intermediaries (landed)
- icij_offshore_leaks_officers (landed)
- icij_offshore_leaks_relationships (landed)
- intl_elections_canada_contributions (modeled)
- intl_fr_data_gouv_full (landed)
- intl_healthcanada_dpd_drug (modeled)
- intl_iso_mic_registry (modeled)
- intl_osfi_regulated_fi (modeled)
- intl_un_consolidated_sanctions (landed)
- intl_un_sc_consolidated_sanctions (landed)
- st_ca_oehha_prop65_chemicals (landed)
- st_nyc_cfb_campaign_2001_contribution (modeled)
- st_nyc_cfb_campaign_2009_contribution (modeled)
- st_nyc_cfb_campaign_2013_contribution (modeled)
- st_nyc_cfb_campaign_2021_contributions (modeled)
- st_nyc_cfb_campaign_2025_contributions (modeled)
- state_oehha_prop65_chemicals (landed)
- uk_companies_house_psc (modeled)
- xc_census_cb_county (landed)
- xc_census_cb_state (landed)
- xc_census_cb_zcta (landed)
- xc_crossref_funder_registry (modeled)
- xc_icij_offshore_nodes_addresses (landed)
- xc_icij_offshore_nodes_entities (landed)
- xc_icij_offshore_nodes_intermediaries (landed)
- xc_icij_offshore_nodes_officers (landed)
- xc_icij_offshore_relationships (landed)
- xc_osf_registrations (modeled)
- xc_ransomwarelive_victims_full_r2 (landed)
- xc_retraction_watch_database (modeled)
- xc_ror_research_organizations (modeled)