# Portal Recon — Wave 1: Platform Fingerprint

_Generated 2026-06-21 19:42:02 UTC · source: `portal supercluster (8 CATEGORY tags)` · 194 portals · includes Wave-1.5 reclaim pass._

## SUMMARY

| Platform | Portals |
|---|---:|
| SOCRATA | 35 |
| ARCGIS | 40 |
| CKAN | 25 |
| OPENDATASOFT | 5 |
| UNKNOWN | 89 |
| **TOTAL** | **194** |

- **Responded:** 186/194 · **Dead / no response:** 8
- **Headline:** **39% of portals are covered by the top-2 platforms** (ARCGIS 40 + SOCRATA 35 = 75 of 194). Top-3 (ARCGIS 40 + SOCRATA 35 + CKAN 25) = 52%; all detected platforms = 105 (54%). Those are your Wave-2 readers, by priority.
- **Reclaim pass:** retried 102 UNKNOWNs, recovered **13** (coverage 47% → 54%). Of recovered, 8 are homepage-branding only (softer — verify in Wave 2).

### ⚠ Flags (9) — dead / redirecting / auth-required

| source_id | portal | issue |
|---|---|---|
| intl_ae_bayanat | UAE Bayanat Open Data Portal | reclaim: still no homepage response |
| intl_lk_datagov | Sri Lanka Open Data Portal (data.gov.lk) | reclaim: still no homepage response |
| intl_ro_datagov | Romania National Open Data Portal (data.gov.ro) | reclaim: still no homepage response |
| intl_sa_opendata | Saudi Arabia National Open Data Platform (open.data.gov.sa) | reclaim: still no homepage response |
| intl_uk_data_gov | UK National Data Library (data.gov.uk) | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200); redirects to ckan.publishing.service.gov.uk |
| intl_za_datagov | South Africa National Data Portal (data.gov.za) | reclaim: still no homepage response |
| loc_lasvegas_open | Las Vegas Open Data Portal | reclaim: still no homepage response |
| loc_miami_city_open | Miami Open Data Portal | reclaim: still no homepage response |
| st_ak_open | Alaska Open Data Portal | reclaim: still no homepage response |

## FULL RESULTS

