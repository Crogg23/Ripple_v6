# Every location-shaped column — 2244 columns, 386 of 607 tables

Source: reports/_all_columns.csv (mart column inventory, 2026-08-20). NAME scan only — not value-verified (fill/distinct unknown). Excludes backups, plumbing, findings. Built 2026-08-29.

## Counts by kind

| kind | columns | tables |
|---|---:|---:|
| state | 494 | 267 |
| address | 268 | 120 |
| city | 258 | 182 |
| zip | 227 | 160 |
| coordinates | 212 | 60 |
| country | 155 | 89 |
| facility_site | 144 | 72 |
| county | 131 | 93 |
| fips | 111 | 70 |
| region | 93 | 71 |
| metro | 55 | 26 |
| cong_district | 49 | 35 |
| census_tract | 28 | 6 |
| airport_port | 9 | 7 |
| geometry | 6 | 5 |
| watershed | 4 | 3 |

### CIVIL_RIGHTS__FED_NARA_WRA_AAD
| column | kind | description | type |
|---|---|---|---|
| CAMP_LOCATION | facility_site | site / location / place name | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |

### CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### CONSUMER_SAFETY__FED_CPSC_NEISS
| column | kind | description | type |
|---|---|---|---|
| LOCATION_CODE | facility_site | site / location / place name | TEXT |

### CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| COUNTRIES | country | country name / ISO code | TEXT |
| COUNTRY_CODES | country | country name / ISO code | TEXT |

### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| COUNTRIES | country | country name / ISO code | TEXT |
| COUNTRY_CODES | country | country name / ISO code | TEXT |
| JURISDICTION | region | region / area / territory / jurisdiction | TEXT |
| JURISDICTION_DESCRIPTION | region | region / area / territory / jurisdiction | TEXT |

### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| COUNTRIES | country | country name / ISO code | TEXT |
| COUNTRY_CODES | country | country name / ISO code | TEXT |

### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS
| column | kind | description | type |
|---|---|---|---|
| COUNTRIES | country | country name / ISO code | TEXT |
| COUNTRY_CODES | country | country name / ISO code | TEXT |

### CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OTHERS
| column | kind | description | type |
|---|---|---|---|
| COUNTRIES | country | country name / ISO code | TEXT |
| COUNTRY_CODES | country | country name / ISO code | TEXT |
| JURISDICTION | region | region / area / territory / jurisdiction | TEXT |
| JURISDICTION_DESCRIPTION | region | region / area / territory / jurisdiction | TEXT |

### CORPORATE_REGISTRY__FED_IRS_EO_BMF
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### CORPORATE_REGISTRY__INTL_ES_BORME
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |
| PROVINCE | state | state name or 2-letter code | TEXT |

### CORPORATE_REGISTRY__INTL_IE_CRO
| column | kind | description | type |
|---|---|---|---|
| REGISTERED_ADDRESS | address | street / mailing address | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |

### CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| POST_TOWN | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| COUNTRY_OF_ORIGIN | country | country name / ISO code | TEXT |
| COUNTY | county | county name or code | TEXT |

### CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_PREMISES | address | street / mailing address | TEXT |
| ADDRESS_LOCALITY | city | city / town / municipality | TEXT |
| ADDRESS_COUNTRY | country | country name / ISO code | TEXT |
| COUNTRY_OF_RESIDENCE | country | country name / ISO code | TEXT |
| COUNTRY_REGISTERED | country | country name / ISO code | TEXT |
| NATIONALITY | country | country name / ISO code | TEXT |
| ADDRESS_POSTAL_CODE | zip | ZIP / postal code | TEXT |

### CRIMINAL_JUSTICE__FED_BJS_DATA
| column | kind | description | type |
|---|---|---|---|
| LOCALITY | city | city / town / municipality | TEXT |
| MSA | metro | metro / CBSA / MSA area | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |

### ECONOMICS__FED_BLS_QCEW
| column | kind | description | type |
|---|---|---|---|
| AREA_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |

### ECONOMICS__FED_DOL_FORM5500
| column | kind | description | type |
|---|---|---|---|
| ADMIN_ADDRESS_SAME_SPON_IND | address | street / mailing address | TEXT |
| ADMIN_FOREIGN_ADDRESS1 | address | street / mailing address | TEXT |
| ADMIN_FOREIGN_ADDRESS2 | address | street / mailing address | TEXT |
| ADMIN_US_ADDRESS1 | address | street / mailing address | TEXT |
| ADMIN_US_ADDRESS2 | address | street / mailing address | TEXT |
| PREPARER_FOREIGN_ADDRESS1 | address | street / mailing address | TEXT |
| PREPARER_FOREIGN_ADDRESS2 | address | street / mailing address | TEXT |
| PREPARER_US_ADDRESS1 | address | street / mailing address | TEXT |
| PREPARER_US_ADDRESS2 | address | street / mailing address | TEXT |
| SPONS_DFE_LOC_FOREIGN_ADDRESS1 | address | street / mailing address | TEXT |
| SPONS_DFE_LOC_FOREIGN_ADDRESS2 | address | street / mailing address | TEXT |
| SPONS_DFE_LOC_US_ADDRESS1 | address | street / mailing address | TEXT |
| SPONS_DFE_LOC_US_ADDRESS2 | address | street / mailing address | TEXT |
| SPONS_DFE_MAIL_US_ADDRESS1 | address | street / mailing address | TEXT |
| SPONS_DFE_MAIL_US_ADDRESS2 | address | street / mailing address | TEXT |
| ADMIN_FOREIGN_CITY | city | city / town / municipality | TEXT |
| ADMIN_US_CITY | city | city / town / municipality | TEXT |
| PREPARER_FOREIGN_CITY | city | city / town / municipality | TEXT |
| PREPARER_US_CITY | city | city / town / municipality | TEXT |
| SPONS_DFE_LOC_FOREIGN_CITY | city | city / town / municipality | TEXT |
| SPONS_DFE_LOC_US_CITY | city | city / town / municipality | TEXT |
| SPONS_DFE_MAIL_FOREIGN_CITY | city | city / town / municipality | TEXT |
| SPONS_DFE_MAIL_US_CITY | city | city / town / municipality | TEXT |
| ADMIN_FOREIGN_CNTRY | country | country name / ISO code | NUMBER |
| PREPARER_FOREIGN_CNTRY | country | country name / ISO code | NUMBER |
| SPONS_DFE_LOC_FOREIGN_CNTRY | country | country name / ISO code | NUMBER |
| SPONS_DFE_MAIL_FOREIGN_CNTRY | country | country name / ISO code | NUMBER |
| ADMIN_FOREIGN_PROV_STATE | state | state name or 2-letter code | TEXT |
| ADMIN_US_STATE | state | state name or 2-letter code | TEXT |
| PREPARER_FOREIGN_PROV_STATE | state | state name or 2-letter code | TEXT |
| PREPARER_US_STATE | state | state name or 2-letter code | TEXT |
| SPONS_DFE_LOC_FORGN_PROV_ST | state | state name or 2-letter code | TEXT |
| SPONS_DFE_LOC_US_STATE | state | state name or 2-letter code | TEXT |
| SPONS_DFE_MAIL_FORGN_PROV_ST | state | state name or 2-letter code | TEXT |
| SPONS_DFE_MAIL_US_STATE | state | state name or 2-letter code | TEXT |
| ADMIN_FOREIGN_POSTAL_CD | zip | ZIP / postal code | TEXT |
| ADMIN_US_ZIP | zip | ZIP / postal code | TEXT |
| PREPARER_FOREIGN_POSTAL_CD | zip | ZIP / postal code | TEXT |
| PREPARER_US_ZIP | zip | ZIP / postal code | TEXT |
| SPONS_DFE_LOC_FORGN_POSTAL_CD | zip | ZIP / postal code | TEXT |
| SPONS_DFE_LOC_US_ZIP | zip | ZIP / postal code | TEXT |
| SPONS_DFE_MAIL_FORGN_POSTAL_CD | zip | ZIP / postal code | TEXT |
| SPONS_DFE_MAIL_US_ZIP | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_FAC_SINGLE_AUDIT
| column | kind | description | type |
|---|---|---|---|
| AUDITEE_ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| AUDITEE_CITY | city | city / town / municipality | TEXT |
| AUDITOR_CITY | city | city / town / municipality | TEXT |
| AUDITEE_STATE | state | state name or 2-letter code | TEXT |
| AUDITOR_STATE | state | state name or 2-letter code | TEXT |
| AUDITEE_ZIP | zip | ZIP / postal code | TEXT |
| AUDITOR_ZIP | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_FDIC_FAILED_BANKS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| CITY_STATE | city | city / town / municipality | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### ECONOMICS__FED_FINCEN_BOI
| column | kind | description | type |
|---|---|---|---|
| BENEFICIAL_OWNER_ADDRESS | address | street / mailing address | TEXT |
| BENEFICIAL_OWNER_ID_ISSUING_JURISDICTION | region | region / area / territory / jurisdiction | TEXT |
| JURISDICTION_OF_FORMATION | region | region / area / territory / jurisdiction | TEXT |
| US_REGISTRATION_STATE | state | state name or 2-letter code | FLOAT |

### ECONOMICS__FED_FOREIGNASSISTANCE
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### ECONOMICS__FED_IRS_990
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_IRS_AUTO_REVOCATIONS
| column | kind | description | type |
|---|---|---|---|
| ORGANIZATION_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_IRS_BMF
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_IRS_EO_PR
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ECONOMICS__FED_IRS_REVOCATION
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_IRS_SOI_CHARITIES
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_PBGC_DATA
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ECONOMICS__FED_SBA_LOANS
| column | kind | description | type |
|---|---|---|---|
| BORROWER_CITY | city | city / town / municipality | TEXT |
| CONGRESSIONAL_DISTRICT | cong_district | congressional / legislative district | TEXT |
| PROJECT_COUNTY | county | county name or code | TEXT |
| BORROWER_STATE | state | state name or 2-letter code | TEXT |
| CDC_STATE | state | state name or 2-letter code | TEXT |
| LENDER_STATE | state | state name or 2-letter code | TEXT |
| PROJECT_STATE | state | state name or 2-letter code | TEXT |
| BORROWER_ZIP | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_SBA_PPP
| column | kind | description | type |
|---|---|---|---|
| BORROWER_CITY | city | city / town / municipality | TEXT |
| CONGRESSIONAL_DISTRICT | cong_district | congressional / legislative district | TEXT |
| PROJECT_COUNTY | county | county name or code | TEXT |
| RURAL_URBAN_INDICATOR | metro | metro / CBSA / MSA area | TEXT |
| BORROWER_STATE | state | state name or 2-letter code | TEXT |
| PROJECT_STATE | state | state name or 2-letter code | TEXT |
| SERVICING_LENDER_STATE | state | state name or 2-letter code | TEXT |
| BORROWER_ZIP | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL
| column | kind | description | type |
|---|---|---|---|
| RECIPIENT_ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| RECIPIENT_ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | city | city / town / municipality | TEXT |
| RECIPIENT_CITY_CODE | city | city / town / municipality | TEXT |
| RECIPIENT_CITY_NAME | city | city / town / municipality | TEXT |
| RECIPIENT_FOREIGN_CITY_NAME | city | city / town / municipality | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_CODE | country | country name / ISO code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_NAME | country | country name / ISO code | TEXT |
| RECIPIENT_COUNTRY_CODE | country | country name / ISO code | TEXT |
| RECIPIENT_COUNTRY_NAME | country | country name / ISO code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTY_NAME | county | county name or code | TEXT |
| RECIPIENT_COUNTY_NAME | county | county name or code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_CODE | facility_site | site / location / place name | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_FOREIGN_LOCATION | facility_site | site / location / place name | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_SCOPE | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_CURRENT | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_ORIGINAL | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_NAME | state | state name or 2-letter code | TEXT |
| RECIPIENT_FOREIGN_PROVINCE_NAME | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE_CODE | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE_NAME | state | state name or 2-letter code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_ZIP_4 | zip | ZIP / postal code | TEXT |
| RECIPIENT_FOREIGN_POSTAL_CODE | zip | ZIP / postal code | TEXT |
| RECIPIENT_ZIP_CODE | zip | ZIP / postal code | TEXT |
| RECIPIENT_ZIP_LAST_4_CODE | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_USASPENDING_CONTRACTS
| column | kind | description | type |
|---|---|---|---|
| PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | city | city / town / municipality | TEXT |
| RECIPIENT_CITY_NAME | city | city / town / municipality | TEXT |
| RECIPIENT_COUNTRY_NAME | country | country name / ISO code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE_CODE | state | state name or 2-letter code | TEXT |
| RECIPIENT_ZIP_4_CODE | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_USASPENDING_CONTRACTS_FULL
| column | kind | description | type |
|---|---|---|---|
| RECIPIENT_ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| RECIPIENT_ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| AIRPORT_AUTHORITY | airport_port | airport / port / station code | TEXT |
| PORT_AUTHORITY | airport_port | airport / port / station code | TEXT |
| CITY_LOCAL_GOVERNMENT | city | city / town / municipality | TEXT |
| MUNICIPALITY_LOCAL_GOVERNMENT | city | city / town / municipality | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | city | city / town / municipality | TEXT |
| RECIPIENT_CITY_NAME | city | city / town / municipality | TEXT |
| SCHOOL_DISTRICT_LOCAL_GOVERNMENT | cong_district | congressional / legislative district | TEXT |
| COUNTRY_OF_PRODUCT_OR_SERVICE_ORIGIN | country | country name / ISO code | TEXT |
| COUNTRY_OF_PRODUCT_OR_SERVICE_ORIGIN_CODE | country | country name / ISO code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_CODE | country | country name / ISO code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_NAME | country | country name / ISO code | TEXT |
| RECIPIENT_COUNTRY_CODE | country | country name / ISO code | TEXT |
| RECIPIENT_COUNTRY_NAME | country | country name / ISO code | TEXT |
| COUNTY_LOCAL_GOVERNMENT | county | county name or code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTY_NAME | county | county name or code | TEXT |
| RECIPIENT_COUNTY_NAME | county | county name or code | TEXT |
| PLACE_OF_MANUFACTURE | facility_site | site / location / place name | TEXT |
| PLACE_OF_MANUFACTURE_CODE | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_CURRENT | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_ORIGINAL | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| HISTORICALLY_UNDERUTILIZED_BUSINESS_ZONE_HUBZONE_FIRM | region | region / area / territory / jurisdiction | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE | state | state name or 2-letter code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_NAME | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE_CODE | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE_NAME | state | state name or 2-letter code | TEXT |
| STATE_CONTROLLED_INSTITUTION_OF_HIGHER_LEARNING | state | state name or 2-letter code | TEXT |
| US_STATE_GOVERNMENT | state | state name or 2-letter code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_ZIP_4 | zip | ZIP / postal code | TEXT |
| RECIPIENT_ZIP_4_CODE | zip | ZIP / postal code | TEXT |

### ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES
| column | kind | description | type |
|---|---|---|---|
| CONGRESSIONAL_JUSTIFICATION_URL | cong_district | congressional / legislative district | TEXT |

### ECONOMICS__FED_US_SEC_EDGAR
| column | kind | description | type |
|---|---|---|---|
| BUSINESS_ADDRESS | address | street / mailing address | TEXT |
| STATE_OF_INCORPORATION | state | state name or 2-letter code | TEXT |

