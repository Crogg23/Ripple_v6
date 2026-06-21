# Portal Recon — Wave 1: Platform Fingerprint

_Generated 2026-06-21 19:23:56 UTC · source category: `portal supercluster (8 CATEGORY tags)` · 194 portals._

## SUMMARY

| Platform | Portals |
|---|---:|
| SOCRATA | 35 |
| CKAN | 19 |
| ARCGIS | 34 |
| OPENDATASOFT | 4 |
| UNKNOWN | 102 |
| **TOTAL** | **194** |

- **Responded:** 185/194 · **Dead / no response:** 9
- **Headline:** **28% of portals are covered by the top 2 platforms** (Socrata 35 + CKAN 19 = 54). Add ArcGIS and it's 45% — that's the Wave-2 reader count.

### ⚠ Flags (15) — dead / redirecting / auth-required

| source_id | portal | issue |
|---|---|---|
| intl_ae_bayanat | UAE Bayanat Open Data Portal | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| intl_fi_avoindata | Finland National Open Data Catalog (avoindata.fi) | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404; redirects to avoindata.suomi.fi:443 |
| intl_jm_opendata | Jamaica Open Data Portal (data.gov.jm) | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| intl_jp_datagojp | Japan National Open Data Portal (data.go.jp) | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404; redirects to data.e-gov.go.jp |
| intl_lk_datagov | Sri Lanka Open Data Portal (data.gov.lk) | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| intl_no_norgeno | Norway National Data Portal (data.norge.no) | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:200; redirects to data.norge.no:443 |
| intl_ro_datagov | Romania National Open Data Portal (data.gov.ro) | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| intl_sa_opendata | Saudi Arabia National Open Data Platform (open.data.gov.sa) | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| intl_sk_datagov | Slovakia National Open Data Portal (data.gov.sk) | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200; redirects to data.slovensko.sk |
| intl_uk_data_gov | UK National Data Library (data.gov.uk) | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200); redirects to ckan.publishing.service.gov.uk |
| intl_za_datagov | South Africa National Data Portal (data.gov.za) | probes=SOCRATA:err(ConnectionError),CKAN:err(ConnectionError),OPENDATASOFT:err(ConnectionError),GEONODE:err(ConnectionError),JUNAR:err(ConnectionError),ARCGIS:err(ConnectionError); no HTTP response (timeout/conn error) |
| loc_lasvegas_open | Las Vegas Open Data Portal | probes=SOCRATA:err(ConnectionError),CKAN:err(ConnectionError),OPENDATASOFT:err(ConnectionError),GEONODE:err(ConnectionError),JUNAR:err(ConnectionError),ARCGIS:err(ConnectionError); no HTTP response (timeout/conn error) |
| loc_miami_city_open | Miami Open Data Portal | probes=SOCRATA:err(ConnectionError),CKAN:err(ConnectionError),OPENDATASOFT:err(ConnectionError),GEONODE:err(ConnectionError),JUNAR:err(ConnectionError),ARCGIS:err(ConnectionError); no HTTP response (timeout/conn error) |
| loc_phoenix_open | Phoenix Open Data Portal | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200; redirects to phoenixstaging.ogopendata.com |
| st_ak_open | Alaska Open Data Portal | probes=SOCRATA:err(ConnectionError),CKAN:err(ConnectionError),OPENDATASOFT:err(ConnectionError),GEONODE:err(ConnectionError),JUNAR:err(ConnectionError),ARCGIS:err(ConnectionError); no HTTP response (timeout/conn error) |

## FULL RESULTS