| source_id | portal name | base URL | platform detected | API base URL | responded? | method | notes |
|---|---|---|---|---|:--:|---|---|
| fed_datagov_catalog | Data.gov Catalog API | https://open.gsa.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ae_bayanat | UAE Bayanat Open Data Portal | https://bayanat.ae | UNKNOWN |  | ❌ |  | reclaim: still no homepage response |
| intl_ar_datosgob | Argentina National Open Data Portal (datos.gob.ar) | https://datos.gob.ar | CKAN | https://datos.gob.ar/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| intl_at_datagvat | Austria National Open Data Portal (data.gv.at) | https://www.data.gv.at | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_au_data_gov | data.gov.au | https://data.gov.au | CKAN | https://data.gov.au/data/api/3/action | ✅ | subpath | reclaimed at subpath /data (CKAN) |
| intl_bd_datagov | Bangladesh Open Government Data Portal (data.gov.bd) | https://data.gov.bd | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_be_datagovbe | Belgium Federal Open Data Portal (data.gov.be) | https://data.gov.be | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_bg_opendata | Bulgaria National Open Data Portal (opendata.government.bg) | https://opendata.government.bg | UNKNOWN |  | ✅ |  | reclaim: still no homepage response |
| intl_bh_opendata | Bahrain Open Data Portal (data.gov.bh) | https://data.gov.bh | OPENDATASOFT | https://data.gov.bh/api/v2 | ✅ | pass-1 | matched OPENDATASOFT via /api/v2/catalog/datasets?limit=0 (HTTP 200) |
| intl_br_dados_gov | dados.gov.br | https://dados.gov.br | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ca_open_canada | Open Government Portal Canada (open.canada.ca) | https://open.canada.ca | CKAN | https://open.canada.ca/data/api/3/action | ✅ | subpath | reclaimed at subpath /data (CKAN) |
| intl_ch_opendataswiss | Switzerland Open Government Data Portal (opendata.swiss) | https://handbook.opendata.swiss | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_cl_datosgob | Chile National Open Data Portal (datos.gob.cl) | https://datos.gob.cl | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_co_datosgov | Colombia National Open Data Portal (datos.gov.co) | https://www.datos.gov.co | SOCRATA | https://www.datos.gov.co/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| intl_cy_opendata | Cyprus National Open Data Portal | https://dateno.io | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_cz_nkod | Czechia National Open Data Catalog (NKOD) (data.gov.cz) | https://data.gov.cz | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_de_govdata | GovData.de | https://www.govdata.de | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_eg_capmas | Egypt Data Portal (opendataforafrica.org/Egypt) | https://egypt.opendataforafrica.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_es_datosgob | Spain National Open Data Portal (datos.gob.es) | https://datos.gob.es | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_eu_data_europa | European Data Portal (data.europa.eu) | https://data.europa.eu | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_fi_avoindata | Finland National Open Data Catalog (avoindata.fi) | https://www.avoindata.fi | CKAN | https://www.avoindata.fi/data/api/3/action | ✅ | subpath | reclaimed at subpath /data (CKAN) |
| intl_fr_data_gouv | data.gouv.fr | https://www.data.gouv.fr | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ge_datagov | Georgia National Open Data Portal (data.gov.ge) | https://www.opengovpartnership.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_gh_datagovgh | Ghana Open Data Initiative (data.gov.gh) | https://data.gov.gh | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_gr_datagov | Greece National Open Data Portal (data.gov.gr) | https://data.gov.gr | CKAN | https://data.gov.gr/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| intl_hdx | Humanitarian Data Exchange (HDX) CKAN API | https://data.humdata.org | CKAN | https://data.humdata.org/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| intl_hk_datagov | Hong Kong Open Data Portal (data.gov.hk) | https://data.gov.hk | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_hr_datagov | Croatia National Open Data Portal (data.gov.hr) | https://data.gov.hr | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_hu_opendata | Hungary National Open Data Portal (opendata.hu) | https://opendata.hu | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_id_datagoid | Indonesia Satu Data Portal (data.go.id) | https://data.go.id | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ie_datagovie | Ireland National Open Data Portal (data.gov.ie) | https://data.gov.ie | CKAN | https://data.gov.ie/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| intl_il_datagov | Israel National Open Data Portal (data.gov.il) | https://data.gov.il | CKAN | https://data.gov.il/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| intl_in_data_gov | Open Government Data Platform India (data.gov.in) | https://www.data.gov.in | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_is_opendata | Iceland Open Data Portal (island.is/en/o/digital-iceland/open-data) | https://island.is | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_it_datigovit | Italy National Open Data Portal (dati.gov.it) | https://www.dati.gov.it | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_jm_opendata | Jamaica Open Data Portal (data.gov.jm) | https://data.gov.jm | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_jo_opendata | Jordan Open Government Data Portal (opendata.gov.jo) | https://www.opendata.gov.jo | CKAN |  | ✅ | branding | homepage branding => CKAN (NOT API-confirmed) |
| intl_jp_datagojp | Japan National Open Data Portal (data.go.jp) | https://www.data.go.jp | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ke_opendata | Kenya Open Data Initiative (opendata.go.ke) | https://www.opendata.go.ke | ARCGIS |  | ✅ | branding | homepage branding => ARCGIS (NOT API-confirmed) |
| intl_kr_datagokr | South Korea Public Data Portal (data.go.kr) | https://www.data.go.kr | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_lk_datagov | Sri Lanka Open Data Portal (data.gov.lk) | https://data.gov.lk | UNKNOWN |  | ❌ |  | reclaim: still no homepage response |
| intl_lt_datagov | Lithuania National Open Data Portal (data.gov.lt) | https://data.gov.lt | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ma_opendata | Morocco National Open Data Portal (data.gov.ma) | https://dataportals.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_md_datagov | Moldova National Open Data Portal (data.gov.md) | https://data.gov.md | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_mx_datos_gob | datos.gob.mx | https://www.datos.gob.mx | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_my_datagov | Malaysia National Open Data Portal (data.gov.my) | https://data.gov.my | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ng_datagov | Nigeria Open Data Portal (data.gov.ng) | http://www.data.gov.ng | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_nl_overheid | Netherlands National Data Register (data.overheid.nl) | https://data.overheid.nl | CKAN | https://data.overheid.nl/data/api/3/action | ✅ | subpath | reclaimed at subpath /data (CKAN) |
| intl_no_norgeno | Norway National Data Portal (data.norge.no) | https://data.norge.no | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_np_opendata | Open Data Nepal Portal (opendatanepal.com) | https://opendatanepal.com | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_nz_datagovtnz | New Zealand Government Open Data Catalog (data.govt.nz) | https://data.govt.nz | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_om_opendata | Oman National Open Data Portal (oman.om open data) | https://oman.om | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_owid | Our World in Data Catalog API | https://docs.owid.io | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_pe_datosabiertos | Peru National Open Data Platform (datosabiertos.gob.pe) | https://www.datosabiertos.gob.pe | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ph_datagovph | Philippines Open Data Portal (data.gov.ph) | https://data.gov.ph | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_pl_danegov | Poland National Open Data Portal (dane.gov.pl) | https://api.dane.gov.pl | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_pt_dadosgov | Portugal Open Data Portal (dados.gov.pt) | https://dados.gov.pt | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_qa_datagov | Qatar National Open Data Portal (data.gov.qa) | https://www.data.gov.qa | OPENDATASOFT | https://www.data.gov.qa/api/v2 | ✅ | pass-1 | matched OPENDATASOFT via /api/v2/catalog/datasets?limit=0 (HTTP 200) |
| intl_ro_datagov | Romania National Open Data Portal (data.gov.ro) | https://data.gov.ro | UNKNOWN |  | ❌ |  | reclaim: still no homepage response |
| intl_rs_opendata | Serbia National Open Data Portal (data.gov.rs) | https://www.ite.gov.rs | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_sa_opendata | Saudi Arabia National Open Data Platform (open.data.gov.sa) | https://od.data.gov.sa | UNKNOWN |  | ❌ |  | reclaim: still no homepage response |
| intl_se_dataportal | Sweden National Data Portal (dataportal.se) | https://www.dataportal.se | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_sg_data_gov | data.gov.sg | https://data.gov.sg | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_si_datagov | Slovenia Open Data Portal (podatki.gov.si) | https://nio.gov.si | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_sk_datagov | Slovakia National Open Data Portal (data.gov.sk) | https://data.gov.sk | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_sn_opendata | Senegal Data Portal (opendataforafrica.org/Senegal) | https://senegal.opendataforafrica.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_th_datagoth | Thailand Open Government Data Portal (data.go.th) | https://api.data.go.th | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_tw_datagov | Taiwan Government Open Data Platform (data.gov.tw) | https://data.gov.tw | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_ua_datagov | Ukraine National Open Data Portal (data.gov.ua) | https://data.gov.ua | CKAN | https://data.gov.ua/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| intl_uk_data_gov | UK National Data Library (data.gov.uk) | https://www.data.gov.uk | CKAN | https://www.data.gov.uk/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200); redirects to ckan.publishing.service.gov.uk |
| intl_uy_datos | Uruguay Open Data Platform (datos.gub.uy) | https://datos.gub.uy | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| intl_za_datagov | South Africa National Data Portal (data.gov.za) | http://data.gov.za | UNKNOWN |  | ❌ |  | reclaim: still no homepage response |
| loc_albuquerque_open | ABQ Data Open Data Portal | https://opendata.cabq.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| loc_alleghenycounty_open | WPRDC Allegheny County Data | https://data.wprdc.org | CKAN | https://data.wprdc.org/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| loc_asheville_open | Asheville Open Data Portal | https://data-avl.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_atlanta_open | Atlanta DataAtlanta / City Planning GIS Open Data Hub | https://dpcd-coaplangis.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_austin_open | Austin Open Data | https://data.austintexas.gov | SOCRATA | https://data.austintexas.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_baltimore_open | Open Baltimore | https://data.baltimorecity.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_baton_rouge_open | Open Data BR | https://data.brla.gov | SOCRATA | https://data.brla.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_boston_open | Analyze Boston | https://data.boston.gov | CKAN | https://data.boston.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| loc_buffalo_open | OpenData Buffalo | https://data.buffalony.gov | SOCRATA | https://data.buffalony.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_cambridge_open | Cambridge Open Data Portal | https://data.cambridgema.gov | SOCRATA | https://data.cambridgema.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_charlotte_open | Charlotte Open Data Portal | https://data.charlottenc.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_chicago_open | Chicago Data Portal | https://data.cityofchicago.org | SOCRATA | https://data.cityofchicago.org/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_cincinnati_open | Open Data Cincinnati | https://data.cincinnati-oh.gov | SOCRATA | https://data.cincinnati-oh.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_cleveland_open | Cleveland Open Data Portal | https://data.clevelandohio.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_columbus_open | Columbus GIS Open Data | https://opendata.columbus.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_cookcounty_open | Cook County Open Data Portal | https://datacatalog.cookcountyil.gov | SOCRATA | https://datacatalog.cookcountyil.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_dallas_open | Dallas OpenData | https://www.dallasopendata.com | SOCRATA | https://www.dallasopendata.com/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_dc_open | Open Data DC | https://opendata.dc.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_denver_open | Denver Open Data Catalog | https://denvergov.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| loc_detroit_open | Detroit Open Data Portal | https://data.detroitmi.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_fairfaxcounty_open | Fairfax County GIS Open Data Site | https://data-fairfaxcountygis.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_fortworth_open | Fort Worth Open Data | https://data.fortworthtexas.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_gainesville_open | DataGNV Gainesville Open Data Portal | https://data.cityofgainesville.org | SOCRATA | https://data.cityofgainesville.org/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_harriscounty_open | Harris County Open Data / Dashboards & Datasets Hub | https://geo-harriscounty.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_hartford_open | Open Data Hartford | https://data.hartford.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_houston_open | Houston Open Data | https://data.houstontx.gov | CKAN | https://data.houstontx.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| loc_indianapolis_open | Open Indy Data Portal | https://data.indy.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_kcmo_open | Open Data KC | https://data.kcmo.org | SOCRATA | https://data.kcmo.org/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_kingcounty_open | King County Open Data | https://data.kingcounty.gov | SOCRATA | https://data.kingcounty.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_la_open | DataLA — Los Angeles Open Data | https://data.lacity.org | SOCRATA | https://data.lacity.org/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_lacounty_open | LA County Open Data Portal | https://data.lacounty.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_lasvegas_open | Las Vegas Open Data Portal | https://opendata.lasvegasnevada.gov | UNKNOWN |  | ❌ |  | reclaim: still no homepage response |
| loc_longbeach_open | Long Beach Open Data Portal | https://data.longbeach.gov | OPENDATASOFT | https://data.longbeach.gov/api/v2 | ✅ | pass-1 | matched OPENDATASOFT via /api/v2/catalog/datasets?limit=0 (HTTP 200) |
| loc_louisville_open | Louisville Open Data Portal | https://data.louisvilleky.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_maricopacounty_open | Maricopa County GIS Open Data | https://data-maricopa.opendata.arcgis.com | ARCGIS |  | ✅ | branding | homepage branding => ARCGIS (NOT API-confirmed) |
| loc_mecklenburgcounty_open | Mecklenburg County GIS Open Data Portal | https://data.mecknc.gov | ARCGIS |  | ✅ | branding | homepage branding => ARCGIS (NOT API-confirmed) |
| loc_memphis_open | Memphis Open Data Hub | https://data.memphistn.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_mesa_open | Mesa City Data Hub | https://data.mesaaz.gov | SOCRATA | https://data.mesaaz.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_miami_city_open | Miami Open Data Portal | https://data.miamigov.com | UNKNOWN |  | ❌ |  | reclaim: still no homepage response |
| loc_miamidade_open | Miami-Dade County Open Data Hub | https://opendata.miamidade.gov | ARCGIS |  | ✅ | branding | homepage branding => ARCGIS (NOT API-confirmed) |
| loc_minneapolis_open | Open Data Minneapolis | https://opendata.minneapolismn.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_montgomerycounty_open | dataMontgomery Open Data Portal | https://data.montgomerycountymd.gov | SOCRATA | https://data.montgomerycountymd.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_nashville_open | Nashville Open Data | https://data.nashville.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_nyc_open | NYC Open Data | https://opendata.cityofnewyork.us | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| loc_nyc_palmbeach | Palm Beach County Open Data | https://opendata2-pbcgov.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_oakland_open | Oakland Open Data Portal | https://data.oaklandca.gov | SOCRATA | https://data.oaklandca.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_orangecounty_ca_open | Orange County Open GIS Data Portal | https://data-ocpw.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_orlando_open | Orlando Open Data Portal | https://data.cityoforlando.net | SOCRATA | https://data.cityoforlando.net/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_philadelphia_open | OpenDataPhilly | https://opendataphilly.org | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_phoenix_open | Phoenix Open Data Portal | https://data.phoenix.gov | CKAN | https://phoenixstaging.ogopendata.com/api/3/action | ✅ | redirect-reprobe | reclaimed at redirect target https://phoenixstaging.ogopendata.com (CKAN) |
| loc_pittsburgh_open | Western Pennsylvania Regional Data Center (WPRDC) - Pittsburgh Data | https://data.wprdc.org | CKAN | https://data.wprdc.org/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| loc_portland_open | Portland Open Data | https://www.portland.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| loc_raleigh_open | Open Data Raleigh | https://data.raleighnc.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_sacramento_open | Sacramento Open Data Portal | https://data.cityofsacramento.org | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_sanantonio_open | Open Data SA | https://data.sanantonio.gov | CKAN | https://data.sanantonio.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| loc_sandiego_city_open | San Diego Open Data Portal | https://data.sandiego.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| loc_sandiegocounty_open | San Diego County Open Data Portal | https://data.sandiegocounty.gov | SOCRATA | https://data.sandiegocounty.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_sanjose_open | San Jose Open Data Portal | https://data.sanjoseca.gov | CKAN | https://data.sanjoseca.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| loc_santaclara_county_open | Santa Clara County Open Data Portal | https://data.sccgov.org | SOCRATA | https://data.sccgov.org/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_seattle_open | Seattle Open Data | https://data.seattle.gov | SOCRATA | https://data.seattle.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_sf_open | SF OpenData (DataSF) | https://data.sfgov.org | SOCRATA | https://data.sfgov.org/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| loc_stlouis_open | St. Louis City Open Data | https://www.stlouis-mo.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_tampa_open | Tampa Open Data Portal | https://opendata.tampa.gov | CKAN | https://opendata.tampa.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| loc_tempe_open | Tempe Open Data Catalog | https://data.tempe.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_tucson_open | Tucson Open Data | https://gisdata.tucsonaz.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| loc_wakecounty_open | Wake County Open Data | https://data.wake.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| st_ak_open | Alaska Open Data Portal | https://data.alaska.gov | UNKNOWN |  | ❌ |  | reclaim: still no homepage response |
| st_ar_open | Arkansas Open Data (GIS/fragmented) | https://gis.arkansas.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_ca_open | California Open Data Portal | https://data.ca.gov | CKAN | https://data.ca.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| st_co_open | Colorado Information Marketplace | https://data.colorado.gov | SOCRATA | https://data.colorado.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_ct_open | Connecticut Open Data Portal | https://data.ct.gov | SOCRATA | https://data.ct.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_de_open | Delaware Open Data Portal | https://data.delaware.gov | SOCRATA | https://data.delaware.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_fl_open | Florida Open Data (no unified portal — agency-fragmented) | https://geodata.floridagio.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| st_ga_open | Georgia Open Data (GDAC) | https://gdac.georgia.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_hi_open | Hawaii Open Data Portal | https://data.hawaii.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_ia_open | Iowa Data Hub | https://data.iowa.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_id_open | Idaho Open Data (GIS-focused) | https://gis.idaho.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_il_open | Illinois Open Data Portal | https://data.illinois.gov | SOCRATA | https://data.illinois.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_in_open | Indiana Data Hub | https://hub.mph.in.gov | CKAN | https://hub.mph.in.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| st_ks_open | Kansas Open Gov | https://kansasopengov.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_ky_open | Kentucky Open GIS Data | https://opengisdata.ky.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| st_ma_open | Massachusetts Data Hub | https://data.mass.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_md_open | Maryland Open Data Portal | https://opendata.maryland.gov | SOCRATA | https://opendata.maryland.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_me_open | Maine Open Data | https://www.maine.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_mi_open | Michigan Open Data Portal | https://data.michigan.gov | SOCRATA | https://data.michigan.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_mn_open | Minnesota Geospatial Commons / TransparencyMN | https://gisdata.mn.gov | CKAN | https://gisdata.mn.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| st_mo_open | Missouri Open Data Portal | https://data.mo.gov | SOCRATA | https://data.mo.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_ms_open | Mississippi GIS Open Data | https://opendata.gis.ms.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| st_mt_open | Montana Data Portal | https://data.mt.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_nc_open | NC LINC / NC OSBM Open Data | https://linc.osbm.nc.gov | OPENDATASOFT | https://linc.osbm.nc.gov/api/v2 | ✅ | pass-1 | matched OPENDATASOFT via /api/v2/catalog/datasets?limit=0 (HTTP 200) |
| st_nd_open | North Dakota Open Data (fragmented) | https://www.nd.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_ne_open | Nebraska Open Data / StateSpending | https://www.nebraska.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_nh_open | New Hampshire Geodata Portal | https://new-hampshire-geodata-portal-1-nhgranit.hub.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| st_nj_open | NJ Open Data Center | https://data.nj.gov | SOCRATA | https://data.nj.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_nm_open | New Mexico Open Data (fragmented — agency-level) | https://data-nmenv.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| st_nv_open | Nevada Open Data Portal | https://open.nv.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_ny_open | New York State Open Data | https://data.ny.gov | SOCRATA | https://data.ny.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_oh_open | DataOhio | https://data.ohio.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_ok_open | Oklahoma Open Data Portal | https://data.ok.gov | CKAN | https://data.ok.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| st_or_open | Oregon Open Data Portal | https://data.oregon.gov | SOCRATA | https://data.oregon.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_pa_open | PA Open Data Portal | https://data.pa.gov | SOCRATA | https://data.pa.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_ri_open | Rhode Island Open Data Portal | https://www.ri.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_sc_open | South Carolina Data and Transparency | https://sc.gov | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| st_tn_open | TN DATA / Tennessee Geospatial Portal | https://geodata.tn.gov | ARCGIS |  | ✅ | branding | homepage branding => ARCGIS (NOT API-confirmed) |
| st_tx_open | Texas Open Data Portal | https://data.texas.gov | SOCRATA | https://data.texas.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_ut_open | Utah Open Data Portal | https://opendata.utah.gov | SOCRATA | https://opendata.utah.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_va_open | Virginia Open Data Portal | https://data.virginia.gov | CKAN | https://data.virginia.gov/api/3/action | ✅ | pass-1 | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| st_vt_open | Vermont Open Geodata / Open Data | https://geodata.vermont.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| st_wa_open | Washington State Open Data Portal | https://data.wa.gov | SOCRATA | https://data.wa.gov/api/catalog/v1 | ✅ | pass-1 | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| st_wi_open | Wisconsin Open Data (fragmented — no unified portal) | https://data.dhsgis.wi.gov | ARCGIS | hub.arcgis.com/api/search/v1 | ✅ | pass-1 | ✅ |
| st_wv_open | West Virginia Open Data (fragmented — GIS-focused) | https://data-wvdot.opendata.arcgis.com | ARCGIS |  | ✅ | branding | homepage branding => ARCGIS (NOT API-confirmed) |
| st_wy_open | Wyoming GeoHub | https://wyogeo.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_aws_opendata | Registry of Open Data on AWS | https://registry.opendata.aws | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_azure_open_datasets | Azure Open Datasets | https://learn.microsoft.com | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_data_world | data.world | https://developer.data.world | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_dataportals_org | DataPortals.org | https://dataportals.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_gcp_public_datasets | Google Cloud Public Datasets | https://cloud.google.com | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_google_dataset_search | Google Dataset Search | https://datasetsearch.research.google.com | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_huggingface_datasets | Hugging Face Datasets Hub | https://huggingface.co | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_kaggle_datasets | Kaggle Datasets | https://www.kaggle.com | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
| xc_open_data_inception | Open Data Inception | https://opendatainception.io | OPENDATASOFT |  | ✅ | branding | homepage branding => OPENDATASOFT (NOT API-confirmed) |
| xc_re3data | re3data.org (Registry of Research Data Repositories) | https://www.re3data.org | UNKNOWN |  | ✅ |  | reclaim: no subpath/redirect/branding match |