### ECONOMICS__FED_US_USASPENDING_API
| column | kind | description | type |
|---|---|---|---|
| PLACE_OF_PERFORMANCE_CITY | city | city / town / municipality | TEXT |
| PLACE_OF_PERFORMANCE_FIPS | fips | FIPS / GEOID census code | TEXT |
| RECIPIENT_LOCATION_FIPS | fips | FIPS / GEOID census code | TEXT |
| PLACE_OF_PERFORMANCE_STATE | state | state name or 2-letter code | TEXT |
| RECIPIENT_LOCATION_STATE | state | state name or 2-letter code | TEXT |

### ECONOMICS__INTL_GFI_TRADE
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### ECONOMICS__INTL_GLEIF
| column | kind | description | type |
|---|---|---|---|
| ENTITY_HEADQUARTERSADDRESS_CITY | city | city / town / municipality | TEXT |
| ENTITY_LEGALADDRESS_CITY | city | city / town / municipality | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_1_CITY | city | city / town / municipality | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_2_CITY | city | city / town / municipality | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_3_CITY | city | city / town / municipality | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_4_CITY | city | city / town / municipality | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_5_CITY | city | city / town / municipality | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_CITY | city | city / town / municipality | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_CITY | city | city / town / municipality | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_CITY | city | city / town / municipality | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_CITY | city | city / town / municipality | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_CITY | city | city / town / municipality | TEXT |
| ENTITY_HEADQUARTERSADDRESS_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_LEGALADDRESS_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_1_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_2_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_3_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_4_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_5_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_COUNTRY | country | country name / ISO code | TEXT |
| ENTITY_HEADQUARTERSADDRESS_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_LEGALADDRESS_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_1_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_2_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_3_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_4_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_5_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_REGION | region | region / area / territory / jurisdiction | TEXT |
| ENTITY_HEADQUARTERSADDRESS_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_LEGALADDRESS_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_1_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_2_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_3_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_4_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_OTHERADDRESSES_OTHERADDRESS_5_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_1_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_2_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_3_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_4_POSTALCODE | zip | ZIP / postal code | TEXT |
| ENTITY_TRANSLITERATEDOTHERADDRESSES_TRANSLITERATEDOTHERADDRESS_5_POSTALCODE | zip | ZIP / postal code | TEXT |

### ECONOMICS__INTL_IPC_FOOD_INSECURITY_GLOBAL
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |
| TOTAL_COUNTRY_POPULATION | country | country name / ISO code | FLOAT |

### ECONOMICS__INTL_IT_ISTAT
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### ECONOMICS__XC_OWID_GINI
| column | kind | description | type |
|---|---|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | region / area / territory / jurisdiction | TEXT |

### EDUCATION__FED_CFTC_COT_FINANCIAL
| column | kind | description | type |
|---|---|---|---|
| ASSET_MGR_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_ASSET_MGR_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_DEALER_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_LEV_MONEY_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_NONREPT_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_OTHER_REPT_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_TOT_REPT_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CONC_GROSS_LE_4_TDR_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CONC_GROSS_LE_8_TDR_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CONC_NET_LE_4_TDR_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CONC_NET_LE_8_TDR_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| DEALER_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| LEV_MONEY_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| NONREPT_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| OTHER_REPT_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| PCT_OF_OI_ASSET_MGR_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| PCT_OF_OI_DEALER_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| PCT_OF_OI_LEV_MONEY_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| PCT_OF_OI_NONREPT_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| PCT_OF_OI_OTHER_REPT_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| PCT_OF_OI_TOT_REPT_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TOT_REPT_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TRADERS_ASSET_MGR_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TRADERS_DEALER_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TRADERS_LEV_MONEY_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TRADERS_OTHER_REPT_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TRADERS_TOT_REPT_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CFTC_REGION_CODE | region | region / area / territory / jurisdiction | TEXT |

### EDUCATION__FED_CFTC_COT_FUTURES
| column | kind | description | type |
|---|---|---|---|
| CHANGE_IN_COMMERCIAL_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_NONCOMMERCIAL_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_NONREPORTABLE_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| CHANGE_IN_TOTAL_REPORTABLE_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| COMMERCIAL_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| COMMERCIAL_POSITIONS_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| COMMERCIAL_POSITIONS_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_GROSS_LT_4_TDR_LONG_OLD | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_GROSS_LT_4_TDR_LONG_OTHER | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_GROSS_LT_8_TDR_LONG_ALL | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_GROSS_LT_8_TDR_LONG_OLD | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_GROSS_LT_8_TDR_LONG_OTHER | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_NET_LT_4_TDR_LONG_ALL | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_NET_LT_4_TDR_LONG_OLD | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_NET_LT_4_TDR_LONG_OTHER | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_NET_LT_8_TDR_LONG_ALL | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_NET_LT_8_TDR_LONG_OLD | coordinates | latitude / longitude point | FLOAT |
| CONCENTRATION_NET_LT_8_TDR_LONG_OTHER | coordinates | latitude / longitude point | FLOAT |
| NONCOMMERCIAL_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| NONCOMMERCIAL_POSITIONS_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| NONCOMMERCIAL_POSITIONS_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| NONREPORTABLE_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| NONREPORTABLE_POSITIONS_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| NONREPORTABLE_POSITIONS_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| OF_OI_COMMERCIAL_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| OF_OI_COMMERCIAL_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| OF_OI_COMMERCIAL_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| OF_OI_NONCOMMERCIAL_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| OF_OI_NONCOMMERCIAL_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| OF_OI_NONCOMMERCIAL_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| OF_OI_NONREPORTABLE_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| OF_OI_NONREPORTABLE_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| OF_OI_NONREPORTABLE_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| OF_OI_TOTAL_REPORTABLE_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| OF_OI_TOTAL_REPORTABLE_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| OF_OI_TOTAL_REPORTABLE_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| TOTAL_REPORTABLE_POSITIONS_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TOTAL_REPORTABLE_POSITIONS_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| TOTAL_REPORTABLE_POSITIONS_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| TRADERS_COMMERCIAL_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TRADERS_COMMERCIAL_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| TRADERS_COMMERCIAL_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| TRADERS_NONCOMMERCIAL_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TRADERS_NONCOMMERCIAL_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| TRADERS_NONCOMMERCIAL_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| TRADERS_TOTAL_REPORTABLE_LONG_ALL | coordinates | latitude / longitude point | TEXT |
| TRADERS_TOTAL_REPORTABLE_LONG_OLD | coordinates | latitude / longitude point | TEXT |
| TRADERS_TOTAL_REPORTABLE_LONG_OTHER | coordinates | latitude / longitude point | TEXT |
| CFTC_REGION_CODE | region | region / area / territory / jurisdiction | TEXT |

### EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| REGION_CODE | region | region / area / territory / jurisdiction | NUMBER |
| STATE | state | state name or 2-letter code | TEXT |
| TUITION_IN_STATE | state | state name or 2-letter code | NUMBER |
| TUITION_OUT_OF_STATE | state | state name or 2-letter code | NUMBER |
| ZIP | zip | ZIP / postal code | TEXT |

### EDUCATION__FED_ED_EDFACTS
| column | kind | description | type |
|---|---|---|---|
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |

### EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_DECLARED_STATS
| column | kind | description | type |
|---|---|---|---|
| ADVERTISER_DECLARED_PROMOTER_ADDRESS | address | street / mailing address | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |

### EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_GEO_SPEND
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |
| COUNTRY_SUBDIVISION_PRIMARY | country | country name / ISO code | TEXT |

### EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS
| column | kind | description | type |
|---|---|---|---|
| REGIONS | region | region / area / territory / jurisdiction | TEXT |

### EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS
| column | kind | description | type |
|---|---|---|---|
| REGIONS | region | region / area / territory / jurisdiction | TEXT |

### EDUCATION__FED_GOOGLE_POLADS_GEO_SPEND
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |
| COUNTRY_SUBDIVISION_PRIMARY | country | country name / ISO code | TEXT |
| COUNTRY_SUBDIVISION_SECONDARY | country | country name / ISO code | TEXT |

### EDUCATION__FED_SENATE_LDA_FILINGS
| column | kind | description | type |
|---|---|---|---|
| REGISTRANT_CITY | city | city / town / municipality | TEXT |
| CLIENT_COUNTRY | country | country name / ISO code | TEXT |
| REGISTRANT_COUNTRY | country | country name / ISO code | TEXT |
| CLIENT_STATE | state | state name or 2-letter code | TEXT |
| REGISTRANT_STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA860_1_UTILITY
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### ENERGY__FED_EIA860_2_PLANT
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY | county | county name or code | TEXT |
| NERC_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### ENERGY__FED_EIA860_3_1_GENERATOR
| column | kind | description | type |
|---|---|---|---|
| COUNTY | county | county name or code | TEXT |
| RTO_ISO_LOCATION_DESIGNATION_FOR_REPORTING_WHOLESALE_SALES_DATA_TO_FERC | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA860_3_2_WIND
| column | kind | description | type |
|---|---|---|---|
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA860_3_3_SOLAR
| column | kind | description | type |
|---|---|---|---|
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA860_3_4_ENERGY_STORAGE
| column | kind | description | type |
|---|---|---|---|
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA860_3_5_MULTIFUEL
| column | kind | description | type |
|---|---|---|---|
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA860_4_OWNER
| column | kind | description | type |
|---|---|---|---|
| OWNER_STREET_ADDRESS | address | street / mailing address | TEXT |
| OWNER_CITY | city | city / town / municipality | TEXT |
| OWNER_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| OWNER_ZIP | zip | ZIP / postal code | TEXT |

### ENERGY__FED_EIA860_6_2_ENVIROEQUIP
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_ADVANCED_METERS
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_DELIVERY_COMPANIES
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_DEMAND_RESPONSE
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_DISTRIBUTION_SYSTEMS
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_DYNAMIC_PRICING
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_ENERGY_EFFICIENCY
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_MERGERS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ENERGY__FED_EIA861_NET_METERING
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_NON_NET_METERING_DISTRIBUTED
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_OPERATIONAL_DATA
| column | kind | description | type |
|---|---|---|---|
| NERC_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_RELIABILITY
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_SALES_ULT_CUST
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_SALES_ULT_CUST_CS
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_SERVICE_TERRITORY
| column | kind | description | type |
|---|---|---|---|
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_SHORT_FORM
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA861_UTILITY_DATA
| column | kind | description | type |
|---|---|---|---|
| NERC_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__FED_EIA_861_BALANCING_AUTHORITY
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### ENERGY__INTL_EMBER_ELEC
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |
| EMBER_REGION | region | region / area / territory / jurisdiction | TEXT |

### ENVIRONMENT__EPA_PENALTY_GAP
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY | county | county name or code | TEXT |
| TRI_ON_SITE_RELEASES | facility_site | site / location / place name | FLOAT |
| FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| EPA_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_AQS_SITES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY_NAME | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY_CODE | county | county name or code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| MET_SITE_COUNTY_CODE | county | county name or code | TEXT |
| AQS_SITE_ID | facility_site | site / location / place name | TEXT |
| LOCAL_SITE_NAME | facility_site | site / location / place name | TEXT |
| LOCATION_SETTING | facility_site | site / location / place name | TEXT |
| MET_SITE_DIRECTION | facility_site | site / location / place name | TEXT |
| MET_SITE_DISTANCE | facility_site | site / location / place name | NUMBER |
| MET_SITE_SITE_NUMBER | facility_site | site / location / place name | TEXT |
| MET_SITE_TYPE | facility_site | site / location / place name | TEXT |
| SITE_CLOSED_DATE | facility_site | site / location / place name | DATE |
| SITE_ESTABLISHED_DATE | facility_site | site / location / place name | DATE |
| SITE_NUMBER | facility_site | site / location / place name | TEXT |
| CBSA_NAME | metro | metro / CBSA / MSA area | TEXT |
| MET_SITE_STATE_CODE | state | state name or 2-letter code | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_ECHO
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY | county | county name or code | TEXT |
| TRI_ON_SITE_RELEASES | facility_site | site / location / place name | FLOAT |
| FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| EPA_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_EGRID_PLANT_2022
| column | kind | description | type |
|---|---|---|---|
| PLANT_LATITUDE | coordinates | latitude / longitude point | FLOAT |
| PLANT_LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| PLANT_COUNTY_NAME | county | county name or code | TEXT |
| PLANT_FIPS_COUNTY_CODE | fips | FIPS / GEOID census code | TEXT |
| PLANT_FIPS_STATE_CODE | fips | FIPS / GEOID census code | TEXT |
| NERC_REGION_ACRONYM | region | region / area / territory / jurisdiction | TEXT |
| PLANT_ASSOCIATED_ISO_RTO_TERRITORY | region | region / area / territory / jurisdiction | TEXT |
| PLANT_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_ENVIROFACTS
| column | kind | description | type |
|---|---|---|---|
| CITY_NAME | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | TEXT |
| LONGITUDE | coordinates | latitude / longitude point | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| SITE_ID | facility_site | site / location / place name | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| POSTAL_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_FRS_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| CONGRESSIONAL_DISTRICT | cong_district | congressional / legislative district | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY | county | county name or code | TEXT |
| SITE_TYPE | facility_site | site / location / place name | TEXT |
| SUPPLEMENTAL_LOCATION | facility_site | site / location / place name | TEXT |
| FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| EPA_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |
| POSTAL_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| FAC_STREET | address | street / mailing address | TEXT |
| FAC_CITY | city | city / town / municipality | TEXT |
| LATITUDE_MEASURE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE_MEASURE | coordinates | latitude / longitude point | NUMBER |
| FAC_COUNTY | county | county name or code | TEXT |
| FAC_EPA_REGION | region | region / area / territory / jurisdiction | TEXT |
| FAC_STATE | state | state name or 2-letter code | TEXT |
| FAC_ZIP | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS
| column | kind | description | type |
|---|---|---|---|
| LOCATION_ADDRESS | address | street / mailing address | TEXT |
| CITY_NAME | city | city / town / municipality | TEXT |
| COUNTRY_NAME | country | country name / ISO code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| SUPPLEMENTAL_LOCATION | facility_site | site / location / place name | TEXT |
| FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |
| POSTAL_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_GHGRP_FACILITY
| column | kind | description | type |
|---|---|---|---|
| ADDRESS1 | address | street / mailing address | TEXT |
| ADDRESS2 | address | street / mailing address | NUMBER |
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY | county | county name or code | TEXT |
| COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| EPA_REGION | region | region / area / territory / jurisdiction | TEXT |
| LOCAL_CONTROL_REGION_CODE | region | region / area / territory / jurisdiction | TEXT |
| LOCAL_CONTROL_REGION_NAME | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES
| column | kind | description | type |
|---|---|---|---|
| STATE_EPA_FLAG | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS
| column | kind | description | type |
|---|---|---|---|
| STATE_EPA_FLAG | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
| column | kind | description | type |
|---|---|---|---|
| STATE_EPA_FLAG | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS
| column | kind | description | type |
|---|---|---|---|
| STATE_EPA_FLAG | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS
| column | kind | description | type |
|---|---|---|---|
| STATE_EPA_FLAG | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
| column | kind | description | type |
|---|---|---|---|
| STATE_CODE | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| LOCATION_ADDRESS | address | street / mailing address | TEXT |
| SUPPLEMENTAL_ADDRESS_TEXT | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| GEOCODE_LATITUDE | coordinates | latitude / longitude point | FLOAT |
| GEOCODE_LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY_CODE | county | county name or code | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS
| column | kind | description | type |
|---|---|---|---|
| STATE_LOCAL_PENALTY_AMT | state | state name or 2-letter code | FLOAT |

### ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
| column | kind | description | type |
|---|---|---|---|
| STATE_EPA_FLAG | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS
| column | kind | description | type |
|---|---|---|---|
| ACTIVITY_LOCATION | facility_site | site / location / place name | TEXT |

### ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS
| column | kind | description | type |
|---|---|---|---|
| ACTIVITY_LOCATION | facility_site | site / location / place name | TEXT |

### ENVIRONMENT__FED_EPA_RCRA_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY_NAME | city | city / town / municipality | TEXT |
| ACTIVITY_LOCATION | facility_site | site / location / place name | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS
| column | kind | description | type |
|---|---|---|---|
| ACTIVITY_LOCATION | facility_site | site / location / place name | TEXT |

### ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS
| column | kind | description | type |
|---|---|---|---|
| ACTIVITY_LOCATION | facility_site | site / location / place name | TEXT |

### ENVIRONMENT__FED_EPA_RCRA_VIOSNC_HISTORY
| column | kind | description | type |
|---|---|---|---|
| ACTIVITY_LOCATION | facility_site | site / location / place name | TEXT |

### ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| STATE_FACILITY_ID | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS
| column | kind | description | type |
|---|---|---|---|
| CITY_SERVED | city | city / town / municipality | TEXT |
| COUNTY_SERVED | county | county name or code | TEXT |
| STATE_SERVED | state | state name or 2-letter code | TEXT |
| ZIP_CODE_SERVED | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE1 | address | street / mailing address | TEXT |
| ADDRESS_LINE2 | address | street / mailing address | TEXT |
| EMAIL_ADDR | address | street / mailing address | TEXT |
| CITY_NAME | city | city / town / municipality | TEXT |
| COUNTRY_CODE | country | country name / ISO code | TEXT |
| EPA_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
| column | kind | description | type |
|---|---|---|---|
| STATE_MCL | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_EPA_SUPERFUND_SITE_BOUNDARIES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_COMMENT | address | street / mailing address | TEXT |
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTY | county | county name or code | TEXT |
| SITE_CONTACT_EMAIL | facility_site | site / location / place name | TEXT |
| SITE_CONTACT_NAME | facility_site | site / location / place name | TEXT |
| SITE_CONTACT_PHONE | facility_site | site / location / place name | TEXT |
| SITE_FEATURE_CLASS | facility_site | site / location / place name | TEXT |
| SITE_FEATURE_DESCRIPTION | facility_site | site / location / place name | TEXT |
| SITE_FEATURE_NAME | facility_site | site / location / place name | TEXT |
| SITE_FEATURE_SOURCE | facility_site | site / location / place name | TEXT |
| SITE_FEATURE_TYPE | facility_site | site / location / place name | TEXT |
| SITE_NAME | facility_site | site / location / place name | TEXT |
| SITE_URL | facility_site | site / location / place name | TEXT |
| EPA_REGION_CODE | region | region / area / territory / jurisdiction | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_TRI_BASIC_2023
| column | kind | description | type |
|---|---|---|---|
| C_5_STREET_ADDRESS | address | street / mailing address | TEXT |
| C_6_CITY | city | city / town / municipality | TEXT |
| C_12_LATITUDE | coordinates | latitude / longitude point | FLOAT |
| C_13_LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| C_7_COUNTY | county | county name or code | TEXT |
| C_104_OFF_SITE_TREATED_TOTAL | facility_site | site / location / place name | TEXT |
| C_109_8_1_A_ON_SITE_CONTAINED | facility_site | site / location / place name | TEXT |
| C_110_8_1_B_ON_SITE_OTHER | facility_site | site / location / place name | TEXT |
| C_111_8_1_C_OFF_SITE_CONTAIN | facility_site | site / location / place name | TEXT |
| C_112_8_1_D_OFF_SITE_OTHER_R | facility_site | site / location / place name | TEXT |
| C_115_8_4_RECYCLING_ON_SITE | facility_site | site / location / place name | TEXT |
| C_117_8_6_TREATMENT_ON_SITE | facility_site | site / location / place name | TEXT |
| C_118_8_7_TREATMENT_OFF_SITE | facility_site | site / location / place name | TEXT |
| C_65_ON_SITE_RELEASE_TOTAL | facility_site | site / location / place name | TEXT |
| C_88_OFF_SITE_RELEASE_TOTAL | facility_site | site / location / place name | TEXT |
| C_94_OFF_SITE_RECYCLED_TOTAL | facility_site | site / location / place name | TEXT |
| C_97_OFF_SITE_ENERGY_RECOVERY_T | facility_site | site / location / place name | TEXT |
| C_9_ZIP | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_EPA_TRI_FACILITY
| column | kind | description | type |
|---|---|---|---|
| MAIL_STREET_ADDRESS | address | street / mailing address | TEXT |
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY_NAME | city | city / town / municipality | TEXT |
| MAIL_CITY | city | city / town / municipality | TEXT |
| FAC_LATITUDE | coordinates | latitude / longitude point | NUMBER |
| FAC_LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| PREF_LATITUDE | coordinates | latitude / longitude point | NUMBER |
| PREF_LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| MAIL_COUNTRY | country | country name / ISO code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| STATE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |
| MAIL_PROVINCE | state | state name or 2-letter code | TEXT |
| MAIL_STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| MAIL_ZIP_CODE | zip | ZIP / postal code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY_NAME | county | county name or code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_FRACFOCUS_REGISTRY
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY_NAME | county | county name or code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_FRACFOCUS_WATER_SOURCE
| column | kind | description | type |
|---|---|---|---|
| COUNTY_NAME | county | county name or code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_NID_DAMS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| CONGRESSIONAL_DISTRICT | cong_district | congressional / legislative district | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY | county | county name or code | TEXT |
| IS_STATE_REGULATED | state | state name or 2-letter code | BOOLEAN |
| STATE | state | state name or 2-letter code | TEXT |
| STATE_REGULATORY_AGENCY | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_NOAA_STORM_EVENTS
| column | kind | description | type |
|---|---|---|---|
| BEGIN_LAT | coordinates | latitude / longitude point | FLOAT |
| BEGIN_LON | coordinates | latitude / longitude point | FLOAT |
| END_LAT | coordinates | latitude / longitude point | FLOAT |
| END_LON | coordinates | latitude / longitude point | FLOAT |
| BEGIN_LOCATION | facility_site | site / location / place name | TEXT |
| END_LOCATION | facility_site | site / location / place name | TEXT |
| CZ_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| TOR_OTHER_CZ_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| TOR_OTHER_CZ_STATE | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_NOAA_WEATHER_API
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| GEOMETRY | geometry | map shape / polygon / WKT | TEXT |
| ZONE_UGC | region | region / area / territory / jurisdiction | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS
| column | kind | description | type |
|---|---|---|---|
| OPERATOR_STREET_ADDRESS | address | street / mailing address | TEXT |
| OPERATOR_CITY | city | city / town / municipality | TEXT |
| LOCATION_LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LOCATION_LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| TIME_ZONE | region | region / area / territory / jurisdiction | TEXT |
| OPERATOR_STATE | state | state name or 2-letter code | TEXT |
| OPERATOR_POSTAL_CODE | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_USCG_NRC_INCIDENTS
| column | kind | description | type |
|---|---|---|---|
| RESPONSIBLE_CITY | city | city / town / municipality | TEXT |
| RESPONSIBLE_STATE | state | state name or 2-letter code | TEXT |
| RESPONSIBLE_ZIP | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS
| column | kind | description | type |
|---|---|---|---|
| RESPONSIBLE_CITY | city | city / town / municipality | TEXT |
| RESPONSIBLE_STATE | state | state name or 2-letter code | TEXT |
| RESPONSIBLE_ZIP | zip | ZIP / postal code | TEXT |

### ENVIRONMENT__FED_USGS_MINERALS
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTRY | country | country name / ISO code | TEXT |
| COUNTY | county | county name or code | TEXT |
| SITE_NAME | facility_site | site / location / place name | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| US_STATE | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY | county | county name or code | TEXT |
| LOCATION_NOTES | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### ENVIRONMENT__FED_USGS_WATER
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY_CD | county | county name or code | TEXT |
| SITE_NAME | facility_site | site / location / place name | TEXT |
| SITE_NO | facility_site | site / location / place name | TEXT |
| STATE_CD | state | state name or 2-letter code | TEXT |
| HUC_CD | watershed | watershed / HUC / basin | TEXT |

### ENVIRONMENT__FED_USGS_WBD_HUC8
| column | kind | description | type |
|---|---|---|---|
| SHAPE_AREA | geometry | map shape / polygon / WKT | FLOAT |
| SHAPE_LENGTH | geometry | map shape / polygon / WKT | FLOAT |
| HUC8 | watershed | watershed / HUC / basin | TEXT |
| WATERSHED_NAME | watershed | watershed / HUC / basin | TEXT |

### ENVIRONMENT__FED_WQP_MONITORING_STATIONS
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTRY_CODE | country | country name / ISO code | TEXT |
| COUNTY_CODE | county | county name or code | TEXT |
| MONITORING_LOCATION_DESCRIPTION_TEXT | facility_site | site / location / place name | TEXT |
| MONITORING_LOCATION_IDENTIFIER | facility_site | site / location / place name | TEXT |
| MONITORING_LOCATION_NAME | facility_site | site / location / place name | TEXT |
| MONITORING_LOCATION_TYPE_NAME | facility_site | site / location / place name | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| HUC_EIGHT_DIGIT_CODE | watershed | watershed / HUC / basin | TEXT |

### ENVIRONMENT__INTL_GEM_HAZARD
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTRY | country | country name / ISO code | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |

### ENVIRONMENT__INTL_GLOBAL_WITNESS_DEFENDERS
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |

### FINANCE__FED_EPA_ICIS_FEC_CASE_ENFORCEMENT_CONCLUSION_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| FACILITY_CITY | city | city / town / municipality | TEXT |
| FACILITY_STATE | state | state name or 2-letter code | TEXT |
| FACILITY_ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| LOCATION_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS
| column | kind | description | type |
|---|---|---|---|
| EPA_REGION_CODE | region | region / area / territory / jurisdiction | TEXT |

### FINANCE__FED_FARA
| column | kind | description | type |
|---|---|---|---|
| FOREIGN_PRINCIPAL_COUNTRY | country | country name / ISO code | NUMBER |

### FINANCE__FED_FATCA_FFI
| column | kind | description | type |
|---|---|---|---|
| COUNTRY_NAME | country | country name / ISO code | TEXT |

### FINANCE__FED_FDIC_BANK_DATA
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| HOLDING_COMPANY_CITY | city | city / town / municipality | TEXT |
| OCC_DISTRICT | cong_district | congressional / legislative district | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY | county | county name or code | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| CBSA | metro | metro / CBSA / MSA area | TEXT |
| CBSA_METRO_NAME | metro | metro / CBSA / MSA area | TEXT |
| FDIC_REGION | region | region / area / territory / jurisdiction | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS
| column | kind | description | type |
|---|---|---|---|
| BRANCH_ADDRESS | address | street / mailing address | TEXT |
| INSTITUTION_ADDRESS | address | street / mailing address | TEXT |
| BRANCH_CITY | city | city / town / municipality | TEXT |
| BRANCH_CITY_ALT | city | city / town / municipality | TEXT |
| HOLDING_COMPANY_CITY | city | city / town / municipality | TEXT |
| INSTITUTION_CITY | city | city / town / municipality | TEXT |
| FED_DISTRICT_CODE | cong_district | congressional / legislative district | TEXT |
| FED_DISTRICT_NAME | cong_district | congressional / legislative district | TEXT |
| OCC_DISTRICT_CODE | cong_district | congressional / legislative district | TEXT |
| OCC_DISTRICT_NAME | cong_district | congressional / legislative district | TEXT |
| SIMS_LATITUDE | coordinates | latitude / longitude point | FLOAT |
| SIMS_LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| BRANCH_COUNTRY | country | country name / ISO code | TEXT |
| INSTITUTION_COUNTRY | country | country name / ISO code | TEXT |
| BRANCH_COUNTY_NAME | county | county name or code | TEXT |
| BRANCH_PLACE_CODE | facility_site | site / location / place name | TEXT |
| BRANCH_COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| BRANCH_STATE_COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| BRANCH_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| INSTITUTION_STATE_COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| BRANCH_CBSA_DIVISION_CODE | metro | metro / CBSA / MSA area | TEXT |
| BRANCH_CBSA_DIVISION_NAME | metro | metro / CBSA / MSA area | TEXT |
| BRANCH_CSA_CODE | metro | metro / CBSA / MSA area | TEXT |
| BRANCH_CSA_NAME | metro | metro / CBSA / MSA area | TEXT |
| BRANCH_METRO_FLAG | metro | metro / CBSA / MSA area | TEXT |
| BRANCH_MSA_CODE | metro | metro / CBSA / MSA area | TEXT |
| BRANCH_MSA_NAME | metro | metro / CBSA / MSA area | TEXT |
| FDIC_REGION_CODE | region | region / area / territory / jurisdiction | TEXT |
| FDIC_REGION_NAME | region | region / area / territory / jurisdiction | TEXT |
| BRANCH_STATE | state | state name or 2-letter code | TEXT |
| BRANCH_STATE_NAME | state | state name or 2-letter code | TEXT |
| HOLDING_COMPANY_STATE | state | state name or 2-letter code | TEXT |
| INSTITUTION_STATE | state | state name or 2-letter code | TEXT |
| INSTITUTION_STATE_NAME | state | state name or 2-letter code | TEXT |
| BRANCH_ZIP | zip | ZIP / postal code | TEXT |
| INSTITUTION_ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FEC_BULK
| column | kind | description | type |
|---|---|---|---|
| CMTE_CITY | city | city / town / municipality | TEXT |
| CMTE_ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FEC_BULK_COMMITTEES
| column | kind | description | type |
|---|---|---|---|
| CMTE_CITY | city | city / town / municipality | TEXT |
| CMTE_ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FEC_CANDIDATES
| column | kind | description | type |
|---|---|---|---|
| CAND_CITY | city | city / town / municipality | TEXT |
| CAND_OFFICE_DISTRICT | cong_district | congressional / legislative district | TEXT |
| CAND_ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FEC_COMMITTEES
| column | kind | description | type |
|---|---|---|---|
| CMTE_CITY | city | city / town / municipality | TEXT |
| CMTE_ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
| column | kind | description | type |
|---|---|---|---|
| CAN_OFFICE_STATE | state | state name or 2-letter code | TEXT |

### FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FHFA_FHLB_MEMBERSHIP
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### FINANCE__FED_FINRA_MPID_LIST
| column | kind | description | type |
|---|---|---|---|
| LOCATION | facility_site | site / location / place name | TEXT |

### FINANCE__FED_IRS_SOI
| column | kind | description | type |
|---|---|---|---|
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_MSRB_REGISTRANTS
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### FINANCE__FED_NCUA_CALL_REPORTS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_NCUA_CALL_REPORTS_FOICU
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| COUNTY_CODE | county | county name or code | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_NCUA_CHARTER_MERGER_EVENTS
| column | kind | description | type |
|---|---|---|---|
| CONTINUING_LOCATION | facility_site | site / location / place name | TEXT |
| MERGING_LOCATION | facility_site | site / location / place name | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |

### FINANCE__FED_NCUA_FEDERALLY_INSURED_CU_LIST
| column | kind | description | type |
|---|---|---|---|
| STREET_MAILING_ADDRESS | address | street / mailing address | TEXT |
| CITY_MAILING_ADDRESS | city | city / town / municipality | TEXT |
| NCUA_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE_MAILING_ADDRESS | state | state name or 2-letter code | TEXT |
| ZIP_CODE_MAILING_ADDRESS | zip | ZIP / postal code | TEXT |

