# Portal Dataset Index — Wave 2

_Generated 2026-06-21 21:59:32 UTC · input: `portal_recon_results.json` · readers: ArcGIS / Socrata / CKAN · metadata only, nothing ingested._

## Headline

- **338,520 datasets indexed** across **96** live portals (100 attempted, 3 errored, 1 empty).
- **19,496 datasets (6%) carry at least one known join key** — the connectivity signal (light pass; full tagging is Wave 3).
- Columns captured for 78,651 (23%); row counts for 45,161 (13%). Missing = `unknown`, never guessed.

## By platform

| Platform | Portals (ok/err/empty) | Datasets |
|---|---|---:|
| ARCGIS | 37/2/1 | 95,348 |
| SOCRATA | 35/0/0 | 29,421 |
| CKAN | 24/1/0 | 213,751 |
| **TOTAL** | **96/3/1** | **338,520** |

## Join keys detected (light scan)

| Join key | Datasets |
|---|---:|
| ZIP | 11,146 |
| lat/lon | 7,796 |
| FIPS | 4,373 |
| NAICS | 364 |
| SIC | 153 |
| COUNTRY_ISO | 107 |
| NPI | 44 |
| EIN | 30 |
| DUNS | 6 |
| NDC | 4 |
| UEI | 2 |

## Top 20 portals by dataset count (the biggest boxes)

| # | Portal | Platform | Datasets | Capped? |
|---:|---|---|---:|:--:|
| 1 | intl_au_data_gov | CKAN | 25,000 | ⚠ |
| 2 | intl_ca_open_canada | CKAN | 25,000 | ⚠ |
| 3 | intl_hdx | CKAN | 25,000 | ⚠ |
| 4 | intl_uk_data_gov | CKAN | 25,000 | ⚠ |
| 5 | st_va_open | CKAN | 25,000 | ⚠ |
| 6 | intl_ie_datagovie | CKAN | 22,328 |  |
| 7 | intl_gr_datagov | CKAN | 20,900 |  |
| 8 | intl_nl_overheid | CKAN | 20,739 |  |
| 9 | intl_ua_datagov | CKAN | 13,200 |  |
| 10 | loc_dc_open | ARCGIS | 10,000 |  |
| 11 | loc_lacounty_open | ARCGIS | 10,000 |  |
| 12 | loc_tucson_open | ARCGIS | 9,786 |  |
| 13 | intl_co_datosgov | SOCRATA | 8,429 |  |
| 14 | loc_orangecounty_ca_open | ARCGIS | 8,002 |  |
| 15 | st_ut_open | SOCRATA | 6,738 |  |
| 16 | loc_louisville_open | ARCGIS | 5,067 |  |
| 17 | loc_minneapolis_open | ARCGIS | 4,665 |  |
| 18 | st_ca_open | CKAN | 4,480 |  |
| 19 | loc_harriscounty_open | ARCGIS | 4,351 |  |
| 20 | loc_baltimore_open | ARCGIS | 4,089 |  |

## ⚠ Portals with no index (4) — errored or empty

| Portal | Platform | Status | Reason |
|---|---|---|---|
| loc_philadelphia_open | ARCGIS | error | orgId resolve failed: HTTP 404 |
| loc_stlouis_open | ARCGIS | error | orgId resolve failed: HTTP 404 |
| st_ms_open | ARCGIS | empty | no datasets returned |
| intl_jo_opendata | CKAN | error | package_search failed: HTTP 400 |

## All portals

