# Duplicate-ingest drop list — 2026-08-10

Found while sorting the 170 "landed" catalog rows this session. Two piles:

## A. Landed twins of already-MODELED sources (same data ingested again under a
different name; row counts match the modeled source exactly). Dropping the twin
landing table + its registry row removes the duplicate storage and the false
"landed backlog" reading. All DROPs are Chris-only (classifier-blocked for
sessions). Row-count match verified live 2026-08-10; eyeball each before drop.

| twin landing table (LIBRARY_RAW.LANDING.*) | rows | modeled as |
|---|---|---|
| ICIJ_OFFSHORE_LEAKS_RELATIONSHIPS | 3,339,267 | fed_icij_offshoreleaks_relationships |
| XC_ICIJ_OFFSHORE_RELATIONSHIPS | 3,339,267 | fed_icij_offshoreleaks_relationships |
| ICIJ_OFFSHORE_LEAKS_ENTITIES | 814,344 | fed_icij_offshoreleaks_entities |
| XC_ICIJ_OFFSHORE_NODES_ENTITIES | 814,344 | fed_icij_offshoreleaks_entities |
| ICIJ_OFFSHORE_LEAKS_OFFICERS | 771,315 | fed_icij_offshoreleaks_officers |
| XC_ICIJ_OFFSHORE_NODES_OFFICERS | 771,315 | fed_icij_offshoreleaks_officers |
| ICIJ_OFFSHORE_LEAKS_ADDRESSES | 402,246 | fed_icij_offshoreleaks_addresses |
| XC_ICIJ_OFFSHORE_NODES_ADDRESSES | 402,246 | fed_icij_offshoreleaks_addresses |
| ICIJ_OFFSHORE_LEAKS_INTERMEDIARIES | 26,768 | fed_icij_offshoreleaks_intermediaries |
| XC_ICIJ_OFFSHORE_NODES_INTERMEDIARIES | 26,768 | fed_icij_offshoreleaks_intermediaries |
| FED_CMS_PECOS_PROVIDER_ENROLLMENT | 2,978,925 | fed_cms_medicare_fee_for_service_public_provider_enrollment |
| FED_EPA_ICIS_ICIS_AIR_TITLEV_CERTS | 2,574,815 | fed_epa_icis_air_icis_air_titlev_certs |
| FED_EPA_ICIS_ICIS_AIR_FCES_PCES | 1,779,096 | fed_epa_icis_air_icis_air_fces_pces |
| FED_EPA_ICIS_ICIS_AIR_POLLUTANTS | 978,398 | fed_epa_icis_air_icis_air_pollutants |
| FED_EPA_ICIS_ICIS_AIR_PROGRAMS | 457,581 | fed_epa_icis_air_icis_air_programs |
| FED_EPA_ICIS_ICIS_AIR_FACILITIES | 279,728 | fed_epa_icis_air_icis_air_facilities |
| FED_SBA_PPP_LOANS_150K_PLUS | 968,524 | fed_sba_ppp |
| FED_IRS_FATCA_FFI_LIST | 516,298 | fed_fatca_ffi |
| FED_IRS_527_ORGS | 77,591 | irs527_8871_orgs |
| INTL_UK_SANCTIONS_LIST | 57,883 | xc_uk_sanctions_list |
| STATE_OEHHA_PROP65_CHEMICALS | 1,021 | st_oehha_proposition_65_list |
| INTL_UN_SC_CONSOLIDATED_SANCTIONS | 1,011 | xc_un_consolidated_sanctions_list |
| INTL_UN_CONSOLIDATED_SANCTIONS | 1,011 | xc_un_consolidated_sanctions_list |
| FED_FHFA_SUSPENDED_COUNTERPARTY | 241 | fed_fhfa_suspended_counterparties |
| FED_FHFA_SUSPENDED_COUNTERPARTY_PROGRAM (registry row only; check table) | 241 | fed_fhfa_suspended_counterparties |

NOT twins (coincidental row-count matches, left in the backlog):
FED_EIA861_RELIABILITY (973), FED_EIA861_DEMAND_RESPONSE (340).

## B. Intra-landed duplicate pairs (same data landed twice, NEITHER modeled yet).
This session models ONE of each pair; the other joins the drop list.

| keep + model | drop twin | rows |
|---|---|---|
| FED_EPA_RCRA_VIOSNC_HISTORY | FED_EPA_RCRA_RCRA_VIOSNC_HISTORY | 2,675,581 |
| FED_EPA_RCRA_FACILITIES | FED_EPA_RCRA_RCRA_FACILITIES | 1,613,224 |
| FED_EPA_RCRA_EVALUATIONS | FED_EPA_RCRA_RCRA_EVALUATIONS | 1,166,410 |
| FED_EPA_RCRA_VIOLATIONS | FED_EPA_RCRA_RCRA_VIOLATIONS | 708,114 |
| FED_EPA_RCRA_ENFORCEMENTS | FED_EPA_RCRA_RCRA_ENFORCEMENTS | 383,519 |
CORRECTION (verified 2026-08-10): the two ITIS pairs are NOT twins — LONGNAMES
and STRIPPEDAUTHOR are legitimate distinct ITIS reference files whose row counts
happen to equal their siblings (one row per taxon / per author either way). Both
stay in the backlog; nothing ITIS goes on the drop list.
RCRA pairs ARE confirmed twins (identical column sets, identical counts).

Also near-twins in the EIA-860 family (two vintages, off-by-one counts):
FED_EIA_860_GENERATOR vs FED_EIA860_3_1_GENERATOR (26,857 / 26,856),
FED_EIA_860_PLANT vs FED_EIA860_2_PLANT, FED_EIA_860_UTILITY vs
FED_EIA860_1_UTILITY, FED_EIA_861_BALANCING_AUTHORITY vs
FED_EIA861_BALANCING_AUTHORITY (189/188). Decide vintage before modeling that
family; not dropped yet.

Drop one-liners (run as ACCOUNTADMIN, table A first, after eyeball):
each is `DROP TABLE LIBRARY_RAW.LANDING.<NAME>;` plus
`DELETE FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY WHERE UPPER(SOURCE_ID)=UPPER('<sid>');`