### FINANCE__FED_OCC_NATIONAL_BANKS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LOC | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### FINANCE__FED_OCC_THRIFTS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LOC | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### FINANCE__FED_PCAOB_FORM_AP_FILINGS
| column | kind | description | type |
|---|---|---|---|
| SIGNED_EMAIL_ADDRESS | address | street / mailing address | TEXT |
| FIRM_ISSUING_CITY | city | city / town / municipality | TEXT |
| FIRM_COUNTRY | country | country name / ISO code | TEXT |
| FIRM_ISSUING_COUNTRY | country | country name / ISO code | TEXT |
| FIRM_ISSUING_STATE | state | state name or 2-letter code | TEXT |

### FINANCE__FED_SEC_13F_FILERS
| column | kind | description | type |
|---|---|---|---|
| FILINGMANAGER_CITY | city | city / town / municipality | TEXT |
| FILINGMANAGER_ZIPCODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_SEC_BUSINESS_DEVELOPMENT_COMPANY_REPORT
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_1 | address | street / mailing address | TEXT |
| ADDRESS_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_SEC_CLOSED_END_FUND_INFORMATION
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_1 | address | street / mailing address | TEXT |
| ADDRESS_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_SEC_INSIDER_REPORTINGOWNER
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_1 | address | street / mailing address | TEXT |
| ADDRESS_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__INTL_ISO_MIC_REGISTRY
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| ISO_COUNTRY_CODE_ISO_3166 | country | country name / ISO code | TEXT |

### FINANCE__INTL_OSFI_REGULATED_FI
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| PROVINCE_STATE | state | state name or 2-letter code | TEXT |
| POSTAL_ZIP_CODE | zip | ZIP / postal code | TEXT |

### FINANCE__INTL_WB_IDS
| column | kind | description | type |
|---|---|---|---|
| COUNTRY_CODE | country | country name / ISO code | TEXT |
| COUNTRY_NAME | country | country name / ISO code | TEXT |

### FOREIGN_INFLUENCE__FED_FARA_BULK
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_1 | address | street / mailing address | TEXT |
| ADDRESS_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY_LOCATION_REPRESENTED | country | country name / ISO code | TEXT |
| FOREIGN_PRINCIPAL_COUNTRY | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### GOVERNMENT_RECORDS__FED_NARA_AAD
| column | kind | description | type |
|---|---|---|---|
| GEO_LOCATION | facility_site | site / location / place name | TEXT |
| FIPS_GEO | fips | FIPS / GEOID census code | TEXT |

### HEALTH__FED_CDC_ANXIETY_DEPRESSION
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CDC_DRUG_POISONING_COUNTY
| column | kind | description | type |
|---|---|---|---|
| COUNTY | county | county name or code | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| FIPS_STATE | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CDC_HEALTH_INSURANCE
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
| column | kind | description | type |
|---|---|---|---|
| GEOID | fips | FIPS / GEOID census code | TEXT |
| ST_GEOID | fips | FIPS / GEOID census code | TEXT |

### HEALTH__FED_CDC_LEADING_CAUSES_STATE
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CDC_OVERDOSE
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CMS_DIALYSIS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| LONG_TERM_CATHETER_DATA_AVAILABILITY_CODE | coordinates | latitude / longitude point | FLOAT |
| NUMBER_OF_PATIENTS_IN_LONG_TERM_CATHETER_SUMMARY | coordinates | latitude / longitude point | NUMBER |
| NUMBER_OF_PATIENT_MONTHS_IN_LONG_TERM_CATHETER_SUMMARY | coordinates | latitude / longitude point | NUMBER |
| PERCENTAGE_OF_ADULT_PATIENTS_WITH_LONG_TERM_CATHETER_IN_USE | coordinates | latitude / longitude point | FLOAT |
| COUNTY_PARISH | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| LONG_STAY_PERCENT | coordinates | latitude / longitude point | FLOAT |
| LONG_STAY_RESIDENTS | coordinates | latitude / longitude point | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| FIPS_COUNTY_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| ENROLLMENT_STATE | state | state name or 2-letter code | TEXT |
| INCORPORATION_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_HCRIS
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| OTHER_LONG_TERM_LIABILITIES | coordinates | latitude / longitude point | FLOAT |
| TOTAL_LONG_TERM_LIABILITIES | coordinates | latitude / longitude point | FLOAT |
| COUNTY | county | county name or code | TEXT |
| MEDICARE_CBSA_NUMBER | metro | metro / CBSA / MSA area | TEXT |
| RURAL_VERSUS_URBAN | metro | metro / CBSA / MSA area | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_HOME_HEALTH
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| DENOMINATOR_FOR_HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | street / mailing address | TEXT |
| FOOTNOTE_FOR_HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | street / mailing address | TEXT |
| HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | street / mailing address | TEXT |
| NUMERATOR_FOR_HOW_OFTEN_PHYSICIAN_RECOMMENDED_ACTIONS_TO_ADDRESS_MEDICATION_ISSUES_WERE_COMPLETELY_TIMELY | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LOCATION_OTHER_TYPE_TEXT | facility_site | site / location / place name | NUMBER |
| PRACTICE_LOCATION_TYPE | facility_site | site / location / place name | TEXT |
| ENROLLMENT_STATE | state | state name or 2-letter code | TEXT |
| INCORPORATION_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_HOSPICE
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| COUNTY_PARISH | county | county name or code | TEXT |
| CMS_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_HOSPITAL_COMPARE
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| COUNTY_PARISH | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| SUBGROUP_LONG_TERM | coordinates | latitude / longitude point | TEXT |
| LOCATION_OTHER_TYPE_TEXT | facility_site | site / location / place name | TEXT |
| PRACTICE_LOCATION_TYPE | facility_site | site / location / place name | TEXT |
| ENROLLMENT_STATE | state | state name or 2-letter code | TEXT |
| INCORPORATION_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_HOSPITAL_GENERAL
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| COUNTY_PARISH | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_HPT_MRF
| column | kind | description | type |
|---|---|---|---|
| HOSPITAL_ADDRESS | address | street / mailing address | TEXT |
| HOSPITAL_LOCATION | facility_site | site / location / place name | TEXT |

### HEALTH__FED_CMS_IRF
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| COUNTY_PARISH | county | county name or code | TEXT |
| CMS_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_LTCH
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| COUNTY_PARISH | county | county name or code | TEXT |
| CMS_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MAIN
| column | kind | description | type |
|---|---|---|---|
| FIPS | fips | FIPS / GEOID census code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| STREET_ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LOCATION_1 | facility_site | site / location / place name | TEXT |
| LOCATION_NAME | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER
| column | kind | description | type |
|---|---|---|---|
| RFRG_PRVDR_CITY | city | city / town / municipality | TEXT |
| RFRG_PRVDR_CNTRY | country | country name / ISO code | NUMBER |
| RFRG_PRVDR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| RFRG_PRVDR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| RFRG_PRVDR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| RFRG_PRVDR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| RFRG_PRVDR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL
| column | kind | description | type |
|---|---|---|---|
| SUPLR_PRVDR_CITY | city | city / town / municipality | TEXT |
| SUPLR_PRVDR_CNTRY | country | country name / ISO code | NUMBER |
| SUPLR_PRVDR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| SUPLR_PRVDR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| SUPLR_PRVDR_RUCA_CAT | metro | metro / CBSA / MSA area | TEXT |
| SUPLR_PRVDR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| SUPLR_PRVDR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| SUPLR_PRVDR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER
| column | kind | description | type |
|---|---|---|---|
| RNDRNG_PRVDR_CITY | city | city / town / municipality | TEXT |
| RNDRNG_PRVDR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| RNDRNG_PRVDR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| RNDRNG_PRVDR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE
| column | kind | description | type |
|---|---|---|---|
| RNDRNG_PRVDR_CITY | city | city / town / municipality | TEXT |
| RNDRNG_PRVDR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| RNDRNG_PRVDR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| RNDRNG_PRVDR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE
| column | kind | description | type |
|---|---|---|---|
| RNDRNG_PRVDR_CITY | city | city / town / municipality | TEXT |
| RNDRNG_PRVDR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| RNDRNG_PRVDR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| RNDRNG_PRVDR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
| column | kind | description | type |
|---|---|---|---|
| RNDRNG_PRVDR_CITY | city | city / town / municipality | TEXT |
| RNDRNG_PRVDR_CNTRY | country | country name / ISO code | NUMBER |
| RNDRNG_PRVDR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| RNDRNG_PRVDR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| RNDRNG_PRVDR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI
| column | kind | description | type |
|---|---|---|---|
| RNDRNG_PRVDR_CITY | city | city / town / municipality | TEXT |
| RNDRNG_PRVDR_CNTRY | country | country name / ISO code | NUMBER |
| PLACE_OF_SRVC | facility_site | site / location / place name | TEXT |
| RNDRNG_PRVDR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| RNDRNG_PRVDR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| RNDRNG_PRVDR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_MEDICARE_PROVIDER
| column | kind | description | type |
|---|---|---|---|
| RNDRNG_PRVDR_CITY | city | city / town / municipality | TEXT |
| RNDRNG_PRVDR_CNTRY | country | country name / ISO code | NUMBER |
| RNDRNG_PRVDR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| RNDRNG_PRVDR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| RNDRNG_PRVDR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| RNDRNG_PRVDR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_NPPES
| column | kind | description | type |
|---|---|---|---|
| PROVIDER_BUSINESS_MAILING_ADDRESS_FAX_NUMBER | address | street / mailing address | TEXT |
| PROVIDER_BUSINESS_MAILING_ADDRESS_TELEPHONE_NUMBER | address | street / mailing address | TEXT |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_FAX_NUMBER | address | street / mailing address | TEXT |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_TELEPHONE_NUMBER | address | street / mailing address | TEXT |
| PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS | address | street / mailing address | TEXT |
| PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS | address | street / mailing address | TEXT |
| PROVIDER_SECOND_LINE_BUSINESS_MAILING_ADDRESS | address | street / mailing address | TEXT |
| PROVIDER_SECOND_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS | address | street / mailing address | TEXT |
| PROVIDER_BUSINESS_MAILING_ADDRESS_CITY_NAME | city | city / town / municipality | TEXT |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME | city | city / town / municipality | TEXT |
| PROVIDER_BUSINESS_MAILING_ADDRESS_COUNTRY_CODE_IF_OUTSIDE_U_S | country | country name / ISO code | TEXT |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_COUNTRY_CODE_IF_OUTSIDE_U_S | country | country name / ISO code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_1 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_10 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_11 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_12 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_13 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_14 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_15 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_16 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_17 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_18 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_19 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_2 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_20 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_21 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_22 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_23 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_24 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_25 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_26 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_27 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_28 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_29 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_3 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_30 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_31 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_32 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_33 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_34 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_35 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_36 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_37 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_38 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_39 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_4 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_40 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_41 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_42 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_43 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_44 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_45 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_46 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_47 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_48 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_49 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_5 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_50 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_6 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_7 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_8 | state | state name or 2-letter code | TEXT |
| OTHER_PROVIDER_IDENTIFIER_STATE_9 | state | state name or 2-letter code | TEXT |
| PROVIDER_BUSINESS_MAILING_ADDRESS_STATE_NAME | state | state name or 2-letter code | TEXT |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_1 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_10 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_11 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_12 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_13 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_14 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_15 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_2 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_3 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_4 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_5 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_6 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_7 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_8 | state | state name or 2-letter code | TEXT |
| PROVIDER_LICENSE_NUMBER_STATE_CODE_9 | state | state name or 2-letter code | TEXT |
| PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE | zip | ZIP / postal code | TEXT |
| PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_NURSING_HOME
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| LONG_STAY_QM_RATING | coordinates | latitude / longitude point | NUMBER |
| COUNTY_PARISH | county | county name or code | TEXT |
| PROVIDER_SSA_COUNTY_CODE | county | county name or code | TEXT |
| LOCATION | facility_site | site / location / place name | TEXT |
| COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| URBAN | metro | metro / CBSA / MSA area | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES
| column | kind | description | type |
|---|---|---|---|
| PROVIDER_ADDRESS | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| LOCATION | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES
| column | kind | description | type |
|---|---|---|---|
| PROVIDER_ADDRESS | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| LOCATION | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_NURSING_HOME_PENALTIES
| column | kind | description | type |
|---|---|---|---|
| PROVIDER_ADDRESS | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| LOCATION | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_OPEN_PAYMENTS
| column | kind | description | type |
|---|---|---|---|
| RECIPIENT_CITY | city | city / town / municipality | TEXT |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE | state | state name or 2-letter code | TEXT |
| RECIPIENT_ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_OPEN_PAYMENTS_2022
| column | kind | description | type |
|---|---|---|---|
| RECIPIENT_CITY | city | city / town / municipality | TEXT |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE | state | state name or 2-letter code | TEXT |
| RECIPIENT_ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_OPEN_PAYMENTS_2023
| column | kind | description | type |
|---|---|---|---|
| RECIPIENT_CITY | city | city / town / municipality | TEXT |
| APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_STATE | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE | state | state name or 2-letter code | TEXT |
| RECIPIENT_ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY_NAME | country | country name / ISO code | TEXT |
| LICENSE_STATE_CODE_1 | state | state name or 2-letter code | TEXT |
| LICENSE_STATE_CODE_2 | state | state name or 2-letter code | TEXT |
| LICENSE_STATE_CODE_3 | state | state name or 2-letter code | TEXT |
| LICENSE_STATE_CODE_4 | state | state name or 2-letter code | TEXT |
| LICENSE_STATE_CODE_5 | state | state name or 2-letter code | TEXT |
| PROVINCE_NAME | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIPCODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS
| column | kind | description | type |
|---|---|---|---|
| FIRST_LINE_STREET_ADDRESS | address | street / mailing address | TEXT |
| SECOND_LINE_STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY_NAME | city | city / town / municipality | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_PARTD_PRESCRIBERS
| column | kind | description | type |
|---|---|---|---|
| PRESCRIBER_CITY | city | city / town / municipality | TEXT |
| PRESCRIBER_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| PRESCRIBER_STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CMS_PART_D_PRESCRIBERS
| column | kind | description | type |
|---|---|---|---|
| PRSCRBR_CITY | city | city / town / municipality | TEXT |
| PRSCRBR_CNTRY | country | country name / ISO code | TEXT |
| PRSCRBR_STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| PRSCRBR_RUCA | metro | metro / CBSA / MSA area | TEXT |
| PRSCRBR_RUCA_DESC | metro | metro / CBSA / MSA area | TEXT |
| PRSCRBR_STATE_ABRVTN | state | state name or 2-letter code | TEXT |
| PRSCRBR_ZIP5 | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_POS_OTHER
| column | kind | description | type |
|---|---|---|---|
| CITY_NAME | city | city / town / municipality | TEXT |
| SSA_CNTY_CD | county | county name or code | NUMBER |
| FIPS_CNTY_CD | fips | FIPS / GEOID census code | NUMBER |
| FIPS_STATE_CD | fips | FIPS / GEOID census code | TEXT |
| CBSA_CD | metro | metro / CBSA / MSA area | TEXT |
| CBSA_URBN_RRL_IND | metro | metro / CBSA / MSA area | TEXT |
| SSA_STATE_CD | state | state name or 2-letter code | TEXT |
| STATE_CD | state | state name or 2-letter code | TEXT |
| STATE_RGN_CD | state | state name or 2-letter code | TEXT |
| ZIP_CD | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE
| column | kind | description | type |
|---|---|---|---|
| PRACTICE_STATE_OR_US_TERRITORY | state | state name or 2-letter code | TEXT |

### HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| ENROLLMENT_STATE | state | state name or 2-letter code | TEXT |
| INCORPORATION_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| ENROLLMENT_STATE | state | state name or 2-letter code | TEXT |
| INCORPORATION_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_DEA_ARCOS
| column | kind | description | type |
|---|---|---|---|
| BUYER_CITY | city | city / town / municipality | TEXT |
| REPORTER_CITY | city | city / town / municipality | TEXT |
| BUYER_COUNTY | county | county name or code | TEXT |
| REPORTER_COUNTY | county | county name or code | TEXT |
| BUYER_STATE | state | state name or 2-letter code | TEXT |
| REPORTER_STATE | state | state name or 2-letter code | TEXT |
| BUYER_ZIP | zip | ZIP / postal code | TEXT |
| REPORTER_ZIP | zip | ZIP / postal code | TEXT |

### HEALTH__FED_FDA_DEVICE_510K
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_1 | address | street / mailing address | TEXT |
| ADDRESS_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY_CODE | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| POSTAL_CODE | zip | ZIP / postal code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_FDA_DEVICE_ENFORCEMENT
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_1 | address | street / mailing address | TEXT |
| ADDRESS_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| POSTAL_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_FDA_DEVICE_PMA
| column | kind | description | type |
|---|---|---|---|
| STREET_1 | address | street / mailing address | TEXT |
| STREET_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |
| ZIP_EXT | zip | ZIP / postal code | TEXT |

### HEALTH__FED_FDA_DRUG_ENFORCEMENT
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_1 | address | street / mailing address | TEXT |
| ADDRESS_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| POSTAL_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_FDA_ESTABLISHMENT_REG
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| ISO_COUNTRY_CODE | country | country name / ISO code | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| POSTAL_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_FDA_FAERS_DEMO
| column | kind | description | type |
|---|---|---|---|
| OCCR_COUNTRY | country | country name / ISO code | TEXT |
| REPORTER_COUNTRY | country | country name / ISO code | TEXT |

### HEALTH__FED_FDA_MAUDE
| column | kind | description | type |
|---|---|---|---|
| MANUFACTURER_CITY | city | city / town / municipality | TEXT |
| MANUFACTURER_COUNTRY | country | country name / ISO code | TEXT |
| MANUFACTURER_STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_HHS_OIG_LEIE
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### HEALTH__FED_HRSA_HPSA_PRIMARY_CARE
| column | kind | description | type |
|---|---|---|---|
| HPSA_ADDRESS | address | street / mailing address | TEXT |
| HPSA_CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COMMON_COUNTY_NAME | county | county name or code | TEXT |
| COUNTY_EQUIVALENT_NAME | county | county name or code | TEXT |
| US_MEXICO_BORDER_COUNTY_INDICATOR | county | county name or code | TEXT |
| HPSA_GEOGRAPHY_ID | facility_site | site / location / place name | TEXT |
| COMMON_STATE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| COMMON_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIMARY_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| METROPOLITAN_INDICATOR | metro | metro / CBSA / MSA area | TEXT |
| METROPOLITAN_INDICATOR_CODE | metro | metro / CBSA / MSA area | TEXT |
| COMMON_REGION_NAME | region | region / area / territory / jurisdiction | TEXT |
| COMMON_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| COMMON_STATE_NAME | state | state name or 2-letter code | TEXT |
| COMPONENT_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| PRIMARY_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| PRIMARY_STATE_NAME | state | state name or 2-letter code | TEXT |
| STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |
| COMMON_POSTAL_CODE | zip | ZIP / postal code | TEXT |
| HPSA_POSTAL_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_HRSA_NPDB
| column | kind | description | type |
|---|---|---|---|
| HOME_COUNTRY | country | country name / ISO code | NUMBER |
| WORK_COUNTRY | country | country name / ISO code | NUMBER |
| HOME_STATE | state | state name or 2-letter code | TEXT |
| LICENSE_STATE | state | state name or 2-letter code | TEXT |
| WORK_STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_HRSA_SHORTAGE_AREAS
| column | kind | description | type |
|---|---|---|---|
| HPSA_ADDRESS | address | street / mailing address | TEXT |
| HPSA_CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COMMON_COUNTY_NAME | county | county name or code | TEXT |
| COUNTY_EQUIVALENT_NAME | county | county name or code | TEXT |
| COUNTY_OR_COUNTY_EQUIVALENT_FEDERAL_INFORMATION_PROCESSING_STANDARD_CODE | county | county name or code | TEXT |
| STATE_AND_COUNTY_FEDERAL_INFORMATION_PROCESSING_STANDARD_CODE | county | county name or code | TEXT |
| U_S_MEXICO_BORDER_COUNTY_INDICATOR | county | county name or code | TEXT |
| HPSA_GEOGRAPHY_IDENTIFICATION_NUMBER | facility_site | site / location / place name | TEXT |
| COMMON_STATE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| COMMON_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIMARY_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| HPSA_METROPOLITAN_INDICATOR_CODE | metro | metro / CBSA / MSA area | TEXT |
| METROPOLITAN_INDICATOR | metro | metro / CBSA / MSA area | TEXT |
| COMMON_REGION_NAME | region | region / area / territory / jurisdiction | TEXT |
| COMMON_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| COMMON_STATE_NAME | state | state name or 2-letter code | TEXT |
| HPSA_COMPONENT_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| PRIMARY_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| PRIMARY_STATE_NAME | state | state name or 2-letter code | TEXT |
| STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |
| COMMON_POSTAL_CODE | zip | ZIP / postal code | TEXT |
| HPSA_POSTAL_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES
| column | kind | description | type |
|---|---|---|---|
| HEALTH_CENTER_STREET_ADDRESS | address | street / mailing address | TEXT |
| SITE_ADDRESS | address | street / mailing address | TEXT |
| SITE_WEB_ADDRESS | address | street / mailing address | TEXT |
| HEALTH_CENTER_CITY | city | city / town / municipality | TEXT |
| SITE_CITY | city | city / town / municipality | TEXT |
| CONGRESSIONAL_DISTRICT_CODE | cong_district | congressional / legislative district | TEXT |
| CONGRESSIONAL_DISTRICT_NAME | cong_district | congressional / legislative district | TEXT |
| CONGRESSIONAL_DISTRICT_NUMBER | cong_district | congressional / legislative district | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COMPLETE_COUNTY_NAME | county | county name or code | TEXT |
| COUNTY_DESCRIPTION | county | county name or code | TEXT |
| COUNTY_EQUIVALENT_NAME | county | county name or code | TEXT |
| US_MEXICO_BORDER_COUNTY_INDICATOR | county | county name or code | TEXT |
| FQHC_SITE_MEDICARE_BILLING_NUMBER | facility_site | site / location / place name | TEXT |
| FQHC_SITE_NPI_NUMBER | facility_site | site / location / place name | TEXT |
| LOCATION_SETTING_DESCRIPTION | facility_site | site / location / place name | TEXT |
| LOCATION_SETTING_ID | facility_site | site / location / place name | TEXT |
| LOCATION_TYPE_DESCRIPTION | facility_site | site / location / place name | TEXT |
| LOCATION_TYPE_ID | facility_site | site / location / place name | TEXT |
| SITE_ADDED_TO_SCOPE_DATE | facility_site | site / location / place name | DATE |
| SITE_NAME | facility_site | site / location / place name | TEXT |
| SITE_TELEPHONE_NUMBER | facility_site | site / location / place name | TEXT |
| SITE_TYPE_DESCRIPTION | facility_site | site / location / place name | TEXT |
| SITE_TYPE_ID | facility_site | site / location / place name | TEXT |
| STATE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS_CONGRESSIONAL_DISTRICT_CODE | fips | FIPS / GEOID census code | TEXT |
| HHS_REGION_CODE | region | region / area / territory / jurisdiction | TEXT |
| HHS_REGION_NAME | region | region / area / territory / jurisdiction | TEXT |
| HEALTH_CENTER_STATE | state | state name or 2-letter code | TEXT |
| SITE_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |
| HEALTH_CENTER_ZIP_CODE | zip | ZIP / postal code | TEXT |
| SITE_POSTAL_CODE | zip | ZIP / postal code | TEXT |

### HEALTH__FED_IHS_FACILITIES
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| LOCATION_TYPE | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### HEALTH__FED_IHS_SCB_FACILITY
| column | kind | description | type |
|---|---|---|---|
| LOCATION_TYPE | facility_site | site / location / place name | TEXT |

### HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP
| column | kind | description | type |
|---|---|---|---|
| ZIP_FILE_NAME | zip | ZIP / postal code | TEXT |

### HEALTH__FED_NURSINGHOME411
| column | kind | description | type |
|---|---|---|---|
| PROVIDER_ADDRESS | address | street / mailing address | TEXT |
| CITY_TOWN | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY_PARISH | county | county name or code | TEXT |
| LOCATION | facility_site | site / location / place name | TEXT |
| CMS_REGION_NUMBER | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### HEALTH__FED_VA_SUICIDE_STATE
| column | kind | description | type |
|---|---|---|---|
| GEOGRAPHIC_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN
| column | kind | description | type |
|---|---|---|---|
| SLA1PORT | airport_port | airport / port / station code | TEXT |

### HISTORY__FED_DENSHO_DDR
| column | kind | description | type |
|---|---|---|---|
| FIPS | fips | FIPS / GEOID census code | TEXT |

### HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC
| column | kind | description | type |
|---|---|---|---|
| SLA1PORT | airport_port | airport / port / station code | TEXT |

### HISTORY__FED_WPA_SLAVE_NARRATIVES
| column | kind | description | type |
|---|---|---|---|
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### HOUSING__FED_CFPB_HMDA
| column | kind | description | type |
|---|---|---|---|
| CENSUS_TRACT | census_tract | census tract / block group | TEXT |
| TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | census tract / block group | NUMBER |
| TRACT_MINORITY_POPULATION_PERCENT | census_tract | census tract / block group | NUMBER |
| TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | census tract / block group | NUMBER |
| TRACT_OWNER_OCCUPIED_UNITS | census_tract | census tract / block group | NUMBER |
| TRACT_POPULATION | census_tract | census tract / block group | NUMBER |
| TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | census tract / block group | NUMBER |
| COUNTY_CODE | county | county name or code | TEXT |
| DERIVED_MSA_MD | metro | metro / CBSA / MSA area | TEXT |
| FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | metro / CBSA / MSA area | NUMBER |
| STATE_CODE | state | state name or 2-letter code | TEXT |

### HOUSING__FED_CFPB_HMDA_DC_ONLY
| column | kind | description | type |
|---|---|---|---|
| CENSUS_TRACT | census_tract | census tract / block group | TEXT |
| TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | census tract / block group | TEXT |
| TRACT_MINORITY_POPULATION_PERCENT | census_tract | census tract / block group | FLOAT |
| TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | census tract / block group | TEXT |
| TRACT_OWNER_OCCUPIED_UNITS | census_tract | census tract / block group | TEXT |
| TRACT_POPULATION | census_tract | census tract / block group | FLOAT |
| TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | census tract / block group | FLOAT |
| COUNTY_CODE | county | county name or code | TEXT |
| DERIVED_MSA_MD | metro | metro / CBSA / MSA area | TEXT |
| FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | metro / CBSA / MSA area | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |

### HOUSING__FED_CFPB_HMDA_HISTORIC
| column | kind | description | type |
|---|---|---|---|
| CENSUS_TRACT_NUMBER | census_tract | census tract / block group | TEXT |
| TRACT_TO_MSAMD_INCOME | census_tract | census tract / block group | NUMBER |
| COUNTY_CODE | county | county name or code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### HOUSING__FED_CFPB_HMDA_LAR
| column | kind | description | type |
|---|---|---|---|
| CENSUS_TRACT | census_tract | census tract / block group | TEXT |
| TRACT_MEDIAN_AGE_OF_HOUSING_UNITS | census_tract | census tract / block group | NUMBER |
| TRACT_MINORITY_POPULATION_PERCENT | census_tract | census tract / block group | NUMBER |
| TRACT_ONE_TO_FOUR_FAMILY_HOMES | census_tract | census tract / block group | NUMBER |
| TRACT_OWNER_OCCUPIED_UNITS | census_tract | census tract / block group | NUMBER |
| TRACT_POPULATION | census_tract | census tract / block group | NUMBER |
| TRACT_TO_MSA_INCOME_PERCENTAGE | census_tract | census tract / block group | NUMBER |
| COUNTY_CODE | county | county name or code | TEXT |
| DERIVED_MSA_MD | metro | metro / CBSA / MSA area | TEXT |
| FFIEC_MSA_MD_MEDIAN_FAMILY_INCOME | metro | metro / CBSA / MSA area | NUMBER |
| STATE_CODE | state | state name or 2-letter code | TEXT |

### HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
| column | kind | description | type |
|---|---|---|---|
| DAMAGED_CITY | city | city / town / municipality | TEXT |
| RENTAL_RESOURCE_CITY | city | city / town / municipality | TEXT |
| COUNTY | county | county name or code | TEXT |
| CURRENT_LOCATION | facility_site | site / location / place name | TEXT |
| HIGH_WATER_LOCATION | facility_site | site / location / place name | TEXT |
| CENSUS_GEOID | fips | FIPS / GEOID census code | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| DAMAGED_STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| RENTAL_RESOURCE_STATE_ABBREV | state | state name or 2-letter code | TEXT |
| DAMAGED_ZIP_CODE | zip | ZIP / postal code | TEXT |
| RENTAL_RESOURCE_ZIP_CODE | zip | ZIP / postal code | TEXT |

### HOUSING__FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK
| column | kind | description | type |
|---|---|---|---|
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### HOUSING__FED_FHFA_HPI
| column | kind | description | type |
|---|---|---|---|
| PLACE_ID | facility_site | site / location / place name | TEXT |
| PLACE_NAME | facility_site | site / location / place name | TEXT |

### HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
| column | kind | description | type |
|---|---|---|---|
| STD_ADDR | address | street / mailing address | TEXT |
| STD_CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| PLACE | facility_site | site / location / place name | TEXT |
| CBSA | metro | metro / CBSA / MSA area | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| STD_ZIP5 | zip | ZIP / postal code | TEXT |

### HOUSING__FED_HUD_DATA
| column | kind | description | type |
|---|---|---|---|
| FIPS | fips | FIPS / GEOID census code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT
| column | kind | description | type |
|---|---|---|---|
| PROPERTY_CITY | city | city / town / municipality | TEXT |
| PROPERTY_COUNTY | county | county name or code | TEXT |
| PROPERTY_STATE | state | state name or 2-letter code | TEXT |
| PROPERTY_ZIP | zip | ZIP / postal code | TEXT |

### HOUSING__FED_HUD_MF_FIRM_COMMITMENTS
| column | kind | description | type |
|---|---|---|---|
| PROJECT_CITY | city | city / town / municipality | TEXT |
| PROJECT_STATE | state | state name or 2-letter code | TEXT |

### HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_TYPE | address | street / mailing address | TEXT |
| HA_EMAIL_ADDRESS | address | street / mailing address | TEXT |
| STD_ADDRESS | address | street / mailing address | TEXT |
| CENSUS_TRACT | census_tract | census tract / block group | TEXT |
| TRACT_LEVEL_KEY | census_tract | census tract / block group | TEXT |
| STD_CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LAT_GEOCODED | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| LON_GEOCODED | coordinates | latitude / longitude point | NUMBER |
| COUNTY_LEVEL_KEY | county | county name or code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| CURRENT_COUNTY_NAME | county | county name or code | TEXT |
| CURRENT_COUNTY_SUBDIVISION | county | county name or code | TEXT |
| CURRENT_COUNTY_SUBDIVISION_NAME | county | county name or code | TEXT |
| PLACE_CLASS_CODE | facility_site | site / location / place name | NUMBER |
| PLACE_INCORPORATED_FLAG | facility_site | site / location / place name | NUMBER |
| PLACE_LEVEL_KEY | facility_site | site / location / place name | TEXT |
| PLACE_NAME | facility_site | site / location / place name | TEXT |
| COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| CURRENT_COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| PLACE_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| CBSA_CODE | metro | metro / CBSA / MSA area | TEXT |
| CBSA_NAME | metro | metro / CBSA / MSA area | TEXT |
| METRO_FLAG | metro | metro / CBSA / MSA area | TEXT |
| MSA_CODE | metro | metro / CBSA / MSA area | TEXT |
| MSA_NAME | metro | metro / CBSA / MSA area | TEXT |
| URBAN_RURAL_FLAG | metro | metro / CBSA / MSA area | TEXT |
| STD_STATE | state | state name or 2-letter code | TEXT |
| STD_ZIP5 | zip | ZIP / postal code | TEXT |
| ZCTA | zip | ZIP / postal code | TEXT |
| ZIP_CLASS | zip | ZIP / postal code | TEXT |

### HOUSING__FED_MAPPING_INEQUALITY
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| LAT | coordinates | latitude / longitude point | FLOAT |
| LON | coordinates | latitude / longitude point | FLOAT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| GEOMETRY | geometry | map shape / polygon / WKT | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS
| column | kind | description | type |
|---|---|---|---|
| MAIN_ADDRESS_LINE1 | address | street / mailing address | TEXT |
| MAIN_ADDRESS_LINE2 | address | street / mailing address | TEXT |
| MAIN_ADDRESS_LINE3 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| STATE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| ENROLLMENT_STATE | state | state name or 2-letter code | TEXT |
| INCORPORATION_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### IMMIGRATION__FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT
| column | kind | description | type |
|---|---|---|---|
| STATE_CD | state | state name or 2-letter code | TEXT |

### IMMIGRATION__FED_DHS_OHSS
| column | kind | description | type |
|---|---|---|---|
| REGION_OR_SECTOR | region | region / area / territory / jurisdiction | TEXT |

### IMMIGRATION__FED_DHS_YEARBOOK
| column | kind | description | type |
|---|---|---|---|
| COUNTRY_OF_BIRTH | country | country name / ISO code | TEXT |
| COUNTRY_OF_LAST_RESIDENCE | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### IMMIGRATION__FED_DOL_OFLC
| column | kind | description | type |
|---|---|---|---|
| AGENT_ATTORNEY_ADDRESS1 | address | street / mailing address | TEXT |
| AGENT_ATTORNEY_ADDRESS2 | address | street / mailing address | TEXT |
| EMPLOYER_ADDRESS1 | address | street / mailing address | TEXT |
| EMPLOYER_ADDRESS2 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_1 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_10 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_2 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_3 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_4 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_5 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_6 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_7 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_8 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS1_9 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_1 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_10 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_2 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_3 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_4 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_5 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_6 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_7 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_8 | address | street / mailing address | TEXT |
| WORKSITE_ADDRESS2_9 | address | street / mailing address | TEXT |
| AGENT_ATTORNEY_CITY | city | city / town / municipality | TEXT |
| EMPLOYER_CITY | city | city / town / municipality | TEXT |
| WORKSITE_CITY_1 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_10 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_2 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_3 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_4 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_5 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_6 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_7 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_8 | city | city / town / municipality | TEXT |
| WORKSITE_CITY_9 | city | city / town / municipality | TEXT |
| AGENT_ATTORNEY_COUNTRY | country | country name / ISO code | TEXT |
| EMPLOYER_COUNTRY | country | country name / ISO code | TEXT |
| WORKSITE_COUNTY_1 | county | county name or code | TEXT |
| WORKSITE_COUNTY_10 | county | county name or code | TEXT |
| WORKSITE_COUNTY_2 | county | county name or code | TEXT |
| WORKSITE_COUNTY_3 | county | county name or code | TEXT |
| WORKSITE_COUNTY_4 | county | county name or code | TEXT |
| WORKSITE_COUNTY_5 | county | county name or code | TEXT |
| WORKSITE_COUNTY_6 | county | county name or code | TEXT |
| WORKSITE_COUNTY_7 | county | county name or code | TEXT |
| WORKSITE_COUNTY_8 | county | county name or code | TEXT |
| WORKSITE_COUNTY_9 | county | county name or code | TEXT |
| AGENT_ATTORNEY_PROVINCE | state | state name or 2-letter code | TEXT |
| AGENT_ATTORNEY_STATE | state | state name or 2-letter code | TEXT |
| EMPLOYER_PROVINCE | state | state name or 2-letter code | TEXT |
| EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| NAME_OF_HIGHEST_STATE_COURT | state | state name or 2-letter code | TEXT |
| STATE_OF_HIGHEST_COURT | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_1 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_10 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_2 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_3 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_4 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_5 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_6 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_7 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_8 | state | state name or 2-letter code | TEXT |
| WORKSITE_STATE_9 | state | state name or 2-letter code | TEXT |
| AGENT_ATTORNEY_POSTAL_CODE | zip | ZIP / postal code | TEXT |
| EMPLOYER_POSTAL_CODE | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_1 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_10 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_2 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_3 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_4 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_5 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_6 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_7 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_8 | zip | ZIP / postal code | TEXT |
| WORKSITE_POSTAL_CODE_9 | zip | ZIP / postal code | TEXT |

### IMMIGRATION__FED_ICE_DETAINERS
| column | kind | description | type |
|---|---|---|---|
| CRIMINAL_STREET_GANG_YES_NO | address | street / mailing address | TEXT |
| PORT_OF_DEPARTURE | airport_port | airport / port / station code | TEXT |
| FACILITY_CITY | city | city / town / municipality | TEXT |
| BIRTH_COUNTRY | country | country name / ISO code | TEXT |
| CITIZENSHIP_COUNTRY | country | country name / ISO code | TEXT |
| DEPARTURE_COUNTRY | country | country name / ISO code | TEXT |
| TOD_CURRENT_DUTY_SITE | facility_site | site / location / place name | TEXT |
| FACILITY_STATE | state | state name or 2-letter code | TEXT |

### IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### IMMIGRATION__FED_ICE_DETENTION_FACILITY_LIST
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### IMMIGRATION__FED_ICE_DETENTION_STINTS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| BIRTH_COUNTRY | country | country name / ISO code | TEXT |
| CITIZENSHIP_COUNTRY | country | country name / ISO code | TEXT |
| DEPARTURE_COUNTRY | country | country name / ISO code | TEXT |
| COUNTY | county | county name or code | TEXT |
| BOOK_IN_SITE | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### IMMIGRATION__FED_ICE_STATISTICS
| column | kind | description | type |
|---|---|---|---|
| COUNTRY_OF_CITIZENSHIP | country | country name / ISO code | TEXT |

### IMMIGRATION__FED_USCIS_DATA
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### IMMIGRATION__XC_OWID_REFUGEES
| column | kind | description | type |
|---|---|---|---|
| REFUGEES_BY_COUNTRY_OF_ORIGIN | country | country name / ISO code | NUMBER |
| WORLD_REGION_ACCORDING_TO_OWID | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__COUNTY_DOUBLE_BURDEN
| column | kind | description | type |
|---|---|---|---|
| COUNTY_NAME | county | county name or code | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### JUSTICE__FED_ATF_FFL
| column | kind | description | type |
|---|---|---|---|
| MAIL_STREET | address | street / mailing address | TEXT |
| PREMISE_STREET | address | street / mailing address | TEXT |
| MAIL_CITY | city | city / town / municipality | TEXT |
| PREMISE_CITY | city | city / town / municipality | TEXT |
| LIC_DISTRICT | cong_district | congressional / legislative district | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| LIC_COUNTY | county | county name or code | TEXT |
| LIC_REGION | region | region / area / territory / jurisdiction | TEXT |
| MAIL_STATE | state | state name or 2-letter code | TEXT |
| PREMISE_STATE | state | state name or 2-letter code | TEXT |
| MAIL_ZIP_CODE | zip | ZIP / postal code | TEXT |
| PREMISE_ZIP_CODE | zip | ZIP / postal code | TEXT |

### JUSTICE__FED_BOP_STATISTICS
| column | kind | description | type |
|---|---|---|---|
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |

### JUSTICE__FED_COURTLISTENER_COURTHOUSES
| column | kind | description | type |
|---|---|---|---|
| ADDRESS1 | address | street / mailing address | TEXT |
| ADDRESS2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY_CODE | country | country name / ISO code | TEXT |
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### JUSTICE__FED_COURTLISTENER_COURTS
| column | kind | description | type |
|---|---|---|---|
| JURISDICTION | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS
| column | kind | description | type |
|---|---|---|---|
| LOCATION | facility_site | site / location / place name | TEXT |

### JUSTICE__FED_COURTLISTENER_DOCKETS
| column | kind | description | type |
|---|---|---|---|
| JURISDICTION_TYPE | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED
| column | kind | description | type |
|---|---|---|---|
| DISTRICT_ID | cong_district | congressional / legislative district | TEXT |
| COUNTY_OF_RESIDENCE | county | county name or code | TEXT |
| JURISDICTION | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__FED_COURTLISTENER_JUDGES
| column | kind | description | type |
|---|---|---|---|
| DOB_CITY | city | city / town / municipality | TEXT |
| DOD_CITY | city | city / town / municipality | TEXT |
| DOB_COUNTRY | country | country name / ISO code | TEXT |
| DOD_COUNTRY | country | country name / ISO code | TEXT |
| DOB_STATE | state | state name or 2-letter code | TEXT |
| DOD_STATE | state | state name or 2-letter code | TEXT |

### JUSTICE__FED_COURTLISTENER_POSITIONS
| column | kind | description | type |
|---|---|---|---|
| LOCATION_CITY | city | city / town / municipality | TEXT |
| LOCATION_STATE | state | state name or 2-letter code | TEXT |

### JUSTICE__FED_DOJ_FCA_SETTLEMENTS
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |

### JUSTICE__FED_FBI_CDE
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### JUSTICE__FED_FBI_NICS_CHECKS
| column | kind | description | type |
|---|---|---|---|
| LONG_GUN | coordinates | latitude / longitude point | FLOAT |
| PREPAWN_LONG_GUN | coordinates | latitude / longitude point | FLOAT |
| PRIVATE_SALE_LONG_GUN | coordinates | latitude / longitude point | FLOAT |
| REDEMPTION_LONG_GUN | coordinates | latitude / longitude point | FLOAT |
| RENTALS_LONG_GUN | coordinates | latitude / longitude point | FLOAT |
| RETURNED_LONG_GUN | coordinates | latitude / longitude point | FLOAT |
| RETURN_TO_SELLER_LONG_GUN | coordinates | latitude / longitude point | FLOAT |
| STATE | state | state name or 2-letter code | TEXT |

### JUSTICE__FED_FHFA_SUSPENDED_COUNTERPARTIES
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### JUSTICE__FED_FJC_IDB_APPELLATE
| column | kind | description | type |
|---|---|---|---|
| DISTRICT_CIRCUIT | cong_district | congressional / legislative district | TEXT |
| DISTRICT_COURT | cong_district | congressional / legislative district | TEXT |
| DISTRICT_DEFENDANT_NUMBER | cong_district | congressional / legislative district | TEXT |
| DISTRICT_DOCKET | cong_district | congressional / legislative district | TEXT |
| DISTRICT_DOCKET_DATE | cong_district | congressional / legislative district | DATE |
| DISTRICT_JUDGE | cong_district | congressional / legislative district | TEXT |
| DISTRICT_OFFICE | cong_district | congressional / legislative district | TEXT |
| JURISDICTION | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__FED_FJC_IDB_BANKRUPTCY
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| DEBTOR1_COUNTY | county | county name or code | TEXT |
| DEBTOR2_COUNTY | county | county name or code | TEXT |
| DEBTOR1_ZIP | zip | ZIP / postal code | TEXT |
| DEBTOR2_ZIP | zip | ZIP / postal code | TEXT |

### JUSTICE__FED_FJC_IDB_CIVIL
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| COUNTY | county | county name or code | TEXT |
| JURISDICTION | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__FED_FJC_IDB_CRIMINAL
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| TRANSFER_DISTRICT | cong_district | congressional / legislative district | TEXT |
| COUNTY | county | county name or code | TEXT |

### JUSTICE__FED_JPML_PENDING_MDLS
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |

### JUSTICE__FED_SCDB
| column | kind | description | type |
|---|---|---|---|
| JURISDICTION_CODE | region | region / area / territory / jurisdiction | NUMBER |
| ADMIN_ACTION_STATE_CODE | state | state name or 2-letter code | NUMBER |
| CASE_ORIGIN_STATE_CODE | state | state name or 2-letter code | NUMBER |
| CASE_SOURCE_STATE_CODE | state | state name or 2-letter code | NUMBER |
| PETITIONER_STATE_CODE | state | state name or 2-letter code | NUMBER |
| RESPONDENT_STATE_CODE | state | state name or 2-letter code | NUMBER |

### JUSTICE__FED_USCOURTS_STATS
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| COUNTY | county | county name or code | TEXT |
| FIPS_CODE | fips | FIPS / GEOID census code | TEXT |

### JUSTICE__INTL_AUSTLII
| column | kind | description | type |
|---|---|---|---|
| JURISDICTION | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__INTL_EURLEX_CELLAR
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### JUSTICE__INTL_EU_SANCTIONS
| column | kind | description | type |
|---|---|---|---|
| ADDR_LEBA_NUMTITLE | address | street / mailing address | TEXT |
| ADDR_LEBA_PUBLICATION_DATE | address | street / mailing address | DATE |
| ADDR_LEBA_URL | address | street / mailing address | TEXT |
| ADDR_LOGICAL_ID | address | street / mailing address | TEXT |
| ADDR_NUMBER | address | street / mailing address | TEXT |
| ADDR_OTHER | address | street / mailing address | TEXT |
| ADDR_PROGRAMME | address | street / mailing address | TEXT |
| ADDR_STREET | address | street / mailing address | TEXT |
| ADDR_CITY | city | city / town / municipality | TEXT |
| ADDR_COUNTRY | country | country name / ISO code | TEXT |
| BIRT_COUNTRY | country | country name / ISO code | TEXT |
| CITI_COUNTRY | country | country name / ISO code | TEXT |
| IDEN_COUNTRY | country | country name / ISO code | TEXT |
| BIRT_PLACE | facility_site | site / location / place name | TEXT |
| ADDR_ZIPCODE | zip | ZIP / postal code | TEXT |

### JUSTICE__INTL_EU_SOCTA_EUROPOL
| column | kind | description | type |
|---|---|---|---|
| GEOGRAPHIC_SCOPE | facility_site | site / location / place name | TEXT |

### JUSTICE__INTL_HUDOC
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### JUSTICE__INTL_NTI_CNS_DPRK_MISSILE_TESTS
| column | kind | description | type |
|---|---|---|---|
| FACILITY_LATITUDE | coordinates | latitude / longitude point | FLOAT |
| FACILITY_LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| FACILITY_LOCATION | facility_site | site / location / place name | TEXT |
| LANDING_LOCATION | facility_site | site / location / place name | TEXT |

### JUSTICE__INTL_OPENSANCTIONS
| column | kind | description | type |
|---|---|---|---|
| COUNTRIES | country | country name / ISO code | TEXT |

