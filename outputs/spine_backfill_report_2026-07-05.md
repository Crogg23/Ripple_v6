# Spine backfill profiling report

HIGH 524 | MEDIUM 400 | AMBIGUOUS 1075 | NO_TABLE 4 | NO_REGISTRY_ROW 199

## HIGH (524)

| source_id | spine_entity | natural_key | grain |
|---|---|---|---|
| FED_EPA_FRS_FULL | facility | REGISTRY_ID | one row per facility (FRS_ID is unique) |
| FED_IRS_EO_PR | organization | EIN | one row per organization (EIN is unique) |
| FED_MSHA_MINES | facility | MINE_ID | one row per facility (MINE_ID is unique) |
| INTL_GLEIF | organization | LEI | one row per organization (LEI is unique) |
| INT_UK_COMPANIES_HOUSE | organization | CompanyNumber | one row per organization (COMPANY_NO is unique) |
| ca_lobby_firm | (unresolved -- grain proven, entity unknown) | FIRM_ID | one row per record (spine_entity not determined -- no registry hint available) (FIRM_ID is unique) |
| ca_lobby_firm_lobbyist | (unresolved -- grain proven, entity unknown) | LOBBYIST_ID | one row per record (spine_entity not determined -- no registry hint available) (LOBBYIST_ID is unique) |
| fed_cisa_kev | (unresolved -- grain proven, entity unknown) | CVE_ID | one row per record (spine_entity not determined -- no registry hint available) (CVE_ID is unique) |
| fed_clinicaltrials | (unresolved -- grain proven, entity unknown) | NCT_ID | one row per record (spine_entity not determined -- no registry hint available) (NCT_ID is unique) |
| fed_cms_ambulatory_specialty_model_participants | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_dialysis | facility | CCN | one row per facility (CCN is unique) |
| fed_cms_facility_affiliation | provider | CCN,NPI | one row per facility-provider relationship (CCN+NPI is unique) |
| fed_cms_fiscal_intermediary_shared_system_attending_and_rendering | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_hcris | facility | PROVIDER_CCN | one row per facility (CCN is unique) |
| fed_cms_home_health | facility | CCN | one row per facility (CCN is unique) |
| fed_cms_hospice | facility | CCN | one row per facility (CCN is unique) |
| fed_cms_hospital_general | facility | CCN | one row per facility (CCN is unique) |
| fed_cms_hpt_mrf | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_irf | facility | CCN | one row per facility (CCN is unique) |
| fed_cms_ltch | facility | CCN | one row per facility (CCN is unique) |
| fed_cms_medicare_durable_medical_equipment_devices_supplies_by_refer | provider | RFRG_NPI | one row per provider (NPI is unique) |
| fed_cms_medicare_inpatient_hospitals_by_provider | facility | RNDRNG_PRVDR_CCN | one row per facility (CCN is unique) |
| fed_cms_medicare_physician_other_practitioners_by_provider | provider | RNDRNG_NPI | one row per provider (NPI is unique) |
| fed_cms_medicare_provider | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_nppes | provider | EMPLOYER_IDENTIFICATION_NUMBER_EIN,NPI,NPI_DEACTIVATION_DATE,NPI_DEACTIVATION_REASON_CODE,NPI_REACTIVATION_DATE,REPLACEMENT_NPI | one row per organization-provider relationship (EIN+NPI+NPI+NPI+NPI+NPI is unique) |
| fed_cms_nursing_home | provider | CMS_CERTIFICATION_NUMBER__CCN,NPI | one row per facility-provider relationship (CCN+NPI is unique) |
| fed_cms_opt_out_affidavits | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_order_and_referring | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_part_d_prescribers | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_pending_initial_logging_and_tracking_non_physicians | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_pending_initial_logging_and_tracking_physicians | provider | NPI | one row per provider (NPI is unique) |
| fed_cms_pos_other | facility | CCN | one row per facility (CCN is unique) |
| fed_congress_legislators | person | BIOGUIDE | one row per person (BIOGUIDE is unique) |
| fed_courtlistener_investments | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| fed_david_rumsey | (unresolved -- grain proven, entity unknown) | MANIFEST_ID | one row per record (spine_entity not determined -- no registry hint available) (MANIFEST_ID is unique) |
| fed_epa_echo | facility | FRS_ID | one row per facility (FRS_ID is unique) |
| fed_epa_npdes_icis_facilities | facility | NPDES_ID | one row per facility (NPDES_ID is unique) |
| fed_epa_sdwa_sdwa_pub_water_systems | facility | PWSID | one row per facility (PWSID is unique) |
| fed_fec_bulk | person | FEC_CAND_ID,FEC_CMTE_ID | one row per organization-person relationship (FEC_CAND_ID+FEC_CMTE_ID is unique) |
| fed_fec_bulk_committees | person | FEC_CAND_ID,FEC_CMTE_ID | one row per organization-person relationship (FEC_CAND_ID+FEC_CMTE_ID is unique) |
| fed_fincen_boi | organization | EIN | one row per organization (EIN is unique) |
| fed_fjc_judges | person | SEAT_ID_1 | one row per person (SEAT_ID_1 is unique) |
| fed_fjc_service | person | SEAT_ID | one row per person (SEAT_ID is unique) |
| fed_google_polads_advertiser_declared_stats | (unresolved -- grain proven, entity unknown) | ADVERTISER_ID | one row per record (spine_entity not determined -- no registry hint available) (ADVERTISER_ID is unique) |
| fed_google_polads_advertiser_stats | (unresolved -- grain proven, entity unknown) | ADVERTISER_ID | one row per record (spine_entity not determined -- no registry hint available) (ADVERTISER_ID is unique) |
| fed_google_polads_creative_stats | (unresolved -- grain proven, entity unknown) | AD_ID | one row per record (spine_entity not determined -- no registry hint available) (AD_ID is unique) |
| fed_google_polads_geo_spend | place | COUNTRY_SUBDIVISION_SECONDARY | one row per place (COUNTRY is unique) |
| fed_grants_gov | (unresolved -- grain proven, entity unknown) | OPPORTUNITY_ID | one row per record (spine_entity not determined -- no registry hint available) (OPPORTUNITY_ID is unique) |
| fed_irs_990 | organization | EIN | one row per organization (EIN is unique) |
| fed_irs_auto_revocations | organization | EIN | one row per organization (EIN is unique) |
| fed_irs_bmf | organization | EIN | one row per organization (EIN is unique) |
| fed_irs_eo_bmf | organization | EIN | one row per organization (EIN is unique) |
| fed_irs_pub78_eligible_donees | organization | EIN | one row per organization (EIN is unique) |
| fed_irs_revocation | organization | EIN | one row per organization (EIN is unique) |
| fed_irs_soi_charities | organization | EIN | one row per organization (EIN is unique) |
| fed_naag_multistate_settlements | (unresolved -- grain proven, entity unknown) | SORT_ID | one row per record (spine_entity not determined -- no registry hint available) (SORT_ID is unique) |
| fed_nursinghome411 | facility | CMS_CERTIFICATION_NUMBER_CCN | one row per facility (CCN is unique) |
| fed_oyez | case | DOCKET | one row per case (DOCKET is unique) |
| fed_sec_business_development_company_report | organization | CIK | one row per organization (CIK is unique) |
| fed_sec_closed_end_fund_information | organization | CIK | one row per organization (CIK is unique) |
| fed_usaspending_toptier_agencies | (unresolved -- grain proven, entity unknown) | AGENCY_ID | one row per record (spine_entity not determined -- no registry hint available) (AGENCY_ID is unique) |
| fed_usgs_3dep | place | SHAPE | one row per place (GEOM is unique) |
| intl_br_dados_gov | (unresolved -- grain proven, entity unknown) | DATASET_ID | one row per record (spine_entity not determined -- no registry hint available) (DATASET_ID is unique) |
| intl_ca_open_canada | (unresolved -- grain proven, entity unknown) | DATASET_ID | one row per record (spine_entity not determined -- no registry hint available) (DATASET_ID is unique) |
| intl_ch_opendataswiss | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| intl_cl_datosgob | (unresolved -- grain proven, entity unknown) | DATASET_ID | one row per record (spine_entity not determined -- no registry hint available) (DATASET_ID is unique) |
| intl_de_govdata | (unresolved -- grain proven, entity unknown) | DATASET_ID | one row per record (spine_entity not determined -- no registry hint available) (DATASET_ID is unique) |
| intl_ec_sercop | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| intl_embl_ensembl | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| intl_gr_datagov | (unresolved -- grain proven, entity unknown) | DATASET_ID | one row per record (spine_entity not determined -- no registry hint available) (DATASET_ID is unique) |
| intl_opensanctions | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| intl_opensanctions_default | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_arc_atlanta_dataatla_d8df9588a6 | case | DOCKET_NO | one row per case (DOCKET is unique) |
| portal_arc_columbus_gis_ope_8259461c2a | organization | EIN | one row per organization (EIN is unique) |
| portal_arc_fort_worth_open_2259070522 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_fort_worth_open_9f0879147a | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_harris_county_op_0f9c7fcb29 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_arc_harris_county_op_119b70555b | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_harris_county_op_32d5ff05ca | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_harris_county_op_360277f8cb | place | ZIP | one row per place (ZIP is unique) |
| portal_arc_harris_county_op_58fab3b4f7 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_harris_county_op_795533139c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_harris_county_op_86ae12cfc0 | provider | NPI | one row per provider (NPI is unique) |
| portal_arc_harris_county_op_89477f0032 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_harris_county_op_b7635629a1 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_harris_county_op_d8cf46061b | place | GEOID20 | one row per place (FIPS is unique) |
| portal_arc_harris_county_op_fa9969d82e | provider | NPI | one row per provider (NPI is unique) |
| portal_arc_la_county_open_d_464355f6d4 | place | ZIP | one row per place (ZIP is unique) |
| portal_arc_la_county_open_d_58a85aed74 | provider | NPI | one row per provider (NPI is unique) |
| portal_arc_la_county_open_d_6df63a4983 | provider | NPI | one row per provider (NPI is unique) |
| portal_arc_la_county_open_d_83f0ba30fb | provider | NPI | one row per provider (NPI is unique) |
| portal_arc_memphis_open_dat_3057d84002 | case | DOCKET | one row per case (DOCKET is unique) |
| portal_arc_memphis_open_dat_9f6f4b2736 | case | DOCKET | one row per case (DOCKET is unique) |
| portal_arc_open_baltimore_6c2257f1c4 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_dc_008ba480f6 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_dc_01f2d9886c | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_dc_32ad83d2ec | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_dc_454981b380 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_dc_56c4f04cf0 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_dc_98319ab13d | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_0426858dfe | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_09e3680fd2 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_1ad7e106e4 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_4c5820fd0a | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_5ac94c44da | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_6cdce692aa | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_7c8c54bd8c | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_7efdca0423 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_bd6a1cacbb | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_be5550ebf6 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_minnea_d808f6bf62 | facility | CCN | one row per facility (CCN is unique) |
| portal_arc_open_data_raleig_bbf9abca0d | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_arc_tucson_open_data_11050c025b | case | DOCKET | one row per case (DOCKET is unique) |
| portal_arc_tucson_open_data_9e24e86b9a | case | DOCKET | one row per case (DOCKET is unique) |
| portal_arc_vermont_open_geo_62f10327d4 | place | LATITUDE | one row per place (LATLON is unique) |
| portal_arc_vermont_open_geo_9e55d67e2c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_vermont_open_geo_de261d6f8c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_arc_wake_county_open_4b425fd089 | organization | USER_EIN__NOT_USED | one row per organization (EIN is unique) |
| portal_arc_wisconsin_open_d_07cf3c3824 | provider | NPI_ID | one row per provider (NPI is unique) |
| portal_arc_wisconsin_open_d_601e691159 | provider | NPI_ID | one row per provider (NPI is unique) |
| portal_cka_analyze_boston_0ced34c7c1 | place | ZIP | one row per place (ZIP is unique) |
| portal_cka_analyze_boston_236a5362b9 | place | SHAPE_WKT | one row per place (GEOM is unique) |
| portal_cka_analyze_boston_45e7e21495 | place | SHAPE_WKT | one row per place (GEOM is unique) |
| portal_cka_analyze_boston_691c77c209 | place | SHAPE_WKT | one row per place (GEOM is unique) |
| portal_cka_analyze_boston_899bb82358 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_analyze_boston_8a02ca5e02 | place | LAT | one row per place (LATLON is unique) |
| portal_cka_analyze_boston_97789ab639 | place | SHAPE_WKT | one row per place (GEOM is unique) |
| portal_cka_analyze_boston_99d95f2df0 | place | GEOID20 | one row per place (FIPS is unique) |
| portal_cka_analyze_boston_9a0fe05b1b | (unresolved -- grain proven, entity unknown) | CNTRCT_HDR_CNTRCT_ID | one row per record (spine_entity not determined -- no registry hint available) (CNTRCT_HDR_CNTRCT_ID is unique) |
| portal_cka_analyze_boston_a4a4828973 | place | SHAPE_WKT | one row per place (GEOM is unique) |
| portal_cka_analyze_boston_acca0df381 | (unresolved -- grain proven, entity unknown) | MAIN_ID | one row per record (spine_entity not determined -- no registry hint available) (MAIN_ID is unique) |
| portal_cka_analyze_boston_bbe261accb | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_analyze_boston_db1aefd5b6 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_analyze_boston_df52d983a2 | place | GEOID20 | one row per place (FIPS is unique) |
| portal_cka_analyze_boston_e1262d25c2 | place | SHAPE_WKT | one row per place (GEOM is unique) |
| portal_cka_analyze_boston_eb235cdc7a | place | SHAPE_WKT | one row per place (GEOM is unique) |
| portal_cka_california_open_0bc18bba68 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_21e0e694b5 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_27dc9c9e51 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_31deeff0a8 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_37c04cba4a | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_3ba640aa6e | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_41b8625438 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_california_open_49d5a45de1 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_6083f016d2 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_6a4468b24f | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_7f65d27db7 | (unresolved -- grain proven, entity unknown) | INDICENT_ID | one row per record (spine_entity not determined -- no registry hint available) (INDICENT_ID is unique) |
| portal_cka_california_open_823711435d | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_8c4aa754ce | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_9c50aef41d | place | ZIP_CODE | one row per place (ZIP is unique) |
| portal_cka_california_open_b7d3e2c140 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_c86733ed60 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_cb7c3747fc | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_e2cdcdbc2c | place | LAT_DDM | one row per place (LATLON is unique) |
| portal_cka_california_open_ee216e8506 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_f039e82e72 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_california_open_f406aad424 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_houston_open_dat_092dc52bc1 | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_09fd7e454a | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_houston_open_dat_0a6665137f | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_405fbdb44a | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_442a765041 | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_48b03033d3 | (unresolved -- grain proven, entity unknown) | BUSINESS_AREA_ID | one row per record (spine_entity not determined -- no registry hint available) (BUSINESS_AREA_ID is unique) |
| portal_cka_houston_open_dat_4df426d97d | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_501ee45dc7 | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_583918009f | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_6082321c0c | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_95cc6891bd | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_aefb1b6a56 | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_ebcdf36b9e | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_houston_open_dat_fb1f968c19 | (unresolved -- grain proven, entity unknown) | FUND_CENTER_ID | one row per record (spine_entity not determined -- no registry hint available) (FUND_CENTER_ID is unique) |
| portal_cka_indiana_data_hub_90819d705e | place | ZIP_CD | one row per place (ZIP is unique) |
| portal_cka_indiana_data_hub_90c2a3ca78 | place | ZCTA | one row per place (ZIP is unique) |
| portal_cka_indiana_data_hub_ba1b037c9e | place | LOCATION_ZIP | one row per place (ZIP is unique) |
| portal_cka_indiana_data_hub_bd531b17f6 | place | FIPS | one row per place (FIPS is unique) |
| portal_cka_ireland_national_12f7eae1d9 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_ireland_national_4049d41c91 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_ireland_national_73a82cb256 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_ireland_national_f2efde1a8c | (unresolved -- grain proven, entity unknown) | PROJECT_ID | one row per record (spine_entity not determined -- no registry hint available) (PROJECT_ID is unique) |
| portal_cka_israel_national_05cd5564c6 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_israel_national_12fc0d7b44 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_israel_national_23ec89fe35 | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID is unique) |
| portal_cka_israel_national_2d69dc52e0 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_israel_national_50096ddb0e | (unresolved -- grain proven, entity unknown) | WARRENT_ID | one row per record (spine_entity not determined -- no registry hint available) (WARRENT_ID is unique) |
| portal_cka_israel_national_6fa4de9040 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_israel_national_7362ebc06f | (unresolved -- grain proven, entity unknown) | ITEM_ID | one row per record (spine_entity not determined -- no registry hint available) (ITEM_ID is unique) |
| portal_cka_israel_national_964780e58d | (unresolved -- grain proven, entity unknown) | TYPE_ID | one row per record (spine_entity not determined -- no registry hint available) (TYPE_ID is unique) |
| portal_cka_israel_national_b37ba647d0 | (unresolved -- grain proven, entity unknown) | MISGERET_ID | one row per record (spine_entity not determined -- no registry hint available) (MISGERET_ID is unique) |
| portal_cka_israel_national_c596979f55 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_israel_national_da3ca6db5d | (unresolved -- grain proven, entity unknown) | WORK_ID | one row per record (spine_entity not determined -- no registry hint available) (WORK_ID is unique) |
| portal_cka_israel_national_ee52e94997 | (unresolved -- grain proven, entity unknown) | ANIMAL_LAB_ID | one row per record (spine_entity not determined -- no registry hint available) (ANIMAL_LAB_ID is unique) |
| portal_cka_israel_national_ff540a3c79 | place | GEOM | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_136d910ad7 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_19461cbd4a | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_19f13722dd | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_1e2348f9b1 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_1f87a7ae2d | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_2c667a6fc6 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_2f8287a9cb | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_320c4dfdb2 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_3769bb8138 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_38df78bd6d | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_3b9ccbcfd0 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_424e5a26f3 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_46bf1abbc1 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_581de3800b | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_58b0401c9a | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_61f8b1c981 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_6891c6fcc4 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_68bcb9dda1 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_726064391e | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_7659b16d25 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_87c271a71e | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_9548772c45 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_9770eb9ebd | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_98d226a574 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_9c302ca0ab | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_ad9a53047c | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_afe18e40af | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_b9860a2de3 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_c12d73f01d | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_c589d75d2f | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_c7cf87b213 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_cc35a6d7fa | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_ce75f7fdde | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_ceb607964a | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_d06a042788 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_d4bc1d6201 | place | ZIPCODE | one row per place (ZIP is unique) |
| portal_cka_open_data_sa_d770780eeb | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_dc31e10278 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_dd50c64c64 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_e078d81651 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_e2b711db0f | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_e6366cdfc9 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_e8025ed747 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_e83e833a45 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_e8bb377538 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_e90902c24c | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_f38d25f947 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_fa2a7705ec | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_open_data_sa_fc8f1bae69 | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_03014f9c15 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_0d51ec3643 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_0e84d71b5d | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_131db5b4a0 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_151f8e4dbb | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_17dd46ea4d | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_1f745f1e15 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_2789ef054e | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_2a3d59095b | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_san_jose_open_da_2ed954c361 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_390a683a1f | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_4006091422 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_4b62ee3e47 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_5635d41e74 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_san_jose_open_da_5a544b8d01 | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_san_jose_open_da_5b443a0101 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_5ed011d868 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_788cbd21b2 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_794f17ebe2 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_7b1a49b2ac | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_804d7561a2 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_846214a7c0 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_876760587a | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_8ae30c65de | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_8bc8cd595b | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_9bcce40a0f | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_9e83620979 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_9eb7d97238 | place | LAT | one row per place (LATLON is unique) |
| portal_cka_san_jose_open_da_9f5fd1969e | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_a02c259acb | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_a1a1e9ba90 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_a52d30d858 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_ad9c79b3a8 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_b00393d49e | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_b374feda3d | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_b5470e08fd | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_b6d7cbc686 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_b7879ede0f | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_ba17cfeaef | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_cc6148cb20 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_cf566b299b | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_d8576cbeb1 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_d86291aab8 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_da9d21318d | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_e2d21c0535 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_e2e136dbe8 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_san_jose_open_da_e55babfe84 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_e5e353e19d | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_f1d1bdd645 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_f8c410bb6b | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_san_jose_open_da_faad5a2133 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_tampa_open_data_044202d137 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_2ff7ba4861 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_31262c6d5a | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_33f54db74c | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_35b3415bb7 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_39c5b89d70 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_3aa5c05b7d | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_456ec0addb | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_485b900d71 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_662d0d6bcb | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_6a2b19fd67 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_6c25ea91d4 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_7b31b708c9 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_8b7716d270 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_9909aa9ed8 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_a61789d619 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_ddbaf3b966 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_e00e42a7e9 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_e290dd0b04 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_e589c6750a | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_tampa_open_data_eaee1e870c | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| portal_cka_virginia_open_da_11b79485f6 | (unresolved -- grain proven, entity unknown) | SSWD_NP_ID | one row per record (spine_entity not determined -- no registry hint available) (SSWD_NP_ID is unique) |
| portal_cka_virginia_open_da_3bb10a6097 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_virginia_open_da_58cf45d167 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_virginia_open_da_6973fd2ba7 | place | ZIP_CODE | one row per place (ZIP is unique) |
| portal_cka_virginia_open_da_97ad4bc66c | (unresolved -- grain proven, entity unknown) | CORE_PARENT_SYS_ID | one row per record (spine_entity not determined -- no registry hint available) (CORE_PARENT_SYS_ID is unique) |
| portal_cka_virginia_open_da_ae7dccb05b | (unresolved -- grain proven, entity unknown) | OUTFALL_ID | one row per record (spine_entity not determined -- no registry hint available) (OUTFALL_ID is unique) |
| portal_cka_virginia_open_da_f40c1f2ece | place | SHAPE__LENGTH | one row per place (GEOM is unique) |
| portal_cka_virginia_open_da_f4fc6168ea | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_virginia_open_da_fc2228a15b | place | LONGITUDE_D | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_00ff03b195 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_010a1b6275 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_03ab547adb | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_0562c5dea2 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_07eaf6e647 | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_092b06e590 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_098bd87ff5 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_0ac79b8eba | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_0c27c4aa90 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_0c63c07381 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_0dd7796234 | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_10c3e0c017 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_11aebe4994 | place | GEOID | one row per place (FIPS is unique) |
| portal_cka_western_pennsylv_13793abc24 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_1430aba184 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_152133d5ed | facility | PWS_ID | one row per facility (PWSID is unique) |
| portal_cka_western_pennsylv_1629502c35 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_1a89f1526c | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_22bdd189f5 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_257ffc7619 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_26239ef185 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_26625d455c | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_2a3b161975 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_2a71c11d68 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_2c3871611d | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_2cfaaea4fd | place | GEOID10 | one row per place (FIPS is unique) |
| portal_cka_western_pennsylv_2dcbf2873b | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_305157e72f | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_321a6575f3 | place | ZIP | one row per place (ZIP is unique) |
| portal_cka_western_pennsylv_36a8032a4c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_372d1987db | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_38abdaec9d | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_3986161420 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_3e5a14a8a0 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_440a699a5b | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_49fab204aa | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_4a48dedefa | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_4c0f4e6c6c | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_4d90100824 | place | GEOID | one row per place (FIPS is unique) |
| portal_cka_western_pennsylv_4e5c66124a | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_4e9f15e555 | place | FIPS | one row per place (FIPS is unique) |
| portal_cka_western_pennsylv_55b456c408 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_5a83580b83 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_5b3c7ae148 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_5c36bf1b9f | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_6271eb297f | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_645f59a90f | place | GEOID10 | one row per place (FIPS is unique) |
| portal_cka_western_pennsylv_654e0b3182 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_68a8a0027a | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_69c80c6f70 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_6d76bcb39c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_6dc9e5d03f | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_6ea0259598 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_72f70a0697 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_769bebae41 | (unresolved -- grain proven, entity unknown) | TRIP_ID | one row per record (spine_entity not determined -- no registry hint available) (TRIP_ID is unique) |
| portal_cka_western_pennsylv_7880b791df | place | GEOID20 | one row per place (FIPS is unique) |
| portal_cka_western_pennsylv_7ac49e7444 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_82d49e467f | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_8863985427 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_8a08b89d4d | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_8b35a60c42 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_8b4d96292c | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_90a0a8b740 | (unresolved -- grain proven, entity unknown) | PARCEL_ID | one row per record (spine_entity not determined -- no registry hint available) (PARCEL_ID is unique) |
| portal_cka_western_pennsylv_90c8ee5e0c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_93f5df3d76 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_9b3ec4abb9 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_a28434a3c7 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_a3608ce8e0 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_ab591e1d68 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_abe01a0035 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_acac6b8fec | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_ad0d8250df | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_b98322d4cc | place | DATASPATIAL_WKT | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_bcbe92c64c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_bdeb900523 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_bfee19f210 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_c458f119b1 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_western_pennsylv_c7339fba3b | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_western_pennsylv_c87fa1c650 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_d179e603d1 | place | GEOID10 | one row per place (FIPS is unique) |
| portal_cka_western_pennsylv_d7da51769c | (unresolved -- grain proven, entity unknown) | PARCEL_ID | one row per record (spine_entity not determined -- no registry hint available) (PARCEL_ID is unique) |
| portal_cka_western_pennsylv_e91e8047aa | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_eac54ade9a | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_eed8a7bfa0 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_f1da76157b | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_f25943de2b | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_f37c7e01bf | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_f5e7848c24 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_f66e0e22da | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_fc5ff8e6dd | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_western_pennsylv_fde38758c9 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_024b629f91 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_0b1ba76ac0 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_191c75508b | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_1ba8209338 | (unresolved -- grain proven, entity unknown) | PARCEL_ID | one row per record (spine_entity not determined -- no registry hint available) (PARCEL_ID is unique) |
| portal_cka_wprdc_allegheny_1e2c46c189 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_1ef371e8e0 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_20bc27569a | place | GEOID10 | one row per place (FIPS is unique) |
| portal_cka_wprdc_allegheny_21287d8a95 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_2169858e8a | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_224873a888 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_2361fe1e6b | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_2525cd1bb1 | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_2c7518708c | place | GEOID10 | one row per place (FIPS is unique) |
| portal_cka_wprdc_allegheny_2d91e81224 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_2dd6b565a7 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_2e4d4f0008 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_361ce9a809 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_3719f1842e | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_38dbfe9aed | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_39aa454dda | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_3c29facd4a | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_3ced3b9382 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_4597fbdfe3 | (unresolved -- grain proven, entity unknown) | TRIP_ID | one row per record (spine_entity not determined -- no registry hint available) (TRIP_ID is unique) |
| portal_cka_wprdc_allegheny_4a2424ea96 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_4a80359b95 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_4ce939751e | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_4d7552bf98 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_4e7d1f0fea | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_4f79fa2e0c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_4f981d5bb2 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_52325c950c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_54998e6eda | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_5c657eba17 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_5fe14c3854 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_60987ada0e | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_60a2a72ffd | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_63627b65f8 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_680ea60076 | place | FIPS | one row per place (FIPS is unique) |
| portal_cka_wprdc_allegheny_694f40a849 | place | ZIP | one row per place (ZIP is unique) |
| portal_cka_wprdc_allegheny_6ac4cb010c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_6c8f129ae5 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_6f406e40a6 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_6f76317272 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_7103930983 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_7431e84319 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_7583eabd41 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_7d1a10da58 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_86091a7f3e | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_860eca7188 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_8777c10d3a | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_8afe5e2497 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_8e6bde379c | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_916d2d00a4 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_91fae70b2d | place | SHAPE_AREA | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_97a64ba0a6 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_982637b35d | place | GEOID10 | one row per place (FIPS is unique) |
| portal_cka_wprdc_allegheny_98a0e89fa3 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_99dbbb9235 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_9aed398c25 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_9bb7597d03 | place | GEOID | one row per place (FIPS is unique) |
| portal_cka_wprdc_allegheny_a2738d79af | place | GEOID | one row per place (FIPS is unique) |
| portal_cka_wprdc_allegheny_a859816f95 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_ae7030c35b | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID is unique) |
| portal_cka_wprdc_allegheny_aec3a74c1a | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_b1e95c9745 | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_b488bfab9d | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_b542229640 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_b62c61bbeb | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_b62d63f711 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_ba28cc40b7 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_bb1bd78412 | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_bbb8fb534f | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_be3c51e436 | place | LATITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_c4d59225cb | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_cc3bd4afc2 | place | GEOID20 | one row per place (FIPS is unique) |
| portal_cka_wprdc_allegheny_cc9ba8bed2 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_cda9e537dc | (unresolved -- grain proven, entity unknown) | PARCEL_ID | one row per record (spine_entity not determined -- no registry hint available) (PARCEL_ID is unique) |
| portal_cka_wprdc_allegheny_d35ad4550a | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_d5f6331dfb | place | DATASPATIAL_WKB | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_d6143bdc6c | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_ddca0024ec | place | DATASPATIAL_WKT | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_e2d2938646 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_e6260cdfe6 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_eef5b53bc5 | facility | PWS_ID | one row per facility (PWSID is unique) |
| portal_cka_wprdc_allegheny_f05d32c3d6 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_f2cf388e3d | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_fa5c68d20d | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_fa5cd1dacf | place | SHAPE_LENGTH | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_fb89781122 | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_cka_wprdc_allegheny_fbf4ba8d72 | place | LONGITUDE | one row per place (LATLON is unique) |
| portal_cka_wprdc_allegheny_fc8733f36b | place | GEOMETRY | one row per place (GEOM is unique) |
| portal_soc_cambridge_open_d_fb7c7229d0 | organization | EIN | one row per organization (EIN is unique) |
| portal_soc_colorado_informa_4bad70f01f | organization | EIN | one row per organization (EIN is unique) |
| portal_soc_connecticut_open_6be2302812 | organization | EIN | one row per organization (EIN is unique) |
| portal_soc_connecticut_open_dea6c4224a | place | ZIP_CODE | one row per place (ZIP is unique) |
| portal_soc_new_york_state_o_0c94dd2b8a | facility | NPDES_ID | one row per facility (NPDES_ID is unique) |
| portal_soc_new_york_state_o_49cd8c5b65 | asset | PATENT_NUMBER | one row per asset (PATENT is unique) |
| portal_soc_santa_clara_coun_487fcd1fab | case | DOCKET | one row per case (DOCKET is unique) |
| portal_soc_texas_open_data_24c81c0c8a | (unresolved -- grain proven, entity unknown) | TWC_ID | one row per record (spine_entity not determined -- no registry hint available) (TWC_ID is unique) |
| portal_soc_texas_open_data_b4fdc1dc58 | facility | CCN_NO | one row per facility (CCN is unique) |
| portal_soc_texas_open_data_f525266f32 | facility | CCN_NO | one row per facility (CCN is unique) |
| portal_soc_utah_open_data_p_1614522f52 | facility | NPDES_ID | one row per facility (NPDES_ID is unique) |
| portal_soc_utah_open_data_p_17cb6b615f | organization | EIN | one row per organization (EIN is unique) |
| portal_soc_utah_open_data_p_589cc47a29 | facility | NPDES_ID | one row per facility (NPDES_ID is unique) |
| portal_soc_utah_open_data_p_701571fd92 | provider | NPI | one row per provider (NPI is unique) |
| portal_soc_utah_open_data_p_8a9374ea5d | organization | EIN | one row per organization (EIN is unique) |
| portal_soc_utah_open_data_p_c357f1f9e1 | organization | PLAN_EIN | one row per organization (EIN is unique) |
| portal_soc_utah_open_data_p_dcd75231f6 | facility | PROVIDER_CCN | one row per facility (CCN is unique) |
| portal_soc_utah_open_data_p_f87fb2bfb7 | organization | EIN | one row per organization (EIN is unique) |
| portal_soc_washington_state_11cd1995b7 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID is unique) |
| xc_epa_corporate_crosswalk | facility | EPA_REGISTRY_ID,MATCHED_LEI,PARENT_CIK,PARENT_UEI,ULTIMATE_PARENT_LEI | one row per facility-organization relationship (FRS_ID+LEI+CIK+UEI+LEI is unique) |

## MEDIUM (400)

