# JOIN_KEYS_STD backfill report

WRITE 142 | SKIP_MEASURED 134 | SKIP_NO_MEASURE 135 | NO_TABLE 2 | NO_REGISTRY_ROW 55

## WOULD WRITE (provisional -> measured)

| source_id | current | measured keys | tier | confirmed columns |
|---|---|---|---|---|
| FED_CMS_PARTD_PRESCRIBER_DRUG | NPI,STATE | NPI,FIPS,NAME | STEEL | Prscrbr_NPI=NPI(100.0%/46900d); Prscrbr_Last_Org_Name=NAME(99.97%/25536d); Prscrbr_First_Name=NAME(99.99%/9840d); Prscrbr_State_FIPS=FIPS(100.0%/58d); Brnd_Name=NAME(100.0%/1251d); Gnrc_Name=NAME(100.0%/914d) |
| FED_EPA_FRS_FULL | COUNTY,FIPS,FRS_ID,STATE,ZIP | FRS_ID,COUNTRY,FIPS,ZIP,ADDRESS,NAME | STEEL | REGISTRY_ID=FRS_ID(100.0%/51003d); PRIMARY_NAME=NAME(99.84%/47727d); LOCATION_ADDRESS=ADDRESS(91.12%/44186d); CITY_NAME=NAME(91.88%/10254d); COUNTY_NAME=NAME(91.06%/2574d); FIPS_CODE=FIPS(79.99%/4597d); STATE_NAME=NAME(96.24%/85d); COUNTRY_NAME=COUNTRY(79.04%/17d); POSTAL_CODE=ZIP(91.42%/16262d); SITE_TYPE_NAME=NAME(95.52%/10d) |
| FED_FAC_SINGLE_AUDIT | EIN,FIPS | EIN,UEI,ZIP,ADDRESS,NAME | STEEL | AUDITEE_UEI=UEI(100.0%/19171d); AUDITEE_EIN=EIN(100.0%/33328d); AUDITEE_NAME=NAME(100.0%/35329d); AUDITEE_ZIP=ZIP(100.0%/13681d); AUDITEE_ADDRESS_LINE_1=ADDRESS(100.0%/32320d); AUDITOR_EIN=EIN(99.94%/4540d); AUDITOR_FIRM_NAME=NAME(100.0%/5661d); AUDITOR_ZIP=ZIP(99.99%/3640d) |
| FED_FEC_INDEPENDENT_EXPENDITURES | FEC_ID | FEC_CAND_ID,NAME | STEEL | cand_id=FEC_CAND_ID(87.52%/1545d); cand_name=NAME(100.0%/2085d) |
| FED_IRS_990_EFILE_INDEX | EIN | EIN,NAME | STEEL | EIN=EIN(100.0%/48405d); TAXPAYER_NAME=NAME(100.0%/49326d) |
| FED_IRS_EO_PR | EIN,ZIP | EIN,ZIP,ADDRESS,NAME | STEEL | EIN=EIN(100.0%/2617d); NAME=NAME(100.0%/2540d); STREET=ADDRESS(100.0%/2441d); ZIP=ZIP(100.0%/166d); ORGANIZATION=NAME(100.0%/5d); SORT_NAME=NAME(16.58%/411d) |
| FED_MSHA_ACCIDENTS | MINE_ID | MINE_ID,FIPS,NAME | STEEL | MINE_ID=MINE_ID(100.0%/7805d); CONTROLLER_NAME=NAME(99.75%/3570d); OPERATOR_NAME=NAME(99.75%/4688d); FIPS_STATE_CD=FIPS(100.0%/53d); EQUIP_MFR_NAME=NAME(100.0%/166d) |
| FED_MSHA_MINES | MINE_ID,STATE | MINE_ID,SIC,FIPS,NAME | STEEL | MINE_ID=MINE_ID(100.0%/49700d); CURRENT_MINE_NAME=NAME(100.0%/36501d); CURRENT_CONTROLLER_NAME=NAME(98.85%/26889d); CURRENT_OPERATOR_NAME=NAME(100.0%/28939d); FIPS_CNTY_CD=FIPS(100.0%/285d); FIPS_CNTY_NM=FIPS(100.0%/1681d); COMPANY_TYPE=NAME(72.73%/4d); OFFICE_NAME=NAME(100.0%/89d); PRIMARY_SIC_CD=SIC(99.64%/115d); PRIMARY_SIC=SIC(99.64%/113d); PRIMARY_SIC_CD_1=SIC(99.64%/28d); PRIMARY_SIC_CD_SFX=SIC(99.64%/28d); SECONDARY_SIC_CD=SIC(0.9%/51d); SECONDARY_SIC=SIC(0.9%/51d); SECONDARY_SIC_CD_1=SIC(0.9%/19d); SECONDARY_SIC_CD_SFX=SIC(0.9%/18d) |
| FED_MSHA_VIOLATIONS | MINE_ID | MINE_ID,DOCKET,NAME | STEEL | CONTROLLER_NAME=NAME(93.03%/7691d); VIOLATOR_NAME=NAME(100.0%/11128d); MINE_ID=MINE_ID(100.0%/12956d); MINE_NAME=NAME(100.0%/11320d); DOCKET_NO=DOCKET(6.21%/2863d); DOCKET_STATUS_CD=DOCKET(6.23%/2d) |
| FED_SEC_INSIDER_REPORTINGOWNER | ACCESSION_NUMBER,STATE,ZIP | ZIP | GEO | RPTOWNER_ZIPCODE=ZIP(96.59%/3563d) |
| FED_USASPENDING_ASSISTANCE_FULL | STATE,UEI | DUNS,UEI,COUNTRY,NAME | STEEL | awarding_agency_name=NAME(100.0%/38d); awarding_sub_agency_name=NAME(100.0%/145d); awarding_office_name=NAME(45.49%/511d); funding_agency_name=NAME(47.51%/34d); funding_sub_agency_name=NAME(47.51%/109d); funding_office_name=NAME(45.21%/481d); recipient_uei=UEI(39.43%/10418d); recipient_duns=DUNS(36.63%/11470d); recipient_name=NAME(100.0%/19387d); recipient_name_raw=NAME(100.0%/20044d); recipient_parent_uei=UEI(21.4%/3534d); recipient_parent_duns=DUNS(18.29%/2817d); recipient_parent_name=NAME(23.05%/3575d); recipient_parent_name_raw=NAME(20.09%/3462d); recipient_country_code=COUNTRY(87.19%/112d); recipient_country_name=COUNTRY(87.19%/108d) |
| FED_USASPENDING_CONTRACTS_FULL | (empty) | DUNS,UEI,NAME | STEEL | parent_award_agency_name=NAME(64.94%/119d); awarding_agency_name=NAME(100.0%/61d); awarding_sub_agency_name=NAME(100.0%/156d); awarding_office_name=NAME(99.99%/3125d); funding_agency_name=NAME(93.14%/69d); funding_sub_agency_name=NAME(93.14%/239d); funding_office_name=NAME(92.71%/5826d); recipient_uei=UEI(100.0%/16817d); recipient_duns=DUNS(66.61%/13143d); recipient_name=NAME(100.0%/15481d); recipient_name_raw=NAME(99.82%/16646d); recipient_doing_business_as_name=NAME(4.6%/1131d); recipient_parent_uei=UEI(99.92%/15271d); recipient_parent_duns=DUNS(66.6%/11634d); recipient_parent_name=NAME(99.94%/14413d); recipient_parent_name_raw=NAME(99.78%/15109d) |
| INTL_GLEIF | LEI | LEI,NAME | STEEL | LEI=LEI(100.0%/49438d); Entity.LegalName=NAME(95.94%/48537d); Entity.LegalName.xmllang=NAME(99.4%/108d); Entity.OtherEntityNames.OtherEntityName.1=NAME(11.92%/5915d); Entity.OtherEntityNames.OtherEntityName.1.xmllang=NAME(11.98%/50d); Entity.OtherEntityNames.OtherEntityName.1.type=NAME(12.11%/3d); Entity.OtherEntityNames.OtherEntityName.2=NAME(1.52%/775d); Entity.OtherEntityNames.OtherEntityName.2.xmllang=NAME(1.55%/36d); Entity.OtherEntityNames.OtherEntityName.2.type=NAME(1.57%/3d) |
| INT_UK_COMPANIES_HOUSE | (empty) | COMPANY_NO,SIC,COUNTRY,ADDRESS,NAME | STEEL | CompanyName=NAME(100.0%/49713d); CompanyNumber=COMPANY_NO(100.0%/50672d); RegAddress.POBox=ADDRESS(0.53%/20d); RegAddress.AddressLine1=ADDRESS(98.96%/38405d); RegAddress.AddressLine2=ADDRESS(59.87%/16295d); RegAddress.PostTown=ADDRESS(98.38%/3055d); RegAddress.County=ADDRESS(28.81%/572d); RegAddress.Country=COUNTRY(84.22%/61d); RegAddress.PostCode=ADDRESS(98.5%/34936d); CompanyCategory=NAME(100.0%/19d); CompanyStatus=NAME(100.0%/9d); CountryOfOrigin=COUNTRY(100.0%/58d); SICCode.SicText_1=SIC(100.0%/703d); SICCode.SicText_2=SIC(20.19%/506d); SICCode.SicText_3=SIC(8.91%/391d) |
| ca_lobby_amendments | (empty) | NAME | PROBABILISTIC | A_LF_NAME=NAME(3.76%/387d); D_LF_NAME=NAME(2.14%/253d) |
| ca_lobby_chg_log | (empty) | ZIP,NAME | GEO | FILER_FULL_NAME=NAME(99.81%/18818d); FILER_ZIP=ZIP(22.97%/1353d); ENTITY_NAME=NAME(91.78%/18016d); ENTITY_ZIP=ZIP(2.12%/332d) |
| ca_lobby_contributions | (empty) | NAME | PROBABILISTIC | RECIPIENT_NAME=NAME(99.42%/1533d); RECIPIENT_ID=NAME(97.28%/561d) |
| ca_lobby_cover | (empty) | NAME | PROBABILISTIC | FIRM_NAME=NAME(64.12%/7824d) |
| ca_lobby_emp_lobbyist | (empty) | NAME | PROBABILISTIC | EMPLOYER_ID=NAME(100.0%/355d); LOBBYIST_LAST_NAME=NAME(100.0%/611d); LOBBYIST_FIRST_NAME=NAME(100.0%/594d); EMPLOYER_NAME=NAME(100.0%/443d) |
| ca_lobby_employer | (empty) | NAME | PROBABILISTIC | EMPLOYER_ID=NAME(100.0%/1730d); EMPLOYER_NAME=NAME(100.0%/1747d); INTEREST_NAME=NAME(99.83%/19d) |
| ca_lobby_employer_firms | (empty) | NAME | PROBABILISTIC | EMPLOYER_ID=NAME(100.0%/176d); FIRM_NAME=NAME(100.0%/172d) |
| ca_lobby_firm | (empty) | NAME | PROBABILISTIC | FIRM_NAME=NAME(100.0%/256d) |
| ca_lobby_firm_employer | (empty) | NAME | PROBABILISTIC | FIRM_NAME=NAME(100.0%/24d); EMPLOYER_NAME=NAME(100.0%/166d) |
| ca_lobby_firm_lobbyist | (empty) | NAME | PROBABILISTIC | LOBBYIST_LAST_NAME=NAME(100.0%/501d); LOBBYIST_FIRST_NAME=NAME(100.0%/500d); FIRM_NAME=NAME(99.65%/340d) |
| fed_cms_ambulatory_specialty_model_participants | NPI,STATE | NPI,NAME | STEEL | NPI=NPI(100.0%/6535d); FIRST_NAME=NAME(99.98%/2360d); LAST_NAME=NAME(99.98%/4994d); ORGANIZATION_LEGAL_NAME=NAME(99.74%/2629d) |
| fed_cms_facility_level_minimum_data_set_frequency | CCN,STATE,ZIP | CCN,FIPS,ZIP,NAME | STEEL | CCN=CCN(98.96%/238d); PROVIDER_NAME=NAME(100.0%/235d); ZIP_CODE=ZIP(100.0%/184d); FIPS_COUNTY_CODE=FIPS(100.0%/76d); COUNTY_NAME=NAME(100.0%/75d) |
| fed_cms_federally_qualified_health_center_enrollments | CCN,NPI,STATE,ZIP | CCN,NPI,ZIP,ADDRESS,NAME | STEEL | NPI=NPI(100.0%/10594d); CCN=CCN(89.98%/10127d); ORGANIZATION_NAME=NAME(100.0%/1526d); DOING_BUSINESS_AS_NAME=NAME(61.41%/5515d); ORGANIZATION_TYPE_STRUCTURE=NAME(11.62%/2d); ORGANIZATION_OTHER_TYPE_TEXT=NAME(11.46%/193d); ADDRESS_LINE_1=ADDRESS(100.0%/10694d); ADDRESS_LINE_2=ADDRESS(21.02%/858d); ZIP_CODE=ZIP(100.0%/6459d) |
| fed_cms_fiscal_intermediary_shared_system_attending_and_rendering | NPI | NPI,NAME | STEEL | NPI=NPI(100.0%/49530d); LAST_NAME=NAME(99.98%/27780d); FIRST_NAME=NAME(99.99%/10576d) |
| fed_cms_home_health_agency_enrollments | CCN,NPI,STATE,ZIP | CCN,NPI,ZIP,ADDRESS,NAME | STEEL | NPI=NPI(100.0%/11435d); CCN=CCN(99.17%/11723d); ORGANIZATION_NAME=NAME(99.99%/9603d); DOING_BUSINESS_AS_NAME=NAME(42.62%/3476d); ORGANIZATION_TYPE_STRUCTURE=NAME(4.0%/3d); ORGANIZATION_OTHER_TYPE_TEXT=NAME(3.13%/129d); ADDRESS_LINE_1=ADDRESS(100.0%/9578d); ADDRESS_LINE_2=ADDRESS(71.22%/1737d); ZIP_CODE=ZIP(100.0%/4571d) |
| fed_cms_hospice_enrollments | CCN,NPI,STATE,ZIP | CCN,NPI,ZIP,ADDRESS,NAME | STEEL | NPI=NPI(100.0%/6174d); CCN=CCN(79.1%/4723d); ORGANIZATION_NAME=NAME(100.0%/5005d); DOING_BUSINESS_AS_NAME=NAME(53.59%/2367d); ORGANIZATION_TYPE_STRUCTURE=NAME(5.03%/3d); ORGANIZATION_OTHER_TYPE_TEXT=NAME(3.51%/78d); ADDRESS_LINE_1=ADDRESS(100.0%/5582d); ADDRESS_LINE_2=ADDRESS(69.45%/1061d); ZIP_CODE=ZIP(100.0%/3182d) |
| fed_cms_hospital_enrollments | CCN,NPI,STATE,ZIP | CCN,NPI,ZIP,ADDRESS,NAME | STEEL | NPI=NPI(100.0%/8693d); CCN=CCN(65.02%/5992d); ORGANIZATION_NAME=NAME(100.0%/5196d); DOING_BUSINESS_AS_NAME=NAME(76.45%/5252d); ORGANIZATION_TYPE_STRUCTURE=NAME(24.32%/3d); ORGANIZATION_OTHER_TYPE_TEXT=NAME(22.45%/431d); ADDRESS_LINE_1=ADDRESS(100.0%/6289d); ADDRESS_LINE_2=ADDRESS(8.27%/578d); ZIP_CODE=ZIP(100.0%/5076d) |
| fed_cms_medicare_diabetes_prevention_program | NPI,STATE,ZIP | NPI,ZIP,ADDRESS,NAME | STEEL | ORGANIZATION_NAME=NAME(100.0%/296d); LOCATION_NAME=NAME(100.0%/424d); STREET_ADDRESS_LINE_1=ADDRESS(100.0%/996d); STREET_ADDRESS_LINE_2=ADDRESS(30.18%/234d); ZIP_CODE=ZIP(100.0%/870d); NPI=NPI(100.0%/313d) |
| fed_cms_medicare_dialysis_facilities | CCN,NPI,STATE | CCN,NPI,NAME | STEEL | CCN=CCN(100.0%/340d); PROVIDER_NAME=NAME(100.0%/320d); NPI=NPI(100.0%/335d) |
| fed_cms_medicare_durable_medical_equipment_devices_supplies_by_refer | (empty) | NPI,COUNTRY,FIPS,ZIP,NAME | STEEL | RFRG_NPI=NPI(100.0%/50402d); RFRG_PRVDR_LAST_NAME_ORG=NAME(99.97%/26494d); RFRG_PRVDR_FIRST_NAME=NAME(99.99%/10239d); RFRG_PRVDR_STATE_FIPS=FIPS(100.0%/57d); RFRG_PRVDR_ZIP5=ZIP(100.0%/10211d); RFRG_PRVDR_CNTRY=COUNTRY(100.0%/5d) |
| fed_cms_medicare_durable_medical_equipment_devices_supplies_by_suppl | (empty) | NPI,FIPS,ZIP,NAME | STEEL | SUPLR_NPI=NPI(100.0%/25338d); SUPLR_PRVDR_LAST_NAME_ORG=NAME(99.99%/8324d); SUPLR_PRVDR_STATE_FIPS=FIPS(100.0%/55d); SUPLR_PRVDR_ZIP5=ZIP(100.0%/9660d) |
| fed_cms_medicare_fee_for_service_public_provider_enrollment | NPI | NPI,NAME | STEEL | NPI=NPI(100.0%/49416d); FIRST_NAME=NAME(85.39%/9321d); MDL_NAME=NAME(52.29%/3476d); LAST_NAME=NAME(85.37%/23940d); ORG_NAME=NAME(14.6%/6752d) |
| fed_cms_medicare_inpatient_hospitals_by_provider | (empty) | CCN,FIPS,ZIP,NAME | STEEL | RNDRNG_PRVDR_CCN=CCN(100.0%/2988d); RNDRNG_PRVDR_ORG_NAME=NAME(100.0%/2971d); RNDRNG_PRVDR_ZIP5=ZIP(100.0%/2863d); RNDRNG_PRVDR_STATE_FIPS=FIPS(100.0%/51d) |
| fed_cms_medicare_inpatient_hospitals_by_provider_and_service | (empty) | CCN,FIPS,ZIP,NAME | STEEL | RNDRNG_PRVDR_CCN=CCN(100.0%/2701d); RNDRNG_PRVDR_ORG_NAME=NAME(100.0%/2705d); RNDRNG_PRVDR_STATE_FIPS=FIPS(100.0%/51d); RNDRNG_PRVDR_ZIP5=ZIP(100.0%/2619d) |
| fed_cms_medicare_outpatient_hospitals_by_provider_and_service | (empty) | CCN,FIPS,ZIP,NAME | STEEL | RNDRNG_PRVDR_CCN=CCN(100.0%/2996d); RNDRNG_PRVDR_ORG_NAME=NAME(100.0%/2963d); RNDRNG_PRVDR_STATE_FIPS=FIPS(100.0%/50d); RNDRNG_PRVDR_ZIP5=ZIP(100.0%/2801d) |
| fed_cms_medicare_physician_other_practitioners_by_provider | NPI | NPI,COUNTRY,FIPS,ZIP,NAME | STEEL | RNDRNG_NPI=NPI(100.0%/51040d); RNDRNG_PRVDR_LAST_ORG_NAME=NAME(99.98%/27642d); RNDRNG_PRVDR_FIRST_NAME=NAME(95.39%/9454d); RNDRNG_PRVDR_STATE_FIPS=FIPS(100.0%/60d); RNDRNG_PRVDR_ZIP5=ZIP(100.0%/9875d); RNDRNG_PRVDR_CNTRY=COUNTRY(100.0%/4d) |
| fed_cms_medicare_physician_other_practitioners_by_provider_and_servi | NPI | NPI,FIPS,ZIP,NAME | STEEL | RNDRNG_NPI=NPI(100.0%/29253d); RNDRNG_PRVDR_LAST_ORG_NAME=NAME(99.98%/17397d); RNDRNG_PRVDR_FIRST_NAME=NAME(95.28%/6592d); RNDRNG_PRVDR_STATE_FIPS=FIPS(100.0%/56d); RNDRNG_PRVDR_ZIP5=ZIP(100.0%/7530d) |
| fed_cms_nursing_home_deficiencies | (empty) | CCN,ZIP,ADDRESS,NAME | STEEL | CMS_CERTIFICATION_NUMBER_CCN=CCN(98.76%/12589d); PROVIDER_NAME=NAME(100.0%/12921d); PROVIDER_ADDRESS=ADDRESS(100.0%/13384d); ZIP_CODE=ZIP(100.0%/8428d) |
| fed_cms_nursing_home_fire_deficiencies | (empty) | CCN,ZIP,ADDRESS,NAME | STEEL | CMS_CERTIFICATION_NUMBER_CCN=CCN(98.48%/11922d); PROVIDER_NAME=NAME(100.0%/12184d); PROVIDER_ADDRESS=ADDRESS(100.0%/12571d); ZIP_CODE=ZIP(100.0%/8141d) |
| fed_cms_nursing_home_penalties | (empty) | CCN,ZIP,ADDRESS,NAME | STEEL | CMS_CERTIFICATION_NUMBER_CCN=CCN(99.09%/6720d); PROVIDER_NAME=NAME(100.0%/6848d); PROVIDER_ADDRESS=ADDRESS(100.0%/6843d); ZIP_CODE=ZIP(100.0%/5254d) |
| fed_cms_opioid_treatment_program_providers | NPI,STATE,ZIP | NPI,ZIP,ADDRESS,NAME | STEEL | NPI=NPI(96.41%/1277d); PROVIDER_NAME=NAME(100.0%/849d); ADDRESS_LINE_1=ADDRESS(100.0%/1527d); ADDRESS_LINE_2=ADDRESS(35.56%/334d); ZIP=ZIP(100.0%/1355d) |
| fed_cms_opt_out_affidavits | NPI,STATE,ZIP | NPI,ZIP,ADDRESS,NAME | STEEL | FIRST_NAME=NAME(100.0%/7053d); LAST_NAME=NAME(99.99%/26591d); NPI=NPI(100.0%/48301d); FIRST_LINE_STREET_ADDRESS=ADDRESS(100.0%/32596d); SECOND_LINE_STREET_ADDRESS=ADDRESS(54.2%/4830d); CITY_NAME=NAME(100.0%/4423d); ZIP_CODE=ZIP(100.0%/8017d) |
| fed_cms_order_and_referring | NPI | NPI,NAME | STEEL | NPI=NPI(100.0%/49618d); LAST_NAME=NAME(99.98%/27166d); FIRST_NAME=NAME(100.0%/10510d) |
| fed_cms_pending_initial_logging_and_tracking_non_physicians | NPI | NPI,NAME | STEEL | NPI=NPI(100.0%/6900d); LAST_NAME=NAME(100.0%/4885d); FIRST_NAME=NAME(99.99%/2610d) |
| fed_cms_pending_initial_logging_and_tracking_physicians | NPI | NPI,NAME | STEEL | NPI=NPI(100.0%/7372d); LAST_NAME=NAME(100.0%/5504d); FIRST_NAME=NAME(99.94%/3212d) |
| fed_cms_quality_payment_program_experience | NPI | NPI | STEEL | NPI=NPI(100.0%/49152d) |
| fed_cms_rural_health_clinic_enrollments | CCN,NPI,STATE,ZIP | CCN,NPI,ZIP,ADDRESS,NAME | STEEL | NPI=NPI(100.0%/5130d); CCN=CCN(96.08%/5381d); ORGANIZATION_NAME=NAME(100.0%/2500d); DOING_BUSINESS_AS_NAME=NAME(82.66%/3958d); ORGANIZATION_TYPE_STRUCTURE=NAME(28.99%/3d); ORGANIZATION_OTHER_TYPE_TEXT=NAME(23.38%/305d); ADDRESS_LINE_1=ADDRESS(100.0%/5398d); ADDRESS_LINE_2=ADDRESS(20.67%/440d); ZIP_CODE=ZIP(100.0%/3678d) |
| fed_cms_skilled_nursing_facility_enrollments | CCN,NPI,STATE,ZIP | CCN,NPI,ZIP,ADDRESS,NAME | STEEL | NPI=NPI(100.0%/14244d); CCN=CCN(98.79%/13834d); ORGANIZATION_NAME=NAME(100.0%/12164d); DOING_BUSINESS_AS_NAME=NAME(88.08%/12234d); ORGANIZATION_TYPE_STRUCTURE=NAME(16.18%/3d); ORGANIZATION_OTHER_TYPE_TEXT=NAME(14.88%/284d); NURSING_HOME_PROVIDER_NAME=NAME(97.39%/13849d); AFFILIATION_ENTITY_NAME=NAME(70.88%/638d); ADDRESS_LINE_1=ADDRESS(100.0%/14693d); ADDRESS_LINE_2=ADDRESS(4.26%/580d); ZIP_CODE=ZIP(100.0%/8996d) |
| fed_college_scorecard_institution | (empty) | FIPS,LATLON,ZIP,ADDRESS | GEO | ZIP=ZIP(100.0%/4473d); ST_FIPS=FIPS(100.0%/58d); LATITUDE=LATLON(91.36%/5691d); LONGITUDE=LATLON(91.36%/5677d); ADDR=ADDRESS(92.46%/5667d) |
| fed_consolidated_screening_list | (empty) | NAME | PROBABILISTIC | NAME=NAME(100.0%/24556d) |
| fed_courtlistener_dockets | DOCKET_NUMBER | DOCKET,NAME | STRONG | CASE_NAME_SHORT=NAME(69.71%/27798d); CASE_NAME=NAME(98.4%/46910d); CASE_NAME_FULL=NAME(8.01%/3966d); DOCKET_NUMBER=DOCKET(95.81%/47996d); DOCKET_NUMBER_CORE=DOCKET(82.59%/39678d); DOCKET_NUMBER_RAW=DOCKET(95.81%/47996d) |
| fed_courtlistener_judges | (empty) | COUNTRY,NAME | GEO | NAME_FIRST=NAME(100.0%/2302d); NAME_MIDDLE=NAME(82.13%/2229d); NAME_LAST=NAME(99.99%/8968d); NAME_SUFFIX=NAME(1.18%/3d); DOB_COUNTRY=COUNTRY(99.96%/63d); DOD_COUNTRY=COUNTRY(99.96%/2d) |
| fed_courtlistener_positions | (empty) | NAME | PROBABILISTIC | ORGANIZATION_NAME=NAME(25.87%/6288d) |
| fed_cpsc_neiss_codes | (empty) | NAME | PROBABILISTIC | FORMAT_NAME=NAME(100.0%/11d) |
| fed_dea_arcos_full | DEA_NO | DEA_NO,ZIP,NAME | STEEL | REPORTER_DEA_NO=DEA_NO(100.0%/329d); REPORTER_NAME=NAME(100.0%/186d); REPORTER_ZIP=ZIP(93.01%/255d); BUYER_DEA_NO=DEA_NO(100.0%/31541d); BUYER_NAME=NAME(100.0%/15772d); BUYER_ZIP=ZIP(93.68%/10905d); DRUG_NAME=NAME(100.0%/2d); PRODUCT_NAME=NAME(100.0%/318d); INGREDIENT_NAME=NAME(100.0%/2d); COMBINED_LABELER_NAME=NAME(100.0%/66d); REVISED_COMPANY_NAME=NAME(100.0%/62d) |
| fed_epa_air_emissions_poll_rpt_combined_emissions | FRS_ID | FRS_ID,NAME | STEEL | REGISTRY_ID=FRS_ID(100.0%/16780d); POLLUTANT_NAME=NAME(100.0%/446d) |
| fed_epa_egrid_plant_2022 | (empty) | FIPS,LATLON,NAME | GEO | PLANT_NAME=NAME(100.0%/11617d); PLANT_TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_NAME=NAME(99.5%/1039d); UTILITY_NAME=NAME(100.0%/5093d); BALANCING_AUTHORITY_NAME=NAME(100.0%/69d); EGRID_SUBREGION_NAME=NAME(100.0%/28d); PLANT_FIPS_STATE_CODE=FIPS(100.0%/53d); PLANT_FIPS_COUNTY_CODE=FIPS(99.71%/256d); PLANT_COUNTY_NAME=NAME(99.8%/1410d); PLANT_LATITUDE=LATLON(99.99%/11970d); PLANT_LONGITUDE=LATLON(99.99%/11783d) |
| fed_epa_frs_frs_naics_codes | FRS_ID | FRS_ID,NAICS | STEEL | NAICS_CODE=NAICS(99.99%/1788d); REGISTRY_ID=FRS_ID(99.93%/48261d) |
| fed_epa_frs_frs_program_links | COUNTY,FIPS,FRS_ID,STATE,ZIP | FRS_ID,COUNTRY,FIPS,ZIP,ADDRESS,NAME | STEEL | REGISTRY_ID=FRS_ID(100.0%/50211d); PRIMARY_NAME=NAME(99.94%/46911d); LOCATION_ADDRESS=ADDRESS(88.78%/42318d); CITY_NAME=NAME(89.52%/9345d); COUNTY_NAME=NAME(64.9%/2070d); FIPS_CODE=FIPS(66.56%/4356d); STATE_NAME=NAME(75.76%/62d); COUNTRY_NAME=COUNTRY(65.84%/13d); POSTAL_CODE=ZIP(89.5%/15386d) |
| fed_epa_frs_frs_sic_codes | FRS_ID | FRS_ID,SIC | STEEL | SIC_CODE=SIC(100.0%/935d); REGISTRY_ID=FRS_ID(99.77%/49339d) |
| fed_epa_icis_air_icis_air_facilities | FRS_ID,STATE,ZIP | FRS_ID,NAICS,SIC,ZIP,ADDRESS,NAME | STEEL | REGISTRY_ID=FRS_ID(99.92%/49711d); FACILITY_NAME=NAME(100.0%/46836d); STREET_ADDRESS=ADDRESS(99.95%/46834d); COUNTY_NAME=NAME(100.0%/1724d); ZIP_CODE=ZIP(99.93%/14460d); SIC_CODES=SIC(76.63%/1577d); NAICS_CODES=NAICS(100.0%/1857d); LOCAL_CONTROL_REGION_NAME=NAME(4.12%/51d) |
| fed_epa_icis_fec_case_enforcement_conclusion_facilities | ACTIVITY_ID,CASE_NUMBER | ZIP,NAME | GEO | FACILITY_NAME=NAME(99.98%/40237d); FACILITY_ZIP=ZIP(98.19%/15886d) |
| fed_epa_icis_fec_case_facilities | FRS_ID,STATE,ZIP | FRS_ID,NAICS,SIC,ZIP,ADDRESS,NAME | STEEL | REGISTRY_ID=FRS_ID(99.63%/35194d); FACILITY_NAME=NAME(99.98%/35654d); LOCATION_ADDRESS=ADDRESS(98.94%/35704d); ZIP=ZIP(98.6%/14524d); PRIMARY_SIC_CODE=SIC(58.33%/874d); PRIMARY_NAICS_CODE=NAICS(39.93%/847d) |
| fed_epa_icis_fec_epa_informal_enforcement_actions | FRS_ID | FRS_ID | STEEL | REGISTRY_ID=FRS_ID(100.0%/14840d) |
| fed_epa_icis_fec_icis_fec_epa_inspections | FRS_ID | FRS_ID,NAME | STEEL | REGISTRY_ID=FRS_ID(99.44%/40691d); FACILITY_NAME=NAME(99.97%/40932d) |
| fed_epa_npdes_icis_facilities | STATE,ZIP | LATLON,ZIP,ADDRESS,NAME | GEO | FACILITY_NAME=NAME(100.0%/49496d); LOCATION_ADDRESS=ADDRESS(99.85%/45834d); SUPPLEMENTAL_ADDRESS_TEXT=ADDRESS(10.19%/3810d); ZIP=ZIP(99.24%/14013d); GEOCODE_LATITUDE=LATLON(93.47%/43672d); GEOCODE_LONGITUDE=LATLON(93.47%/44213d) |
| fed_epa_npdes_npdes_informal_enforcement_actions | FRS_ID | FRS_ID | STEEL | REGISTRY_ID=FRS_ID(100.0%/29944d) |
| fed_epa_npdes_npdes_inspections | FRS_ID | FRS_ID | STEEL | REGISTRY_ID=FRS_ID(99.98%/31955d) |
| fed_epa_npdes_npdes_naics | NPDES_ID | NAICS | STRONG | NAICS_CODE=NAICS(100.0%/789d); NAICS_DESC=NAICS(100.0%/779d) |
| fed_epa_npdes_npdes_sics | NPDES_ID | SIC | STRONG | SIC_CODE=SIC(100.0%/783d); SIC_DESC=SIC(100.0%/764d) |
| fed_epa_sdwa_sdwa_events_milestones | PWSID | PWSID | STEEL | PWSID=PWSID(100.0%/35650d) |
| fed_epa_sdwa_sdwa_facilities | PWSID | PWSID,NAME | STEEL | PWSID=PWSID(100.0%/41923d); FACILITY_NAME=NAME(98.11%/23742d); SELLER_PWSID=PWSID(3.2%/1255d); SELLER_PWS_NAME=NAME(3.19%/1243d) |
| fed_epa_sdwa_sdwa_geographic_areas | PWSID | PWSID,ZIP | STEEL | PWSID=PWSID(100.0%/48522d); ZIP_CODE_SERVED=ZIP(1.23%/421d) |
| fed_epa_sdwa_sdwa_lcr_samples | PWSID | PWSID | STEEL | PWSID=PWSID(100.0%/35993d) |
| fed_epa_sdwa_sdwa_pn_violation_assoc | PWSID | PWSID | STEEL | PWSID=PWSID(100.0%/15795d) |
| fed_epa_sdwa_sdwa_pub_water_systems | PWSID,STATE,ZIP | PWSID,COUNTRY,ZIP,ADDRESS,NAME | STEEL | PWSID=PWSID(100.0%/49369d); PWS_NAME=NAME(99.81%/47277d); ORG_NAME=NAME(44.99%/20757d); ADMIN_NAME=NAME(88.86%/40356d); EMAIL_ADDR=ADDRESS(23.12%/10441d); ADDRESS_LINE1=ADDRESS(61.29%/25738d); ADDRESS_LINE2=ADDRESS(43.18%/17333d); CITY_NAME=NAME(96.58%/11729d); ZIP_CODE=ZIP(94.05%/16885d); COUNTRY_CODE=COUNTRY(97.74%/2d) |
| fed_epa_sdwa_sdwa_service_areas | PWSID | PWSID | STEEL | PWSID=PWSID(100.0%/50113d) |
| fed_epa_sdwa_sdwa_site_visits | PWSID | PWSID | STEEL | PWSID=PWSID(100.0%/43035d) |
| fed_epa_sdwa_sdwa_violations_enforcement | PWSID | PWSID | STEEL | PWSID=PWSID(100.0%/9664d) |
| fed_epa_tri_basic_2023 | (empty) | FRS_ID,LATLON,ZIP,ADDRESS,NAME | STEEL | C_3_FRS_ID=FRS_ID(99.81%/17727d); C_4_FACILITY_NAME=NAME(100.0%/15284d); C_5_STREET_ADDRESS=ADDRESS(100.0%/18564d); C_9_ZIP=ZIP(100.0%/8066d); C_12_LATITUDE=LATLON(100.0%/18372d); C_13_LONGITUDE=LATLON(100.0%/17781d); C_15_PARENT_CO_NAME=NAME(78.69%/3624d); C_17_STANDARD_PARENT_CO_NAME=NAME(88.15%/3912d); C_18_FOREIGN_PARENT_CO_NAME=NAME(14.31%/799d); C_20_STANDARD_FOREIGN_PARENT_CO_NAME=NAME(19.82%/705d) |
| fed_fatca_ffi | (empty) | COUNTRY,NAME | GEO | FI_NAME=NAME(100.0%/49339d); COUNTRY_NAME=COUNTRY(100.0%/192d) |
| fed_fda_faers_demo | (empty) | COUNTRY | GEO | REPORTER_COUNTRY=COUNTRY(28.55%/86d); OCCR_COUNTRY=COUNTRY(25.44%/93d) |
| fed_fec_bulk_linkages | FEC_ID | FEC_CAND_ID,FEC_CMTE_ID | STEEL | CAND_ID=FEC_CAND_ID(100.0%/11478d); CMTE_ID=FEC_CMTE_ID(100.0%/11441d) |
| fed_federal_register_documents | (empty) | DOCKET | STRONG | DOCKET_IDS=DOCKET(66.54%/28590d) |
| fed_fhfa_suspended_counterparty_program | (empty) | NAME | PROBABILISTIC | FIRST_NAME=NAME(87.14%/187d); LAST_NAME=NAME(87.14%/191d); COMPANY=NAME(12.86%/31d) |
| fed_google_polads_advertiser_declared_stats | (empty) | ADDRESS,NAME | PROBABILISTIC | ADVERTISER_DECLARED_NAME=NAME(92.55%/433d); ADVERTISER_DECLARED_PROMOTER_NAME=NAME(5.32%/25d); ADVERTISER_DECLARED_PROMOTER_ADDRESS=ADDRESS(5.96%/28d) |
| fed_google_polads_advertiser_geo_spend | (empty) | COUNTRY,NAME | GEO | ADVERTISER_NAME=NAME(99.99%/12671d); COUNTRY=COUNTRY(100.0%/2d); COUNTRY_SUBDIVISION_PRIMARY=COUNTRY(98.17%/56d) |
| fed_google_polads_advertiser_stats | (empty) | NAME | PROBABILISTIC | ADVERTISER_NAME=NAME(99.03%/19709d) |
| fed_google_polads_advertiser_weekly_spend | (empty) | NAME | PROBABILISTIC | ADVERTISER_NAME=NAME(98.97%/13003d) |
| fed_google_polads_creative_stats | (empty) | NAME | PROBABILISTIC | ADVERTISER_NAME=NAME(99.22%/6121d) |
| fed_google_polads_geo_spend | (empty) | COUNTRY | GEO | COUNTRY=COUNTRY(100.0%/12d); COUNTRY_SUBDIVISION_PRIMARY=COUNTRY(98.6%/204d); COUNTRY_SUBDIVISION_SECONDARY=COUNTRY(100.0%/226d) |
| fed_hud_assisted_housing_projects | (empty) | LATLON,ZIP,ADDRESS,NAME | GEO | NAME=NAME(99.95%/25579d); LATITUDE=LATLON(99.76%/27779d); LONGITUDE=LATLON(99.76%/28226d); STD_ADDR=ADDRESS(96.12%/27656d); STD_ZIP5=ZIP(86.03%/9320d) |
| fed_ice_detention_facility_list | (empty) | NAME | PROBABILISTIC | FACILITY_NAME=NAME(100.0%/163d) |
| fed_icij_offshoreleaks_addresses | (empty) | COUNTRY,ADDRESS,NAME | GEO | ADDRESS=ADDRESS(95.05%/48288d); NAME=NAME(55.39%/27373d); COUNTRY_CODES=COUNTRY(68.89%/197d) |
| fed_icij_offshoreleaks_entities | (empty) | COUNTRY,ADDRESS,NAME | GEO | NAME=NAME(100.0%/51081d); ORIGINAL_NAME=NAME(48.05%/24460d); FORMER_NAME=NAME(0.77%/384d); COMPANY_TYPE=NAME(16.83%/36d); ADDRESS=ADDRESS(36.63%/3594d); COUNTRY_CODES=COUNTRY(61.81%/382d) |
| fed_icij_offshoreleaks_intermediaries | (empty) | COUNTRY,ADDRESS,NAME | GEO | NAME=NAME(99.97%/24318d); ADDRESS=ADDRESS(32.29%/8462d); COUNTRY_CODES=COUNTRY(86.49%/287d) |
| fed_icij_offshoreleaks_officers | (empty) | COUNTRY,NAME | GEO | NAME=NAME(99.99%/40932d); COUNTRY_CODES=COUNTRY(61.3%/1216d) |
| fed_icij_offshoreleaks_others | (empty) | COUNTRY,NAME | GEO | NAME=NAME(99.9%/2973d); COUNTRY_CODES=COUNTRY(12.91%/63d) |
| fed_irs_auto_revocations | EIN,STATE,ZIP | EIN,COUNTRY,ZIP,NAME | STEEL | EIN=EIN(100.0%/49266d); LEGAL_NAME=NAME(100.0%/44674d); ORGANIZATION_ADDRESS=NAME(99.8%/43711d); ZIP_CODE=ZIP(99.71%/16920d); COUNTRY=COUNTRY(100.0%/33d) |
| fed_irs_pub78_eligible_donees | EIN,STATE | EIN,COUNTRY,NAME | STEEL | EIN=EIN(100.0%/49518d); LEGAL_NAME=NAME(100.0%/49032d); COUNTRY=COUNTRY(100.0%/13d) |
| fed_irs_soi_charities | EIN,STATE,ZIP | EIN,ZIP,ADDRESS,NAME | STEEL | EIN=EIN(100.0%/2472d); NAME=NAME(100.0%/2375d); STREET=ADDRESS(100.0%/2227d); ZIP=ZIP(100.0%/112d); C_ORGANIZATION=NAME(100.0%/6d); SORT_NAME=NAME(15.88%/382d) |
| fed_nid_dams | (empty) | LATLON,NAME | GEO | DAM_NAME=NAME(95.37%/43050d); LATITUDE=LATLON(99.83%/47046d); LONGITUDE=LATLON(99.83%/48458d); RIVER_OR_STREAM_NAME=NAME(90.04%/20126d) |
| fed_nih_reporter | (empty) | DUNS,UEI,NAME | STEEL | ORG_NAME=NAME(100.0%/2065d); ORG_DUNS=DUNS(97.99%/1866d); ORG_UEI=UEI(93.16%/1542d) |
| fed_ntsb_aviation_aircraft | (empty) | COUNTRY,ZIP,ADDRESS,NAME | GEO | OWNER_STREET=ADDRESS(33.27%/8137d); OWNER_COUNTRY=COUNTRY(93.74%/148d); OWNER_ZIP=ZIP(78.81%/10030d); OPER_INDIVIDUAL_NAME=NAME(100.0%/2d); OPER_NAME=NAME(50.6%/11891d); OPER_STREET=ADDRESS(26.44%/6855d); OPER_COUNTRY=COUNTRY(93.22%/149d); OPER_ZIP=ZIP(74.21%/9862d); DPRT_COUNTRY=COUNTRY(80.38%/145d); DEST_COUNTRY=COUNTRY(73.1%/150d) |
| fed_ntsb_aviation_events | (empty) | COUNTRY,GEOM,LATLON,ZIP,NAME | GEO | EV_COUNTRY=COUNTRY(99.99%/184d); EV_SITE_ZIPCODE=ZIP(78.27%/9122d); LATLONG_ACQ=GEOM(71.39%/2d); APT_NAME=NAME(61.37%/9888d); DEC_LATITUDE=LATLON(89.12%/23398d); DEC_LONGITUDE=LATLON(89.13%/24235d) |
| fed_osha_ita_300a_summary_2023 | EIN,STATE,ZIP | EIN,NAICS,ZIP,ADDRESS,NAME | STEEL | ESTABLISHMENT_NAME=NAME(99.99%/48830d); EIN=EIN(89.82%/22773d); COMPANY_NAME=NAME(95.14%/25329d); STREET_ADDRESS=ADDRESS(100.0%/48157d); ZIP_CODE=ZIP(96.3%/13733d); NAICS_CODE=NAICS(100.0%/1094d); NAICS_YEAR=NAICS(99.41%/3d) |
| fed_osha_ita_300a_summary_2024 | EIN,STATE,ZIP | EIN,NAICS,ZIP,ADDRESS,NAME | STEEL | ESTABLISHMENT_NAME=NAME(99.99%/49524d); EIN=EIN(89.26%/20491d); COMPANY_NAME=NAME(95.16%/24245d); STREET_ADDRESS=ADDRESS(100.0%/48589d); ZIP_CODE=ZIP(92.51%/12657d); NAICS_CODE=NAICS(100.0%/1024d); NAICS_YEAR=NAICS(100.0%/4d) |
| fed_osha_ita_300a_summary_2025 | EIN,STATE,ZIP | EIN,NAICS,ZIP,ADDRESS,NAME | STEEL | ESTABLISHMENT_NAME=NAME(100.0%/47984d); EIN=EIN(88.85%/19246d); COMPANY_NAME=NAME(95.12%/23017d); STREET_ADDRESS=ADDRESS(100.0%/48440d); ZIP_CODE=ZIP(100.0%/13948d); NAICS_CODE=NAICS(100.0%/997d); NAICS_YEAR=NAICS(100.0%/4d) |
| fed_osha_ita_case_detail_2023 | EIN,STATE,ZIP | EIN,NAICS,ZIP,ADDRESS,NAME | STEEL | ESTABLISHMENT_NAME=NAME(99.99%/26090d); EIN=EIN(91.15%/11377d); COMPANY_NAME=NAME(94.27%/12050d); STREET_ADDRESS=ADDRESS(100.0%/25932d); ZIP_CODE=ZIP(95.34%/10251d); NAICS_CODE=NAICS(100.0%/641d); NAICS_YEAR=NAICS(99.85%/3d) |
| fed_osha_ita_case_detail_2024 | EIN,STATE,ZIP | EIN,NAICS,ZIP,ADDRESS,NAME | STEEL | ESTABLISHMENT_NAME=NAME(99.99%/23791d); EIN=EIN(91.42%/9609d); COMPANY_NAME=NAME(94.77%/10297d); STREET_ADDRESS=ADDRESS(100.0%/23228d); ZIP_CODE=ZIP(91.52%/8919d); NAICS_CODE=NAICS(100.0%/644d); NAICS_YEAR=NAICS(100.0%/3d) |
| fed_osha_ita_case_detail_2025 | EIN,STATE,ZIP | EIN,NAICS,ZIP,ADDRESS,NAME | STEEL | ESTABLISHMENT_NAME=NAME(100.0%/17980d); EIN=EIN(88.73%/8344d); COMPANY_NAME=NAME(93.78%/10081d); STREET_ADDRESS=ADDRESS(100.0%/17715d); ZIP_CODE=ZIP(92.26%/8003d); NAICS_CODE=NAICS(100.0%/623d); NAICS_YEAR=NAICS(100.0%/3d); UNEXPECTED_NAICS_SOC_COMBO=NAICS(100.0%/2d) |
| fed_retraction_watch | (empty) | COUNTRY | GEO | COUNTRY=COUNTRY(99.7%/2865d) |
| fed_sam_exclusions | COUNTRY,STATE,UEI,ZIP | UEI,COUNTRY,ZIP,NAME | STEEL | UEI=UEI(35.64%/2959d); ENTITY_NAME=NAME(100.0%/8023d); FIRST_NAME=NAME(75.33%/2416d); MIDDLE_NAME=NAME(39.24%/1250d); LAST_NAME=NAME(75.32%/3420d); ZIP=ZIP(94.63%/2746d); COUNTRY=COUNTRY(99.98%/61d) |
| fed_sec_13f_filers | ACCESSION_NUMBER | ZIP,NAME | GEO | FILINGMANAGER_NAME=NAME(100.0%/13806d); FILINGMANAGER_ZIPCODE=ZIP(86.64%/3042d) |
| fed_sec_13f_submissions | ACCESSION_NUMBER,CIK | CIK | STEEL | CIK=CIK(100.0%/13223d) |
| fed_sec_business_development_company_report | CIK,STATE,ZIP | CIK,ZIP,ADDRESS,NAME | STEEL | CIK=CIK(100.0%/211d); REGISTRANT_NAME=NAME(100.0%/209d); ADDRESS_1=ADDRESS(100.0%/148d); ADDRESS_2=ADDRESS(53.77%/77d); ZIP_CODE=ZIP(98.58%/90d) |
| fed_sec_closed_end_fund_information | CIK,STATE,ZIP | CIK,ZIP,ADDRESS,NAME | STEEL | CIK=CIK(100.0%/962d); REGISTRANT_NAME=NAME(100.0%/964d); ADDRESS_1=ADDRESS(100.0%/415d); ADDRESS_2=ADDRESS(50.57%/195d); ZIP_CODE=ZIP(98.15%/228d) |
| fed_sec_dera_sub_2024q1 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/5545d); NAME=NAME(100.0%/5553d); SIC=SIC(97.5%/387d); EIN=EIN(76.89%/4221d) |
| fed_sec_dera_sub_2024q2 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/6297d); NAME=NAME(100.0%/6240d); SIC=SIC(97.81%/398d); EIN=EIN(75.88%/4791d) |
| fed_sec_dera_sub_2024q3 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/6106d); NAME=NAME(100.0%/6085d); SIC=SIC(97.54%/391d); EIN=EIN(77.47%/4712d) |
| fed_sec_dera_sub_2024q4 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/5921d); NAME=NAME(100.0%/5839d); SIC=SIC(97.4%/393d); EIN=EIN(79.0%/4663d) |
| fed_sec_dera_sub_2025q1 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/5666d); NAME=NAME(100.0%/5672d); SIC=SIC(97.22%/390d); EIN=EIN(75.53%/4381d) |
| fed_sec_dera_sub_2025q2 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/6090d); NAME=NAME(100.0%/6037d); SIC=SIC(97.46%/392d); EIN=EIN(73.95%/4550d) |
| fed_sec_dera_sub_2025q3 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/5973d); NAME=NAME(100.0%/5900d); SIC=SIC(97.37%/393d); EIN=EIN(75.51%/4522d) |
| fed_sec_dera_sub_2025q4 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/5795d); NAME=NAME(100.0%/5744d); SIC=SIC(96.95%/393d); EIN=EIN(77.27%/4514d) |
| fed_sec_dera_sub_2026q1 | CIK,EIN | CIK,EIN,SIC,NAME | STEEL | CIK=CIK(100.0%/5774d); NAME=NAME(100.0%/5704d); SIC=SIC(97.05%/387d); EIN=EIN(73.45%/4217d) |
| fed_sec_edgar_insiders | ACCESSION_NUMBER,CIK | CIK | STEEL | CIK=CIK(100.0%/5177d) |
| fed_sec_money_market_fund_information | (empty) | CIK,NAME | STEEL | REGISTRANT_CIK=CIK(100.0%/175d); SERIES_NAME=NAME(100.0%/298d); CLASS_NAME=NAME(100.0%/389d) |
| fed_senate_lda_filings | (empty) | COUNTRY,NAME | GEO | REGISTRANT_NAME=NAME(100.0%/4843d); REGISTRANT_COUNTRY=COUNTRY(100.0%/13d); CLIENT_NAME=NAME(100.0%/16656d); CLIENT_COUNTRY=COUNTRY(98.82%/80d) |
| intl_gleif_repex | LEI | LEI | STEEL | LEI=LEI(100.0%/50375d) |
| irs527_8871_orgs | (empty) | EIN,ZIP,ADDRESS,NAME | STEEL | EIN=EIN(100.0%/39239d); ORGANIZATION_NAME=NAME(100.0%/40592d); MAILING_ZIP=ZIP(100.0%/12690d); EMAIL_ADDRESS=ADDRESS(100.0%/27284d); CUSTODIAN_NAME=NAME(100.0%/32648d); CUSTODIAN_ZIP=ZIP(100.0%/12389d); CONTACT_NAME=NAME(100.0%/32545d); CONTACT_ZIP=ZIP(100.0%/12461d); BUSINESS_ZIP=ZIP(99.98%/12785d) |
| irs527_8872_reports | (empty) | EIN,ZIP,ADDRESS,NAME | STEEL | CHANGE_OF_ADDRESS_IND=ADDRESS(100.0%/2d); ORGANIZATION_NAME=NAME(100.0%/4320d); EIN=EIN(100.0%/4045d); MAILING_ZIP=ZIP(100.0%/2752d); EMAIL_ADDRESS=ADDRESS(100.0%/4046d); CUSTODIAN_NAME=NAME(100.0%/4699d); CUSTODIAN_ZIP=ZIP(99.85%/2795d); CONTACT_NAME=NAME(100.0%/4784d); CONTACT_ZIP=ZIP(100.0%/2819d); BUSINESS_ZIP=ZIP(99.99%/2817d) |
| irs527_directors_officers | (empty) | EIN,ZIP,NAME | STEEL | ORG_NAME=NAME(100.0%/26673d); EIN=EIN(100.0%/26885d); ENTITY_NAME=NAME(99.97%/36058d); ENTITY_ZIP=ZIP(99.99%/11434d) |
| irs527_related_entities | (empty) | EIN,ZIP,NAME | STEEL | ORG_NAME=NAME(100.0%/7977d); EIN=EIN(100.0%/7502d); ENTITY_NAME=NAME(99.9%/9117d); ENTITY_ZIP=ZIP(100.0%/3742d) |
| xc_epa_corporate_crosswalk | (empty) | FRS_ID,LEI,UEI,NAME | STEEL | EPA_REGISTRY_ID=FRS_ID(100.0%/48853d); FACILITY_NAME=NAME(99.87%/47605d); MATCHED_LEI=LEI(1.38%/613d); MATCHED_LEGAL_NAME=NAME(1.38%/613d); PARENT_LEGAL_NAME=NAME(1.38%/604d); PARENT_UEI=UEI(0.66%/329d) |
| xc_mapping_police_violence | STATE,ZIP | LATLON,ZIP,ADDRESS,NAME | GEO | VICTIM_S_NAME=NAME(100.0%/14862d); STREET_ADDRESS_OF_INCIDENT=ADDRESS(97.07%/14367d); ZIPCODE=ZIP(99.04%/8044d); LATITUDE=LATLON(93.51%/13974d); LONGITUDE=LATLON(93.51%/14209d); CONGRESSIONAL_REPRESENTATIVE_FULL_NAME_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES=NAME(94.92%/441d) |
| xc_uk_sanctions_list | (empty) | ADDRESS,NAME | PROBABILISTIC | NAME_6=NAME(99.8%/9830d); NAME_1=NAME(41.58%/2172d); NAME_2=NAME(21.15%/1493d); NAME_3=NAME(4.41%/314d); NAME_4=NAME(0.81%/72d); NAME_TYPE=NAME(99.89%/3d); NAME_NON_LATIN_SCRIPT=NAME(1.64%/197d); REGIME_NAME=NAME(100.0%/31d); ADDRESS_LINE_1=ADDRESS(56.16%/1589d); ADDRESS_LINE_2=ADDRESS(35.94%/904d); ADDRESS_LINE_3=ADDRESS(21.99%/481d); ADDRESS_LINE_4=ADDRESS(9.19%/230d); ADDRESS_LINE_5=ADDRESS(13.31%/294d); ADDRESS_LINE_6=ADDRESS(65.95%/538d); ADDRESS_POSTAL_CODE=ADDRESS(19.6%/630d) |
| xc_un_consolidated_sanctions_list | (empty) | ADDRESS,NAME | PROBABILISTIC | FIRST_NAME=NAME(100.0%/820d); SECOND_NAME=NAME(71.91%/593d); INDIVIDUAL_ADDRESS=ADDRESS(72.8%/237d); THIRD_NAME=NAME(34.03%/280d); FOURTH_NAME=NAME(16.82%/130d); ENTITY_ADDRESS=ADDRESS(27.2%/143d) |