| Portal | Platform | Datasets | Status | Notes |
|---|---|---:|---|---|
| loc_dc_open | ARCGIS | 10,000 | ok | orgId=neT9SoYxizqTHZPH; api_total=23348 |
| loc_lacounty_open | ARCGIS | 10,000 | ok | orgId=RmCCgQtiZLDCtblq; api_total=13312 |
| loc_tucson_open | ARCGIS | 9,786 | ok | orgId=9coHY2fvuFjG9HQX; api_total=9786 |
| loc_orangecounty_ca_open | ARCGIS | 8,002 | ok | orgId=UXmFoWC7yDHcDN5Q; api_total=8002 |
| loc_louisville_open | ARCGIS | 5,067 | ok | orgId=79kfd2K6fskCAkyg; api_total=5067 |
| loc_minneapolis_open | ARCGIS | 4,665 | ok | orgId=afSMGVsC7QlRK1kZ; api_total=4665 |
| loc_harriscounty_open | ARCGIS | 4,351 | ok | orgId=su8ic9KbA7PYVxPS; api_total=4351 |
| loc_baltimore_open | ARCGIS | 4,089 | ok | orgId=UWYHeuuJISiGmgXx; api_total=4089 |
| loc_raleigh_open | ARCGIS | 3,754 | ok | orgId=v400IkDOw1ad7Yad; api_total=3754 |
| loc_maricopacounty_open | ARCGIS | 3,655 | ok | orgId=ykpntM6e3tHvzKRJ; api_total=3655 |
| loc_atlanta_open | ARCGIS | 3,007 | ok | orgId=5RxyIIJ9boPdptdo; api_total=3007 |
| loc_miamidade_open | ARCGIS | 2,417 | ok | orgId=8Pc9XBTAsYuxx9Ny; api_total=2417 |
| loc_fairfaxcounty_open | ARCGIS | 2,186 | ok | orgId=ioennV6PpG5Xodq0; api_total=2186 |
| loc_charlotte_open | ARCGIS | 1,983 | ok | orgId=9Nl857LBlQVyzq54; api_total=1983 |
| loc_mecklenburgcounty_open | ARCGIS | 1,863 | ok | orgId=BWD3gDuaqc7SQmy7; api_total=1863 |
| loc_detroit_open | ARCGIS | 1,844 | ok | orgId=qvkbeam7Wirps6zC; api_total=1844 |
| loc_tempe_open | ARCGIS | 1,701 | ok | orgId=lQySeXwbBg53XWDi; api_total=1701 |
| loc_nashville_open | ARCGIS | 1,481 | ok | orgId=HdTo6HJqh92wn4D8; api_total=1481 |
| loc_wakecounty_open | ARCGIS | 1,470 | ok | orgId=a7CWfuGP5ZnLYE7I; api_total=1470 |
| st_ky_open | ARCGIS | 1,455 | ok | orgId=ghsX9CKghMvyYjBU; api_total=1455 |
| loc_indianapolis_open | ARCGIS | 1,391 | ok | orgId=xBsPUWYKO89lShIO; api_total=1391 |
| loc_fortworth_open | ARCGIS | 1,306 | ok | orgId=3ddLCBXe1bRt7mzj; api_total=1306 |
| loc_columbus_open | ARCGIS | 1,276 | ok | orgId=9yy6msODkIBzkUXU; api_total=1276 |
| loc_nyc_palmbeach | ARCGIS | 998 | ok | orgId=ZWOoUZbtaYePLlPw; api_total=998 |
| st_vt_open | ARCGIS | 899 | ok | orgId=BkFxaEFNwHqX3tAw; api_total=899 |
| st_nh_open | ARCGIS | 889 | ok | orgId=wnvDDrXX8EouLkZP; api_total=889 |
| loc_memphis_open | ARCGIS | 884 | ok | orgId=saWmpKJIUAjyyNVc; api_total=884 |
| loc_hartford_open | ARCGIS | 848 | ok | orgId=WM6ZNcwewSWH8Mo9; api_total=848 |
| loc_sacramento_open | ARCGIS | 838 | ok | orgId=54falWtcpty3V47Z; api_total=838 |
| loc_cleveland_open | ARCGIS | 664 | ok | orgId=dty2kHktVXHrqO8i; api_total=664 |
| st_tn_open | ARCGIS | 640 | ok | orgId=YuVBSS7Y1of2Qud1; api_total=640 |
| loc_asheville_open | ARCGIS | 600 | ok | orgId=aJ16ENn1AaqdFlqx; api_total=600 |
| st_fl_open | ARCGIS | 480 | ok | orgId=Gh9awoU677aKree0; api_total=480 |
| intl_ke_opendata | ARCGIS | 388 | ok | orgId=um8CA8KcKChzWgPS; api_total=388 |
| st_nm_open | ARCGIS | 317 | ok | orgId=sqciGhV7WvGQn4ky; api_total=317 |
| st_wi_open | ARCGIS | 152 | ok | orgId=ISZ89Z51ft1G16OK; api_total=152 |
| st_wv_open | ARCGIS | 2 | ok | orgId=xLpB90lOmCXYDAWo; api_total=2 |
| loc_philadelphia_open | ARCGIS | 0 | error |  |
| loc_stlouis_open | ARCGIS | 0 | error |  |
| st_ms_open | ARCGIS | 0 | empty | orgId=XSDoE9o9b2LpxKKd; api_total=0 |
| intl_au_data_gov | CKAN | 25,000 | ok | api_total=135890; enriched_cols/rows=152; CAPPED at 25000 |
| intl_ca_open_canada | CKAN | 25,000 | ok | api_total=47446; enriched_cols/rows=200; CAPPED at 25000 |
| intl_hdx | CKAN | 25,000 | ok | api_total=27814; enriched_cols/rows=100; CAPPED at 25000 |
| intl_uk_data_gov | CKAN | 25,000 | ok | api_total=57760; enriched_cols/rows=98; CAPPED at 25000 |
| st_va_open | CKAN | 25,000 | ok | api_total=33258; enriched_cols/rows=100; CAPPED at 25000 |
| intl_ie_datagovie | CKAN | 22,328 | ok | api_total=22328; enriched_cols/rows=200 |
| intl_gr_datagov | CKAN | 20,900 | ok | api_total=22482; enriched_cols/rows=0; TIMED_OUT at 300s (partial) |
| intl_nl_overheid | CKAN | 20,739 | ok | api_total=20739; enriched_cols/rows=0 |
| intl_ua_datagov | CKAN | 13,200 | ok | api_total=36871; enriched_cols/rows=0; TIMED_OUT at 300s (partial) |
| st_ca_open | CKAN | 4,480 | ok | api_total=4480; enriched_cols/rows=100 |
| intl_fi_avoindata | CKAN | 2,525 | ok | api_total=2525; enriched_cols/rows=200 |
| intl_il_datagov | CKAN | 1,193 | ok | api_total=1193; enriched_cols/rows=200 |
| st_mn_open | CKAN | 1,058 | ok | api_total=1058; enriched_cols/rows=0 |
| st_ok_open | CKAN | 389 | ok | api_total=389; enriched_cols/rows=100 |
| loc_alleghenycounty_open | CKAN | 369 | ok | api_total=369; enriched_cols/rows=200 |
| loc_pittsburgh_open | CKAN | 369 | ok | api_total=369; enriched_cols/rows=200 |
| intl_ar_datosgob | CKAN | 300 | ok | api_total=1235; enriched_cols/rows=0 |
| loc_boston_open | CKAN | 232 | ok | api_total=232; enriched_cols/rows=100 |
| loc_sanjose_open | CKAN | 170 | ok | api_total=170; enriched_cols/rows=100 |
| loc_sanantonio_open | CKAN | 162 | ok | api_total=162; enriched_cols/rows=100 |
| loc_phoenix_open | CKAN | 149 | ok | api_total=149; enriched_cols/rows=100 |
| loc_houston_open | CKAN | 94 | ok | api_total=94; enriched_cols/rows=70 |
| st_in_open | CKAN | 66 | ok | api_total=66; enriched_cols/rows=63 |
| loc_tampa_open | CKAN | 28 | ok | api_total=28; enriched_cols/rows=28 |
| intl_jo_opendata | CKAN | 0 | error |  |
| intl_co_datosgov | SOCRATA | 8,429 | ok | api_total=8429 |
| st_ut_open | SOCRATA | 6,738 | ok | api_total=6738 |
| st_md_open | SOCRATA | 1,567 | ok | api_total=1567 |
| st_wa_open | SOCRATA | 1,063 | ok | api_total=1063 |
| st_ny_open | SOCRATA | 1,018 | ok | api_total=1018 |
| loc_chicago_open | SOCRATA | 909 | ok | api_total=909 |
| st_tx_open | SOCRATA | 808 | ok | api_total=808 |
| loc_austin_open | SOCRATA | 719 | ok | api_total=719 |
| loc_sf_open | SOCRATA | 658 | ok | api_total=658 |
| st_co_open | SOCRATA | 649 | ok | api_total=649 |
| st_ct_open | SOCRATA | 641 | ok | api_total=641 |
| loc_cookcounty_open | SOCRATA | 521 | ok | api_total=521 |
| st_or_open | SOCRATA | 508 | ok | api_total=508 |
| loc_montgomerycounty_open | SOCRATA | 467 | ok | api_total=467 |
| st_pa_open | SOCRATA | 368 | ok | api_total=368 |
| loc_la_open | SOCRATA | 360 | ok | api_total=360 |
| loc_dallas_open | SOCRATA | 342 | ok | api_total=342 |
| loc_mesa_open | SOCRATA | 320 | ok | api_total=320 |
| loc_sandiegocounty_open | SOCRATA | 317 | ok | api_total=317 |
| loc_oakland_open | SOCRATA | 313 | ok | api_total=313 |
| st_il_open | SOCRATA | 295 | ok | api_total=295 |
| loc_cambridge_open | SOCRATA | 279 | ok | api_total=279 |
| loc_kingcounty_open | SOCRATA | 265 | ok | api_total=265 |
| st_mo_open | SOCRATA | 256 | ok | api_total=256 |
| st_mi_open | SOCRATA | 253 | ok | api_total=253 |
| loc_baton_rouge_open | SOCRATA | 240 | ok | api_total=240 |
| loc_kcmo_open | SOCRATA | 201 | ok | api_total=201 |
| st_de_open | SOCRATA | 171 | ok | api_total=171 |
| loc_seattle_open | SOCRATA | 144 | ok | api_total=144 |
| loc_buffalo_open | SOCRATA | 139 | ok | api_total=139 |
| loc_santaclara_county_open | SOCRATA | 131 | ok | api_total=131 |
| st_nj_open | SOCRATA | 114 | ok | api_total=114 |
| loc_cincinnati_open | SOCRATA | 102 | ok | api_total=102 |
| loc_gainesville_open | SOCRATA | 89 | ok | api_total=89 |
| loc_orlando_open | SOCRATA | 27 | ok | api_total=27 |