### JUSTICE__INTL_OPENSANCTIONS_DEFAULT
| column | kind | description | type |
|---|---|---|---|
| COUNTRIES | country | country name / ISO code | TEXT |

### JUSTICE__INTL_UCDP_GED
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| WHERE_COORDINATES | coordinates | latitude / longitude point | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| COUNTRY_ID | country | country name / ISO code | TEXT |
| GEOM_WKT | geometry | map shape / polygon / WKT | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__RACIAL_JAIL_DISPARITY
| column | kind | description | type |
|---|---|---|---|
| COUNTY_NAME | county | county name or code | TEXT |
| COUNTY_YEAR_KEY | county | county name or code | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |

### JUSTICE__STATE_MO_SEX_OFFENDER_REGISTRY
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### JUSTICE__XC_MAPPING_POLICE_VIOLENCE
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS_OF_INCIDENT | address | street / mailing address | TEXT |
| CENSUS_TRACT_CODE | census_tract | census tract / block group | TEXT |
| MEDIAN_HOUSEHOLD_INCOME_ACS_CENSUS_TRACT | census_tract | census tract / block group | TEXT |
| TOTAL_POPULATION_OF_CENSUS_TRACT_2019_ACS_5_YEAR_ESTIMATES | census_tract | census tract / block group | TEXT |
| CITY | city | city / town / municipality | TEXT |
| CONGRESSIONAL_DISTRICT | cong_district | congressional / legislative district | TEXT |
| CONGRESSIONAL_REPRESENTATIVE_FULL_NAME_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES | cong_district | congressional / legislative district | TEXT |
| CONGRESSIONAL_REPRESENTATIVE_PARTY_HTTPS_BALLOTPEDIA_ORG_UNITED_STATES_HOUSE_OF_REPRESENTATIVES | cong_district | congressional / legislative district | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY | county | county name or code | TEXT |
| HUD_UPSAI_GEOGRAPHY | facility_site | site / location / place name | TEXT |
| NCHS_URBAN_RURAL_CLASSIFICATION_SCHEME_CODES_HTTPS_WWW_CDC_GOV_NCHS_DATA_ACCESS_URBAN_RURAL_HTM | metro | metro / CBSA / MSA area | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| GEOGRAPHY_VIA_TRULIA_METHODOLOGY_BASED_ON_ZIPCODE_POPULATION_DENSITY_HTTP_JEDKOLKO_COM_WP_CONTENT_UPLOADS_2015_05_FULL_ZCTA_URBAN_SUBURBAN_RURAL_CLASSIFICATION_XLSX | zip | ZIP / postal code | TEXT |
| ZIPCODE | zip | ZIP / postal code | TEXT |

### JUSTICE__XC_OWID_HOMICIDE
| column | kind | description | type |
|---|---|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__XC_OWID_TERRORISM_DEATHS
| column | kind | description | type |
|---|---|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | region / area / territory / jurisdiction | TEXT |

### JUSTICE__XC_RANSOMWARELIVE_VICTIMS
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### JUSTICE__XC_UK_SANCTIONS_LIST
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| TOWN_OF_BIRTH | city | city / town / municipality | TEXT |
| ADDRESS_COUNTRY | country | country name / ISO code | TEXT |
| COUNTRY_OF_BIRTH | country | country name / ISO code | TEXT |
| ADDRESS_POSTAL_CODE | zip | ZIP / postal code | TEXT |

### JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST
| column | kind | description | type |
|---|---|---|---|
| ENTITY_ADDRESS | address | street / mailing address | TEXT |
| INDIVIDUAL_ADDRESS | address | street / mailing address | TEXT |
| NATIONALITY | country | country name / ISO code | TEXT |
| INDIVIDUAL_PLACE_OF_BIRTH | facility_site | site / location / place name | TEXT |

### JUSTICE__XC_VERA_INCARCERATION_TRENDS
| column | kind | description | type |
|---|---|---|---|
| COUNTY_CODE | county | county name or code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| METRO_AREA | metro | metro / CBSA / MSA area | TEXT |
| COMMUTING_ZONE | region | region / area / territory / jurisdiction | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |
| IS_UNIFIED_STATE | state | state name or 2-letter code | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |

### JUSTICE__XC_WAPO_FATAL_FORCE
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB
| column | kind | description | type |
|---|---|---|---|
| SB_ACTUARY_FOREIGN_ADDRESS1 | address | street / mailing address | TEXT |
| SB_ACTUARY_FOREIGN_ADDRESS2 | address | street / mailing address | TEXT |
| SB_ACTUARY_US_ADDRESS1 | address | street / mailing address | TEXT |
| SB_ACTUARY_US_ADDRESS2 | address | street / mailing address | TEXT |
| SB_PORT_PREFNDNG_FNDNG_CAR_AMT | airport_port | airport / port / station code | NUMBER |
| SB_ACTUARY_FOREIGN_CITY | city | city / town / municipality | TEXT |
| SB_ACTUARY_US_CITY | city | city / town / municipality | TEXT |
| SB_ACTUARY_FOREIGN_CNTRY | country | country name / ISO code | TEXT |
| SB_ACTUARY_FOREIGN_PROV_STATE | state | state name or 2-letter code | TEXT |
| SB_ACTUARY_US_STATE | state | state name or 2-letter code | TEXT |
| SB_ACTUARY_FOREIGN_POSTAL_CD | zip | ZIP / postal code | TEXT |
| SB_ACTUARY_US_ZIP | zip | ZIP / postal code | TEXT |

### LABOR__FED_DOL_OLMS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_ID | address | street / mailing address | TEXT |
| ADDRESS_TYPE | address | street / mailing address | TEXT |
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### LABOR__FED_MSHA_ACCIDENTS
| column | kind | description | type |
|---|---|---|---|
| FIPS_STATE_CD | fips | FIPS / GEOID census code | TEXT |

### LABOR__FED_MSHA_MINES
| column | kind | description | type |
|---|---|---|---|
| NEAREST_TOWN | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| FIPS_CNTY_CD | fips | FIPS / GEOID census code | TEXT |
| FIPS_CNTY_NM | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### LABOR__FED_OSHA_ITA_300A_SUMMARY_2023
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### LABOR__FED_OSHA_ITA_300A_SUMMARY_2025
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### LABOR__FED_OSHA_ITA_CASE_DETAIL_2023
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| NEW_INCIDENT_LOCATION | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### LABOR__FED_OSHA_ITA_CASE_DETAIL_2024
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| NEW_INCIDENT_LOCATION | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### LABOR__FED_OSHA_ITA_CASE_DETAIL_2025
| column | kind | description | type |
|---|---|---|---|
| STREET_ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| NEW_INCIDENT_LOCATION | facility_site | site / location / place name | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### LABOR__FED_PBGC_TRUSTEED_PLANS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS
| column | kind | description | type |
|---|---|---|---|
| LOCATION_SETTLEMENT_FILED | facility_site | site / location / place name | TEXT |
| OTHER_SINGLE_STATE_SETTLEMENTS | state | state name or 2-letter code | TEXT |
| STATE_COSTS_FEES | state | state name or 2-letter code | TEXT |

### MARITIME__FED_NOAA_AIS
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| POSITION_GEOGRAPHY | facility_site | site / location / place name | GEOGRAPHY |

### MONEY__DEBT_REPAYMENT_CLIFF
| column | kind | description | type |
|---|---|---|---|
| COUNTRY_CODE | country | country name / ISO code | TEXT |
| COUNTRY_NAME | country | country name / ISO code | TEXT |
| COUNTRY_YEAR_ID | country | country name / ISO code | TEXT |

### OPEN_DATA__INTL_BR_DADOS_GOV
| column | kind | description | type |
|---|---|---|---|
| GEOGRAPHIC_COVERAGE | facility_site | site / location / place name | TEXT |

### OPEN_DATA__INTL_CH_OPENDATASWISS
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### OPEN_DATA__INTL_CL_DATOSGOB
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### OPEN_DATA__INTL_ES_DATOSGOB
| column | kind | description | type |
|---|---|---|---|
| GEOGRAPHIC_COVERAGE | facility_site | site / location / place name | TEXT |

### OPEN_DATA__INTL_GE_DATAGOV
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### POLITICS__BILL_COSPONSORS
| column | kind | description | type |
|---|---|---|---|
| COSPONSOR_STATE | state | state name or 2-letter code | TEXT |

### POLITICS__CA_LOBBY_CHG_LOG
| column | kind | description | type |
|---|---|---|---|
| ENTITY_CITY | city | city / town / municipality | TEXT |
| FILER_CITY | city | city / town / municipality | TEXT |
| ENTITY_ZIP | zip | ZIP / postal code | TEXT |
| FILER_ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__CA_LOBBY_COVER
| column | kind | description | type |
|---|---|---|---|
| FIRM_CITY | city | city / town / municipality | TEXT |

### POLITICS__FEC_CANDIDATE
| column | kind | description | type |
|---|---|---|---|
| OFFICE_DISTRICT | cong_district | congressional / legislative district | TEXT |
| OFFICE_STATE | state | state name or 2-letter code | TEXT |

### POLITICS__FEC_COMMITTEE
| column | kind | description | type |
|---|---|---|---|
| CMTE_CITY | city | city / town / municipality | TEXT |
| CMTE_ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__FED_CONGRESS_LEGISLATORS
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### POLITICS__FED_EAC_EAVS
| column | kind | description | type |
|---|---|---|---|
| FIPSCODE | fips | FIPS / GEOID census code | TEXT |
| JURISDICTION_NAME | region | region / area / territory / jurisdiction | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_FULL | state | state name or 2-letter code | TEXT |

### POLITICS__FED_FCC_LICENSING
| column | kind | description | type |
|---|---|---|---|
| ADDRESS_LINE1 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| FCC_COUNTY_CODE | county | county name or code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### POLITICS__FED_FEC_API
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| CONTRIBUTOR_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| CONTRIBUTOR_ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__FED_FJC_JUDGES
| column | kind | description | type |
|---|---|---|---|
| BIRTH_CITY | city | city / town / municipality | TEXT |
| DEATH_CITY | city | city / town / municipality | TEXT |
| BIRTH_STATE | state | state name or 2-letter code | TEXT |
| DEATH_STATE | state | state name or 2-letter code | TEXT |

### POLITICS__FED_MEDSL_HOUSE_RETURNS
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### POLITICS__FED_MEDSL_PRESIDENT_RETURNS
| column | kind | description | type |
|---|---|---|---|
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### POLITICS__FED_MEDSL_SENATE_RETURNS
| column | kind | description | type |
|---|---|---|---|
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### POLITICS__FED_VOTEVIEW_MEMBERS
| column | kind | description | type |
|---|---|---|---|
| DISTRICT_CODE | cong_district | congressional / legislative district | TEXT |
| STATE_ABBREV | state | state name or 2-letter code | TEXT |
| STATE_ICPSR | state | state name or 2-letter code | TEXT |

### POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS
| column | kind | description | type |
|---|---|---|---|
| CONTRIBUTOR_CITY | city | city / town / municipality | TEXT |
| ELECTORAL_DISTRICT | cong_district | congressional / legislative district | TEXT |
| CONTRIBUTOR_PROVINCE | state | state name or 2-letter code | TEXT |
| CONTRIBUTOR_POSTAL_CODE | zip | ZIP / postal code | TEXT |

### POLITICS__INTL_FREEDOMHOUSE
| column | kind | description | type |
|---|---|---|---|
| COUNTRY_TERRITORY | country | country name / ISO code | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |

### POLITICS__INTL_OWID_MILSPEND
| column | kind | description | type |
|---|---|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | region / area / territory / jurisdiction | TEXT |

### POLITICS__IRS527_8871_ORGS
| column | kind | description | type |
|---|---|---|---|
| EMAIL_ADDRESS | address | street / mailing address | TEXT |
| MAILING_ADDR1 | address | street / mailing address | TEXT |
| MAILING_CITY | city | city / town / municipality | TEXT |
| MAILING_STATE | state | state name or 2-letter code | TEXT |
| MAILING_ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__IRS527_8872_REPORTS
| column | kind | description | type |
|---|---|---|---|
| CHANGE_OF_ADDRESS_IND | address | street / mailing address | TEXT |
| EMAIL_ADDRESS | address | street / mailing address | TEXT |
| MAILING_ADDR1 | address | street / mailing address | TEXT |
| MAILING_ADDR2 | address | street / mailing address | TEXT |
| BUSINESS_CITY | city | city / town / municipality | TEXT |
| CONTACT_CITY | city | city / town / municipality | TEXT |
| CUSTODIAN_CITY | city | city / town / municipality | TEXT |
| MAILING_CITY | city | city / town / municipality | TEXT |
| BUSINESS_STATE | state | state name or 2-letter code | TEXT |
| CONTACT_STATE | state | state name or 2-letter code | TEXT |
| CUSTODIAN_STATE | state | state name or 2-letter code | TEXT |
| MAILING_STATE | state | state name or 2-letter code | TEXT |
| PRE_OR_POST_ELECT_STATE | state | state name or 2-letter code | TEXT |
| BUSINESS_ZIP | zip | ZIP / postal code | TEXT |
| BUSINESS_ZIP_EXT | zip | ZIP / postal code | TEXT |
| CONTACT_ZIP | zip | ZIP / postal code | TEXT |
| CONTACT_ZIP_EXT | zip | ZIP / postal code | TEXT |
| CUSTODIAN_ZIP | zip | ZIP / postal code | TEXT |
| CUSTODIAN_ZIP_EXT | zip | ZIP / postal code | TEXT |
| MAILING_ZIP | zip | ZIP / postal code | TEXT |
| MAILING_ZIP_EXT | zip | ZIP / postal code | TEXT |

### POLITICS__IRS527_DIRECTORS_OFFICERS
| column | kind | description | type |
|---|---|---|---|
| ENTITY_CITY | city | city / town / municipality | TEXT |
| ENTITY_STATE | state | state name or 2-letter code | TEXT |
| ENTITY_ZIP | zip | ZIP / postal code | TEXT |
| ENTITY_ZIP_EXT | zip | ZIP / postal code | TEXT |

### POLITICS__IRS527_EAIN
| column | kind | description | type |
|---|---|---|---|
| STATE_ISSUED | state | state name or 2-letter code | TEXT |

### POLITICS__IRS527_RELATED_ENTITIES
| column | kind | description | type |
|---|---|---|---|
| ENTITY_CITY | city | city / town / municipality | TEXT |
| ENTITY_STATE | state | state name or 2-letter code | TEXT |
| ENTITY_ZIP | zip | ZIP / postal code | TEXT |
| ENTITY_ZIP_EXT | zip | ZIP / postal code | TEXT |

### POLITICS__MEMBER_BILL_RECORD
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### POLITICS__MEMBER_CROSSWALK
| column | kind | description | type |
|---|---|---|---|
| LAST_DISTRICT | cong_district | congressional / legislative district | TEXT |
| LAST_STATE | state | state name or 2-letter code | TEXT |

### POLITICS__MEMBER_FEC_ID
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### POLITICS__MEMBER_INDIV_DONATIONS
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### POLITICS__MEMBER_MONEY_RAISED
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### POLITICS__MEMBER_SPINE
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### POLITICS__MEMBER_VOTING_RECORD
| column | kind | description | type |
|---|---|---|---|
| STATE | state | state name or 2-letter code | TEXT |

