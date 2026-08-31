# Tap repair runbook — 2026-07-05

Generated from the tap-health audit (46 diagnostic agents, endpoints curl-verified where possible).

## 1. Auto-repour queue (19 taps) — run this

```bash
python onboard.py --queue outputs/tap_repairs_2026-07-05.json --yes
```
Resumes via `onboarding_log.json`; taps needing a key auto-skip as `needs_key` (no LLM burn) until the key is in `.env`.

### Quick wins — keyless one-line re-URLs (7)

| source_id | was | new data endpoint | probe |
|---|---|---|---|
| `fed_bjs_data` | wrong url html page | https://api.ojp.gov/bjsdataset/v1/gcuy-rt5g.csv | verified |
| `fed_bls_qcew` | wrong url html page | https://data.bls.gov/cew/data/files/2022/csv/2022_annual_singlefile.zip | verified |
| `fed_faa_data_portal` | wrong url html page | https://registry.faa.gov/database/ReleasableAircraft.zip | verified |
| `fed_sba_ppp` | wrong url html page | https://data.sba.gov/dataset/8aa276e2-6cab-4f86-aca4-a7dde42adf24/resource/c1275a03-c25c-488a-bd95-403c4b2fa036/download/public_150k_plus_240930.csv | verified |
| `fed_slavevoyages_transatlantic` | wrong url html page | https://legacy.slavevoyages.org/documents/download/tastdb-exp-2019.csv | verified |
| `intl_fao_faostat` | wrong url html page | https://bulks-faostat.fao.org/production/datasets_E.json | verified |
| `intl_ie_cro` | wrong url html page | https://opendata.cro.ie/dataset/bf6f837d-0946-4c14-9a99-82cd6980c121/resource/3fef41bc-b8f4-4b10-8434-ce51c29b1bba/download/companies.csv.zip | verified |

### Loader/parse regen — repours against the corrected endpoint (7)

| source_id | issue | data endpoint | probe |
|---|---|---|---|
| `fed_cdc_wonder` | wrong url html page | https://wonder.cdc.gov/controller/datarequest/D76 | unverified |
| `fed_cms_open_payments_2022` | loader code bug | https://download.cms.gov/openpayments/PGYR2022_P01232026_01102026/OP_DTL_GNRL_PGYR2022_P01232026_01102026.csv | verified |
| `fed_ed_fsa_datacenter` | wrong url html page | https://studentaid.gov/sites/default/files/fsawg/datacenter/library/PortfolioSummary.xls | verified |
| `fed_fjc_idb` | density parse junk | https://www.fjc.gov/sites/default/files/idb/textfiles/cv88on_0.zip | verified |
| `fed_hhs_taggs` | portal only no bulk | https://api.usaspending.gov/api/v2/search/spending_by_award/ | verified |
| `fed_nih_reporter` | wrong api method | https://api.reporter.nih.gov/v2/projects/search | verified |
| `intl_gleif` | loader code bug | https://leidata.gleif.org/api/v1/concatenated-files/lei2/latest?format=xml | verified |

> Notes: `fed_nih_reporter` endpoint is POST-only; `fed_cms_open_payments_2022` URL was already correct (a 7.4GB streaming bug — recodegen fixes it); `fed_fjc_idb` needs the tab-delimited parse; `fed_cdc_wonder` sits behind an Akamai WAF that may 403 server-side pulls; `fed_hhs_taggs` re-scopes to the USASpending API for the same HHS grant rows.

### Needs a free API key first (5) — add to `library-onboarding/.env`, then they repour

| source_id | env var to set | data endpoint |
|---|---|---|
| `fed_dol_wage_hour` | DOL_API_KEY (free @ dataportal.dol.gov/api-keys) | https://apiprod.dol.gov/v4/get/whd/enforcement/csv |
| `fed_fbi_cde` | FBI_CDE_API_KEY / api.data.gov key (free @ api.data.gov/signup) | https://api.usa.gov/crime/fbi/cde/ |
| `fed_fcc_broadband` | FCC_BROADBAND_API_KEY (username+hash @ broadbandmap.fcc.gov) | https://broadbandmap.fcc.gov/api/public/map/downloads/listAvailabilityData/{as_of_date} |
| `fed_fra_safety` | FRA key — SOAP service, may need a custom loader | https://safetydata.fra.dot.gov/MASTERWEBSERVICE/DatadownloadService.asmx?WSDL |
| `fed_usitc_dataweb` | USITC_DATAWEB_TOKEN (Bearer @ dataweb.usitc.gov/api-key) | https://datawebws.usitc.gov/dataweb/api/v2/report2/runReport |

## 2. Needs a custom loader (4) — NOT in the auto queue

| source_id | why | what to build |
|---|---|---|
| `fed_cms_hpt_mrf` | portal only no bulk | No re-URL fixes this: github.com/CMSgov is only the schema/validator/TXT-generator, not data. Quarantine the junk row and either build a distributed crawler tha |
| `fed_dea_arcos` | portal only no bulk | No machine-readable endpoint to re-URL to; the only downloads are PDFs (pattern https://www.deadiversion.usdoj.gov/arcos/retail_drug_summary/report_yr_YYYY.pdf, |
| `fed_doj_crt_cases` | portal only no bulk | No re-URL possible: no CSV/JSON/API exists. Rebuild as a Playwright scraper that drives the faceted search at justice.gov/crt/search-cases-and-matters (results  |
| `intl_ge_datagov` | wrong url html page | Re-point off opengovpartnership.org onto data.gov.ge's own catalog: harvest the dataset index (atom.xml feed, or scrape /Datasets) one row per dataset, and pull |

## 3. Retire / re-scope (2) — no public data

| source_id | why |
|---|---|
| `fed_fincen_boi` | Retire/quarantine this tap: there is no public BOI data feed. FinCEN's BOI is confidential under the Corporate Transparency Act, stored in the nonpublic BOSS system; the only machi |
| `intl_austlii` | Retire intl_austlii as a direct tap — AustLII's Usage Policy prohibits scraping/API/bulk access and there is no official machine-readable endpoint. Re-scope to a real dataset: onbo |

## 4. Already fixed in code

- **Pipeline gates hardened** in `library-onboarding/ingest.py`: `_reject_html` now catches HTML in any column/cell (not just single-column), and snapshot loads demote a lone scraped row (`DENSITY_MIN_ROWS`). 100 tests pass. No new tap can silently land HTML junk as `success`.

## 5. Separate workstream — 8 marts hiding real data

Landing tables are full but dbt models froze the mart at 1–3 rows (e.g. `fed_slavevoyages_intraamerican` 11,521→1; staging selects `VOYAGE_ID`/`DOCTYPE_HTML` columns absent from the real landing). Fix = regen the staging models against the actual landing schema, then re-run dbt. See the audit dashboard.