| portal name | base URL | platform detected | API base URL | responded? | notes |
|---|---|---|---|:--:|---|
| Data.gov Catalog API | https://open.gsa.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:200 |
| UAE Bayanat Open Data Portal | https://bayanat.ae | UNKNOWN |  | ❌ | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| Argentina National Open Data Portal (datos.gob.ar) | https://datos.gob.ar | CKAN | https://datos.gob.ar/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Austria National Open Data Portal (data.gv.at) | https://www.data.gv.at | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| data.gov.au | https://data.gov.au | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Bangladesh Open Government Data Portal (data.gov.bd) | https://data.gov.bd | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:err(ReadTimeout) |
| Belgium Federal Open Data Portal (data.gov.be) | https://data.gov.be | UNKNOWN |  | ✅ | probes=SOCRATA:503,CKAN:503,OPENDATASOFT:503,GEONODE:503,JUNAR:503,ARCGIS:503 |
| Bulgaria National Open Data Portal (opendata.government.bg) | https://opendata.government.bg | UNKNOWN |  | ✅ | probes=SOCRATA:403,CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout) |
| Bahrain Open Data Portal (data.gov.bh) | https://data.gov.bh | OPENDATASOFT | https://data.gov.bh/api/v2 | ✅ | matched OPENDATASOFT via /api/v2/catalog/datasets?limit=0 (HTTP 200) |
| dados.gov.br | https://dados.gov.br | UNKNOWN |  | ✅ | probes=SOCRATA:401,CKAN:401,OPENDATASOFT:401,GEONODE:401,JUNAR:401,ARCGIS:401 |
| Open Government Portal Canada (open.canada.ca) | https://open.canada.ca | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Switzerland Open Government Data Portal (opendata.swiss) | https://handbook.opendata.swiss | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Chile National Open Data Portal (datos.gob.cl) | https://datos.gob.cl | UNKNOWN |  | ✅ | probes=SOCRATA:503,CKAN:503,OPENDATASOFT:503,GEONODE:503,JUNAR:503,ARCGIS:503 |
| Colombia National Open Data Portal (datos.gov.co) | https://www.datos.gov.co | SOCRATA | https://www.datos.gov.co/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Cyprus National Open Data Portal | https://dateno.io | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200 |
| Czechia National Open Data Catalog (NKOD) (data.gov.cz) | https://data.gov.cz | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| GovData.de | https://www.govdata.de | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Egypt Data Portal (opendataforafrica.org/Egypt) | https://egypt.opendataforafrica.org | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Spain National Open Data Portal (datos.gob.es) | https://datos.gob.es | UNKNOWN |  | ✅ | probes=SOCRATA:403,CKAN:403,OPENDATASOFT:403,GEONODE:403,JUNAR:403,ARCGIS:404 |
| European Data Portal (data.europa.eu) | https://data.europa.eu | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Finland National Open Data Catalog (avoindata.fi) | https://www.avoindata.fi | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404; redirects to avoindata.suomi.fi:443 |
| data.gouv.fr | https://www.data.gouv.fr | UNKNOWN |  | ✅ | probes=SOCRATA:503,CKAN:503,OPENDATASOFT:503,GEONODE:503,JUNAR:503,ARCGIS:503 |
| Georgia National Open Data Portal (data.gov.ge) | https://www.opengovpartnership.org | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Ghana Open Data Initiative (data.gov.gh) | https://data.gov.gh | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200 |
| Greece National Open Data Portal (data.gov.gr) | https://data.gov.gr | CKAN | https://data.gov.gr/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Humanitarian Data Exchange (HDX) CKAN API | https://data.humdata.org | CKAN | https://data.humdata.org/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Hong Kong Open Data Portal (data.gov.hk) | https://data.gov.hk | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Croatia National Open Data Portal (data.gov.hr) | https://data.gov.hr | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200 |
| Hungary National Open Data Portal (opendata.hu) | https://opendata.hu | UNKNOWN |  | ✅ | probes=SOCRATA:503,CKAN:503,OPENDATASOFT:503,GEONODE:503,JUNAR:503,ARCGIS:503 |
| Indonesia Satu Data Portal (data.go.id) | https://data.go.id | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Ireland National Open Data Portal (data.gov.ie) | https://data.gov.ie | CKAN | https://data.gov.ie/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Israel National Open Data Portal (data.gov.il) | https://data.gov.il | CKAN | https://data.gov.il/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Open Government Data Platform India (data.gov.in) | https://www.data.gov.in | UNKNOWN |  | ✅ | probes=SOCRATA:403,CKAN:403,OPENDATASOFT:403,GEONODE:403,JUNAR:403,ARCGIS:403 |
| Iceland Open Data Portal (island.is/en/o/digital-iceland/open-data) | https://island.is | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Italy National Open Data Portal (dati.gov.it) | https://www.dati.gov.it | UNKNOWN |  | ✅ | probes=SOCRATA:403,CKAN:403,OPENDATASOFT:403,GEONODE:403,JUNAR:403,ARCGIS:403 |
| Jamaica Open Data Portal (data.gov.jm) | https://data.gov.jm | UNKNOWN |  | ❌ | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| Jordan Open Government Data Portal (opendata.gov.jo) | https://www.opendata.gov.jo | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:400,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Japan National Open Data Portal (data.go.jp) | https://www.data.go.jp | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404; redirects to data.e-gov.go.jp |
| Kenya Open Data Initiative (opendata.go.ke) | https://www.opendata.go.ke | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| South Korea Public Data Portal (data.go.kr) | https://www.data.go.kr | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Sri Lanka Open Data Portal (data.gov.lk) | https://data.gov.lk | UNKNOWN |  | ❌ | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| Lithuania National Open Data Portal (data.gov.lt) | https://data.gov.lt | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Morocco National Open Data Portal (data.gov.ma) | https://dataportals.org | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Moldova National Open Data Portal (data.gov.md) | https://data.gov.md | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| datos.gob.mx | https://www.datos.gob.mx | UNKNOWN |  | ✅ | probes=SOCRATA:503,CKAN:503,OPENDATASOFT:503,GEONODE:503,JUNAR:503,ARCGIS:503 |
| Malaysia National Open Data Portal (data.gov.my) | https://data.gov.my | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Nigeria Open Data Portal (data.gov.ng) | http://www.data.gov.ng | UNKNOWN |  | ✅ | probes=SOCRATA:503,CKAN:503,OPENDATASOFT:503,GEONODE:503,JUNAR:503,ARCGIS:503 |
| Netherlands National Data Register (data.overheid.nl) | https://data.overheid.nl | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Norway National Data Portal (data.norge.no) | https://data.norge.no | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:200; redirects to data.norge.no:443 |
| Open Data Nepal Portal (opendatanepal.com) | https://opendatanepal.com | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| New Zealand Government Open Data Catalog (data.govt.nz) | https://data.govt.nz | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:404 |
| Oman National Open Data Portal (oman.om open data) | https://oman.om | UNKNOWN |  | ✅ | probes=SOCRATA:503,CKAN:503,OPENDATASOFT:503,GEONODE:503,JUNAR:503,ARCGIS:503 |
| Our World in Data Catalog API | https://docs.owid.io | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Peru National Open Data Platform (datosabiertos.gob.pe) | https://www.datosabiertos.gob.pe | UNKNOWN |  | ✅ | probes=SOCRATA:403,CKAN:403,OPENDATASOFT:403,GEONODE:403,JUNAR:403,ARCGIS:403 |
| Philippines Open Data Portal (data.gov.ph) | https://data.gov.ph | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:403,GEONODE:200,JUNAR:200,ARCGIS:200 |
| Poland National Open Data Portal (dane.gov.pl) | https://api.dane.gov.pl | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Portugal Open Data Portal (dados.gov.pt) | https://dados.gov.pt | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Qatar National Open Data Portal (data.gov.qa) | https://www.data.gov.qa | OPENDATASOFT | https://www.data.gov.qa/api/v2 | ✅ | matched OPENDATASOFT via /api/v2/catalog/datasets?limit=0 (HTTP 200) |
| Romania National Open Data Portal (data.gov.ro) | https://data.gov.ro | UNKNOWN |  | ❌ | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| Serbia National Open Data Portal (data.gov.rs) | https://www.ite.gov.rs | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Saudi Arabia National Open Data Platform (open.data.gov.sa) | https://od.data.gov.sa | UNKNOWN |  | ❌ | probes=SOCRATA:err(ReadTimeout),CKAN:err(ReadTimeout),OPENDATASOFT:err(ReadTimeout),GEONODE:err(ReadTimeout),JUNAR:err(ReadTimeout),ARCGIS:err(ReadTimeout); no HTTP response (timeout/conn error) |
| Sweden National Data Portal (dataportal.se) | https://www.dataportal.se | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| data.gov.sg | https://data.gov.sg | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Slovenia Open Data Portal (podatki.gov.si) | https://nio.gov.si | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:200 |
| Slovakia National Open Data Portal (data.gov.sk) | https://data.gov.sk | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200; redirects to data.slovensko.sk |
| Senegal Data Portal (opendataforafrica.org/Senegal) | https://senegal.opendataforafrica.org | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Thailand Open Government Data Portal (data.go.th) | https://api.data.go.th | UNKNOWN |  | ✅ | probes=SOCRATA:403,CKAN:403,OPENDATASOFT:403,GEONODE:403,JUNAR:403,ARCGIS:403 |
| Taiwan Government Open Data Platform (data.gov.tw) | https://data.gov.tw | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Ukraine National Open Data Portal (data.gov.ua) | https://data.gov.ua | CKAN | https://data.gov.ua/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| UK National Data Library (data.gov.uk) | https://www.data.gov.uk | CKAN | https://www.data.gov.uk/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200); redirects to ckan.publishing.service.gov.uk |
| Uruguay Open Data Platform (datos.gub.uy) | https://datos.gub.uy | UNKNOWN |  | ✅ | probes=SOCRATA:503,CKAN:503,OPENDATASOFT:503,GEONODE:503,JUNAR:503,ARCGIS:503 |
| South Africa National Data Portal (data.gov.za) | http://data.gov.za | UNKNOWN |  | ❌ | probes=SOCRATA:err(ConnectionError),CKAN:err(ConnectionError),OPENDATASOFT:err(ConnectionError),GEONODE:err(ConnectionError),JUNAR:err(ConnectionError),ARCGIS:err(ConnectionError); no HTTP response (timeout/conn error) |
| ABQ Data Open Data Portal | https://opendata.cabq.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| WPRDC Allegheny County Data | https://data.wprdc.org | CKAN | https://data.wprdc.org/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Asheville Open Data Portal | https://data-avl.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Atlanta DataAtlanta / City Planning GIS Open Data Hub | https://dpcd-coaplangis.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Austin Open Data | https://data.austintexas.gov | SOCRATA | https://data.austintexas.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Open Baltimore | https://data.baltimorecity.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Open Data BR | https://data.brla.gov | SOCRATA | https://data.brla.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Analyze Boston | https://data.boston.gov | CKAN | https://data.boston.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| OpenData Buffalo | https://data.buffalony.gov | SOCRATA | https://data.buffalony.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Cambridge Open Data Portal | https://data.cambridgema.gov | SOCRATA | https://data.cambridgema.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Charlotte Open Data Portal | https://data.charlottenc.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Chicago Data Portal | https://data.cityofchicago.org | SOCRATA | https://data.cityofchicago.org/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Open Data Cincinnati | https://data.cincinnati-oh.gov | SOCRATA | https://data.cincinnati-oh.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Cleveland Open Data Portal | https://data.clevelandohio.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Columbus GIS Open Data | https://opendata.columbus.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Cook County Open Data Portal | https://datacatalog.cookcountyil.gov | SOCRATA | https://datacatalog.cookcountyil.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Dallas OpenData | https://www.dallasopendata.com | SOCRATA | https://www.dallasopendata.com/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Open Data DC | https://opendata.dc.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Denver Open Data Catalog | https://denvergov.org | UNKNOWN |  | ✅ | probes=SOCRATA:err(ReadTimeout),CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Detroit Open Data Portal | https://data.detroitmi.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Fairfax County GIS Open Data Site | https://data-fairfaxcountygis.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Fort Worth Open Data | https://data.fortworthtexas.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| DataGNV Gainesville Open Data Portal | https://data.cityofgainesville.org | SOCRATA | https://data.cityofgainesville.org/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Harris County Open Data / Dashboards & Datasets Hub | https://geo-harriscounty.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Open Data Hartford | https://data.hartford.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Houston Open Data | https://data.houstontx.gov | CKAN | https://data.houstontx.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Open Indy Data Portal | https://data.indy.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Open Data KC | https://data.kcmo.org | SOCRATA | https://data.kcmo.org/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| King County Open Data | https://data.kingcounty.gov | SOCRATA | https://data.kingcounty.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| DataLA — Los Angeles Open Data | https://data.lacity.org | SOCRATA | https://data.lacity.org/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| LA County Open Data Portal | https://data.lacounty.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Las Vegas Open Data Portal | https://opendata.lasvegasnevada.gov | UNKNOWN |  | ❌ | probes=SOCRATA:err(ConnectionError),CKAN:err(ConnectionError),OPENDATASOFT:err(ConnectionError),GEONODE:err(ConnectionError),JUNAR:err(ConnectionError),ARCGIS:err(ConnectionError); no HTTP response (timeout/conn error) |
| Long Beach Open Data Portal | https://data.longbeach.gov | OPENDATASOFT | https://data.longbeach.gov/api/v2 | ✅ | matched OPENDATASOFT via /api/v2/catalog/datasets?limit=0 (HTTP 200) |
| Louisville Open Data Portal | https://data.louisvilleky.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Maricopa County GIS Open Data | https://data-maricopa.opendata.arcgis.com | UNKNOWN |  | ✅ | probes=ARCGIS:err(ReadTimeout),SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404; host hint ARCGIS unconfirmed by endpoint |
| Mecklenburg County GIS Open Data Portal | https://data.mecknc.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Memphis Open Data Hub | https://data.memphistn.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Mesa City Data Hub | https://data.mesaaz.gov | SOCRATA | https://data.mesaaz.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Miami Open Data Portal | https://data.miamigov.com | UNKNOWN |  | ❌ | probes=SOCRATA:err(ConnectionError),CKAN:err(ConnectionError),OPENDATASOFT:err(ConnectionError),GEONODE:err(ConnectionError),JUNAR:err(ConnectionError),ARCGIS:err(ConnectionError); no HTTP response (timeout/conn error) |
| Miami-Dade County Open Data Hub | https://opendata.miamidade.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:500 |
| Open Data Minneapolis | https://opendata.minneapolismn.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| dataMontgomery Open Data Portal | https://data.montgomerycountymd.gov | SOCRATA | https://data.montgomerycountymd.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Nashville Open Data | https://data.nashville.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| NYC Open Data | https://opendata.cityofnewyork.us | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Palm Beach County Open Data | https://opendata2-pbcgov.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Oakland Open Data Portal | https://data.oaklandca.gov | SOCRATA | https://data.oaklandca.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Orange County Open GIS Data Portal | https://data-ocpw.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Orlando Open Data Portal | https://data.cityoforlando.net | SOCRATA | https://data.cityoforlando.net/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| OpenDataPhilly | https://opendataphilly.org | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Phoenix Open Data Portal | https://data.phoenix.gov | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200; redirects to phoenixstaging.ogopendata.com |
| Western Pennsylvania Regional Data Center (WPRDC) - Pittsburgh Data | https://data.wprdc.org | CKAN | https://data.wprdc.org/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Portland Open Data | https://www.portland.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Open Data Raleigh | https://data.raleighnc.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Sacramento Open Data Portal | https://data.cityofsacramento.org | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Open Data SA | https://data.sanantonio.gov | CKAN | https://data.sanantonio.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| San Diego Open Data Portal | https://data.sandiego.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| San Diego County Open Data Portal | https://data.sandiegocounty.gov | SOCRATA | https://data.sandiegocounty.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| San Jose Open Data Portal | https://data.sanjoseca.gov | CKAN | https://data.sanjoseca.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Santa Clara County Open Data Portal | https://data.sccgov.org | SOCRATA | https://data.sccgov.org/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Seattle Open Data | https://data.seattle.gov | SOCRATA | https://data.seattle.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| SF OpenData (DataSF) | https://data.sfgov.org | SOCRATA | https://data.sfgov.org/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| St. Louis City Open Data | https://www.stlouis-mo.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Tampa Open Data Portal | https://opendata.tampa.gov | CKAN | https://opendata.tampa.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Tempe Open Data Catalog | https://data.tempe.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Tucson Open Data | https://gisdata.tucsonaz.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Wake County Open Data | https://data.wake.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Alaska Open Data Portal | https://data.alaska.gov | UNKNOWN |  | ❌ | probes=SOCRATA:err(ConnectionError),CKAN:err(ConnectionError),OPENDATASOFT:err(ConnectionError),GEONODE:err(ConnectionError),JUNAR:err(ConnectionError),ARCGIS:err(ConnectionError); no HTTP response (timeout/conn error) |
| Arkansas Open Data (GIS/fragmented) | https://gis.arkansas.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| California Open Data Portal | https://data.ca.gov | CKAN | https://data.ca.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Colorado Information Marketplace | https://data.colorado.gov | SOCRATA | https://data.colorado.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Connecticut Open Data Portal | https://data.ct.gov | SOCRATA | https://data.ct.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Delaware Open Data Portal | https://data.delaware.gov | SOCRATA | https://data.delaware.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Florida Open Data (no unified portal — agency-fragmented) | https://geodata.floridagio.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Georgia Open Data (GDAC) | https://gdac.georgia.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Hawaii Open Data Portal | https://data.hawaii.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Iowa Data Hub | https://data.iowa.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Idaho Open Data (GIS-focused) | https://gis.idaho.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Illinois Open Data Portal | https://data.illinois.gov | SOCRATA | https://data.illinois.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Indiana Data Hub | https://hub.mph.in.gov | CKAN | https://hub.mph.in.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Kansas Open Gov | https://kansasopengov.org | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Kentucky Open GIS Data | https://opengisdata.ky.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Massachusetts Data Hub | https://data.mass.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Maryland Open Data Portal | https://opendata.maryland.gov | SOCRATA | https://opendata.maryland.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Maine Open Data | https://www.maine.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Michigan Open Data Portal | https://data.michigan.gov | SOCRATA | https://data.michigan.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Minnesota Geospatial Commons / TransparencyMN | https://gisdata.mn.gov | CKAN | https://gisdata.mn.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Missouri Open Data Portal | https://data.mo.gov | SOCRATA | https://data.mo.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Mississippi GIS Open Data | https://opendata.gis.ms.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Montana Data Portal | https://data.mt.gov | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200 |
| NC LINC / NC OSBM Open Data | https://linc.osbm.nc.gov | OPENDATASOFT | https://linc.osbm.nc.gov/api/v2 | ✅ | matched OPENDATASOFT via /api/v2/catalog/datasets?limit=0 (HTTP 200) |
| North Dakota Open Data (fragmented) | https://www.nd.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Nebraska Open Data / StateSpending | https://www.nebraska.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| New Hampshire Geodata Portal | https://new-hampshire-geodata-portal-1-nhgranit.hub.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| NJ Open Data Center | https://data.nj.gov | SOCRATA | https://data.nj.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| New Mexico Open Data (fragmented — agency-level) | https://data-nmenv.opendata.arcgis.com | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Nevada Open Data Portal | https://open.nv.gov | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200 |
| New York State Open Data | https://data.ny.gov | SOCRATA | https://data.ny.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| DataOhio | https://data.ohio.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Oklahoma Open Data Portal | https://data.ok.gov | CKAN | https://data.ok.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Oregon Open Data Portal | https://data.oregon.gov | SOCRATA | https://data.oregon.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| PA Open Data Portal | https://data.pa.gov | SOCRATA | https://data.pa.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Rhode Island Open Data Portal | https://www.ri.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| South Carolina Data and Transparency | https://sc.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| TN DATA / Tennessee Geospatial Portal | https://geodata.tn.gov | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:500 |
| Texas Open Data Portal | https://data.texas.gov | SOCRATA | https://data.texas.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Utah Open Data Portal | https://opendata.utah.gov | SOCRATA | https://opendata.utah.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Virginia Open Data Portal | https://data.virginia.gov | CKAN | https://data.virginia.gov/api/3/action | ✅ | matched CKAN via /api/3/action/package_search?rows=0 (HTTP 200) |
| Vermont Open Geodata / Open Data | https://geodata.vermont.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| Washington State Open Data Portal | https://data.wa.gov | SOCRATA | https://data.wa.gov/api/catalog/v1 | ✅ | matched SOCRATA via /api/catalog/v1?limit=0 (HTTP 200) |
| Wisconsin Open Data (fragmented — no unified portal) | https://data.dhsgis.wi.gov | ARCGIS | hub.arcgis.com/api/search/v1 | /api/feed/dcat-us | ✅ | matched ARCGIS via /data.json (HTTP 200) |
| West Virginia Open Data (fragmented — GIS-focused) | https://data-wvdot.opendata.arcgis.com | UNKNOWN |  | ✅ | probes=ARCGIS:403,SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404; host hint ARCGIS unconfirmed by endpoint |
| Wyoming GeoHub | https://wyogeo.org | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Registry of Open Data on AWS | https://registry.opendata.aws | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Azure Open Datasets | https://learn.microsoft.com | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| data.world | https://developer.data.world | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| DataPortals.org | https://dataportals.org | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Google Cloud Public Datasets | https://cloud.google.com | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Google Dataset Search | https://datasetsearch.research.google.com | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Hugging Face Datasets Hub | https://huggingface.co | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:401,JUNAR:404,ARCGIS:404 |
| Kaggle Datasets | https://www.kaggle.com | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
| Open Data Inception | https://opendatainception.io | UNKNOWN |  | ✅ | probes=SOCRATA:200,CKAN:200,OPENDATASOFT:200,GEONODE:200,JUNAR:200,ARCGIS:200 |
| re3data.org (Registry of Research Data Repositories) | https://www.re3data.org | UNKNOWN |  | ✅ | probes=SOCRATA:404,CKAN:404,OPENDATASOFT:404,GEONODE:404,JUNAR:404,ARCGIS:404 |