### POLITICS__ST_CANNABIS_POLICY_BUNDLES
| column | kind | description | type |
|---|---|---|---|
| LEGISLATIVE_ACTION | cong_district | congressional / legislative district | FLOAT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| STATE_AB | state | state name or 2-letter code | TEXT |
| STATE_COURT_SIG_ACTION | state | state name or 2-letter code | TEXT |
| STATE_SALES_TAX_HIGH_RCL_APP | state | state name or 2-letter code | TEXT |
| STATE_SALES_TAX_HIGH_RCL_IMP | state | state name or 2-letter code | TEXT |

### POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION
| column | kind | description | type |
|---|---|---|---|
| EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NUMBER | address | street / mailing address | TEXT |
| STREET_NAME | address | street / mailing address | TEXT |
| STREET_NUMBER | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| EMPLOYER_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_EMPLOYER_CITY | city | city / town / municipality | TEXT |
| BOROUGH_CODE | county | county name or code | TEXT |
| EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_ZIP | zip | ZIP / postal code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION
| column | kind | description | type |
|---|---|---|---|
| EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NUMBER | address | street / mailing address | TEXT |
| STREET_NAME | address | street / mailing address | TEXT |
| STREET_NUMBER | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| EMPLOYER_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_EMPLOYER_CITY | city | city / town / municipality | TEXT |
| BOROUGH_CODE | county | county name or code | TEXT |
| EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_ZIP | zip | ZIP / postal code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION
| column | kind | description | type |
|---|---|---|---|
| EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NUMBER | address | street / mailing address | TEXT |
| STREET_NAME | address | street / mailing address | TEXT |
| STREET_NUMBER | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| EMPLOYER_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_EMPLOYER_CITY | city | city / town / municipality | TEXT |
| BOROUGH_CODE | county | county name or code | TEXT |
| EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_ZIP | zip | ZIP / postal code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS
| column | kind | description | type |
|---|---|---|---|
| EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NUMBER | address | street / mailing address | TEXT |
| STREET_NAME | address | street / mailing address | TEXT |
| STREET_NUMBER | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| EMPLOYER_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_EMPLOYER_CITY | city | city / town / municipality | TEXT |
| BOROUGH_CODE | county | county name or code | TEXT |
| EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_ZIP | zip | ZIP / postal code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS
| column | kind | description | type |
|---|---|---|---|
| EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_EMPLOYER_STREET_NUMBER | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NAME | address | street / mailing address | TEXT |
| INTERMEDIARY_STREET_NUMBER | address | street / mailing address | TEXT |
| STREET_NAME | address | street / mailing address | TEXT |
| STREET_NUMBER | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| EMPLOYER_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_CITY | city | city / town / municipality | TEXT |
| INTERMEDIARY_EMPLOYER_CITY | city | city / town / municipality | TEXT |
| BOROUGH_CODE | county | county name or code | TEXT |
| EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_EMPLOYER_STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_STATE | state | state name or 2-letter code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| INTERMEDIARY_ZIP | zip | ZIP / postal code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### POLITICS__WHO_WON
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### POLITICS__XC_OWID_CPI
| column | kind | description | type |
|---|---|---|---|
| WORLD_REGION_ACCORDING_TO_OWID | region | region / area / territory / jurisdiction | TEXT |

### PROCUREMENT__FED_SAM_EXCLUSIONS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### PROCUREMENT__FED_USASPENDING_BULK
| column | kind | description | type |
|---|---|---|---|
| RECIPIENT_ADDRESS_LINE_1 | address | street / mailing address | TEXT |
| RECIPIENT_ADDRESS_LINE_2 | address | street / mailing address | TEXT |
| AIRPORT_AUTHORITY | airport_port | airport / port / station code | TEXT |
| PORT_AUTHORITY | airport_port | airport / port / station code | TEXT |
| CITY_LOCAL_GOVERNMENT | city | city / town / municipality | TEXT |
| MUNICIPALITY_LOCAL_GOVERNMENT | city | city / town / municipality | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | city | city / town / municipality | TEXT |
| RECIPIENT_CITY_NAME | city | city / town / municipality | TEXT |
| SCHOOL_DISTRICT_LOCAL_GOVERNMENT | cong_district | congressional / legislative district | TEXT |
| COUNTRY_OF_PRODUCT_OR_SERVICE_ORIGIN | country | country name / ISO code | TEXT |
| COUNTRY_OF_PRODUCT_OR_SERVICE_ORIGIN_CODE | country | country name / ISO code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_CODE | country | country name / ISO code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTRY_NAME | country | country name / ISO code | TEXT |
| RECIPIENT_COUNTRY_CODE | country | country name / ISO code | TEXT |
| RECIPIENT_COUNTRY_NAME | country | country name / ISO code | TEXT |
| COUNTY_LOCAL_GOVERNMENT | county | county name or code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_COUNTY_NAME | county | county name or code | TEXT |
| RECIPIENT_COUNTY_NAME | county | county name or code | TEXT |
| PLACE_OF_MANUFACTURE | facility_site | site / location / place name | TEXT |
| PLACE_OF_MANUFACTURE_CODE | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_CURRENT | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_CD_ORIGINAL | facility_site | site / location / place name | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| HISTORICALLY_UNDERUTILIZED_BUSINESS_ZONE_HUBZONE_FIRM | region | region / area / territory / jurisdiction | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE | state | state name or 2-letter code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_STATE_NAME | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE_CODE | state | state name or 2-letter code | TEXT |
| RECIPIENT_STATE_NAME | state | state name or 2-letter code | TEXT |
| STATE_CONTROLLED_INSTITUTION_OF_HIGHER_LEARNING | state | state name or 2-letter code | TEXT |
| US_STATE_GOVERNMENT | state | state name or 2-letter code | TEXT |
| PRIMARY_PLACE_OF_PERFORMANCE_ZIP_4 | zip | ZIP / postal code | TEXT |
| RECIPIENT_ZIP_4_CODE | zip | ZIP / postal code | TEXT |

### PROCUREMENT__INTL_ADB_DATA
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | NUMBER |

### REFERENCE__FED_DHS_HIFLD
| column | kind | description | type |
|---|---|---|---|
| ADDRESS | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| LATITUDE | coordinates | latitude / longitude point | NUMBER |
| LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| COUNTY | county | county name or code | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### REFERENCE__FED_ITIS_GEOGRAPHIC_DIV
| column | kind | description | type |
|---|---|---|---|
| GEOGRAPHIC_VALUE | facility_site | site / location / place name | TEXT |
| ITIS_GEOGRAPHIC_DIV_KEY | facility_site | site / location / place name | TEXT |

### REFERENCE__FED_ITIS_JURISDICTION
| column | kind | description | type |
|---|---|---|---|
| ITIS_JURISDICTION_KEY | region | region / area / territory / jurisdiction | TEXT |
| JURISDICTION_VALUE | region | region / area / territory / jurisdiction | TEXT |

### REFERENCE__FED_ITIS_PUBLICATIONS
| column | kind | description | type |
|---|---|---|---|
| PUB_PLACE | facility_site | site / location / place name | TEXT |

### REFERENCE__FED_USGS_TOPOVIEW
| column | kind | description | type |
|---|---|---|---|
| COUNTIES | county | county name or code | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |

### REFERENCE__INTL_EG_CAPMAS
| column | kind | description | type |
|---|---|---|---|
| COUNTRY | country | country name / ISO code | TEXT |

### REFERENCE__INTL_GDELT
| column | kind | description | type |
|---|---|---|---|
| ACTIONGEO_LAT | coordinates | latitude / longitude point | FLOAT |
| ACTIONGEO_LONG | coordinates | latitude / longitude point | FLOAT |
| ACTOR1GEO_LAT | coordinates | latitude / longitude point | FLOAT |
| ACTOR1GEO_LONG | coordinates | latitude / longitude point | FLOAT |
| ACTOR2GEO_LAT | coordinates | latitude / longitude point | FLOAT |
| ACTOR2GEO_LONG | coordinates | latitude / longitude point | FLOAT |

### REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTRY_CODE | country | country name / ISO code | TEXT |
| COUNTRY_NAME | country | country name / ISO code | TEXT |
| LOCATION_NAME | facility_site | site / location / place name | TEXT |

### REF__DIM_GEOGRAPHY
| column | kind | description | type |
|---|---|---|---|
| CENTROID_LATITUDE | coordinates | latitude / longitude point | FLOAT |
| CENTROID_LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY_NAME | county | county name or code | TEXT |
| COUNTY_FIPS_SUFFIX | fips | FIPS / GEOID census code | TEXT |
| FIPS_CODE | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| EPA_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### REF__DIM_STATE
| column | kind | description | type |
|---|---|---|---|
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |
| CENSUS_REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE_ABBR | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### SCIENCE_RESEARCH__FED_NIH_REPORTER
| column | kind | description | type |
|---|---|---|---|
| ORG_CITY | city | city / town / municipality | TEXT |
| ORG_COUNTRY | country | country name / ISO code | TEXT |
| ORG_FIPS | fips | FIPS / GEOID census code | TEXT |
| ORG_STATE | state | state name or 2-letter code | TEXT |
| ORG_STATE_NAME | state | state name or 2-letter code | TEXT |
| ORG_ZIP | zip | ZIP / postal code | TEXT |

### SCIENCE_RESEARCH__FED_RETRACTION_WATCH
| column | kind | description | type |
|---|---|---|---|
| COUNTRIES | country | country name / ISO code | TEXT |

### SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS
| column | kind | description | type |
|---|---|---|---|
| ADDRESS1 | address | street / mailing address | TEXT |
| ADDRESS2 | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### SCIENCE_RESEARCH__XC_OSF_REGISTRATIONS
| column | kind | description | type |
|---|---|---|---|
| REGION_ID | region | region / area / territory / jurisdiction | TEXT |
| REVIEWS_STATE | state | state name or 2-letter code | TEXT |
| REVISION_STATE | state | state name or 2-letter code | TEXT |

### SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE
| column | kind | description | type |
|---|---|---|---|
| COUNTRIES | country | country name / ISO code | TEXT |

### SCIENCE__FED_NSF_AWARDS
| column | kind | description | type |
|---|---|---|---|
| CITY | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP | zip | ZIP / postal code | TEXT |

### SCIENCE__FED_USGS_EARTHQUAKES
| column | kind | description | type |
|---|---|---|---|
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| PLACE | facility_site | site / location / place name | TEXT |

### SCIENCE__INTL_EMBL_ENSEMBL
| column | kind | description | type |
|---|---|---|---|
| REGION | region | region / area / territory / jurisdiction | TEXT |
| SEQ_REGION_NAME | region | region / area / territory / jurisdiction | TEXT |

### TRANSPORT__FED_DOT_BTS
| column | kind | description | type |
|---|---|---|---|
| COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |

### TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY_CODE | country | country name / ISO code | TEXT |
| COUNTY_CODE | county | county name or code | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### TRANSPORT__FED_FAA_DATA_PORTAL
| column | kind | description | type |
|---|---|---|---|
| AIRPORT_ID | airport_port | airport / port / station code | TEXT |
| LAT | coordinates | latitude / longitude point | FLOAT |
| LON | coordinates | latitude / longitude point | FLOAT |
| GEOGRAPHIC_SCOPE | facility_site | site / location / place name | TEXT |
| FIPS | fips | FIPS / GEOID census code | TEXT |

### TRANSPORT__FED_FAA_REGISTRY
| column | kind | description | type |
|---|---|---|---|
| STREET | address | street / mailing address | TEXT |
| CITY | city | city / town / municipality | TEXT |
| COUNTRY | country | country name / ISO code | TEXT |
| COUNTY | county | county name or code | TEXT |
| REGION | region | region / area / territory / jurisdiction | TEXT |
| STATE | state | state name or 2-letter code | TEXT |
| ZIP_CODE | zip | ZIP / postal code | TEXT |

### TRANSPORT__FED_FRA_CASUALTIES
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY_CODE | county | county name or code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| GENERAL_LOCATION_OF_PERSON | facility_site | site / location / place name | TEXT |
| GENERAL_LOCATION_OF_PERSON_CODE | facility_site | site / location / place name | TEXT |
| LOCATION_OF_INJURY_ON_BODY | facility_site | site / location / place name | TEXT |
| SPECIFIC_LOCATION | facility_site | site / location / place name | TEXT |
| SPECIFIC_LOCATION_OF_PERSON | facility_site | site / location / place name | TEXT |
| SPECIFIC_LOCATION_OF_PERSON_CODE | facility_site | site / location / place name | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### TRANSPORT__FED_FRA_CROSSING_INCIDENTS
| column | kind | description | type |
|---|---|---|---|
| CITY_NAME | city | city / town / municipality | TEXT |
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| COUNTY_CODE | county | county name or code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| CROSSING_WARNING_LOCATION | facility_site | site / location / place name | TEXT |
| CROSSING_WARNING_LOCATION_CODE | facility_site | site / location / place name | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS
| column | kind | description | type |
|---|---|---|---|
| DISTRICT | cong_district | congressional / legislative district | TEXT |
| LATITUDE | coordinates | latitude / longitude point | FLOAT |
| LONGITUDE | coordinates | latitude / longitude point | FLOAT |
| COUNTY_CODE | county | county name or code | TEXT |
| COUNTY_NAME | county | county name or code | TEXT |
| LOCATION | facility_site | site / location / place name | TEXT |
| STATE_ABBREVIATION | state | state name or 2-letter code | TEXT |
| STATE_CODE | state | state name or 2-letter code | TEXT |
| STATE_NAME | state | state name or 2-letter code | TEXT |

### TRANSPORT__FED_FRA_SAFETY
| column | kind | description | type |
|---|---|---|---|
| COUNTY_FIPS | fips | FIPS / GEOID census code | TEXT |
| STATE_FIPS | fips | FIPS / GEOID census code | TEXT |

### TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT
| column | kind | description | type |
|---|---|---|---|
| OPER_ADDR_SAME | address | street / mailing address | TEXT |
| OPER_STREET | address | street / mailing address | TEXT |
| OWNER_STREET | address | street / mailing address | TEXT |
| DEST_CITY | city | city / town / municipality | TEXT |
| DPRT_CITY | city | city / town / municipality | TEXT |
| OPER_CITY | city | city / town / municipality | TEXT |
| OWNER_CITY | city | city / town / municipality | TEXT |
| DEST_COUNTRY | country | country name / ISO code | TEXT |
| DPRT_COUNTRY | country | country name / ISO code | TEXT |
| OPER_COUNTRY | country | country name / ISO code | TEXT |
| OWNER_COUNTRY | country | country name / ISO code | TEXT |
| SITE_SEEING | facility_site | site / location / place name | TEXT |
| DEST_STATE | state | state name or 2-letter code | TEXT |
| DPRT_STATE | state | state name or 2-letter code | TEXT |
| OPER_STATE | state | state name or 2-letter code | TEXT |
| OWNER_STATE | state | state name or 2-letter code | TEXT |
| OPER_ZIP | zip | ZIP / postal code | TEXT |
| OWNER_ZIP | zip | ZIP / postal code | TEXT |

### TRANSPORT__FED_NTSB_AVIATION_EVENTS
| column | kind | description | type |
|---|---|---|---|
| EV_CITY | city | city / town / municipality | TEXT |
| DEC_LATITUDE | coordinates | latitude / longitude point | NUMBER |
| DEC_LONGITUDE | coordinates | latitude / longitude point | NUMBER |
| LATITUDE | coordinates | latitude / longitude point | TEXT |
| LONGITUDE | coordinates | latitude / longitude point | TEXT |
| EV_COUNTRY | country | country name / ISO code | TEXT |
| LATLONG_ACQ | geometry | map shape / polygon / WKT | TEXT |
| EV_STATE | state | state name or 2-letter code | TEXT |
| EV_SITE_ZIPCODE | zip | ZIP / postal code | TEXT |
