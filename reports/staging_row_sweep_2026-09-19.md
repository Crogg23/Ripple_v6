# Staging row sweep, 2026-09-19

What was checked: every staging model file was read for its landing table and its dedupe rule.
The view in LIBRARY_STAGING.DBT_CROGERS was counted and compared to the landing row count.
Second pass: distinct load run ids per landing table, to separate a double load from a rule that hides rows.

A hit (view short, one load): rows that arrived in one file were collapsed by the dedupe rule.
Not checked: whether the collapsed rows are true copies or different records. Small shares may be true copies.
A miss (view equals landing): the rule is right for this load. It cannot see a landing table that is itself a double load.

Full rows: staging_row_sweep_2026-09-19_all.tsv. Short views with load counts: staging_row_sweep_2026-09-19_short.tsv.

## One load, view short of landing, worst first

| view | landing rows | view rows | hidden | share | dedupe rule |
|---|---:|---:|---:|---:|---|
| STG_PORTAL_CKA_CALIFORNIA_OPEN_0AD648012F__RECORDS | 1,999,247 | 44,664 | 1,954,583 | 97.8% | station_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ANALYZE_BOSTON_E4C004D662__CASES | 2,000,000 | 50,863 | 1,949,137 | 97.5% | case_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_CALIFORNIA_OPEN_AC6C9E2B47__RECORDS | 1,976,268 | 47,643 | 1,928,625 | 97.6% | stn_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_INDIANA_DATA_HUB_83BA6435C2__PLACES | 980,219 | 126,295 | 853,924 | 87.1% | location_id, date order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_TEXAS_OPEN_DATA_A415622C5D__PLACES | 1,426,095 | 1,076,829 | 349,266 | 24.5% | loc_zip, permit_date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_DDB61776D0__RECORDS | 195,963 | 19,244 | 176,719 | 90.2% | inspection_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_49ED6437BF__RECORDS | 195,963 | 19,244 | 176,719 | 90.2% | inspection_id order by _loaded_at desc) = 1 |
| STG_FED_FARA_BULK__FARA_REGISTRATIONS | 221,900 | 48,103 | 173,797 | 78.3% | registration_number, |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_0AF7431C6C__FACILITIES | 177,741 | 13,904 | 163,837 | 92.2% | state_county_fips_code, reporting_year, zip_code, primary_sic_code, tr |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_DE448D04D4__FACILITIES | 177,741 | 13,904 | 163,837 | 92.2% | state_county_fips_code, reporting_year, zip_code, primary_sic_code, tr |
| STG_PORTAL_SOC_TEXAS_OPEN_DATA_5410A1009F__PLACES | 884,342 | 737,577 | 146,765 | 16.6% | outlet_zip_code, outlet_permit_issue_date order by _loaded_at desc) =  |
| STG_PORTAL_CKA_INDIANA_DATA_HUB_FE00D42ACC__PLACES | 216,533 | 82,404 | 134,129 | 61.9% | fips, date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_58B0401C9A__PLACES | 197,984 | 98,224 | 99,760 | 50.4% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_COLORADO_INFORMA_DE6C8A6901__PLACES | 2,000,000 | 1,930,299 | 69,701 | 3.5% | county_fips, fiscal_year, start_date, exit_date, state_id, state_id_co |
| STG_FED_DEA_ARCOS_FULL__ORGANIZATIONS | 178,598,026 | 178,545,073 | 52,953 | 0.0% | reporter_dea_no, transaction_date, transaction_code, drug_code, transa |
| STG_PORTAL_SOC_DATALA_LOS_ANGEL_361B8161B7__PLACES | 1,433,580 | 1,384,880 | 48,700 | 3.4% | mailing_zip_code, location_start_date, location_end_date, zip_code ord |
| STG_FED_EPA_SDWA_SDWA_SITE_VISITS__FACILITIES | 2,495,249 | 2,447,708 | 47,541 | 1.9% | pwsid, visit_date, first_reported_date, last_reported_date order by _l |
| STG_CA_LOBBY_COVER__FILINGS | 568,988 | 524,828 | 44,160 | 7.8% | filing_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_F40C1F2ECE__PLACES | 78,400 | 39,008 | 39,392 | 50.2% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_68A8A0027A__PLACES | 54,088 | 27,045 | 27,043 | 50.0% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_54998E6EDA__PLACES | 54,088 | 27,045 | 27,043 | 50.0% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_440A699A5B__PLACES | 53,636 | 26,721 | 26,915 | 50.2% | dataspatial_wkb order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_B1E95C9745__PLACES | 53,636 | 26,721 | 26,915 | 50.2% | dataspatial_wkb order by _loaded_at desc) = 1 |
| STG_FED_USASPENDING_CONTRACTS__ORGANIZATIONS | 6,325,622 | 6,299,122 | 26,500 | 0.4% | recipient_uei, action_date, period_of_performance_start_date, period_o |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_7880B791DF__PLACES | 49,574 | 24,788 | 24,786 | 50.0% | geoid20 order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_CC3BD4AFC2__PLACES | 49,574 | 24,788 | 24,786 | 50.0% | geoid20 order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_CALIFORNIA_OPEN_35E42B9770__RECORDS | 87,244 | 63,112 | 24,132 | 27.7% | org_id, water_system_id, report_period_start_date order by _loaded_at  |
| STG_XC_UK_SANCTIONS_LIST__DESIGNATIONS | 57,883 | 33,828 | 24,055 | 41.6% | _SRC_SHA256, |
| STG_FED_EPA_ECHO__RECORDS | 3,157,891 | 3,135,554 | 22,337 | 0.7% | frs_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_EAC54ADE9A__PLACES | 43,040 | 21,521 | 21,519 | 50.0% | dataspatial_wkb order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_99DBBB9235__PLACES | 43,040 | 21,521 | 21,519 | 50.0% | dataspatial_wkb order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_OPEN_DATA_BR_6083BC2934__RECORDS | 199,821 | 178,879 | 20,942 | 10.5% | lot_id order by _loaded_at desc) = 1 |
| STG_FED_IRS_AUTO_REVOCATIONS__ORGANIZATIONS | 1,207,295 | 1,187,976 | 19,319 | 1.6% | ein order by _loaded_at desc) = 1 |
| STG_FED_IRS_REVOCATION__ORGANIZATIONS | 1,206,628 | 1,187,367 | 19,261 | 1.6% | ein order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_4E5C66124A__PLACES | 38,625 | 19,621 | 19,004 | 49.2% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_C4D59225CB__PLACES | 38,625 | 19,621 | 19,004 | 49.2% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_CALIFORNIA_OPEN_27DC9C9E51__PLACES | 41,291 | 23,326 | 17,965 | 43.5% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_039AACD655__RECORDS | 33,780 | 16,136 | 17,644 | 52.2% | id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_90A0A8B740__RECORDS | 96,713 | 79,235 | 17,478 | 18.1% | parcel_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_1BA8209338__RECORDS | 96,713 | 79,235 | 17,478 | 18.1% | parcel_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_CALIFORNIA_OPEN_F406AAD424__PLACES | 34,527 | 18,058 | 16,469 | 47.7% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_DATALA_LOS_ANGEL_DC3670AFE1__PLACES | 633,782 | 617,861 | 15,921 | 2.5% | mailing_zip_code, location_start_date, zip_code order by _loaded_at de |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_010A1B6275__PLACES | 29,348 | 14,675 | 14,673 | 50.0% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_FA5C68D20D__PLACES | 29,348 | 14,675 | 14,673 | 50.0% | geometry order by _loaded_at desc) = 1 |
| STG_FED_CONGRESS_COMMITTEE_MEMBERSHIP__PEOPLE | 26,971 | 12,401 | 14,570 | 54.0% | bioguide, committee_code order by _loaded_at desc) = 1 |
| STG_FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS__RECORDS | 499,113 | 489,215 | 9,898 | 2.0% | pgm_sys_id, activity_id order by _loaded_at desc) = 1 |
| STG_FED_EPA_FRS_FRS_PROGRAM_LINKS__RECORDS | 4,406,498 | 4,396,854 | 9,644 | 0.2% | pgm_sys_id order by _loaded_at desc) = 1 |
| STG_FED_MAPPING_INEQUALITY__HOLC_NEIGHBORHOOD_GRADES | 10,154 | 1,155 | 8,999 | 88.6% | holc_neighborhood_key |
| STG_PORTAL_ARC_OPEN_DATA_DC_ADF4F0E413__PLACES | 20,292 | 12,729 | 7,563 | 37.3% | safegraph_place_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_6A4C3E0E78__RECORDS | 7,921 | 1,001 | 6,920 | 87.4% | inspection_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_DA448E7083__RECORDS | 7,921 | 1,001 | 6,920 | 87.4% | inspection_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_TEXAS_OPEN_DATA_354E3ABF4F__PLACES | 42,272 | 36,066 | 6,206 | 14.7% | site_zip_cd, nor_registration_date order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_SEATTLE_OPEN_DAT_C8F2072189__PLACES | 84,399 | 79,726 | 4,673 | 5.5% | zip, license_start_date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_HOUSTON_OPEN_DAT_A4490182BA__PLACES | 196,552 | 192,026 | 4,526 | 2.3% | zipcode, sr_create_date, due_date, date_closed, tax_id order by _loade |
| STG_PORTAL_CKA_INDIANA_DATA_HUB_D4DAE8D984__PLACES | 16,502 | 12,806 | 3,696 | 22.4% | zipcode, year, age_group order by _loaded_at desc) = 1 |
| STG_FED_EPA_SDWA_SDWA_LCR_SAMPLES__RECORDS | 927,415 | 923,863 | 3,552 | 0.4% | sar_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_D7DA51769C__RECORDS | 37,982 | 34,922 | 3,060 | 8.1% | parcel_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_CDA9E537DC__RECORDS | 37,982 | 34,922 | 3,060 | 8.1% | parcel_id order by _loaded_at desc) = 1 |
| STG_FED_FEC_PAC_SUMMARY__RECORDS | 48,395 | 45,709 | 2,686 | 5.6% | cmte_id, cvg_end_dt |
| STG_FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS__RECORDS | 478,855 | 477,288 | 1,567 | 0.3% | activity_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_E90902C24C__PLACES | 21,880 | 20,347 | 1,533 | 7.0% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_TEXAS_OPEN_DATA_DA657010B1__PLACES | 34,753 | 33,645 | 1,108 | 3.2% | loc_zip, resp_begin_date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_F82E02E6B2__RECORDS | 22,674 | 21,684 | 990 | 4.4% | ev_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_FA3191E7A1__RECORDS | 22,674 | 21,684 | 990 | 4.4% | ev_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ANALYZE_BOSTON_D5A9AD584E__FILINGS | 36,729 | 35,768 | 961 | 2.6% | zip_code, permit_application_filing_date, permit_issued_date, rezoning |
| STG_FED_EPA_TRI_BASIC_2023__FACILITIES | 78,647 | 77,783 | 864 | 1.1% | c_3_frs_id, c_1_year, c_22_industry_sector_code, c_23_industry_sector, |
| STG_FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS__RECORDS | 106,009 | 105,186 | 823 | 0.8% | pgm_sys_id, activity_id order by _loaded_at desc) = 1 |
| STG_FED_USACE_NID_DAMS__RECORDS | 92,766 | 91,979 | 787 | 0.8% | nid_id order by _loaded_at desc) = 1 |
| STG_FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS__RECORDS | 260,556 | 259,861 | 695 | 0.3% | activity_id order by _loaded_at desc) = 1 |
| STG_FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES__RECORDS | 1,779,096 | 1,778,462 | 634 | 0.0% | pgm_sys_id, activity_id order by _loaded_at desc) = 1 |
| STG_FED_NARA_AAD__ARCHIVAL_RECORDS | 554 | 9 | 545 | 98.4% | dataset_id, record_id |
| STG_FED_FDIC_FAILED_BANKS__FAILED_BANKS | 4,115 | 3,584 | 531 | 12.9% | fdic_cert |
| STG_INTL_EU_SANCTIONS__PLACES | 42,347 | 41,857 | 490 | 1.2% | addr_zipcode, date_file, leba_publication_date, naal_leba_publication_ |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_AD0D8250DF__PLACES | 27,919 | 27,455 | 464 | 1.7% | latitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_BB1BD78412__PLACES | 27,919 | 27,455 | 464 | 1.7% | latitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_1A89F1526C__PLACES | 45,767 | 45,358 | 409 | 0.9% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_98A0E89FA3__PLACES | 45,767 | 45,358 | 409 | 0.9% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_ED65B530A3__PLACES | 155,765 | 155,373 | 392 | 0.3% | geoid, quarter order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_9CCBEFBACC__PLACES | 155,765 | 155,373 | 392 | 0.3% | geoid, quarter order by _loaded_at desc) = 1 |
| STG_FED_USASPENDING_BULK__ORGANIZATIONS | 50,000 | 49,613 | 387 | 0.8% | recipient_uei, action_date, action_date_fiscal_year, period_of_perform |
| STG_PORTAL_CKA_OPEN_DATA_SA_1E2348F9B1__PLACES | 115,294 | 115,070 | 224 | 0.2% | shape__length order by _loaded_at desc) = 1 |
| STG_XC_RETRACTION_WATCH_DATABASE__RETRACTIONS | 71,608 | 71,388 | 220 | 0.3% | RECORD_ID |
| STG_PORTAL_CKA_ANALYZE_BOSTON_5CCB249B71__RECORDS | 24,727 | 24,527 | 200 | 0.8% | swk_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_B25E480DFC__ASSETS | 32,177 | 32,002 | 175 | 0.5% | asset_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_B9904B63C2__ASSETS | 32,177 | 32,002 | 175 | 0.5% | asset_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_NEW_YORK_STATE_O_EFF72C4402__RECORDS | 65,231 | 65,079 | 152 | 0.2% | project_id_number order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_ATLANTA_DATAATLA_EAD25CBDC7__PLACES | 19,297 | 19,168 | 129 | 0.7% | longitude, business_license_year, date_of_opening_in_atlanta, previous |
| STG_FED_SEC_DERA_SUB_2026Q1__ORGANIZATIONS | 6,169 | 6,049 | 120 | 1.9% | cik, period, fy order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_CALIFORNIA_OPEN_3B70AD4F80__RECORDS | 7,754 | 7,639 | 115 | 1.5% | stn_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_1C37EE3869__PLACES | 8,640 | 8,537 | 103 | 1.2% | shape__length, fiscal_year order by _loaded_at desc) = 1 |
| STG_FED_SEC_DERA_SUB_2025Q4__ORGANIZATIONS | 6,304 | 6,202 | 102 | 1.6% | cik, period, fy order by _loaded_at desc) = 1 |
| STG_FED_HHS_OIG_LEIE__EXCLUSIONS | 83,842 | 83,747 | 95 | 0.1% | exclusion_sk |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_8AE30C65DE__PLACES | 17,550 | 17,455 | 95 | 0.5% | shape_area order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_E2B711DB0F__PLACES | 12,423 | 12,345 | 78 | 0.6% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_INDIANA_DATA_HUB_7747EFE139__RECORDS | 40,577 | 40,501 | 76 | 0.2% | id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_794F17EBE2__PLACES | 5,025 | 4,955 | 70 | 1.4% | shape_area order by _loaded_at desc) = 1 |
| STG_ST_OEHHA_PROPOSITION_65_LIST__CHEMICAL | 1,021 | 952 | 69 | 6.8% | chemical, cas_no |
| STG_PORTAL_ARC_MEMPHIS_OPEN_DAT_9F6F4B2736__CASES | 11,108 | 11,048 | 60 | 0.5% | docket order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_23B8B5B7D2__PLACES | 3,420 | 3,360 | 60 | 1.8% | zip_code, create_date, property_type, inspection_status, parcel_id ord |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_1C103EE2CD__PLACES | 3,420 | 3,360 | 60 | 1.8% | zip_code, create_date, property_type, inspection_status, parcel_id ord |
| STG_PORTAL_CKA_ISRAEL_NATIONAL_07EC1AF377__RECORDS | 3,873 | 3,819 | 54 | 1.4% | deaceased_id, deaceased_date order by _loaded_at desc) = 1 |
| STG_FED_CMS_FACILITY_AFFILIATION__PROVIDERS | 2,260,193 | 2,260,146 | 47 | 0.0% | ccn, npi order by _loaded_at desc) = 1 |
| STG_FED_COURTLISTENER_FINANCIAL_DISCLOSURES__PEOPLE | 70,776 | 70,731 | 45 | 0.1% | person_id, date_created, date_modified, year, id order by _loaded_at d |
| STG_PORTAL_CKA_ISRAEL_NATIONAL_338EF2B642__RECORDS | 185,420 | 185,375 | 45 | 0.0% | fund_id, managing_corporation_legal_id, report_period order by _loaded |
| STG_FED_HHS_TAGGS__GRANT_AWARDS | 45 | 1 | 44 | 97.8% | award_number |
| STG_PORTAL_CKA_ANALYZE_BOSTON_F1B3F76830__PLACES | 9,999 | 9,956 | 43 | 0.4% | contact_zip, status_dttm order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_B5470E08FD__PLACES | 3,000 | 2,958 | 42 | 1.4% | shape_area order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_FAAD5A2133__PLACES | 3,191 | 3,149 | 42 | 1.3% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_FC2228A15B__PLACES | 4,883 | 4,842 | 41 | 0.8% | longitude_d order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_CONNECTICUT_OPEN_FF2B86A533__PLACES | 2,204 | 2,164 | 40 | 1.8% | zip_code, fiscal_year, contract_execution_date order by _loaded_at des |
| STG_INTL_GR_GEMI__GREEK_COMPANIES | 40 | 1 | 39 | 97.5% | gemi_number |
| STG_PORTAL_CKA_ISRAEL_NATIONAL_6C5E40114C__RECORDS | 43,134 | 43,096 | 38 | 0.1% | fund_id, report_period order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_2DFC1ADDEA__PLACES | 7,723 | 7,686 | 37 | 0.5% | decedent_zip, death_date_and_time order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_A4E9CE945B__PLACES | 7,723 | 7,686 | 37 | 0.5% | decedent_zip, death_date_and_time order by _loaded_at desc) = 1 |
| STG_FED_NARA_WRA_AAD__JAPANESE_AMERICAN_RELOCATION_RECORDS | 36 | 1 | 35 | 97.2% | record_id |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_9B3EC4ABB9__PLACES | 12,479 | 12,444 | 35 | 0.3% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_6F76317272__PLACES | 12,479 | 12,444 | 35 | 0.3% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ANALYZE_BOSTON_4EDDC3919B__PLACES | 8,250 | 8,216 | 34 | 0.4% | zip_code, application_date order by _loaded_at desc) = 1 |
| STG_FED_EPA_NPDES_NPDES_SE_VIOLATIONS__RECORDS | 305,478 | 305,445 | 33 | 0.0% | npdes_violation_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ISRAEL_NATIONAL_32CF786F4C__RECORDS | 7,534 | 7,501 | 33 | 0.4% | project_id, building_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_CC6148CB20__PLACES | 5,794 | 5,764 | 30 | 0.5% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_MEMPHIS_OPEN_DAT_3057D84002__CASES | 1,537 | 1,508 | 29 | 1.9% | docket order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_B6D7CBC686__PLACES | 11,243 | 11,214 | 29 | 0.3% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ISRAEL_NATIONAL_E3D369B05F__PLACES | 2,297 | 2,269 | 28 | 1.2% | stn_lat, date_open, date_close order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_OPEN_DATA_BR_C110D5CF59__PLACES | 1,468 | 1,441 | 27 | 1.8% | zip, business_naics_code, resource_type, sub_resource_type, business_i |
| STG_PORTAL_SOC_NEW_YORK_STATE_O_0C94DD2B8A__RECORDS | 1,999 | 1,973 | 26 | 1.3% | npdes_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_424E5A26F3__PLACES | 3,597 | 3,573 | 24 | 0.7% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_C87FA1C650__PLACES | 2,929 | 2,905 | 24 | 0.8% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_4E7D1F0FEA__PLACES | 2,929 | 2,905 | 24 | 0.8% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_2C667A6FC6__PLACES | 99,147 | 99,124 | 23 | 0.0% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_97AD4BC66C__RECORDS | 4,457 | 4,434 | 23 | 0.5% | core_parent_sys_id order by _loaded_at desc) = 1 |
| STG_INTL_ES_BORME__BORME_CORPORATE_ACTS | 25 | 3 | 22 | 88.0% | company_id, country, date, act_type, cve |
| STG_PORTAL_CKA_ANALYZE_BOSTON_A4A4828973__PLACES | 24,022 | 24,000 | 22 | 0.1% | shape_wkt order by _loaded_at desc) = 1 |
| STG_FED_FHFA_SUSPENDED_COUNTERPARTY_PROGRAM__SUSPENDED_COUNTERPARTY | 241 | 222 | 19 | 7.9% | last_name, company |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_51B8DCF278__PLACES | 1,975 | 1,957 | 18 | 0.9% | latitude, start_year, approved_date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_CE7A2694FC__PLACES | 1,975 | 1,957 | 18 | 0.9% | latitude, start_year, approved_date order by _loaded_at desc) = 1 |
| STG_INTL_CH_ZEFIX__COMPANIES | 18 | 1 | 17 | 94.4% | company_id |
| STG_PORTAL_ARC_OPEN_DATA_DC_32AD83D2EC__FACILITIES | 26,559 | 26,542 | 17 | 0.1% | ccn order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_09335A764B__RECORDS | 9,999 | 9,982 | 17 | 0.2% | start_station_id, end_station_id, start_date order by _loaded_at desc) |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_7AF23ACD2F__RECORDS | 9,999 | 9,982 | 17 | 0.2% | start_station_id, end_station_id, start_date order by _loaded_at desc) |
| STG_PORTAL_SOC_COLORADO_INFORMA_6367A44C92__RECORDS | 1,989 | 1,972 | 17 | 0.9% | id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_HOUSTON_OPEN_DAT_07C9C99EB1__EVENTS | 2,216 | 2,200 | 16 | 0.7% | temp_event_id, inspection_date, activity_type, staff_code order by _lo |
| STG_PORTAL_SOC_CONNECTICUT_OPEN_AEB46F6C94__PLACES | 2,125 | 2,109 | 16 | 0.8% | c_9_zip, c_1_year, c_18_industry_sector_code, c_19_industry_sector, c_ |
| STG_PORTAL_CKA_CALIFORNIA_OPEN_490B55C81B__RECORDS | 6,160 | 6,145 | 15 | 0.2% | id order by _loaded_at desc) = 1 |
| STG_FED_USGS_3DEP__PLACES | 5,000 | 4,986 | 14 | 0.3% | shape order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_2A3D59095B__PLACES | 22,668 | 22,654 | 14 | 0.1% | latitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_9BCCE40A0F__PLACES | 3,591 | 3,577 | 14 | 0.4% | shape_length order by _loaded_at desc) = 1 |
| STG_FED_FDIC_ENFORCEMENT__ENFORCEMENT_ORDERS | 14 | 1 | 13 | 92.9% | docket_number, fdic_cert_number, coalesce(person_name, respondent_name |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_5635D41E74__PLACES | 1,411 | 1,398 | 13 | 0.9% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_788CBD21B2__PLACES | 1,701 | 1,688 | 13 | 0.8% | shape_area order by _loaded_at desc) = 1 |
| STG_INTL_GR_DATAGOV__RECORDS | 5,000 | 4,988 | 12 | 0.2% | dataset_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ISRAEL_NATIONAL_EE52E94997__RECORDS | 864 | 852 | 12 | 1.4% | animal_lab_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_03014F9C15__PLACES | 1,246 | 1,234 | 12 | 1.0% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_0D51EC3643__PLACES | 35,792 | 35,780 | 12 | 0.0% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_5A544B8D01__PLACES | 1,336 | 1,324 | 12 | 0.9% | latitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_AD9C79B3A8__PLACES | 35,727 | 35,715 | 12 | 0.0% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_66C519BCCF__FACILITIES | 893 | 881 | 12 | 1.3% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_7F45E582F7__FACILITIES | 851 | 839 | 12 | 1.4% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_FED_FJC_SERVICE__PEOPLE | 4,766 | 4,755 | 11 | 0.2% | seat_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_COLORADO_INFORMA_E80CA7800E__PLACES | 2,000 | 1,989 | 11 | 0.6% | county_fips, exit_date, fiscal_year, start_date, state_id, state_id_co |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_38579BBDBC__FACILITIES | 850 | 839 | 11 | 1.3% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_5C3521189E__FACILITIES | 861 | 850 | 11 | 1.3% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_636FFFDFA2__FACILITIES | 865 | 854 | 11 | 1.3% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A45115B872__FACILITIES | 917 | 906 | 11 | 1.2% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_CDBDD459C0__FACILITIES | 835 | 824 | 11 | 1.3% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ANALYZE_BOSTON_8A02CA5E02__PLACES | 1,382 | 1,372 | 10 | 0.7% | lat order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_846214A7C0__PLACES | 993 | 983 | 10 | 1.0% | shape_area order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A54AA90538__FACILITIES | 896 | 886 | 10 | 1.1% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_FED_FEDERAL_REGISTER_DOCUMENTS__FEDERAL_REGISTER_DOCUMENTS | 485,594 | 485,585 | 9 | 0.0% | document_number |
| STG_PORTAL_CKA_CALIFORNIA_OPEN_A5D78A8B63__PLACES | 1,326 | 1,317 | 9 | 0.7% | latitude, last_modified_date, date_data_refers_to, dwr_gw_site_code or |
| STG_PORTAL_CKA_INDIANA_DATA_HUB_90C2A3CA78__PLACES | 784 | 775 | 9 | 1.1% | zcta order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_6F5FCC229F__FACILITIES | 842 | 833 | 9 | 1.1% | tri_facility_id, frs_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_D5F7CA2621__PLACES | 2,000 | 1,991 | 9 | 0.5% | c_9_zip, c_1_year, c_18_industry_sector_code, c_19_industry_sector, c_ |
| STG_FED_HUD_MF_FIRM_COMMITMENTS__COMMITMENTS | 25,565 | 25,557 | 8 | 0.0% | fha_number_raw, firm_activity_date_raw |
| STG_PORTAL_CKA_OPEN_DATA_SA_19F13722DD__PLACES | 801 | 793 | 8 | 1.0% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_E078D81651__PLACES | 902 | 894 | 8 | 0.9% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_8D9FB9A1A3__FACILITIES | 813 | 805 | 8 | 1.0% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_5E73751281__FACILITIES | 817 | 809 | 8 | 1.0% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A3B79359D3__FACILITIES | 731 | 723 | 8 | 1.1% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_FED_DOJ_FCA_SETTLEMENTS__FCA_SETTLEMENTS | 19 | 12 | 7 | 36.8% | fca_settlement_id |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_F326BAD0FC__FACILITIES | 713 | 706 | 7 | 1.0% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_FED_US_SEC_EDGAR__EDGAR_FILINGS | 48,990 | 48,984 | 6 | 0.0% | accession_number |
| STG_FED_USGS_GNIS_ALL_NAMES__NAME_CITATIONS | 1,249,630 | 1,249,624 | 6 | 0.0% | feature_id, feature_name, citation |
| STG_PORTAL_ARC_VERMONT_OPEN_GEO_62F10327D4__PLACES | 424 | 418 | 6 | 1.4% | latitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_2789EF054E__PLACES | 6,486 | 6,480 | 6 | 0.1% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_F8C410BB6B__PLACES | 1,832 | 1,826 | 6 | 0.3% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_A5715666DA__FACILITIES | 791 | 785 | 6 | 0.8% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_B5E39C25F8__FACILITIES | 835 | 829 | 6 | 0.7% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_FED_FDA_PURPLE_BOOK__LICENSES | 2,233 | 2,228 | 5 | 0.2% | UNNAMED_2, UNNAMED_20, UNNAMED_16 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_4FC22C2C30__PLACES | 427 | 422 | 5 | 1.2% | zip_code, permit_issue_date, permit_expire_date, project_type, parcel_ |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_BB0184F847__PLACES | 427 | 422 | 5 | 1.2% | zip_code, permit_issue_date, permit_expire_date, project_type, parcel_ |
| STG_PORTAL_SOC_AUSTIN_OPEN_DATA_0B4C639A1C__RECORDS | 526 | 521 | 5 | 1.0% | employee_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_TEXAS_OPEN_DATA_6F798A64FA__ORGANIZATIONS | 622,647 | 622,642 | 5 | 0.0% | ein, active_date, appointment_type, naic_id order by _loaded_at desc)  |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_4388C129F2__FACILITIES | 807 | 802 | 5 | 0.6% | tri_facility_id, cas_compound_id order by _loaded_at desc) = 1 |
| STG_FED_IHS_FACILITIES__FACILITIES | 1,010 | 1,006 | 4 | 0.4% | IHS_TRIBAL_URBAN_INDIAN_HEALTH_FACILITIES_LIST_RELEASED_JUNE_2023, UNN |
| STG_FED_REVOLVINGDOOR_PROJECT__PERSONNEL_POSITIONS | 409 | 405 | 4 | 1.0% | position_key |
| STG_INTL_IE_CRO__CRO_COMPANIES | 821,697 | 821,693 | 4 | 0.0% | company_id, country |
| STG_INTL_WB_IDS__PLACES | 62,983 | 62,979 | 4 | 0.0% | country_code, counterpart_area_code, series_code order by _loaded_at d |
| STG_PORTAL_CKA_OPEN_DATA_SA_C7CF87B213__PLACES | 141,213 | 141,209 | 4 | 0.0% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_A8EF161189__PLACES | 6,493 | 6,489 | 4 | 0.1% | shape__length, created_date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_3BB10A6097__PLACES | 263 | 259 | 4 | 1.5% | shape_area order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_77706D86DA__RECORDS | 34,207 | 34,203 | 4 | 0.0% | swc_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_ACE8AC0352__RECORDS | 1,045 | 1,041 | 4 | 0.4% | tmdl_eq_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_COLORADO_INFORMA_1D5CFAD830__PLACES | 2,000 | 1,996 | 4 | 0.2% | county_fips, fiscal_year, start_date, exit_date, state_id, state_id_co |
| STG_FED_CFPB_COMPLAINTS__COMPLAINTS | 17,589,039 | 17,589,036 | 3 | 0.0% | complaint_id |
| STG_FED_OSHA_ITA_300A_SUMMARY_2025__RECORDS | 383,283 | 383,280 | 3 | 0.0% | id order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_OPEN_DATA_DC_008BA480F6__FACILITIES | 1,915 | 1,912 | 3 | 0.2% | ccn order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ANALYZE_BOSTON_9FE0838E9F__PLACES | 968 | 965 | 3 | 0.3% | zipcode, date_business_established, business_type, cob_category_codes1 |
| STG_PORTAL_CKA_ANALYZE_BOSTON_BBE261ACCB__PLACES | 13,747 | 13,744 | 3 | 0.0% | latitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_HOUSTON_OPEN_DAT_5848C85560__RECORDS | 5,060 | 5,057 | 3 | 0.1% | transportation_id, vehicle_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_HOUSTON_OPEN_DAT_76E445329F__RECORDS | 4,308 | 4,305 | 3 | 0.1% | transportation_id, vehicle_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_1F87A7AE2D__PLACES | 8,547 | 8,544 | 3 | 0.0% | shape__length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_151F8E4DBB__PLACES | 30,163 | 30,160 | 3 | 0.0% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_E2E136DBE8__PLACES | 789 | 786 | 3 | 0.4% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_651C0C423A__PLACES | 449 | 446 | 3 | 0.7% | zip_code, starting_date, expiration_date, inserted_date, buffer_id ord |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_305157E72F__PLACES | 1,026 | 1,023 | 3 | 0.3% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_5A83580B83__PLACES | 445 | 442 | 3 | 0.7% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_39AA454DDA__PLACES | 445 | 442 | 3 | 0.7% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_6C8F129AE5__PLACES | 1,026 | 1,023 | 3 | 0.3% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_SF_OPENDATA_DATA_C19EE9EB44__PROVIDERS | 157 | 154 | 3 | 1.9% | npi, program_name order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_F1292B8D2F__ORGANIZATIONS | 249 | 246 | 3 | 1.2% | duns_no, fiscal_year, evaluation_closed_date order by _loaded_at desc) |
| STG_XC_MAPPING_POLICE_VIOLENCE__RECORDS | 15,476 | 15,473 | 3 | 0.0% | mpv_id order by _loaded_at desc) = 1 |
| STG_FED_EIA861_DELIVERY_COMPANIES__SALES | 9 | 7 | 2 | 22.2% | UNNAMED_0, UNNAMED_1, UNNAMED_6, UNNAMED_3, UNNAMED_4 |
| STG_FED_EIA861_ENERGY_EFFICIENCY__PROGRAMS | 460 | 458 | 2 | 0.4% | UNNAMED_0, UNNAMED_1, UNNAMED_3 |
| STG_FED_EIA861_NET_METERING__CAPACITY | 1,006 | 1,004 | 2 | 0.2% | UNNAMED_0, UNNAMED_2, UNNAMED_1, CAPACITY_MW |
| STG_FED_EIA861_SALES_ULT_CUST__SALES | 2,817 | 2,815 | 2 | 0.1% | UNNAMED_0, UNNAMED_1, UNNAMED_6, UNNAMED_3, UNNAMED_4 |
| STG_FED_EIA861_SALES_ULT_CUST_CS__FACILITY_SALES | 676 | 674 | 2 | 0.3% | UNNAMED_0, UNNAMED_1, UNNAMED_3, UNNAMED_5 |
| STG_FED_EIA861_RELIABILITY__RELIABILITY_METRICS | 973 | 971 | 2 | 0.2% | UNNAMED_0, UNNAMED_1, UNNAMED_3 |
| STG_FED_FJC_JUDGES__PEOPLE | 4,067 | 4,065 | 2 | 0.0% | seat_id_1 order by _loaded_at desc) = 1 |
| STG_FED_ICE_DETENTION_FACILITY_LIST__FACILITY | 165 | 163 | 2 | 1.2% | facility_name |
| STG_PORTAL_ARC_ATLANTA_DATAATLA_51A606F539__PLACES | 486 | 484 | 2 | 0.4% | longitude, business_license_year, date_of_opening_in_atlanta, previous |
| STG_PORTAL_ARC_LA_COUNTY_OPEN_D_6DF63A4983__PROVIDERS | 187 | 185 | 2 | 1.1% | npi order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_VERMONT_OPEN_GEO_DE261D6F8C__PLACES | 286 | 284 | 2 | 0.7% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ANALYZE_BOSTON_7D75FD803F__RECORDS | 134 | 132 | 2 | 1.5% | csp_sch_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ANALYZE_BOSTON_899BB82358__PLACES | 572 | 570 | 2 | 0.3% | longitude order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_VERMONT_OPEN_GEO_9E55D67E2C__PLACES | 286 | 284 | 2 | 0.7% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_OPEN_DATA_SA_5B3CE659E5__RECORDS | 108 | 106 | 2 | 1.9% | id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_A02C259ACB__PLACES | 713 | 711 | 2 | 0.3% | shape_area order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_TAMPA_OPEN_DATA_18B980D54D__RECORDS | 952 | 950 | 2 | 0.2% | id, date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_F4FC6168EA__PLACES | 356 | 354 | 2 | 0.6% | shape_area order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_070A16004D__PLACES | 410 | 408 | 2 | 0.5% | zipcode, last_edit_date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_12C9244C06__PLACES | 410 | 408 | 2 | 0.5% | zipcode, last_edit_date order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_TEXAS_OPEN_DATA_D83872D208__CASES | 239 | 237 | 2 | 0.8% | district_court_docket_no, order_date order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_TEXAS_OPEN_DATA_F525266F32__FACILITIES | 474 | 472 | 2 | 0.4% | ccn_no order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_WASHINGTON_STATE_1A95FB1665__ORGANIZATIONS | 112 | 110 | 2 | 1.8% | ubi_ein, audit_closed_date, recipient_type, audit_type order by _loade |
| STG_FED_EIA860_4_OWNER__ALL | 5,496 | 5,495 | 1 | 0.0% | (no dedupe) |
| STG_FED_EIA860_3_1_GENERATOR__ALL | 26,856 | 26,855 | 1 | 0.0% | (no dedupe) |
| STG_FED_EIA860_6_1_ENVIROASSOC__ALL | 7,021 | 7,020 | 1 | 0.0% | (no dedupe) |
| STG_FED_EIA860_6_2_ENVIROEQUIP__ALL | 4,429 | 4,428 | 1 | 0.0% | (no dedupe) |
| STG_FED_EIA861_DYNAMIC_PRICING__ENROLLMENT | 858 | 857 | 1 | 0.1% | UNNAMED_0, UNNAMED_1, UNNAMED_4 |
| STG_FED_EIA861_OPERATIONAL_DATA__OPERATIONS | 1,712 | 1,711 | 1 | 0.1% | UNNAMED_0, UNNAMED_1, UNNAMED_3 |
| STG_FED_EIA861_DEMAND_RESPONSE__PROGRAMS | 340 | 339 | 1 | 0.3% | UNNAMED_0, UNNAMED_1, UNNAMED_3 |
| STG_FED_HRSA_UDS_TABLE3A_PATIENTS__BY_CENTER | 1,357 | 1,356 | 1 | 0.1% | (no dedupe) |
| STG_FED_OFAC_SDN__SDN_ENTITIES | 19,115 | 19,114 | 1 | 0.0% | ent_num |
| STG_INT_UK_COMPANIES_HOUSE__ALL | 5,734,780 | 5,734,779 | 1 | 0.0% | UK_COMPANY_NUMBER |
| STG_PORTAL_ARC_COLUMBUS_GIS_OPE_8259461C2A__ORGANIZATIONS | 5,423 | 5,422 | 1 | 0.0% | ein order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_HARRIS_COUNTY_OP_32D5FF05CA__PLACES | 100 | 99 | 1 | 1.0% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_HARRIS_COUNTY_OP_1966AC023B__PLACES | 55 | 54 | 1 | 1.8% | zip, val_date order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_HARRIS_COUNTY_OP_119B70555B__PLACES | 74 | 73 | 1 | 1.4% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_LA_COUNTY_OPEN_D_0A94DB308E__PROVIDERS | 93 | 92 | 1 | 1.1% | ccn, npi, participation_date, approval_date, start_date order by _load |
| STG_PORTAL_ARC_HARRIS_COUNTY_OP_795533139C__PLACES | 100 | 99 | 1 | 1.0% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_OPEN_BALTIMORE_751D91C991__FACILITIES | 62 | 61 | 1 | 1.6% | ccn, type order by _loaded_at desc) = 1 |
| STG_PORTAL_ARC_TUCSON_OPEN_DATA_3A7E0821D1__CASES | 61 | 60 | 1 | 1.6% | docket, last_edited_date order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ISRAEL_NATIONAL_23EC89FE35__RECORDS | 364 | 363 | 1 | 0.3% | gis_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_ISRAEL_NATIONAL_511B70EB2B__RECORDS | 15,325 | 15,324 | 1 | 0.0% | bus_license_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_98849B65EE__PLACES | 1,616 | 1,615 | 1 | 0.1% | latitude, reportdate order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_SAN_JOSE_OPEN_DA_D8576CBEB1__PLACES | 786 | 785 | 1 | 0.1% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_VIRGINIA_OPEN_DA_AC3869EE0E__RECORDS | 11,856 | 11,855 | 1 | 0.0% | parcel_id order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_03AB547ADB__PLACES | 111 | 110 | 1 | 0.9% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_26239EF185__PLACES | 739 | 738 | 1 | 0.1% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_4E9F15E555__PLACES | 130 | 129 | 1 | 0.8% | fips order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_6271EB297F__PLACES | 1,305 | 1,304 | 1 | 0.1% | latitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_645F59A90F__PLACES | 361 | 360 | 1 | 0.3% | geoid10 order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_A3608CE8E0__PLACES | 145 | 144 | 1 | 0.7% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_E91E8047AA__PLACES | 53,035 | 53,034 | 1 | 0.0% | dataspatial_wkb order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WESTERN_PENNSYLV_F66E0E22DA__PLACES | 1,431 | 1,430 | 1 | 0.1% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_20BC27569A__PLACES | 361 | 360 | 1 | 0.3% | geoid10 order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_224873A888__PLACES | 739 | 738 | 1 | 0.1% | shape_length order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_7431E84319__PLACES | 53,035 | 53,034 | 1 | 0.0% | dataspatial_wkb order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_680EA60076__PLACES | 130 | 129 | 1 | 0.8% | fips order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_B488BFAB9D__PLACES | 1,431 | 1,430 | 1 | 0.1% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_BE3C51E436__PLACES | 1,305 | 1,304 | 1 | 0.1% | latitude order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_D6143BDC6C__PLACES | 145 | 144 | 1 | 0.7% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_CKA_WPRDC_ALLEGHENY_E2D2938646__PLACES | 111 | 110 | 1 | 0.9% | geometry order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_NEW_YORK_STATE_O_49CD8C5B65__ASSETS | 161 | 160 | 1 | 0.6% | patent_number order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_1614522F52__RECORDS | 575 | 574 | 1 | 0.2% | npdes_id order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_7A3C73B2FD__FACILITIES | 2,000 | 1,999 | 1 | 0.1% | tri_facility_id, cas_compound_id, year order by _loaded_at desc) = 1 |
| STG_PORTAL_SOC_UTAH_OPEN_DATA_P_DCD75231F6__FACILITIES | 61 | 60 | 1 | 1.6% | provider_ccn order by _loaded_at desc) = 1 |
| STG_ST_CANNABIS_POLICY_BUNDLES__PLACES | 1,500 | 1,499 | 1 | 0.1% | fips, year order by _loaded_at desc) = 1 |