## SKIP -- provisional but no key survived value-measurement

| source_id | name-detected but rejected |
|---|---|
| FED_FDA_CAERS | (no key-named columns) |
| FED_FDA_DEVICE_510K | (no key-named columns) |
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
| INT_GLEIF_RR | (no key-named columns) |
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
| fed_courtlistener_financial_disclosures | (no key-named columns) |
| fed_courtlistener_investments | (no key-named columns) |
| fed_cpsc_neiss | (no key-named columns) |
| fed_david_rumsey | (no key-named columns) |
| fed_densho_ddr | FIPS=FIPS(0.0%/0d) |
| fed_dhs_yearbook | COUNTRY_OF_BIRTH=COUNTRY(0.0%/0d); COUNTRY_OF_LAST_RESIDENCE=COUNTRY(0.0%/0d); TABLE_NAME=NAME(0.0%/0d) |
| fed_docsouth | (no key-named columns) |
| fed_doj_crt_cases | COMPANY_ID=NAME(0.0%/0d); PERSON_NAME=NAME(0.0%/0d) |
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
| fed_epa_npdes_npdes_cs_violations | (no key-named columns) |
| fed_epa_npdes_npdes_formal_enforcement_actions | (no key-named columns) |
| fed_epa_npdes_npdes_ps_violations | (no key-named columns) |
| fed_epa_npdes_npdes_qncr_history | (no key-named columns) |
| fed_epa_npdes_npdes_se_violations | (no key-named columns) |
| fed_faa_data_portal | DATASET_NAME=NAME(100.0%/3d); FIPS=FIPS(0.0%/0d); LAT=LATLON(0.0%/0d); LON=LATLON(0.0%/0d) |
| fed_fbi_cde | AGENCY_NAME=NAME(0.0%/0d); FIPS_STATE_CODE=FIPS(0.0%/0d); FIPS_COUNTY_CODE=FIPS(0.0%/0d); OFFENSE_NAME=NAME(0.0%/0d) |
| fed_fbi_nics_checks | (no key-named columns) |
| fed_fda_faers_drug | (no key-named columns) |
| fed_fda_faers_indi | (no key-named columns) |
| fed_fda_faers_outc | (no key-named columns) |
| fed_fda_faers_reac | (no key-named columns) |
| fed_ffiec_call_reports | INSTITUTION_NAME=NAME(0.0%/0d) |
| fed_fincen_boi | REPORTING_COMPANY_NAME=NAME(100.0%/1d); EIN=EIN(0.0%/0d); BENEFICIAL_OWNER_FULL_NAME=NAME(0.0%/0d); BENEFICIAL_OWNER_ADDRESS=ADDRESS(0.0%/0d) |
| fed_foreignassistance | COUNTRY=COUNTRY(0.0%/0d); EIN=EIN(0.0%/0d) |
| fed_fra_safety | RAILROAD_NAME=NAME(100.0%/1d); STATE_FIPS=FIPS(100.0%/1d); COUNTY_FIPS=FIPS(100.0%/1d) |
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
| fed_sec_edgar_company_tickers_exchange | (no key-named columns) |
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
| intl_gleif_relationships | (no key-named columns) |
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
- fed_cms_dialysis (CCN,STATE,ZIP / STEEL)
- fed_cms_facility_affiliation (CCN,NPI / STEEL)
- fed_cms_hcris (CCN,COUNTY,STATE,ZIP / STEEL)
- fed_cms_home_health (CCN,STATE,ZIP / STEEL)
- fed_cms_hospice (CCN,STATE,ZIP / STEEL)
- fed_cms_hospital_compare (STATE,ZIP / GEO)
- fed_cms_hospital_general (CCN,STATE,ZIP / STEEL)
- fed_cms_irf (CCN,STATE,ZIP / STEEL)
- fed_cms_ltch (CCN,STATE,ZIP / STEEL)
- fed_cms_medicare_provider (NPI / STEEL)
- fed_cms_nppes (NPI / STEEL)
- fed_cms_nursing_home (ADDRESS,CCN,FIPS,LATLON,NAME,NPI,ZIP / STEEL)
- fed_cms_open_payments (CCN,NPI / STEEL)
- fed_cms_open_payments_2022 (CCN,NPI / STEEL)
- fed_cms_open_payments_2023 (CCN,NPI / STEEL)
- fed_cms_part_d_prescribers (NPI,STATE / STEEL)
- fed_cms_pos_other (CCN / STEEL)
- fed_congress_committee_membership (BIOGUIDE / STEEL)
- fed_congress_legislators (BIOGUIDE,ICPSR,STATE / STEEL)
- fed_dhs_ohss (NAME / PROBABILISTIC)
- fed_doj_epstein_library (none / NONE)
- fed_dol_form5500 (EIN,ZIP,NAME / STEEL)
- fed_dol_oflc (NAICS,COUNTRY,ZIP,NAME / STRONG)
- fed_dot_bts (NAME / PROBABILISTIC)
- fed_eac_eavs (STATE / GEO)
- fed_ed_edfacts (NAME / PROBABILISTIC)
- fed_epa_echo (COUNTY,FIPS,FRS_ID,STATE,ZIP / STEEL)
- fed_faa_registry (COUNTY,STATE,ZIP / GEO)
- fed_fara (NAME / PROBABILISTIC)
- fed_fara_bulk (STATE,ZIP / GEO)
- fed_fcc_licensing (STATE,ZIP / GEO)
- fed_fdic_enforcement (none / NONE)
- fed_fdic_failed_banks (FIPS,NAME / GEO)
- fed_fec_bulk (FEC_CMTE_ID,FEC_CAND_ID / STEEL)
- fed_fec_bulk_candidates (FEC_ID / STEEL)
- fed_fec_bulk_committees (FEC_CMTE_ID,FEC_CAND_ID / STEEL)
- fed_fec_bulk_summary (FEC_ID / STEEL)
- fed_fec_committee_to_candidate (FEC_ID,STATE,ZIP / STEEL)
- fed_fec_indiv_contributions (FEC_ID,STATE,ZIP / STEEL)
- fed_fhfa_hpi (NAME / PROBABILISTIC)
- fed_fhfa_nmdb (NAME / PROBABILISTIC)
- fed_fjc_judges (none / STRONG)
- fed_fjc_service (none / STRONG)
- fed_ftc_datasets (NAME / PROBABILISTIC)
- fed_govinfo_bill_cosponsors (BIOGUIDE / STEEL)
- fed_govinfo_billstatus (BIOGUIDE / STEEL)
- fed_hhs_oig_leie (NPI,STATE,ZIP / STEEL)
- fed_hrsa_shortage_areas (STATE / GEO)
- fed_hud_data (NAME / PROBABILISTIC)
- fed_ice_statistics (COUNTRY / GEO)
- fed_irs_990 (EIN / STEEL)
- fed_irs_bmf (EIN,STATE,ZIP / STEEL)
- fed_irs_revocation (COUNTRY,EIN,STATE,ZIP / STEEL)
- fed_irs_soi (FIPS,STATE,ZIP / GEO)
- fed_mapping_inequality (STATE / GEO)
- fed_medsl_house_returns (FIPS,STATE / GEO)
- fed_medsl_president_returns (FIPS,STATE / GEO)
- fed_medsl_senate_returns (FIPS,STATE / GEO)
- fed_nara_aad (FIPS / GEO)
- fed_nara_wra_aad (FIPS / GEO)
- fed_nasa_open_data (NAME / PROBABILISTIC)
- fed_ncua_call_reports (STATE,ZIP / GEO)
- fed_noaa_ais (IMO / STEEL)
- fed_noaa_storm_events (FIPS,STATE / GEO)
- fed_noaa_weather_api (GEOM,NAME / GEO)
- fed_nsf_awards (STATE,ZIP / GEO)
- fed_nursinghome411 (CCN,LATLON,ADDRESS,NAME / STEEL)
- fed_ofac_sdn (IMO / STEEL)
- fed_oyez (DOCKET,NAME / STRONG)
- fed_pbgc_data (STATE / GEO)
- fed_revolvingdoor_project (NAME / PROBABILISTIC)
- fed_sba_loans (ZIP,ADDRESS,NAME / GEO)
- fed_scdb (DOCKET_ID / STEEL)
- fed_sec_edgar (CIK,EIN / STEEL)
- fed_sec_edgar_company_tickers (CIK / STEEL)
- fed_sec_edgar_financials (CIK,EIN / STEEL)
- fed_senate_stock_watcher (none / PROBABILISTIC)
- fed_treasury_avg_interest_rates (none / NONE)
- fed_treasury_debt_to_penny (none / NONE)
- fed_us_sec_edgar (ACCESSION_NUMBER,CIK,EIN / STEEL)
- fed_us_usaspending_api (NAME / PROBABILISTIC)
- fed_usaspending_contracts (STATE,UEI / STEEL)
- fed_usaspending_toptier_agencies (NAME / PROBABILISTIC)
- fed_usgs_earthquakes (LATLON / GEO)
- fed_usgs_minerals (STATE / GEO)
- fed_usgs_water (LATLON,NAME / GEO)
- fed_voteview_members (BIOGUIDE,ICPSR / STEEL)
- fed_voteview_rollcalls (ICPSR / STEEL)
- fed_wpa_slave_narratives (STATE / GEO)
- intl_adb_data (NAME / PROBABILISTIC)
- intl_ar_datosgob (NAME / PROBABILISTIC)
- intl_ch_zefix (ADDRESS,COUNTRY,NAME / GEO)
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
- intl_global_witness_defenders (COUNTRY / GEO)
- intl_gr_gemi (NAME / PROBABILISTIC)
- intl_hudoc (COUNTRY / GEO)
- intl_ie_cro (NAME / PROBABILISTIC)
- intl_ipc_food_insecurity_global (COUNTRY / GEO)
- intl_it_istat (COUNTRY / GEO)
- intl_nti_cns_dprk_missile_tests (LATLON,NAME / GEO)
- intl_opensanctions (NAME / PROBABILISTIC)
- intl_ucdp_ged (COUNTRY,GEOM,LATLON,NAME / GEO)
- intl_wb_ids (COUNTRY,NAME / GEO)
- st_cannabis_policy_bundles (FIPS,STATE / GEO)
- xc_jcs_coa (NAME / PROBABILISTIC)
- xc_jcs_scotus (none / STEEL)
- xc_ransomwarelive_victims (COUNTRY,NAME / GEO)
- xc_vera_incarceration_trends (COUNTY,FIPS,STATE / GEO)
- xc_wapo_fatal_force (COUNTY,STATE / GEO)
- xc_wayback_doj_epstein (none / NONE)
- xc_wayback_replay_doj_deep_pages (none / NONE)
- xc_wayback_replay_doj_listing (none / NONE)
- xc_wikipedia_largest_us_companies (NAME / PROBABILISTIC)