| source_id | spine_entity | natural_key | grain |
|---|---|---|---|
| FED_CFPB_COMPLAINTS | (unresolved -- grain proven, entity unknown) | Complaint ID | one row per record (spine_entity not determined -- no registry hint available) (Complaint ID unique) |
| FED_FAC_SINGLE_AUDIT | (unresolved -- grain proven, entity unknown) | REPORT_ID | one row per record (spine_entity not determined -- no registry hint available) (REPORT_ID unique) |
| FED_FEC_LEADERSHIP_PAC | (unresolved -- grain proven, entity unknown) | FEC_CANDIDATE_ID,FEC_COMMITTEE_ID | one row per record (spine_entity not determined -- no registry hint available) (FEC_CANDIDATE_ID+FEC_COMMITTEE_ID unique) |
| FED_IRS_990_EFILE_INDEX | (unresolved -- grain proven, entity unknown) | OBJECT_ID | one row per record (spine_entity not determined -- no registry hint available) (OBJECT_ID unique) |
| FED_PHMSA_FLAGGED_INCIDENTS | place | ONSHORE_POSTAL_CODE,REPORT_RECEIVED_DATE | one row per place (ZIP+REPORT_RECEIVED_DATE unique) |
| FED_USASPENDING_CONTRACTS_FULL | organization | recipient_uei,action_date,action_date_fiscal_year,period_of_performance_start_date,award_id_piid,parent_award_agency_id,parent_award_id_piid | one row per organization (UEI+action_date+action_date_fiscal_year+period_of_performance_start_date+award_id_piid+parent_award_agency_id+parent_award_id_piid unique) |
| ca_lobby_amendments | filing | FILING_ID,AMEND_ID | one row per filing (FILING_ID+AMEND_ID unique) |
| ca_lobby_cover | filing | FILING_ID,AMEND_ID | one row per filing (FILING_ID+AMEND_ID unique) |
| ca_lobby_cover2 | filing | AMEND_ID,ENTITY_ID,FILING_ID,TRAN_ID | one row per filing (AMEND_ID+ENTITY_ID+FILING_ID+TRAN_ID unique) |
| ca_lobby_emp_lobbyist | (unresolved -- grain proven, entity unknown) | LOBBYIST_ID,SESSION_ID | one row per record (spine_entity not determined -- no registry hint available) (LOBBYIST_ID+SESSION_ID unique) |
| fed_cms_federally_qualified_health_center_enrollments | (unresolved -- grain proven, entity unknown) | ENROLLMENT_ID | one row per record (spine_entity not determined -- no registry hint available) (ENROLLMENT_ID unique) |
| fed_cms_home_health_agency_enrollments | (unresolved -- grain proven, entity unknown) | ENROLLMENT_ID | one row per record (spine_entity not determined -- no registry hint available) (ENROLLMENT_ID unique) |
| fed_cms_hospice_enrollments | (unresolved -- grain proven, entity unknown) | ENROLLMENT_ID | one row per record (spine_entity not determined -- no registry hint available) (ENROLLMENT_ID unique) |
| fed_cms_hospital_compare | facility | FACILITY_ID | one row per facility (FACILITY_ID unique) |
| fed_cms_hospital_enrollments | (unresolved -- grain proven, entity unknown) | ENROLLMENT_ID | one row per record (spine_entity not determined -- no registry hint available) (ENROLLMENT_ID unique) |
| fed_cms_main | (unresolved -- grain proven, entity unknown) | DATASET_ID | one row per record (spine_entity not determined -- no registry hint available) (DATASET_ID unique) |
| fed_cms_medicare_diabetes_prevention_program | (unresolved -- grain proven, entity unknown) | UNIQUE_ID | one row per record (spine_entity not determined -- no registry hint available) (UNIQUE_ID unique) |
| fed_cms_medicare_dialysis_facilities | provider | CCN,NPI,YEAR,OWNERSHIP_TYPE,MEASURE_ID | one row per provider (CCN+NPI+YEAR+OWNERSHIP_TYPE+MEASURE_ID unique) |
| fed_cms_medicare_fee_for_service_public_provider_enrollment | (unresolved -- grain proven, entity unknown) | ENRLMT_ID | one row per record (spine_entity not determined -- no registry hint available) (ENRLMT_ID unique) |
| fed_cms_nursing_home_penalties | facility | CMS_CERTIFICATION_NUMBER_CCN,PENALTY_DATE,PAYMENT_DENIAL_START_DATE,PROCESSING_DATE,FINE_ID | one row per facility (CCN+PENALTY_DATE+PAYMENT_DENIAL_START_DATE+PROCESSING_DATE+FINE_ID unique) |
| fed_cms_open_payments | (unresolved -- grain proven, entity unknown) | RECORD_ID | one row per record (spine_entity not determined -- no registry hint available) (RECORD_ID unique) |
| fed_cms_open_payments_2022 | (unresolved -- grain proven, entity unknown) | RECORD_ID | one row per record (spine_entity not determined -- no registry hint available) (RECORD_ID unique) |
| fed_cms_open_payments_2023 | (unresolved -- grain proven, entity unknown) | RECORD_ID | one row per record (spine_entity not determined -- no registry hint available) (RECORD_ID unique) |
| fed_cms_quality_payment_program_experience | provider | NPI,CLINICIAN_TYPE,SMALL_PRACTICE_STATUS,RURAL_STATUS,MIPS_VALUE_PATHWAY_ID,QUALITY_MEASURE_ID_1,QUALITY_MEASURE_ID_2,QUALITY_MEASURE_ID_3,QUALITY_MEASURE_ID_4,QUALITY_MEASURE_ID_5,QUALITY_MEASURE_ID_6,QUALITY_MEASURE_ID_7,QUALITY_MEASURE_ID_8,QUALITY_MEASURE_ID_9,QUALITY_MEASURE_ID_10,QUALITY_MEASURE_ID_11,QUALITY_MEASURE_ID_12,CEHRT_ID,PI_MEASURE_ID_1,PI_MEASURE_ID_2,PI_MEASURE_ID_3,PI_MEASURE_ID_4,PI_MEASURE_ID_5,PI_MEASURE_ID_6,PI_MEASURE_ID_7,PI_MEASURE_ID_8,PI_MEASURE_ID_9,PI_MEASURE_ID_10,PI_MEASURE_ID_11,PI_MEASURE_ID_12,PI_MEASURE_ID_13,PI_MEASURE_ID_14,PI_MEASURE_ID_15,PI_MEASURE_ID_16,PI_MEASURE_ID_17,PI_MEASURE_ID_18,PI_MEASURE_ID_19,PI_MEASURE_ID_20,PI_MEASURE_ID_21,IA_MEASURE_ID_1,IA_MEASURE_ID_2,IA_MEASURE_ID_3,IA_MEASURE_ID_4,COST_MEASURE_ID_1,COST_MEASURE_ID_2,COST_MEASURE_ID_3,COST_MEASURE_ID_4,COST_MEASURE_ID_5,COST_MEASURE_ID_6,COST_MEASURE_ID_7,COST_MEASURE_ID_8,COST_MEASURE_ID_9,COST_MEASURE_ID_10,COST_MEASURE_ID_11,COST_MEASURE_ID_12,COST_MEASURE_ID_13,COST_MEASURE_ID_14,COST_MEASURE_ID_15,COST_MEASURE_ID_16,COST_MEASURE_ID_17,COST_MEASURE_ID_18,COST_MEASURE_ID_19,COST_MEASURE_ID_20,COST_MEASURE_ID_21,COST_MEASURE_ID_22,COST_MEASURE_ID_23,COST_MEASURE_ID_24,COST_MEASURE_ID_25,COST_MEASURE_ID_26,COST_MEASURE_ID_27,COST_MEASURE_ID_28 | one row per provider (NPI+CLINICIAN_TYPE+SMALL_PRACTICE_STATUS+RURAL_STATUS+MIPS_VALUE_PATHWAY_ID+QUALITY_MEASURE_ID_1+QUALITY_MEASURE_ID_2+QUALITY_MEASURE_ID_3+QUALITY_MEASURE_ID_4+QUALITY_MEASURE_ID_5+QUALITY_MEASURE_ID_6+QUALITY_MEASURE_ID_7+QUALITY_MEASURE_ID_8+QUALITY_MEASURE_ID_9+QUALITY_MEASURE_ID_10+QUALITY_MEASURE_ID_11+QUALITY_MEASURE_ID_12+CEHRT_ID+PI_MEASURE_ID_1+PI_MEASURE_ID_2+PI_MEASURE_ID_3+PI_MEASURE_ID_4+PI_MEASURE_ID_5+PI_MEASURE_ID_6+PI_MEASURE_ID_7+PI_MEASURE_ID_8+PI_MEASURE_ID_9+PI_MEASURE_ID_10+PI_MEASURE_ID_11+PI_MEASURE_ID_12+PI_MEASURE_ID_13+PI_MEASURE_ID_14+PI_MEASURE_ID_15+PI_MEASURE_ID_16+PI_MEASURE_ID_17+PI_MEASURE_ID_18+PI_MEASURE_ID_19+PI_MEASURE_ID_20+PI_MEASURE_ID_21+IA_MEASURE_ID_1+IA_MEASURE_ID_2+IA_MEASURE_ID_3+IA_MEASURE_ID_4+COST_MEASURE_ID_1+COST_MEASURE_ID_2+COST_MEASURE_ID_3+COST_MEASURE_ID_4+COST_MEASURE_ID_5+COST_MEASURE_ID_6+COST_MEASURE_ID_7+COST_MEASURE_ID_8+COST_MEASURE_ID_9+COST_MEASURE_ID_10+COST_MEASURE_ID_11+COST_MEASURE_ID_12+COST_MEASURE_ID_13+COST_MEASURE_ID_14+COST_MEASURE_ID_15+COST_MEASURE_ID_16+COST_MEASURE_ID_17+COST_MEASURE_ID_18+COST_MEASURE_ID_19+COST_MEASURE_ID_20+COST_MEASURE_ID_21+COST_MEASURE_ID_22+COST_MEASURE_ID_23+COST_MEASURE_ID_24+COST_MEASURE_ID_25+COST_MEASURE_ID_26+COST_MEASURE_ID_27+COST_MEASURE_ID_28 unique) |
| fed_cms_rural_health_clinic_enrollments | (unresolved -- grain proven, entity unknown) | ENROLLMENT_ID | one row per record (spine_entity not determined -- no registry hint available) (ENROLLMENT_ID unique) |
| fed_cms_skilled_nursing_facility_enrollments | (unresolved -- grain proven, entity unknown) | ENROLLMENT_ID | one row per record (spine_entity not determined -- no registry hint available) (ENROLLMENT_ID unique) |
| fed_congress_committee_membership | person | BIOGUIDE,COMMITTEE_CODE | one row per person (BIOGUIDE+COMMITTEE_CODE unique) |
| fed_consolidated_screening_list | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_courtlistener_dockets | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_courtlistener_financial_disclosures | person | PERSON_ID,DATE_CREATED,DATE_MODIFIED,YEAR,ID | one row per person (CL_PERSON_ID+DATE_CREATED+DATE_MODIFIED+YEAR+ID unique) |
| fed_courtlistener_judges | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_courtlistener_positions | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_dea_arcos_full | organization | REPORTER_DEA_NO,TRANSACTION_DATE,TRANSACTION_CODE,DRUG_CODE,TRANSACTION_ID | one row per organization (DEA_NO+TRANSACTION_DATE+TRANSACTION_CODE+DRUG_CODE+TRANSACTION_ID unique) |
| fed_densho_ddr | (unresolved -- grain proven, entity unknown) | OBJECT_ID | one row per record (spine_entity not determined -- no registry hint available) (OBJECT_ID unique) |
| fed_dhs_yearbook | place | COUNTRY_OF_LAST_RESIDENCE,FISCAL_YEAR | one row per place (COUNTRY+FISCAL_YEAR unique) |
| fed_dol_form5500 | (unresolved -- grain proven, entity unknown) | ACK_ID | one row per record (spine_entity not determined -- no registry hint available) (ACK_ID unique) |
| fed_epa_egrid_plant_2022 | facility | PLANT_FIPS_COUNTY_CODE,DATA_YEAR,DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE | one row per facility (FIPS+DATA_YEAR+DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE unique) |
| fed_epa_frs_frs_naics_codes | facility | REGISTRY_ID,NAICS_CODE,PGM_SYS_ID | one row per facility (FRS_ID+NAICS+PGM_SYS_ID unique) |
| fed_epa_frs_frs_program_links | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID unique) |
| fed_epa_frs_frs_sic_codes | facility | REGISTRY_ID,SIC_CODE,PGM_SYS_ID | one row per facility (FRS_ID+SIC+PGM_SYS_ID unique) |
| fed_epa_icis_air_icis_air_facilities | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID unique) |
| fed_epa_icis_air_icis_air_fces_pces | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID,ACTIVITY_ID | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID+ACTIVITY_ID unique) |
| fed_epa_icis_air_icis_air_formal_actions | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID,ACTIVITY_ID | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID+ACTIVITY_ID unique) |
| fed_epa_icis_air_icis_air_program_subparts | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID,PROGRAM_CODE,PROGRAM_DESC,AIR_PROGRAM_SUBPART_CODE | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID+PROGRAM_CODE+PROGRAM_DESC+AIR_PROGRAM_SUBPART_CODE unique) |
| fed_epa_icis_air_icis_air_programs | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID,BEGIN_DATE,UPDATED_DATE,PROGRAM_CODE | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID+BEGIN_DATE+UPDATED_DATE+PROGRAM_CODE unique) |
| fed_epa_icis_air_icis_air_stack_tests | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID,ACTIVITY_ID | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID+ACTIVITY_ID unique) |
| fed_epa_icis_air_icis_air_titlev_certs | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID,ACTIVITY_ID | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID+ACTIVITY_ID unique) |
| fed_epa_icis_air_icis_air_violation_history | (unresolved -- grain proven, entity unknown) | PGM_SYS_ID,ACTIVITY_ID | one row per record (spine_entity not determined -- no registry hint available) (PGM_SYS_ID+ACTIVITY_ID unique) |
| fed_epa_icis_fec_icis_fec_epa_inspections | (unresolved -- grain proven, entity unknown) | ACTIVITY_ID | one row per record (spine_entity not determined -- no registry hint available) (ACTIVITY_ID unique) |
| fed_epa_npdes_npdes_cs_violations | (unresolved -- grain proven, entity unknown) | NPDES_VIOLATION_ID | one row per record (spine_entity not determined -- no registry hint available) (NPDES_VIOLATION_ID unique) |
| fed_epa_npdes_npdes_formal_enforcement_actions | facility | NPDES_ID,SETTLEMENT_ENTERED_DATE,ACTIVITY_TYPE_CODE,ENF_TYPE_CODE,ACTIVITY_ID | one row per facility (NPDES_ID+SETTLEMENT_ENTERED_DATE+ACTIVITY_TYPE_CODE+ENF_TYPE_CODE+ACTIVITY_ID unique) |
| fed_epa_npdes_npdes_informal_enforcement_actions | (unresolved -- grain proven, entity unknown) | ACTIVITY_ID | one row per record (spine_entity not determined -- no registry hint available) (ACTIVITY_ID unique) |
| fed_epa_npdes_npdes_ps_violations | (unresolved -- grain proven, entity unknown) | NPDES_VIOLATION_ID | one row per record (spine_entity not determined -- no registry hint available) (NPDES_VIOLATION_ID unique) |
| fed_epa_npdes_npdes_se_violations | (unresolved -- grain proven, entity unknown) | NPDES_VIOLATION_ID | one row per record (spine_entity not determined -- no registry hint available) (NPDES_VIOLATION_ID unique) |
| fed_epa_sdwa_sdwa_events_milestones | facility | PWSID,EVENT_END_DATE,EVENT_ACTUAL_DATE,FIRST_REPORTED_DATE,EVENT_SCHEDULE_ID | one row per facility (PWSID+EVENT_END_DATE+EVENT_ACTUAL_DATE+FIRST_REPORTED_DATE+EVENT_SCHEDULE_ID unique) |
| fed_epa_sdwa_sdwa_facilities | facility | PWSID,FACILITY_DEACTIVATION_DATE,FIRST_REPORTED_DATE,LAST_REPORTED_DATE,FACILITY_ID,STATE_FACILITY_ID | one row per facility (PWSID+FACILITY_DEACTIVATION_DATE+FIRST_REPORTED_DATE+LAST_REPORTED_DATE+FACILITY_ID+STATE_FACILITY_ID unique) |
| fed_epa_sdwa_sdwa_geographic_areas | (unresolved -- grain proven, entity unknown) | GEO_ID | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID unique) |
| fed_epa_sdwa_sdwa_lcr_samples | (unresolved -- grain proven, entity unknown) | SAR_ID | one row per record (spine_entity not determined -- no registry hint available) (SAR_ID unique) |
| fed_epa_sdwa_sdwa_pn_violation_assoc | facility | PWSID,COMPL_PER_BEGIN_DATE,COMPL_PER_END_DATE,NON_COMPL_PER_BEGIN_DATE,PN_VIOLATION_ID,RELATED_VIOLATION_ID | one row per facility (PWSID+COMPL_PER_BEGIN_DATE+COMPL_PER_END_DATE+NON_COMPL_PER_BEGIN_DATE+PN_VIOLATION_ID+RELATED_VIOLATION_ID unique) |
| fed_epa_sdwa_sdwa_service_areas | facility | PWSID,FIRST_REPORTED_DATE,LAST_REPORTED_DATE,SERVICE_AREA_TYPE_CODE | one row per facility (PWSID+FIRST_REPORTED_DATE+LAST_REPORTED_DATE+SERVICE_AREA_TYPE_CODE unique) |
| fed_epa_sdwa_sdwa_site_visits | facility | PWSID,VISIT_DATE,FIRST_REPORTED_DATE,LAST_REPORTED_DATE | one row per facility (PWSID+VISIT_DATE+FIRST_REPORTED_DATE+LAST_REPORTED_DATE unique) |
| fed_epa_sdwa_sdwa_violations_enforcement | facility | PWSID,COMPL_PER_BEGIN_DATE,COMPL_PER_END_DATE,NON_COMPL_PER_BEGIN_DATE,VIOLATION_ID,FACILITY_ID,SAMPLE_RESULT_ID,CORRECTIVE_ACTION_ID,ENFORCEMENT_ID | one row per facility (PWSID+COMPL_PER_BEGIN_DATE+COMPL_PER_END_DATE+NON_COMPL_PER_BEGIN_DATE+VIOLATION_ID+FACILITY_ID+SAMPLE_RESULT_ID+CORRECTIVE_ACTION_ID+ENFORCEMENT_ID unique) |
| fed_epa_tri_basic_2023 | facility | C_3_FRS_ID,C_1_YEAR,C_22_INDUSTRY_SECTOR_CODE,C_23_INDUSTRY_SECTOR,C_39_TRI_CHEMICAL_COMPOUND_ID,C_41_SRS_ID | one row per facility (FRS_ID+C_1_YEAR+C_22_INDUSTRY_SECTOR_CODE+C_23_INDUSTRY_SECTOR+C_39_TRI_CHEMICAL_COMPOUND_ID+C_41_SRS_ID unique) |
| fed_faa_aircraft_registry | (unresolved -- grain proven, entity unknown) | UNIQUE_ID | one row per record (spine_entity not determined -- no registry hint available) (UNIQUE_ID unique) |
| fed_fdic_bank_data | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_fdic_failed_banks | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_fec_api | (unresolved -- grain proven, entity unknown) | TRANSACTION_ID | one row per record (spine_entity not determined -- no registry hint available) (TRANSACTION_ID unique) |
| fed_fec_bulk_candidates | person | CAND_ID,CAND_ELECTION_YR,CYCLE | one row per person (FEC_CAND_ID+CAND_ELECTION_YR+CYCLE unique) |
| fed_fec_bulk_linkages | (unresolved -- grain proven, entity unknown) | LINKAGE_ID | one row per record (spine_entity not determined -- no registry hint available) (LINKAGE_ID unique) |
| fed_fec_bulk_summary | person | CAND_ID,CYCLE | one row per person (FEC_CAND_ID+CYCLE unique) |
| fed_fec_committee_to_candidate | (unresolved -- grain proven, entity unknown) | SUB_ID | one row per record (spine_entity not determined -- no registry hint available) (SUB_ID unique) |
| fed_fec_indiv_contributions | (unresolved -- grain proven, entity unknown) | SUB_ID | one row per record (spine_entity not determined -- no registry hint available) (SUB_ID unique) |
| fed_google_polads_advertiser_weekly_spend | (unresolved -- grain proven, entity unknown) | ADVERTISER_ID,ELECTION_CYCLE,WEEK_START_DATE | one row per record (spine_entity not determined -- no registry hint available) (ADVERTISER_ID+ELECTION_CYCLE+WEEK_START_DATE unique) |
| fed_ice_detention_stints | (unresolved -- grain proven, entity unknown) | STINT_ID | one row per record (spine_entity not determined -- no registry hint available) (STINT_ID unique) |
| fed_icij_offshoreleaks_addresses | (unresolved -- grain proven, entity unknown) | NODE_ID | one row per record (spine_entity not determined -- no registry hint available) (NODE_ID unique) |
| fed_icij_offshoreleaks_entities | (unresolved -- grain proven, entity unknown) | NODE_ID | one row per record (spine_entity not determined -- no registry hint available) (NODE_ID unique) |
| fed_icij_offshoreleaks_intermediaries | (unresolved -- grain proven, entity unknown) | NODE_ID | one row per record (spine_entity not determined -- no registry hint available) (NODE_ID unique) |
| fed_icij_offshoreleaks_officers | (unresolved -- grain proven, entity unknown) | NODE_ID | one row per record (spine_entity not determined -- no registry hint available) (NODE_ID unique) |
| fed_icij_offshoreleaks_others | (unresolved -- grain proven, entity unknown) | NODE_ID | one row per record (spine_entity not determined -- no registry hint available) (NODE_ID unique) |
| fed_nid_dams | (unresolved -- grain proven, entity unknown) | NID_ID | one row per record (spine_entity not determined -- no registry hint available) (NID_ID unique) |
| fed_nih_reporter | (unresolved -- grain proven, entity unknown) | APPL_ID | one row per record (spine_entity not determined -- no registry hint available) (APPL_ID unique) |
| fed_noaa_storm_events | event | EVENT_ID | one row per event (EVENT_ID unique) |
| fed_noaa_weather_api | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_ntsb_aviation_aircraft | (unresolved -- grain proven, entity unknown) | EV_ID | one row per record (spine_entity not determined -- no registry hint available) (EV_ID unique) |
| fed_ntsb_aviation_events | (unresolved -- grain proven, entity unknown) | EV_ID | one row per record (spine_entity not determined -- no registry hint available) (EV_ID unique) |
| fed_osha_ita_300a_summary_2023 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_osha_ita_300a_summary_2024 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_osha_ita_300a_summary_2025 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_osha_ita_case_detail_2023 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_osha_ita_case_detail_2024 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_osha_ita_case_detail_2025 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_pbgc_trusteed_plans | organization | EIN,DATE_OF_PLAN_TERMINATION,DATE_OF_PBGC_TRUSTEESHIP,NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION | one row per organization (EIN+DATE_OF_PLAN_TERMINATION+DATE_OF_PBGC_TRUSTEESHIP+NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION unique) |
| fed_retraction_watch | (unresolved -- grain proven, entity unknown) | RECORD_ID | one row per record (spine_entity not determined -- no registry hint available) (RECORD_ID unique) |
| fed_sec_dera_sub_2025q4 | organization | CIK,PERIOD,FY | one row per organization (CIK+PERIOD+FY unique) |
| fed_sec_dera_sub_2026q1 | organization | CIK,PERIOD,FY | one row per organization (CIK+PERIOD+FY unique) |
| fed_treasury_mts_receipts | (unresolved -- grain proven, entity unknown) | PARENT_ID,CLASSIFICATION_ID | one row per record (spine_entity not determined -- no registry hint available) (PARENT_ID+CLASSIFICATION_ID unique) |
| fed_us_usaspending_api | (unresolved -- grain proven, entity unknown) | AWARD_ID | one row per record (spine_entity not determined -- no registry hint available) (AWARD_ID unique) |
| fed_usace_nid_dams | (unresolved -- grain proven, entity unknown) | NID_ID | one row per record (spine_entity not determined -- no registry hint available) (NID_ID unique) |
| fed_usaspending_bulk | organization | RECIPIENT_UEI,ACTION_DATE,ACTION_DATE_FISCAL_YEAR,PERIOD_OF_PERFORMANCE_START_DATE,AWARD_ID_PIID,PARENT_AWARD_AGENCY_ID,PARENT_AWARD_ID_PIID | one row per organization (UEI+ACTION_DATE+ACTION_DATE_FISCAL_YEAR+PERIOD_OF_PERFORMANCE_START_DATE+AWARD_ID_PIID+PARENT_AWARD_AGENCY_ID+PARENT_AWARD_ID_PIID unique) |
| fed_usaspending_contracts | organization | RECIPIENT_UEI,ACTION_DATE,PERIOD_OF_PERFORMANCE_START_DATE,PERIOD_OF_PERFORMANCE_CURRENT_END_DATE,AWARD_ID_PIID | one row per organization (UEI+ACTION_DATE+PERIOD_OF_PERFORMANCE_START_DATE+PERIOD_OF_PERFORMANCE_CURRENT_END_DATE+AWARD_ID_PIID unique) |
| fed_usaspending_contracts_full_r2 | organization | RECIPIENT_UEI,ACTION_DATE,PERIOD_OF_PERFORMANCE_START_DATE,PERIOD_OF_PERFORMANCE_CURRENT_END_DATE,AWARD_ID_PIID | one row per organization (UEI+ACTION_DATE+PERIOD_OF_PERFORMANCE_START_DATE+PERIOD_OF_PERFORMANCE_CURRENT_END_DATE+AWARD_ID_PIID unique) |
| fed_usgs_earthquakes | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| fed_usgs_minerals | (unresolved -- grain proven, entity unknown) | DEP_ID | one row per record (spine_entity not determined -- no registry hint available) (DEP_ID unique) |
| fed_wpa_slave_narratives | (unresolved -- grain proven, entity unknown) | LOC_ITEM_ID | one row per record (spine_entity not determined -- no registry hint available) (LOC_ITEM_ID unique) |
| intl_eu_sanctions | place | ADDR_ZIPCODE,DATE_FILE,LEBA_PUBLICATION_DATE,NAAL_LEBA_PUBLICATION_DATE,ENTITY_LOGICAL_ID,NAAL_LOGICAL_ID,ENTITY_LOGICAL_ID_1,ENTITY_LOGICAL_ID_2,BIRT_LOGICAL_ID,ENTITY_LOGICAL_ID_3,IDEN_LOGICAL_ID,ENTITY_LOGICAL_ID_4,CITI_LOGICAL_ID,ENTITY_LOGICAL_ID_5 | one row per place (ZIP+DATE_FILE+LEBA_PUBLICATION_DATE+NAAL_LEBA_PUBLICATION_DATE+ENTITY_LOGICAL_ID+NAAL_LOGICAL_ID+ENTITY_LOGICAL_ID_1+ENTITY_LOGICAL_ID_2+BIRT_LOGICAL_ID+ENTITY_LOGICAL_ID_3+IDEN_LOGICAL_ID+ENTITY_LOGICAL_ID_4+CITI_LOGICAL_ID+ENTITY_LOGICAL_ID_5 unique) |
| intl_fr_data_gouv | (unresolved -- grain proven, entity unknown) | DATASET_ID,RESOURCE_ID | one row per record (spine_entity not determined -- no registry hint available) (DATASET_ID+RESOURCE_ID unique) |
| intl_gem_hazard | (unresolved -- grain proven, entity unknown) | HAZARD_MODEL_ID | one row per record (spine_entity not determined -- no registry hint available) (HAZARD_MODEL_ID unique) |
| intl_gleif_repex | organization | LEI,EXCEPTION_CATEGORY | one row per organization (LEI+EXCEPTION_CATEGORY unique) |
| intl_hudoc | case | CASE_ID | one row per case (CASE_ID unique) |
| intl_ucdp_ged | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| intl_wb_ids | place | COUNTRY_CODE,COUNTERPART_AREA_CODE,SERIES_CODE | one row per place (COUNTRY+COUNTERPART_AREA_CODE+SERIES_CODE unique) |
| irs527_8871_orgs | (unresolved -- grain proven, entity unknown) | FORM_ID_NUMBER | one row per record (spine_entity not determined -- no registry hint available) (FORM_ID_NUMBER unique) |
| irs527_8872_reports | (unresolved -- grain proven, entity unknown) | FORM_ID_NUMBER | one row per record (spine_entity not determined -- no registry hint available) (FORM_ID_NUMBER unique) |
| irs527_directors_officers | (unresolved -- grain proven, entity unknown) | DIRECTOR_ID | one row per record (spine_entity not determined -- no registry hint available) (DIRECTOR_ID unique) |
| irs527_eain | (unresolved -- grain proven, entity unknown) | FORM_ID_NUMBER,EAIN_ID | one row per record (spine_entity not determined -- no registry hint available) (FORM_ID_NUMBER+EAIN_ID unique) |
| irs527_related_entities | (unresolved -- grain proven, entity unknown) | ENTITY_ID | one row per record (spine_entity not determined -- no registry hint available) (ENTITY_ID unique) |
| portal_arc_atlanta_dataatla_1a7f4adc21 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_atlanta_dataatla_4ab9f9e31e | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_atlanta_dataatla_51a606f539 | place | LONGITUDE,BUSINESS_LICENSE_YEAR,DATE_OF_OPENING_IN_ATLANTA,PREVIOUS_YEAR_REPORTED_REVENUE | one row per place (LATLON+BUSINESS_LICENSE_YEAR+DATE_OF_OPENING_IN_ATLANTA+PREVIOUS_YEAR_REPORTED_REVENUE unique) |
| portal_arc_atlanta_dataatla_5d9b9c30a9 | place | ZIP,INDUSTRY_DESC | one row per place (ZIP+INDUSTRY_DESC unique) |
| portal_arc_atlanta_dataatla_79e3c7bd36 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_atlanta_dataatla_a59db2e766 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_atlanta_dataatla_de1e9d4350 | (unresolved -- grain proven, entity unknown) | USER_FORMATTED_ID | one row per record (spine_entity not determined -- no registry hint available) (USER_FORMATTED_ID unique) |
| portal_arc_atlanta_dataatla_ead25cbdc7 | place | LONGITUDE,BUSINESS_LICENSE_YEAR,DATE_OF_OPENING_IN_ATLANTA,PREVIOUS_YEAR_REPORTED_REVENUE | one row per place (LATLON+BUSINESS_LICENSE_YEAR+DATE_OF_OPENING_IN_ATLANTA+PREVIOUS_YEAR_REPORTED_REVENUE unique) |
| portal_arc_atlanta_dataatla_fd3576897b | place | ZIP,INDUSTRY_DESC | one row per place (ZIP+INDUSTRY_DESC unique) |
| portal_arc_harris_county_op_12691a85a0 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_1966ac023b | place | ZIP,VAL_DATE | one row per place (ZIP+VAL_DATE unique) |
| portal_arc_harris_county_op_1a53499962 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_2d6f9d0da7 | (unresolved -- grain proven, entity unknown) | OBJECT_ID | one row per record (spine_entity not determined -- no registry hint available) (OBJECT_ID unique) |
| portal_arc_harris_county_op_3cfe4113ed | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_3e1426df10 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_6cdcf96ca7 | place | ZIP,VAL_DATE,IN_100_YR_FLOODPLAIN,IN_500_YR_FLOODPLAIN,ID,STATE_ID | one row per place (ZIP+VAL_DATE+IN_100_YR_FLOODPLAIN+IN_500_YR_FLOODPLAIN+ID+STATE_ID unique) |
| portal_arc_harris_county_op_8549ec1226 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_87f4853c1a | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_a2dae85c30 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_d354d2d6e2 | (unresolved -- grain proven, entity unknown) | OBJECT_ID | one row per record (spine_entity not determined -- no registry hint available) (OBJECT_ID unique) |
| portal_arc_harris_county_op_d9a3089ed0 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_e87e81379a | place | ZIP,VAL_DATE,IN_100_YR_FLOODPLAIN,IN_500_YR_FLOODPLAIN,ID,STATE_ID | one row per place (ZIP+VAL_DATE+IN_100_YR_FLOODPLAIN+IN_500_YR_FLOODPLAIN+ID+STATE_ID unique) |
| portal_arc_harris_county_op_ede1e11f9d | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_harris_county_op_f3d3a3ab57 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_la_county_open_d_0a94db308e | provider | CCN,NPI,PARTICIPATION_DATE,APPROVAL_DATE,START_DATE | one row per provider (CCN+NPI+PARTICIPATION_DATE+APPROVAL_DATE+START_DATE unique) |
| portal_arc_la_county_open_d_2e79eb67c8 | place | SAFEGRAPH_PLACE_ID | one row per place (SAFEGRAPH_PLACE_ID unique) |
| portal_arc_la_county_open_d_75836d970c | (unresolved -- grain proven, entity unknown) | FAC_ID | one row per record (spine_entity not determined -- no registry hint available) (FAC_ID unique) |
| portal_arc_la_county_open_d_d75e8ea051 | facility | TRI_FACILITY_ID | one row per facility (TRI_FACILITY_ID unique) |
| portal_arc_la_county_open_d_e034245e05 | provider | NPI,SCC_TYPE | one row per provider (NPI+SCC_TYPE unique) |
| portal_arc_la_county_open_d_e549c7c921 | facility | TRI_FACILITY_ID | one row per facility (TRI_FACILITY_ID unique) |
| portal_arc_new_mexico_open_1b6c7f7fbd | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_arc_open_baltimore_751d91c991 | facility | CCN,TYPE | one row per facility (CCN+TYPE unique) |
| portal_arc_open_data_dc_582a28d212 | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID unique) |
| portal_arc_open_data_dc_59913164d2 | (unresolved -- grain proven, entity unknown) | EGIS_ID | one row per record (spine_entity not determined -- no registry hint available) (EGIS_ID unique) |
| portal_arc_open_data_dc_5b867c795c | facility | CCN_REV,DATE | one row per facility (CCN+DATE unique) |
| portal_arc_open_data_dc_5cb81acbdd | place | SAFEGRAPH_PLACE_ID | one row per place (SAFEGRAPH_PLACE_ID unique) |
| portal_arc_open_data_dc_74d9616143 | (unresolved -- grain proven, entity unknown) | EGIS_ID | one row per record (spine_entity not determined -- no registry hint available) (EGIS_ID unique) |
| portal_arc_open_data_dc_adf4f0e413 | place | SAFEGRAPH_PLACE_ID | one row per place (SAFEGRAPH_PLACE_ID unique) |
| portal_arc_open_data_dc_d359158bc8 | (unresolved -- grain proven, entity unknown) | INFOUSA_ID | one row per record (spine_entity not determined -- no registry hint available) (INFOUSA_ID unique) |
| portal_arc_open_data_dc_d8e55d5b7f | facility | CCN_REV,DATE | one row per facility (CCN+DATE unique) |
| portal_arc_open_data_dc_e1dd5d3551 | (unresolved -- grain proven, entity unknown) | UNIQUE_ID | one row per record (spine_entity not determined -- no registry hint available) (UNIQUE_ID unique) |
| portal_arc_open_data_dc_f37f5ddc3d | (unresolved -- grain proven, entity unknown) | ANC_ID | one row per record (spine_entity not determined -- no registry hint available) (ANC_ID unique) |
| portal_arc_open_data_raleig_5e5b26dc88 | (unresolved -- grain proven, entity unknown) | INFOUSA_ID | one row per record (spine_entity not determined -- no registry hint available) (INFOUSA_ID unique) |
| portal_arc_open_data_raleig_8ee851c810 | (unresolved -- grain proven, entity unknown) | INFOUSA_ID | one row per record (spine_entity not determined -- no registry hint available) (INFOUSA_ID unique) |
| portal_arc_open_data_raleig_df19dcbb03 | (unresolved -- grain proven, entity unknown) | INFOUSA_ID | one row per record (spine_entity not determined -- no registry hint available) (INFOUSA_ID unique) |
| portal_arc_open_data_raleig_efbb617010 | (unresolved -- grain proven, entity unknown) | INFOUSA_ID | one row per record (spine_entity not determined -- no registry hint available) (INFOUSA_ID unique) |
| portal_arc_open_data_raleig_f18f09f22f | place | SHIPPING_ZIP_POSTAL_CODE,APPLICATION_DATE | one row per place (ZIP+APPLICATION_DATE unique) |
| portal_arc_orange_county_op_05390f8d55 | (unresolved -- grain proven, entity unknown) | INVENTORY_ID | one row per record (spine_entity not determined -- no registry hint available) (INVENTORY_ID unique) |
| portal_arc_orange_county_op_0dea033879 | (unresolved -- grain proven, entity unknown) | INVENTORY_ID | one row per record (spine_entity not determined -- no registry hint available) (INVENTORY_ID unique) |
| portal_arc_orange_county_op_2f4310b675 | facility | FACILITY_ID | one row per facility (FACILITY_ID unique) |
| portal_arc_orange_county_op_41e4e2185f | (unresolved -- grain proven, entity unknown) | INVENTORY_ID | one row per record (spine_entity not determined -- no registry hint available) (INVENTORY_ID unique) |
| portal_arc_orange_county_op_43a1fe3fbe | (unresolved -- grain proven, entity unknown) | INVENTORY_ID | one row per record (spine_entity not determined -- no registry hint available) (INVENTORY_ID unique) |
| portal_arc_orange_county_op_572f3c6271 | facility | FACILITY_ID | one row per facility (FACILITY_ID unique) |
| portal_arc_orange_county_op_62e4574f5e | facility | FACILITY_ID | one row per facility (FACILITY_ID unique) |
| portal_arc_orange_county_op_644fb9535b | place | ZIP,INSPECTION_DATE,OPERATIONAL_STATUS,PROGRAM_ELEMENT | one row per place (ZIP+INSPECTION_DATE+OPERATIONAL_STATUS+PROGRAM_ELEMENT unique) |
| portal_arc_orange_county_op_dd64a3f2b8 | facility | FACILITY_ID | one row per facility (FACILITY_ID unique) |
| portal_arc_tn_data_tennesse_655f6bcc6d | (unresolved -- grain proven, entity unknown) | INFOUSA_ID | one row per record (spine_entity not determined -- no registry hint available) (INFOUSA_ID unique) |
| portal_arc_tucson_open_data_14c7aa5ccf | place | ZIP,INDUSTRY_DESC | one row per place (ZIP+INDUSTRY_DESC unique) |
| portal_arc_tucson_open_data_32a72d9d1d | place | ZIP,INDUSTRY_DESC | one row per place (ZIP+INDUSTRY_DESC unique) |
| portal_arc_tucson_open_data_3a7e0821d1 | case | DOCKET,LAST_EDITED_DATE | one row per case (DOCKET+LAST_EDITED_DATE unique) |
| portal_arc_tucson_open_data_55d5164315 | (unresolved -- grain proven, entity unknown) | SCHOOLS_UNIVERSAL_ID | one row per record (spine_entity not determined -- no registry hint available) (SCHOOLS_UNIVERSAL_ID unique) |
| portal_arc_tucson_open_data_63c0193ff1 | case | DOCKET,LAST_EDITED_DATE | one row per case (DOCKET+LAST_EDITED_DATE unique) |
| portal_arc_tucson_open_data_7468cf46db | case | DOCKET,LAST_EDITED_DATE | one row per case (DOCKET+LAST_EDITED_DATE unique) |
| portal_arc_tucson_open_data_cdffe1002a | case | DOCKET,LAST_EDITED_DATE | one row per case (DOCKET+LAST_EDITED_DATE unique) |
| portal_arc_tucson_open_data_e0edea39be | place | ZIP,INDUSTRY_DESC | one row per place (ZIP+INDUSTRY_DESC unique) |
| portal_arc_tucson_open_data_f0203665dd | place | ZIP,INDUSTRY_DESC | one row per place (ZIP+INDUSTRY_DESC unique) |
| portal_arc_tucson_open_data_f919285f50 | case | DOCKET,LAST_EDITED_DATE | one row per case (DOCKET+LAST_EDITED_DATE unique) |
| portal_arc_wisconsin_open_d_022efd1ae5 | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID unique) |
| portal_arc_wisconsin_open_d_4ebc995c5d | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID unique) |
| portal_arc_wisconsin_open_d_5206358bdd | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID unique) |
| portal_arc_wisconsin_open_d_717f8037eb | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID unique) |
| portal_arc_wisconsin_open_d_b2efa24715 | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID unique) |
| portal_arc_wisconsin_open_d_cb1509f410 | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID unique) |
| portal_arc_wisconsin_open_d_d05399642c | (unresolved -- grain proven, entity unknown) | GIS_ID | one row per record (spine_entity not determined -- no registry hint available) (GIS_ID unique) |
| portal_cka_analyze_boston_0012b002be | place | SHAPE_WKT,DATE_AND_TIME | one row per place (GEOM+DATE_AND_TIME unique) |
| portal_cka_analyze_boston_0f7b6b1f80 | (unresolved -- grain proven, entity unknown) | NEIGHBORHOOD_ID | one row per record (spine_entity not determined -- no registry hint available) (NEIGHBORHOOD_ID unique) |
| portal_cka_analyze_boston_1321cb60b5 | place | LAT,DATE_TIME | one row per place (LATLON+DATE_TIME unique) |
| portal_cka_analyze_boston_4eddc3919b | place | ZIP_CODE,APPLICATION_DATE | one row per place (ZIP+APPLICATION_DATE unique) |
| portal_cka_analyze_boston_5288db6955 | place | SHAPE_WKT,DATE_DESIGNATED_1,CREATED_DATE,LAST_EDITED_DATE,UNIQUE_ID | one row per place (GEOM+DATE_DESIGNATED_1+CREATED_DATE+LAST_EDITED_DATE+UNIQUE_ID unique) |
| portal_cka_analyze_boston_5ccb249b71 | (unresolved -- grain proven, entity unknown) | SWK_ID | one row per record (spine_entity not determined -- no registry hint available) (SWK_ID unique) |
| portal_cka_analyze_boston_5fc2a4d010 | (unresolved -- grain proven, entity unknown) | POLYGON_ID | one row per record (spine_entity not determined -- no registry hint available) (POLYGON_ID unique) |
| portal_cka_analyze_boston_7d75fd803f | (unresolved -- grain proven, entity unknown) | CSP_SCH_ID | one row per record (spine_entity not determined -- no registry hint available) (CSP_SCH_ID unique) |
| portal_cka_analyze_boston_7f82f529e8 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_analyze_boston_824b1b659e | (unresolved -- grain proven, entity unknown) | PROJECT_ID | one row per record (spine_entity not determined -- no registry hint available) (PROJECT_ID unique) |
| portal_cka_analyze_boston_9fe0838e9f | place | ZIPCODE,DATE_BUSINESS_ESTABLISHED,BUSINESS_TYPE,COB_CATEGORY_CODES1 | one row per place (ZIP+DATE_BUSINESS_ESTABLISHED+BUSINESS_TYPE+COB_CATEGORY_CODES1 unique) |
| portal_cka_analyze_boston_a6c2b4684a | (unresolved -- grain proven, entity unknown) | TOWNS_ID | one row per record (spine_entity not determined -- no registry hint available) (TOWNS_ID unique) |
| portal_cka_analyze_boston_b6c7223760 | (unresolved -- grain proven, entity unknown) | OS_ID | one row per record (spine_entity not determined -- no registry hint available) (OS_ID unique) |
| portal_cka_analyze_boston_bbe6f0fd04 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_analyze_boston_d5a9ad584e | place | ZIP_CODE,PERMIT_APPLICATION_FILING_DATE,PERMIT_ISSUED_DATE,REZONING_EFFECTIVE_DATE,PARCEL_ID,SAM_ID | one row per place (ZIP+PERMIT_APPLICATION_FILING_DATE+PERMIT_ISSUED_DATE+REZONING_EFFECTIVE_DATE+PARCEL_ID+SAM_ID unique) |
| portal_cka_analyze_boston_db29ec5366 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_analyze_boston_dd269d0a1d | place | ZIP_R,SEGMENT_ID | one row per place (ZIP+SEGMENT_ID unique) |
| portal_cka_analyze_boston_e4c004d662 | case | CASE_ID | one row per case (CASE_ID unique) |
| portal_cka_analyze_boston_f1b3f76830 | place | CONTACT_ZIP,STATUS_DTTM | one row per place (ZIP+STATUS_DTTM unique) |
| portal_cka_california_open_0ad648012f | (unresolved -- grain proven, entity unknown) | STATION_ID | one row per record (spine_entity not determined -- no registry hint available) (STATION_ID unique) |
| portal_cka_california_open_3501b678fa | facility | PWSID,SYSTEM_START_DATE,SYSTEM_END_DATE,APPLICABLE_START_DATE | one row per facility (PWSID+SYSTEM_START_DATE+SYSTEM_END_DATE+APPLICABLE_START_DATE unique) |
| portal_cka_california_open_35e42b9770 | (unresolved -- grain proven, entity unknown) | ORG_ID,WATER_SYSTEM_ID,REPORT_PERIOD_START_DATE | one row per record (spine_entity not determined -- no registry hint available) (ORG_ID+WATER_SYSTEM_ID+REPORT_PERIOD_START_DATE unique) |
| portal_cka_california_open_3b70ad4f80 | (unresolved -- grain proven, entity unknown) | STN_ID | one row per record (spine_entity not determined -- no registry hint available) (STN_ID unique) |
| portal_cka_california_open_490b55c81b | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_california_open_6611464444 | place | LONGITUDE,SITE_CODE | one row per place (LATLON+SITE_CODE unique) |
| portal_cka_california_open_a5d78a8b63 | place | LATITUDE,LAST_MODIFIED_DATE,DATE_DATA_REFERS_TO,DWR_GW_SITE_CODE | one row per place (LATLON+LAST_MODIFIED_DATE+DATE_DATA_REFERS_TO+DWR_GW_SITE_CODE unique) |
| portal_cka_california_open_ac6c9e2b47 | (unresolved -- grain proven, entity unknown) | STN_ID | one row per record (spine_entity not determined -- no registry hint available) (STN_ID unique) |
| portal_cka_california_open_c19a7c8625 | facility | PWS_ID_OR_OTHER_ID,SUBMITTED_DATE | one row per facility (PWSID+SUBMITTED_DATE unique) |
| portal_cka_california_open_c65b641866 | (unresolved -- grain proven, entity unknown) | STATION_ID | one row per record (spine_entity not determined -- no registry hint available) (STATION_ID unique) |
| portal_cka_california_open_f8f7b5716b | (unresolved -- grain proven, entity unknown) | ORG_ID,FY_START_DATE | one row per record (spine_entity not determined -- no registry hint available) (ORG_ID+FY_START_DATE unique) |
| portal_cka_houston_open_dat_07c9c99eb1 | event | TEMP_EVENT_ID,INSPECTION_DATE,ACTIVITY_TYPE,STAFF_CODE | one row per event (TEMP_EVENT_ID+INSPECTION_DATE+ACTIVITY_TYPE+STAFF_CODE unique) |
| portal_cka_houston_open_dat_1629ef6392 | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_19cbd263cc | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_2e1926ecb2 | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_399393985d | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_5848c85560 | (unresolved -- grain proven, entity unknown) | TRANSPORTATION_ID,VEHICLE_ID | one row per record (spine_entity not determined -- no registry hint available) (TRANSPORTATION_ID+VEHICLE_ID unique) |
| portal_cka_houston_open_dat_702315b033 | (unresolved -- grain proven, entity unknown) | TRANSPORTATION_ID | one row per record (spine_entity not determined -- no registry hint available) (TRANSPORTATION_ID unique) |
| portal_cka_houston_open_dat_76e445329f | (unresolved -- grain proven, entity unknown) | TRANSPORTATION_ID,VEHICLE_ID | one row per record (spine_entity not determined -- no registry hint available) (TRANSPORTATION_ID+VEHICLE_ID unique) |
| portal_cka_houston_open_dat_7a8148751c | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_a4490182ba | place | ZIPCODE,SR_CREATE_DATE,DUE_DATE,DATE_CLOSED,TAX_ID | one row per place (ZIP+SR_CREATE_DATE+DUE_DATE+DATE_CLOSED+TAX_ID unique) |
| portal_cka_houston_open_dat_aa67e5b416 | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_ab35bb6552 | place | ZIP,IN_DATE,DUE_DATE,OUT_DATE,ID | one row per place (ZIP+IN_DATE+DUE_DATE+OUT_DATE+ID unique) |
| portal_cka_houston_open_dat_aeb065e230 | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_bdf3a70a86 | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_cfdcdf13fd | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_houston_open_dat_f572136326 | (unresolved -- grain proven, entity unknown) | GEO_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (GEO_ID+YEAR unique) |
| portal_cka_indiana_data_hub_7747efe139 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_indiana_data_hub_78f3e49d13 | place | COUNTY_FIPS,SCHOOL_YEAR,SUBMISSION_STATUS,SCHOOL_ID | one row per place (FIPS+SCHOOL_YEAR+SUBMISSION_STATUS+SCHOOL_ID unique) |
| portal_cka_indiana_data_hub_83ba6435c2 | (unresolved -- grain proven, entity unknown) | LOCATION_ID,DATE | one row per record (spine_entity not determined -- no registry hint available) (LOCATION_ID+DATE unique) |
| portal_cka_indiana_data_hub_d4dae8d984 | place | ZIPCODE,YEAR,AGE_GROUP | one row per place (ZIP+YEAR+AGE_GROUP unique) |
| portal_cka_indiana_data_hub_fe00d42acc | place | FIPS,DATE | one row per place (FIPS+DATE unique) |
| portal_cka_israel_national_03d9d0d534 | place | ZIPCODE,OPEN_DATE,CLOSE_DATE,BRANCH_CODE,ID | one row per place (ZIP+OPEN_DATE+CLOSE_DATE+BRANCH_CODE+ID unique) |
| portal_cka_israel_national_07ec1af377 | (unresolved -- grain proven, entity unknown) | DEACEASED_ID,DEACEASED_DATE | one row per record (spine_entity not determined -- no registry hint available) (DEACEASED_ID+DEACEASED_DATE unique) |
| portal_cka_israel_national_32cf786f4c | (unresolved -- grain proven, entity unknown) | PROJECT_ID,BUILDING_ID | one row per record (spine_entity not determined -- no registry hint available) (PROJECT_ID+BUILDING_ID unique) |
| portal_cka_israel_national_338ef2b642 | (unresolved -- grain proven, entity unknown) | FUND_ID,MANAGING_CORPORATION_LEGAL_ID,REPORT_PERIOD | one row per record (spine_entity not determined -- no registry hint available) (FUND_ID+MANAGING_CORPORATION_LEGAL_ID+REPORT_PERIOD unique) |
| portal_cka_israel_national_44788840fc | (unresolved -- grain proven, entity unknown) | EQUIPMENT_GROUP_ID,MANUFACTER_ID,MODEL_ID | one row per record (spine_entity not determined -- no registry hint available) (EQUIPMENT_GROUP_ID+MANUFACTER_ID+MODEL_ID unique) |
| portal_cka_israel_national_511b70eb2b | (unresolved -- grain proven, entity unknown) | BUS_LICENSE_ID | one row per record (spine_entity not determined -- no registry hint available) (BUS_LICENSE_ID unique) |
| portal_cka_israel_national_6272f09a75 | place | ZIP_CODE,CATEGORY,BANK_CODE | one row per place (ZIP+CATEGORY+BANK_CODE unique) |
| portal_cka_israel_national_6c5e40114c | (unresolved -- grain proven, entity unknown) | FUND_ID,REPORT_PERIOD | one row per record (spine_entity not determined -- no registry hint available) (FUND_ID+REPORT_PERIOD unique) |
| portal_cka_israel_national_c05e5881a0 | place | ZIP_CODE,INSTITUTE_CODE | one row per place (ZIP+INSTITUTE_CODE unique) |
| portal_cka_israel_national_d59087e169 | (unresolved -- grain proven, entity unknown) | FUND_ID,MANAGING_CORPORATION_LEGAL_ID,REPORT_PERIOD | one row per record (spine_entity not determined -- no registry hint available) (FUND_ID+MANAGING_CORPORATION_LEGAL_ID+REPORT_PERIOD unique) |
| portal_cka_israel_national_e3d369b05f | place | STN_LAT,DATE_OPEN,DATE_CLOSE | one row per place (LATLON+DATE_OPEN+DATE_CLOSE unique) |
| portal_cka_open_data_sa_1c37ee3869 | place | SHAPE__LENGTH,FISCAL_YEAR | one row per place (GEOM+FISCAL_YEAR unique) |
| portal_cka_open_data_sa_2fcd3aefd6 | place | SHAPE__LENGTH,CREATED_DATE | one row per place (GEOM+CREATED_DATE unique) |
| portal_cka_open_data_sa_5b3ce659e5 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_open_data_sa_9dca88d285 | place | SHAPE__LENGTH,FISCAL_YEAR | one row per place (GEOM+FISCAL_YEAR unique) |
| portal_cka_open_data_sa_a8ef161189 | place | SHAPE__LENGTH,CREATED_DATE | one row per place (GEOM+CREATED_DATE unique) |
| portal_cka_open_data_sa_e846782f2c | (unresolved -- grain proven, entity unknown) | RECORD_ID | one row per record (spine_entity not determined -- no registry hint available) (RECORD_ID unique) |
| portal_cka_san_jose_open_da_00b8041d47 | (unresolved -- grain proven, entity unknown) | INCIDENT_ID | one row per record (spine_entity not determined -- no registry hint available) (INCIDENT_ID unique) |
| portal_cka_san_jose_open_da_98849b65ee | place | LATITUDE,REPORTDATE | one row per place (LATLON+REPORTDATE unique) |
| portal_cka_tampa_open_data_06c9cc7276 | (unresolved -- grain proven, entity unknown) | ID,DATE,PERIOD | one row per record (spine_entity not determined -- no registry hint available) (ID+DATE+PERIOD unique) |
| portal_cka_tampa_open_data_18b980d54d | (unresolved -- grain proven, entity unknown) | ID,DATE | one row per record (spine_entity not determined -- no registry hint available) (ID+DATE unique) |
| portal_cka_tampa_open_data_c8043a5df9 | (unresolved -- grain proven, entity unknown) | ID,DATE,PERIOD | one row per record (spine_entity not determined -- no registry hint available) (ID+DATE+PERIOD unique) |
| portal_cka_virginia_open_da_039aacd655 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_virginia_open_da_1d39bdec50 | (unresolved -- grain proven, entity unknown) | FAC_ID | one row per record (spine_entity not determined -- no registry hint available) (FAC_ID unique) |
| portal_cka_virginia_open_da_3e67a117fb | place | FIPS,REPORT_DATE | one row per place (FIPS+REPORT_DATE unique) |
| portal_cka_virginia_open_da_651c0c423a | place | ZIP_CODE,STARTING_DATE,EXPIRATION_DATE,INSERTED_DATE,BUFFER_ID | one row per place (ZIP+STARTING_DATE+EXPIRATION_DATE+INSERTED_DATE+BUFFER_ID unique) |
| portal_cka_virginia_open_da_77706d86da | (unresolved -- grain proven, entity unknown) | SWC_ID | one row per record (spine_entity not determined -- no registry hint available) (SWC_ID unique) |
| portal_cka_virginia_open_da_ac3869ee0e | (unresolved -- grain proven, entity unknown) | PARCEL_ID | one row per record (spine_entity not determined -- no registry hint available) (PARCEL_ID unique) |
| portal_cka_virginia_open_da_ace8ac0352 | (unresolved -- grain proven, entity unknown) | TMDL_EQ_ID | one row per record (spine_entity not determined -- no registry hint available) (TMDL_EQ_ID unique) |
| portal_cka_virginia_open_da_cbc7fe8b75 | place | INCIDENT_FIPS,INCIDENT_YEAR,INCIDENT_MONTH | one row per place (FIPS+INCIDENT_YEAR+INCIDENT_MONTH unique) |
| portal_cka_virginia_open_da_e4498c978c | (unresolved -- grain proven, entity unknown) | PRP_REPORT_ID | one row per record (spine_entity not determined -- no registry hint available) (PRP_REPORT_ID unique) |
| portal_cka_western_pennsylv_070a16004d | place | ZIPCODE,LAST_EDIT_DATE | one row per place (ZIP+LAST_EDIT_DATE unique) |
| portal_cka_western_pennsylv_09335a764b | (unresolved -- grain proven, entity unknown) | START_STATION_ID,END_STATION_ID,START_DATE | one row per record (spine_entity not determined -- no registry hint available) (START_STATION_ID+END_STATION_ID+START_DATE unique) |
| portal_cka_western_pennsylv_0af7431c6c | facility | EPA_REGISTRY_ID,REPORTING_YEAR,STATE_COUNTY_FIPS_CODE,ZIP_CODE,TRI_FACILITY_ID,TRI_CHEM_ID,SRS_ID | one row per facility (FRS_ID+REPORTING_YEAR+FIPS+ZIP+TRI_FACILITY_ID+TRI_CHEM_ID+SRS_ID unique) |
| portal_cka_western_pennsylv_20c6fc6029 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_western_pennsylv_20e1a330ce | (unresolved -- grain proven, entity unknown) | CLIENT_ID | one row per record (spine_entity not determined -- no registry hint available) (CLIENT_ID unique) |
| portal_cka_western_pennsylv_23b8b5b7d2 | place | ZIP_CODE,CREATE_DATE,PROPERTY_TYPE,INSPECTION_STATUS,PARCEL_ID | one row per place (ZIP+CREATE_DATE+PROPERTY_TYPE+INSPECTION_STATUS+PARCEL_ID unique) |
| portal_cka_western_pennsylv_2dfc1addea | place | DECEDENT_ZIP,DEATH_DATE_AND_TIME | one row per place (ZIP+DEATH_DATE_AND_TIME unique) |
| portal_cka_western_pennsylv_4fc22c2c30 | place | ZIP_CODE,PERMIT_ISSUE_DATE,PERMIT_EXPIRE_DATE,PROJECT_TYPE,PARCEL_ID | one row per place (ZIP+PERMIT_ISSUE_DATE+PERMIT_EXPIRE_DATE+PROJECT_TYPE+PARCEL_ID unique) |
| portal_cka_western_pennsylv_51b8dcf278 | place | LATITUDE,START_YEAR,APPROVED_DATE | one row per place (LATLON+START_YEAR+APPROVED_DATE unique) |
| portal_cka_western_pennsylv_6a4c3e0e78 | (unresolved -- grain proven, entity unknown) | INSPECTION_ID | one row per record (spine_entity not determined -- no registry hint available) (INSPECTION_ID unique) |
| portal_cka_western_pennsylv_7bfb1a4c7d | (unresolved -- grain proven, entity unknown) | MARKET_ID | one row per record (spine_entity not determined -- no registry hint available) (MARKET_ID unique) |
| portal_cka_western_pennsylv_7d8c19b074 | (unresolved -- grain proven, entity unknown) | ET_ID | one row per record (spine_entity not determined -- no registry hint available) (ET_ID unique) |
| portal_cka_western_pennsylv_9ef4c60f58 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_western_pennsylv_a3b7349811 | (unresolved -- grain proven, entity unknown) | CLOSURE_ID | one row per record (spine_entity not determined -- no registry hint available) (CLOSURE_ID unique) |
| portal_cka_western_pennsylv_aad84a1f6e | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_western_pennsylv_b25e480dfc | asset | ASSET_ID | one row per asset (ASSET_ID unique) |
| portal_cka_western_pennsylv_ddb61776d0 | (unresolved -- grain proven, entity unknown) | INSPECTION_ID | one row per record (spine_entity not determined -- no registry hint available) (INSPECTION_ID unique) |
| portal_cka_western_pennsylv_ed65b530a3 | place | GEOID,QUARTER | one row per place (FIPS+QUARTER unique) |
| portal_cka_western_pennsylv_ef682f7e59 | (unresolved -- grain proven, entity unknown) | PERMIT_ID | one row per record (spine_entity not determined -- no registry hint available) (PERMIT_ID unique) |
| portal_cka_western_pennsylv_f6a018a1cb | (unresolved -- grain proven, entity unknown) | INSPECTION_ID | one row per record (spine_entity not determined -- no registry hint available) (INSPECTION_ID unique) |
| portal_cka_western_pennsylv_f810addeec | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_western_pennsylv_f82e02e6b2 | (unresolved -- grain proven, entity unknown) | EV_ID | one row per record (spine_entity not determined -- no registry hint available) (EV_ID unique) |
| portal_cka_western_pennsylv_fbecf42e16 | (unresolved -- grain proven, entity unknown) | REF_ID | one row per record (spine_entity not determined -- no registry hint available) (REF_ID unique) |
| portal_cka_western_pennsylv_fd81b4fb82 | (unresolved -- grain proven, entity unknown) | CONTAINER_ID | one row per record (spine_entity not determined -- no registry hint available) (CONTAINER_ID unique) |
| portal_cka_wprdc_allegheny_0cd6a9957c | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_wprdc_allegheny_12c9244c06 | place | ZIPCODE,LAST_EDIT_DATE | one row per place (ZIP+LAST_EDIT_DATE unique) |
| portal_cka_wprdc_allegheny_16a0bb67b4 | (unresolved -- grain proven, entity unknown) | CLIENT_ID | one row per record (spine_entity not determined -- no registry hint available) (CLIENT_ID unique) |
| portal_cka_wprdc_allegheny_1b2d51749e | (unresolved -- grain proven, entity unknown) | CLOSURE_ID | one row per record (spine_entity not determined -- no registry hint available) (CLOSURE_ID unique) |
| portal_cka_wprdc_allegheny_1c103ee2cd | place | ZIP_CODE,CREATE_DATE,PROPERTY_TYPE,INSPECTION_STATUS,PARCEL_ID | one row per place (ZIP+CREATE_DATE+PROPERTY_TYPE+INSPECTION_STATUS+PARCEL_ID unique) |
| portal_cka_wprdc_allegheny_415f1fe712 | (unresolved -- grain proven, entity unknown) | ET_ID | one row per record (spine_entity not determined -- no registry hint available) (ET_ID unique) |
| portal_cka_wprdc_allegheny_49ed6437bf | (unresolved -- grain proven, entity unknown) | INSPECTION_ID | one row per record (spine_entity not determined -- no registry hint available) (INSPECTION_ID unique) |
| portal_cka_wprdc_allegheny_508c030bd9 | (unresolved -- grain proven, entity unknown) | CONTAINER_ID | one row per record (spine_entity not determined -- no registry hint available) (CONTAINER_ID unique) |
| portal_cka_wprdc_allegheny_5b37a5568e | (unresolved -- grain proven, entity unknown) | PERMIT_ID | one row per record (spine_entity not determined -- no registry hint available) (PERMIT_ID unique) |
| portal_cka_wprdc_allegheny_692c217fc7 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_wprdc_allegheny_7af23acd2f | (unresolved -- grain proven, entity unknown) | START_STATION_ID,END_STATION_ID,START_DATE | one row per record (spine_entity not determined -- no registry hint available) (START_STATION_ID+END_STATION_ID+START_DATE unique) |
| portal_cka_wprdc_allegheny_7b65ae0cff | (unresolved -- grain proven, entity unknown) | INSPECTION_ID | one row per record (spine_entity not determined -- no registry hint available) (INSPECTION_ID unique) |
| portal_cka_wprdc_allegheny_822e5dba4c | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_wprdc_allegheny_9ccbefbacc | place | GEOID,QUARTER | one row per place (FIPS+QUARTER unique) |
| portal_cka_wprdc_allegheny_a4e9ce945b | place | DECEDENT_ZIP,DEATH_DATE_AND_TIME | one row per place (ZIP+DEATH_DATE_AND_TIME unique) |
| portal_cka_wprdc_allegheny_b20a13551f | (unresolved -- grain proven, entity unknown) | REF_ID | one row per record (spine_entity not determined -- no registry hint available) (REF_ID unique) |
| portal_cka_wprdc_allegheny_b78655de4f | (unresolved -- grain proven, entity unknown) | MARKET_ID | one row per record (spine_entity not determined -- no registry hint available) (MARKET_ID unique) |
| portal_cka_wprdc_allegheny_b9904b63c2 | asset | ASSET_ID | one row per asset (ASSET_ID unique) |
| portal_cka_wprdc_allegheny_bb0184f847 | place | ZIP_CODE,PERMIT_ISSUE_DATE,PERMIT_EXPIRE_DATE,PROJECT_TYPE,PARCEL_ID | one row per place (ZIP+PERMIT_ISSUE_DATE+PERMIT_EXPIRE_DATE+PROJECT_TYPE+PARCEL_ID unique) |
| portal_cka_wprdc_allegheny_c96164a13d | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_cka_wprdc_allegheny_ce7a2694fc | place | LATITUDE,START_YEAR,APPROVED_DATE | one row per place (LATLON+START_YEAR+APPROVED_DATE unique) |
| portal_cka_wprdc_allegheny_da448e7083 | (unresolved -- grain proven, entity unknown) | INSPECTION_ID | one row per record (spine_entity not determined -- no registry hint available) (INSPECTION_ID unique) |
| portal_cka_wprdc_allegheny_de448d04d4 | facility | EPA_REGISTRY_ID,REPORTING_YEAR,STATE_COUNTY_FIPS_CODE,ZIP_CODE,TRI_FACILITY_ID,TRI_CHEM_ID,SRS_ID | one row per facility (FRS_ID+REPORTING_YEAR+FIPS+ZIP+TRI_FACILITY_ID+TRI_CHEM_ID+SRS_ID unique) |
| portal_cka_wprdc_allegheny_fa3191e7a1 | (unresolved -- grain proven, entity unknown) | EV_ID | one row per record (spine_entity not determined -- no registry hint available) (EV_ID unique) |
| portal_soc_austin_open_data_0b4c639a1c | (unresolved -- grain proven, entity unknown) | EMPLOYEE_ID | one row per record (spine_entity not determined -- no registry hint available) (EMPLOYEE_ID unique) |
| portal_soc_cambridge_open_d_8a1152140c | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_chicago_data_por_26de83baf4 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_1d5cfad830 | place | COUNTY_FIPS,FISCAL_YEAR,START_DATE,EXIT_DATE,STATE_ID,STATE_ID_COPY,APPRENTICE_ID,PROGRAM_ID | one row per place (FIPS+FISCAL_YEAR+START_DATE+EXIT_DATE+STATE_ID+STATE_ID_COPY+APPRENTICE_ID+PROGRAM_ID unique) |
| portal_soc_colorado_informa_239fba8b76 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_46101be391 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_6367a44c92 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_a50da9b699 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_b4dd509314 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_d017cfcf7f | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_de6c8a6901 | place | COUNTY_FIPS,FISCAL_YEAR,START_DATE,EXIT_DATE,STATE_ID,STATE_ID_COPY,APPRENTICE_ID,PROGRAM_ID | one row per place (FIPS+FISCAL_YEAR+START_DATE+EXIT_DATE+STATE_ID+STATE_ID_COPY+APPRENTICE_ID+PROGRAM_ID unique) |
| portal_soc_colorado_informa_e80ca7800e | place | COUNTY_FIPS,EXIT_DATE,FISCAL_YEAR,START_DATE,STATE_ID,STATE_ID_COPY,APPRENTICE_ID,PROGRAM_ID | one row per place (FIPS+EXIT_DATE+FISCAL_YEAR+START_DATE+STATE_ID+STATE_ID_COPY+APPRENTICE_ID+PROGRAM_ID unique) |
| portal_soc_colorado_informa_f0e162d7a8 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_f78543c045 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_colorado_informa_f9498d9b7f | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_connecticut_open_88b075d7af | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_connecticut_open_aeb46f6c94 | facility | C_3_FRS_ID,C_1_YEAR,C_18_INDUSTRY_SECTOR_CODE,C_19_INDUSTRY_SECTOR,C_35_CAS_COMPOUND_ID,C_36_SRS_ID | one row per facility (FRS_ID+C_1_YEAR+C_18_INDUSTRY_SECTOR_CODE+C_19_INDUSTRY_SECTOR+C_35_CAS_COMPOUND_ID+C_36_SRS_ID unique) |
| portal_soc_connecticut_open_ff2b86a533 | place | ZIP_CODE,FISCAL_YEAR,CONTRACT_EXECUTION_DATE | one row per place (ZIP+FISCAL_YEAR+CONTRACT_EXECUTION_DATE unique) |
| portal_soc_datala_los_angel_361b8161b7 | place | MAILING_ZIP_CODE,LOCATION_START_DATE,LOCATION_END_DATE,ZIP_CODE | one row per place (ZIP+LOCATION_START_DATE+LOCATION_END_DATE+ZIP unique) |
| portal_soc_datala_los_angel_dc3670afe1 | place | MAILING_ZIP_CODE,LOCATION_START_DATE,ZIP_CODE | one row per place (ZIP+LOCATION_START_DATE+ZIP unique) |
| portal_soc_new_york_state_o_c08efa40c8 | (unresolved -- grain proven, entity unknown) | DEC_ID,YEAR | one row per record (spine_entity not determined -- no registry hint available) (DEC_ID+YEAR unique) |
| portal_soc_new_york_state_o_eff72c4402 | (unresolved -- grain proven, entity unknown) | PROJECT_ID_NUMBER | one row per record (spine_entity not determined -- no registry hint available) (PROJECT_ID_NUMBER unique) |
| portal_soc_open_data_br_6083bc2934 | (unresolved -- grain proven, entity unknown) | LOT_ID | one row per record (spine_entity not determined -- no registry hint available) (LOT_ID unique) |
| portal_soc_open_data_br_c110d5cf59 | place | ZIP,BUSINESS_NAICS_CODE,RESOURCE_TYPE,SUB_RESOURCE_TYPE,BUSINESS_ID,METADATA_ID | one row per place (ZIP+NAICS+RESOURCE_TYPE+SUB_RESOURCE_TYPE+BUSINESS_ID+METADATA_ID unique) |
| portal_soc_seattle_open_dat_c8f2072189 | place | ZIP,LICENSE_START_DATE | one row per place (ZIP+LICENSE_START_DATE unique) |
| portal_soc_sf_opendata_data_79618299a6 | place | BUSINESS_ZIP,DBA_START_DATE,LOCATION_START_DATE | one row per place (ZIP+DBA_START_DATE+LOCATION_START_DATE unique) |
| portal_soc_sf_opendata_data_8dccc91916 | provider | NPI,PROVIDER_TYPE,SITE_ID | one row per provider (NPI+PROVIDER_TYPE+SITE_ID unique) |
| portal_soc_sf_opendata_data_c19ee9eb44 | provider | NPI,PROGRAM_NAME | one row per provider (NPI+NAME unique) |
| portal_soc_texas_open_data_0f8f4663c8 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_texas_open_data_28e2f49084 | organization | NPN_EIN,ACTIVE_DATE,APPOINTMENT_TYPE,NAIC_ID | one row per organization (EIN+ACTIVE_DATE+APPOINTMENT_TYPE+NAIC_ID unique) |
| portal_soc_texas_open_data_354e3abf4f | place | SITE_ZIP_CD,NOR_REGISTRATION_DATE | one row per place (ZIP+NOR_REGISTRATION_DATE unique) |
| portal_soc_texas_open_data_5410a1009f | place | OUTLET_ZIP_CODE,OUTLET_PERMIT_ISSUE_DATE | one row per place (ZIP+OUTLET_PERMIT_ISSUE_DATE unique) |
| portal_soc_texas_open_data_6f798a64fa | organization | EIN,ACTIVE_DATE,APPOINTMENT_TYPE,NAIC_ID | one row per organization (EIN+ACTIVE_DATE+APPOINTMENT_TYPE+NAIC_ID unique) |
| portal_soc_texas_open_data_a415622c5d | place | LOC_ZIP,PERMIT_DATE | one row per place (ZIP+PERMIT_DATE unique) |
| portal_soc_texas_open_data_d83872d208 | case | DISTRICT_COURT_DOCKET_NO,ORDER_DATE | one row per case (DOCKET+ORDER_DATE unique) |
| portal_soc_texas_open_data_da657010b1 | place | LOC_ZIP,RESP_BEGIN_DATE | one row per place (ZIP+RESP_BEGIN_DATE unique) |
| portal_soc_utah_open_data_p_103f7d641f | organization | RECIPIENT_DUNS,PERIOD_OF_PERFORMANCE_START,PERIOD_OF_PERFORMANCE_CURRENT,LAST_MODIFIED_DATE,AWARD_ID_FAIN,AWARD_ID_URI | one row per organization (DUNS+PERIOD_OF_PERFORMANCE_START+PERIOD_OF_PERFORMANCE_CURRENT+LAST_MODIFIED_DATE+AWARD_ID_FAIN+AWARD_ID_URI unique) |
| portal_soc_utah_open_data_p_289c31329b | case | CASE_ID | one row per case (CASE_ID unique) |
| portal_soc_utah_open_data_p_33421b5a2a | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID,YEAR | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID+YEAR unique) |
| portal_soc_utah_open_data_p_38579bbdbc | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_3c77c8480b | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID,YEAR | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID+YEAR unique) |
| portal_soc_utah_open_data_p_4309355f14 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID,YEAR | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID+YEAR unique) |
| portal_soc_utah_open_data_p_4388c129f2 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_4eba247771 | provider | PROVIDER_NPI,REPORTING_PERIOD,PROVIDER_POSTAL_CODE,MEASURE_ID | one row per provider (NPI+REPORTING_PERIOD+ZIP+MEASURE_ID unique) |
| portal_soc_utah_open_data_p_55ef6ef0c6 | provider | NPI,HCPCS_CODE | one row per provider (NPI+HCPCS_CODE unique) |
| portal_soc_utah_open_data_p_5c3521189e | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_5e73751281 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_5ef68422ff | organization | RECIPIENT_DUNS,PERIOD_OF_PERFORMANCE_START,PERIOD_OF_PERFORMANCE_CURRENT,PERIOD_OF_PERFORMANCE,AWARD_ID_PIID,PARENT_AWARD_AGENCY_ID,PARENT_AWARD_ID | one row per organization (DUNS+PERIOD_OF_PERFORMANCE_START+PERIOD_OF_PERFORMANCE_CURRENT+PERIOD_OF_PERFORMANCE+AWARD_ID_PIID+PARENT_AWARD_AGENCY_ID+PARENT_AWARD_ID unique) |
| portal_soc_utah_open_data_p_636fffdfa2 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_66c519bccf | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_6f5fcc229f | facility | FRS_ID,YEAR,INDUSTRY_SECTOR_CODE,INDUSTRY_SECTOR,TRI_FACILITY_ID,CAS_COMPOUND_ID,SRS_ID | one row per facility (FRS_ID+YEAR+INDUSTRY_SECTOR_CODE+INDUSTRY_SECTOR+TRI_FACILITY_ID+CAS_COMPOUND_ID+SRS_ID unique) |
| portal_soc_utah_open_data_p_7186edb84b | facility | PROVIDER_CCN,YEAR,FISCAL_YEAR_BEGIN_DATE | one row per facility (CCN+YEAR+FISCAL_YEAR_BEGIN_DATE unique) |
| portal_soc_utah_open_data_p_7a3c73b2fd | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID,YEAR | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID+YEAR unique) |
| portal_soc_utah_open_data_p_7f45e582f7 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_81a81b1650 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_utah_open_data_p_8d9fb9a1a3 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_8de28da9d9 | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |
| portal_soc_utah_open_data_p_a3b79359d3 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_a4022a1a2d | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID,YEAR | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID+YEAR unique) |
| portal_soc_utah_open_data_p_a45115b872 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_a54aa90538 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_a5715666da | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_a5ae4fd7a4 | facility | PROVIDER_CCN,FISCAL_YEAR_BEGIN_DATE | one row per facility (CCN+FISCAL_YEAR_BEGIN_DATE unique) |
| portal_soc_utah_open_data_p_a9b7e273c8 | facility | PROVIDER_CCN,FISCAL_YEAR_BEGIN_DATE | one row per facility (CCN+FISCAL_YEAR_BEGIN_DATE unique) |
| portal_soc_utah_open_data_p_b0f7881369 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID,YEAR | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID+YEAR unique) |
| portal_soc_utah_open_data_p_b5e39c25f8 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_cdbdd459c0 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_d4aca49a9b | provider | PROVIDER_NPI,REPORTING_PERIOD,PROVIDER_POSTAL_CODE,MEASURE_ID | one row per provider (NPI+REPORTING_PERIOD+ZIP+MEASURE_ID unique) |
| portal_soc_utah_open_data_p_d5f7ca2621 | facility | C_3_FRS_ID,C_1_YEAR,C_18_INDUSTRY_SECTOR_CODE,C_19_INDUSTRY_SECTOR,C_35_CAS_COMPOUND_ID,C_36_SRS_ID | one row per facility (FRS_ID+C_1_YEAR+C_18_INDUSTRY_SECTOR_CODE+C_19_INDUSTRY_SECTOR+C_35_CAS_COMPOUND_ID+C_36_SRS_ID unique) |
| portal_soc_utah_open_data_p_f1292b8d2f | organization | DUNS_NO,FISCAL_YEAR,EVALUATION_CLOSED_DATE | one row per organization (DUNS+FISCAL_YEAR+EVALUATION_CLOSED_DATE unique) |
| portal_soc_utah_open_data_p_f326bad0fc | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID unique) |
| portal_soc_utah_open_data_p_f8cdd62630 | provider | PROVIDER_NPI,REPORTING_PERIOD,PROVIDER_POSTAL_CODE,MEASURE_ID | one row per provider (NPI+REPORTING_PERIOD+ZIP+MEASURE_ID unique) |
| portal_soc_utah_open_data_p_fe79f02e34 | facility | TRI_FACILITY_ID,CAS_COMPOUND_ID,YEAR | one row per facility (TRI_FACILITY_ID+CAS_COMPOUND_ID+YEAR unique) |
| portal_soc_washington_state_1a95fb1665 | organization | UBI_EIN,AUDIT_CLOSED_DATE,RECIPIENT_TYPE,AUDIT_TYPE | one row per organization (EIN+AUDIT_CLOSED_DATE+NAME+AUDIT_TYPE unique) |
| portal_soc_washington_state_48eeef5dfc | (unresolved -- grain proven, entity unknown) | BUSINESS_ID,ID | one row per record (spine_entity not determined -- no registry hint available) (BUSINESS_ID+ID unique) |
| st_cannabis_policy_bundles | place | FIPS,YEAR | one row per place (FIPS+YEAR unique) |
| xc_mapping_police_violence | (unresolved -- grain proven, entity unknown) | MPV_ID | one row per record (spine_entity not determined -- no registry hint available) (MPV_ID unique) |
| xc_owid_refugees | place | REFUGEES_BY_COUNTRY_OF_ORIGIN,YEAR,CODE | one row per place (COUNTRY+YEAR+CODE unique) |
| xc_vera_incarceration_trends | place | STATE_FIPS,YEAR,STATE_CODE,COUNTY_CODE | one row per place (FIPS+YEAR+STATE_CODE+COUNTY_CODE unique) |
| xc_wapo_fatal_force | (unresolved -- grain proven, entity unknown) | ID | one row per record (spine_entity not determined -- no registry hint available) (ID unique) |