## Many loads, dedupe plausibly right

| view | landing rows | view rows | loads | biggest load |
|---|---:|---:|---:|---:|
| STG_FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS__PROVIDERS | 6,637 | 6,510 | 6637 | 1 |
| STG_FED_CMS_OPT_OUT_AFFIDAVITS__PROVIDERS | 57,209 | 56,455 | 57209 | 1 |
| STG_FED_CMS_ORDER_AND_REFERRING__PROVIDERS | 2,018,354 | 2,018,350 | 2018354 | 1 |
| STG_FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE__PROVIDERS | 503,917 | 499,190 | 503917 | 1 |
| STG_FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING__PROVIDERS | 2,047,828 | 2,047,826 | 2047828 | 1 |
| STG_FED_DOL_OSHA_INSPECTION__ALL | 5,611,412 | 5,196,412 | 4 | 2,410,000 |
| STG_FED_NOAA_AIS__AIS_VESSEL_POSITIONS | 58,106,517 | 58,104,610 | 2 | 50,810,242 |
| STG_FED_USASPENDING_CONTRACTS_FULL_R2__ORGANIZATIONS | 93,153,424 | 92,377,266 | 2 | 63,729,002 |
| STG_UK_COMPANIES_HOUSE_PSC__PSC_RECORDS | 15,804,612 | 15,804,611 | 2 | 8,804,612 |

## View larger than landing

| view | landing rows | view rows |
|---|---:|---:|
| STG_FED_FDA_DEVICE_CLASSIFICATION__DEVICE_CLASSIFICATIONS | 1 | 7,087 |
| STG_FED_FDA_DEVICE_ENFORCEMENT__DEVICE_ENFORCEMENT_RECALLS | 20 | 39,635 |
| STG_FED_FDA_DEVICE_510K__ALL | 88 | 175,686 |
| STG_FED_FDA_DRUG_ENFORCEMENT__DRUG_ENFORCEMENT_RECALLS | 1 | 17,876 |
| STG_FED_FDA_CAERS__ALL | 1 | 85,511 |
| STG_FED_FDA_DEVICE_PMA__ALL | 29 | 56,853 |
| STG_FED_FDA_ESTABLISHMENT_REG__ALL | 166 | 263,374 |
| STG_FED_FDA_MAUDE__ALL | 1,386 | 2,743,561 |
| STG_FED_FDA_GUDID__ALL | 2,542 | 5,083,948 |
| STG_FED_SEC_13F_POSITIONS__ALL | 3,822,885 | 101,261,252 |