## No physical LANDING table (2)

- fed_dea_arcos (modeled)
- intl_uk_companies_house (modeled)

## No SOURCE_REGISTRY row (55)

- fed_atf_ffl (modeled)
- fed_cfpb_hmda_historic (landed)
- fed_eia860_1_utility (landed)
- fed_eia860_2_plant (landed)
- fed_eia860_3_1_generator (landed)
- fed_eia860_3_2_wind (landed)
- fed_eia860_3_3_solar (landed)
- fed_eia860_3_4_energy_storage (landed)
- fed_eia860_3_5_multifuel (landed)
- fed_eia860_4_owner (landed)
- fed_eia860_6_1_enviroassoc (landed)
- fed_eia860_6_2_enviroequip (landed)
- fed_eia861_advanced_meters (landed)
- fed_eia861_balancing_authority (landed)
- fed_eia861_delivery_companies (landed)
- fed_eia861_demand_response (landed)
- fed_eia861_distribution_systems (landed)
- fed_eia861_dynamic_pricing (landed)
- fed_eia861_energy_efficiency (landed)
- fed_eia861_frame (landed)
- fed_eia861_mergers (landed)
- fed_eia861_net_metering (landed)
- fed_eia861_non_net_metering_distributed (landed)
- fed_eia861_operational_data (landed)
- fed_eia861_reliability (landed)
- fed_eia861_sales_ult_cust (landed)
- fed_eia861_sales_ult_cust_cs (landed)
- fed_eia861_service_territory (landed)
- fed_eia861_short_form (landed)
- fed_eia861_utility_data (landed)
- fed_epa_frs_frs_facilities (landed)
- fed_epa_ghgrp_emission (landed)
- fed_epa_ghgrp_facility (landed)
- fed_fda_gudid__staging (landed)
- fed_fema_ia_housing_registrations (landed)
- fed_fhfa_suspended_counterparty (landed)
- fed_fracfocus_disclosure_list (landed)
- fed_fracfocus_registry (landed)
- fed_fracfocus_water_source (landed)
- fed_hrsa_npdb (modeled)
- fed_ice_detention_facility_codes (landed)
- fed_irs_527_orgs (landed)
- fed_jpml_pending_mdl (landed)
- fed_occ_national_banks (landed)
- fed_occ_thrifts (landed)
- icij_offshore_leaks_addresses (landed)
- icij_offshore_leaks_entities (landed)
- icij_offshore_leaks_intermediaries (landed)
- icij_offshore_leaks_officers (landed)
- icij_offshore_leaks_relationships (landed)
- intl_opensanctions_default (landed)
- intl_uk_sanctions_list (landed)
- intl_un_consolidated_sanctions (landed)
- state_oehha_prop65_chemicals (landed)
- uk_companies_house_psc (landed)