## AMBIGUOUS (1075) -- needs a human call, never auto-written

| source_id | reason | detail |
|---|---|---|
| FED_CMS_PARTD_PRESCRIBER_DRUG | not-unique-after-dimension-search | base=Prscrbr_NPI key_ratio=0.0409 dims_tried=[Prscrbr_Type, Prscrbr_Type_Src] ratios_at_each_level=[0.0409, 0.0409, 0.0409] |
| FED_FDA_CAERS | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FDA_DEVICE_510K | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FDA_DEVICE_CLASSIFICATION | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FDA_DEVICE_ENFORCEMENT | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FDA_DEVICE_PMA | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FDA_DRUG_ENFORCEMENT | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FDA_ESTABLISHMENT_REG | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FDA_GUDID | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FDA_MAUDE | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FEC_CANDIDATES | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FEC_CAND_CMTE_LINKAGE | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FEC_COMMITTEES | no-key-column | ENTITY_TYPES hint: (none) |
| FED_FEC_INDEPENDENT_EXPENDITURES | not-unique-after-dimension-search | base=CAND_ID key_ratio=0.0135 dims_tried=[EXP_DATE, FEC_ELECTION_YR, CYCLE_FILE, SPE_ID, TRAN_ID] ratios_at_each_level=[0.0135, 0.0155, 0.6483, 0.1927, 0.1936, 0.1936, 0.8649] |
| FED_FEC_PAC_SUMMARY | no-key-column | ENTITY_TYPES hint: (none) |
| FED_MSHA_ACCIDENTS | not-unique-after-dimension-search | base=MINE_ID key_ratio=0.0493 dims_tried=[CAL_YR, CAL_QTR, FISCAL_YR, CONTROLLER_ID, OPERATOR_ID, CONTRACTOR_ID] ratios_at_each_level=[0.0493, 0.0242, 0.0292, 0.0188, 0.2566, 0.4572, 0.4572, 0.512] |
| FED_MSHA_VIOLATIONS | not-unique-after-dimension-search | base=DOCKET_NO+DOCKET_STATUS_CD+MINE_ID key_ratio=0.0063 dims_tried=[CAL_YR, CAL_QTR, FISCAL_YR, CONTROLLER_ID, VIOLATOR_ID, CONTRACTOR_ID] ratios_at_each_level=[0.0063, 0.014, 0.0071, 0.0223, 0.0956, 0.1518, 0.1518, 0.181] |
| FED_NHTSA_COMPLAINTS | no-key-column | ENTITY_TYPES hint: (none) |
| FED_NHTSA_INVESTIGATIONS | no-key-column | ENTITY_TYPES hint: (none) |
| FED_NHTSA_RECALLS | no-key-column | ENTITY_TYPES hint: (none) |
| FED_SEC_13F_POSITIONS | no-key-column | ENTITY_TYPES hint: (none) |
| FED_SEC_13F_SUBMISSION | no-key-column | ENTITY_TYPES hint: (none) |
| FED_SEC_INSIDER_DERIV_TRANS | no-key-column | ENTITY_TYPES hint: (none) |
| FED_SEC_INSIDER_NONDERIV_TRANS | no-key-column | ENTITY_TYPES hint: (none) |
| FED_SEC_INSIDER_REPORTINGOWNER | not-unique-after-dimension-search | base=RPTOWNER_ZIPCODE key_ratio=0.0056 dims_tried=[(none found)] ratios_at_each_level=[0.0056] |
| FED_SEC_INSIDER_SUBMISSION | no-key-column | ENTITY_TYPES hint: (none) |
| FED_USASPENDING_ASSISTANCE_FULL | not-unique-after-dimension-search | base=recipient_uei key_ratio=0.0112 dims_tried=[action_date, action_date_fiscal_year, period_of_performance_start_date, award_id_fain, award_id_uri] ratios_at_each_level=[0.0112, 0.5185, 0.4008, 0.1763, 0.1763, 0.2368, 0.8984] |
| ca_lobby_chg_log | not-unique-after-dimension-search | base=ENTITY_ZIP key_ratio=0.0064 dims_tried=[FILER_TYPE, ENTITY_TYPE, FILER_ID, SESSION_ID, ENTITY_ID] ratios_at_each_level=[0.0064, 0.2535, 0.0002, 0.2307, 0.0116, 0.0134, 0.8216] |
| ca_lobby_contributions | not-unique-after-dimension-search | base=FILER_ID key_ratio=0.0912 dims_tried=[FILING_PERIOD_START_DT, FILING_PERIOD_END_DT] ratios_at_each_level=[0.0912, 0.1465, 0.1467] |
| ca_lobby_employer | not-unique-after-dimension-search | base=SESSION_ID key_ratio=0.0006 dims_tried=[CONTRIBUTOR_ID, CURRENT_QTR_AMT, SESSION_YR_1] ratios_at_each_level=[0.0006, 0.0092, 0.0786, 0.0786] |
| ca_lobby_employer_firms | not-unique-after-dimension-search | base=FIRM_ID key_ratio=0.25 dims_tried=[SESSION_ID] ratios_at_each_level=[0.25, 0.5477] |
| ca_lobby_firm_employer | not-unique-after-dimension-search | base=FIRM_ID key_ratio=0.1412 dims_tried=[FILING_ID] ratios_at_each_level=[0.1412, 0.1412] |
| fed_bia_tribal_geo | not-unique-after-dimension-search | base=FIPS key_ratio=0.01 dims_tried=[(none found)] ratios_at_each_level=[0.01] |
| fed_bjs_data | no-key-column | ENTITY_TYPES hint: (none) |
| fed_bls_qcew | not-unique-after-dimension-search | base=AREA_FIPS key_ratio=0.0012 dims_tried=[YEAR, QTR, OWN_CODE] ratios_at_each_level=[0.0012, 0.0012, 0.0012, 0.0053] |
| fed_bop_statistics | not-unique-after-dimension-search | base=STATE_FIPS key_ratio=0.02 dims_tried=[REPORT_DATE, CATEGORY, FACILITY_TYPE] ratios_at_each_level=[0.02, 0.02, 0.02, 0.02] |
| fed_cbp_encounters | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cdc_anxiety_depression | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cdc_data_portal | not-unique-after-dimension-search | base=FIPS key_ratio=0.0001 dims_tried=[YEAR, ZIP_CODE, DATA_VALUE_TYPE, DATASET_ID] ratios_at_each_level=[0.0001, 0.0002, 0.0013, 0.0013, 0.0013, 0.0013] |
| fed_cdc_drug_poisoning_county | not-unique-after-dimension-search | base=FIPS_STATE key_ratio=0.001 dims_tried=[YEAR] ratios_at_each_level=[0.001, 0.0162] |
| fed_cdc_health_insurance | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cdc_injury_violence_county | not-unique-after-dimension-search | base=ST_GEOID key_ratio=0.0004 dims_tried=[PERIOD, TTM_DATE_RANGE] ratios_at_each_level=[0.0004, 0.0027, 0.0031] |
| fed_cdc_leading_causes_state | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cdc_nndss_weekly_2024 | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cdc_overdose | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cdc_suicide_rates | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cdc_wonder | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cfpb_hmda | not-unique-after-dimension-search | base=LEI key_ratio=0.019 dims_tried=[ACTIVITY_YEAR, INTRO_RATE_PERIOD, STATE_CODE] ratios_at_each_level=[0.019, 0.019, 0.0348, 0.0348] |
| fed_cftc_cot_financial | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cftc_cot_futures | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cms_facility_level_minimum_data_set_frequency | not-unique-after-dimension-search | base=CCN key_ratio=0.0005 dims_tried=[REPORT_DATE, ZIP_CODE, FIPS_COUNTY_CODE] ratios_at_each_level=[0.0005, 0.0005, 0.0005, 0.0005] |
| fed_cms_medicare_durable_medical_equipment_devices_supplies_by_suppl | not-unique-after-dimension-search | base=SUPLR_NPI key_ratio=0.1262 dims_tried=[RBCS_ID] ratios_at_each_level=[0.1262, 0.0001] |
| fed_cms_medicare_inpatient_hospitals_by_provider_and_service | not-unique-after-dimension-search | base=RNDRNG_PRVDR_CCN key_ratio=0.0199 dims_tried=[(none found)] ratios_at_each_level=[0.0199] |
| fed_cms_medicare_outpatient_hospitals_by_provider_and_service | not-unique-after-dimension-search | base=RNDRNG_PRVDR_CCN key_ratio=0.0269 dims_tried=[(none found)] ratios_at_each_level=[0.0269] |
| fed_cms_medicare_physician_other_practitioners_by_provider_and_servi | not-unique-after-dimension-search | base=RNDRNG_NPI key_ratio=0.1234 dims_tried=[RNDRNG_PRVDR_TYPE] ratios_at_each_level=[0.1234, 0.1234] |
| fed_cms_nadac | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cms_nursing_home_deficiencies | not-unique-after-dimension-search | base=CMS_CERTIFICATION_NUMBER_CCN key_ratio=0.035 dims_tried=[SURVEY_DATE, CORRECTION_DATE, INSPECTION_CYCLE] ratios_at_each_level=[0.035, 0.2169, 0.2519, 0.2536] |
| fed_cms_nursing_home_fire_deficiencies | not-unique-after-dimension-search | base=CMS_CERTIFICATION_NUMBER_CCN key_ratio=0.0696 dims_tried=[SURVEY_DATE, CORRECTION_DATE, INSPECTION_CYCLE] ratios_at_each_level=[0.0696, 0.1846, 0.2804, 0.2808] |
| fed_cms_opioid_treatment_program_providers | not-unique-after-dimension-search | base=NPI key_ratio=0.8601 dims_tried=[MEDICARE_ID_EFFECTIVE_DATE] ratios_at_each_level=[0.8601, 0.8659] |
| fed_cpsc_neiss | no-key-column | ENTITY_TYPES hint: (none) |
| fed_cpsc_neiss_codes | no-key-column | ENTITY_TYPES hint: (none) |
| fed_dhs_hifld | not-unique-after-dimension-search | base=FIPS key_ratio=0.002 dims_tried=[SOURCE_DATE, NAICS_CODE, STATUS] ratios_at_each_level=[0.002, 0.08, 0.08, 0.082] |
| fed_dhs_ohss | no-key-column | ENTITY_TYPES hint: (none) |
| fed_docsouth | no-key-column | ENTITY_TYPES hint: (none) |
| fed_doj_epstein_library | no-key-column | ENTITY_TYPES hint: (none) |
| fed_doj_fca_settlements | no-key-column | ENTITY_TYPES hint: (none) |
| fed_dol_oflc | not-unique-after-dimension-search | base=WORKSITE_POSTAL_CODE_10 key_ratio=0.0003 dims_tried=[DECISION_DATE, ORIGINAL_CERT_DATE, PERIOD_OF_EMPLOYMENT_START_DATE] ratios_at_each_level=[0.0003, 0.0719, 0.1186, 0.5928] |
| fed_dol_osha_inspections | not-unique-after-dimension-search | base=MAIL_ZIP key_ratio=0.008 dims_tried=[OPEN_DATE, CASE_MOD_DATE, CLOSE_CONF_DATE, REPORTING_ID] ratios_at_each_level=[0.008, 0.0001, 0.5336, 0.6171, 0.6605, 0.7582] |
| fed_dot_bts | not-unique-after-dimension-search | base=COUNTY_FIPS key_ratio=0.0476 dims_tried=[YEAR, MONTH, CARRIER_CODE] ratios_at_each_level=[0.0476, 0.0476, 0.0476, 0.0476] |
| fed_eac_eavs | no-key-column | ENTITY_TYPES hint: (none) |
| fed_ed_edfacts | not-unique-after-dimension-search | base=STATE_FIPS key_ratio=0.0303 dims_tried=[SCHOOL_YEAR, PROGRAM_PARTICIPATION, PROFICIENCY_LEVEL, LEA_ID, SCHOOL_ID, SEA_ID] ratios_at_each_level=[0.0303, 0.0303, 0.0303, 0.0303, 0.0303, 0.6667, 0.6667, 0.6667] |
| fed_eoir_case_data | no-key-column | ENTITY_TYPES hint: (none) |
| fed_epa_air_emissions_poll_rpt_combined_emissions | not-unique-after-dimension-search | base=REGISTRY_ID key_ratio=0.0156 dims_tried=[REPORTING_YEAR, NEI_TYPE, PGM_SYS_ID] ratios_at_each_level=[0.0156, 0.018, 0.0654, 0.105, 0.1111] |
| fed_epa_envirofacts | not-unique-after-dimension-search | base=FRS_ID key_ratio=0.0002 dims_tried=[CREATED_DATE, PROGRAM_SCHEMA, STATE_CODE, HANDLER_ID, SITE_ID] ratios_at_each_level=[0.0002, 0.0002, 0.0002, 0.0002, 0.0002, 0.0002, 0.0002] |
| fed_epa_icis_air_icis_air_informal_actions | not-unique-after-dimension-search | base=PGM_SYS_ID key_ratio=0.1791 dims_tried=[ACTIVITY_ID, ACHIEVED_DATE, ACTIVITY_TYPE_CODE] ratios_at_each_level=[0.1791, 0.5194, 0.5194, 0.5194] |
| fed_epa_icis_air_icis_air_pollutants | not-unique-after-dimension-search | base=PGM_SYS_ID key_ratio=0.2617 dims_tried=[SRS_ID, POLLUTANT_CODE, AIR_POLLUTANT_CLASS_CODE] ratios_at_each_level=[0.2617, 0.8695, 0.8847, 0.9693] |
| fed_epa_icis_fec_case_enforcement_conclusion_facilities | not-unique-after-dimension-search | base=FACILITY_ZIP key_ratio=0.2411 dims_tried=[ACTIVITY_ID, ENF_CONCLUSION_ID, ICIS_FACILITY_INTEREST_ID] ratios_at_each_level=[0.2411, 0.8064, 0.8242, 0.7764] |
| fed_epa_icis_fec_case_facilities | not-unique-after-dimension-search | base=REGISTRY_ID key_ratio=0.5581 dims_tried=[STATE_CODE, PRIMARY_SIC_CODE, PRIMARY_NAICS_CODE, ACTIVITY_ID] ratios_at_each_level=[0.5581, 0.6598, 0.5584, 0.5928, 0.6295, 0.9772] |
| fed_epa_icis_fec_epa_informal_enforcement_actions | not-unique-after-dimension-search | base=REGISTRY_ID key_ratio=0.666 dims_tried=[ACHIEVED_DATE, ACTIVITY_TYPE_CODE, ENF_TYPE_CODE, PGM_SYS_ID] ratios_at_each_level=[0.666, 0.6948, 0.9497, 0.9497, 0.9508, 0.9783] |
| fed_epa_npdes_npdes_inspections | not-unique-after-dimension-search | base=REGISTRY_ID key_ratio=0.1385 dims_tried=[ACTUAL_BEGIN_DATE, ACTUAL_END_DATE, ACTIVITY_TYPE_CODE, ACTIVITY_ID] ratios_at_each_level=[0.1385, 0.9405, 0.5125, 0.8967, 0.8967, 0.9405] |
| fed_epa_npdes_npdes_naics | not-unique-after-dimension-search | base=NPDES_ID key_ratio=0.9398 dims_tried=[NAICS_CODE] ratios_at_each_level=[0.9398, 0.9732] |
| fed_epa_npdes_npdes_qncr_history | not-unique-after-dimension-search | base=NPDES_ID key_ratio=0.0868 dims_tried=[(none found)] ratios_at_each_level=[0.0868] |
| fed_epa_npdes_npdes_sics | not-unique-after-dimension-search | base=NPDES_ID key_ratio=0.902 dims_tried=[SIC_CODE] ratios_at_each_level=[0.902, 0.9732] |
| fed_epa_superfund_site_boundaries | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.7488 dims_tried=[LAST_CHANGE_DATE, ORIGINAL_CREATION_DATE, REGION_CODE, EPA_ID] ratios_at_each_level=[0.7488, 0.9026, 0.8803, 0.886, 0.886, 0.9125] |
| fed_faa_data_portal | not-unique-after-dimension-search | base=FIPS key_ratio=0.25 dims_tried=[CATEGORY, DATASET_ID, AIRPORT_ID] ratios_at_each_level=[0.25, 0.25, 0.25, 0.25, 0.25] |
| fed_fara | not-unique-after-dimension-search | base=EIN key_ratio=0.0333 dims_tried=[REGISTRATION_DATE, TERMINATION_DATE, PERIOD_START] ratios_at_each_level=[0.0333, 0.0333, 0.0333, 0.0333] |
| fed_fara_bulk | not-unique-after-dimension-search | base=ZIP key_ratio=0.0075 dims_tried=[REGISTRATION_DATE, TERMINATION_DATE, DATE_STAMPED] ratios_at_each_level=[0.0075, 0.0314, 0.0535, 0.1164] |
| fed_fatca_ffi | not-unique-after-dimension-search | base=COUNTRY_NAME key_ratio=0.0005 dims_tried=[(none found)] ratios_at_each_level=[0.0005] |
| fed_fbi_cde | no-key-column | ENTITY_TYPES hint: (none) |
| fed_fbi_nics_checks | no-key-column | ENTITY_TYPES hint: (none) |
| fed_fcc_licensing | not-unique-after-dimension-search | base=EIN key_ratio=0.0 dims_tried=[GRANT_DATE, EXPIRED_DATE, CANCELLATION_DATE, EBF_TRANSACTION_ID] ratios_at_each_level=[0.0, 0.0, 0.0059, 0.176, 0.2863, 0.2863] |
| fed_fda_faers_demo | not-unique-after-dimension-search | base=OCCR_COUNTRY key_ratio=0.0 dims_tried=[I_F_CODE] ratios_at_each_level=[0.0, 0.0001] |
| fed_fda_faers_drug | no-key-column | ENTITY_TYPES hint: (none) |
| fed_fda_faers_indi | no-key-column | ENTITY_TYPES hint: (none) |
| fed_fda_faers_outc | no-key-column | ENTITY_TYPES hint: (none) |
| fed_fda_faers_reac | no-key-column | ENTITY_TYPES hint: (none) |
| fed_fdic_enforcement | no-key-column | ENTITY_TYPES hint: (none) |
| fed_federal_register_documents | not-unique-after-dimension-search | base=DOCKET_IDS key_ratio=0.5334 dims_tried=[PUBLICATION_DATE, TYPE, SUBTYPE, REGULATION_ID_NUMBERS] ratios_at_each_level=[0.5334, 0.042, 0.6677, 0.6828, 0.685, 0.6909] |
| fed_ffiec_call_reports | not-unique-after-dimension-search | base=RSSD_ID key_ratio=0.0033 dims_tried=[REPORTING_PERIOD_END_DATE, MDRM_CONCEPT_CODE] ratios_at_each_level=[0.0033, 0.0033, 0.0033] |
| fed_fhfa_hpi | not-unique-after-dimension-search | base=PLACE_ID key_ratio=0.0026 dims_tried=[YR, PERIOD, HPI_TYPE] ratios_at_each_level=[0.0026, 0.1159, 0.4677, 0.5107] |
| fed_fhfa_nmdb | no-key-column | ENTITY_TYPES hint: (none) |
| fed_fhfa_suspended_counterparty_program | no-key-column | ENTITY_TYPES hint: (none) |
| fed_foreignassistance | not-unique-after-dimension-search | base=EIN key_ratio=0.0 dims_tried=[FISCAL_YEAR, USG_SECTOR, DAC_CATEGORY] ratios_at_each_level=[0.0, 0.0009, 0.0009, 0.0009] |
| fed_fra_casualties | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.0438 dims_tried=[INCIDENT_YEAR, INCIDENT_MONTH, DATE] ratios_at_each_level=[0.0438, 0.0475, 0.0511, 0.0616] |
| fed_fra_crossing_incidents | not-unique-after-dimension-search | base=GRADE_CROSSING_ID key_ratio=0.4017 dims_tried=[REPORT_YEAR, INCIDENT_YEAR, INCIDENT_MONTH] ratios_at_each_level=[0.4017, 0.8771, 0.8771, 0.9501] |
| fed_fra_equipment_accidents | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.1197 dims_tried=[YEAR, ACCIDENT_YEAR, ACCIDENT_MONTH, GRADE_CROSSING_ID] ratios_at_each_level=[0.1197, 0.0376, 0.1273, 0.1273, 0.1371, 0.17] |
| fed_frb_h15_selected_rates | no-key-column | ENTITY_TYPES hint: (none) |
| fed_frb_z1_csv | no-key-column | ENTITY_TYPES hint: (none) |
| fed_ftc_datasets | not-unique-after-dimension-search | base=EIN key_ratio=0.0008 dims_tried=[DATE_FILED, CASE_TYPE, STATUS] ratios_at_each_level=[0.0008, 0.4583, 0.4583, 0.4583] |
| fed_google_polads_advertiser_geo_spend | not-unique-after-dimension-search | base=COUNTRY_SUBDIVISION_PRIMARY key_ratio=0.0001 dims_tried=[ADVERTISER_ID] ratios_at_each_level=[0.0001, 0.0262] |
| fed_google_polads_advertiser_id_mapping | no-key-column | ENTITY_TYPES hint: (none) |
| fed_google_polads_creative_id_mapping | no-key-column | ENTITY_TYPES hint: (none) |
| fed_govinfo_bill_cosponsors | not-unique-after-dimension-search | base=COSPONSOR_BIOGUIDE key_ratio=0.0017 dims_tried=[SPONSORSHIP_DATE, SPONSORSHIP_WITHDRAWN_DATE, BILL_TYPE] ratios_at_each_level=[0.0017, 0.464, 0.4642, 0.577] |
| fed_govinfo_billstatus | not-unique-after-dimension-search | base=SPONSOR_BIOGUIDE key_ratio=0.0173 dims_tried=[INTRODUCED_DATE, LATEST_ACTION_DATE, BILL_TYPE] ratios_at_each_level=[0.0173, 0.8089, 0.8543, 0.8732] |
| fed_hhs_oig_leie | not-unique-after-dimension-search | base=NPI key_ratio=0.1019 dims_tried=[(none found)] ratios_at_each_level=[0.1019] |
| fed_hrsa_shortage_areas | not-unique-after-dimension-search | base=STATE_FIPS_CODE key_ratio=0.0004 dims_tried=[HPSA_DESIGNATION_DATE, HPSA_DESIGNATION_LAST_UPDATE_DATE, WITHDRAWN_DATE, HPSA_ID] ratios_at_each_level=[0.0004, 0.2556, 0.0876, 0.1229, 0.123, 0.2559] |
| fed_hrsa_uds_health_center_info | no-key-column | ENTITY_TYPES hint: (none) |
| fed_hrsa_uds_table3a_patients | no-key-column | ENTITY_TYPES hint: (none) |
| fed_hud_assisted_housing_projects | not-unique-after-dimension-search | base=STD_ZIP5 key_ratio=0.2892 dims_tried=[QUARTER, RENT_PER_MONTH, SPENDING_PER_MONTH] ratios_at_each_level=[0.2892, 0.2892, 0.7848, 0.7909] |
| fed_hud_data | not-unique-after-dimension-search | base=EIN key_ratio=0.013 dims_tried=[YEAR] ratios_at_each_level=[0.013, 0.026] |
| fed_ice_detainers | not-unique-after-dimension-search | base=DETENTION_FACILITY_CODE key_ratio=0.0087 dims_tried=[DETAINER_PREPARE_DATE, DEPARTED_DATE, BIRTH_YEAR] ratios_at_each_level=[0.0087, 0.575, 0.7264, 0.9629] |
| fed_ice_detention_facility_list | no-key-column | ENTITY_TYPES hint: (none) |
| fed_ice_statistics | not-unique-after-dimension-search | base=COUNTRY_OF_CITIZENSHIP key_ratio=0.8959 dims_tried=[FISCAL_YEAR, FISCAL_QUARTER, SNAPSHOT_DATE] ratios_at_each_level=[0.8959, 0.8959, 0.8959, 0.8959] |
| fed_icij_offshoreleaks_relationships | not-unique-after-dimension-search | base=NODE_ID_START key_ratio=0.3388 dims_tried=[NODE_ID_END, START_DATE, END_DATE] ratios_at_each_level=[0.3388, 0.8676, 0.8855, 0.8878] |
| fed_irs_soi | not-unique-after-dimension-search | base=STATE_FIPS key_ratio=0.0003 dims_tried=[TAX_YEAR, ZIP_CODE] ratios_at_each_level=[0.0003, 0.0003, 0.1667] |
| fed_jpml_pending_mdls | no-key-column | ENTITY_TYPES hint: (none) |
| fed_mapping_inequality | not-unique-after-dimension-search | base=FIPS key_ratio=0.0001 dims_tried=[YEAR_MAPPED, HOLC_ID] ratios_at_each_level=[0.0001, 0.0001, 0.0001, 0.0001] |
| fed_medsl_house_returns | not-unique-after-dimension-search | base=STATE_FIPS key_ratio=0.0017 dims_tried=[YEAR] ratios_at_each_level=[0.0017, 0.0371] |
| fed_medsl_president_returns | not-unique-after-dimension-search | base=STATE_FIPS key_ratio=0.0136 dims_tried=[YEAR] ratios_at_each_level=[0.0136, 0.15] |
| fed_medsl_senate_returns | not-unique-after-dimension-search | base=STATE_FIPS key_ratio=0.0127 dims_tried=[YEAR] ratios_at_each_level=[0.0127, 0.2132] |
| fed_nara_aad | not-unique-after-dimension-search | base=DATASET_ID key_ratio=0.0162 dims_tried=[RECORD_ID, DATE, RECORD_GROUP] ratios_at_each_level=[0.0162, 0.0162, 0.0162, 0.0162] |
| fed_nara_wra_aad | not-unique-after-dimension-search | base=FIPS key_ratio=0.0278 dims_tried=[DATE, CITIZENSHIP_STATUS, SERIES_ID, RECORD_ID] ratios_at_each_level=[0.0278, 0.0278, 0.0278, 0.0278, 0.0278, 0.0278] |
| fed_nasa_open_data | no-key-column | ENTITY_TYPES hint: (none) |
| fed_noaa_ais | not-unique-after-dimension-search | base=MMSI key_ratio=0.0004 dims_tried=[DATE, STATUS, TRANSCEIVER_CLASS] ratios_at_each_level=[0.0004, 0.0021, 0.0023, 0.0023] |
| fed_nsf_awards | not-unique-after-dimension-search | base=EIN key_ratio=0.008 dims_tried=[AWARD_DATE, START_DATE, END_DATE, AWARD_ID] ratios_at_each_level=[0.008, 0.92, 0.304, 0.44, 0.568, 0.92] |
| fed_ofac_sdn | not-unique-after-dimension-search | base=IMO key_ratio=0.1063 dims_tried=[SDN_TYPE, PROGRAM, VESS_TYPE] ratios_at_each_level=[0.1063, 0.1065, 0.1247, 0.1247] |
| fed_pbgc_data | no-key-column | ENTITY_TYPES hint: (none) |
| fed_revolvingdoor_project | no-key-column | ENTITY_TYPES hint: (none) |
| fed_sam_exclusions | not-unique-after-dimension-search | base=NPI+UEI key_ratio=0.3242 dims_tried=[ACTIVATION_DATE, TERMINATION_DATE, CLASSIFICATION] ratios_at_each_level=[0.3242, 0.3242, 0.5122, 0.5138] |
| fed_sba_loans | not-unique-after-dimension-search | base=CDC_ZIP key_ratio=0.0001 dims_tried=[PROGRAM] ratios_at_each_level=[0.0001, 0.0001] |
| fed_sba_ppp | no-key-column | ENTITY_TYPES hint: (none) |
| fed_scdb | not-unique-after-dimension-search | base=DOCKET key_ratio=0.0826 dims_tried=[(none found)] ratios_at_each_level=[0.0826] |
| fed_sec_13f_filers | not-unique-after-dimension-search | base=FILINGMANAGER_ZIPCODE key_ratio=0.0166 dims_tried=[(none found)] ratios_at_each_level=[0.0166] |
| fed_sec_13f_holdings | no-key-column | ENTITY_TYPES hint: (none) |
| fed_sec_13f_submissions | not-unique-after-dimension-search | base=CIK key_ratio=0.0485 dims_tried=[FILING_DATE] ratios_at_each_level=[0.0485, 0.9605] |
| fed_sec_dera_sub_2024q1 | not-unique-after-dimension-search | base=CIK key_ratio=0.9134 dims_tried=[PERIOD, FY] ratios_at_each_level=[0.9134, 0.9637, 0.9726] |
| fed_sec_dera_sub_2024q2 | not-unique-after-dimension-search | base=CIK key_ratio=0.8143 dims_tried=[PERIOD, FY] ratios_at_each_level=[0.8143, 0.9483, 0.9707] |
| fed_sec_dera_sub_2024q3 | not-unique-after-dimension-search | base=CIK key_ratio=0.8969 dims_tried=[PERIOD, FY] ratios_at_each_level=[0.8969, 0.964, 0.977] |
| fed_sec_dera_sub_2024q4 | not-unique-after-dimension-search | base=CIK key_ratio=0.8986 dims_tried=[PERIOD, FY] ratios_at_each_level=[0.8986, 0.9623, 0.9767] |
| fed_sec_dera_sub_2025q1 | not-unique-after-dimension-search | base=CIK key_ratio=0.9103 dims_tried=[PERIOD, FY] ratios_at_each_level=[0.9103, 0.9597, 0.9677] |
| fed_sec_dera_sub_2025q2 | not-unique-after-dimension-search | base=CIK key_ratio=0.8676 dims_tried=[PERIOD, FY] ratios_at_each_level=[0.8676, 0.9541, 0.9729] |
| fed_sec_dera_sub_2025q3 | not-unique-after-dimension-search | base=CIK key_ratio=0.9034 dims_tried=[PERIOD, FY] ratios_at_each_level=[0.9034, 0.967, 0.9787] |
| fed_sec_edgar | not-unique-after-dimension-search | base=CIK key_ratio=0.1 dims_tried=[REPORTDATE] ratios_at_each_level=[0.1, 0.46] |
| fed_sec_edgar_company_tickers | not-unique-after-dimension-search | base=CIK_STR key_ratio=0.7699 dims_tried=[(none found)] ratios_at_each_level=[0.7699] |
| fed_sec_edgar_company_tickers_exchange | not-unique-after-dimension-search | base=CIK key_ratio=0.7692 dims_tried=[(none found)] ratios_at_each_level=[0.7692] |
| fed_sec_edgar_financials | not-unique-after-dimension-search | base=CIK key_ratio=0.1458 dims_tried=[PERIOD, FY] ratios_at_each_level=[0.1458, 0.9275, 0.9537] |
| fed_sec_edgar_insiders | not-unique-after-dimension-search | base=CIK key_ratio=0.0766 dims_tried=[FILING_DATE, PERIOD_OF_REPORT, DATE_OF_ORIG_SUB] ratios_at_each_level=[0.0766, 0.3117, 0.3444, 0.346] |
| fed_sec_money_market_fund_information | not-unique-after-dimension-search | base=REGISTRANT_CIK key_ratio=0.1459 dims_tried=[SERIES_CATEGORY, CLASS_NAME, CLASS_ID, SERIES_ID] ratios_at_each_level=[0.1459, 0.2653, 0.1857, 0.6459, 0.869, 0.869] |
| fed_senate_lda_filings | not-unique-after-dimension-search | base=CLIENT_COUNTRY key_ratio=0.0003 dims_tried=[FILING_YEAR, FILING_PERIOD, FILING_PERIOD_DISPLAY, REGISTRANT_ID, CLIENT_ID] ratios_at_each_level=[0.0003, 0.0226, 0.1525, 0.0014, 0.0032, 0.0032, 0.8333] |
| fed_senate_stock_watcher | no-key-column | ENTITY_TYPES hint: (none) |
| fed_slavevoyages_intraamerican | no-key-column | ENTITY_TYPES hint: (none) |
| fed_slavevoyages_transatlantic | no-key-column | ENTITY_TYPES hint: (none) |
| fed_treasury_avg_interest_rates | no-key-column | ENTITY_TYPES hint: (none) |
| fed_treasury_debt_outstanding | no-key-column | ENTITY_TYPES hint: (none) |
| fed_treasury_debt_to_penny | no-key-column | ENTITY_TYPES hint: (none) |
| fed_treasury_dts_deposits | no-key-column | ENTITY_TYPES hint: (none) |
| fed_us_sec_edgar | not-unique-after-dimension-search | base=CIK key_ratio=0.0005 dims_tried=[PERIOD_OF_REPORT, FORM_TYPE, SIC_CODE] ratios_at_each_level=[0.0005, 0.1848, 0.2215, 0.2215] |
| fed_usaspending_subawards | no-key-column | ENTITY_TYPES hint: (none) |
| fed_uscis_data | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.0003 dims_tried=[FISCAL_YEAR, QUARTER, PUBLICATION_DATE] ratios_at_each_level=[0.0003, 0.0006, 0.0006, 0.0006] |
| fed_uscourts_stats | not-unique-after-dimension-search | base=FIPS_CODE key_ratio=0.02 dims_tried=[REPORTING_PERIOD, CHAPTER_CODE, CASE_TYPE] ratios_at_each_level=[0.02, 0.02, 0.02, 0.02] |
| fed_usgs_topoview | not-unique-after-dimension-search | base=FIPS key_ratio=0.004 dims_tried=[(none found)] ratios_at_each_level=[0.004] |
| fed_usgs_water | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.0006 dims_tried=[DATA_TYPE] ratios_at_each_level=[0.0006, 0.0011] |
| fed_va_allcause_mortality | no-key-column | ENTITY_TYPES hint: (none) |
| fed_va_suicide_appendix | no-key-column | ENTITY_TYPES hint: (none) |
| fed_va_suicide_national | no-key-column | ENTITY_TYPES hint: (none) |
| fed_va_suicide_state | no-key-column | ENTITY_TYPES hint: (none) |
| fed_voteview_members | not-unique-after-dimension-search | base=ICPSR key_ratio=0.2483 dims_tried=[DISTRICT_CODE, PARTY_CODE] ratios_at_each_level=[0.2483, 0.3304, 0.3547] |
| fed_voteview_rollcall_meta | no-key-column | ENTITY_TYPES hint: event |
| fed_voteview_rollcalls | not-unique-after-dimension-search | base=ICPSR key_ratio=0.0007 dims_tried=[CAST_CODE] ratios_at_each_level=[0.0007, 0.0022] |
| intl_adb_data | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.0244 dims_tried=[APPROVAL_DATE, YEAR, SECTOR, PROJECT_ID] ratios_at_each_level=[0.0244, 0.0244, 0.0244, 0.0244, 0.0244, 0.0244] |
| intl_ar_datosgob | not-unique-after-dimension-search | base=DATASET_ID key_ratio=0.1409 dims_tried=[SERIE_ID, PROVINCIA_ID, MUNICIPIO_ID, DEPARTAMENTO_ID] ratios_at_each_level=[0.1409, 0.0284, 0.1409, 0.1474, 0.1755, 0.2036] |
| intl_bd_datagov | no-key-column | ENTITY_TYPES hint: (none) |
| intl_eg_capmas | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.0067 dims_tried=[YEAR, CATEGORY] ratios_at_each_level=[0.0067, 0.0067, 0.0067] |
| intl_ember_elec | not-unique-after-dimension-search | base=COUNTRY_OR_REGION key_ratio=0.0006 dims_tried=[DATE, ISO_3_CODE, AREA_TYPE] ratios_at_each_level=[0.0006, 0.0155, 0.0155, 0.0155] |
| intl_es_borme | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.04 dims_tried=[DATE, ACT_TYPE] ratios_at_each_level=[0.04, 0.04, 0.04] |
| intl_es_datosgob | no-key-column | ENTITY_TYPES hint: (none) |
| intl_eu_socta_europol | no-key-column | ENTITY_TYPES hint: (none) |
| intl_eurlex_cellar | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.0189 dims_tried=[DATE_PUBLISHED, DATE_OF_DOCUMENT, DOCUMENT_TYPE, CELEX_ID, ECLI_ID] ratios_at_each_level=[0.0189, 0.2453, 0.0189, 0.2264, 0.2264, 0.2264, 0.2453] |
| intl_eurostat | not-unique-after-dimension-search | base=DATAFLOW_ID key_ratio=0.0044 dims_tried=[OBS_STATUS] ratios_at_each_level=[0.0044, 0.0044] |
| intl_fao_faostat | no-key-column | ENTITY_TYPES hint: (none) |
| intl_fao_faostat_food_security | no-key-column | ENTITY_TYPES hint: (none) |
| intl_fatf_ratings | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.79 dims_tried=[EVALUATION_YEAR] ratios_at_each_level=[0.79, 0.79] |
| intl_freedomhouse | not-unique-after-dimension-search | base=COUNTRY_TERRITORY key_ratio=0.0779 dims_tried=[STATUS] ratios_at_each_level=[0.0779, 0.094] |
| intl_gdelt | not-unique-after-dimension-search | base=ACTIONGEO_LAT key_ratio=0.2246 dims_tried=[YEAR, ACTOR1CODE, ACTOR1TYPE1CODE] ratios_at_each_level=[0.2246, 0.2276, 0.4956, 0.4956] |
| intl_gfi_trade | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.04 dims_tried=[YEAR] ratios_at_each_level=[0.04, 0.04] |
| intl_gh_datagovgh | no-key-column | ENTITY_TYPES hint: (none) |
| intl_gleif_relationships | no-key-column | ENTITY_TYPES hint: (none) |
| intl_global_witness_defenders | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.0302 dims_tried=[YEAR, INCIDENT_TYPE, SECTOR] ratios_at_each_level=[0.0302, 0.1078, 0.2328, 0.2629] |
| intl_ie_cro | no-key-column | ENTITY_TYPES hint: (none) |
| intl_ipc_food_insecurity_global | not-unique-after-dimension-search | base=TOTAL_COUNTRY_POPULATION key_ratio=0.0667 dims_tried=[DATE_OF_ANALYSIS, VALIDITY_PERIOD] ratios_at_each_level=[0.0667, 0.068, 0.1429] |
| intl_it_istat | not-unique-after-dimension-search | base=DATAFLOW_ID key_ratio=0.0 dims_tried=[DATE, OBS_STATUS] ratios_at_each_level=[0.0, 0.0002, 0.0003] |
| intl_leiden_russian_ops_europe | no-key-column | ENTITY_TYPES hint: (none) |
| intl_nti_cns_dprk_missile_tests | not-unique-after-dimension-search | base=FACILITY_LONGITUDE key_ratio=0.1584 dims_tried=[DATE, DATE_ENTERED_UPDATED, MISSILE_TYPE] ratios_at_each_level=[0.1584, 0.5248, 0.5347, 0.5545] |
| intl_owid_milspend | no-key-column | ENTITY_TYPES hint: (none) |
| intl_uk_sanctions_list | not-unique-after-dimension-search | base=IMO_NUMBER key_ratio=0.0114 dims_tried=[DATE_DESIGNATED, YEAR_BUILT, OFSI_GROUP_ID, UNIQUE_ID] ratios_at_each_level=[0.0114, 0.1086, 0.0189, 0.0189, 0.0995, 0.1086] |
| intl_voeten_unga_votes | no-key-column | ENTITY_TYPES hint: (none) |
| portal_arc_atlanta_dataatla_03dc194f2a | not-unique-after-dimension-search | base=ZIP key_ratio=0.0846 dims_tried=[(none found)] ratios_at_each_level=[0.0846] |
| portal_arc_atlanta_dataatla_05328f7540 | not-unique-after-dimension-search | base=DOCKET_NO key_ratio=0.6885 dims_tried=[CREATED_DATE, LAST_EDITED_DATE, STATUS] ratios_at_each_level=[0.6885, 0.8065, 0.858, 0.864] |
| portal_arc_atlanta_dataatla_0f1c49c840 | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.9314 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.9314, 0.9331, 0.9365, 0.9365] |
| portal_arc_atlanta_dataatla_17c43e4ba3 | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.931 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.931, 0.9327, 0.9327, 0.9327] |
| portal_arc_atlanta_dataatla_32bd015354 | not-unique-after-dimension-search | base=DOCKET_NO key_ratio=0.6885 dims_tried=[CREATED_DATE, LAST_EDITED_DATE, STATUS] ratios_at_each_level=[0.6885, 0.6885, 0.6885, 0.7085] |
| portal_arc_atlanta_dataatla_3e1237b0e9 | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.7188 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.7188, 0.7266, 0.7266, 0.7266] |
| portal_arc_atlanta_dataatla_3e6e5804c7 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0026 dims_tried=[(none found)] ratios_at_each_level=[0.0026] |
| portal_arc_atlanta_dataatla_3f5da71919 | not-unique-after-dimension-search | base=ZIP key_ratio=0.5345 dims_tried=[(none found)] ratios_at_each_level=[0.5345] |
| portal_arc_atlanta_dataatla_4c51545609 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1887 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1887, 0.8302] |
| portal_arc_atlanta_dataatla_5a321b0c21 | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.6949 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.6949, 0.7034, 0.7034, 0.7034] |
| portal_arc_atlanta_dataatla_5add5eaf6a | not-unique-after-dimension-search | base=ZIP key_ratio=0.0617 dims_tried=[(none found)] ratios_at_each_level=[0.0617] |
| portal_arc_atlanta_dataatla_610443017c | not-unique-after-dimension-search | base=ZIP key_ratio=0.0397 dims_tried=[(none found)] ratios_at_each_level=[0.0397] |
| portal_arc_atlanta_dataatla_7b1d4c8e25 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1957 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1957, 0.837] |
| portal_arc_atlanta_dataatla_7d3c4a9739 | not-unique-after-dimension-search | base=ZIP key_ratio=0.4737 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.4737, 0.8246] |
| portal_arc_atlanta_dataatla_7e542e6bfa | not-unique-after-dimension-search | base=ZIP key_ratio=0.65 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.65, 0.95] |
| portal_arc_atlanta_dataatla_898cd032b3 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0459 dims_tried=[(none found)] ratios_at_each_level=[0.0459] |
| portal_arc_atlanta_dataatla_93aa493487 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0429 dims_tried=[(none found)] ratios_at_each_level=[0.0429] |
| portal_arc_atlanta_dataatla_a0f4032894 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0459 dims_tried=[(none found)] ratios_at_each_level=[0.0459] |
| portal_arc_atlanta_dataatla_a29d594b47 | not-unique-after-dimension-search | base=ZIP key_ratio=0.7143 dims_tried=[(none found)] ratios_at_each_level=[0.7143] |
| portal_arc_atlanta_dataatla_a6a6a74172 | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.6949 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.6949, 0.7034, 0.7034, 0.7034] |
| portal_arc_atlanta_dataatla_a6d51869af | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.7188 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.7188, 0.7266, 0.7266, 0.7266] |
| portal_arc_atlanta_dataatla_a9fa6b1c3c | not-unique-after-dimension-search | base=ZIP key_ratio=0.2286 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.2286, 0.8571] |
| portal_arc_atlanta_dataatla_aaf9599f45 | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.6949 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.6949, 0.7034, 0.7034, 0.7034] |
| portal_arc_atlanta_dataatla_b9dc3dfa97 | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.9314 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.9314, 0.9331, 0.9365, 0.9365] |
| portal_arc_atlanta_dataatla_baa69e0d06 | not-unique-after-dimension-search | base=ZIP key_ratio=0.451 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.451, 0.9216] |
| portal_arc_atlanta_dataatla_baac9a60c4 | not-unique-after-dimension-search | base=SUP_DOCKET key_ratio=0.7165 dims_tried=[APPR_DATE, CREATED_DATE, DATE_APP] ratios_at_each_level=[0.7165, 0.7244, 0.7244, 0.7244] |
| portal_arc_atlanta_dataatla_c1da9cd6a0 | not-unique-after-dimension-search | base=ZIP key_ratio=0.4667 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.4667, 0.7333] |
| portal_arc_atlanta_dataatla_cc5fa4ca01 | not-unique-after-dimension-search | base=ZIP key_ratio=0.041 dims_tried=[(none found)] ratios_at_each_level=[0.041] |
| portal_arc_atlanta_dataatla_cf92c66ab6 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.9515 dims_tried=[STATUS] ratios_at_each_level=[0.9515, 0.9515] |
| portal_arc_atlanta_dataatla_d6c1e3b844 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0025 dims_tried=[GIS_LAND_PARCELS_CAMA_ST_CLASS, GIS_LAND_PARCELS_CAMA_ST_STATUS, STATUS, GIS_LAND_PARCELS_CAMA_ST_OLD_ID] ratios_at_each_level=[0.0025, 0.0025, 0.0051, 0.0051, 0.0076, 0.0076] |
| portal_arc_atlanta_dataatla_d70207fa18 | not-unique-after-dimension-search | base=DOCKET_NO key_ratio=0.6885 dims_tried=[CREATED_DATE, LAST_EDITED_DATE, STATUS] ratios_at_each_level=[0.6885, 0.8065, 0.858, 0.864] |
| portal_arc_atlanta_dataatla_ddcdf8f47f | not-unique-after-dimension-search | base=ZIP key_ratio=0.004 dims_tried=[(none found)] ratios_at_each_level=[0.004] |
| portal_arc_atlanta_dataatla_e1f71f6ee6 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0478 dims_tried=[STATUS] ratios_at_each_level=[0.0478, 0.0478] |
| portal_arc_atlanta_dataatla_e2c03512e7 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1667 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1667, 0.8571] |
| portal_arc_atlanta_dataatla_e3f1bf2204 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0485 dims_tried=[STATUS] ratios_at_each_level=[0.0485, 0.0485] |
| portal_arc_atlanta_dataatla_f07e02da21 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1781 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1781, 0.8082] |
| portal_arc_atlanta_dataatla_fb2953f9b7 | not-unique-after-dimension-search | base=ZIP key_ratio=0.005 dims_tried=[(none found)] ratios_at_each_level=[0.005] |
| portal_arc_cleveland_open_d_590209b88b | not-unique-after-dimension-search | base=NPI_SII key_ratio=0.2353 dims_tried=[(none found)] ratios_at_each_level=[0.2353] |
| portal_arc_harris_county_op_167ec31b95 | not-unique-after-dimension-search | base=USER_CCN key_ratio=0.5938 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.5938, 0.5938, 0.6042, 0.625] |
| portal_arc_harris_county_op_183e778c9d | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.0034 dims_tried=[INDUSTRY_DESC, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.0034, 0.2603, 0.2603, 0.2671] |
| portal_arc_harris_county_op_19fe875d1d | not-unique-after-dimension-search | base=ZIP key_ratio=0.6 dims_tried=[VAL_DATE, TYPE, STATUS, SHELTER_ID] ratios_at_each_level=[0.6, 0.0286, 0.9143, 0.9714, 0.9714, 0.9714] |
| portal_arc_harris_county_op_1ba6e8027e | not-unique-after-dimension-search | base=SITE_LONGITUDE key_ratio=0.5556 dims_tried=[CALC_DATA_YEAR, POLLUTANT_TYPE_S, TRI_FACILITY_ID] ratios_at_each_level=[0.5556, 0.3704, 0.5556, 0.5556, 0.5556] |
| portal_arc_harris_county_op_1f4d98f329 | not-unique-after-dimension-search | base=ZIP_CODE_1 key_ratio=0.0009 dims_tried=[ZIP_CODE, INDUSTRY_DESCRIPTION, NAICS_INDUSTRY_SECTOR, OBJECT_ID] ratios_at_each_level=[0.0009, 0.2222, 0.0577, 0.1356, 0.1356, 0.2222] |
| portal_arc_harris_county_op_2718b3279a | not-unique-after-dimension-search | base=USER_CCN key_ratio=0.7013 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.7013, 0.7013, 0.7143, 0.7532] |
| portal_arc_harris_county_op_28cf881303 | not-unique-after-dimension-search | base=ZIP key_ratio=0.9231 dims_tried=[VAL_DATE, TYPE, STATUS] ratios_at_each_level=[0.9231, 0.9231, 0.9231, 0.9231] |
| portal_arc_harris_county_op_2a7a02b1e2 | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.8571 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.8571, 0.8571, 0.8571, 0.8571] |
| portal_arc_harris_county_op_3304c540b7 | not-unique-after-dimension-search | base=ZIP_CODE_1 key_ratio=0.0016 dims_tried=[ZIP_CODE, INDUSTRY_DESCRIPTION, NAICS_INDUSTRY_SECTOR, OBJECT_ID] ratios_at_each_level=[0.0016, 0.3922, 0.1023, 0.2403, 0.2403, 0.3922] |
| portal_arc_harris_county_op_33a3918c80 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1322 dims_tried=[VAL_DATE, TYPE, STATUS, SHELTER_ID] ratios_at_each_level=[0.1322, 0.0661, 0.4545, 0.4904, 0.5179, 0.5565] |
| portal_arc_harris_county_op_374d2e791f | not-unique-after-dimension-search | base=CCN key_ratio=0.7013 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.7013, 0.7013, 0.7013, 0.7532] |
| portal_arc_harris_county_op_3e1a188e92 | not-unique-after-dimension-search | base=CCN key_ratio=0.785 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.785, 0.785, 0.7913, 0.8178] |
| portal_arc_harris_county_op_3e3bfd2059 | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.9331 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.9331, 0.9331, 0.9331, 0.9331] |
| portal_arc_harris_county_op_41fba6bf22 | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.8 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.8, 0.8, 0.8, 0.8] |
| portal_arc_harris_county_op_4e0f396a33 | not-unique-after-dimension-search | base=CCN key_ratio=0.8781 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.8781, 0.8781, 0.8808, 0.8861] |
| portal_arc_harris_county_op_4f19f66c45 | not-unique-after-dimension-search | base=USER_CCN key_ratio=0.875 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.875, 0.875, 0.875, 0.9107] |
| portal_arc_harris_county_op_510b4a2ab2 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1331 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1331, 0.5519] |
| portal_arc_harris_county_op_52229e2e24 | not-unique-after-dimension-search | base=USER_ZIP_CODE_1 key_ratio=0.002 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE, USER_OBJECT_ID] ratios_at_each_level=[0.002, 0.5266, 0.0041, 0.0061, 0.0184, 0.5266] |
| portal_arc_harris_county_op_5ab72d4a23 | not-unique-after-dimension-search | base=CCN key_ratio=0.6407 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.6407, 0.6407, 0.6445, 0.6483] |
| portal_arc_harris_county_op_6133483de0 | not-unique-after-dimension-search | base=USER_ZIP_CODE_1 key_ratio=0.0149 dims_tried=[MATCH_TYPE, ADDR_TYPE, STATUS, USER_OBJECT_ID] ratios_at_each_level=[0.0149, 0.0149, 0.0149, 0.0448, 0.0597, 0.0597] |
| portal_arc_harris_county_op_619a8f0a78 | not-unique-after-dimension-search | base=USER_CCN key_ratio=0.785 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.785, 0.785, 0.7944, 0.8224] |
| portal_arc_harris_county_op_6529979a2a | not-unique-after-dimension-search | base=ZIP key_ratio=0.3364 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.3364, 0.8505] |
| portal_arc_harris_county_op_672c54adb5 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1175 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1175, 0.5356] |
| portal_arc_harris_county_op_78806a4cf7 | not-unique-after-dimension-search | base=ZIP key_ratio=0.6 dims_tried=[VAL_DATE, TYPE, STATUS, SHELTER_ID] ratios_at_each_level=[0.6, 0.0286, 0.9143, 0.9714, 0.9714, 0.9714] |
| portal_arc_harris_county_op_7bd125dfb0 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1337 dims_tried=[VAL_DATE, TYPE, STATUS, SHELTER_ID] ratios_at_each_level=[0.1337, 0.0696, 0.4624, 0.4958, 0.5042, 0.5432] |
| portal_arc_harris_county_op_8ce538dbe3 | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.87 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.87, 0.87, 0.87, 0.87] |
| portal_arc_harris_county_op_a2c8055efb | not-unique-after-dimension-search | base=ZIP key_ratio=0.0855 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.0855, 0.3885] |
| portal_arc_harris_county_op_a35053ac76 | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.8421 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.8421, 0.8421, 0.8421, 0.8421] |
| portal_arc_harris_county_op_a5e2395522 | not-unique-after-dimension-search | base=ZIP key_ratio=0.9231 dims_tried=[VAL_DATE, TYPE, STATUS] ratios_at_each_level=[0.9231, 0.9231, 0.9231, 0.9231] |
| portal_arc_harris_county_op_b86519b42d | not-unique-after-dimension-search | base=ZIP key_ratio=0.0855 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.0855, 0.3885] |
| portal_arc_harris_county_op_bef7c03176 | not-unique-after-dimension-search | base=USER_CCN key_ratio=0.8781 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.8781, 0.8781, 0.8795, 0.8848] |
| portal_arc_harris_county_op_c23dc4baf8 | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.9629 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.9629, 0.9629, 0.9629, 0.9629] |
| portal_arc_harris_county_op_caf5c156e3 | not-unique-after-dimension-search | base=USER_CCN key_ratio=0.6407 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.6407, 0.6407, 0.6426, 0.6464] |
| portal_arc_harris_county_op_cb850cc4b0 | not-unique-after-dimension-search | base=USER_ZIP_CODE key_ratio=0.118 dims_tried=[MATCH_TYPE, ADDR_TYPE, STATUS] ratios_at_each_level=[0.118, 0.1404, 0.2135, 0.2247] |
| portal_arc_harris_county_op_cbd49c80e4 | not-unique-after-dimension-search | base=CCN key_ratio=0.2339 dims_tried=[TYPE] ratios_at_each_level=[0.2339, 0.2417] |
| portal_arc_harris_county_op_d044517cb3 | not-unique-after-dimension-search | base=ZIP_CODE_1 key_ratio=0.0028 dims_tried=[ZIP_CODE, INDUSTRY_DESCRIPTION, NAICS_INDUSTRY_SECTOR, OBJECT_ID] ratios_at_each_level=[0.0028, 0.3567, 0.1081, 0.2331, 0.2331, 0.3708] |
| portal_arc_harris_county_op_d048520a99 | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.9331 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.9331, 0.9331, 0.9331, 0.9331] |
| portal_arc_harris_county_op_d1eb790fbd | not-unique-after-dimension-search | base=ZIP key_ratio=0.1322 dims_tried=[VAL_DATE, TYPE, STATUS, SHELTER_ID] ratios_at_each_level=[0.1322, 0.0661, 0.4545, 0.4904, 0.5179, 0.5565] |
| portal_arc_harris_county_op_d248a81cd8 | not-unique-after-dimension-search | base=ZIP_CODE_1 key_ratio=0.0005 dims_tried=[ZIP_CODE, INDUSTRY_DESCRIPTION, NAICS_INDUSTRY_SECTOR, OBJECT_ID] ratios_at_each_level=[0.0005, 0.1275, 0.033, 0.078, 0.078, 0.1275] |
| portal_arc_harris_county_op_d53d8cc5d8 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1331 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1331, 0.5519] |
| portal_arc_harris_county_op_e68addc07c | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.9394 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.9394, 0.9394, 0.9394, 0.9394] |
| portal_arc_harris_county_op_ea34bddb5d | not-unique-after-dimension-search | base=ZIP key_ratio=0.9231 dims_tried=[VAL_DATE, TYPE, STATUS] ratios_at_each_level=[0.9231, 0.9231, 0.9231, 0.9231] |
| portal_arc_harris_county_op_f22d53c24d | not-unique-after-dimension-search | base=CCN key_ratio=0.875 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.875, 0.875, 0.875, 0.9107] |
| portal_arc_harris_county_op_f9118d0dee | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.9313 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.9313, 0.9321, 0.9321, 0.933] |
| portal_arc_harris_county_op_fb6331e67a | not-unique-after-dimension-search | base=ZIP key_ratio=0.046 dims_tried=[INDUSTRY_D] ratios_at_each_level=[0.046, 0.7404] |
| portal_arc_harris_county_op_fcfe62d3be | not-unique-after-dimension-search | base=GEOID20 key_ratio=0.5 dims_tried=[(none found)] ratios_at_each_level=[0.5] |
| portal_arc_harris_county_op_fe2134f2c8 | not-unique-after-dimension-search | base=USER_CCN key_ratio=0.6407 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.6407, 0.6407, 0.6426, 0.6464] |
| portal_arc_kentucky_open_gi_100da931eb | not-unique-after-dimension-search | base=ZIP key_ratio=0.4074 dims_tried=[END_ACTIVE_DATE, LAST_EDITED_DATE, CREATED_DATE, KBIF_ID, CHF_ID_PR, CHF_ID_COM, CHF_ID_EX] ratios_at_each_level=[0.4074, 0.5916, 0.0127, 0.0005, 0.0005, 0.4074, 0.5018, 0.5018, 0.7215] |
| portal_arc_kentucky_open_gi_23e8e1668c | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.969 dims_tried=[(none found)] ratios_at_each_level=[0.969] |
| portal_arc_kentucky_open_gi_2a1893fe0b | not-unique-after-dimension-search | base=COUNTY_FIPS key_ratio=0.058 dims_tried=[ISSUE_DATE, EXPIRATION_DATE, SIC_CODE, ADD_ID] ratios_at_each_level=[0.058, 0.0075, 0.897, 0.8995, 0.91, 0.91] |
| portal_arc_la_county_open_d_108a1e6982 | not-unique-after-dimension-search | base=ZIP key_ratio=0.5753 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.5753, 0.5808, 0.5863] |
| portal_arc_la_county_open_d_1632a8e413 | not-unique-after-dimension-search | base=ZIP key_ratio=0.75 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.75, 0.75, 0.75] |
| portal_arc_la_county_open_d_18ee361084 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1032 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.1032, 0.1032, 0.1032] |
| portal_arc_la_county_open_d_1a6706943d | not-unique-after-dimension-search | base=NPI key_ratio=0.478 dims_tried=[FAC_TYPE_C, CCLHO_CODE, TYPE_OF_CA, OSHPD_ID] ratios_at_each_level=[0.478, 0.6795, 0.489, 0.489, 0.489, 0.8055] |
| portal_arc_la_county_open_d_1edd056661 | not-unique-after-dimension-search | base=CCN+NPI key_ratio=0.7095 dims_tried=[PARTICIPATION_DATE, APPROVAL_DATE, START_DATE, HCAI_ID] ratios_at_each_level=[0.7095, 0.5975, 0.598, 0.598, 0.629, 0.884] |
| portal_arc_la_county_open_d_3d07eb80ac | not-unique-after-dimension-search | base=ZIP key_ratio=0.1911 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.1911, 0.1963, 0.2074] |
| portal_arc_la_county_open_d_460f3f619b | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.8361 dims_tried=[(none found)] ratios_at_each_level=[0.8361] |
| portal_arc_la_county_open_d_501c20229c | not-unique-after-dimension-search | base=USER_MAILING_ZIP_CODE key_ratio=0.3344 dims_tried=[USER_ZIP_CODE] ratios_at_each_level=[0.3344, 0.9495] |
| portal_arc_la_county_open_d_5ab83c24a0 | not-unique-after-dimension-search | base=NPI key_ratio=0.32 dims_tried=[ZIP_CODE, SCC_TYPE, FAMILY_FRIENDLY_SCC_TYPE] ratios_at_each_level=[0.32, 0.3822, 0.9689, 0.9778] |
| portal_arc_la_county_open_d_6f0fcb8a75 | not-unique-after-dimension-search | base=ZIP key_ratio=0.5304 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.5304, 0.5377, 0.5426] |
| portal_arc_la_county_open_d_73b029dcd6 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1383 dims_tried=[(none found)] ratios_at_each_level=[0.1383] |
| portal_arc_la_county_open_d_7528d085ce | not-unique-after-dimension-search | base=ZIP key_ratio=0.5714 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.5714, 0.5775, 0.5775] |
| portal_arc_la_county_open_d_86c98732bb | not-unique-after-dimension-search | base=ZIP key_ratio=0.8151 dims_tried=[CATEGORY] ratios_at_each_level=[0.8151, 0.8767] |
| portal_arc_la_county_open_d_90f6889981 | not-unique-after-dimension-search | base=ZIP key_ratio=0.5472 dims_tried=[(none found)] ratios_at_each_level=[0.5472] |
| portal_arc_la_county_open_d_92cd102da7 | not-unique-after-dimension-search | base=NPI key_ratio=0.3037 dims_tried=[SCC_TYPE, ZIP_CODE] ratios_at_each_level=[0.3037, 0.8906, 0.9485] |
| portal_arc_la_county_open_d_92efbd96e7 | not-unique-after-dimension-search | base=ZIP key_ratio=0.9286 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.9286, 0.9286, 0.9286] |
| portal_arc_la_county_open_d_a77e98386f | not-unique-after-dimension-search | base=ZIP key_ratio=0.1325 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.1325, 0.139, 0.1395] |
| portal_arc_la_county_open_d_ad0b3db8cd | not-unique-after-dimension-search | base=ZIP key_ratio=0.6364 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.6364, 0.6364, 0.6364] |
| portal_arc_la_county_open_d_e59bd7cf06 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1806 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.1806, 0.1851, 0.1882] |
| portal_arc_la_county_open_d_e68ddab268 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1257 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.1257, 0.1257, 0.1257] |
| portal_arc_la_county_open_d_e6a4c1d69b | not-unique-after-dimension-search | base=ZIP key_ratio=0.155 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.155, 0.162, 0.1635] |
| portal_arc_la_county_open_d_e85041e063 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1408 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.1408, 0.1458, 0.1584] |
| portal_arc_la_county_open_d_f6444997fa | not-unique-after-dimension-search | base=ZIP key_ratio=0.8829 dims_tried=[STATUS, REC_TYPE] ratios_at_each_level=[0.8829, 0.8829, 0.8829] |
| portal_arc_louisville_open_0574425f4f | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.5882 dims_tried=[PROGRAM_LEVEL, INDUSTRY] ratios_at_each_level=[0.5882, 0.6471, 0.7647] |
| portal_arc_louisville_open_4654b3d9ba | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.0265 dims_tried=[PRIMARY_SIC_CODE, SIC_CODE_1, SIC_CODE_1_DESCRIPTION] ratios_at_each_level=[0.0265, 0.2785, 0.2785, 0.2785] |
| portal_arc_louisville_open_733584a9a0 | not-unique-after-dimension-search | base=GEOMETRY key_ratio=0.1818 dims_tried=[(none found)] ratios_at_each_level=[0.1818] |
| portal_arc_louisville_open_b5dab97e2b | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.016 dims_tried=[PRIMARY_SIC_CODE, SIC_CODE_1, SIC_CODE_1_DESCRIPTION] ratios_at_each_level=[0.016, 0.6815, 0.6815, 0.6815] |
| portal_arc_louisville_open_e92145c6d2 | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.5556 dims_tried=[PROGRAM_LEVEL, INDUSTRY] ratios_at_each_level=[0.5556, 0.6111, 0.7222] |
| portal_arc_louisville_open_f2b7ca4b76 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.0905 dims_tried=[(none found)] ratios_at_each_level=[0.0905] |
| portal_arc_maricopa_county_55b91e4bd1 | not-unique-after-dimension-search | base=ACC_DOCKET key_ratio=0.341 dims_tried=[(none found)] ratios_at_each_level=[0.341] |
| portal_arc_maricopa_county_91150b6a88 | not-unique-after-dimension-search | base=ACC_DOCKET key_ratio=0.2718 dims_tried=[(none found)] ratios_at_each_level=[0.2718] |
| portal_arc_memphis_open_dat_47c4a90fea | not-unique-after-dimension-search | base=DOCKET key_ratio=0.9592 dims_tried=[YEAR] ratios_at_each_level=[0.9592, 0.9592] |
| portal_arc_memphis_open_dat_c9e8070496 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.9619 dims_tried=[YEAR] ratios_at_each_level=[0.9619, 0.9619] |
| portal_arc_memphis_open_dat_d0ae25bc24 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.8593 dims_tried=[YEAR] ratios_at_each_level=[0.8593, 0.8593] |
| portal_arc_new_hampshire_ge_6731f28d87 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.848 dims_tried=[(none found)] ratios_at_each_level=[0.848] |
| portal_arc_new_mexico_open_3382d9f21e | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.0525 dims_tried=[DISCOVERY_DATE, EVENT_START_DATE, EVENT_END_DATE, TEMPO_AI_ID] ratios_at_each_level=[0.0525, 0.0525, 0.7995, 0.8265, 0.871, 0.871] |
| portal_arc_new_mexico_open_6e34862f8d | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.0525 dims_tried=[DISCOVERY_DATE, EVENT_START_DATE, EVENT_END_DATE, TEMPO_AI_ID] ratios_at_each_level=[0.0525, 0.0525, 0.7995, 0.8265, 0.871, 0.871] |
| portal_arc_new_mexico_open_7de8f482f1 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0075 dims_tried=[VAL_DATE, YEAR, TYPE_CODE, ID, ST_ASGN_ID] ratios_at_each_level=[0.0075, 0.0235, 0.0104, 0.0075, 0.0075, 0.0188, 0.0612] |
| portal_arc_new_mexico_open_fc7aade1b3 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.0525 dims_tried=[EVENT_START_DATE, EVENT_END_DATE, SOURCE_CLASSIFICATION] ratios_at_each_level=[0.0525, 0.819, 0.8665, 0.8665] |
| portal_arc_open_data_dc_43dcbd8be3 | not-unique-after-dimension-search | base=CCN key_ratio=0.774 dims_tried=[REPORTDATE, YEAR_BUILT, LEVEL, WARD_ID, ANC_ID, SMD_ID, GIS_ID, LEA_ID, SCHOOL_ID, MAR_ID, FACILITY_ID, ID] ratios_at_each_level=[0.774, 0.004, 0.019, 0.0945, 0.1125, 0.025, 0.0875, 0.07, 0.0885, 0.0215, 0.7745, 0.7745, 0.7745, 0.7745] |
| portal_arc_open_data_dc_8c6ef16235 | not-unique-after-dimension-search | base=SUM_CCN key_ratio=0.8235 dims_tried=[YEAR] ratios_at_each_level=[0.8235, 0.8235] |
| portal_arc_open_data_dc_9a20ce1fc5 | not-unique-after-dimension-search | base=CCN_ANONYMIZED key_ratio=0.801 dims_tried=[STOP_DATE, ARREST_DATE, STOP_TYPE] ratios_at_each_level=[0.801, 0.801, 0.8285, 0.8285] |
| portal_arc_open_data_dc_b1daeccb1b | not-unique-after-dimension-search | base=NPDES_ID key_ratio=0.7952 dims_tried=[EFFECTIVE_DATE, ORIGINAL_ISSUE_DATE, TYPE_OF_FACILITY, OBJ_ID] ratios_at_each_level=[0.7952, 0.7952, 0.7952, 0.7952, 0.7952, 0.7952] |
| portal_arc_open_data_dc_d74755206a | no-key-column | ENTITY_TYPES hint: (none) |
| portal_arc_open_data_dc_e28c8c471a | not-unique-after-dimension-search | base=NPDES_ID key_ratio=0.7952 dims_tried=[EFFECTIVE_DATE, ORIGINAL_ISSUE_DATE, TYPE_OF_FACILITY, OBJ_ID] ratios_at_each_level=[0.7952, 0.7952, 0.7952, 0.7952, 0.7952, 0.7952] |
| portal_arc_open_data_hartfo_8a24ea33e4 | not-unique-after-dimension-search | base=SECONDARY_ZIP_CODE key_ratio=0.0165 dims_tried=[CENSUS_BLOCK_GROUP, PRIMARY_SIC_CODE, NAICS_CODE] ratios_at_each_level=[0.0165, 0.0335, 0.553, 0.553] |
| portal_arc_open_data_minnea_5381ac03f1 | not-unique-after-dimension-search | base=ZIP key_ratio=0.195 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.195, 0.1975, 0.1975, 0.2385] |
| portal_arc_open_data_minnea_5605a903bd | not-unique-after-dimension-search | base=ZIP key_ratio=0.4103 dims_tried=[VAL_DATE, TYPE, STATUS, SHELTER_ID] ratios_at_each_level=[0.4103, 0.0513, 0.9487, 0.9487, 0.9487, 0.9487] |
| portal_arc_open_data_minnea_f87ff14b56 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1037 dims_tried=[STATUS, MATCH_TYPE, ADDR_TYPE] ratios_at_each_level=[0.1037, 0.1067, 0.1067, 0.1709] |
| portal_arc_open_data_raleig_67efbac9dd | not-unique-after-dimension-search | base=SHIPPING_ZIP_POSTAL_CODE key_ratio=0.1818 dims_tried=[APPLICATION_DATE, NAICS_6_DIGIT_CODE] ratios_at_each_level=[0.1818, 0.75, 0.9545] |
| portal_arc_open_data_raleig_e6d57da26d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_arc_orange_county_op_1a50e60d53 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0769 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.0769, 0.2308, 0.0769, 0.0769, 0.8462, 0.8462] |
| portal_arc_orange_county_op_27452024db | not-unique-after-dimension-search | base=ZIP key_ratio=0.0678 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.0678, 0.0339, 0.0678, 0.0678, 0.9153, 0.9153] |
| portal_arc_orange_county_op_3a2a7267d1 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1212 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.1212, 0.0303, 0.1212, 0.1212, 0.1212, 0.1212] |
| portal_arc_orange_county_op_5e4098f260 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0159 dims_tried=[SIC_CODE] ratios_at_each_level=[0.0159, 0.0317] |
| portal_arc_orange_county_op_6baa47a46b | not-unique-after-dimension-search | base=ZIP key_ratio=0.0303 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.0303, 0.0606, 0.0303, 0.0303, 0.9697, 0.9697] |
| portal_arc_orange_county_op_75efff54d5 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1356 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.1356, 0.0339, 0.1695, 0.1695, 0.1864, 0.2034] |
| portal_arc_orange_county_op_8c9550f9c6 | not-unique-after-dimension-search | base=ZIP key_ratio=0.6154 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.6154, 0.0769, 0.6154, 0.6923, 0.6923, 0.6923] |
| portal_arc_orange_county_op_a69a248695 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.1, 0.1, 0.1, 0.1, 0.9, 0.9] |
| portal_arc_orange_county_op_bfabcc10a2 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1111 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.1111, 0.9167, 0.1111, 0.125, 0.4861, 0.9444] |
| portal_arc_orange_county_op_ea54ec8366 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1111 dims_tried=[INSPECTION_DATE, OPERATIONAL_STATUS, PROGRAM_ELEMENT, FACILITY_ID] ratios_at_each_level=[0.1111, 0.9167, 0.1111, 0.125, 0.4861, 0.9444] |
| portal_arc_tn_data_tennesse_32a03713cf | not-unique-after-dimension-search | base=ZIP_4 key_ratio=0.001 dims_tried=[FILE_TYPE, STATUS_1, SCHOOL_TYPE, COUNTY_ID] ratios_at_each_level=[0.001, 0.011, 0.0025, 0.003, 0.0055, 0.024] |
| portal_arc_tn_data_tennesse_6321c469fe | not-unique-after-dimension-search | base=ZIP_4 key_ratio=0.001 dims_tried=[FILE_TYPE, STATUS_1, SCHOOL_TYPE, COUNTY_ID] ratios_at_each_level=[0.001, 0.048, 0.0025, 0.0035, 0.0075, 0.1265] |
| portal_arc_tn_data_tennesse_a88ff7d84f | not-unique-after-dimension-search | base=ZIP_4 key_ratio=0.0005 dims_tried=[FILE_TYPE, STATUS_1, SCHOOL_TYPE, COUNTY_ID] ratios_at_each_level=[0.0005, 0.0475, 0.001, 0.0015, 0.005, 0.1045] |
| portal_arc_tn_data_tennesse_b3e1127384 | not-unique-after-dimension-search | base=ZIP_4 key_ratio=0.092 dims_tried=[STATUS] ratios_at_each_level=[0.092, 0.095] |
| portal_arc_tucson_open_data_04ee75be01 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3164 dims_tried=[PUR_DATE, APP_DATE, ORD3_RESO_DATE, ID, OLD_ID] ratios_at_each_level=[0.3164, 0.9058, 0.9012, 0.4642, 0.498, 0.4998, 0.9064] |
| portal_arc_tucson_open_data_057c5355e3 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.0005 dims_tried=[POSTAL_CODE, ADR_STATUS, PRICE_CATEGORY] ratios_at_each_level=[0.0005, 0.707, 0.768, 0.8265] |
| portal_arc_tucson_open_data_0697237a35 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.4249 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.4249, 0.594, 0.594, 0.594] |
| portal_arc_tucson_open_data_080c2334ee | not-unique-after-dimension-search | base=DOCKET key_ratio=0.7647 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.7647, 0.8824, 0.8824, 0.8824] |
| portal_arc_tucson_open_data_0f83b7c628 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.2887 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.2887, 0.4789, 0.4789, 0.507] |
| portal_arc_tucson_open_data_1073539fe2 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.7073 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.7073, 0.9756, 0.9756, 0.9756] |
| portal_arc_tucson_open_data_172a59fdf6 | not-unique-after-dimension-search | base=ZIP key_ratio=0.25 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.25, 0.75] |
| portal_arc_tucson_open_data_1e628cd572 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1268 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1268, 0.6901] |
| portal_arc_tucson_open_data_289e71c579 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.0005 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.0005, 0.0725, 0.0725, 0.0725] |
| portal_arc_tucson_open_data_28f95ebb76 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.6957 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.6957, 0.8261, 0.8261, 0.8261] |
| portal_arc_tucson_open_data_328af9f277 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.5 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.5, 0.6667, 0.6667, 0.6667] |
| portal_arc_tucson_open_data_3d7c82e432 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.373 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.373, 0.7335, 0.7335, 0.7335] |
| portal_arc_tucson_open_data_40615e7b14 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.4778 dims_tried=[PUR_DATE, APP_DATE, ORD3_RESO_DATE, ID, OLD_ID] ratios_at_each_level=[0.4778, 0.8725, 0.8423, 0.573, 0.6136, 0.6152, 0.9185] |
| portal_arc_tucson_open_data_44f7648869 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.0005 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.0005, 0.1965, 0.1965, 0.1965] |
| portal_arc_tucson_open_data_4b31591f91 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.025 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT, BB_ID] ratios_at_each_level=[0.025, 0.006, 0.2525, 0.2525, 0.2525, 0.2665] |
| portal_arc_tucson_open_data_4fb5ea68fc | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3085 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3085, 0.651, 0.651, 0.651] |
| portal_arc_tucson_open_data_563e6e04a6 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0383 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.0383, 0.6873] |
| portal_arc_tucson_open_data_575b865a46 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.5094 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.5094, 0.7925, 0.7925, 0.7925] |
| portal_arc_tucson_open_data_57df097e01 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.527 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.527, 0.8243, 0.8243, 0.8243] |
| portal_arc_tucson_open_data_5b985cbfb5 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3375 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3375, 0.62, 0.62, 0.62] |
| portal_arc_tucson_open_data_5d84af2604 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3421 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3421, 0.8632, 0.8632, 0.8632] |
| portal_arc_tucson_open_data_65984adfba | not-unique-after-dimension-search | base=DOCKET key_ratio=0.479 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.479, 0.5745, 0.5745, 0.5745] |
| portal_arc_tucson_open_data_65a6cdef8f | not-unique-after-dimension-search | base=ZIP key_ratio=0.1316 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1316, 0.6447] |
| portal_arc_tucson_open_data_664d252729 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.368 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.368, 0.5, 0.5, 0.5] |
| portal_arc_tucson_open_data_6720a5ff25 | not-unique-after-dimension-search | base=ZIP key_ratio=0.2 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.2, 0.6] |
| portal_arc_tucson_open_data_688a84ddbf | not-unique-after-dimension-search | base=DOCKET_PAGE key_ratio=0.1695 dims_tried=[APP_DATE, CIRC_DATE, SUM_LTR_DATE, ID, ID_1] ratios_at_each_level=[0.1695, 0.0005, 0.0005, 0.2645, 0.269, 0.2695, 0.2695] |
| portal_arc_tucson_open_data_69487e016f | not-unique-after-dimension-search | base=DOCKET key_ratio=0.387 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.387, 0.6867, 0.6867, 0.6867] |
| portal_arc_tucson_open_data_6a79648a77 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.375 dims_tried=[LAST_EDITED_DATE, POSTAL_CODE, ADR_STATUS] ratios_at_each_level=[0.375, 0.375, 0.6185, 0.638] |
| portal_arc_tucson_open_data_6e966edc1b | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3011 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3011, 0.8977, 0.8977, 0.8977] |
| portal_arc_tucson_open_data_7044e0923d | not-unique-after-dimension-search | base=DOCKET key_ratio=0.6923 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.6923, 0.9231, 0.9231, 0.9231] |
| portal_arc_tucson_open_data_70cedcb206 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3725 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3725, 0.7375, 0.7375, 0.7375] |
| portal_arc_tucson_open_data_726a6c58e2 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3825 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT, BB_ID, URBAN_ID, BB_ID_1, URBAN_ID_1, UNIQUE_ID, ADR_ID, BLD_ID, UNIT_ID, CITY_ID, LOT_ID, BU_ADR_ID] ratios_at_each_level=[0.3825, 0.0035, 0.0035, 0.0005, 0.003, 0.033, 0.0005, 0.0005, 0.0005, 0.0005, 0.0005, 0.0005, 0.6765, 0.6765, 0.6765, 0.7195] |
| portal_arc_tucson_open_data_7672db717a | not-unique-after-dimension-search | base=DOCKET key_ratio=0.5015 dims_tried=[LAST_EDITED_DATE, POSTAL_CODE, ADR_STATUS] ratios_at_each_level=[0.5015, 0.5015, 0.827, 0.837] |
| portal_arc_tucson_open_data_78a99cb261 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.479 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.479, 0.5745, 0.5745, 0.5745] |
| portal_arc_tucson_open_data_78df4dc45f | not-unique-after-dimension-search | base=ZIP key_ratio=0.0244 dims_tried=[(none found)] ratios_at_each_level=[0.0244] |
| portal_arc_tucson_open_data_7b6232f22d | not-unique-after-dimension-search | base=DOCKET key_ratio=0.289 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.289, 0.497, 0.497, 0.497] |
| portal_arc_tucson_open_data_7b93faac46 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0367 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.0367, 0.6864] |
| portal_arc_tucson_open_data_7e21327fcb | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3197 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3197, 0.8129, 0.8129, 0.8129] |
| portal_arc_tucson_open_data_7f7e374c68 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.391 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.391, 0.5629, 0.5629, 0.5629] |
| portal_arc_tucson_open_data_80b28fb6d7 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.5714 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.5714, 0.9048, 0.9048, 0.9048] |
| portal_arc_tucson_open_data_81514e21d3 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.378 dims_tried=[LAST_EDITED_DATE, POSTAL_CODE, ADR_STATUS] ratios_at_each_level=[0.378, 0.378, 0.6165, 0.636] |
| portal_arc_tucson_open_data_81eb8ba37c | not-unique-after-dimension-search | base=DOCKET key_ratio=0.288 dims_tried=[STATUS_1, SUB_TYPE, TYPE_DESC] ratios_at_each_level=[0.288, 0.3835, 0.5045, 0.5045] |
| portal_arc_tucson_open_data_821c8a43b1 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.5595 dims_tried=[FP_STATUS] ratios_at_each_level=[0.5595, 0.5595] |
| portal_arc_tucson_open_data_82607fbfc9 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.5355 dims_tried=[LAST_EDITED_DATE, POSTAL_CODE, ADR_STATUS] ratios_at_each_level=[0.5355, 0.5355, 0.793, 0.7975] |
| portal_arc_tucson_open_data_86a898ef77 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.4256 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.4256, 0.8603, 0.8603, 0.8603] |
| portal_arc_tucson_open_data_8896d12631 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.0005 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.0005, 0.0725, 0.0725, 0.0725] |
| portal_arc_tucson_open_data_89df24d316 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.5015 dims_tried=[LAST_EDITED_DATE, POSTAL_CODE, ADR_STATUS] ratios_at_each_level=[0.5015, 0.5015, 0.827, 0.837] |
| portal_arc_tucson_open_data_8aad75bf85 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.1933 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.1933, 0.2017, 0.2017, 0.2017] |
| portal_arc_tucson_open_data_8ab8eaf3df | not-unique-after-dimension-search | base=DOCKET key_ratio=0.423 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.423, 0.5465, 0.5465, 0.5465] |
| portal_arc_tucson_open_data_8e55e53d8d | not-unique-after-dimension-search | base=DOCKET key_ratio=0.0005 dims_tried=[YEAR, PRICE_CATEGORY, ADR_STATUS] ratios_at_each_level=[0.0005, 0.0485, 0.1265, 0.149] |
| portal_arc_tucson_open_data_90c091b01b | not-unique-after-dimension-search | base=DOCKET key_ratio=0.489 dims_tried=[ADR_STATUS] ratios_at_each_level=[0.489, 0.5595] |
| portal_arc_tucson_open_data_90cc86dc8c | not-unique-after-dimension-search | base=DOCKET key_ratio=0.374 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.374, 0.671, 0.671, 0.671] |
| portal_arc_tucson_open_data_944b32bc37 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0538 dims_tried=[(none found)] ratios_at_each_level=[0.0538] |
| portal_arc_tucson_open_data_95246841cb | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3439 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3439, 0.8042, 0.8042, 0.8042] |
| portal_arc_tucson_open_data_97b5e23500 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.4755 dims_tried=[POSTAL_CODE] ratios_at_each_level=[0.4755, 0.776] |
| portal_arc_tucson_open_data_9b42294e74 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.2368 dims_tried=[R_DATE, EXP_DATE] ratios_at_each_level=[0.2368, 0.9737, 0.9737] |
| portal_arc_tucson_open_data_a0293b412c | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3611 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3611, 0.7917, 0.7917, 0.7917] |
| portal_arc_tucson_open_data_a2044bd114 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0148 dims_tried=[(none found)] ratios_at_each_level=[0.0148] |
| portal_arc_tucson_open_data_a40fb2876b | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3345 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3345, 0.6245, 0.6245, 0.6245] |
| portal_arc_tucson_open_data_a54a25ca53 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.325 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.325, 0.5765, 0.5765, 0.5765] |
| portal_arc_tucson_open_data_a937d836b3 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3725 dims_tried=[LAST_EDITED_DATE, POSTAL_CODE, ADR_STATUS] ratios_at_each_level=[0.3725, 0.3725, 0.6155, 0.6265] |
| portal_arc_tucson_open_data_a94d7dfbcf | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3375 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3375, 0.62, 0.62, 0.62] |
| portal_arc_tucson_open_data_ac3b9c03a4 | not-unique-after-dimension-search | base=ZIP key_ratio=0.01 dims_tried=[(none found)] ratios_at_each_level=[0.01] |
| portal_arc_tucson_open_data_ad408fdf6d | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3345 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3345, 0.6245, 0.6245, 0.6245] |
| portal_arc_tucson_open_data_ad6f34f882 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3164 dims_tried=[PUR_DATE, APP_DATE, ORD3_RESO_DATE, ID, OLD_ID] ratios_at_each_level=[0.3164, 0.9058, 0.9012, 0.4642, 0.498, 0.4998, 0.9064] |
| portal_arc_tucson_open_data_b15ae2b075 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.4727 dims_tried=[PUR_DATE, APP_DATE, ORD3_RESO_DATE, ID, OLD_ID] ratios_at_each_level=[0.4727, 0.88, 0.8407, 0.5728, 0.6141, 0.6161, 0.9174] |
| portal_arc_tucson_open_data_b44ead49d6 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.4545 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.4545, 0.7576, 0.7576, 0.7576] |
| portal_arc_tucson_open_data_b64e31a541 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.4699 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.4699, 0.8709, 0.8709, 0.8709] |
| portal_arc_tucson_open_data_b77e902275 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.434 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.434, 0.6945, 0.6945, 0.6945] |
| portal_arc_tucson_open_data_b8be43cf1c | not-unique-after-dimension-search | base=DOCKET key_ratio=0.369 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.369, 0.4905, 0.4905, 0.4905] |
| portal_arc_tucson_open_data_bade778b92 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.36 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.36, 0.6845, 0.6845, 0.6845] |
| portal_arc_tucson_open_data_bda54fb1d9 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.421 dims_tried=[(none found)] ratios_at_each_level=[0.421] |
| portal_arc_tucson_open_data_c1addcddd2 | not-unique-after-dimension-search | base=DOCKET_PAGE key_ratio=0.3495 dims_tried=[STATUS, ACTION_STATUS] ratios_at_each_level=[0.3495, 0.5355, 0.5435] |
| portal_arc_tucson_open_data_c92a89bb0d | not-unique-after-dimension-search | base=DOCKET key_ratio=0.374 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.374, 0.707, 0.707, 0.707] |
| portal_arc_tucson_open_data_cdd4037df8 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.331 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.331, 0.4675, 0.4675, 0.4675] |
| portal_arc_tucson_open_data_cf1942a6ce | not-unique-after-dimension-search | base=DOCKET key_ratio=0.4755 dims_tried=[POSTAL_CODE] ratios_at_each_level=[0.4755, 0.776] |
| portal_arc_tucson_open_data_cf31c19a20 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.1305 dims_tried=[PUR_DATE, APP_DATE, ORD3_RESO_DATE, ID, OLD_ID] ratios_at_each_level=[0.1305, 0.4121, 0.3776, 0.2628, 0.2704, 0.2713, 0.4408] |
| portal_arc_tucson_open_data_d4ffb81e01 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3989 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3989, 0.7119, 0.7119, 0.7119] |
| portal_arc_tucson_open_data_db600d27ae | not-unique-after-dimension-search | base=DOCKET key_ratio=0.278 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.278, 0.415, 0.415, 0.415] |
| portal_arc_tucson_open_data_e794dddf28 | not-unique-after-dimension-search | base=ZIP key_ratio=0.1594 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.1594, 0.5616] |
| portal_arc_tucson_open_data_e9360f6c40 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3349 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3349, 0.557, 0.557, 0.557] |
| portal_arc_tucson_open_data_ea7adf4848 | not-unique-after-dimension-search | base=ZIP key_ratio=0.7391 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.7391, 0.9565] |
| portal_arc_tucson_open_data_eab8d87a4d | not-unique-after-dimension-search | base=DOCKET key_ratio=0.371 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.371, 0.508, 0.508, 0.508] |
| portal_arc_tucson_open_data_ec706ead4c | not-unique-after-dimension-search | base=DOCKET key_ratio=0.2929 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.2929, 0.8284, 0.8284, 0.8284] |
| portal_arc_tucson_open_data_ee2e5db309 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3665 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.3665, 0.69, 0.69, 0.69] |
| portal_arc_tucson_open_data_f23f6e5c44 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0403 dims_tried=[(none found)] ratios_at_each_level=[0.0403] |
| portal_arc_tucson_open_data_f5dcf594af | not-unique-after-dimension-search | base=DOCKET key_ratio=0.3485 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT, BB_ID] ratios_at_each_level=[0.3485, 0.0055, 0.6445, 0.6445, 0.6445, 0.6735] |
| portal_arc_tucson_open_data_f91596293e | not-unique-after-dimension-search | base=ZIP key_ratio=0.2222 dims_tried=[INDUSTRY_DESC] ratios_at_each_level=[0.2222, 0.8056] |
| portal_arc_tucson_open_data_f9376d5072 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.476 dims_tried=[POSTAL_CODE] ratios_at_each_level=[0.476, 0.7765] |
| portal_arc_tucson_open_data_f970baadb3 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.308 dims_tried=[LAST_EDITED_DATE, POSTAL_CODE, ADR_STATUS] ratios_at_each_level=[0.308, 0.308, 0.558, 0.659] |
| portal_arc_tucson_open_data_fa71372c44 | not-unique-after-dimension-search | base=DOCKET key_ratio=0.376 dims_tried=[LAST_EDITED_DATE, CREATED_DATE_COT, LAST_EDITED_DATE_COT] ratios_at_each_level=[0.376, 0.6235, 0.6235, 0.6235] |
| portal_cka_analyze_boston_03ecd5c73d | not-unique-after-dimension-search | base=LAT key_ratio=0.6013 dims_tried=[MODE_TYPE, LOCATION_TYPE] ratios_at_each_level=[0.6013, 0.6781, 0.6784] |
| portal_cka_analyze_boston_0bdff0513c | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0775 dims_tried=[LATEST_AMENDMENT_EFFECTIVE_DATE, CREATED_DATE, LAST_EDITED_DATE] ratios_at_each_level=[0.0775, 0.0775, 0.0775, 0.0836] |
| portal_cka_analyze_boston_0ccfffcc26 | not-unique-after-dimension-search | base=ZIP key_ratio=0.003 dims_tried=[STATUS, LICENSE_TYPE] ratios_at_each_level=[0.003, 0.0085, 0.0143] |
| portal_cka_analyze_boston_1020ccd06a | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0417 dims_tried=[(none found)] ratios_at_each_level=[0.0417] |
| portal_cka_analyze_boston_11b21c9100 | not-unique-after-dimension-search | base=ZIP key_ratio=0.561 dims_tried=[STATUS, LICENSE_CATEGORY, LICENSE_TYPE] ratios_at_each_level=[0.561, 0.561, 0.561, 0.7317] |
| portal_cka_analyze_boston_134a12a020 | not-unique-after-dimension-search | base=FACILITY_ZIP_CODE key_ratio=0.1149 dims_tried=[APP_LICENSE_CATEGORY, APP_LICENSE_STATUS, LT_LICENSE_TYPE] ratios_at_each_level=[0.1149, 0.3489, 0.4766, 0.4766] |
| portal_cka_analyze_boston_3032706ee4 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0417 dims_tried=[(none found)] ratios_at_each_level=[0.0417] |
| portal_cka_analyze_boston_38eb48ca38 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.4837 dims_tried=[(none found)] ratios_at_each_level=[0.4837] |
| portal_cka_analyze_boston_3947f1d3d1 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_analyze_boston_4a5ca3bce5 | not-unique-after-dimension-search | base=DEVICE_LAT key_ratio=0.2957 dims_tried=[NEIGHBORHOOD_ID] ratios_at_each_level=[0.2957, 0.2093] |
| portal_cka_analyze_boston_5544aba2e2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_analyze_boston_59330da889 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0455 dims_tried=[(none found)] ratios_at_each_level=[0.0455] |
| portal_cka_analyze_boston_5dd692715c | not-unique-after-dimension-search | base=ZIP key_ratio=0.01 dims_tried=[PROPERTY_ID] ratios_at_each_level=[0.01, 0.6726] |
| portal_cka_analyze_boston_5edcde6490 | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.5 dims_tried=[(none found)] ratios_at_each_level=[0.5] |
| portal_cka_analyze_boston_727723877e | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0417 dims_tried=[YEAR] ratios_at_each_level=[0.0417, 0.0833] |
| portal_cka_analyze_boston_75afc07272 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0769 dims_tried=[(none found)] ratios_at_each_level=[0.0769] |
| portal_cka_analyze_boston_78e7b87dd3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_analyze_boston_78e8cd45c9 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.025 dims_tried=[(none found)] ratios_at_each_level=[0.025] |
| portal_cka_analyze_boston_79b955775b | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.1333 dims_tried=[YEAR, USE_TYPE, TYPE] ratios_at_each_level=[0.1333, 0.7333, 0.8, 0.8] |
| portal_cka_analyze_boston_7a1246d4b5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_analyze_boston_80ff6d8e34 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0242 dims_tried=[STATUS, LICENSE_TYPE] ratios_at_each_level=[0.0242, 0.0242, 0.0661] |
| portal_cka_analyze_boston_897a9990fc | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.2208 dims_tried=[(none found)] ratios_at_each_level=[0.2208] |
| portal_cka_analyze_boston_8a79542c61 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0264 dims_tried=[TYPE] ratios_at_each_level=[0.0264, 0.0573] |
| portal_cka_analyze_boston_92ef0e3576 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0192 dims_tried=[(none found)] ratios_at_each_level=[0.0192] |
| portal_cka_analyze_boston_941e6c1d15 | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.7692 dims_tried=[(none found)] ratios_at_each_level=[0.7692] |
| portal_cka_analyze_boston_94ae63a33f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_analyze_boston_9791d2174d | not-unique-after-dimension-search | base=X_LONGITUDE key_ratio=0.969 dims_tried=[POLYGON_ID] ratios_at_each_level=[0.969, 0.7829] |
| portal_cka_analyze_boston_992876d5ab | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0036 dims_tried=[(none found)] ratios_at_each_level=[0.0036] |
| portal_cka_analyze_boston_9c8338c5c2 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0203 dims_tried=[STATUS, LICENSE_TYPE] ratios_at_each_level=[0.0203, 0.0203, 0.2062] |
| portal_cka_analyze_boston_9ee23f0172 | not-unique-after-dimension-search | base=ZIP key_ratio=0.7778 dims_tried=[(none found)] ratios_at_each_level=[0.7778] |
| portal_cka_analyze_boston_a9b7e5c08a | not-unique-after-dimension-search | base=ZIP key_ratio=0.0029 dims_tried=[SUBMITTED_DATE, RECEIVED_DATE, HEARING_DATE] ratios_at_each_level=[0.0029, 0.5681, 0.5998, 0.6494] |
| portal_cka_analyze_boston_b4c5e99b0a | not-unique-after-dimension-search | base=MAIL_ZIP_CODE key_ratio=0.0409 dims_tried=[YR_BUILT, YR_REMODEL, ZIP_CODE, CM_ID, GIS_ID] ratios_at_each_level=[0.0409, 0.0653, 0.5912, 0.1461, 0.2631, 0.2634, 0.7175] |
| portal_cka_analyze_boston_bd5a2f9374 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.7965 dims_tried=[TYPE] ratios_at_each_level=[0.7965, 0.7971] |
| portal_cka_analyze_boston_be87d5ea10 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.1 dims_tried=[IEL_TYPE] ratios_at_each_level=[0.1, 0.1002] |
| portal_cka_analyze_boston_c0890b412f | not-unique-after-dimension-search | base=ZIP key_ratio=0.4857 dims_tried=[(none found)] ratios_at_each_level=[0.4857] |
| portal_cka_analyze_boston_c1b203dc0a | not-unique-after-dimension-search | base=ZIP key_ratio=0.0085 dims_tried=[STATUS, LICENSE_CATEGORY, LICENSE_TYPE] ratios_at_each_level=[0.0085, 0.0085, 0.0317, 0.1162] |
| portal_cka_analyze_boston_c36f95122c | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.05 dims_tried=[ROW_ID] ratios_at_each_level=[0.05, 0.05] |
| portal_cka_analyze_boston_cf53830f73 | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.1111 dims_tried=[TYPE] ratios_at_each_level=[0.1111, 0.2222] |
| portal_cka_analyze_boston_df0a6de397 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0033 dims_tried=[LICENSE_TYPE] ratios_at_each_level=[0.0033, 0.0079] |
| portal_cka_analyze_boston_ec027d890c | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.1667 dims_tried=[(none found)] ratios_at_each_level=[0.1667] |
| portal_cka_analyze_boston_ecc632a66f | not-unique-after-dimension-search | base=SHAPE_WKT key_ratio=0.0769 dims_tried=[(none found)] ratios_at_each_level=[0.0769] |
| portal_cka_analyze_boston_f059843ba0 | not-unique-after-dimension-search | base=LATITUDE key_ratio=0.8329 dims_tried=[PURCHASED_DATE, METER_TYPE, HOUSING_TYPE, METER_ID] ratios_at_each_level=[0.8329, 0.018, 0.8329, 0.8401, 0.8401, 0.8401] |
| portal_cka_analyze_boston_f267f0b038 | not-unique-after-dimension-search | base=BUSINESS_ZIPCODE key_ratio=0.1618 dims_tried=[BUSINESS_TYPE] ratios_at_each_level=[0.1618, 0.8353] |
| portal_cka_analyze_boston_f5e467a238 | not-unique-after-dimension-search | base=ZIP key_ratio=0.2644 dims_tried=[TYPE] ratios_at_each_level=[0.2644, 0.4828] |
| portal_cka_california_open_016fce0e20 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_07d8d8e651 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_09f2ecf408 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_1424436f0d | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.0205 dims_tried=[FISCAL_YEAR, TYPE, CATEGORY] ratios_at_each_level=[0.0205, 0.0324, 0.0324, 0.0633] |
| portal_cka_california_open_22f6b7db0f | not-unique-after-dimension-search | base=RES_ZIP_CODE key_ratio=0.096 dims_tried=[TYPE, PROGRAM_TYPE, STATUS] ratios_at_each_level=[0.096, 0.316, 0.316, 0.3393] |
| portal_cka_california_open_2d939c89a5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_3972a98745 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_4789f4fdc3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_59afd10b01 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_5dd35f95d8 | not-unique-after-dimension-search | base=CCN+NPI key_ratio=0.6418 dims_tried=[PARTICIPATION_DATE, APPROVAL_DATE, START_DATE, HCAI_ID] ratios_at_each_level=[0.6418, 0.8132, 0.8134, 0.8134, 0.8472, 0.9008] |
| portal_cka_california_open_67a021fadc | not-unique-after-dimension-search | base=LON key_ratio=0.1802 dims_tried=[(none found)] ratios_at_each_level=[0.1802] |
| portal_cka_california_open_72414c64df | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_782f060364 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_878e5cbec3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_89f906dc75 | not-unique-after-dimension-search | base=SHAPE__LENGTH key_ratio=0.8395 dims_tried=[TYPE, PROGRAM] ratios_at_each_level=[0.8395, 0.8625, 0.8758] |
| portal_cka_california_open_94c5c44a4f | not-unique-after-dimension-search | base=GSPAR_ID key_ratio=0.5425 dims_tried=[ALTAR_ID, REPORT_YEAR] ratios_at_each_level=[0.5425, 0.6316, 0.6316] |
| portal_cka_california_open_a6fc6ee30b | not-unique-after-dimension-search | base=ZIP key_ratio=0.1122 dims_tried=[DATE_NOTICE_ISSUED, NOA_DUE_DATE, LOCAL_AGENCY_TYPE] ratios_at_each_level=[0.1122, 0.2431, 0.2441, 0.2543] |
| portal_cka_california_open_a8c3ced685 | not-unique-after-dimension-search | base=ZIP key_ratio=0.3026 dims_tried=[(none found)] ratios_at_each_level=[0.3026] |
| portal_cka_california_open_aa8c1ecaf6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_ad71d0ffde | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_b100823f62 | not-unique-after-dimension-search | base=FACILITY_ZIP key_ratio=0.3545 dims_tried=[LIC_EXPIRATION_DATE, COUNTY_CODE, TYPE_OF_APPLICATION] ratios_at_each_level=[0.3545, 0.8748, 0.8757, 0.9221] |
| portal_cka_california_open_b36ad1f596 | not-unique-after-dimension-search | base=VISIT_TYPE_ID key_ratio=0.0071 dims_tried=[VISIT_CATEGORY_ID, REPORTING_YEAR, PAYER_TYPE] ratios_at_each_level=[0.0071, 0.0071, 0.0071, 0.0152] |
| portal_cka_california_open_b98053323b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_bffafc771d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_cc3ca4c413 | not-unique-after-dimension-search | base=OFFSITE_ZIP key_ratio=0.0568 dims_tried=[START_DATE, DATA_DATE, FAC_TYPE_CODE] ratios_at_each_level=[0.0568, 0.2911, 0.2911, 0.3035] |
| portal_cka_california_open_d33a75d890 | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.168 dims_tried=[EXPIRATION_DATE] ratios_at_each_level=[0.168, 0.9756] |
| portal_cka_california_open_d8c67a34a8 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_dcaeba5312 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_california_open_e27dbb825c | not-unique-after-dimension-search | base=SHAPE__LENGTH key_ratio=0.8023 dims_tried=[DATE_COMPLETED, TREATMENT_TYPE, FUEL_TYPE, PROJECT_ID] ratios_at_each_level=[0.8023, 0.0431, 0.9038, 0.9096, 0.9102, 0.9102] |
| portal_cka_california_open_e87d6ed57d | not-unique-after-dimension-search | base=PL_ADDRESS_ZIP_CODE key_ratio=0.3456 dims_tried=[FAILING_START_DATE, CREATED_DATE, FEDERAL_CLASSIFICATION_TYPE] ratios_at_each_level=[0.3456, 0.4469, 0.4469, 0.5041] |
| portal_cka_houston_open_dat_0aa7c87f45 | not-unique-after-dimension-search | base=DEPARTMENT_ID key_ratio=0.0024 dims_tried=[BIRTH_YEAR, YEAR, DATE_POSITION_BEGAN] ratios_at_each_level=[0.0024, 0.0971, 0.0971, 0.6665] |
| portal_cka_houston_open_dat_1439e11e74 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_1612361f51 | not-unique-after-dimension-search | base=ZIP key_ratio=0.3514 dims_tried=[(none found)] ratios_at_each_level=[0.3514] |
| portal_cka_houston_open_dat_18a3ca22af | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_1e1227f82a | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_21ff930703 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_4581da6829 | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.0246 dims_tried=[(none found)] ratios_at_each_level=[0.0246] |
| portal_cka_houston_open_dat_49ffab9edc | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_5b1522dd22 | not-unique-after-dimension-search | base=PAYEE_ZIP key_ratio=0.0555 dims_tried=[(none found)] ratios_at_each_level=[0.0555] |
| portal_cka_houston_open_dat_824d8a7b02 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_932db3fb0b | not-unique-after-dimension-search | base=ZIP key_ratio=0.6034 dims_tried=[STATUS] ratios_at_each_level=[0.6034, 0.6092] |
| portal_cka_houston_open_dat_9a02a5cfc0 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_bc15145e45 | not-unique-after-dimension-search | base=FUND_ID key_ratio=0.0105 dims_tried=[DEPARTMENT_ID, FISCAL_YEAR, FUND_TYPE] ratios_at_each_level=[0.0105, 0.0178, 0.0178, 0.0178] |
| portal_cka_houston_open_dat_c3f216770e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_c5521bda2a | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_e748ac9e19 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_ebab30a0f0 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_houston_open_dat_f10142914f | not-unique-after-dimension-search | base=ZIP key_ratio=0.0583 dims_tried=[INSPECTION_DATE, CREATED_DATE, LAST_MODIFIED_DATE, INSPECTOR_ID] ratios_at_each_level=[0.0583, 0.0058, 0.6296, 0.6695, 0.6828, 0.7481] |
| portal_cka_indiana_data_hub_0ed686abd6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_34b4dee108 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_378e0419e1 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_45d5d2f154 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_4cfffdcca9 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_4f4ec0066b | not-unique-after-dimension-search | base=LOCATION_ID key_ratio=0.3333 dims_tried=[LOCATION_LEVEL] ratios_at_each_level=[0.3333, 0.3333] |
| portal_cka_indiana_data_hub_50eccf3529 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_517d2c08eb | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_56bfd51405 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_63403b5ee5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_66a945cf17 | not-unique-after-dimension-search | base=PROVIDER_NPI key_ratio=0.168 dims_tried=[YEAR, PROVIDER_ADDRESS_ZIP_CODE, PROVIDER_TYPE, PROVIDER_ID] ratios_at_each_level=[0.168, 0.2082, 0.6366, 0.7278, 0.7314, 0.753] |
| portal_cka_indiana_data_hub_6cff9e6a68 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_71c6f53126 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_77fcbc0131 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_7f118fae1c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_8d92e2391e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_90026d479a | not-unique-after-dimension-search | base=CORP_ID key_ratio=0.0225 dims_tried=[CAL_YEAR, FUND_CLASSIFICATION] ratios_at_each_level=[0.0225, 0.2461, 0.7742] |
| portal_cka_indiana_data_hub_948340249f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_a95d120aeb | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_bd98260749 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_bf3b083e9d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_d0e8c9c66d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_d718232fbc | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_e1074f0714 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_ef21700614 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_indiana_data_hub_fc0abc5edf | not-unique-after-dimension-search | base=OFFENSE_STATE_FIPS key_ratio=0.0001 dims_tried=[OFFENSE_YEAR, ARREST_YEAR, ARREST_MONTH, OFFENDER_STATE_ID_HASHED, ARREST_ID_HASHED, OFFENSE_ID_HASHED] ratios_at_each_level=[0.0001, 0.3517, 0.379, 0.4806, 0.0018, 0.0018, 0.004, 0.4806] |
| portal_cka_indiana_data_hub_fd8fce5dea | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_ireland_national_7b813f1d72 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_ireland_national_8b963015f5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_ireland_national_dc8e6f93c3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_ireland_national_f340fb5cbd | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_0010f646f4 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_0bd41805c9 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_12c20cdac2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_148fdfe63d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_2e5c5129dd | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_3319ebf0c5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_33baa6b58a | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_36f3314f93 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_37143e478a | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_3ef90f6eef | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_3f4b3f41be | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_4145ff0883 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_479e4dc076 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_52ad02ebe0 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_535b8902a2 | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.4317 dims_tried=[DATE] ratios_at_each_level=[0.4317, 0.4317] |
| portal_cka_israel_national_55d94b871e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_5a45b45e6b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_5a78e186da | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_5ab9e69a36 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_612d5c06c4 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_6a3dec66ca | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_6fbfbf9298 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_8649911221 | not-unique-after-dimension-search | base=ZIP key_ratio=0.3325 dims_tried=[(none found)] ratios_at_each_level=[0.3325] |
| portal_cka_israel_national_878a0365b9 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_87e3c2014f | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.575 dims_tried=[OPEN_DATE, CLOSE_DATE, BANK_CODE] ratios_at_each_level=[0.575, 0.8399, 0.8428, 0.9045] |
| portal_cka_israel_national_916719ecc6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_936e1a0ba2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_94ce459e75 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_96d1b74c94 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_973eee3e46 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_b0a05d8626 | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.6966 dims_tried=[APPOINTMENT_DATE] ratios_at_each_level=[0.6966, 0.9793] |
| portal_cka_israel_national_b0e3b6b19b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_b87c2b5695 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_bd42818fc5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_cb289c316e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_d4f3080d38 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_d762c7d9e9 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_d8977c1891 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_da9560f407 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_de246c30f5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_e2dd642689 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_e5bc15077d | not-unique-after-dimension-search | base=ZIP key_ratio=0.6423 dims_tried=[(none found)] ratios_at_each_level=[0.6423] |
| portal_cka_israel_national_e9c63efcda | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_ed3df4543b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_f1419d1386 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_f6de3cb3a1 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_israel_national_f758e5d16e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_017a35122c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_042a7f3ed2 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.593 dims_tried=[PO_DATE, PO_DATE_EXCEL, PO_TYPE] ratios_at_each_level=[0.593, 0.593, 0.593, 0.593] |
| portal_cka_oklahoma_open_da_07a59969f7 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_082d7a8847 | not-unique-after-dimension-search | base=VOUCHER_ID key_ratio=0.6198 dims_tried=[VOUCHER_ID_RELATED, PROJECT_ID, PO_ID] ratios_at_each_level=[0.6198, 0.6198, 0.6198, 0.6198] |
| portal_cka_oklahoma_open_da_085b547d9c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_089b4e30ce | not-unique-after-dimension-search | base=PO_ID key_ratio=0.6022 dims_tried=[PO_DATE, PO_DATE_EXCEL] ratios_at_each_level=[0.6022, 0.6023, 0.6023] |
| portal_cka_oklahoma_open_da_0a2227fc62 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_0e22a8c042 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.5731 dims_tried=[PO_DATE, PO_DATE_EXCEL, PO_TYPE] ratios_at_each_level=[0.5731, 0.5731, 0.5731, 0.5731] |
| portal_cka_oklahoma_open_da_116f4033aa | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_136a4dcd44 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.5722 dims_tried=[PO_DATE, PO_DATE_EXCEL] ratios_at_each_level=[0.5722, 0.5723, 0.5723] |
| portal_cka_oklahoma_open_da_13ac1849e2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_22a43dbe5f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_2a27dea617 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.578 dims_tried=[PO_DATE, PO_DATE_EXCEL] ratios_at_each_level=[0.578, 0.5782, 0.5782] |
| portal_cka_oklahoma_open_da_2d8a48ce3d | not-unique-after-dimension-search | base=PO_ID key_ratio=0.5873 dims_tried=[PO_DATE, PO_DATE_EXCEL] ratios_at_each_level=[0.5873, 0.5875, 0.5875] |
| portal_cka_oklahoma_open_da_2fb541d487 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_314bb9e894 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.4579 dims_tried=[PO_DATE, PO_DATE_EXCEL] ratios_at_each_level=[0.4579, 0.4579, 0.4579] |
| portal_cka_oklahoma_open_da_3b16211196 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_3c2b4d89d6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_41334802fd | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_41b624c494 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_46271d5059 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.387 dims_tried=[REQUISITION_ID, PO_DATE, REQUISITION_DATE] ratios_at_each_level=[0.387, 0.521, 0.521, 0.5217] |
| portal_cka_oklahoma_open_da_49a4d42820 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.5767 dims_tried=[PO_DATE, PO_DATE_EXCEL, PO_TYPE] ratios_at_each_level=[0.5767, 0.5767, 0.5767, 0.5767] |
| portal_cka_oklahoma_open_da_4b6e3ca1ad | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_4cb3b085d7 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.5946 dims_tried=[PO_DATE, PO_DATE_EXCEL, PO_TYPE] ratios_at_each_level=[0.5946, 0.5946, 0.5946, 0.5946] |
| portal_cka_oklahoma_open_da_4da0b9cf8c | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.2751 dims_tried=[YEAR_PROPERTY_ACQUIRED, YEAR_BUILT, LOCATION_TYPE, AGENCY_INVENTORY_ID] ratios_at_each_level=[0.2751, 0.0582, 0.5291, 0.5661, 0.5661, 0.5661] |
| portal_cka_oklahoma_open_da_5869531ec6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_5ede090003 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.3983 dims_tried=[REQUISITION_ID, PO_DATE, REQUISITION_DATE] ratios_at_each_level=[0.3983, 0.5103, 0.5103, 0.5103] |
| portal_cka_oklahoma_open_da_62289bd012 | not-unique-after-dimension-search | base=VOUCHER_ID key_ratio=0.5248 dims_tried=[VOUCHER_ID_RELATED, PROJECT_ID, PO_ID] ratios_at_each_level=[0.5248, 0.5249, 0.5249, 0.5263] |
| portal_cka_oklahoma_open_da_6382f88afe | not-unique-after-dimension-search | base=PO_ID key_ratio=0.3929 dims_tried=[REQUISITION_ID, PO_DATE, PO_DATE_EXCEL] ratios_at_each_level=[0.3929, 0.5014, 0.5014, 0.5014] |
| portal_cka_oklahoma_open_da_67dc405ee6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_682edc2856 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_6b2f35d72c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_6c534d482a | not-unique-after-dimension-search | base=PO_ID key_ratio=0.5416 dims_tried=[PO_DATE, PO_DATE_EXCEL, PO_TYPE] ratios_at_each_level=[0.5416, 0.5416, 0.5416, 0.5416] |
| portal_cka_oklahoma_open_da_6dfa4ff30d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_70dbfdba5c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_7267b4bc2f | not-unique-after-dimension-search | base=VOUCHER_ID key_ratio=0.5199 dims_tried=[VOUCHER_ID_RELATED, PROJECT_ID, PO_ID] ratios_at_each_level=[0.5199, 0.52, 0.52, 0.521] |
| portal_cka_oklahoma_open_da_836c92e47c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_840020a9de | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_8f8a85793f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_92c8cc9499 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_96b2c45728 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_9f247d2153 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_9f748576a8 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_a90b591b09 | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.0012 dims_tried=[YEAR_PROPERTY_ACQUIRED_4_DIGIT_YEAR, LOCATION_TYPE, LEASE_CLASS, AGENCY_INVENTORY_ID] ratios_at_each_level=[0.0012, 0.0357, 0.043, 0.0454, 0.0763, 0.1108] |
| portal_cka_oklahoma_open_da_ab49b627ef | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_ad79042537 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.9244 dims_tried=[(none found)] ratios_at_each_level=[0.9244] |
| portal_cka_oklahoma_open_da_b1c8714a03 | not-unique-after-dimension-search | base=VOUCHER_ID key_ratio=0.4361 dims_tried=[VOUCHER_ID_RELATED, PROJECT_ID, PO_ID] ratios_at_each_level=[0.4361, 0.4361, 0.4361, 0.4364] |
| portal_cka_oklahoma_open_da_b2751a2821 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_b65187987b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_bb949bd77e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_bdc41752a1 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_bebd242d3d | not-unique-after-dimension-search | base=PO_ID key_ratio=0.524 dims_tried=[PO_DATE, PO_DATE_EXCEL, PO_TYPE] ratios_at_each_level=[0.524, 0.524, 0.524, 0.524] |
| portal_cka_oklahoma_open_da_c877a4f53f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_c96ba4e090 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.5603 dims_tried=[LOCATION_TYPE, OWNERSHIP_STATUS, PROPERTY_TYPE, AGENCY_INVENTORY_ID] ratios_at_each_level=[0.5603, 0.0433, 0.5671, 0.5705, 0.6154, 0.6316] |
| portal_cka_oklahoma_open_da_cabb75c107 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_cdf9bdc1c8 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.5177 dims_tried=[PO_DATE, PO_DATE_EXCEL, PO_TYPE] ratios_at_each_level=[0.5177, 0.5177, 0.5177, 0.5177] |
| portal_cka_oklahoma_open_da_ce3cc11024 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.4752 dims_tried=[PO_DATE, PO_DATE_EXCEL] ratios_at_each_level=[0.4752, 0.4752, 0.4752] |
| portal_cka_oklahoma_open_da_dd9095a39b | not-unique-after-dimension-search | base=VOUCHER_ID key_ratio=0.8317 dims_tried=[VOUCHER_ID_RELATED, PROJECT_ID, PO_ID] ratios_at_each_level=[0.8317, 0.8317, 0.8317, 0.8317] |
| portal_cka_oklahoma_open_da_de6ee9058e | not-unique-after-dimension-search | base=PO_ID key_ratio=0.5601 dims_tried=[PO_DATE, PO_DATE_EXCEL, PO_TYPE] ratios_at_each_level=[0.5601, 0.5601, 0.5601, 0.5601] |
| portal_cka_oklahoma_open_da_e1aa111c19 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_e7e7a9c70c | not-unique-after-dimension-search | base=PO_ID key_ratio=0.3988 dims_tried=[REQUISITION_ID, PO_DATE, REQUISITION_DATE] ratios_at_each_level=[0.3988, 0.5102, 0.5102, 0.5102] |
| portal_cka_oklahoma_open_da_f095948ac7 | not-unique-after-dimension-search | base=PO_ID key_ratio=0.4017 dims_tried=[REQUISITION_ID, PO_DATE, PO_DATE_EXCEL] ratios_at_each_level=[0.4017, 0.5218, 0.5218, 0.5218] |
| portal_cka_oklahoma_open_da_f394b50b84 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_fe586f412b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_oklahoma_open_da_fff97e32ba | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_146ebe0cc0 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_18a877ddc9 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_33003c2e61 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_33173c8f40 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_4b1a24aa85 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_529bdbcd10 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_60379efd4f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_650a56f29c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_6b3408d74f | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.0002 dims_tried=[REPORT_DATE, REPORT_MONTH, REPORT_ID] ratios_at_each_level=[0.0002, 0.6739, 0.2199, 0.2199, 0.6739] |
| portal_cka_open_data_sa_6ce5e8b218 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_6d1b83ac0a | not-unique-after-dimension-search | base=SHAPE__LENGTH key_ratio=0.6174 dims_tried=[DATE_FOUNDED, STATUS] ratios_at_each_level=[0.6174, 0.6783, 0.7217] |
| portal_cka_open_data_sa_6fd1bd1867 | not-unique-after-dimension-search | base=SHAPE__LENGTH key_ratio=0.9647 dims_tried=[STATUS] ratios_at_each_level=[0.9647, 0.9647] |
| portal_cka_open_data_sa_7073b94b84 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_721bebb7df | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_75596f44e9 | not-unique-after-dimension-search | base=SHAPE__LENGTH key_ratio=0.9429 dims_tried=[TYPE] ratios_at_each_level=[0.9429, 0.9429] |
| portal_cka_open_data_sa_7cbc348f9d | not-unique-after-dimension-search | base=SHAPE__LENGTH key_ratio=0.1444 dims_tried=[CONSTRUCTION_START_DATE, CONSTRUCTION_END_DATE, BOND_YEAR] ratios_at_each_level=[0.1444, 0.1455, 0.1455, 0.1455] |
| portal_cka_open_data_sa_8b475b44a2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_a33086054b | not-unique-after-dimension-search | base=ZIP key_ratio=0.4082 dims_tried=[TYPE] ratios_at_each_level=[0.4082, 0.4158] |
| portal_cka_open_data_sa_bc29dffc76 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_d4d6661d85 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_open_data_sa_f128e26a15 | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.7188 dims_tried=[(none found)] ratios_at_each_level=[0.7188] |
| portal_cka_open_data_sa_fbab8e5e1e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_0aae3b04a3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_242d633a81 | not-unique-after-dimension-search | base=LATITUDE key_ratio=0.9024 dims_tried=[(none found)] ratios_at_each_level=[0.9024] |
| portal_cka_san_jose_open_da_2a3b7a30d6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_30d54cbfb9 | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.0959 dims_tried=[STATUS] ratios_at_each_level=[0.0959, 0.0988] |
| portal_cka_san_jose_open_da_32aed231b0 | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.8363 dims_tried=[(none found)] ratios_at_each_level=[0.8363] |
| portal_cka_san_jose_open_da_395812e4d0 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_399cadbc5e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_4218690bb6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_5120c908ca | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.3333 dims_tried=[(none found)] ratios_at_each_level=[0.3333] |
| portal_cka_san_jose_open_da_56e25afe36 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_5c575bfeb9 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_5f864a8799 | not-unique-after-dimension-search | base=LON key_ratio=0.21 dims_tried=[STATUS] ratios_at_each_level=[0.21, 0.21] |
| portal_cka_san_jose_open_da_79010b8e46 | not-unique-after-dimension-search | base=SHAPE_LENGTH key_ratio=0.7979 dims_tried=[PROGRAM] ratios_at_each_level=[0.7979, 0.8004] |
| portal_cka_san_jose_open_da_981e07d5db | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_9a45ef98ee | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.7143 dims_tried=[STATUS] ratios_at_each_level=[0.7143, 0.8571] |
| portal_cka_san_jose_open_da_9e7f660889 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_ae9aa2585e | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.9394 dims_tried=[(none found)] ratios_at_each_level=[0.9394] |
| portal_cka_san_jose_open_da_b5eb095bc3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_b701cda393 | not-unique-after-dimension-search | base=ZIP key_ratio=0.5714 dims_tried=[(none found)] ratios_at_each_level=[0.5714] |
| portal_cka_san_jose_open_da_ba8cf13e13 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_bbe1045a31 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_c9d4859b38 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_d35d991fba | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_d4bf270a36 | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.1957 dims_tried=[STATUS] ratios_at_each_level=[0.1957, 0.2391] |
| portal_cka_san_jose_open_da_d724f2d525 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_ed235b292f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_san_jose_open_da_ef31016039 | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.88 dims_tried=[STATUS] ratios_at_each_level=[0.88, 0.88] |
| portal_cka_san_jose_open_da_f1315a36e0 | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.6823 dims_tried=[(none found)] ratios_at_each_level=[0.6823] |
| portal_cka_san_jose_open_da_f194d54765 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.6262 dims_tried=[YEAR] ratios_at_each_level=[0.6262, 0.727] |
| portal_cka_tampa_open_data_08860f4f6e | not-unique-after-dimension-search | base=ID key_ratio=0.8773 dims_tried=[DATE, PERIOD, CATEGORY] ratios_at_each_level=[0.8773, 0.8773, 0.8773, 0.9618] |
| portal_cka_tampa_open_data_3dae51799d | not-unique-after-dimension-search | base=ID key_ratio=0.1617 dims_tried=[DATE, PERIOD, CATEGORY] ratios_at_each_level=[0.1617, 0.1617, 0.594, 0.8045] |
| portal_cka_tampa_open_data_710a91a2fd | not-unique-after-dimension-search | base=ID key_ratio=0.6149 dims_tried=[DATE, PERIOD, CATEGORY] ratios_at_each_level=[0.6149, 0.6588, 0.6692, 0.6937] |
| portal_cka_virginia_open_da_154b43ed61 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_virginia_open_da_1598ead304 | not-unique-after-dimension-search | base=COUNTY_FIPS key_ratio=0.0001 dims_tried=[REPORT_DATE, WEEK_ENDING_DATE, YEAR] ratios_at_each_level=[0.0001, 0.0001, 0.0338, 0.0338] |
| portal_cka_virginia_open_da_1f3259d1c8 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_virginia_open_da_39c6e329f1 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_virginia_open_da_4e05a500e2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_virginia_open_da_5ab7cd31bf | not-unique-after-dimension-search | base=FIPS key_ratio=0.0341 dims_tried=[YEAR, GEOGRAPHY_LEVEL] ratios_at_each_level=[0.0341, 0.0681, 0.0684] |
| portal_cka_virginia_open_da_6207bdeb36 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_virginia_open_da_68afe3ae03 | not-unique-after-dimension-search | base=FIPS key_ratio=0.0174 dims_tried=[REPORT_DATE] ratios_at_each_level=[0.0174, 0.0522] |
| portal_cka_virginia_open_da_803d29bfe0 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_virginia_open_da_8a70de2fb1 | not-unique-after-dimension-search | base=CITY_STATE_ZIP key_ratio=0.0188 dims_tried=[TAX_YEAR] ratios_at_each_level=[0.0188, 0.0607] |
| portal_cka_virginia_open_da_9eb4920327 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.4028 dims_tried=[CREATED_DATE, LAST_EDITED_DATE, VDOT_RECEIVED_DATE, PROJECT_ID, MASTER_ID, LOCAL_PROJECT_ID, PROJECT_GROUP_ID, PARCEL_ID] ratios_at_each_level=[0.4028, 0.7639, 0.75, 0.4722, 0.1389, 0.1806, 0.4028, 0.4028, 0.75, 0.7639] |
| portal_cka_virginia_open_da_a1b2888c0a | not-unique-after-dimension-search | base=FAC_ID key_ratio=0.8919 dims_tried=[DATE_JOINED, VEEP_LEVEL, MEMBER_TYPE] ratios_at_each_level=[0.8919, 0.8919, 0.971, 0.971] |
| portal_cka_virginia_open_da_a7663008d7 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.4797 dims_tried=[CREATED_DATE, LAST_EDITED_DATE, VDOT_RECEIVED_DATE, PROJECT_ID, MASTER_ID, LOCAL_PROJECT_ID, PROJECT_GROUP_ID, PARCEL_ID] ratios_at_each_level=[0.4797, 0.965, 0.9537, 0.8524, 0.1126, 0.2951, 0.4797, 0.4797, 0.7923, 0.9661] |
| portal_cka_virginia_open_da_b3a21c711b | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.1769 dims_tried=[CREATED_DATE, LAST_EDITED_DATE, VDOT_RECEIVED_DATE, PROJECT_ID, MASTER_ID, LOCAL_PROJECT_ID, PROJECT_GROUP_ID, PARCEL_ID] ratios_at_each_level=[0.1769, 0.9724, 0.9708, 0.664, 0.0698, 0.3896, 0.1769, 0.1769, 0.724, 0.9724] |
| portal_cka_virginia_open_da_c06203327d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_virginia_open_da_cc1870e66b | not-unique-after-dimension-search | base=ZONE_ID key_ratio=0.0043 dims_tried=[DATE_OCCURRED, DATE_FOUND, OFFENSE_CODE] ratios_at_each_level=[0.0043, 0.9111, 0.9125, 0.9302] |
| portal_cka_virginia_open_da_d5d649203d | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.0016 dims_tried=[ADDRESS_CLASS, ADDRESS_CLASS_DESCRIPTION] ratios_at_each_level=[0.0016, 0.0026, 0.0026] |
| portal_cka_virginia_open_da_e3c86f8b93 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_virginia_open_da_f11e52d4b6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_03fa5ab0c2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_073e47dfba | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.0461 dims_tried=[DATE, PROGRAM, PROGRAM_CATEGORY] ratios_at_each_level=[0.0461, 0.8394, 0.9514, 0.9514] |
| portal_cka_western_pennsylv_09ab742fe8 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_130e50e683 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_1a5ddb6efa | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_1a8329b111 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_203ec904cd | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.625 dims_tried=[TYPE] ratios_at_each_level=[0.625, 0.9375] |
| portal_cka_western_pennsylv_2350d74335 | not-unique-after-dimension-search | base=ZIP key_ratio=0.913 dims_tried=[(none found)] ratios_at_each_level=[0.913] |
| portal_cka_western_pennsylv_2aa69e6971 | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.3597 dims_tried=[CLASS] ratios_at_each_level=[0.3597, 0.5257] |
| portal_cka_western_pennsylv_2c24d9b40b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_2deaa849e4 | not-unique-after-dimension-search | base=R_ZIP key_ratio=0.0106 dims_tried=[EDIT_DATE, ST_TYPE, SOURCE_ID] ratios_at_each_level=[0.0106, 0.0011, 0.2734, 0.3215, 0.3224] |
| portal_cka_western_pennsylv_322fdf0e2e | not-unique-after-dimension-search | base=LONGITUDE_STR key_ratio=0.0278 dims_tried=[(none found)] ratios_at_each_level=[0.0278] |
| portal_cka_western_pennsylv_34dd959083 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_3782283d39 | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.0588 dims_tried=[(none found)] ratios_at_each_level=[0.0588] |
| portal_cka_western_pennsylv_38f78ba9e4 | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.0435 dims_tried=[(none found)] ratios_at_each_level=[0.0435] |
| portal_cka_western_pennsylv_3bc0395530 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_4070ff54be | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_42719841f1 | not-unique-after-dimension-search | base=ARRESTPERSON_ID key_ratio=0.3523 dims_tried=[ARREST_DATE, ARREST_YEAR, ARREST_MONTH] ratios_at_each_level=[0.3523, 0.3542, 0.3542, 0.3542] |
| portal_cka_western_pennsylv_57184a8fe4 | not-unique-after-dimension-search | base=STATEFP key_ratio=0.0025 dims_tried=[(none found)] ratios_at_each_level=[0.0025] |
| portal_cka_western_pennsylv_5c8bba2d74 | not-unique-after-dimension-search | base=COUNTYFP key_ratio=0.0067 dims_tried=[(none found)] ratios_at_each_level=[0.0067] |
| portal_cka_western_pennsylv_64295c4f58 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_6498507aef | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_6519eacd82 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_6d0f07679b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_6f8489e18f | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.5445 dims_tried=[YEAR, MONTH] ratios_at_each_level=[0.5445, 0.7469, 0.8479] |
| portal_cka_western_pennsylv_700a3671cd | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.2 dims_tried=[(none found)] ratios_at_each_level=[0.2] |
| portal_cka_western_pennsylv_7c5012db2a | not-unique-after-dimension-search | base=LONGITUDE_STR key_ratio=0.0028 dims_tried=[DATE_OF_PREDICTION, AQI_TYPE] ratios_at_each_level=[0.0028, 0.0028, 0.0111] |
| portal_cka_western_pennsylv_a1b3bc6c07 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_a58cf00a10 | not-unique-after-dimension-search | base=ZIP key_ratio=0.7222 dims_tried=[(none found)] ratios_at_each_level=[0.7222] |
| portal_cka_western_pennsylv_abefc58c3e | not-unique-after-dimension-search | base=CASE_ID key_ratio=0.8544 dims_tried=[FILING_DATE, PARTY_TYPE] ratios_at_each_level=[0.8544, 0.8544, 0.8544] |
| portal_cka_western_pennsylv_b26184ed51 | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.2458 dims_tried=[(none found)] ratios_at_each_level=[0.2458] |
| portal_cka_western_pennsylv_b81b12d211 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.6055 dims_tried=[INCIDENT_TYPE, TYPE_DESCRIPTION] ratios_at_each_level=[0.6055, 0.7875, 0.7876] |
| portal_cka_western_pennsylv_bd609b0793 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_c0a2a6745a | not-unique-after-dimension-search | base=DOCKET_TYPE key_ratio=0.0114 dims_tried=[FILING_DATE, CASE_ID] ratios_at_each_level=[0.0114, 0.9483, 0.4171, 0.9483] |
| portal_cka_western_pennsylv_d078e6f18c | not-unique-after-dimension-search | base=USER_ZIPCODE key_ratio=0.0739 dims_tried=[(none found)] ratios_at_each_level=[0.0739] |
| portal_cka_western_pennsylv_d0e4884ea3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_d654695651 | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.0149 dims_tried=[REQUEST_DATE, REQUEST_TYPE, PROPERTY_TYPE] ratios_at_each_level=[0.0149, 0.6532, 0.7946, 0.8255] |
| portal_cka_western_pennsylv_db88bde311 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_dce73f8efa | not-unique-after-dimension-search | base=FIPS key_ratio=0.8012 dims_tried=[TYPE, CNTL_ID] ratios_at_each_level=[0.8012, 0.7764, 0.8075, 0.8075] |
| portal_cka_western_pennsylv_ed5f10964e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_f1230a63da | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_f5fb6ccb69 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_western_pennsylv_f9c1429ab4 | not-unique-after-dimension-search | base=LOCATION_ZIP_CODE key_ratio=0.2059 dims_tried=[CATEGORY] ratios_at_each_level=[0.2059, 0.4542] |
| portal_cka_wprdc_allegheny_060112d129 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_0ce6cd67aa | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_12918a9a0a | not-unique-after-dimension-search | base=STATEFP key_ratio=0.0025 dims_tried=[(none found)] ratios_at_each_level=[0.0025] |
| portal_cka_wprdc_allegheny_145b5f2466 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.6055 dims_tried=[INCIDENT_TYPE, TYPE_DESCRIPTION] ratios_at_each_level=[0.6055, 0.7875, 0.7876] |
| portal_cka_wprdc_allegheny_1d9621e88d | not-unique-after-dimension-search | base=ZIP key_ratio=0.913 dims_tried=[(none found)] ratios_at_each_level=[0.913] |
| portal_cka_wprdc_allegheny_238d230c29 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_27d8bf386d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_29d102482d | not-unique-after-dimension-search | base=USER_ZIPCODE key_ratio=0.0739 dims_tried=[(none found)] ratios_at_each_level=[0.0739] |
| portal_cka_wprdc_allegheny_2d99f866d7 | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.2458 dims_tried=[(none found)] ratios_at_each_level=[0.2458] |
| portal_cka_wprdc_allegheny_316a5acd77 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_31d26600c9 | not-unique-after-dimension-search | base=DOCKET_TYPE key_ratio=0.0114 dims_tried=[FILING_DATE, CASE_ID] ratios_at_each_level=[0.0114, 0.9483, 0.4171, 0.9483] |
| portal_cka_wprdc_allegheny_3ac597333e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_3b5f278b80 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_46c43d5623 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_4e99637062 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_4fc34000ce | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_5163016c30 | not-unique-after-dimension-search | base=LOCATION_ZIP_CODE key_ratio=0.2059 dims_tried=[CATEGORY] ratios_at_each_level=[0.2059, 0.4542] |
| portal_cka_wprdc_allegheny_52a0e51aca | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_55c0e96166 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_5c03b21365 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_615c42bb56 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_65d88e2bef | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.5445 dims_tried=[YEAR, MONTH] ratios_at_each_level=[0.5445, 0.7469, 0.8479] |
| portal_cka_wprdc_allegheny_8824deaa23 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_886bd5e998 | not-unique-after-dimension-search | base=COUNTYFP key_ratio=0.0067 dims_tried=[(none found)] ratios_at_each_level=[0.0067] |
| portal_cka_wprdc_allegheny_8dde33b4be | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.3597 dims_tried=[CLASS] ratios_at_each_level=[0.3597, 0.5257] |
| portal_cka_wprdc_allegheny_8f9481cfa8 | not-unique-after-dimension-search | base=LONGITUDE_STR key_ratio=0.0028 dims_tried=[DATE_OF_PREDICTION, AQI_TYPE] ratios_at_each_level=[0.0028, 0.0028, 0.0111] |
| portal_cka_wprdc_allegheny_90e172f9b4 | not-unique-after-dimension-search | base=ARRESTPERSON_ID key_ratio=0.3523 dims_tried=[ARREST_DATE, ARREST_YEAR, ARREST_MONTH] ratios_at_each_level=[0.3523, 0.3542, 0.3542, 0.3542] |
| portal_cka_wprdc_allegheny_98b94025ac | not-unique-after-dimension-search | base=ZIP_CODE key_ratio=0.0149 dims_tried=[REQUEST_DATE, REQUEST_TYPE, PROPERTY_TYPE] ratios_at_each_level=[0.0149, 0.6532, 0.7946, 0.8255] |
| portal_cka_wprdc_allegheny_a515b81ddf | not-unique-after-dimension-search | base=R_ZIP key_ratio=0.0106 dims_tried=[EDIT_DATE, ST_TYPE, SOURCE_ID] ratios_at_each_level=[0.0106, 0.0011, 0.2734, 0.3215, 0.3224] |
| portal_cka_wprdc_allegheny_a6b2e0c749 | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.2 dims_tried=[(none found)] ratios_at_each_level=[0.2] |
| portal_cka_wprdc_allegheny_b10f4b5c32 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_b497c35747 | not-unique-after-dimension-search | base=LONGITUDE key_ratio=0.0461 dims_tried=[DATE, PROGRAM, PROGRAM_CATEGORY] ratios_at_each_level=[0.0461, 0.8394, 0.9514, 0.9514] |
| portal_cka_wprdc_allegheny_ba92a76441 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_c12ac76e17 | not-unique-after-dimension-search | base=ZIP key_ratio=0.7222 dims_tried=[(none found)] ratios_at_each_level=[0.7222] |
| portal_cka_wprdc_allegheny_c947d54b10 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_d0168f8de5 | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.0588 dims_tried=[(none found)] ratios_at_each_level=[0.0588] |
| portal_cka_wprdc_allegheny_ea2ee5f5ad | not-unique-after-dimension-search | base=ZIPCODE key_ratio=0.625 dims_tried=[TYPE] ratios_at_each_level=[0.625, 0.9375] |
| portal_cka_wprdc_allegheny_eec7410b74 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_cka_wprdc_allegheny_f38f393b45 | not-unique-after-dimension-search | base=FIPS key_ratio=0.8012 dims_tried=[TYPE, CNTL_ID] ratios_at_each_level=[0.8012, 0.7764, 0.8075, 0.8075] |
| portal_cka_wprdc_allegheny_f60a9edcbd | not-unique-after-dimension-search | base=LONGITUDE_STR key_ratio=0.0278 dims_tried=[(none found)] ratios_at_each_level=[0.0278] |
| portal_cka_wprdc_allegheny_f727ac582e | not-unique-after-dimension-search | base=CASE_ID key_ratio=0.8544 dims_tried=[FILING_DATE, PARTY_TYPE] ratios_at_each_level=[0.8544, 0.8544, 0.8544] |
| portal_cka_wprdc_allegheny_f878f4aa8a | not-unique-after-dimension-search | base=SHAPE_AREA key_ratio=0.0435 dims_tried=[(none found)] ratios_at_each_level=[0.0435] |
| portal_cka_wprdc_allegheny_f891a6d2ee | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_austin_open_data_b5e56c7a67 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_cambridge_open_d_d1389afe1e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_chicago_data_por_1719dae821 | not-unique-after-dimension-search | base=DOCKET_NO key_ratio=0.4995 dims_tried=[VIOLATION_DATE, STREET_TYPE, CASE_TYPE] ratios_at_each_level=[0.4995, 0.5555, 0.5695, 0.5695] |
| portal_soc_chicago_data_por_1ca267a903 | not-unique-after-dimension-search | base=ZIP key_ratio=0.917 dims_tried=[TYPE_OF_FILER] ratios_at_each_level=[0.917, 0.9195] |
| portal_soc_chicago_data_por_51304d7360 | not-unique-after-dimension-search | base=DOCKET_NUMBER key_ratio=0.9245 dims_tried=[ISSUED_DATE, LAST_HEARING_DATE, VIOLATION_TYPE] ratios_at_each_level=[0.9245, 0.9245, 0.9245, 0.961] |
| portal_soc_chicago_data_por_fc19b9a2be | not-unique-after-dimension-search | base=ZIP key_ratio=0.0818 dims_tried=[CLASS, SCHOOL_TYPE, S_TYPE, ISBE_ID] ratios_at_each_level=[0.0818, 0.8586, 0.1176, 0.1875, 0.2054, 0.9613] |
| portal_soc_colombia_nationa_3c8f38b720 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_colombia_nationa_95d4789ba7 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_colorado_informa_0637be3aac | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_colorado_informa_1cf33fb763 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_colorado_informa_4844ca967d | not-unique-after-dimension-search | base=ZIP key_ratio=0.2222 dims_tried=[(none found)] ratios_at_each_level=[0.2222] |
| portal_soc_colorado_informa_502999772d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_colorado_informa_6be19a7323 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_colorado_informa_9224cc38d4 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_colorado_informa_9a760aefaa | not-unique-after-dimension-search | base=ZIP key_ratio=0.1243 dims_tried=[YEAR, CLASSIFICATION] ratios_at_each_level=[0.1243, 0.1243, 0.2131] |
| portal_soc_colorado_informa_c4d7351098 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_connecticut_open_1cd7311280 | not-unique-after-dimension-search | base=DOCKET_OR_PETITION_NUM key_ratio=0.0816 dims_tried=[TWR_TYPE, BACKUP_POWER_TYPE] ratios_at_each_level=[0.0816, 0.0934, 0.1115] |
| portal_soc_connecticut_open_28f32b559b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_connecticut_open_421e7f6a7e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_connecticut_open_55ff4e7ba7 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_connecticut_open_6cdd9e3a6e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_connecticut_open_7909c84ee4 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_connecticut_open_886aef6ac6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_connecticut_open_95ac60cee1 | not-unique-after-dimension-search | base=PATENT_NO key_ratio=0.8294 dims_tried=[CLASS] ratios_at_each_level=[0.8294, 0.8449] |
| portal_soc_connecticut_open_9a34cd28ae | not-unique-after-dimension-search | base=CCN key_ratio=0.015 dims_tried=[HOSPITAL_SUBTYPE, FIPS_CODE, HHS_ID] ratios_at_each_level=[0.015, 0.015, 0.015, 0.015, 0.015] |
| portal_soc_connecticut_open_b2b9303a5f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_connecticut_open_bd88772b17 | not-unique-after-dimension-search | base=HOST_ZIP key_ratio=0.1741 dims_tried=[VINTAGE_MSA_AMI_BAND, VINTAGE_MSA_SMI_BAND, VINTAGE_MSA_CRA_AMI_BAND] ratios_at_each_level=[0.1741, 0.3489, 0.3643, 0.3884] |
| portal_soc_connecticut_open_f42eda9b76 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_datala_los_angel_a94a3a65bd | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_delaware_open_da_98a9ee0bc7 | not-unique-after-dimension-search | base=DUNS_NUM key_ratio=0.3912 dims_tried=[AGENCY_TYPE, RESOURCE_TYPE, TECHNOLOGY_TYPE] ratios_at_each_level=[0.3912, 0.3951, 0.4215, 0.4312] |
| portal_soc_delaware_open_da_9e200409c5 | not-unique-after-dimension-search | base=FAC_ZIP key_ratio=0.0205 dims_tried=[(none found)] ratios_at_each_level=[0.0205] |
| portal_soc_delaware_open_da_d15606cf5c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_delaware_open_da_eb5f15ed0e | not-unique-after-dimension-search | base=DOCKET_NO key_ratio=0.8806 dims_tried=[ISSUE_DATE, STATUS] ratios_at_each_level=[0.8806, 0.8955, 0.9104] |
| portal_soc_maryland_open_da_1b2cc0adb9 | not-unique-after-dimension-search | base=CCN key_ratio=0.9531 dims_tried=[TYPE] ratios_at_each_level=[0.9531, 0.9688] |
| portal_soc_maryland_open_da_786470e96f | not-unique-after-dimension-search | base=FDMS_DOCKET_ID key_ratio=0.0361 dims_tried=[SIP_DUE_DATE, SUBMITTAL_DATE, LATEST_COMPLETENESS_DATE] ratios_at_each_level=[0.0361, 0.0722, 0.0979, 0.1082] |
| portal_soc_maryland_open_da_7ce817c5ce | not-unique-after-dimension-search | base=CCN key_ratio=0.9531 dims_tried=[TYPE] ratios_at_each_level=[0.9531, 0.9688] |
| portal_soc_maryland_open_da_8eed7b8121 | not-unique-after-dimension-search | base=FDMS_DOCKET_ID key_ratio=0.0151 dims_tried=[SIP_DUE_DATE, SUBMITTAL_DATE, LATEST_COMPLETENESS_DATE] ratios_at_each_level=[0.0151, 0.0635, 0.1316, 0.1513] |
| portal_soc_maryland_open_da_baa13fc4ec | not-unique-after-dimension-search | base=ZIP key_ratio=0.1102 dims_tried=[FISCAL_YEAR, PROGRAM_NAME_LEVEL_ONE, PROGRAM_NAME_LEVEL_TWO] ratios_at_each_level=[0.1102, 0.335, 0.4652, 0.4692] |
| portal_soc_maryland_open_da_d9d09ef11b | not-unique-after-dimension-search | base=FDMS_DOCKET_ID key_ratio=0.0123 dims_tried=[SIP_DUE_DATE, SUBMITTAL_DATE, LATEST_COMPLETENESS_DATE] ratios_at_each_level=[0.0123, 0.0688, 0.1155, 0.1302] |
| portal_soc_mesa_city_data_h_1d5c4ed269 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_new_york_state_o_153df2db81 | not-unique-after-dimension-search | base=FACILITY_ZIP key_ratio=0.3753 dims_tried=[REPORTING_START_DATE, REPORTING_END_DATE, ORGANIZATION_TYPE, PARENT_BODY_ID, FACILITY_ID] ratios_at_each_level=[0.3753, 0.1368, 0.726, 0.5661, 0.5892, 0.6087, 0.7375] |
| portal_soc_new_york_state_o_1c387b0ae6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_new_york_state_o_4a5291be83 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_new_york_state_o_7b6eacd070 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_new_york_state_o_7dd1c9cb24 | not-unique-after-dimension-search | base=DUNS_NUMBER key_ratio=0.6366 dims_tried=[CONTRACT_EXECUTION_DATE, CONTRACT_END_DATE] ratios_at_each_level=[0.6366, 0.9637, 0.9731] |
| portal_soc_new_york_state_o_9bb5326481 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_new_york_state_o_a677772945 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_new_york_state_o_df2d96a77f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_nj_open_data_cen_a0d94510ca | not-unique-after-dimension-search | base=NPI_NUMBER key_ratio=0.249 dims_tried=[EFFECTIVE_DATE, EXPIRATION_DATE] ratios_at_each_level=[0.249, 0.677, 0.7125] |
| portal_soc_open_data_br_21bb19a94a | not-unique-after-dimension-search | base=ZIP key_ratio=0.012 dims_tried=[BUSINESS_NAICS_CODE] ratios_at_each_level=[0.012, 0.4555] |
| portal_soc_open_data_br_b141e1c0f8 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0015 dims_tried=[BUSINESS_NAICS_CODE, BLOCK_GROUP, ZONING_TYPE, LOT_ID] ratios_at_each_level=[0.0015, 0.9305, 0.023, 0.028, 0.051, 0.9645] |
| portal_soc_open_data_br_fc0d2daa2b | not-unique-after-dimension-search | base=ZIP key_ratio=0.0115 dims_tried=[MODIFIED_DATE, CREATED_DATE, ST_SUFFIX_TYPE] ratios_at_each_level=[0.0115, 0.3437, 0.3562, 0.4582] |
| portal_soc_oregon_open_data_072d0c4a94 | not-unique-after-dimension-search | base=EMPLOYER_ZIP_CODE key_ratio=0.0535 dims_tried=[CLAIM_REFERENCE_YEAR, DATE_OF_INJURY, OCCUPATION_CODE] ratios_at_each_level=[0.0535, 0.257, 0.5465, 0.7795] |
| portal_soc_oregon_open_data_dc4aee7db0 | not-unique-after-dimension-search | base=MAIL_ZIP_4 key_ratio=0.845 dims_tried=[INSURER_STATUS_DATE, LIAB_BEGIN_DATE, LIAD_END_DATE] ratios_at_each_level=[0.845, 0.979, 0.9795, 0.9795] |
| portal_soc_oregon_open_data_e338c547c2 | not-unique-after-dimension-search | base=GASO_NPI key_ratio=0.013 dims_tried=[RECORDED_DATE, EFFECTIVE_DATE, ZIP_CODE] ratios_at_each_level=[0.013, 0.0135, 0.0135, 0.1085] |
| portal_soc_pa_open_data_por_5a9f04bb9c | not-unique-after-dimension-search | base=ZIP key_ratio=0.0105 dims_tried=[RECEIVE_DATE, CERT_SIGNED_DATE, RHEE_START_DATE, HANDLER_ID, HD_CERTIFICATION_ID, HD_EPISODIC_EVENT_ID, HD_EPISODIC_WASTE_ID, HD_EPISODIC_WASTE_CODE_ID, HD_OWNEROP_ID, HD_WASTE_CODE_ID] ratios_at_each_level=[0.0105, 0.0076, 0.0099, 0.0082, 0.0117, 0.0432, 0.0158, 0.0666, 0.0117, 0.0129, 0.0129, 0.9603] |
| portal_soc_pa_open_data_por_7d4f8fce94 | not-unique-after-dimension-search | base=COUNTY_FIPS key_ratio=0.0476 dims_tried=[CALENDAR_YEAR, COUNTY_CODE] ratios_at_each_level=[0.0476, 0.0476, 0.0476] |
| portal_soc_pa_open_data_por_84400dc75d | not-unique-after-dimension-search | base=COUNTY_FIPS key_ratio=0.034 dims_tried=[CALENDAR_QUARTER, COUNTY_CODE] ratios_at_each_level=[0.034, 0.048, 0.048] |
| portal_soc_pa_open_data_por_cd66682741 | not-unique-after-dimension-search | base=CCN key_ratio=0.0935 dims_tried=[HOSPITAL_SUBTYPE, FIPS_CODE] ratios_at_each_level=[0.0935, 0.0935, 0.0935] |
| portal_soc_texas_open_data_31f82d63f8 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_texas_open_data_38b5253053 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_texas_open_data_4d3a5eed0f | not-unique-after-dimension-search | base=LOC_ZIP key_ratio=0.1425 dims_tried=[RESP_BEGIN_DATE, OUT_OF_BUSINESS_DATE] ratios_at_each_level=[0.1425, 0.2555, 0.261] |
| portal_soc_texas_open_data_5a5338f21b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_texas_open_data_91f1c8d27d | not-unique-after-dimension-search | base=ASSOCIATED_LICENSEE_EIN key_ratio=0.4395 dims_tried=[ASSOCIATION_BEGIN_DATE, ASSOCIATION_TYPE, ASSOCIATED_LICENSEE_NAIC_ID] ratios_at_each_level=[0.4395, 0.0225, 0.911, 0.929, 0.929] |
| portal_soc_texas_open_data_a124dc2a11 | not-unique-after-dimension-search | base=SCHOOL_ZIP key_ratio=0.512 dims_tried=[UPDATE_DATE, SCHOOL_STATUS_DATE, DISTRICT_TYPE] ratios_at_each_level=[0.512, 0.5305, 0.8455, 0.8455] |
| portal_soc_texas_open_data_a7ab49cb1a | not-unique-after-dimension-search | base=NPI key_ratio=0.6242 dims_tried=[YEAR, DATE_SUBMITTED] ratios_at_each_level=[0.6242, 0.868, 0.8837] |
| portal_soc_texas_open_data_b8ddc96bff | not-unique-after-dimension-search | base=UEI key_ratio=0.594 dims_tried=[PROGRAM] ratios_at_each_level=[0.594, 0.594] |
| portal_soc_texas_open_data_d1849939bc | not-unique-after-dimension-search | base=DOCKET_NUMBER key_ratio=0.8728 dims_tried=[SIGNED_DATE, ORDER_TYPE, ORDER_SUB_TYPE] ratios_at_each_level=[0.8728, 0.9033, 0.9033, 0.9135] |
| portal_soc_texas_open_data_eadc02d661 | not-unique-after-dimension-search | base=INSURED_EMPLOYER_ZIP_EXTENTION key_ratio=0.4568 dims_tried=[POLICY_EFFECTIVE_DATE, POLICY_EXPIRATION_DATE, CANCELLATION_EFFECTIVE_DATE, NCCI_COVERAGE_PROVIDER_ID] ratios_at_each_level=[0.4568, 0.0005, 0.4568, 0.4573, 0.4588, 0.4588] |
| portal_soc_utah_open_data_p_0028f23236 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_0844d0bd12 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0775 dims_tried=[(none found)] ratios_at_each_level=[0.0775] |
| portal_soc_utah_open_data_p_08ba00868c | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_0f31165e86 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_124ad2a7e9 | not-unique-after-dimension-search | base=ZIP key_ratio=0.4336 dims_tried=[OWNERSHIP] ratios_at_each_level=[0.4336, 0.4386] |
| portal_soc_utah_open_data_p_18582ddc54 | not-unique-after-dimension-search | base=PATENT_NBR key_ratio=0.6165 dims_tried=[CLASS, LOT_TYPE_CD, SOLD_STATUS_DESCR] ratios_at_each_level=[0.6165, 0.6165, 0.619, 0.6205] |
| portal_soc_utah_open_data_p_193d6feec1 | not-unique-after-dimension-search | base=GEO_ID key_ratio=0.023 dims_tried=[YEAR_ID] ratios_at_each_level=[0.023, 0.0345] |
| portal_soc_utah_open_data_p_1a3ede9cad | not-unique-after-dimension-search | base=NPI key_ratio=0.0809 dims_tried=[(none found)] ratios_at_each_level=[0.0809] |
| portal_soc_utah_open_data_p_1c0c156da7 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_1e3f70c6a8 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_2027b55eda | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.2914 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.2914, 0.9238, 0.9238, 0.939] |
| portal_soc_utah_open_data_p_2065ce1d57 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_21e87270e6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_266d3fb7bf | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_267abee380 | not-unique-after-dimension-search | base=ZIP key_ratio=0.0887 dims_tried=[FISCAL_YEAR, TAX_ID] ratios_at_each_level=[0.0887, 0.5435, 0.2476, 0.9473] |
| portal_soc_utah_open_data_p_275cd55e37 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_27f4752a1b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_2853122765 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_294fe280ef | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_2f94947455 | not-unique-after-dimension-search | base=PATENT_NR key_ratio=0.2595 dims_tried=[CREATE_DATE, MODIFY_DATE, STATUS] ratios_at_each_level=[0.2595, 0.262, 0.266, 0.2685] |
| portal_soc_utah_open_data_p_2fdf78bd22 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_327d0e821d | not-unique-after-dimension-search | base=ZIP key_ratio=0.6505 dims_tried=[OWNERSHIP] ratios_at_each_level=[0.6505, 0.66] |
| portal_soc_utah_open_data_p_3345d79e51 | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.039 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.039, 0.1282, 0.9286, 0.9286] |
| portal_soc_utah_open_data_p_36be408253 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_37575ad872 | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.2826 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.2826, 0.9445, 0.9445, 0.9535] |
| portal_soc_utah_open_data_p_376293fcf7 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_37975584a8 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_3967e73a16 | not-unique-after-dimension-search | base=PATENT_NBR key_ratio=0.618 dims_tried=[CLASS, LOT_TYPE_CD, SOLD_STATUS_DESCR] ratios_at_each_level=[0.618, 0.618, 0.621, 0.6225] |
| portal_soc_utah_open_data_p_3ccc1d14ac | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_42ca38b0b0 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_447082e18e | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_47dcffc8c1 | not-unique-after-dimension-search | base=SHAPE_LENG key_ratio=0.9286 dims_tried=[EDIT_DATE, DA_DATE, CLASS] ratios_at_each_level=[0.9286, 0.9286, 0.9286, 0.9286] |
| portal_soc_utah_open_data_p_49602baec5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_4ad0b626c8 | not-unique-after-dimension-search | base=ZIP key_ratio=0.6348 dims_tried=[OWNERSHIP] ratios_at_each_level=[0.6348, 0.6564] |
| portal_soc_utah_open_data_p_4b47fccae8 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_4c3c656c61 | not-unique-after-dimension-search | base=PATENT_NBR key_ratio=0.513 dims_tried=[CLASS, PROCESS_STATUS] ratios_at_each_level=[0.513, 0.516, 0.518] |
| portal_soc_utah_open_data_p_4da2a1e62f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_4dde6e2c89 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_4ed1b6ffa6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_4fe1d49f45 | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.2714 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.2714, 0.9052, 0.9052, 0.9201] |
| portal_soc_utah_open_data_p_50b9839dcd | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_51f192b9ac | not-unique-after-dimension-search | base=GEO_ID key_ratio=0.0202 dims_tried=[YEAR_ID] ratios_at_each_level=[0.0202, 0.0303] |
| portal_soc_utah_open_data_p_52003d36f8 | not-unique-after-dimension-search | base=NPI key_ratio=0.187 dims_tried=[OFFICE_VISIT_TYPE, POS_CATEGORY] ratios_at_each_level=[0.187, 0.3375, 0.3775] |
| portal_soc_utah_open_data_p_55b6e45f3f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_5822aaee01 | not-unique-after-dimension-search | base=PATENT_NR key_ratio=0.2595 dims_tried=[CREATE_DATE, MODIFY_DATE, STATUS] ratios_at_each_level=[0.2595, 0.262, 0.266, 0.2685] |
| portal_soc_utah_open_data_p_58a8494eea | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_598c279750 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_598e83da4d | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.276 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.276, 0.9036, 0.9036, 0.9149] |
| portal_soc_utah_open_data_p_59e244e1cc | not-unique-after-dimension-search | base=ZIP key_ratio=0.5368 dims_tried=[OWNERSHIP] ratios_at_each_level=[0.5368, 0.5474] |
| portal_soc_utah_open_data_p_5a037856fe | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_5d4caad7fb | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_5e52f5d62f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_5ef25af42c | not-unique-after-dimension-search | base=IMPUTED_PROVIDER_NPI key_ratio=0.1285 dims_tried=[REPORTING_PERIOD, CI_MEASURE_ID] ratios_at_each_level=[0.1285, 0.006, 0.1285, 0.788] |
| portal_soc_utah_open_data_p_617eba9cd6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_6223211050 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_623dbee2ef | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_62bb6c079e | not-unique-after-dimension-search | base=REFERRING_NPI key_ratio=0.1985 dims_tried=[REFERRING_ENTITY_CODE, REFERRING_PROVIDER_TYPE, REFERRING_PROVIDER_TYPE_FLAG] ratios_at_each_level=[0.1985, 0.1985, 0.1985, 0.1985] |
| portal_soc_utah_open_data_p_6319d859b5 | not-unique-after-dimension-search | base=FAC_ZIP key_ratio=0.1566 dims_tried=[(none found)] ratios_at_each_level=[0.1566] |
| portal_soc_utah_open_data_p_645b93d1c3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_6679f2dedb | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_6862b465d5 | not-unique-after-dimension-search | base=PRIME_AWARDEE_DUNS key_ratio=0.1105 dims_tried=[SUBAWARD_ACTION_DATE, SUBAWARD_REPORT_YEAR, SUBAWARD_REPORT_MONTH] ratios_at_each_level=[0.1105, 0.5619, 0.6049, 0.6676] |
| portal_soc_utah_open_data_p_6deee0bf03 | not-unique-after-dimension-search | base=WORKSITE_POSTAL_CODE key_ratio=0.1492 dims_tried=[RECEIVED_DATE, DECISION_DATE, BEGIN_DATE] ratios_at_each_level=[0.1492, 0.7815, 0.8092, 0.885] |
| portal_soc_utah_open_data_p_6e687d44e0 | not-unique-after-dimension-search | base=PATENT_NBR key_ratio=0.51 dims_tried=[CLASS, PROCESS_STATUS] ratios_at_each_level=[0.51, 0.513, 0.5155] |
| portal_soc_utah_open_data_p_6f316de0b0 | not-unique-after-dimension-search | base=BILLING_NPI key_ratio=0.1415 dims_tried=[REPORTING_PERIOD, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE] ratios_at_each_level=[0.1415, 0.2471, 0.2471] |
| portal_soc_utah_open_data_p_7105312f13 | not-unique-after-dimension-search | base=PATENT_NBR key_ratio=0.5135 dims_tried=[CLASS, PROCESS_STATUS] ratios_at_each_level=[0.5135, 0.5165, 0.52] |
| portal_soc_utah_open_data_p_728fda9fb7 | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.2686 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.2686, 0.9276, 0.9276, 0.9371] |
| portal_soc_utah_open_data_p_79cfd825bf | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_79eab10d34 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_7b0a7183bd | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.2694 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.2694, 0.9336, 0.9336, 0.9469] |
| portal_soc_utah_open_data_p_7dacfb4113 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_8196274d0d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_862ba39eb7 | not-unique-after-dimension-search | base=FAC_ZIP key_ratio=0.3529 dims_tried=[(none found)] ratios_at_each_level=[0.3529] |
| portal_soc_utah_open_data_p_86fcd42645 | not-unique-after-dimension-search | base=GEO_ID key_ratio=0.0194 dims_tried=[YEAR_ID] ratios_at_each_level=[0.0194, 0.0194] |
| portal_soc_utah_open_data_p_944a7b18a7 | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.2171 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.2171, 0.9718, 0.9718, 0.9718] |
| portal_soc_utah_open_data_p_956795da22 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_9837982623 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_9875d7f6e3 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_990c78c284 | not-unique-after-dimension-search | base=BILLING_PROVIDER_NPI key_ratio=0.054 dims_tried=[YEAR, CLAIM_CATEGORY_HEADER, HCPCS_CPT_PROCEDURE_CODE] ratios_at_each_level=[0.054, 0.054, 0.055, 0.7115] |
| portal_soc_utah_open_data_p_99d27e2813 | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.2746 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.2746, 0.9545, 0.9545, 0.9621] |
| portal_soc_utah_open_data_p_9c28a0a981 | not-unique-after-dimension-search | base=GEO_ID key_ratio=0.0227 dims_tried=[YEAR_ID] ratios_at_each_level=[0.0227, 0.0341] |
| portal_soc_utah_open_data_p_9cf01a9e6c | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.2926 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.2926, 0.9372, 0.9372, 0.9479] |
| portal_soc_utah_open_data_p_a3773e6ff0 | not-unique-after-dimension-search | base=GEO_ID key_ratio=0.0227 dims_tried=[YEAR_ID] ratios_at_each_level=[0.0227, 0.0341] |
| portal_soc_utah_open_data_p_a396f5d252 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_a6509f0d9f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_a6af8166d5 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_a8921e729f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_aa0ab39dee | not-unique-after-dimension-search | base=PATENT_NBR key_ratio=0.6175 dims_tried=[CLASS, LOT_TYPE_CD, SOLD_STATUS_DESCR] ratios_at_each_level=[0.6175, 0.6175, 0.62, 0.6215] |
| portal_soc_utah_open_data_p_aa199b616a | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_ac08d0651f | not-unique-after-dimension-search | base=BILLING_PROVIDER_NPI key_ratio=0.0485 dims_tried=[YEAR, TAXONOMY_CLASSIFICATION, CLAIM_CATEGORY_HEADER] ratios_at_each_level=[0.0485, 0.0485, 0.101, 0.1025] |
| portal_soc_utah_open_data_p_ac57352c67 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_acb06f036d | not-unique-after-dimension-search | base=PATENT_NBR key_ratio=0.6345 dims_tried=[CLASS, LOT_TYPE_CD, SOLD_STATUS_DESCR] ratios_at_each_level=[0.6345, 0.6345, 0.638, 0.64] |
| portal_soc_utah_open_data_p_ad1173edf2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_afad2153ea | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_b0241dee4b | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_b21f81e6f9 | not-unique-after-dimension-search | base=PATENT_NR key_ratio=0.251 dims_tried=[CREATE_DATE, MODIFY_DATE, STATUS] ratios_at_each_level=[0.251, 0.251, 0.2535, 0.2575] |
| portal_soc_utah_open_data_p_b55a5210a0 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_b84814b0c6 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_bacd4ff0a2 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_bf328add84 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_bf857f3b65 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_c3b6301825 | not-unique-after-dimension-search | base=PATENT_NBR key_ratio=0.6345 dims_tried=[CLASS, LOT_TYPE_CD, SOLD_STATUS_DESCR] ratios_at_each_level=[0.6345, 0.6345, 0.638, 0.64] |
| portal_soc_utah_open_data_p_c3b898941a | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_c68bc3f05c | not-unique-after-dimension-search | base=ALTERNATE_CCN_1 key_ratio=0.2432 dims_tried=[HEMOGLOBIN_12_G_DL_PERFORMANCE_PERIOD_RATE, NUMBER_OF_HEMOGLOBIN_ELIGIBLE_PATIENTS_PERFORMANCE_PERIOD, HEMOGLOBIN_12_G_DL_BASELINE_PERIOD_RATE] ratios_at_each_level=[0.2432, 0.2703, 0.8378, 0.973] |
| portal_soc_utah_open_data_p_caebcfeeaf | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_cc88c02100 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_cee3f16579 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_d769afdaba | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.0931 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.0931, 0.3337, 0.9467, 0.9572] |
| portal_soc_utah_open_data_p_d903a6fe0d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_d9caa2e2f3 | not-unique-after-dimension-search | base=GEO_ID key_ratio=0.0215 dims_tried=[YEAR_ID] ratios_at_each_level=[0.0215, 0.0323] |
| portal_soc_utah_open_data_p_e776045748 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_e7a8212053 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_e801b0732d | not-unique-after-dimension-search | base=PATENT_NR key_ratio=0.2515 dims_tried=[CREATE_DATE, MODIFY_DATE, STATUS] ratios_at_each_level=[0.2515, 0.253, 0.2545, 0.259] |
| portal_soc_utah_open_data_p_e8fd09be6d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_eefc28ce6f | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_f023097d74 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_f10f70de47 | not-unique-after-dimension-search | base=BILLING_PROVIDER_NPI key_ratio=0.072 dims_tried=[YEAR, CLAIM_CATEGORY_HEADER, HCPCS_CPT_PROCEDURE_CODE] ratios_at_each_level=[0.072, 0.072, 0.073, 0.723] |
| portal_soc_utah_open_data_p_f259cd7fc8 | not-unique-after-dimension-search | base=TRI_FACILITY_ID key_ratio=0.0211 dims_tried=[CAS_COMPOUND_ID, YEAR, CLASSIFICATION] ratios_at_each_level=[0.0211, 0.1393, 0.9432, 0.9552] |
| portal_soc_utah_open_data_p_f6e04b3d02 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_f7cb1e8c0d | not-unique-after-dimension-search | base=BILLING_PROVIDER_NPI key_ratio=0.0675 dims_tried=[YEAR, CLAIM_CATEGORY_HEADER, HCPCS_CPT_PROCEDURE_CODE] ratios_at_each_level=[0.0675, 0.0675, 0.0675, 0.698] |
| portal_soc_utah_open_data_p_f8e4ec438d | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_f9efc33574 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_fa2123b348 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_utah_open_data_p_fb07cfaf59 | not-unique-after-dimension-search | base=ALTERNATE_CCN_1 key_ratio=0.2432 dims_tried=[ZIP_CODE] ratios_at_each_level=[0.2432, 0.8649] |
| portal_soc_utah_open_data_p_fb657aa744 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_washington_state_0dae4a9b61 | no-key-column | ENTITY_TYPES hint: (none) |
| portal_soc_washington_state_914cf85743 | not-unique-after-dimension-search | base=GASO_NPI key_ratio=0.3988 dims_tried=[RECORDED_DATE, EFFECTIVE_DATE, RATE_TYPE] ratios_at_each_level=[0.3988, 0.7166, 0.7551, 0.9777] |
| st_oehha_proposition_65_list | no-key-column | ENTITY_TYPES hint: (none) |
| state_mo_sex_offender_registry | not-unique-after-dimension-search | base=ZIP key_ratio=0.0369 dims_tried=[DATE_OF_BIRTH, TIER] ratios_at_each_level=[0.0369, 0.7846, 0.7868] |
| tx_lobby_awards | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_cover | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_dockets | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_entertainment | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_events | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_food_beverage | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_gifts | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_individual_reporting | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_subject_matter | no-key-column | ENTITY_TYPES hint: (none) |
| tx_lobby_transportation | no-key-column | ENTITY_TYPES hint: (none) |
| xc_biorxiv_medrxiv | not-unique-after-dimension-search | base=FUNDING_ID key_ratio=0.0023 dims_tried=[FUNDING_ID_TYPE, DATE, PREPRINT_DATE] ratios_at_each_level=[0.0023, 0.0023, 0.0046, 0.6134] |
| xc_guttmacher_monthly_abortion | no-key-column | ENTITY_TYPES hint: (none) |
| xc_jcs_coa | no-key-column | ENTITY_TYPES hint: person |
| xc_jcs_medians | no-key-column | ENTITY_TYPES hint: (none) |
| xc_jcs_scotus | no-key-column | ENTITY_TYPES hint: person |
| xc_nagix_dprk_missile_tests | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_ai_incidents_annual | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_co2 | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_cpi | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_fertility | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_fossil_share | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_gini | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_homicide | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_life_expectancy | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_nuclear_warheads | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_temp_anomaly | no-key-column | ENTITY_TYPES hint: (none) |
| xc_owid_terrorism_deaths | no-key-column | ENTITY_TYPES hint: (none) |
| xc_ransomwarelive_victims | not-unique-after-dimension-search | base=COUNTRY key_ratio=0.006 dims_tried=[GROUP_NAME] ratios_at_each_level=[0.006, 0.1369] |
| xc_uk_sanctions_list | not-unique-after-dimension-search | base=IMO_NUMBER key_ratio=0.0114 dims_tried=[DATE_DESIGNATED, YEAR_BUILT, OFSI_GROUP_ID, UNIQUE_ID] ratios_at_each_level=[0.0114, 0.1091, 0.019, 0.019, 0.1002, 0.1091] |
| xc_un_consolidated_sanctions_list | no-key-column | ENTITY_TYPES hint: (none) |
| xc_wayback_doj_epstein | no-key-column | ENTITY_TYPES hint: (none) |
| xc_wayback_replay_doj_deep_pages | no-key-column | ENTITY_TYPES hint: (none) |
| xc_wayback_replay_doj_listing | no-key-column | ENTITY_TYPES hint: (none) |
| xc_wikipedia_largest_us_companies | no-key-column | ENTITY_TYPES hint: (none) |

## No physical LANDING table (4)

- INT_GLEIF_RR (modeled)
- fed_dea_arcos (modeled)
- fed_fjc_idb (modeled)
- intl_uk_companies_house (modeled)

## No SOURCE_REGISTRY row (199)

- fed_atf_ffl (modeled)
- fed_atf_ffl_locations (sampled)
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
- fed_dol_ofccp_csal (sampled)
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
